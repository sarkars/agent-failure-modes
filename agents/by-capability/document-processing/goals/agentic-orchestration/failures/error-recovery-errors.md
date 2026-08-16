# Agent "Fixes" Correct Data and Corrupts It: Causes and Fixes

## Issue: The agent's own error-recovery step corrects a value that wasn't actually wrong, corrupting good data to satisfy a validation check

**Frequency**: Occasional

**Symptoms**
- Agent attempts to fix a detected extraction error
- The "fix" introduces new errors or corrupts data that was already correct
- Cascading corrections worsen overall accuracy instead of improving it

**Root Cause**
When agents detect errors and attempt corrections without sufficient context, they may "fix" things that weren't broken or make changes that violate constraints.

**Example**
```
Extracted invoice lines:
1. Widget A - $100 - Qty 5 - Total $500
2. Widget B - $150 - Qty 3 - Total $450
Extracted Grand Total: $900 (misread, actual $950)

Agent "fix": Notices mismatch, adjusts Widget B total to $400 to match

Result: Agent "corrected" good data to match bad extraction
```

## How to Fix Agent Self-Correction Errors

## Mitigation Strategies

### Prevention
1. **Correction scope constraints**: Explicitly define, per field type, whether it is "correctable" (agent may adjust it based on validation failures) or "fixed" (only ever taken from direct extraction, never algorithmically adjusted). Line items extracted directly from a table should generally be fixed; a computed total should be the correctable side of a mismatch. Trade-off: requires a per-template policy decision that must be maintained as document templates change.
2. **Confidence-gated correction**: Only permit the agent to modify a value if its own extraction confidence for that value was below a threshold; high-confidence extractions should never be "corrected" to satisfy an unrelated validation check. Trade-off: if confidence scoring itself is miscalibrated, this gate provides false safety.
3. **Reliability-ranked validation**: When a cross-check fails (e.g., sum of line items != stated total), always adjust the less-reliable field type first (per a pre-established reliability ranking: line items > subtotals > grand totals for most invoice templates) rather than adjusting whichever field happens to be evaluated last in the correction loop.

### Detection & Response
1. **Correction audit logging**: Log every value the agent changes after initial extraction, including what triggered the correction and the before/after values, so any "fix" that introduced an error can be traced back and reviewed.
2. **Post-correction re-validation**: After any automated correction, re-run the full validation suite (not just the check that triggered the correction) to catch cases where fixing one inconsistency introduced a new one elsewhere.
3. **Correction rate monitoring by field**: Track how often each field type gets algorithmically corrected; a field that's "corrected" unusually often likely has an upstream extraction quality problem that correction is masking rather than fixing.

### Architecture Patterns
1. **Immutable extraction + separate correction ledger**: Store the original extracted value as immutable, and record any correction as a separate, reversible ledger entry with justification — never overwrite the original in place. This lets a bad correction be rolled back without re-running extraction.
2. **Confidence-threshold human gate**: Route any correction affecting a field above a materiality threshold (e.g., financial fields over a dollar amount, or any field with downstream compliance implications) to mandatory human approval before it's applied, regardless of the agent's confidence in the fix.
3. **Deterministic reconciliation over generative correction**: Where a correction is really just arithmetic (totals should equal sum of line items), use a deterministic recompute rather than asking the LLM to "fix" the value generatively — reserve LLM-based correction for cases with genuine ambiguity.

### Metrics
1. **correction_introduced_error_rate**: Target: < 1% of automated corrections found to introduce a new error on audit; Alert if > 5%
2. **field_correction_frequency**: Target: track per field type as baseline; Alert if any field's correction rate exceeds 2x its historical baseline
3. **post_correction_revalidation_pass_rate**: Target: > 99%; Alert if < 95%
4. **human_gate_bypass_rate**: Target: 0% of above-threshold corrections applied without human approval; Alert on any occurrence

### Alerts
1. **Correction-Introduced Error Detected** (P1): Condition - audit sampling finds an automated correction that made extracted data less accurate. Action: Disable auto-correction for that field/template pending review, re-process affected documents.
2. **Field Correction Frequency Spike** (P2): Condition - a specific field's correction rate exceeds 2x baseline. Action: Investigate whether upstream extraction quality has degraded for that field rather than continuing to rely on correction to compensate.
3. **Human Gate Bypass** (P1): Condition - a correction above the materiality threshold was applied without the required human approval step. Action: Immediately audit the affected document, halt the pipeline path that allowed the bypass, and fix the gating logic.

## References

- [Production-Ready AI Agent for Document Extraction](https://www.stackai.com/insights/how-to-build-a-production-ready-ai-agent-for-document-data-extraction) - Error handling strategies
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Recovery failure modes
- [AlterSquare: Document AI Fails](https://altersquare.io/enterprise-document-ai-fails-extraction-layer-not-model-layer/) - Cascading correction errors
