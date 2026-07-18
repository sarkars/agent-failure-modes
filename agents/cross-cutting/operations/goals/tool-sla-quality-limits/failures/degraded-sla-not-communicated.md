# Degraded SLA Not Communicated

## Issue
A tool vendor experiences an internal incident — an overloaded backend, a partial regional outage, a resource-constrained fallback mode — and quietly degrades service quality (higher latency, lower accuracy, reduced feature availability) to keep the system technically "up," without posting to a status page or notifying API consumers. The agent has no explicit signal that anything has changed; it just observes worse results and, absent any error or status indicator, has no basis to distinguish a genuine data or logic problem from a vendor-side degradation it should be working around.

**Frequency**: Occasional

**Symptoms**
- Output quality or latency degrades noticeably with no corresponding change in the agent's own code, input data, or configuration
- The tool continues returning HTTP 200 success responses throughout, so no error-rate-based alerting fires
- The degradation resolves itself after some hours or days with no announcement, matching the typical lifecycle of a vendor-side incident that was never publicly disclosed
- Vendor's public status page shows "all systems operational" throughout the period, contradicted by the agent's own observed quality metrics
- Support tickets filed during the degradation window get a response only after the vendor's internal incident is independently resolved, often with no acknowledgment that the issue occurred at all

## Root Cause
Vendors facing internal capacity problems or partial outages sometimes choose (or their systems automatically choose, via load-shedding logic) to preserve uptime and response-success-rate metrics by silently degrading quality — using a smaller or cheaper model variant, skipping optional processing steps, applying more aggressive caching or truncation — rather than returning errors that would show up clearly in status pages and SLA reporting. This is a rational choice from the vendor's perspective (a slightly worse but successful response is often preferable to a hard failure) but it means the primary signal an agent typically monitors — HTTP status codes and error rates — never fires, because nothing actually errored. Detecting degradation requires monitoring output quality directly, which most agents don't do since it's harder to instrument than error rates.

## Example
```
1. An agent uses a vendor's real-time translation API to translate customer support
   messages, normally achieving consistently fluent, accurate translations.
2. The vendor experiences a regional GPU capacity shortage during a traffic spike and,
   rather than returning errors, automatically routes a portion of requests to a smaller,
   faster fallback model with noticeably lower translation quality, without updating
   their public status page (which only tracks uptime, not quality) or notifying API
   consumers.
3. For six hours, the agent's translation requests continue succeeding with HTTP 200,
   but roughly 40% of them (the ones routed to the fallback model) produce translations
   with noticeably more grammatical errors and occasional mistranslations of key terms.
4. The agent has no quality-monitoring signal beyond "did the call succeed," so nothing
   flags the degradation internally.
5. Customer support agents relying on the translated messages start noticing confusing
   or nonsensical translations and escalate as a possible bug in the support tool itself.
6. It takes escalation to the vendor's support team, and their internal incident
   postmortem (shared only after the fact), to confirm the six-hour silent quality
   degradation actually happened.
```

## Statistics
| Finding | Context |
|---------|---------|
| Silent quality degradation during vendor-side incidents is a recognized failure mode particularly for ML-backed APIs, where load-shedding to a cheaper model preserves uptime metrics at the cost of unreported quality loss | Consistent with vendors optimizing for the metrics that appear on their status pages |
| Teams that instrument output-quality monitoring (beyond simple success/error rate) detect degradation incidents substantially faster, often within the hour, versus days for teams relying only on status-page monitoring | Because quality metrics are a direct signal where error rate is not |
| Vendor status pages predominantly track availability/uptime and rarely include a quality or accuracy dimension, meaning "all systems operational" provides little assurance about output quality specifically | Reflects the industry-standard scope of most public status page tooling |

## Mitigations
1. **Independent output-quality monitoring**: Instrument metrics that measure the actual quality characteristics of the tool's output (translation fluency scores, extraction confidence, response length/structure anomalies) rather than relying solely on HTTP success/error rates.
2. **Canary comparison against a stable baseline**: Periodically run a fixed, known set of test inputs through the tool and compare current output to a historical known-good baseline, flagging drift even when nothing has technically errored.
3. **Don't trust status pages as a quality signal**: Treat vendor status pages as an availability indicator only, and build independent detection for quality-specific degradation rather than assuming "all systems operational" means output quality is normal.
4. **Contractual or informal escalation channel for quality issues**: Establish a direct escalation path with the vendor (account manager, dedicated support tier) specifically for reporting suspected silent degradation, since it often isn't visible in the vendor's own public tooling.
5. **Graceful fallback on detected quality drops**: When quality monitoring detects a significant drop, automatically route to a secondary vendor or fall back to a more conservative/manual process until quality is confirmed restored.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tool.output_quality_score_vs_baseline` | Current output quality (via canary tests or sampled scoring) compared to a rolling historical baseline | Alert when current score drops more than 15% below baseline |
| `tool.response_characteristic_anomaly_rate` | Rate of responses with anomalous characteristics (unusual length, structure, or confidence distribution) vs. historical norms | Alert on a sustained shift from baseline |
| `vendor.status_page_uptime_vs_internal_quality_signal` | Divergence between vendor-reported uptime (typically 100%) and internally measured quality metrics | Track as a diagnostic signal during suspected incidents |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Quality score drop with no status page incident | `output_quality_score_vs_baseline` drops significantly while vendor status page shows all-clear | High | Activate fallback path, escalate directly to vendor support for confirmation |
| Sustained response-characteristic anomalies | `response_characteristic_anomaly_rate` elevated for over 30 minutes | Medium | Investigate for silent vendor-side degradation before assuming an internal bug |

## Related Patterns
- [Accuracy Guarantee Not Met](./accuracy-guarantee-not-met.md) - both involve a gap between assumed and actual output quality, but this pattern is specifically about a transient, incident-driven degradation
- [Prediction Model Accuracy Regression](./prediction-model-accuracy-regression.md) - a related but permanent version of undetected quality loss, following a model update rather than a transient incident
- [Latency Sla Violation](./latency-sla-violation.md) - latency-focused degradation often accompanies or precedes quality degradation during the same underlying vendor incident
