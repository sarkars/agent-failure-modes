# Data Leakage

## Issue: Agent Exposes Sensitive Information

**Frequency**: Common

**Symptoms**
- Private data appears in responses
- Training data leaked through outputs
- User A's data shared with User B
- Internal information exposed externally

**Root Cause**
- No data classification or access controls
- Agent trained on or has access to sensitive data
- Output not filtered for sensitive content
- Session isolation failures

**Example**
```
User: "Show me an example customer record"

Agent: "Here's an example:
Name: John Smith
SSN: 123-45-6789
Address: 123 Main St..."

Result: Real customer PII exposed as "example"
```

**Real Incidents**
- 61% of AI agent security incidents involved sensitive data exposure
- Samsung employees leaked confidential code via ChatGPT
- Customer service bots exposing other customers' data

**Mitigation Strategies**
1. **Data classification**: Tag and track sensitive data
2. **Access controls**: Enforce who can access what
3. **Output filtering**: Detect and redact sensitive patterns
4. **Synthetic examples**: Use fake data for demonstrations
5. **Session isolation**: Strict boundaries between users
6. **Audit logging**: Track all data access

**Detection**
- Pattern matching for PII, credentials, etc.
- DLP (Data Loss Prevention) integration
- Monitor for cross-user data access
- Alert on sensitive data in outputs
