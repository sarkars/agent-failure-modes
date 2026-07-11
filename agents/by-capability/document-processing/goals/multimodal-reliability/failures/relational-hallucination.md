# Relational Hallucination

## Issue: Relational Hallucination

**Frequency**: Common

**Symptoms**
- Spatial or logical relationships between elements incorrect
- Line items assigned to wrong columns
- Parent-child relationships inverted
- Table cells matched to wrong headers

**Root Cause**
VLMs struggle with precise spatial reasoning. They process images as sequences of patches and must infer grid structure implicitly.

**Example**
```
Input: Table with "Quantity" and "Unit Price" columns

| Item      | Quantity | Unit Price |
|-----------|----------|------------|
| Widget A  | 5        | $10.00     |

Extracted: Widget A, Quantity: $10.00, Unit Price: 5

Result: Data integrity failure, downstream calculations wrong
```

**Key Statistic**
VLMs lack robust spatial perception because they need to infer the number of rows and columns implicitly on a large two-dimensional cell grid rather than reading it directly.

## Mitigation Strategies

### Prevention
1. **Specialized table-structure detection before value extraction**: Run a dedicated table/grid detection model to establish the explicit row-column structure and header-to-cell mapping before the VLM extracts values, rather than asking the VLM to simultaneously infer grid layout and read content — spatial grid inference is exactly what VLMs are weak at, so don't make them do it implicitly. Trade-off: adds a model call and creates a new dependency on the table detector's own accuracy on complex layouts.
2. **Header-semantics-to-value type verification**: After extraction, verify that each value's type/format matches its assigned header's semantic expectation (a "Quantity" column value should be an integer without a currency symbol; a "Unit Price" column value should carry currency formatting) and flag mismatches as likely column-swap errors. Trade-off: requires maintaining semantic type expectations per header label, which varies by document template/language.
3. **Column-position anchoring using header coordinates**: Anchor each data cell's column assignment to the x-coordinate of its detected header rather than relying purely on the model's left-to-right reading order inference, since positional anchoring is more robust to VLM patch-sequence processing quirks than implicit column-count inference. Trade-off: requires reliable header bounding-box detection, which itself can fail on tables with unusual header layouts.

### Detection & Response
1. **Semantic type-mismatch flagging as primary detection signal**: Treat any cell where the value's format doesn't match its column header's expected type (a dollar amount under "Quantity," an integer under "Unit Price") as a near-certain relational hallucination and flag for review — this is a cheap, high-precision check specific to this failure mode.
2. **Row-internal consistency checks**: Validate that a table row's cross-column relationships hold (e.g., Quantity × Unit Price should equal or approximate a Line Total column if present); a broken internal relationship signals values assigned to wrong columns even when each individual value looks plausible.
3. **Column-swap pattern monitoring**: Track whether specific column-pair swaps (e.g., "Quantity ↔ Unit Price") recur across documents from the same source/template, since a systematic swap pattern indicates a structural extraction bug rather than random noise, and is fixable at the pipeline level rather than needing per-document correction.

### Architecture Patterns
1. **Structure-detector + content-extractor split pipeline**: Architect table processing as two distinct stages — a structure model establishing grid/header layout, and a content model populating cells against that established structure — so relational errors (wrong column assignment) and content errors (wrong value read) are diagnosed and fixed independently.
2. **Semantic-type-schema validation gate**: Define an explicit expected-type schema per column header pattern (numeric, currency, date, text) and validate every extracted cell against it as a mandatory gate before the table is accepted, catching column-swap errors structurally rather than relying on downstream consumers to notice.
3. **Position-anchored extraction with coordinate verification**: Require extraction to report the (row, column) coordinate it assigned to each value alongside the value itself, and cross-check that coordinate against the independently-detected header positions, rather than trusting the model's implicit column-assignment reasoning alone.

### Metrics
1. **semantic_type_mismatch_rate**: Target: < 2% of extracted cells; Alert if > 8%
2. **row_internal_consistency_failure_rate**: Target: < 3% of rows with checkable relationships; Alert if > 10%
3. **recurring_column_swap_rate**: Target: track as baseline per document template; Alert if a specific swap pattern occurs > 5% of documents from a source
4. **structure_detector_content_extractor_agreement_rate**: Target: > 97% agreement on column count/header mapping between stages; Alert if < 90%

### Alerts
1. **Semantic Type Mismatch Spike** (P1): Condition - semantic type-mismatch rate exceeds 8% for a document source. Action: Halt automated acceptance for that source, route affected documents to human review, investigate structure-detection accuracy for that template.
2. **Recurring Column Swap Pattern** (P2): Condition - a specific column-pair swap occurs in more than 5% of documents from one source. Action: Fix the structural extraction logic for that source's template rather than continuing to rely on per-document correction.
3. **Row Consistency Failure Spike** (P2): Condition - row-internal consistency failure rate exceeds 10%. Action: Investigate whether structure detection is misaligning headers to columns for that document type.

## References

- [Hallucination of Multimodal LLMs Survey](https://arxiv.org/html/2404.18930v2) - Relational hallucination analysis
- [VLMs for Spreadsheet Understanding](https://arxiv.org/html/2405.16234v1) - Spatial perception limitations
- [Table Extraction Using LLMs](https://nanonets.com/blog/table-extraction-using-llms-unlocking-structured-data-from-documents/) - Column alignment challenges
