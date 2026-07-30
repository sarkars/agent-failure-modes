# No Vendor Risk Control

## Issue: External model/tool vendors create unmanaged risk.

**Frequency**: Common

**Symptoms**
- Vendor outage/change/security issue affects agent.
- A model provider silently deprecates the pinned model version, breaking agent behavior with no advance warning reaching the team.
- A vendor discloses a security incident and the company cannot quickly determine what data was exposed or which agent functionality depends on the vendor.
- The agent goes fully down during a vendor outage because no fallback path was ever designed for that "critical" dependency.

**Root Cause**
External model/tool vendors create unmanaged risk.

**Example**
```
An agent relies on a single third-party embeddings API for its
retrieval pipeline, integrated years ago with no formal vendor risk
assessment and no fallback provider.

The vendor experiences a multi-hour outage during a regional
infrastructure failure. Because the agent's retrieval calls go directly
to the vendor SDK with no circuit breaker or fallback, the entire agent
becomes non-functional for the outage's duration — not just degraded,
but fully down.

Post-incident review finds the vendor was never classified as
critical-path despite the agent having no functional path without it,
and no one had reviewed the vendor's own uptime SLA or incident history
before relying on it for a production-critical function.
```

**Contributing Factors**
- Vendors are integrated based on functional fit alone, without a risk-tiering or security assessment step.
- No architectural fallback exists for vendors the agent cannot function without.
- Vendor API calls are made directly via SDK calls scattered through the codebase, with no abstraction layer to swap providers quickly.
- Vendor changelogs, deprecation notices, and security disclosures are not systematically monitored or routed to an owning team.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Circuit breaker failover | Simulated elevated error rate/latency from a critical vendor | Circuit breaker trips and traffic routes to fallback provider | Agent continues sending traffic to the failing vendor with no failover |
| Vendor risk assessment coverage | A newly integrated vendor | Risk assessment completed and vendor registered before go-live | Vendor is integrated into production with no recorded assessment |
| Security incident exposure assessment | Simulated vendor security incident disclosure | Data exposure and affected functionality are assessed within target time | Exposure assessment is not completed or takes far longer than target |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| circuit_breaker_failover_success_rate | 100% | Simulate vendor degradation and verify traffic reroutes to fallback within target time |
| vendor_assessment_precheck_rate | 100% | Audit recently integrated vendors for a completed risk assessment before go-live |
| incident_exposure_assessment_time | < 4 hours | Time a simulated vendor incident disclosure to a completed exposure assessment |

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
| vendor_risk_assessment_coverage_percent | < 100% |
| critical_vendor_fallback_coverage_percent | < 100% |
| vendor_incident_response_time_hours | > 24 hours |
| stale_vendor_assessment_count | > 0 for critical-tier vendors |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Critical Vendor Outage Detected | Critical-path vendor API error rate or latency breaches threshold | Critical |
| Vendor Security Incident Disclosed | Vendor reports a breach or critical vulnerability affecting shared data or integrated tooling | Critical |
| Vendor Assessment Overdue | Critical or high-tier vendor's risk assessment is past its review cadence | Warning |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
