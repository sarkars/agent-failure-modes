# Security Agent

This section documents **security-focused failure patterns** for AI agents. These patterns cover prompt injection, data leakage, runtime exploitation, and trust vulnerabilities that affect any agent handling sensitive data or performing privileged actions.

Use this as a security checklist when building or auditing agent systems.

## Goals

| Goal | Description | Failure Patterns |
|------|-------------|------------------|
| [Safety & Security](goals/safety-security/) | Prevent prompt injection, data leakage, and unauthorized actions | 19 patterns |
| [Runtime Security](goals/runtime-security/) | Prevent exploitation during agent execution (MCP, tokens, RCE) | 8 patterns |
| [Agent Trust](goals/agent-trust/) | Establish and verify trust between agents | 8 patterns |
| [Data Loss Prevention](goals/data-loss-prevention/) | Prevent sensitive data exposure through outputs, logs, and tools | 8 patterns |

## Structure

```
security-agent/
├── README.md
└── goals/
    ├── safety-security/
    │   ├── README.md
    │   └── failures/
    │       ├── prompt-injection.md
    │       ├── data-leakage.md
    │       └── ...
    ├── runtime-security/
    │   └── failures/
    │       ├── mcp-protocol-exploitation.md
    │       ├── oauth-token-theft.md
    │       └── ...
    ├── agent-trust/
    │   └── failures/
    │       ├── agent-impersonation.md
    │       ├── blind-delegation.md
    │       └── ...
    └── data-loss-prevention/
        └── failures/
            ├── pii-exposure.md
            ├── credential-leakage.md
            └── ...
```

## Key Statistics (2026)

| Finding | Source |
|---------|--------|
| 88% of enterprises reported AI agent security incidents | VentureBeat/Kiteworks 2026 |
| 61% of incidents involved sensitive data exposure | CSA Report April 2026 |
| 45% of AI-generated code has security vulnerabilities | Veracode 2026 |
| MCP vulnerability affects 200,000+ servers | OX Security April 2026 |
| Three AI coding agents leaked secrets via single injection | VentureBeat 2026 |
| 82% discovered unknown AI agents in past year | CSA Report |

## How to Use

1. **Review each goal** - Understand what "secure" looks like
2. **Check failure patterns** - See if your agent exhibits these vulnerabilities
3. **Apply mitigations** - Implement suggested security controls
4. **Audit regularly** - Security posture degrades without maintenance

## Cross-References

- [Accuracy Agent](../accuracy-agent/) - Output correctness and reasoning
- [Operations Agent](../operations-agent/) - Tool reliability and cost
- [RAG Agent](../../rag-agent/) - Retrieval-specific security concerns
