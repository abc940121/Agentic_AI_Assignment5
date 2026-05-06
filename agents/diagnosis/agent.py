from typing import Any

class DiagnosisAgent:
    def run(self, execution: dict[str, Any]) -> dict[str, str]:
        if execution.get("error"): return {"label": "QUERY_ERROR", "reason": execution["error"]}
        # Threshold 0.25 to ensure quality
        if not execution.get("rows") or execution["rows"][0]["score"] < 0.25:
            return {"label": "NO_DATA", "reason": "Low confidence."}
        return {"label": "SUCCESS", "reason": "Success."}
