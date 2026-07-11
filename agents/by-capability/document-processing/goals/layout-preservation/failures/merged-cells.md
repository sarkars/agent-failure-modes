# Merged Cells

## Issue: Merged and Split Cells Mishandled

**Frequency**: Common

**Symptoms**
- Multi-row cells extracted multiple times
- Spanning headers not associated with correct columns
- Cell content assigned to wrong row

**Root Cause**
Complex table structures with merged cells, spanning headers, or nested tables break the simple grid assumption.

**Example**
```
Input:
| Region    | Q1    | Q2    |
| North     |       |       |
|   - East  | $100  | $150  |
|   - West  | $200  | $175  |

Extracted rows:
Row 1: ["Region", "Q1", "Q2"]
Row 2: ["North", "", ""]
Row 3: ["- East", "$100", "$150"]
Row 4: ["- West", "$200", "$175"]

Expected: East and West should be children of North
Actual: Flat list with hierarchy lost
```

## Mitigation Strategies

### Prevention
1. **Tree-structured table models instead of flat-grid output**: Use extraction models/schemas that natively output a hierarchical tree (parent rows with child rows nested beneath, spanning cells represented as covering multiple child rows/columns) rather than forcing output into a flat row-by-row grid, since flattening is exactly where the parent-child relationship gets destroyed. Trade-off: requires downstream consumers to handle tree-structured data rather than simple flat rows, adding integration complexity.
2. **Indentation/bullet-marker hierarchy detection**: Detect visual hierarchy cues (leading whitespace, indentation level, bullet/dash markers like "- East") as an explicit signal for parent-child row relationships, and use detected indentation level to reconstruct nesting rather than treating all rows as siblings. Trade-off: relies on the source document using consistent visual hierarchy cues; documents without such cues need a different detection strategy (e.g., merged-cell span detection instead).
3. **Merged-cell span detection as a structural pre-pass**: Detect actual merged-cell spans (a cell visually spanning multiple rows, like "North" spanning the East/West rows) as part of table-structure detection before content extraction, and propagate the span information explicitly (e.g., "North" tagged as parent of both East and West) rather than letting extraction independently guess at each row's relationship to its neighbors. Trade-off: requires a structure-detection model capable of recognizing cell spans, which is itself an unsolved-in-general vision problem for tables without clear borders.

### Detection & Response
1. **Row-grouping consistency validation**: After extraction, validate that rows following a pattern suggestive of grouping (e.g., an empty-valued parent row followed by rows with a common indentation/marker) are actually tagged with the correct parent-child relationship, and flag cases where the pattern was detected but not correctly resolved into hierarchy.
2. **Empty-cell-as-continuation heuristic validation**: When empty cells in a row are interpreted as "continuation of the parent's value" (row-grouping heuristic), verify this interpretation against the surrounding structural context (indentation, merged-cell detection) rather than applying it uniformly, and flag ambiguous cases for review rather than silently guessing.
3. **Downstream aggregation-mismatch detection**: Where hierarchy has business meaning (e.g., "North" total should equal East + West), validate that aggregation relationships hold post-extraction; a mismatch signals the hierarchy was likely flattened or misassigned during extraction.

### Architecture Patterns
1. **Structure-detection-then-content-extraction pipeline**: Architect table processing as two stages — a structure detector identifying merged-cell spans and hierarchy markers, and a content extractor populating the tree established by that structure — so hierarchy reconstruction doesn't depend on the content-extraction step inferring it implicitly from a flat token stream.
2. **Tree-native storage with flat-view projection**: Store extracted tables in a hierarchical/tree representation internally, generating any flat-row view as a derived, clearly-labeled projection for consumers that need it, so the parent-child relationship is never the thing that's discarded by default.
3. **Domain-specific post-processing rule layer**: For document types with well-known hierarchical conventions (regional sales rollups, chart-of-accounts hierarchies), maintain a post-processing rule layer that reconstructs expected hierarchy patterns using domain knowledge as a supplement to general structure detection.

### Metrics
1. **hierarchy_reconstruction_accuracy**: Target: > 92% of parent-child relationships correctly reconstructed (measured via audit); Alert if < 75%
2. **aggregation_mismatch_rate**: Target: < 3% of hierarchical tables with checkable rollups; Alert if > 10%
3. **row_grouping_ambiguity_flag_rate**: Target: track as baseline; Alert if it changes > 2x (signals a new table convention not yet handled)
4. **flat_projection_information_loss_rate**: Target: 0% of hierarchy lost before reaching tree-native storage; Alert on any occurrence

### Alerts
1. **Hierarchy Reconstruction Accuracy Drop** (P2): Condition - hierarchy reconstruction accuracy falls below 75% for a document source. Action: Sample affected tables to determine whether structure detection or indentation-cue detection needs retuning for that source's conventions.
2. **Aggregation Mismatch Spike** (P1): Condition - rollup/aggregation mismatch rate exceeds 10% for hierarchical tables. Action: Route affected documents to human review; investigate whether hierarchy is being flattened or misassigned during extraction.
3. **Row Grouping Ambiguity Surge** (P3): Condition - ambiguity flag rate for row grouping doubles from baseline. Action: Review recent documents for a new table layout convention (e.g., different indentation style) requiring updated detection rules.

## References
- [Table Extraction Using LLMs](https://nanonets.com/blog/table-extraction-using-llms-unlocking-structured-data-from-documents/) - Merged cell handling
- [VLMs for Spreadsheet Understanding](https://arxiv.org/html/2405.16234v1) - Complex table structures
