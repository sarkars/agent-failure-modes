# Capability Patterns

Failure patterns driven by **what the system does** - the capabilities that introduce specific failure modes.

## Categories

| Capability | Description | Goals | Patterns |
|------------|-------------|-------|----------|
| [Workflow](workflow/) | Goal understanding, task planning | 2 | 20 |
| [Action](action/) | Action execution in external systems | 1 | 11 |
| [Voice](voice/) | Speech recognition and synthesis | 4 | 26 |
| [Domain Expertise](domain-expertise/) | Domain-specific judgment | 1 | 10 |

**Total: 67 patterns across 8 goals**

## Why "Capabilities"?

These failures come from **how the system is designed**:

- **Workflow**: Planning failures (bad decomposition, missing prerequisites)
- **Action**: Execution failures (wrong target, no rollback)
- **Voice**: Audio/speech failures (accent bias, interruption handling)
- **Domain Expertise**: Judgment failures (regulatory misses)

## Cross-References

- [Core](../core/) - Cross-cutting patterns (apply to all)
- [Domains](../domains/) - Use-case specific patterns
