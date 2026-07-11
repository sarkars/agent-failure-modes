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

## Mitigation Strategies

### Prevention
1. **Layout-preserving OCR as the default, not an opt-in**: Standardize on OCR/parsing tools that output bounding-box coordinates and structural metadata (row/column groupings, header associations) as the primary output format, rather than flattened reading-order text, since once layout information is discarded in preprocessing it cannot be recovered downstream no matter how good the extraction model is. Trade-off: layout-preserving output is more complex to store, transmit, and consume than plain text, requiring downstream systems to handle structured input.
2. **Multi-layer output retaining both text and spatial data**: Store both the flattened text (for search/simple use cases) and the full spatial/structural layer (bounding boxes, table grid coordinates) as co-equal outputs of preprocessing, so any downstream consumer needing structure has it available rather than needing to re-run OCR from the source. Trade-off: increases storage and pipeline complexity versus a single text output.
3. **Document-type-specific preprocessing pipelines**: Route document types with heavy structural content (tables, forms) through a layout-aware pipeline distinct from document types that are primarily narrative text, rather than a single generic "clean the text" preprocessing step applied uniformly, since a one-size-fits-all preprocessing step optimized for narrative text will systematically destroy tabular structure. Trade-off: requires document-type classification as a prerequisite step, and additional pipeline paths to maintain.

### Detection & Response
1. **Structural validation against expected schema**: After preprocessing, validate that documents expected to contain tables/structured layout actually retain identifiable row/column structure in the output, flagging cases where structure appears to have collapsed to flat text as a preprocessing failure requiring reprocessing with a layout-preserving path.
2. **Automation-rate plateau monitoring as a leading indicator**: Track automation/straight-through-processing rate over time; a plateau around 60-70% despite continued model improvements is a documented signature of layout-signal-loss in preprocessing, not a model capability ceiling, and should redirect investigation toward the preprocessing stage.
3. **Reading-order artifact detection**: Scan extracted text for signatures of collapsed table structure (e.g., a sequence of alternating label/value tokens with no delimiter, like "Product Qty Price Widget 5 $10") to flag documents where layout was likely destroyed during preprocessing.

### Architecture Patterns
1. **Structure-preserving preprocessing as a pipeline-wide standard**: Architect the entire document-processing pipeline around a structured intermediate representation (text + coordinates + structural metadata) as the canonical preprocessing output, with any flattened-text view generated as a derived, lossy projection for consumers that don't need structure — never the other way around.
2. **Type-routed preprocessing dispatch**: Classify document type before preprocessing and dispatch to a layout-aware pipeline for structurally-rich documents versus a simpler pipeline for narrative documents, rather than routing all documents through the same preprocessing regardless of expected content structure.
3. **Structural-schema validation gate**: Insert a mandatory validation gate after preprocessing that checks structural completeness for document types expected to contain tables/forms, rejecting/reprocessing outputs that fail structural checks before they proceed to extraction.

### Metrics
1. **structural_completeness_rate**: Target: > 95% of table/form documents retain identifiable structure post-preprocessing; Alert if < 80%
2. **automation_rate_plateau_signal**: Target: continued improvement or stability above 85%; Alert if automation rate plateaus in the 60-70% band for more than one quarter without corresponding root-cause investigation
3. **reading_order_collapse_detection_rate**: Target: < 3% of structured documents show collapse signatures; Alert if > 10%
4. **downstream_table_extraction_accuracy_vs_narrative_accuracy**: Target: < 15 percentage point gap; Alert if gap > 30 points (signals layout loss specifically affecting structured content)

### Alerts
1. **Structural Completeness Drop** (P1): Condition - structural completeness rate for table/form documents falls below 80%. Action: Halt processing through the affected preprocessing path, switch to a layout-preserving alternative, reprocess affected documents.
2. **Automation Plateau Detected** (P2): Condition - automation rate has plateaued in the 60-70% range for a full quarter. Action: Investigate preprocessing layout handling as the primary hypothesis before pursuing model upgrades.
3. **Reading-Order Collapse Spike** (P2): Condition - collapse-signature detection rate exceeds 10% for a document type. Action: Switch that document type to a layout-preserving preprocessing pipeline immediately.

## References

- [OCR vs IDP](https://forage.ai/blog/ocr-vs-idp/) - Layout preservation importance
- [Why OCR Is the Weakest Part of Document AI](https://medium.com/@manalisomani099/why-ocr-is-the-weakest-part-of-most-document-ai-systems-c9188381d1b9) - Structure loss
- [IDP Challenges 2026](https://idp-software.com/guides/idp-challenges-2026/) - Layout variance challenges
