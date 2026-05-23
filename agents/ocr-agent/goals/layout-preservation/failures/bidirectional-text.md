# Bidirectional Text

## Issue: Right-to-Left and Mixed Direction Text

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

**Mitigation Strategies**
1. **Script detection**: Identify script before applying reading direction
2. **Bidirectional algorithm**: Implement Unicode BiDi algorithm for mixed text
3. **Segment-level processing**: Extract RTL and LTR segments separately, then combine
4. **Field-level direction**: Use field type to determine expected direction
