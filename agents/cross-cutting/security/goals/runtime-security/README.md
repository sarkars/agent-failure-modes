# What Are the Most Common Runtime Security Failures in AI Agents?

**Runtime security fails when attacks targeting agent execution at inference time—injection, exploitation, credential theft, tool-level compromise—succeed because runtime defenses are incomplete or misconfigured.** An MCP protocol message queue lacks authentication and an attacker injects malicious tool definitions that agents execute without verification, an agent processing untrusted user input in its context window does not isolate context from reasoning and leaks sensitive data from prior sessions mixed into context, and OAuth tokens used by agents are exfiltrated via side-channels or stored in memory without proper lifecycle management. Runtime security failures matter precisely because they occur during inference, not training: a model can pass all training-time security checks and still execute attacker-controlled code at runtime if the agent's runtime environment is compromised.

## Key Takeaways

- 8 patterns cover runtime security, grouped into four mechanisms: context/environment poisoning, malicious tool injection, protocol exploitation, and credential/session compromise.
- Tool-execution and protocol-exploitation patterns are rated Common: attackers compromise tool-definition channels or protocol implementations and inject malicious tools/commands that agents execute without independent verification.
- Credential compromise (OAuth token theft, session hijacking, credential exposure in memory) is rated Common in production and often discovered only via incident response, not through normal monitoring.
- Runtime defenses require layered verification: tool-definition authentication (verify tool definitions before execution), input isolation (sandbox untrusted context separately from trusted reasoning), token lifecycle management (generate short-lived tokens, rotate frequently, never store long-lived credentials in memory).

## Scope

- **Context/Environment Poisoning** — Untrusted input in agent context (user messages, retrieved documents) contains malicious instructions that agent reasoning executes because context is not isolated from reasoning.
- **Malicious Tool Injection** — Attackers compromise tool-definition channels, protocol implementations, or dependency sources and inject malicious tool definitions that agents execute without verification.
- **Protocol Exploitation** — Agents communicate via protocols (MCP, custom agent-to-tool protocols) that lack authentication, encryption, or input validation, enabling attackers to intercept and manipulate communication.
- **Credential and Session Compromise** — Agents store credentials in memory, use long-lived tokens, or fail to rotate session tokens, enabling token-theft attacks and session hijacking.

## When Runtime Security Matters

- Agents process untrusted input (user queries, retrieved documents, data from external sources) in their context and must execute reasoning without executing untrusted instructions.
- Agents invoke external tools via protocols, and tool-definition sources are not authenticated or are subject to compromise.
- Agents use credentials (API keys, OAuth tokens, database passwords) to access external services and must protect credentials from in-memory exposure and long-term token risk.

## Cross-Pattern Insight

Effective runtime security in agent systems requires distinguishing defenses that work at design-time (tool-contract verification, protocol design) versus defenses that must work at runtime (credential rotation, input isolation, runtime tool verification). The shared lesson is that runtime environment trust cannot be assumed: agents running in shared infrastructure, with untrusted input, accessing external tools via unverified channels face multiple exploit vectors that training-time security checks do not address. The solution requires layered, runtime-specific defenses: isolate untrusted input from trusted reasoning (sandboxing), verify tool definitions before execution (signed tools), rotate credentials frequently (short-lived tokens), and monitor runtime behavior for exfiltration attempts (detect when agents suddenly access unusual credentials or invoke unusual tools).

## Frequently Asked Questions

### How do you prevent context-window poisoning when agent context naturally contains untrusted input?
Context isolation is required: separate untrusted input (user messages, retrieved documents) from trusted context (system prompts, agent instructions) using format markers, XML tags, or structural boundaries that reasoning cannot cross. Require explicit agent reasoning that says "user-provided input is untrusted" before executing instructions from untrusted input. Use adversarial testing: provide injected instructions in user input and verify agents do not execute injected commands.

### Can tool sandboxing prevent malicious-tool-injection if tool-definition channels are compromised?
Tool sandboxing limits damage an invoked tool can cause, but it does not prevent the agent from invoking a malicious tool. Defense against injection requires: (1) tool-definition authentication (sign tool definitions with trusted authority, verify signatures before loading), (2) tool-definition audit logging (log every tool definition change and review unusual changes), (3) runtime tool verification (before first invocation, verify tool definition matches audit trail). If tool definitions are untrusted, sandboxing is insufficient without upstream verification.

### How do you manage OAuth tokens securely in agents that need to access multiple services?
Never store long-lived tokens in agent memory or state. Instead: (1) generate short-lived access tokens (15-30 minutes expiry), (2) store refresh tokens in secure, out-of-process storage (key vault, credential manager), (3) implement token refresh automatically when access token approaches expiry, (4) audit token-usage patterns and alert on unusual token access. This ensures token compromise is time-limited and detected quickly.

### What's the fastest way to detect session hijacking if agents share infrastructure?
Monitor for session-anomaly patterns: one session suddenly accessing data normally accessed by different session, one session accessing unusual services, unusual token usage patterns. Implement per-session isolation (each session gets separate memory/storage), audit all cross-session data access, and alert on any session accessing data from prior sessions. Session-isolation by design is more robust than post-hoc detection.

## Patterns

| Pattern | Mechanism | Frequency |
|---|---|---|
| [Context Window Poisoning](failures/context-window-poisoning.md) | Untrusted context contains malicious instructions agent executes | Common |
| [Cross Tenant Leakage](failures/cross-tenant-leakage.md) | One agent's context leaks into another agent's execution | Occasional |
| [Malicious Tool Injection](failures/malicious-tool-injection.md) | Attacker injects malicious tool definitions into tool registry | Common |
| [MCP Protocol Exploitation](failures/mcp-protocol-exploitation.md) | Unauthenticated MCP protocol enables command injection | Common |
| [OAuth Token Theft](failures/oauth-token-theft.md) | Attackers steal OAuth tokens via side-channels or memory access | Occasional |
| [Runtime Credential Exposure](failures/runtime-credential-exposure.md) | Credentials exposed in memory, logs, or error messages at runtime | Common |
| [Session Hijacking](failures/session-hijacking.md) | Attacker hijacks agent session or impersonates authorized session | Occasional |
| [Tool Execution RCE](failures/tool-execution-rce.md) | Tool execution vulnerabilities enable remote code execution on agent host | Occasional |

**Total: 8 patterns**

## Related Goals

- [Agent Trust](../agent-trust/) — runtime attacks (poison, tool injection, credential theft) often depend on compromised agents being trusted by downstream agents.
- [Tool Authorization Limits](../tool-authorization-limits/) — controls which tools agents can invoke; runtime-security verifies tool definitions before execution.
- [Data Loss Prevention](../data-loss-prevention/) — runtime attacks often attempt to exfiltrate data via compromised tools or protocol channels; runtime security prevents exfiltration at the tool/protocol boundary.
