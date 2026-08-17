# Table Boundaries Not Detected, Rows Extracted as Plain Text: Causes and Fixes

## Issue: Agent Extracts Table Data as Continuous Text Instead of Rows and Columns

Commonly reported in table-extraction pipelines built with frameworks like LlamaIndex or LangChain document loaders, where borderless or inconsistently formatted tables fall back to reading-order extraction.

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

## Mitigation Strategies

How to fix it: run dedicated table-region detection before text extraction so column/row structure is known ahead of time, instead of inferring it from reading order.

### Prevention
1. **Dedicated table-region detection before text extraction**: Run a specialized table-detection model to identify table boundaries (region, rows, columns) as a distinct step before any text extraction runs, so text extraction operates on a known table structure rather than needing to infer tabular boundaries from reading order alone. Trade-off: table detectors trained on bordered/well-formatted tables can still miss borderless tables with inconsistent whitespace-only column alignment.
2. **Whitespace/alignment-pattern column detection**: For borderless tables, analyze consistent vertical whitespace gaps or text alignment patterns across multiple lines to infer column boundaries, rather than assuming the presence of visible grid lines is required to detect tabular structure. Trade-off: whitespace-based detection is fragile against proportional fonts or documents where column content varies enough in width to break consistent gap alignment.
3. **Template-based explicit region definition for known formats**: For recurring document formats/vendors, define the table region and column boundaries explicitly as part of that vendor's template configuration, bypassing general-purpose table detection entirely for known formats where a explicit, validated definition is more reliable. Trade-off: only helps for previously-onboarded formats; offers no benefit for novel/one-off documents, and requires maintenance if the vendor's format later changes (see [[template-drift]]).

### Detection & Response
1. **Field-count-per-document validation against expected schema**: Compare the number of fields/columns extracted per row against the expected schema for that document type, and flag documents where the count differs (a signature of table-boundary detection failure collapsing structure into continuous text).
2. **Concatenation/truncation pattern detection**: Scan extracted values for concatenation signatures (a single "value" containing what looks like multiple distinct fields run together, e.g., "Widget A 5 $10.00") and flag for reprocessing with explicit table detection rather than accepting the concatenated string as a single field value.
3. **Downstream parsing exception monitoring**: Treat downstream parsing exceptions (a system expecting a numeric quantity field receiving a concatenated string) as a primary detection signal for table-boundary failures, and correlate exception spikes back to specific document sources/formats to prioritize detection improvements.

### Architecture Patterns
1. **Detect-then-extract two-stage table pipeline**: Architect table processing so a structure-detection stage (identifying table region, row/column boundaries) always precedes content extraction, treating "where is the table and what's its grid" as a distinct, independently-validated problem from "what does each cell contain."
2. **Line-based row parsing with column-boundary anchoring**: Process detected table regions as horizontal slices (rows) and assign values to columns using anchored boundary positions (from whitespace analysis or detected borders) rather than relying purely on reading-order token sequence to imply structure.
3. **Format registry with template-first routing**: Maintain a registry of known document formats with pre-validated explicit table region definitions, routing recognized formats through the template path and falling back to general table detection only for unrecognized formats.

### Metrics
1. **field_count_mismatch_rate**: Target: < 3% of documents show field-count deviation from expected schema; Alert if > 10%
2. **concatenation_signature_detection_rate**: Target: < 2% of extracted rows; Alert if > 8%
3. **downstream_parsing_exception_rate**: Target: < 1% of processed documents; Alert if > 5%
4. **table_region_detection_confidence**: Target: > 90% of tables detected with high confidence; Alert if < 75% for a document source

### Alerts
1. **Field Count Mismatch Spike** (P1): Condition - field-count mismatch rate exceeds 10% for a document source. Action: Route affected documents to human review; investigate whether that source's tables are borderless/whitespace-only and need dedicated detection tuning.
2. **Concatenation Signature Surge** (P2): Condition - concatenation-signature detection rate exceeds 8%. Action: Add or strengthen table-region detection for the affected document type before continuing automated processing.
3. **Downstream Parsing Exception Spike** (P1): Condition - downstream parsing exception rate exceeds 5% correlated with a specific document source. Action: Halt automated ingestion from that source until table-boundary detection is fixed; reprocess affected documents once resolved.

## References
- [Table Extraction Using LLMs](https://nanonets.com/blog/table-extraction-using-llms-unlocking-structured-data-from-documents/) - Table detection challenges
- [IDP Challenges 2026](https://idp-software.com/guides/idp-challenges-2026/) - Table extraction as hardest problem
- [VLMs for Spreadsheet Understanding](https://arxiv.org/html/2405.16234v1) - Table structure recognition
