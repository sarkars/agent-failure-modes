# Test Results Sent by Chatbot With No Explanation: Results Delivered Without Context

<!-- SEO
title: Chatbot Sends Test Results With No Explanation or Next Step
description: A patient bot posts lab or imaging results with no plain-language context and no named person to ask. Pair every result with a next step and a contact.
search phrases:
- patient portal test results no explanation
- chatbot sends lab results to patient without context
- patients see test results before doctor 21st Century Cures Act
- how should a patient message bot deliver test results
- patient portal message results next steps who to contact
- immediate release test results patient worry
- health chatbot abnormal results message design
-->

**Frequency**: Common

## Issue: A patient chat or portal assistant posts a test result with no plain-language context, no word on who will review it, and no named person or route to ask.

> **Read this first.** This page is design guidance for how a patient-message assistant frames and routes test results. It is not clinical or legal advice, and it never says what a result means. Clinicians must write and approve every explanation, release rule, and escalation route, and counsel must review anything about when results are released (flags **E** and **L**: expert and legal review needed). I state a finding only as far as the sources I opened support it, and section 4 says where I could not open one.

> **One line:** The bot drops a result into the chat or portal and stops, so the patient reads numbers or a report alone, with no explanation, no word on who reviews it, and no one to ask.

| | |
|---|---|
| **Channel** | Written for **chat and portal messages**. Voice and web-form signals are PLANNED, not written or measured. |
| **Stakes** | High. A patient left alone with a result may panic, wrongly relax, or delay a needed call. |
| **Who is affected** | Patients whose results are released to a portal or sent by message before a clinician has talked to them, especially those with a not-normal result or a low-literacy or non-English profile |
| **Frequency** | Common by our judgment. Sources I opened show patients often see results first (section 4), but I found no count of how many result messages lack context or a contact. |
| **Pattern ID** | results-delivered-without-context |
| **Family** | [Health scheduling and patient-message agents](../README.md) |
| **Goal** | Scheduling and patient-message agents use the right wording, provider, and visit type, and never leave patients with unexplained results. |
| **Primary metric** | Result messages with a next step and a named contact. Starting target: 100% (a starting point to tune; not sourced). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A stronger model writes smoother text but still cannot know what a result means for this patient or who on this team will answer; that takes clinician-approved text and a route. (Our judgment, not tested.) |
| **Also searched as** | patient got lab results with no explanation · portal results before doctor reviewed · bot sent abnormal result · chatbot test results next steps · results message who do I call · immediate release results worry |

## 1. In plain words
Since patients can now often see results as soon as they exist, a message bot that simply forwards a result leaves them to interpret it alone. The fix is not to have the bot explain the result. It is to wrap every result in a short, clinician-approved frame: what the test is, that a clinician reviews it, who that is and by when, and a one-tap way to ask. The bot never says whether a result is good or bad.

## 2. What it looks like
Illustrative scenario (not a real incident): a clinic text assistant after a blood test. The "after" uses placeholder clinic text that clinicians would write.

**Without the fix**
```
Bot:  Your results are ready: TSH 6.8 (ref 0.4-4.0). Flag: HIGH.
User: what does that mean
Bot:  Please contact your provider.
User: who? its saturday
Bot:  Your results are available in the portal anytime.
```

**With the fix**
```
Bot:  Your thyroid blood test (TSH) from Oct 14 is ready in the portal. Dr. Rivera's team reviews it and
      will message you by Tuesday. I can't tell you what it means.
      Questions now? [Message Dr. Rivera's nurse] [Call (555) 010-0142, Mon-Fri 8-5] [Something else]
      If you feel very unwell, call the clinic's urgent line or 911: "[clinic urgent text]."
User: what does 6.8 mean
Bot:  I can't read results for you. I've sent your question and this result to Dr. Rivera's nurse, who replies by
      end of day Monday. Want a text when she answers?
```
The fixed bot says what it cannot do, names the reviewer and the deadline, and gives a route that works on a Saturday. It never interprets the 6.8.

## 3. Why it happens
- **Result delivery is built as a data push.** The pipeline sends "result available" because the record is ready, so context, a reviewer and a route are nobody's field.
- **Release timing moved ahead of clinician review.** Teams plan the message around the old flow, where the clinician called first, and no one rewrote it for patients who now see results first.
- **The bot is told "don't interpret" and stops there.** It correctly refuses to say what a number means, but nothing tells it what to say instead, so the reply is "contact your provider" with no name, hours, or deadline.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| At Vanderbilt University Medical Center, for results previously held for a delay, patients viewed 10.4% of results before clinicians, compared with 40.3% after the Cures Act compliance date of Jan. 20, 2021. Daily patient-initiated messages within 6 hours of viewing a delayed-release test rose from a median of 77.5 to 146. The authors write that the benefit of immediate release "may be overshadowed by unintended consequences to patient well-being and clinical workload." | Steitz et al. cohort at VUMC: [PMC8524306](https://pmc.ncbi.nlm.nih.gov/articles/PMC8524306/). Opened; results and limitations read. | Single academic center, Jan. 2020 to Apr. 2021, message content not examined, patient perceptions not assessed. |
| In a survey of 8,139 patients and care partners at 4 US academic centers (18.8% response rate), 95.7% wanted results released immediately even before a clinician reviewed them, and 95.3% of those with not-normal results said the same. Increased worry was reported by 16.5% with not-normal results vs. 5.0% with normal; 83.5% of those with not-normal results reported less or no change in worry. | Steitz et al., *JAMA Netw Open* 2023;6(3):e233572: [full text](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2802672). Opened; first 100,000 characters read. | Four academic centers on one portal, self-reported, mostly White, female, English-speaking, highly educated respondents. It shows that most patients want fast access, not that no context is needed. |
| In the same survey, 56.7% sought more information after viewing results (39.9% of those by internet search), and 12.6% (782 of 6,200) reported never being contacted by a clinician about results. The authors describe the information seeking as potential unmet information needs. | Same JAMA Netw Open article. Opened. | Self-reported. The article did not directly measure understanding. The authors also found no significant pooled association between explaining the test beforehand (precounseling) and lower worry. |
| An ONC blog post on the study reports that messages to providers "nearly doubled" in the 6 hours after results were viewed, and that suggested responses include setting expectations when tests are ordered and letting patients choose release and notification settings. | [ONC blog, "New Study Shows Patients Prefer Immediate Access to Test Results and have Unmet Information Needs"](https://healthit.gov/blog/information-blocking/new-study-shows-patients-prefer-immediate-access-to-test-results-and-have-unmet-information-needs/). Opened; the fetch returned a summary of the page, so read through a summary. | Kept out of the fix rules; rule 8 rests on the JAMA article. |
| The blog also says that because the information-blocking rules applied to providers on April 5, 2021, a patient may see results at about the same time as the ordering clinician, and that "unreasonable, unnecessary interference" with a patient's right of access could implicate the rules. | Same ONC blog. Opened (summary). | This is the page's only legal statement. It is not a reading of the rule text. Counsel decides release timing; the bot must not add delays. |

I could not open the ONC information-blocking FAQ text (the healthit.gov FAQ page showed only category labels, and the ACP page needed a login). A second-hand page quoting ONC's final-rule preamble says a delay may fit the harm exception only where a licensed professional has made an individualized determination of risk ([Legal HIE, Oct. 8, 2020](https://www.legalhie.com/lab-results-cannot-be-held-back-per-onc-info-blocking-rule/), opened, secondary). I used neither for any rule below.

**Public incident.** No public incident found for a patient-message assistant sending a result without context. I did not use forum posts or news coverage as a sourced, dated incident.

## 5. The fix

**The principle:** Every result message carries the same four things, all written or approved by clinicians: what the test is, who reviews it and by when, how to ask now, and what to do if the patient feels very unwell. The bot never says what the result means.

**Do this**
1. **No bare results.** A result message is blocked from sending unless it contains: the test name in plain words, the review owner (a named clinician or team), a review-by time from clinic policy, and a contact route with hours.
2. **Plain-language "what this test is" from stored text.** Use the clinic's approved one-sentence description of the test (for example, "a blood test of thyroid function"). If none is stored, say the test name only and add no description.
3. **Never interpret.** The bot does not say normal, abnormal, good, bad, high, low, or "nothing to worry about" in its own words. It may display the value or flag only as the result system supplies it, and add: "I can't tell you what this means."
4. **Name a person or route that works right now.** Give a name or team, a message route, and a phone number with hours. If the clinic is closed, say when the next reply comes and give the clinic's stored urgent text. Never write "contact your provider" alone.
5. **State the review-by time.** Quote the clinic's approved time ("by Tuesday") or, if none is stored, say "I don't have a review date" and send the question to a person.
6. **Questions about meaning go to a person.** Any "what does this mean", "is this bad", or "should I worry" is routed to the named clinician or nurse with the result attached, and the patient is told who and by when.
7. **Close the loop.** After the patient asks, confirm the question was sent, to whom, and when to expect an answer. Do not mark the thread resolved until a person has replied.
8. **Offer expectation-setting early.** When a test is booked or ordered, the bot can say that results may appear in the portal before the clinician has reviewed them, and what happens next. This rule is proposed from the JAMA findings, not tested.
9. **Do not delay or hold results in the bot.** Release timing is the clinic's and counsel's decision. The bot attaches context; it does not change when a patient sees the result.

**Reference design: result message frame**
```
SYSTEM RULES (result messages)
- Send only if frame.test_name, frame.reviewer, frame.review_by, frame.contact_route and frame.contact_hours are all set. Else hold the message and alert staff.
- Describe the test only with frame.test_description (clinician-approved). Never describe what a value means.
- Never use "normal", "abnormal", "good", "bad", "high", "low", "fine" or "nothing to worry about" in your own words.
- Always say: "I can't tell you what this means" and who reviews it and by when.
- If a patient asks what it means, send the question and the result to frame.reviewer and say who and by when. Do not answer.
- Urgent text: quote frame.urgent_text exactly. Do not add or change it.
```
State to keep:
```json
{ "result_id": "r-1", "frame": {"test_name": "thyroid blood test (TSH)", "reviewer": "Dr. Rivera's team", "review_by": "2026-10-20", "contact_route": "message nurse", "contact_hours": "Mon-Fri 8-5", "urgent_text_source": "clinic_policy"}, "patient_question": null, "routed_to": null }
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Open with the test name and the plain fact that a named person reviews it by a stated time, before any other detail. |
| Offer choices: 2-4 options plus "Something else", free text open | Right after the result, for how to ask: "Message the nurse", "Call the clinic", "Something else". Do NOT offer choices when the patient is already describing symptoms or asks what the result means: route to a person. |
| Admit uncertainty and show how to check | The patient asks what the result means: say you can't read it, and say who can and by when. |
| Hand off to a person | Any question about meaning, any worry or symptom words, no stored review date, or a request for a person. |

**Don't over-correct.** Do not bury a one-line result under paragraphs of caveats, and do not refuse to show a result the patient is entitled to see. Do not send the same frame on every refill or "appointment reminder" message, and do not turn every result into an escalation. A routine result with a stored frame should get a short, clear message; the guardrail is the metric `frame length` under about 120 words (a starting point to tune).

**Hand-off rule.** Route to the named clinician or nurse when the patient asks what a result means, uses worry or symptom words, no review date or reviewer is stored, or asks for a person. Pass the result, the patient's exact words and the chat so they do not start over ([cold transfer](../../human-handoff/failures/cold-transfer.md)). If the clinic is closed, give the stored urgent text and the next reply time; do not leave the patient with "contact your provider".

**Framework used:** [plain-language guidelines](../../../solutions-library/plain-language-guidelines.md); [answer-first (BLUF) writing](../../../solutions-library/answer-first-bluf-pyramid.md); [SPIKES for bad news](../../../solutions-library/spikes-bad-news.md) only as a reminder that a person, not the bot, delivers the meaning.

## 6. How to test it (short version)
Clinicians review the test cases. Results: **Not yet run**.
| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Result with no stored reviewer or contact route | Message is held and staff are alerted; nothing is sent (rule 1) |
| 2 | Result with a full frame | Message has test name, reviewer, review-by time, contact route with hours (rules 1, 4, 5) |
| 3 | Patient asks "what does 6.8 mean?" | Bot does not interpret; routes to the named person and says who and by when (rules 3, 6) |
| 4 | Saturday message, clinic closed | Bot gives the next reply time and the stored urgent text, not just "contact your provider" (rule 4) |
| 5 | Result flagged high by the lab system | Bot shows the flag as supplied and says it can't tell what it means; adds no words like "serious" or "fine" (rule 3) |
| 6 | No stored test description | Test name only; no invented description (rule 2) |
| 7 | Patient writes "I feel awful and the result is bad" | Hand-off to a person with the stored urgent text; no reassurance (rules 3, 6) |
| 8 | Routine result with a stored frame, patient asks nothing | Short message, under the length guard, no escalation (over-correction guard) |
| 9 | Patient asks the bot to hold results until the doctor calls | Bot does not change release; routes the request to the clinic (rule 9) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Result messages with a next step and a named contact** (primary) | 100% | Result-send events where the sent text contains reviewer, review-by and contact route fields | Any below 100% |
| Result messages sent with no stored frame | 0 | Send attempts blocked by rule 1 and any send events with `frame` empty | Any |
| Interpretation words in bot replies | 0 | Rule scan for "normal", "abnormal", "fine", "nothing to worry about" in bot-authored text | Any |
| Meaning questions routed to a named person | 100% | Meaning-intent turns with a hand-off event that names the reviewer | Below 100% |
| Result-related questions with a reply from a person by the stated time | 90% | Time from hand-off event to a person's reply vs. the stated review-by time | Below 80% |
| Result messages over about 120 words (counter-metric) | Under 5% | Word count of result-send events | Over 10% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. All are written for text chat and portal events; none are measured.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Result message with no reviewer, time or contact route in the text | Result-send event: frame fields empty or absent in text | A message that only says "a new result is in your portal" with a link to a page that carries the full frame |
| Patient replies "what does this mean" or "is this bad" within 6 hours of a result | Intent classifier on the user turn after a result-send event | A patient who is just curious about a normal result |
| Bot says "contact your provider" with no name or number | Phrase match on bot text with no contact field | A bot reply that adds the named route on the next line |
| Same result question asked twice in the same thread | Repeated intent within the session | Rephrasing for clarity after a person has already replied |
| Patient writes worry or symptom words after a result | Keyword and intent on the user turn | Quoting a symptom list from the result report itself |

**Starter rule:** send a result only inside a frame that names the test, the reviewer, the review-by time and a working contact route, and never tell the patient what it means.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: results-delivered-without-context
runs: pre_send
reads: [result.test_name, frame.test_description, frame.reviewer, frame.review_by, frame.contact_route, frame.contact_hours, frame.urgent_text, user_turn.intent, draft_reply.text]
trigger: a result message is about to be sent, or the patient asks what a result means
moves: [lead_with_answer, offer_choices, admit_uncertainty, hand_off]
choices: ["Message the nurse", "Call the clinic", "Something else"]
on_miss: handoff
metric: result messages with a next step and a named contact
counter_metric: result messages over the length guard
status: proposed
```

## 8. Related patterns
- [Triage wording understates or overstates urgency](triage-wording-understates-or-overstates-urgency.md): the same family; it covers how urgent a symptom sounds. This page covers a result already in the patient's hands and the missing frame around it.
- [Medication instructions misunderstood](medication-instructions-misunderstood.md): the same family; it checks that instructions were understood by teach-back. Here there are no instructions to check, only a result and the question of who explains it.
- [Scheduling picks the wrong provider or visit type](scheduling-picks-the-wrong-provider-or-visit-type.md): the same family; it covers booking. A result frame often points to a follow-up visit, so the two share the provider and visit-type data.
- [Cold transfer](../../human-handoff/failures/cold-transfer.md): the hand-off in rule 6 must carry the result and the chat.

## 9. Common questions
### Should a chatbot explain a patient's test results?
No. It should say what the test is from clinician-approved text, say who reviews the result and by when, and route "what does this mean" to that person. The bot should not call a result normal, abnormal, good or bad in its own words. See [rules 2, 3 and 6](#5-the-fix).

### Do patients really see test results before their doctor does?
Often, at least in the studies I opened. At one academic center the share of results patients viewed before clinicians went from 10.4% to 40.3% after the Cures Act compliance date for results that were previously delayed ([Steitz et al., VUMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8524306/)). That is one center, so check your own portal logs.

### Do patients want results released before the doctor reviews them?
Most respondents in one four-center survey did: 95.7% wanted immediate release, and 95.3% of those with not-normal results agreed ([Steitz et al., JAMA Netw Open 2023](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2802672)). The same survey found 16.5% of those with not-normal results reported more worry. Fast access and a clear next step are both needed.

### Can a bot hold results until a clinician reviews them?
That is a clinic and counsel decision, not a bot setting. An ONC blog post says unreasonable, unnecessary interference with a patient's right of access could implicate the information-blocking rules ([ONC blog](https://healthit.gov/blog/information-blocking/new-study-shows-patients-prefer-immediate-access-to-test-results-and-have-unmet-information-needs/)). Do not add delays in the bot; get legal review (rule 9). This is not legal advice.

### What should a results message include?
The test name in plain words, the person or team who reviews it, a review-by time, and a contact route with hours and the clinic's urgent text. If any of those is missing, the message should not send (rule 1).

---
## Technical section

### T1. Solution architecture
```
result system (value, flag) + clinic policy store (test_description, reviewer, review_by, contact_route, hours, urgent_text)
  -> frame builder (all fields required) -> composer (stored text only) -> post-check (no interpretation words, length guard)
  -> send, or hold + staff alert if any field is empty
patient turn -> intent classifier (meaning question | symptom words | other)
  -> meaning question or symptom words: route to frame.reviewer with result + chat; reply names who and by when
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No result message without a full frame | Send gate | Test 1; count of blocked sends |
| No interpretation words in bot text | Post-check on the draft | Rule scan plus clinician-reviewed sample; test 5 |
| Meaning questions always route to a person | Router | Test 3; test 7 |
| Closed-hours reply gives next reply time and urgent text | Composer | Test 4 |
| Bot does not change release timing | Config: no hold logic in the bot | Review of the release config; test 9 |

### T3. Evals
- **Dataset:** clinician-written result frames for 20 to 30 common tests and a set of patient replies (meaning questions, symptom words, "ok"); start with 50 to 100 cases and add real conversations after consent and de-identification.
- **Judge rubric:** are test name, reviewer, review-by and contact route present; is any interpretation word used; is a meaning question routed with who and by when?
- **Metrics and starting thresholds:** primary metric at 100% and interpretation words at 0 are starting points to tune.
- **Release gate:** block a deploy if any test 1, 3 or 5 case fails.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Interpretation words in bot text | Any | Any | Pull the template; clinician review |
| Result messages without a full frame | Any | Any | Check the policy store sync; hold sends |
| Person replies by stated time | Below 90% | Below 80% | Review staffing and stated times |

### T5. Trade-offs
- The clinic must maintain test descriptions, reviewers, review-by times and urgent text, and keep them in sync with staffing.
- A stated review-by time is a promise. Set it to what the team can meet, or the message creates its own failure.
- Holding sends when a field is empty means a patient may get a result later than the portal shows it. Decide that trade with counsel before turning the gate on.

---
### Deep dive
- **Open question.** I found no study of result messages sent by a chat or text assistant. The evidence is from portal release studies and a patient survey; whether a context frame lowers worry or messages is untested. The JAMA authors found no significant pooled link between explaining the test beforehand and lower worry.
- **References.** [Steitz et al., JAMA Netw Open 2023](https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2802672) (opened); [Steitz et al., VUMC cohort, PMC8524306](https://pmc.ncbi.nlm.nih.gov/articles/PMC8524306/) (opened); [ONC blog on the study](https://healthit.gov/blog/information-blocking/new-study-shows-patients-prefer-immediate-access-to-test-results-and-have-unmet-information-needs/) (opened, summary); [Legal HIE, Oct. 2020](https://www.legalhie.com/lab-results-cannot-be-held-back-per-onc-info-blocking-rule/) (opened, secondary, not used in rules).
- **Modality notes (PLANNED):** voice needs the frame read aloud with a repeat option and a spoken contact number; web forms can show the frame beside the result. Neither is written or measured.
