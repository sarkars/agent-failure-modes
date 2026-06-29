# Hallucinated Specific Fraud Indicator Not Present in Claim File

## Issue: A Fraud-Detection Agent Drafting an SIU-Referral Justification Cites a Specific Fraud Indicator -- an Exact Prior-Claim Number, a Named Witness Inconsistency, a Specific Repair-Shop Affiliation Flagged in a Prior Investigation -- That Does Not Actually Appear Anywhere in the Claim File or Any Tool Result Returned During the Review, Fabricating a Concrete-Sounding Detail to Round Out an Otherwise Thin Justification

**Frequency**: Occasional

**Symptoms**
- The SIU-referral justification names a specific prior claim number, repair shop, or witness detail that does not appear in the claim file, the claims-history tool result, or any other document the agent actually retrieved during the session
- Searching the claims system directly for the cited specific detail (claim number, shop name) returns no match or a match to an unrelated claim
- The underlying tool calls in the trace returned genuine but more general fraud-risk signals (e.g., a moderately elevated risk score) with no specific corroborating detail of the kind cited in the justification
- The fabricated detail is specific and verifiable-sounding rather than vague, which is what allows it to pass an SIU reviewer's first read
- A legitimate claimant is referred to SIU, or an investigation is opened, on the strength of a justification that partly rests on a detail that does not exist in any system of record

**Example**
```
Claims-history tool returns a moderately elevated fraud-risk score for a claimant but no specific matching prior claim
or named association in its result payload
Fraud-detection agent drafts the SIU referral: "Refer for investigation -- claimant's prior claim #88213-B at the same
repair facility, Eastside Auto Body, was previously flagged for inflated estimate submission"
No claim #88213-B exists in the claims system, and "Eastside Auto Body" does not appear anywhere in the claimant's
file or in the claims-history tool's actual returned result
SIU opens an investigation partly on the strength of this specific-sounding prior-claim detail; the claimant, who has
no fraud history, is delayed and contacted for additional documentation
When SIU staff attempt to pull claim #88213-B to review the prior flag, it cannot be located because it was never real
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Survey research on LLM agent hallucination documents fabrication of specific, verifiable-seeming details -- record numbers, named entities, prior incidents -- as a recurring failure mode that is more likely to be accepted by reviewers than vague fabrications | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Execution-provenance research argues that without evidence tracing linking each specific factual assertion in an agent's output to an actual tool-returned record, reviewers cannot distinguish a genuine corroborating detail from a fabricated one | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |
| Tool-use error analysis finds agents tend to elaborate on a generic or thin tool result with additional plausible-sounding specifics rather than reporting the result's actual, more limited content | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |

**Contributing Factors**
- The agent's referral-drafting step is not constrained to only state specific facts (claim numbers, shop names, named prior flags) that are verifiably present in a tool-returned result
- A moderately elevated but non-specific risk score is treated as a justification gap the agent is implicitly rewarded for filling with concrete-sounding corroboration
- No automated cross-check verifies that every specific factual detail in an SIU referral corresponds to an actual record returned by a claims-history or prior-claims tool call in that session
- SIU reviewers' time pressure favors referrals with concrete, specific-sounding justifications, creating an incentive structure where fabricated specificity is more likely to pass review than an honest "elevated score, no specific corroboration"

---

## Mitigation Strategies

1. **Fact-to-Tool-Result Binding for Referrals**: Require every specific factual claim in an SIU-referral justification (claim numbers, shop names, named prior flags) to be programmatically matched against an actual tool-returned record ID before the referral can be submitted
2. **Separate Risk-Score from Corroborating-Detail Fields**: Structure the referral format so that a quantitative risk score and any specific corroborating detail are distinct, independently-sourced fields, preventing a thin score-only result from being dressed up with unverified specifics
3. **Mandatory Source-Link in Referral**: Require every named claim number or entity in a referral to include a direct link or ID reference to the tool result it came from, making an unbound fabricated detail immediately visible to reviewers
4. **Independent Verification Before Investigation Opens**: Require SIU intake to independently verify at least one specific cited detail in a referral against the claims system before formally opening an investigation, rather than accepting the referral justification at face value

### Metrics
- Rate of SIU-referral justifications containing a specific factual detail with no matching tool-returned record ID
- Number of opened SIU investigations later found to rest partly on an unverifiable or nonexistent cited detail
- Average specificity-to-verification gap (how often specific details in referrals are independently confirmed versus not)

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unbound specific detail in referral | Referral cites a claim number, shop, or named entity with no matching tool-returned record | P1 | Hold referral from SIU queue; require source verification before submission |
| Referral based solely on risk score plus unverified detail | Referral combines a generic risk score with a specific detail absent from any tool result | P1 | Escalate to fraud-model lead for justification audit |
| Recurrence across referrals | Multiple unbound specific details detected across referrals from the same agent session pattern within a rolling window | P2 | Audit referral-drafting prompt for fabrication tendency |

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
