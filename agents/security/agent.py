class SecurityAgent:
    def run(self, question: str, intent_type: str) -> dict[str, str]:
        # Malicious keywords list
        blocked = ["delete", "drop", "merge", "create", "set ", "remove", "ignore", "bypass", "system prompt", "admin", "credential", "password", "database", "shutdown", "grant"]
        q_low = question.lower()
        
        # Only reject if it's a real attack or NLU confirmed unsafe
        if any(p in q_low for p in blocked) or intent_type == "unsafe":
            return {"decision": "REJECT", "reason": "Security policy violation."}
        return {"decision": "ALLOW", "reason": "Passed."}
