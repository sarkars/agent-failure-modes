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

**Mitigation Strategies**
1. **Hierarchical table models**: Use models that output tree structures, not just grids
2. **Indentation detection**: Use leading whitespace/bullets to infer hierarchy
3. **Post-processing rules**: Apply domain-specific rules to reconstruct hierarchy
4. **Row grouping heuristics**: Empty cells often indicate continuation of previous row's value

## References
- [Table Extraction Using LLMs](https://nanonets.com/blog/table-extraction-using-llms-unlocking-structured-data-from-documents/) - Merged cell handling
- [VLMs for Spreadsheet Understanding](https://arxiv.org/html/2405.16234v1) - Complex table structures
