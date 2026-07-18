# Accuracy Guarantee Not Met

## Issue
An agent relies on a tool that advertises a specific accuracy figure for an ML-based capability — an entity-extraction API claiming 95% precision, a classification model claiming 90% F1 — and treats results as trustworthy at that advertised rate. In production, real-world accuracy often falls short of the marketed number because vendor benchmarks are measured on curated test sets that don't reflect the agent's actual input distribution. The agent, having no independent accuracy monitoring, keeps trusting outputs at the assumed rate and propagates a higher error rate downstream than anyone accounted for.

**Frequency**: Common

**Symptoms**
- Downstream decisions based on the tool's output are wrong more often than the advertised accuracy would predict, discovered only through unrelated complaints or audits
- Accuracy varies significantly across different subsets of input data (certain document types, languages, or edge cases) in ways the single advertised aggregate figure obscures
- No internal process exists to sample and manually verify the tool's output against ground truth on an ongoing basis
- The vendor's accuracy claim, on close reading, is qualified by conditions ("under optimal conditions," "on our benchmark dataset") that don't match the agent's actual use case
- Errors cluster in specific categories (e.g., handwritten text, non-English documents, edge-case formats) that were underrepresented in the vendor's published benchmark

## Root Cause
Vendors typically measure and publish accuracy figures against a benchmark dataset chosen to showcase the model favorably — often cleaner, more standardized, or more aligned with the model's training distribution than a given customer's real-world input. An agent's actual data (messy real-world documents, adversarial or unusual inputs, domain-specific jargon, non-English content) can differ substantially from that benchmark distribution, and accuracy on out-of-distribution data is frequently and significantly lower than the headline figure. Because the agent has no mechanism to independently measure accuracy against its own data and ground truth, this gap between advertised and actual accuracy stays invisible — the agent just keeps trusting every result at face value, propagating a silently higher error rate than the accuracy figure would suggest.

## Example
```
1. A document-processing agent uses a vendor's OCR-plus-classification API advertised
   at "97% field-extraction accuracy," used to auto-populate expense-report fields from
   photographed receipts.
2. The vendor's 97% figure was measured on a benchmark set of clean, well-lit, printed
   receipts from major US retailers.
3. In production, roughly 30% of submitted receipts are handwritten, faded thermal-paper
   receipts, or photographed at an angle under poor lighting — a distribution the
   benchmark didn't represent.
4. Actual field-extraction accuracy on this real-world mix is closer to 78%, though
   no one has measured it, since the agent auto-populates fields and marks the task
   complete regardless of confidence.
5. Over several months, a growing number of expense reports contain silently incorrect
   amounts or vendor names, discovered only when finance's quarterly audit flags an
   anomalous rate of manually-corrected expense reports.
6. Retroactively sampling 200 processed receipts against manual review reveals the
   true 78% accuracy rate, far below the vendor's advertised figure.
```

## Statistics
| Finding | Context |
|---------|---------|
| Real-world accuracy for ML-based extraction/classification tools commonly falls 10-25 percentage points below vendor-advertised benchmark figures when applied to messier, more diverse production data | Reflects the general gap between curated benchmark distributions and real-world input diversity |
| A large majority of organizations deploying third-party ML APIs do not run any independent accuracy sampling against their own data, relying solely on the vendor's published figure | Consistent with accuracy validation being an easy step to skip during integration |
| Organizations that implement even lightweight periodic human-in-the-loop sampling (reviewing 1-5% of outputs) catch accuracy regressions substantially faster, often within days rather than months | By providing an independent, ongoing measurement rather than a one-time trust decision |

## Mitigations
1. **Independent accuracy sampling against your own data**: Periodically sample a statistically meaningful subset of the tool's outputs and manually verify against ground truth using data representative of actual production inputs, not the vendor's benchmark.
2. **Confidence-score-based routing**: Where the tool exposes a confidence score, route low-confidence outputs to human review rather than auto-accepting every result at the same trust level, since accuracy is rarely uniform across the confidence distribution.
3. **Segment accuracy measurement by input category**: Track accuracy separately for known input subtypes (document format, language, image quality) rather than trusting a single aggregate figure, since error rates often concentrate in specific underrepresented categories.
4. **Downstream error-detection signals**: Build lightweight sanity checks on the tool's output (range checks, cross-field consistency, format validation) that can catch a subset of errors even without full ground-truth comparison.
5. **Contractual accuracy commitments with audit rights**: For high-stakes use cases, negotiate a contractual accuracy SLA (not just a marketing claim) with the vendor, including the right to audit against a jointly agreed sample.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tool.measured_accuracy_vs_advertised` | Accuracy measured via periodic sampling against ground truth, compared to the vendor's advertised figure | Alert when measured accuracy falls more than 10 percentage points below advertised |
| `tool.low_confidence_output_rate` | Share of outputs falling below a defined confidence threshold | Alert on a sustained upward trend, indicating input distribution drift |
| `downstream.manual_correction_rate` | Rate at which humans correct or override the tool's output downstream | Alert on a sustained increase over baseline |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Measured accuracy significantly below advertised | `measured_accuracy_vs_advertised` gap exceeds 10 points on a sampling run | High | Increase human review rate immediately, escalate to vendor with sampled evidence |
| Manual correction rate trending upward | `manual_correction_rate` rises significantly over a rolling 30-day window | Medium | Investigate for input distribution shift or vendor-side model regression |

## Related Patterns
- [Prediction Model Accuracy Regression](./prediction-model-accuracy-regression.md) - a related but distinct failure: accuracy that was previously adequate silently degrading after a vendor-side model update
- [Degraded Sla Not Communicated](./degraded-sla-not-communicated.md) - both involve a quality gap the agent has no direct signal to detect
- [Latency Sla Violation](./latency-sla-violation.md) - a parallel case of an advertised SLA figure (latency instead of accuracy) not holding up in practice
