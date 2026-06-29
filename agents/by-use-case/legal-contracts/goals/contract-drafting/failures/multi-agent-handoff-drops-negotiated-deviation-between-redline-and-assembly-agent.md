# Multi-Agent Handoff Drops Negotiated Deviation Between Redline Agent and Final-Assembly Agent

## Issue: A Redlining Agent That Negotiates a Deal-Specific Deviation From Standard Contract Terms in Its Own Turn-by-Turn Conversation With Counterparty Counsel Hands Off the Negotiated Document to a Separate Final-Assembly Agent Through a Structured "Accepted Clause Set" Record That Captures Only the Clause IDs Used, Not the Specific Negotiated Variable Within Each Clause, So the Assembly Agent Reinserts the Clause's Standard Default Variable Instead of the Negotiated One

**Frequency**: Occasional

**Symptoms**
- Final assembled contract uses a clause's standard default term (notice period, cap amount, renewal length) where the redline negotiation actually agreed to a different, deal-specific value for that same clause
- The redlining agent's own conversation transcript shows the negotiated deviation was reached and confirmed with counterparty counsel, but the structured handoff record passed to the assembly agent lists only the clause template ID, not the specific negotiated parameter value
- Counterparty's final read-through catches the discrepancy between what was agreed in redline and what appears in the assembled final document, requiring a re-negotiation cycle that damages negotiating credibility
- Comparing the redlining agent's transcript against the assembly agent's structured input record shows the deviation existed at handoff time in prose form but had no corresponding field in the structured record
- Re-running the handoff with an explicit "negotiated parameter override" field added to the clause-set record causes the assembly agent to correctly use the negotiated value, confirming the omission was a schema gap between the two agents rather than a misunderstanding by either one

**Example**
```
Redlining agent negotiates a vendor agreement's limitation-of-liability clause with counterparty counsel across several rounds, ultimately agreeing to raise the standard 1x-fees cap to 3x-fees for this specific deal given the contract's higher deal value
Redlining agent's handoff to the document-assembly agent: { clause_id: "LOL-STANDARD-v4", status: "accepted" } -- the clause ID refers to the standard template; the negotiated 3x multiplier exists only in the redline conversation transcript, not in the structured handoff
Assembly agent inserts the standard LOL-STANDARD-v4 clause using its default 1x-fees cap, since that is the value defined in the template behind that clause ID
Final contract is issued to the counterparty with a 1x cap; counterparty's counsel flags the discrepancy against their own redline notes, requiring an embarrassing correction cycle before signature
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent system failures concentrate at agent-to-agent handoff points, where a structured interchange format captures less information than the upstream agent's actual conversational state, causing downstream agents to act on an incomplete record | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| LLM agents are shown to assert a task is complete based on surface-level closing signals (an "accepted" status) without the receiving process verifying that the full negotiated state was actually carried into the next stage | [From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents](https://arxiv.org/html/2606.09863) |
| Execution-provenance research for LLM agents argues that traceable evidence linking a downstream artifact to the specific negotiated value it should reflect is necessary because handoff schemas do not reliably preserve deal-specific deviations from a standard template | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |

**Contributing Factors**
- The interchange schema between the redlining agent and the assembly agent records clause template IDs and an accept/reject status, with no field for a negotiated override of a specific variable within that clause
- The redlining agent's full negotiation transcript is logged but not treated as part of the authoritative handoff payload the assembly agent is required to consume
- No validation step compares the redlining agent's transcript for negotiated-value language against the structured clause-set record to flag unrepresented deviations
- Standard clause IDs are reused across many deals with only the variable terms changing deal-to-deal, so a schema built around clause ID alone systematically cannot represent the most common form of negotiation outcome

---

## Mitigation Strategies

1. **Structured Negotiated-Override Field**: Require every redline-to-assembly handoff to include an explicit override field for any variable within a clause that deviates from the clause template's default, populated directly from the negotiation outcome rather than inferred later
2. **Transcript-to-Schema Reconciliation Check**: Before assembly proceeds, run an automated check comparing the redlining agent's negotiation transcript for value-specific language (caps, periods, percentages) against the structured override fields, flagging any negotiated value not represented in the structured record
3. **Block Template-ID-Only Handoffs for Negotiated Clauses**: Reject a handoff record that marks a clause as "accepted" following a multi-round negotiation if no override field is present, treating template-ID-only handoffs as valid only for clauses accepted without negotiation
4. **Final-Assembly Diff Against Redline Transcript**: Require a final automated diff between the assembled document's clause values and the negotiation transcript's agreed values before the document is sent to the counterparty

### Metrics
- Rate of assembled contracts where a clause's final value does not match the negotiated value recorded in the redlining agent's transcript
- Number of handoffs for negotiated clauses using template-ID-only records versus records with an explicit override field
- Mean time between document issuance and detection of a dropped negotiated deviation (internal review vs. counterparty-flagged)

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Transcript-schema value mismatch | Redline transcript contains a negotiated value not present in the structured override field | P1 | Block assembly/issuance pending correction of the handoff record |
| Template-ID-only handoff for negotiated clause | Clause marked "accepted" after multi-round negotiation with no override field | P2 | Require schema correction before document assembly proceeds |
| Counterparty-flagged discrepancy | Counterparty redline or sign-off flags a value mismatch against their own negotiation notes | P1 | Halt signature process; reconcile against full negotiation transcript |

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents](https://arxiv.org/html/2606.09863)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
