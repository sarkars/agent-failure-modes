# Multi-Agent Handoff Drops Data-Quality Flag Between Cleansing Agent and Downstream Consuming Agent

## Issue: A Data-Cleansing Agent Notes in Free Text That a Field It Cleaned Was Ambiguous or Low-Confidence, but the Structured Cleansed Record Handed Off to a Downstream Risk- or Pricing-Consuming Agent Has No Field for Cleansing Confidence, So the Downstream Agent Treats the Value as Fully Reliable

**Frequency**: Occasional

**Symptoms**
- A downstream risk or pricing calculation uses a cleansed field value with full confidence, even though the data-cleansing agent's own notes describe that field as ambiguous, inferred, or resolved by a low-confidence heuristic rather than a clean source match
- The structured cleansed record handed off to the downstream consuming agent contains the field's final value and a "cleansed" status flag, but no field capturing the cleansing agent's confidence level or method (direct source match vs. inferred/imputed)
- Downstream agents operating purely from the structured cleansed record show a materially higher reliance rate on low-confidence-cleansed fields than agents given the cleansing agent's full reasoning transcript alongside the record
- The low-confidence origin of a field surfaces only when a risk or valuation output is later challenged and a reviewer traces the field back through the cleansing agent's transcript, by which point the output has already been used downstream
- Fields requiring the cleansing agent to choose among multiple plausible source values, or to infer a value from a partial record, make up a disproportionate share of the misses, precisely because those are the cases where a confidence distinction would have changed how downstream agents treated the value

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

### Prevention

1. **Confidence and method fields in the cleansed-record handoff schema**: Extend the structured cleansed record to include `cleansing_confidence: (HIGH|MEDIUM|LOW)` and `resolution_method: (SOURCE_MATCH|INFERRED|IMPUTED)` alongside the final value and cleansed status. Require the cleansing agent to populate both whenever it resolves a field by choosing among conflicting sources or inferring from a partial record, rather than leaving that reasoning in free text only. Root cause: gives the confidence signal a structured home so it cannot be dropped simply because it originated as narrative reasoning.

2. **Confidence-aware consumption gate in downstream agents**: Require risk- and pricing-consuming agents to check `cleansing_confidence` before using a field in a calculation; on MEDIUM or LOW, either widen the associated uncertainty band, require a secondary source check, or route the value to human confirmation before it feeds a published output. Root cause: closes the gap where a downstream agent has no incentive to look past the fields its own logic already consumes.

3. **Multi-source disagreement flag independent of final resolution**: Whenever two or more source feeds disagree on a field's value, record that disagreement as a structured flag (`source_disagreement: true`, with the conflicting values) regardless of how the cleansing agent ultimately resolved it, so downstream agents can see that a choice was made even without reading the reasoning behind it.

### Detection & Response

1. **Cleansing-note-to-schema reconciliation audit**: Periodically scan the cleansing agent's free-text notes for confidence-qualifying language ("resolved to", "inferred from", "pattern match", "feeds disagree") and cross-check that the corresponding structured record has `cleansing_confidence` set below HIGH and `resolution_method` populated accordingly. Flag and log any mismatch as a handoff gap.

2. **Post-hoc confidence-outcome reconciliation**: When a risk or valuation output is challenged or fails model validation, trace the fields it depended on back to their `cleansing_confidence` values; track whether LOW/MEDIUM-confidence fields are disproportionately represented among challenged outputs, independent of whether the specific field in question turns out to have been wrong.

### Architecture Patterns

1. **Confidence-Aware Cleansed Record**: Cleansed record schema carries `value`, `cleansed_status`, `cleansing_confidence`, `resolution_method`, and `source_disagreement` as first-class fields populated at cleansing time, not inferred downstream from a raw value with no accompanying metadata.

2. **Downstream Confidence Gate**: A consumption-time check in risk/pricing agents that reads `cleansing_confidence` before use; on MEDIUM/LOW, either widens the uncertainty band applied to the value, triggers a secondary-source check, or blocks automated use pending human confirmation, with the action logged for audit.

3. **Source-Disagreement Ledger**: An independent log of every field where source feeds disagreed at cleansing time, keyed by field and resolution method, queryable separately from the final cleansed value so a reviewer can audit resolution patterns across many records without re-reading each transcript.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Confidence-Field Population Rate | 100% | <98% | # of cleansing records where free-text notes contain confidence-qualifying language and `cleansing_confidence`/`resolution_method` are populated / total records with such language |
| Downstream Confidence-Gate Trigger Rate | tracked, no fixed target | sustained spike vs. trailing baseline | # of downstream uses where a MEDIUM/LOW-confidence field triggered a widened band, secondary check, or hold / total downstream uses of cleansed fields |
| Challenged-Output Low-Confidence Concentration | tracked, no fixed target | LOW/MEDIUM fields >2x their base rate among challenged outputs | Share of challenged risk/valuation outputs that depended on a LOW/MEDIUM-confidence field, vs. the base rate of such fields across all outputs |
| Model-Validation Miss Rate | 0% | >0.2% | # of quarterly model-validation discrepancies traced to a cleansed field with no confidence flag set / total discrepancies |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Confidence Language Not Reflected in Schema | Cleansing notes contain confidence-qualifying language but `cleansing_confidence` is left at HIGH (or unset) in the handed-off record | P1 | Block record from downstream consumption; escalate to data-ops for manual confidence determination |
| Output Published on Low-Confidence Field | Downstream agent uses a LOW-confidence field without triggering the confidence gate | P1 | Flag the output; require secondary-source confirmation before it is relied upon further |
| Model-Validation Discrepancy Traced to Unflagged Field | Quarterly model-validation review finds a discrepancy traced to a cleansed field that carried no confidence flag | P2 | Investigate why the confidence gate did not trigger; audit similar fields resolved by the same cleansing pathway |


## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
- [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439)
