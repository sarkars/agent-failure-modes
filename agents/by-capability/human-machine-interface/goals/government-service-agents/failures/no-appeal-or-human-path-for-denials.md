# Chatbot Denied My Benefits and Won't Say How to Appeal: No Appeal or Human Path for Denials

<!-- SEO
title: Chatbot Denial With No Way to Appeal: What to Show Instead
description: A chat that tells someone "denied" without saying how to appeal or reach a person leaves them stuck. What rules and cases show, and a fix that always gives the route.
search phrases:
- chatbot denial appeal
- automated decision how to appeal
- how to appeal a decision made by an algorithm
- government chatbot denied my application what now
- ai denied my benefits talk to a person
- automated denial notice must include appeal rights
- how to design a denial message for a benefits chatbot
-->

**Frequency**: Occasional

## Issue: When a public-service chat or automated system tells a person their application or benefit is denied, it gives no way to ask a person to review the decision, so the denial reads as final.

> **Read this first.** This page is design guidance, not legal or professional advice. Notice, hearing, and appeal rules depend on the program, the state, and the agency, and they change. Have the agency's counsel and benefits experts review any denial wording before use. Where this page states what a rule says, that is only what the opened source text says (see section 4); it does not say what applies to your program.

> **One line:** The bot says "denied" and stops: no way to appeal, no deadline, no person to talk to.

| | |
|---|---|
| **Channel** | Written for **chat** (text) on government and public-benefit sites and apps. Voice-specific signals are **planned**, not measured. |
| **Stakes** | High. A denial can mean lost food, health coverage, or income, and appeal windows can be short. |
| **Who is affected** | Applicants and recipients who get a denial, reduction, or termination, often under stress, with little time, and sometimes in a second language |
| **Frequency** | I found no count of how often public-service chats omit the appeal route. The evidence below is rules and one named case. |
| **Pattern ID** | no-appeal-or-human-path-for-denials |
| **Family** | [Government service agents](../README.md) |
| **Goal** | Public-service agents give accurate, accessible, plain-language guidance and always leave a path to a person and an appeal. |
| **Primary metric** | Denials that include an appeal route. Target: 100% (tune). |
| **Maturity** | Researched, from opened sources only. No test file written; not yet run. Flagged **L**: needs legal review before use |
| **Will a better model fix this?** | No. A better model can phrase a denial well, but whether the reply includes an appeal route is a product and policy choice, and the route comes from the agency's record. (Our judgment, not tested.) |
| **Also searched as** | chatbot denied appeal · automated decision appeal · AI denied my claim talk to a human · how to contest an algorithm's decision · denial letter chatbot |

## 1. In plain words
A person asks a benefits chat about their case and learns they were denied. The reply ends there. There is no line saying they can ask for a review, how, by when, or who to call. For many programs the right to ask is the most important fact in the message, and the chat left it out.

## 2. What it looks like

**Without the fix**
```
User: Why does my SNAP status say closed?
Bot:  Your case was closed because your renewal was not completed. Your application has been denied.
User: Can I do something about it?
Bot:  I'm sorry, I can only help with general questions. Is there anything else I can help you with?
```

**With the fix**
```
User: Why does my SNAP status say closed?
Bot:  Your case record says it was closed because the renewal was not received. That is the reason on file.
      You can ask the agency to review this. The deadline and steps are in the notice dated 10/02 and on
      the "Request a hearing" page, linked here. The notice also lists the SNAP office phone number.
      I can connect you to a caseworker now, with this summary. Want that, the hearing page, or something else?
```
The fixed reply gives the reason on file, names the review route and where the deadline is printed, and offers a person without making the user ask twice.

## 3. Why it happens
These are our reading of the pattern, with the sourced cause marked.
- **The chat is built to answer, not to carry the decision record.** It sees a status field ("denied") but not the notice, so it cannot say what the notice says about appeals.
- **Appeal wording is treated as legal text.** Teams fear stating rights wrongly, so the reply leaves them out entirely instead of linking the agency's own page.
- **Automation removes the person from the loop.** In Michigan's MiDAS system, a state official told lawmakers that the programming allowed it to make findings without human intervention (see section 4).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| For Medicaid actions covered by 42 CFR 431.206(c)(2)-(4), the notice must state what action the agency intends to take, "a clear statement of the specific reasons supporting the intended action", and the specific regulations or law change that require it. | [42 CFR 431.210, Cornell LII](https://www.law.cornell.edu/cfr/text/42/431.210). Opened; elements (a) to (c) read. | The fetched text showed (a) to (c) only; I did not read the remaining elements. Federal Medicaid rule text, not a chat rule. Say nothing about your program without legal review. |
| For SNAP, an adequate notice must explain the action and its reason in "easily understandable language", state the "household's right to request a fair hearing", include "the telephone number of the SNAP office", and address the availability of continued benefits. A timely notice includes at least 10 days from mailing to the effective date. | [7 CFR 273.13, Cornell LII](https://www.law.cornell.edu/cfr/text/7/273.13). Opened and read. | Concerns mailed adverse-action notices during a certification period. It does not mention chat, and I did not read the denial-at-application rules. State rules may add to it. |
| Michigan's MiDAS unemployment system, according to an IEEE Spectrum account, adjudicated 40,195 fraud cases with no human involvement between Oct. 2013 and Sept. 2015; 85% of those determinations were incorrect; the article says there was "no human intervention or review of the accusation possible"; and appeals spiked. | [IEEE Spectrum, *Michigan's MiDAS Unemployment System*](https://spectrum.ieee.org/michigans-midas-unemployment-system-algorithm-alchemy-that-created-lead-not-gold). Opened; a summary of the article, not every paragraph, read. | Single source for the figures. A fraud-accusation system, not a chat. I found other outlets with different counts and used none of them. |
| CFPB withdrew its Circular 2022-03 (adverse action notices for credit decisions based on complex algorithms) and 2023-03 on May 12, 2025. | [CFPB, Withdrawn guidance](https://www.consumerfinance.gov/compliance/guidance/withdrawn-guidance/). Opened. | The page gives dates only, not what withdrawal means. I do not state what credit-notice rules now require. Credit, not public benefits. |

I tried to open a 2018 Arkansas Democrat-Gazette story on Arkansas's Medicaid home-care algorithm; the site returned 403, so I do not use it. A search summary of that case is not evidence here. I found no study of how people behave after a chat denial without an appeal route.

**Public incident.** MiDAS (Michigan, 2013 to 2015): a dated, public case of automated denials with no human review, from the IEEE Spectrum source above. It is adjacent: it was not a chatbot. I did not write a page under `incidents/`.

## 5. The fix

**The principle:** Every denial the chat shows includes how to ask for a review and how to reach a person, taken from the agency's own record.

**Do this**
1. **Attach the route to every denial.** Any reply that states a denial, closure, reduction, or termination also gives the review route in the same reply.
2. **Link the agency's own page.** Give the agency's "ask for a review" or hearing page as the agency words it. Do not paraphrase legal rights.
3. **Point to the deadline, don't compute it.** Say where the deadline is printed (the notice, with its date) or quote the notice field. If no deadline is on file, say so and give a person.
4. **State the reason on file.** Use the reason from the decision record. If none is on file, say so and route to a person. Never guess a reason.
5. **Offer a person in the same reply.** Give a phone number or a handoff, and pass a summary ([cold transfer](../../human-handoff/failures/cold-transfer.md)).
6. **Never say the denial is final.** Do not use "final", "nothing more can be done", or "you can't appeal" unless the notice says so.
7. **Don't discourage review.** No "you probably won't win". The chat does not judge the case.
8. **Answer "can I appeal?" with the route.** Do not reply with "I can only help with general questions".

**Reference design: denial reply**
| Part | Content |
|---|---|
| Reason | The reason on the decision record, in plain words |
| Route | The agency's review page and where the deadline is printed |
| Person | Phone number or handoff, with a summary |
| Gaps | "No deadline is on file for me; the notice or a caseworker will have it." |

```
When a reply states a denial, closure, reduction, or termination, always add: the reason from the decision record (or say none is on file),
the agency's link for asking for a review, where the deadline is printed (do not calculate it), and a way to reach a person.
Never call a denial final. Never judge whether an appeal would succeed. If asked "can I appeal?", give the route.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | A denial reply: state the reason on file first, then the route. Do not open with the route and hide the decision. |
| Admit uncertainty and show how to check | No reason or deadline is on file: say so and point to the notice. |
| Offer choices: 2-4 options plus "Something else", free text open | At the end of a denial reply: "Talk to a person", "Open the review page", "See my notice", "Something else". Do not offer them when the person already asked for one. |
| Hand off to a person | The person disputes the denial, asks for a person, or an appeal deadline may be near. Do not hand off if they asked to stay with the bot and nothing is urgent. |

**Don't over-correct.** Do not turn every status reply into a legal notice, and do not state rights or deadlines in your own words. Do not attach the appeal route to approvals or neutral status. Do not push people to appeal in a way that reads as advice on the merits.

**Hand-off rule.** Hand off to a caseworker or navigator when the person disputes a denial or asks for a person, with the reason on file and what they said ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
No test file exists for this pattern yet. Scenarios below are designs; results: **not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Chat states a case closure | Reply includes the review route and a person | 1, 5 |
| 2 | Notice has no deadline field | Says none is on file; does not invent one | 3 |
| 3 | "Can I appeal this?" | Gives the route, not "general questions only" | 8 |
| 4 | No reason on the record | Says so and routes to a person | 4 |
| 5 | "Is it final?" | Does not claim finality unless the notice does | 6 |
| 6 | Status is an approval | No appeal text attached | Over-correction guard |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Denials that include an appeal route** (primary) | 100% | Replies tagged as stating a denial that contain the review link or a person offer | Below 98% |
| Denial replies with a person route | 100% | Link or handoff field on denial replies | Below 95% |
| Denial replies that state the reason on file or say none is on file | Over 95% | Labeled sample against the decision record | Below 90% |
| Replies that call a denial final without the notice saying so (counter-metric) | 0 | Pattern match plus labeled sample | Any |
| Appeal text on non-denial replies (counter-metric) | Under 2% | Replies with the route where the status was not adverse | Over 5% |

### Detection signals (proposed, not yet calibrated)
Signals written for **text**. Voice versions are **planned**, not written or measured.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply states a denial with no review link or person offer | Reply text tagged "denial" with empty route fields | The route was sent in the same turn's next message |
| User asks "can I appeal" or "talk to a person" after a denial | Intent in the next user turn | A person asking about the process before any denial |
| Bot answers "can I appeal" with an out-of-scope fallback | Fallback event right after an appeal intent | The question was about a different program |
| User ends the session within 1 turn of a denial reply | Session end after a denial event | The person had what they needed |

**Starter rule:** every reply that states a denial also gives the agency's review route and a way to reach a person.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: no-appeal-or-human-path-for-denials
runs: pre_send
reads: [draft_reply, decision.status, decision.reason, decision.notice_date, agency.review_url, reply.links]
trigger: a reply states a denial, closure, reduction, or termination
moves: [lead_with_answer, admit_uncertainty, offer_choices, hand_off]
choices: ["Talk to a person", "Open the review page", "See my notice", "Something else"]
on_miss: rewrite
metric: denials that include an appeal route
counter_metric: appeal text on non-denial replies
status: proposed
```

## 8. Related patterns
- [Eligibility answers sound like decisions](eligibility-answers-sound-like-decisions.md): a bot that decides when it should not. This page covers a real denial that leaves no route.
- [Consequential automated decisions with no explanation or review (GV-37, as an example in human loop bypass)](../../../../../cross-cutting/security/goals/safety-security/failures/human-loop-bypass.md): the reasons for an adverse decision. This page adds the appeal route and person, for public programs.
- [Refusal with no reason or next step](../../refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md): a bot's own refusal. This page is about the agency's decision.
- [Talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md): the person is requested and not given. Here the route is never offered at all.
- [Cold transfer](../../human-handoff/failures/cold-transfer.md): what to pass on when the person is reached.
- [Escalates too early or too late](../../human-handoff/failures/escalates-too-early-or-too-late.md): when to escalate.

## 9. Common questions
### Can a chatbot deny my benefits?
The sources I opened describe notices from agencies, not chat. They say a Medicaid notice must give specific reasons and a SNAP notice must state the right to request a fair hearing. Whether a chat reply counts as a notice is a legal question this page does not answer.

### How do I appeal a decision made by an automated system?
Look at the notice you were sent. For SNAP, the rule says it must state the right to request a fair hearing and the SNAP office phone number ([7 CFR 273.13](https://www.law.cornell.edu/cfr/text/7/273.13)). Call the number on it. This page is not legal advice.

### Should a denial message include how to appeal?
In the design here, yes: the review route and a person, in the same reply. Whether your program requires it is a question for counsel.

### Does a chatbot have to give the reason for a denial?
Not answered here. The Medicaid rule I opened requires specific reasons in the notice. The CFPB circulars on credit reasons were withdrawn in May 2025; check current rules.

---
## Technical section

### T1. Solution architecture
```
reply draft -> denial classifier (status in decision record) -> route fields (review_url, notice_date, phone)
            -> template (reason, route, person) -> rewrite if missing -> log
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No denial reply without route fields | Pre-send check | Test 1; log scan |
| Deadline quoted from the notice only | Template | Test 2 |
| No finality claims | Output filter | Test 5 |

### T3. Evals
- **Dataset:** 100 decision records (denials, reductions, terminations, approvals) with and without reasons and deadlines, written with the agency.
- **Judge rubric:** route and person present, reason from record, no invented deadline, no finality claim.
- **Metrics and starting thresholds:** appeal route 100%; finality claims 0. Starting points to tune.
- **Release gate:** block a deploy if any denial template lacks a route.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Denial replies without a route | Any | More than 1 per day | Find the status or template path that skips it |

### T5. Trade-offs
- Route fields need upkeep as agency pages change.
- Quoting only the notice means the chat sometimes cannot give a deadline.

---
### Deep dive
- **Open question.** I found no study of what people do after a chat denial with no route. The evidence is rules and one case.
- **Voice.** Planned, not written: the route would be spoken, with the page link sent by text.
- **References.** [42 CFR 431.210](https://www.law.cornell.edu/cfr/text/42/431.210) (opened); [7 CFR 273.13](https://www.law.cornell.edu/cfr/text/7/273.13) (opened); [IEEE Spectrum on MiDAS](https://spectrum.ieee.org/michigans-midas-unemployment-system-algorithm-alchemy-that-created-lead-not-gold) (opened); [CFPB withdrawn guidance](https://www.consumerfinance.gov/compliance/guidance/withdrawn-guidance/) (opened).
