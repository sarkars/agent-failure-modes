# Geographic Data Access Restriction

## Issue
Data subject to geographic access or residency restrictions — most commonly EU personal data under GDPR, but also sector-specific rules like data-localization laws — is returned to an agent whose processing, storage, or invoking context sits outside the permitted region. This happens when the tool layer checks whether the requester is authorized in a general sense but doesn't verify that the specific data-residency or cross-border-transfer condition is also satisfied for that particular request.

**Frequency**: Occasional

**Symptoms**
- An agent instance running in a US region returns EU customer PII in response to a routine lookup, with no regional gate applied
- Data residency violations are only caught during compliance audits, not at request time
- The same tool behaves correctly when called from an EU-deployed agent instance but incorrectly from a globally-routed one
- Cross-border transfer logs show data movement that isn't backed by a valid transfer mechanism (e.g., standard contractual clauses) at the time of the agent's request
- Support or research agents "helpfully" aggregate data across regions in a single answer, flattening a distinction the compliance team intended to keep separate

## Root Cause
Geographic access restrictions are usually implemented as an infrastructure-level concern — data is stored in a regional database, and requests are expected to be routed to the correct regional instance. Agent architectures often break this assumption because a single agent deployment may be invoked from anywhere and may call a globally load-balanced or centrally-aggregated tool endpoint that doesn't itself track or enforce the requester's region against the data's residency requirement, treating regional storage as a deployment optimization rather than a hard compliance boundary.

## Example
```
A global customer-analytics platform stores EU customer data in an
EU-region database (for GDPR compliance) and US customer data in a
US-region database, with a unified "customer profile" tool that an
internal analytics agent calls regardless of where the agent itself is
deployed. The tool's query router picks the regional database based on
the customer's declared country field, but doesn't check where the
*requesting* agent instance or its invoking user is located, only
whether the credential presented is generally valid.

A US-based sales-operations agent, investigating a pattern across a
global account, calls the customer-profile tool for a contact who is an
EU resident. The tool returns the EU customer's PII to the US-based
agent instance, which logs the conversation (including the returned
PII) in a US-region logging system — completing a cross-border transfer
of EU personal data with no transfer mechanism in place and no consent
or contractual basis recorded for it.
```

## Statistics
| Finding | Context |
|---------|---------|
| Data-residency violations are among the more frequently cited findings in GDPR compliance audits of systems with global request routing | Common in enterprise GDPR compliance reviews |
| Unified/global data-access APIs are disproportionately implicated in residency violations compared to region-siloed APIs, since a single endpoint often serves requesters from any region | Typical of centralized platform architectures |
| A material share of cross-border transfer incidents are discovered through downstream artifacts (logs, caches, backups) created in the wrong region rather than through the originating query itself | Common in post-incident forensic reviews |

## Mitigations
1. **Requester-region and data-region joint enforcement**: Require every tool call touching residency-restricted data to validate both the data's region tag and the requester's/agent-instance's region, denying or redirecting the call if they don't satisfy an approved transfer path.
2. **Regional data isolation with no global aggregation endpoint**: Avoid building a single globally-callable tool over region-partitioned data; instead, deploy region-scoped tool instances that can only query their own regional store, making cross-region access a deliberate integration rather than a default capability.
3. **Transfer-mechanism gating**: When a legitimate cross-border transfer is necessary, require an explicit, logged transfer justification (e.g., standard contractual clause reference, documented legal basis) attached to the request before the tool releases the data.
4. **Downstream artifact region tagging**: Propagate the data's residency tag into every downstream artifact — logs, caches, conversation transcripts — so a compliance scan can detect region violations that occur after the initial query, not just at query time.
5. **Automated residency compliance testing**: Run scheduled synthetic queries from agent instances in each deployed region against known-tagged test records to verify residency enforcement holds across all routing paths, not just the primary one.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `cross_region_data_return_count` | Count of tool responses returning residency-restricted data to a requester outside the approved region without a logged transfer justification | Alert threshold: > 0 (any occurrence) |
| `untagged_transfer_artifact_count` | Count of downstream logs/caches containing residency-restricted data without a propagated region tag | Alert threshold: > 0 |
| `regional_canary_test_pass_rate` | Pass rate of scheduled synthetic residency-compliance queries across all deployed regions | Alert threshold: < 100% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unauthorized Cross-Border Transfer | Residency-restricted data returned to a requester/region without a valid transfer justification | P1 | Halt the tool path, notify legal/compliance, assess breach-notification obligations |
| Regional Canary Failure | Synthetic residency-compliance test fails in any deployed region | P1 | Page on-call, block the affected tool until enforcement is restored |

## Related Patterns
- [Data Classification Access Not Enforced](./data-classification-access-not-enforced.md) - geographic restriction is a specific instance of a classification/policy tag not being checked at serve time
- [Time-Based Data Access Not Enforced](./time-based-data-access-not-enforced.md) - both involve a compliance-driven access dimension (region, time) that the tool layer treats as metadata rather than a hard gate
- [Workspace Isolation Bypass](./workspace-isolation-bypass.md) - shares the pattern of a globally-routed endpoint undermining an intended partition
