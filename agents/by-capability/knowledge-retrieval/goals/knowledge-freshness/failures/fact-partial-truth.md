# Fact Partial Truth

## Issue
An agent presents a fact that is technically accurate as stated but omits a critical qualifier that would materially change how a user should act on it — not because the qualifier is missing from the source, but because it was dropped somewhere in retrieval or generation and the resulting statement, while not false, is misleadingly incomplete. This differs from a fabrication: every word the agent says checks out against the source, but the selective omission changes the practical meaning.

**Frequency**: Very Common

**Symptoms**
- Every individual claim in the agent's response is independently verifiable as true against the source
- A critical qualifier, exception, or condition present in the source is absent from the response
- Users act on the partial truth in ways they would not have if the omitted qualifier were included
- Fact-checking tools that verify claims in isolation pass the response, since each isolated claim is accurate

## Root Cause
Standard fact-checking and hallucination-detection approaches verify whether a stated claim is supported by the source, but they don't verify completeness — whether everything the source says that's relevant to the claim was included. A response can pass every per-sentence accuracy check while still being materially misleading because of what it leaves out, since omission is invisible to verification methods built to catch commission (stating something false) rather than exclusion (failing to state something true and necessary). Summarization and length-constrained generation naturally compress source material, and qualifiers — often phrased as secondary or subordinate clauses — are the first casualty of compression because they're not the sentence's main clause even though they may be the operative constraint.

## Example
```
A source product safety document states: "The device is rated for
continuous operation at ambient temperatures up to 40C. Above 40C,
continuous operation is not recommended and may void the warranty;
intermittent use with cooldown periods remains supported up to 50C."

A user asks a support agent whether the device can run continuously in
a server room they describe as running around 42C. The agent responds:
"The device is rated for continuous operation up to 40C" — a fact that
is completely accurate on its own, and technically answers the literal
question (implying no at 42C), but omits the source's further detail
about intermittent-use support up to 50C, and doesn't explicitly warn
the user that continuous operation at their stated 42C would void the
warranty.

The user, reading only the truncated response, may either wrongly
conclude the device simply won't function above 40C (missing the
intermittent-use option that might suit their case) or run it
continuously anyway without realizing the warranty implication that
was in the source but never surfaced.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 20-35% of agent responses summarizing multi-clause source documents omit at least one qualifier the source explicitly treats as load-bearing | Estimated from completeness audits of summarization pipelines against source documents |
| Per-claim fact-checking (verifying each stated sentence against source) catches a small fraction of partial-truth omissions, since the omitted content was never stated to check | Typical limitation observed across standard hallucination-detection tooling |
| Adding explicit completeness scoring (checking what the source says that the response doesn't) alongside accuracy scoring catches the large majority of these cases in tested pipelines | Reported range across teams that added completeness-specific verification |

## Mitigations
1. **Completeness verification alongside accuracy verification**: Add a dedicated check comparing what the source states as relevant to the query against what the response includes, flagging significant omissions rather than only checking stated claims for accuracy.
2. **Qualifier-tagging at ingestion**: Explicitly tag source clauses that function as qualifiers, exceptions, or conditions (via structural cues or manual annotation for high-stakes documents), and require the generation step to include or explicitly acknowledge tagged qualifiers when citing the primary claim.
3. **"Anything else relevant?" self-check**: Prompt the generation step to explicitly review the full retrieved source for additional relevant conditions before finalizing a response, rather than stopping once a literal answer to the query is found.
4. **Warn on truncation-sensitive domains**: In domains with known high consequence for incomplete answers (safety, medical, financial, legal), default to including more source context rather than the minimal literal answer, even at the cost of longer responses.
5. **User-facing "source has more detail" signal**: When the response is a compressed version of a longer source, indicate this explicitly and offer the fuller source, so users with materially different circumstances know to check further.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| qualifier_inclusion_rate | Share of responses that include tagged source qualifiers relevant to the query | Alert if < 85% |
| completeness_score | Automated score comparing response content against source content relevant to the query | Alert if median score drops below domain-specific baseline |
| partial_truth_correction_rate | Rate of expert/user corrections adding a qualifier the response omitted despite being technically accurate | Alert if > 5% of responses in qualifier-heavy domains |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Critical qualifier omitted in high-stakes response | Review confirms a safety/medical/financial/legal qualifier was omitted from an otherwise-accurate response | High | Correct the response, add source document to qualifier-tagging backlog |
| Completeness score regression | completeness_score drops below baseline after a summarization pipeline or prompt change | Medium | Review recent changes for over-aggressive compression |

## Related Patterns
- [Fact Context Loss](./fact-context-loss.md) - the retrieval-stage mechanism (qualifier dropped during chunking) that frequently produces this generation-stage symptom
- [Fact Generalization Error](./fact-generalization-error.md) - a specific form of partial truth where the dropped qualifier is specifically the fact's population/condition scope
- [Domain Exception Not Handled](./domain-exception-not-handled.md) - the rule-level analog, where the omitted element is a documented exception rather than a qualifying clause on a fact
