# Voice Receptionist Agents: Goal, Metrics, and Patterns

> **Goal:** Phone agents confirm critical details, catch emergencies, and meet disclosure and consent rules.

## Why this family exists
AI agents now answer and place phone calls for clinics, salons, restaurants, and collections teams. A caller cannot see a screen, so a wrong booking detail or a missing disclosure is easy to miss until it costs something. This family covers those failures. The guidance is design guidance only, not legal advice. Have counsel read the pages marked "Read this first" before launch. Voice-channel signals are planned, not measured.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data.
| Metric | Target | Defined in |
|---|---|---|
| Bookings where the agent read back name, date, time, and service before saving | Start: 100% | [bookings without confirming details](failures/bookings-without-confirming-details.md) |
| Collections calls that give the required disclosures | Start: 100% | [collections calls without required disclosures](failures/collections-calls-without-required-disclosures.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Bookings without confirming details](failures/bookings-without-confirming-details.md) | The agent saves an appointment without reading the details back to the caller |
| [Collections calls without required disclosures](failures/collections-calls-without-required-disclosures.md) | An AI collections caller leaves out disclosures the rules require |

## Planned (not yet written)
Missed emergency signals on phone calls already have an example on [missed crisis signals](../vulnerable-users/failures/missed-crisis-signals.md). Other rows are tracked in the [agent types roadmap](../../roadmap/agent-types.md).

## Related
- [Voice](../voice/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
