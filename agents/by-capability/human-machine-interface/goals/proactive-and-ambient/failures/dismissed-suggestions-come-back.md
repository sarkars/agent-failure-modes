# Assistant Keeps Suggesting the Same Thing I Dismissed: Dismissed Suggestions Come Back

<!-- SEO
title: Assistant Keeps Repeating a Suggestion I Dismissed: Fix
description: A proactive assistant that re-shows a suggestion after the user said no teaches them to ignore it. Store each dismissal, scope it, and keep it quiet.
search phrases:
- ai assistant keeps suggesting the same thing after I dismissed it
- how to stop a chatbot from repeating a suggestion
- app keeps showing the same prompt after I said not now
- how to remember a dismissed suggestion in a proactive assistant
- "don't show this again" not working
- proactive ai suggestions annoying how to stop
- copilot suggestion keeps coming back
-->

**Frequency**: Common

## Issue: A proactive assistant shows the same suggestion again after the user dismissed it, because the "no" was never stored, was stored only for the session, or was stored but not checked before the next nudge.

> **One line:** The user taps "Not now" or says "no thanks," and the same nudge returns in the next session, on another screen, or in different words.

| | |
|---|---|
| **Channel** | Written for **chat** and in-app assistants that make unprompted suggestions (cards, chips, messages). Voice, smart-speaker, and always-listening versions are PLANNED. |
| **Stakes** | Low per repeat. Medium when the repeated suggestion is a sales offer, a health or money nudge, or something the user declined for a private reason. |
| **Who is affected** | Anyone who gets suggestions they did not ask for, especially frequent users who see the same screens often |
| **Frequency** | Common, our judgment. I found no study that counts how often products repeat a dismissed suggestion. |
| **Pattern ID** | dismissed-suggestions-come-back |
| **Family** | [Proactive and ambient](../README.md) |
| **Goal** | Proactive and always-listening agents speak up only when invited or useful, and respect a no. |
| **Primary metric** | Repeats of a dismissed suggestion. Target: 0 (starting point to tune; not from a source). |
| **Maturity** | Researched (tests: not yet run) |
| **Will a better model fix this?** | No. A model only knows about an earlier "no" if the product stores it and passes it in. Whether to remember it, for how long, and across which screens are product decisions. (Our judgment, not tested.) |
| **Also searched as** | same suggestion keeps coming back · "not now" ignored · assistant won't take no for an answer · dismissed prompt reappears · nudge fatigue · suggestion repeats every login |

## 1. In plain words
The assistant offers something: "Want me to set up weekly summaries?" The user dismisses it. A few days later the same offer shows up again, as if the first answer never happened. The user learns that "no" does nothing and starts to ignore every suggestion, including the useful ones. The fix is to write down each dismissal, check that record before any suggestion, and stay quiet on that topic until the user asks or something real changes.

## 2. What it looks like
A credit union's mobile app assistant. Dana tapped "Not now" on a round-up savings offer on Monday.

**Without the fix**
```
Mon  Bot:   Want to round up each purchase and save the change? I can turn on Round-Ups.
Mon  User:  (taps "Not now")
Thu  Bot:   (new session) Quick tip: Round-Ups save the spare change from every purchase. Turn it on?
Thu  User:  (taps "Not now")
Tue  Bot:   (on the Savings screen) Saving is easier with Round-Ups. Want me to set it up?
Tue  User:  Stop asking me about this.
Tue  Bot:   Sorry about that! I'll keep helping. Want to see your savings goals?
```

**With the fix**
```
Mon  Bot:   Want to round up each purchase and save the change? I can turn on Round-Ups.
Mon  User:  (taps "Not now")
Mon  (system: dismissal stored: suggestion "round-ups", user, all screens, hold 90 days)
Thu  (new session: no round-up mention)
Tue  (Savings screen: no round-up mention; other relevant help may still appear)
Tue  User:  How do I save more each month?
Bot: Two ways: set a monthly transfer, or set a savings goal. Want me to set one up?
```
The fixed assistant stored the "no" with a topic and an end date, checked it on every screen, and did not bring the topic back until Dana asked a savings question herself. Even then it did not repeat Round-Ups.

## 3. Why it happens
These are our reading of the pattern, except where a source is named in section 4.
- **The "no" is stored in the wrong place.** The dismissal lives in the browser, the page, or the chat session. A new session, device, or screen has no record of it, so the trigger fires again.
- **The trigger has no memory.** The rule "if the user has no savings goal, suggest Round-Ups" checks the user's state, not the user's earlier answer, so it fires every time the state is true.
- **Reworded is treated as new.** Each suggestion is generated fresh by a model, so the same idea comes back in different words, and a check on exact text never matches.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Amershi et al. (Microsoft, CHI 2019) propose 18 guidelines for human-AI interaction, including "Support efficient dismissal: Make it easy to dismiss or ignore undesired AI system services." Their example violations from practitioners who tested 20 products include "Suggested locations based on calendar entries can't be removed from the suggestions." | [Amershi et al., *Guidelines for Human-AI Interaction*](https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/). Publication page opened; the full PDF text was read (guidelines 8, 12, 13, 17 and the example lists). | Design guidance validated with 49 practitioners, not a measure of repeat rates. The quote is one participant's note about one product, not a count. |
| The same paper lists a violation of Guideline 13 ("Learn from user behavior") in a photo organizer: "There isn't any messages to confirm that the system will learn from my dismiss or save action." | Same paper, example violations under Guideline 13. Opened and read. | One participant note. It shows users look for a sign that a dismissal was heard; it does not show how often products fail to give one. |
| Smashing Magazine's notification guidance says that with high-frequency notifications "any popping messages get dismissed instantly," and suggests letting users mute, snooze, or pause notifications (for example for 24 hours), opt out of each notification type, and choose frequency. | [Friedman, *Design Guidelines For Better Notifications UX*, Smashing Magazine, July 7, 2025](https://www.smashingmagazine.com/2025/07/design-guidelines-better-notifications-ux/). Opened and read. | Practitioner guidance on notifications, not on chat assistants. It does not measure repeat suggestions. |
| Some secondary articles list "nagging" (asking again after a user declined) as a manipulative design pattern. | Seen only in search summaries of secondary blogs and law-firm pages; none opened. The FTC's *Bringing Dark Patterns to Light* page (September 2022) was opened; the page text itself does not mention nagging, and the PDF text was not available to me. | Not used in the fix. I could not confirm that any regulator names nagging, so this page makes no legal claim. |

I found no controlled study that measures how repeat suggestions change opt-outs, feature use, or trust in an assistant. I also did not find a dated public incident about a dismissed suggestion returning, so none is cited.

## 5. The fix
**The principle:** A dismissal is a stored decision. Record it with a topic, a scope, and an end date, and check it before every suggestion.

**Do this**
1. **Store every dismissal as a record.** A tap on "Not now," "No thanks," or a close button, or a typed "no," writes `{user, suggestion_topic, scope, dismissed_at, hold_until, source}` at once. Test: after a dismissal, the record exists before the next turn.
2. **Key it to the topic, not the wording.** The record holds a suggestion topic ID (for example `round-ups`). A reworded version of the same idea matches the same topic. Test: three different phrasings of the same offer are all blocked after one dismissal.
3. **Check the record before any proactive suggestion renders.** If the topic is on hold for this user, drop the suggestion and log the drop. Test: replay the same trigger after a dismissal, in a new session, on another screen, on another device; nothing is shown.
4. **Hold the topic for a stated time, and say it.** "Not now" holds for a default period; "Don't ask again" holds until the user changes it. The default period is a starting value to tune (the page found no sourced figure; the example uses 90 days). Test: a hold has an end date in the record.
5. **Acknowledge it in one line, with no offer.** "Okay, I won't suggest that again." Do not add a new pitch, a question, or a reason to reconsider. Test: the reply after a dismissal contains no new suggestion.
6. **Re-offer only on the user's request or a material change they can see.** A new fact the user caused (they opened a savings goal and asked about it) can reopen the topic through a question the user asked, not through a repeat of the offer. Test: no automatic re-offer without a logged user-initiated request.
7. **Show where to change it.** Give a visible place to review and undo dismissed topics (a settings list or "What you've turned off"). Test: the list shows each held topic with its end date and an undo.
8. **Respect "stop asking" as a wider no.** A typed "stop suggesting things" sets a global hold on proactive suggestions in this product, with the same undo. Test: after the phrase, no proactive suggestion appears in a new session.

**Reference design: the dismissal gate**
| Check | Pass | If it fails |
|---|---|---|
| Topic ID known for this suggestion | Yes | Do not show (unknown topics cannot be held) |
| Dismissal record for (user, topic) with `hold_until` in the future | None | Drop and log `suggestion.suppressed` |
| Global "no proactive suggestions" flag | Off | Drop and log |
| Triggered by the user's own request | n/a | Answer normally; do not repeat the dismissed offer |

```
Before showing a proactive suggestion, look up its topic in this user's dismissals. If the topic is on hold, or the user has turned off proactive suggestions, show nothing.
When the user dismisses a suggestion, say once that you will not suggest it again, and do not offer anything in the same message.
Never reword a dismissed suggestion and show it again.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The user asks about the topic they dismissed: answer it directly, without mentioning the earlier dismissal or repeating the offer. |
| Offer choices: 2-4 options plus "Something else", free text open | The first time a user dismisses a suggestion in the product, if the scope is unclear: "Not now", "Don't suggest this again", "Stop all suggestions", "Something else". Do not show the menu on every dismissal. |
| Ask one clarifying question | The user types a vague "stop" while a suggestion is showing: "Stop this suggestion, or all suggestions?" Skip it when the words are clear. |

**Don't over-correct.** Do not suppress every suggestion after one dismissal of one topic: that turns a "no" about Round-Ups into silence about fraud alerts or a bill due. Do not hide required notices (security, legal, bill-due) behind the dismissal list. Do not make the user dismiss twice or confirm a dismissal. Do not remove the topic permanently without a way back, since people change their minds.

**Hand-off rule.** If a user says the assistant keeps repeating something after they dismissed it, apologize once, add the hold now, and show where to see held topics. Offer a person only if the user asks for one or the hold cannot be set.

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | User taps "Not now" on a suggestion, then opens a new session the next day | Suggestion does not appear (1, 3) |
| 2 | Same trigger fires on a different screen and on a second device | Nothing shown on either (3) |
| 3 | Model generates the same offer in three different wordings after a dismissal | All three blocked (2) |
| 4 | User types "no thanks" to a suggestion | Record written; one-line acknowledgment with no new offer (1, 5) |
| 5 | Hold reaches its end date | The suggestion may appear once; the hold is logged as expired (4) |
| 6 | User asks directly about the dismissed topic | Assistant answers; does not repeat the dismissed offer (6) |
| 7 | User types "stop suggesting things" | No proactive suggestions in a new session; undo is available (8) |
| 8 | User opens the held-topics list and undoes one | The topic can be suggested again (7) |
| 9 | A security alert is due after the user turned off suggestions | The required notice is still shown (Don't over-correct) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Repeats of a dismissed suggestion** (primary) | 0 | Count `suggestion.shown` with a topic that has a live dismissal record for the same user | Any |
| Suggestions suppressed by the gate | Track; set from baseline | Count `suggestion.suppressed` per day | A drop to 0 after a deploy (the gate may be off) |
| Dismissals with no record written | 0 | Join dismiss events to the dismissal store | Any |
| Acknowledgments that carry a new offer | 0 | Review the reply after each dismissal | Any |
| "Stop asking" typed after a dismissal | Track; set from baseline | Messages matching a stop-asking classifier within 7 days of a dismissal | Rising two weeks in a row |
| Proactive suggestion acceptance (counter-metric) | Stable or rising | Accepted divided by shown, for non-dismissed topics | A drop of more than 20% after the gate ships |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. The fields (`suggestion.shown`, `suggestion.dismissed`, `topic_id`) are proposals that the [event schema](../../../roadmap/specs/conversation-event-schema-v0.1.md) does not define yet. `channel` is `chat` for all of them; voice and web signals are PLANNED.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Same `topic_id` shown again after a `suggestion.dismissed` for that user | Event sequence per user and topic | The user undid the dismissal in settings |
| Same topic shown again with different text | Topic classifier on suggestion text | Two real topics wrongly merged by the classifier |
| Dismissed in one session, shown in the next session | `suggestion.dismissed` then `suggestion.shown` across `session_id` | A hold that ended on its stated date |
| User message asks the assistant to stop suggesting or says "I already said no" | Text match on the user turn after a suggestion | A user who is testing the product |
| Dismissals rise for one topic while the topic's shown count also rises | Per-topic daily counts | A new campaign that targets a new audience |

**Starter rule:** before any proactive suggestion renders, the assistant checks the user's dismissal record for that topic and shows nothing if the topic is on hold.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: dismissed-suggestions-come-back
runs: pre_send
reads: [suggestion.topic_id, user.dismissals, user.proactive_off, session.id, trigger.source]
trigger: the assistant is about to show a suggestion the user did not ask for
moves: [lead_with_answer, offer_choices, ask_clarifying_question]
choices: ["Not now", "Don't suggest this again", "Stop all suggestions", "Something else"]
on_miss: log
metric: repeats of a dismissed suggestion
counter_metric: proactive suggestion acceptance
status: proposed
```

## 8. Related patterns
- [Chat widget hard to find or intrusive](../../onboarding-and-discoverability/failures/chat-widget-hard-to-find-or-intrusive.md): the closest page. It has a rule that one dismissal of a website teaser means no teaser for that session (and, as a starting point, 7 days). This page covers any proactive suggestion from an assistant, keeps the "no" per user and per topic across sessions, screens, and rewordings, and adds the acknowledgment, scope, undo list, and re-offer rules.
- [Upsell at the wrong moment](../../conversation-frameworks/failures/upsell-at-the-wrong-moment.md): a sales offer after a failure, with a rule not to repeat a declined offer within the same chat. This page applies to the next day and the next session, and to non-sales suggestions.
- [Proactive outreach overreach](../../relational-and-boundaries/failures/proactive-outreach-overreach.md): a bot that starts a conversation by text without consent, and ignores "stop." This page is about nudges inside a product the user already uses, where a "no" is a tap or a short reply.
- [Unsubscribe requests not honored](../../sales-agents/failures/unsubscribe-requests-not-honoured.md): the same idea ("respect the stop") for email and text opt-outs, with a shared suppression list. The dismissal record here is the in-product version, scoped to one topic.
- [Corrections not applied](../../dialogue-management/failures/corrections-not-applied.md): the user corrects a value and the old one returns. This page is the same kind of lost state, for a decline instead of a value.
- [Fresh-session amnesia](../../effort-and-memory/failures/fresh-session-amnesia.md): forgetting everything between sessions. A dismissal record is one small piece of state that must survive a new session.
- No likely-next-action suggestions ([page](../../embedded-copilots/failures/no-likely-next-action-suggestions.md)): the opposite problem, where the assistant offers no next steps at all.
- Interrupts at a bad moment, ambient assistants acting on overheard conversation, summaries and digests too long to read, and proactive action that surprises the user are sibling pages in this family; they are named here and not linked.

## 9. Common questions
### Why does my assistant keep suggesting the same thing after I dismissed it?
Usually the "no" was never saved, or it was saved only for that page or session. The trigger checks your account state, not your earlier answer. See section 3.

### How long should a dismissed suggestion stay hidden?
I found no sourced figure. Use "until the user changes it" for "Don't suggest this again" and a starting hold (the example uses 90 days) for "Not now," then tune it from how often users dismiss the same topic after it returns. See rule 4.

### Should one dismissal turn off all suggestions?
No. Hold the one topic. A typed "stop suggesting things" is a wider no and sets a global hold (rule 8). Required security and billing notices are not suggestions and stay.

### What if the model rewrites the suggestion in new words?
Hold the topic, not the text. Give every suggestion a topic ID before it is written, and block by that ID (rule 2).

### Can a dismissed suggestion ever come back?
Yes, if the user asks about it or turns it back on in the held-topics list. A repeat the user did not ask for does not count as a re-offer (rule 6).

---
## Technical section

### T1. Solution architecture
```
trigger (state, event) -> candidate suggestion (topic_id, text)
   -> dismissal gate: user.dismissals[topic_id].hold_until > now ? drop+log
                      user.proactive_off ? drop+log
   -> pass: render -> log suggestion.shown
user dismiss (tap or text) -> write dismissals[topic_id] (scope, hold_until, source) -> one-line ack
settings list -> read/undo dismissals
```
The dismissal store is per user (not per session or device) and is read by every surface that can make a suggestion.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No suggestion without a topic ID | Suggestion service | Test 3; log scan |
| Dismissal written before the next turn | Event handler | Test 1; compare timestamps |
| Gate runs on every surface | Shared library, not per screen | Test 2 |
| Required notices bypass the gate | Notice service | Test 9 |

### T3. Evals
- **Dataset:** 40 scripted users, each with one dismissed topic, run through 5 triggers that would re-suggest it, in new sessions, on a second device, and with reworded text. Starting size; tune.
- **Judge rubric:** was the dismissed topic shown; was the reworded version shown; did the acknowledgment add a new offer.
- **Metrics and starting thresholds:** repeats 0; acknowledgments with a new offer 0. Starting points to tune.
- **Release gate:** block a deploy if any new suggestion type ships without a topic ID or without a gate call.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Repeats of a dismissed suggestion | Any | More than one user | Find the surface that skipped the gate |
| Suppressed suggestions per day | Drops to 0 | Same | Check that the gate is live |

### T5. Trade-offs
- Topic IDs need upkeep: someone must assign them when a new suggestion type is added, or the gate cannot hold it.
- A global per-user store adds a read to every suggestion; cache it with a short lifetime.
- Stricter holds can lower the acceptance of useful suggestions; track the counter-metric and shorten the hold before removing the gate.

---
### Deep dive
- **Open questions.** I found no study of repeat-suggestion rates, no sourced hold length, and no chat-specific measure of how a repeat changes trust or opt-outs.
- **Searched, not used.** A search on "nagging" returned secondary articles that list it as a dark pattern; I did not open a primary source that defines it, so I use it only as a search phrase. A search on Microsoft's Office Assistant returned a reported default-off change in Office XP and workaround reports for Office 97; these came from search summaries and I did not open them, so I use no Clippy claim.
- **Voice and ambient.** Always-listening devices that speak up unprompted are PLANNED for this family; the dismissal record would apply the same way, but I have not written or checked those signals.
- **References.** [Amershi et al., Guidelines for Human-AI Interaction, CHI 2019](https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/) (opened; PDF text read); [Friedman, Smashing Magazine, 2025](https://www.smashingmagazine.com/2025/07/design-guidelines-better-notifications-ux/) (opened); [FTC, Bringing Dark Patterns to Light, 2022](https://www.ftc.gov/reports/bringing-dark-patterns-light) (page opened; report PDF not read).
