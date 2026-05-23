# Table Boundaries

## Issue: Table Boundaries Not Detected

**Frequency**: Very Common

**Symptoms**
- Table data extracted as continuous text
- Column values misaligned (value from column A assigned to column B)
- Header row merged with first data row

**Root Cause**
Tables without visible borders or with inconsistent formatting fail boundary detection. The model extracts text in reading order rather than tabular structure.

**Example**
```
Input Table:
| Item       | Qty | Price  |
|------------|-----|--------|
| Widget A   | 5   | $10.00 |
| Widget B   | 3   | $15.00 |

Extracted: "Item Qty Price Widget A 5 $10.00 Widget B 3 $15.00"

Result: Cannot parse individual line items
```

**Mitigation Strategies**
1. **Explicit table detection**: Run table detection model before text extraction
2. **Whitespace analysis**: Detect column alignment via spacing patterns
3. **Line-based parsing**: Process horizontal slices as rows
4. **Template-based extraction**: For known formats, define table regions explicitly
5. **Multi-column heuristics**: Detect when single "line" contains multiple data fields

**Detection**
- Field count per document differs from expected
- Values appear truncated or concatenated
- Downstream parsing exceptions
