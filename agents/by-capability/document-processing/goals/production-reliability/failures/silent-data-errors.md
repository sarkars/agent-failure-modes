# Document Extraction Produces Correct-Looking but Wrong Data: Causes and Fixes

## Issue: Extraction Completes Successfully but the Data Relationships Are Wrong

**Frequency**: Very Common

**Symptoms**
- The pipeline reports success and completes without any errors
- No errors are logged and no alerts fire
- The data looks well-formed and valid, but the relationships between values are wrong
- The error is only discovered later, through audits or customer complaints

**Root Cause**
The worst OCR failures are not the ones that throw errors - they are silent failures where the output looks correct, no errors are flagged, and the extraction completes successfully, but the data relationships are wrong.

**Example**
```
Input: Invoice with two tables - "Items Ordered" and "Items Backordered"

Pipeline output:
- Item: Widget A, Qty: 10, Status: Ordered
- Item: Widget B, Qty: 5, Status: Ordered

Actual:
- Widget A: 10 ordered
- Widget B: 5 backordered (from wrong table)

Result: Inventory system expects shipment that's actually backordered
```

**Key Statistic**
88% of businesses still report errors in their data pipelines, with teams spending six or more hours per week fixing "automated" data.

Fixing this means adding structural/relational validation that can catch a well-formed-but-wrong output, since format checks alone never will — the strategies below cover how to build that safety net.

## Mitigation Strategies

### Prevention
1. **Dual independent extraction with cross-comparison**: Run extraction through two independent methods/models and require agreement (or reconciliation) on structurally-important classifications (e.g., which table a line item belongs to), since silent errors specifically arise when a single pipeline produces a well-formed but structurally-wrong result with nothing to check it against. Trade-off: doubles processing cost for the fields/documents where this safeguard is applied.
2. **Business-rule sanity checks specific to document semantics**: Encode domain-specific rules that check for structurally-plausible-but-wrong outcomes (e.g., if a document has both "Ordered" and "Backordered" tables, verify no item's quantity double-counts or its status contradicts an explicit backorder note elsewhere in the document) rather than only generic field-format validation. Trade-off: requires domain expertise to define meaningful rules per document type, and rules can become numerous and hard to maintain as document variety grows.
3. **Table/section provenance tagging through the whole pipeline**: When a document has multiple similar-looking tables or sections, tag every extracted value with which specific table/section it came from and preserve that tag through the full pipeline, so a downstream validation or human reviewer can verify a "Widget B, Qty 5" came from "Items Ordered" and not "Items Backordered" without re-reading the source document. Trade-off: adds metadata overhead throughout the pipeline.

### Detection & Response
1. **Statistical distribution monitoring on extracted value patterns**: Track the statistical distribution of key extracted fields (status values, quantities, category assignments) over time and flag shifts that don't correspond to known business changes, since a silent structural error (e.g., systematically misreading table boundaries) often produces a detectable shift in the aggregate distribution even when individual documents look fine.
2. **Scheduled sample audits against full source re-read**: Regularly select a random sample of "successfully" processed documents and have a human fully re-verify them against the source document (not just spot-check the final numbers), specifically looking for structural/relational errors that wouldn't trigger any format or range validation.
3. **Low-friction customer/downstream feedback channel**: Make it easy and fast for downstream consumers (inventory systems, customers, internal teams) to flag "this looks wrong" even when they can't articulate the exact error, and treat these reports as a primary detection channel for silent errors specifically, since silent errors by definition don't trigger the pipeline's own alerts.

### Architecture Patterns
1. **Structural-relationship validation as a first-class pipeline stage**: Architect a dedicated validation stage focused specifically on structural/relational correctness (right value in right table/section/relationship) as distinct from field-format validation, since these require different logic and are the specific failure mode silent data errors represent.
2. **Provenance-preserving data model**: Design the extracted-data model so every value carries its full provenance (source table/section, extraction method, confidence) through the entire pipeline and into storage, enabling both automated structural checks and human audit without needing to re-extract from source.
3. **Continuous sampling-audit pipeline integrated into production**: Build sample auditing into the standing production pipeline (a defined percentage of documents routed to full human re-verification on an ongoing basis) rather than treating audits as periodic, occasional, manual exercises disconnected from day-to-day operations.

### Metrics
1. **structural_relationship_validation_failure_rate**: Target: < 1% of documents with checkable structural relationships; Alert if > 4%
2. **distribution_shift_detection_rate**: Target: track as baseline; Alert on any statistically significant shift (e.g., z-score > 3) not correlated with a known business change
3. **sample_audit_silent_error_rate**: Target: < 2% of audited "successful" documents found to contain a silent structural error; Alert if > 6%
4. **customer_reported_error_rate**: Target: track as baseline; Alert if it rises > 2x month-over-month

### Alerts
1. **Structural Validation Failure Spike** (P1): Condition - structural-relationship validation failure rate exceeds 4% for a document type. Action: Halt automated acceptance for that type, route to human review, investigate the specific structural-check failure pattern.
2. **Sample Audit Silent Error Rate High** (P1): Condition - scheduled sample audits find silent structural errors in more than 6% of "successfully" processed documents. Action: Treat as a systemic pipeline defect requiring investigation, not an isolated incident; expand audit sampling to bound the affected population.
3. **Distribution Shift Without Business Cause** (P2): Condition - a statistically significant shift in extracted value distribution occurs with no corresponding known business change. Action: Investigate for a silent structural extraction error before assuming the shift reflects genuine business activity.

## References

- [AI Agents and Document Processing 2026](https://parsio.io/blog/ai-agents-document-processing-2026) - 88% pipeline error rate
- [LinkedIn: Silent Failures of Production AI](https://www.linkedin.com/pulse/silent-failures-production-ai-why-most-llm-monitoring-praveen-juyal-iqgyc) - Silent failure patterns
- [IDP Accuracy Reckoning 2026](https://idp-software.com/news/idp-accuracy-reckoning-2026/) - Correct-looking wrong data
