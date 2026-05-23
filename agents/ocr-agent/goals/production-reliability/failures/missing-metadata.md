# Missing Document Metadata

## Issue: Missing Document Metadata

**Frequency**: Common

**Symptoms**
- Extraction accuracy varies unexpectedly across documents
- Same document type from same vendor fails inconsistently
- Model lacks context needed for disambiguation

**Root Cause**
The deeper pattern across extraction failures is a context engineering problem - what information the extraction model receives (document metadata, layout signals, cross-document state, domain vocabulary) determines output quality more than model size or OCR accuracy alone.

**Example**
```
Input: Invoice with ambiguous date "03/04/2024"

Without context: Could be March 4 or April 3
With vendor metadata: Vendor is UK-based, so April 3 (DD/MM format)
With historical data: This vendor always uses DD/MM

Result: Without context, 50% chance of wrong date
```

**Mitigation Strategies**
1. **Metadata enrichment**: Pass sender, document type, locale to extraction
2. **Historical patterns**: Use past extractions from same source
3. **Cross-document state**: Share context across related documents
4. **Domain vocabularies**: Load industry-specific terminology
