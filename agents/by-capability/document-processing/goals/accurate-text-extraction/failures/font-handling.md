# Font and Style Handling

## Issue: Decorative and Stylized Font Failures

**Frequency**: Occasional

**Symptoms**
- High error rates on specific document sources
- Certain company's documents consistently fail extraction
- Brand names and logos text extracted incorrectly

**Root Cause**
Decorative fonts, stylized text, and brand-specific typography differ significantly from standard fonts in training data.

**Example**
```
Input: Company logo with stylized "ACME CORP"
Expected: ACME CORP
Actual: RCME CORF (stylized A looks like R, P like F)
```

**Mitigation Strategies**
1. **Template matching**: For known document sources, define fixed regions to skip or use template-specific extraction
2. **Logo detection**: Identify and exclude logo regions from text extraction
3. **Source-specific fine-tuning**: Train on documents from frequent sources
4. **Fallback to business rules**: Use sender metadata instead of extracted company name

## References

- [Why AI OCR Fails](https://parseur.com/blog/why-ai-ocr-fail) - Font recognition problems
- [AlterSquare: Document AI Fails](https://altersquare.io/enterprise-document-ai-fails-extraction-layer-not-model-layer/) - Extraction layer issues
