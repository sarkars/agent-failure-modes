# Layout Signal Loss

## Issue: Layout Signal Loss

**Frequency**: Common

**Symptoms**
- Document structure lost in preprocessing
- Spatial relationships between fields destroyed
- Tables flatten to unstructured text

**Root Cause**
Some preprocessing pipelines strip layout information in the name of "cleaning" documents, losing critical structural context.

**Example**
```
Original PDF: Table with clear columns and rows
After preprocessing: All text extracted left-to-right, top-to-bottom
Lost: Column boundaries, row groupings, header associations

Result: "Product Qty Price" becomes "Product Qty Price Widget 5 $10 Gadget 3 $15"
```

**Key Statistic**
Legacy OCR pipelines often plateau around 60-70% automation because they break under layout variance.

**Mitigation Strategies**
1. **Layout-preserving OCR**: Use tools that output coordinates and structure
2. **Multi-layer output**: Keep both text and spatial information
3. **Structural validation**: Verify table structures match expected schemas
4. **Document type-specific handling**: Different pipelines for different layouts
