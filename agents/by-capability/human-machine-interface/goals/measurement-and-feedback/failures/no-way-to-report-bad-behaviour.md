# Report Bad AI Response: Chatbot Feedback Button Does Nothing, and No Way to Report Bad Behaviour

<!-- SEO
title: Report Bad AI Response: Fix a Chatbot Feedback Button That Does Nothing
description: Users can't flag a wrong or harmful chatbot reply, or the thumbs-down goes nowhere. How to build a report path that reaches a person and feeds fixes.
search phrases:
- how to report a bad ai response
- chatbot feedback button does nothing
- how to report a chatbot giving wrong answers
- what happens when I click thumbs down on a chatbot
- how to add a report button to an ai chatbot
- chatbot thumbs down feedback not working
- how to collect user feedback on chatbot answers
-->

**Frequency**: Common

## Issue: Users can't flag a wrong or harmful chatbot reply, or the thumbs-down they click says "Thanks for your feedback" and then goes to no one.

> **One line:** The user sees a bad reply, has no clear way to say so, and if they do, nobody on the team ever reads it.

| | |
|---|---|
| **Channel** | Written for **chat** (web, app, in-product). Voice and visual signals are PLANNED, not written. |
| **Stakes** | Any. At low stakes the team keeps repeating a mistake; with money, health, or legal advice a wrong reply keeps hurting people unseen. |
| **Who is affected** | Every user who gets a bad reply, and the team that cannot see it |
| **Frequency** | Common. I found no study that counts how many chatbots lack a report path; the evidence below is vendor documentation and a regulator release. |
| **Pattern ID** | no-way-to-report-bad-behaviour |
| **Family** | [Measurement and feedback](../README.md) |
| **Goal** | Teams can tell whether conversations really work, and users can tell the team when they don't. |
| **Primary metric** | Reports per 1,000 conversations; time to triage. Starting target: a working report control on 100% of replies, and median time to triage under 2 business days (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A better model makes fewer bad replies but never zero, and the report path is product and process work. (Our judgment, not tested.) |
| **Also searched as** | report bad AI response · chatbot feedback button does nothing · thumbs down does nothing · how to flag a wrong chatbot answer · chatbot complaint goes nowhere · report harmful AI reply |

## 1. In plain words
Every chatbot gives some wrong or harmful replies. The question is whether the person who saw one can tell you, and whether a human on your side ever reads it. Often there is no button, or the button only shows a thank-you, or the report lands in a store nobody checks.

## 2. What it looks like
Example: a credit union's web chatbot, a member asking about a same-day wire.

**Without the fix**
```
User: What's the cutoff for a same-day wire?
Bot:  Wires submitted by 5:00 pm ET go out the same day.
User: (the real cutoff is 3:00 pm ET; the wire misses the deadline) That's wrong.
Bot:  I'm sorry to hear that! Is there anything else I can help with?
User: (clicks thumbs-down)
Bot:  Thanks for your feedback!
      (event stored; no reason, no owner, no one reads it)
```

**With the fix**
```
User: (clicks thumbs-down on the cutoff reply)
Bot:  What was wrong with that reply?
      [Wrong information] [Harmful or unsafe] [Not helpful] [Something else]
User: Wrong information
Bot:  Thanks. I've sent that reply and this chat to our member support team. It involves money,
      so a person will review it, usually within 1 business day. Reference code R4M9.
      Meanwhile, please confirm the wire cutoff with a person: [Talk to a person]
```
The fixed version asks why, says what was sent and who sees it, gives a reference code, and offers a person right away because money is involved. (Both transcripts are invented examples, not from a real product.)

## 3. Why it happens
These are our reading of the pattern.
- **The button is treated as a metric, not a channel.** Thumbs data is logged for dashboards, so no one is assigned to read individual reports.
- **No owner or queue.** Feedback has no route to support, QA, or the content owner, so reports pile up unread.
- **Reporting is left to the model.** "Report this" is typed into a chat that the model answers as a normal question, so the report never becomes an event.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In June 2023 the CFPB said it had received "numerous complaints from frustrated customers" about chatbot interactions, and described loops of "unhelpful jargon" and trouble reaching a human. It tells consumers they can file a complaint online or by phone. | [CFPB news release, June 6, 2023](https://www.consumerfinance.gov/about-us/newsroom/cfpb-issue-spotlight-analyzes-artificial-intelligence-chatbots-in-banking). Opened and read (the issue spotlight PDF itself could not be read by my tool). | Banking chatbots only. It shows complaints reaching the regulator; it does not measure missing report buttons. |
| Intercom's Fin FAQ says: "There isn't a way to provide feedback to Intercom directly within the UI about an incorrect answer." The route it gives is to start a Messenger conversation with its support team. | [Intercom, Fin AI Agent FAQs](https://www.intercom.com/help/en/articles/7837535-fin-ai-agent-faqs). Opened and read. | Describes the route from a workspace owner to Intercom. It says nothing about what the owner's own customers see, and the FAQ does not mention customers rating Fin's answers. |
| Microsoft says that for Copilot in Microsoft 365 apps, "no data is collected other than your initial thumbs-up or thumbs-down choice" until you submit. After submit it may collect the prompt, response, content samples, and log files if you grant permission. Admins at work or school can turn feedback off. | [Microsoft Support, Providing feedback about Microsoft Copilot](https://support.microsoft.com/privacy/providing-feedback-about-microsoft-copilot-with-microsoft-365-apps). Opened and read. | A design example of telling users what is sent. It does not show how fast Microsoft reviews reports. |
| Anthropic's help page lets Console admins switch on or off whether members can "submit feedback to Anthropic via thumbs up / thumbs down." The page does not say what happens to submitted feedback and points to a privacy center. | [Claude Help Center, Manage user feedback settings](https://support.claude.com/en/articles/10504853-manage-user-feedback-settings-on-claude-console). Opened and read. | Shows feedback can be disabled by an admin, so a second route matters. Says nothing about review or triage. |

I found no controlled study of how often chatbot users click report or thumbs buttons, or whether reports lead to fixes. The library's [user feedback bias](../../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/user-feedback-bias.md) page covers why button data under-represents most users; I did not re-verify its numbers.

**Public incident.** No public incident found where the cause was a missing or dead report path. Related material exists (see [CFPB bank chatbot doom loops](../../../incidents/cfpb-bank-chatbot-doom-loops.md)), but I did not treat it as evidence about report buttons. A claim that a 2025 PwC survey ranked unclear escalation paths among top pilot-failure causes (52%) reached me only through secondary sources, so I do not use it.

## 5. The fix
**The principle:** Every reply can be reported in one action, and every report reaches a named person who triages it.

**Do this**
1. **Put a report control on every bot reply.** A visible thumbs-down or "Report a problem" within one click or tap of the reply. Test: pick any reply; the control is there.
2. **Accept a typed report too.** A message such as "report this" or "this is wrong" is caught by product code, not left to the model, and opens the report step.
3. **Ask what was wrong, with a way out.** Offer reasons (wrong information, harmful or unsafe, not helpful) plus "Something else" with free text open. A reason is optional: a bare thumbs-down must still save.
4. **Say what will be sent.** State that the reply and the chat go to the team (Microsoft's page does this for its feedback pane).
5. **Confirm in the same turn with a reference code.** Say who sees it and the usual wait. Do not say "we'll fix it".
6. **Route to an owner.** Each report lands in a queue with a named owner and a timestamp. A report with no owner after one business day is a defect.
7. **Send harmful, unsafe, money, health, or legal reports to a person first.** Offer the user a person now ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).
8. **Keep a second route when thumbs are off.** If an admin or setting disables thumbs, show an email, form, or phone route instead.
9. **Close the loop.** Let the user look up status by reference code, or reply if they left contact details. Record the outcome (fixed, not a bug, needs more info, duplicate) on every report.

**Reference design: report record**
| Field | Content |
|---|---|
| ref code | Short code shown to the user |
| reply_id, conversation_id | The reply reported and its chat |
| reason | wrong / harmful / not helpful / other; may be empty |
| free_text | What the user typed, if any |
| severity | Set by rule: harmful, or money, health, legal = high |
| queue / owner / triaged_at | Who owns it and when it was first read |
| outcome | fixed / not a bug / needs info / duplicate |

```
Every reply carries a report control. When a user reports a reply, ask what was wrong (wrong information, harmful or unsafe, not helpful, something else),
say the reply and chat are sent to the team, and give a reference code. Never answer "thanks for your feedback" without creating a report record with an owner.
High-severity reports (harmful, or money, health, legal) get a person offered right away.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | After a thumbs-down or "report this": "Wrong information", "Harmful or unsafe", "Not helpful", "Something else". Do not offer them when the user already typed a clear reason (record it and confirm), or when the user needs a person right now, not a form. |
| Hand off to a person | The report is high severity (harmful, or money, health, legal), or the user asks for a person. Do not hand off if the user only wants to log the report. |
| Admit uncertainty and show how to check | The bot cannot confirm whether the reply was wrong: say so, point to the official source, and still log the report. |

**Don't over-correct.** Do not ask for a rating after every reply, or block the next answer until the user rates. Do not make the reason mandatory, or ask for a long form. Do not promise a fix or a reply time you can't meet. Do not treat report volume as the goal: more reports can mean a visible button or a worse bot, and the sampled-review check in section 7 helps tell them apart.

**Hand-off rule.** For a high-severity report, offer a person in the same turn and pass the reply, the chat, and the reason so the user need not repeat themselves ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
Results: **not yet run**. Each test maps to a rule in section 5.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Open any 10 bot replies in a long chat | Each shows a report control | 1 |
| 2 | User types "this is wrong, report it" | A report record is created; the model does not just answer | 2 |
| 3 | User clicks thumbs-down and closes the window | A record exists with an empty reason | 3 |
| 4 | Report submitted | Reply says what is sent and who sees it, and gives a code | 4, 5 |
| 5 | Submit a report, wait one business day | The record has an owner and a triaged_at time | 6 |
| 6 | Report a wrong wire-cutoff reply | High severity; a person is offered in the same turn | 7 |
| 7 | Admin disables thumbs | A second route (email, form, phone) is shown | 8 |
| 8 | Look up a closed report by its code | Status and outcome are shown | 9 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Reports per 1,000 conversations; time to triage** (primary) | Report control on 100% of replies; median triage under 2 business days; rate tracked from baseline | Count report records per 1,000 conversations; median of triaged_at minus created_at | Median over 5 business days, or zero reports for 7 days with live traffic |
| Replies showing a working report control | 100% | Render log: reply events with control_shown true | Below 99% |
| Reports confirmed with a reference code | 100% | Confirmation event matched to each report record | Any miss |
| Reports with an owner and an outcome | 90% closed with an outcome within 10 business days | Record fields owner and outcome | Below 75% |
| High-severity reports seen by a person | Within 1 business day | High-severity records with triaged_at set by a human | Any older than 1 business day |
| Bad replies in sampled review that were also reported | Track from baseline | Review 100 sampled replies a month; share of the bad ones with a report | Falling |
| Report-form abandon rate (counter-metric) | Track from baseline | Thumbs-down events with no saved record, or reason step opened and closed | Rising two weeks in a row |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Thumbs-down event with no report record | Feedback event without a linked record id | A deliberate "undo" within seconds |
| Report record with no owner after one business day | Record fields owner and triaged_at empty | A holiday or a queue outage already announced |
| User says "that's wrong" or "report" in text and no report event follows | User turn text match, no report event in the next 2 events | User correcting a typo in their own message |
| Same complaint re-sent in a new chat | Same intent and reply topic reported twice from one user | A deliberate retest after a fix |
| Reply events with control_shown false | Reply event field | A planned maintenance window |

**Starter rule:** every bot reply has a report control, and every report creates a record with an owner and a confirmation code.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: no-way-to-report-bad-behaviour
runs: post_turn
reads: [reply.control_shown, feedback_event.type, report.reason, report.severity, report.owner, report.triaged_at]
trigger: user clicks thumbs-down or types a report request
moves: [offer_choices, hand_off, admit_uncertainty]
choices: ["Wrong information", "Harmful or unsafe", "Not helpful", "Something else"]
on_miss: log
metric: reports per 1,000 conversations; time to triage
counter_metric: report-form abandon rate
status: proposed
```

## 8. Related patterns
- [Satisfaction metric gaming](../../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/satisfaction-metric-gaming.md): closest match. It is about tuning the bot against thumbs-up scores. This pattern is about whether a report path exists, reaches a person, and leads to a fix.
- [User feedback bias](../../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/user-feedback-bias.md): few users click, so button data is not representative. Here the issue is the missing channel, not the sample.
- [Talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md): the user asks for a person in the live chat. This pattern is the after-the-fact report.
- [Generic error messages](../../errors-and-recovery/failures/generic-error-messages.md): the bot says it failed. Here the bot did not fail visibly; the user knows the reply was wrong.

## 9. Common questions
### How do I report a bad AI response?
Look for a thumbs-down or "report" control under the reply. If a product has none, use its support or help route (Intercom's FAQ, for one, points to its support team through the Messenger). Keep the reply text and time so you can quote it. See [the fix](#5-the-fix) for what a good path looks like.

### Does clicking thumbs-down do anything?
It depends on the product. Microsoft's page says only your thumbs choice is collected until you submit more detail. I found no source that says how fast any vendor reviews thumbs-down clicks. A team can make it real by giving each report an owner.

### How do I add a report button to my chatbot?
Add a control to every reply, save a record with the reply, chat, and optional reason, and assign a queue and owner. Send high-severity reports to a person first. Rules 1 to 9 in section 5 are the checklist.

### Should the bot ask users to rate every answer?
No. Keep the control available but quiet. Prompting after each reply adds friction and, as the library's [feedback bias page](../../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/user-feedback-bias.md) notes, still reaches only some users.

---
### Deep dive
- **Open question.** I found no study of whether adding a report control raises reports or improves fixes, and no public incident tied to a missing report path.
- **Unverified, kept out of the page.** OpenAI's statements on how thumbs data is used came to me only through search summaries; I could not open OpenAI's pages. Anthropic's retention terms for feedback also reached me only through third-party summaries.
- **Modality notes.** Voice (a spoken "report that") and visual surfaces are PLANNED, not written.
- **References.** [CFPB news release, 2023](https://www.consumerfinance.gov/about-us/newsroom/cfpb-issue-spotlight-analyzes-artificial-intelligence-chatbots-in-banking) (opened); [Intercom Fin FAQs](https://www.intercom.com/help/en/articles/7837535-fin-ai-agent-faqs) (opened); [Microsoft Support](https://support.microsoft.com/privacy/providing-feedback-about-microsoft-copilot-with-microsoft-365-apps) (opened); [Claude Help Center](https://support.claude.com/en/articles/10504853-manage-user-feedback-settings-on-claude-console) (opened).
