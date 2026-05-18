# Layout Understanding

Preserving document structure is critical for extracting meaningful data. A document isn't just text - it's tables, columns, headers, and spatial relationships.

---

## Table Detection

### Issue: Table Boundaries Not Detected

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

---

### Issue: Merged and Split Cells Mishandled

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

---

## Column Ordering

### Issue: Multi-Column Page Reading Order Errors

**Frequency**: Common

**Symptoms**
- Text from different columns interleaved
- Sentences start in one column, continue with text from another
- Paragraphs appear out of order

**Root Cause**
Multi-column layouts (newspapers, academic papers, brochures) require detecting column boundaries and reading each column top-to-bottom before moving to the next.

**Example**
```
Input: Two-column newsletter

Column 1:              Column 2:
"The company           "Sales increased
announced today        by 20% over
that production        last quarter
will increase..."      results..."

Extracted: "The company Sales increased announced today by 20% over..."

Result: Nonsensical text
```

**Mitigation Strategies**
1. **Column detection**: Identify vertical gutters between columns
2. **Reading order models**: Use models trained on multi-column layouts
3. **Semantic coherence checks**: Detect when adjacent text doesn't form coherent sentences
4. **Document type classification**: Apply column-aware processing for detected types (newspaper, paper, etc.)

---

### Issue: Right-to-Left and Mixed Direction Text

**Frequency**: Occasional (common in multilingual contexts)

**Symptoms**
- Arabic/Hebrew text reversed
- Mixed LTR/RTL text garbled
- Numbers in RTL context appear in wrong position

**Root Cause**
Bidirectional text requires understanding both the script direction and the embedding rules for mixed-direction content.

**Example**
```
Input: Arabic invoice with English product codes
Expected: "فاتورة #INV-001"
Actual: "100-VNI# ةروتاف" (reversed and jumbled)
```

**Mitigation Strategies**
1. **Script detection**: Identify script before applying reading direction
2. **Bidirectional algorithm**: Implement Unicode BiDi algorithm for mixed text
3. **Segment-level processing**: Extract RTL and LTR segments separately, then combine
4. **Field-level direction**: Use field type to determine expected direction

---

## Header and Footer Handling

### Issue: Headers/Footers Duplicated or Misplaced

**Frequency**: Common

**Symptoms**
- Same header text appears multiple times in extraction
- Page numbers interleaved with content
- Running headers merged with body text

**Root Cause**
Multi-page documents have repeating headers and footers. Without page boundary detection, these repeat in output and disrupt content flow.

**Example**
```
Input: 5-page report

Extracted: "...end of section 1. Company Name | Confidential | Page 2 Section 2 begins..."

Result: Header content pollutes body text
```

**Mitigation Strategies**
1. **Page region classification**: Identify header/footer zones by position
2. **Repetition detection**: Remove text that repeats at consistent positions across pages
3. **Page number detection**: Identify and exclude page numbering patterns
4. **First-page exception**: Headers on first page often differ - handle separately

---

### Issue: Footnotes and Marginal Notes Misplaced

**Frequency**: Occasional

**Symptoms**
- Footnotes appear in middle of paragraphs
- Marginal annotations merged with body text
- Reference numbers disconnected from footnote content

**Root Cause**
Footnotes and margin notes exist outside the main content flow. Reading-order extraction places them incorrectly.

**Example**
```
Input:
"The study found significant results¹ in all tested conditions."

Footnote at bottom:
"¹ p < 0.05"

Extracted: "The study found significant results in all tested conditions. ¹ p < 0.05"

Expected: Footnote linked to reference
Actual: Footnote appended as regular text
```

**Mitigation Strategies**
1. **Footnote region detection**: Identify footnote sections by position and formatting
2. **Reference linking**: Match superscript numbers to footnote numbers
3. **Structured output**: Output footnotes as separate linked elements
4. **Exclusion option**: For some use cases, exclude footnotes entirely
