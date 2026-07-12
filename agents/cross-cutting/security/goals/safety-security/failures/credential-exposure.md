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

## Mitigation Strategies

### Prevention
1. **Secret-manager-only credential sourcing, never embedded in prompts or config**: Require every credential the agent's tools need to be fetched at call time from a secret manager rather than embedded in prompts, system messages, or configuration files, since the root cause is that "credentials not properly scoped or protected" and the agent has direct access to secrets it can then surface in a response. Trade-off: every tool integration must be rewritten to call the secret manager rather than reading a local value, adding integration overhead.
2. **Token-based credential isolation instead of raw-secret access**: Give the agent only scoped, revocable tokens (never the underlying raw password/API key) for any operation, so that even the exact failure mode in the example — an error message echoing "password 'Pr0d_P@ss123'" — becomes structurally impossible because the agent process never held the raw password to begin with. Trade-off: requires the target systems (databases, APIs) to support token-based auth rather than static username/password, which isn't always available for legacy systems.
3. **Sanitized error-handling templates for connection/auth failures**: Replace verbose exception pass-through with sanitized error templates that never interpolate the raw connection string or credential into user-facing text, directly preventing the documented example where a database connection failure error included the full "password 'Pr0d_P@ss123' at host db.internal:5432" string. Trade-off: sanitized errors are less useful for the agent's own self-debugging, requiring a separate secure diagnostic channel for legitimate troubleshooting.

### Detection & Response
1. **Credential-pattern regex/entropy scanning on every agent response**: Scan all outbound agent responses for credential-shaped strings (password= patterns, connection-string syntax, high-entropy tokens) and redact or block before delivery, catching leaks like the documented database error even if the sanitization template fails.
2. **Log-sanitization verification with periodic secret-pattern audits**: Regularly audit stored logs (not just live output) for credential patterns that may have slipped through at write time, since "logging not sanitized" is named as a root cause distinct from response-time exposure — logs can leak secrets even when user-facing responses are clean.
3. **Automatic credential rotation triggered on any confirmed exposure**: Wire an automatic rotation pipeline that fires the moment a credential-pattern match is confirmed as a real exposure (not a false positive), minimizing the exposure window since a leaked static credential remains valid and exploitable until explicitly rotated.

### Architecture Patterns
1. **Secret-manager broker sitting between agent and credentialed systems**: Architect a broker service that holds all raw secrets and issues only short-lived, scoped tokens to the agent on demand, so the agent's process memory, context, and logs never contain a raw, long-lived secret capable of the kind of direct exposure shown in the example.
2. **Centralized log-redaction pipeline applied before persistence**: Route all agent and tool logs through a centralized redaction pipeline that strips credential patterns before write, rather than relying on each logging call site to self-sanitize, closing the "logging not sanitized" gap architecturally rather than per-call-site.
3. **Short-lived, automatically-expiring token issuance**: Architect credential issuance so every token has a short TTL and is automatically invalidated after task completion, ensuring that even an undetected leak has a bounded window of usefulness to an attacker.

### Metrics
1. **credential_pattern_leak_rate**: Target: 0 confirmed credential exposures per month across responses and logs; Alert on any confirmed match
2. **raw_secret_agent_access_incidents**: Target: 0 instances of the agent process holding a raw (non-tokenized) secret; Alert on any detected raw-secret access
3. **rotation_time_after_exposure_minutes**: Target: automatic rotation completes within minutes of confirmed exposure; Alert if rotation exceeds the target window
4. **log_redaction_coverage_pct**: Target: 100% of log write paths pass through the centralized redaction pipeline; Alert on any unredacted write path found

### Alerts
1. **Credential Pattern Detected in Response** (P1): Condition - a credential-shaped string is found in agent output before delivery. Action: Block the response, redact and regenerate, trigger rotation of the exposed credential.
2. **Unsanitized Credential Found in Logs** (P1): Condition - a periodic log audit finds a credential pattern that bypassed the redaction pipeline. Action: Purge/redact the log entry, trigger credential rotation, fix the logging call site that bypassed sanitization.
3. **Rotation Not Completed Within SLA** (P2): Condition - automatic rotation following a confirmed exposure has not completed within the target window. Action: Manually force rotation, escalate to the credential owner, investigate the rotation pipeline failure.

## References

## References
- [Check Point: Claude Code RCE & Token Exfiltration](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)
- [SecurityWeek: Claude OAuth Token Theft](https://www.securityweek.com/claude-code-oauth-tokens-can-be-stolen-through-stealthy-mcp-hijacking/)
- [VentureBeat: Comment and Control Attack](https://venturebeat.com/security/ai-agent-runtime-security-system-card-audit-comment-and-control-2026)
