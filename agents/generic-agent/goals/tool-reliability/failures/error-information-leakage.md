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

**Mitigation Strategies**
1. **Structured error responses**: Return {error: type, message: safe_msg}
2. **Error categorization**: "database_unavailable" vs raw exception
3. **Actionable guidance**: Include retry_after, fallback suggestions
4. **Sanitize before return**: Strip paths, IPs, credentials
5. **Log internally, summarize externally**: Full trace to logs only
6. **Error enums**: Define known error types AI can reason about

**Detection**
- Search tool responses for file paths (/, \\)
- Check for IP addresses in error responses
- Look for "Traceback" keyword in responses
- Monitor context token usage on error paths

## References

- [5 MCP Server Mistakes](https://dev.to/thedailyagent/5-mcp-server-mistakes-that-waste-your-ai-agents-time-and-how-to-fix-them-18m5) - Mistake #5: Error leakage
- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Information disclosure risks
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) - Sensitive information disclosure
