# Per-Agent-Type Gap Analysis: Six Most-Built Agent Types

> **Status: first pass, 2026-10-19 (task 13b).** For each type, I opened the abstract or page of the main failure and benchmark references the searches turned up and record what they cover, what they leave out, and what the library adds. **Read** says what I opened: *abstract* (arXiv abstract page), *page* (a web page), or *PDF text* (extracted text of the paper). Nothing here is from search summaries alone unless marked **summary only**. Each "nothing found" claim rests on one or two searches, not a systematic review. Library counts come from the catalog files and are rows (candidates plus written), not verified patterns. Written so far: 18 flagship HMI patterns, all in the human-side areas.

## How to read this
"What the library adds" is a claim about content, not about quality or ranking. Where outside work already covers a topic well, the answer is "link to it, do not compete".

## 1. Customer service and support agents
| Source | Read | What it covers |
|---|---|---|
| [τ-bench](https://arxiv.org/abs/2406.12045) | PDF text | Simulated user conversations with domain tools and policy; retail and airline-style domains. In a manual review of gpt-4o failures in τ-retail, 40 of 115 sampled trajectories failed; 4 were user-instruction problems and 36 were agent issues, of which wrong-decision failures (missing domain rules) were 25% and wrong-argument or wrong-information failures were about 55% (33.3% plus 22.2% in the paper's figure) |
| [τ²-bench](https://arxiv.org/abs/2506.07982) | Abstract | A telecom domain where the user also acts on a shared world; the authors report significant performance drops when agents move from no-user to dual-control, and separate reasoning errors from communication and coordination errors |
| [*From Confident Closing to Silent Failure* (false success)](https://arxiv.org/abs/2606.09863) | Abstract | On 9,876 τ²-bench trajectories from 8 model families and 1,879 AppWorld trajectories, false success (claiming completion when the state shows otherwise) was 45% to 48% of failures in single-control τ²-bench domains, 3% in dual-control telecom, and 75.8% of AppWorld coding-agent trajectories with explicit status claims; no judge setup exceeded AUROC 0.65 on τ²-bench |
| [*Towards a Science of AI Agent Reliability*](https://arxiv.org/abs/2602.16666) | Abstract | Twelve reliability metrics across consistency, robustness, predictability, and safety; 15 models; the authors report that capability gains yielded only small reliability gains |

**What they leave out:** they measure task success, state correctness, and consistency. None of the abstracts or the τ-bench failure analysis covers handoff to a person, tone, accessibility, refusals that help, or how the bot ends a conversation. A handover dataset (QiscusCS) turned up in the earlier gap analysis, **summary only**.
**What the library adds:** the human-side patterns: handoff (3 written), embedded copilots (8), conversation leadership (1), response structure (2), dialogue management (1), effort and memory (3), each with a test file (not yet run) and a metric. The false-success result lines up with [incomplete work reported as complete (EM-07)](effort-completeness-and-memory.md), still a candidate.

## 2. Coding agents
| Source | Read | What it covers |
|---|---|---|
| [Majgaonkar et al., *Understanding Code Agent Behaviour*](https://arxiv.org/abs/2511.00197) | Abstract | Trajectories of OpenHands, SWE-agent, and Prometheus on SWE-Bench; strategies such as defensive programming and context gathering separate success from failure |
| [Mehtiyev and Assunção, *Beyond Resolution Rates*](https://arxiv.org/abs/2604.02547) | Abstract | 9,374 trajectories from 19 agents on 500 tasks; top agents fail on over 20% of benchmarked problems; patch complexity alone does not explain difficulty (12 never-solved tasks need simple patches) |
| [Kim et al., *Coherence Collapse*](https://arxiv.org/abs/2603.24631) | Abstract | 16,758 trajectories; 60% to 69% of failures on two architectures reach and edit the correct functions yet produce wrong patches; the largest theme is overwriting or thrashing correct code after reaching it |
| [SWE-Compass](https://arxiv.org/abs/2511.05459) | Abstract | A benchmark of 2,000 instances across 8 task types and 10 languages, tested under SWE-Agent and Claude Code. The root-cause taxonomy named in my search summary is **not confirmed** from the abstract |

**What they leave out:** these study whether the patch is right. None of the abstracts covers the user-facing side of coding agents: claims that tests pass, changes beyond the request, destroyed uncommitted work, or invented packages (the CD rows).
**What the library adds:** six candidate rows (CD-01 to CD-06), none written, built on existing cross-cutting patterns. The agent-types file notes the older Code Agent area has four goals marked Planned with no pattern files. Link to the trajectory studies rather than compete.

## 3. Research and data-analysis agents
| Source | Read | What it covers |
|---|---|---|
| [ReportBench](https://arxiv.org/abs/2508.15804) | Abstract | Evaluates research reports on cited-literature quality and statement faithfulness, using published survey papers as references |
| [Rao et al., *Detecting and Correcting Reference Hallucinations*](https://arxiv.org/abs/2604.03173) | Abstract | On 10 models and agents (53,090 URLs on DRBench) and 3 models on ExpertQA (168,021 URLs), 3% to 13% of citation URLs were hallucinated and 5% to 18% did not resolve; deep research agents produced more citations and hallucinated URLs at higher rates |
| [Hirsch et al., *Who is the Agent to Blame?*](https://arxiv.org/abs/2608.24306) | Abstract | A method that localizes faithfulness and citation errors to the agent that introduced them, with four error types: hallucination, uncited input reliance, uncited output, insufficient citations |

**What they leave out:** all three are about deep-research reports and citations. I found no work on data-analysis agents (wrong joins, wrong business definitions) in one search.
**What the library adds:** five candidate rows (DA-01 to DA-05), none written; DA-04 (claims to have read inaccessible sources) extends existing citation patterns. Citation validity is well covered outside; the data-analysis half is the opening.

## 4. Workflow-automation agents
| Source | Read | What it covers |
|---|---|---|
| [WorkArena](https://arxiv.org/abs/2403.07718) | Abstract | 33 tasks on ServiceNow plus the BrowserGym environment; a considerable gap to full automation; a significant gap between open and closed-source models |
| [WorkArena++](https://arxiv.org/abs/2407.05291) | Abstract | 682 tasks of realistic workflows testing planning, reasoning, retrieval, and contextual understanding, with human workers as a comparison |
| [TheAgentCompany](https://arxiv.org/abs/2412.14161) | Abstract | A simulated software company; the most competitive agent completed 30% of tasks autonomously, with long-horizon tasks still out of reach |

**What they leave out:** capability on workflows, not what the person sees: whether a skipped step is reported, whether a confirmation matches a stored result, or whether approval was asked for. Figures I saw for GPT-4o on these benchmarks came from blog write-ups (**summary only**) and are not used.
**What the library adds:** four candidate rows (workflow-automation section), none written. Related written patterns: [lazy completion](../goals/effort-and-memory/failures/lazy-completion.md) and [no warning of context loss](../goals/effort-and-memory/failures/no-warning-of-context-loss.md).

## 5. IT and security agents
| Source | Read | What it covers |
|---|---|---|
| [ITBench](https://arxiv.org/abs/2502.05352) | Abstract | 94 real-world scenarios across SRE, compliance and security operations, and FinOps; agents resolved 13.8% of SRE scenarios, 25.2% of CISO scenarios, and 0% of FinOps scenarios |
| [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/2025/12/09/owasp-genai-security-project-releases-top-10-risks-and-mitigations-for-agentic-ai-security/) | Page (press release) | Released in December 2025 with input from over 100 contributors; highlights agent behavior hijacking, tool misuse and exploitation, and identity and privilege abuse. I did not open the list itself, so the full ten are **unverified** here |

**What they leave out:** ITBench scores resolution; OWASP covers threats. Neither, in what I opened, covers how an agent explains an action to an operator, asks for approval, or hands an incident to a human.
**What the library adds:** five candidate rows (IT and security section), none written, plus older cross-cutting security patterns the rows extend. A security vendor's incident write-up (opened in the first-pass analysis) maps incidents to OWASP categories; do not compete on the threat catalog.

## 6. Copilots (embedded assistants)
| Source | Read | What it covers |
|---|---|---|
| [Liang et al., *A Large-Scale Survey on the Usability of AI Programming Assistants*](https://arxiv.org/abs/2303.17125) | Abstract | Survey of 410 developers; developers do not use these tools mainly because the output does not meet functional or non-functional requirements and because they have trouble controlling it |
| [Wang et al., *Investigating and Designing for Trust in AI-powered Code Generation Tools*](https://arxiv.org/abs/2305.11248) | Abstract | Interviews with 17 developers; three challenges: building appropriate expectations, configuring tools, and validating suggestions; plus a design probe |

**What they leave out:** both are about programming assistants. Neither covers assistants embedded in consumer or business products: re-asking known information, forced logins, sales pitches in help, cancellation friction. Microsoft's human-AI interaction guidelines were not readable (the page is rendered by script), so I cannot say what they cover.
**What the library adds:** the [embedded copilots family](../goals/embedded-copilots/README.md): 8 patterns written, with tests (not yet run) and incident pages for two. The first-pass analysis counted 23 catalog rows for this type; I did not recount.

## What this changes
- **Customer service** is where the library already differs most (human-side behavior). The false-success result gives the "claims it did what it didn't" pattern outside backing to link to.
- **Coding, research, workflow, and IT** are covered on capability and security by strong outside work. The library's opening is the user-facing side, and none of those rows is written. Order in the queue is unchanged.
- **Not done in this pass:** reading full papers (abstracts only), and the other agent types in the agent-types file.
