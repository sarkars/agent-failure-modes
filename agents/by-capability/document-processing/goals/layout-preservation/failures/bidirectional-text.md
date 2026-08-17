# RTL and Bidirectional Text Extracted Reversed or Garbled: Causes and Fixes

## Issue: Agent Extracts Right-to-Left and Mixed-Direction Text Reversed or Jumbled

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

## Mitigation Strategies

How to fix it: detect script direction per text run and apply the Unicode BiDi algorithm to recombine segments, rather than assuming one document-wide reading direction.

### Prevention
1. **Script detection before direction assignment**: Run script/language detection on each text run before deciding reading direction, rather than assuming a single document-level direction, since a single invoice can mix Arabic body text with embedded English product codes that must each be read in their own direction. Trade-off: script detection on short embedded runs (a 4-character code) can be ambiguous and misclassified.
2. **Unicode BiDi algorithm implementation**: Apply the standard Unicode Bidirectional Algorithm to properly interleave RTL and LTR segments according to embedding rules, rather than a naive left-to-right or right-to-left concatenation, since ad hoc handling is exactly what produces reversed/jumbled output like "100-VNI# ةروتاف". Trade-off: correct BiDi implementation is nontrivial and numeral-handling within RTL context (European vs. Arabic-Indic digits) needs explicit rules.
3. **Segment-level extraction and recombination**: Extract contiguous RTL and LTR segments as separate units first, preserving their internal order, then recombine them according to BiDi embedding rules rather than attempting a single end-to-end read across the direction change. Trade-off: requires accurate segment-boundary detection, which itself can be error-prone at script transition points.

### Detection & Response
1. **Reversed-text pattern detection**: Monitor extracted text for signatures of BiDi failure (e.g., a known field value appearing character-reversed, or a mix of scripts in an order that doesn't match any valid reading order) and flag for reprocessing with corrected BiDi handling.
2. **Field-level direction mismatch alerts**: For fields with a known expected direction (e.g., a numeric ID field should read left-to-right even embedded in RTL text), validate extracted field values against that expectation and flag mismatches.
3. **Language/script distribution monitoring**: Track the script/language mix detected across a document source; a source expected to be predominantly RTL that suddenly shows garbled or majority-LTR-looking output signals a BiDi processing regression.

### Architecture Patterns
1. **Confidence-gated human-in-the-loop review queue**: Route documents with detected mixed-direction text and low BiDi-resolution confidence to bilingual reviewers rather than accepting best-effort automated recombination.
2. **Field-type-driven direction override**: Architect field extraction so each field type carries a known expected direction (numeric IDs, dates always LTR regardless of surrounding script) that overrides general BiDi inference when the two conflict.
3. **Script-segmented extraction pipeline**: Structure extraction as script detection -> per-segment extraction -> BiDi-rule recombination, as three distinct, independently testable stages rather than a single monolithic OCR-to-text step.

### Metrics
1. **bidi_reversal_defect_rate**: Target: < 2% of mixed-direction documents; Alert threshold: > 6%
2. **field_direction_mismatch_rate**: Target: < 1% of direction-constrained fields; Alert threshold: > 4%
3. **script_detection_accuracy**: Target: > 97%; Alert threshold: < 90%
4. **review_routing_rate_for_mixed_direction**: Target: matches detected ambiguous-segment rate; Alert threshold: gap > 10%

### Alerts
1. **BiDi Reversal Defect Spike** (P2): Condition - reversal defect rate for a source/language pair exceeds 6%. Action: Sample documents, verify BiDi algorithm implementation and segment boundary detection for that script pair.
2. **Field Direction Mismatch** (P2): Condition - direction-constrained field mismatch rate exceeds 4%. Action: Review field-type direction override rules; check for a new field type not yet covered.
3. **Script Detection Degradation** (P3): Condition - script detection accuracy for a source drops below 90%. Action: Investigate short-segment ambiguity or a new script/language appearing in the source mix.

## References
- [Why AI OCR Fails](https://parseur.com/blog/why-ai-ocr-fail) - Multi-language challenges
- [IDP Accuracy Reckoning 2026](https://idp-software.com/news/idp-accuracy-reckoning-2026/) - RTL text handling
