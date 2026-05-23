# Input Quality Gap

## Issue: Input Quality Gap

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
