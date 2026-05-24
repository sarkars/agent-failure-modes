# Accuracy Agent

This section documents **accuracy and correctness failure patterns** for AI agents. These patterns cover hallucination, reasoning errors, and context management issues that cause agents to produce incorrect, fabricated, or misleading outputs.

Use this as a quality checklist when building agents that must be factually correct.

## Goals

| Goal | Description | Failure Patterns |
|------|-------------|------------------|
| [Output Accuracy](goals/output-accuracy/) | Eliminate hallucinations and ensure grounded outputs | 11 patterns |
| [Reasoning Quality](goals/reasoning-quality/) | Ensure sound planning, self-correction, and goal adherence | 12 patterns |
| [Context Management](goals/context-management/) | Handle context windows, memory, and state effectively | 7 patterns |
| [Evaluation Reliability](goals/evaluation-reliability/) | Ensure golden datasets and evals reflect real performance | 8 patterns |

## Structure

```
accuracy-agent/
├── README.md
└── goals/
    ├── output-accuracy/
    │   ├── README.md
    │   └── failures/
    │       ├── confident-fabrication.md
    │       ├── entity-confusion.md
    │       └── ...
    ├── reasoning-quality/
    │   └── failures/
    │       ├── goal-drift.md
    │       ├── sycophancy.md
    │       └── ...
    ├── context-management/
    │   └── failures/
    │       ├── context-overflow.md
    │       ├── instruction-drift.md
    │       └── ...
    └── evaluation-reliability/
        └── failures/
            ├── golden-data-staleness.md
            ├── distribution-shift.md
            └── ...
```

## Key Statistics (2026)

| Finding | Source |
|---------|--------|
| 52% of enterprise AI responses contain fabrications | Enterprise Survey 2026 |
| Legal RAG tools hallucinate 17-33% | Stanford Study |
| Only 29% of developers trust AI output accuracy | Industry Survey |
| Multi-agent systems fail at 41-86.7% rates | MAST Taxonomy |
| 40% of agentic AI projects will be scrapped by 2027 | Gartner |
| 83% of RAG systems fail on production cases despite benchmarks | RAGAS Study |
| Eval-production gap: 15-40% performance drop common | MLOps Research |

## How to Use

1. **Review each goal** - Understand what "accurate" looks like
2. **Check failure patterns** - See if your agent exhibits these issues
3. **Apply mitigations** - Implement verification and grounding
4. **Monitor in production** - Track accuracy metrics continuously

## Cross-References

- [Security Agent](../security-agent/) - Security vulnerabilities
- [Operations Agent](../operations-agent/) - Tool reliability and cost
- [RAG Agent](../../rag-agent/) - Retrieval-specific accuracy issues
