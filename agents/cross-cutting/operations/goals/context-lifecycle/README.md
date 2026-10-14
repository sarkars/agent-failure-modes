# Context Lifecycle Failures in AI Agents: Truncation, Stale Context, and Prompt Displacement

**Context lifecycle failures happen when an agent assembles, truncates, or refreshes its context window badly: critical instructions get cut, old facts outlive corrections, or partial content confuses the model.** The six patterns here cover what goes in, what gets dropped, and what stays too long.

## Key Takeaways

- Truncation that drops the oldest content first can remove user preferences, key facts, or even parts of the system prompt.
- Assembly order and priority matter: a large tool output can displace the instructions the agent depends on.
- Context can also be wrong rather than missing: outdated information kept while corrections are discarded.
- Cutting at an exact token limit can leave broken JSON or half-finished instructions.

## Patterns

| Pattern | What goes wrong |
|---|---|
| [Context Assembly Race](failures/context-assembly-race.md) | Race Conditions During Context Assembly Cause Inconsistent State |
| [Context Priority Inversion](failures/context-priority-inversion.md) | Low-Priority Content Displaces High-Priority Content |
| [Stale Context Retention](failures/stale-context-retention.md) | Outdated Information Kept While Current Information Discarded |
| [System Prompt Displacement](failures/system-prompt-displacement.md) | System Prompt Gets Truncated or Overwritten |
| [Truncation Information Loss](failures/truncation-information-loss.md) | Critical Information Lost When Context is Truncated |
| [Window Boundary Artifacts](failures/window-boundary-artifacts.md) | Content Cut at Token Boundaries Creates Artifacts |

**Total: 6 patterns**

## How These Patterns Group

- **Assembly:** [Context Assembly Race](failures/context-assembly-race.md), [Context Priority Inversion](failures/context-priority-inversion.md)
- **Truncation:** [Truncation Information Loss](failures/truncation-information-loss.md), [System Prompt Displacement](failures/system-prompt-displacement.md), [Window Boundary Artifacts](failures/window-boundary-artifacts.md)
- **Freshness:** [Stale Context Retention](failures/stale-context-retention.md)

## When This Matters

- Sessions run long enough to hit the context limit
- Context is built from several sources: history, retrieved documents, tool output, memory
- Safety rules or behavior depend on the system prompt staying intact

## Frequently Asked Questions

### Why does my agent forget instructions in a long conversation?

Usually truncation. If the oldest content is dropped first, early instructions and preferences go with it. See [truncation information loss](failures/truncation-information-loss.md) and [system prompt displacement](failures/system-prompt-displacement.md).

### Why does my agent keep using information the user already corrected?

Truncation by age can keep the old version longer than the correction. See [stale context retention](failures/stale-context-retention.md).

### How is context lifecycle different from memory management?

Context lifecycle is about what is in the window for the current call. [Memory management](../memory-management/) is about what is stored and retrieved across calls.

## Related

- [All operations goals](../)
- [Operations overview](../../)
