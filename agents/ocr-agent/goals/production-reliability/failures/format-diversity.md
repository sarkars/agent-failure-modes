# Format Diversity

## Issue: Format Diversity Overwhelms Rules

**Frequency**: Very Common

**Symptoms**
- Works for top vendors, fails for long tail
- Every new vendor requires manual configuration
- Maintenance burden grows linearly with vendor count

**Root Cause**
Invoices arrive in multiple formats - PDFs, Excel files, scanned images, or paper copies. Each may follow a different layout, include varying fields, or use unique terminology. Non-standard invoices hinder automation as systems struggle to extract data from inconsistent formats.

**Example**
```
Vendor A: PDF, structured, "Total Due" field
Vendor B: Scanned image, "Amount Payable" field
Vendor C: Excel, amounts in various cells
Vendor D: Handwritten corrections over printed form

Result: System configured for A works, B-D require custom handling
```

**Key Finding**
More than half of all the work AP does revolves around manual invoice data entry and classification due to format diversity.

**Mitigation Strategies**
1. **ML-based extraction**: Train on diverse examples rather than rigid rules
2. **Semantic understanding**: Map diverse labels to canonical fields
3. **Tiered automation**: High automation for common formats, human assist for rare
4. **Vendor onboarding process**: Collect sample documents, validate extraction before go-live

## References

- [IDP Challenges 2026](https://idp-software.com/guides/idp-challenges-2026/) - Format diversity challenges
- [Why OCR Alone Fails](https://dev.to/jakemiller/why-ocr-alone-fails-in-real-world-documents-5f86) - Multi-format handling
- [Document AI: Next Evolution of IDP](https://www.llamaindex.ai/blog/document-ai-the-next-evolution-of-intelligent-document-processing) - Semantic extraction
