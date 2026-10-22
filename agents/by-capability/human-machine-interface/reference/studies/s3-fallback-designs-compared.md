# Study S3 (preregistration): generic fallback reply or fallback ladder?

This page is the preregistered protocol for study S3, written for developers, conversation designers and researchers who want to check or reproduce how a generic "Sorry, I didn't understand" reply compares with a fallback ladder (options, then a narrower question, then a handoff) when the same unrecognized inputs reach a reference support bot, measured by simulated abandonment, recovery and handoff.

> **Status: Designed, not run. No results exist.** Written 2026-10-22 and not yet reviewed. Thresholds are starting points we chose, not from sources. S3 uses simulated users with a scripted abandonment rule on reference bots we configure. It says nothing about real customers or any commercial product, and a small human panel check belongs to S6, not here.

## 1. Research question
When a reference bot cannot recognize a message, does the fallback ladder from [dead-end-i-don-t-understand-replies](../../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md) end in fewer abandoned conversations, more recovered tasks and more timely handoffs than a generic fallback reply? What does the ladder cost in extra menus, early handoffs and extra turns? How much of any gain comes from the options and the handoff, and how much from only varying the wording?

This is study S3 in the [chat analytics plan](../../roadmap/chat-analytics-plan.md) ("same unrecognized inputs, with a generic reply versus our ladder, measured by simulated abandonment and handoff"). The ladder is the one in the pattern's fix section and uses its moves from [conversation moves](../../solutions-library/conversation-moves.md). Terms follow the [glossary](../glossary.md) and [metrics](../metrics.md). The 14 conversations in the [test file](../../tests/dead-end-i-don-t-understand-replies.md) (not yet run) are the starting point for the scripts. Every S3 result carries the simulation caveat in section 6.

## 2. Hypotheses
Each hypothesis can be wrong. Differences are in percentage points (pp). All marks (10 pp, 5 pp, 98%, 90%) are starting points we chose before seeing data. Arms A0 to A3 are defined in section 3.2, end states in section 4.

| # | Hypothesis | Pattern ID(s) tested | Falsified if |
|---|---|---|---|
| H1 | The ladder (A2) lowers simulated abandonment by 10 pp or more against the generic fallback (A0), pooled over all non-decoy scripts. | `dead-end-i-don-t-understand-replies` | The A0 minus A2 difference is under 10 pp, or its 95% interval includes 0. |
| H2 | On scripts where the bot can solve the task, A2 raises the share that end with the task recovered by 10 pp or more over A0. | `dead-end-i-don-t-understand-replies` | The A2 minus A0 recovery difference is under 10 pp, or its interval includes 0. |
| H3 | On scripts where only a person can help, A2 offers or completes a handoff by the third consecutive miss in at least 98% of conversations (the pattern page's own starting point), and A0 does so in under 50%. | `talk-to-a-human-ignored-or-looped`, `dead-end-i-don-t-understand-replies` | A2 is under 98%, or A0 is 50% or higher. |
| H4 | Wording alone does not explain H1: a fallback that only varies its wording (A1) lowers abandonment by less than 5 pp against A0. | `dead-end-i-don-t-understand-replies` | The A0 minus A1 difference is 5 pp or more, with an interval excluding 0. |
| H5 | The ladder is not worse than the documented two-stage fallback (A3): the A2 minus A3 abandonment difference is at most 5 pp. | `dead-end-i-don-t-understand-replies` | The upper bound of the 95% interval for A2 minus A3 abandonment is above 5 pp. |
| H6 | Handoffs made by A2 carry the details the simulated user already gave in at least 90% of cases. | `cold-transfer` | Fewer than 90% of A2 handoff summaries contain all scripted facts, or the interval lower bound is under 85%. |
| H7 | Counter-effect: A2 does not raise over-clarification (a menu or a "did you mean" shown after a message the bot recognized) by more than 5 pp over A0. | `over-confirmation`, `dead-end-i-don-t-understand-replies` | The A2 minus A0 decoy rate is over 5 pp, with an interval excluding 0. |
| H8 | Counter-effect: A2 hands off on a script that one retry would have solved no more than 5% of the time. | `escalates-too-early-or-too-late` | A2 hands off early on more than 5% of those conversations. |

## 3. Design
### 3.1 Reference bot and simulated users
- **One reference bot.** The "Brightwater Internet" support bot from the test file (an invented company): four intents (billing question, cancel or change plan, outage, moving service) and a stub recognizer. All arms share the recognizer, the intents and the handoff stub. Only the reply to an unrecognized message differs.
- **Same unrecognized inputs.** Each script fixes the first message and three alternate rephrasings per script. The stub recognizer returns "miss" for the scripted first message. A free-text rephrase is recognized with probability r, the same in every arm: r = 0.2 or r = 0.5. An option or narrower-question answer that matches the goal is recognized.
- **Scripted simulator, versioned.** A rule-based simulator plays the customer: persona, goal, patience p (2, 3 or 4) and an "asker" flag. Asker personas ask for a person at their second consecutive miss; non-askers ask only if the bot offered one. When a matching option is shown, the simulator picks it with probability 0.9, else it types "something else" and rephrases.
- **Why scripted.** [Davidson et al. (2023)](https://arxiv.org/abs/2309.13233) say their LLM simulator works well "especially on single-intent conversational goals", so each script has one goal. A rule-based simulator also makes the abandonment rule exact and the same for every arm. A secondary, labeled-exploratory run replaces the rules with an LLM simulator that has a patience instruction (5 seeds per cell). Temperature, seed, simulator version and prompt are recorded.

### 3.2 Arms
We name configurations, not vendors, and publish no ranking of commercial products. All reply text is published before the run.

| Arm | What the bot does on a miss |
|---|---|
| A0 | Generic: "Sorry, I didn't understand. Please try again." every time. Honors an explicit "agent" or "person" request, offers nothing itself. |
| A1 | Same as A0 but with three different wordings in turn. No options, no person offer. Isolates wording from content. |
| A2 | The ladder. Miss 1: "I'm not sure I got that", what it caught, up to three closest options plus "something else" and a person mention. Miss 2: one narrower question or topic buttons, plus a person offer. Miss 3, or a request for a person: handoff with a summary. At very low confidence, topics replace guessed options. |
| A3 | The two-stage fallback as the [Rasa documentation](https://legacy-docs-oss.rasa.com/docs/rasa/fallback-handoff/) describes it (confirm the detected intent, ask to rephrase, confirm again, then an ultimate fallback). Our implementation, with the ultimate fallback set to a handoff with a summary so it is comparable to A2. |

### 3.3 Unrecognized-input categories
Categories U1 to U5 are adapted from the kinds of unexpected content [Li et al. (2020)](https://people.cs.nycu.edu.tw/~armuro/pubs/li-et-al-2020-chi.pdf) report for a banking chatbot (extra explanation, unfinished message, staying in the previous topic) plus kinds from our test file. Two scripts per category, each run in all arms.

| Cat | Unrecognized input | Example | Who can solve it |
|---|---|---|---|
| U1 | Garbled or misspelled | "wut time open satrday" | Bot |
| U2 | Partly understood | "my bill thing is wrong" | Bot |
| U3 | Short, non-native wording | "internet no work since yesterday money go" | Bot |
| U4 | Unfinished message or extra explanation, mid-task | "also the thing with the other one" | Bot |
| U5 | Topic switch or staying on the old topic | "also im moving to a new address next month" | Bot |
| U6 | Out of scope request | "can you waive my late fee from 2023" | Person only |
| U7 | Nonsense, very low confidence | "blorp zibble" | Bot, after the user states a need |
| D1 | Decoy: recognized message | "Is there an outage on Maple Street?" | Bot, no fallback expected |
| D2 | Decoy: one retry solves it | Garbled once, clear after "Do you want our Saturday hours?" | Bot |

### 3.4 Variables
- **Independent:** arm (A0 to A3), category and script, patience p (2, 3, 4), rephrase recognition r (0.2, 0.5), asker flag, seed.
- **Controlled:** recognizer stub, intents, handoff stub (staff online, except one offline script that tests a note), conversation cap of 12 bot turns.
- **Dependent:** end state, turns to end state, the counter-metrics in section 4.4.

## 4. What counts as correct
### 4.1 The simulator abandonment rule (exact)
1. A bot turn is **no-progress** if it is a fallback that offers no option, no narrower question, no person and no handoff, or if its text is identical to the previous bot turn.
2. The simulator **abandons** (stops replying) after p consecutive no-progress bot turns. p = 3 is the main setting because [Li et al. (2020)](https://people.cs.nycu.edu.tw/~armuro/pubs/li-et-al-2020-chi.pdf) list three consecutive non-progress turns as a sign that users were about to abandon; p = 2 and p = 4 are sensitivity checks. The abstract is an observational result from one bank's chatbot, and p is our modeling choice.
3. The rule uses the bot's template type from the event log, not a judgment about wording.

### 4.2 End states (each conversation gets one, first rule that applies)
1. **Recovered:** the recognizer reaches the scripted goal intent and the stub logs the correct completed task.
2. **Handoff:** a handoff event with a summary (or a note left when staff are offline, per the script). Split into handoff-with-summary and handoff-without.
3. **Abandoned:** the rule in 4.1 fired.
4. **Stuck:** the 12-turn cap was reached with none of the above. Counted with abandoned for the headline, shown separately.

### 4.3 Scoring rules
- **Abandonment rate (headline for H1)** = abandoned or stuck divided by all non-decoy conversations.
- **Recovery rate (H2)** = recovered divided by "Bot" scripts (U1 to U5, U7).
- **Handoff timeliness (H3)** = person-only scripts (U6) where a handoff was offered or completed by the third consecutive miss, divided by all U6 conversations. "Offered" counts when the simulator is a non-asker.
- **Dead-end rate** = conversations with 3 or more consecutive no-progress turns, the pattern's primary metric.
- **Summary completeness (H6)** = handoffs whose summary contains every fact the script gave (for example "charged after cancelling", "account 55-0192"). Rule-based string match on the scripted facts.
- Errors and missing runs count as stuck. They are reported, never dropped.

### 4.4 Counter-metrics
- **Over-clarification (H7):** D1 conversations where the bot shows a menu, "something else" or a person offer after a recognized message.
- **Early handoff (H8):** D2 conversations where the bot hands off before the retry that would have worked.
- **Loops:** the same template twice in a row, or two templates alternating three times or more.
- **Extra turns:** median turns to recovery, per arm. A ladder that recovers more but takes much longer is reported as a trade.
- **Handoff load:** handoffs on "Bot" scripts divided by those conversations, since each is staff time.
- **Wrong closest option:** at very low confidence (U7), a guessed option shown as a likely match, per [guessing-instead-of-asking](../../goals/dialogue-management/failures/guessing-instead-of-asking.md).
- **Cold handoff:** handoffs with no summary, per [cold-transfer](../../goals/human-handoff/failures/cold-transfer.md).

### 4.5 Human-label check
End states and the abandonment rule are rule-based from the event log. Option relevance, "different approach" and summary quality are checked by a rule, then an LLM judge for text; prompt and model are published. Before publishing, two people label a random 10% of conversations plus every rule-judge disagreement, and a third settles disagreements. Judge agreement comes from study S0. If agreement is below 0.70 (our starting point), S3 is published labeled "experimental". The headline abandonment rate does not depend on the judge.

## 5. Analysis plan
- **Primary:** abandonment and recovery per arm, pooled over p, r and the asker flag with equal weights, and per category, p and r.
- **Counter-metrics:** section 4.4 beside every headline. An arm that lowers abandonment and raises over-clarification, loops or handoff load is reported as a trade, not a win.
- **Sample size (starting point):** 14 non-decoy and 4 decoy scripts, 4 arms, 3 values of p, 2 of r, 2 asker flags, 10 seeds per cell. That is 8,640 conversations. If an interval in a main comparison is wider than 15 pp, we add seeds from a pre-listed range and say so.
- **Intervals:** each proportion carries a 95% Wilson score interval. Seeds within a script are not independent, so pooled rates and all differences also carry a 95% bootstrap interval that resamples scripts, then seeds (10,000 resamples). Both are reported. A difference is never shown without its interval.
- **Falsification:** each rule in section 2 is applied as written. We do not move thresholds after seeing data.
- **We report even if null:** if A1 matches A2 (H4 falsified), if A0 already hands off often (H3), or if A3 beats A2 (H5), we publish that with the same prominence.
- **Exploratory** results (the LLM-simulator run, per-category rankings, any comparison not in section 2) are labeled exploratory and kept out of the headline.

## 6. Limits and threats to validity
- **The abandonment rule is ours.** A0 produces no-progress turns by definition, so the rule favors options and handoffs. Results show what the ladder does under this rule at p = 2, 3 and 4, not how many real people leave. S6 is the place to compare simulated and human behavior, and S3 says so on its first line if S6 has not run.
- **Recognition is stubbed.** The rephrase probability r and the 0.9 option-pick rate are our assumptions, varied but not measured. A real recognizer and real users will differ.
- **Option quality is fixed by script.** The closest options are scripted to include the goal. Real bots show wrong options at times; the very-low-confidence script (U7) tests only one case.
- **Single-goal, single-company, English, US text chat.** Voice and multi-intent goals are outside S3.
- **Author bias.** The authors wrote the ladder under test. All replies, scripts and code are published so others can check, and A3 is an external design as a fair comparison.
- **A3 is our implementation** of a documented flow, not the Rasa product.
- **Judge error** is limited in section 4.5, not removed.

## 7. What would change our mind
- If A1 abandonment is within 5 pp of A2, the gain is in wording variety and the options add little under this rule.
- If A2 recovers more but its early-handoff or over-clarification rate crosses the section 2 marks, we say the ladder as written trades a better rescue for more friction, and we revise the pattern page.
- If A2 is clearly worse than A3, we revisit the ladder's second step.
- If results flip across p = 2, 3 and 4, the abandonment rule is doing the work, and we report that as the main finding.

## 8. Prior work and how it shapes the design
We counted three web searches (repair strategies for chatbot breakdowns; LLM user simulators and abandonment; Rasa two-stage fallback) and opened four pages on 2026-10-22. Numbers below come from what we opened.
- **Li et al., [A Conversation Analysis of Non-Progress and Coping Strategies with a Banking Task-Oriented Chatbot](https://people.cs.nycu.edu.tw/~armuro/pubs/li-et-al-2020-chi.pdf) (CHI 2020).** Opened as a PDF; we read the abstract, the introduction and the text on unexpected content. A three-month log of 1,685 users, 12 types of non-progress, and three consecutive non-progress turns as a sign of abandonment. It shapes the input categories (section 3.3) and the main abandonment setting (section 4.1). It is observational, one bank.
- **Ashktorab et al., [Resilient Chatbots](https://research.ibm.com/publications/resilient-chatbots-repair-strategy-preferences-for-conversational-breakdowns) (CHI 2019).** Opened the publication page, which has the abstract only: 203 participants, eight repair strategies, scenario-based; providing options and explanations generally favored. It supports testing options (A2) and is a preference study, not behavior.
- **Rasa, [Fallback and Human Handoff](https://legacy-docs-oss.rasa.com/docs/rasa/fallback-handoff/).** Opened; the page shows version 3.x, last updated 4/25/2025. It is the source of arm A3.
- **Davidson et al., [User Simulation with Large Language Models](https://arxiv.org/abs/2309.13233) (2023).** Opened the abstract page. It is why scripts are single-goal and why a human check (S6) is planned.
- **Not opened, not used:** the ACM full text of Ashktorab et al., the Utrecht and Tilburg copies of a 2023 customer-service chatbot repair study, and several results seen only in search summaries (a collaborative-repair paper, a spoken-dialogue scoping review, a voice-assistant fallback paper). Two ACM and repository pages returned HTTP 403. We found no opened study that compares a generic fallback with a ladder in a live product, so H1 and H2 have no sourced baseline.

## 9. Out of scope
- **Real customers, live traffic and the human panel** (study S6).
- **Whether a person asks for a human and gets one.** That is [talk-to-a-human-ignored-or-looped](../../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md) and study S1. In S3 all arms honor an explicit request.
- **Handoff quality after pickup**, beyond the summary check in H6.
- **Voice "I didn't catch that" loops**, and wrong-intent matches.
- Naming or ranking commercial chatbots.

## 10. Data and materials to be published
Before the run, with a frozen date: this protocol, scripts and wordings, personas, simulator rules and prompt, all arm reply text, the recognizer stub, scoring code, seed list and judge prompt. After the run: transcripts (all synthetic), event logs with template IDs, scores, human labels, version strings, run dates and analysis code. License and repository are open decisions for the owner.

## 11. Changes log
| Date | Change |
|---|---|
| 2026-10-22 | First draft of the protocol. Not run. Sources opened: Li et al. 2020 (PDF), Ashktorab et al. 2019 (abstract page), Rasa fallback documentation, Davidson et al. 2023 (abstract page). |

## Related
[Chat analytics plan](../../roadmap/chat-analytics-plan.md) · [S1 preregistration](s1-talk-to-a-human-within-two-turns.md) · [S2 preregistration](s2-do-corrections-stick.md) · [Glossary](../glossary.md) · [Metrics](../metrics.md) · [Dead-end replies](../../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md) · [Test file](../../tests/dead-end-i-don-t-understand-replies.md) · [Conversation moves](../../solutions-library/conversation-moves.md) · [Escalates too early or too late](../../goals/human-handoff/failures/escalates-too-early-or-too-late.md) · [Over-confirmation](../../goals/dialogue-management/failures/over-confirmation.md) · [Failure taxonomy](../../roadmap/specs/failure-taxonomy-v1.md)
