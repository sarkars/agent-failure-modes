# What Are the Most Common Tool Reliability Failures in AI Agents?

**Tool reliability fails when tools return stale data, when tool outputs are misinterpreted, when tools silently fail without error signals, when external system failures cascade into agent failures, or when tool API versions change without backward compatibility.** The 19 reliability patterns documented here cover the full tool-use lifecycle — from selecting the right tool through invoking it correctly, handling output, and recovering from failures. Tool reliability is the foundation of agent reliability: unreliable tools cause unreliable agents, and failures in tool output parsing or handling propagate silently through agent reasoning.

## Key Takeaways

- 19 patterns span tool selection, invocation, output handling, failure recovery, and system compatibility.
- Silent Failures and Error Information Leakage are most severe: silent failures leave agents unaware anything went wrong, error leakage exposes sensitive information.
- Output Misinterpretation and Parameter Mismatches are second-order: agents receive correct data but interpret it wrong, or pass parameters that don't match tool expectations.
- Tool Version Incompatibility and Schema Drift are architectural failures: tool APIs change without notice, breaking agent assumptions built during testing.

## Scope

- **Tool Selection and Capability** — [Wrong Tool Selection](failures/wrong-tool-selection.md), [Tool Capability Overestimation](failures/tool-capability-overestimation.md), [Vague Tool Descriptions](failures/vague-tool-descriptions.md).
- **Invocation Correctness** — [Missing Parameters](failures/missing-parameters.md), [Parameter Mismatches](failures/parameter-mismatches.md).
- **Output Handling** — [Output Misinterpretation](failures/output-misinterpretation.md), [Output Processing Errors](failures/output-processing-errors.md), [Silent Type Coercion](failures/silent-type-coercion.md).
- **Failure Modes** — [Silent Failures](failures/silent-failures.md), [Action-Completion Claimed Without Status Check](failures/action-completion-claimed-without-status-check.md), [Stale Tool Confirmation After Revision](failures/stale-tool-confirmation-after-revision.md).
- **System Integration** — [External System Failures](failures/external-system-failures.md), [Tool Availability Assumptions](failures/tool-availability-assumptions.md), [Blocking Tool Operations](failures/blocking-tool-operations.md).
- **API Compatibility** — [Tool Version Incompatibility](failures/tool-version-incompatibility.md), [Schema Drift](failures/schema-drift.md).
- **State and Navigation** — [State Space Navigation](failures/state-space-navigation.md), [Sequencing Errors](failures/sequencing-errors.md), [Error Information Leakage](failures/error-information-leakage.md).

## When Tool Reliability Matters

- An agent depends on tool correctness and availability; unreliable tools cascade into unreliable agents.
- Multiple tools must be composed (one tool's output feeds another tool's input); failures compound.
- Tool APIs evolve; backward compatibility cannot be assumed.

## Cross-Pattern Insight

The 19 patterns describe systems where tool reliability is assumed: tools are assumed to always be available, to return correct data, to be backward-compatible, and to fail loudly (with clear error signals). When any assumption breaks, agent behavior becomes unpredictable. The mitigation that recurs across all patterns is explicit validation: validate tool responses against expected schemas, implement explicit error handling for known failure modes, test tool composition under realistic conditions, and maintain tool health metrics (availability, error rate, latency) to catch reliability degradation early.

## Frequently Asked Questions

### How do you prevent silent tool failures?
Per [Silent Failures](failures/silent-failures.md), tools should return explicit success/failure signals, and agents should check those signals before proceeding. Never assume a tool succeeded because it didn't return an error — verify success explicitly.

### What should an agent do when tool API changes?
Per [Tool Version Incompatibility](failures/tool-version-incompatibility.md) and [Schema Drift](failures/schema-drift.md), maintain tool API contracts and validate against them at deployment time. When APIs change, update contracts and agents together, never one without the other.

### How do you handle tool outputs that need complex parsing?
Per [Output Misinterpretation](failures/output-misinterpretation.md) and [Output Processing Errors](failures/output-processing-errors.md), validate output format against expected schema before parsing, handle parsing errors explicitly, and test with real tool outputs not just examples.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Action-Completion Claimed Without Status Check](failures/action-completion-claimed-without-status-check.md) | Tool action initiated but completion status not verified; agent assumes success |
| [Blocking Tool Operations](failures/blocking-tool-operations.md) | Tool operation blocks indefinitely or for unexpectedly long time; agent cannot proceed |
| [Error Information Leakage](failures/error-information-leakage.md) | Tool errors expose sensitive information; agent or user sees information that should be hidden |
| [External System Failures](failures/external-system-failures.md) | Tool depends on external service that fails; tool failure cascades from external system |
| [Missing Parameters](failures/missing-parameters.md) | Tool requires parameters; agent doesn't provide them; call fails |
| [Output Misinterpretation](failures/output-misinterpretation.md) | Tool output is correct but agent interprets it wrong; agent acts on misunderstood data |
| [Output Processing Errors](failures/output-processing-errors.md) | Tool output format is unexpected; parsing fails; agent errors |
| [Parameter Mismatches](failures/parameter-mismatches.md) | Agent passes parameters of wrong type or format; tool parsing fails |
| [Schema Drift](failures/schema-drift.md) | Tool response schema changes; agent parsing breaks |
| [Sequencing Errors](failures/sequencing-errors.md) | Tools must be called in specific order; agent calls in wrong order; fails or produces wrong results |
| [Silent Failures](failures/silent-failures.md) | Tool call fails but returns no error signal; agent unaware of failure |
| [Silent Type Coercion](failures/silent-type-coercion.md) | Tool implicitly coerces types (string to number); coercion fails silently or produces wrong results |
| [Stale Tool Confirmation After Revision](failures/stale-tool-confirmation-after-revision.md) | Tool confirmation message outdated after tool revision; agent acts on stale confirmation |
| [State Space Navigation](failures/state-space-navigation.md) | Tool has complex state space; agent doesn't navigate correctly; reaches invalid or unexpected states |
| [Tool Availability Assumptions](failures/tool-availability-assumptions.md) | Agent assumes tool is always available; tool downtime causes agent failure |
| [Tool Capability Overestimation](failures/tool-capability-overestimation.md) | Agent assumes tool has capabilities it doesn't; calls fail or produce wrong results |
| [Tool Version Incompatibility](failures/tool-version-incompatibility.md) | Tool version changes; API incompatibility breaks agent |
| [Vague Tool Descriptions](failures/vague-tool-descriptions.md) | Tool documentation is unclear; agent misunderstands tool purpose or behavior |
| [Wrong Tool Selection](failures/wrong-tool-selection.md) | Agent selects wrong tool for task; tool call fails or produces irrelevant results |

**Total: 19 patterns**

## Related Goals

- [Tool Selection](../tool-selection/) — tool selection is upstream of reliability
- [Tool Error Handling](../tool-error-handling/) — error handling is key to tool reliability
- [Tool Invocation](../tool-invocation/) — invocation correctness supports tool reliability
