# Query Executor Agent
## Responsibilities
- Interface with the Neo4j Knowledge Graph.
- Perform high-performance full-text search across Articles and Rules.

## Configuration
- Utilizes the `article_content_idx` and `rule_idx` full-text indexes.
- Returns ranked results based on Lucene scoring.
- Aggregates evidence from multiple regulatory documents.
