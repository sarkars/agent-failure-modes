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

**Mitigation Strategies**
1. **Two-stage parsing**: Detect table structure first, then extract content
2. **Column alignment heuristics**: Use header positions to anchor column assignment
3. **Empty cell handling**: Explicitly model missing values rather than skipping
4. **Post-validation**: Verify column counts match expected schema
