# Prediction Model Accuracy Regression

## Issue
An agent depends on an ML-powered tool (a classifier, a recommendation engine, a scoring API) whose underlying model the vendor updates server-side — a retraining, a new model version rollout, a fine-tuning change. Because the API contract (request/response shape) usually stays the same across a model update, nothing about the integration breaks; the model simply starts producing systematically different, and sometimes measurably worse, predictions for the agent's specific use case, with no changelog entry, version number bump, or notification distinguishing "same API, different model behavior underneath."

**Frequency**: Occasional

**Symptoms**
- Prediction quality or agreement-with-ground-truth degrades gradually or in a step change with no corresponding code or configuration change on the agent's side
- The regression affects specific categories or edge cases disproportionately, consistent with a retraining that shifted the model's learned distribution
- No entry in the vendor's changelog or API version history corresponds to the timing of the regression, since model updates are often treated as an internal implementation detail rather than a customer-facing change
- Downstream metrics dependent on the tool's predictions (conversion rate, false-positive rate, user complaints) shift in a way ultimately traced back to the tool, not the agent's own logic
- Re-running previously-scored inputs through the tool today produces different scores than when they were originally scored, despite no visible version change in the API

## Root Cause
ML vendors frequently treat model weights as an internal implementation detail decoupled from the API's version number — the endpoint URL, request schema, and response schema stay identical across a model retraining or architecture change, so from a pure API-contract perspective nothing has changed, and no deprecation or version-bump process is triggered. But the actual mapping from input to prediction has shifted, sometimes significantly, especially for edge cases or underrepresented categories in the vendor's updated training data. Agents have no way to detect this because they're not monitoring model behavior directly — they're monitoring API contract compliance (schema validity, status codes), which remains unaffected by a purely behavioral, server-side model change.

## Example
```
1. An agent uses a vendor's content-moderation API to flag policy-violating user posts
   before publication, calling a stable "/v1/moderate" endpoint that has not changed
   its request/response schema in over a year.
2. The vendor retrains the underlying model to improve performance on a newly prioritized
   category (hate speech in a specific language), as an internal improvement not
   communicated as a customer-facing release.
3. The retraining subtly shifts the model's decision boundary for an unrelated category
   (borderline sarcasm/humor), causing it to flag roughly 3x more benign sarcastic posts
   as violations than before.
4. The agent's moderation queue volume roughly triples within a week, with no
   corresponding change in actual user posting behavior or the agent's own code.
5. The operations team initially assumes a spam attack or a bug in their own filtering
   logic, spending two days investigating before comparing the model's current output
   on a fixed test set against a snapshot from a month earlier and discovering the
   scores have shifted meaningfully, even though nothing in the API version or docs
   indicated a change.
```

## Statistics
| Finding | Context |
|---------|---------|
| Server-side ML model updates are commonly deployed without any customer-facing changelog entry or version increment, since vendors typically treat the API contract, not the model weights, as the versioned surface | Reflects how ML API versioning conventions differ from traditional REST API versioning |
| Organizations that maintain a fixed "golden set" of test inputs scored periodically against the live API detect model regressions substantially faster, often within days, versus weeks or months for organizations relying only on downstream metric monitoring | By providing a direct, controlled comparison isolated from other confounding factors |
| Regressions from model updates disproportionately concentrate in edge cases and underrepresented categories relative to the vendor's retraining focus, rather than uniformly across all input types | Consistent with retraining typically targeting specific improvement areas that can shift decision boundaries elsewhere |

## Mitigations
1. **Golden-set regression testing against the live API**: Maintain a fixed, representative set of test inputs with known expected outputs, and periodically re-score them against the production API to detect drift in predictions even when the API version hasn't changed.
2. **Monitor downstream outcome metrics tied to the tool's predictions**: Track business-level metrics (false-positive rate, conversion rate, override rate) that depend on the tool's output, since these can surface a regression even without direct model access.
3. **Request model-change notifications contractually**: For high-stakes ML dependencies, negotiate with the vendor for advance notice of significant model updates, even if the API contract itself isn't changing.
4. **Version-pin where the vendor offers model-version selection**: Some ML API vendors offer explicit model-version pinning (distinct from API versioning); use it where available to control exactly when a model update takes effect for your traffic.
5. **Human-in-the-loop sampling on a rolling basis**: Continuously sample a small percentage of live predictions for human review, independent of any suspected incident, to catch gradual drift that a golden-set snapshot comparison might miss between test runs.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `model.golden_set_agreement_rate` | Agreement rate between current live predictions and expected outputs on a fixed golden test set | Alert when agreement drops more than 10 percentage points from the established baseline |
| `downstream.override_or_correction_rate` | Rate at which humans or downstream logic override/correct the tool's predictions | Alert on a sustained increase over a rolling 14-day baseline |
| `model.prediction_distribution_shift` | Statistical distance (e.g., KL divergence) between the current output distribution and a historical reference distribution on a fixed sample | Alert on significant divergence from baseline |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Golden set agreement drop | `golden_set_agreement_rate` falls below the alert threshold on a scheduled re-scoring run | High | Compare current vs. historical outputs on the golden set to characterize the shift, escalate to vendor |
| Sustained rise in downstream overrides | `override_or_correction_rate` trends upward significantly over 14 days | Medium | Investigate for silent model update; run golden-set comparison to confirm |

## Related Patterns
- [Accuracy Guarantee Not Met](./accuracy-guarantee-not-met.md) - a related but distinct failure: never having met the advertised accuracy at all, versus previously adequate accuracy regressing after a change
- [Degraded Sla Not Communicated](./degraded-sla-not-communicated.md) - shares the "silent, undetected quality change" structure, though driven by a permanent model update rather than a transient incident
- [Beta Feature Instability](../../tool-capability-limits/failures/beta-feature-instability.md) - beta/preview ML features are especially prone to frequent, uncommunicated model changes
