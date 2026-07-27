# Missing Task Specialization

## Issue: Agent stays on generic frontier-model prompting for a high-volume, narrow, repetitive task long after fine-tuning or distillation would outperform it on both cost and quality.

**Frequency**: Common

**Symptoms**
- A single task type accounts for a large share of monthly request volume, still served by a general-purpose prompt on a frontier model
- Per-request cost for the narrow task remains at frontier-model pricing month over month even though the task's input/output format hasn't changed and volume has grown well past the point where fine-tuning economics would favor a smaller model
- Prompt for the task has accumulated many few-shot examples and defensive formatting instructions to force a narrow, repetitive output shape, an indicator the task is stable and specializable rather than genuinely open-ended
- No fine-tuning, distillation, or smaller-model pilot has ever been run or evaluated for the task despite its volume and narrowness being visible in cost/usage dashboards
- Latency for the task is dominated by frontier-model inference time on a prompt that is mostly boilerplate/repeated instructions rather than task-specific novel content

**Root Cause**
Agent stays on generic frontier-model prompting for a high-volume, narrow, repetitive task long after fine-tuning or distillation would outperform it on both cost and quality.

**Example**
```
A support-ticket triage agent for a project-management SaaS product classifies every incoming
ticket into one of eighteen fixed categories and extracts a handful of structured fields
(account tier, affected feature, urgency) before routing it to the right team queue. The task
has run on the same frontier general-purpose model with a long, example-laden prompt for over
a year, processing more than 40,000 tickets a day. The category set and output schema haven't
changed in six months. No one has revisited the model choice since the pipeline was first
built, because it works and nobody owns the recurring cost/quality review. A cost audit
finally flags that this single task accounts for close to a third of the team's monthly
inference bill, driven almost entirely by a locked, narrow, high-volume classification task
that is a textbook fine-tuning candidate. A subsequent pilot fine-tuning a much smaller model
on a year of labeled ticket data matches the frontier model's classification accuracy at a
fraction of the per-request cost and with noticeably lower latency, but the switch is delayed
by months simply because no recurring process existed to trigger the evaluation earlier.
```

**Contributing Factors**
- No recurring review of task volume/narrowness against the fine-tune/distill decision threshold (commonly cited around 10K+ requests/day or 50M+ tokens/month for a locked, narrow task)
- Cost and quality metrics are tracked in aggregate across all tasks rather than broken out per task type, so a single high-volume narrow task's outsized contribution to spend is invisible without a dedicated audit
- Team lacks in-house fine-tuning/distillation tooling or experience, making a frontier-model prompt the path of least resistance even after the task has proven stable and specializable
- Organizational incentive is to ship the pipeline once and move on to new features, with no owner responsible for periodically revisiting model-selection decisions on mature, high-volume tasks

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Volume/narrowness threshold audit | Per-task-type request volume and output-schema stability logs over the past 90 days | Tasks exceeding the volume/narrowness threshold are flagged for a fine-tune/distill evaluation | A task exceeds the threshold with no fine-tuning evaluation on record |
| Fine-tuned vs. frontier accuracy comparison | A held-out labeled eval set for the candidate task, run against both the current frontier-model prompt and a fine-tuned smaller-model candidate | Fine-tuned candidate matches or exceeds frontier accuracy within an acceptable margin | Fine-tuned candidate is never evaluated, or evaluation results are ignored/not acted upon |
| Per-task cost breakdown review | Aggregate monthly inference spend broken out by task type | Any single narrow task representing a large spend share triggers a specialization review | Cost dashboards report only aggregate spend with no per-task breakdown, hiding the concentration |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Time-to-specialization-review after threshold crossed | <30 days | Measure elapsed time between a task crossing the volume/narrowness threshold and a documented fine-tune/distill evaluation being run |
| Cost delta between frontier and specialized model on qualifying tasks | >=50% reduction where specialization is adopted | Compare per-request cost before/after fine-tuning or distillation on tasks that crossed the threshold |
| Share of high-volume narrow tasks still on frontier general-purpose prompting | <10% of qualifying tasks | Cross-reference the per-task volume/narrowness audit against which tasks have been specialized |

---

## Mitigation Strategies

### Prevention
1. **Per-task cost and volume dashboard**: Break out inference spend, request volume, and output-schema stability by task type (not just in aggregate) so a high-volume, narrow task's disproportionate cost share is visible without a special audit.
2. **Scheduled fine-tune/distill review at volume threshold**: Trigger a mandatory specialization evaluation whenever a task crosses a defined volume/narrowness threshold (e.g., 10K+ requests/day or 50M+ tokens/month with a stable output schema), rather than leaving the decision to ad hoc discovery.
3. **Task-maturity ownership**: Assign an owner responsible for periodically revisiting model-selection decisions on mature, high-volume tasks, separate from the team that originally shipped the pipeline and moved on to new features.

### Detection & Response
1. **Cost-per-task anomaly detection**: Alert when a single task type's share of total inference spend exceeds a set percentage, prompting a specialization review even if no one manually audits it.
2. **Fine-tune pilot fast-track**: When a task is flagged, run a time-boxed pilot comparing a fine-tuned/distilled smaller model against the frontier-model baseline on a held-out eval set, with a pre-agreed decision rule for switching.

### Architecture Patterns
1. **Volume-triggered specialization pipeline**: An automated workflow that flags tasks crossing the volume/narrowness threshold and kicks off data collection for a fine-tuning candidate without requiring manual initiation.
2. **Shadow-mode fine-tuned model evaluation**: Run a fine-tuned/distilled candidate in parallel (shadow mode) against live traffic for a qualifying task before cutting over, so quality parity is confirmed under real conditions.
3. **Model-tier registry per task**: A registry recording which model (frontier vs. specialized) currently serves each task type and when it was last reviewed, making stale frontier-only assignments visible at a glance.

### Metrics
1. **time_to_specialization_review_days**: Target: <30; Alert threshold: >90
2. **specialized_vs_frontier_cost_reduction_pct**: Target: >=50%; Alert threshold: <20%
3. **qualifying_tasks_unspecialized_pct**: Target: <10%; Alert threshold: >30%

### Alerts
1. **Task Exceeds Specialization Threshold Unreviewed** (P2 - Warning): Condition - a task crosses the volume/narrowness threshold and remains unreviewed for longer than the 30-day SLA. Action: assign the task-maturity owner to run a fine-tune/distill pilot within the next sprint.
2. **Disproportionate Task Cost Share** (P2 - Warning): Condition - a single task type accounts for more than a set share (e.g., 20%) of total monthly inference spend while still on a frontier general-purpose model. Action: escalate to engineering leadership for a specialization decision.
3. **Fine-Tune Pilot Shows Clear Win, Not Adopted** (P3 - Info): Condition - a completed pilot shows the specialized model meets quality bar at materially lower cost, but no cutover has occurred after 60 days. Action: revisit the rollout plan and remove adoption blockers.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| Days since a qualifying task's last specialization review | >90 |
| Share of monthly inference spend from a single unspecialized task | >20% |
| Qualifying tasks still on frontier general-purpose prompting | >30% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Specialization review overdue | Qualifying task unreviewed for over 90 days | Medium |
| Cost concentration in unspecialized task | Single task exceeds 20% of monthly spend, still frontier-served | Medium |
| Pilot win not adopted | Fine-tuned pilot shows clear cost/quality win, no cutover after 60 days | Low |

---

## Related Patterns

- [Model Selection Waste](../../cost-efficiency/failures/model-selection-waste.md) - the tier-routing failure (choosing among existing off-the-shelf models); this pattern is the distinct case of never specializing a model to the task at all
- [Non-Generalized Plan Template](./non-generalized-plan-template.md) - a related but distinct specialization gap at the plan level rather than the model level

## References

- [Is Fine-Tuning Better Than Prompt Engineering in 2026?](https://llm-stats.com/blog/research/fine-tuning-vs-prompt-engineering-2026) - decision thresholds: fine-tune above ~10K requests/day or when a hyper-specific format can't be reliably enforced by prompting alone
- [The AI Project Distillation Case: When a Smaller Fine-Tune Beats a Bigger Model](https://sfailabs.com/guides/the-ai-project-distillation-case-when-a-smaller-fine-tune-beats-a-bigger-model) - a fine-tuned 8B model can match a 70B model on a narrow, repetitive task
- [Distilling Step-by-Step: Outperforming Larger Language Models with Less Training](https://research.google/blog/distilling-step-by-step-outperforming-larger-language-models-with-less-training-data-and-smaller-model-sizes/) - Google Research on distillation outperforming larger general-purpose models on specialized tasks
