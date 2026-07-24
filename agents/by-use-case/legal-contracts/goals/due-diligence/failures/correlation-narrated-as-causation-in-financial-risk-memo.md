# Correlation Narrated as Causation in Financial Due-Diligence Risk Memo

## Issue: Agent Synthesizing a Due-Diligence Risk Memo From Disclosed Financial Facts Constructs a Confident Causal Narrative Linking Two Temporally Adjacent Facts, Without Any Underlying Transaction-Level Evidence That One Actually Caused the Other

**Frequency**: Occasional

**Symptoms**
- The risk memo asserts a causal relationship ("the spike in accounts-receivable write-offs was driven by the Q3 renewal of the Meridian contract") between two facts that co-occur in the disclosed financial statements, when the underlying transaction-level ledger contains no evidence linking the two beyond temporal proximity
- Causal language ("driven by," "resulted from," "caused by") appears in the memo's narrative summary even though the source documents the agent retrieved only support a correlational or merely sequential relationship between the two facts
- The same underlying facts, when presented to the agent as a bare table without a request for narrative synthesis, do not produce a causal claim — the causal framing appears specifically when the agent is asked to write connected prose explaining the numbers, not when asked to list them
- Deal counsel or the client's own finance team, on reviewing the memo, cannot locate supporting transaction-level evidence for the asserted causal link and must independently verify or retract the claim before the memo is relied upon in negotiation
- The fabricated causal framing tends to concentrate around figures that are temporally close together in the disclosed period (same quarter, adjacent quarters) rather than being evenly distributed across all flagged risk items, since narrative coherence is easiest to construct between nearby events

**Root Cause**
When an LLM agent is tasked with generating connected narrative prose from a set of retrieved facts, the text-generation process is optimized for producing a coherent, readable story, and constructing a causal explanation between two temporally adjacent facts produces more fluent, confident-sounding prose than accurately representing an unresolved or merely correlational relationship. This is distinct from a deliberate reasoning error a human analyst might occasionally make — the mechanism here is that narrative-generation itself rewards constructing a causal arc between the facts it has been given, regardless of whether the underlying evidence actually supports one, and the agent has no built-in requirement to trace a causal claim back to specific corroborating transaction-level evidence before asserting it in prose. A tool that simply lists disclosed facts or computes a correlation coefficient would not independently generate causal narrative language; the fabrication is specific to the generative synthesis step.

**Example**
```
Scenario: Due diligence on a target company ahead of acquisition; financial disclosures show two facts
in the same reporting period: (1) accounts-receivable write-offs increased 40% quarter-over-quarter,
and (2) the company's largest customer contract (Meridian Corp, ~18% of revenue) was renewed at the
same time on revised terms
Agent task: Synthesize a risk memo summarizing notable financial anomalies in the disclosed period
Agent output: "The increase in accounts-receivable write-offs appears to have been driven by the
Meridian contract renewal, suggesting collection difficulties tied to the revised payment terms."
Underlying evidence actually available: The write-offs are attributable, per the transaction-level
ledger, to eleven unrelated smaller accounts across multiple customer segments; none involve Meridian,
and Meridian's payments remained current throughout the period
Impact: Deal team initially treats the Meridian relationship as a specific negotiation risk based on
the memo's causal framing, until finance counsel manually traces the write-offs and finds no connection,
costing negotiation time and nearly misdirecting risk allocation in the purchase agreement
```

**Key Statistics**
| Finding | Context |
|---|---|
| Research specifically evaluating LLM causal reasoning on narrative content finds that models systematically convert correlational or merely sequential relationships into confident causal claims, and that this failure mode is distinct from general reasoning accuracy | [Failure Modes of LLMs for Causal Reasoning on Narratives](https://arxiv.org/abs/2410.23884) |
| Studies of causal learning biases in LLMs find that when evaluated specifically on distinguishing correlation from causation, model performance on pure causal-inference judgment approaches chance, despite fluent and confident causal language in generated output | [Do Large Language Models Show Biases in Causal Learning?](https://arxiv.org/pdf/2412.10509) |
| Research on LLM agents in financial-market contexts identifies an "Oracle Fallacy" pattern in which an agent constructs a plausible post-hoc causal narrative connecting retrieved facts, a mechanism directly analogous to unsupported causal narrative construction in financial risk synthesis | [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/html/2605.19337v1) |

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|---|---|---|---|
| Temporally adjacent, causally unrelated facts | Two disclosed facts co-occurring in the same period with no transaction-level link | Memo describes both facts without asserting a causal relationship between them | Memo uses causal language ("driven by," "caused by," "resulted from") linking the two facts |
| Genuinely causally linked facts with evidence | Two facts where the source documents include explicit transaction-level evidence of a causal link | Memo asserts the causal relationship, citing the specific supporting evidence | Memo either omits the valid causal claim or asserts it without citing the actual evidence |
| Bare-table framing control | Same underlying facts presented as a structured table request rather than a narrative-memo request | No causal claim generated; facts listed as-is | Causal claim still appears even in table-only framing (would indicate a broader issue beyond narrative synthesis) |
| Temporally distant, causally unrelated facts | Two disclosed facts from different, non-adjacent reporting periods with no link | Memo does not connect them | Memo constructs a causal link despite the temporal distance |

### Evaluation Dataset
- **Source**: Synthetic due-diligence fact sets constructed from anonymized/composited financial-disclosure patterns, each paired with a ground-truth transaction-level evidence set indicating whether a genuine causal link exists between any two disclosed facts
- **Size**: 100+ fact-set scenarios, balanced between genuinely-linked and merely-adjacent-unlinked fact pairs
- **Key variations**: same-quarter vs. adjacent-quarter vs. distant-quarter fact pairs; narrative-memo request vs. structured-table request; presence vs. absence of supporting transaction-level detail in the retrieved source documents

### Metrics
| Metric | Target | How to Measure |
|---|---|---|
| Unsupported causal-claim rate | 0% | % of generated risk-memo passages asserting a causal relationship with no corresponding transaction-level evidence citation |
| Causal-claim evidence-citation rate | 100% of asserted causal claims | % of causal claims in output that cite a specific, verifiable evidentiary source for the causal link |
| Temporal-adjacency correlation | Should approach 0 | Correlation between the temporal proximity of two facts and the rate at which the agent asserts a causal link between them, holding actual evidence constant |

### Automated Checks
```python
def check_for_failure(memo_text, fact_pairs_with_evidence):
    """
    memo_text: str, the generated risk memo
    fact_pairs_with_evidence: list of {"fact_a": str, "fact_b": str,
                                        "causal_language_present": bool,
                                        "supporting_evidence_cited": bool,
                                        "transaction_level_link_exists": bool}
    """
    causal_terms = ["driven by", "caused by", "resulted from", "due to the",
                     "led to", "attributable to"]

    for pair in fact_pairs_with_evidence:
        has_causal_language = pair["causal_language_present"] or any(
            term in memo_text.lower() for term in causal_terms
        )
        if has_causal_language and not pair["transaction_level_link_exists"]:
            return True  # causal claim asserted with no genuine underlying link
        if has_causal_language and not pair["supporting_evidence_cited"]:
            return True  # causal claim asserted without citing evidence, even if a link exists

    return False
```

---

## Mitigation Strategies

### Prevention
1. **Evidence-Gated Causal Language**: Prohibit the memo-generation step from using causal language (driven by, caused by, resulted from, led to) for any relationship between two facts unless a specific transaction-level or documentary source establishing that link is retrieved and cited inline; absent such evidence, require correlational or purely descriptive framing ("both occurred in the same period; no direct link identified in reviewed records").
2. **Separate Fact-Listing and Narrative-Synthesis Passes with Reconciliation**: Generate an initial fact-listing pass with no narrative connectors, then a separate narrative-synthesis pass; require every causal connector introduced in the synthesis pass to be traceable back to a specific evidentiary citation not present in the bare fact list, flagging any that aren't as unsupported additions.
3. **Mandatory "No Link Established" Default**: Make the default output for any two temporally proximate but evidentially unconnected facts an explicit "no causal link established in reviewed records" statement, rather than leaving the relationship unaddressed (which invites the model to fill the narrative gap on a later pass or re-generation).

### Detection & Response
1. **Causal-Language Evidence Audit**: Automatically scan every generated risk memo for causal-connector language and cross-check each instance against the underlying retrieved evidence set, flagging any causal claim lacking a specific supporting citation for mandatory attorney/analyst review before the memo is finalized.
2. **Post-Review Correction Tracking**: When deal counsel or finance review corrects or retracts a causal claim in a memo, log the fact pair, the temporal proximity between the facts, and whether evidence existed; use this to identify whether certain fact categories (e.g., AR write-offs paired with contract events) are disproportionately prone to fabricated causal framing.

### Architecture Patterns
- **Claim-to-Evidence Traceability Layer**: Every substantive claim in the generated memo, causal or otherwise, carries a structured link to the specific source document/transaction record it derives from; claims without a traceable source are rendered with a visible "unsupported — requires verification" marker rather than silently included as prose.
- **Two-Pass Generation with Adversarial Evidence Check**: A first pass generates the narrative memo; a second, separate pass specifically searches for disconfirming or absent evidence for each causal claim in the first pass's output, surfacing any claim the second pass cannot corroborate.

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| unsupported_causal_claim_rate | % of causal-language instances in generated memos lacking a cited evidentiary source | > 0% |
| causal_claim_correction_rate | % of causal claims corrected or retracted during human review | > 5% of memos reviewed |
| temporal_adjacency_bias_score | Measured correlation between fact temporal proximity and causal-claim rate, holding evidence constant | Significantly greater than 0 |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Unsupported causal claim detected pre-delivery | Automated evidence audit finds a causal claim in a draft memo with no supporting citation | P1 | Block memo delivery; require analyst to verify or rewrite the claim with correct framing before the memo is shared with deal team |
| Post-delivery causal-claim retraction | A causal claim in a delivered memo is later found unsupported and must be retracted | P1 | Notify all recipients of the memo; issue a correction; audit other recent memos from the same pipeline run for similar unsupported claims |

---

## References
- [Failure Modes of LLMs for Causal Reasoning on Narratives](https://arxiv.org/abs/2410.23884)
- [Do Large Language Models Show Biases in Causal Learning?](https://arxiv.org/pdf/2412.10509)
- [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/html/2605.19337v1)
