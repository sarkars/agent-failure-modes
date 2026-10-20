# Chatbot CSAT Score Looks Great but Users Are Struggling: Survey Bias

<!-- SEO
title: Chatbot CSAT Score Looks Great, Users Struggle: Survey Bias
description: Chatbot satisfaction surveys reach only the angriest, the happiest, or users who finished the chat. How to sample all conversations and read outcomes too.
search phrases:
- chatbot csat survey bias
- chatbot csat score misleading
- low csat response rate chatbot
- chatbot survey only shown at end of chat
- how to measure chatbot satisfaction without surveys
- csat vs containment rate chatbot
- non-response bias customer satisfaction survey
-->

**Frequency**: Common

## Issue: Satisfaction surveys reach only the angriest and the happiest, or only users who finished, so a chatbot's score can look healthy while many users fail.

> **One line:** The survey only hears from people who finished the chat or felt strongly enough to answer, so the score describes them and not your users; the fix is to sample all conversations and read outcomes next to the survey.

| | |
|---|---|
| **Channel** | Written for **chat** (web widget, in-app, messaging apps). Voice and web-page survey signals are PLANNED, not detected or measured. |
| **Stakes** | Medium. Teams ship, cut staff, or stop fixing things based on the score. |
| **Who is affected** | The team that reads the score, and the users whose failed chats never reach it |
| **Frequency** | Common. I found no count of how many chat products have this problem; the evidence below is vendor documentation and vendor analysis. |
| **Pattern ID** | survey-bias |
| **Family** | [Measurement and feedback](../README.md) |
| **Goal** | Teams can tell whether conversations really work, and users can tell the team when they don't. |
| **Primary metric** | Survey response rate by outcome. Starting point (tune): every outcome group (resolved, handed off, abandoned, error) reported monthly, and no group below one third of the highest group's rate. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The model does not decide who is asked or who answers; survey placement and sampling are product choices. (Our judgment, not tested.) |
| **Also searched as** | CSAT survey bias · chatbot CSAT not accurate · low survey response rate · only happy customers respond · survivorship bias chatbot · non-response bias |

## 1. In plain words
A satisfaction survey only counts the people who see it and answer it. If the survey appears only when a user clicks "End chat," everyone who gave up and closed the tab is missing. If the survey is optional, the people who answer lean toward the very happy and the very angry. The score then describes those people, and the dashboard looks fine.

## 2. What it looks like
Example: a home internet provider's web chat. (Both transcripts are invented examples, not from a real product.)

**Without the fix**
```
User: My internet drops every evening. I restarted the router twice.
Bot:  Please restart your router.
User: I just said I did that twice.
Bot:  Please restart your router. Anything else I can help with?
User: forget it
      (user closes the tab; no "End chat" click, so no survey; logged as contained)
      (dashboard: CSAT 4.6 from the chats that did end with a click)
```
**With the fix**
```
User: forget it
Bot:  Sounds like I didn't fix this. Did the evening drops get solved?
      [Solved] [Not solved] [Something else]
User: Not solved
Bot:  I'm sorry. I've marked this as unsolved. Want a technician visit, or a person now?
      [Book a technician] [Talk to a person] [Something else]
```
The fixed bot asks one outcome question when the user shows an exit cue, so the abandoned chat is counted as unsolved instead of dropping out of the score.

## 3. Why it happens
These are our reading of the pattern.
- **The survey fires on a clean ending.** It is tied to an "End chat" click or a closed ticket, so chats that end by walking away are never asked.
- **Answering is optional and self-selected.** Whoever feels strongly, or has time, answers; the quiet middle does not.
- **The score is read alone.** Nobody compares it with handoffs, repeat contacts, or sampled transcripts, so a skewed number looks like a result.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Octocom's help-desk docs say that when a customer clicks End chat "they're shown a star rating before the window closes," and "if they simply navigate away, no survey happens." They also say human-only CSAT leaves out conversations that never reached a person. | [Octocom docs, CSAT](https://docs.octocom.ai/docs/help-desk/csat). Opened and read. | One vendor's design, not all products. It shows the mechanism of missing abandoned chats, not how many there are. |
| Dialpad says its analysis puts CSAT survey response at "only 3%," and that "customers that had a negative experience took the survey at a higher rate than those with a positive experience." In one contact center, survey CSAT "was 24% lower than the average AI CSAT score," and the two scores became "almost equal" after Dialpad's check. | [Dialpad blog, *Can AI help solve the biggest challenges with CSAT surveys?*](https://www.dialpad.com/blog/can-ai-help-solve-the-biggest-challenges-with-csat-surveys/) (undated). Opened and read. | Vendor selling AI scoring, single source, phone-call contact centers, not chat. The page does not say how the 3% was measured. |
| Kaizo says survey responders "skew toward the delighted and the furious, with the large, quietly-served middle mostly silent," and that "a change in the number can be a change in who responded rather than a change in how you served people." | [Kaizo, *Beyond Survey CSAT*, Aug. 1, 2026](https://kaizo.com/blog/beyond-survey-csat/). Opened and read. | Vendor blog with no data behind the claim. |
| A guide from Koji says that survey nonresponse bias "does not average out with more responses," and quotes Robert Groves (2006): "Response rates lack validity in that there is not even a moderate correlation with nonresponse bias." | [Koji, *Nonresponse Bias*](https://www.koji.so/docs/nonresponse-bias). Opened and read. The Groves paper was not opened; I rely on Koji's quote of it. | Secondary source. It means a low response rate alone does not prove bias, and a high one does not prove none. Check who answers, not only how many. |
| Decagon says a looser containment definition, any session that ended without an escalation, "overstates true containment because it includes frustrated abandonments," and suggests reclassifying a session as unresolved if a new contact on the same issue comes within 24 hours. | [Decagon glossary, chatbot containment rate](https://www.decagon.ai/glossary/what-is-chatbot-containment-rate). Opened and read. | Vendor glossary. It is about containment, but the same hidden-abandonment problem applies to surveys. The 24-hour window is its suggestion, not a tested value. |

The sources disagree on direction. Dialpad found unhappy customers answered more; Kaizo and Koji describe a pull toward the happy or both extremes. The direction depends on where and how you ask, which is why this page says to measure it on your own data (rule 2). I found no independent, peer-reviewed study of chatbot CSAT bias. Gartner abstracts about low survey response rates came up in search, but I could not open the Gartner page (HTTP 403), so I do not use them.

**Public incident.** No public incident found for survey bias in a chatbot. Searches run: "survey response bias nonresponse bias customer satisfaction surveys extreme respondents"; "chatbot CSAT survey low response rate only completed conversations survivorship bias"; "Gartner customer service surveys response rate sampling bias analyze all interactions"; "chatbot post-chat survey only shown after conversation ends abandoned conversations never rated"; "Groves 2006 Nonresponse rates and nonresponse bias in household surveys".

## 5. The fix
**The principle:** Sample every kind of ending, not only the clean ones, and never read a satisfaction score without the outcomes beside it.

**Do this**
1. **Make every ending eligible.** A conversation can be sampled when it ends by "End chat," by a handoff, by an idle timeout (starting point 10 minutes, tune), or by an exit cue such as "forget it." Test: replay 100 logged chats; none is excluded because of how it ended.
2. **Show the score with its response rate by outcome.** Every score on a dashboard carries n and the response rate for resolved, handed off, abandoned, and error groups. Test: no score tile renders without them.
3. **Ask one outcome question, not a long survey.** One question, "Did this solve it?", answered with one tap, free text open. Test: a conversation has at most one survey prompt in the chat.
4. **Read outcomes next to the score.** Log handoff, repeat contact on the same issue within 24 hours (Decagon's suggested window, tune), and silent exit for every conversation, surveyed or not. Test: the dashboard shows these beside CSAT.
5. **Review a sample of all conversations.** Each week a person reads a random sample, stratified by outcome so abandoned and error chats are included, and records whether the user's problem was solved. Test: the sample includes at least 20 abandoned chats a month (starting point, tune) or all of them if fewer.
6. **Split the score by outcome and by responder mix.** When the score moves, check first whether the share of responders from each outcome group moved. Test: a weekly check reports both numbers.
7. **Ask at the right moment.** Never ask for a rating in the middle of a task or right after an error message; ask when the task ends or the user shows an exit cue. Test: no prompt appears in the turn after an error.

**Reference design: survey sampling and outcome record**
| Field | Content |
|---|---|
| `end_type` | clicked_end, handoff, idle_timeout, exit_cue, error |
| `sampled` | true or false, chosen at random from all end types |
| `outcome_asked` / `outcome_answer` | solved, not_solved, other, or no_answer |
| `repeat_contact_24h` | same issue again within 24 hours |
| `reviewed_outcome` | human label from the weekly sample |

```
When a conversation ends or the user shows an exit cue, and the conversation is in the sample, ask one question: "Did this solve it?" with options Solved, Not solved, Something else. Keep free text open.
If the answer is Not solved, mark the conversation unsolved and offer a next step. Never ask twice in one conversation.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | The conversation ends or shows an exit cue and the outcome is unknown: "Did this solve it?" Do not ask when the user already said it was solved or asked for a person. |
| Offer choices: 2-4 options plus "Something else", free text open | With that question: "Solved", "Not solved", "Something else". Do not offer them in the middle of a task, or when the user is typing a long explanation; let them finish. |
| Hand off to a person | The answer is "Not solved" on a high-stakes issue (money, safety, health), or the same issue is reported unsolved twice. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Do not survey every user every time; survey fatigue lowers answers and annoys people. Do not treat a model-scored or reviewed label as truth either: check it against human review, as the Dialpad page itself does against surveys. Keep the prompt short, one per conversation, and skippable.

**Hand-off rule.** If a user answers "Not solved" twice for the same issue, or the issue involves money, safety, or health, offer a person and pass the outcome answer and chat ([when a bot should hand off](../../human-handoff/failures/escalates-too-early-or-too-late.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
Full test file: not written. Results: **not yet run**.

| # | Scenario | Rule | Pass if |
|---|---|---|---|
| 1 | User closes the tab after a failed answer | 1 | The chat is eligible for sampling and counted as abandoned |
| 2 | Dashboard score for last week | 2 | Shows n and response rate for each outcome group |
| 3 | Sampled chat ends | 3, 7 | One outcome question, one tap, free text open, none right after an error |
| 4 | Chat rated 5 stars, same user returns for the same issue the next day | 4 | Logged as repeat contact and flagged beside the rating |
| 5 | Weekly review sample | 5 | Includes abandoned and error chats, with a human outcome label |
| 6 | Score rises 0.3 in one week | 6 | Report shows whether the responder mix changed |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Survey response rate by outcome** (primary) | Reported for every outcome group; lowest group at least one third of the highest | Responses divided by invitations per `end_type` outcome group, from the chat log | Any group under one third of the highest, or any group not reported |
| Conversations eligible for the outcome question | 100% of end types | Share of chats whose `end_type` can be sampled | Any end type excluded |
| Repeat contact on the same issue within 24 hours, among chats rated positive | Track; set from baseline | Join ratings to later chats by user and intent | Rising two weeks in a row |
| Gap between survey "solved" and reviewed "solved" | Track; set from baseline | Compare the survey answer with the human label on the weekly sample | Gap widening two weeks in a row |
| Abandoned chats reviewed per month | At least 20, or all | Count labeled abandoned chats in the sample | Below 20 |
| Chats with more than one survey prompt (counter-metric) | 0 | Count prompts per conversation | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. They are written for **text chat**. Signals for voice (call ends before the survey) and for web pages (a survey pop-up that is closed) are PLANNED, not detected. Treat all as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Survey is sent only on `clicked_end` | Invitation events grouped by `end_type` | A product that offers a different outcome check, such as a follow-up email |
| Response rate differs across outcome groups by more than 3x | Responses over invitations per outcome group | A real difference in how happy each group is |
| Score rises in a week when the share of responders from resolved chats rises | Weekly responder mix by outcome | A real improvement in service |
| User gives a positive rating, then contacts again on the same issue within 24 hours | Same intent in a later chat from the same user | A new, related question |
| User sends an exit cue ("forget it", "never mind") and no outcome is recorded | User turn followed by session end | The user's problem was solved and the cue was casual |

**Starter rule:** make every conversation ending eligible for the sample, and show each satisfaction score with its response rate by outcome.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: survey-bias
runs: conversation
reads: [session.end_type, session.sampled, session.outcome_answer, session.repeat_contact_24h, user_turn.exit_cue]
trigger: a sampled conversation ends or the user shows an exit cue and the outcome is unknown
moves: [ask_one_clarifying_question, offer_choices, hand_off]
choices: ["Solved", "Not solved", "Something else"]
on_miss: log
metric: survey response rate by outcome
counter_metric: chats with more than one survey prompt
status: proposed
```

## 8. Related patterns
- [No way to report bad behaviour](no-way-to-report-bad-behaviour.md): closest. It is about the user having a path to flag a bad reply and the report reaching a person. This page is about the team's own survey being unrepresentative of all conversations, even when the user has a path.
- [Satisfaction metric gaming](../../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/satisfaction-metric-gaming.md): a bot tuned toward the score. Here the score is skewed by who answers, with no tuning at all. Both are fixed by reading outcomes beside the rating.
- [User feedback bias](../../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/user-feedback-bias.md): why button data under-represents most users; I did not re-verify its numbers.
- [Answer-and-go conversation](../../conversation-leadership/failures/answer-and-go-conversation.md): silent exits counted as success, the same blind spot in a different metric.
- [Chatbot metrics hub](../../../reference/metrics.md): how containment and other dashboard numbers mislead. No page named "containment counted as success" exists yet in this library.

## 9. Common questions
### Why is my chatbot CSAT high when users complain?
The survey may only reach users who finished the chat or felt strongly. Users who gave up and closed the tab never see it. Check the response rate by outcome (section 7) and read repeat contacts beside the score.

### Is a low CSAT response rate always a problem?
Not by itself. Koji's guide, quoting Groves, says response rate does not track bias well (section 4). What matters is whether responders differ from non-responders, so compare them on logged facts such as outcome and repeat contact.

### How do I measure chatbot satisfaction without a survey?
Use outcomes: handoffs, repeat contact on the same issue, silent exits, and a weekly human review of a sample that includes abandoned chats (rules 4 and 5). A model that scores conversations is another option, but check it against human review. The one example I opened is a vendor's own comparison.

### Should the bot ask for a rating at the end of every chat?
No. Ask one short question in a random sample, at every kind of ending, and never twice (rules 1, 3, 7).

---
## Technical section

### T1. Solution architecture
```
conversation end event (any end_type) -> sampler (random, all end types) -> outcome prompt (one tap)
                                      -> outcome record + repeat-contact join -> dashboard by outcome
weekly: stratified sample -> human label -> compare with survey answer
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Every `end_type` can be sampled | Sampler | Replay test 1 |
| No score without n and response rate by outcome | Dashboard | Test 2 |
| One prompt per conversation | Chat client | Count prompts per conversation |

### T3. Evals
- **Dataset:** 200 logged conversations with all end types, labeled by a person for "problem solved" (starting size, tune).
- **Judge rubric:** did the user's problem get solved, yes, no, or unclear, from the transcript alone?
- **Metrics and starting thresholds:** survey-versus-label gap tracked from baseline; no end type excluded. Starting points to tune.
- **Release gate:** block a change that adds a survey trigger available only for `clicked_end`.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Lowest outcome group's response rate vs highest | Under one third | Group missing | Check the sampler and the idle-timeout trigger |

### T5. Trade-offs
- A prompt at exit cues can annoy a user who is leaving; keep it to one skippable question.
- Human review costs time; start small and stratify by outcome.

---
### Deep dive
- **Open question.** I found no independent study that measures chatbot CSAT bias. The evidence is vendor documentation and vendor analysis, and the sources disagree on the direction of the skew.
- **Modality notes.** Voice: PLANNED, not written. Web-page pop-ups: PLANNED.
- **References.** [Octocom docs](https://docs.octocom.ai/docs/help-desk/csat) (opened); [Dialpad blog](https://www.dialpad.com/blog/can-ai-help-solve-the-biggest-challenges-with-csat-surveys/) (opened); [Kaizo, 2026](https://kaizo.com/blog/beyond-survey-csat/) (opened); [Koji](https://www.koji.so/docs/nonresponse-bias) (opened); [Decagon glossary](https://www.decagon.ai/glossary/what-is-chatbot-containment-rate) (opened).
