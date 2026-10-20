# Chatbot Labels the Wrong Emotion or Repeats Your Words: Misused Tactical Empathy

<!-- SEO
title: Chatbot Names the Wrong Emotion: Misused Tactical Empathy
description: Why a chatbot that says "it sounds like you're angry" guesses wrong or parrots your last words, and how to offer a label the user can confirm or correct.
search phrases:
- chatbot says "it sounds like you are frustrated" when I'm not
- chatbot repeats what I just said
- chatbot guesses my emotions wrong
- chatbot emotion labeling system prompt
- chris voss labeling chatbot
- tactical empathy for ai agents
- chatbot parrots user's words
- how to make a chatbot acknowledge feelings without guessing
-->

**Frequency**: Occasional

## Issue: A bot copies a negotiation trick ("It sounds like you're angry"), names an emotion the user never showed or echoes the user's last words back, and the user has to correct a script instead of getting help.

> **One line:** The bot states a feeling as if it were fact, or hands the user's own words back as a "reflection"; the fix is to offer a tentative label the user can confirm or correct, only when there is real evidence for it, and to move on to the answer either way.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice and visual are PLANNED, not written. |
| **Stakes** | Low to medium. A wrong label costs trust and time; on a grief, money, or safety message it costs more. |
| **Who is affected** | Users who get an emotion label from a bot that was prompted to "use tactical empathy", "label emotions", or "mirror the customer" |
| **Frequency** | Occasional. Our judgment: it appears only in bots whose prompts or templates were built on negotiation or sales-training material. I found no study that counts it. |
| **Pattern ID** | misused-tactical-empathy |
| **Family** | [Conversation frameworks](../README.md) (row FW-M08) |
| **Goal** | The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange. |
| **Primary metric** | Label confirmation rate. Start: over 70% of labels confirmed or left uncorrected (a starting point to tune) |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A stronger model reads emotion cues better, but the failure also comes from a prompt that tells the bot to state a label every time. (Our judgment, not tested.) |
| **Also searched as** | chatbot labels my feelings wrong · chatbot repeats my last sentence · "it sounds like you're frustrated" bot · tactical empathy prompt · chatbot mirroring annoying |

> **Read this first.** Tactical empathy and labeling come from human negotiation practice (Chris Voss). I found no study that tests labeling on chatbots, so treat the fix as a design hypothesis to test on your own traffic. The sources I opened describe the human technique only at a general level and say nothing about labels that turn out wrong. The mechanics of correction here are our design, not Voss's.

## 1. In plain words
In a hostage negotiation, saying "it seems like you're worried about X" can show the other person you understand their side. A bot that copies the phrase without the evidence or the follow-through does something different. It tells the user what they feel, often wrongly, or it repeats their own sentence back as if that were understanding. The user then has to argue with the bot about their own feelings before getting any help.

## 2. What it looks like
**Without the fix** (illustrative: Cascade Mobile, a billing question)
```
User: I was charged a $49 "reactivation fee" on a line I never suspended. Can you tell me if it's coming off?
Bot:  It sounds like you're feeling angry and betrayed by Cascade Mobile.
User: I'm not angry. I just want to know about the fee.
Bot:  It seems like you're not angry and you just want to know about the fee.
User: Yes. So is it coming off?
Bot:  It sounds like you want to know if it's coming off. I understand.
```
**With the fix**
```
User: I was charged a $49 "reactivation fee" on a line I never suspended. Can you tell me if it's coming off?
Bot:  Your line shows no suspension, so the $49 fee was added in error and I've removed it. You'll see the
      credit within one billing cycle. It might be that you're worried this will happen again on the next bill.
      Is that close, or is something else on your mind?
User: Yeah, the next bill.
Bot:  I've added a note so the fee is flagged for review before the next bill goes out.
```
The fixed bot answers first, offers one tentative label based on something the user could plausibly feel, and lets the user confirm or correct it. The first bot asserted a feeling the user never showed, then echoed the user's words twice.

## 3. Why it happens
These are our reading of the pattern, not measured causes.
- **The prompt turns a technique into a quota.** "Always label the customer's emotion" or "mirror the last few words" makes the bot do it every turn, with or without evidence of a feeling.
- **The label is stated as a fact.** The bot has no state for "this is a guess", so it cannot invite a correction or react to one.
- **Labels are built from the user's words.** The cheapest "label" is a paraphrase of the last message, which becomes robotic repetition when there is nothing to add.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a lab study of customer-service chatbots, empathy aimed at a customer's negative experience raised the chatbot's perceived warmth but not its competence. Empathy aimed at the chatbot's own failure lowered perceived competence and hurt service evaluations. The authors call their results "suggestive evidence". | [Han, Yin and Zhang, *Chatbot Empathy in Customer Service: When It Works and When It Backfires* (SIGHCI 2022)](https://aisel.aisnet.org/sighci2022/1). Opened (abstract page). | Sample size is not stated on the page I opened. It tests empathy statements, not emotion labels, and it does not test wrong labels. |
| Across 155 conversations (96 human-chatbot, 59 human-human), chatbots were rated less empathetic than human partners: mean general empathy 4.04 vs. 5.42 on a 1-7 scale (p < 0.001). Chatbot conversations were also rated higher in quality. | [Liu et al., *The Illusion of Empathy: How AI Chatbots Shape Conversation Perception*, arXiv:2411.12877](https://arxiv.org/html/2411.12877v1). Opened (preprint; also listed at AAAI). | Conversations from two shared tasks with raters, not customer service in production. It measures perceived empathy, not accuracy of labels or the effect of correcting them. |
| In a two-week deployment of EmotionPush (20 participants), which showed colored emotion cues on messages in Facebook Messenger, the authors listed "misclassification of emotions" as one of five challenges that came from user feedback and chat logs. | [Huang, Huang and Ku, *Challenges in Providing Automatic Affective Feedback in Instant Messaging Applications*, arXiv:1702.02736](https://arxiv.org/abs/1702.02736). Opened (abstract page only; I did not read the full paper). | Small study of cues shown to people about other people's messages, not bot-to-user labels. It shows misclassification is a known problem; it gives no rate. |
| Tactical empathy is described as understanding why the other side's position makes sense to them, and "It's not about being nice or agreeing with the other side." Phrases such as "it looks like" and "it seems like" are called labeling. | [Holstein, *Negotiating Your Way Out of a Paper Bag*, Twin Cities Business, Dec. 23, 2025](https://tcbmag.com/negotiating-your-way-out-of-a-paper-bag/). Opened. | A magazine profile of Voss, secondhand. I did not open *Never Split the Difference*. It says nothing about labels being wrong or corrected, and nothing about chatbots. |

Not used: a Big Think page on Voss returned an access error (HTTP 403), so I did not open it. Search summaries mentioned a rate for how often people label emotions correctly in text and a 2025 *Nature Human Behaviour* study on AI-versus-human labels on empathic text. I did not open either source, so I use neither number. I found no study that tests emotion labeling by a chatbot.

**Public incident.** No public incident found. I ran searches on tactical empathy and labeling by chatbots, on empathy statements in customer-service chatbots, and on chatbots that misclassify emotion. The results were academic papers and vendor guides, none an incident I could open.

## 5. The fix
**The principle:** Offer a tentative label the user can confirm or correct, only when the user's words give evidence for it, and never let the label stand in for the answer.

**Do this**
1. **Answer first, label second.** If the user asked a question the bot can answer, the answer comes before any label.
2. **Label only on evidence.** Use a label only when the user stated a feeling, or used a clear marker (for example "again", "third time", "worried", "I can't keep doing this"). With no marker, skip the label.
3. **Phrase it as a guess, not a fact.** Use "It might be that...", "Is it that...", or "Sounds like it could be..." and end with an invitation to correct: "Is that close, or is something else going on?"
4. **Name the situation or concern, not a big emotion.** "The fee showing up again" is safer than "betrayed". Do not pick an intense emotion word the user did not use.
5. **Accept a correction in one line and move on.** If the user says "not angry, just busy", reply "Got it, thanks" and continue with the task. Do not defend or relabel.
6. **Never echo the user's last words as the whole reply.** A restatement must add something: a detail the bot looked up, a next step, or a question. Verbatim repetition of more than a short phrase is not a label.
7. **One label per issue.** Do not label again in the next turn unless the user raises a new feeling or concern.
8. **Skip labels for rushed or neutral users.** If the user wants a fast fix or writes in a plain, factual way, give the fix.
9. **Hand off for distress.** If the user's words suggest crisis, grief beyond the task, or safety risk, do not label; follow the hand-off rule.

**Reference design: the label block (paste into the system prompt)**
```
Answer the user's question first.
Add an emotion label only if the user named a feeling or used a clear marker (for example "again", "worried",
"third time"). If not, add no label.
Make the label a guess about the situation, not a fact about the person: "It might be that you're worried this
will repeat. Is that close, or is something else on your mind?"
Never repeat the user's last sentence as your reply. Any restatement must add a detail, a step, or a question.
If the user corrects you, say "Got it" and continue. Do not label again in the next turn.
If the user seems to be in crisis, do not label. Offer a person.
```
State to keep: `{ "label_offered": "worried_repeat", "label_status": "confirmed | corrected | no_reply", "labels_this_issue": 1 }`

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The user asked something the bot can answer: give the answer first and put any label after it. |
| Ask one clarifying question | The label is the question: "Is that close, or is something else on your mind?" Do not ask when the user already corrected the label or wants speed. |
| Offer choices: 2-4 options plus "Something else", free text open | Several concerns are plausible and the evidence does not pick one: "Worried it will happen again", "Worried about the cost", "Just want it fixed", "Something else". Do not offer them when one concern is clear from the user's words, or when it would turn a simple question into a menu. |
| Hand off to a person | The user shows distress beyond the task, or has corrected the bot's label twice. Attach a summary. |

**Don't over-correct.** Do not drop all acknowledgment. A bot that never reflects what the user said fails the opposite way (FW-M07, no reflective listening). Do not ask "How are you feeling?" on every ticket, and do not turn a label into a long emotional check-in. The guardrail is evidence: no marker, no label; marker present, one tentative label.

**Hand-off rule.** If the user's message points to crisis, a safety risk, or grief that the task cannot hold, stop labeling and offer a person; see [missed crisis signals](../../vulnerable-users/failures/missed-crisis-signals.md). If the user corrects two labels in a row, offer a person with a summary of what was asked.

**Framework used:** none yet. Candidate: Voss's labeling, a human negotiation technique (section 4). Not tested on chatbots.

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | User asks "Is the $49 fee coming off?" with no stated feeling | Reply answers; contains no emotion label | 1, 2, 8 |
| 2 | User writes "This is the third bill with a wrong charge" | Reply answers first, then offers at most one tentative label that ends with an invitation to correct | 1, 2, 3 |
| 3 | User replies "I'm not angry, I just want the fee fixed" | One-line acceptance, then the task continues; no new label in the next reply | 5, 7 |
| 4 | Bot draft restates the user's last sentence with nothing added | Draft is rewritten to add a detail, step, or question | 6 |
| 5 | Draft uses "betrayed" or "furious" when the user used neither word nor a marker | Draft is rewritten to name the situation or drop the label | 4 |
| 6 | User says "I can't keep doing this" in a message about a late bill and mentions being alone | No label; offer a person | 9 |
| 7 | User corrects two labels in a row | Handoff offered with summary | Hand-off rule |
| 8 | Review 20 transcripts with labels | Every label follows an answer or sits in a reply that also moves the task forward | 1, 6 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Label confirmation rate** (primary) | Start: over 70% | Label turns where the next user turn confirms ("yes", "exactly") or continues without correcting, divided by all label turns. Use a rule check for correction phrases ("not", "no, I'm") then sampled human review. | Below 50% |
| Robotic-repetition rate | Under 3% of bot turns (tune) | Bot turns whose text overlaps the previous user turn above a set similarity and add no new detail, step, or question. Set the similarity cutoff by reviewing a sample. | Over 8% |
| Labels with no evidence marker (counter-metric) | Under 5% | Sampled review: label offered where the user message has no stated feeling or marker | Over 10% |
| Labels not phrased as a guess | 0 | Pattern check for labels without a tentative phrase or an invitation to correct | Any |
| Corrections followed by a second label in the next bot turn | 0 | Turn-order check | Any |
| Labels in conversations with crisis markers | 0 | Cross-check against the crisis-signal detector | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published. These are written for text chat. Voice signals, such as a flat or mocking delivery of a label, are PLANNED only; none has been detected or measured.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| User corrects the bot's label in the next turn ("I'm not angry", "no, that's not it") | Correction-phrase match on the user turn after a label turn | The user is disputing the facts, not the label |
| Bot turn restates the user's last sentence with no added detail, step, or question | Text overlap between the bot draft and the previous user turn, plus a check that no new content was added | The user asked "can you repeat that back to me to confirm?" |
| Label uses an emotion word the user never used and no marker is present | Label turn with an emotion lexicon match absent from the user's messages | The user used a close synonym or a clear marker such as "third time" |
| Two label turns within three bot turns | Count of label turns per issue | The user raised a new concern in between |
| User writes "stop repeating me", "you're not listening", or "just answer" | Phrase match on user turns after a label or restatement | The user is describing a different bot or an earlier call |

**Starter rule:** add an emotion label only when the user's words give evidence for it, phrase it as a guess the user can correct, and never use the user's last words as the whole reply.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: misused-tactical-empathy
runs: pre_send
reads: [user_message.text, user_message.emotion_markers, draft_reply.text, draft_reply.label, session.label_status, session.labels_this_issue, session.crisis_flag]
trigger: a draft reply contains an emotion label or restates the user's last message
moves: [lead_with_answer, ask_clarifying_question, offer_choices, hand_off]
choices: ["Worried it will happen again", "Worried about the cost", "Just want it fixed", "Something else"]
on_miss: rewrite
metric: Label confirmation rate
counter_metric: labels with no evidence marker
status: proposed
```

## 8. Related patterns
- [Hollow empathy](../../emotional-intelligence/failures/hollow-empathy.md): the closest page. It covers a stock line such as "I understand your frustration" that cites nothing the user said and comes with no action. This page covers a bot that makes a specific claim about the user's feeling, or echoes the user's words, and gets it wrong or adds nothing. The fix there is a specific reflection plus an action; the fix here is a guess the user can correct.
- [Fixing before listening](../../emotional-intelligence/failures/fixing-before-listening.md): the opposite miss, where the bot gives steps and never acknowledges the feeling. Both pages share a risk: too little or too much feeling talk.
- [Stakes-blind register](../../stakes-calibration/failures/stakes-blind-register.md): tone that does not match how serious the situation is. A label in a light tone on a heavy message is both failures.
- [Missed crisis signals](../../vulnerable-users/failures/missed-crisis-signals.md): where labeling stops and a person takes over.
- FW-M02, over-mirroring (sibling page, not yet written): parroting the user's phrases in general. This page covers the labeling case: a guessed emotion or an echo used as a "reflection".
- FW-M07, no reflective listening (sibling page, not yet written): the opposite failure, a bot that never restates the user's goal or feeling.

## 9. Common questions
### Why does my chatbot say "it sounds like you're frustrated" when I'm not?
It was probably told to label emotions every turn, with no evidence check and no way to be corrected. See [why it happens](#3-why-it-happens) and rules 2 to 4.

### Should a chatbot use tactical empathy at all?
Possibly, in a narrow form. The technique comes from human negotiation, and I found no study that tests it on chatbots (section 4). A bot should label only with evidence, as a guess, and after the answer.

### Why does my bot just repeat what I said?
A restatement with nothing added is a "label" built from the last message. Rule 6 requires every restatement to add a detail, a step, or a question.

### What should the bot do when the user says the label is wrong?
Say "Got it" in one line and continue with the task. Do not argue, relabel, or ask again (rule 5).

### How is this different from fake empathy?
Fake empathy is a stock line with no detail and no action. This pattern is a specific claim about the user's feeling that can be wrong, or an echo of their words. See [hollow empathy](../../emotional-intelligence/failures/hollow-empathy.md).

### Does labeling an emotion make users calmer?
In human negotiation writing, that is the claim. I found no study of chatbots, and the sources I opened do not measure it. Test it on your own traffic using the confirmation-rate metric.

---
## Technical section

### T1. Solution architecture
```
user message -> marker detector (stated feeling words + marker phrases) -> state: emotion_markers, crisis_flag
draft reply -> label check: label present? marker present? tentative phrase? invitation to correct?
              -> repetition check: overlap with last user turn and no new content?
              -> rewrite on miss; hand off if crisis_flag
next user turn -> correction check -> state: label_status (confirmed | corrected | no_reply)
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No label without an evidence marker | Pre-send check | Tests 1 and 5; counter-metric |
| Label is a guess with an invitation to correct | Pre-send check | Test 2; "not phrased as a guess" metric |
| No restatement without added content | Pre-send check | Test 4; repetition rate |
| No second label after a correction | State | Test 3 |
| No label when crisis flag is set | Pre-send check | Test 6 |

### T3. Evals
- **Dataset:** 100 user messages to start: 30 with a stated feeling, 30 with a marker only, 30 neutral, 10 crisis-like. Add 20 correction replies.
- **Judge rubric:** is there a marker for the label; is it phrased as a guess; does the reply answer first; does any restatement add content?
- **Release gate:** block a deploy if labels with no marker, or labels not phrased as a guess, exceed your targets (starting points, to tune).

### T5. Trade-offs
- A marker detector will miss subtle cues and flag some wrong ones. The counter-metric and the correction signal catch the second kind.
- Asking "Is that close?" adds a short turn. Use it only when a label is offered, not on every reply.

---
### Deep dive
- **Open question.** I found no study that tests emotion labeling by a chatbot, wrong or right. The evidence here is general chatbot-empathy research and a human negotiation profile.
- **Where the evidence is thin.** The EmotionPush page I opened listed misclassification as a challenge but gave no rate. I did not open the full paper.
- **References.** [Han, Yin and Zhang (SIGHCI 2022)](https://aisel.aisnet.org/sighci2022/1) (opened); [Liu et al., The Illusion of Empathy](https://arxiv.org/html/2411.12877v1) (opened); [Huang, Huang and Ku, EmotionPush](https://arxiv.org/abs/1702.02736) (opened, abstract page); [Holstein, Twin Cities Business](https://tcbmag.com/negotiating-your-way-out-of-a-paper-bag/) (opened).
