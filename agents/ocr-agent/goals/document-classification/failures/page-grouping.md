# Page Grouping

## Issue: Page-to-Document Grouping Failures

**Frequency**: Common

**Symptoms**
- Multi-page document split into multiple single-page documents
- Pages from different documents incorrectly merged
- Page order scrambled

**Root Cause**
When processing batch scans or bulk uploads, determining which pages belong together requires detecting document boundaries.

**Example**
```
Input: Batch scan of 3 invoices (2 pages, 1 page, 3 pages)
Expected: 3 documents
Actual: 6 documents (each page separate)
        or: 2 documents (first two invoices merged)
```

**Mitigation Strategies**
1. **Barcode/separator detection**: Use separator sheets or barcodes between documents
2. **First-page indicators**: Detect "Page 1" or document start markers
3. **Continuity analysis**: Same invoice number, sender, style suggests same document
4. **Header matching**: Pages with matching headers likely belong together
