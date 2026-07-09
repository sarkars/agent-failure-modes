# No Vendor Risk Control

## Issue: External model/tool vendors create unmanaged risk.

**Frequency**: Common

**Symptoms**
- Vendor outage/change/security issue affects agent.
- [Add more specific symptoms]

**Root Cause**
External model/tool vendors create unmanaged risk.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **Vendor Risk Tiering at Onboarding**: Classify every third-party model/tool/API vendor by risk tier (data sensitivity handled, criticality to agent function, vendor security posture) before integration, and require higher-tier vendors to pass a formal security/privacy assessment (SOC 2 review, data processing agreement, subprocessor disclosure) before go-live.
2. **Contractual Data-Handling Review**: Require legal/security review of vendor contracts specifically for AI-relevant terms — data retention by the vendor, whether vendor uses submitted data for model training, breach notification SLAs, and right-to-audit — before any sensitive data flows to that vendor's API.
3. **Fallback Provider Design**: For any vendor classified as critical-path (agent cannot function without it), require an architected fallback (alternate model provider, cached/degraded-mode behavior) so a vendor outage or deprecation doesn't produce a full agent outage.

### Detection & Response
1. **Vendor Health Monitoring**: Continuously monitor vendor API status pages, latency, and error rates for every integrated vendor, feeding into the agent's own health dashboard so a vendor-side degradation is detected as fast as an internal one.
2. **Vendor Change Notification Tracking**: Subscribe to vendor changelogs/deprecation notices and model version update announcements; route these to the owning team with an assessment deadline so silent vendor-side changes (model behavior drift, API deprecation) don't surface only as a production regression.
3. **Vendor Security Incident Response Linkage**: Maintain a process for ingesting vendor-reported security incidents (breach notifications, CVEs in vendor tooling) and immediately assessing exposure — what data was shared with that vendor, what agent functionality depends on it — rather than treating vendor incidents as someone else's problem.

### Architecture Patterns
1. **Vendor Risk Registry**: Maintain a registry mapping vendor → risk_tier → data_shared → contract_terms → last_assessment_date → fallback_provider, reviewed on a cadence proportional to risk tier (e.g., critical vendors reviewed quarterly).
2. **Abstraction Layer Over Vendor APIs**: Route all agent calls to external models/tools through an internal abstraction layer (not direct vendor SDK calls scattered through the codebase) so swapping to a fallback provider or pinning a version is a configuration change, not a code migration.
3. **Circuit Breaker for Vendor Calls**: Wrap vendor API calls in a circuit breaker that trips on elevated error rate/latency and routes to the fallback provider or a safe degraded mode, preventing a vendor outage from cascading into full agent failure.

### Metrics
1. **vendor_risk_assessment_coverage_percent**: Target: 100% of active vendors assessed and current; Alert threshold: < 100%
2. **critical_vendor_fallback_coverage_percent**: Target: 100% of critical-path vendors have a tested fallback; Alert threshold: < 100%
3. **vendor_incident_response_time_hours**: Target: exposure assessed within 4 hours of vendor incident disclosure; Alert threshold: > 24 hours
4. **stale_vendor_assessment_count**: Target: 0 assessments past their review cadence; Alert threshold: > 0 for critical-tier vendors

### Alerts
1. **Critical Vendor Outage Detected** (P1 - Critical): Condition - critical-path vendor API error rate or latency breaches threshold. Action: Trip circuit breaker to fallback provider, notify on-call, monitor for full recovery.
2. **Vendor Security Incident Disclosed** (P1 - Critical): Condition - vendor reports a breach or critical vulnerability affecting shared data or integrated tooling. Action: Immediately assess data exposure, notify security and legal, consider suspending the integration pending vendor remediation confirmation.
3. **Vendor Assessment Overdue** (P2 - Warning): Condition - critical or high-tier vendor's risk assessment is past its review cadence. Action: Notify vendor risk owner, prioritize reassessment, flag in vendor risk registry.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
