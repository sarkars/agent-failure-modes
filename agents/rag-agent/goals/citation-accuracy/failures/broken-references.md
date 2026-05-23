# Broken References

## Issue: Citations Link to Unavailable or Moved Content

**Frequency**: Occasional

**Symptoms**
- Citation URLs return 404
- Document has been moved or deleted
- Permission denied when following citation
- Link format incorrect

**Root Cause**
- Documents moved after indexing
- URLs changed without index update
- Permission changes not reflected
- Temporary documents cited

**Example**
```
Agent response: "See the policy document [1]"

Citation [1]: https://internal.company.com/docs/policy-v2.pdf

User clicks: "404 Not Found - This page doesn't exist"

Reality: Policy renamed to policy-v3.pdf last month

Result: User can't access cited information
```

**Mitigation Strategies**
1. **Link validation**: Check URLs are accessible before citing
2. **Canonical URLs**: Use permanent, stable identifiers
3. **Freshness checks**: Verify links periodically
4. **Fallback content**: Include enough context that link isn't critical
5. **Version tracking**: Detect when documents are updated/moved
6. **Archive links**: Maintain accessible copies of cited content

**Detection**
- Automated link checking
- Track 404 rates on citations
- Monitor user reports of broken links
- Regular crawl of cited URLs
