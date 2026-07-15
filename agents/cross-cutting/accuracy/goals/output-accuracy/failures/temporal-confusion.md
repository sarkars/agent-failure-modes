# Temporal Confusion

## Issue: Agent Confuses Timeframes or Uses Outdated Information

**Frequency**: Common

**Symptoms**
- Agent uses training data as current fact
- Past events described as ongoing
- Future events described as completed
- Version numbers, dates, or status outdated

**Root Cause**
LLMs have knowledge cutoffs and don't inherently track time. They may present training data as current truth even when information has changed.

**Example**
```
User: "Who is the CEO of Example Corp?"

Agent: "John Smith is the CEO of Example Corp. He's been leading 
the company since 2019."

Reality: John Smith resigned in 2024. Jane Doe is current CEO.

Result: User acts on outdated information
```

## Mitigation Strategies

### Prevention
1. **Volatile-fact classification with mandatory real-time retrieval**: Classify query targets known to change over time (executive roles, prices, statuses, versions) and require real-time retrieval for these rather than answering from parametric knowledge — directly prevents the example, where "who is the CEO" should trigger a live lookup instead of relying on a training-data snapshot from before the 2024 resignation. Trade-off: real-time retrieval adds latency and requires reliable, current data sources for every volatile-fact category the agent might be asked about.
2. **Knowledge-cutoff disclosure on time-sensitive answers**: When the agent cannot verify a fact against a current source, state the training cutoff and flag the answer as potentially outdated rather than presenting it with unqualified confidence ("He's been leading the company since 2019"). Trade-off: reduces perceived confidence/authority of responses even when the underlying fact happens to still be correct.
3. **Recency-signal requirement in retrieved context**: Require retrieved passages used to answer time-sensitive queries to carry an explicit as-of date, and surface that date to the user rather than presenting retrieved information as unconditionally current. Trade-off: requires the retrieval corpus to be consistently timestamped, which many source documents don't provide natively.

### Detection & Response
1. **Authoritative-source comparison sampling**: Periodically sample agent answers to volatile-fact categories (leadership, pricing, product versions) and compare against a current authoritative source; a mismatch (as in the CEO example) is a direct, checkable detection signal.
2. **Outdated-information correction tracking**: Log user corrections specifically tied to outdated facts ("that's no longer true," "they left the company") and track rate and category, since these cluster around specific volatile-fact types that need tighter real-time coverage.
3. **Recent-event query monitoring**: Track the volume and pattern of queries about entities or topics with a known recent change (e.g., a company that just had a leadership change) to proactively identify where the agent's knowledge is most likely to be stale before users report it.

### Architecture Patterns
1. **Real-time retrieval layer for volatile-fact categories**: Maintain a live-updated data source (API, scraped feed, or curated database) for known volatile categories and route matching queries through it instead of the base model's parametric knowledge. Deployment consideration: requires ongoing data pipeline maintenance and a way to keep the volatile-category list current as new fact types prove unstable.
2. **Timestamp-tagged retrieval index**: Tag every document in the retrieval corpus with its effective/as-of date, and prefer or require the most recent tagged document when multiple conflicting versions exist. Deployment consideration: needs disciplined document ingestion practices to capture accurate as-of dates, which many existing corpora lack retroactively.
3. **Cutoff-aware response gating**: Build an explicit check that compares a query's implied time-sensitivity against the model's knowledge cutoff and routes to real-time retrieval or a hedged response when the gap is material. Deployment consideration: requires reliably estimating a query's time-sensitivity, which is itself a nontrivial classification problem for ambiguous queries.

### Metrics
1. **volatile_fact_accuracy_rate**: % of sampled volatile-fact answers matching current authoritative sources; target > 95%; alert if < 85%.
2. **outdated_info_correction_rate**: User corrections tied to outdated facts per 1,000 relevant queries; target < 5; alert if > 20.
3. **real_time_retrieval_coverage**: % of volatile-fact-category queries that triggered real-time retrieval rather than parametric-only answering; target > 90%; alert if < 70%.
4. **unhedged_stale_answer_rate**: % of answers on volatile topics delivered without cutoff disclosure or hedging when real-time retrieval wasn't available; target < 5%; alert if > 15%.

### Alerts
1. **Volatile Fact Accuracy Drop** (P2): Condition — volatile_fact_accuracy_rate falls below 85% for a fact category (e.g., executive roles). Action: audit the real-time retrieval source for that category for staleness or outage, and add cutoff disclosure to affected responses in the interim.
2. **Real-Time Retrieval Coverage Gap** (P2): Condition — real_time_retrieval_coverage drops below 70% for a volatile-fact category. Action: investigate retrieval pipeline failures or missing routing rules for that category.
3. **Outdated Info Correction Spike** (P3): Condition — outdated_info_correction_rate exceeds 20 per 1,000 queries for a specific entity/topic. Action: manually verify and refresh the source data for that entity and confirm the routing rule is triggering correctly.

---

## References

- [Atlan: LLM Hallucinations 2026](https://atlan.com/know/llm-hallucinations/) - Overview of temporal hallucination patterns in LLMs
- [Medium: 7 RAG Hallucination Root Causes](https://medium.com/@umesh382.kushwaha/why-your-rag-pipeline-hallucinates-7-root-causes-and-how-to-fix-them-1a04a84be7f5) - Analysis of time-related hallucination causes in RAG systems
