# Source Misattribution

## Issue: Agent Attributes Information to Wrong Source

**Frequency**: Common

**Symptoms**
- Citations point to documents that don't contain the claim
- Quote attributed to wrong person
- Statistics linked to wrong study
- Source exists but doesn't support the claim made

**Root Cause**
Agent knows information should be cited but doesn't maintain accurate links between claims and sources. May confuse which source contained which information.

**Example**
```
Agent: "According to the Q3 2024 report, revenue increased 15% [1]"

Source [1] content: Q2 2024 report showing 12% growth

Reality: Q3 report showed 15%, but citation points to Q2 report

Result: User follows citation, finds different data, loses trust
```

**Mitigation Strategies**
1. **Extractive citations**: Quote directly from source
2. **Page/line references**: Point to exact location
3. **Citation verification**: Validate claim appears in cited source
4. **Source-claim linking**: Maintain explicit mappings
5. **Retrieval-then-generate**: Generate only from retrieved content
6. **Citation auditing**: Regularly verify citation accuracy

**Detection**
- Automated citation verification
- Compare extracted quotes to source text
- Track user reports of broken citations
- Sample-based human review
