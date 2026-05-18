# Document Classification

Correctly identifying document types is essential for applying the right extraction logic. Misclassification cascades into extraction failures.

---

## Template Confusion

### Issue: Similar Templates Misclassified

**Frequency**: Common

**Symptoms**
- Invoice processing pipeline receives POs and fails
- Wrong extraction schema applied to document
- Fields extracted from incorrect positions

**Root Cause**
Business documents from the same company or industry often share similar layouts, logos, and formatting. The model cannot distinguish between closely related document types.

**Example**
```
Input: Purchase Order from Vendor A
Expected Classification: purchase_order
Actual Classification: invoice

Result: PO sent to AP workflow, fields misextracted (no "Amount Due" exists on PO)
```

**Commonly Confused Document Pairs**

| Document A | Document B | Why They're Similar |
|------------|------------|---------------------|
| Invoice | Purchase Order | Same vendor templates, similar line items |
| Quote | Invoice | Both have line items and totals |
| Receipt | Invoice | Similar structure, amounts, items |
| Packing Slip | Invoice | Same sender, same items |
| Statement | Invoice | Both have amounts and dates |
| Credit Memo | Invoice | Identical layout, only headers differ |

**Mitigation Strategies**
1. **Multi-label classification**: Classify document type AND subtype
2. **Key phrase detection**: Look for distinguishing text ("INVOICE", "PURCHASE ORDER")
3. **Field presence validation**: Certain fields only exist on certain doc types
4. **Sender-specific rules**: Same sender's invoices vs. POs have known differences
5. **Amount sign heuristics**: Credit memos have negative amounts

**Detection**
- Field extraction failures (expected field not found)
- Downstream workflow errors (wrong process triggered)
- User corrections in review interface

---

### Issue: Version and Variant Confusion

**Frequency**: Occasional

**Symptoms**
- Old template version extracted with new schema (or vice versa)
- Different regional variants handled incorrectly
- Draft vs. final versions not distinguished

**Root Cause**
Document templates evolve over time. The same document type from the same sender may have multiple versions in circulation.

**Example**
```
Input: 2023 invoice template from Vendor B
Classification: invoice (correct)
Schema Applied: 2024 template schema (incorrect)

Result: "Total" field moved in 2024, now extracting from wrong position
```

**Mitigation Strategies**
1. **Version detection**: Include version/template ID in classification
2. **Date-based routing**: Use document date to select appropriate schema
3. **Template fingerprinting**: Use layout hash to detect exact template
4. **Fallback extraction**: When primary positions fail, try alternate known positions

---

## Multi-Page Documents

### Issue: Page-to-Document Grouping Failures

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

---

### Issue: Attachments and Embedded Documents

**Frequency**: Occasional

**Symptoms**
- Email attachment classified as email
- Cover letter and attached document merged
- Embedded tables treated as separate documents

**Root Cause**
Documents containing or attached to other documents create nested classification challenges.

**Example**
```
Input: Email PDF with attached invoice

Classification: email (for entire PDF)
Result: Invoice never processed

Better: Classify email + detect and separately process attached invoice
```

**Mitigation Strategies**
1. **Attachment detection**: Identify embedded document boundaries
2. **Recursive processing**: Process main document, then process detected attachments
3. **Page content analysis**: Different formatting/style suggests different document
4. **Explicit markers**: Look for "Attachment", "Appendix", "Exhibit" headers

---

## Edge Cases

### Issue: Blank or Near-Blank Pages

**Frequency**: Common

**Symptoms**
- Processing time wasted on blank pages
- Blank pages classified as document type (forcing downstream errors)
- Pages with only signatures/stamps classified incorrectly

**Root Cause**
Blank pages from scanning, intentional separator pages, or pages with minimal content (just a signature) need special handling.

**Example**
```
Input: Blank separator page between documents
Classification: unknown (low confidence)
Result: Review queue flooded with blank pages
```

**Mitigation Strategies**
1. **Content threshold**: Require minimum text/content to process
2. **Blank detection**: Explicit "blank page" classifier
3. **Auto-discard**: Skip pages below content threshold with logging
4. **Signature-only detection**: Recognize pages that only contain signatures

---

### Issue: Poor Quality Rejects Valid Documents

**Frequency**: Occasional

**Symptoms**
- Legitimate documents rejected as "unreadable"
- Quality threshold too aggressive
- Faxes, copies of copies consistently fail

**Root Cause**
Quality filters meant to catch truly unprocessable documents also reject low-quality but readable documents.

**Example**
```
Input: Faxed invoice, low quality but readable
Classification: rejected (quality too low)
Result: Valid invoice requires manual processing
```

**Mitigation Strategies**
1. **Tiered processing**: Low quality → different pipeline, not rejection
2. **Preprocessing boost**: Apply enhancement before quality check
3. **Quality vs. confidence separation**: Low image quality doesn't mean low extraction confidence
4. **Source-specific thresholds**: Fax channel has lower quality expectations
