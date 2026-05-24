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

**Mitigation Strategies**
1. **Use async I/O**: asyncio, httpx, asyncpg for all external calls
2. **Connection pooling**: Reuse connections instead of creating new ones
3. **Timeout management**: Set appropriate timeouts per operation type
4. **Background processing**: Queue long operations, return job ID
5. **Progress reporting**: Stream updates for long operations
6. **Concurrent limits**: Cap parallel operations to prevent overload

**Detection**
- Monitor tool execution times
- Track timeout rates by tool
- Measure queue depth under load
- Profile blocking time vs. execution time

## References

- [5 MCP Server Mistakes](https://dev.to/thedailyagent/5-mcp-server-mistakes-that-waste-your-ai-agents-time-and-how-to-fix-them-18m5) - Mistake #3: Blocking calls
- [Aegis: Agent-Environment Failures](https://arxiv.org/abs/2508.19504) - Resource exhaustion patterns
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - System design issues
