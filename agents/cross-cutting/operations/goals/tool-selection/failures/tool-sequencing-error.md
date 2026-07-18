# Tool Sequencing Error

## Issue: Agent calls write tool before reading/verifying current state.

**Frequency**: Common

**Symptoms**
- Update/delete/send precedes read/confirm.
- [Add more specific symptoms]

**Root Cause**
Agent calls write tool before reading/verifying current state.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

## Test Scenario & Reproduction

### Scenario Setup
- Deploy an agent with a `update_inventory_count` write tool and a `get_inventory_count` read tool, with no state-aware gateway enforcing a read-before-write invariant
- No version/ETag token is required on write calls, so the write tool accepts any count value regardless of whether the agent has current information
- The inventory count for a specific SKU changed (via a separate process) between the start of the agent's session and the moment it issues a write

### Trigger Mechanism
1. The agent is asked to decrement inventory for a SKU after a sale, and proceeds directly to the write tool using a count value it remembers from earlier in a long session
2. No read call precedes this specific write within the current turn
3. The write succeeds, overwriting the current (already-changed) inventory count with a stale-derived value
4. The actual inventory count is now incorrect, having been calculated from outdated information

### Example Reproduction Steps
```
1. Early in session: agent reads inventory for SKU-42 -> count: 100
   (10:00:00)
2. Separately, another process sells 5 units, updating count to 95
   (10:05:00, not observed by the agent)
3. At 10:10:00, agent is asked to record a new sale of 3 units for
   SKU-42, and calls: update_inventory_count(sku="SKU-42", count=97)
   -- calculated as 100-3, using the stale 10:00:00 read, with no
   fresh read call in this turn
4. Actual correct count should be 95-3=92, but the write sets it to 97
5. Check tool-call trace for a read_inventory_count call immediately
   preceding this write -> none present within the staleness window
```

### Expected Failure State
The inventory count is silently corrupted to an incorrect value (97 instead of 92) because the agent wrote based on a stale read from 10 minutes earlier rather than verifying current state immediately before the write, with no error surfaced anywhere. A correctly defended system requires a version/ETag token from a read taken within a defined staleness window immediately before the write, rejecting the write attempt (or forcing a fresh read) since the stale 10:00:00 read's version token no longer matches current state.

## Mitigation Strategies

### Prevention
1. **Read-Before-Write Invariant Enforcement**: The tool gateway tracks, per resource identifier, whether a read/verification call occurred earlier in the current session. Write, update, delete, and send calls targeting a resource with no preceding read in the session's tool-call history are rejected outright, forcing the agent through a verify step it cannot skip.
2. **Version/ETag-Bound Writes**: Every write call must carry a version token or ETag obtained from the most recent read of that resource. The backend rejects writes whose token doesn't match current state, which both enforces sequencing and catches the case where the state changed between read and write (stale-read races).
3. **Staleness Window on Read-Write Pairing**: Even when a read occurred, require it to be within a configured recency window (e.g., last 2 turns or N seconds) relative to the write; a read from early in a long session is treated as stale and a fresh read is forced before the write proceeds.

### Detection & Response
1. **Sequence Pattern Analyzer**: Continuously scan tool-call traces for write/delete/send actions that lack a preceding read/get/list call on the same resource within the session; flag violations for immediate review, since this is the direct signature of the failure mode.
2. **Stale-State Write Detector**: Compare the timestamp of the last read against the timestamp of the write and against any known external change events (webhooks, audit logs) on the resource; if the resource changed between read and write and the agent didn't re-verify, flag as a stale write.
3. **Post-Hoc Intended-vs-Actual Diff**: After a write completes, diff the agent's stated intent (from its reasoning trace) against the actual resulting state; mismatches indicate the agent acted on an outdated mental model of the resource.

### Architecture Patterns
1. **State-Aware Tool Gateway**: A gateway service sits in front of all write-capable tools and maintains a per-resource read/write history for the active session, enforcing the read-before-write invariant and rejecting non-compliant calls with a clear corrective error the agent can act on.
2. **Optimistic Concurrency Control**: Require ETag/version tokens on all write APIs, sourced from the immediately preceding read, so sequencing violations and race conditions are caught by the backend itself rather than relying solely on agent discipline.
3. **Transactional Read-Verify-Write Wrapper**: Expose write operations to the agent only through a composite tool that internally performs read, diff-against-intent, confirm, then write as a single atomic unit — removing the possibility of the agent skipping the read step because there is no standalone "write" tool to call.

### Metrics
1. **read_before_write_compliance_rate**: Target: 100%; Alert threshold: < 99.5%
2. **stale_write_rate**: Target: < 0.5% of writes; Alert threshold: > 2%
3. **version_mismatch_rejection_count**: Target: tracked baseline; Alert threshold: sudden increase indicating race conditions or gateway bypass
4. **write_rollback_rate**: Target: < 1%; Alert threshold: > 3%

### Alerts
1. **Write Without Preceding Read** (P1 - Critical): Condition - gateway detects (or, worse, a bypass allows) a write/delete/send call with no prior read on the resource in-session. Action: Block the call, alert on-call, audit gateway enforcement config for the bypass path.
2. **Version/ETag Mismatch on Write** (P1 - Critical): Condition - write rejected due to stale version token, indicating the agent acted on outdated state. Action: Force fresh read-and-retry flow, log for stale-write trend analysis.
3. **Rising Stale-Write Trend** (P2 - Warning): Condition - stale_write_rate trending upward over a rolling week. Action: Review staleness window configuration, check for high-concurrency resources needing shorter windows.

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
