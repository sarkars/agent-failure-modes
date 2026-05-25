# Cross-Session Data Bleed

## Issue: Data from One User's Session Appears in Another's

**Frequency**: Common

**Symptoms**
- User sees another user's conversation history
- Previous session data influences current response
- Multi-tenant data contamination
- Personal context from User A appears for User B
- Agent references conversations it shouldn't know about

**Root Cause**
Improper session isolation allows data to persist or leak between user sessions. This can happen through: shared conversation buffers, improperly scoped memory systems, caching without user partitioning, or context windows that aren't properly cleared. In multi-tenant deployments, tenant isolation failures expose one customer's data to another.

**Example**
```
Session 1 (User A - Healthcare company):
User A: "Summarize the patient records for John Doe"
Agent: "Patient John Doe, DOB 05/12/1965, diagnosed with..."

[Session ends, but agent memory not properly cleared]

Session 2 (User B - Different company):
User B: "What do you know about John?"
Agent: "Based on the records, John Doe is a patient born 
        05/12/1965 with a diagnosis of..."

Problem: User B received User A's patient data
         Session isolation failure

---

Caching failure example:

User A: "What's my account balance?"
Agent: [Retrieves] "Your balance is $45,230.00"
[Response cached]

User B: "What's my account balance?"
Agent: [Returns cached] "Your balance is $45,230.00"

Problem: Cache key didn't include user ID
```

**Key Statistics**
From Session Isolation Research (2026):
- Cross-tenant data leakage: Top 5 AI security concern
- Session isolation failures: 20% of enterprise deployments
- Memory systems: Most common source of bleed
- Cache misconfigurations: Second most common
- Average exposure: 3-5 sessions before detection

**Bleed Vectors**
| Vector | Cause | Risk Level |
|--------|-------|------------|
| Memory systems | Shared memory without user scope | Critical |
| Response caching | Cache key missing user ID | Critical |
| Context windows | Previous context not cleared | High |
| RAG retrieval | Embeddings not user-partitioned | High |
| Conversation buffers | Shared buffer pool | Critical |
| Model state | Stateful models without reset | Medium |

**Contributing Factors**
- Shared infrastructure without isolation
- Memory/cache keys missing user identifiers
- "Optimization" that removes isolation
- Long-running agent instances
- RAG without tenant filtering
- Conversation history not scoped

**Mitigation Strategies**
1. **Session isolation**: Strict boundaries per user/tenant
2. **Scoped caching**: Include user ID in all cache keys
3. **Memory partitioning**: Separate memory stores per user
4. **Context clearing**: Explicit reset between sessions
5. **RAG filtering**: Tenant ID in all retrieval queries
6. **Stateless design**: Prefer stateless agent architecture

**Detection**
- Audit logs for cross-user data access
- Canary data per user to detect bleed
- Monitor for references to "other" conversations
- Test with synthetic multi-user scenarios
- Alert on user A's data patterns in user B's session

## References

- [OWASP: Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- [Multi-Tenant LLM Security](https://www.anthropic.com/research/multi-tenant-security)
- [CSA: AI Security Incidents](https://cloudsecurityalliance.org/) - Cross-tenant issues
- [LangChain Memory](https://python.langchain.com/docs/modules/memory/) - Session scoping
