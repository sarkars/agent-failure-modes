# Model A/B Test Interference

## Issue
Two or more concurrent A/B tests, each rolling out a different model version or configuration to a cohort of users, overlap in ways their designers didn't account for — a user gets assigned to conflicting cohorts across tests, or a shared downstream system (a cache, a session, a fine-tuned classifier) is implicitly tuned for one test's model and breaks for the other's. The result is inconsistent user-facing behavior that isn't explained by either experiment's own design, and that neither experiment's metrics dashboard is set up to detect since each only tracks its own cohort in isolation.

**Frequency**: Occasional

**Symptoms**
- The same user or session receives visibly different model behavior across nominally unrelated features, traced back to two independent experiments both touching model selection
- One experiment's metrics look anomalous only for users who also happen to be in a second, unrelated experiment's treatment group
- A shared component tuned assuming one experiment's model version (a prompt template, a response parser) breaks specifically for users in the other experiment's cohort
- Experiment analysis teams debug a metrics anomaly for days before discovering a second, independently-run test was interacting with theirs
- Cohort assignment logs show the same user classified into overlapping treatment groups across tests that were designed and shipped without cross-team coordination

## Root Cause
A/B testing infrastructure is usually built to isolate one experiment's effect by randomizing cohort assignment independently per experiment, which is correct for the statistical goal of each individual test but doesn't prevent two independently-randomized experiments from assigning the same user to interacting treatment conditions simultaneously. When both experiments touch the same underlying resource — which model serves a given request — their effects aren't simply additive; a downstream system built and tuned against the assumption of one model version can behave unpredictably when a second experiment substitutes a different version for a subset of the same traffic. This is compounded by the common practice of running experiments in independent, siloed teams with separate dashboards and separate significance testing, so cross-experiment interaction isn't something any single team's monitoring is positioned to catch — it only becomes visible in the union of both experiments' cohorts, which nobody is dedicated to watching.

## Example
```
Team A runs an experiment testing a newer, more verbose model version for
20% of users on the "email drafting" feature, measuring draft-acceptance
rate.

Independently, Team B runs an experiment on the same platform testing a
stricter output-length limit (a prompt-level change, not a model change)
for 15% of users across all AI-assisted features, measuring time-to-send.

Users in the intersection of both cohorts (an estimated 3% of traffic)
get the newer, more verbose model combined with the stricter length limit
- a combination neither team tested in isolation. The verbose model,
constrained to a shorter length, produces truncated, incomplete-sounding
drafts. Team A sees a small, statistically ambiguous dip in acceptance
rate they attribute to noise; Team B sees a small dip in time-to-send
they attribute to their length limit working "too well." Neither team's
dashboard segments by the other's cohort, so the actual interaction -
verbose model plus aggressive truncation producing bad drafts for 3% of
users - is never identified without a manual cross-team investigation.
```

## Statistics
| Finding | Context |
|---------|---------|
| A meaningful share of unexplained experiment metric anomalies in platforms running many concurrent tests are ultimately attributed to cross-experiment interaction once investigated | Estimated from postmortems of experiment anomaly investigations |
| Experiments touching the same underlying resource (model selection, prompt template) without coordinated cohort exclusion show measurably higher rates of interaction-driven anomalies than resource-disjoint experiments | Typical pattern observed across multi-team experimentation platforms |
| Adding mutual-exclusion or explicit interaction-tracking layers between experiments sharing a resource substantially reduces undetected interaction incidents | Typical range reported by teams that added this coordination layer |

## Mitigations
1. **Resource-aware mutual exclusion**: Track which underlying resource (model selection, prompt version) each experiment touches, and either mutually exclude cohorts of experiments sharing a resource or explicitly design them to be tested in combination.
2. **Cross-experiment cohort registry**: Maintain a central, queryable registry of active experiments and cohort assignments so any team can check for overlap before or during their own experiment's analysis.
3. **Interaction-segment monitoring**: For any pair of experiments sharing a resource, automatically segment metrics by the intersection cohort and flag anomalies specific to that intersection rather than only tracking each experiment's isolated cohort.
4. **Experiment launch review gate**: Require new experiments touching model selection or shared prompt infrastructure to be reviewed against the current registry of active experiments before launch, not just approved in isolation by the owning team.
5. **Factorial design for known-overlapping tests**: When two experiments are known to share a resource and can't be mutually excluded, explicitly design them as a factorial experiment (testing all combinations) rather than as two independent tests analyzed separately.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| cohort_overlap_rate | Share of users assigned to treatment cohorts in two or more concurrent experiments touching the same resource | Alert if > 0 without an explicit factorial design |
| intersection_cohort_metric_anomaly | Metric deviation specific to the intersection of two experiments' cohorts, versus each cohort in isolation | Alert if deviation exceeds each individual experiment's own noise floor |
| unregistered_experiment_resource_touch | An experiment modifying model selection or prompt infrastructure without a corresponding registry entry | Alert if detected |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unplanned cohort overlap detected | Two active experiments touching the same resource show nonzero cohort overlap without factorial design | High | Pause one experiment or add mutual exclusion, notify both owning teams |
| Intersection anomaly found | intersection_cohort_metric_anomaly crosses threshold | Medium | Segment analysis by intersection cohort, investigate interaction before drawing conclusions from either experiment |

## Related Patterns
- [Model Behavior Change Detection Failure](./model-behavior-change-detection-failure.md) - both involve behavior changes that existing monitoring isn't structured to detect, one from interaction effects and one from lack of eval coverage
- [Model Release Cycle Timing Mismatch](./model-release-cycle-timing-mismatch.md) - concurrent experiments and provider release cadence both introduce version changes that can arrive faster than validation processes can isolate their effects
- [Model Update Rollback Delay](./model-update-rollback-delay.md) - an undetected interaction effect from this pattern often takes longer to diagnose and roll back precisely because its cause isn't a single experiment's own metrics
