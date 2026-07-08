# Wrong Retrieval Channel

## Issue: Agent searches public web instead of internal/private source or vice versa.

**Frequency**: Common

**Symptoms**
- Source does not match requested data class.
- [Add more specific symptoms]

**Root Cause**
Agent searches public web instead of internal/private source or vice versa.

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
1. **Data-Classification-Driven Retrieval Routing**: Tag every query with a data-sensitivity/domain class (public-general, internal-proprietary, customer-PII, regulated) using a trained classifier, and enforce a fixed mapping from class to permitted retrieval channel at the routing layer — proprietary/PII queries are structurally disallowed from reaching the public web search tool, and vice versa for general public-knowledge queries that shouldn't burn internal-index quota or expose internal query patterns externally.
2. **Dual-Index Retrieval Abstraction**: Expose internal and external search as two distinct, separately-scoped tools rather than a single ambiguous "search" tool the model must disambiguate by judgment alone; the tool name/description itself removes the ambiguity that leads to misrouting.
3. **Channel Allowlist per Task Type**: For task types with known data requirements (e.g., "look up customer account status" is always internal-only, "summarize competitor pricing" is always public-only), hardcode the allowlist at the task-template level so channel selection isn't re-derived by the model on every call.

### Detection & Response
1. **Source-vs-Data-Class Audit**: Continuously compare the classified sensitivity of each query against the channel actually used to answer it; any internal/private-classified query answered via public web search (or public-only query routed to internal indices unnecessarily) is logged as a policy violation.
2. **Private-Data Leakage Detector**: Specifically scan outbound public-search queries for internal identifiers, customer names/PII, or proprietary terminology; any match indicates a wrong-channel routing that risks leaking private data to an external service and is treated as a security event, not just a quality issue.
3. **Channel-Routing Classifier Confidence Monitoring**: Track the confidence distribution of the routing classifier over time; a drift toward more low-confidence routing decisions signals the classifier needs retraining on new query patterns before misroutes accumulate.

### Architecture Patterns
1. **Retrieval Router/Gateway**: A dedicated routing service inspects each query's classification before any retrieval tool is dispatched and enforces the channel allowlist, rejecting or rerouting calls that violate the policy rather than trusting the agent's inline tool choice.
2. **Separate Internal/External Search Endpoints**: Internal knowledge base search and public web search are implemented as fully separate tools with distinct names, descriptions, and access controls, eliminating the single-tool ambiguity that causes misrouting in the first place.
3. **Policy Engine with Audit Logging**: A policy engine maintains the domain-class-to-channel mapping as versioned configuration, consulted by the router on every call, with every routing decision logged for compliance audit and periodic policy review.

### Metrics
1. **channel_misroute_rate**: Target: < 1% of queries; Alert threshold: > 3%
2. **internal_data_to_public_channel_leak_count**: Target: 0; Alert threshold: any occurrence
3. **retrieval_policy_violation_rate**: Target: < 1%; Alert threshold: > 2%
4. **routing_classifier_confidence_p50**: Target: > 0.9; Alert threshold: < 0.75 sustained over a week

### Alerts
1. **Private Data Sent to Public Channel** (P1 - Critical): Condition - leakage detector matches PII/proprietary content in an outbound public search query. Action: Block the call, alert security/privacy team, audit affected session for further exposure.
2. **Unauthorized Internal Source Use for Public Query** (P2 - Warning): Condition - a public-only-classified query is routed to internal indices without policy justification. Action: Review classifier decision, correct routing policy if misconfigured.
3. **Routing Classifier Confidence Drop** (P2 - Warning): Condition - routing_classifier_confidence_p50 falls below threshold. Action: Schedule classifier retraining, increase human-review sampling rate in the interim.

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
