# Fact Negation Confusion

## Issue
An agent drops, adds, or misplaces a negation while processing retrieved text, asserting the opposite of what the source actually states. Unlike a full directional inversion, this failure is specifically about negation words and constructions ("not," "no longer," "except," "unless," double negatives) being mishandled during retrieval, summarization, or paraphrase, producing a claim that reads fluently but contradicts the source on the single most important word in the sentence.

**Frequency**: Occasional

**Symptoms**
- Agent output omits or adds a "not"/"no"/"never" relative to the source sentence
- Errors concentrate around double negatives, "unless" clauses, and negated compound conditions
- The rest of the sentence structure and vocabulary matches the source closely, isolating the negation itself as the point of failure
- Fact-checking against the source, when done sentence-by-sentence, immediately catches what response-level review misses

## Root Cause
Negation is syntactically lightweight — a single short word or prefix can invert an entire clause's meaning — which makes it disproportionately vulnerable to being dropped or misplaced during any lossy transformation of text: chunking that splits a negation from what it modifies, summarization that compresses a sentence and loses the negating word in the process, or paraphrase that restructures a negated clause and inverts it along the way. Double negatives and negated conditionals compound the problem because correctly tracking two or more negations through a paraphrase requires precise logical bookkeeping that surface-level language generation isn't guaranteed to preserve, and unlike a factual substitution, a dropped negation produces a sentence that is often just as fluent and plausible as the correct one.

## Example
```
A source compliance document states: "This exemption does not apply to
transactions that are not conducted at arm's length."  (i.e., the
exemption DOES apply only to arm's-length transactions; non-arm's-length
transactions are excluded from the exemption.)

An agent summarizing this for a user asks about a related-party
transaction (which is not arm's length) responds: "This exemption
applies to your transaction" — having dropped one of the two negations
in the double-negative construction during paraphrase, inverting the
actual scope of the exemption.

The user proceeds as though exempt, structures the transaction
accordingly, and only discovers the exemption never applied when the
transaction is later reviewed against the original compliance text.
```

## Statistics
| Finding | Context |
|---------|---------|
| Negation-handling error rates are markedly higher on double-negative and negated-conditional constructions than on single, simple negations | Typical pattern observed in NLI (natural language inference) and summarization-fidelity benchmarks |
| An estimated 3-8% of summarized sentences containing a negation drop, add, or misplace it relative to the source | Estimated from summarization-fidelity audits involving negated source sentences |
| Explicit negation-preservation checks (verbatim comparison of negation words between source and output) catch the large majority of these errors before they reach users in tested pipelines | Reported range across teams that added negation-specific verification |

## Mitigations
1. **Negation-preservation verification**: Run an automated check specifically comparing negation words/constructions between source sentences and generated output, flagging any mismatch for review before the response is finalized.
2. **Double-negative simplification at ingestion**: Where possible, pre-process source content to rewrite double-negative and complex negated-conditional constructions into logically equivalent positive statements, reducing the surface area for negation errors during generation.
3. **Verbatim quotation for negation-critical clauses**: For compliance, medical, and legal domains where a dropped negation has high consequence, require verbatim quotation of the negated clause rather than paraphrase.
4. **Sentence-level fact-checking granularity**: Perform fact-checking at the individual-clause level rather than only at the whole-response level, since negation errors are most visible when the specific negated clause is checked in isolation against its source.
5. **Explicit negation test suite**: Maintain an evaluation set of source sentences with single, double, and negated-conditional constructions, and test summarization/paraphrase pipelines against it on every change.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| negation_preservation_rate | Share of generated clauses whose negation status matches the corresponding source clause | Alert if < 95% |
| double_negative_error_rate | Error rate specifically on source sentences containing double negatives or negated conditionals | Track separately; alert if markedly above single-negation error rate |
| negation_correction_rate | Rate of expert/user corrections identifying a dropped, added, or misplaced negation | Alert if > 2% of responses summarizing negation-containing source text |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Negation error in compliance/legal/medical response | Review confirms a dropped or inverted negation in a high-stakes domain response | High | Retract/correct immediately, add source sentence to negation test suite |
| Negation preservation rate drop | negation_preservation_rate falls below threshold after a summarization pipeline change | Medium | Review recent prompt/pipeline changes for negation-handling regressions |

## Related Patterns
- [Fact Inversion](./fact-inversion.md) - the broader pattern of flipped meaning; negation confusion is the specific linguistic mechanism that produces one common form of it
- [Domain Rule Misunderstanding](./domain-rule-misunderstanding.md) - negated conditional clauses ("unless," "except when") are a frequent source of rule scope misreads
- [Domain Terminology Confusion](./domain-terminology-confusion.md) - both are single-token-level linguistic failures with outsized effect on overall meaning
