# Stale Training-Corpus Fraud Typology Overrides Current SIU Red-Flag List

## Issue: A Fraud-Detection Agent Screening Claims for SIU Referral Applies a Generic Fraud-Typology Pattern Absorbed During Pretraining (e.g., a Widely Discussed Staged-Collision Pattern or a Generic Soft-Tissue-Injury Red-Flag Profile) Instead of Querying the Live, Internally Maintained SIU Red-Flag List That the Carrier Has Available as a Tool, Missing a Recently Added Red Flag Specific to a Current Fraud Ring or Failing to Apply a Recently Retired Flag the Carrier Stopped Using Because It Generated Excessive False Positives

**Frequency**: Occasional

**Symptoms**
- Claims matching a fraud pattern recently added to the carrier's internal SIU red-flag list (e.g., a new staged-incident ring operating in a specific geography) pass through screening without referral
- Claims are referred to SIU citing a red flag the carrier's internal list retired months earlier because it was found to generate excessive false positives, while the live red-flag tool, if queried, would have shown the flag's retired status
- The agent's screening reasoning reflects fraud patterns that read as generic industry knowledge rather than the carrier's specific, currently maintained flag list
- The agent had a live SIU red-flag-list tool available for the session but the trace shows no call to it before the screening decision was finalized
- When explicitly instructed to "check the current SIU red-flag list before screening," the agent retrieves the live list and revises its referral decision

**Example**
```
Carrier's SIU unit retires a long-standing "rental car claim within 48 hours of policy inception" red flag three months
ago after data showed it had a high false-positive rate and was generating excessive low-value referrals
Fraud-detection agent screens a new claim matching exactly that retired pattern and, without querying the live
red-flag-list tool, refers it to SIU citing "claim filed within 48 hours of inception involving a rental vehicle --
known fraud indicator"
SIU intake rejects the referral on review, noting the flag was formally retired and is no longer an active screening
criterion; the referral consumed investigator time that could have gone to a currently valid case
Separately, that same week, a claim matching a newly added red flag for a specific staged-collision ring operating in
one metro area passes through screening unflagged, because the agent's reasoning relied on general staged-collision
patterns rather than the live list's geography-specific update
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Survey research on LLM agent hallucination identifies reliance on memorized, static training-time patterns in place of an available live tool result as a distinct failure mechanism that produces confidently wrong outputs without outright fabrication | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use error detection research finds agents often default to an internally generated, plausible-sounding answer in situations where a tool call would resolve whether that answer is still current | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Execution-provenance research argues that without traceable evidence linking a screening decision to an actual current tool call, there is no way to distinguish a decision grounded in the live red-flag list from one based on outdated general pattern-matching | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |

**Contributing Factors**
- The agent treats fraud-typology patterns as stable general knowledge rather than as a carrier-specific, actively curated and versioned list subject to addition and retirement
- No standing instruction requiring a red-flag-list tool call on every screening pass regardless of whether the agent's own reasoning already produces a plausible-sounding flag
- The agent's training data and general familiarity with widely discussed fraud patterns (staged collisions, soft-tissue injury mills) compete with, rather than defer to, the carrier's specific current list
- No automated alert notifies the screening pipeline when the SIU red-flag list changes, so there is no trigger forcing re-verification of recent screening decisions against the updated list

---

## Mitigation Strategies

1. **Mandatory Red-Flag-List Call Before Every Screening Decision**: Require a live SIU red-flag-list tool call before any referral or clearance decision, regardless of whether the agent's own reasoning already suggests a familiar pattern
2. **List-Change Trigger for Re-Screening**: When the red-flag list is updated (additions or retirements), automatically flag recently screened claims in affected categories for re-screening against the current list
3. **Retired-Flag Suppression**: Maintain an explicit retired-flags registry the agent must check before citing a pattern, distinct from the active list, so a retired flag cannot be cited as if still active
4. **Recency-Tagged List Snapshot**: Pass the red-flag list's last-updated timestamp alongside its content in tool results so the agent can recognize when general background pattern knowledge might be out of step with the carrier's current criteria

### Metrics
- Rate of SIU referrals citing a red flag absent from or retired on the current live list
- Number of claims matching a newly added red flag that passed screening unflagged in the weeks following its addition
- Time lag between a red-flag-list update and the first screening decision that correctly reflects it

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Referral cites retired flag | SIU referral justification matches a flag marked retired on the current live list | P2 | Reject referral; require re-screening with current list |
| Screening without live list call | Screening decision made with no red-flag-list tool call in trace | P3 | Flag for audit; reinforce mandatory-call instruction |
| Post-update miss spike | Claims matching a newly added red flag pass screening unflagged at elevated rate in the weeks after addition | P2 | Trigger mandatory re-verification mode for affected claim categories |

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
