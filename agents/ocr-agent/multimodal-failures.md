# Multimodal and VLM Failures

Vision-Language Models (VLMs) and multimodal LLMs bring new capabilities to document processing, but also introduce failure modes that differ fundamentally from traditional OCR.

---

## Silent Failures

### Issue: Plausible but Wrong Outputs

**Frequency**: Very Common

**Symptoms**
- Extracted values look reasonable but are incorrect
- No errors flagged in pipeline
- Downstream systems process bad data without alerting
- Errors discovered only during audits or customer complaints

**Root Cause**
Classical OCR fails loudly - when Tesseract cannot read a character, it produces garbled output or blanks. The failure is visible. MLLMs fail silently - when a multimodal LLM cannot confidently read a digit, it produces the most statistically plausible digit instead of indicating uncertainty.

**Example**
```
Input: Scanned invoice with slightly damaged "$10,000"
Expected: $10,000
Actual: $3,000 (model filled in plausible value)

Result: Payment processed for wrong amount, no error flagged
```

**Key Statistic**
Unlike OCR errors which are often obvious and consistent, LLM errors are plausible and hidden, making them far harder to detect at scale in high-stakes industries.

**Mitigation Strategies**
1. **Cross-field validation**: Verify totals against line item sums
2. **Confidence thresholds**: Force explicit uncertainty scores, flag low confidence
3. **Dual extraction**: Run multiple models, compare outputs
4. **Business logic checks**: Flag values outside expected ranges
5. **Human-in-the-loop**: Route high-value documents to review

**Detection**
- Reconciliation failures in accounting systems
- Customer disputes on invoiced amounts
- Audit findings revealing systematic errors
- A/B testing against human extraction

---

### Issue: Fabricated Content Not Grounded in Input

**Frequency**: Common

**Symptoms**
- Extracted fields contain text not present in document
- Model "completes" partial information with invented data
- Addresses, names, or codes appear that don't exist in source

**Root Cause**
When visual input is ambiguous or incomplete, VLMs draw on training data patterns to generate plausible completions rather than admitting uncertainty.

**Example**
```
Input: Partially obscured address "123 Main St, San ___"
Expected: Extract only visible text or flag incomplete
Actual: "123 Main St, San Francisco, CA 94102" (ZIP fabricated)

Result: Package shipped to wrong address
```

**Mitigation Strategies**
1. **Grounding checks**: Verify every extracted token appears in source
2. **Character-level alignment**: Map outputs back to image regions
3. **Refusal training**: Fine-tune model to say "unclear" rather than guess
4. **OCR fallback**: Use traditional OCR as cross-check

---

## Hallucination Types

### Issue: Object Hallucination

**Frequency**: Occasional

**Symptoms**
- Model describes elements not present in document
- Phantom tables, signatures, or stamps extracted
- Non-existent fields populated with values

**Root Cause**
The model's language prior about "what invoices usually contain" overrides what this specific document actually contains.

**Example**
```
Input: Simple invoice without purchase order reference
Model output: "PO Number: PO-2024-0892"

Result: Fake PO number causes ERP lookup failure or worse, matches wrong PO
```

**Mitigation Strategies**
1. **Schema constraints**: Only extract fields visually confirmed
2. **Bounding box validation**: Require spatial coordinates for each extraction
3. **Negative sampling**: Train on documents missing common fields

---

### Issue: Attribute Hallucination

**Frequency**: Common

**Symptoms**
- Correct field identified but wrong value assigned
- Colors, dates, or quantities slightly off
- Model "corrects" values to common patterns

**Root Cause**
Model identifies the right object but assigns properties based on training distribution rather than image content.

**Example**
```
Input: Invoice dated "2024-02-29" (leap year)
Actual: "2024-02-28" (model "corrects" to common date)

Result: Payment terms calculated from wrong date
```

**Mitigation Strategies**
1. **Domain validation**: Verify dates are valid, amounts are plausible
2. **Unusual value alerting**: Flag extractions that differ from OCR baseline
3. **Raw vs. parsed**: Keep original extraction separate from normalized values

---

### Issue: Relational Hallucination

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

---

## Visual Degradation Sensitivity

### Issue: Performance Collapse Under Visual Noise

**Frequency**: Common

**Symptoms**
- Accuracy drops dramatically on low-quality scans
- Model confident but wrong on degraded inputs
- Blurred, occluded, or low-contrast regions cause errors

**Root Cause**
VLMs trained primarily on clean images don't recognize when visual quality is too poor for reliable extraction. They produce outputs with high confidence even when input is ambiguous.

**Example**
```
Input: Faxed document with coffee stain over total
Expected: Flag as unreadable or low confidence
Actual: Extracts plausible total from surrounding context

Result: Wrong amount processed with high confidence
```

**Key Finding**
Under visual degradation (blur, occlusion, low contrast), the current response paradigm often fails to adequately perceive visual degradation and ambiguity, leading to overreliance on linguistic priors. This difficulty in recognizing uncertainty frequently results in hallucinations.

**Mitigation Strategies**
1. **Quality scoring**: Pre-filter images below quality threshold
2. **Uncertainty calibration**: Train model to output calibrated confidence scores
3. **Refusal training**: Teach model to refuse extraction on degraded regions
4. **Ensemble methods**: Multiple models vote, disagreement flags uncertainty
5. **Human routing**: Automatically escalate degraded documents

---

## Table Extraction Failures

### Issue: Cell Omission and Merging

**Frequency**: Very Common

**Symptoms**
- Table rows or columns missing from output
- Multiple cells treated as single cell
- Sparse tables with empty cells cause column misalignment

**Root Cause**
VLMs sometimes struggle to split multiple cells and mistakenly treat them as a single cell. Spatial perception limitations make grid inference unreliable.

**Example**
```
Input: 
| Product | Q1   | Q2   | Q3   | Q4   |
|---------|------|------|------|------|
| Alpha   | 100  |      | 150  |      |
| Beta    | 200  | 250  |      | 300  |

Extracted (misaligned):
Product: Alpha, Q1: 100, Q2: 150, Q3: [missing], Q4: [missing]
Product: Beta, Q1: 200, Q2: 250, Q3: 300, Q4: [missing]

Result: Q2 and Q4 data lost or misattributed
```

**Key Statistic**
Table extraction works effectively in most cases, but sparse tables with multiple empty cells present a unique challenge. The model sometimes mismatches columns, leading to errors in the extracted tabular data.

**Mitigation Strategies**
1. **Two-stage parsing**: Detect table structure first, then extract content
2. **Column alignment heuristics**: Use header positions to anchor column assignment
3. **Empty cell handling**: Explicitly model missing values rather than skipping
4. **Post-validation**: Verify column counts match expected schema

---

### Issue: Merged Cell and Nested Header Failures

**Frequency**: Common

**Symptoms**
- Multi-row headers collapsed to single row
- Spanning cells duplicated or lost
- Hierarchical structure flattened

**Root Cause**
Complex table structures with merged cells, nested structures, or multi-row column headers disrupt standard parsing techniques.

**Example**
```
Input:
|          | 2024 Revenue    |
|          | Q1    | Q2      |
| North    | $100  | $150    |
| South    | $200  | $175    |

Extracted:
Headers: ["", "2024 Revenue", "Q1", "Q2"]  # Header hierarchy lost
Row 1: ["North", "$100", "$150"]           # Q1/Q2 attribution unclear

Result: Cannot programmatically determine which values belong to which quarter
```

**Mitigation Strategies**
1. **Hierarchical table models**: Use models outputting tree structures
2. **Prompt chaining**: Decompose extraction into sequential tasks
3. **Specialized benchmarks**: Train on complex table datasets (RD-TableBench)
4. **Table Transformer**: Run table detection before VLM processing

---

## Enterprise Document Challenges

### Issue: Input Quality Gap

**Frequency**: Very Common

**Symptoms**
- Benchmark performance far exceeds production performance
- Models perform well in demos but fail on real documents
- Accuracy varies wildly across document sources

**Root Cause**
Enterprise documents include scanned PDFs with inconsistent OCR quality, complex regulatory submissions with nested table structures, CAD drawings and mixed-format engineering packages, handwritten forms, and legacy system exports never designed for machine consumption.

**Key Finding**
The gap between benchmark performance and production performance in enterprise document environments is not a model gap - it is an input quality gap.

**Mitigation Strategies**
1. **Document preprocessing pipeline**:
   - Normalize across file types
   - Multi-layer OCR preserving layout context
   - Document type classification
   - Quality validation before model inference
2. **Source-specific handling**: Different pipelines for different input sources
3. **Quality feedback loops**: Report input quality issues to upstream systems

**Key Statistic**
Databricks found that even highly capable frontier agents scored below 50% accuracy on real enterprise document reasoning tasks. The bottleneck wasn't reasoning - it was reading.

---

## Confidence Calibration

### Issue: Overconfident Wrong Answers

**Frequency**: Very Common

**Symptoms**
- High confidence scores on incorrect extractions
- Confidence doesn't correlate with accuracy
- Cannot use confidence to route to human review

**Root Cause**
VLMs are trained to produce fluent outputs, not calibrated uncertainty estimates. They express certainty linguistically even when visually uncertain.

**Example**
```
Extraction: "Total: $5,847.00" (confidence: 0.97)
Actual document: "$5,347.00"

Result: High-confidence wrong answer bypasses review queue
```

**Mitigation Strategies**
1. **Confidence recalibration**: Post-hoc calibration on held-out set
2. **Ensemble disagreement**: Multiple models, use variance as uncertainty proxy
3. **Token-level confidence**: Examine per-token probabilities, not just final score
4. **Human-in-the-loop thresholds**: Set thresholds based on empirical accuracy, not raw scores

---

## References

- [Hallucination of Multimodal Large Language Models: A Survey](https://arxiv.org/html/2404.18930v2)
- [Seeing is Believing? Mitigating OCR Hallucinations in MLLMs](https://arxiv.org/html/2506.20168v2)
- [Why LLMs Hallucinate More on Enterprise Documents](https://www.adlibsoftware.com/news/why-llms-hallucinate-more-on-enterprise-documents)
- [How to Evaluate Multimodal LLMs for Production Reliability](https://galileo.ai/blog/multimodal-llm-guide-evaluation)
- [Vision Language Models for Spreadsheet Understanding: Challenges and Opportunities](https://arxiv.org/html/2405.16234v1)
- [Why Frontier Agents Can't Read Documents](https://www.databricks.com/blog/why-frontier-agents-cant-read-documents-and-how-were-fixing-it)
