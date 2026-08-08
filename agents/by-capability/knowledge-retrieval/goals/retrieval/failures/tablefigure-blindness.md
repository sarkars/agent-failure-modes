# Table/Figure Blindness

## Issue: Agent misses data embedded in tables, charts, images, or PDFs.

**Frequency**: Occasional

**Symptoms**
- Relevant value only present visually; answer omits it.
- Answer omits a specific numeric value that exists only inside a table cell or chart, even though the surrounding prose is retrieved and used.
- Query referencing a named table or figure ("Table 3", "Figure 2") returns the paragraph mentioning the reference but not the table/figure's actual content.
- Retrieved chunk contains a table rendered as OCR'd row-jumbled text, and the synthesized answer misattributes a value to the wrong row or column.

**Root Cause**
The ingestion pipeline treats documents as flat text, running OCR or extraction that captures prose but does not detect or structurally parse tabular layouts, so cell values are either lost or flattened into unusable strings before they ever reach the index. Because no separate table index or structured representation exists, and no vision/multimodal step is applied to charts and figures, numeric values that are only ever encoded visually simply never become retrievable text. The gap is made worse by the absence of any mechanism to resolve a text reference like "see Table 2" to the table's actual content, so even when the surrounding prose is retrieved correctly, the data it points to remains invisible to the system.

**Example**
```
Query: "What's the warranty period for the industrial model?"
The spec sheet PDF states the answer only in Table 2 (a grid mapping model names to
warranty months), while the surrounding prose just says "see Table 2 for warranty
details by model." The ingestion pipeline extracts document text via plain OCR that
does not parse table structure, so the table's actual cell values are never indexed.
The agent retrieves the paragraph, sees "see Table 2," but has no indexed table content
to draw from, and answers "The warranty period is not specified" despite the number
being present in the source document.
```

**Contributing Factors**
- Ingestion pipeline extracts document text via plain OCR/text extraction that does not detect or structurally parse tables, so table cell values are lost or flattened into unusable text.
- No separate table-index or structured JSON representation of table data alongside the text index.
- No table-reference resolution linking a text mention ("see Table 2") to the corresponding table's actual content.
- Vision/multimodal extraction not applied to figures and charts, so numeric values encoded only visually are never captured as retrievable text.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Table-only value missing | Query whose answer exists only as a cell value in a table, not restated in surrounding prose | Answer includes the correct table cell value | Answer states the information isn't available, or omits the value |
| Table reference not resolved | Document text says "see Table 3" and Table 3 contains the needed data | Retrieval resolves the reference and surfaces Table 3's content alongside the paragraph | Only the referencing paragraph is retrieved; table content is absent |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| table_content_retrieval_recall_percent | > 85% | Run eval set of queries whose ground-truth answer lives in a table cell, measure % where the table content is present in retrieved results |

---

## Mitigation Strategies

### Prevention
1. **Multimodal Document Extraction**: For PDFs/images with tables/figures, extract both text AND images. Use table_ocr + vision_model to understand tables structurally (extract rows/columns/headers). Index table_contents separately from text_contents.
2. **Table-Specific Index**: Create separate index for table data. When query contains table_keywords ('table', 'chart', 'figure', 'data_comparison'), also search table_index in addition to text_index. Re-rank merged results.
3. **PDF/Table Eval Suite**: Build eval set specifically testing retrieval over documents with tables/figures. Measure recall/precision on table_content queries. Target: > 85% recall on table queries.

### Detection & Response
1. **Table Reference Detection**: When document references a table ('see Table 3', 'as shown in Figure 2'), extract the table and link table_content to reference. Index linked table for query matching.
2. **Visual Element Presence Flagging**: Detect presence of tables/figures in documents via image analysis. Tag documents with 'has_tables', 'has_figures' metadata. Use tags for query routing.
3. **Query-Table Relevance Verification**: For queries that seem table-related (numerical comparisons, data lookups, "compare X and Y"), verify retrieved results include table_content. Alert if table-relevant query returns only text results.

### Architecture Patterns
1. **Multimodal Indexing Pipeline**: For each document, extract & index: text (OCR), tables (table-detection + table-OCR → structured JSON), figures (vision_model classification). Create separate indexed representations for each modality.
2. **Table Extraction Service**: Deploy specialized service that: detects tables in images/PDFs, extracts table structure (rows/columns/headers), applies table-OCR. Output: structured JSON table representation that's queryable.
3. **Hybrid Search with Table Index**: When querying, search both text_index and table_index in parallel. Re-rank results by relevance. Include table_context in results with clear 'TABLE' markers.

### Metrics
1. **table_content_retrieval_recall_percent**: Target: > 85%; Alert threshold: < 75%
2. **figure_reference_resolution_rate_percent**: Target: > 90%; Alert threshold: < 80%
3. **table_detection_precision_percent**: Target: > 95%; Alert threshold: < 90%
4. **multimodal_indexing_coverage_percent**: Target: 100%; All documents processed for multimodal content
5. **user_satisfaction_on_table_queries_percent**: Target: > 80%; Alert threshold: < 70%

### Alerts
1. **Table Content Not Retrieved** (P2 - Warning): Condition - table-relevant query returns no table results. Action: Audit table extraction, update table_index, rerun multimodal indexing.
2. **Figure Detection Failure** (P2 - Warning): Condition - document has visible figures but not tagged 'has_figures'. Action: Review visual detection model, retag documents.
3. **Table Extraction Error** (P1 - Critical): Condition - table_ocr accuracy < 80% for document. Action: Mark table as low-confidence, provide disclaimer, request manual table entry.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| table_content_retrieval_recall_percent | < 75% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Table Content Retrieval Failure | table_content_retrieval_recall_percent on eval sample drops below 75% | Medium |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
