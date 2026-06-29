# Multi-Agent Handoff Drops Data-Quality Flag Between Cleansing Agent and Downstream Consuming Agent

## Issue: A Data-Cleansing Agent Notes in Free Text That a Field It Cleaned Was Ambiguous or Low-Confidence, but the Structured Cleansed Record Handed Off to a Downstream Risk- or Pricing-Consuming Agent Has No Field for Cleansing Confidence, So the Downstream Agent Treats the Value as Fully Reliable

**Frequency**: Occasional

**Symptoms**
- A downstream risk or pricing calculation uses a cleansed field value with full confidence, even though the data-cleansing agent's own notes describe that field as ambiguous, inferred, or resolved by a low-confidence heuristic rather than a clean source match
- The structured cleansed record handed off to the downstream consuming agent contains the field's final value and a "cleansed" status flag, but no field capturing the cleansing agent's confidence level or method (direct source match vs. inferred/imputed)
- Downstream agents operating purely from the structured cleansed record show a materially higher reliance rate on low-confidence-cleansed fields than agents given the cleansing agent's full reasoning transcript alongside the record
- The low-confidence origin of a field surfaces only when a risk or valuation output is later challenged and a reviewer traces the field back through the cleansing agent's transcript, by which point the output has already been used downstream
- The mismatch concentrates on fields where the cleansing agent had to choose among multiple plausible source values or infer a value from a partial record, since those are the cases where a confidence distinction would matter most

**Root Cause**
The downstream consuming agent's logic operates on the structured cleansed record's fixed schema, and that schema was built to track whether a field was cleansed and what its final value is, not the confidence or method behind that cleansing. Because a low-confidence resolution is expressed through the cleansing agent's free-text reasoning rather than a structured confidence field, it has no corresponding place in the handoff schema and is therefore invisible to the downstream agent, even though the same model, given the full cleansing transcript, would readily flag the value as uncertain.

**Example**
```
Data-cleansing agent reconciles a corporate bond's maturity date across two source feeds that show different values, and notes in free text: "Feeds disagree by 6 months; resolved to the later date based on a pattern match to the issuer's typical amortization schedule, not a confirmed source value"
Cleansing agent records the resolved maturity date in the structured cleansed record with status "cleansed," with no field for resolution confidence or method
Structured record handed off to a downstream risk-duration agent shows the maturity date as cleansed, with no indication it was inferred rather than source-confirmed
Risk-duration agent uses the inferred maturity date with full confidence in a portfolio duration calculation
Discrepancy surfaces during a quarterly model-validation review when the actual maturity date, confirmed from the bond's prospectus, differs from the inferred value used in the duration calculation
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Surveys of multi-agent LLM system failures identify narrow handoff interfaces between staged agents, where a downstream agent's structured input omits a confidence or provenance signal an upstream agent's free-text reasoning surfaced, as a distinct and recurring failure category | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Platform-orchestrated agentic workflow failure studies find that narrowing the interface between orchestrated stages to a fixed value-plus-status schema is a primary mechanism by which a confidence or method signal present upstream fails to reach a downstream consuming stage | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |
| Research on agentic AI applied to financial-services modeling and model-risk-management tasks identifies the absence of a shared, confidence-aware structured state between sequential cleansing and consuming agents as a distinct reliability gap from either agent's individual accuracy | [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439) |

**Contributing Factors**
- Structured cleansed-record schema tracks only final field value and cleansed/not-cleansed status, with no field for resolution confidence or method
- Cleansing agent's reasoning about ambiguous or inferred resolutions is recorded only in free-text notes, with no structured escalation path into the downstream consuming agent's input
- No mandatory flag or hold is triggered in downstream calculations when the cleansing agent's free-text notes contain low-confidence or inference language, since the consuming agent's logic does not parse those notes

---

## Mitigation Strategies

1. **Add a Cleansing-Confidence Field to the Handoff Schema**: Require the cleansing agent to record a confidence level and resolution method (direct source match, vendor-confirmed, inferred/imputed) for every field in a dedicated structured field passed to downstream consumers, rather than leaving it only in free-text notes
2. **Downstream Agent Cross-Checks Cleansing Transcript for Low-Confidence Language**: Require downstream consuming agents to scan the cleansing agent's free-text notes for ambiguity or inference language before using a field with full confidence, not just the structured value-and-status field
3. **Mandatory Flag on Low-Confidence Fields in Risk and Pricing Outputs**: Automatically flag any risk or pricing calculation that consumed a field cleansed with low confidence or by inference, requiring it to be surfaced to reviewers rather than presented identically to a fully source-confirmed value
4. **Track Confidence-Field-Absent Downstream Usage Rate**: Continuously measure how often a low-confidence-cleansed field is used in a downstream calculation with no confidence flag carried through the handoff

### Metrics
- Rate of downstream calculations that consumed a field whose cleansing transcript contained ambiguity or inference language not reflected in a structured confidence field
- Time between a downstream output's use and a later-discovered cleansing error traced to a low-confidence field
- Downstream reliance rate on low-confidence-cleansed fields, segmented by presence vs. absence of a structured confidence field in the handoff

### Alerts
- A risk or pricing calculation uses a field whose cleansing transcript contains unresolved ambiguity or inference language with no structured confidence flag → P1
- A downstream output is found via review to have relied on a low-confidence-cleansed field that was later confirmed incorrect → P1
- Confidence-field-absent downstream usage rate across a rolling window exceeds the defined threshold → P2

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
- [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439)
