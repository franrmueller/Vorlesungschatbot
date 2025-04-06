# app/db/connect.py
from neo4j import GraphDatabase, basic_auth
import os
import logging

logger = logging.getLogger(__name__)

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "your_neo4j_password") # Use secure handling

_driver = None

def get_driver():
    """Initializes and returns the Neo4j driver instance."""
    global _driver
    if _driver is None:
        logger.info("Initializing Neo4j driver...")
        try:
            _driver = GraphDatabase.driver(
                NEO4J_URI,
                auth=basic_auth(NEO4J_USERNAME, NEO4J_PASSWORD)
            )
            _driver.verify_connectivity()
            logger.info("Neo4j driver initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Neo4j driver: {e}")
            raise RuntimeError(f"Failed to initialize Neo4j driver: {e}") from e
    return _driver

def close_driver():
    """Closes the Neo4j driver connection."""
    global _driver
    if _driver is not None:
        logger.info("Closing Neo4j driver.")
        _driver.close()
        _driver = None

# Optional: Add FastAPI lifespan events in main.py to call close_driver on shutdown