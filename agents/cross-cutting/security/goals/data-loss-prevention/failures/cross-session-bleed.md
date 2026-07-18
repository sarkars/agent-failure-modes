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

## Test Scenario & Reproduction

### Scenario Setup
- Deploy a multi-tenant agent service where response caching keys are built from the query text alone, without including the requesting user's ID
- Two different users, User A (healthcare company) and User B (a different company), share the same agent deployment and cache layer
- No canary-data detection or cross-user audit process monitors for cache-key collisions
- Session/context clearing between requests relies on assumed rather than verified behavior

### Trigger Mechanism
1. User A asks a question that triggers a lookup and gets a response, which is cached under a key derived only from the query text
2. User A's session ends
3. User B, unrelated to User A, asks a structurally similar or identical query
4. The cache layer returns User A's cached response to User B because the cache key didn't distinguish between users

### Example Reproduction Steps
```
1. Session A (user_id=A): "What's my account balance?"
   Agent retrieves and responds: "Your balance is $45,230.00"
   Cache write: key = hash("What's my account balance?") -> "$45,230.00"
2. Session B (user_id=B): "What's my account balance?"
   Cache lookup: key = hash("What's my account balance?") -> HIT
   Agent returns cached: "Your balance is $45,230.00"
3. Verify User B's actual balance differs from the cached value
   returned, confirming User A's data was served to User B
```

### Expected Failure State
User B receives User A's account balance (or, in the healthcare variant, User A's patient record) because the cache key lacked a user/tenant identifier, with no error or warning surfaced to either user. A correctly isolated system includes the user or tenant ID as a mandatory component of every cache key, so a structurally identical query from a different user can never produce a cache hit against another user's cached response.

## Mitigation Strategies

### Prevention
1. **User/tenant ID as a mandatory component of every cache and memory key**: Require every cache key, memory-store key, and retrieval query filter to include the user or tenant identifier as a non-optional, enforced-at-the-framework-level component, so it becomes structurally impossible to read another user's cached response or memory even if application logic elsewhere has a bug. Trade-off: requires auditing and retrofitting every existing caching/memory layer in the system, which can be extensive in mature codebases with ad hoc caching added over time.
2. **Stateless agent architecture with explicit context passed per request**: Prefer designing agent instances to be stateless between requests, with all session/user context explicitly passed in on each call rather than persisted in shared, long-running agent instance memory, eliminating the entire class of bugs where a previous user's context lingers in an agent instance reused for a new user. Trade-off: stateless design can increase per-request latency (context must be reloaded each time) and complicates use cases that benefit from genuine long-running conversational memory.
3. **Explicit session/context clearing with verification, not assumption**: When session-scoped state must exist, implement and test explicit clearing logic between sessions, with automated tests verifying that state is actually empty post-clear (not just assuming a reset call worked), since "context not properly cleared" was a documented root cause even in systems that believed they were clearing state.

### Detection & Response
1. **Canary data per user for bleed detection**: Seed each user/tenant's session with a unique, synthetic canary value and periodically check whether any other user's session ever surfaces that canary, providing an active, continuous test for cross-session bleed rather than relying solely on passive audit review.
2. **Cross-user data access auditing**: Regularly audit logs for any case where a response to User B's request contains data patterns, identifiers, or content traceable to User A, treating any confirmed instance as a critical incident given the demonstrated potential for full patient/financial record exposure.
3. **Synthetic multi-user test scenarios in CI/staging**: Run automated multi-user test scenarios (simulating rapid session switching, concurrent multi-tenant load) specifically designed to trigger bleed conditions before any deployment, since this failure mode is often load- or concurrency-dependent and won't surface in single-user manual testing.

### Architecture Patterns
1. **Hard tenant/user partitioning at the data-store level**: Architect memory stores, caches, and RAG indices with hard partitioning (separate physical/logical stores per tenant, or database-enforced row-level security keyed to tenant ID) rather than relying on application-level filters that can be forgotten or misapplied in a specific code path.
2. **Request-scoped context injection over shared long-running state**: Design the agent execution model so context is injected fresh per request from an explicitly-scoped source (not read from a shared, potentially-stale in-memory object), eliminating reliance on correct manual clearing.
3. **Automated isolation-verification gate in CI/CD**: Build cross-session-bleed test scenarios into the standard CI/CD pipeline as a release gate, not an occasional manual audit, so isolation regressions are caught before deployment rather than discovered in production.

### Metrics
1. **canary_bleed_detection_rate**: Target: 0 canary values ever surface outside their originating session; Alert on any occurrence
2. **cache_key_scoping_coverage**: Target: 100% of cache/memory keys include user/tenant ID; Alert if any unscoped key pattern is found in audit
3. **cross_user_data_audit_finding_rate**: Target: 0 confirmed cross-user exposures; Alert on any occurrence
4. **isolation_test_pass_rate_in_ci**: Target: 100% of multi-user isolation tests pass before deployment; Alert/block deployment on any failure

### Alerts
1. **Canary Data Bleed Detected** (P1): Condition - a user-specific canary value surfaces in another user's session. Action: Treat as a confirmed critical incident; investigate the specific caching/memory layer responsible immediately, assess scope of actual user data exposed during the same window.
2. **Cross-User Data Exposure Confirmed** (P1): Condition - audit finds a response containing another user's data. Action: Immediately notify affected users per breach-notification policy, contain the responsible code path, conduct full incident review.
3. **Isolation Test Failure in CI** (P1): Condition - a multi-user isolation test fails during CI/CD. Action: Block the deployment; do not allow release until the isolation defect is fixed and tests pass.

## References

- [OWASP: Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
- [Multi-Tenant LLM Security](https://www.anthropic.com/research/multi-tenant-security)
- [CSA: AI Security Incidents](https://cloudsecurityalliance.org/) - Cross-tenant issues
- [LangChain Memory](https://python.langchain.com/docs/modules/memory/) - Session scoping
