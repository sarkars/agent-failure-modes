# What Are the Most Common Tool Selection Sequencing Failures in AI Agents?

**Tool selection sequencing fails when agents call tools in wrong order, when tool outputs that should feed into downstream tools are formatted incorrectly, when agent forgets required prerequisites before calling a tool, or when conditional logic doesn't properly guard when tools should be called.** The 8 sequencing patterns documented here cover the challenge of orchestrating multiple tools into correct sequences — from tool dependencies through conditional invocation, to error recovery when one tool fails and downstream tools must adapt. Sequencing failures are particularly dangerous because a single tool called at the wrong time or with wrong prerequisites can cascade into complete workflow failure.

## Key Takeaways

- 8 patterns span tool ordering, prerequisites, conditional logic, error propagation, and workflow composition.
- Wrong Sequence Order is most severe: calling tools in wrong order violates dependencies and produces wrong results.
- Missing Prerequisites and Conditional Logic Errors are second-order: agents forget required setup or call tools when conditions don't permit.
- Error Propagation Failure is architectural: when one tool fails, downstream tools should adapt or stop, but don't.

## Scope

- **Sequencing and Dependencies** — Tool ordering, prerequisites, dependency chains.
- **Conditional Logic** — Conditional invocation, early termination, error recovery.
- **Data Flow** — Output formatting between tools, cardinality mismatch, state propagation.

## When Sequencing Matters

- Multi-step workflows require specific tool ordering.
- Tool output from one step must feed into next step correctly formatted.
- Failure in one tool should stop or redirect downstream tools.

## Cross-Pattern Insight

Sequencing failures result from treating each tool call independently rather than as part of a workflow. Tools are not orchestrated; they're called opportunistically. When sequencing requirements exist, failures cascade silently. The mitigation is explicit workflow specification: model tool dependencies as a DAG (directed acyclic graph), validate that agent follows dependencies, and test workflows under failure conditions (tool fails at step 2; verify step 3 doesn't execute or adapts).

## Frequently Asked Questions

### How do you specify tool sequencing requirements?
Model tools and their dependencies explicitly: Tool A must be called before Tool B, Tool B's output must be passed to Tool C. Document these requirements and add agent-level validation to detect sequencing violations.

### What should happen if a prerequisite tool fails?
If prerequisite fails, downstream tools should not be called (or should be called with fallback data). Make failure propagation explicit: if Tool A fails, don't call Tool B.

## Patterns

| Pattern | Mechanism |
|---|---|
| Wrong sequence order | Tools called in wrong order; violates dependencies |
| Missing prerequisites | Tool requires prior setup or data; agent doesn't provide it |
| Conditional logic error | Conditional should prevent tool call; condition is wrong or missing |
| Early termination | Workflow should stop after tool failure; agent continues |
| Output format mismatch | Tool 1 output formatted wrong for Tool 2 input |
| Cardinality mismatch | Tool 1 returns N results; Tool 2 expects 1 result; mismatch causes error |
| State not propagated | Tool 1 modifies state; Tool 2 needs modified state; state not passed between tools |
| Error recovery sequence | Tool fails; error recovery sequence is wrong or missing |

**Total: 8 patterns**

## Related Goals

- [Tool Selection](../tool-selection/) — tool selection precedes sequencing
- [Tool Invocation](../tool-invocation/) — invocation correctness complements sequencing
- [Planning and Decomposition](../planning-and-decomposition/) — workflow planning informs sequencing
