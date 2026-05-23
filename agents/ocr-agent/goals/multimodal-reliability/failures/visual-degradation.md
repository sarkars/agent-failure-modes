# Visual Degradation

## Issue: Performance Collapse Under Visual Noise

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
