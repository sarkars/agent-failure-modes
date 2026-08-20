# One Bad Extraction Cascades Into Every Downstream System: Causes and Fixes

## Issue: A Single Extraction Error Cascades Across Downstream Systems

**Frequency**: Common

**Symptoms**
- Agent extracts one wrong value and it silently corrupts multiple downstream systems
- The bad value propagates to other systems before anyone detects the original error
- Cleanup after the fact requires touching every system the value reached

**Root Cause**
Automation moves data faster - meaning bad inputs create even bigger issues downstream. Errors in GL coding, invoice matching, or field mapping propagate across financial reports and compliance processes in real time.

**Example**
```
OCR extracts vendor: "ABC Corp" (actual: "ABG Corp")

Downstream impact:
- Payment routed to wrong vendor in AP system
- Spend analytics misattribute purchase
- Tax reporting shows incorrect vendor payments
- Audit flags unexplained vendor discrepancy
```

Fixing this means stopping trust in a single extracted value from carrying unchecked across every system it touches — the strategies below add validation and blast-radius limits at each hop instead of only at the source.

## Mitigation Strategies

### Prevention
1. **Validation gate at every integration boundary**: Insert a validation check (format, plausibility, reference-lookup) immediately before data crosses into each downstream system (AP, tax reporting, spend analytics), rather than validating once at extraction and trusting the value through every subsequent hop — cascading errors specifically happen because a single bad value is trusted uniformly across many systems. Trade-off: adds latency and validation logic at each integration point rather than a single centralized check.
2. **Reference/master-data lookup verification before propagation**: For fields like vendor name/ID that key into master data, verify the extracted value resolves to exactly one valid master-data record (not a fuzzy/near match) before allowing it to propagate to any downstream system, since a near-miss value like "ABC Corp" vs "ABG Corp" is exactly the kind of error that passes a naive "looks like a valid vendor name" check. Trade-off: strict matching increases the rate of legitimate documents requiring human resolution when the extracted name has natural variation (abbreviations, DBA names).
3. **Batch/blast-radius boundaries**: Limit how many downstream records a single automated push can affect before requiring a checkpoint or confirmation, so a systematic extraction error (e.g., a bad OCR run affecting every document in a batch) cannot silently propagate across the entire batch before detection. Trade-off: adds friction/latency to legitimate high-volume processing.

### Detection & Response
1. **Cross-system consistency reconciliation**: Periodically reconcile the same entity's data across systems it was propagated to (AP, tax, analytics) and flag discrepancies, since an error that has already cascaded is often still detectable by comparing systems against each other rather than only against the original source document.
2. **Anomaly detection on propagated values**: Monitor for statistically anomalous values entering downstream systems (a vendor receiving payments that don't match its historical pattern, a GL code suddenly used far more or less often than baseline) as an independent detection layer beyond point-of-entry validation.
3. **Audit-flagged discrepancy fast-tracking**: When an audit or compliance process flags a discrepancy that traces back to an extraction error, treat it as a signal to check for the same error pattern across other recently-processed documents from the same source, not just fix the single flagged instance.

### Architecture Patterns
1. **Soft-delete / recoverable original data**: Never overwrite or hard-delete the original extracted value when downstream corrections are made; retain it in a recoverable form so that when a cascading error is discovered, the blast radius (all downstream writes derived from the bad value) can be identified and reversed.
2. **Rollback-capable downstream writes**: Architect downstream integrations (AP, ERP, tax systems) to support reversal of a batch of writes tied to a specific source document or extraction run, rather than only supporting forward-only appends, so a discovered cascading error can be surgically undone.
3. **Staged propagation with confirmation checkpoints**: For high-blast-radius operations (payment runs, tax filings), stage the propagation through a checkpoint that requires either automated validation confidence or human confirmation before the final, hard-to-reverse step (actual payment, filed report) executes.

### Metrics
1. **cross_system_reconciliation_discrepancy_rate**: Target: < 0.5% of entities show cross-system discrepancy; Alert if > 2%
2. **master_data_resolution_ambiguity_rate**: Target: < 1% of extracted reference fields fail to resolve to exactly one master-data record; Alert if > 5%
3. **cascading_error_blast_radius**: Target: < 5 downstream records affected per detected error; Alert if any single error traces to > 25 affected records
4. **rollback_capability_coverage**: Target: 100% of high-blast-radius integrations support rollback; Alert on any integration lacking rollback capability

### Alerts
1. **Cross-System Discrepancy Spike** (P1): Condition - reconciliation discrepancy rate between systems exceeds 2%. Action: Halt further propagation from the source pipeline, trace discrepancies back to their origin document(s), assess blast radius before resuming.
2. **Master Data Resolution Ambiguity Spike** (P2): Condition - reference-field resolution ambiguity rate exceeds 5% for a document source. Action: Route affected documents to human review for master-data matching rather than allowing best-guess propagation.
3. **Large Blast Radius Detected** (P1): Condition - a single detected extraction error is found to have propagated to more than 25 downstream records. Action: Trigger rollback procedures for all affected records, treat as an incident requiring root-cause review of the validation gate that should have caught it earlier.

## References

- [AlterSquare: Document AI Fails](https://altersquare.io/enterprise-document-ai-fails-extraction-layer-not-model-layer/) - Downstream propagation
- [Production-Ready AI Agent for Document Extraction](https://www.stackai.com/insights/how-to-build-a-production-ready-ai-agent-for-document-data-extraction) - Validation gates
- [IDP Accuracy Reckoning 2026](https://idp-software.com/news/idp-accuracy-reckoning-2026/) - GL coding error impact
