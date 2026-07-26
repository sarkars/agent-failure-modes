# Cost Optimization

Agentic planning, learning, and architecture-level cost waste — distinct from [Cost Efficiency](../cost-efficiency/)'s execution-level patterns (batching, retries, model routing). This goal covers failures where a known cost-optimization technique (plan reuse, prompt caching, adaptive ensembling, negative caching, compression) exists but isn't applied, or is applied incorrectly.

## Failure Patterns

| Pattern |
|---------|
| [Unnecessary Planning Step](failures/unnecessary-planning-step.md) |
| [No Preplanned Workflow for Frequent Operations](failures/no-preplanned-workflow-for-frequent-operations.md) |
| [Non-Generalized Plan Template](failures/non-generalized-plan-template.md) |
| [Under-Planning Costly Rework](failures/under-planning-costly-rework.md) |
| [Repeated Regeneration of Known-Incorrect Answer](failures/repeated-regeneration-of-known-incorrect-answer.md) |
| [Redundant Self-Reflection Passes](failures/redundant-self-reflection-passes.md) |
| [Unbounded Context Growth Across Turns](failures/unbounded-context-growth-across-turns.md) |
| [Prompt Caching Underutilization](failures/prompt-caching-underutilization.md) |
| [Multi-Agent Context Broadcast Waste](failures/multi-agent-context-broadcast-waste.md) |
| [Unnecessary Ensemble Voting Overhead](failures/unnecessary-ensemble-voting-overhead.md) |
| [Full Reprocessing on Incremental Change](failures/full-reprocessing-on-incremental-change.md) |
| [Prompt Compression Not Applied](failures/prompt-compression-not-applied.md) |
| [Missing Task Specialization](failures/missing-task-specialization.md) |

**Total: 13 patterns**
