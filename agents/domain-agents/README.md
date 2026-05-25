# Domain Agents

Agents defined by their **use case or domain** - what problem they solve, not how they're built.

## Agents

| Agent | Description | Goals | Patterns |
|-------|-------------|-------|----------|
| [RAG Agent](rag-agent/) | Retrieval-augmented generation | 5 | 52 |
| [OCR Agent](ocr-agent/) | Document text extraction and processing | 6 | 48 |
| [Customer Service Agent](customer-service-agent/) | Customer conversation and support | 1 | 11 |
| [Multi-Agent System](multi-agent/) | Agent coordination and orchestration | 1 | 15 |
| [Code Agent](code-agent/) | Code generation, review, modification | - | Planned |
| [Data Extraction Agent](data-extraction-agent/) | Structured data extraction | - | Planned |

**Total: 126 patterns across 13 goals**

## Why "Domain Agents"?

These agents are defined by **where they're used**, not just what they do:

- **RAG Agent**: Knowledge retrieval and synthesis for any domain
- **OCR Agent**: Document processing across industries
- **Customer Service Agent**: Support interactions across products
- **Multi-Agent System**: Coordinated agent workflows

## How to Use

1. **Identify your domain** - RAG? OCR? Customer service?
2. **Apply base-agent patterns first** - Cross-cutting patterns apply to all
3. **Add capability patterns** - If your agent plans, executes actions, handles voice
4. **Layer domain-specific patterns** - These address use-case specific failures

## Cross-References

- [Base Agent](../base-agent/) - Cross-cutting patterns (apply to all)
- [Capability Agents](../capability-agents/) - Design/capability-based patterns
