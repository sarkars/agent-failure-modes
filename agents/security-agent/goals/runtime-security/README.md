# Goal: Agent Runtime Security

Prevent exploitation of AI agents during execution. Runtime security failures occur when agents are actively running and can be exploited through protocol vulnerabilities, tool manipulation, or environmental attacks.

## Business Context

- MCP and tool protocols create new attack surfaces
- Runtime exploits can achieve RCE through AI agents
- Token and credential theft enables persistent access
- Cross-tenant attacks expose multiple customers
- Supply chain compromises propagate through AI integrations

## Failure Patterns

| Failure Pattern | Frequency | Impact |
|-----------------|-----------|--------|
| [MCP Protocol Exploitation](failures/mcp-protocol-exploitation.md) | Emerging | Critical |
| [OAuth Token Theft](failures/oauth-token-theft.md) | Emerging | Critical |
| [Tool Execution RCE](failures/tool-execution-rce.md) | Occasional | Critical |
| [Cross-Tenant Data Leakage](failures/cross-tenant-leakage.md) | Occasional | Critical |
| [Agent Session Hijacking](failures/session-hijacking.md) | Occasional | Critical |
| [Malicious Tool Injection](failures/malicious-tool-injection.md) | Emerging | Critical |
| [Context Window Poisoning](failures/context-window-poisoning.md) | Common | High |
| [Runtime Credential Exposure](failures/runtime-credential-exposure.md) | Common | Critical |

## Key Statistics

| Finding | Source |
|---------|--------|
| MCP vulnerability affects 200,000+ servers | OX Security April 2026 |
| 88% of enterprises reported AI agent security incidents | VentureBeat/Kiteworks 2026 |
| 61% of incidents involved sensitive data exposure | CSA Report April 2026 |
| 82% discovered unknown AI agents in past year | CSA "Autonomous but Not Controlled" |
| Three AI coding agents leaked secrets via single prompt injection | VentureBeat Comment & Control 2026 |

## Key Metrics

- Runtime exploit detection rate
- Token theft incident count
- Mean time to detect agent compromise
- Cross-tenant isolation violations
- Unauthorized tool execution attempts
