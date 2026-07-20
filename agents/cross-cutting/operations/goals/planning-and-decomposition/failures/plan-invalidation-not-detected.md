# Plan Invalidation Not Detected

## Issue
While an agent is mid-execution on a multi-step plan, something in the external world changes in a way that invalidates the plan's premise — a price changes, an item goes out of stock, a policy is updated, a file the plan depends on is deleted — but the agent has no mechanism actively watching for such changes and keeps executing the now-invalid plan exactly as originally generated. Unlike a step that fails outright, an invalidated plan often continues to execute "successfully" step by step, since none of the individual actions error out; the plan simply no longer serves its original purpose.

**Frequency**: Common

**Symptoms**
- A plan completes all its steps without error, but the final result is based on assumptions that were true at plan time but false by execution time
- Actions taken later in a plan that contradict information available earlier in the same execution, because nothing re-checked
- No re-validation or freshness check anywhere between plan generation and the plan's final step, especially in long-running or paused workflows
- Discrepancies discovered by the user or a downstream system rather than by the agent itself
- The gap between plan generation and plan completion correlating strongly with invalidation incidents (longer-running plans invalidate more often)

## Root Cause
Plans are generated as a snapshot of the world at one point in time, but execution — especially for multi-step, tool-calling, or human-approval-gated workflows — can span seconds, minutes, or hours. Most agent architectures have no built-in mechanism to re-verify the plan's load-bearing assumptions against current reality before or during execution; the plan is treated as a fixed artifact to be worked through rather than a hypothesis that could be falsified by new information. This is distinct from a step simply failing: an invalidated plan's steps can all execute without technical error, because nothing about the tool calls themselves is wrong — it's the premise underlying why those steps make sense that has silently become false.

## Example
```
An e-commerce agent is asked to "reorder our top-selling SKU when stock
drops below 50 units" and, upon detecting SKU-2201 at 42 units, generates
a 4-step plan:
  1. Confirm SKU-2201 is still the top-selling SKU (checked: yes, at plan
     generation time).
  2. Calculate reorder quantity based on the last 30 days of sales
     velocity.
  3. Submit a purchase order to the primary supplier for the calculated
     quantity.
  4. Notify the inventory manager that a reorder was placed.

Between step 1 (confirmed at 09:00:00) and step 3 (executed at
09:04:30, after a human-approval gate that took 4 minutes), the primary
supplier's account is suspended due to an unrelated billing dispute --
a fact available in the supplier-management system by 09:02:00, two
minutes before step 3 executes, but the plan has no step that re-checks
supplier status before submitting the order.

Step 3 executes as planned and fails at the supplier API with "account
suspended," but because the plan had no re-validation step, the agent
had no way to catch this two minutes earlier when the information was
already available, and instead of a controlled early exit, the customer
sees a bare integration error with no explanation of what happened or
what to do next.
```

## Statistics
| Finding | Context |
|---------|---------|
| Plans with execution windows longer than a few minutes (due to approval gates, long-running tool calls, or scheduled steps) show a disproportionately higher rate of premise invalidation than short, immediately-executed plans | Typical range observed in agent workflow retrospectives |
| Systems with no re-validation checkpoint are estimated to complete a meaningful share of multi-step plans "successfully" despite an invalidating change occurring mid-execution | Estimated from analysis of long-running agent workflow traces |
| Adding a lightweight pre-critical-step freshness check (re-verifying load-bearing assumptions immediately before an irreversible action) is reported to catch the majority of invalidation cases before they cause downstream harm | Reported range across teams that added re-validation gates before high-stakes steps |

## Mitigations
1. **Freshness checks before irreversible steps**: Immediately before any step with real-world, hard-to-reverse consequences (a purchase, a send, a payment), re-verify the specific assumptions that step depends on against current data, not just at plan generation time.
2. **Assumption tagging with expiry**: Have the planner explicitly tag which facts a plan depends on and how time-sensitive each is, so the executor knows which assumptions need re-checking and how urgently, rather than treating the whole plan as equally fresh throughout.
3. **Event-driven re-validation triggers**: Where the domain supports it, subscribe to change events on the specific entities the plan depends on (stock level, account status, price) so an invalidating change actively interrupts execution rather than requiring a poll.
4. **Bounded plan validity windows**: Set an explicit expiry on how long a generated plan remains valid without re-verification, forcing a refresh of key assumptions if execution stalls or is delayed past that window (e.g. by a slow approval gate).
5. **Post-execution assumption audit**: Log the assumptions a plan relied on alongside the actual state of those facts at each step's execution time, and periodically review the gap to identify which assumption types invalidate most often and need tighter checks.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| plan_execution_window_duration | Time elapsed between plan generation and plan completion | Track distribution; flag outliers for review |
| premise_invalidation_detected_rate | Fraction of executions where a re-validation check caught an invalidated assumption before it caused harm | Track as a positive signal; investigate if trending toward 0 despite long execution windows |
| post_hoc_invalidation_discovery_count | Cases where an invalidated plan's bad outcome was discovered only after the fact, not during execution | Alert if > 0 for high-stakes workflows |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Irreversible step executed on stale assumption | A high-stakes step ran without a freshness check despite the plan's execution window exceeding the assumption's validity period | High | Halt further execution, audit outcome, add re-validation gate for this step type |
| Long execution window with no re-validation checkpoint | A plan's execution spans longer than a defined threshold with zero re-validation events logged | Medium | Flag workflow for adding assumption-expiry checks |

## Related Patterns
- [Plan Adaptability Failure](./plan-adaptability-failure.md) - invalidation-not-detected is the specific failure to notice a changed premise, while adaptability failure is the broader inability to act on it even once noticed
- [Contingency Plan Missing](./contingency-plan-missing.md) - a well-designed contingency for "assumption no longer holds" would catch what an invalidated plan otherwise executes blindly through
- [Plan Hallucination Detection Failure](./plan-hallucination-detection-failure.md) - both involve the plan being disconnected from ground truth, one from the start and one developing over the execution window
