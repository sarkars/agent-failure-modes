# Goal: Context Lifecycle

Manage the lifecycle of context passed to LLMs - from assembly through truncation to expiration. Context lifecycle failures cause information loss, degraded responses, and unpredictable behavior as conversations grow.

## Business Context

- Context windows have hard limits (4K to 200K tokens)
- Truncation strategies determine what information survives
- Priority-based selection affects response quality
- Long conversations require active context management
- RAG, tools, and system prompts compete for context space

## Failure Patterns

| Failure Pattern | Frequency | Impact |
|-----------------|-----------|--------|
| [Truncation Information Loss](failures/truncation-information-loss.md) | Very Common | High |
| [Context Priority Inversion](failures/context-priority-inversion.md) | Common | High |
| [System Prompt Displacement](failures/system-prompt-displacement.md) | Common | Critical |
| [Stale Context Retention](failures/stale-context-retention.md) | Common | Medium |
| [Context Assembly Race](failures/context-assembly-race.md) | Occasional | High |
| [Window Boundary Artifacts](failures/window-boundary-artifacts.md) | Common | Medium |

## Key Statistics

| Finding | Source |
|---------|--------|
| "Lost in the middle" - 30% accuracy drop | Research |
| System prompt truncation causes jailbreaks | Security Research |
| Context overflow is top-3 agent failure mode | AWS Analysis |
| Optimal context often 4-16K, not max window | Research |

## Key Metrics

- Context utilization rate
- Truncation frequency
- Information retention score
- System prompt integrity
- Context assembly latency
