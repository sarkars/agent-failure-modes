# Multi-Agent Handoff Drops Specialist-Noted Contraindication Before Care-Plan Finalization

## Issue: A Specialist-Consult Agent That Identifies, in Its Own Consult-Note Reasoning, a Contraindication to a Specific Treatment Approach Hands That Finding Off to a Primary Treatment-Planning Agent Through a Structured Consult Summary That Has No Field for Contraindications, So the Treatment-Planning Agent Finalizes a Care Plan Including the Approach the Specialist Had Ruled Out

**Frequency**: Occasional

**Symptoms**
- The specialist-consult agent's note explicitly states a specific treatment approach is contraindicated given a finding from the consult, but the structured consult summary handed to the treatment-planning agent contains only the consult's general recommendation field, with no contraindication flag
- The treatment-planning agent, which builds the care plan from the structured consult summary, includes the contraindicated approach because the summary's schema gives it no reason not to
- Re-reading the specialist-consult agent's full consult-note transcript clearly shows the contraindication was identified and reasoned through; it simply never reached a structured field the treatment-planning agent reads
- The gap concentrates on contraindications that are specific to the individual patient's consult findings rather than a standard, widely known contraindication already encoded in general clinical-guideline references the treatment-planning agent might otherwise check
- The error surfaces only when a clinician manually cross-references the full specialist consult note against the finalized care plan, since the care plan otherwise reads as complete and clinically reasonable

**Root Cause**
The specialist-consult agent and the treatment-planning agent communicate through a structured consult-summary schema that captures the consult's general recommendation but has no dedicated field for a patient-specific contraindication identified during that consult, so any such finding exists only in the consult agent's narrative reasoning and is invisible to the treatment-planning agent's plan-generation process. The treatment-planning agent has no mechanism to discover the contraindication because it never consults the specialist agent's full reasoning, only the structured summary the schema permits.

**Example**
```
Specialist-consult agent reviews a patient's cardiology workup ahead of a planned orthopedic procedure, noting: "Patient's recent stress test shows findings that contraindicate the standard regional anesthesia approach typically paired with this procedure; general anesthesia protocol should be used instead"
Specialist agent's structured consult summary handed to the treatment-planning agent includes only a general recommendation field: "Cleared for procedure with cardiology monitoring"; no contraindication field exists in the schema
Treatment-planning agent finalizes the care plan using the standard regional anesthesia approach, the exact approach the specialist's consult note had ruled out
Anesthesia team discovers the contraindication only when manually reviewing the full cardiology consult note shortly before the procedure, requiring a late plan change
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM systems exhibit a documented failure category where a determination established by one agent is lost or never reaches a downstream agent's effective input, distinct from either agent reasoning incorrectly on its own | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Studies of collaborative failure modes in medical multi-agent systems identify structured finding propagation between consult and planning agents as a distinct reliability requirement separate from either agent's individual diagnostic accuracy | [MedAgentAudit: Diagnosing and Quantifying Collaborative Failure Modes in Medical Multi-Agent Systems](https://arxiv.org/pdf/2510.10185) |
| Tiered multi-agent healthcare systems are shown to require explicit, structured escalation and constraint-passing between agent tiers because narrative consult notes alone do not reliably propagate safety-relevant restrictions | [Tiered Agentic Oversight: A Hierarchical Multi-Agent System for Healthcare Safety](https://arxiv.org/pdf/2506.12482) |

**Contributing Factors**
- The consult-summary schema has a general recommendation field but no dedicated, structured field for patient-specific contraindications identified during the consult
- The treatment-planning agent's plan-generation process consults only the structured consult summary, never the specialist agent's full consult-note transcript
- No reconciliation step compares contraindication language in the specialist agent's consult note against what the structured summary actually encodes before the care plan is finalized

---

## Mitigation Strategies

1. **Structured Contraindication Field in Consult-Summary Schema**: Extend the consult-summary schema to carry an explicit, mandatory-to-populate contraindication field, and require the specialist-consult agent to write any patient-specific contraindication directly into it rather than leaving it in narrative consult-note form only
2. **Mandatory Pre-Finalization Contraindication Check**: Before a treatment-planning agent finalizes a care plan, require an automated check of the structured contraindication field from any relevant specialist consult, blocking finalization on any unresolved discrepancy
3. **Consult-Note-to-Summary Reconciliation Pass**: Run an automated pass comparing every contraindication-related statement in the specialist's consult-note transcript against the structured summary, flagging any contraindication mentioned in the note but absent from structured fields
4. **Treatment-Planning Agent Access to Full Consult Rationale**: Require the treatment-planning agent's plan-generation step to have direct access to the specialist's full consult-note transcript, not only the structured summary, for any case involving a specialist consult

### Metrics
- Rate of care plans where a relevant specialist consult note contains contraindication language not reflected in the structured consult summary
- Rate of care-plan changes required late in the planning process due to a missed specialist-identified contraindication
- Time between contraindication identification during consult and its incorporation into the structured consult summary

### Alerts
- A care plan is finalized including an approach a specialist consult note explicitly identified as contraindicated → P1
- A specialist consult note contains contraindication language not reflected in the structured summary before care-plan finalization → P2
- Contraindication-reconciliation mismatch rate exceeds the defined threshold for a rolling window → P2

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [MedAgentAudit: Diagnosing and Quantifying Collaborative Failure Modes in Medical Multi-Agent Systems](https://arxiv.org/pdf/2510.10185)
- [Tiered Agentic Oversight: A Hierarchical Multi-Agent System for Healthcare Safety](https://arxiv.org/pdf/2506.12482)
