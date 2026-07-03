# Model Denial Of Service

## Issue: Input causes excessive cost/latency or service exhaustion.

**Frequency**: Common

**Symptoms**
- Long context/tool loops; resource spikes.
- Model token consumption exceeds expected budget by 5-10x (e.g., 100K tokens for typical task that uses 10K).
- Agent enters infinite retry loop or repeats same tool call 50+ times.
- Request latency increases from normal 2-5s to 60+ seconds.
- CPU/memory/token quota exhausted; rate limiter triggers on legitimate requests from other users.
- Model output repeatedly regenerates the same failed request or loops through variations of same action.

**Root Cause**
Input causes excessive cost/latency or service exhaustion.

**Example**
```
Scenario 1 (Adversarial Input):
Setup:
- Search agent has no token limit or depth limit on tool use.
- Attacker submits query: "Find all variations of 'explain quantum computing' in the database."

Attack:
Model enters loop:
1. Call search_database("explain quantum computing") → 50,000 results
2. Model tries to summarize all results (context overflows)
3. Model calls search again with broader query
4. Generates 200,000+ token response trying to list/summarize
5. Request times out after consuming 500K tokens, blocking other users

Impact:
- $50+ in API costs for one request
- Other users' requests queued and delayed
- Service degradation or brief outage
- Attacker can repeat for continued DoS

Scenario 2 (Unintended Loop):
Agent tries to fetch user profile. API returns error.
Agent retries 50 times with slightly different prompts, each retry consuming context.
No exponential backoff or retry limit enforced.
```

**Contributing Factors**
- No per-request token budget or hard limit on model.generate() calls.
- No max depth or iteration count on tool loops (agent can call tools indefinitely).
- Adversarial user input designed to trigger broad queries (e.g., "find everything", "list all users").
- Tool responses can be very large (entire database dumps) with no pagination or size limits.
- Model not trained to recognize when to stop iterating or ask for clarification.
- Retry logic uses simple exponential backoff without jitter or max attempts.
- No request-level rate limiting or per-user quota per time window.
- Verbose logging or tracing that adds token overhead.

---


## Test Scenario & Reproduction

### Scenario Setup
- Agent calls language model for processing
- No input validation or length limits
- Attacker can provide arbitrarily long input
- Model processing has no timeout

### Trigger Mechanism
```
1. Attacker provides extremely long input (1M+ tokens)
2. Agent forwards to model API
3. Model processing consumes excessive compute
4. API rate limits or timeouts triggered
5. Service unavailable for legitimate users
```

### Expected Failure State
- Model processing times out or fails
- High compute/memory consumption
- Service unavailable or degraded
- Multiple requests cascade into complete DoS

### Mitigation Validation Protocol
**Test Checklist:**
- [ ] Reproduce: Long input causes timeout/failure
- [ ] Apply mitigations (input limits, rate limiting)
- [ ] Re-run with clamped input → processes normally
- [ ] Test under load with legitimate users

**Success Criteria:**
- Input length limits enforced
- Rate limiting prevents DoS
- Service remains responsive under attack

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **Per-request token budget**: Set hard cap on total tokens used per request (e.g., 50K max). Abort gracefully if exceeded with user-facing message.
2. **Tool loop depth limit**: Limit agent tool call depth to max 10-20 iterations per request. Warn user if limit approaching.
3. **Tool response pagination**: Add pagination to all data-returning tools. Cap single response to max 10 records/5K tokens. Require explicit "next page" request.
4. **Timeout per tool call**: Kill any tool call taking >30 seconds. Log as potential DoS and skip to next action.
5. **User-level rate limiting**: Implement token quota per user per hour/day (e.g., 1M tokens/day). Reject requests that exceed quota.
6. **Query complexity heuristics**: Detect overly broad queries ("find all", "list everything", wildcard patterns). Route to human or simplify automatically.
7. **Exponential backoff + jitter**: Implement retry logic with max 3 retries, jitter to avoid thundering herd.

### Detection
- Long context/tool loops; resource spikes.

### Recovery
**Immediate (Stop the Attack)**
1. Identify the request ID causing high token usage from logs.
2. Kill the request and associated agent process.
3. If attack is sustained, throttle or block the source IP/user account temporarily.
4. Alert on-call team to monitor for similar patterns.

**Investigation (Understand Scope)**
1. Extract the malicious query/input that triggered the loop.
2. Review agent's tool call sequence: identify which tool or which query parameter caused explosion.
3. Correlate request rate with API cost spike. Calculate total blast radius.
4. Determine if this is targeted attack (specific user/query) or algorithmic bug.
5. Check model response logs for evidence of infinite reasoning (repeated thoughts, same conclusions).

**Remediation (Prevent Recurrence)**
1. Implement token budget and depth limits (see Prevention).
2. Add the malicious query pattern to a blocklist for real-time detection.
3. Retrain or fine-tune model to recognize and abort complex queries gracefully.
4. Add query complexity scoring to ingest pipeline; route high-complexity queries to simpler logic path.
5. Update tool contract documentation to clarify pagination and max response size.
6. Conduct chaos engineering test: inject adversarial queries and verify budget enforcement works.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [OWASP-LLM-Top10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- Note: LLM application risks including prompt injection, insecure output handling, supply chain, sensitive information disclosure, excessive agency.
