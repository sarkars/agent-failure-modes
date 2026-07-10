# Scope Misunderstanding

## Issue: Agent Answers at Wrong Scope or Specificity

**Frequency**: Common

**Symptoms**
- Answer too broad when specific info needed
- Answer too narrow when overview requested
- Wrong product/version/context assumed
- Timeframe mismatch (current vs. historical)

**Root Cause**
Query doesn't specify scope, and model assumes wrong scope. Or scope is specified but not respected.

**Example**
```
Query: "What changed in the last update?"

Context: User is on mobile app
Retrieved: Web platform changelog (last update)

Agent: "The last update includes improved dashboard loading times, 
new keyboard shortcuts, and better multi-monitor support."

Reality: These are web features, not mobile app changes

Result: User looks for features that don't exist in their app
```

## Mitigation Strategies

### Prevention
1. **Query-Time Scope Classifier**: Extract product/version/platform/timeframe entities from the query using a lightweight classifier before retrieval runs. If scope can't be resolved with confidence, treat the query as ambiguous and route to clarification or user-context fallback rather than guessing. Trade-off: adds a classification step to every query's latency budget.
2. **Mandatory Scope Metadata Schema**: Require every document to carry scope tags (platform, version, region, timeframe) at ingestion; reject or quarantine untagged documents from scope-sensitive collections. This directly prevents the mobile/web changelog confusion in the example, but requires ongoing tagging discipline as content is authored.
3. **User-Context-First Scoping**: When user attributes are available (device type, plan, region), use them to auto-scope retrieval before falling back to LLM inference from query text alone, since the model has no way to know the user's platform unless it's supplied. Falls back to query-based inference only when user context is unavailable.

### Detection & Response
1. **Scope-Mismatch Correction Clustering**: Correlate follow-up messages like "that's not for my app" against the original query's inferred scope; feed clusters into a weekly scope-taxonomy review to find systemic gaps.
2. **Confirmation-Loop Analytics**: Track how often scope-confirmation prompts are shown versus skipped, and whether skipping correlates with negative feedback, to tune when confirmation is worth the added friction.
3. **Cross-Scope Citation Audit**: Sample transcripts where the retrieved document's scope tag differs from the user's inferred scope; flag as scope leakage and route to the retrieval team.

### Architecture Patterns
1. **Scope-Routing Layer**: Classify query scope first, then route to scope-partitioned indices (e.g., separate mobile/web collections); only fall back to an unscoped merged search if the scoped index returns nothing.
2. **Explicit Scope Disclosure in Generation**: Require the answer template to state scope ("For the mobile app...") so any residual mismatch is visible to the user instead of silently presented as universally applicable.
3. **Ambiguity-Triggered Clarification**: Use a confidence-below-threshold branch that asks "Are you asking about X or Y?" instead of guessing scope, mirroring disambiguation patterns used elsewhere in query understanding.

### Metrics
1. **scope_classification_accuracy**: Target: > 90%; Alert threshold: < 80%
2. **scope_mismatch_correction_rate**: Target: < 5% of sessions; Alert threshold: > 10%
3. **unscoped_query_rate**: Target: < 15%; Alert threshold: > 30%
4. **scope_confirmation_skip_rate**: Target: < 20%; Alert threshold: > 40%

### Alerts
1. **Scope Drift Spike** (P2): Condition - scope_mismatch_correction_rate exceeds 10% for a product/platform over 7 days. Action: audit scope tagging for that product's docs, review classifier confidence distribution.
2. **Untagged Document Ingestion** (P2): Condition - documents enter a scope-sensitive index without scope metadata. Action: block ingestion, route to a tagging queue before the document becomes retrievable.
3. **Cross-Platform Leakage** (P1): Condition - retrieved document scope contradicts detected user platform in > 5% of sessions. Action: escalate to the retrieval team, disable unscoped fallback until root cause is fixed.

## References

- [CMARix: RAG & AI Trust Statistics 2026](https://www.cmarix.com/blog/rag-ai-statistics/) - Scope detection challenges
- [Medium: 7 RAG Hallucination Root Causes](https://medium.com/@umesh382.kushwaha/why-your-rag-pipeline-hallucinates-7-root-causes-and-how-to-fix-them-1a04a84be7f5) - Context boundaries
