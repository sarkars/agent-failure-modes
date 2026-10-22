# Study S4 (preregistration): do opening messages change early drop-off?

This page is the preregistered protocol for study S4, written for developers, conversation designers and researchers who want to check or reproduce how five kinds of first message compare on whether a user starts a conversation and finishes a first task, first with simulated users and then with a small human panel that checks whether the simulation matches.

> **Status: Designed, not run. No results exist.** Written 2026-10-22 and not yet reviewed. Thresholds are starting points we chose, not from sources. Simulated results are not results on real users and are never reported as such. The human panel sees a mock-up, not a live product. S4 says nothing about any commercial product.

## 1. Research question
When the same in-app assistant opens with a generic greeting, a capability card, a context-aware opener, both together, or a light joke, does the share of users who start a conversation change, and does the share who complete a first task change? What does a better opener cost (a wrong guess, a sensitive inference, a longer message)? And does a simulated-user ranking of the openers match what a small panel of people does with the same mock-ups?

This is study S4 in the [chat analytics plan](../../roadmap/chat-analytics-plan.md) ("several openers on a common task; simulated engagement, then a small human panel to check whether the simulation matches"). It tests the fixes of [generic-first-response](../../goals/embedded-copilots/failures/generic-first-response.md) and [doesn-t-say-what-it-can-do](../../goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md). Their test files ([one](../../tests/generic-first-response.md), [two](../../tests/doesn-t-say-what-it-can-do.md)) are not yet run. Terms follow the [glossary](../glossary.md) and [metrics](../metrics.md). The evidence review ([why people leave chatbots](../../roadmap/evidence/why-people-leave-chatbots.md)) has no opened study on greetings, so S4 has no sourced baseline.

## 2. Hypotheses
Each hypothesis can be wrong. Differences are in percentage points (pp). All marks (10 pp, 5 pp, 20%, 0.6, 7 points) are starting points we chose before seeing data. Openers O0 to O4 are defined in section 3.2, measures in section 4.

| # | Hypothesis | Pattern ID(s) tested | Falsified if |
|---|---|---|---|
| H1 | Simulated: the context-aware opener (O2) raises the start rate by 10 pp or more over the generic opener (O0), in scenarios where context exists (C1, C3, D1). | `generic-first-response` | The O2 minus O0 start-rate difference is under 10 pp, or its 95% interval includes 0. |
| H2 | Simulated: the capability card (O1) raises the start rate by 5 pp or more over O0 in the no-context scenario (C2). | `doesn-t-say-what-it-can-do` | The O1 minus O0 difference in C2 is under 5 pp, or its interval includes 0. |
| H3 | Simulated: first-task success within 6 bot turns is higher for O3 (context plus capability plus person route) than for O0 by 10 pp or more, pooled. | `generic-first-response`, `doesn-t-say-what-it-can-do` | The O3 minus O0 difference is under 10 pp, or its interval includes 0. |
| H4 | The light joke (O4) does not move the simulated start rate: within 5 pp of O0 in every scenario. | `generic-first-response` | Any scenario's O4 minus O0 difference is 5 pp or more, with an interval excluding 0. |
| H5 | Counter-effect: when the user came for a different reason than the context suggests (C3), the wrong-guess rate of O2 and O3 stays under 20% (the generic-first-response page's starting target). | `generic-first-response`, `guessing-instead-of-asking` | The wrong-guess rate for O2 or O3 in C3 is 20% or higher, or the interval lower bound is above 15%. |
| H6 | Counter-effect: with sensitive context in the record (D1), O2 and O3 open with no inference about it. | `generic-first-response` | Any O2 or O3 opener in D1 names the sensitive item. |
| H7 | Validity: the simulated order of O0 to O4 by start rate matches the panel's order, Kendall tau of 0.6 or higher, and no simulated pairwise difference named in H1 or H2 has the opposite sign in the panel. | all above | Tau is under 0.6, or any H1 or H2 sign flips with a panel interval excluding 0. |
| H8 | Validity: simulated users start more often than panel participants on O0 by 10 pp or more. | `generic-first-response` | The simulated minus panel O0 start-rate difference is under 10 pp. |

## 3. Design
### 3.1 Reference product and scenarios
- **One invented product.** The "Harbor Fitness" membership app has an in-app assistant with four tools: look up invoices, change the billing date, freeze a membership, book a class. It cannot change a plan. A person can. After the opener, every arm uses the same bot logic and the same replies. Only the opening message differs.
- **Four scenarios,** each a mock-up screen plus a record of what the app knows:

| ID | Screen and record | User's real goal | What it tests |
|---|---|---|---|
| C1 | Billing page, failed payment on Oct 18 | Fix the payment | Context matches the goal |
| C2 | Account home, nothing notable | Vague: "just looking, what is this?" | No context, vague goal |
| C3 | Billing page, failed payment on Oct 18 | Freeze the membership, not pay | Context does not match (wrong guess) |
| D1 | Account page, membership frozen with a "medical leave" note | Book a class | Sensitive context in the record |

### 3.2 Openers (arms)
We name wordings, not vendors. All five say "AI" in the same words, so disclosure is held constant (disclosure moved outcomes in the studies in the [evidence review](../../roadmap/evidence/why-people-leave-chatbots.md)). All text is published before the run.

| Arm | Opener (abbreviated) |
|---|---|
| O0 | "Hi! I'm the Harbor assistant, an AI. How can I help you today?" |
| O1 | O0's first line, then what it can do (from the tool list), what it cannot, and three starters from the tool list, not the screen. |
| O2 | One sentence naming what the app sees ("your payment on October 18 didn't go through"), up to three likely steps plus "Something else". No capability line. With no usable context (C2) it falls back to the pattern's one-line capability sentence. |
| O3 | O2 plus the capability line and an offer to reach a person. Same C2 fallback. |
| O4 | O0 plus a light joke about the assistant ("great with invoices, bad with jokes"). No context, no capability list. |

Because O2 and O3 collapse toward O1 in C2, H1 and H3 use the scenarios with context (C1, C3, D1, and C2 for O1 against O0 and O4 only).

### 3.3 Simulated users
- **LLM simulator, versioned.** An LLM plays a user from a persona: goal (scenario), vagueness (clear or vague), AI experience (low or high), and patience. It reads the opener and chooses one action: type a message, tap a starter, or close. It must give a one-sentence reason, which we log. The start rule is not coded in, so the opener's effect is the simulator's behavior, not our assumption. After the first action, the scripted bot answers and the simulator plays on until the task is done, it stops, or 6 bot turns pass.
- **Two or more simulator models,** from at least two providers, named by exact version at registration. Temperature, seed and prompt are recorded.
- **Why this needs a panel.** [Seshadri et al. (2026)](https://arxiv.org/abs/2601.17087) report that simulated users are unreliable proxies for people in agent tests (up to 9 pp swings by simulator model; different failure patterns). [Wang et al. (2025)](https://arxiv.org/abs/2509.17619) report significant behavioral differences between simulated and human users, including engagement. Both are abstract-level for us.

### 3.4 Human panel (small)
- **Mock-ups, not a live bot.** Each participant sees two scenarios (random order, random opener per scenario, no repeated opener) as a screen with the chat opened. They choose one: type a message (and type it), tap a starter, or close the chat. They then rate "I know what this assistant can do" and "It seemed to know too much about me", 1 to 7.
- **Size (starting point):** 30 views per opener per scenario in C1, C2, C3, which is 450 views and 225 participants. D1 is simulation only because it uses a sensitive record. An interval for one cell at n = 30 is about 30 pp wide, so the panel can confirm order and large gaps and cannot detect small ones. We say so in the results.
- **Recruitment, pay, consent and ethics review** are open decisions for the owner. No personal data is collected beyond a participant ID and age band.

### 3.5 Variables
- **Independent:** opener (O0 to O4), scenario, vagueness, AI experience, simulator model, seed.
- **Controlled:** post-opener bot logic, tool stubs, 6-bot-turn cap, mock-up layout, disclosure wording.
- **Dependent:** the measures in section 4.

## 4. What counts as correct
### 4.1 Measures (exact)
1. **Start:** the user types a message or taps a starter within the opener turn. Closing, or no action, is **not started**.
2. **Start rate (primary)** = started sessions divided by sessions opened.
3. **First-task success** = started sessions in which the stub logs the scripted goal as done, or the correct answer is given, within 6 bot turns, divided by sessions opened. Not started counts as not successful.
4. **Early drop-off** = sessions that end with zero user turns, or with one user turn and the task not done, divided by sessions opened. It is reported next to start rate because it also catches a user who starts and leaves after the first reply.
5. **Turns to first useful answer,** median, among started sessions.
6. **Opener length** in words, a cost.

### 4.2 Counter-metrics
- **Wrong-guess rate (H5):** in sessions where options were shown, the share followed by "something else" or a typed correction, from the event log, as in the generic-first-response page.
- **Sensitive inference (H6):** an opener that names the medical-leave note, by string match plus a person's check.
- **Felt too personal:** the 1 to 7 rating in the panel, and the simulator's stated reason for closing, tagged by a rule.
- **Capability accuracy:** after the opener, a scripted "can you change my plan?" turn, scored against the tool list.
- A variant that raises start rate and raises wrong guesses, "too personal" ratings or length together is reported as a trade, not a win.

### 4.3 Human-label check
Start, task and drop-off come from the event log and need no judge. The simulator's reasons are tagged by a rule, then by a judge, and two people label a random 10% plus every disagreement; a third settles ties. If judge agreement with people (from study S0) is below 0.70 (our starting point), the tagged reasons are labeled "experimental". The headline measures do not depend on the judge.

## 5. Analysis plan
- **Primary:** start rate and first-task success per opener, pooled over personas with equal weight, and per scenario, for each simulator model and for the panel. Simulated and panel results are shown side by side, never merged.
- **Sample size (starting point):** 4 scenarios, 5 openers, 4 persona cells (vagueness by experience), 20 seeds, which is 1,600 sessions per simulator model. If a main interval is wider than 15 pp, we add seeds from a pre-listed range and say so.
- **Intervals:** every proportion carries a 95% Wilson interval. Seeds within a persona are not independent, so differences also carry a 95% bootstrap interval that resamples personas, then seeds (10,000 resamples). Panel differences use a bootstrap that resamples participants. A difference is never shown without its interval.
- **Validity check (H7, H8):** Kendall tau between the simulated and panel order of openers per scenario; sign agreement of each pairwise difference; the size gap in O0 start rate. If tau is under 0.6, simulated results are published labeled "does not match people in this setting".
- **Falsification:** each rule in section 2 is applied as written. We do not move thresholds after seeing data.
- **We report even if null:** if O0 starts as often as O2 (H1), if the joke matters (H4), or if simulated and human orders disagree (H7), we publish that with the same prominence.
- **Exploratory** results (per-model rankings, persona effects, any comparison not in section 2) are labeled exploratory and kept out of the headline.

## 6. Limits and threats to validity
- **Simulators are not people.** The sources in section 7 say so. A tau of 0.6 is a weak match, and 225 participants cannot tell small effects from noise. Simulated lifts must not be quoted as lifts for real users.
- **The panel sees a mock-up.** A first click in a static screen is not behavior in a live product with its own habits, page load and prior use.
- **Panel is not your users.** An online panel may differ from a gym's members. Age band and AI experience are recorded, not balanced.
- **One invented product, English, US, text.** Voice and non-US greeting norms are outside S4.
- **We wrote the openers.** O2 and O3 are the fixes on our pattern pages. All wording is published. O4 is one joke, not humor in general.
- **First task is scripted,** and the post-opener bot is the same for all arms. A real bot's later turns can change the picture.
- **Simulator choice is part of the result.** Different simulator models may reorder the arms. We run at least two and report both.
- **Judge error** is limited in section 4.3, not removed.

## 7. Prior work and how it shapes the design
We counted three web searches on 2026-10-22 (greeting design and abandonment; opening message and capability disclosure; validity of simulated users). We opened six pages. The fetch tool returns a digest of a page, not raw text, so "opened" below means read through that digest. We found no opened study that compares greetings on abandonment in a live product, so H1 to H4 have no sourced baseline.
- **Zheng et al., [IceBreaker (arXiv 2604.18375)](https://arxiv.org/abs/2604.18375), April 2026.** Abstract page opened. It names a "first-message barrier" (a vague need, no explicit query) and reports online A/B gains on one large consumer assistant: active days +0.184%, click-through +9.425%. It concerns suggested starters, one company, not greetings in a support product. We tried the PDF and could not read it, so we did not verify the pattern page's "about 20%" no-start figure and do not use it.
- **Nielsen Norman Group, [New Users Need Support with Generative-AI Tools](https://www.nngroup.com/articles/new-ai-users-onboarding/), March 29, 2024.** Article opened. A qualitative study of 6 participants on 3 Chinese chatbots; users who could not tell what a tool did asked the bot about itself. It shapes the capability line and the capability-accuracy check. It shows a mechanism, not a rate.
- **Lekaviciute, Auruskeviciene and Reardon, [Should Your Chatbot Joke?](https://www.journals.vu.lt/omee/article/view/29887/31386) (2023).** Article page opened. A randomized online study on a fictional gift shop, 103 usable participants (57 humorous, 46 neutral), reporting higher engagement, attachment and a self-reported chance of sharing an email with a humorous greeting. It measured stated intent, not abandonment, and its authors note the small sample and brief interaction. It is why O4 exists and why H4 is a test and not an assumption.
- **Zurb, [Chatbot Welcome Messages](https://glare.zurb.com/docs/decision-map/measure/concepts/product-features/chatbot-welcome-messages).** Page opened; it has no date. It proposes scoring a welcome message on expectations, sentiment, success and intent, and shows one case (100 professionals) with high sentiment and low task success. A vendor case, not a controlled comparison. It supports reporting start and task success separately.
- **Seshadri et al., [Lost in Simulation (arXiv 2601.17087)](https://arxiv.org/abs/2601.17087), January 2026.** Abstract page opened. Simulated users as proxies for people in retail agent tasks: success varied by up to 9 pp across simulator models, simulated users misjudged difficulty, and the proxy was weakest for some dialect speakers. Not about openers. It is why two simulator models and a panel are in the design.
- **Wang et al., [Human vs. Agent in Task-Oriented Conversations (arXiv 2509.17619)](https://arxiv.org/abs/2509.17619), September 2025.** Abstract page opened. Reports significant behavioral differences between simulated and human users, including engagement and language style. It is why H8 asks for the gap.
- **Seen only in search summaries, not opened, not used:** vendor greeting blogs and documentation (including claims that a user's name or a persona lifts engagement), a trade-press note on polite bots, and two repository mirrors. Nothing from them is in the design.

## 8. Out of scope
- **Real customers, live traffic and A/B tests in production.** S4 supports no lift claim.
- **Whether disclosing "AI" changes outcomes.** Held constant here. The [evidence review](../../roadmap/evidence/why-people-leave-chatbots.md) covers the sources, and [undisclosed-bot-identity](../../goals/trust-and-rapport/failures/undisclosed-bot-identity.md) covers the pattern.
- **Proactive popups, invitation timing and voice greetings.**
- **Dark patterns and persuasion.** Openers that pressure the user are not tested.
- **Containment versus resolution** (study S5) and detector accuracy (study S0).
- Naming or ranking commercial chatbots.

## 9. Data and materials to be published
Before the run, with a frozen date: this protocol, the four scenarios and records, all five openers, persona prompts, simulator prompt, post-opener bot logic, panel instructions and mock-ups, scoring code, seed list and judge prompt. After the run: transcripts and event logs (all synthetic), the simulator's logged reasons, anonymized panel responses, scores, version strings, run dates and analysis code. License and repository are open decisions for the owner.

## 10. Changes log
| Date | Change |
|---|---|
| 2026-10-22 | First draft of the protocol. Not run. Sources opened: IceBreaker (abstract page), NN/g article, Lekaviciute et al. (article page), Zurb page, Seshadri et al. (abstract page), Wang et al. (abstract page). |

## Related
[Chat analytics plan](../../roadmap/chat-analytics-plan.md) · [S2 preregistration](s2-do-corrections-stick.md) · [S3 preregistration](s3-fallback-designs-compared.md) · [Glossary](../glossary.md) · [Metrics](../metrics.md) · [Generic first response](../../goals/embedded-copilots/failures/generic-first-response.md) · [Doesn't say what it can do](../../goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md) · [No likely-next-action suggestions](../../goals/embedded-copilots/failures/no-likely-next-action-suggestions.md) · [Guessing instead of asking](../../goals/dialogue-management/failures/guessing-instead-of-asking.md) · [Failure taxonomy](../../roadmap/specs/failure-taxonomy-v1.md)
