class QueryRepairAgent:
    def run(self, keywords: list[str]) -> list[str]:
        # Minimalist repair: just add the core institution context
        return list(set(keywords + ["National", "Central", "University", "Regulations"]))
