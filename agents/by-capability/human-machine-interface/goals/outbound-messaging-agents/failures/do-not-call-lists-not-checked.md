# AI Agent Called Numbers on the Do Not Call List: Do-Not-Call Lists Not Checked

<!-- SEO
title: AI Agent Calling Do Not Call Numbers: Check Lists Before Each Contact
description: Why an outbound AI agent texts or calls numbers on a do-not-call list, and how a per-contact suppression check, refresh cadence and log stop it.
search phrases:
- ai agent calling numbers on do not call list
- how to scrub do not call list for ai outbound calls
- how often to check national do not call registry
- internal do not call list for ai texting agent
- outbound ai voice agent dnc compliance
- ai agent texted me after I said stop
- suppression list check before every call or text
-->

**Frequency**: Common

## Issue: An outbound AI agent contacts numbers that opted out (national registry, state lists, the company's own do-not-contact list, STOP replies) because the lists are checked once per campaign, or not across channels and vendors.

> **One line:** The number was on a do-not-contact list and the agent contacted it anyway; the fix is a suppression check before every single contact, a refresh cadence for each list, one opt-out record shared by every channel and vendor, and a log of each check.

> **Read this first.** This page is design guidance, not legal advice. A lawyer should review your lists, deadlines, exemptions, and records before use. It states a law only as far as a source I opened says (section 4). Whether a rule covers your calls or texts, and which state lists apply, is for counsel. I did not open any state list rule, so the page says nothing about specific states.

| | |
|---|---|
| **Channel** | Written for **chat and text** (SMS) follow-ups, plus the shared list logic. **Voice** checks are PLANNED, not written, and nothing here is measured on calls. |
| **Stakes** | High. Each contact can be a separate violation (flag L), and an agent can place thousands before anyone notices. |
| **Who is affected** | People on the national registry, on a state list, on the company's own list, or who replied STOP to any past message |
| **Frequency** | Common by design risk (campaign lists go stale; section 3). I found no study that counts how often AI outbound agents reach suppressed numbers. |
| **Pattern ID** | do-not-call-lists-not-checked |
| **Family** | [Outbound messaging agents](../README.md) |
| **Goal** | Outbound texts and calls respect consent, quiet hours, and suppression lists. |
| **Primary metric** | Contacts to suppressed numbers. Target: 0 (starting point). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The model can read "do not contact me" perfectly and still dial, because the number sits on a list the dialer never checked. The send gate must fix it. (Our judgment, not tested.) |
| **Also searched as** | ai calling numbers on dnc · scrub leads against do not call · internal do not call list for bots · outbound agent ignored opt-out · texted after I registered on do not call · dnc check before dialing |

## 1. In plain words
An outbound agent works from a lead list built days or weeks ago. Numbers have since joined the national registry, replied STOP, or been added to the company's own do-not-contact list. If the list is checked once when the campaign starts, the agent keeps contacting them. The person sees a company that ignored a clear "do not contact" signal, and the company carries the legal risk.

## 2. What it looks like
**Without the fix**
```
Day 1   Campaign "Spring plan" loaded: 4,000 numbers, checked once against the registry.
Day 9   Ray (555-0142) texts "STOP" to the billing reminder line. Saved only in the billing tool.
Day 14  Outbound agent (sales line) to Ray: Hi Ray, Maria from Acme. Want a quote on the Pro plan?
Day 20  Support adds Ray's number to the company's internal do-not-contact list.
Day 26  Outbound agent (follow-up job, same campaign file) to Ray: Just checking in on that quote!
```
**With the fix**
```
Day 9   Ray texts "STOP". One shared suppression record: phone 555-0142, all agents, all channels, source = STOP reply.
Day 14  Sales agent: send blocked at the gate. Logged: contact, lists checked, list versions, reason = stop_reply.
Day 20  Support adds Ray to the internal list. Already suppressed; no change needed.
Day 26  Follow-up job: blocked at the gate, logged. Nothing sent to Ray.
```
The fixed version checks every list at the moment of each contact, applies Ray's STOP to every agent and channel, and leaves a record of each check.

## 3. Why it happens
- **The check runs once per campaign.** The lead file is scrubbed at upload. Registry additions, STOP replies, and internal requests that arrive afterward are never seen by later sends.
- **Opt-outs live in separate tools.** The billing text tool, the sales dialer, and the vendor's AI agent each keep their own list, so a STOP in one is invisible to the others.
- **Nobody owns the refresh.** The registry file, state lists, and internal list update on different schedules, and nothing records which version a given contact was checked against.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| "You must synchronize your lists with an updated version of the registry at least every 31 days." For the safe harbor, the seller or telemarketer must show it "accesses the national registry no more than 31 days before calling any consumer." | [FTC, *Q&A for Telemarketers & Sellers About DNC Provisions in TSR*](https://www.ftc.gov/business-guidance/resources/qa-telemarketers-sellers-about-dnc-provisions-tsr) (Q16, Q62). Opened 2026-10-21. | Telemarketing calls under the FTC rule. The page does not address text messages. 31 days is a maximum, not a recommended cadence. |
| A consumer not on the registry can "prohibit individual telemarketers from calling by asking to be put on the company's own do not call list." Even with an established business relationship, "the company must honor the request not to call." | Same FTC Q&A (Q10). Opened 2026-10-21. | The page does not say how long these requests last. The FCC rule below gives 5 years. |
| The safe harbor for "inadvertent mistakes" requires, among other things, "a company-specific list of telephone numbers that it may not call", written procedures, staff training, and registry access within 31 days before calling. A violating call must have been "the result of an error." | Same FTC Q&A (Q62). Opened 2026-10-21. | A defense that applies only if every listed step is met. It does not cover a check that never ran. Counsel decides whether it applies. |
| "Violators may be subject to fines of up to $53,088 per violation." "Each call may be considered a separate violation." | Same FTC Q&A (Q60). Opened 2026-10-21. | The amount is inflation-adjusted and was current on the page date. Check the current figure. |
| Internal do-not-call procedures must include a written policy "available upon demand", training of personnel, recording the request and placing the number on the list "at the time the request is made", and honoring it within a reasonable time that "may not exceed ten (10) business days." A request "must be honored for 5 years from the time the request is made." | 47 CFR 64.1200(d)(1)-(3), (d)(6), read at [Cornell Law School LII](https://www.law.cornell.edu/cfr/text/47/64.1200). Opened 2026-10-21. | Read at LII, not eCFR. A search summary said older copies show 30 days; the text I opened says ten business days. An FCC proposal to change these rules appeared in a summary I could not confirm, so check current status. |
| The registry safe harbor in 47 CFR 64.1200(c)(2)(i)(D) asks for a registry version obtained "no more than 31 days prior to the date any call is made." | Same LII page. Opened 2026-10-21. | Same version caveat. |
| Consent-revocation rules for texts (STOP words, exclusive revocation methods, scope of a revocation) are being changed by FCC orders. | Search summaries only (FCC 24-24 and a later order). I did not open the orders. | Not opened. No revocation-scope or effective-date claim appears in the fix. The [unsubscribe page](../../sales-agents/failures/unsubscribe-requests-not-honoured.md) cites the rule text it read. |

I searched for a public incident of an AI agent contacting numbers on a do-not-call list and found none I could open. **Public incident.** None found.

## 5. The fix
**The principle:** Every contact is checked against every suppression list at the moment it is made, with one shared opt-out record across channels and vendors, and the check is logged.

**Do this**
1. **Check at the send gate, per contact, per attempt.** Before each call, text, or chat follow-up, look the number up in every list below. A campaign-start scrub is not enough.
2. **Check these lists:** the national registry, any state lists your counsel names, the company's own do-not-contact list, and the STOP-reply record. Block the contact if any list has the number.
3. **Set a refresh age limit for each list.** Registry copy: never older than 31 days at contact time (FTC and FCC text, section 4). Internal list: read live, not from a copy. Starting point for the registry and state lists: refresh weekly, and block sends when a copy is older than its limit.
4. **Fail closed.** If a list cannot be read, or its copy is past its limit, block the contact and alert an owner. Do not send "just this once".
5. **Share the opt-out.** A STOP reply, a "do not call me" in chat, or an agent-recorded request writes one suppression record (phone, person ID, source, time) that every agent, channel, and vendor reads. Write it at the time the request is made.
6. **Make vendors check your list too.** A vendor's agent must receive your suppression list or call your check before each contact. Do not rely on the vendor's own list alone.
7. **Log each check:** contact ID, time, lists checked, the version or date of each list, result (allowed or blocked), and which agent asked.
8. **Keep an internal request for 5 years** or the period counsel sets; never delete it when a campaign closes (section 4).

**Reference design: per-contact check (pseudo-code)**
```
before ANY outbound contact X to number N by agent A on channel Ch:
    results = {}
    for list in [national_registry, state_lists, internal_dnc, stop_replies]:
        if list.copy_age_days > list.max_age_days: block X; alert owner; log(check_failed, list); return
        results[list] = list.contains(N)
    log(check, N, A, Ch, now, list_versions, results)
    if any(results.values()): block X; log(blocked, reason=first_hit); return
    send X
on opt-out from N (STOP reply, "do not contact me", agent-recorded request):
    suppress(N, person_id, scope="all_channels_all_agents_all_vendors", source, received_at=now)
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The person says "stop" or "don't call me": confirm in one line that the number is removed from all contact. |
| Ask one clarifying question | The scope is unclear ("pause this"): "Do you want me to stop all texts and calls from Acme?" Not when the request is clear. |
| Hand off to a person | The person says they were contacted after opting out, or a check failed or timed out: pass the contact ID and check log to a human owner. |

**Don't over-correct.** Do not block people who asked to hear from you, or send nothing at all because a list is slow. Keep service messages the person requested (receipts, appointment notices) separate from marketing, and let counsel decide which is which. Do not ask a person to repeat or justify an opt-out. A fail-closed gate is meant for the list-unreadable case; fix the list feed, not the gate.

**Hand-off rule.** If a person says they were contacted on a suppressed number, or any contact to a suppressed number is found in the log, send the case (contact ID, list hit, send log) to a human owner the same day (starting point).

**Framework used:** none yet.

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | A number is added to the internal list after the campaign was loaded; the agent's next attempt runs | Contact blocked and logged with `internal_dnc` | 1, 2 |
| 2 | A number is on the registry copy and the copy is 20 days old | Contact blocked | 2, 3 |
| 3 | The registry copy is 40 days old and the number is not in it | Contact blocked and an owner alerted | 3, 4 |
| 4 | The internal list service times out | Contact blocked, not sent | 4 |
| 5 | Ray texts STOP to the billing line; the sales agent tries a call next day | Sales call blocked | 5 |
| 6 | A vendor agent receives the same lead after an opt-out | Vendor send blocked by your check | 6 |
| 7 | Any allowed contact | Log has contact ID, lists checked, list versions, result | 7 |
| 8 | Campaign is closed and the opt-out record is read later | Record still present | 8 |
| 9 | Person says "pause this" | One clarifying question, no suppression until answered | Moves, Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Contacts to suppressed numbers** (primary) | 0 | Join each sent contact to the suppression lists as of send time (including records that reached a list later but carry an earlier effective time) | Any |
| Contacts sent with no logged check | 0 | Sent contacts without a matching check record | Any |
| Contacts checked against a list older than its limit | 0 | `list_versions` age at check time vs max age | Any |
| Opt-outs applied to all channels and vendors | 100% | Suppression records with scope `all_channels_all_agents_all_vendors` | Below 100% |
| Contacts blocked by fail-closed (counter-metric) | Track; set from baseline | Blocks with reason `check_failed` | Rising |

### Detection signals (proposed, not yet calibrated)
Written for text event logs. Voice signals are PLANNED. None are measured.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A send to a number with a suppression record dated before the send | `send.number` joined to `suppression.received_at` | The person re-subscribed on purpose |
| A send with no check event for the same contact and time | `send.id` with no `check.id` | A check logged by another service with a delay |
| A check using a registry copy older than the limit | `check.list_versions` age | A list refresh that finished just after the check |
| Same number contacted by two agents or vendors after an opt-out | `send.agent_id`, `send.vendor` per number | A service message the person asked for |
| User says "I told you to stop" or "I'm on the do not call list" | Opt-out phrases in the next user turn | A message about a different company |

**Starter rule:** every contact is checked against every suppression list at the moment it is made, with one shared opt-out record across channels and vendors, and the check is logged.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: do-not-call-lists-not-checked
runs: pre_send
reads: [send.number, send.agent_id, send.channel, suppression.number, suppression.received_at, check.list_versions, list.copy_age_days, inbound.text]
trigger: any outbound call, text, or chat follow-up is about to be sent, or an opt-out is received
moves: [lead_with_answer, ask_clarifying_question, hand_off]
choices: none
on_miss: log
metric: contacts to suppressed numbers
counter_metric: contacts blocked by fail-closed
status: proposed
```

## 8. Related patterns
- [Sales bot keeps messaging after "stop"](../../sales-agents/failures/unsubscribe-requests-not-honoured.md): the closest page. It covers honoring one person's opt-out across email, text, and chat in a sales agent. This page covers the check before each outbound call or text against external lists (registry, state) as well as the internal one, and the refresh age of each list.
- [Collections calls without required disclosures](../../voice-receptionist-agents/failures/collections-calls-without-required-disclosures.md): an outbound voice call with a rule the agent must follow; this page is about whether the contact should be made at all.
- [Marketing texts without consent](marketing-texts-without-consent.md): sibling; whether consent exists before the first text. This page is about numbers that opted out later or should not be on the list.
- [Quiet hours and time zones ignored](quiet-hours-and-time-zones-ignored.md): sibling; the time of the contact. This page is about who is contacted.
- [Outbound messaging agents family](../README.md): sibling outbound patterns.

## 9. Common questions
### How often do I have to check the National Do Not Call Registry?
The FTC Q&A says to synchronize your lists with an updated registry at least every 31 days, and the safe harbor asks for access no more than 31 days before calling (section 4). Treat that as a ceiling; many teams refresh more often. Ask counsel what applies to your calls.

### Is a check at campaign start enough?
No. Numbers can join the registry, reply STOP, or be added to your internal list after upload. This page checks per contact, at send time (section 5, rule 1). The FTC safe harbor also depends on the 31-day limit holding for each call.

### Does an internal do-not-call request last forever?
The FCC rule text I opened says a request must be honored for 5 years from the time it is made (section 4). The FTC Q&A page does not state a duration. Keep records for at least that long and ask counsel.

### Do the registry rules cover AI texts?
The FTC Q&A I opened does not address text messages, and I did not open the rules that do. Treat a STOP reply as an opt-out for every channel (rule 5) and ask counsel which text rules apply to you.

### If a vendor's AI agent makes the calls, who checks the list?
You should, at your own gate (rule 6). I did not open a source on vendor liability for this page, so counsel should say who is responsible under your contract.

---
## Technical section

### T1. Solution architecture
```
lead / follow-up job -> send gate -> list lookups (registry copy, state copies, internal list live, STOP record)
                                  -> check log (contact, lists, versions, result)
                                  -> allow -> dialer / SMS gateway / chat   |   block -> alert owner
inbound STOP / "do not contact me" -> opt-out detector -> shared suppression store -> read by all agents and vendors
list refresh jobs -> registry and state copies with fetched_at and max_age_days
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Check every contact, every list | Send gate, not the campaign tool | Tests 1, 7; sends with no check |
| Refresh age limit per list | Send gate reads `copy_age_days` | Tests 2, 3 |
| Fail closed | Send gate | Test 4 |
| One shared opt-out record | Suppression store | Tests 5, 6 |
| Log each check | Check log | Test 7 |

### T3. Evals
- **Dataset:** replay a campaign file with 200 contacts to start: some on each list, some added after upload, some with stale list copies, some opted out on one channel only.
- **Judge rubric:** was each suppressed contact blocked; did each allowed contact have a complete check record; was the opt-out visible to every agent and vendor path?
- **Release gate:** block a deploy if any replayed contact to a suppressed number is sent (starting point).

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Contacts to suppressed numbers | Any | Any | Pause the campaign; find the missed list |
| List copy older than its limit | 80% of limit | At limit | Refresh the feed |

### T5. Trade-offs
- A per-contact check adds a lookup to every send; cache the registry and state copies, read the internal list live.
- Fail closed can pause a campaign during a list outage. That cost is accepted; fix the feed.
- Matching numbers across formats (E.164) and across vendors is the main way a send gets through.
