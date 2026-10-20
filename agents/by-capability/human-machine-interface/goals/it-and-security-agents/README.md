# IT and Security Agents: Goal, Metrics, and Patterns

> **Goal:** IT and security agents act within verified authority, explain what they close, and never contain or reset without the right approval.

## Why this family exists
IT and security assistants triage alerts, follow runbooks, and sometimes act on accounts and devices. The analyst usually sees only the status they set. A real alert closed as "false positive" with no stated reason, an account disabled with no sign-off, or an indicator that does not exist can all look like routine work. This family covers the one written so far. The rest are catalogued in the [agent types roadmap](../../roadmap/agent-types.md); three of them are already covered by a chat example on an existing pattern page.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Closures with a stated reason | 100% | [true alerts closed as false positives](failures/true-alerts-closed-as-false-positives.md) |

## Patterns
| Pattern | One line |
|---|---|
| [True alerts closed as false positives](failures/true-alerts-closed-as-false-positives.md) | A triage assistant dismisses a real threat with no reason; state the evidence behind every closure, keep high-risk alerts with a person, audit a sample |

## Chat examples on existing pages
- Containment without human sign-off: [missing approval gates](../../../../cross-cutting/operations/goals/human-oversight-reliability/failures/missing-approval-gates.md)
- Outdated runbook followed with confidence: [policy version mismatch](../../../../cross-cutting/governance/goals/approval-workflows/failures/policy-version-mismatch.md)
- Fabricated indicators or vulnerability details: [fabricated citations](../../../knowledge-retrieval/goals/citation-accuracy/failures/fabricated-citations.md)

## Planned (not yet written)
None listed here. See the [roadmap](../../roadmap/index.md) for the rest.

## Related
- [Errors and recovery](../errors-and-recovery/README.md)
- [Research and data agents](../research-and-data-agents/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
