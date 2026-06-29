# Multi-Agent Handoff Drops Fact-Checker's Statistical Caveat Before Publishing

## Issue: A Fact-Checking Agent's Free-Text Note That a Statistical Claim Is Approved Only With a Specific Qualifier (e.g., "True for the U.S. Market Only" or "Based on a 2023 Sample, Reverify Before Reuse After mid-2026") Is Not Captured in the Structured Approve/Reject Schema Passed to the Downstream Publishing Agent, Which Publishes the Statistic Globally and Without the Qualifier as a Flatly Approved Fact

**Frequency**: Occasional

**Symptoms**
- Published content states a statistic as a flat, unqualified fact when the fact-checking agent's review notes had approved it only with a specific scope or expiration caveat
- The fact-checking agent's transcript or reasoning log contains the caveat in free text, but the structured field passed to the publishing agent (typically a simple approved/rejected boolean or status enum) has no field to carry it
- The publishing agent's own logs show it received only an "approved" status with no qualifier text, confirming the caveat was generated but not transmitted
- The same statistic, when fact-checked again independently, is flagged by a reviewer as needing the qualifier that was silently dropped the first time
- The gap reproduces consistently for any caveat attached to an otherwise-approved claim, not just occasionally, because the handoff schema structurally has no slot for it

**Example**
```
Fact-checking agent reviews the claim "73% of renters say in-unit laundry is a top-three priority" against a cited
2023 industry survey and approves it, but its reasoning notes: "Approved -- caveat: this figure is U.S.-only and from
a 2023 survey; if reused for non-U.S. content or after the survey is superseded, re-verify"
The handoff to the publishing agent uses a structured schema with fields {claim_id, status: approved/rejected,
source_id}; there is no field for a scoping or expiration caveat
Publishing agent receives {claim_id: 4471, status: approved, source_id: SRC-2023-114} and publishes the statistic
in a UK-market blog post with no scope qualifier, presenting it as a flat global fact
A reader in the UK market questions the figure's applicability; on review, the original fact-check caveat is found
in the fact-checking agent's reasoning log but was never present anywhere in the publishing pipeline
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent system failure analysis identifies information loss at agent-to-agent handoffs -- where one agent's full reasoning is compressed into a narrower structured interface consumed by the next agent -- as one of the most common root causes of multi-agent task failure | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Execution-provenance research for LLM agent pipelines argues that without traceable links from a downstream agent's action back to the full upstream finding, qualifiers and conditions attached to an approval are easily and silently lost in transit | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |
| Broader failure-mode research on LLM systems documents structured-interface bottlenecks between pipeline stages as a recurring mechanism by which a correctly generated finding fails to reach the stage where it needs to take effect | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |

**Contributing Factors**
- The structured handoff schema between fact-checking and publishing agents was designed around a binary approve/reject decision, with no field anticipated for conditional or scoped approvals
- The fact-checking agent's full reasoning text is logged but not treated as part of the authoritative handoff payload the publishing agent is required to consult
- No validation step checks whether an "approved" status was accompanied by caveat language in the reasoning log before allowing unscoped publication
- Caveats are relatively rare compared to flat approvals, so the missing schema field had not surfaced as a problem until a claim with a caveat was reused outside its original scope

---

## Mitigation Strategies

1. **Add a Structured Caveat Field**: Extend the approve/reject handoff schema with an explicit, always-checked caveat or scope field, defaulting to "none" rather than being absent, so the publishing agent cannot proceed without acknowledging it
2. **Block Unscoped Reuse of Scoped Approvals**: When a caveat field is populated, require the publishing agent to either include the qualifier in the published text or route to human review before publishing without it
3. **Reasoning-Log Cross-Check**: Run an automated check comparing the fact-checking agent's free-text reasoning against the structured handoff payload to flag any approval whose reasoning contains caveat language not reflected in a structured field
4. **Expiration-Aware Claim Reuse**: For caveats tied to a time window (e.g., "reverify after mid-2026"), store an explicit expiration date on the claim record so any future reuse attempt after that date triggers mandatory re-verification regardless of handoff schema completeness

### Metrics
- Rate of fact-checking approvals containing caveat language in free-text reasoning with no corresponding structured caveat field populated
- Number of published claims later found to have been published outside the scope of their original fact-check approval
- Time between caveat-loss incidents and detection via reader or reviewer report versus automated cross-check

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Caveat language detected with no structured field | Fact-checker reasoning log contains scope/expiration language not present in structured handoff payload | P2 | Block publishing agent from proceeding; backfill structured caveat field |
| Scoped claim published without qualifier | Publishing agent publishes a claim carrying a populated caveat field without including the qualifier in the text | P1 | Pull content for correction; review publishing-agent caveat-handling logic |
| Expired claim reused | Claim with an expiration-tagged caveat is reused in new content after its expiration date | P2 | Force re-verification before allowing publication |

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
