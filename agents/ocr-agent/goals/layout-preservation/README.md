# Goal: Layout Preservation

Preserving document structure is critical for extracting meaningful data. A document isn't just text - it's tables, columns, headers, and spatial relationships.

## Business Context

- Invoice line items must map to correct columns
- Multi-column documents need correct reading order
- Headers and footers should be separated from body content

## Failure Patterns

| Failure Pattern | Frequency | Impact |
|-----------------|-----------|--------|
| [Table Boundaries](failures/table-boundaries.md) | Very Common | High |
| [Merged Cells](failures/merged-cells.md) | Common | High |
| [Column Ordering](failures/column-ordering.md) | Common | High |
| [Bidirectional Text](failures/bidirectional-text.md) | Occasional | Medium |
| [Headers and Footers](failures/headers-footers.md) | Common | Medium |
| [Footnotes](failures/footnotes.md) | Occasional | Low |

## Key Metrics

- Table detection precision/recall
- Column assignment accuracy
- Reading order correctness
