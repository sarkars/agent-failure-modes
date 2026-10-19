# End State: A Self-Correcting Agent, and the Base Level to Start From

> **Goal.** An agent that keeps learning and improves, built on today's knowledge. The first deliverable is a **base level** that applies what this library already knows, so the learning loop has something to learn from. Read the [gap analysis](gap-analysis.md) first: the loop itself is published by others, so the aim here is a base agent and a gated policy tied to named failure patterns.

## Levels
| Level | What it is | What a scheduled run can produce | What needs a person or a runtime |
|---|---|---|---|
| L0 | **Base spec.** The behaviors the agent must show and avoid, taken from the flagship patterns' fixes | A spec document and a table mapping each behavior to a pattern and a test | Review |
| L1 | **Base agent.** A minimal customer-support agent: prompt, tool contracts, handoff and refusal rules, test cases | Prompt text, tool schemas, and test cases, all labeled **untested** | Running it against a model; recording results |
| L2 | **Observed.** Traces tagged with pattern IDs, failure rate per pattern | A tagging schema and a dashboard spec | Real traces, a runtime, a tracing tool |
| L3 | **Proposes fixes.** The agent drafts changes (prompt edits, new test cases, memory entries) and a person reviews them | A candidate-registry format and a review checklist | Running the agent; human review |
| L4 | **Gated self-update.** Low-risk changes apply automatically after passing held-out regression tests; everything else waits for a person | A policy document and the gate definition | A runtime, the held-out test set, monitoring |

## Rules for the learning loop (to be checked against opened sources)
1. **The agent proposes; a separate layer decides.** Evaluation and approval sit outside the agent's write access.
2. **Never self-modifiable:** permissions, guardrails, the graders and held-out tests, the approval rules, and the logging. Sources I read through summaries point the same way (see the gap analysis); the scheduled gap analysis must open them.
3. **Changes are versioned candidates,** not in-place edits: candidate, then active, with quarantine and rollback.
4. **Held-out evaluation.** Tests used to accept a change must be hidden from the proposing process, since optimizing against visible graders invites overfitting and gaming.
5. **Failure IDs are the vocabulary.** Every trace flagged, every test added, and every change links to a pattern ID or a new one proposed.
6. **High-stakes classes never auto-apply:** crisis signals, children, money, legal, and identity.
7. **Report the loop's own health:** regression escapes, changes rejected, changes rolled back.

## What a scheduled run cannot do
It cannot run an agent against a model, collect real traces, or measure improvement. Any claim that the agent "improves" needs a human-run evaluation recorded with model, version, and date. Until then, L1 to L4 are designs.

## Related
- [Gap analysis](gap-analysis.md)
- [L1 harness decision record](l1-harness-decision.md)
- [L0 base spec (draft)](l0-base-spec.md)
- [Content program](content-program.md)
- [Execution plan](execution-plan.md)
