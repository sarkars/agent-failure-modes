# Model Behavior Change Detection Failure

## Issue
A provider ships a new model version, the team's existing evaluation suite passes it (or the update is adopted without a full re-run), and a real behavior regression on a specific task type ships to production undetected — because the eval suite doesn't cover that task type, uses stale test cases the new model has effectively memorized, or measures aggregate pass rate in a way that dilutes a regression concentrated in one narrow slice of traffic. The team only learns about the regression from user complaints or downstream error spikes, well after the update is already serving all production traffic.

**Frequency**: Common

**Symptoms**
- A model version update passes the existing evaluation suite with no red flags, but a specific task type regresses in production shortly after
- Aggregate eval pass rate stays flat or even improves across a version update while a narrow but important slice of traffic degrades
- The regression is only found through user complaints, support ticket spikes, or a downstream metric (conversion, escalation rate) drifting, not through the evaluation pipeline
- Post-incident review finds the eval suite's test cases don't cover the specific task pattern that regressed, or were written against the old model version and don't stress the new one's actual failure modes
- The same regression, once identified, is trivially reproducible with a handful of examples — the eval gap was in coverage, not in difficulty of detection

## Root Cause
Evaluation suites are built once against the failure modes known at the time, using test cases and metrics chosen to catch the kinds of errors the current model makes — but a new model version can have a different error profile entirely, regressing on task types the old model handled well and that the eval suite therefore never needed to test. Aggregate pass-rate metrics compound this by construction: if a regression is concentrated in a narrow but real task type that represents a small fraction of the eval suite's test cases, its impact on the overall score can be statistically invisible even though it's a significant real-world problem for the users who hit it. Teams also frequently treat "passed the existing eval suite" as sufficient justification to adopt a new version, without recognizing that an eval suite's coverage is a snapshot of past failure modes, not a guarantee against new ones introduced by a different training run, different fine-tuning data, or different alignment tuning in the new version.

## Example
```
A legal-document-summarization agent's eval suite consists of 200 test
documents with human-graded summary quality scores, built two years
earlier and covering primarily contract and NDA documents, since that
was the dominant use case at the time.

The team adopts a new model version after it passes the eval suite with
a 94% quality score, up from 91% on the prior version - a clear
improvement, so the update ships to all traffic.

Three weeks later, support tickets spike specifically for summaries of
patent filings, a document type that had grown to 15% of real traffic
but was never represented in the original 200-document eval set. The new
version, it turns out, systematically drops key claim-scope details in
patent summaries - a regression invisible to an eval suite built around
a document mix from two years earlier and only caught once patent-summary
users started complaining in volume.
```

## Statistics
| Finding | Context |
|---------|---------|
| A meaningful share of production model-version regressions are found via user complaints or downstream metrics rather than pre-deployment evaluation, in teams without task-representative eval coverage | Estimated from postmortems of model update incidents |
| Eval suites more than 12-18 months old, unrefreshed against current production traffic mix, show measurably lower correlation with real-world regression detection than suites refreshed quarterly | Typical pattern observed across eval-suite maintenance audits |
| Slicing eval results by task subtype (rather than reporting aggregate pass rate alone) surfaces a substantial share of regressions that aggregate scoring alone would miss | Typical range reported by teams that added subtype-sliced eval reporting |

## Mitigations
1. **Task-representative eval refresh cadence**: Periodically regenerate or resample the evaluation suite against current production traffic distribution, not a fixed historical snapshot, so coverage tracks what users actually do.
2. **Subtype-sliced reporting, not just aggregate scores**: Report eval results broken out by task subtype/category, and require every subtype to individually clear a quality floor before a version update ships, rather than relying on an aggregate score that can hide concentrated regressions.
3. **Regression-specific test case accumulation**: Every production regression found post-launch should be converted into a permanent eval test case, so the suite's coverage grows to include real failure modes as they're discovered rather than staying static.
4. **Shadow evaluation on live traffic**: Run a new model version against a sample of real, current production requests (not just the static eval set) before full rollout, comparing outputs against the current version to catch distributional gaps the static suite misses.
5. **Staged rollout with per-segment monitoring**: Roll out version updates to a small percentage of traffic first, with monitoring sliced by task type/segment, so a narrow regression is caught by production signal before it reaches full traffic even if the eval suite missed it.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| eval_suite_traffic_representativeness | Statistical similarity between eval suite task-type distribution and current production traffic distribution | Alert if divergence exceeds calibrated threshold |
| subtype_quality_floor_breach | Any task subtype's eval score falling below its individual quality floor, independent of aggregate score | Alert if any subtype breaches floor |
| post_update_complaint_rate_by_task_type | Support/complaint rate broken out by task type in the period following a version update | Alert if any task type shows elevated rate versus pre-update baseline |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Subtype quality floor breached pre-launch | A task subtype fails its individual quality floor during pre-deployment evaluation | High | Block full rollout, investigate regression, consider staged rollout with monitoring |
| Post-launch complaint spike by task type | post_update_complaint_rate_by_task_type spikes for a specific task type after a version update | High | Roll back or restrict the update for the affected task type, add the failure case to the eval suite |

## Related Patterns
- [Model Update Accuracy Regression](./model-update-accuracy-regression.md) - describes the regression itself; this pattern describes why the detection mechanism failed to catch it before launch
- [Model AB Test Interference](./model-ab-test-interference.md) - both describe behavior changes that existing monitoring isn't structured to surface, one from interaction effects and one from eval coverage gaps
- [Model Update Rollback Delay](./model-update-rollback-delay.md) - a detection failure at launch directly extends the time before a rollback decision can even be triggered
