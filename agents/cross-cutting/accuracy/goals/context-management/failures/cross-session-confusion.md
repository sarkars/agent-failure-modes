# Cross-Session Confusion

## Issue: Agent Confuses Information Across Sessions

**Frequency**: Occasional

**Symptoms**
- Agent references conversation from different user
- Private information leaks between sessions
- Agent applies one user's preferences to another
- Session boundaries not respected

**Root Cause**
- Shared memory or state across sessions
- Improper session isolation
- User identification errors
- Cached responses reused incorrectly

**Example**
```
Session A (User Alice): "I'm working on Project Gamma"
Session B (User Bob): "What project am I working on?"
Agent: "You're working on Project Gamma"

Result: Bob sees Alice's project info - privacy violation
```

---

## Test Scenario & Reproduction

### Scenario Setup
- Two distinct, separately authenticated user sessions (Session A as Alice, Session B as Bob) sharing the same underlying memory/cache infrastructure
- No per-session state isolation or owner-tag enforcement on stored/cached data
- No mandatory user-authentication check gating memory reads against the requesting user's identity

### Trigger Mechanism
1. In Session A (authenticated as Alice), state a private fact ("I'm working on Project Gamma")
2. Leave Session A active or closed, then open Session B authenticated as a different user (Bob)
3. In Session B, ask a question that would only be answerable from Alice's private state ("What project am I working on?")
4. Observe whether Bob's session returns Alice's information

**Example Reproduction Steps:**
```
1. Open Session A, authenticate as Alice
2. Send: "I'm working on Project Gamma"
3. Open a separate Session B, authenticate as Bob
4. Send: "What project am I working on?"
5. Capture Session B's response verbatim
6. Check memory/cache access logs for the requesting user ID vs. the owner ID of the data returned
```

### Expected Failure State
- Session B (Bob) receives "You're working on Project Gamma" - information that belongs exclusively to Alice's session
- Memory-access logs show a read where the requester's authenticated user ID does not match the memory record's owner ID, with no rejection
- No error or access-denial is raised despite the cross-user boundary violation
- A correctly-behaving system would return no result (or an explicit "no information on file") for Bob rather than leaking Alice's data

---

## Mitigation Strategies

### Prevention
1. **Strict per-session state isolation**: Architect session state (conversation history, working memory, retrieved context) so each session has its own isolated store keyed to a verified session/user ID, with no code path capable of reading another session's state, since the root cause is shared memory or state across sessions combined with improper isolation letting one user's data leak into another's session. Trade-off: full isolation prevents legitimate cross-session features (e.g., "resume where I left off across devices" for the same user) unless explicitly re-architected as same-user, cross-device access rather than shared global state.
2. **Mandatory user authentication before memory access**: Require verified user identity (not just a session token) before any long-term memory or preference lookup, and reject memory reads/writes where the requesting session's authenticated user doesn't match the memory's owner tag, directly closing the vector where "user identification errors" let one user's session retrieve another user's info. Trade-off: adds an authentication dependency to every memory-touching operation, which can add latency or break in degraded-auth scenarios (e.g., anonymous/guest sessions that still expect some personalization).
3. **Cache keying on full session/user identity, not just conversation content**: Ensure any response or state cache is keyed on the combination of user ID and session ID (never on conversation content alone), so a cached response generated for one user's context can never be served to a different user asking a similarly-worded question. Trade-off: reduces cache hit rate and thus increases latency/cost compared to a content-only cache key, since near-identical questions from different users won't share a cache entry.

### Detection & Response
1. **Cross-session data reference monitoring**: Scan agent outputs for references to entities (project names, personal details) that were introduced in a different session than the current one, flagging any match as a potential leak, since the observable symptom is the agent stating information it could only have if session boundaries were violated.
2. **User ID mismatch alerting on memory access**: Log every memory read/write with both the requesting session's authenticated user ID and the memory record's owner ID, and alert immediately on any mismatch, since this is the direct, structural signature of the failure rather than an inferred one.
3. **Session isolation regression testing**: Run scheduled synthetic tests that open two sessions as two distinct test users, have one state a private fact, and verify the other cannot retrieve it, catching isolation regressions introduced by code changes before real users are exposed.

### Architecture Patterns
1. **Per-user memory namespacing with owner-tag enforcement**: Architect long-term memory storage so every entry is tagged with an immutable owner (user ID), and the retrieval layer structurally cannot return entries whose owner tag doesn't match the requesting session's authenticated user — enforced at the data layer, not just the prompt layer, so a prompt-injection or logic bug can't bypass it.
2. **Ephemeral, non-persistent session cache with explicit invalidation**: Architect session-scoped caches (recent turns, working context) to be created fresh per session and explicitly destroyed at session end, rather than a long-lived shared cache keyed loosely enough that stale entries can be served to the wrong session.
3. **Audit-logged memory access layer**: Interpose a dedicated memory-access service between the agent and the memory store that logs every access with requester identity and returns a hard error (not a fallback to default/shared data) on any authorization failure, making cross-session access both harder to trigger accidentally and easier to trace when it happens.

### Metrics
1. **cross_session_reference_rate**: Target: 0 instances of one session's private data appearing in another session; Alert on any detected occurrence
2. **user_id_mismatch_rate**: Target: 0% of memory accesses show requester/owner ID mismatch; Alert on any mismatch, treated as a P1 incident
3. **session_isolation_test_pass_rate**: Target: 100% pass rate on scheduled synthetic isolation tests; Alert on any failure
4. **cache_cross_user_hit_rate**: Target: 0 cache hits served across different authenticated users; Alert on any occurrence

### Alerts
1. **Cross-Session Data Leak Confirmed** (P1): Condition - a memory or cache entry owned by one user is served to a session authenticated as a different user. Action: Immediately invalidate the affected cache/session, notify affected users per privacy policy, freeze the code path pending root-cause fix.
2. **Memory Access Owner Mismatch** (P1): Condition - memory-access audit log shows a read/write where requester user ID doesn't match record owner ID. Action: Block the access, log full context for investigation, review recent deploys touching the memory-access layer.
3. **Session Isolation Regression Test Failure** (P2): Condition - scheduled synthetic isolation test detects one test user's data accessible from another test session. Action: Treat as a release blocker, roll back the most recent change to session/memory handling, re-run tests before allowing further deploys.

---

## References

- [VentureBeat: 88% Enterprises Breached](https://venturebeat.com/security/most-enterprises-cant-stop-stage-three-ai-agent-threats-venturebeat-survey-finds/) - Data exposure across sessions
- [CSA "Autonomous but Not Controlled"](https://cloudsecurityalliance.org/) - 82% unknown agents statistic
