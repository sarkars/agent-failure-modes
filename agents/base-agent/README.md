# Base Agent

This section documents **cross-cutting failure patterns** that apply to any AI agent regardless of domain. These foundational patterns affect code agents, customer service agents, RAG agents, and every other agent type.

Use these as a checklist when building or evaluating any agent system.

## Agent Categories

| Agent | Description | Goals | Patterns |
|-------|-------------|-------|----------|
| [Security Agent](security-agent/) | Security, trust, runtime protection | 3 | 35 |
| [Accuracy Agent](accuracy-agent/) | Output correctness, anti-hallucination | 3 | 30 |
| [Operations Agent](operations-agent/) | Tools, cost, coordination, traceability, human oversight | 5 | 44 |

**Total: 109 patterns across 11 goals**

## Structure

```
base-agent/
├── README.md
├── security-agent/
│   └── goals/
│       ├── safety-security/        (19 patterns)
│       ├── runtime-security/       (8 patterns)
│       └── agent-trust/            (8 patterns)
│
├── accuracy-agent/
│   └── goals/
│       ├── output-accuracy/        (11 patterns)
│       ├── reasoning-quality/      (12 patterns)
│       └── context-management/     (7 patterns)
│
└── operations-agent/
    └── goals/
        ├── tool-reliability/       (14 patterns)
        ├── cost-efficiency/        (9 patterns)
        ├── multi-agent-coordination/ (5 patterns)
        ├── traceability/           (8 patterns)
        └── human-oversight-reliability/ (8 patterns)
```

## How to Use

1. **Start with Security** - Review security patterns first for any agent handling sensitive data
2. **Check Accuracy** - Ensure your agent doesn't hallucinate or drift from goals
3. **Optimize Operations** - Improve tool reliability and cost efficiency
4. **Apply to Domain Agents** - These patterns complement domain-specific agents (OCR, RAG, etc.)

## Key Statistics (2026)

| Finding | Source |
|---------|--------|
| 88% of enterprises reported AI agent security incidents | VentureBeat/Kiteworks 2026 |
| 52% of enterprise AI responses contain fabrications | Enterprise Survey 2026 |
| 37% of tool calls have silent parameter mismatches | Developer Analysis |
| Multi-agent systems fail at 41-86.7% rates | MAST Taxonomy |
| $47,000 spent on single 11-day agent loop | DEV.to incident report |
