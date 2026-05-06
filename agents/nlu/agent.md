# NLU Agent
## Responsibilities
- Parse the user question into structured intent data.
- Extract key entities for knowledge graph retrieval.
- Classify the question type (normal, unsafe, failure) to guide downstream agents.

## Methodology
- Uses **Qwen2.5-3B** with a specialized prompt to extract nouns and aspect categories.
- Distinguishes between regulatory inquiries about violations and actual malicious system-level queries.
