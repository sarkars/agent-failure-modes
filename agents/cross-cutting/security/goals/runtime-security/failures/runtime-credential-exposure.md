# Runtime Credential Exposure

## Issue: Agent Exposes Credentials During Normal Operation

**Frequency**: Common

**Symptoms**
- API keys appear in agent responses
- Credentials logged in debug output
- Environment variables leaked through tool calls
- Secrets included in generated code
- Connection strings exposed in error messages

**Root Cause**
AI agents operate with access to credentials for tool authentication, API access, and system integration. During normal operation, these credentials can be exposed through various channels: the agent may include them in responses, log them during debugging, pass them to untrusted tools, or generate code that hardcodes secrets. Unlike traditional applications, agents may not understand what constitutes sensitive data.

**Example**
```
Multiple Credential Exposure Vectors:

Vector 1 - Direct exposure in response:
User: "What's my database connection configured as?"
Agent: "Your database is configured with:
        host: db.prod.company.com
        user: admin
        password: Pr0d$ecret123  ← Exposed
        port: 5432"

Vector 2 - Code generation exposure:
User: "Write a script to call our API"
Agent generates:
  import requests
  API_KEY = "sk-prod-abc123xyz"  ← Hardcoded secret
  response = requests.get(url, headers={"Authorization": API_KEY})

Vector 3 - Tool call exposure:
Agent calls external tool with full environment:
  debug_tool(context={
    "env": {
      "AWS_SECRET_ACCESS_KEY": "...",  ← Passed to tool
      "DATABASE_URL": "postgres://user:pass@..."
    }
  })

Vector 4 - Error message exposure:
Tool fails, returns:
  "Connection failed: mysql://root:admin123@10.0.1.5:3306/prod"
Agent includes full error in response to user
```

**Key Statistics**
From Security Research (2026):
- Three AI coding agents leaked secrets through single prompt injection
- 45% of AI-generated code has security vulnerabilities (Veracode)
- Environment variable exfiltration documented in CVE-2026-21852
- Comment and Control attack specifically targeted credentials
- 61% of AI security incidents involved sensitive data exposure

**Exposure Vectors**
| Vector | Cause | Risk Level |
|--------|-------|------------|
| Direct response | Agent doesn't recognize secrets | High |
| Generated code | Hardcoded credentials | Critical |
| Tool parameters | Passing env to tools | Critical |
| Error messages | Verbose error handling | High |
| Debug logging | Development settings in prod | High |
| Memory dumps | Crash reports with context | Medium |

**Contributing Factors**
- Agents don't inherently understand secret sensitivity
- Environment variables accessible to agent process
- Tools receive full context by default
- Error messages not sanitized
- Debug logging left enabled
- No secret detection in outputs

## Mitigation Strategies

### Prevention
1. **Reference-based credential injection instead of raw-value access**: Give the agent process references/handles to credentials (e.g., a secret-manager lookup key) that are resolved by a separate runtime layer at the point of use, never exposing the raw value to the agent's context, since the root cause is that credentials sit directly in agent-accessible environment/context and the agent cannot distinguish them from any other string. Trade-off: requires rearchitecting how tools receive configuration, and any tool that genuinely needs the raw secret (e.g., to build a connection string) needs a trusted resolution boundary outside the LLM loop.
2. **Environment variable minimization per agent process**: Launch each agent process with only the specific environment variables its current task requires, rather than inheriting the full production environment, so vectors like "debug_tool(context={env: {...}})" have nothing broad to leak even if a tool call exposes its full context. Trade-off: requires per-task environment scoping infrastructure and breaks the convenience of a single shared environment for all agent operations.
3. **Template-based error handling that excludes interpolated secrets**: Build error-message templates that reference credential fields symbolically (e.g., "connection to {host} failed") rather than interpolating the live connection string/exception text, since the documented Vector 4 shows raw exceptions like "mysql://root:admin123@..." flowing straight from a tool failure into the user-facing response. Trade-off: sanitized error templates convey less diagnostic detail, slowing legitimate debugging unless a separate secure channel carries the full error to operators.

### Detection & Response
1. **Regex/entropy-based output scanning before delivery**: Scan every agent response and generated code block for credential-shaped patterns (API key prefixes, high-entropy strings, connection-string syntax) before it reaches the user, and block or redact matches, catching Vector 1 (direct exposure) and Vector 2 (hardcoded secrets in generated code) at the last line of defense.
2. **Tool-call parameter auditing for environment payloads**: Inspect outbound tool-call parameters for embedded environment variables or secret-shaped values (as in the `debug_tool` example) and block calls that pass full environment context to a tool that didn't request it, since Vector 3 shows tools receiving the full context by default.
3. **Debug-logging-in-production drift detection**: Continuously verify that debug/verbose logging configuration matches the intended environment (dev vs. prod) and alert when production logging levels are found in verbose mode, since the contributing factor list explicitly names "debug logging left enabled" as a persistent gap.

### Architecture Patterns
1. **Secret-manager-backed credential broker**: Route all credential access through a dedicated secret-manager service (Vault, AWS Secrets Manager, etc.) that issues short-lived, scoped tokens on request, so no long-lived secret ever needs to live in an environment variable or config file the agent process can read.
2. **Sandboxed tool execution with explicit context allowlisting**: Run tools in a sandbox that receives only an explicitly allowlisted subset of context/environment per call, structurally preventing the "tools receive full context by default" contributing factor from ever surfacing a secret to a tool that doesn't need it.
3. **Output-sanitization gateway between agent and user/tool boundary**: Insert a mandatory sanitization gateway that all agent output (responses, generated code, error text) passes through before crossing any trust boundary, centralizing secret redaction rather than relying on each generation path to self-censor.

### Metrics
1. **credential_pattern_detection_rate**: Target: 0 confirmed credential leaks per month in delivered outputs; Alert on any regex/entropy match that passes the sanitization gateway
2. **full_env_tool_call_rate**: Target: 0% of tool calls pass unscoped environment/context objects; Alert on any tool call containing more than its allowlisted parameters
3. **prod_debug_logging_incidents**: Target: 0 production services running debug-level logging; Alert immediately on any detected drift
4. **secret_manager_coverage_pct**: Target: 100% of credentials sourced from the secret manager rather than env vars/config files; Alert on any new credential introduced outside the broker

### Alerts
1. **Credential Detected in Agent Output** (P1): Condition - the output-sanitization scan matches a credential pattern in a response or generated code block. Action: Block delivery of the output, redact and regenerate, rotate the exposed credential if it reached the user.
2. **Unscoped Environment Passed to Tool** (P2): Condition - a tool call includes environment/context data beyond its declared allowlist. Action: Block the call, log the offending tool integration, review its input-handling code for the missing scoping.
3. **Verbose Error Exposed Raw Credentials** (P1): Condition - an error message forwarded to the user contains connection-string or credential syntax. Action: Suppress the message, rotate the exposed credential immediately, replace the error path with a sanitized template.

## References

## References

- [VentureBeat: Comment and Control Attack](https://venturebeat.com/security/ai-agent-runtime-security-system-card-audit-comment-and-control-2026) - Credential exfiltration
- [Check Point: Claude Code CVE-2025-59536](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/) - Token exfiltration
- [Veracode 2026](https://www.veracode.com/) - 45% AI code has vulnerabilities
- [GitHub Discussion: AI Security Headaches 2026](https://github.com/orgs/community/discussions/194034) - Community-reported issues
