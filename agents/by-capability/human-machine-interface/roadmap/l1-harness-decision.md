# Decision Record: Build the L1 Base Agent on an Existing Harness, or From Scratch?

> **Status: proposed, 2026-10-19 (task 13c).** A person confirms or overrides it. It rests on the sources named below, all opened on 2026-10-19 at the level stated. Nothing here has been run.

## The question
[learning-agent.md](learning-agent.md) defines L1 as a minimal customer-support agent: prompt, tool contracts, handoff and refusal rules, and test cases, all labeled **untested**. Should that be built **on an existing harness** (the τ-bench family, or the OpenAI self-evolving-agents cookbook loop) or **from scratch**?

## What a scheduled run can and cannot do
This library is Markdown only, and a scheduled run cannot run an agent against a model. So L1 can only be a **specification**: text, tool schemas as tables, and test cases. That limits the choice to what the spec should be *shaped like*, not what it should be *run on*.

## Options and what the sources say
| Option | What I opened | What it gives | What it costs |
|---|---|---|---|
| **A. τ-bench or τ²-bench as the test harness** | [τ-bench](https://arxiv.org/abs/2406.12045) (PDF text), [τ²-bench](https://arxiv.org/abs/2506.07982) (abstract) | Conversations between a simulated user and an agent with domain tools and policy; scoring by comparing the final database state with a goal state; a `pass^k` reliability metric. τ²-bench adds a telecom domain where the user also acts | Its domains are retail, airline, and telecom, and the score is task success. It does not score handoff, tone, refusals, or conversation endings, so the library's tests would not fit without new code. I did not open its repository or license |
| **B. OpenAI self-evolving-agents cookbook loop** | [Cookbook](https://cookbook.openai.com/examples/partners/self_evolving_agents/autonomous_agent_retraining) (intro and structure) | A repeatable loop of baseline agent, feedback (human or LLM judge), and prompt refinement, with a versioned prompt record that keeps a fallback history | Written around one vendor's tooling and a healthcare documentation task; its baseline agent is deliberately simple. It is a loop (L3 and L4), not a base agent |
| **C. A gated-edit design (GRASP)** | [GRASP](https://arxiv.org/abs/2605.29668) (abstract) | Each candidate edit is admitted only if it nets an improvement on a held-out probe under a regression budget, applied to a bounded library | Evaluated on clinical-tool benchmarks; the abstract does not describe customer conversation |
| **D. From scratch, framework-neutral** | [Anthropic, *Building effective agents*](https://www.anthropic.com/engineering/building-effective-agents) (page) | The source says the most successful implementations it saw used "simple, composable patterns rather than complex frameworks", and notes the tooling landscape has changed since December 2024 | The spec has no executable check until a person builds one |

## Recommendation
1. **L1 is a framework-neutral specification** (option D): a prompt, tool contracts as tables, handoff and refusal rules taken from the written patterns' fixes, and test cases. This fits a Markdown-only repository and avoids tying the spec to a framework whose tooling the source says changes.
2. **Borrow the evaluation shape from τ-bench (option A), not the code.** Write L1's test cases as: a persona and goal, a policy, the tools the agent has, and an expected end state plus the behaviors from each pattern's test file. Report consistency across repeated runs, as `pass^k` does, when a person runs them.
3. **Borrow the versioned candidate record from the cookbook (option B) and the acceptance gate from GRASP (option C) for L3 and L4**, as design references only. Task 13f checks each rule against the sources.
4. **Defer any runtime choice** until a person supplies one. If a person wants executable tests, the first thing to check is whether τ²-bench's domains can host the library's behaviors, which I could not establish from the abstract.

## What would change this
- A person provides a runtime and a model to run against: then re-evaluate option A for executable tests.
- τ-style harnesses add handoff, tone, or ending checks: then option A fits better.
- Evidence that framework-based agents beat simple ones on customer support: I found none in the sources opened.

## What this record does not establish
- Nothing was run. No claim here is that any option performs better.
- Repositories, licenses, and maintenance state of the benchmarks were not opened.
- The cookbook was read at the intro and structure level, not run.

## Related
- [Gap analysis](gap-analysis.md) · [Agent-type gap analysis](agent-type-gap-analysis.md) · [Learning agent](learning-agent.md) · [Content program](content-program.md)
