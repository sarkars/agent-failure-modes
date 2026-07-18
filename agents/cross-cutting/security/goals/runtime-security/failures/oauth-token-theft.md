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

## Test Scenario & Reproduction

### Scenario Setup
- Deploy an agent (e.g., a coding assistant) that supports connecting to third-party MCP servers for tool access
- No cryptographic verification of MCP server identity is required before initiating an OAuth flow through that connection
- Set up an attacker-controlled MCP server disguised as a legitimate integration (e.g., presented to the user as a GitHub helper tool)
- The agent's OAuth token exchange passes the token through the MCP connection itself rather than a separate, non-agent-visible credential broker

### Trigger Mechanism
1. The user connects the agent to the attacker's disguised MCP server, believing it to be legitimate
2. The user authenticates to GitHub through the normal OAuth flow, which the agent initiates through the compromised MCP connection
3. The malicious MCP server intercepts the OAuth token as it passes through the connection during the handshake
4. The attacker uses the stolen token independently, from their own infrastructure, to access the user's repositories

### Example Reproduction Steps
```
1. User connects agent to "github-helper" MCP server (attacker-controlled)
2. User: "Connect my GitHub account"
3. Agent initiates OAuth flow through the MCP connection
4. Malicious server logs the OAuth callback token before forwarding
   the (spoofed) success response back to the agent
5. From a separate machine: curl -H "Authorization: Bearer <stolen_token>"
   https://api.github.com/user/repos
6. Observe the attacker's request succeeds and returns the user's
   private repository list, with no alert raised on the legitimate
   account
```

### Expected Failure State
The attacker gains a valid, persistent OAuth token usable from their own infrastructure with no authentication prompt or security alert triggered on the user's side, and the token remains valid until manually revoked. A correctly defended system either blocks the OAuth flow from initiating through an unverified MCP server, or issues tokens through a credential broker that never exposes the raw value to the MCP connection layer in the first place.

## Mitigation Strategies

### Prevention
1. **Token isolation from agent context entirely**: Architect the OAuth flow so tokens never pass through or become visible within the agent's LLM context/conversation state — token exchange and storage should happen in a separate, non-LLM-accessible credential broker, since the documented theft vector is interception during passage through the MCP connection and extraction from agent memory/context. Trade-off: requires a more complex credential-broker architecture separating token handling from the conversational agent layer, rather than the simpler (but vulnerable) pattern of tokens flowing through agent-visible state.
2. **Cryptographic MCP server verification before OAuth flow initiation**: Require cryptographic verification of an MCP server's identity before allowing any OAuth authentication flow to proceed through that connection, so a malicious server disguised as a legitimate tool cannot intercept tokens during the handshake. Trade-off: requires a verified-server registry/certificate infrastructure, and users must be prevented from (or warned strongly against) connecting to unverified MCP servers even when convenient.
3. **Short-lived tokens with minimal necessary scope**: Request only the minimum OAuth scopes required for the specific task, and use tokens with the shortest practical TTL, so even a successfully-stolen token provides limited access and expires quickly, rather than a broad, long-lived token granting persistent full-account access. Trade-off: short-lived tokens require more frequent re-authentication, adding friction, and minimal scopes may require re-prompting for additional consent if the task scope expands.

### Detection & Response
1. **Token-usage location/pattern monitoring**: Monitor OAuth token usage for access from unexpected IP addresses, geographic locations, or usage patterns inconsistent with the legitimate user's normal behavior, since stolen tokens are typically used from different infrastructure than the original user, providing a detectable anomaly signal.
2. **Scope-usage-vs-granted-scope auditing**: Audit actual API calls made with a token against the scopes it was granted, flagging any usage pattern suggesting broader access than the task justified (e.g., bulk repository access when the task was a single commit), since this can reveal token misuse even without a location-based anomaly.
3. **MCP server connection tracking with anomaly detection**: Track and log every MCP server connection the agent makes, specifically flagging new/unrecognized servers and connections that coincide with subsequent unusual token usage, to correlate the theft vector back to its originating connection.

### Architecture Patterns
1. **Credential-broker architecture separating tokens from agent context**: Architect a dedicated credential-broker service that handles OAuth flows and token storage entirely outside the LLM's context/memory, exposing only a scoped, audited API for the agent to request specific actions rather than ever holding or seeing the raw token itself.
2. **OS-keychain-backed secure token storage**: Store tokens exclusively in OS-native secure storage (keychain/credential manager), never in environment variables, plaintext config, or anywhere accessible to the agent's context or debug logging, closing off the "context extraction" and "log exposure" theft vectors.
3. **Verified-server-only OAuth flow gating**: Architect the system so OAuth authentication flows can only be initiated through cryptographically-verified MCP server connections, structurally blocking the "malicious server disguised as legitimate tool" attack path at the point of the auth flow itself.

### Metrics
1. **token_usage_location_anomaly_rate**: Target: track as baseline; Alert on any token usage from a new/unexpected location or IP
2. **scope_usage_vs_grant_mismatch_rate**: Target: 0% of token usage exceeds its task-justified scope; Alert on any significant mismatch (e.g., bulk access when single-item access was expected)
3. **token_context_exposure_rate**: Target: 0% of tokens ever appear in agent-visible context or logs; Alert on any detected exposure
4. **unverified_mcp_server_oauth_attempt_rate**: Target: 0 OAuth flows initiated through unverified MCP server connections; Alert on any occurrence

### Alerts
1. **Token Usage Anomaly Detected** (P1): Condition - OAuth token usage occurs from an unexpected location/IP or shows a scope-usage mismatch. Action: Revoke the token immediately, notify the affected user, investigate the connection history for the theft vector.
2. **Token Exposure in Context/Logs** (P1): Condition - a raw OAuth token is found in agent-visible context or log output. Action: Revoke the exposed token immediately, treat as a confirmed incident, fix the architectural gap that allowed context/log exposure.
3. **OAuth Flow via Unverified MCP Server** (P1): Condition - an OAuth authentication flow is initiated through an MCP server that failed or lacks cryptographic verification. Action: Block the flow, warn the user, investigate the server's legitimacy before allowing any future connection.

## References

- [SecurityWeek: Claude OAuth Token Theft via MCP Hijacking](https://www.securityweek.com/claude-code-oauth-tokens-can-be-stolen-through-stealthy-mcp-hijacking/) - April 2026
- [Check Point: Claude Code RCE & Token Exfiltration](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/) - CVE details
- [VentureBeat: Comment and Control Attack](https://venturebeat.com/security/ai-agent-runtime-security-system-card-audit-comment-and-control-2026) - Three agents leaked secrets
- [Obot: Claude Leak Crisis MCP Security](https://obot.ai/blog/mcp-security-masterclass-claude-leak-crisis/) - Source map leak analysis
