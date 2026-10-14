# External Actions AI Agent Failures by Goal: 11 Patterns, Causes, and Fixes

**External Actions AI agents fail in 1 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 11 documented patterns across 1 goal; the most documented is [Action Execution](action-execution/) with 11.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## External Actions Goals

| Goal | When it fails | Patterns |
|---|---|---|
| Action Execution | When an agent's decision to act is correct but the act itself — its authorization, target, timing, or mechanics — is not | 11 |

**Total: 11 patterns**

## Frequently Asked Questions

### What's the difference between unauthorized-action and policy-violating-action?

Unauthorized-action means the agent lacks permission for the action or target resource at all — an identity/capability failure caught by a capability token or namespace check. See Action Execution.

## Related

- [External Actions overview](../)
- [All agent failure patterns](../../../)
