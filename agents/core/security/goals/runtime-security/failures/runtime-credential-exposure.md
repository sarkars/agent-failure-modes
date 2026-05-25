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

**Mitigation Strategies**
1. **Secret detection**: Scan agent outputs for credential patterns
2. **Environment isolation**: Minimal env vars accessible to agent
3. **Secret managers**: Use vaults, not env vars or config files
4. **Output sanitization**: Redact secrets before returning responses
5. **Tool sandboxing**: Tools can't access process environment
6. **Audit logging**: Track all credential access

**Detection**
- Regex scanning of agent outputs for secret patterns
- Monitor for high-entropy strings in responses
- Track environment variable access
- Alert on credential patterns in generated code
- Audit tool calls for sensitive parameters

## References

- [VentureBeat: Comment and Control Attack](https://venturebeat.com/security/ai-agent-runtime-security-system-card-audit-comment-and-control-2026) - Credential exfiltration
- [Check Point: Claude Code CVE-2025-59536](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/) - Token exfiltration
- [Veracode 2026](https://www.veracode.com/) - 45% AI code has vulnerabilities
- [GitHub Discussion: AI Security Headaches 2026](https://github.com/orgs/community/discussions/194034) - Community-reported issues
