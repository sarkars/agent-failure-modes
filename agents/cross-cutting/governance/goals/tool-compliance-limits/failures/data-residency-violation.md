# Data Residency Violation

## Issue
Data subject to a jurisdictional residency requirement (e.g. EU customer data must stay within the EU, certain government data must stay within national borders) passes through a tool call — an LLM inference API, a third-party enrichment service, a logging pipeline, a backup destination — that processes or stores it in a different region than required, because the tool's regional routing wasn't configured or verified against the residency requirement at integration time.

**Frequency**: Occasional

**Symptoms**
- A tool's default API endpoint routes to a specific region (often US) regardless of where the calling agent or its data subjects are located
- Logging or observability pipelines forward request/response payloads (including any embedded PII) to a centralized, single-region log store regardless of data origin
- Third-party tools integrated into the agent's toolchain don't expose or document their data-processing region, and no one verified it before integration
- Backup or disaster-recovery replication copies data cross-region as a platform default, without residency-aware configuration
- A data-flow map, if one exists, doesn't match the actual regions traffic is observed passing through in network/API logs

## Root Cause
Modern agent toolchains are typically composed of multiple third-party and internal services, each with its own default region and routing behavior, and residency requirements are a data-governance concern that has to be actively enforced against every one of those services individually. Without a systematic review of each tool's actual data-processing region — and without infrastructure-level enforcement (regional endpoint pinning, geo-fencing) — the default behavior of any given service (often "route to the nearest or cheapest region, usually US") silently overrides the residency requirement, and the violation is invisible unless someone traces the actual network path the data took.

## Example
```
1. A customer-support agent serving EU customers is required, under the company's data-processing
   agreement with those customers, to keep all customer data processing within EU infrastructure.
2. The agent's toolchain includes a third-party sentiment-analysis API integrated to help triage tickets.
   The integration was set up using the vendor's default global endpoint, which routes requests to
   whichever region has capacity, commonly a US data center.
3. No one on the integration team checked the vendor's regional processing options or residency
   guarantees before wiring the tool into the agent's pipeline, because the integration was treated as a
   routine API addition rather than a data-governance decision.
4. Every EU customer ticket processed through the agent has its content sent to the sentiment-analysis
   API's US endpoint for analysis, in violation of the EU data-residency commitment.
5. The violation is discovered months later during a data-processing audit that traces the actual network
   destinations of API calls made by the agent's toolchain.
```

## Statistics
| Finding | Context |
|---------|---------|
| Third-party tool integrations added after an agent's initial data-residency review are a common source of undetected residency violations | Common finding in cross-border data-flow audits |
| Default/global API endpoints are frequently used in integrations without explicit regional configuration, even when the calling application has residency requirements | Typical pattern in vendor integration reviews |
| Explicit regional endpoint pinning combined with automated network-destination auditing catches most of these violations before or shortly after they occur | Standard remediation for residency-compliance findings |

## Mitigations
1. **Maintain a data-flow map covering every tool in the agent's toolchain**: Document the actual processing region for each internal and third-party service the agent calls, and require this documentation before any new tool is added.
2. **Pin API calls to region-specific endpoints where residency is required**: Configure tools serving residency-constrained data to use the vendor's region-specific endpoint explicitly, never a global/default endpoint whose region isn't guaranteed.
3. **Geo-fence outbound traffic at the network layer as defense-in-depth**: Use network policy to block or flag outbound calls carrying residency-constrained data toward endpoints outside the approved region, independent of application-level configuration.
4. **Require a residency review as part of new-tool onboarding**: Add explicit confirmation of a vendor's data-processing region to the checklist for integrating any new tool that will handle residency-constrained data.
5. **Audit actual network destinations against the data-flow map on a recurring schedule**: Periodically compare observed API call destinations in network/API logs against the documented data-flow map to catch drift or undocumented tools.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| out_of_region_calls_with_constrained_data | Outbound API calls carrying residency-constrained data destined for a non-approved region | > 0 |
| unmapped_toolchain_services | Tools in active use that don't appear in the documented data-flow map | > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Residency-constrained data routed out of region | Network monitoring detects constrained data sent to an endpoint outside the approved region | Critical | Block the call path immediately, assess scope of exposure, notify legal/compliance |
| New tool added without residency review | A new tool begins receiving traffic without an entry in the data-flow map | High | Suspend the integration pending a residency review |

## Related Patterns
- [Data Deletion Compliance](./data-deletion-compliance.md) - both stem from an incomplete inventory of every downstream system the agent's data actually flows through
- [PII Retention Policy Violation](./pii-retention-policy-violation.md) - both are data-governance requirements that must be enforced consistently across every tool in the chain, not just the primary store
- [Audit Logging Not Enforced](./audit-logging-not-enforced.md) - logging pipelines are themselves a common, overlooked vector for residency violations when log destinations aren't region-aware
