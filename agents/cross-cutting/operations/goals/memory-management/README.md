# AI Agent Memory Management Failures: Summary Drift, Stale Retrieval, and Corruption

**Memory management failures happen when an agent's stored memory degrades or is retrieved badly: summaries drift, compaction drops key facts, stale entries win, indexes corrupt, and different agents hold contradictory versions.** These 22 patterns cover summarization, storage, and retrieval.

## Key Takeaways

- Summarizing and compacting memory can lose information, and repeated summarization degrades it further.
- Retrieval can fail by missing relevant memories, returning stale or contradictory ones, or returning too many.
- Storage problems include fragmentation, corrupted indexes, loss on reboot, and embedding-model changes that shift the vector space.
- Privacy boundaries are also at risk when memory scoped to one user surfaces in another's session.

## Patterns

| Pattern | What goes wrong |
|---|---|
| [Compaction Information Loss](failures/compaction-information-loss.md) | Memory Compaction Removes Critical Information |
| [Context Coherence Loss](failures/context-coherence-loss.md) | Over a long-running session, an agent's live working context (the conversation buffer, scratchpad, and accumulated tool outputs for the current run) comes to contain… |
| [Context Refresh Stale State](failures/context-refresh-stale-state.md) | Many agent architectures periodically "refresh" a block of context — re-fetching current system state (order status, ticket state, account balance, feature flags) and… |
| [Context Window Awareness Failure](failures/context-window-awareness-failure.md) | An agent has no internal tracking of how much of its context window is currently consumed, so as the session grows — tool outputs, retrieved documents, prior turns —… |
| [Memory Coherence Breakdown](failures/memory-coherence-breakdown.md) | Retrieved Memories Contradict Each Other |
| [Memory Corruption Detection Failure](failures/memory-corruption-detection-failure.md) | Individual entries in a persistent memory store can become corrupted — truncated writes from a crashed process, malformed JSON from a partial serialization, encoding… |
| [Memory Fragmentation](failures/memory-fragmentation.md) | As a memory store accumulates entries over months of operation — many small, partial, or redundant writes rather than clean consolidated records — the store fragments:… |
| [Memory Inconsistency Between Agents](failures/memory-inconsistency-between-agents.md) | When multiple agent instances or agent types share a common memory store — a customer-service agent and a billing agent both reading/writing facts about the same… |
| [Memory Interleaving Corruption](failures/memory-interleaving-corruption.md) | When two writes to the same memory record happen concurrently and the storage layer performs a non-atomic read-modify-write cycle (read current value, apply an update in… |
| [Memory Loss on Reboot](failures/memory-loss-on-reboot.md) | An agent accumulates state — working memory, in-progress task tracking, session-scoped facts — purely in the host process's memory (a Python dict, an in-memory cache, an… |
| [Memory Not Updated Stale Retrieval](failures/memory-not-updated-stale-retrieval.md) | A memory write completes and is acknowledged as successful, but the read path the agent actually queries — a separate search index, a cache layer, a denormalized read… |
| [Memory Priority Inversion](failures/memory-priority-inversion.md) | A shared memory store's write path — a queue, a lock, a single-threaded writer — has no concept of write priority, so a burst of low-priority writes (verbose interaction… |
| [Memory Privacy Boundary Violation](failures/memory-privacy-boundary-violation.md) | Memory intended to be scoped to a single user, tenant, or session leaks into a different user's, tenant's, or session's context — a shared vector index queried without a… |
| [Memory Retrieval Failures](failures/memory-retrieval-failures.md) | Relevant Memories Not Retrieved When Needed |
| [Memory Summarization Lossy](failures/memory-summarization-lossy.md) | When long-term memory is compacted to fit a fixed storage or retrieval-token budget — a periodic "condense this user's history into a compact profile" job, rather than… |
| [Retrieval Confidence Miscalibration](failures/retrieval-confidence-miscalibration.md) | A retrieval system's relevance or similarity score (cosine similarity, a reranker's confidence output, a hybrid search's combined score) is meant to signal how useful a… |
| [Retrieval Deduplication Failure](failures/retrieval-deduplication-failure.md) | A memory store accumulates near-duplicate entries — the same fact stated slightly differently across multiple writes, or the same document ingested more than once — and… |
| [Retrieval Index Corruption](failures/retrieval-index-corruption.md) | The retrieval index itself — the vector index's internal graph/tree structure, an inverted index's postings lists, or a search engine's shard metadata — becomes… |
| [Retrieval Temporal Ordering Failure](failures/retrieval-temporal-ordering-failure.md) | Retrieval ranks results primarily or purely by semantic similarity to the query, with no explicit weighting for recency, so when a memory store contains both an older… |
| [Semantic Drift in Embeddings](failures/semantic-drift-in-embeddings.md) | When the embedding model used to index a memory store is upgraded or swapped — a new model version, a provider change, a fine-tuning update — the vector space it… |
| [Summary Drift](failures/summary-drift.md) | Repeated Summarization Degrades Information Quality |
| [Working Memory Overflow](failures/working-memory-overflow.md) | Too Much Information Retrieved for Effective Use |

**Total: 22 patterns**

## How These Patterns Group

- **Summarizing and compacting:** [Compaction Information Loss](failures/compaction-information-loss.md), [Memory Summarization Lossy](failures/memory-summarization-lossy.md), [Summary Drift](failures/summary-drift.md)
- **Retrieval quality:** [Memory Retrieval Failures](failures/memory-retrieval-failures.md), [Memory Not Updated Stale Retrieval](failures/memory-not-updated-stale-retrieval.md), [Retrieval Confidence Miscalibration](failures/retrieval-confidence-miscalibration.md), [Retrieval Deduplication Failure](failures/retrieval-deduplication-failure.md), [Retrieval Temporal Ordering Failure](failures/retrieval-temporal-ordering-failure.md), [Working Memory Overflow](failures/working-memory-overflow.md), [Memory Priority Inversion](failures/memory-priority-inversion.md)
- **Coherence and consistency:** [Context Coherence Loss](failures/context-coherence-loss.md), [Context Refresh Stale State](failures/context-refresh-stale-state.md), [Context Window Awareness Failure](failures/context-window-awareness-failure.md), [Memory Coherence Breakdown](failures/memory-coherence-breakdown.md), [Memory Inconsistency Between Agents](failures/memory-inconsistency-between-agents.md), [Memory Interleaving Corruption](failures/memory-interleaving-corruption.md)
- **Storage and index health:** [Memory Fragmentation](failures/memory-fragmentation.md), [Memory Corruption Detection Failure](failures/memory-corruption-detection-failure.md), [Memory Loss on Reboot](failures/memory-loss-on-reboot.md), [Retrieval Index Corruption](failures/retrieval-index-corruption.md), [Semantic Drift in Embeddings](failures/semantic-drift-in-embeddings.md)
- **Privacy:** [Memory Privacy Boundary Violation](failures/memory-privacy-boundary-violation.md)

## When This Matters

- Sessions or memory stores run for weeks or months
- More than one agent or tenant shares a memory store
- You upgrade embedding models or rebuild indexes

## Frequently Asked Questions

### Why does my agent contradict itself in a long session?

See [context coherence loss](failures/context-coherence-loss.md) and [memory coherence breakdown](failures/memory-coherence-breakdown.md).

### Why did retrieval quality drop after an embedding model upgrade?

See [semantic drift in embeddings](failures/semantic-drift-in-embeddings.md).

### How can one user's memory leak into another's session?

Usually a missing scope filter on retrieval. See [memory privacy boundary violation](failures/memory-privacy-boundary-violation.md).

### What is the difference between memory management and memory safety?

This goal is about quality and consistency of memory. [Memory safety](../memory-safety/) is about what should and should not be remembered, recalled, or deleted.

## Related

- [All operations goals](../)
- [Operations overview](../../)
