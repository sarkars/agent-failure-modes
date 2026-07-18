# Request Timeout No Graceful Handling

## Issue
Some tools enforce a hard request timeout with no partial-result mechanism: if the operation isn't fully complete when the clock runs out, the connection is simply dropped and any work done up to that point is discarded rather than returned. An agent that issues a single long-running call (a large data export, a bulk transformation, a synchronous report generation) against such a tool loses all progress when the timeout fires, and — because the response is indistinguishable from other connection failures — the agent typically retries the entire operation from scratch rather than recognizing that the work needs to be restructured into smaller, checkpointable steps.

**Frequency**: Common

**Symptoms**
- A long-running call that fails at a suspiciously consistent elapsed time across multiple attempts, matching a fixed timeout rather than variable network conditions
- No partial output, progress indicator, or resumable token returned before the connection drops — full state loss on every timeout
- Agents retrying the identical full-scope operation after a timeout, taking as long or longer on the retry and often timing out again
- Increasing timeout configuration (where the agent controls the client-side timeout) does nothing, because the limit is enforced server-side and independent of client settings
- Jobs that "never complete" in production despite working in smaller-scale testing, because only production data volume pushes the operation past the fixed timeout

## Root Cause
Some tool backends are architected for synchronous request/response with no support for checkpointing, streaming partial results, or resuming an interrupted operation — the entire operation either completes within the connection's lifetime or is entirely rolled back / discarded. This is common for tools built around a single synchronous handler rather than a job-queue or streaming architecture, where adding partial-result support would require significant re-architecture the tool provider hasn't done. Agents that treat "call the tool, wait, get result" as the default interaction pattern have no mechanism to detect that a given tool lacks partial-progress support until they experience total work loss on a timeout, and their generic retry logic — built for transient failures where retrying is genuinely stateless and cheap — is a poor fit for a timeout that represents guaranteed, deterministic failure at the same scope.

## Example
```
An agent kicks off a data-export job via a synchronous
`POST /reports/generate` call against an analytics tool, requesting a
90-day transaction export. The tool has no async job API — the request
must complete within the platform's fixed 30-second request timeout or
the connection is terminated and all generated output is discarded
server-side (the tool does not persist partial exports). For a 90-day
range, report generation takes 47 seconds. The connection is cut at
30 seconds with a generic `ETIMEDOUT`, no partial file, and no resume
token. The agent's retry logic retries the identical 90-day request,
which again takes 47 seconds and again times out at 30. After 3 retries
consuming over 2 minutes of wall-clock time with zero output, the agent
gives up and reports failure, without ever trying the one approach that
would have worked: splitting the 90-day request into three 30-day
requests, each comfortably under the 30-second timeout.
```

## Statistics
| Finding | Context |
|---------|---------|
| Synchronous request/response tools without async job support are common among simpler or older internal APIs, particularly reporting and export tools not originally designed for large-scale use | Common architectural pattern in tools not built with agent-scale usage in mind |
| Timeouts on tools with no partial-result mechanism typically represent 100% work loss, versus streaming or checkpointed tools where a timeout may still yield partial progress | Structural distinction defining this failure mode |
| Consistent failure latency across repeated attempts (matching a fixed timeout value) is a reliable signal that scope reduction, not retrying, is the correct remediation | Based on typical fixed-timeout server behavior |

## Mitigations
1. **Detect fixed-timeout, no-partial-progress tools and scope requests accordingly**: When a tool exhibits this behavior, proactively split large requests into chunks sized to comfortably complete within the known timeout, rather than requesting the full scope and hoping it fits.
2. **Never blindly retry an identical over-scope request**: If a request times out at a consistent elapsed time across attempts, treat that as a deterministic scope problem and reduce scope before retrying, not as a transient failure warranting an unchanged retry.
3. **Prefer async/job-polling variants of a tool when available**: Many platforms offer both a synchronous and an asynchronous (submit-job, poll-status, fetch-result) version of the same operation; default to the async variant for any operation whose duration is data-dependent and potentially large.
4. **Estimate operation duration before submission when possible**: Use available signals (record count, date-range span, a lightweight count/estimate endpoint) to predict whether a request is likely to exceed the known timeout, and pre-emptively chunk if so.
5. **Track and alert on wasted work from repeated full-scope timeouts**: Log elapsed time and requested scope on every timeout so operations that are timing out at full/near-full duration on every attempt are flagged for chunking rather than left to retry indefinitely.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `request.timeout_latency_consistency` | Variance in elapsed time across repeated timeouts for the same operation type | Alert when variance is low and latency matches a known fixed timeout (strong no-graceful-handling signal) |
| `request.identical_scope_retry_count` | Count of retries issued with unchanged request scope after a timeout | Alert if >= 2 |
| `job.total_work_loss_events` | Count of operations where a timeout resulted in zero partial output being retained | Track as a measure of wasted compute/time |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Fixed-timeout total work loss | Timeout at consistent latency with no partial result returned | High | Halt naive retry, reduce request scope/chunk, resubmit |
| Repeated full-scope retry after timeout | Same unchunked request retried 2+ times after timing out | Critical | Disable naive retry path for this tool, require scope-reduction logic before further attempts |

## Related Patterns
- [Total Job Timeout](./total-job-timeout.md) - a related but distinct limit on overall multi-step job duration rather than a single request's hard cutoff
- [Query Planning Timeout](./query-planning-timeout.md) - another timeout variant where the failure mode (no result, no partial progress) looks similar but occurs before execution even begins
- [Backoff Envelope Violation](./backoff-envelope-violation.md) - retrying too aggressively after a timeout compounds wasted work when the tool offers no partial-progress recovery
