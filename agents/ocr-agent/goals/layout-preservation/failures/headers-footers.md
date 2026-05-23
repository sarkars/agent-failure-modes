# Headers and Footers

## Issue: Headers/Footers Duplicated or Misplaced

**Frequency**: Common

**Symptoms**
- Same header text appears multiple times in extraction
- Page numbers interleaved with content
- Running headers merged with body text

**Root Cause**
Multi-page documents have repeating headers and footers. Without page boundary detection, these repeat in output and disrupt content flow.

**Example**
```
Input: 5-page report

Extracted: "...end of section 1. Company Name | Confidential | Page 2 Section 2 begins..."

Result: Header content pollutes body text
```

**Mitigation Strategies**
1. **Page region classification**: Identify header/footer zones by position
2. **Repetition detection**: Remove text that repeats at consistent positions across pages
3. **Page number detection**: Identify and exclude page numbering patterns
4. **First-page exception**: Headers on first page often differ - handle separately
