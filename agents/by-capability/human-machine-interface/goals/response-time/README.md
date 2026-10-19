# Response Time: Goal, Metrics, and Patterns

> **Goal:** Replies arrive at a pace that fits the channel and the user's urgency, and waits are never silent.

## Why this family exists
Speed and silence decide whether a user waits, resends, or leaves. This family covers how waits are shown and handled; the technical causes of slowness are covered elsewhere in the library.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Share of waits over 10 seconds with a progress or ETA message | Over 95% (tune) | [silent long-running work](failures/silent-long-running-work.md) |
| Silent-failure rate (requests ending with no reply, error, or incomplete marker) | 0 (tune) | [silent failure and timeout](failures/silent-failure-and-timeout.md) |

## Patterns
| Pattern | One line |
|---|---|
| Silent long-running work | The assistant works for about 10 seconds or more with no status, progress, or estimate |
| Silent failure and timeout | A request times out or an answer is cut off with no error, or partial text looks finished |

## Planned (not yet written)
The rest of the family is listed in the [roadmap](../../roadmap/response-time.md).

## Related
- [Errors and recovery](../errors-and-recovery/README.md): what to say when a wait ends in failure
- [Effort and memory](../effort-and-memory/README.md): reporting what is left
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
