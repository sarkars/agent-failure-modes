# Domain Patterns

Failure patterns specific to **where the system is used** - the use case or domain.

## Categories

| Domain | Description | Goals | Patterns |
|--------|-------------|-------|----------|
| [RAG](rag/) | Retrieval-augmented generation | 5 | 52 |
| [OCR](ocr/) | Document text extraction | 6 | 48 |
| [Customer Service](customer-service/) | Customer conversations | 1 | 11 |
| [Multi-Agent Systems](multi-agent-systems/) | Agent coordination | 1 | 15 |
| [Code](code/) | Code generation and review | - | Planned |
| [Data Extraction](data-extraction/) | Structured data extraction | - | Planned |

**Total: 126 patterns across 13 goals**

## Why "Domains"?

These failures come from **where the system operates**:

- **RAG**: Knowledge retrieval and synthesis failures
- **OCR**: Document processing failures
- **Customer Service**: Conversation handling failures
- **Multi-Agent Systems**: Coordination failures

## Cross-References

- [Core](../core/) - Cross-cutting patterns (apply to all)
- [Capabilities](../capabilities/) - Design-driven patterns
