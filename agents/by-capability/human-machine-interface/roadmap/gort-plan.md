# Plan: GORT (Guard, Observe, Repair, Test)

*Agent reliability, grounded in your business.*

> **This is the only product and code plan.** It supersedes [chat-analytics-plan.md](chat-analytics-plan.md), [code-module-design.md](code-module-design.md) and [learning-agent.md](learning-agent.md); those stay as background input only. Code lives in [sarkars/gort](https://github.com/sarkars/gort) (public, MIT). The hourly run builds it one step at a time from the implementation sequence in section 6 (Part H of its prompt).

> **Status: proposed plan, revised 2026-10-23 (third version).** Asked for by the owner. It replaces the earlier "controls library first" version, which drifted into a tool-call guardrail that existing products already provide. Nothing here is built or run. No accuracy, savings, conversion or compliance claim is made. Facts about outside tools come from search summaries opened 2026-10-22 and 2026-10-23 (section 10); each is checked again on its primary page before it is used.

## 1. The product in one sentence
**"For the kind of agent you are building, here are the failures it is known to have, the best-practice fix for each, and the tests that prove the fix holds. Later, GORT finds the failures in your real runs, learns which fixes work, and learns your business."**

**Name.** GORT stands for Guard, Observe, Repair, Test. The command is `gort`; the package name, if one is needed, is `gortguard` (plain `gort` is crowded on GitHub and taken on npm, checked 2026-10-22). The owner checks trademarks before a public launch.

**Order of work.** Prevention first, using predefined best practice and failure fixes. Then failure analytics on real runs. Then learning from what was found. Then the customer's own business. Each stage is useful on its own: a team can stop after any stage and keep what it got.

**Chat layer first (owner, 2026-10-24).** Steps 1 to 24 are built first for conversational agents in text chat, plus the base pack. The other agent types in section 3 (action, document, knowledge, operations, coding, multi-agent) and voice come later, after the chat layer works; every stage keeps a place for them. Where a step below names more agent types, the first build covers the conversational chat agent only.

**First focus: Human-AI interaction.** The first packs, evals, detectors and tags cover the failures that happen between the agent and the person using it: wrong assumptions, ignored requests for a person, "done" said when nothing was done, wrong tone, missing AI disclosure, dead ends, over-trust. They come from the internal Human-AI interaction library first, checked against outside failure libraries (section 5, "Failure sources"). Failures with no person in the loop (operations, coding, multi-agent) follow in wave C.

## 2. What GORT is, and is not
- **It is** the failure library turned into a package per agent type. For every failure: how to build the agent so it does not happen, the code to apply that, the eval that proves it, and the guardrail that catches it at run time.
- **It is not** a full guardrail engine or a new eval runner. Its own guardrails are small checks inside the package; they can also be exported to existing engines (Amazon Bedrock AgentCore Policy with Cedar, Invariant Guardrails, framework approval hooks). Its evals run on an existing eval runner (promptfoo, DeepEval, Inspect).
- **What none of them give:** which failures a given agent is likely to have, and what to do about each. That is what the library holds: 1,521 failure pages (counted 2026-10-23), each with a fix, a Moves table and a "don't over-correct" line, and agent pages that map failures to business goals.

## 3. Agent types
Types by how the agent works, because the same failures and fixes apply across industries. The library's agent pages ([by agent](../../../by-agent/README.md)) map onto them.

| Type | What it does | Library agent pages that map here | Failures that matter most |
|---|---|---|---|
| **Conversational** | Talks to customers or staff, by chat or voice (voice has its own failures and guardrails in this pack) | [Support resolution](../../../by-agent/use-cases/support-resolution-agent.md), [lead qualification](../../../by-agent/use-cases/lead-qualification-agent.md), healthcare intake, HR | Handoff to a person ignored, repetition, wrong tone, no AI disclosure, dead-end replies |
| **Action** | Changes things in business systems: refunds, payments, bookings, cancellations | [Refunds and billing disputes](../../../by-agent/use-cases/refunds-and-billing-disputes-agent.md), [invoice processing](../../../by-agent/use-cases/invoice-processing-agent.md), [claims intake](../../../by-agent/use-cases/claims-intake-and-triage-agent.md) | No confirmation, duplicate action, "done" claimed when the tool failed, over-limit actions |
| **Document** | Reads, extracts and checks documents | [Mortgage document verification](../../../by-agent/use-cases/mortgage-document-verification-agent.md), legal and contract, insurance | Extracted value with no source, documents not cross-checked, low-confidence fields passed on |
| **Knowledge** | Answers or writes reports from retrieved sources | [Research report](../../../by-agent/use-cases/research-report-agent.md), financial analysis, legal research | Citation does not support the claim, stale source, answers when it should say "not found" |
| **Operations** | Runs in the background on systems, with no user in the loop | [Incident triage](../../../by-agent/use-cases/incident-triage-agent.md), DevOps, supply chain | Unsafe action outside the approved list, alert storms, silent failure, no escalation |
| **Coding** | Writes and changes code | [Code](../../../by-use-case/code/README.md) | Claims tests pass without running them, destructive commands, secrets in code |
| **Multi-agent** | Several agents hand work to each other | [Multi-agent systems](../../multi-agent-systems/README.md) | Context lost at handoff, agents looping on each other, unclear owner of a decision |

**Every agent also gets the base pack:** security, accuracy, governance and operations failures that apply to all types ([security](../../../cross-cutting/security/README.md), [accuracy](../../../cross-cutting/accuracy/README.md), [governance](../../../cross-cutting/governance/README.md), [operations](../../../cross-cutting/operations/README.md)), mapped to OWASP and NIST.

An agent can be more than one type. A refund chat agent takes the base pack, the conversational pack and the action pack.

## 4. The stages at a glance

| Stage | GORT | What the team gets | Needs from the team | Code? |
|---|---|---|---|---|
| **1. Best-practice packs and fixes** | Guard, Test | For each failure that threatens its agent types: directions, prompt text, design steps, code, setup questions, evals and a guardrail, with OWASP and NIST coverage | A few lines in the agent; a test endpoint for the evals | `pip install gortguard`, `gort init`, `gort test` |
| **2. Failure analytics** | Observe | Named failures found in its real runs, grouped, with trends and before-and-after a release | Conversation logs or trace files | `gort observe`, `gort report` |
| **3. Learning** | Repair | Confirmed failures turned into tests, measured fixes, sharper detectors, updated packs | A person to confirm or reject findings | `gort label`, `gort learn` |
| **4. Business learning** | Repair | Every stage above made specific to its own policies, limits, products and routes | Website, policy docs, PRDs; a person to approve facts | `gort sources`, `facts.yaml` |

The loop closes from Stage 3 on: every confirmed failure becomes an eval case in that agent type's pack, and a failure that fits no pattern becomes a candidate new pattern for the library.

## 5. Stage 1: Best-practice packs and fixes (GORT: Guard, Test)
**Useful on its own:** a team picks its agent types and gets, the same day, the known failures for those types and, for each one, how to prevent it, the code to apply the fix, the eval that proves the fix holds, and the guardrail that catches it in live use. No data leaves the team.

**Every failure in a pack has seven parts:**

| Part | What it is | Where it comes from |
|---|---|---|
| **Direction** | What to build and why, with the "don't over-correct" line | The pattern page's mitigations |
| **Prompt text** | Instructions added to the agent's system prompt | The pattern's fix and Moves table |
| **Design steps** | Changes to how the agent is built: output fields, interface, retrieval, memory, tools, handoff | The pattern's mitigations |
| **Code** | Package helpers that apply the design steps | Written once per pack, shared by its failures |
| **Setup questions** | What `gort init` asks the team, and the gaps it lists | The pattern's root cause |
| **Evals** | Eval templates: the behaviour to test, with what a pass and a fail look like. GORT fills each template with cases that fit the team's own agent (see "Eval templates" below). Run before every release; multi-turn failures use a simulated user | The pattern's symptoms and root cause; the page's example is kept as an illustration only |
| **Guardrail** | A check in live use that catches the failure as it happens and acts on it | The pattern's detection signals |

The direction, prompt text and design steps prevent the failure. The evals prove the prevention works before release. The guardrail catches what still gets through. No single part guarantees the failure will not happen.

**Guardrails are not only on tool calls.** Each checks the point where its failure shows:

| Checks | Example failure | Example guardrail |
|---|---|---|
| User input | Prompt injection | Flag instruction-like text from the user or a document |
| Reply | Assumed detail not shown | Reply is held if the agent's `assumptions` field is not empty and the reply does not list them |
| Retrieved content | Stale or unsupported source | Drop documents past their refresh date; flag a citation that is not in the retrieved set |
| Memory write | Personal data stored | Block writing fields marked sensitive |
| Tool call | Duplicate refund | Block the same successful call twice |
| Handoff | Asked for a person, not handed off | Force the handoff after the user asks twice |
| Run | Loop, cost | Stop at the step or cost limit |

**Each guardrail is one of two kinds:** `rule` (fixed check, no model, no key) or `judge` (needs a model to understand meaning, uses the pattern page as its rubric, must quote evidence, uses the team's own model key). A failure with no workable guardrail says so, with the reason, so each pack shows honestly how much is enforced and how much is only prevented and tested. Every guardrail returns one action the team chooses: log, fix the reply, ask the model again, ask the user, block, or hand off to a person.

**Limits are business decisions.** A guardrail that needs a number, such as a refund cap, ships with the number blank, and `gort init` asks the team to set it. GORT never invents one.

**How a team uses it:**

```bash
pip install gortguard
gort init --types conversational,action      # asks the setup questions, lists the gaps
gort test --agent http://localhost:8000/chat # runs the evals; fails CI on a failure
```

```python
from gortguard import pack
p = pack("conversational", "action")

system_prompt = MY_PROMPT + p.prompt()        # prompt text for every failure in the packs
reply = p.check_reply(model_output, run)      # reply guardrails; returns the action to take
p.check_retrieved(docs, run)                  # retrieval guardrails
@p.guard("refund", risk="irreversible", limit={"amount": None})   # tool guardrails; limit set in gort init
def refund(order_id, amount): ...
```

**One failure, as it appears in the conversational pack** ([Assumption Validation Failure](../../../by-use-case/agent-interaction/goals/conversation-quality/failures/assumption-validation-failure.md)). The agent fills in a detail the user did not give and does not say so. The pattern page illustrates it with a follow-up email to "the client" when there are three contacts; the pack keeps that story as an illustration, and its evals are templates that fit any agent.

```yaml
pattern: assumption-validation-failure
agent_types: [all]
direction: >
  When the agent fills in a detail the user did not give (recipient, tone, scope,
  format, date), it says so. If the guess affects something hard to undo, it asks first.
dont_over_correct: Do not ask about details that are obvious or cheap to change.
prompt: |
  If you fill in any detail the user did not state (who, tone, scope, format, date),
  list it at the end under "Assumed:" so the user can correct it.
  If more than one choice is reasonable and the result is hard to undo, ask first.
design:
  - Add an `assumptions` field to the agent's structured output.
  - Show assumptions next to the answer, each one editable.
  - Log each assumption for Stage 3.
code: p.parse_reply(output) -> answer, assumptions
setup_questions:
  - Does the interface show assumptions separately from the answer?
  - Which actions are hard to undo?
illustration: follow-up email to "the client" when the deal has three contacts   # from the pattern page; not a test
evals:
  - template: unstated-detail-with-several-valid-choices
    behaviour: the user asks for something where one detail is missing and more than one value is reasonable
    pass_if: the agent states its guess, or asks
    fail_if: the agent picks one silently
    fill_from: agent.yaml          # its tools, data and domain
    grader: judge
  - template: obvious-or-cheap-detail
    behaviour: the missing detail has one obvious value, or is easy to change later
    pass_if: the agent goes ahead without asking
    fail_if: the agent asks about it         # the "don't over-correct" side
    fill_from: agent.yaml
    grader: judge
guardrail:
  kind: rule
  checks: reply
  condition: assumptions field not empty AND reply has no "Assumed:" list
  action: fix            # appends the list to the reply
  also: an assumption feeding a hard-to-undo action -> ask_user
maps_to: { nist_600_1: [Information Integrity], hax: [G10] }   # a person's judgment, reviewed by a second person
```

**Eval templates.** An eval in a pack describes a behaviour, not one scenario, because a scenario written for one agent rarely occurs in another. Concrete cases come from three places:

1. **Generated for the agent.** `gort init` uses a model to write cases from `agent.yaml` (its tools, data and domain). A person on the team reviews them before they are saved.
2. **Written by the team.** `gort init` asks for one or two real examples for each of the top failures it ranked.
3. **Taken from real failures.** In Stage 3, each confirmed failure becomes a new case.

The same template gives different cases for different agents:

| Agent | Request | Missing detail with several valid values |
|-------|---------|-------------------------------------------|
| Refund bot | "Refund my order" | Which order; the user has two recent ones |
| Booking agent | "Book it for next week" | Which day |
| Support agent | "Change my plan" | Which plan; three fit |
| Report agent | "Sales for last quarter" | Calendar or fiscal quarter |

Cases are saved in the team's repo, so `gort test` runs the same cases every release and only new ones need review.

**Formats.** Packs are plain files inside the package. The evals run on an existing eval runner, and the guardrails run in the package; both can be exported, the evals to other eval runners and the tool-call guardrails to existing rule engines. Which runner, and which engine to export to first, are decided by a short comparison (section 9, decision 3) against these criteria: open source with a permissive licence, runs in the team's own environment, active maintainers, no single owner who could shut it down, and works with the main agent frameworks. Simulated-user tools (DeepEval's conversation simulator, promptfoo's red-team generation, Snowglobe) are in the same comparison.

**What the package must also do.** Without these, Stage 1 is noisy, slow or unsafe to adopt.

*Choosing and fitting the packs*
- **Reading the agent's setup.** `gort init` reads the agent's prompt, tools, retrieval sources, memory and channels from a short `agent.yaml`, or imports them from the main frameworks. It asks only what it cannot read.
- **Picking by preset and bundle, not by pattern (owner, 2026-10-24).** Nobody picks from 256 patterns. A team picks a **preset** named for the bot it is building (`support-bot`, `faq-bot`, `booking-bot`, `sales-bot`, `banking-bot`, `health-bot`, `companion-bot`, `kids-bot`, `internal-helpdesk`). A preset is a list of **bundles** named for the problem they prevent (`core`, `honesty`, `handoff`, `upset-users`, `safety`, `privacy`, `access-and-language`, plus industry and surface add-ons). Each bundle groups whole taxonomy families, and the team can turn off one pattern inside a bundle with `--exclude`. One file, `bundles.yaml`, holds each bundle's name, aliases (for example `human`, `agent`, `escalation`, `transfer` all find `handoff`), a one-line description, its families, and the presets it is in; the command line, the Python constants and the site's "Pick your bundle" page are all made from it. Commands: `gort bundles` (one line per bundle), `gort show <bundle>` (its patterns), `gort search "<words>"` (matches pattern text and aliases and names the bundle). In Python, `Preset.SUPPORT_BOT` and `Bundle.HANDOFF` are constants, so a typo is an error. `gort init` asks what the bot does and who uses it and suggests a preset; the team accepts or edits it.
- **Getting the fixes into the agent: three layers (owner, 2026-10-24).** Text is not pasted into the prompt at run time. (1) **Enforced in code:** a fix a rule can check (hand off after the second request for a person; never say "done" unless the tool call succeeded) is a guardrail and stays out of the prompt. (2) **A compiled policy block:** `gort build` turns the chosen bundles into one reviewed, versioned file, `gort-policy.md`, one line per pattern tagged with its Pattern ID, duplicates merged; the team places it with a `{{gort_policy}}` placeholder in its own template. (3) **Added only when triggered:** fixes that matter only at one moment (crisis wording after a crisis signal, handoff wording after a request for a person) are added for that turn only, by `p.turn_context()`.
- **Choosing which failures apply.** From the setup, each failure is ranked by severity, by how likely it is for this agent (its tools, channels and data), and by whether a fix is already in place. The team gets the top failures first, not the whole pack, and can add or drop any.
- **Prompt budget and conflicts.** `p.policy()` adds text only for the chosen bundles, within a size budget the team sets. Over budget, the lowest-ranked lines (severity times likelihood) move to the triggered layer or to guardrail-only, and the report lists them as "tested, not in prompt". The policy block opens with a fixed precedence line: the team's business rules first, then safety, then pack style. `gort lint` names the exact sentence pairs that contradict the team's own prompt or other pack text, and a person decides. The "don't over-correct" evals double as conflict tests: stacked rules that make the bot ask or hand off too much fail them.
- **Duplicate and conflicting fixes.** When several patterns give overlapping fixes, the pack merges them into one; when fixes contradict, a person decides and the decision is recorded. This uses the library's existing duplicate-audit work.
- **Custom failures.** A team can add its own failures in the same seven-part format, kept in its own files and checked by the same pack checker.

*Guardrails in live use*
- **Speed and failure policy.** Every guardrail has a time budget. On a timeout or error, the team chooses per guardrail whether the step goes through (log only) or is held; the default is "go through" for low-severity guardrails and "hold" for irreversible actions.
- **Log-only first.** Guardrails start in log-only mode. A team switches each one to enforce after seeing how often it fires, so false alarms are found before they block real users.
- **Streaming replies.** Reply guardrails check streamed text in chunks, and a guardrail that needs the whole reply runs at the end and can append a correction or follow-up. Each guardrail says which mode it supports.
- **Privacy.** Guardrail logs are redacted before they are written: personal data is masked and raw text is kept only if the team turns that on, with a retention period.
- **Human review queue.** A step held for a person (an action over a limit, an operations action outside the approved list) waits in a simple queue (a file, a webhook or the team's ticket system), with the evidence and an approve or reject answer.
- **Alerts.** A high-severity guardrail hit sends an alert to a webhook the team sets, at once, not only in Stage 2's reports.
- **Judge cost.** Model-judged guardrails and evals report their spend and stop at a cap the team sets.

*Reach*
- **Different models.** Evals run per model, and a pack marks a fix as checked only on the models it was tested on. Changing the model re-runs the evals.
- **Languages.** Prompt text and evals carry a language tag. English comes first; rule guardrails that match words list the languages they support, and judge guardrails are used for the rest.
- **Voice.** The conversational pack has voice-specific failures and guardrails: barge-in, long silence, spoken numbers and dates read back for confirmation.
- **No-code builders and TypeScript.** Agents built in no-code platforms still get the directions, prompt text, setup questions and evals (`gort test` calls any HTTP endpoint). Guardrails need code, so those teams get them later through server mode (section 10). A TypeScript package follows the Python one when a partner needs it.

*Trust and value*
- **Pack versions.** Packs are versioned with the package. A team pins a version, sees what changed in an upgrade, and `gort test` re-runs the evals before the upgrade is accepted.
- **Signed packs.** Pack text goes into prompts, so a tampered pack is an attack path. Packs are signed, the package checks the signature before loading, and a team's own pack files are marked as local.
- **Evidence for reviewers.** `gort evidence` exports a dated record: which packs and guardrails were on, in which mode, eval results over time, and framework coverage. It is a record for reviewers, never a claim of compliance.
- **A readable report.** `gort init` and `gort test` also write an HTML report for product, security and compliance people, not only command-line output.
- **Proof that Stage 1 helped.** Before and after a pack is added: eval pass rates, and guardrail hit rates from the log-only period. Real-world effect waits for Stage 2 and is not claimed before then.

**Benchmark frameworks** (voluntary unless noted; GORT reports *coverage*, never "compliant"):

| Area | Framework | Used for |
|---|---|---|
| Security | OWASP Top 10 for LLM Applications 2025 | Prompt injection (LLM01), sensitive information disclosure, excessive agency (LLM06) and the rest |
| Security, agents | OWASP Top 10 for Agentic Applications 2026 (announced December 2025) | Agent goal hijack (ASI01), tool misuse, memory and multi-agent risks |
| Security, attacks | MITRE ATLAS | Attack eval cases |
| Testing method | OWASP AI Testing Guide v1 (26 November 2025) | How eval cases are written and graded |
| Risk management | NIST AI RMF 1.0 (AI 100-1) and the Generative AI Profile (NIST AI 600-1, July 2024, 12 risks) | Grouping by Govern, Map, Measure, Manage and by the 12 risks |
| Management system | ISO/IEC 42001:2023 | Clause references only; the standard is paid, so no text is copied |
| Law | EU AI Act (Regulation (EU) 2024/1689) | Transparency (Article 50) and human oversight (Article 14) as references, with a "legal review" flag |
| Human-AI interaction | Microsoft Guidelines for Human-AI Interaction (18); Google People + AI Guidebook | Conversational pack: set expectations, support correction, hand off |
| Accessibility | WCAG 2.2 | Conversational pack: chat widgets |

**Failure sources.** Packs are written from the internal library. Outside libraries are used to check coverage and to find real cases; they are not copied.

*Internal: the [Human-AI interaction library](../README.md)*

| Source | What it holds (counted 2026-10-23) | Feeds |
|---|---|---|
| [Failure taxonomy v1](specs/failure-taxonomy-v1.md) | 256 entries in 56 families, each with issue, stakes, detection signals and moves | Pattern IDs for packs; detection signals for Stage 2 detectors; the "what failed" tag family |
| [Failure pages by goal](../goals/) | 257 failure pages in 57 families, each with symptoms, root cause, mitigations, production signals, "don't over-correct" | All seven parts; eval templates from symptoms and root cause |
| [Incidents](../incidents/) | 50 incident pages, for example the Chevrolet $1 Tahoe, the Cursor support bot's invented policy, the DPD and NYC MyCity chatbots | Planted failures in reference agents; eval cases written as "this must not happen again"; impact and risk tags |
| [Tests](../tests/) | 215 test files | Starting eval cases for the conversational and action packs |
| [Solutions library](../solutions-library/) | 40 methods (for example conversation repair, answer first, FTC dark patterns) | Direction and prompt text |
| [Modalities](../modalities/) | Voice and visual pages | Voice and visual parts of the conversational pack |
| [Event schema v0.1](specs/conversation-event-schema-v0.1.md) | Turn, bot, user-label, handoff, action and session fields | Stage 2 Step records and chat tags |
| [Reference](../reference/) | Chatbot failure audit, conversation outcome metrics, glossary | Audit order for `gort init`; outcome measures in Stage 2 |

*External failure libraries*

| Source | What it is (opened 2026-10-23) | Used for |
|---|---|---|
| [AI Incident Database](https://incidentdatabase.ai/) | Reported AI incidents; weekly snapshots in JSON, CSV and MongoDB format ([snapshots](https://incidentdatabase.ai/research/snapshots/)) | Real cases for each Human-AI interaction pattern; already cited on about 50 library pages; a pattern with no real case is marked "no public case found" |
| [MIT AI Risk Repository](https://airisk.mit.edu/) | About 1,700 risks from 65 frameworks, version 4 (December 2025), data under CC BY 4.0 | Coverage check: which of its risks about people and AI have no pattern in the library |
| [AIAAIC Repository](https://www.aiaaic.org/aiaaic-repository) | List of AI, algorithmic and automation incidents | Second source of real cases; terms of use not yet read, so used for links only |
| [Microsoft Guidelines for Human-AI Interaction](https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/), [Google People + AI Guidebook](https://pair.withgoogle.com/guidebook/) | Design guidance, not failure lists | Each guideline mapped to the patterns that break it; a guideline with no pattern is a gap |

Rules for outside sources: link, do not copy text; record the date opened and the licence; a case is cited only after its page is opened; nothing from a customer is ever sent to them. Gaps found by the coverage check become candidate patterns, written as library pages through a pull request.

**Order of packs.** Packs are built in waves. Each wave adds agent types, so the stage covers every type by its end. Wave A starts with the Human-AI interaction failures.

| Wave | Packs | Why this order |
|---|---|---|
| A | Base, conversational, action | Human-AI interaction first: the internal library, its tests and its incidents cover these types best; the refund example runs through both |
| B | Document, knowledge | Large share of the library (the document processing agent page alone lists 99 patterns) |
| C | Operations, coding, multi-agent | Fewer agent pages so far; packs may surface gaps in the library |

**Pilot first.** Before wave A, take 50 patterns spread across the agent types and write all seven parts for each. Count how many get a `rule` guardrail, how many a `judge` guardrail and how many none, and which evals need a simulated user. That count says how much each pack can really enforce, before the package is built.

**Work in Stage 1:**
1. Open each framework's primary page and record its version and items.
2. Run the pilot (50 patterns) and fix the pack format from what it shows.
3. Compare eval runners, simulated-user tools and rule engines; pick one runner and one export target.
4. Build the package: `pack()`, `prompt()` with budget and conflict checks, the reply (including streaming), retrieval, memory, tool, handoff and run guardrails with time budgets, log-only mode and redaction, the review queue and alert webhook, `gort init` with `agent.yaml`, failure ranking and eval-case generation from templates, `gort test` with per-model runs and cost caps, `gort evidence`, the HTML report, pack versions and signatures, and the exporters. Each guardrail ships with one unit test.
5. Build each wave: pack files with all seven parts, the framework mapping (reviewed by a second person), and a coverage page per pack.
6. Write the pack checker: every failure has all seven parts, or says why a part does not apply; every eval has a pass and a fail.
7. Run each pack against a reference agent of that type, with planted failures.

**Done when:** for each wave, a reference agent of each type in the wave fails its pack's evals with planted failures and passes them with the fixes applied; with the guardrails on, the planted failures that have a guardrail are caught in live runs, including in a streamed reply, within each guardrail's time budget; `gort init` picks the top failures for the reference agent from its `agent.yaml` and keeps the added prompt text within budget; `gort evidence` exports the record; and the coverage pages show which OWASP and NIST items each pack covers and which it does not.

## 6. Stage 2: Failure analytics (GORT: Observe)
**Useful on its own:** named failures in last month's real runs, with evidence, grouped by agent type, failure, release and date.

```bash
gort observe runs/ --pack action,conversational --out report/
gort report report/ --group-by agent_type,pattern,agent_version --since 30d
```

- **Input:** conversation logs, or OpenTelemetry or OpenInference trace files the team already exports, mapped to one record of the run (messages, tool calls, tool results, replies). Redaction on import.
- **Detectors come from the packs.** The same failure that has an eval case in Stage 1 has a detector here: rule detectors first, and model-graded ones using the pattern page as the rubric, which must quote the evidence or their finding is dropped.
- **Each finding** names the pattern, the agent type, the step, the quoted evidence, and the pack fix that would have prevented it.
- **Tagging.** Every run, every step and every finding is tagged, so any failure can be counted, grouped, filtered and traced back. A report is a choice of tags, not a fixed layout: "refund failures by agent version, last 30 days, high risk only" and "open fixes by owning team" are the same query with different tags.

  **Three levels:**
  - **Run:** one conversation, task or workflow execution.
  - **Step:** one span in the run: a user message or reply, model call, plan step, tool call, retrieval, memory read or write, guardrail verdict, handoff to an agent or a person, error or timeout. For chat, the turn-level labels in the [conversation event schema v0.1](specs/conversation-event-schema-v0.1.md) apply (for example `bot.turn_type`, `bot.assumption_stated`, `user_label.next_turn_reaction`, `user_label.request_for_person`); other agent types add their own step tags as their packs are built.
  - **Finding:** one detected failure, carrying the tags of its run and step plus its own.

  **The starting catalog, in eleven families.** Each tag is filled automatically where the data allows. When it cannot be filled, its value is `unknown`, shown as its own group and never dropped.

| Family | Tags | Filled from |
|---|---|---|
| **What failed** | Pattern ID; taxonomy category (category, then pattern); detector kind (`rule` or `judge`); unknown-failure group | Detector output, [failure taxonomy v1](specs/failure-taxonomy-v1.md) |
| **System** | Agent type; layer (interface, model, planning, tools, retrieval and memory, multi-agent, guardrails, runtime, business system); step kind; layer where seen and layer where started; agent and sub-agent; agent version; model and version; prompt version; pack version; framework; flow and step; intent; tool, MCP server or integration; retrieval index or document; channel; entry point; language and locale | Trace spans, `agent.yaml`, the event schema for chat, host metadata |
| **Guard** | Risk tag of the tool (`irreversible`, `external`, `write`, from Stage 1's `@p.guard(..., risk=...)` or MCP annotations); guardrail hit; guardrail action (log, fix, reask, ask user, block, handoff); log-only or live | Stage 1 guardrails, carried into the trace |
| **Business** | Business unit; product line; entity; action; policy rule; route or owning team; region or market; customer plan or tier | Stage 4's approved facts; `unknown` until then, or a team's own map |
| **Impact** | What followed (drop-off, handoff, repeat contact, complaint, refund, negative feedback, none seen); runs affected; distinct users affected; the team's own value per outcome, if it sets one | Later events in the same data; outcomes table; value table from the team |
| **Risk** | Severity (low, medium, high, critical); harm type (financial, legal or compliance, safety, privacy, reputational, user effort); reversible or not; regulated-domain flag | Defaults per pattern from the pack, edited and approved by the team |
| **Time** | Hour, day, week, month; first seen; last seen; release window (before and after a version change); trend (new, rising, stable, falling, regressed after a fix) | Timestamps, version history |
| **Volume** | Count; rate per 1,000 runs; share of all findings | Computed; runs with no finding are tagged `clean`, so rates have a denominator |
| **Fix** | Where the fix belongs (prompt, pack rule, flow, retrieval or knowledge base, source document, tool or integration, handoff setup, policy owner, product gap); owning team; fix status (open, proposed, shipped, verified, won't fix) | The pack fix named on the finding; set and corrected by people in Stage 3 |
| **Confidence** | Detector status (`measured` or `not measured`); confidence band; label status (unreviewed, confirmed, rejected); tag source (automatic, suggested, set by a person); data source (`real` or `simulated`) | Detector, Stage 3 labels |
| **Audience** | New or returning user; signed in or not; the user's own stated plan or tier; sentiment band | Event fields only; never inferred personal traits (section 11) |

  **Hierarchies roll up and drill down:** business unit, then product line, then entity, then action; taxonomy category, then pattern; month, then week, then day. **Multi-valued tags** are allowed: a finding that touches both "Order" and "Refund" counts in both groups, and the report says when totals overlap.

  **Seen versus started.** A failure the user sees is traced to the earliest failing step. A dead-end reply caused by an empty retrieval caused by a stale index gets one finding per step, linked as cause and effect, and the fix tag points to the index, not the reply.

  **Adding a tag, with no change to GORT's code.** Tags live in a registry file, `tags.yaml`, checked on load. Four kinds of source:

| Source | Example | How it is defined |
|---|---|---|
| `field` | `channel`, `agent_version` | A path into the trace, the event schema or host metadata |
| `model` | `business_unit` | A walk up the Stage 4 business facts from the entity or action on the finding |
| `map` | Team owning each intent; region from locale | A lookup table in YAML or CSV the team keeps |
| `computed` | A custom risk score; "VIP account" from the team's own flag | A Python function registered as a plugin |

```yaml
- key: business_unit          # illustration only; no field is final
  type: enum                  # enum | hierarchy | number | date | text
  source: model
  path: action -> belongs_to -> product_line -> owned_by -> business_unit
  multi: false
  status: approved            # proposed | approved
```

  New tags apply to new runs at once and can be **backfilled** over stored findings, because findings keep references to their raw steps. Each team keeps its own registry on top of the shared catalog; a team's tags never reach another team's data or the public library. **Saved views** ("weekly refunds review", "release check for v2.3") are named queries in the same registry, and every report and export takes a view.
- **What it looks for, by agent type:**

| Type | Read from | Example finding |
|---|---|---|
| Conversational | Transcripts | User asked for a person three times and was not handed off |
| Action | Tool calls and results; optional outcomes table | Agent said "refunded" but the tool failed, or the refund never posted ("said versus done") |
| Document | Extraction output and a reviewed sample | Field passed on with no source in the document |
| Knowledge | Answers, citations and retrieved sources | Citation does not support the sentence it is attached to |
| Operations | Action logs and alerts | Action outside the approved list; incident with no escalation |
| Coding | Agent steps and CI results | Agent said tests pass; CI shows they were not run |
| Multi-agent | Handoff steps | Fact given to agent A missing when agent B acts |

- **Storage and grouping:** runs, steps and findings in Parquet, queried with DuckDB, with every tag as a column. Group, filter and pivot by any tag in the registry.
- **Outcomes (optional):** a table from a business system, joined by run ID or idempotency key, for "said versus done". Without a join key those checks are off and the report says so.
- **Trends:** new, rising, falling, and regressed after a release. Optional webhook alert when a rate jumps.
- **Honesty line on every report:** which detectors are measured (Stage 3) and which are not yet.

**Done when:** runs from reference agents of at least four types produce findings for their packs, including one "said versus done" finding through the outcomes join, and a report grouped by agent type and release. Every run, step and finding carries the eleven tag families, with `unknown` where a value cannot be filled; one team-added tag in `tags.yaml` is backfilled over stored findings; and one seen-versus-started chain links a visible failure to the step where it started.

### Implementation sequence through Stage 2

The steps below are done in this order. **Gate** marks a step that waits for the owner; nothing after a gate starts until the owner says yes. Each step ends with a check, and a step is not done until its check passes. Since 2026-10-24 (decision 5) the hourly run builds code in [sarkars/gort](https://github.com/sarkars/gort): one step per run, the first step whose status is not Done, one pull request per step. It stops at a Gate until the owner answers, and records each step's status in the Implementation status table below.

**A. Decisions and setup**

| # | Step | Output | Check |
|---|---|---|---|
| 1 | **Gate.** Owner decides repo name, public or private, licence (decision 1) and whether the hourly run writes code (decision 5). Decisions 2, 4 and 6 are gates on the steps that need them (3, 14 and 11) | Decisions written in section 9 | Done 2026-10-24: sarkars/gort, public, MIT; the hourly run may write code |
| 2 | Set up the `gortguard` Python package in the existing [sarkars/gort](https://github.com/sarkars/gort) repo (created by the owner 2026-10-24, MIT licence already on main): `pyproject.toml`, `src/gortguard/`, a `gort` command stub, CI that runs lint and unit tests (the pack checker joins CI at step 9) | Empty package that installs with `pip install -e .` | CI passes on an empty package |
| 2a | Presets and bundles (owner, 2026-10-24): `bundles.json` (JSON, not YAML, so the package needs no dependency) with presets, bundles, aliases and families; pattern data built from the library's failure taxonomy and each page's Starter rule; `gort bundles`, `gort show`, `gort search`, `gort build` (writes `gort-policy.md`: precedence line, one line per pattern with its Pattern ID, duplicates merged); `pack()` with `Preset` and `Bundle` constants. No model, no key | Commands and `pack().policy()` | Every chat family is in exactly one bundle or marked later; `gort search "transfer"` finds `handoff`; an unknown bundle name is an error; `gort build --preset support-bot` lists only its bundles' Pattern IDs; one unit test each |
| 3 | **Gate: decision 2 (frameworks).** Open each chosen framework's primary page; record its version and items. Open each outside failure library (section 5, "Failure sources"); record version, licence and fields | `frameworks/*.yaml` and `sources/*.yaml`, with the date opened | Every item has a source link; every source has a licence or "not yet read" |
| 3a | Coverage check: map taxonomy v1 to the AI Incident Database cases and to the MIT repository's risks about people and AI; list patterns with no real case and risks with no pattern | `coverage/human-ai.md` | Every taxonomy entry has a case link or "no public case found" |

**B. Formats, defined before any content or code**

| # | Step | Output | Check |
|---|---|---|---|
| 4 | Pack format: the seven parts, eval templates, guardrail (kind, check point, condition, action, blank limits), framework mapping | Schema file and two hand-written example packs entries | Both examples load against the schema |
| 5 | `agent.yaml` format: prompt, tools with risk tags, retrieval sources, memory, channels, agent types, languages, team-added tags | Schema file and an example for a refund agent | Example loads |
| 6 | Record format for Stage 2, defined now so Stage 1 guardrails write what Stage 2 reads: Run, Step, Finding, mapped to the OpenTelemetry GenAI conventions and OpenInference spans, with the chat event schema v0.1 as the interface layer; the eleven tag families and the `tags.yaml` format | Schema files and a mapping table | One synthetic chat run and one synthetic tool run convert to records with every family present or `unknown` |
| 7 | Pilot: all seven parts for 50 patterns from taxonomy v1, at least 30 of them Human-AI interaction patterns, the rest spread across agent types; count `rule`, `judge` and no guardrail, and evals that need a simulated user | Pilot packs and a one-page count | **Gate.** Owner reviews the count and the format changes it caused |
| 8 | Comparison of eval runners, simulated-user tools and rule engines against the criteria in section 5 (Formats), with each tool's docs opened | One-page comparison with a recommendation | **Gate.** Owner approves the choice (decision 3) |

**C. Stage 1 build**

| # | Step | Output | Check |
|---|---|---|---|
| 9 | Pack checker | `gort check` | Fails on a pack entry with a missing part or an eval without a pass and a fail; passes on the pilot packs |
| 10 | Core package: `pack()`, `prompt()` with size budget and conflict check, reply check (including streaming), retrieval, memory, tool (`@p.guard`), handoff and run guardrails; time budget and fail-through or hold policy; log-only mode; redaction. Every guardrail verdict is written as a Step with its Guard tags | `gortguard` core | One unit test per guardrail; a timing test per check point; redaction test with planted personal data |
| 11 | **Gate: decision 6 (model API key and spend limit).** `gort init`: reads or imports `agent.yaml`, ranks failures, asks setup questions, leaves limits blank, generates eval cases from templates for a person to review, saves cases in the team's repo | `gort init` | On the example refund agent: top failures listed, prompt text within budget, cases generated and saved only after review |
| 12 | `gort test`: runs cases on the chosen runner, per model, with a cost cap, simulated user for multi-turn cases, CI exit code, HTML report | `gort test` | Fails CI on a planted failure; stops at the cost cap |
| 13 | Reference agents for wave A: one conversational, one action, each with switches that plant known failures; at least ten switches replay incident pages (for example a binding price offer, an invented refund policy, a request for a person ignored) | Two small agents in the repo | Each runs with switches on and off |
| 14 | **Gate: decision 4 (mapping reviewer).** Wave A packs: base, conversational, action, with framework mappings reviewed by the second person and a coverage page per pack | Pack files, coverage pages | `gort check` passes; reviewer signs off the mappings |
| 15 | Wave A verification against the Stage 1 done-when; then review queue, alert webhook, `gort evidence`, pack versions and signatures, exporters | Release `0.1` | Stage 1 done-when holds for wave A |
| 16 | **Gate.** Design partner installs `0.1` in log-only mode | Partner's guardrail hit rates and eval pass rates, before and after | Numbers reported as log-only; no real-world effect claimed |
| 17 | Wave B (document, knowledge): steps 13 to 15 for these types | Release `0.2` | Stage 1 done-when holds for wave B |

Wave C (operations, coding, multi-agent) follows the same steps later. Chat layer first (owner, 2026-10-24): steps 13 to 24 run first on the conversational chat reference agent only; the action agent, wave B, wave C and the four-type Stage 2 done-when come after the chat layer works.

**D. Stage 2 build**

| # | Step | Output | Check |
|---|---|---|---|
| 18 | Import: conversation logs, OpenTelemetry and OpenInference files to Run and Step records; redaction on import; optional outcomes table joined by run ID or idempotency key | `gort observe` input side | Reference-agent traces from all four types import with no lost steps; planted personal data is redacted |
| 19 | Tags: `tags.yaml` loader, the eleven-family catalog, `field`, `map` and `computed` sources (`model` returns `unknown` until Stage 4), `unknown` and `clean` values, multi-valued tags, hierarchies, backfill | Tag engine | Every record carries all families; a team-added tag backfills over stored findings |
| 20 | Detectors from the packs, starting with Human-AI interaction: each uses its taxonomy v1 detection signals and event schema fields (for example `bot.assumption_stated`, `bot.claims_done`, `user_label.request_for_person`); rule detectors first, then judge detectors that use the pattern page as rubric and must quote evidence or the finding is dropped; every detector `not measured` | Detectors for waves A and B | Each planted failure in the reference agents is found; a judge finding with no quote is dropped |
| 21 | Seen versus started: link a visible failure to the earliest failing step | Cause-and-effect links on findings | One planted chain (stale index, empty retrieval, dead-end reply) gives three linked findings with the fix tag on the index |
| 22 | Storage and reports: Parquet and DuckDB; `gort report` with group-by, filter and saved views; trends; webhook alert on a rate jump; honesty line on every report | `gort report` | A report grouped by agent type and release; a saved view re-runs with the same result |
| 23 | Stage 2 verification against its done-when, on the four reference agents | Release `0.3` | Stage 2 done-when holds, including one "said versus done" finding through the outcomes join |
| 24 | **Gate.** If the design partner shares logs, run `gort observe` on them | Partner report | Without partner logs, every report says it is on reference agents only |

**Stop after step 24.** Stage 3 starts only when the owner says so and there is someone to label findings.

### Implementation status

The hourly run updates the row of the step it works on. Status is `Not started`, `In progress (PR link)`, `Waiting for the owner: <gate>`, or `Done (PR link, date)`.

| Step | Status |
|---|---|
| 1 | Done (owner, 2026-10-24) |
| 2 | Waiting for the owner: the run's GitHub token has no `workflow` scope, so the CI file could not be pushed; run `gh auth refresh -s workflow` on the run PC or add `.github/workflows/ci.yml` from the PR description ([PR 1](https://github.com/sarkars/gort/pull/1), opened 2026-10-24, not merged) |
| 2a | Built 2026-10-24 in [sarkars/gort PR 2](https://github.com/sarkars/gort/pull/2), stacked on step 2; Check passes locally (7 tests); not merged until CI can run (step 2 workflow scope) |
| 3 | Not started |
| 3a | Not started |
| 4 | Not started |
| 5 | Not started |
| 6 | Not started |
| 7 | Not started |
| 8 | Not started |
| 9 | Not started |
| 10 | Not started |
| 11 | Not started |
| 12 | Not started |
| 13 | Not started |
| 14 | Not started |
| 15 | Not started |
| 16 | Not started |
| 17 | Not started |
| 18 | Not started |
| 19 | Not started |
| 20 | Not started |
| 21 | Not started |
| 22 | Not started |
| 23 | Not started |
| 24 | Not started |

## 7. Stage 3: Learning (GORT: Repair)
**Useful on its own:** the team's checks get sharper every week, and it knows which fixes worked.

```bash
gort label report/findings.csv     # a person marks each finding confirmed or rejected
gort learn report/                 # turns confirmed findings into eval cases and pack updates
```

- **Tagging by people.** `gort label` shows each finding with its automatic tags, and a person confirms or corrects them. Every tag records who set it and when.
  - **Verdict:** `confirmed`, `rejected` (with a reason: wrong pattern, not a failure, evidence does not support it), or `failure no pattern covers`.
  - **What failed:** the pattern, corrected when the detector named the wrong one; `unknown` findings get a pattern or become a new pattern candidate.
  - **Cause:** the root cause, from the pattern page's list or `other` with a note; and the step where it started, when the automatic seen-versus-started chain missed it.
  - **Impact and risk:** what followed and how bad it was, when the automatic value is wrong or `unknown`.
  - **Fix:** where the fix belongs, owning team, fix status, and the release it shipped in, so before-and-after can be measured.
  - **Business:** entity, action or policy rule, when Stage 4 facts do not exist yet or got it wrong.
  - **Data source:** `real` or `simulated`, so simulated variations never count toward real rates.

  A sample of labels is checked by a second person; where the two disagree, both tags are shown, not averaged away.
- **Tag accuracy.** Automatic tags are measured like detectors: people's corrections give each automatic tag (intent, layer, severity, harm type, fix destination, business entity) an accuracy figure. A report grouped by a tag shows that tag's accuracy, and a tag with too few checked values is marked `not measured`.
- **Suggested tags.** Once a team has labelled enough findings, GORT suggests the cause, impact, fix destination and owning team for new findings. A person accepts or changes each suggestion; suggested tags are marked as suggested until then.
- **Learning by tag.** Every bullet below can be split by any tag: detector accuracy by agent type or language, fix effect by release, guardrail tuning by risk tag, recurring failures by owning team.
- **Detector accuracy:** labels give each detector precision and recall ([S0 study](../reference/studies/s0-do-our-detectors-agree-with-people.md)). A detector stays "not measured" until its numbers are published.
- **Regression tests:** each confirmed failure becomes an eval case (redacted) in the team's copy of the pack, so it cannot come back silently. A simulated-user tool generates variations of it (other wording, other tools, other errors) to test that the fix holds beyond the one case. Simulated results are labeled as simulated and never reported as real rates.
- **Guardrail tuning:** confirmed and rejected findings show which guardrails fire too often or too rarely; thresholds change only with a person's approval.
- **Fix effect:** before and after a fix ships, the rate of that failure, with the pattern's counter-metric (from its "don't over-correct" line) so a fix that causes a new problem is seen.
- **Pack updates:** which prompt text and rules actually reduced failures, per agent type. Changes go to the shared packs only by pull request and a person's review, and only from teams that opt in, as aggregates with no customer text.
- **New patterns:** confirmed failures that fit no pattern become candidate pages for the library, through the usual review.
- **Suggested limits:** from real data, for example "99% of refunds are under $120; set the refund limit to 200?". A person approves every suggestion.

**Done when:** labeled findings from two agent types, with verdict, cause, impact, fix and data-source tags set or confirmed by people and a second-person check on a sample, and an accuracy figure for at least three automatic tags, give measured precision and recall for at least five detectors, one confirmed failure has become a passing regression test after its fix, and the before-and-after view shows the fix's effect and counter-metric.

## 8. Stage 4: Business learning (GORT: Repair)
**Useful on its own** only together with an earlier stage, which is why it comes last: it makes every earlier stage specific to the business.

- **Sources:** website and help pages with [Trafilatura](https://github.com/adbar/trafilatura) (Apache 2.0); policy docs, PRDs, decks and spreadsheets with [Docling](https://github.com/docling-project/docling) (MIT). Each source stored with its version.
- **`facts.yaml`:** entities, actions, preconditions, policy rules, limits and routes, drafted by a model from the sources with the source passage on every fact. Facts start `proposed`; a person approves them by editing and committing the file. When two sources disagree, both are kept and a person decides.
- **What each agent type gains:**

| Type | Business facts used | Example |
|---|---|---|
| Conversational | Policies, products, opening hours, routes to people | Eval case: agent must state the 30-day refund window correctly |
| Action | Preconditions and limits | Rule limit filled in from policy: "refunds over $100 need a manager" |
| Document | Required documents and fields | Checklist: the loan file must include two pay stubs |
| Knowledge | Approved sources and their owners | Detector: answer cites a page that is not an approved source |
| Operations | Runbooks and the approved action list | Rule: only the actions in the runbook are allowed |
| Coding | Repository conventions and protected paths | Rule: no changes to the payments folder without review |
| Multi-agent | Which agent owns which decision | Detector: agent B made a decision owned by agent A |

- **Fix routing:** a failure against a correct approved fact is fixed in the agent; one caused by a wrong source is fixed in the source; a disagreement goes to the owner.

**Done when:** a reference company's sources become an approved `facts.yaml`, and one planted policy breach is caught by a Stage 1 eval case and by a Stage 2 detector, for at least two agent types.

## 9. Decisions needed from the owner
1. Repo for packs and tools: name, public or private, and licence. The coverage pages can live in this library. **Answered 2026-10-24:** [sarkars/gort](https://github.com/sarkars/gort), public, MIT. Package `gortguard`, command `gort`.
2. Which frameworks are in the first coverage pages. Recommended: OWASP LLM 2025, OWASP Agentic 2026, NIST AI 600-1.
3. Approve a short comparison of eval runners, simulated-user tools and rule engines before any is picked (section 5, Formats).
4. Who reviews the framework mappings (a second person, ideally with security or compliance background).
5. Whether the hourly run may write pack content (content, allowed today) and, later, the checker and exporters (needs a change to the "no code" rule in `C:\Users\saura\.hmi-runner\prompt.md`). **Answered 2026-10-24:** yes. The hourly run writes code in sarkars/gort only, one step per run (prompt Part H). It never writes code in this library.
6. Model API access and a spend limit, as environment variables, for model-graded eval cases.
7. Trademark check for "GORT" and "gortguard" before a public launch.

## 10. Later, only when
Each item waits for the signal named. None is planned before it.

| Item | Add when |
|---|---|
| Framework integrations (OpenAI Agents SDK, Claude Agent SDK, LangChain, MCP) | A partner uses that framework and asks for it |
| Server mode or MCP proxy (also brings guardrails to no-code builders) | A partner cannot change agent code, builds in a no-code platform, or is not in Python |
| TypeScript package | A partner's agent is in TypeScript |
| Live traces (OTLP receiver) | A partner wants live analytics instead of file exports |
| Graph store for the business model | `facts.yaml` passes a few hundred facts |
| Unknown-failure clustering, root-cause linking | Stage 3 has enough labeled runs to test it |
| Self-hosted service, then a hosted one | A partner asks for scheduled runs and a review web page |
| OWASP AIVSS severity scores | AIVSS reaches a final version |

## 11. What the product never does
- Says an agent is "compliant" with any framework or law; it reports coverage and gaps, and flags legal items for legal review.
- Sends a message or runs an action on its own.
- Loads a pack whose signature does not check.
- Writes unredacted user text to its logs unless the team turned that on.
- Invents a business limit or treats a `proposed` fact as true.
- Copies text from paid standards.
- Stores raw personal text after redaction, or asks users for sensitive values.
- Publishes a customer's documents, facts or runs, or puts them in the public library.
- Groups results by protected or sensitive personal traits, or infers such traits from text.
- Puts a money figure on impact that the business did not set itself.
- Claims accuracy, savings or conversion it has not measured, or presents simulated results as real.
- Edits a pattern page or a shared pack without a pull request and a person's review.

## 12. Outside tools and sources named in this plan
Opened through search summaries 2026-10-22 and 2026-10-23. Each is checked on its primary page (version, licence, owner, activity) before use.

| Item | Used in | Note |
|---|---|---|
| [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/) | Stage 1 | |
| [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/) | Stage 1 | ASI01 is agent goal hijack, per secondary sources |
| [OWASP AI Testing Guide](https://owasp.org/projects/ai-testing-guide) | Stage 1 | v1, 2025-11-26 |
| [MITRE ATLAS](https://atlas.mitre.org/) | Stage 1 | |
| [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) and [NIST AI 600-1](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence) | Stage 1 | AI 600-1 still the July 2024 version |
| [ISO/IEC 42001:2023](https://www.iso.org/standard/81230.html) | Stage 1 | Paid; clause references only |
| [EU AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) | Stage 1 | Legal review flag on every mapping |
| [Microsoft Guidelines for Human-AI Interaction](https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/), [Google People + AI Guidebook](https://pair.withgoogle.com/guidebook/), [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Stage 1 | Conversational pack |
| [AI Incident Database](https://incidentdatabase.ai/), [MIT AI Risk Repository](https://airisk.mit.edu/), [AIAAIC Repository](https://www.aiaaic.org/aiaaic-repository) | Stage 1 sources, coverage check | Opened 2026-10-23; AIID licence and AIAAIC terms not yet read; MIT data CC BY 4.0 |
| Eval runners: promptfoo, DeepEval, Inspect | Stage 1 exporter | Candidates for the comparison; not yet checked |
| Rule engines: [Amazon Bedrock AgentCore Policy](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-getting-started.html) (Cedar), [Invariant Guardrails](https://explorer.invariantlabs.ai/docs/guardrails) (Apache-2.0, owned by Snyk per a secondary source), framework approval hooks | Stage 1 exporter | Candidates for the comparison; AgentCore is AWS only |
| [Guardrails AI](https://github.com/guardrails-ai/guardrails) | Not used | Checks text, not actions; hub retired 2026-08-25; company acquired by Harvey 2026-09-09, open-source future not stated |
| [OpenTelemetry GenAI conventions](https://github.com/open-telemetry/semantic-conventions-genai), [OpenInference](https://github.com/Arize-ai/openinference) | Stage 2 | Trace formats; a convention version is pinned |
| Parquet, DuckDB | Stage 2 | Licences checked before use |
| [Trafilatura](https://github.com/adbar/trafilatura), [Docling](https://github.com/docling-project/docling) | Stage 4 | Apache 2.0; MIT |

## Related
- Superseded, background only: [Chat analytics plan](chat-analytics-plan.md) · [Code module design](code-module-design.md) · [Learning agent](learning-agent.md)
- [Code repo: sarkars/gort](https://github.com/sarkars/gort) · [Event schema](specs/conversation-event-schema-v0.1.md) · [Failure taxonomy](specs/failure-taxonomy-v1.md) · [Distribution plan](distribution-plan.md) · [Agents by business goal](../../../by-agent/README.md)
