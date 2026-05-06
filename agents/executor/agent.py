import os
from typing import Any
from neo4j import GraphDatabase

class QueryExecutionAgent:
    def __init__(self):
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        auth = (os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password"))
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def run(self, keywords: list[str]) -> dict[str, Any]:
        if not keywords: return {"rows": [], "error": None}
        
        # Mixed Search: Fuzzy for short words, exact/boosted for key terms
        clauses = []
        for k in keywords:
            if len(k) < 4:
                clauses.append(f"{k}~") # Fuzzy for short
            else:
                clauses.append(f"\"{k}\"^2") # Boosted exact for long
                clauses.append(f"{k}~") # Also fuzzy just in case
        
        q = " OR ".join(clauses)
        
        results = []
        try:
            with self.driver.session() as session:
                res = session.run("""
                    CALL db.index.fulltext.queryNodes("article_content_idx", $q) 
                    YIELD node, score 
                    RETURN node.number as num, node.content as content, node.reg_name as reg, score 
                    ORDER BY score DESC LIMIT 15
                """, q=q)
                for r in res:
                    results.append({"type": "article", "id": r["num"], "text": r["content"], "reg": r["reg"], "score": r["score"]})
                
                res_rule = session.run("""
                    CALL db.index.fulltext.queryNodes("rule_idx", $q) 
                    YIELD node, score 
                    RETURN node.rule_id as id, node.action as act, node.result as res, node.reg_name as reg, score 
                    ORDER BY score DESC LIMIT 10
                """, q=q)
                for r in res_rule:
                    results.append({"type": "rule", "id": r["id"], "text": f"{r['act']} -> {r['res']}", "reg": r["reg"], "score": r["score"]})
                    
            return {"rows": sorted(results, key=lambda x: x["score"], reverse=True), "error": None}
        except Exception as e:
            return {"rows": [], "error": str(e)}
