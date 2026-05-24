# Goal: Tool Reliability

Ensure tools are called correctly, consistently, and with proper error handling. Tool calling failures are among the most common reasons agents fail in production.

## Business Context

- Tool failures break agent workflows completely
- Silent parameter errors corrupt downstream data
- Missing error handling causes cascading failures
- Poor tool design makes agents unreliable

## Failure Patterns

| Failure Pattern | Frequency | Impact |
|-----------------|-----------|--------|
| [Parameter Type Mismatches](failures/parameter-mismatches.md) | Very Common | High |
| [Missing Required Parameters](failures/missing-parameters.md) | Common | High |
| [Wrong Tool Selection](failures/wrong-tool-selection.md) | Common | High |
| [Silent Tool Failures](failures/silent-failures.md) | Common | Critical |
| [Tool Output Misinterpretation](failures/output-misinterpretation.md) | Common | High |
| [Sequencing Errors](failures/sequencing-errors.md) | Common | Medium |
| [Tool Schema Drift](failures/schema-drift.md) | Occasional | High |
| [State-Space Navigation](failures/state-space-navigation.md) | Common | High |
| [Output Processing Errors](failures/output-processing-errors.md) | Common | High |
| [External System Failures](failures/external-system-failures.md) | Common | High |
| [Vague Tool Descriptions](failures/vague-tool-descriptions.md) | Very Common | High |
| [Silent Type Coercion](failures/silent-type-coercion.md) | Very Common | High |
| [Error Information Leakage](failures/error-information-leakage.md) | Common | Medium |
| [Blocking Tool Operations](failures/blocking-tool-operations.md) | Common | High |

## Key Statistics

| Finding | Source |
|---------|--------|
| 37% of tool calls have silent parameter mismatches | Developer Analysis |
| Tool-calling is the #1 failure mode in multi-agent systems | MAST Taxonomy |
| 5 MCP server mistakes waste agent time consistently | Developer report |

## Key Metrics

- Tool call success rate
- Parameter validation failure rate
- Tool selection accuracy
- Mean time to recover from tool failure
