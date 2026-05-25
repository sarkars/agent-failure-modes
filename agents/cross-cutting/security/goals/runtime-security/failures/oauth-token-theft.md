# OAuth Token Theft

## Issue: AI Agent OAuth Tokens Stolen Through Protocol Hijacking

**Frequency**: Emerging

**Symptoms**
- OAuth tokens exfiltrated without user awareness
- Persistent unauthorized access to connected services
- Silent MCP server hijacking intercepts tokens
- Tokens used for lateral movement across services
- No authentication prompts despite token theft

**Root Cause**
AI agents require OAuth tokens to access external services (GitHub, Google Drive, Slack, etc.). Attackers can hijack the MCP connection between the agent and its tools to intercept OAuth tokens during the authentication flow or extract them from agent memory/context. Once stolen, tokens provide persistent access that survives session termination.

**Example**
```
Claude Code OAuth Token Theft (CVE-2026-21852):

Attack flow:
1. Attacker creates malicious MCP server
2. User connects Claude Code to attacker's server
   (disguised as legitimate tool)

3. When user authenticates to GitHub via Claude:
   - OAuth flow initiates normally
   - Token passes through MCP connection
   - Malicious MCP server intercepts token
   
4. Attacker now has:
   - GitHub OAuth token with user's permissions
   - Access to all repositories user can access
   - Ability to commit code, create PRs, access secrets

5. Persistence:
   - Token remains valid until revoked
   - User unaware of compromise
   - No security alerts triggered

Detection difficulty: "Stealthy" - appears as normal MCP traffic
```

**Key Statistics**
From Security Research (2026):
- CVE-2025-59536: RCE through Claude Code project files
- CVE-2026-21852: API token exfiltration via MCP
- "Silent OAuth token interception" documented (SecurityWeek April 2026)
- Three AI coding agents leaked secrets through single prompt injection
- 61% of AI security incidents involved sensitive data exposure

**Token Theft Vectors**
| Vector | Mechanism | Difficulty |
|--------|-----------|------------|
| MCP hijacking | Intercept OAuth flow | Medium |
| Context extraction | Prompt injection to reveal tokens | Low |
| Memory dump | Access agent memory/state | High |
| Log exposure | Tokens in debug logs | Low |
| Clipboard interception | Copy/paste of tokens | Medium |

**Contributing Factors**
- OAuth tokens passed through agent context
- MCP connections not always authenticated
- Users trust "official-looking" MCP servers
- Tokens stored in accessible memory
- Debug logging includes sensitive data

**Mitigation Strategies**
1. **MCP server verification**: Cryptographic verification of MCP servers
2. **Token isolation**: Never pass tokens through agent context
3. **Short-lived tokens**: Use tokens with minimal TTL
4. **Scope limitation**: Request minimum required OAuth scopes
5. **Token monitoring**: Alert on token usage from new locations
6. **Secure storage**: Use OS keychain, not environment variables

**Detection**
- Monitor OAuth token usage patterns
- Alert on token use from unexpected IPs/locations
- Track MCP server connections
- Audit token scope usage vs. granted scope
- Watch for bulk repository access patterns

## References

- [SecurityWeek: Claude OAuth Token Theft via MCP Hijacking](https://www.securityweek.com/claude-code-oauth-tokens-can-be-stolen-through-stealthy-mcp-hijacking/) - April 2026
- [Check Point: Claude Code RCE & Token Exfiltration](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/) - CVE details
- [VentureBeat: Comment and Control Attack](https://venturebeat.com/security/ai-agent-runtime-security-system-card-audit-comment-and-control-2026) - Three agents leaked secrets
- [Obot: Claude Leak Crisis MCP Security](https://obot.ai/blog/mcp-security-masterclass-claude-leak-crisis/) - Source map leak analysis
