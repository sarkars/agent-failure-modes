# Sensitive Data in Logs

## Issue: PII and Secrets Written to Logs, Traces, and Observability Systems

**Frequency**: Very Common

**Symptoms**
- Full prompts with PII in log files
- API responses with sensitive data logged
- Credentials visible in trace spans
- Debug logs containing customer data
- Observability tools storing unredacted data

**Root Cause**
Agent systems generate extensive logs for debugging, monitoring, and compliance. Without log sanitization, these logs capture everything - including sensitive prompts, responses containing PII, credentials in context, and customer data. Logs often have broader access than production systems and longer retention, amplifying exposure.

**Example**
```
Typical agent log entry (INSECURE):

2026-05-25 14:32:15 INFO  AgentExecutor - Processing request
2026-05-25 14:32:15 DEBUG Prompt: "Look up customer SSN 287-65-4921 
                          and update their address to 123 Main St"
2026-05-25 14:32:16 DEBUG Tool call: database_query
                          params: {"ssn": "287-65-4921"}
2026-05-25 14:32:16 DEBUG Tool response: {"name": "John Smith", 
                          "ssn": "287-65-4921", "dob": "1985-03-15"}
2026-05-25 14:32:17 INFO  Response: "I've updated John Smith's 
                          address. SSN 287-65-4921 confirmed."

Problems:
- SSN logged 4 times
- Full customer record in logs
- Debug logging captured everything
- These logs shipped to Datadog/Splunk

---

Trace span exposure:

span: agent.execute
  attributes:
    prompt: "Transfer $50,000 from account 4532-XXXX-XXXX-7890"
    user.email: "john@company.com"
    response: "Transfer complete. New balance: $125,430"

Problem: OpenTelemetry traces contain financial data
```

**Key Statistics**
From Log Security Research (2026):
- 60%+ of agent logs contain some PII
- Log retention: Often 30-90 days (longer exposure)
- Log access: Typically broader than production
- Third-party logging: Data leaves your infrastructure
- Compliance: Logs rarely covered by data policies

**Sensitive Data in Logs**
| Data Type | Common Locations | Risk |
|-----------|------------------|------|
| Full prompts | Request logs | PII, secrets |
| Tool parameters | Function call logs | Credentials, PII |
| Tool responses | Debug logs | Full data records |
| Agent responses | Response logs | Synthesized PII |
| Context/RAG | Retrieval logs | Document contents |
| Errors | Stack traces | Connection strings |

**Contributing Factors**
- Debug logging left on in production
- No log sanitization layer
- Third-party observability ingesting everything
- "Log everything" culture
- Error messages with full context
- Tracing capturing all span attributes

## Test Scenario & Reproduction

### Scenario Setup
- Deploy an agent with DEBUG-level logging enabled in production, capturing full prompts, tool call parameters, and tool responses via direct calls to the logging framework (no mandatory sanitizing wrapper)
- Logs are shipped to a third-party observability platform (e.g., Datadog/Splunk) with 30-90 day retention and broader internal access than the production database itself
- OpenTelemetry tracing captures full span attributes, including prompt and response text, without sensitivity filtering
- No periodic PII-pattern scanning runs against stored logs

### Trigger Mechanism
1. A user asks the agent to look up a customer's SSN and update their address
2. The agent logs the incoming prompt, the tool call parameters, and the tool response at DEBUG level, each containing the SSN
3. The final agent response (also containing the SSN) is logged and additionally captured as a trace span attribute
4. All of this data ships to the third-party observability platform as part of normal log/trace forwarding

### Example Reproduction Steps
```
1. User: "Look up customer SSN 287-65-4921 and update their address
   to 123 Main St"
2. Logs emitted:
   DEBUG Prompt: "Look up customer SSN 287-65-4921 and update..."
   DEBUG Tool call: database_query params: {"ssn": "287-65-4921"}
   DEBUG Tool response: {"name": "John Smith", "ssn": "287-65-4921", ...}
   INFO  Response: "I've updated John Smith's address. SSN
         287-65-4921 confirmed."
3. Trace span: agent.execute { attributes: { prompt: "...", response: "..." } }
4. Query the third-party log platform for the string "287-65-4921"
   -> 4+ matches across log lines and trace spans, all outside the
   production database's access controls
```

### Expected Failure State
The customer's SSN appears four or more times across logs and trace spans, now stored in a third-party system with broader access and longer retention than the production database, with no redaction applied at any point. A correctly defended system routes all logging through a sanitizing wrapper that redacts SSN-pattern fields at the call site, and defaults production logging to INFO level so DEBUG-level full-payload capture never occurs without explicit, time-limited authorization.

## Mitigation Strategies

### Prevention
1. **Sanitization at the logging call site, not after the fact**: Redact/mask known-sensitive field patterns (SSN, card numbers, credentials) at the point logging statements are written — using a shared, mandatory logging wrapper that all agent code must use — rather than relying on downstream log-storage scrubbing to catch what was already captured verbatim. Trade-off: requires disciplined use of the sanitizing wrapper across the entire codebase, and any code path that logs directly (bypassing the wrapper) reintroduces the risk.
2. **Structured logging with sensitivity-tagged fields**: Use structured log formats where fields are explicitly tagged by sensitivity level, and configure the logging pipeline to strip or redact fields above the destination's authorized sensitivity level before shipping to third-party observability tools, rather than logging free-form strings that mix sensitive and non-sensitive content indistinguishably. Trade-off: requires restructuring logging calls throughout the codebase to use tagged fields instead of interpolated strings.
3. **Debug-level logging disabled by default in production**: Default production logging configuration to INFO level or higher, with DEBUG-level (which the example shows capturing full prompts, tool parameters, and responses) requiring explicit, time-limited, audited enablement rather than being left on as a standing default. Trade-off: reduces the diagnostic detail available for troubleshooting production issues, requiring more deliberate temporary debug-enablement workflows when issues arise.

### Detection & Response
1. **Periodic PII-pattern scanning of log storage**: Regularly scan stored logs (including third-party destinations like Datadog/Splunk) for PII patterns (SSN format, card number format, email addresses) that should have been redacted, catching sanitization gaps in the pipeline before they accumulate across the full retention window.
2. **Trace/span attribute auditing**: Specifically review OpenTelemetry/tracing span attributes for sensitive data, since the example shows financial transaction details and emails landing in trace attributes through a different code path than traditional log statements, requiring separate scrutiny from standard log-content audits.
3. **Third-party log destination compliance auditing**: Audit every third-party service that receives logs (observability platforms, log aggregators) for its own data-handling and retention practices, since sensitive data reaching a third party effectively expands the compliance/exposure boundary beyond internal systems.

### Architecture Patterns
1. **Mandatory sanitizing logging wrapper as the only logging interface**: Architect the codebase so all logging goes through a single, mandatory wrapper library that performs sanitization/redaction, rather than allowing direct use of the underlying logging framework, structurally preventing the "one overlooked log statement" failure pattern.
2. **Sensitivity-tiered log routing**: Route logs to different storage/retention tiers based on their sensitivity tags — non-sensitive operational logs to standard long-retention storage, sensitive-field logs to a restricted-access, short-retention, encrypted store (or excluded from third-party shipping entirely).
3. **Sampling with sensitivity-aware exclusion**: When sampling logs to reduce volume, ensure the sampling logic doesn't inadvertently over-represent sensitive interactions, and apply sanitization uniformly regardless of whether a given request is sampled for detailed logging.

### Metrics
1. **log_sanitization_coverage**: Target: 100% of logging call sites use the mandatory sanitizing wrapper; Alert on any direct/bypassing logging call detected in code review or static analysis
2. **pii_pattern_detection_in_stored_logs**: Target: 0% of stored logs contain unredacted PII patterns; Alert on any detection during periodic scans
3. **debug_logging_production_enablement_duration**: Target: 0 standing DEBUG-level loggers in production; Alert if DEBUG logging is enabled for longer than its authorized time-limited window
4. **third_party_log_destination_compliance_coverage**: Target: 100% of log destinations reviewed and compliant; Alert on any destination lacking a completed compliance review

### Alerts
1. **PII Found in Stored Logs** (P1): Condition - periodic scanning finds unredacted PII in log storage (internal or third-party). Action: Purge/redact the affected log entries where feasible, investigate which logging call site bypassed sanitization, fix the gap.
2. **Standing Debug Logging in Production** (P2): Condition - DEBUG-level logging is found enabled in production beyond its authorized window. Action: Disable immediately, audit what sensitive data may have been captured during the exposure window.
3. **Sensitive Data in Trace Spans** (P1): Condition - audit finds sensitive data (financial details, PII) in tracing/span attributes. Action: Update instrumentation to exclude the sensitive attribute, purge affected spans from trace storage if retention policy allows.

## References

- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [OpenTelemetry Data Security](https://opentelemetry.io/docs/security/)
- [GDPR: Data Minimization](https://gdpr-info.eu/art-5-gdpr/) - Article 5
- [Braintrust: Agent Observability](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026)
