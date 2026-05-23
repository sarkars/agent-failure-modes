# Granularity Mismatch

## Issue: Citation Points to Wrong Level of Specificity

**Frequency**: Common

**Symptoms**
- Citation to entire document when specific section needed
- Page/section numbers missing or wrong
- User must search within document to find info
- Too-specific citation misses broader context

**Root Cause**
Citations may be at document level when paragraph-level needed, or vice versa. Model may not track or output precise locations.

**Example**
```
Agent response: "The API rate limit is 100 requests per minute [1]"

Citation [1]: "Technical Documentation" (500-page PDF)

User experience: Must search 500 pages for rate limit info

Better citation: "Technical Documentation, Section 4.2.3: Rate Limits"
```

**Mitigation Strategies**
1. **Hierarchical citations**: Document > Section > Paragraph
2. **Page/section tracking**: Maintain location in chunk metadata
3. **Deep linking**: Link to specific section when possible
4. **Quote inclusion**: Include excerpt so user doesn't need to search
5. **Location metadata**: Store and output precise locations
6. **Chunk-level attribution**: Cite specific chunk, not just document

**Detection**
- Track time users spend finding cited information
- Monitor citation specificity levels
- User feedback on citation usefulness
- Compare citation granularity to claim specificity
