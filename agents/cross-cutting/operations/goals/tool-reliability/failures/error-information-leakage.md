# Error Information Leakage

## Issue: Raw Errors Expose Internal Details and Waste Context

**Frequency**: Common

**Symptoms**
- Full stack traces returned to AI agent
- Internal file paths exposed in error messages
- Connection strings and credentials leaked
- AI context window filled with useless traceback
- Agent can't reason about error cause

**Root Cause**
When tools fail, unhandled exceptions propagate raw tracebacks to the AI client. This wastes context tokens on information the AI can't use, leaks sensitive internal details (paths, versions, credentials), and gives the AI no structured information about what went wrong or how to recover.

**Example**
```python
# BAD: Raw exception propagation
def get_customer(customer_id: str):
    return db.query(f"SELECT * FROM customers WHERE id = {customer_id}")

# When database is down, AI receives:
"""
Traceback (most recent call last):
  File "/app/tools/customer.py", line 42, in get_customer
    return db.query(f"SELECT * FROM customers WHERE id = {customer_id}")
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/base.py", line 1412, in execute
    return meth(self, multiparams, params)
  File "/usr/local/lib/python3.11/site-packages/sqlalchemy/engine/default.py", line 536, in do_execute
    cursor.execute(statement, parameters)
psycopg2.OperationalError: could not connect to server: Connection refused
    Is the server running on host "db.internal.company.com" (10.0.1.42) and accepting
    TCP/IP connections on port 5432?
"""

# Problems:
# - 50+ lines of traceback waste context tokens
# - Leaked: internal hostname, IP address, port
# - AI can't reason about what to do next

---

# GOOD: Structured error response
def get_customer(customer_id: str):
    try:
        return db.query(...)
    except OperationalError:
        return {
            "error": "database_unavailable",
            "message": "Customer database temporarily unavailable",
            "retry_after_seconds": 30,
            "fallback": "Ask user to try again shortly"
        }

# AI receives actionable, structured error
# No internal details leaked
# Context preserved for reasoning
```

**Key Statistics**
From MCP Server Mistakes Analysis (2026):
- Error leakage is #5 most common MCP server mistake
- Average stack trace: 40-60 lines, 500-1000 tokens wasted
- Leaked information found in 73% of unhandled tool errors
- Structured errors improve agent recovery rate by 3x

**Leakage Types**
- **File paths**: Internal directory structure exposed
- **Hostnames**: Internal service names and IPs
- **Credentials**: Connection strings, API keys in errors
- **Library versions**: Vulnerability information
- **Business logic**: Internal table names, field names

**Contributing Factors**
- Development-style error handling in production
- No distinction between human and AI error consumers
- Try/except blocks that re-raise without sanitization
- Logging that prints full exceptions
- Framework default error handlers

---

## Test Scenario & Reproduction

### Scenario Setup
- A tool (e.g., `get_customer`) has no try/except boundary around its database/API call
- No sanitization or error-translation middleware sits between the raw exception and the AI-facing response
- No response scanning for traceback/path/credential patterns

### Trigger Mechanism
1. Force the underlying dependency (database, API) to fail (stop the service, block the port, revoke credentials)
2. Call the tool as the agent normally would
3. Inspect the returned response for raw traceback text, internal hostnames, or credentials

**Example Reproduction Steps:**
```
1. Stop or block the test database the get_customer tool depends on
2. Call get_customer(customer_id="test_123") through the agent
3. Capture the full raw response returned to the agent
4. Scan the response for "Traceback", file paths, hostnames/IPs, or connection-string patterns
5. Measure: token count of the error response vs. the ~20-50 token structured-error baseline
```

### Expected Failure State
- Response contains a multi-line stack trace with internal file paths and hostname/IP
- No structured `{error, message, retry_after_seconds}` payload was returned instead
- The response consumes hundreds of context tokens instead of a compact structured error

---

## Mitigation Strategies

### Prevention
1. **Catch at the tool boundary, never let exceptions propagate raw**: Wrap every tool implementation in a try/except that converts internal exceptions (like the `OperationalError` from a downed Postgres connection) into a structured `{error: "database_unavailable", message, retry_after_seconds}` payload before it reaches the AI. Trade-off: requires an explicit mapping from every internal exception type to a safe external error code, which is ongoing maintenance as new failure modes appear.
2. **Sanitize before return, not after**: Strip hostnames, IPs, file paths, and connection strings from any text that could reach the response — don't rely on remembering to redact case-by-case, since the example shows a leaked internal hostname (`db.internal.company.com`) and IP (`10.0.1.42`) in a single unhandled traceback. Trade-off: aggressive sanitization can also strip legitimately useful debugging context the AI needs to self-correct (e.g., which field was invalid).
3. **Define a closed set of AI-facing error enums**: Limit tool errors to a known vocabulary (`database_unavailable`, `rate_limited`, `invalid_input`, `not_found`) instead of forwarding whatever exception class the underlying library raised, so the AI can pattern-match and choose a recovery path instead of parsing prose. Trade-off: novel failure modes not yet mapped to an enum fall back to a generic "unknown_error" until someone adds a case.

### Detection & Response
1. **Traceback keyword scan on tool responses**: Grep outgoing tool responses for `"Traceback"`, `File "`, or stack-frame patterns; any match means an unhandled exception leaked past the sanitization layer, exactly the 40-60 line dumps described in the root cause.
2. **Sensitive-pattern scan**: Regex-scan responses for IPv4 addresses, `/`-or-`\`-delimited absolute paths, and common credential patterns (`postgres://`, `Bearer `, API key prefixes); a hit indicates the exact leakage class this failure mode describes.
3. **Context-token cost on error paths**: Track average response token count specifically on error-returning calls; since a full traceback wastes 500-1000 tokens per the cited stats, error responses averaging near that size (vs. the ~20-50 tokens of a structured error) signal unsanitized leakage.

### Architecture Patterns
1. **Error-translation middleware layer**: Centralize exception-to-structured-error mapping in one middleware/decorator applied to every tool, rather than per-tool try/except blocks, so sanitization can't be forgotten on a new tool; deployment consideration — a single shared layer becomes a single point that must handle every exception class thrown anywhere in the tool surface.
2. **Dual-channel logging**: Send full unredacted tracebacks to an internal log/observability system (Sentry, Datadog) for human debugging while the AI-facing channel only ever sees the sanitized enum-based error; deployment consideration — requires correlating an internal trace ID between the two channels so on-call engineers can find the full context from a sanitized error report.
3. **Circuit breaker on the failing dependency**: When the same underlying error (e.g., `database_unavailable`) recurs repeatedly, trip a circuit breaker that short-circuits to the structured error immediately instead of re-attempting the call and re-generating a fresh traceback each time; deployment consideration — needs a reset/half-open policy so the tool recovers automatically once the dependency is healthy again.

### Metrics
1. **leaked_error_rate**: Target < 0.1% of error responses containing a sanitization-scan hit (path, IP, or "Traceback"); Alert if > 1% over a 1-hour window.
2. **avg_error_response_tokens**: Target < 100 tokens per structured error response; Alert if average exceeds 300 tokens (indicates raw tracebacks slipping through).
3. **unmapped_exception_rate**: Target < 1% of tool errors falling through to a generic/unknown enum; Alert if > 5% over 24 hours (signals missing exception mappings).
4. **agent_recovery_rate_on_error**: Target > 70% of tool errors followed by a sensible agent recovery action (retry, fallback, user notification) rather than a stalled or nonsensical response; Alert if it drops below 50%.

### Alerts
1. **Raw Traceback Leaked** (P1): Condition - a tool response matches the traceback/path/IP sanitization scan. Action: page the owning team, patch the specific tool's exception handling immediately, treat as a potential credential-exposure incident and check whether any leaked value was sensitive.
2. **Error Sanitization Coverage Gap** (P2): Condition - unmapped_exception_rate exceeds 5% for a given tool over 24 hours. Action: review logs for the specific exception classes falling through, add explicit mappings to the error-translation layer.
3. **Elevated Error Token Cost** (P3): Condition - avg_error_response_tokens exceeds 300 for a tool. Action: audit that tool's error path for missed sanitization or verbose default exception formatting.

## References

- [5 MCP Server Mistakes](https://dev.to/thedailyagent/5-mcp-server-mistakes-that-waste-your-ai-agents-time-and-how-to-fix-them-18m5) - Mistake #5: Error leakage
- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Information disclosure risks
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) - Sensitive information disclosure
