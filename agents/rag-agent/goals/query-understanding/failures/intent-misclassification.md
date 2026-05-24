# Intent Misclassification

## Issue: Agent Misunderstands What User Wants to Accomplish

**Frequency**: Common

**Symptoms**
- Informational response when action needed
- Action taken when information wanted
- Wrong type of answer (comparison vs. explanation)
- Response doesn't match user's actual goal

**Root Cause**
The literal query may differ from user intent. Model interprets surface meaning, missing underlying goal.

**Example**
```
Query: "How do I change my password?"

User intent: Want step-by-step instructions to change password NOW

Agent response: "Password changes are handled by our security team. 
Passwords must be at least 12 characters with a mix of letters, 
numbers, and symbols. Regular password changes every 90 days are 
recommended for security."

Missing: Actual steps to change password

Result: User gets policy info instead of actionable instructions
```

**Mitigation Strategies**
1. **Intent classification**: Categorize query type before retrieval
2. **Action vs. info routing**: Different retrieval strategies by intent
3. **Response type matching**: Ensure response format matches intent
4. **Clarifying questions**: Confirm action vs. information needs
5. **Task-oriented responses**: Focus on user's goal, not just topic
6. **Intent signals**: Detect "how do I" vs. "what is" patterns

**Detection**
- Track response type vs. query type alignment
- Monitor user follow-ups indicating wrong response type
- Classify queries and compare to response format
- User satisfaction by intent category

## References

- [Mindee: RAG Hallucinations Explained](https://www.mindee.com/blog/rag-hallucinations-explained) - Intent recognition
- [FloTorch: 2026 RAG Performance Landscape](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know) - Query routing
