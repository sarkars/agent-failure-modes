# What Are the Most Common Layout Preservation Problems in AI Agents?

**Layout preservation fails when an agent reads every character correctly but flattens the document's two-dimensional structure into the wrong one-dimensional text stream.** Table boundaries, spanning headers, footnotes, running headers, and mixed-direction scripts all carry positional or hierarchical meaning that a naive top-to-bottom, left-to-right reading pass destroys — a two-column newsletter interleaves into a nonsensical sentence, a footnote reference gets appended as trailing body text, and a table with borders and no whitespace runs into one unparseable string. Layout preservation failures are especially dangerous because the extracted characters are individually correct, so the error only shows up when something tries to parse structure out of the flattened text — a line-item total, a footnote citation, a column value — and finds it's in the wrong place or missing entirely.

## Key Takeaways

- 6 patterns cover layout preservation, grouped into three mechanisms: table-structure loss, reading-order/page-flow errors, and script-direction handling.
- Table-boundaries is rated Very Common — tables without visible borders or with inconsistent formatting get extracted in reading order rather than tabular structure, misaligning column values or merging the header row with the first data row.
- Reading-order failures (columns, footnotes, headers/footers) share the same root cause: content that exists outside the main linear text flow (a second column, a bottom-of-page note, a repeating running header) gets pulled into that flow at the wrong position instead of being classified as its own region first.
- Merged-cells failures are a hierarchy problem, not just a grid problem: flattening a table with spanning headers or nested rows (e.g., "North" spanning "East"/"West" sub-rows) discards a parent-child relationship that has business meaning, such as a rollup total.

## Scope

- **Table-structure loss** — [table-boundaries](failures/table-boundaries.md), [merged-cells](failures/merged-cells.md). Both break the simple-grid assumption: table-boundaries is about detecting where a table's rows/columns even are when there are no visible borders, and merged-cells is about preserving hierarchy (spanning headers, nested rows) once a table region is already detected.
- **Reading-order / page-flow errors** — [column-ordering](failures/column-ordering.md), [footnotes](failures/footnotes.md), [headers-footers](failures/headers-footers.md). All three involve content positioned outside the primary linear reading path (a second column, a bottom-of-page footnote, a repeating header/footer band) that a naive single-pass reading order pulls into the body text at the wrong point.
- **Script-direction handling** — [bidirectional-text](failures/bidirectional-text.md). Right-to-left and mixed-direction scripts require explicit BiDi-algorithm handling; ad hoc concatenation reverses or jumbles text rather than an ordering mistake within a single direction.

## When Layout Preservation Matters

- Source documents use multi-column layouts (newspapers, academic papers, brochures) or contain footnotes/margin notes carrying citations or qualifiers with legal or scientific significance
- Tables lack visible borders, use whitespace-only column alignment, or contain spanning headers and nested/hierarchical rows (regional sales rollups, chart-of-accounts structures)
- Documents mix scripts — Arabic or Hebrew body text with embedded English product codes or numeric IDs — where a single assumed reading direction will reverse or jumble the mixed segments

## Cross-Pattern Insight

Every layout-preservation pattern's mitigation follows the same two-stage shape: classify page regions or structural elements first (table grid, column boundary, footnote band, header/footer band, script segment), then extract or recombine content within that established structure as a separate step — never let a single extraction pass do both region-classification and content-reading at once. Table-boundaries and merged-cells both push toward detect-structure-then-extract-content pipelines; column-ordering, footnotes, and headers-footers all push toward segment-pages-into-regions-then-read-each-region; bidirectional-text pushes toward script-detection-then-BiDi-recombination. The unifying diagnostic is a coherence or consistency check run after extraction — semantic coherence checks catch scrambled column text, orphaned-marker detection catches lost footnote links, repetition validation catches header/footer leakage, and aggregation-mismatch checks catch flattened table hierarchy — because layout errors don't corrupt individual characters, only their structural relationships.

## Frequently Asked Questions

### How is layout preservation different from accurate text extraction?
Text extraction failures are character-level: the model misreads a `0` as an `O`. Layout preservation failures happen even when every character is read correctly — the structural relationship between correctly-read pieces of text (which column a sentence belongs to, which row a footnote references, which parent row a table cell nests under) is lost or scrambled. See [Accurate Text Extraction](../accurate-text-extraction/).

### What makes borderless tables fail more often than bordered ones?
Because table-boundaries detection has no visual grid line to anchor on and must infer structure from whitespace projection profiles or alignment patterns instead, and table-boundaries failure is rated Very Common precisely because so many real-world tables use whitespace-only alignment rather than drawn borders.

### What's the difference between table-boundaries and merged-cells?
Table-boundaries is about detecting that a table exists and where its grid lines are at all; merged-cells is a step further — once the grid is detected, spanning headers and nested rows (a cell that visually covers multiple rows) still need to be reconstructed as a hierarchy rather than flattened into a flat list of siblings.

### Can a semantic coherence check catch every reading-order failure?
No, but it catches a specific and common subset. The column-ordering pattern's mitigation runs a lightweight language-model coherence check on extracted paragraphs to catch text that jumps between unrelated topics mid-sentence — the signature of interleaved columns — but the coherence check is a detection method, not a fix; the underlying gutter/column-boundary detection still needs to be correct for the extraction to be right in the first place.

### Is bidirectional text handling only relevant for Arabic/Hebrew documents?
Primarily, but the failure also appears in mixed-script documents like an Arabic invoice with embedded English product codes or numeric IDs — the bidirectional-text pattern's mitigation specifically calls out that numeric/ID fields need a field-type-driven direction override, since they should read left-to-right even when embedded in right-to-left surrounding text.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Bidirectional Text](failures/bidirectional-text.md) | RTL/LTR script mixing reversed or jumbled without proper BiDi-algorithm handling |
| [Column Ordering](failures/column-ordering.md) | Multi-column pages read across columns instead of down each column, interleaving unrelated text |
| [Footnotes](failures/footnotes.md) | Footnote/margin content appended as inline body text, losing its reference link |
| [Headers Footers](failures/headers-footers.md) | Repeating headers/footers and page numbers bleed into body content mid-paragraph |
| [Merged Cells](failures/merged-cells.md) | Spanning headers and nested rows flattened into a sibling list, losing parent-child hierarchy |
| [Table Boundaries](failures/table-boundaries.md) | Borderless/inconsistent tables extracted as continuous text with misaligned columns |

**Total: 6 patterns**

## Related Goals

- [Accurate Text Extraction](../accurate-text-extraction/) — character-level misreads versus structural relationships lost here
- [Multimodal Reliability](../multimodal-reliability/) — complex-tables and table-cell-omission cover VLM-specific table failures (hallucinated/omitted cells) rather than reading-order/structure detection
- [Document Classification](../document-classification/) — page-grouping and embedded-documents run upstream, determining document boundaries before layout preservation even begins
