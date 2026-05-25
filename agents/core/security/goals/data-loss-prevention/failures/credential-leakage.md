# Credential Leakage

## Issue: Agent Exposes API Keys, Passwords, or Secrets in Output

**Frequency**: Common

**Symptoms**
- API keys appear in agent responses
- Database connection strings exposed
- Passwords or tokens in code suggestions
- Cloud credentials in configuration examples
- Internal URLs with embedded auth tokens

**Root Cause**
Agents often have access to codebases, configuration files, or documentation containing credentials. When asked about configuration, debugging, or code examples, the agent may include real credentials. Code generation agents are particularly prone to copying credential patterns from training data or context.

**Example**
```
User: "How do I configure the database connection?"

Agent response:
"Here's how to configure the database connection:

```python
import psycopg2

conn = psycopg2.connect(
    host='prod-db.company.internal',
    database='customers',
    user='admin',
    password='Pr0d_Db_P@ss2024!'  # <-- REAL CREDENTIAL
)
```

Make sure to set the host to your database endpoint..."

---

Another example (code completion):

User: "Complete this AWS config"

Agent: "
aws_access_key_id = AKIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
region = us-west-2
"

Problem: Agent generated what looks like example keys
         but pattern matches real AWS credential format
```

**Key Statistics**
From Credential Exposure Research (2026):
- 45% of AI-generated code contains security issues
- GitHub scans find 2M+ secrets annually in public repos
- AI coding agents leaked secrets via single injection (2026)
- Average time to exploit exposed credential: <1 hour
- Cost of credential breach: $4.5M average

**Credential Types at Risk**
| Type | Pattern | Impact |
|------|---------|--------|
| AWS Keys | AKIA... | Cloud takeover |
| GitHub Tokens | ghp_... | Code access |
| API Keys | Various | Service abuse |
| Database passwords | Connection strings | Data breach |
| JWT Secrets | Base64 strings | Auth bypass |
| Private Keys | -----BEGIN RSA----- | Full compromise |

**Contributing Factors**
- Credentials in codebase accessible to agent
- Training data containing real credentials
- Code completion from context with secrets
- Configuration file access without filtering
- No secret detection on outputs
- Environment variable values exposed

**Mitigation Strategies**
1. **Secret scanning**: Scan all outputs for credential patterns
2. **Input sanitization**: Remove credentials from context before agent sees it
3. **Placeholder patterns**: Train agent to use `<API_KEY>` placeholders
4. **Vault integration**: Credentials never in plain text
5. **Pre-commit hooks**: Catch credentials before they're added to context
6. **Real-time blocking**: Block output if credential detected

**Detection**
- Pattern matching: AWS keys, GitHub tokens, etc.
- Entropy analysis: High-entropy strings
- Known secret patterns database
- Comparison against internal credential stores
- Monitor for connection strings, URLs with auth

## References

- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning) - Pattern detection
- [Gitleaks](https://github.com/gitleaks/gitleaks) - Secret detection tool
- [VentureBeat: AI Agents Leaked Secrets](https://venturebeat.com/security/ai-agent-runtime-security-system-card-audit-comment-and-control-2026)
- [TruffleHog](https://github.com/trufflesecurity/trufflehog) - Credential scanning
