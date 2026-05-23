# Background Interference

## Issue: Background Interference

**Frequency**: Common

**Symptoms**
- Extra characters appear in extracted text
- Watermarks partially extracted as text
- Security patterns (guilloche) cause garbled output

**Root Cause**
Background elements like watermarks, security patterns, colored backgrounds, and stamps are interpreted as text characters.

**Example**
```
Input: Invoice with "PAID" watermark across page
Extracted line: "Total Due: $0P.0A0I D"

Result: Amount parsing fails
```

**Mitigation Strategies**
1. **Background removal**: Preprocess to isolate foreground text
2. **Color channel separation**: Process different color channels independently
3. **Watermark detection**: Identify and mask known watermark patterns
4. **Confidence filtering**: Watermark-derived characters typically have lower confidence
