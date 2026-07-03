# Vision Model Grid Cell Counting Failure

## Issue: Vision-language models fail to accurately count grid cells in low-resolution or small-cell images; state-of-the-art models hallucinate counts at specific cell sizes

**Frequency**: Common

**Symptoms**
- Model returns incorrect count for simple grid cell counting tasks (off-by 2-5+ cells)
- Errors concentrate on specific cell sizes (e.g., 32px cells counted correctly, 24px cells miscounted)
- Error rates increase as cells become smaller or less visually distinct
- Same image counted differently by same model on repeated queries
- Model expresses high confidence in incorrect counts

**Root Cause**
Vision-language models tokenize images into patches (typically 14×14 or 16×16 pixels). When grid cells are small (16-24 pixels), patch boundaries misalign with cell boundaries. Model sees partial cells at edges, conflates cells separated by thin lines, or miscounts due to incomplete visual information at patch boundaries. Patch tokenization creates "visual blind spots" that don't align with semantic grid structure.

**Examples**

### Example 1: Grid Cell Counting in Data Visualization
```
Image: 8×8 grid of small cells (20px each), alternating colors
Model asked: "How many cells are colored red?"
Model response: "There are 35 red cells"
Actual count: 32 red cells
Root cause: Patch boundaries split some cells, causing 3-cell miscount
```

### Example 2: Chess Board Square Counting
```
Image: Standard chess board (8×8 = 64 squares)
Model asked: "Count the white squares on this board"
Model response: "There are 48 white squares"
Actual count: 32 white squares
Confidence: 95%
Root cause: Patch size (16px) misaligns with square boundaries (30px); model sees fragments
```

### Example 3: Microscopy Grid Analysis
```
Image: 10×10 grid of cells from microscope (cell size 18px at screen resolution)
Model asked: "How many cells contain dark staining?"
Model response: "Approximately 45 cells"
Actual count: 38 cells
Impact: Researchers miscount stained cells, incorrect analysis
Root cause: Small cell size causes tokenization misalignment
```

### Example 4: Spreadsheet Cell Analysis
```
Image: 12×12 spreadsheet grid (cells 15px)
Model asked: "How many cells have numeric values?"
Model response: "87 cells"
Actual count: 72 cells
Impact: Automated data extraction fails
Root cause: Cell size smaller than patch granularity
```

**Key Statistics**
| Finding | Source |
|---|---|
| State-of-the-art VLMs fail at grid cell counting | arXiv:2509.15435 (ORCA) |
| Error rates >20% for cells <24px | arXiv:2509.15435 |
| Specific cell sizes show systematic bias | arXiv:2509.15435 |
| Patch tokenization creates visual blind spots | arXiv:2509.15435 |

---


## Test Scenario & Reproduction

### Scenario Setup
- Vision model with standard patch tokenization (14x14 or 16x16)
- Test images with small grid cells (16-24 pixels)
- No preprocessing or image enhancement
- Single-pass model evaluation

### Trigger Mechanism
```
1. Create test image: 10x10 grid, 20px cells, alternating colors
2. Ask model: "Count red cells"
3. Model processes image with default patch size
4. Compare model count to actual count
5. Record error rate and confidence
```

### Expected Failure State
- Model count off by 2-5+ cells
- Errors systematic at specific cell sizes
- Model expresses high confidence despite error
- Small cell sizes (16-24px) trigger failures
- Same image counted differently on retry

### Mitigation Validation Protocol
**Test Checklist:**
- [ ] Reproduce: Count error >10% on small-cell grids
- [ ] Apply mitigation (upscale image 2-4x)
- [ ] Re-run → counting accuracy improves >90%
- [ ] Test multiple cell sizes (8px, 16px, 24px, 32px)

**Success Criteria:**
- Counting accuracy >95% across all cell sizes
- Error rate proportional to cell size addressed
- No high-confidence miscounts in test suite

## Mitigation Strategies

1. **Pre-Processing: Upscale Small Grids**
   - Enlarge image 2-4x before passing to vision model
   - Ensures cells are larger than typical patch size (14-16 pixels)
   - Trade-off: Increased compute, potential artifacts

2. **Overlay Grid Lines**
   - Add high-contrast grid lines (white or black) between cells
   - Helps model distinguish individual cells even at small sizes
   - Verify grid lines don't introduce new visual artifacts

3. **Divide-and-Conquer Strategy**
   - Crop image into smaller sections (each containing 2-3 cells)
   - Have model count cells in each section
   - Sum results and verify for overlaps
   - More reliable than single-pass counting

4. **Multi-Modal Verification**
   - Use OCR to detect cell values/text
   - Use object detection to find cell boundaries
   - Compare vision model count against structural analysis
   - Flag mismatches for manual review

5. **Use Specialized Vision Models**
   - Consider models trained on grid/table analysis (e.g., table detection models)
   - General-purpose vision models not optimized for counting small, uniform objects
   - Domain-specific models have better patch alignment with typical grid structures

6. **Temperature & Sampling Control**
   - Set model temperature to 0.0 (deterministic) for counting tasks
   - Repeated queries show variation; take median of 3-5 runs
   - High variation suggests low-confidence counting

### Metrics
- Counting error rate (|predicted - actual| / actual)
- Error rate by cell size (track separately for 8px, 16px, 24px, 32px, etc.)
- Confidence calibration: % of high-confidence incorrect counts
- False positive rate: Models claiming to count when grid is ambiguous

### Alerts
- Counting error >10% on validation set → Model degradation
- High-confidence count differs from structured analysis (OCR, object detection) → P1
- Cell size changes without model revalidation → Request revalidation

---

## Related Patterns
- [Confident Fabrication](../../../../../cross-cutting/accuracy/goals/output-accuracy/failures/confident-fabrication.md) — High confidence despite incorrect counting
- [Vision Model Hallucination - Patch Tokenization Boundaries](./vision-model-patch-tokenization-boundary-failure.md) — Root cause: patch misalignment
- [Semantic Similarity Retrieval Misses Structural Attributes](../../../../../by-capability/knowledge-retrieval/goals/retrieval-relevance/failures/semantic-similarity-retrieval-misses-structural-attributes.md) — Structural attribute detection failures

---

## References

- [ORCA: An Agentic Reasoning Framework for Hallucination and Adversarial Robustness in Vision-Language Models](https://arxiv.org/abs/2509.15435) - Core reference; documents VLM counting failures at specific cell sizes
- [A Survey on Agentic Multimodal Large Language Models](https://arxiv.org/abs/2510.10991) - Survey of multimodal agent failures including visual reasoning
- [Automatically Generating Visual Hallucination Test Cases for Multimodal Large Language Models](https://arxiv.org/abs/2410.11242) - Test case generation for systematic evaluation
