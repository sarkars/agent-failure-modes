# Plan Adaptability Failure

## Issue
An agent commits to a plan generated at the start of a task and continues executing it step by step even after circumstances relevant to the plan have visibly changed mid-execution — new information arrives, an assumption the plan relied on turns out false, or the user's actual need shifts. Rather than re-planning or adjusting, the agent treats the original plan as fixed, executing later steps that no longer make sense given what's now known.

**Frequency**: Common

**Symptoms**
- Later plan steps executed even though earlier steps surfaced information that makes them irrelevant or counterproductive
- The agent completing a plan "successfully" by its own step-checklist while producing an outcome the user no longer wants
- No re-planning or plan-revision step anywhere in the execution trace, only forward step-by-step execution
- User mid-task clarifications or corrections that don't visibly change the remaining steps the agent takes
- Post-hoc review showing the plan was reasonable when generated but stale by the time later steps executed

## Root Cause
Most agent architectures generate a plan once, up front, and treat execution as simply working through that plan's step list, because re-planning is more expensive (another LLM call, more latency, more chance of inconsistency) than blindly continuing. There is often no explicit checkpoint built into the execution loop that asks "does the plan still make sense given what I now know," so the agent has no natural moment to reconsider. Even when agents are technically capable of re-planning, the trigger for doing so is usually only a hard step failure, not a softer signal like "the information I just retrieved changes what should happen next" — so plans remain static in the face of information that would clearly have changed a human's approach.

## Example
```
A research agent is asked to "find the best vendor for cloud storage
under our $500/month budget" and generates a 6-step plan:
  1. List cloud storage vendors.
  2. Get pricing for each at the required volume.
  3. Filter to vendors under $500/month.
  4. Compare feature sets among the filtered vendors.
  5. Recommend the top choice with a comparison table.
  6. Draft an email summary to the user.

Step 2 reveals that, at the required volume (2.8 PB), every mainstream
vendor's list price exceeds $500/month by a wide margin -- the entire
premise of step 3 (filtering to a non-empty budget-compliant set) is now
false. The plan has no re-evaluation checkpoint, so the agent proceeds
to step 3 anyway, produces an empty filtered list, and step 4 ("compare
feature sets among the filtered vendors") silently operates on zero
vendors. Step 5 outputs "no vendors meet the criteria" without ever
stepping back to reconsider the actual goal -- e.g. proposing volume
discounts, negotiated pricing, or a revised budget conversation with the
user, which is what a human analyst would have done as soon as step 2's
result contradicted the plan's premise.
```

## Statistics
| Finding | Context |
|---------|---------|
| Plans that never re-evaluate mid-execution are estimated to complete "successfully" by their own step-checklist while missing the user's actual current need in a meaningful share of multi-step tasks with real-world information gaps | Typical range observed in agent evaluation studies involving information discovered mid-task |
| Adding an explicit re-planning checkpoint after each information-gathering step is reported to catch a majority of premise-invalidating discoveries before they propagate into wasted downstream steps | Reported range across teams that added mid-plan re-evaluation |
| Tasks with 5+ sequential steps show disproportionately higher rates of stale-plan execution than shorter tasks, correlating with more opportunities for new information to invalidate early assumptions | Estimated from agent trace analysis across task lengths |

## Mitigations
1. **Periodic re-planning checkpoints**: Insert explicit "does this plan still make sense" evaluation points after steps likely to surface new information (searches, data retrievals, tool calls with variable results), not only after hard failures.
2. **Premise tracking**: Have the planner record the key assumptions each step depends on, and check those assumptions against newly discovered information at each checkpoint, triggering re-planning specifically when a tracked assumption is contradicted.
3. **Lightweight incremental re-planning**: Rather than regenerating the entire plan from scratch on every checkpoint (expensive and slow), support partial revision of just the affected downstream steps when an upstream assumption changes.
4. **User-visible plan state**: Surface the current plan and its key assumptions to the user at natural checkpoints, so a human can catch and correct a stale plan even if the agent's own re-evaluation logic misses it.
5. **Outcome-oriented step evaluation**: Evaluate each step's result against the original goal, not just against "did this step technically complete," so a technically-successful-but-goal-irrelevant result triggers reconsideration.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| plan_revision_rate | Fraction of multi-step executions that trigger at least one re-planning event | Alert if near 0% across a large task population (suggests re-planning never fires) |
| premise_contradiction_undetected | Count of cases where a later step's result contradicts an earlier tracked assumption with no re-plan triggered | Alert if > 0 for flagged high-stakes workflows |
| goal_alignment_score_drift | Divergence between the final outcome and the original stated goal, scored post-hoc | Alert if trending downward across a task cohort |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Empty or degenerate downstream result from stale premise | A filtering/comparison step operates on an empty or clearly-invalid set without triggering re-planning | Medium | Flag for review, check whether premise tracking caught the upstream contradiction |
| Task completed with low goal-alignment score | Final outcome scored as misaligned with the original user goal despite all plan steps completing | High | Route to human review before delivering result to user |

## Related Patterns
- [Plan Invalidation Not Detected](./plan-invalidation-not-detected.md) - a closely related failure focused specifically on external changes invalidating the plan, versus adaptability's broader inability to revise given any new information
- [Contingency Plan Missing](./contingency-plan-missing.md) - both leave the agent unable to deviate from an original plan, one for failures and one for new information
- [Plan Backtracking Failure](./plan-backtracking-failure.md) - adapting the plan often requires backtracking to undo or bypass steps built on the now-invalid premise
