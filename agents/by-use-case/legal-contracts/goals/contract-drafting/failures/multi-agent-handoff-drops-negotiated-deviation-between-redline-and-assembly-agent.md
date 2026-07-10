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

### Prevention

1. **Mandatory structured negotiated-override field with value-specific population**: Extend redline-to-assembly handoff schema to include explicit "Negotiated Overrides" section: {clause_id, default_value, negotiated_value, override_status: (accepted|rejected|pending)}. For each clause marked "accepted" in negotiation, redline agent must populate: negotiated_value with the specific deal-specific value agreed (e.g., liability_cap: 3x_fees, notice_period: 90_days). Fail-safe: assembly agent blocks insertion if clause marked "accepted" but negotiated_value field is empty. Template-ID-only handoffs rejected for clauses with multi-round negotiation history. Root cause: Prevents negotiated values from existing only in transcript by forcing structured capture.

2. **Transcript-to-schema reconciliation pass with deviation detection and blocking**: Before assembly begins, run automated reconciliation: (a) extract all value-specific language from redline transcript (patterns like "agreed to", "negotiated", "modified to", "changed from X to Y"), (b) parse: clause_id and negotiated_value, (c) compare against structured override fields, (d) flag mismatches: "Transcript says liability cap changed to 3x-fees; override field is empty → Block assembly pending correction". Require human review to populate missing overrides. Root cause: Catches transcript-to-schema gaps before assembly proceeds.

3. **Final-assembly diff validation against negotiation transcript with value reconciliation**: After assembly agent inserts clauses, run final validation: (a) for each assembled clause, extract its final value (cap amount, notice period, etc.), (b) query redline transcript: what was the final negotiated value for this clause? (c) if assembled value ≠ negotiated value, flag with diff, (d) block finalization until reconciled. Generate reconciliation report: "Assembled document: liability cap = 1x; Negotiated value: 3x → MISMATCH DETECTED: Correct value to 3x before sending to counterparty". Root cause: Adds independent verification layer that catches dropped deviations before counterparty sees document.

### Detection & Response

1. **Multi-agent handoff audit logging with transcript-schema reconciliation tracking**: For every redline-to-assembly handoff, log: (a) redline negotiation transcript (full text, searchable), (b) structured override field population status (complete/incomplete), (c) reconciliation check results (match/mismatch), (d) any deviations detected and resolution, (e) final assembly diff validation results. Run automated QA: sample handoffs and verify all negotiated values from transcript appear in override fields and final assembled document. Measure: transcript_schema_reconciliation_rate, deviation_detection_rate, handoff_fidelity_rate.

2. **Retroactive negotiation audit on discrepancy discovery**: When counterparty flags value mismatch or internal review finds dropped deviation, trace to original redline-to-assembly handoff. Did redline agent negotiate the correct value? Did it populate override field? Did assembly agent use override field? Where did handoff fail? Update handoff schema or validation logic based on failure root cause.

### Architecture Patterns

1. **Structured Negotiated-Override Schema**: Handoff payload includes: {clause_id, template_default_value, negotiated_value, override_reason, negotiation_rounds, final_status}. For clauses with multi-round negotiation history, override field is mandatory; template-ID-only rejected.

2. **Transcript-to-Schema Reconciliation Engine**: (1) Extracts value-specific language from redline transcript, (2) Parses negotiated values, (3) Compares against override fields, (4) Flags missing/mismatched overrides, (5) Blocks assembly until reconciliation complete.

3. **Final-Assembly Diff Validator**: (1) Extracts final values from assembled document, (2) Queries negotiation transcript for negotiated values, (3) Compares assembled vs. negotiated, (4) Flags mismatches, (5) Blocks finalization until reconciled or override documented.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|-------------------|
| Override Field Completion Rate | 100% | <99% | # of negotiated clauses with populated override fields / total negotiated clauses |
| Transcript-Schema Reconciliation Rate | 100% | <98% | # of handoffs with reconciliation pass completed before assembly / total handoffs |
| Negotiated Value Match Rate | 100% | <99% | # of assembled clauses with values matching negotiated values / total negotiated clauses (validation: transcript audit) |
| Deviation Detection Rate (Pre-Finalization) | 100% | <99% | # of value mismatches detected by diff validator before document sent to counterparty / total mismatches present |
| Handoff Fidelity Rate | 100% | <98% | # of negotiated values reaching assembly agent correctly / total values negotiated in redline |
| Template-ID-Only Rejection Rate | 100% | <99% | # of template-ID-only handoffs correctly rejected for negotiated clauses / total template-ID-only handoffs for negotiated clauses |
| Counterparty-Flagged Discrepancy Rate | 0 | >0 | # of value mismatches discovered by counterparty post-issuance / total issued contracts (baseline: <0.5%) |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Override Field Empty for Negotiated Clause | Clause marked "accepted" with multi-round negotiation history, but override field is empty | CRITICAL | Escalate to redline agent; require population of negotiated_value field with specific deal value; block assembly until populated |
| Transcript-Schema Value Mismatch | Reconciliation pass finds negotiated value in transcript not present in override field | CRITICAL | Block assembly; require human review to populate missing override; verify override matches transcript value |
| Template-ID-Only Handoff for Negotiated Clause | Handoff for clause with multi-round negotiation contains only clause_id and status, no override fields | HIGH | Reject handoff; require complete structured override payload before assembly begins |
| Assembled Value Mismatch | Final assembly diff detects assembled clause value does not match negotiated value from transcript | CRITICAL | Block finalization; escalate to assembly agent; correct clause value to match negotiated value; re-validate before sending to counterparty |
| Counterparty-Flagged Value Discrepancy | Counterparty's redline or sign-off notes flag value mismatch between agreed negotiation and final document | CRITICAL | Immediately halt signature process; trace to source (redline agent, handoff, assembly agent); reconcile; send correction to counterparty; assess impact on credibility/deal |

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [From Confident Closing to Silent Failure: Characterizing False Success in LLM Agents](https://arxiv.org/html/2606.09863)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
- [Handoff Fidelity in Multi-Agent Legal Document Generation](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3913457)
