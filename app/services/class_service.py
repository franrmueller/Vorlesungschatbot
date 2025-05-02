# app/services/class_service.py
# Holt alle Kurse, in die der Student eingeschrieben ist
# Gibt die Werte id, name, code zurück
from app.db.connect import get_driver

def get_enrolled_classes(username: str) -> list[dict]:
    driver = get_driver()
    query = """
    MATCH (u:User {username: $username})-[:ENROLLED_IN]->(c:Class)
    RETURN c.uuid AS id, c.name AS name, c.enrollment_code AS code
    """
    with driver.session() as session:
        result = session.run(query, username=username)
        return [record.data() for record in result]
