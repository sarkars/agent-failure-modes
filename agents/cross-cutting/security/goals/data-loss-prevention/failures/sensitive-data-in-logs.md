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

**Mitigation Strategies**
1. **Log sanitization**: Redact PII/secrets before logging
2. **Structured logging**: Separate sensitive from non-sensitive fields
3. **Log levels**: Disable debug logging in production
4. **Sampling**: Don't log every request
5. **Retention policies**: Minimize sensitive data retention
6. **Access controls**: Restrict who can view logs

**Detection**
- Scan log storage for PII patterns
- Audit third-party log destinations
- Review trace attributes for sensitive fields
- Monitor log access patterns
- Periodic log content audits

## References

- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [OpenTelemetry Data Security](https://opentelemetry.io/docs/security/)
- [GDPR: Data Minimization](https://gdpr-info.eu/art-5-gdpr/) - Article 5
- [Braintrust: Agent Observability](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026)
