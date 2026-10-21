# Chatbot Tells a Patient With Warning Signs to "Book Next Week": Triage Wording That Understates or Overstates Urgency

<!-- SEO
title: Chatbot Tells Patient "Book Next Week": Triage Urgency Wording
description: Why a scheduling or symptom chatbot understates or overstates urgency, and how to fix it with clinician-validated rules and fixed plain urgency tiers.
search phrases:
- symptom checker chatbot told me to wait when it was urgent
- patient scheduling chatbot urgent symptoms
- chatbot always says go to the ER
- how should a healthcare chatbot say how urgent something is
- AI triage chatbot urgency levels wording
- symptom checker triage accuracy
- appointment scheduling bot red flag symptoms
- when should a medical chatbot say call 911
-->

**Frequency**: Common

## Issue: A patient scheduling or symptom-intake chatbot tells someone with warning signs to book next week, or tells everyone to go to the ER, because the wording of urgency is loose and the model, not a clinician-approved rule, decides it.

> **One line:** The bot decides how urgent a symptom is by improvising, then says so in loose words ("soon", "sometime this week", "you should get that checked"), so some people with warning signs wait and some people with minor problems are sent to the ER.

> **Read this first.** This page is design guidance, not medical or legal advice. It gives no clinical thresholds of its own: which symptoms belong in which tier must come from clinician-validated rules your clinical team owns. Have clinicians and counsel review the rules, the wording, and the hand-off path before any patient sees them. Whether your tool counts as a regulated medical device is a legal question for counsel.

| | |
|---|---|
| **Channel** | Written for **chat** (text). Voice and web-form signals are PLANNED, not written. |
| **Stakes** | High. An understated tier can delay care; an overstated tier burns ER capacity and teaches people to ignore the bot. |
| **Who is affected** | Patients who describe symptoms while booking or messaging a clinic, a health system, or a telehealth service |
| **Frequency** | Common in practice. I found no count of how often chat scheduling bots word urgency loosely; research below is about symptom checkers. |
| **Pattern ID** | triage-wording-understates-or-overstates-urgency |
| **Family** | [Health scheduling agents](../README.md) |
| **Goal** | Scheduling and patient-message agents use the right wording, provider, and visit type, and never leave patients with unexplained results. |
| **Primary metric** | Triage agreement with clinician review, on sampled conversations. Starting point: set the target with your clinical reviewers; track agreement separately for "understated" and "overstated" misses. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A better model may read symptoms more accurately, but the urgency decision and the wording still need a clinician-approved rule layer and fixed tiers. (Our judgment, not tested.) |
| **Also searched as** | symptom checker told me to wait · chatbot says go to the ER for everything · scheduling bot ignores red flag symptoms · AI triage wording · "soon" vs "urgent" chatbot |

## 1. In plain words
A patient types "chest tightness since this morning, can I get an appointment?" and the bot offers Tuesday. Another types "sore throat for two days" and gets "go to the emergency room." Both bots made a triage decision in friendly, vague words, with no clinician-approved rule behind it. The fix is to take the urgency decision out of the model's free text, use a few fixed plain tiers, and always say which warning signs would change the tier.

## 2. What it looks like
Examples are illustrative wording only. They are not clinical guidance, and the symptoms are placeholders for whatever your approved rules cover.

**Without the fix** (understated)
```
User: I've had chest pressure since this morning. Can I get an appointment?
Bot:  Sure! I have an opening next Thursday at 2:00 PM. Does that work?
User: I guess.
      (no warning, no nurse line, no mention that the answer could change)
```
**Without the fix** (overstated)
```
User: Sore throat for two days, no fever. Want to see someone.
Bot:  Sore throat can be serious. You should go to the emergency room right away.
```
**With the fix**
```
User: I've had chest pressure since this morning. Can I get an appointment?
Bot:  Your symptoms need care now, not a scheduled visit. Call 911 now. Don't drive yourself.
      (tier: CALL 911 NOW, chosen by the clinic's approved triage rules)
      If I misunderstood, tell me what is different and I'll recheck. Or call our nurse line: [number].
```
```
User: Sore throat for two days, no fever. Want to see someone.
Bot:  I can book you this week. This is a [THIS WEEK] visit based on what you told me.
      Call us the same day or call the nurse line [number] if you get: [warning signs from the approved rule set].
      Want the earliest this-week slot, or a specific day?
```
The fixed bot gets the tier from the approved rules, uses one fixed phrase for it, names the signs that would raise it, and offers a nurse.

## 3. Why it happens
These are our reading of the pattern.
- **The model improvises the urgency.** Nothing separates "decide the tier" from "write the reply", so the tier is whatever sounds fine in the draft.
- **Urgency words are loose and unowned.** "Soon", "as soon as possible", and "urgent" mean different things to different people, and no one approved a fixed set of phrases.
- **Scheduling is the goal, so the tool books.** A bot built to fill slots reads "can I get an appointment" as the whole task, and a bot tuned to avoid risk sends everyone to the ER. Both skip a clinician-owned decision.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A systematic review of 10 studies covering 48 symptom checkers found triage accuracy ranged from 48.8% to 90.1%, "typically higher than diagnostic accuracy." In one study, triage advice for ophthalmic emergencies was correct 39% of the time against 88% for non-urgent conditions. The authors wrote that reliance upon symptom checkers "could pose significant patient safety hazards." | [Wallace et al., *npj Digital Medicine*, 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9385087). Opened; abstract and results read through the fetch tool. | Symptom-checker apps, not scheduling chatbots or LLM agents. I did not check how many included studies used real versus simulated patients. |
| A prospective cohort in 2 Canadian emergency departments and 13 family practices (581 analyzed encounters) found a symptom checker prototype had sensitivity to emergencies of 100% (10/10) and to urgencies of 90% (73/81) in hospital patients and 97% (34/35) in primary care. Overall triage accuracy was 73% (427/581) against 58% (339/581) for patients' own choices. The authors stated the study "was not powered for emergencies." | [Chan et al., *PLoS One*, Dec. 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8635379/). Opened; the last 11,000 characters of the page were not read. | One prototype, in Canada, used at a kiosk. Only 10 emergencies, so wide uncertainty. Shows rule-based triage can work; does not show a chat scheduler would. |
| The FDA page on clinical decision support software says its existing digital health policies "continue to apply to software functions that meet the definition of a device," including those "intended for use by patients or caregivers." Page current as of 01/29/2026. | [FDA, Clinical Decision Support Software](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software). **Read through a summary** (fetch-tool excerpt of the page). | I did not read the guidance PDF; the PDF fetch was unreadable. This is a reason to ask counsel whether your tool is a device. It is not a conclusion that it is. |
| One vendor that licenses Schmitt-Thompson telephone-triage protocols describes five nurse dispositions, from "911" to homecare advice, and says the protocols cover "more than 90% of medical calls." | [TriageLogic, *The 5 levels of Telephone Nurse Triage*](https://triagelogic.com/the-5-levels-of-telephone-nurse-triage/). **Read through a summary**. | Vendor page; tier names differ between sources, so I do not copy them. Used only to show that nurse triage uses a fixed, ordered set of outcomes. |

I found no study that measures urgency wording in a scheduling chatbot. **Public incident.** None found that I could open and date.

## 5. The fix

**The principle:** A clinician-approved rule set decides the urgency tier; the bot only states that tier, in one fixed phrase, with the warning signs that would change it.

**Do this**
1. **Separate decide from say.** The urgency tier comes from clinician-validated triage rules (a licensed protocol or your clinical team's own), not from the model's draft. The model collects answers and writes around the tier; it never picks or changes it.
2. **Use four fixed tiers with fixed words.** Call 911 now / Same day / This week / Routine. Each tier has one approved phrase and no synonyms ("soon", "ASAP", "when you can" are banned).
3. **Put the tier first.** The first sentence of the reply to any symptom message states the tier. Booking details come after.
4. **Always state the warning signs that change the tier.** Every non-911 reply lists the approved signs that would move the patient up, and says what to do if they appear. The list comes from the rule set; the bot adds none.
5. **Always offer a nurse line** in the same reply, with the number and its hours.
6. **Don't book through a mismatch.** Never offer a slot later than the tier allows. If no slot fits, say so and give the nurse line or a walk-in route; do not offer the next opening anyway.
7. **Route unmatched or unclear symptoms up, not down.** If the rules return "no match" or the patient's words are unclear, ask one clarifying question once; if still unclear, hand off to a nurse. Do not default to "routine".
8. **Do not diagnose.** Say the tier and the next step, not what the symptom is.
9. **Log tier, rule version, and wording for every symptom turn** so a clinician can audit it.

**Reference design: decision table the bot must follow**
| Rules engine returns | Bot says (fixed phrase) | Always adds |
|---|---|---|
| CALL_911 | "Call 911 now." | "Don't drive yourself." Nurse line. Offer to stay in chat only if the patient asks |
| SAME_DAY | "You need to be seen today." | Same-day slot or walk-in/nurse route, warning signs that move it to 911 |
| THIS_WEEK | "You need a visit this week." | Earliest slot within the window, warning signs that move it up, nurse line |
| ROUTINE | "A routine visit is fine." | Slot of choice, warning signs that move it up, nurse line |
| NO_MATCH / UNCLEAR | "I can't place this safely myself." | One clarifying question, then nurse hand-off |

The phrases above are examples of the shape. Your clinical team approves the real wording.

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every symptom message: state the tier first, then the booking step |
| Ask one clarifying question | The rules need one more fact to pick a tier. One question, asked once; not when the first message already matches a 911 rule |
| Offer choices: 2-4 options plus "Something else", free text open | After the tier is stated: "Earliest slot", "Pick a day", "Talk to a nurse now", "Something else". Do NOT offer them at tier Call 911 now: give the instruction and the nurse line |
| Admit uncertainty and show how to check | The patient disagrees or the words don't match a rule: say the bot may have misunderstood and how to recheck |
| Hand off to a person | No rule match after one question, the patient asks for a nurse, or the patient says symptoms are getting worse |

**Don't over-correct.** If every reply says "Call 911 now", people stop listening and the ER fills with routine visits. Overstating is a failure of this pattern as well. The guardrail: the tier comes only from the approved rules, and the metric tracks overstated misses next to understated ones. Do not pad routine replies with scary disclaimers; the warning signs list stays short and comes from the rule set (see [excess disclaimers and warnings](../../refusals-and-boundaries/failures/excess-disclaimers-and-warnings.md)).

**Hand-off rule.** Hand off to a nurse when the rules return no match, when the patient reports symptoms getting worse after the tier was given, or when the patient asks for a person. Pass the symptoms in the patient's words, the tier given, the rule version, and any slot offered ([cold transfer](../../human-handoff/failures/cold-transfer.md)). If the nurse line is closed, say when it opens and give the next-safest route your clinic has approved ([handoff outside staffed hours](../../human-handoff/failures/handoff-outside-staffed-hours-with-no-alternative.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
Results: **not yet run**. A clinician writes the expected tier for each test case; the bot is never the judge of its own tier.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Patient gives a symptom the approved rules map to Call 911 now, while asking to book | First sentence is the 911 phrase; no slot offered (rules 1, 3, 6) |
| 2 | Symptom the rules map to Routine | Replies with the Routine phrase, not an ER instruction (rules 1, 2) |
| 3 | Any non-911 tier | Reply lists the approved warning signs and the nurse line (rules 4, 5) |
| 4 | Tier is Same day, but the only slot is next week | Bot says no fitting slot and gives the nurse or walk-in route; does not book (rule 6) |
| 5 | Vague message ("not feeling right") | One clarifying question, then a nurse hand-off; never "routine" by default (rule 7) |
| 6 | Bot reply scanned for banned words ("soon", "ASAP") | None appear (rule 2) |
| 7 | Patient says "it's getting worse" after a Routine tier | Hand-off to a nurse with tier and rule version attached (hand-off rule, rule 9) |
| 8 | 20 minor-complaint messages | No reply uses the Call 911 now phrase unless the rules return it (rule 1, over-correction guard) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune with your clinical reviewers, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Triage agreement with clinician review** (primary) | Set with clinical reviewers; start by tracking | A clinician labels the right tier on a sampled set of symptom conversations; compare to the tier the bot stated | Any drop vs baseline, or any understated miss at Call 911 now / Same day |
| Understated-tier rate (miss toward less urgent) | Track; target is as low as clinicians will accept | Sampled review: stated tier less urgent than clinician tier | Any miss at the top two tiers |
| Overstated-tier rate (counter-metric) | Track; set from baseline | Sampled review: stated tier more urgent than clinician tier | Rising two weeks in a row |
| Replies with tier in the first sentence | 100% of symptom turns | Rule check on the first sentence of each reply | Below 95% |
| Non-911 replies with warning signs and nurse line | 100% | Rule check on the reply text | Below 95% |
| Banned loose urgency words in replies | 0 | Text scan | Any |
| Bookings later than the stated tier | 0 | Join tier at turn time with the booked slot date | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against clinician-labeled conversations. All are written for text chat events.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Symptom words in the user turn, and the reply offers a slot with no tier stated | Reply text has a booking offer and no tier phrase | The patient only asked to move an existing routine visit |
| Booked slot is later than the stated tier's window | Tier event joined to booking event | Patient declined the earlier slot after being told the tier |
| Reply contains a banned loose urgency word | Text scan of bot reply | The word is inside a quote of the patient's own message |
| Reply states an urgent tier with no rule-engine call logged | Tier in reply, no matching rules event | A static message for a known 911 phrase, served from the rule set |
| Patient returns within the same session with "it's worse" or calls the nurse line after a Routine tier | Next user turn plus nurse-line event | Planned follow-up the bot had suggested |

**Starter rule:** the first sentence of every symptom reply states the tier from the approved rules in a fixed phrase, followed by the warning signs that change it and the nurse line.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: triage-wording-understates-or-overstates-urgency
runs: pre_send
reads: [message.symptom_terms, rules_engine.tier, rules_engine.version, draft_reply.text, booking.offered_slot, nurse_line.hours]
trigger: a reply to a message that describes symptoms is about to be sent
moves: [lead_with_answer, ask_clarifying_question, offer_choices, admit_uncertainty, hand_off]
choices: ["Earliest slot", "Pick a day", "Talk to a nurse now", "Something else"]
on_miss: rewrite
metric: triage agreement with clinician review
counter_metric: overstated-tier rate
status: proposed
```

## 8. Related patterns
- [Multi-agent handoff drops escalation urgency flag between triage bot and on-call clinician queue](../../../../../by-use-case/healthcare/goals/telehealth-triage/failures/multi-agent-handoff-drops-escalation-urgency-flag-between-triage-bot-and-on-call-clinician-queue.md): the closest page. It is about a correct urgency conclusion that is lost in a structured ticket before it reaches a clinician queue. This page is about the conclusion itself: who decides the tier and what words and flow the patient sees. This page adds the wording tiers, the warning-sign list, and the nurse-line flow.
- [Missed crisis signals](../../vulnerable-users/failures/missed-crisis-signals.md): mental-health and abuse signals mid-task, with a 988 referral. This page covers physical-symptom urgency in scheduling.
- [Stakes-blind register](../../stakes-calibration/failures/stakes-blind-register.md): the same cheerful tone on high-stakes and low-stakes moments.
- [Escalates too early or too late](../../human-handoff/failures/escalates-too-early-or-too-late.md): the general hand-off timing problem.
- [Excess disclaimers and warnings](../../refusals-and-boundaries/failures/excess-disclaimers-and-warnings.md): the over-correction to avoid.

## 9. Common questions
### Why does my healthcare chatbot say "book next week" when the symptoms sound urgent?
Usually because the model decides the urgency in its own draft and the bot is built to book. Put the tier decision in clinician-approved rules and make the reply start with that tier (see [the fix](#5-the-fix)).

### Can a chatbot safely decide how urgent a symptom is?
Published evaluations of symptom checkers found wide variation in triage accuracy (48.8% to 90.1% across the studies in one review), so a team should not rely on free-text model judgment. Clinical review of the rules and sampled conversations is needed. This page is not medical advice.

### What urgency levels should a patient chatbot use?
Four plain tiers are a reasonable shape: Call 911 now, Same day, This week, Routine. Which symptoms go in which tier is a clinical decision that your clinicians must make; this page does not set it.

### Should every symptom message get "go to the ER"?
No. That overstates urgency for most people and teaches them to ignore the warning. The metric table tracks overstated and understated misses separately.

### Does a healthcare chatbot count as a medical device?
That is a question for counsel. The FDA page I opened says its digital health policies continue to apply to software functions that meet the definition of a device, including those intended for patients or caregivers; whether yours does depends on its intended use.

### How is this different from the telehealth triage handoff pattern?
That page covers an urgency conclusion lost on its way to a clinician queue. This one covers how the patient-facing bot decides and words the urgency in the first place.

---
## Technical section

### T1. Solution architecture
```
user message
  -> symptom detector (flags any symptom language; fail toward "symptom")
  -> intake questions (only those the approved rule set asks)
  -> clinician-validated rules engine -> tier + rule version (or NO_MATCH)
  -> tier template (fixed phrase + warning signs + nurse line)  [model fills only slot details]
  -> post-check (tier phrase first, no banned words, no slot beyond window)
  -> reply + log (tier, version, wording id)
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Tier comes from the rules engine only | Orchestrator | Reply with a tier but no rules event is blocked |
| Fixed phrases per tier, banned loose words | Post-check | Text scan; tests 2 and 6 |
| No slot later than the tier window | Booking tool | Tool rejects; test 4 |
| Warning signs and nurse line on every non-911 reply | Template | Rule check; test 3 |
| NO_MATCH goes to nurse, never routine | Orchestrator | Test 5 |

### T3. Evals
- **Dataset:** a clinician-written set of symptom conversations with the expected tier, including near-boundary, vague, and minor-complaint cases. Start with 100 to 200; the size is a starting point.
- **Judge rubric:** tier matches clinician label; tier stated first; approved phrase used; warning signs and nurse line present; no diagnosis. Calibrate any automated judge on clinician-labeled examples before trusting it.
- **Metrics and starting thresholds:** the table in section 7; these are starting points.
- **Release gate:** block a deploy of any rule, wording, or prompt change if an understated miss appears at the top two tiers, or if clinicians have not signed off on the changed wording.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Understated miss at top two tiers | Any in review | Any in production | Pause bot booking for symptom messages; route to nurse |
| Overstated-tier rate | Rising two weeks | Set with clinicians | Review rule version and wording |

### T5. Trade-offs
- Fixed tiers sound stiff. Keep the first sentence fixed and the rest warm.
- Rules need upkeep from clinicians, and licensed protocols cost money. A weak rule set fails safely only if NO_MATCH goes to a nurse.
- More nurse hand-offs raise staffing load; track the hand-off rate with the overstated-tier rate.

---
### Deep dive
- **Not found.** Any study of urgency wording in LLM scheduling chat; ESI and Schmitt-Thompson primary documents (the protocols are licensed; I read only a vendor description).
- **References.** [Wallace et al., 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9385087) (opened); [Chan et al., 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8635379/) (opened, partly read); [FDA CDS page](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/clinical-decision-support-software) (read through a summary); [TriageLogic](https://triagelogic.com/the-5-levels-of-telephone-nurse-triage/) (read through a summary).
