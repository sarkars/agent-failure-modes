# AI Document Extraction Accuracy Drops in Production vs Benchmarks: Causes and Fixes

## Issue: Input Quality Gap — Real Documents Are Messier Than Benchmark Documents

**Frequency**: Very Common

**Symptoms**
- Benchmark performance far exceeds real production performance
- Agent performs well in demos but fails on real, messy enterprise documents
- Accuracy varies wildly across document sources with no single root cause
- Commonly reported when scaling LlamaIndex- or LangChain-style document ingestion pipelines from a clean demo corpus to real scanned/legacy enterprise input

**Root Cause**
Enterprise documents include scanned PDFs with inconsistent OCR quality, complex regulatory submissions with nested table structures, CAD drawings and mixed-format engineering packages, handwritten forms, and legacy system exports never designed for machine consumption.

**Key Finding**
The gap between benchmark performance and production performance in enterprise document environments is not a model gap - it is an input quality gap.

**How to fix it**: normalize inconsistent real-world formats into a standard internal representation before inference, gate low-quality input to a different path, and build source-specific pipelines rather than one generic path. See the mitigations below.

## Mitigation Strategies

### Prevention
1. **Standardized preprocessing pipeline across file types**: Normalize scanned PDFs, CAD drawings, legacy exports, and handwritten forms into a consistent internal representation (e.g., structured layout + multi-layer OCR text) before any model inference, so extraction quality doesn't depend on which raw format a document happened to arrive in. Trade-off: building and maintaining normalizers for every real-world source format is a substantial, ongoing engineering investment, not a one-time task.
2. **Pre-inference quality validation gate**: Score input quality (resolution, contrast, completeness, OCR confidence on a first pass) before running the primary extraction model, and route documents below a quality floor to a different path (rescan request, enhanced preprocessing, human transcription) rather than running them through the standard pipeline and hoping for the best. Trade-off: adds a gating stage and requires defining quality thresholds per document type, which take tuning.
3. **Source-specific pipeline branches**: Build distinct preprocessing/extraction paths per known input source (e.g., "legacy ERP export," "faxed form," "high-res scan") rather than one generic pipeline, since sources differ systematically in their failure modes and a one-size pipeline optimizes for none of them well. Trade-off: increases pipeline complexity and the number of paths to maintain and monitor.

### Detection & Response
1. **Benchmark-vs-production accuracy gap tracking**: Continuously compare production accuracy against benchmark/demo accuracy for the same model version; a persistent, large gap is itself the signal that input quality — not model capability — is the binding constraint, and that finding should redirect investment toward preprocessing rather than model upgrades.
2. **Source-level accuracy segmentation**: Track extraction accuracy separately per input source/document type rather than only in aggregate; a source with disproportionately low accuracy needs source-specific preprocessing investment, which aggregate metrics would hide.
3. **Upstream quality feedback loop**: When a document source consistently produces low-quality input (e.g., a scanning process, an upstream system's export format), feed that finding back to the team/system generating the input rather than only compensating downstream — fixing the source is often cheaper than compensating for it repeatedly.

### Architecture Patterns
1. **Quality-gated multi-path pipeline**: Architect the pipeline so a quality-scoring stage runs first and routes documents into different downstream paths (standard, enhanced-preprocessing, human-transcription) based on measured input quality, rather than a single fixed path for all input.
2. **Multi-layer OCR with layout preservation**: Use an OCR/parsing layer that preserves structural/layout context (not just raw text) as the normalized intermediate representation feeding the extraction model, since layout context materially improves extraction accuracy on real enterprise documents versus flattened text.
3. **Per-source pipeline registry**: Maintain a registry mapping known document sources to their specific preprocessing pipeline, with a documented default/fallback path for genuinely novel sources, so new source types can be onboarded with source-specific handling rather than forced through a generic path.

### Metrics
1. **benchmark_vs_production_accuracy_gap**: Target: < 10 percentage points; Alert if > 25 points (signals input quality, not model choice, is the priority)
2. **input_quality_gate_rejection_rate**: Target: track as baseline per source; Alert if it changes > 2x (signals upstream quality regression)
3. **per_source_accuracy_variance**: Target: < 15 percentage point spread across known sources; Alert if any source falls > 25 points below the average
4. **quality_feedback_loop_response_rate**: Target: > 80% of flagged upstream quality issues acknowledged/addressed within 2 weeks; Alert if < 40%

### Alerts
1. **Benchmark/Production Gap Widening** (P2): Condition - the gap between benchmark and production accuracy exceeds 25 points for a document type. Action: Prioritize preprocessing/input-quality investigation over model upgrades for that document type.
2. **Source-Specific Accuracy Outlier** (P1): Condition - a specific input source's accuracy falls more than 25 points below the cross-source average. Action: Build or improve a dedicated preprocessing path for that source before continuing to route it through the generic pipeline.
3. **Quality Gate Rejection Spike** (P2): Condition - quality-gate rejection rate for a source doubles from baseline. Action: Investigate whether the upstream system/process generating that source has degraded, and notify the owning team.

**Key Statistic**
Databricks found that even highly capable frontier agents scored below 50% accuracy on real enterprise document reasoning tasks. The bottleneck wasn't reasoning - it was reading.

## References

- [Why Frontier Agents Can't Read Documents](https://www.databricks.com/blog/why-frontier-agents-cant-read-documents-and-how-were-fixing-it) - OfficeQA benchmark, <50% accuracy
- [Why LLMs Hallucinate More on Enterprise Documents](https://www.adlibsoftware.com/news/why-llms-hallucinate-more-on-enterprise-documents) - Input quality gap analysis
- [AlterSquare: Document AI Fails](https://altersquare.io/enterprise-document-ai-fails-extraction-layer-not-model-layer/) - Benchmark vs. production gap
