# Capability Agents

Agents where the **design and capability** introduces specific failure modes. These patterns emerge from how the agent is architected rather than its domain.

## Agents

| Agent | Description | Goals | Patterns |
|-------|-------------|-------|----------|
| [Workflow Agent](workflow-agent/) | Goal understanding, task planning, sequencing | 2 | 20 |
| [Action Agent](action-agent/) | Action execution in external systems | 1 | 11 |
| [Voice Agent](voice-agent/) | Speech recognition, synthesis, conversation | 4 | 26 |
| [Domain Expert Agent](domain-expert-agent/) | Domain-specific judgment and decisions | 1 | 10 |

**Total: 67 patterns across 8 goals**

## Why "Capability Agents"?

These agents share a common trait: their failure modes come from **what they do**, not **where they're used**:

- **Workflow Agent**: Planning and sequencing failures (bad decomposition, missing prerequisites)
- **Action Agent**: Execution failures (wrong target, unauthorized actions, no rollback)
- **Voice Agent**: Audio/speech failures (mishearing, accent bias, interruption handling)
- **Domain Expert Agent**: Judgment failures (regulatory misses, risk misclassification)

## How to Use

1. **Identify capabilities in your agent** - Does it plan? Execute actions? Handle voice? Make domain judgments?
2. **Apply relevant patterns** - Each capability brings specific failure modes
3. **Layer with base-agent** - These complement cross-cutting security/accuracy/operations patterns
4. **Add domain-specific patterns** - If using RAG, OCR, etc., add those patterns too

## Cross-References

- [Base Agent](../base-agent/) - Cross-cutting patterns (apply to all)
- [Domain Agents](../domain-agents/) - Use-case specific agents (RAG, OCR, customer service)
