from typing import Any

class QueryPlannerAgent:
    def run(self, keywords: list[str], aspect: str) -> dict[str, Any]:
        synonyms = {
            "fee": ["fee", "cost", "NTD", "200", "money", "payment", "reissue"],
            "replacing": ["reissue", "replace", "loss", "lost", "missing"],
            "credits": ["credits", "course", "graduation", "units", "128", "total"],
            "expelled": ["dismissed", "withdraw", "terminated", "dismissal", "1/2", "grades"],
            "penalty": ["points", "deduction", "zero", "disciplinary", "punish", "violations"],
            "late": ["minutes", "time", "barred", "delay", "20"],
            "exam": ["test", "examination", "midterm", "final", "barred", "40"],
            "duration": ["years", "semesters", "duration", "study", "extension", "4", "2"]
        }
        expanded = set(keywords)
        for k in keywords:
            k_low = k.lower()
            for key, syns in synonyms.items():
                if k_low == key or k_low in syns:
                    expanded.update(syns)
        
        # Add context keywords for specific aspects
        if aspect == "credits": expanded.update(["graduation", "minimum"])
        if aspect == "duration": expanded.update(["study", "maximum"])
        
        return {"keywords": list(expanded), "aspect": aspect}
