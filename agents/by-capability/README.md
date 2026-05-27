# Patterns by Capability

Failure patterns driven by **what the system does** - the capabilities that introduce specific failure modes.

## Categories

| Capability | Description | Goals | Patterns |
|------------|-------------|-------|----------|
| [Task Planning](task-planning/) | Goal understanding, task planning | 2 | 20 |
| [External Actions](external-actions/) | Action execution in external systems | 1 | 11 |
| [Speech and Audio](speech-and-audio/) | Speech recognition and synthesis | 4 | 66 |
| [Domain Expertise](domain-expertise/) | Domain-specific judgment | 1 | 10 |
| [Document Processing](document-processing/) | OCR and document text extraction | 6 | 48 |
| [Knowledge Retrieval](knowledge-retrieval/) | RAG and retrieval-augmented generation | 5 | 52 |
| [Multi-Agent Systems](multi-agent-systems/) | Agent coordination and orchestration | 1 | 15 |

**Total: 222 patterns across 20 goals**

## Why "By Capability"?

These failures come from **how the system is designed**:

- **Task Planning**: Planning failures (bad decomposition, missing prerequisites)
- **External Actions**: Execution failures (wrong target, no rollback)
- **Speech and Audio**: Audio/speech failures (accent bias, interruption handling)
- **Domain Expertise**: Judgment failures (regulatory misses)
- **Document Processing**: OCR and extraction failures (character confusion, layout errors)
- **Knowledge Retrieval**: Retrieval failures (context precision, answer relevancy)
- **Multi-Agent Systems**: Coordination failures (agent misalignment, communication breakdowns)

## Cross-References

- [Cross-Cutting](../cross-cutting/) - Patterns that apply to all systems
- [By Use Case](../by-use-case/) - Domain-specific patterns
