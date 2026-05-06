class ExplanationAgent:
    def run(self, diagnosis: str, repair_attempted: bool, answer: str) -> str:
        return f"NCU-Agent-System [Status: {diagnosis} | Repair: {repair_attempted}]: {answer}"
