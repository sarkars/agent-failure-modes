# Transitive Tool Dependency Failure

## Issue
A tool the agent calls directly is itself built on top of one or more other tools or services — an aggregator API that queries several upstream data providers, a workflow-automation tool that calls out to a third-party integration, a wrapper library that proxies another vendor's SDK. When one of these indirect, transitive dependencies fails, the agent sees only a failure (or a degraded, incomplete, or wrong result) from the tool it called directly, with no visibility into the actual failing component, making the failure much harder to diagnose or route around than a failure in a tool the agent calls itself.

**Frequency**: Common

**Symptoms**
- A tool call fails or returns degraded output with an error message that doesn't identify the true root cause, sometimes citing only a generic "upstream error" or "internal error"
- The failure resolves on its own after some time with no action taken by the agent's own team, consistent with an issue in a dependency neither the agent nor its immediate tool provider directly controls
- The tool's own status page shows no incident, because the outage is in one of its own dependencies rather than the tool itself
- Diagnosing the failure requires contacting the tool vendor's support, who then has to trace the issue to their own upstream provider — a multi-hop diagnostic process the agent's operators have no direct visibility into

## Root Cause
Most tools an agent integrates with are themselves composed of other services, and this composition is usually opaque from the outside — the agent (and often its immediate operators) only sees the tool's public interface, not its internal dependency graph. When the agent's error handling is designed around "did tool X succeed or fail," it has no framework for reasoning about why X failed, because the actual cause may be two or three layers removed from anything the agent's own telemetry can observe. This differs from a simple tool outage in that even the tool's own operators may need time to isolate and communicate the root cause, meaning the information the agent would need to make an informed fallback decision (is this transient? is there a workaround? should I use an alternate tool?) is not available at the time the failure occurs.

## Example
```
An agent uses a "AddressValidate" tool to verify and normalize
shipping addresses before finalizing orders. AddressValidate's own
backend calls a national postal-service API to check address validity
against the authoritative postal database -- a dependency the agent's
team doesn't know about, since AddressValidate's own documentation
just describes it as "address validation with 99.9% accuracy."

The postal-service API undergoes unscheduled maintenance, returning
elevated 5xx errors for 3 hours. AddressValidate's own error handling
for this scenario is to return its own generic response: {"status":
"unable_to_validate", "confidence": "low"} rather than surfacing the
specific postal-API outage, because it doesn't want to expose its own
vendor relationships to callers.

The ordering agent, seeing "unable_to_validate" for what looks like a
tool-specific data-quality issue, falls back to its configured
behavior for that response: proceed with the unvalidated address as
entered by the customer. Over the 3-hour window, several dozen orders
ship with unvalidated addresses, some containing typos that would
normally have been caught, resulting in misdelivered packages days
later -- with no one on the ordering-agent team aware that the actual
cause was an outage two dependency hops away from anything they
directly integrate with.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 20-30% of third-party API/tool failures observed by downstream agent integrations originate in a dependency of the directly-called tool, not the tool itself | Typical range observed across API reliability postmortems involving layered service architectures |
| Time-to-root-cause for transitive dependency failures is substantially longer than for direct tool failures, often requiring vendor support escalation | Reported range across incident response teams working with third-party tool vendors |
| Tools that publish dependency-transparency information (which upstream providers they rely on) are a minority of commonly integrated SaaS/API tools | Estimated from surveys of API documentation practices across common categories (address validation, payments, identity, geocoding) |

## Mitigations
1. **Dependency-agnostic fallback design**: Design fallback behavior around the semantic meaning of a failure (e.g., "validation unavailable, proceed with caution") rather than assuming any given failure response reflects a specific, well-understood cause, and default to conservative behavior (flag for review) rather than silent pass-through when validation confidence is low.
2. **Vendor dependency disclosure requests**: When evaluating or contracting with a tool vendor, ask what upstream dependencies the tool relies on for critical functionality, and factor known fragile dependencies into risk assessment.
3. **Confidence-aware degraded-response handling**: Treat any response indicating reduced confidence or partial failure (not just outright errors) as a signal requiring escalation or a stricter fallback path, rather than treating it as equivalent to a full success.
4. **Multi-vendor diversification for critical paths**: For tool categories critical to correctness (address validation, identity verification, payment processing), maintain integration with more than one vendor with ideally non-overlapping upstream dependencies, to provide genuine redundancy.
5. **Status-correlation tooling**: Where possible, subscribe to status pages or incident feeds not just for directly-integrated tools but for major infrastructure providers those tools are known or suspected to depend on, to speed up root-cause attribution.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| degraded_confidence_response_rate | Rate of tool responses indicating reduced confidence or partial validation rather than a clean success | Alert if > 2x the tool's normal baseline |
| unresolved_generic_error_rate | Rate of tool failures with generic/unattributed error messages that can't be mapped to a known cause | Alert if > 1% |
| pass_through_on_degraded_response_count | Count of tasks that proceeded using unvalidated or low-confidence data due to a fallback triggered by a degraded tool response | Alert if > 0 for safety-critical task types |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Spike in low-confidence/degraded responses | A tool's degraded-response rate rises sharply above baseline | High | Suspect a transitive dependency issue, switch to stricter fallback (flag for manual review instead of pass-through), contact vendor support |
| Generic unattributed error spike | A tool's unresolved_generic_error_rate spikes with no corresponding incident on the tool's own status page | Medium | Escalate to vendor support to investigate potential upstream dependency issues |

## Related Patterns
- [Cascading External Failures](./cascading-external-failures.md) - a related mechanism where multiple directly-integrated tools share a transitive dependency, so one upstream outage cascades across several tools at once
- [Required Field Added To API](./required-field-added-to-api.md) - both involve failures originating outside the agent's direct control and outside its visibility until a call fails or degrades
