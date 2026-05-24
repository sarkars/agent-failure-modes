# Generic Agent

This section documents failure patterns that apply to **any AI agent** regardless of domain. These cross-cutting concerns affect code agents, customer service agents, RAG agents, and every other agent type.

Use this as a checklist when building or evaluating any agent system.

## Goals

| Goal | Description | Failure Patterns |
|------|-------------|------------------|
| [Cost Efficiency](goals/cost-efficiency/) | Minimize token usage and API costs | 9 patterns |
| [Tool Reliability](goals/tool-reliability/) | Ensure tools are called correctly and consistently | 14 patterns |
| [Output Accuracy](goals/output-accuracy/) | Eliminate hallucinations and ensure grounded outputs | 11 patterns |
| [Context Management](goals/context-management/) | Handle context windows, memory, and state effectively | 7 patterns |
| [Safety & Security](goals/safety-security/) | Prevent prompt injection, data leakage, and unauthorized actions | 19 patterns |
| [Reasoning Quality](goals/reasoning-quality/) | Ensure sound planning, self-correction, and goal adherence | 12 patterns |
| [Multi-Agent Coordination](goals/multi-agent-coordination/) | Ensure agents work together effectively | 5 patterns |
| [Agent Runtime Security](goals/agent-runtime-security/) | Prevent exploitation during agent execution | 8 patterns |

## Structure

```
generic-agent/
├── README.md
└── goals/
    ├── cost-efficiency/
    │   ├── README.md
    │   └── failures/
    │       ├── infinite-loops.md
    │       ├── token-explosion.md
    │       └── ...
    ├── tool-reliability/
    ├── output-accuracy/
    ├── context-management/
    ├── safety-security/
    ├── reasoning-quality/
    ├── multi-agent-coordination/
    └── agent-runtime-security/
```

## Key Statistics (2026)

| Finding | Source |
|---------|--------|
| Multi-agent systems fail at 41-86.7% rates | MAST Taxonomy |
| 37% of tool calls have silent parameter mismatches | Developer Analysis |
| 88% of enterprises reported AI agent security incidents | VentureBeat/Kiteworks 2026 |
| 45% of AI-generated code has security vulnerabilities | Veracode 2026 |
| 52% of enterprise AI responses contain fabrications | Enterprise Survey 2026 |
| $47,000 spent on single 11-day agent loop | DEV.to incident report |
| MCP vulnerability affects 200,000+ servers | OX Security April 2026 |
| Three AI coding agents leaked secrets via single injection | VentureBeat 2026 |

## How to Use

1. **Review each goal** - Understand what "success" looks like
2. **Check failure patterns** - See if your agent exhibits these symptoms
3. **Apply mitigations** - Implement suggested fixes
4. **Monitor in production** - Track metrics to catch regressions

## Cross-References

Many failures documented here also appear in domain-specific agent sections with additional context:
- OCR Agent: [Agentic Orchestration](../ocr-agent/goals/agentic-orchestration/)
- Workflow Agent: [Error Recovery](../workflow-agent/)
- RAG Agent: [Answer Synthesis](../rag-agent/)
