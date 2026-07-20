# Contingency Plan Missing

## Issue
An agent generates a plan as a single linear sequence of steps with no fallback for what to do if a given step fails, returns an unexpected result, or becomes unavailable. When the primary path breaks partway through execution, the agent has no pre-defined alternative to fall back to and either halts entirely, retries the same failing step indefinitely, or improvises an ungrounded workaround on the spot with no guardrails.

**Frequency**: Very Common

**Symptoms**
- Execution halts completely on the first step failure with no attempt at an alternative approach
- The agent retries the identical failing action multiple times with no variation, as if repetition alone might change the outcome
- When the agent does improvise after a failure, the improvised action is ungrounded and often worse than simply stopping (e.g. guessing at data instead of fetching it a different way)
- Post-incident review shows the failure point was foreseeable (a flaky API, a permission that might be missing) but no branch was planned for it
- User-facing failures that trace back to a single-point-of-failure step with no planned alternative

## Root Cause
Plan generation, especially when driven by an LLM producing a step list in one pass, is optimized to describe the happy path because that's what the task description and available examples most directly imply. Producing a contingency branch requires the planner to explicitly reason about failure modes for each step — a distinct and often-skipped cognitive step from describing what should happen when things go right. Most planning frameworks also don't structurally require a fallback field per step, so there's no forcing function making the planner consider "what if this doesn't work" before execution begins, and by the time a step actually fails, the agent is in a reactive posture with only the tools available at that moment, not a considered alternative.

## Example
```
A travel-booking agent is asked to book a flight and, if the flight is
available, reserve a hotel at the destination for the same dates.

Generated plan:
  1. Search flights for the requested route/dates.
  2. Book the cheapest available flight.
  3. Search hotels at the destination for the matching dates.
  4. Book a hotel.
  5. Send confirmation summary to the user.

Step 2 fails: the previously-available cheapest flight sold out between
the search and the booking call (a common race condition with third-party
inventory), and the booking API returns "fare no longer available."

The plan has no branch for this. The agent's only defined next action was
step 3, which assumed step 2 succeeded. With no contingency ("if booking
fails, re-search and select the next cheapest option, up to 2 retries"),
the agent either halts with an unhelpful error, or -- worse -- proceeds to
book the hotel anyway for dates with no corresponding flight, leaving the
user with a hotel reservation and no way to get there.
```

## Statistics
| Finding | Context |
|---------|---------|
| Plans generated without explicit fallback steps are estimated to fail outright (full halt) on a meaningful minority of executions where at least one step encounters a transient error | Typical range observed in agent execution logs across tool-using workflows |
| Steps involving third-party APIs or external inventory are disproportionately represented among failures with no contingency, given their higher baseline transient-failure rate | Estimated from instrumented multi-step agent traces |
| Requiring at least one fallback branch per external-dependency step is reported to cut full-plan-halt incidents substantially | Reported range across teams that added mandatory contingency fields to planning templates |

## Mitigations
1. **Mandatory fallback field per step**: Require the planner to populate an explicit fallback or "on-failure" action for every step that depends on an external system, even if the fallback is simply "retry once, then escalate to human," rather than leaving it implicit.
2. **Pre-mortem prompting during plan generation**: Prompt the planning step to explicitly enumerate plausible failure modes for each action before finalizing the plan, surfacing contingencies the happy-path framing would otherwise skip.
3. **Failure-mode library by step type**: Maintain a reusable library of common contingencies for common step types (API call -> retry-then-alternate-provider, search -> broaden-query, payment -> retry-then-escalate) that the planner can attach rather than generating from scratch each time.
4. **Graceful degradation over hard halt**: Design the executor so that when no contingency exists for a failed step, it defaults to a safe partial-completion state (report what succeeded, flag what didn't) rather than either halting silently or improvising an ungrounded workaround.
5. **Post-execution contingency gap analysis**: Log every step failure that had no matching contingency and periodically review these gaps to backfill the fallback library, closing the most common missing branches first.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| plan_halt_on_first_failure_rate | Fraction of executions that stop entirely at the first step failure with no fallback attempted | Alert if > 10% |
| steps_without_contingency_ratio | Fraction of external-dependency steps in generated plans that have no defined fallback | Alert if > 30% |
| ungrounded_improvisation_count | Instances where the agent took an unplanned, unreviewed action after a step failure | Alert if > 0 for high-stakes workflows |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Plan halted with no fallback available | A step fails and no contingency branch exists in the plan | Medium | Notify workflow owner, review whether a fallback should be added to the template |
| Improvised action taken post-failure | Agent takes an action not present in the original plan or fallback library after a step failure | High | Flag for human review before downstream effects proceed |

## Related Patterns
- [Plan Adaptability Failure](./plan-adaptability-failure.md) - missing contingencies are the static-planning-time counterpart to the dynamic inability to adapt mid-execution
- [Plan Backtracking Failure](./plan-backtracking-failure.md) - even when a contingency exists, the agent still needs the ability to cleanly unwind and retry the failed branch
- [Plan Invalidation Not Detected](./plan-invalidation-not-detected.md) - both leave the agent executing blindly forward when the world no longer matches the plan's assumptions
