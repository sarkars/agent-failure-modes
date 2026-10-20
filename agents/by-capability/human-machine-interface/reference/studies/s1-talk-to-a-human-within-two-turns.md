# Study S1 (preregistration): how often do chatbots honor "talk to a human" within two turns?

This page is the preregistered protocol for study S1, written for developers, conversation designers and researchers who want to check or reproduce how often a simulated customer who asks a chatbot for a person gets a transfer, a callback or a real route within two bot turns.

> **Status: Designed, not run. No results exist.** Written 2026-10-20 and not yet reviewed. Every threshold below is a starting point we chose before seeing data. None comes from a source. The study uses simulated users on reference bots we configure; it says nothing about real customers or any commercial product.

## 1. Research question
When a simulated customer clearly asks for a person, in how many conversations does a reference chatbot hand off, create a callback or ticket with a time, or state a concrete route, by the end of its second reply? How does that rate change with the bot's configuration, the underlying model, and the situation (staffed, not staffed, no account)?

This is study S1 in the [chat analytics plan](../../roadmap/chat-analytics-plan.md). Its metric is the primary metric of [talk-to-a-human-ignored-or-looped](../../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md), human-request fulfillment within 2 bot turns. Terms follow the [glossary](../glossary.md) and [metrics](../metrics.md); the handoff rate there counts requests and completed handoffs separately, and so does this study.

## 2. Hypotheses
Each hypothesis can be wrong. "Honor rate" is defined in section 4. Differences are in percentage points (pp). The 10 pp and 90% marks are our pre-stated starting points, not findings.

| # | Hypothesis | Pattern ID(s) tested | Falsified if |
|---|---|---|---|
| H1 | With a generic support prompt and no handoff instruction (configuration C0), the pooled honor rate is below 90%. | `talk-to-a-human-ignored-or-looped` | The pooled C0 honor rate is 90% or higher, with a 95% interval lower bound of 85% or higher. |
| H2 | Adding the pattern page's prompt block (C2) raises the pooled honor rate over C0 by 10 pp or more. | `talk-to-a-human-ignored-or-looped` | The C2 minus C0 difference is under 10 pp, or its 95% interval includes 0. |
| H3 | Configuration moves the honor rate more than the choice of model does. The pattern page's answer to "will a better model fix this?" is "No (our judgment, not tested)". | `talk-to-a-human-ignored-or-looped` | Within C0, the gap between the best and worst model is larger than the pooled C0 to C2 gap. |
| H4 | Out-of-hours requests (nobody staffed) are honored at least 10 pp less often than in-hours requests under C0 and C1, because the bot says a person will come but offers no callback or time. | `handoff-outside-staffed-hours-with-no-alternative` | The in-hours minus out-of-hours gap is under 10 pp, or its interval includes 0, under either C0 or C1. |
| H5 | A requester who says they have no account or cannot log in is honored at least 10 pp less often than a plain requester under C0, because the bot asks for a login first. | `forces-a-fresh-login` | The plain minus no-account gap is under 10 pp, or its interval includes 0. |
| H6 | Counter-effect: C2 does not raise false transfers on decoy messages ("I'm an insurance agent, can I get a bulk quote?") by more than 5 pp over C0. | `escalates-too-early-or-too-late` | C2 raises the decoy transfer rate by more than 5 pp over C0, with an interval excluding 0. |

## 3. Design
### 3.1 Simulated users
- **One simulator prompt, versioned.** An LLM plays a customer with a persona (name, goal, tone), a patience level, and a scripted list of request wordings. The wordings are fixed per scenario and not left to the LLM, so the request is always clear and identical across bots.
- **Scripted second request.** If bot turn 1 does not honor the request, the simulated customer's next message repeats the request in different scripted wording (and may answer the bot's question first). It never drops the request before bot turn 2.
- **Why scripted.** LLM user simulators have known faults. One published simulator study reports the simulated user ending dialogues early, before all goals were met ([Davidson et al., 2023](https://arxiv.org/abs/2309.13233)). Scripting the scored turns removes that failure where it matters.
- Temperature, seed, simulator model and prompt are recorded for every run.

### 3.2 Scenario set
Twelve scenario families, adapted from the [12 test conversations](../../tests/talk-to-a-human-ignored-or-looped.md) for this pattern (not yet run). Each has a US setting (for example a utility billing bot, a bank card-dispute bot, a telecom plan bot) and several request wordings.

| Family | Situation | Counted in the honor rate? |
|---|---|---|
| A. Plain ask | "I need to talk to a person." Staffed | Yes |
| B. One word | "agent" | Yes |
| C. Asked after a failed try | The bot answers a billing question, then the customer asks for a person | Yes |
| D. Disguised as a question | "Can I speak to someone about this?" | Yes |
| E. Out of hours | Nobody staffed; a callback or ticket exists | Yes (alternative route required) |
| F. No account | Customer has no account or is locked out | Yes (route must work without login) |
| G. Handoff tool errors | The transfer returns an error | Yes (another route required) |
| H. Callback ask | "Call me instead." | Yes |
| I. Frustration, no explicit ask | "This is useless, I've asked three times." | No: reported separately as unprompted offers |
| J. Decoy: insurance agent | Contains "agent", asks for a quote | No: scored for false transfers |
| K. Decoy: bot can answer | "What are your hours?" | No: scored for false transfers |
| L. Decoy: travel agent | "Cancel my travel agent booking" | No: scored for false transfers |

The scenario files, personas and wordings are published before the run.

### 3.3 Reference bots, by configuration
We name configurations, not vendors, and publish no ranking of commercial products. Models are listed by exact version string when the run is registered: at least three, from at least two providers, plus one run locally.

| Config | What it is |
|---|---|
| C0 | Generic support system prompt for the scenario's business. No instruction about people. |
| C1 | C0 plus one sentence: "If the customer asks for a person, connect them." |
| C2 | C0 plus the prompt block and decision table from the pattern page's fix. |
| C3 | C2 plus `transfer_to_agent` and `create_callback` tools, with staffing state passed in. |
| C4 | A scripted menu bot with a fallback and no LLM, as a deterministic baseline. Its handoff keywords are published. |

### 3.4 Variables
- **Independent:** configuration (C0 to C4), model (C0 to C3), scenario family, request wording, staffed or not.
- **Controlled:** simulator prompt and model, scenario text, tool behavior, conversation cap (8 bot turns), seed list.
- **Dependent:** honored at bot turn 1, honored by bot turn 2, never honored within the cap, false transfer on decoys.

## 4. What counts as honoring the request
### 4.1 Turn counting (exact)
1. A **user turn** is one user message, or several user messages sent with no bot message between them.
2. A **bot turn** is all bot output between two user turns. Several messages, tool calls and system notices in that span are one turn. A typing indicator is not a turn.
3. The **request turn** is the first user turn containing a clear request for a person. The scenario script fixes it, so it is known in advance.
4. **Bot turn 1** is the bot output right after the request turn. **Bot turn 2** is the bot output after the next user turn. Nothing later counts toward the two-turn rate.
5. If bot turn 1 honors the request, the scripted second request is not sent. The conversation is scored "honored at turn 1", which also counts as "by turn 2".
6. Each conversation is scored once. If the bot honors at turn 3 or later, the conversation is "not honored by turn 2" and its turn number is recorded.

### 4.2 Qualifying actions
A bot turn honors the request if it contains at least one of:
- **Transfer:** a recorded `handoff` event to a person or queue (a tool call in C3, or an explicit "connecting you now" with the handoff logged by the harness).
- **Callback, ticket or email created**, with the contact detail confirmed and a stated time window.
- **Stated route:** a named channel plus a way to use it (a phone number with hours, or a chat link that needs no login) and when someone answers.

These do **not** count: a menu, a diagnostic question in place of an answer, "I can help with that", a link to FAQ pages, "please call us" with no number, or a route that needs a login the scenario says the customer lacks. One short offer to try helping first is allowed only when the qualifying action is in the same bot turn.

### 4.3 Scoring rule
- **Honor rate (primary)** = conversations in counted families honored by bot turn 2, divided by conversations in counted families.
- **Turn-1 rate** = honored at bot turn 1, divided by the same denominator.
- **False transfer rate (counter-metric)** = decoy conversations (J, K, L) where the bot transfers or offers a person, divided by decoy conversations.
- A conversation that errors out or hits the cap with no honor counts as not honored. Missing runs are reported, never dropped.

### 4.4 Human-label check (S0 and S6 tie-in)
- Scoring is rule-based first (tool events, patterns for phone numbers and times), then an LLM judge for text-only routes. The judge prompt and model are published.
- Before any result is published, two people independently label a random 10% of conversations plus every conversation where rule and judge disagree. A third person settles disagreements.
- The judge's precision, recall and agreement come from study S0. If agreement with people is below 0.70 (our starting point), S1 is published labeled "experimental" and the human labels, not the judge, give the headline numbers.
- Study S6 compares simulated-user behavior with human participants. If S6 has not run when S1 publishes, S1 says so on its first line and claims nothing about real users.

## 5. Analysis plan
- **Primary metric:** honor rate by bot turn 2, per configuration and model, pooled and per scenario family.
- **Counter-metric:** false transfer rate on decoys (H6). A configuration that raises the honor rate and the false transfer rate together is reported as a trade, not a win. Turn-1 rate is also reported, because "within 2 turns" can hide a bot that needs a second ask.
- **Sample size (starting point):** 20 seeds per scenario, wording and cell. If an interval in a main comparison is wider than 15 pp, we add seeds from a pre-listed range and say so.
- **Intervals:** every proportion carries a 95% Wilson score interval. Seeds within one scenario are not independent, so pooled rates and all differences also carry a 95% interval from a bootstrap that resamples scenario families, then seeds within them (10,000 resamples). Both are reported. A difference is never shown without its interval. P-values are not the headline.
- **Falsification:** each hypothesis has its rule in section 2. We apply it as written and do not move thresholds after seeing data.
- **We report even if null:** if C0 already honors at 90% or more (H1), if the prompt block does little (H2), if model matters more than configuration (H3), or if the prompt block raises false transfers (H6), we publish that with the same prominence.
- **Exploratory results** (anything outside section 2, such as per-model rankings of families) are labeled exploratory and kept out of the headline.

## 6. Threats to validity
- **Simulator realism.** Simulated customers are not people, and scripted requests are cleaner than many real ones. Davidson et al. report that system performance fell as goals got more complex, so our scenarios keep to one goal. Only S6 can say how far results carry.
- **Prompt sensitivity.** We write C0 to C3. Another wording of "generic support prompt" could change C0. We publish every prompt and run one alternate C0 wording as a check.
- **Judge error.** Section 4.4 limits it and does not remove it.
- **Setting.** English, US, text chat. Real deployments have routing, queues and policies we do not model.
- **Simulated staffing and tools.** A real transfer can fail in ways the harness does not.
- **Models change.** Hosted models are updated. We record version strings and dates, and the result is a snapshot.
- **Author bias.** The authors wrote the pattern whose fix is tested in H2 and H6. Rules and materials are published so others can check.
- **Scenario choice.** Families come from our own test file, chosen before any run. We publish all of them, including ones we expect bots to pass.

## 7. Prior work and how it shapes the design
- Nielsen Norman Group's article on site-specific AI chatbots says a bot should never gatekeep when the user explicitly asks to be connected to a human, and shows a bot that did not offer a handoff after three requests in different words ([Kenderova and Kohler, NN/g](https://www.nngroup.com/articles/dimensions-of-ai-chatbots)). The text we read gives no sample size or study date, so it is a qualitative example, not a rate. It is why family B and the repeat wording exist.
- Liu et al. propose a model that predicts when a chatbot should hand a conversation to a person, and a tolerance-based metric for the timing ([AAAI-21, "Time to Transfer"](https://ojs.aaai.org/index.php/AAAI/article/view/16731/16538)). It addresses bot-detected transfers; S1 addresses user requests. We borrow only the idea that handoff timing should be scored, and keep the library's exact two-turn rule.
- Davidson et al. describe an in-context-learning user simulator for task-oriented dialogue, a human dataset for comparison, and a premature-termination fault ([arXiv 2309.13233](https://arxiv.org/abs/2309.13233)). From it we took checking the simulator against people, which becomes S6, and scripting the request turns.
- The library's [evidence review](../../roadmap/evidence/why-people-leave-chatbots.md) covers a regulator report on bank chatbots with no route to a person. It describes complaints, not a measured rate. We found no opened study that measures how often chatbots honor such a request across configurations, so H1 has no sourced baseline.

## 8. Out of scope
- **Voice agents.** Interruptions, speech errors and phone menus are different. Voice is planned, not covered.
- **Web analytics** (clicks, page flows, widgets).
- Real customers, live traffic and real transcripts.
- What happens after the handoff, including the summary and what the person sees ([cold-transfer](../../goals/human-handoff/failures/cold-transfer.md)). S1 scores only whether the request was honored.
- Whether the bot should offer a person unprompted (family I is reported separately, outside the primary metric).
- Naming or ranking commercial chatbots. That needs a reproducible, permitted and fair design first, per the analytics plan.

## 9. Data and materials to be published
Before the run, with a frozen date: this protocol, scenarios and wordings, personas, simulator prompt, C0 to C4 prompts and tool definitions, scoring code, seed list and judge prompt. After the run: raw transcripts (all synthetic, no personal data), event logs with scores, human labels with labeler notes, model version strings and run dates, analysis code, and a results page that follows section 5. License and repository location are open decisions for the owner.

## 10. Changes log
| Date | Change |
|---|---|
| 2026-10-20 | First draft of the protocol. Not run. Sources opened for it: NN/g article, Davidson et al., Liu et al. |

## Related
[Chat analytics plan](../../roadmap/chat-analytics-plan.md) · [Distribution plan](../../roadmap/distribution-plan.md) · [Glossary](../glossary.md) · [Metrics](../metrics.md) · [Talk to a human ignored or looped](../../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md) · [Failure taxonomy](../../roadmap/specs/failure-taxonomy-v1.md)
