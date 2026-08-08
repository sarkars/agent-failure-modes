# Wrong Corpus Retrieval

## Issue: Agent searches the wrong knowledge base or tenant corpus.

**Frequency**: Common

**Symptoms**
- Retrieved docs unrelated to user/account/product.
- Retrieved documents belong to a different product line or a different tenant's knowledge base than the one the querying user is scoped to.
- Answer blends terminology/policies from a different corpus (e.g., a different product's pricing) with the user's actual product context.
- A cross-tenant document appears in results with no access-control rejection, exposing another customer's content.

**Root Cause**
This happens because multiple products' or tenants' documents live in a single shared vector index with no mandatory corpus or tenant filter enforced at query time, so semantically similar phrasing across unrelated corpora can win the ranking regardless of which product the user actually belongs to. There is no pre-retrieval step that classifies the query and routes it to the correct corpus before search runs, and because corpus/tenant metadata is attached inconsistently at ingestion, even a filter that does exist can silently miss documents it should have caught. Access control is also enforced only at the application or display layer rather than at the index itself, so the wrong-corpus document is retrieved and scored as a real candidate well before any permission check would have hidden it.

**Example**
```
A support agent for "Product A" (a project management tool) is asked "How do I reset
my password?" The retrieval system searches a shared vector index that contains docs
for both Product A and Product B (a separate CRM product) with no corpus/tenant filter
applied to the query. Because "password reset" phrasing is nearly identical across
both products' help docs, the top result comes from Product B's corpus, and the agent
gives Product B's reset instructions (different URL, different support contact) to a
Product A user.
```

**Contributing Factors**
- Shared vector index across multiple products/tenants with no mandatory corpus or tenant_id filter applied at query time.
- No pre-retrieval query classification step to route the query to the correct corpus before search executes.
- Corpus/tenant metadata attached inconsistently at ingestion, so filtering by corpus_id silently misses some documents.
- Access-control checks enforced only at the application/display layer rather than at the index/query layer, so wrong-corpus documents are retrieved even if later hidden.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Cross-product leakage | Query phrased identically to a query valid in two different product corpora, run against Product A's scoped session | Results come only from Product A's corpus | Results include documents from Product B's corpus |
| Tenant isolation breach | Query run under Tenant A's session, corpus contains Tenant B's documents with similar content | No Tenant B documents appear in results | At least one Tenant B document appears in retrieved results |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| wrong_corpus_retrieval_rate_percent | 0% | Run tenant/corpus isolation test suite in CI, measure % of test queries that return any document tagged with the wrong corpus_id |

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
| wrong_corpus_retrieval_rate_percent | > 0% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Cross-Corpus Retrieval Detected | Any retrieved document's corpus_id does not match the query's scoped corpus/tenant | High |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
