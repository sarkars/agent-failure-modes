# Complex Table Structures

## Issue: Merged Cell and Nested Header Failures

**Frequency**: Common

**Symptoms**
- Multi-row headers collapsed to single row
- Spanning cells duplicated or lost
- Hierarchical structure flattened

**Root Cause**
Complex table structures with merged cells, nested structures, or multi-row column headers disrupt standard parsing techniques.

**Example**
```
Input:
|          | 2024 Revenue    |
|          | Q1    | Q2      |
| North    | $100  | $150    |
| South    | $200  | $175    |

Extracted:
Headers: ["", "2024 Revenue", "Q1", "Q2"]  # Header hierarchy lost
Row 1: ["North", "$100", "$150"]           # Q1/Q2 attribution unclear

Result: Cannot programmatically determine which values belong to which quarter
```

## Mitigation Strategies

### Prevention
1. **Dedicated table-structure detection before VLM extraction**: Run a specialized table-structure model (e.g., Table Transformer) to first detect row/column spans and header hierarchy as a structural tree, then hand that structure to the VLM for content extraction rather than asking the VLM to infer structure and content simultaneously. Trade-off: adds a model call and dependency on the table-detector's own accuracy for complex/atypical table layouts.
2. **Hierarchical output schema enforcement**: Require extraction output to conform to a tree-structured schema that explicitly represents header nesting (e.g., `{"2024 Revenue": {"Q1": ..., "Q2": ...}}`) rather than a flat list of headers, forcing the model to commit to a parent-child relationship instead of flattening it away. Trade-off: flat-table downstream consumers need an adapter layer to work with hierarchical output.
3. **Decomposed prompt chaining for header resolution**: Break extraction into sequential steps — first identify header row spans, then identify header hierarchy relationships, then assign data cells to the fully-resolved header path — rather than a single end-to-end extraction prompt, since each sub-task is more reliably solved in isolation. Trade-off: increases latency and cost versus single-pass extraction.

### Detection & Response
1. **Header-hierarchy consistency validation**: After extraction, validate that every data cell has a complete header path (e.g., both "2024 Revenue" and "Q1" resolved, not just one) and flag any cell with an incomplete or ambiguous header attribution for review.
2. **Column-count/row-count sanity checks against visual table span**: Compare the number of extracted columns/rows against an independent structural detection pass; a mismatch signals merged-cell or nested-header collapse even before checking individual values.
3. **Benchmark-tracked accuracy on complex-table test sets**: Continuously evaluate against a held-out set of merged-cell/nested-header tables (e.g., RD-TableBench-style examples) as a leading indicator, since aggregate accuracy across mostly-simple tables can mask poor performance specifically on complex structures.

### Architecture Patterns
1. **Two-model pipeline: structure detector + content extractor**: Architect table processing as two independently-versioned stages — a structure/layout model producing the row-column-header tree, and a content extraction model populating leaf values — so structure errors and content errors can be diagnosed and fixed separately.
2. **Tree-native data model with flat-view adapter**: Store extracted tables internally in a hierarchical/tree representation that preserves nested headers and spans, with a separate flattening adapter for downstream systems that require flat rows — never let the flattening happen inside the extraction step itself, where it destroys information irreversibly.
3. **Confidence-gated escalation for detected nested structures**: When structure detection flags a table as having merged cells or multi-row headers (higher inherent difficulty), automatically lower the confidence threshold for automatic acceptance and increase the likelihood of human review for that specific table.

### Metrics
1. **header_hierarchy_completeness_rate**: Target: > 95% of cells have a fully-resolved header path; Alert if < 85%
2. **structural_column_row_count_mismatch_rate**: Target: < 3% of tables; Alert if > 10%
3. **complex_table_benchmark_accuracy**: Target: > 90% on merged-cell/nested-header test set; Alert if < 75%
4. **flattening_information_loss_rate**: Target: 0% of hierarchical structure lost before reaching the tree-native store; Alert on any occurrence

### Alerts
1. **Header Completeness Drop** (P2): Condition - header hierarchy completeness rate falls below 85% for a document source. Action: Sample affected tables to determine whether nested-header detection needs retuning for that source's table layout conventions.
2. **Complex Table Benchmark Regression** (P1): Condition - accuracy on the complex-table benchmark test set drops below 75%. Action: Block deployment of the change that caused the regression; investigate structure-detection or content-extraction stage separately.
3. **Structure Mismatch Spike** (P2): Condition - column/row count mismatch rate between structure detection and content extraction exceeds 10%. Action: Route affected tables to human review, investigate pipeline desync between the two stages.

## References

- [Table Extraction Using LLMs](https://nanonets.com/blog/table-extraction-using-llms-unlocking-structured-data-from-documents/) - Merged cells, complex layouts
- [IDP Challenges 2026](https://idp-software.com/guides/idp-challenges-2026/) - Nested header handling
- [VLMs for Spreadsheet Understanding](https://arxiv.org/html/2405.16234v1) - Hierarchical structure parsing
