# Study S6 (preregistration): simulation validity

This page is the preregistered protocol for study S6, written for developers, conversation designers and researchers who read studies S1 to S5 and want to know how far their simulated users behave like people, measured by running a small panel of human participants through the same scenarios on the same reference bots.

> **Status: Designed, not run. No results exist.** Written 2026-10-22 and not yet reviewed. Thresholds and sample sizes are starting points we chose, not from sources. S6 compares simulated users with paid human participants on reference bots we configure, for invented companies. Participants are not customers, so S6 says nothing about real customers or any commercial product. The human panel needs owner approval, an ethics decision and a budget before it can run.

## 1. Research question
When people and simulated users get the same goal, on the same scenario, against the same reference bot, do they behave the same way at the moments S1 to S5 score? Where do they differ: how long they wait before leaving, how they word a request for a person, whether they catch a wrong summary, whether they say "yes, fixed" to a check, and how often they go off script? And for each headline comparison in S1 to S5 that can be replayed with people, does the direction of the result hold?

This is study S6 in the [chat analytics plan](../../roadmap/chat-analytics-plan.md) ("compare simulated-user behavior with a small set of human participants on the same scenarios"). The plan's risk table says every simulated result carries a validity note. S6 is where that note comes from. Terms follow the [glossary](../glossary.md) and [metrics](../metrics.md). S6 replays scenarios from [S1](s1-talk-to-a-human-within-two-turns.md), [S2](s2-do-corrections-stick.md), [S3](s3-fallback-designs-compared.md) and [S5](s5-containment-versus-confirmed-resolution.md). [S4](s4-opening-messages-and-early-drop-off.md) has its own panel check (its H7 and H8), so S6 reads S4's panel result and does not run openers again. Human labels of the transcripts reuse the guide and process of [S0](s0-do-our-detectors-agree-with-people.md).

## 2. Hypotheses
Each hypothesis can be wrong. Differences are in percentage points (pp). All marks (10 pp, 15 pp, 25%, 80%, 0.10) are starting points we chose before seeing data. "Sim" means the simulator each source study names as primary, run on the same goal card the person got. Scenario codes are defined in section 3.2.

| # | Hypothesis | Pattern ID(s) tested | Falsified if |
|---|---|---|---|
| H1 | Direction holds: in the human group, the S3 ladder (A2) still has lower abandonment than the generic fallback (A0), as the S3 simulator predicts. | `dead-end-i-don-t-understand-replies` | The human A0 minus A2 abandonment difference is 0 or below, or has the opposite sign of the simulated one with an interval excluding 0. |
| H2 | People run out of patience sooner than the S3 rule assumes: the human median count of consecutive no-progress bot turns before leaving, on A0, is under 3 (the S3 main setting p). | `dead-end-i-don-t-understand-replies` | The human median is 3 or more. |
| H3 | Scripted request wordings cover how people ask: on the same bot configuration, the honor rate on human-written requests for a person is within 10 pp of the rate on S1's scripted wordings. | `talk-to-a-human-ignored-or-looped` | The difference is more than 10 pp with an interval excluding 0. |
| H4 | People ask for a person without being told to: on S1 family I (frustration, no explicit ask), humans make an explicit request for a person 15 pp or more often than the LLM simulator does. | `talk-to-a-human-ignored-or-looped`, `escalates-too-early-or-too-late` | The human minus simulated difference is under 15 pp, or its interval includes 0. |
| H5 | People catch some stale summaries: when the S2 bot shows a summary with the old value, humans object before the action in at least 25% of those conversations. The S2 simulator, by design, never does. | `corrections-not-applied` | Humans object in under 25% of stale-summary conversations. |
| H6 | People say "yes, fixed" at a rate inside the S5 range: on the S5 checking bot (B0) with a correct fix, the human explicit-confirm rate falls between 0.3 and 0.9, the confirm propensities S5 varies. | `answer-and-go-conversation`, `survey-bias` | The human rate, with its interval, lies entirely below 0.3 or above 0.9. |
| H7 | People also confirm wrong answers: on the S5 wrong-answer bot (B2), humans say the issue is fixed in at least 10% of conversations, which the scripted S5 simulator never does. | `confident-wrong-answer-with-no-way-to-check`, `survey-bias` | Humans confirm a wrong answer in under 10% of B2 conversations. |
| H8 | Counter-effect on S0: detectors trained and checked on simulated text agree with people less on human transcripts; kappa on human transcripts is at least 0.10 lower than on simulated transcripts of the same scenarios. | `talk-to-a-human-ignored-or-looped`, `dead-end-i-don-t-understand-replies`, `corrections-not-applied` | The kappa drop is under 0.10 for every detector, or its interval includes 0. |

## 3. Design
### 3.1 Reference bots and simulated users (reused, not rebuilt)
- **Same bots.** S6 uses the reference bots of the source studies, frozen at the version each study registers: the S1 configurations C0 and C2 on one model, the S2 configurations C0 and C3 on one model, the S3 arms A0 and A2, and the S5 bots B0, B1 and B2. Settings are the source studies' invented companies, such as the "Brightwater Internet" support bot (invented). We name configurations, not vendors, and publish no ranking of commercial products.
- **Same simulators.** Each scenario runs with the simulator its source study names as primary (LLM-plus-script for S1 and S2, rule-based for S3 and S5). An unscripted LLM simulator, given only the goal card a person gets, runs on every scenario as a second comparison, on at least two models from two providers. Temperature, seed, simulator version and prompt are recorded.
- **Why both.** The scripted simulators fix the scored turns, so they can only be checked where people are free to differ. The unscripted simulator shows what an LLM does with the same freedom a person has.

### 3.2 Scenarios (a subset of S1, S2, S3 and S5)
| Code | Source | Scenario | Goal card says | What is compared |
|---|---|---|---|---|
| P1 | S1 family A | Plain ask, staffed | "You want to speak to a person about a billing charge." | Request wording, honor rate (H3) |
| P2 | S1 family I | Frustration, no explicit ask | "The bot's answers have not helped. Get your charge fixed." | Unprompted request for a person (H4) |
| P3 | S2 family A | Correct a date | "Book Monday, then change it to Tuesday before you finish." | Correction wording, stale-summary catch (H5) |
| P4 | S2 family D | Cascade | "Book Friday, then move it to Saturday. Check the total." | Stale-summary catch (H5) |
| P5 | S3 U2 | Partly understood | "Tell the bot your bill looks wrong, your own way." | Patience, abandonment (H1, H2) |
| P6 | S3 U4 | Unfinished message mid-task | "You are moving. Ask about it in pieces, as you would." | Patience, abandonment (H1, H2) |
| P7 | S5 billing, solvable | Correct fix shown | "Find out why your bill went up and fix it." | Confirm rate on B0 (H6), leaving without a word on B1 |
| P8 | S5 outage, wrong answer | B2 gives a wrong fix | "Your internet is down. Get it working." | Confirming a wrong answer (H7) |

Every goal card gives an invented name, address and account number, so no participant types real personal data. Cards say what the person wants, never how many turns to wait or what words to use. Cards are published before the run.

### 3.3 Human panel (small)
- **Who.** US adults, 18 or older, reading and writing English, who use chat support at least sometimes (self-reported). No other screen. Age band and self-rated AI experience are recorded, not balanced.
- **Recruitment** through an online research panel or a university participant pool. The owner chooses which. We make no promise about any vendor's population, quality or price.
- **Consent.** Before starting, each person reads that they will chat with test bots for invented companies, that the chats are recorded and may be published without names, that they must not type real personal data, and that they may stop at any time. They agree or leave.
- **Pay** is a flat amount per session, set by the owner before the run, paid in full whether the person finishes, leaves a chat or stops early. Leaving a chat costs them nothing, so pay does not reward staying.
- **Session.** Each person does four chats, one from each source study, in random order, each with a randomly assigned bot or arm. They type freely and may press "End chat" at any time. A chat also ends at the source study's turn cap. After each chat they answer one question: "Was your problem solved?" (yes, no, not sure).
- **Approval.** Recruitment, pay, consent wording, data retention and ethics review are open decisions for the owner. The plan lists human labeling capacity as a need for S0 and S6. S6 does not run until the owner approves a budget. Data handling follows [privacy, governance and access](../../roadmap/privacy-governance-and-access.md).

### 3.4 Variables
- **Independent:** user type (human, scripted simulator, unscripted LLM simulator), scenario P1 to P8, bot or arm, simulator model, seed.
- **Controlled:** bot versions, goal cards, turn caps, stubs, the post-chat question.
- **Dependent:** the behavior features in section 4.1, end states as each source study defines them, and S0 detector agreement.

## 4. What counts as a match
### 4.1 Behavior features (exact, one value per conversation)
1. **End state:** as the source study defines it (honored, end-state correct, recovered, handed off, abandoned, confirmed, dropped).
2. **No-progress turns before leaving:** consecutive no-progress bot turns (S3 rule 4.1.1) right before the user leaves. Missing if the user did not leave.
3. **Request for a person:** the user turn that first asks for a person, labeled by two people with the S0 guide.
4. **Stale-summary objection:** after a summary holding an old value, the user corrects it before the action.
5. **Explicit confirm:** a yes to a bot check, or a thanks that names the fix (S5 definition 4.1.2).
6. **Off-goal turn:** a user turn that neither answers the bot nor moves the goal (small talk, venting, a new topic). Two people label it.
7. **Message length:** words per user turn.

### 4.2 Match marks
- A **direction match** is a pairwise difference (arm against arm) with the same sign in the human and the simulated group.
- A **rate match** is a human and simulated rate within 10 pp, with the difference interval inside plus or minus 15 pp.
- Each source study gets one validity note from S6, published on its results page: **Holds** (direction match and rate match on its compared features), **Direction only** (direction match, rate mismatch), or **Does not hold** (a sign flip with an interval excluding 0). A study with no replayed comparison is noted **Not checked**.

### 4.3 Human labels
Features 3 and 6 are labeled by two people on every human and every simulated transcript in the comparison, blind to user type where the text allows; a third settles disagreements. Label agreement is reported. If kappa between the two labelers is below 0.70 (our starting point, as in S0), the feature is reported without a conclusion.

## 5. Analysis plan
- **Primary:** each feature in 4.1, per scenario and bot, for humans and each simulator, side by side. Simulated and human results are never merged or averaged.
- **Sample size (starting point):** 120 participants, 4 chats each, 480 human conversations, 60 per scenario, 20 to 30 per bot or arm cell. Simulators run the same cards with 10 seeds per cell. At this size a single human cell has a 95% interval about 20 to 40 pp wide, so S6 can catch large gaps and sign flips and cannot confirm small matches. We say so with every result.
- **Intervals:** proportions carry a 95% Wilson score interval. Human differences carry a 95% bootstrap interval that resamples participants (10,000 resamples). Medians in H2 carry a bootstrap interval. A difference is never shown without its interval.
- **S0 detectors (H8):** each S0 detector is scored against the two-person labels on human transcripts and on the matched simulated transcripts, kappa for each, with a bootstrap interval on the drop.
- **Falsification:** each rule in section 2 is applied as written. We do not move thresholds after seeing data.
- **We report even if null:** if simulators match people well (H2, H4, H5, H7 fail), we publish that with the same prominence, and the validity notes say **Holds**.
- **Exploratory:** comparisons across simulator models, message length, the post-chat "solved" answer against end state, and any feature not in section 2. Labeled exploratory and kept out of the headline.

## 6. Limits and threats to validity
- **Participants are not customers.** They act on a goal card, for an invented company, with nothing at stake. A real customer with a real bill may wait longer or leave sooner. S6 compares simulators with paid participants, not with real users.
- **Small panel.** 120 people cannot detect small gaps. A **Holds** note means no large gap was found, not that the simulator is right.
- **Subset of scenarios.** Eight scenarios from four studies. A note applies to the scenarios checked, not to every family in the source study.
- **One model per bot.** Human chats use one model per configuration to keep cells filled, so model effects from S1 and S2 are not checked.
- **Order and learning.** Four chats per person can teach them the bots. Order is random and logged, and first chats are analyzed alone as a check.
- **English, US, text chat.** Dialect effects are outside S6. [Seshadri et al. (2026)](https://arxiv.org/abs/2601.17087) report the proxy was worse for some dialect speakers, so this is a known gap.
- **Author bias.** We built the bots, scripts and simulators under test. All materials are published.

## 7. What would change our mind
- If H1 fails (the ladder does not lower human abandonment), the S3 headline is published labeled **Does not hold** and the fallback ladder on the [pattern page](../../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md) loses its simulated support.
- If H5 or H7 hold, S2 and S5 add a note that their scripted simulators never catch or confirm wrongly, and that their error rates are not what people would notice.
- If H8 holds, S0 precision and recall are reported as simulated-text figures only, and detectors stay "experimental" for real logs.
- If every hypothesis on a gap fails, simulators match people on these scenarios better than the sources below suggest, and we say so.

## 8. Prior work and how it shapes the design
We counted three web searches on 2026-10-22 (LLM user simulator validity compared with human users; sim-to-real gap in user simulation for conversational agents; how realistic LLM user simulators are in task-oriented dialogue). We opened the five pages below on 2026-10-22. The fetch tool returns a digest of a page, not raw text, so "opened" means read through that digest. Numbers below appear in the digest of the page opened.
- **Zhou et al., [Mind the Sim2Real Gap in User Simulation for Agentic Tasks (arXiv 2603.11245)](https://arxiv.org/abs/2603.11245), March 2026.** Abstract page opened, and the HTML full text read through a fetch digest (not read line by line). They ran a full agent benchmark with 451 human participants on 165 tasks and compared 31 LLM simulators. They report simulators that are overly cooperative, stylistically uniform and rarely frustrated, which makes tasks look easier, and more positive feedback than people give. Their index combines communication style, information pattern, clarification, error reaction, success calibration and rating agreement; the human baseline scored 92.9 and the best simulator 76.0. This is why S6 compares behaviors (features 2 to 6), not only end states, and why H4 and H7 expect people to be less cooperative.
- **Seshadri et al., [Lost in Simulation (arXiv 2601.17087)](https://arxiv.org/abs/2601.17087), January 2026.** Abstract page opened. Agent success varied by up to 9 pp across simulator models, simulated users misjudged performance by task difficulty, did worse for some dialect speakers, and showed different failure patterns than people. It is why S6 runs at least two simulator models and names dialect as a gap.
- **Wang et al., [Human vs. Agent in Task-Oriented Conversations (arXiv 2509.17619)](https://arxiv.org/abs/2509.17619), September 2025.** Abstract page opened. Parallel simulated and human conversations across four scenarios, ten behavior dimensions; differences in problem-solving and engagement, consistency on some others. It is why S6 uses parallel goal cards.
- **Meshi et al., [ConvApparel (arXiv 2602.16938)](https://arxiv.org/abs/2602.16938), February 2026.** Abstract page opened. A human dataset collected with a "good" and a "bad" recommender, used to check whether simulators react to a bad system as people do (counterfactual validation); they report a realism gap across all simulators. It is why S6 replays good and bad bots (A0 and A2, B0 and B2) and checks direction, not only rates.
- **Davidson et al., [User Simulation with Large Language Models for Evaluating Task-Oriented Dialogue (arXiv 2309.13233)](https://arxiv.org/abs/2309.13233), 2023.** Abstract page opened. The simulator aims for a goal success rate like that of people, works best on single-intent goals, and the authors collected a dataset of people using the same systems. This is the source S1 to S5 cite for scripting single-goal scenarios. S6 tests that choice.
- **Seen only in search summaries, not opened, not used:** a fine-tuned simulator paper and a dual-model simulator paper on ACL Anthology pages, a simulator benchmark with annotated human conversations, a negotiation-dialogue simulator study, a persuasion-dialogue study with a human-or-simulator guessing test, a paper on distributional gaps across many simulators known to us only from a summary site, and a corporate blog post on ConvApparel. No number from them is in this page. We found no opened study that compares simulated and human users on chatbot handoff, fallback or correction scenarios, so H1 to H8 have no sourced baseline.

## 9. Out of scope
- **Real customers and live traffic.** S6 supports no claim about any production bot or its users.
- **Opening messages.** S4 runs its own panel; S6 only reports S4's validity note alongside the others.
- **Model comparisons from S1 and S2.** One model per configuration in the human panel.
- **Voice, email and non-English chat.**
- Naming or ranking commercial chatbots, simulator products or panel vendors.

## 10. Data and materials to be published
Before the run, with a frozen date: this protocol, goal cards, consent text, panel instructions, bot versions, simulator prompts and rules, seed list, label guide and scoring code. After the run: human transcripts with any personal data removed (cards use invented data, and anything else typed is redacted), simulated transcripts, event logs, labels, the post-chat answers, version strings, run dates, analysis code and the validity note for each of S1 to S5. License and repository are open decisions for the owner.

## 11. Changes log
| Date | Change |
|---|---|
| 2026-10-22 | First draft of the protocol. Not run. Pages opened: Zhou et al. 2026 (abstract page and HTML full text through a fetch digest), Seshadri et al. 2026, Wang et al. 2025, Meshi et al. 2026, Davidson et al. 2023 (abstract pages). |

## Related
[Chat analytics plan](../../roadmap/chat-analytics-plan.md) · [S0 preregistration](s0-do-our-detectors-agree-with-people.md) · [S1 preregistration](s1-talk-to-a-human-within-two-turns.md) · [S2 preregistration](s2-do-corrections-stick.md) · [S3 preregistration](s3-fallback-designs-compared.md) · [S4 preregistration](s4-opening-messages-and-early-drop-off.md) · [S5 preregistration](s5-containment-versus-confirmed-resolution.md) · [Glossary](../glossary.md) · [Metrics](../metrics.md) · [Talk to a human ignored or looped](../../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md) · [Corrections not applied](../../goals/dialogue-management/failures/corrections-not-applied.md) · [Dead-end replies](../../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md) · [Answer-and-go conversation](../../goals/conversation-leadership/failures/answer-and-go-conversation.md) · [Confident wrong answer](../../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) · [Survey bias](../../goals/measurement-and-feedback/failures/survey-bias.md) · [Failure taxonomy](../../roadmap/specs/failure-taxonomy-v1.md)
