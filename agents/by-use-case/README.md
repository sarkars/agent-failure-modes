# Patterns by Use Case

Failure patterns specific to **where the system is used** - the use case or domain.

## Categories

| Use Case | Description | Goals | Patterns |
|----------|-------------|-------|----------|
| [Knowledge Retrieval](knowledge-retrieval/) | RAG and retrieval-augmented generation | 5 | 52 |
| [Document Processing](document-processing/) | OCR and document text extraction | 6 | 48 |
| [Customer Service](customer-service/) | Customer conversations | 1 | 11 |
| [Multi-Agent Systems](multi-agent-systems/) | Agent coordination | 1 | 15 |
| [Code](code/) | Code generation and review | - | Planned |
| [Data Extraction](data-extraction/) | Structured data extraction | - | Planned |

**Total: 126 patterns across 13 goals**

## Why "By Use Case"?

These failures come from **where the system operates**:

- **Knowledge Retrieval**: Retrieval and synthesis failures
- **Document Processing**: OCR and extraction failures
- **Customer Service**: Conversation handling failures
- **Multi-Agent Systems**: Coordination failures

## Cross-References

- [Cross-Cutting](../cross-cutting/) - Patterns that apply to all systems
- [By Capability](../by-capability/) - Design-driven patterns
