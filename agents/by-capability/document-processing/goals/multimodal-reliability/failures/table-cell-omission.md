# Table Cell Omission

## Issue: Cell Omission and Merging

**Frequency**: Very Common

**Symptoms**
- Table rows or columns missing from output
- Multiple cells treated as single cell
- Sparse tables with empty cells cause column misalignment

**Root Cause**
VLMs sometimes struggle to split multiple cells and mistakenly treat them as a single cell. Spatial perception limitations make grid inference unreliable.

**Example**
```
Input: 
| Product | Q1   | Q2   | Q3   | Q4   |
|---------|------|------|------|------|
| Alpha   | 100  |      | 150  |      |
| Beta    | 200  | 250  |      | 300  |

Extracted (misaligned):
Product: Alpha, Q1: 100, Q2: 150, Q3: [missing], Q4: [missing]
Product: Beta, Q1: 200, Q2: 250, Q3: 300, Q4: [missing]

Result: Q2 and Q4 data lost or misattributed
```

**Key Statistic**
Table extraction works effectively in most cases, but sparse tables with multiple empty cells present a unique challenge. The model sometimes mismatches columns, leading to errors in the extracted tabular data.

## Mitigation Strategies

### Prevention
1. **Two-stage structure-then-content parsing**: Detect the full table grid (including empty cells) as a structural pass before content extraction, so the extraction step fills in values against a pre-established fixed-size grid rather than inferring grid size from however many non-empty values it happens to find. Trade-off: requires the structure detector to correctly identify sparse/empty regions as part of the grid, which is itself a hard vision problem.
2. **Explicit empty-cell modeling**: Require the extraction schema to explicitly represent every cell in the detected grid, including empty ones (as `null` or an explicit "empty" marker), rather than allowing the model to simply skip cells with no visible content — skipping is exactly what causes column-count drift and misattribution in sparse tables. Trade-off: increases output verbosity and requires downstream consumers to handle explicit nulls rather than absent keys.
3. **Header-position column anchoring**: Anchor each column's data extraction to the x-coordinate range of its header, independent of how many values are actually present in that column for a given row, so a row with several empty cells doesn't cause remaining values to shift into the wrong column. Trade-off: requires reliable header bounding-box detection as a prerequisite.

### Detection & Response
1. **Column-count consistency validation against schema**: After extraction, verify that every row has exactly the expected number of columns (matching the detected header count), and flag any row with a mismatched count as a likely cell-omission/misalignment case rather than silently accepting a shorter row.
2. **Sparse-table-specific accuracy audits**: Specifically track extraction accuracy on tables with a high proportion of empty cells (sparse tables), since aggregate accuracy across mostly-dense tables can mask a much higher error rate concentrated in sparse ones.
3. **Value-shift pattern detection**: Check whether values in a row appear systematically shifted left relative to their expected column (a signature of omitted-cell collapse) by comparing extracted values' apparent types against their assigned column's expected type across the full table.

### Architecture Patterns
1. **Fixed-grid extraction against pre-detected structure**: Architect extraction so the model fills a pre-established, fixed-dimension grid (rows × columns from the structure-detection stage) rather than free-form generating a variable-length row per line — this removes the model's ability to silently collapse a row by skipping empty cells.
2. **Post-extraction schema validation gate**: Insert a mandatory validation step that checks every extracted row against the expected column count and flags/rejects any mismatch before the table is accepted, rather than relying on downstream consumers to notice a shifted column mapping.
3. **Sparse-table specialized handling path**: Route tables flagged (during structure detection) as having a high proportion of empty cells through a variant extraction path specifically tuned/prompted for explicit empty-cell modeling, rather than using the same generic extraction path for both dense and sparse tables.

### Metrics
1. **row_column_count_mismatch_rate**: Target: < 2% of extracted rows; Alert if > 8%
2. **sparse_table_extraction_accuracy**: Target: > 90% (tracked separately from dense-table accuracy); Alert if < 75%
3. **value_shift_detection_rate**: Target: < 3% of tables show a detected column-shift pattern; Alert if > 10%
4. **empty_cell_explicit_modeling_rate**: Target: > 98% of detected empty cells represented explicitly (not silently dropped); Alert if < 90%

### Alerts
1. **Column Count Mismatch Spike** (P1): Condition - row/column count mismatch rate exceeds 8% for a document source. Action: Halt automated acceptance, route affected documents to human review, investigate structure-detection accuracy for sparse tables in that source.
2. **Sparse Table Accuracy Regression** (P2): Condition - sparse-table-specific accuracy drops below 75% even if aggregate accuracy looks stable. Action: Treat as a real regression requiring investigation, since aggregate metrics are known to mask this failure mode.
3. **Value Shift Pattern Detected** (P2): Condition - value-shift detection flags more than 10% of tables from a source. Action: Fix empty-cell handling in the extraction pipeline for that document type rather than relying on downstream correction.

## References

- [VLMs for Spreadsheet Understanding](https://arxiv.org/html/2405.16234v1) - Cell omission and spatial perception
- [Table Extraction Using LLMs](https://nanonets.com/blog/table-extraction-using-llms-unlocking-structured-data-from-documents/) - Sparse table challenges
- [IDP Challenges 2026](https://idp-software.com/guides/idp-challenges-2026/) - Table extraction as unsolved problem
