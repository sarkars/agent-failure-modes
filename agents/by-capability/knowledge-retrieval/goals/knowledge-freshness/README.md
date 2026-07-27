# What Are the Most Common Knowledge Freshness Failures in AI Agents?

**Knowledge freshness fails when an agent applies information that is true in isolation but wrong for the moment, scope, or domain-context it's actually needed in — a fact that was accurate a year ago, a rule correctly quoted but misapplied to a case its exception covers, or a single retrieved sentence stripped of the qualifier that made it safe to act on.** The 22 patterns documented here span three distinct levels of the same underlying problem: domain-level judgment that a generic retrieval pipeline doesn't encode, single-fact distortions introduced during retrieval or generation, and system-level architecture gaps — no expiration mechanism, no update pipeline, no source-trust weighting — that make the other two levels of failure more likely. None of the 22 patterns require a hallucinated fact; every one is about a true fact applied at the wrong time, scope, or level of domain nuance.

## Key Takeaways

- 22 patterns are documented here, the largest goal in knowledge retrieval, organized into domain-level misapplication (7), single-fact distortion (8), and system-level architecture gaps (7).
- Fact Context Loss and Fact Generalization Error are both rated "Very Common," and an estimated 20-35% of agent responses summarizing multi-clause source documents omit at least one qualifier the source explicitly treats as load-bearing — completeness failures are common enough to be the default, not the exception.
- Domain Best-Practice Ignorance estimates a 6-18 month effective half-life for best-practice guidance in fast-moving technical domains, with 20-35% of "how should I do X" agent responses in actively-evolving domains referencing an approach practitioners now consider legacy.
- Knowledge Expiration Not Enforced documents a systems-level root cause behind many of the other 21 patterns: knowledge bases without any TTL or expiration mechanism retain an estimated 30-50% of ingested content well past its practical accuracy window within 18-24 months of launch.

## Scope

- **Domain-Level Misapplication** — [Domain Best-Practice Ignorance](failures/domain-best-practice-ignorance.md), [Domain Constraint Violation](failures/domain-constraint-violation.md), [Domain Context Loss](failures/domain-context-loss.md), [Domain Exception Not Handled](failures/domain-exception-not-handled.md), [Domain Risk Blindness](failures/domain-risk-blindness.md), [Domain Rule Misunderstanding](failures/domain-rule-misunderstanding.md), [Domain Terminology Confusion](failures/domain-terminology-confusion.md). An agent correctly retrieves domain knowledge but misapplies the domain-specific judgment layered on top of it — missing that a practice went stale, that a hard constraint applies, that an exception carves a case back in, that a fact combination is a red flag, that a rule's scope boundary excludes a case, or that a term means something different in-domain than in general usage.
- **Single-Fact Distortion** — [Fact Context Loss](failures/fact-context-loss.md), [Fact Generalization Error](failures/fact-generalization-error.md), [Fact Inversion](failures/fact-inversion.md), [Fact Negation Confusion](failures/fact-negation-confusion.md), [Fact Partial Truth](failures/fact-partial-truth.md), [Fact Probabilistic Mismatch](failures/fact-probabilistic-mismatch.md), [Fact Source Confusion](failures/fact-source-confusion.md), [Fact Timestamp Error](failures/fact-timestamp-error.md). A single retrieved fact survives retrieval and generation correctly in its core content, but loses the qualifier, direction, negation, completeness, certainty level, entity attribution, or time-validity that made it correctly applicable.
- **System-Level Freshness Architecture Gaps** — [Knowledge Contradiction Unresolved](failures/knowledge-contradiction-unresolved.md), [Knowledge Expiration Not Enforced](failures/knowledge-expiration-not-enforced.md), [Knowledge Scope Assumption Wrong](failures/knowledge-scope-assumption-wrong.md), [Knowledge Source Reliability Unknown](failures/knowledge-source-reliability-unknown.md), [Knowledge Temporal Context Lost](failures/knowledge-temporal-context-lost.md), [Knowledge Update Lag](failures/knowledge-update-lag.md), [Knowledge Version Mismatch](failures/knowledge-version-mismatch.md). Architecture-level gaps in the knowledge base itself — no contradiction detection between retrieved passages, no expiration/TTL mechanism, no scope confirmation before answering, no source-reliability weighting, no "as of" preservation, no re-indexing speed matched to source change rate, no version tagging — that make individual fact-level and domain-level errors more likely to occur and go uncaught.

## When Knowledge Freshness Matters

- An agent operates in a domain where best practice, regulation, or terminology shifts on a timescale shorter than the knowledge base's re-verification cycle — security, medicine, tax, compliance, fast-moving engineering tooling
- A knowledge base mixes documents from multiple time periods, jurisdictions, product versions, or authority levels (official policy alongside team wikis or forum posts) with no explicit metadata distinguishing one from another
- Retrieved facts are compressed, summarized, or chunked before reaching generation, since qualifiers, exceptions, and "as of" framing are exactly the content most likely to be trimmed during compression

## Cross-Pattern Insight

The throughline across all three levels of knowledge freshness is that standard fact-checking — does the stated claim match what the source says — is necessary but not sufficient, because every one of the 22 patterns describes a fact that is individually true and still produces a wrong outcome. Domain-level patterns fail because generic retrieval has no representation of domain-specific judgment (currency, hard constraints, exception carve-backs, risk salience) layered on top of literal fact accuracy. Single-fact patterns fail because compression and generation systematically strip the qualifying clause, direction, negation, or "as of" framing that made a true statement correctly scoped. System-level patterns fail because most knowledge base architectures are built to grow a corpus, not to manage its decay, with no default mechanism for expiration, contradiction detection, or source-trust weighting. The fix that recurs at every level is the same structural move: attach explicit metadata (currency tags, scope conditions, effective-date windows, source-reliability tiers) at ingestion time and enforce it as a first-class gate at retrieval or generation time, rather than trusting that semantic relevance or per-claim accuracy checking will catch a freshness problem it was never built to detect.

## Frequently Asked Questions

### What is the difference between a fact-level distortion and a domain-level misapplication?
A single-fact distortion (like [Fact Inversion](failures/fact-inversion.md) or [Fact Context Loss](failures/fact-context-loss.md)) happens to one specific retrieved statement during retrieval or generation — the direction gets flipped, or a qualifying clause gets dropped. A domain-level misapplication (like [Domain Exception Not Handled](failures/domain-exception-not-handled.md) or [Domain Rule Misunderstanding](failures/domain-rule-misunderstanding.md)) happens even when every individual fact is retrieved and stated correctly — the error is in applying correct domain judgment (which exception governs, which scope boundary applies) on top of accurate facts.

### How do you catch a fact that is accurate but incomplete?
Per [Fact Partial Truth](failures/fact-partial-truth.md), standard per-claim fact-checking won't catch a partial-truth omission, since every stated claim passes verification against the source — the omission is invisible to methods built to catch commission (a false claim) rather than exclusion (a true but incomplete one). The documented fix is a dedicated completeness check that compares what the source says relevant to the query against what the response actually includes, rather than relying on accuracy scoring alone.

### Does pinning a knowledge base to "the most recent document" solve staleness?
Not on its own. [Knowledge Update Lag](failures/knowledge-update-lag.md) shows the index itself can lag the actual source-of-truth system regardless of how recency is weighted in ranking, and [Knowledge Expiration Not Enforced](failures/knowledge-expiration-not-enforced.md) shows that without an explicit TTL or deprecation mechanism, an old and a new version of the same fact can coexist as equally retrievable, with recency-weighting only helping if the freshness metadata itself is tracked and enforced.

### Can a single retrieval pipeline fix knowledge scope errors across jurisdiction, version, and time simultaneously?
The mechanism is shared but the fix needs distinct metadata per scope dimension: [Knowledge Scope Assumption Wrong](failures/knowledge-scope-assumption-wrong.md) covers jurisdiction/unit/version scope broadly, [Knowledge Version Mismatch](failures/knowledge-version-mismatch.md) is the product-version-specific case, and [Fact Timestamp Error](failures/fact-timestamp-error.md)/[Knowledge Temporal Context Lost](failures/knowledge-temporal-context-lost.md) cover the time-validity case specifically. A single generic "check the scope" step won't work without each dimension's metadata (jurisdiction tags, version tags, effective-date windows) captured separately at ingestion.

### What causes domain best practices to go stale even when the underlying facts stay true?
Per [Domain Best-Practice Ignorance](failures/domain-best-practice-ignorance.md), best practice is a "currently endorsed approach" judgment, not a truth judgment — a historically correct method can remain factually accurate while the field's consensus moves past it, and no single retrieved passage contradicts the old advice, so ordinary fact-checking and consistency checks never flag the staleness. Only an explicit currency check against the domain's current guidance catches it.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Domain Best-Practice Ignorance](failures/domain-best-practice-ignorance.md) | Retrieved advice was correct best practice at indexing time but has since been superseded by the field's current consensus |
| [Domain Constraint Violation](failures/domain-constraint-violation.md) | A hard regulatory or safety constraint loses the relevance-ranking competition against more topically prominent but non-binding content |
| [Domain Context Loss](failures/domain-context-loss.md) | Domain framing established early in a session decays as the conversation grows, with nothing re-asserting it |
| [Domain Exception Not Handled](failures/domain-exception-not-handled.md) | A documented exception to a general rule is under-retrieved relative to the more prominent general rule it modifies |
| [Domain Risk Blindness](failures/domain-risk-blindness.md) | A domain-standard risk pattern arising from a combination of facts isn't flagged, even though each individual fact is stated correctly |
| [Domain Rule Misunderstanding](failures/domain-rule-misunderstanding.md) | A correctly-quoted rule is misapplied because compound or negated qualifying conditions are misread |
| [Domain Terminology Confusion](failures/domain-terminology-confusion.md) | A term with a specialized in-domain meaning is interpreted using its general-language sense instead |
| [Fact Context Loss](failures/fact-context-loss.md) | A fact and its qualifying clause fall into separate chunks, so only the unqualified fact reaches generation |
| [Fact Generalization Error](failures/fact-generalization-error.md) | A narrowly-scoped fact (specific population, configuration, jurisdiction) is stripped of its scope and presented as a general truth |
| [Fact Inversion](failures/fact-inversion.md) | A fact's direction or polarity is flipped during summarization, stating the opposite of the source |
| [Fact Negation Confusion](failures/fact-negation-confusion.md) | A negation word is dropped, added, or misplaced during paraphrase, inverting a clause's meaning |
| [Fact Partial Truth](failures/fact-partial-truth.md) | A response states only individually-accurate claims while omitting a qualifier that materially changes what a user should do |
| [Fact Probabilistic Mismatch](failures/fact-probabilistic-mismatch.md) | A source's probability or confidence framing is dropped, turning a likelihood into a stated certainty |
| [Fact Source Confusion](failures/fact-source-confusion.md) | Facts about two similarly-named entities are conflated because retrieval matched on name similarity rather than disambiguated identity |
| [Fact Timestamp Error](failures/fact-timestamp-error.md) | A fact's time-bound validity window is mismanaged, applying an outdated or future value as though currently valid |
| [Knowledge Contradiction Unresolved](failures/knowledge-contradiction-unresolved.md) | Two retrieved sources directly disagree and the response answers from one without noticing or disclosing the conflict |
| [Knowledge Expiration Not Enforced](failures/knowledge-expiration-not-enforced.md) | The knowledge base has no TTL or expiration mechanism, so content is retrievable indefinitely regardless of shelf life |
| [Knowledge Scope Assumption Wrong](failures/knowledge-scope-assumption-wrong.md) | The system silently assumes a default jurisdiction, version, or unit instead of confirming the scope the user's situation actually falls under |
| [Knowledge Source Reliability Unknown](failures/knowledge-source-reliability-unknown.md) | Every indexed source is treated as equally trustworthy, with no weighting distinguishing official content from unreviewed content |
| [Knowledge Temporal Context Lost](failures/knowledge-temporal-context-lost.md) | An explicit "as of [date]" anchor from the source is stripped during generation, presenting a time-bound fact as timeless |
| [Knowledge Update Lag](failures/knowledge-update-lag.md) | The re-indexing pipeline runs on a cadence slower than the source system's actual rate of change |
| [Knowledge Version Mismatch](failures/knowledge-version-mismatch.md) | An answer is scoped to whichever product/policy version dominates the knowledge base rather than the version the user is actually on |

**Total: 22 patterns**

## Related Goals

- [Retrieval Quality](../retrieval-quality/) — Temporal Relevance and Index Staleness there share the update-lag and supersession mechanisms documented in depth across knowledge freshness's system-level cluster
- [Citation Accuracy](../citation-accuracy/) — Misgrounded Citation is the citation-specific case of citing a source that's been superseded, the same mechanism as Fact Timestamp Error and Knowledge Temporal Context Lost
- [Answer Synthesis](../answer-synthesis/) — Source Contradiction there is the generation-stage symptom of the same unresolved-conflict mechanism documented at the knowledge-base level in Knowledge Contradiction Unresolved
