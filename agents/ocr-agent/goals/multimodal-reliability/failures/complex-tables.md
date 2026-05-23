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

**Mitigation Strategies**
1. **Hierarchical table models**: Use models outputting tree structures
2. **Prompt chaining**: Decompose extraction into sequential tasks
3. **Specialized benchmarks**: Train on complex table datasets (RD-TableBench)
4. **Table Transformer**: Run table detection before VLM processing
