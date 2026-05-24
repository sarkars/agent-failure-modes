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

**Mitigation Strategies**
1. **Table detection first**: Use specialized table detector before VLM extraction
2. **Header alignment verification**: Cross-check extracted values match column semantics
3. **Semantic type checking**: Quantities should be integers, prices should have currency

## References

- [Hallucination of Multimodal LLMs Survey](https://arxiv.org/html/2404.18930v2) - Relational hallucination analysis
- [VLMs for Spreadsheet Understanding](https://arxiv.org/html/2405.16234v1) - Spatial perception limitations
- [Table Extraction Using LLMs](https://nanonets.com/blog/table-extraction-using-llms-unlocking-structured-data-from-documents/) - Column alignment challenges
