# AI Agent Cost Optimization Failures: Missing Plan Reuse, Prompt Caching, and Compression

**Cost optimization failures happen when a known technique for cutting agent cost exists but is not applied, or is applied wrong: prompt caching, plan reuse, compression, incremental updates, or right-sizing the model.** These 13 patterns cover planning, learning, and architecture-level waste, as distinct from the execution-level patterns in [cost efficiency](../cost-efficiency/).

## Key Takeaways

- Several patterns are about not reusing work: plans, stable prompt prefixes, and previous answers.
- Others are about doing too much: unneeded planning, reflection, or ensemble voting for simple tasks.
- Under-planning is also costly: skipping planning on a task that needed it causes failed attempts and rework.
- Multi-agent systems add their own waste, such as broadcasting full context to every sub-agent.

## Patterns

| Pattern | What goes wrong |
|---|---|
| [Full Reprocessing on Incremental Change](failures/full-reprocessing-on-incremental-change.md) | A Small Edit to a Source Document Triggers Full Re-Embedding/Re-Analysis of the Entire Document Instead of an Incremental Update to Just the Changed Portion |
| [Missing Task Specialization](failures/missing-task-specialization.md) | Agent stays on generic frontier-model prompting for a high-volume, narrow, repetitive task long after fine-tuning or distillation would outperform it on both cost and… |
| [Multi-Agent Context Broadcast Waste](failures/multi-agent-context-broadcast-waste.md) | A Coordinator Broadcasts Full Shared Context/History to Every Sub-Agent Regardless of Relevance, Multiplying Token Cost by Agent Count |
| [No Preplanned Workflow for Frequent Operations](failures/no-preplanned-workflow-for-frequent-operations.md) | Agent Re-Derives an Identical Multi-Step Plan From Scratch for Every Occurrence of a Routine, Frequently-Repeated Operation |
| [Non-Generalized Plan Template](failures/non-generalized-plan-template.md) | Agent's "Reused" Plans Are Not Actually Parameterized, So Near-Identical Requests Still Trigger Full Re-Planning Instead of a Template Substitution |
| [Prompt Caching Underutilization](failures/prompt-caching-underutilization.md) | A Stable Prompt Prefix (System Prompt, Tool Schemas, Few-Shot Examples) Is Retransmitted and Rebilled at Full Price on Every Call Instead of Using Available… |
| [Prompt Compression Not Applied](failures/prompt-compression-not-applied.md) | Verbose but Relevant Prompt Content Is Sent Uncompressed at Full Token Cost When Established Compression Techniques Would Preserve Meaning at a Fraction of the Length |
| [Redundant Self-Reflection Passes](failures/redundant-self-reflection-passes.md) | Agent Runs Multiple Self-Critique/Verification Calls by Default, Regardless of Whether the Task Actually Benefits From Them |
| [Repeated Regeneration of Known-Incorrect Answer](failures/repeated-regeneration-of-known-incorrect-answer.md) | Agent Has No Negative-Cache/Failure-Memory, So It Regenerates and Re-Serves an Answer Already Confirmed Wrong When the Same or a Similar Question Recurs |
| [Unbounded Context Growth Across Turns](failures/unbounded-context-growth-across-turns.md) | Conversation History and Tool Output Are Appended Every Turn With No Truncation or Summarization, So Total Session Cost Grows Superlinearly as the Conversation Lengthens |
| [Under-Planning Costly Rework](failures/under-planning-costly-rework.md) | Agent Skips Upfront Planning on a Task That Genuinely Needed It, Causing Failed Attempts and Expensive Rework |
| [Unnecessary Ensemble Voting Overhead](failures/unnecessary-ensemble-voting-overhead.md) | N Expensive Model Calls Run in Parallel to Vote/Merge on an Answer, for Tasks a Single Call Would Have Handled Just as Well |
| [Unnecessary Planning Step](failures/unnecessary-planning-step.md) | Agent Runs a Full Planning/Decomposition Call for Tasks Simple Enough to Execute Directly |

**Total: 13 patterns**

## How These Patterns Group

- **Reuse not applied:** [No Preplanned Workflow for Frequent Operations](failures/no-preplanned-workflow-for-frequent-operations.md), [Non-Generalized Plan Template](failures/non-generalized-plan-template.md), [Prompt Caching Underutilization](failures/prompt-caching-underutilization.md), [Prompt Compression Not Applied](failures/prompt-compression-not-applied.md), [Full Reprocessing on Incremental Change](failures/full-reprocessing-on-incremental-change.md), [Repeated Regeneration of Known-Incorrect Answer](failures/repeated-regeneration-of-known-incorrect-answer.md)
- **Too much processing:** [Unnecessary Planning Step](failures/unnecessary-planning-step.md), [Redundant Self-Reflection Passes](failures/redundant-self-reflection-passes.md), [Unnecessary Ensemble Voting Overhead](failures/unnecessary-ensemble-voting-overhead.md), [Unbounded Context Growth Across Turns](failures/unbounded-context-growth-across-turns.md), [Multi-Agent Context Broadcast Waste](failures/multi-agent-context-broadcast-waste.md)
- **Wrong amount of planning or specialization:** [Under-Planning Costly Rework](failures/under-planning-costly-rework.md), [Missing Task Specialization](failures/missing-task-specialization.md)

## When This Matters

- The same operations repeat often
- Prompts share a long stable prefix
- Sessions are long, or several agents share context

## Frequently Asked Questions

### How do I reduce LLM costs without changing models?

Look at [prompt caching underutilization](failures/prompt-caching-underutilization.md), [prompt compression not applied](failures/prompt-compression-not-applied.md), and [unbounded context growth](failures/unbounded-context-growth-across-turns.md).

### Should every agent plan before it acts?

Not necessarily. [Unnecessary planning step](failures/unnecessary-planning-step.md) and [under-planning costly rework](failures/under-planning-costly-rework.md) describe the cost of getting this wrong in either direction.

### What is the difference between cost optimization and cost efficiency?

Cost efficiency covers execution-level waste (batching, retries, routing). This goal covers techniques that exist but are not applied.

## Related

- [All operations goals](../)
- [Operations overview](../../)
