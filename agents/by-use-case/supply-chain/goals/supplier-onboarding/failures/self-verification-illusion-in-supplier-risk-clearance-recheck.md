# Self-Verification Illusion in Supplier Risk-Clearance Recheck

## Issue: When Asked to Double-Check a Flagged Supplier's Risk Clearance Before Onboarding, the Same Agent Re-Examines the Same Submitted Documents Using the Same Reasoning That Produced the Original Clearance Determination, Confirms Its Own Conclusion, and Reports the Supplier Cleared Even Though an Independent Sanctions or Business-Registry Check Would Surface a Disqualifying Match

**Frequency**: Occasional

**Symptoms**
- A "double-check this supplier's risk clearance" request returns a confident confirmation that no disqualifying issues exist, even though an independent sanctions-list or business-registry query against the same supplier's name and registration details surfaces a match
- The agent's recheck re-reads the same submitted onboarding documents and re-applies the same name and registration-detail matching judgment that produced the original clearance, rather than querying an independent, authoritative external database
- Asking the agent to explain how it verified clearance describes re-reviewing the submitted documents and reasoning about them again, not a fresh query against an external sanctions or registry source
- Running the same supplier's details through an independent sanctions-list or registry lookup, separate from the agent's narrative reasoning, surfaces the disqualifying match that the self-check missed
- The miss concentrates on suppliers whose registered name has minor formatting differences (abbreviations, punctuation, transliteration variants) from the name as it appears on the sanctions list or registry entry, since the original clearance's name-matching judgment did not catch the variant

**Root Cause**
A same-model self-check re-derives its clearance judgment from the same document set and reasoning process that produced the original determination, so any systematic gap in that reasoning -- such as not recognizing a transliteration or formatting variant of a sanctioned entity's name -- is reproduced rather than corrected on recheck. Because the self-check produces a fluent, confident restatement of the original "cleared" conclusion, it is indistinguishable in tone from a check that actually queried an independent authoritative source, giving reviewers false confidence that verification occurred before onboarding proceeds.

**Example**
```
Onboarding agent reviews a prospective supplier's submitted registration documents, listing the company name in a transliterated form that differs slightly in spacing and punctuation from how the same entity appears on a sanctions list
Original clearance determination finds no disqualifying issues and approves the supplier for onboarding
Procurement lead requests the agent double-check the clearance before finalizing the contract
Agent re-reviews the same submitted documents, reasons that the company name "does not match any obviously concerning entity," and reports: "Risk clearance re-confirmed, no issues found"
An independent sanctions-list query against the supplier's registration number, rather than name text, immediately surfaces a disqualifying match that the self-check's name-based re-review did not catch
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Tool-use and reasoning agents show a measurable gap between expressed confidence after a self-check and the actual correctness of the underlying conclusion, particularly when the self-check does not introduce an independent evidence source | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |
| Surveys of agent hallucination identify same-model self-consistency checks as an unreliable substitute for grounding in an independent, authoritative source, particularly for name-matching tasks prone to formatting and transliteration variance | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Multi-agent consensus-seeking research in supply-chain contexts identifies independent, structured verification against authoritative external sources as a distinct reliability requirement for autonomous supplier-onboarding decisions | [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184) |

**Contributing Factors**
- The risk-clearance verification step is implemented as a second prompt to the same model rather than a fresh query against an independent, authoritative sanctions or registry database
- No distinction is enforced between "re-reasoned about the same documents" and "queried an independent external source" in how the clearance-verification result is logged or reported
- Name-matching against sanctions and registry sources relies on the model's own text comparison rather than registration-number matching or a dedicated fuzzy-matching service tuned for transliteration variants

---

## Mitigation Strategies

1. **Independent Sanctions and Registry Query as Mandatory Verification Source**: Require any supplier risk-clearance verification to query an independent, authoritative sanctions-list and business-registry database using registration number rather than name text alone, rather than relying on the same model re-reasoning about submitted documents
2. **Disallow Same-Model Self-Check as Sole Verification**: Prohibit a risk-clearance verification from being satisfied solely by a second response from the same model that produced the original clearance; require either an independent database query or independent compliance-officer review
3. **Registration-Number-Based Matching Over Name-Text Matching**: Require sanctions and registry matching to use registration number or other unique identifier as the primary match key, with name-text matching used only as a supplementary signal
4. **Periodic Re-Screening Independent of Onboarding Session**: Re-run independent sanctions and registry screening for all onboarded suppliers on a recurring schedule, independent of any single onboarding session's clearance determination

### Metrics
- Rate of "cleared" suppliers where an independent sanctions or registry query, run after the fact, surfaces a disqualifying match
- Rate of risk-clearance verifications that queried an independent external source versus those that re-reasoned narratively only
- Time between supplier onboarding and detection of a missed disqualifying match, when caught downstream

### Alerts
- An independent sanctions or registry query finds a disqualifying match for a supplier marked "cleared" by self-check alone → P1
- A supplier is onboarded with no record of an independent sanctions or registry query having been run → P2
- Self-check-only risk-clearance verifications as a share of total verifications exceed the defined threshold for a rolling window → P3

---

## References

- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184)
