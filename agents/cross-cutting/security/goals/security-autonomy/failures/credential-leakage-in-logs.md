# Credential Leakage in Logs

## Issue: API Keys, Passwords, Tokens Exposed in Logs or Error Messages

**Frequency**: Occasional

**Symptoms**
- API keys visible in log files
- Database passwords in error messages
- OAuth tokens in debug output
- Credentials in exception stack traces
- Log files accessible to unauthorized users
- Credentials exposed in monitoring dashboards

**Root Cause**
When agents call external APIs or databases, they often pass credentials (API keys, passwords, tokens) in requests. Unfiltered logging captures these credentials, and they persist in logs, debug output, error messages, and monitoring systems. Attackers who gain access to logs can extract credentials and compromise external services.

**Example**
```
Agent code:
response = api_client.call(
    api_key="sk_live_abc123xyz789",  # Real API key
    endpoint="/users",
    params={"id": user_id}
)

Error occurs:
"API call failed: POST https://api.service.com/users?api_key=sk_live_abc123xyz789"

Log output:
2026-07-13 10:30:45 ERROR: API call failed with exception
Traceback: ...
  response = api_client.call(api_key="sk_live_abc123xyz789", endpoint="/users", ...)

Result: API key exposed in logs
Impact: Attacker with log access can use the key to make API calls as the agent
```

**Key Statistics**
- 60-80% of breaches involved exposed credentials in logs
- Average time from exposure to exploitation: <24 hours
- Cost of compromised API key: $5K-500K (depends on key's privilege)
- Logs are often less protected than the systems they monitor

**Contributing Factors**
- No credential redaction in logging
- Credentials in error messages/stack traces
- Logging of full request/response bodies
- Log retention policies too long
- Insufficient log access controls

---

## Test Scenario & Reproduction

### Scenario Setup
- Agent makes API calls with credentials (keys, tokens, passwords)
- Logging is unfiltered
- Error handling logs full context
- Logs are stored/accessible

### Trigger Mechanism
1. Inject failure into API call (timeout, unauthorized, rate limit)
2. Observe: Does error message include credentials?
3. Check logs: Are credentials visible?

**Example Reproduction Steps:**
```
1. Set up agent that calls external API with API key
2. Trigger API failure (return 401 error)
3. Observe error message and logs
4. Search logs: "api_key=", "Authorization:", "password="
5. Measure: % of logs containing credentials
6. Verify: Are logs protected from unauthorized access?
```

### Expected Failure State
- Credentials logged in plain text
- Error messages include full request (with credentials)
- Stack traces show credentials
- Logs accessible to multiple people
- No redaction or masking

---

## Mitigation Strategies

### Prevention

1. **Automatic Credential Redaction in Logging Framework**: Implement logging middleware that redacts common credential patterns (API keys, bearer tokens, basic auth, passwords). Pattern: "api_key=***REDACTED***". Make this automatic, not optional.

2. **Environment Variable for Credentials, Not Hardcoded**: Load credentials from environment variables or secure vaults (AWS Secrets Manager, HashiCorp Vault), not from code. This prevents them from being logged in the first place.

3. **Structured Logging with Credential-Aware Fields**: Use structured logging where sensitive fields are explicitly marked and automatically redacted. Example: `log.error("API call failed", api_key=REDACTED, endpoint="/users")`.

### Detection & Response

1. **Log Scanning for Credentials**: Regularly scan logs for exposed credentials using pattern matching (regex for API key formats, JWT structure). Alert on any matches.

2. **Credential Rotation Monitoring**: If credentials are detected in logs, trigger automatic rotation of that credential in the external service.

3. **Access Control Audits on Logs**: Verify who has access to logs. Restrict to only necessary personnel. Revoke access when credentials compromised.

### Architecture Patterns

1. **Secret Management Integration**: Use cloud secret managers (AWS Secrets Manager, Azure Key Vault) for all credentials. Agents retrieve credentials at runtime, never store in code/config.

2. **Request/Response Redaction Layer**: Wrap API client calls with redaction layer that removes credentials before logging. Example:
   ```
   def log_request(request):
       sanitized = redact_sensitive_fields(request)
       logger.info("API request", request=sanitized)
   ```

3. **Structured Logging with Sensitive Field Tagging**: Mark fields as sensitive; logging framework automatically redacts them.

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `exposed_credentials_in_logs_count` | Number of credentials found in logs | >0 |
| `credential_redaction_coverage` | % of sensitive fields redacted | >99% |
| `log_access_violations` | Unauthorized access attempts to logs | >0 |
| `credential_rotation_time` | Time to rotate compromised credential | >1 hour |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Credential Exposed in Logs | API key, token, or password found in logs | P1 | Immediately rotate credential; investigate source |
| Redaction Bypass | Sensitive field not redacted | P1 | Fix redaction logic; audit recent logs |
| Unauthorized Log Access | User accessing logs without permission | P1 | Revoke access; investigate intent |
| Credential Compromise Detected | Compromised credential used outside normal patterns | P1 | Revoke immediately; incident response |

---

## References

- [OWASP: Sensitive Data Exposure](https://owasp.org/www-project-top-10/2021/A02_2021-Cryptographic_Failures/) — Credential exposure risks
- [CWE-532: Insertion of Sensitive Information into Log File](https://cwe.mitre.org/data/definitions/532.html) — Technical guidance
- [AWS Secrets Manager Best Practices](https://docs.aws.amazon.com/secretsmanager/) — Secret management patterns
