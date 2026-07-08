# Wrong Corpus Retrieval

## Issue: Agent searches the wrong knowledge base or tenant corpus.

**Frequency**: Common

**Symptoms**
- Retrieved docs unrelated to user/account/product.
- [Add more specific symptoms]

**Root Cause**
Agent searches the wrong knowledge base or tenant corpus.

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
1. **Intelligent Corpus Routing**: Implement classifier that routes query to appropriate corpus before retrieval. Classify based on: keywords, user_context (product_type, account_type, region). Example: 'What's the return policy?' → route to 'company_policies' corpus, NOT 'tech_docs'.
2. **Tenant Isolation Tests**: For multi-tenant system, create comprehensive test suite verifying queries only retrieve documents from authorized tenant. Example: 'Tenant_A user should not see Tenant_B docs'. Run tests in CI/CD.
3. **Corpus Metadata Tagging**: Tag all documents with corpus_id/name at indexing time. Before retrieval, validate expected_corpus. After retrieval, verify retrieved_docs match expected_corpus. Flag corpus mismatches.

### Detection & Response
1. **Wrong Corpus Retrieval Detection**: Compare retrieved_corpus against expected_corpus (based on query intent). Flag mismatches. Log: query, expected_corpus, retrieved_corpus, mismatch_severity.
2. **Tenant Boundary Violation Detection**: For multi-tenant retrieval, verify all results belong to querying tenant. Any cross-tenant result = instant alert. Log: query, query_tenant, retrieved_tenant, doc_id.
3. **User Feedback Corpus Misalignment**: When user marks result as irrelevant, check if result came from wrong corpus. Bucket irrelevant results by corpus to identify patterns.

### Architecture Patterns
1. **Query-to-Corpus Classifier**: Train classifier on historical queries mapped to correct corpus. Deploy as pre-retrieval step. Classifier outputs: predicted_corpus + confidence_score. Low confidence → escalate to manual routing.
2. **Isolated Corpus Indices**: Maintain separate indices per corpus/tenant. Queries only search assigned index. No cross-index queries. Explicit policy: no cross-corpus search.
3. **Corpus Access Control Middleware**: Middleware between query and indices. Verifies tenant/user has permission to query corpus. Blocks unauthorized corpus access. Logs all access attempts.

### Metrics
1. **wrong_corpus_retrieval_rate_percent**: Target: 0%; Alert threshold: > 0%; Any wrong-corpus is critical
2. **tenant_isolation_violation_rate_percent**: Target: 0%; Alert threshold: > 0%; Cross-tenant leaks are security incidents
3. **corpus_routing_accuracy_percent**: Target: 99.5%; Alert threshold: < 98%; Routing classifier accuracy
4. **cross_tenant_result_attempts_per_month**: Target: 0; Alert on any attempts
5. **corpus_classifier_precision_percent**: Target: > 98%; Alert threshold: < 95%

### Alerts
1. **Wrong Corpus Retrieved** (P1 - Critical): Condition - retrieved_corpus ≠ expected_corpus. Action: Block results, audit corpus routing, manual query reclassification, investigation.
2. **Tenant Boundary Violation** (P1 - Critical): Condition - single document from wrong tenant in results. Action: Immediate incident response, security alert, tenant isolation audit, data loss investigation.
3. **Corpus Routing Failure** (P1 - Critical): Condition - query cannot be classified to corpus (low confidence). Action: Route to manual review, escalate to content team, update classifier training data.

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

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
