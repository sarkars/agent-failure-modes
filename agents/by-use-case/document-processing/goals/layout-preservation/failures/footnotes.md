# Footnotes

## Issue: Footnotes and Marginal Notes Misplaced

**Frequency**: Occasional

**Symptoms**
- Footnotes appear in middle of paragraphs
- Marginal annotations merged with body text
- Reference numbers disconnected from footnote content

**Root Cause**
Footnotes and margin notes exist outside the main content flow. Reading-order extraction places them incorrectly.

**Example**
```
Input:
"The study found significant results¹ in all tested conditions."

Footnote at bottom:
"¹ p < 0.05"

Extracted: "The study found significant results in all tested conditions. ¹ p < 0.05"

Expected: Footnote linked to reference
Actual: Footnote appended as regular text
```

**Mitigation Strategies**
1. **Footnote region detection**: Identify footnote sections by position and formatting
2. **Reference linking**: Match superscript numbers to footnote numbers
3. **Structured output**: Output footnotes as separate linked elements
4. **Exclusion option**: For some use cases, exclude footnotes entirely

## References
- [AlterSquare: Document AI Fails](https://altersquare.io/enterprise-document-ai-fails-extraction-layer-not-model-layer/) - Document structure
- [Why OCR Alone Fails](https://dev.to/jakemiller/why-ocr-alone-fails-in-real-world-documents-5f86) - Content flow issues
