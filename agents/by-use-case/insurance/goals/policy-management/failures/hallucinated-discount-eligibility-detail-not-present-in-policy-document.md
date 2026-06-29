# Hallucinated Discount-Eligibility Detail Not Present in Policy Document

## Issue: A Policy-Servicing Agent Responding to a Policyholder's Question About Why a Specific Discount Does or Does Not Apply Cites a Specific-Sounding Eligibility Detail -- a Named Discount Program, a Specific Qualifying Condition, a Stated Percentage -- That Does Not Actually Appear in the Policy Document or Rating Tool Result the Agent Retrieved, Fabricating a Plausible Explanation Rather Than Reporting What the Retrieved Document Actually Says

**Frequency**: Occasional

**Symptoms**
- The agent's explanation to the policyholder names a specific discount program, percentage, or qualifying condition that does not appear anywhere in the policy document or rating-engine tool result actually retrieved during the session
- Searching the policy document or rating system directly for the cited specific program or condition returns no match
- The underlying tool call in the trace returned a more limited or different result (e.g., a current premium figure with no breakdown by discount) than what the agent's explanation describes in detail
- The fabricated explanation is specific and plausible (a named program consistent with the carrier's general discount offerings) rather than vague, which is what allows it to pass a cursory review
- A policyholder acts on the fabricated explanation (e.g., attempts to enroll in a discount program that does not exist as described) and is later told by a human agent that no such program or condition exists

**Example**
```
Policyholder asks the policy-servicing agent why their multi-policy discount dropped off at renewal
Agent calls the rating-engine tool, which returns the current premium breakdown showing only that the multi-policy
discount line item is absent, with no explanation field describing why
Agent's response to the policyholder: "Your multi-policy discount was removed because your auto policy's renewal
date fell outside the 30-day bundling window required under our Loyalty Bundle Program"
No "Loyalty Bundle Program" or "30-day bundling window" requirement exists anywhere in the policyholder's documents,
the rating engine's actual returned result, or the carrier's discount rules; the explanation was generated to sound
plausible and complete rather than reported from what the tool actually returned
The policyholder calls back upset after a human service rep cannot find any record of a "Loyalty Bundle Program";
investigation reveals the discount actually dropped due to an unrelated address-verification lapse, never mentioned
in the agent's fabricated explanation
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Survey research on LLM agent hallucination documents fabrication of specific, plausible-sounding supporting detail -- named programs, conditions, figures -- to fill a gap left by a less detailed or incomplete tool result, rather than reporting the tool's actual content | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Execution-provenance research argues that without evidence tracing linking each specific explanatory detail back to an actual tool-returned field, reviewers and policyholders cannot distinguish a genuine policy provision from a fabricated one | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |
| Tool-use error detection research finds agents tend to elaborate confidently on an incomplete or under-specified tool result rather than reporting its actual, more limited content or flagging the gap | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |

**Contributing Factors**
- The agent's explanation-generation step is not constrained to only state discount-eligibility details that are verifiably present in the policy document or rating-tool result
- An incomplete tool result (e.g., a premium breakdown with no explanatory field) is treated as a narrative gap the agent is implicitly expected to fill rather than a limit on what it can honestly tell the policyholder
- No automated cross-check verifies that every named program, condition, or percentage in a servicing explanation corresponds to an actual field or document the agent retrieved in that session
- Policyholder-facing explanations are optimized for sounding complete and reassuring, creating pressure toward filling gaps with plausible specifics rather than admitting "the system doesn't show why"

---

## Mitigation Strategies

1. **Fact-to-Tool-Result Binding for Servicing Explanations**: Require every specific discount-eligibility detail in a policyholder-facing explanation (program names, conditions, percentages) to be programmatically matched against an actual field in the retrieved policy document or rating-tool result
2. **Explicit "Reason Unavailable" Fallback**: When the rating-engine tool result does not include an explanatory field for a discount change, require the agent to state that the reason is not available in the system and offer escalation, rather than generating a plausible-sounding explanation
3. **Discount-Rule Reference Table Cross-Check**: Validate any named discount program or condition cited by the agent against the carrier's actual current discount-rules reference table before the explanation is sent to the policyholder
4. **Audit Sample of Servicing Explanations**: Periodically sample agent-generated policyholder explanations and verify each specific factual claim against the underlying tool trace to catch fabrication patterns before they accumulate into a volume of policyholder complaints

### Metrics
- Rate of policyholder-facing explanations containing a specific discount-eligibility detail with no matching field in the retrieved tool result or policy document
- Number of policyholder complaints citing an explanation that could not be substantiated on follow-up review
- Average gap between tool-result completeness and explanation specificity across sampled servicing interactions

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unbound discount detail in explanation | Servicing explanation cites a named program or condition absent from the retrieved tool result or policy document | P1 | Hold explanation from being sent; require source verification |
| Explanation generated from incomplete tool result | Rating-engine result lacks an explanatory field but agent's response includes a detailed causal explanation | P2 | Route to human review before sending to policyholder |
| Repeated fabricated-program citations | Same nonexistent program or condition cited across multiple policyholder interactions within a rolling window | P2 | Audit servicing-explanation prompt for fabrication tendency |

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
