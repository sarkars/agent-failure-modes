# Patterns by Use Case

Failure patterns specific to **where the system is used** - the use case or domain.

## Categories

| Use Case | Description | Goals | Patterns |
|----------|-------------|-------|----------|
| [Customer Service](customer-service/) | Customer conversations | 1 | 11 |
| [Mortgage Documents](mortgage-documents/) | Mortgage document OCR, fraud, AI reliability | 6 | 44 |
| [Code](code/) | Code generation and review | - | Planned |
| [Data Extraction](data-extraction/) | Structured data extraction | - | Planned |

**Total: 55 patterns across 7 goals**

## Why "By Use Case"?

These failures come from **where the system operates**:

- **Customer Service**: Conversation handling failures, escalation timing, sentiment misreads
- **Mortgage Documents**: Compliance validation, fraud detection, income calculation, TRID timing

## Cross-References

- [Cross-Cutting](../cross-cutting/) - Patterns that apply to all systems
- [By Capability](../by-capability/) - Design-driven patterns (includes document processing, knowledge retrieval, multi-agent systems)
