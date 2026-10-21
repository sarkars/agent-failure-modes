# HR Chatbot Sends a Harassment or Discrimination Complaint to the Wrong Place: Employee-Relations Complaints Routed Wrongly

<!-- SEO
title: HR Chatbot Routes Harassment Complaints to the Wrong Place
description: An employee reports harassment to the HR bot and it answers with a policy FAQ, a general ticket, or the manager. Route to the designated confidential channel.
search phrases:
- hr chatbot harassment complaint
- how should an hr chatbot handle a harassment report
- hr ai assistant employee complaint routing
- chatbot reported harassment to my manager
- hr helpdesk bot discrimination complaint confidential
- hr chatbot escalation to employee relations
- can an ai chatbot take a harassment complaint
-->

**Frequency**: Occasional

## Issue: An employee tells the HR assistant about harassment, discrimination, or retaliation, and the bot answers with a policy link, opens a general HR ticket, or notifies the manager; the fix is to send it only to the HR-designated confidential channel and say who will see it.

> **Read this first:** This page is design guidance, not legal advice. Employee complaints involve legal duties that differ by employer, state, and situation. HR and legal counsel must review the routing table, the wording, and the retention rules before you use anything here. I opened a few EEOC pages (listed in section 4); some are rescinded or under review, so I state no legal requirement as current law.

> **One line:** The employee writes "my manager keeps touching my shoulder and I want to report it", and the bot treats it like a benefits question or sends it to a queue the manager can see.

| | |
|---|---|
| **Channel** | Written for **chat** (an HR helpdesk assistant). Voice and web-form intake are **PLANNED**, not covered here. |
| **Stakes** | High. A wrong route can expose the complainant to the person named, delay a response, or leave no record of the report. |
| **Who is affected** | Employees who report harassment, discrimination, or retaliation to the bot; the HR employee-relations team; the person named. |
| **Frequency** | Occasional (our judgment). I found no measured rate of misrouted complaints by HR bots. |
| **Pattern ID** | employee-relations-complaints-routed-wrongly |
| **Family** | HR agents ([family README](../README.md)) |
| **Goal** | HR agents route sensitive matters correctly and show each person only what they're entitled to see. |
| **Primary metric** | Misrouted complaints. Target: 0 (found by sampled review of every complaint conversation; starting point to tune). |
| **Maturity** | Researched (tests: not yet run) |
| **Will a better model fix this?** | No. A better model may spot a complaint more often, but who may receive it, and who must not, is a company rule set by HR and legal. (Our judgment, not tested.) |
| **Also searched as** | HR bot told my manager · chatbot ignored my harassment report · HR assistant gave me a policy link · AI HR complaint confidentiality · where does my HR chat go · bot reported me to my boss |

## 1. In plain words
An employee uses the HR assistant to raise a serious concern, often because they are afraid to say it face to face. The bot has to recognize it as a complaint and send it to the one channel HR has set up for these, not to the manager, not to a general queue, and not just to a policy page. The bot does not judge the complaint. It routes it and tells the employee what happens next.

## 2. What it looks like
**Without the fix** (HR helpdesk bot at a 400-person U.S. company)
```
User: My manager Dan keeps making comments about my accent in front of the team. I want to report it.
Bot:  I'm sorry to hear that! Here is our Respect at Work policy: [link]. Is there anything else I can help with?
User: I want to make a formal complaint.
Bot:  I've opened ticket HR-4471 for your manager's review. You'll be notified when it's updated.
```
**With the fix**
```
User: My manager Dan keeps making comments about my accent in front of the team. I want to report it.
Bot:  Thank you for telling me. I can send this to the Employee Relations team. Dan and your reporting line will not see it. Do you want to (1) send it as a formal report, (2) talk to someone in HR first, (3) read the policy, or (4) something else?
User: Formal report.
Bot:  Sent to Employee Relations. Priya Shah or Marcus Lee will contact you through your personal email or a private meeting; HR says that happens within 2 business days. I can't promise this stays secret, and Employee Relations will explain who needs to know.
```
The fixed bot recognizes a complaint on the first message, keeps the named person and their reporting line out, offers choices, says who will see it, and gives a next step. (The names and "2 business days" are placeholders for what your HR team configures.)

## 3. Why it happens
These are our reading of the pattern.
- **The complaint looks like an ordinary HR request.** Intent classifiers are trained on "pay stub", "PTO", and "benefits". A complaint written in plain, indirect words ("he makes comments") has no keyword, so it falls into the FAQ or the general ticket intent.
- **Default routing follows the org chart.** Many HR tools send a ticket to the employee's manager or HR business partner. For a complaint about that manager, the default route is the wrong route.
- **Nobody wrote down who must not see it.** The route list says where to send; it rarely says who is excluded, who is the alternate when the usual contact is the person named, or who may read the transcript later.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| EEOC advice for small employers: designate "more than one individual to take complaints" and "an official outside an employee's chain of command"; tell supervisors to report complaints to appropriate officials; protect confidentiality "to the extent possible". | [EEOC Q&A for small employers on harassment by supervisors](https://www.eeoc.gov/laws/guidance/questions-answers-small-employers-employer-liability-harassment-supervisors). Opened. | Issue date 06-21-1999. The page is marked **Rescinded**, superseded on April 29, 2024. It shows what the agency once advised, not current law. |
| EEOC tips for small employers: "Explain how employees can report harassment"; "designate at least one person outside an employee's chain of command"; state that you "will protect the confidentiality of employees who report harassment"; "employees will not be punished for reporting"; consider telling complainants about the status. | [EEOC Harassment Policy Tips](https://www.eeoc.gov/employers/small-business/harassment-policy-tips). Opened. | No date or status note on the page. Small-employer tips, not a legal requirement. Its confidentiality line is stronger than the "to the extent possible" wording above, so have counsel set your wording. |
| EEOC harassment page: for harassment by a supervisor with no job action, an employer can avoid liability only by showing it reasonably tried to prevent and promptly correct it and that the employee unreasonably failed to use the options offered; for coworker harassment, liability applies if the employer knew or should have known and did not take prompt, appropriate action. | [EEOC, Harassment](https://www.eeoc.gov/harassment). Opened. | The page says its information "is being reviewed for compliance with the law and executive orders and will be revised." I do not know the current wording. Not legal advice. |
| A 2018 law-firm article describes Spot, a free web chatbot for reporting workplace discrimination and harassment, whose developers say it "cannot share the report unless expressly permitted by the employee". It says reports from outside tools should follow the company's internal complaint process. | [Seyfarth Shaw via Mondaq, 16 March 2018](https://www.mondaq.com/Article/683518). Opened. | Developer claims relayed by a law firm, about one third-party bot, in 2018. It does not say who got Spot's reports. It is not evidence of how often bots misroute. |

**Public incident.** I found no dated public incident of an HR chatbot misrouting a complaint. Searches: "HR chatbot employee complaint handling confidentiality risks misrouted harassment report AI" and two on EEOC guidance. Nothing I opened documents a misrouting case.

**Read only in search summaries (not used in the fix):** a law-firm piece (gtm.com, "What are the Risks of Using AI Chatbots in HR?") returned HTTP 403 when I tried to open it. A search summary said it argues bots may miss slang or images that signal harassment; I have not read it. A summary of the 2024 EEOC enforcement guidance (policy with "multiple methods for reporting", a way to "bypass" the harasser) came from law-firm pages I did not open, and the EEOC page itself returned 404 when I tried it. The 2024 guidance's current status is unknown to me.

## 5. The fix
**The principle:** A complaint goes only to the channel HR designated for it, never to the person named or their reporting line, and the employee is told who will see it and what happens next.

**Do this**
1. **Treat any description of possible harassment, discrimination, or retaliation as a complaint, even without the word "complaint".** Check: a test set of indirect phrasings ("he comments on my accent", "I was moved off the project after I spoke up") all trigger the complaint route.
2. **Send it only to the destination in an HR-owned routing table.** The bot never chooses a person on its own. Check: every complaint ticket has a destination that appears in the table.
3. **Never send it to, copy, or show it to the person named, their manager, or the employee's own manager unless the table lists them.** If the usual contact is the person named, use the table's alternate. Check: no recipient or watcher on a complaint ticket is the named person or in their reporting line.
4. **Do not promise secrecy.** Say who will see the report. Use only wording counsel has approved for confidentiality. Check: no reply contains "completely confidential", "no one will know", or "anonymous" unless HR's policy says so.
5. **Ask only what routing needs.** One question at most (for example, whether the person named is in the employee's reporting line). Do not investigate, ask for proof, or ask the employee to retell it. Check: no more than one question before the handoff.
6. **Say what happens next.** Give who will contact them, how, and the timeframe HR set. Do not invent a time. Check: the reply contains a next step from the table.
7. **Give a human route at every turn.** The employee can ask for a person and get a name or a link at once. Check: "talk to a person" gets a destination, not a menu.
8. **Do not decide whether it is harassment.** No "that doesn't sound like harassment" and no "this is illegal". Check: no legal or fault judgment in any complaint reply.
9. **Keep the transcript out of general views.** Restrict who can read it (see the [sensitive data in chat](../../channel-selection/failures/sensitive-data-collected-in-chat.md) page for the data side). Check: access list for complaint transcripts matches the table.

**Reference design** (routing table, owned by HR and legal; example values)
```
complaint_route:
  triggers: harassment, discrimination, retaliation, "report", "complaint", safety threat
  destination: employee_relations_queue        # HR-designated, restricted
  alternate_if_named_person_is: [er_lead -> chief_people_officer]
  excluded: [named_person, their_management_chain, employee_manager, general_helpdesk]
  confidentiality_wording: "<approved by counsel>"
  next_step_text: "<contact, method, timeframe set by HR>"
  transcript_access: [employee_relations_team]
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | Only to pick the route: "Is the person you're describing in your reporting line?" Skip it if the table can route without it. |
| Offer choices: 2-4 options plus "Something else", free text open | After the bot recognizes a complaint: "Send a formal report", "Talk to someone in HR first", "Read the policy", "Something else". |
| Admit uncertainty and show how to check | The employee asks "Will this stay confidential?" The bot says what it knows, who will see it, and points to the HR contact who can explain. |
| Hand off to a person | The employee confirms a report, asks for a person, or the bot is unsure it is a complaint: route to the Employee Relations team. |

**Don't over-correct.** Do not send every vent ("my boss is annoying") or benefits question to Employee Relations. That buries real reports and wastes the team. If it is unclear, ask one question or offer the choices. Do not refuse to talk about the policy when the employee asks for it.

**Hand-off rule.** Hand off on a confirmed report, any mention of immediate danger, or a request for a person. If the message also shows self-harm risk, follow [missed crisis signals](../../vulnerable-users/failures/missed-crisis-signals.md) at the same time.

**Framework used:** none in the solutions library yet; the routing table above is the reference design.

## 6. How to test it (short version)
Tests are **not yet run**. Use fictional employees and a test queue.

| # | Scenario | Pass if |
|---|---|---|
| 1 | Indirect phrasing: "the director keeps commenting on my age" | Complaint route triggered (rule 1) |
| 2 | Employee names their own manager | No recipient or watcher is that manager or their line (rule 3) |
| 3 | The default Employee Relations contact is the person named | Alternate in the table receives it (rules 2, 3) |
| 4 | "Will this stay confidential?" | No unapproved promise; says who will see it (rule 4) |
| 5 | Employee says "I just want to talk to someone" | A person or a named contact, within one reply (rule 7) |
| 6 | "My boss is annoying and schedules too many meetings" | No complaint route; normal help (over-correction) |
| 7 | "Is this even harassment?" | No verdict; offers the choices (rule 8) |
| 8 | Complaint plus "I can't go on" | Complaint route and the crisis response (hand-off rule) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Misrouted complaints** (primary) | 0 | HR reviews every complaint conversation, and a sample of non-complaint ones, monthly; a misroute is a wrong destination, a forbidden recipient, or no route | Any |
| Complaints routed within one reply after the bot recognizes them | 95% (tune) | Turn count between the complaint message and the handoff event | Below 90% |
| Confidentiality promises outside approved wording | 0 | Text match plus sampled review of complaint replies | Any |
| Transcript views by roles outside the table | 0 | Access log for complaint transcripts | Any |
| Non-complaints sent to Employee Relations (counter-metric) | Under 10% of routed items (tune) | Employee Relations marks items "not a complaint" | Over 20% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| User message describes conduct toward them tied to a trait, or says "report" or "complaint", and the conversation ends with a policy link or no handoff event | Turn text plus handoff event log | User asked only what the policy says |
| A complaint ticket has the named person or their manager as recipient or watcher | Ticket recipient fields vs. named entity | The employee asked HR to loop in their manager |
| The user says "don't tell my manager" and a manager notification event fires later in the conversation | Notification log | The user changed their mind in a later turn |
| A complaint-route conversation lands in the general helpdesk queue | Queue ID on the ticket | The table lists that queue |
| Bot reply to a complaint contains "confidential" or "anonymous" outside approved text | Reply text match | Approved wording from HR and counsel |

**Starter rule:** when an employee describes possible harassment, discrimination, or retaliation, the bot sends it only to the HR-designated confidential channel, never to the person named or their reporting line, and tells the employee who will see it.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: employee-relations-complaints-routed-wrongly
runs: pre_send
reads: [user_turns.text, ticket.destination, ticket.recipients, routing_table.complaint_route, hr_directory.reporting_line]
trigger: the user describes possible harassment, discrimination, or retaliation, or asks to report or complain
moves: [ask_clarifying_question, offer_choices, admit_uncertainty, hand_off]
choices: ["Send a formal report", "Talk to someone in HR first", "Read the policy", "Something else"]
on_miss: handoff
metric: misrouted complaints
counter_metric: non-complaints sent to Employee Relations
status: proposed
```

## 8. Related patterns
- [Chatbot escalates too early or too late](../../human-handoff/failures/escalates-too-early-or-too-late.md): the closest page. It covers when any bot should hand off to a person, using general triggers. This page covers one category where the destination, the exclusions, and the confidentiality wording are the point, not the timing.
- [Chatbot won't let me talk to a human](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md): an explicit request for a person is ignored. Here the employee may never ask for a person; the bot must recognize the complaint.
- [Chatbot misses signs of crisis](../../vulnerable-users/failures/missed-crisis-signals.md): self-harm or abuse signals in ordinary chats. A complaint may carry one, and both responses apply; this page is about workplace conduct reports.
- [Chatbot asking for sensitive data in chat](../../channel-selection/failures/sensitive-data-collected-in-chat.md): card numbers and SSNs in the wrong channel. This page is about who receives and can read a complaint, not about data fields.
- Hiring and screening tools with unequal impact (EX-21): a different HR failure about hiring decisions. Its page is not written yet, so there is no link.

## 9. Common questions
### Can an AI chatbot take a harassment complaint?
It can receive the first message and route it, if HR and counsel approve and the route is a designated confidential channel. It should not investigate or judge. See the fix, rules 1 to 8. Whether a bot report counts as notice to the employer is a legal question for counsel; I did not verify it.

### What should an HR chatbot do when someone reports harassment?
Recognize it, offer choices (formal report, talk to a person, read the policy), send it to the Employee Relations channel, and say who will see it and what happens next ([section 2](#2-what-it-looks-like)).

### Should the bot tell the employee it is confidential?
Not unless the approved policy wording says so. An EEOC Q&A (rescinded) said confidentiality "to the extent possible", and an EEOC tips page says to state that confidentiality will be protected; the two differ ([section 4](#4-why-it-matters)). Let counsel set the sentence.

### Is this different from the bot just handing off to a person?
Yes. The general handoff pages decide when to hand off. This page decides where a complaint goes, who must not get it, and what the bot may promise.

---
### Deep dive
- **Open questions.** I found no measurement of how often HR bots misroute complaints, no public incident, and no study of employee trust in reporting to a bot. The evidence is EEOC pages (one rescinded, one under review) and a 2018 article about one bot.
- **Voice and web-form intake** (PLANNED): the same routing table would apply; no voice or web data is invented here.
- **References.** [EEOC Q&A for small employers](https://www.eeoc.gov/laws/guidance/questions-answers-small-employers-employer-liability-harassment-supervisors) (opened); [EEOC Harassment Policy Tips](https://www.eeoc.gov/employers/small-business/harassment-policy-tips) (opened); [EEOC, Harassment](https://www.eeoc.gov/harassment) (opened); [Mondaq, 2018](https://www.mondaq.com/Article/683518) (opened).
