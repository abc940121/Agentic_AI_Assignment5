from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()
uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
auth = (os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))
driver = GraphDatabase.driver(uri, auth=auth)

with driver.session() as session:
    print("--- Searching for 'EasyCard' ---")
    res = session.run("MATCH (a:Article) WHERE a.content CONTAINS 'EasyCard' RETURN a.number, a.content")
    for r in res:
        print(f"Article {r['a.number']}: {r['a.content'][:100]}...")

    print("\n--- Searching for '200' ---")
    res = session.run("MATCH (a:Article) WHERE a.content CONTAINS '200' RETURN a.number, a.content")
    for r in res:
        print(f"Article {r['a.number']}: {r['a.content'][:100]}...")
driver.close()
