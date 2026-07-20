# Domain Terminology Confusion

## Issue
An agent interprets a domain-specific term using its common, general-language meaning instead of the narrower or entirely different meaning the term carries within the specialized domain, producing a response that's coherent but answers the wrong question. This happens most with terms that are ordinary English words repurposed with precise technical meaning (e.g. "significant" in statistics, "material" in accounting, "positive" in a lab result), where the domain meaning can even be the near-opposite of the everyday connotation.

**Frequency**: Common

**Symptoms**
- Agent response is fluent and internally consistent but reflects the wrong sense of a key term
- Errors concentrate on terms that are ordinary words with a specialized technical redefinition in the domain
- Domain experts describe the response as "answering a different question than the one asked"
- The confusion is often invisible to non-expert users, who read the response as making sense

## Root Cause
Language models and retrieval systems learn word meaning primarily from statistical co-occurrence across a broad corpus, where the general-language sense of a common word vastly outnumbers its domain-specific technical usage. Without an explicit domain-term glossary that pins a term to its in-domain definition for the current context, the system defaults toward the dominant, general-corpus sense — especially for terms where the domain meaning is a specialized narrowing or inversion of the common one rather than a totally distinct token. The failure is compounded because the response often remains fluent and plausible under either interpretation, so there's no surface-level signal (like a nonsensical sentence) that would otherwise prompt a second look.

## Example
```
A user asks a lab-results assistant: "My biopsy report says the margins
are positive, is that good news?"

In everyday language, "positive" reads as good news. In pathology,
"positive margins" specifically means residual disease was found at
the edge of the excised tissue, which is a concerning finding
typically requiring further treatment — the technical meaning is
effectively inverted relative to the colloquial connotation.

An agent leaning on general-language association between "positive"
and "good" responds with a reassuring tone, or fails to flag the
term's specific clinical significance, when the medically accurate
response is that positive margins are a finding that warrants prompt
follow-up with the treating physician.
```

## Statistics
| Finding | Context |
|---------|---------|
| Terms with a general-language sense that inverts or substantially narrows the domain-specific sense show markedly higher misinterpretation rates than domain-exclusive jargon with no common-language overlap | Typical pattern observed in domain-terminology evaluation sets |
| Explicit glossary grounding (pinning ambiguous terms to domain definitions at retrieval time) reduces terminology-confusion errors by roughly half in tested systems | Reported range across teams that added domain glossaries |
| Non-expert users detect terminology-confusion errors at a much lower rate than domain experts reviewing the same output, since the response remains fluent under either reading | Estimated from comparative review studies in medical/legal/financial QA |

## Mitigations
1. **Domain glossary grounding**: Maintain an explicit glossary of terms with divergent general vs. domain meanings, and inject the domain definition into context whenever such a term appears in a domain-scoped query, rather than relying on the model's default sense.
2. **Ambiguous-term flagging**: When a query or retrieved passage contains a term known to carry both general and specialized meanings, have the agent explicitly state which sense it is using, making the interpretation visible and checkable rather than implicit.
3. **Inverted-connotation term watchlist**: Maintain a specifically curated list of terms where the domain meaning inverts or strongly diverges from colloquial connotation (e.g. clinical "positive," statistical "significant," legal "consideration"), and apply extra scrutiny/hedging whenever these appear.
4. **Domain-scoped retrieval filtering**: Bias retrieval toward domain-specific glossaries and definitional sources over general-language references when the query context establishes a specialized domain.
5. **Expert-reviewed terminology test set**: Build and maintain an evaluation set specifically of common-word/technical-term pairs known to cause confusion in the domain, and test against it on every model or retrieval pipeline change.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| watchlist_term_accuracy | Accuracy on the curated inverted/divergent-connotation term test set | Alert if < 95% |
| glossary_grounding_coverage | Share of domain-scoped queries containing a watchlist term that actually receive glossary grounding in context | Alert if < 95% |
| terminology_confusion_correction_rate | Rate of expert corrections attributing the error specifically to wrong-sense term interpretation | Track trend; alert on sustained increase |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Watchlist term test failure | Evaluation run shows regression on the inverted-connotation term test set | High | Block deployment, review glossary grounding pipeline for the affected terms |
| Terminology confusion in high-stakes domain | Expert review confirms wrong-sense interpretation of a domain term in medical/legal/financial output | High | Escalate for incident review, add term and case to watchlist test set |

## Related Patterns
- [Fact Negation Confusion](./fact-negation-confusion.md) - a related linguistic-mishandling failure, negation rather than sense-disambiguation
- [Domain Rule Misunderstanding](./domain-rule-misunderstanding.md) - terminology confusion is often the specific trigger for a broader rule-scope misread
- [Fact Inversion](./fact-inversion.md) - shares the "meaning flips to its near-opposite" shape, at the level of a retrieved fact's polarity rather than a term's sense
