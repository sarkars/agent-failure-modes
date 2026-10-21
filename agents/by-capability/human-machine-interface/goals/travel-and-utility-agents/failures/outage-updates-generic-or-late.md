# Power Outage Chatbot Says "We Are Working on It": Outage Updates Generic or Late

<!-- SEO
title: Outage Chatbot Says "Working on It": Updates That Name Cause and Time
description: Why a utility or telecom chatbot that says "we are working on it" fails customers during an outage, what outage-communication sources say, and a template with cause, area, and next update time.
search phrases:
- power outage chatbot restoration time
- outage status update template
- internet outage chatbot says working on it
- utility outage chatbot no estimated restoration time
- how often should a utility update customers during an outage
- what to say in an outage update when you have no ETA
- telecom outage chatbot design
-->

**Frequency**: Common

## Issue: During an outage, the utility or telecom chatbot says "we are working on it" and nothing more: no cause, no affected area, no time for the next update, and updates that arrive late or not at all.

> **One line:** The bot says crews are working, and the customer still cannot tell what broke, who is affected, or when they will hear again.

| | |
|---|---|
| **Channel** | Written for **chat** (web chat, app, text). Voice (an outage hotline) is PLANNED, not written or measured. |
| **Stakes** | Medium to high. Customers decide whether to wait, move food or medicine, find another place to work or stay, or call for help. |
| **Who is affected** | Customers of power, gas, water, internet, and mobile services during an outage, planned or not |
| **Frequency** | Common. This is our judgment from how outage bots are usually built (a lookup plus a fixed line). I found no study that counts how often bots do this. |
| **Pattern ID** | outage-updates-generic-or-late |
| **Family** | [Travel and utility agents](../README.md) (row TV-02) |
| **Goal** | Travel and utility agents give the real rule, the real status and the next step, and offer a person when a customer is stranded or without service. |
| **Primary metric** | Updates with an estimated next update time. Target: 100% (tune). |
| **Maturity** | Researched. Some sources were blocked or read through summaries only (see section 4). |
| **Will a better model fix this?** | No. What the bot can say depends on the outage data it is given and on the update schedule the company commits to. (Our judgment, not tested.) |
| **Also searched as** | outage status update · power out chatbot no ETA · internet down "we are aware" · outage update template · restoration time estimate |

## 1. In plain words
A storm or a fault knocks out service. The customer opens chat and gets "We are aware of an outage and are working to restore service." That is true and no use. It does not say what failed, whether the customer's street is in the affected area, or when the next update will come. So the customer checks again and again, or calls.

## 2. What it looks like

**Without the fix**
```
User: Power's been out since 4. When is it coming back?
Bot:  We are aware of an outage in your area and our crews are working on it.
User: Do you know what caused it?
Bot:  We are working to restore service as soon as possible. Thank you for your patience.
(No further message arrives. At 9 p.m. the customer asks again.)
```
**With the fix**
```
User: Power's been out since 4. When is it coming back?
Bot:  Your outage (ZIP 78704, about 1,200 customers) was caused by a damaged transformer. A crew is on site.
      I don't have a restoration time yet; the crew will give one after they finish checking the damage.
      Next update from me by 7:30 p.m., sooner if the estimate changes. Want a text at that time?
      [Text me the update] [Report a downed line] [Talk to a person]
```
The fixed reply gives the cause, the area, what is not yet known, and a clock time for the next update, and it keeps its promise.

## 3. Why it happens
These are our reading of the pattern.
- **The bot only reads a status field.** The outage system may hold a cause code, a crew status, and an estimate, but the chat template shows one fixed line.
- **No owner for the update clock.** Nobody is assigned to publish by a set time, so an update goes out when someone remembers, or when the customer asks.
- **An estimate that is not ready is hidden, not explained.** Teams fear a wrong time, so they show none and say nothing about why.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Atlassian's Statuspage guidance says: "Provide updates every 30 minutes (or whatever cadence is appropriate for the situation)", advises early on to "promise further updates", and says to "Own the problem" even if another provider caused it. | [Atlassian Support, *Incident communication tips*](https://support.atlassian.com/statuspage/docs/incident-communication-tips). Opened and read. | Guidance for software status pages, not for utilities or telecoms. The page gives no specific next-update time. |
| A post on incident updates without a recovery estimate says to label three times separately (evidence time, recovery estimate, next communication checkpoint), warns that "Next update by 11:30 UTC" must not read like "service returns at 11:30 UTC", and says the checkpoint promise should continue even when the estimate is withdrawn. | [Dhandala, *How to Write Useful Incident Status Updates Without a Recovery ETA*, OneUptime, Sept. 29, 2026](https://oneuptime.com/blog/post/2026-09-29-status-updates-without-recovery-eta/view). Opened and read. | One vendor's blog post, not a study. The 30-minute figure in it is an example, not a rule. |
| A utility-industry podcast page quotes a Chartwell speaker saying customers rank "the estimated restoration time, the crew status, and the geographic area impacted by the outage" as most important. The page says about 40% of customers wanted hourly updates in a 2023 survey of outages over six hours, 18% every two hours, and 36% contact only when information changed. | [KUBRA, *Navigating outages* podcast page, May 7, 2025](https://www.kubra.com/blog/navigating-outages-driving-sustainability-utilities-roadmap-podcast). Opened and read. | Vendor page, secondhand description of a survey. The page states no sample size, and the top-three ranking is not tied to a survey year. |
| J.D. Power residential electric studies (2012 to 2015) link proactive, regular outage communication to higher satisfaction. | [J.D. Power press release, 2013](https://www.jdpower.com/business/press-releases/2013-electric-utility-residential-customer-satisfaction-study). Read through a summary only; the page returned 403 when I tried to open it. | Not used in the fix. Old, and I did not read the source text. |
| FCC rules cover outage reports to the FCC and to 911 centers; a proposal about customer notice of 911 outages was described in a 2021 fact sheet. | [FCC 911 outages reporting](https://www.fcc.gov/enforcement/areas/911-outages-reporting). Read through a summary only; the page returned 403 when I tried to open it. | Not used in the fix. I state no legal duty on this page; check current FCC and state rules with counsel. |

Two more sources I tried (a Renewable Energy World article and an E Source deck) returned 403 and 404, and two state commission filings did not load, so I use none of them. I found no study that compares generic and specific outage messages from a chatbot.

**Public incident.** No public incident found for a chatbot giving generic outage updates. I ran three searches (utility outage communication, status page update cadence, FCC outage reporting) and found guidance and vendor material, not a dated, sourced incident about a bot.

## 5. The fix

**The principle:** Every outage update says what happened, who is affected, what is not yet known, and when the next update comes, then keeps that time.

**Do this**
1. **Name the cause in plain words when it is known.** "A damaged transformer", "a fiber cut". If unknown, say "the cause is still being checked".
2. **Name the area.** Use the customer's ZIP, street, or account address, and the count of customers if the system has it.
3. **Give the next update time as a clock time.** "Next update by 7:30 p.m." in every update, even when there is no restoration estimate.
4. **Keep the two times apart.** A next-update time is not a restoration time. Label them separately so one cannot be read as the other.
5. **Say what is unknown and why.** "No restoration time yet; the crew is still checking the damage." Never invent an estimate.
6. **Update on or before the stated time.** If nothing changed, say so ("Still no estimate; next update by 8:30 p.m."). A missed time is a failure.
7. **Show estimates as given by the outage system, with the time they were made.** If the estimate changes, say it changed and why.
8. **Offer a person and the safety route.** A downed line or a customer on medical equipment goes to the emergency or priority route, not to another status line.

**Reference design: outage update**
| Part | Content |
|---|---|
| What | "Cause: [plain-words cause, or 'still being checked']." |
| Where | "Area: [customer's ZIP or street], about [N] customers." (only if known) |
| Status | "Crew: [on site / on the way / assessing]." |
| Estimate | "Restoration: [time as given, made at 5:10 p.m.] or 'not yet available'." |
| Next | "Next update by [clock time], sooner if this changes." |
| Help | "[Text me the update] [Report a downed line] [Talk to a person]" |

```
During an outage, every update has: cause, area, crew status, restoration estimate or "not yet available", and "Next update by <clock time>".
Never say only "we are working on it". Never invent a restoration time. Send the update by the time you promised, even if nothing changed.
If the customer mentions a downed line, a hazard, or medical equipment, give the emergency or priority route and offer a person.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The customer asks "when is it back?": give cause, area, estimate or "not yet available", then next update time first, before any apology. |
| Admit uncertainty and show how to check | No restoration estimate exists: say so, say who will set it, and give the time of the next update. |
| Offer choices: 2-4 options plus "Something else", free text open | After the update: "Text me the update", "Report a downed line", "Talk to a person", "Something else". Skip them when the customer only asked for the status. |
| Hand off to a person | The customer reports a hazard or medical need, the estimate has slipped twice, or the customer asks for a person. |

**Don't over-correct.** Do not promise a restoration time the crew has not given. Do not send an update every few minutes with nothing new; pick a cadence that fits the outage and say so (see the cadence sources in section 4). Do not blame the weather or a vendor to dodge ownership.

**Hand-off rule.** Offer a person when the customer reports a safety hazard or medical equipment, when the restoration estimate has moved twice, or when the customer asks. Pass the address, outage ID, and what the bot has already said ([cold transfer](../../human-handoff/failures/cold-transfer.md)). Outside staffed hours, give the emergency route and the next update time ([handoff outside staffed hours](../../human-handoff/failures/handoff-outside-staffed-hours-with-no-alternative.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
Results: **Not yet run.** No test file is written for this pattern.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Cause is known | The update names the cause (rule 1) |
| 2 | Customer in the affected ZIP | The update names the area (rule 2) |
| 3 | No restoration estimate | Says "not yet available" and gives a clock time for the next update (rules 3, 5) |
| 4 | Nothing changed at the promised time | An update still goes out by that time (rule 6) |
| 5 | Estimate moves from 7 p.m. to 10 p.m. | Says it changed, shows the new time (rule 7) |
| 6 | Customer says a power line is down | Gives the emergency route and offers a person (rule 8) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Updates with an estimated next update time** (primary) | 100% | Share of outage updates sent that contain a next-update clock time (log field `next_update_at`) | Below 95% |
| Updates sent by the promised time | Over 95% (tune) | `sent_at` less than or equal to the earlier `next_update_at` | Below 90% |
| Updates with cause and area | Over 90% (tune) | Updates with `cause` and `area` fields filled, excluding "unknown" cause by design | Below 80% |
| Repeat "any update?" asks | Falling | Same intent twice within 60 minutes in one outage | Rising two weeks in a row |
| Invented or stale estimates (counter-metric) | 0 | Estimates shown with no matching outage-system value | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Written for text; voice signals are PLANNED.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Outage reply contains no clock time | Reply text and `next_update_at` empty | A resolution message after service returned |
| Reply is the fixed "working on it" template | Template name on the outage reply | A short acknowledgment followed by the full update in the same turn |
| Customer asks "any update" or "when" again within an hour | Same intent in a later turn of the same outage | The customer wanted a different channel |
| No outbound update by the promised time | Outbound events versus `next_update_at` | The outage was resolved and a close-out was sent |

**Starter rule:** every outage update gives a next-update clock time, and an update goes out by it.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: outage-updates-generic-or-late
runs: pre_send
reads: [outage.cause, outage.area, outage.crew_status, outage.estimate, outage.next_update_at]
trigger: an outage status reply is about to be sent
moves: [lead_with_answer, admit_uncertainty, offer_choices, hand_off]
choices: ["Text me the update", "Report a downed line", "Talk to a person", "Something else"]
on_miss: rewrite
metric: updates with an estimated next update time
counter_metric: invented or stale estimates
status: proposed
```

## 8. Related patterns
- [Silent long-running work](../../response-time/failures/silent-long-running-work.md): a wait of seconds with no status; this page is an outage lasting hours, where the missing part is cause, area, and update time.
- [No proactive updates](../../conversation-frameworks/failures/no-proactive-updates.md): the general case of telling users before they ask; this page adds the outage content and the clock-time promise.
- [Generic error messages](../../errors-and-recovery/failures/generic-error-messages.md): the bot's own failure; here the failure is outside the bot and the customer needs facts about it.
- [Handoff outside staffed hours](../../human-handoff/failures/handoff-outside-staffed-hours-with-no-alternative.md): what to offer when no person is available.
- [Cold transfer](../../human-handoff/failures/cold-transfer.md): what to pass to the person.

## 9. Common questions
### What should a utility chatbot say during an outage?
Cause if known, the affected area, crew status, a restoration time if one exists (or "not yet available"), and the time of the next update. See section 5.

### What if we have no restoration estimate yet?
Say so, say what is being checked, and still give a next-update time. One source says the checkpoint promise should continue even when the estimate is withdrawn ([OneUptime post](https://oneuptime.com/blog/post/2026-09-29-status-updates-without-recovery-eta/view)).

### How often should the bot update customers during an outage?
I found no utility rule I could open. Atlassian's guidance suggests every 30 minutes or "whatever cadence is appropriate"; one vendor page reports customer preferences varying from hourly to only when information changes. Pick a cadence, state it, and keep it.

### Is "next update by 7:30" the same as "power back at 7:30"?
No. Label them separately, or customers will read the update time as a restoration promise.

---
## Technical section

### T1. Solution architecture
```
outage system (cause, area, crew, estimate, made_at) -> update composer (template + customer address match)
   -> scheduler (next_update_at; backup publisher) -> send + log (sent_at, next_update_at, fields present)
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No outage reply without `next_update_at` | Pre-send check | Log scan; test 3 |
| Estimates only from the outage system, with `made_at` | Composer | Test 5 |
| Scheduled send fires by `next_update_at`, even with no change | Scheduler | Test 4 |

### T3. Evals
- **Dataset:** 50 simulated outages (storm, fault, planned work) with known, partial, and missing cause, area, and estimate.
- **Judge rubric:** does the reply carry each field, label the estimate and the next-update time separately, and invent nothing?
- **Metrics and starting thresholds:** next-update time 100%; invented estimates 0. Starting points to tune.
- **Release gate:** block a deploy if any outage template can render without a next-update time.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Updates past `next_update_at` | Any | Over 10% of active outages | Assign a publisher; send the last verified facts with a new time |

### T5. Trade-offs
- A committed update time creates work for crews and communications staff; a missed one is worse than a longer interval.
- Customer counts and cause codes may need review before they are shown to the public.

---
### Deep dive
- **Open question.** I found no study that tests chatbot outage wording. The evidence is incident-communication guidance, one vendor blog post, and a vendor-hosted survey description.
- **Blocked sources.** Several utility and regulator pages returned 403, 404, or connection errors; a person should read the J.D. Power and FCC pages directly before the page cites any rule.
- **Voice (PLANNED).** An outage hotline would need the same fields, spoken short, with the next-update time repeated at the end. Not written or measured.
- **References.** [Atlassian, *Incident communication tips*](https://support.atlassian.com/statuspage/docs/incident-communication-tips) (opened); [OneUptime, Sept. 2026](https://oneuptime.com/blog/post/2026-09-29-status-updates-without-recovery-eta/view) (opened); [KUBRA podcast page, 2025](https://www.kubra.com/blog/navigating-outages-driving-sustainability-utilities-roadmap-podcast) (opened).
