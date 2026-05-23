# Goal: Agentic Orchestration

AI agents that orchestrate document processing introduce new failure modes beyond traditional OCR or even VLM extraction. These failures occur at the orchestration, tool-calling, and reasoning layers.

## Business Context

- Agent reasoning depends on accurate document reading
- Tool selection errors compound extraction failures
- Infinite loops can cause massive cost overruns

## Failure Patterns

| Failure Pattern | Frequency | Impact |
|-----------------|-----------|--------|
| [Document Reading Bottleneck](failures/reading-bottleneck.md) | Very Common | Critical |
| [Conflicting Information](failures/conflicting-information.md) | Common | High |
| [Wrong Tool Selection](failures/wrong-tool-selection.md) | Common | High |
| [Tool Parameter Errors](failures/tool-parameter-errors.md) | Common | High |
| [Infinite Loops](failures/infinite-loops.md) | Occasional | Critical |
| [Error Recovery Errors](failures/error-recovery-errors.md) | Occasional | High |
| [Context Window Limits](failures/context-window-limits.md) | Common | High |
| [Unstructured Documents](failures/unstructured-documents.md) | Common | Medium |

## Key Statistics

| Finding | Source |
|---------|--------|
| Frontier agents score <50% on enterprise document reasoning | Databricks OfficeQA 2026 |
| $47,000 spent on single 11-day agent loop | DEV.to incident report |
| 37% of tool calls have parameter mismatches | Developer analysis |

## Key Metrics

- End-to-end task success rate
- Tool selection accuracy
- Cost per document processed
