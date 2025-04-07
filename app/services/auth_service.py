# app/services/auth_service.py
from neo4j import Driver
from app.db.connect import get_driver
from ..models import user as user_models
from ..core import security
import logging
import uuid

logger = logging.getLogger(__name__)

async def get_user_by_username(username: str) -> user_models.UserInDB | None:
    """Fetches a user by username from Neo4j."""
    driver: Driver = get_driver()
    try:
        records, _, _ = await driver.execute_query(
            "MATCH (u:User {username: $username}) RETURN u",
            username=username,
            database_="neo4j" # Specify database if not default
        )
        if records and records[0] and records[0].data()['u']:
             user_data = records[0].data()['u']
             # Ensure role is present, default if necessary (shouldn't happen if created correctly)
             if 'role' not in user_data:
                 user_data['role'] = 'STUDENT' # Or handle error
             # Add uuid if missing (shouldn't happen)
             if 'uuid' not in user_data:
                  user_data['uuid'] = str(uuid.uuid4())
             return user_models.UserInDB(**user_data)
        return None
    except Exception as e:
        logger.error(f"Error fetching user {username}: {e}")
        return None

async def create_user(user_data: user_models.UserCreate) -> user_models.User | None:
    """Creates a new user node in Neo4j."""
    # Check if user already exists
    existing_user = await get_user_by_username(user_data.username)
    if existing_user:
        logger.warning(f"Username {user_data.username} already registered.")
        return None

    driver: Driver = get_driver()
    hashed_password = security.get_password_hash(user_data.password)
    user_uuid = str(uuid.uuid4())
    # Default role is STUDENT if not provided, but model sets default too
    role = user_data.role if user_data.role else "STUDENT"

    try:
        records, _, _ = await driver.execute_query(
            """
            CREATE (u:User {
                uuid: $uuid,
                username: $username,
                hashed_password: $hashed_password,
                name: $name,
                role: $role,
                created_at: datetime()
            })
            RETURN u
            """,
            uuid=user_uuid,
            username=user_data.username,
            hashed_password=hashed_password,
            name=user_data.name,
            role=role,
            database_="neo4j"
        )
        if records and records[0] and records[0].data()['u']:
            new_user_data = records[0].data()['u']
            # Return the User model (without hash)
            return user_models.User(**new_user_data)
        return None
    except Exception as e:
        logger.error(f"Error creating user {user_data.username}: {e}")
        # Consider specific Neo4j constraint violation errors
        return None


async def authenticate_user(username: str, password: str) -> user_models.UserInDB | None:
    """Authenticates a user by checking username and password."""
    user = await get_user_by_username(username)
    if not user:
        logger.info(f"Authentication failed: User '{username}' not found.")
        return None
    if not security.verify_password(password, user.hashed_password):
        logger.info(f"Authentication failed: Incorrect password for user '{username}'.")
        return None
    logger.info(f"User '{username}' authenticated successfully.")
    return user