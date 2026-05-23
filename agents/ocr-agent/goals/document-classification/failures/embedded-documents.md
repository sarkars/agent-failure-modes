# Embedded Documents

## Issue: Attachments and Embedded Documents

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
