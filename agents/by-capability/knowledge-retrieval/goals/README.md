# Knowledge Retrieval AI Agent Failures by Goal: 74 Patterns, Causes, and Fixes

**Knowledge Retrieval AI agents fail in 7 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 74 documented patterns across 7 goals; the most documented is [Knowledge Freshness](knowledge-freshness/) with 22.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## Knowledge Retrieval Goals

| Goal | When it fails | Patterns |
|---|---|---|
| [Answer Synthesis](answer-synthesis/) | When a model has the right retrieved context in front of it and still produces a wrong or misleading answer — drifting off the actual question, ignoring the context in favor of stale training data | 11 |
| [Citation Accuracy](citation-accuracy/) | When a citation exists and looks legitimate but doesn't actually do the job a citation is supposed to do — either the source doesn't exist at all | 7 |
| [Knowledge Freshness](knowledge-freshness/) | When an agent applies information that is true in isolation but wrong for the moment, scope, or domain-context it's actually needed in — a fact that was accurate a year ago | 22 |
| [Query Understanding](query-understanding/) | When an agent resolves what a user actually wants silently and incorrectly — guessing at an ambiguous term instead of asking, accepting a false premise embedded in the question | 8 |
| [Retrieval](retrieval/) | When the pipeline searches the wrong corpus, returns too few or too many documents, misses content trapped in tables or scanned images | 12 |
| [Retrieval Quality](retrieval-quality/) | When the pipeline finds documents that are topically plausible but wrong along a dimension similarity search doesn't measure — outdated, jurisdictionally inapplicable | 13 |
| [Retrieval Relevance](retrieval-relevance/) | When an agent selects a comparable or reference item using text-embedding similarity alone, and the selected item matches on language but not on the structured attributes | 1 |

**Total: 74 patterns**

## Frequently Asked Questions

### What is the difference between a fact-level distortion and a domain-level misapplication?

A single-fact distortion (like [Fact Inversion](knowledge-freshness/failures/fact-inversion.md) or [Fact Context Loss](knowledge-freshness/failures/fact-context-loss.md)) happens to one specific retrieved statement during retrieval or generation — the direction gets flipped, or a qualifying clause gets dropped. See [Knowledge Freshness](knowledge-freshness/).

### How is a reranker able to make retrieval quality worse instead of better?

Per [Reranking Degradation](retrieval-quality/failures/reranking-degradation.md), a cross-encoder or LLM-based reranker trained on general web data learns biases toward fluency, length, and typical document formatting that don't track actual task relevance — the documented example shows a reranker demoting a terse, correct technical spec sheet below a well-written but useless marketing document, a -27% Context Precision drop. See [Retrieval Quality](retrieval-quality/).

### How much does a wrong-corpus retrieval matter compared to an ordinary low-relevance result?

Considerably more in a multi-tenant or multi-product system — per [Wrong Corpus Retrieval](retrieval/failures/wrong-corpus-retrieval.md), retrieving from the wrong corpus can mean surfacing one customer's or one product line's documents to a different customer's query, a tenant-isolation violation and potential security/compliance incident rather than merely a quality miss. See [Retrieval](retrieval/).

## Related

- [Knowledge Retrieval overview](../)
- [All agent failure patterns](../../../)
