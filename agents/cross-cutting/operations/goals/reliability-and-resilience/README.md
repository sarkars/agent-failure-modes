# What Are the Most Common Reliability and Resilience Failures in AI Agents?

**Reliability and resilience fail when agents cannot continue operating in degraded mode when a dependency becomes unavailable, when a system that works well at pilot scale silently degrades accuracy without alerting operators, or when architecture assumes all components will always be available.** The 2 patterns documented here cover graceful degradation (what happens when a dependency fails) and scale degradation (what happens as data volume increases 1000x) — both are reliability issues invisible in development or pilot testing because development doesn't replicate production conditions: pilots run on small datasets with reliable infrastructure, while production simultaneously scales data, infrastructure, and concurrency, each multiplying the conditions under which graceful degradation matters.

## Key Takeaways

- 2 patterns are documented here, spanning graceful degradation when dependencies fail and accuracy degradation when corpus scale increases without architectural adjustment.
- Missing Graceful Degradation is the most severe in customer-facing scenarios: when one dependency (e.g., a search API) becomes unavailable, the entire agent fails instead of operating in reduced-capability mode, turning a single-service outage into a total service outage for users.
- RAG Scale Degradation is a silent failure: retrieval quality doesn't alert operators when it starts declining, so a system that works at 10K documents may be silently returning wrong answers at 10M documents by the time anyone notices.
- Both patterns share a root cause: architecture designed for happy path and happy scale, without explicit fallback paths, partitioning strategies, or scale testing before production deployment.

## Scope

- **Graceful Degradation and Fallback** — [Missing Graceful Degradation](failures/missing-graceful-degradation.md). When dependencies fail (external APIs, tool services, databases), the agent should continue operating in reduced mode rather than failing completely: fallback retrieval strategies, reduced-accuracy paths, partial responses, and explicit user messaging about capability loss.
- **Scale and Volume Resilience** — [RAG Scale Degradation](failures/rag-scale-degradation.md). Systems that work at pilot scale often collapse when data volume increases 1000x without matching architectural changes: flat vector indices that work at 10K documents hit latency cliffs at 100K, retrieval accuracy silently degrades without alerting, and end-to-end system accuracy drops as component errors compound across pipeline stages.

## When Reliability and Resilience Matter

- An agent depends on external services (APIs, tools, databases), where any single service outage should not cause total service failure to users.
- A system transitions from pilot (small corpus, controlled environment) to production (large corpus, real users, infrastructure variation), where architecture must be redesigned to handle 100-1000x scale increase in data and traffic.
- Accuracy or quality is critical enough that silent degradation (system returns wrong answers without alerting operators) is worse than partial degradation (system acknowledges capability loss and offers reduced-mode alternatives).

## Cross-Pattern Insight

Reliability and resilience failures are the result of testing in the wrong environment: pilots test happy-path scenarios at small scale with reliable infrastructure, so they never surface the failures that occur when a single dependency breaks or when data scales 1000x. The mitigation that recurs across both patterns is the same architectural move — design explicitly for failure modes that will occur in production (dependency failures, scale transitions, resource constraints) rather than assuming perfect availability: build fallback paths before production, partition and test at 10x and 100x intended scale before claiming scalability, and instrument accuracy metrics continuously so degradation is visible the moment it starts, not after users report wrong answers. No system designed only for happy path survives the journey from pilot to production.

## Frequently Asked Questions

### How do you design graceful degradation before knowing which dependencies will fail?
Per [Missing Graceful Degradation](failures/missing-graceful-degradation.md), identify all hard dependencies (external APIs, required tools, databases that have no fallback), then design fallback paths for each: local approximations, reduced-accuracy paths, cached results from previous requests, or explicit capability reduction and user messaging. Test each fallback path independently before production, not just in simulation — a cached fallback that hasn't been used in months is just dead code.

### At what corpus size does RAG scale degradation typically occur?
Per [RAG Scale Degradation](failures/rag-scale-degradation.md), naive flat-index retrieval starts hitting latency cliffs around 100K-500K documents and accuracy cliffs around 1M-10M documents, but exact thresholds depend on embedding model quality, reranking strategy, and inference infrastructure. Don't assume a system that works at 100K will work at 1M — test at 10x intended scale before considering the architecture proven.

### How do you catch scale degradation before users notice accuracy dropping?
Per [RAG Scale Degradation](failures/rag-scale-degradation.md), instrument end-to-end accuracy separately from component accuracy and alert when accuracy drops more than a configured threshold (e.g., alert if accuracy drops > 2% per month or < 90% absolute). If using retrieval + reranking + generation, measure accuracy at each stage independently so you can see whether degradation is in retrieval, reranking, or generation — degradation in retrieval signals you need hierarchical partitioning or vector-index optimization, not better generation.

### Is graceful degradation the same as fallback?
Graceful degradation includes fallback (trying an alternative when primary fails), but also reduced-mode operation, partial responses, and explicit user messaging. A fallback that returns results users don't know are degraded is hiding the failure, not handling it gracefully — tell users when capability is reduced.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Missing Graceful Degradation](failures/missing-graceful-degradation.md) | When a dependency (external API, tool, database) fails, the entire agent fails instead of operating in reduced mode with fallback paths |
| [RAG Scale Degradation](failures/rag-scale-degradation.md) | Retrieval accuracy silently drops and latency increases exponentially when corpus scales 1000x (10K → 10M documents) without hierarchical partitioning |

**Total: 2 patterns**

## Related Goals

- [Real-Time Performance](../real-time-performance/) — overlaps on latency degradation under scale and timeout configuration for fallback paths
- [Resource Consumption Management](../resource-consumption-management/) — scale degradation is often accompanied by resource exhaustion; monitoring one informs the other
- [Recovery Mechanisms](../recovery-mechanisms/) — graceful degradation requires recovery strategies that activate when primary paths fail
- [Observability Monitoring](../observability-monitoring/) — scale degradation is invisible without continuous accuracy and latency instrumentation
