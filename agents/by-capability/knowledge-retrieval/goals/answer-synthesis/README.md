# What Are the Most Common Answer Synthesis Failures in AI Agents?

**Answer synthesis fails when a model has the right retrieved context in front of it and still produces a wrong or misleading answer — drifting off the actual question, ignoring the context in favor of stale training data, cherry-picking supporting evidence while dropping caveats, hallucinating details the context never contained, or losing a fact to over- or under-stuffed context.** All 11 patterns describe failures that happen after retrieval has already succeeded, which is what makes answer synthesis distinct from a retrieval problem: the correct information was there, and the generation step still didn't deliver it faithfully.

## Key Takeaways

- 11 patterns are documented here, and Confidence Miscalibration is explicitly linked to a universal cross-cutting pattern (`hallucination-confidence-miscalibration` in `cross-cutting/accuracy`), with sibling domain variants for document processing and vision.
- Context Window Saturation reports a measured quality curve: answer quality holds around 0.89-0.92 from 2k-8k tokens of context, then drops to 0.78 at 32k tokens and 0.61 at 80k tokens — stuffing more retrieved content into context degrades answer quality past a certain point rather than improving it.
- Hallucination Despite Context cites the same 17-33% hallucination rate documented in legal RAG tools even when retrieval-augmented — context reduces but does not eliminate fabrication, since the model can still fill gaps in incomplete context with plausible-sounding invented detail.
- Answer-Query Drift and Noise Corruption are measured separately in RAGAS evaluations: context-distracted responses occur in 25-35% of queries, and adding noise documents to otherwise-clean context produces a 20-40% quality drop — both are distinct from hallucination, since the answer can be fully grounded in context and still fail to be the right answer.

## Scope

- **Context Fidelity Failures** — [Context Ignored](failures/context-ignored.md), [Parametric Override](failures/parametric-override.md), [Hallucination Despite Context](failures/hallucination-despite-context.md). The model has correct retrieved context available but doesn't faithfully use it — falling back to generic training-data knowledge, overriding current context with a stale prior, or fabricating detail the context never contained.
- **Context Volume and Signal Management** — [Context Window Saturation](failures/context-window-saturation.md), [Noise Corruption](failures/noise-corruption.md), [Compression Information Loss](failures/compression-information-loss.md). Too much context, irrelevant context, or over-aggressively compressed context all degrade synthesis quality through different volume-management failures rather than a content-fidelity failure.
- **Query Alignment and Evidence Handling** — [Answer-Query Drift](failures/answer-query-drift.md), [Cherry-Picking](failures/cherry-picking.md), [Source Contradiction](failures/source-contradiction.md), [Synthesis Errors](failures/synthesis-errors.md). The answer is grounded in context but still goes wrong — addressing the wrong aspect of the query, presenting one-sided evidence, silently picking a side in a source conflict, or incorrectly combining facts from multiple entities.
- **Confidence Signaling** — [Confidence Miscalibration](failures/confidence-miscalibration.md). The model states an answer with the same declarative confidence regardless of how well the retrieved context actually supports it.

## When Answer Synthesis Matters

- A pipeline retrieves the correct supporting documents reliably, but users or evaluators report wrong or incomplete answers anyway — a signal the failure is downstream of retrieval, in synthesis itself
- Retrieved context is long, multi-document, or contains genuinely conflicting information (differing versions, differing sources) that the generation step must reconcile rather than just summarize
- The domain has known caveats, exceptions, or risk factors (medical, financial, legal) where an answer that's technically grounded but one-sided or overconfident carries real consequences

## Cross-Pattern Insight

Nearly every answer-synthesis pattern documents the same underlying tension: a language model is optimized to produce a fluent, complete-sounding, decisive answer, and that training pressure works against faithfully representing an incomplete, conflicting, or off-target set of retrieved context. Whether the failure looks like ignoring context in favor of a training-data prior, papering over a source conflict, dropping caveats to sound more decisive, or stating an answer with unwarranted confidence, the mechanism is the same optimization pressure showing up in different places along the synthesis pipeline. The mitigations that recur across the goal all push back against that pressure explicitly: query-decomposition and answer-relevancy verification steps that check the answer against the actual parsed query rather than trusting the generation step got it right, multi-source consensus checks that require disagreement to be surfaced rather than silently resolved, and structured response templates that mandate a caveats/limitations section rather than leaving completeness to the model's own judgment.

## Frequently Asked Questions

### What is the difference between hallucination despite context and confidence miscalibration?
[Hallucination Despite Context](failures/hallucination-despite-context.md) is about the content of the answer — the model states facts, numbers, or details that the retrieved context never contained. [Confidence Miscalibration](failures/confidence-miscalibration.md) is about the framing of the answer — the model states its answer (whether accurate or hallucinated) with the same declarative certainty regardless of how well-supported it actually is by the context.

### How do you tell answer-query drift apart from a retrieval failure?
Per [Answer-Query Drift](failures/answer-query-drift.md), retrieval succeeded — the relevant documents are in context — but the generated answer addresses a different aspect of the topic than what was actually asked (e.g. answering a question about card activation steps when the user asked whether personal expenses are allowed on a corporate card). If the retrieved context itself is wrong or missing, that's a retrieval-stage failure; if the context is right and the answer still misses the question, it's synthesis drift.

### Does more retrieved context always produce a better synthesized answer?
No — [Context Window Saturation](failures/context-window-saturation.md) documents the opposite past a certain point: quality holds fairly steady from 2k to 8k tokens of context, then degrades measurably at 32k and drops sharply by 80k tokens, driven partly by the "lost in the middle" effect where facts placed in the middle of a long context are recalled markedly less reliably than facts at the start or end.

### How do you stop a model from silently picking one side when sources disagree?
Per [Source Contradiction](failures/source-contradiction.md), add explicit conflict detection between retrieved passages before generation, and require the response to surface the disagreement (which sources say what, and why) rather than silently defaulting to whichever source happens to be retrieved first or scores marginally higher on relevance.

### Can cherry-picking be fixed just by telling the model to "be balanced"?
Prompting alone helps but the documented, more reliable fix in [Cherry-Picking](failures/cherry-picking.md) is structural: require extraction to explicitly populate a caveats/limitations/exceptions section as part of the response schema, rather than relying on the model to remember to volunteer qualifying information it has an incentive to omit for a cleaner-sounding answer.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Answer-Query Drift](failures/answer-query-drift.md) | Model generates an answer about the retrieved context's topic rather than the specific question actually asked |
| [Cherry-Picking](failures/cherry-picking.md) | Model selects supporting evidence while omitting caveats, exceptions, or contradicting information from the same context |
| [Compression Information Loss](failures/compression-information-loss.md) | Context summarization before synthesis drops specific numbers, dates, or exceptions the query needed |
| [Confidence Miscalibration](failures/confidence-miscalibration.md) | Model states an answer with the same declarative confidence regardless of how well the context actually supports it |
| [Context Ignored](failures/context-ignored.md) | Model responds from generic training knowledge instead of the specific retrieved context provided |
| [Context Window Saturation](failures/context-window-saturation.md) | Excess retrieved context dilutes model attention and degrades answer quality past an optimal context size |
| [Hallucination Despite Context](failures/hallucination-despite-context.md) | Model fabricates plausible-sounding detail (numbers, names, dates) not present in the retrieved context |
| [Noise Corruption](failures/noise-corruption.md) | Irrelevant retrieved documents mixed into context corrupt or distract from an otherwise correct answer |
| [Parametric Override](failures/parametric-override.md) | Model's training-data prior overrides current, correct information present in the retrieved context |
| [Source Contradiction](failures/source-contradiction.md) | Retrieved documents disagree and the model silently picks one without acknowledging or reconciling the conflict |
| [Synthesis Errors](failures/synthesis-errors.md) | Model incorrectly associates facts or attributes across multiple entities when combining multi-source context |

**Total: 11 patterns**

## Related Goals

- [Retrieval](../retrieval/) — the pipeline stage upstream of answer synthesis; several answer-synthesis patterns assume retrieval already succeeded
- [Citation Accuracy](../citation-accuracy/) — a deeper treatment of the attribution failures that often accompany cherry-picking and source contradiction
- [Query Understanding](../query-understanding/) — Answer-Query Drift's generation-side symptom traces back to the same underspecified or fragmented queries documented there
