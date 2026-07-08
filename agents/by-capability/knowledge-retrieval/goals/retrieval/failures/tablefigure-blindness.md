# Table/Figure Blindness

## Issue: Agent misses data embedded in tables, charts, images, or PDFs.

**Frequency**: Occasional

**Symptoms**
- Relevant value only present visually; answer omits it.
- [Add more specific symptoms]

**Root Cause**
Agent misses data embedded in tables, charts, images, or PDFs.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

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
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Medium |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
