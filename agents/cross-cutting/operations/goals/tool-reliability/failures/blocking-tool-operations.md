# Blocking Tool Operations

## Issue: Slow Tool Calls Block All Other Operations

**Frequency**: Common

**Symptoms**
- Agent becomes unresponsive during slow operations
- Other tools timeout while waiting
- Simple queries take as long as complex ones
- Parallel tool calls execute sequentially
- Client disconnects during long operations

**Root Cause**
MCP servers and tool handlers using synchronous I/O block the entire server while one tool executes. A single slow database query or API call with a 30-second timeout blocks every other tool, causing cascading timeouts and client disconnections even for fast operations.

**Example**
```python
# BAD: Synchronous blocking
import requests

def run_report(report_id: str):
    # This blocks for 30+ seconds
    response = requests.get(f"https://api.internal/reports/{report_id}", 
                           timeout=30)
    return response.json()

def list_products():
    # Fast query, but must wait for run_report to finish
    return db.query("SELECT * FROM products LIMIT 10")

# Timeline when both called:
# 0s:  run_report starts
# 0s:  list_products queued (blocked)
# 30s: run_report finishes
# 30s: list_products finally starts
# 31s: list_products returns

# Client timeout at 10s → both fail

---

# GOOD: Async with connection pooling
import httpx
import asyncio

async def run_report(report_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.internal/reports/{report_id}")
        return response.json()

async def list_products():
    return await db.fetch("SELECT * FROM products LIMIT 10")

# Timeline when both called:
# 0s:  run_report starts (async)
# 0s:  list_products starts (async, concurrent)
# 1s:  list_products returns
# 30s: run_report returns

# Fast operations aren't blocked by slow ones
```

**Key Statistics**
From MCP Server Mistakes Analysis (2026):
- Blocking I/O is #3 most common MCP server mistake
- Default stdio/SSE transports handle one request at a time
- 10-second client timeouts common, 30-second operations fail
- Async I/O improves throughput 5-10x for mixed workloads

**Blocking Patterns**
| Operation | Typical Duration | Blocking Impact |
|-----------|-----------------|-----------------|
| Database query | 10-100ms | Low |
| External API | 1-10s | High |
| Report generation | 10-60s | Critical |
| File processing | 5-30s | High |
| AI model call | 2-20s | High |

**Contributing Factors**
- Default Python I/O is synchronous
- Easy to write blocking code, hard to write async
- Testing with fast operations masks blocking issues
- Single-threaded server architectures
- Tutorials show synchronous examples

## Mitigation Strategies

### Prevention
1. **Migrate to async I/O for all external calls**: Replace synchronous `requests`/blocking DB drivers with `httpx.AsyncClient`, `asyncpg`, etc., so a 30-second report call no longer holds the single-threaded MCP server hostage while a 10-100ms product query waits behind it. Trade-off: async rewrites touch every I/O call site and require re-testing error/cancellation paths that behave differently than sync code.
2. **Route long-running work through a job queue**: For operations like report generation (10-60s) or file processing (5-30s), have the tool enqueue work and immediately return a job ID rather than holding the connection open past typical 10-second client timeouts. Trade-off: the agent must now poll or subscribe for completion, adding a second tool call and more orchestration logic.
3. **Cap concurrent slow operations with a worker pool**: Bound simultaneous AI-model calls or report jobs (e.g., a semaphore of 4-8) so a burst of slow requests can't starve fast ones even under async I/O. Trade-off: legitimate bursts get queued and delayed rather than all running immediately.

### Detection & Response
1. **Per-tool execution time percentiles**: Track p50/p95/p99 execution time per tool; a normally-fast tool (list_products, 10-100ms baseline) whose p95 spikes into seconds signals it's being blocked behind a slow synchronous call sharing the same server thread.
2. **Timeout rate correlated by tool pairing**: Log which tool was executing when a different tool's client-side timeout fired; repeated timeouts on fast tools coinciding with slow-tool execution windows confirms blocking rather than tool-specific failure.
3. **Queue depth under load**: Monitor the server's pending-request queue depth; sustained non-zero depth on a nominally async server indicates a blocking call slipped through (e.g., a sync library invoked from async code).

### Architecture Patterns
1. **Async-first server runtime**: Build the MCP server on an async framework (asyncio/FastAPI+uvicorn) from the start so blocking is the exception; deployment consideration — audit third-party client libraries for hidden sync calls (e.g., a sync boto3 client inside an async handler still blocks the event loop).
2. **Background job + polling pattern**: For 10s+ operations, return `{job_id, status: "running"}` immediately and expose a `check_job_status(job_id)` tool; deployment consideration — requires a job store (Redis/DB) with TTL cleanup so abandoned jobs don't leak.
3. **Bulkhead isolation**: Run slow external-API-bound tools in a separate worker pool or process from fast DB-bound tools so exhaustion in one pool can't starve the other; deployment consideration — adds operational surface (two pools to monitor/scale) but contains blast radius.

### Metrics
1. **tool_p95_latency_ms** (per tool): Target: DB-backed tools < 200ms, external-API tools < 5s; Alert if p95 exceeds 2x its 7-day baseline.
2. **client_timeout_rate**: Target < 0.5% of calls; Alert if > 2% over a 15-minute window.
3. **event_loop_blocked_ms**: Target: 0 sustained blocking on an async server; Alert if any single blocking span exceeds 500ms.
4. **queue_depth**: Target: 0 steady-state; Alert if > 10 pending requests for more than 60 seconds.

### Alerts
1. **Blocking Call Detected** (P1): Condition - event_loop_blocked_ms exceeds 500ms on a server expected to be fully async. Action: page on-call, capture a stack trace via profiler, identify and patch the synchronous call site (common culprits: sync DB driver, sync HTTP client, CPU-bound loop with no yield).
2. **Fast Tool Timeout Spike** (P2): Condition - a normally sub-200ms tool's timeout rate exceeds 2% while a known slow tool executes concurrently. Action: confirm blocking via queue-depth correlation, temporarily cap concurrent slow-tool invocations, file a bug against the blocking call.
3. **Queue Depth Sustained** (P3): Condition - queue_depth > 10 for 5+ minutes. Action: check for a traffic spike vs. a blocking regression; scale the worker pool if traffic-driven, investigate code if not.

## References

- [5 MCP Server Mistakes](https://dev.to/thedailyagent/5-mcp-server-mistakes-that-waste-your-ai-agents-time-and-how-to-fix-them-18m5) - Mistake #3: Blocking calls
- [Aegis: Agent-Environment Failures](https://arxiv.org/abs/2508.19504) - Resource exhaustion patterns
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - System design issues
