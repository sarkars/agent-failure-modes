# Domain Agents

Domain-specific AI agents with specialized failure patterns.

## Agents

| Agent | Description | Goals | Patterns |
|-------|-------------|-------|----------|
| [Action Agent](action-agent/) | Action execution in external systems | 1 | 11 |
| [Code Agent](code-agent/) | Code generation, review, and modification | - | Planned |
| [Customer Service Agent](customer-service-agent/) | Customer conversation and support | 1 | 11 |
| [Data Extraction Agent](data-extraction-agent/) | Structured data extraction | - | Planned |
| [Domain Expert Agent](domain-agent/) | Domain-specific judgment and decisions | 1 | 10 |
| [Multi-Agent System](multi-agent/) | Agent coordination and orchestration | 1 | 15 |
| [OCR Agent](ocr-agent/) | Document text extraction and processing | 6 | 48 |
| [RAG Agent](rag-agent/) | Retrieval-augmented generation | 5 | 52 |
| [Voice Agent](voice-agent/) | Speech recognition, synthesis, and conversation | 4 | 26 |
| [Workflow Agent](workflow-agent/) | Goal understanding, task planning, and sequencing | 2 | 20 |

**Total: 193 patterns across 21 goals**

## How to Use

1. **Identify your agent type** - Find the category that matches your use case
2. **Apply base-agent patterns first** - Cross-cutting patterns apply to all agents
3. **Add domain-specific patterns** - These complement the base patterns
4. **Monitor and iterate** - Track domain-specific metrics

## Cross-References

See [Base Agent](../base-agent/) for cross-cutting patterns that apply to all agents.
