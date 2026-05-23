# Column Ordering

## Issue: Multi-Column Page Reading Order Errors

**Frequency**: Common

**Symptoms**
- Text from different columns interleaved
- Sentences start in one column, continue with text from another
- Paragraphs appear out of order

**Root Cause**
Multi-column layouts (newspapers, academic papers, brochures) require detecting column boundaries and reading each column top-to-bottom before moving to the next.

**Example**
```
Input: Two-column newsletter

Column 1:              Column 2:
"The company           "Sales increased
announced today        by 20% over
that production        last quarter
will increase..."      results..."

Extracted: "The company Sales increased announced today by 20% over..."

Result: Nonsensical text
```

**Mitigation Strategies**
1. **Column detection**: Identify vertical gutters between columns
2. **Reading order models**: Use models trained on multi-column layouts
3. **Semantic coherence checks**: Detect when adjacent text doesn't form coherent sentences
4. **Document type classification**: Apply column-aware processing for detected types (newspaper, paper, etc.)
