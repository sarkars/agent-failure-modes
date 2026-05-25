# Similar Templates

## Issue: Similar Templates Misclassified

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

## References

- [AlterSquare: Document AI Fails](https://altersquare.io/enterprise-document-ai-fails-extraction-layer-not-model-layer/) - Template matching challenges
- [IDP Challenges 2026](https://idp-software.com/guides/idp-challenges-2026/) - Document type confusion
- [Why OCR Alone Fails](https://dev.to/jakemiller/why-ocr-alone-fails-in-real-world-documents-5f86) - Classification limitations
