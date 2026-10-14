# Task Planning AI Agent Failures by Goal: 20 Patterns, Causes, and Fixes

**Task Planning AI agents fail in 2 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 20 documented patterns across 2 goals; the most documented is [Goal Understanding](goal-understanding/) with 10.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## Task Planning Goals

| Goal | When it fails | Patterns |
|---|---|---|
| Goal Understanding | When an agent optimizes for the wrong version of what it was asked to do | 10 |
| [Planning](planning/) | When the plan an agent builds — or its absence — doesn't match what the task actually requires | 10 |

**Total: 20 patterns**

## Frequently Asked Questions

### What's the difference between goal drift and scope creep?

Goal-drift-across-turns is the original objective itself eroding or shifting over a long session — later actions no longer match the initial goal statement. See Goal Understanding.

### What's the difference between no-plan-before-action and bad-task-decomposition?

No-plan-before-action is skipping planning altogether — the agent jumps straight into tool calls on a complex task with no decomposition step at all. See Planning.

## Related

- [Task Planning overview](../)
- [All agent failure patterns](../../../)
