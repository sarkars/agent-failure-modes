# Credential Exposure

## Issue: Agent Leaks API Keys, Passwords, or Tokens

**Frequency**: Common

**Symptoms**
- Credentials appear in agent responses
- API keys logged in plain text
- Tokens passed to untrusted tools
- Credentials stored insecurely

**Root Cause**
- Credentials not properly scoped or protected
- Agent has direct access to secrets
- Error messages include credentials
- Logging not sanitized

**Example**
```
Error handling:
Agent: "I couldn't connect to the database. 
Error: Connection failed for user 'admin' with password 'Pr0d_P@ss123' 
at host db.internal:5432"

Result: Production database credentials exposed
```

**Mitigation Strategies**
1. **Secret managers**: Never embed credentials in prompts
2. **Credential isolation**: Agent uses tokens, not raw secrets
3. **Output sanitization**: Filter credential patterns
4. **Secure logging**: Redact secrets in all logs
5. **Short-lived tokens**: Use temporary, scoped credentials
6. **Rotation on exposure**: Automatic rotation if leak detected

**Detection**
- Scan outputs for credential patterns
- Monitor for secret patterns in logs
- Alert on credential-like strings
- Track credential access patterns
