# Input Size Not Validated

## Issue
An agent accepts an input payload (a document, a file upload, a JSON body, an attachment) without checking its size against any reasonable bound before processing it, so an unusually large input — whether legitimate, accidental, or adversarial — is loaded fully into memory, tokenized in full, or passed whole into a downstream call, causing memory pressure, request-latency spikes, or costly API usage that a small size check would have caught in microseconds.

**Frequency**: Common

**Symptoms**
- Worker processes hitting memory limits or getting OOM-killed correlated with specific large-input requests
- Request latency for a small fraction of calls spiking orders of magnitude above the median, tracing back to input size
- Token-usage or API-cost spikes from a single oversized document being passed whole into an LLM call
- Timeouts on requests that would otherwise be simple, because the agent attempted to fully load/parse a multi-hundred-megabyte payload first
- No dedicated error path for "input too large" — failures manifest as generic timeouts, OOM crashes, or downstream 500s

## Root Cause
Input-handling code is typically written and tested against realistic, moderately-sized examples, so a size check feels unnecessary during development — the happy-path input is never large enough to expose the gap. Without an explicit, enforced ceiling, the size of accepted input is bounded only by whatever the surrounding infrastructure (a load balancer's body-size limit, a language runtime's memory ceiling) happens to allow, which is usually far larger than any input the business logic can actually process efficiently. The failure mode differs from a normal error because there's no invalid syntax or bad value to reject — the input is entirely well-formed, just too big — so validation logic that only checks structure and content, not size, lets it through cleanly.

## Example
```
A document-summarization agent exposes an endpoint that accepts a
PDF or text file and returns a summary. The handler reads the entire
file into memory before checking its content:

    contents = request.files["document"].read()
    text = extract_text(contents)
    summary = llm_summarize(text)

A user (or a misconfigured automated integration retrying a failed
upload) submits a 2.3 GB log file mistakenly attached instead of the
intended 40 KB PDF report.

The handler reads the full 2.3 GB into memory, extract_text attempts to
process it as a document and spends several minutes churning through it,
and the worker process's memory usage climbs past the container's 4 GB
limit. The container is OOM-killed by the orchestrator mid-request,
taking down the two other requests concurrently being handled by the
same worker. The client sees a generic connection-reset error with no
indication that the actual problem was an oversized upload, and retries,
triggering the same crash again.
```

## Statistics
| Finding | Context |
|---------|---------|
| A significant share of OOM-related worker crashes in document/file-processing agent pipelines trace to a single oversized input rather than aggregate load | Typical range observed in incident postmortems |
| Adding a simple pre-read size check (rejecting inputs above a configured ceiling before full ingestion) prevents the large majority of these incidents | Estimated from the low false-positive cost of reasonable size ceilings |
| Oversized-input incidents disproportionately correlate with retry loops, since the same oversized payload gets resubmitted automatically after each crash | Common pattern in postmortem retry-loop analysis |

## Mitigations
1. **Enforce a size ceiling before full ingestion**: Check `Content-Length` or stream size against a configured maximum before reading the full payload into memory, rejecting oversized inputs with a clear "input too large" error rather than attempting to process them.
2. **Streaming/chunked processing for large legitimate inputs**: For use cases where genuinely large inputs are valid (bulk exports, large document ingestion), process them in bounded chunks rather than loading the entire payload into memory at once.
3. **Separate size tiers with different handling paths**: Route inputs above a "normal" threshold but below a hard maximum to an asynchronous or resource-isolated processing path, so large-but-legitimate inputs don't compete with normal-latency requests on the same worker pool.
4. **Circuit-break retry loops on rejected oversized input**: Ensure "input too large" is a distinct, non-retriable error class communicated clearly to the caller, so automated retry logic doesn't resubmit the same oversized payload repeatedly.
5. **Cost/latency budget checks pre-flight**: For LLM-backed processing specifically, estimate token count from raw size before submission and reject or chunk inputs that would exceed a configured cost or context-window budget.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| oversized_input_rejection_rate | Rate of inputs rejected for exceeding the configured size ceiling | Informational; alert on sudden spike |
| worker_oom_kill_count | Count of worker processes terminated due to memory exhaustion | Alert if > 0 sustained |
| p99_request_latency_by_input_size | Latency distribution bucketed by input size | Alert if large-input bucket latency exceeds SLA by a wide margin |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Worker OOM-killed during input processing | A worker process is terminated for memory exhaustion while processing an input payload | High | Identify the triggering payload, add/tighten size ceiling, isolate affected requests |
| Oversized input rejection spike | oversized_input_rejection_rate exceeds baseline within a rolling window | Medium | Investigate whether a specific client/integration is misconfigured or retry-looping |

## Related Patterns
- [Input Recursion Limit](./input-recursion-limit.md) - a related failure to bound input cost, but along the nesting-depth dimension rather than raw size
- [Output Length Not Enforced](./output-length-not-enforced.md) - the mirror-image failure on the output side, where generated content isn't bounded before being handed to a consumer
- [Output Truncation Silent](./output-truncation-silent.md) - a frequent downstream consequence when an oversized input's output is force-truncated without signaling the caller
