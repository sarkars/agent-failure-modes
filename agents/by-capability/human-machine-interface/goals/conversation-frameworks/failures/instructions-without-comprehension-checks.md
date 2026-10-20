# Chatbot Gives Multi-Step Instructions and Never Checks They Were Understood: Instructions Without Comprehension Checks

<!-- SEO
title: Chatbot Never Checks You Understood the Steps: Teach-Back
description: Why a chatbot gives multi-step instructions and moves on with "any questions?", and a teach-back rule: chunk the steps, ask for them in the user's words.
search phrases:
- chatbot gives long instructions and never checks understanding
- how to make a chatbot confirm the user understood the steps
- teach-back method for chatbots
- chatbot "does that make sense" doesn't work
- chatbot instructions user does steps in the wrong order
- how to check user comprehension in a chatbot conversation
- chatbot user says ok but didn't understand
-->

**Frequency**: Common

## Issue: The bot gives a multi-step instruction, ends with "Does that make sense?" or nothing, and treats "ok" as understanding, so a skipped or reordered step shows up later as an error.

> **One line:** The bot lists the steps and moves on without asking the user to say them back; the fix is to give a few steps at a time and, for any step that costs money or data if missed, ask the user to put it in their own words before going on.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice and visual are PLANNED, not written. |
| **Stakes** | Low for a settings tip. High when a missed or reordered step causes a double charge, lost data, or a missed deadline. |
| **Who is affected** | Anyone following a multi-step task from a bot, most of all people doing it for the first time or while distracted |
| **Frequency** | Common. This is our judgment from how instruction replies are usually written; I found no study that counts how often bots skip comprehension checks. |
| **Pattern ID** | instructions-without-comprehension-checks |
| **Family** | [Conversation frameworks](../README.md) (row FW-C09) |
| **Goal** | The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange. |
| **Primary metric** | Comprehension-check rate: replies that give a multi-step instruction with a costly step and are followed by an open comprehension check. Start: over 80% (tune). Reported with the error rate at each step. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A stronger model writes clearer steps, but whether to stop and check is a conversation rule the product sets and tests. (Our judgment, not tested.) |
| **Also searched as** | chatbot never confirms I understood · bot says "any questions?" and leaves · chatbot teach-back · bot assumes I got it · chatbot instructions too long to follow |

> **Read this first.** Teach-back comes from human practice, mostly health communication: a clinician asks a patient to restate instructions in their own words. I found no study that tests it on chatbots, so treat the fix as a hypothesis to test on your own traffic. The one outcome study I opened (section 4) is a small non-randomized pilot with human staff.

## 1. In plain words
When a person explains something complicated, a good teacher stops and asks, "What will you do first?" A bot often gives four steps, adds "Let me know if you have questions!", and counts the chat as done. Most people reply "ok" because it is polite, not because they followed it. The misunderstanding only appears later, when the step goes wrong.

## 2. What it looks like
**Without the fix** (Harbor Credit Union app, moving autopay to a new card before the 15th)
```
User: I got a new debit card. How do I move my car loan autopay to it?
Bot:  1) Add the new card under Payments > Cards. 2) Turn off autopay on the old card. 3) Turn on autopay with
      the new card and pick a date. 4) Confirm the first payment shows as scheduled. Make sure it's done before
      the 15th. Does that make sense?
User: ok got it
Bot:  Great! Anything else I can help with?
(Two days later) User: I was charged twice for the loan.
```
**With the fix**
```
User: I got a new debit card. How do I move my car loan autopay to it?
Bot:  Two steps first. 1) Add the new card under Payments > Cards. 2) Turn on autopay with the new card.
      Do not turn off the old autopay yet: leaving both on before the 15th can charge you twice.
      In your own words, what will you do first, and what will you wait on?
User: add the card, then turn off the old one I guess
Bot:  Close. Add the card first, yes. Then set up the new autopay, and turn off the old one only after the new one
      shows "Scheduled". I explained that badly. Want to try the order again, or have me list it as a checklist?
```
The fixed bot sends two steps, names the costly mistake, asks for the plan in the user's words, and corrects the one gap it hears.

## 3. Why it happens
- **The bot is written to be complete in one reply.** A prompt that says "give all the steps" produces the full list, and the end of the list is where "Does that make sense?" gets pasted.
- **A closed question invites a polite yes.** "Does that make sense?" and "Any questions?" take one word to answer, and nothing in the product reads that word as anything but success.
- **The bot cannot see the task.** A nurse can watch a patient hold an inhaler. A chat bot sees only text, so without a request to say or show the plan back, it has no signal of a misunderstanding until the user comes back with an error.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a Dutch emergency department pilot, older adults (137 analyzed: 70 standard care, 67 teach-back) fully retained the medication instructions at discharge in 50.0% of the standard-care group and 91.8% of the teach-back group (adjusted odds ratio 14.89; 95% CI 4.12 to 53.85). | [Hesselink et al., *Emergency Medicine Journal*, 2022: teach-back of discharge instructions, pre-post pilot](https://pmc.ncbi.nlm.nih.gov/articles/PMC8788250). Opened and read. | Human staff, hospital discharge, not a chatbot. Non-randomized pre-post at one site (March to October 2019) and the authors call it a pilot. Gains were smaller or not significant in other domains (for example, post-ED care 69.4% vs 75.0%). |
| In the same pilot, 7-day return visits were 5.0% (17 patients) in standard care and 1.0% (3 patients) with teach-back, but the adjusted difference was not statistically significant (AOR 0.23; 95% CI 0.05 to 1.07). | Same page. Opened and read. | A signal, not proof of fewer errors. Do not read it as "teach-back prevents revisits". |
| The same pilot found a median discharge conversation of 7 minutes (standard care) vs 5 minutes (teach-back) for older adults, p=0.22. | Same page. Opened and read. | Not statistically significant. It shows no clear time penalty in that study; it does not show teach-back saves time. |
| Teach-back means asking people to restate information in their own words, using open-ended questions that "cannot be answered by 'yes' or 'no'". The post also says studies show 40-80% of medical information is forgotten right after an encounter. | [WebMD Ignite, *The teach-back method*](https://webmdignite.com/blog/teach-back-method-communicating-more-effectively-patients-improve-health-outcomes) (no publication date shown). Opened and read. | A vendor blog. The 40-80% figure cites unnamed "studies", so I do not use it in the fix. |
| A nursing-association blog describes teach-back as sharing small portions, confirming each one before going on, filling the gap if a patient cannot explain a point back, and asking for a demonstration (show-me) for hands-on tasks. | [Carpenter, *Tackling the Teach-Back Method*, Healthy Nurse, Healthy Nation, Sep 27, 2023](https://engage.healthynursehealthynation.org/blogs/8/4537). Opened and read. | A blog, not a study. It does not address "Do you understand?" directly. |

Not opened: the AHRQ teach-back tool pages, an NSW Health teach-back PDF, and a PubMed Central systematic review all returned 403 or a browser check, and a second emergency department paper redirected to a login. I read only search summaries of them. A summary mentioned a 2019 meta-analysis on 30-day readmission and a chunk-size guide; I use none of it. I found no study of a chatbot doing teach-back. A search returned learning-by-teaching bots (where the learner teaches the bot), which is a different method, and I did not open them.

**Public incident.** No public incident found. Searches returned teach-back method guides and clinical studies, not a dated incident involving a chatbot's instructions.

## 5. The fix
**The principle:** For any multi-step instruction with a costly step, send a few steps at a time and ask the user to say the plan back in their own words before sending more.

**Do this**
1. **Chunk.** Send at most 3 steps per reply (a starting point to tune, not a sourced limit). Put the costly step and the mistake it prevents in the first chunk.
2. **Name the costly step.** Mark any step where an error costs money, data, or a deadline, and say what goes wrong if it is missed or done out of order.
3. **Ask open, not closed.** End the chunk with a question that needs the user's own words: "In your own words, what will you do first?" Do not end with "Does that make sense?", "Any questions?", or "Got it?".
4. **Do not count "ok" as understood** when the chunk has a costly step. Ask the open question once more, in a lighter form.
5. **Compare the reply with the steps.** Check the order and the costly detail. Pass it if both are right; do not grade wording.
6. **If there is a gap, own it and re-explain differently.** Say the miss was in the explanation, use different words or a checklist, and ask once more. Never repeat the same text.
7. **For hands-on steps, ask for what the screen shows.** "Tell me what the status says after step 2" is the text version of show-me.
8. **Log the check.** Store the chunk, the costly step, the user's restatement, and pass or gap, so a hand-off carries it.

**Reference design: the instruction block (paste into the system prompt)**
```
When you give a task with 3 or more steps, and any step can cost money, lose data, or miss a deadline:
1. Send at most 3 steps. Put the costly step first, and say what goes wrong if it is skipped or done out of order.
2. End with ONE open question that asks for the plan in the user's words ("In your own words, what will you do first?").
   Never end with "Does that make sense?" or "Any questions?".
3. If the user replies only "ok" or "got it", ask once more: "Quick check: which step comes first?"
4. Compare the reply with the steps. If the order or the costly detail is wrong, say the explanation was unclear,
   re-explain in different words, and ask again once. After two misses, offer a person.
5. Only then send the next chunk.
```
State to keep: `{ "task": "move_autopay", "chunks": [{"steps": [1,2], "costly_step": 2, "check": "asked", "user_restatement": "add card, turn off old", "result": "gap"}], "misses": 1 }`

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | After each chunk that has a costly step: one open question asking the user to say the plan in their words. |
| Offer choices: 2-4 options plus "Something else", free text open | After a gap: "Explain it again", "Show it as a checklist", "Talk to a person", "Something else". Do not offer them on a first check that passed, or when the user is fluent and already stated the plan. |
| Hand off to a person | Two misses in a row on the same costly step, or the user says they are stuck or asks for a person. Attach the check log. |

**Don't over-correct.** A check after every instruction feels like a quiz, and users stop answering. Skip it for low-stakes tips ("tap Settings, then Dark mode") and when the user already restated the plan unprompted. Ask at most one check per costly step. Keep the tone as "so I know I explained it well," not a test, and let "I've done this before" end the check. The guardrails are the costly-step rule and the two-miss limit. See [over-confirmation](../../dialogue-management/failures/over-confirmation.md) for the same trap with "are you sure?".

**Hand-off rule.** After two misses on the same costly step, or when the user asks for a person, hand off with the task, the chunks sent, and each restatement, so the person does not start over.

**Framework used:** none yet. Candidate: the teach-back and chunk-and-check practice described in the sources in section 4, from human health communication and untested on chatbots.

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | User asks how to move autopay to a new card (a 4-step task) | First reply has at most 3 steps and puts the double-charge warning in them | 1, 2 |
| 2 | Same task | Reply ends with an open question asking for the plan in the user's words, not "Does that make sense?" | 3 |
| 3 | User answers "ok got it" | Bot asks one lighter check before sending more steps | 4 |
| 4 | User says "add the card, turn off the old one" (wrong order) | Bot flags the order, says its explanation was unclear, and re-explains in different words | 5, 6 |
| 5 | User gets it right in their own words | Bot confirms and sends the next chunk without a second check | 5 |
| 6 | Hands-on step (find and read a status) | Bot asks what the screen shows after the step | 7 |
| 7 | Low-stakes tip: turn on dark mode | Bot gives the steps and does not ask for a restatement | Don't over-correct |
| 8 | Two misses on the same costly step | Bot offers a person and passes the check log | Hand-off |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Comprehension-check rate** (primary) | Over 80% (tune) | Replies with 3 or more steps and a flagged costly step that are followed by an open check, divided by all such replies. Rule check on the draft plus a judge on a sample. | Under 60% |
| Error rate at each step | Track; set from baseline | Per task, user turns reporting a wrong, skipped, or out-of-order step, divided by chats that reached that step. Sampled review plus intent tags. | Up 20% vs baseline |
| Closed-prompt endings on costly instructions | Under 10% (tune) | Rule check: replies ending with "Does that make sense?", "Any questions?" or "Got it?" | Over 20% |
| Checks on low-stakes instructions (over-correction) | Under 10% (tune) | Open checks on replies with no flagged costly step, divided by such replies | Over 20% |
| Chats that end after a check with no reply (friction) | Under 10% (tune) | Chats whose last event is an unanswered check, divided by chats with a check | Over 20% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A reply gives 3 or more steps and ends with a closed prompt or nothing | `bot_reply.step_count` of 3 or more and `bot_reply.ends_with_open_check` is false | The task is low-stakes, or the user asked for a quick list |
| The user replies only with "ok" or "got it" and the bot sends more steps | Short acknowledgment turn followed by a new bot chunk with no check | The user already restated the plan earlier in the chat |
| The user asks which step comes first or asks for a repeat within 3 turns | User turn matching a repeat or order question after an instruction reply | The user is skipping to a later step on purpose |
| The user later reports a step done out of order or skipped | User turn naming a step result that contradicts the logged order | The user took a valid alternative order |
| The bot resends the same steps after the user's confusion | New bot reply text near-identical to the earlier instruction reply | The user asked to see the list again |

**Starter rule:** for any instruction with a costly step, send at most 3 steps and end with an open question that asks the user to say the plan in their own words.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: instructions-without-comprehension-checks
runs: pre_send
reads: [draft_reply.step_count, draft_reply.has_costly_step, draft_reply.ends_with_open_check, session.comprehension_checks, session.misses]
trigger: a reply is about to be sent with 3 or more steps and a costly step, and it has no open comprehension check, or the user answered a check with only an acknowledgment
moves: [ask_clarifying_question, offer_choices, hand_off]
choices: ["Explain it again", "Show it as a checklist", "Talk to a person", "Something else"]
on_miss: rewrite
metric: comprehension-check rate
counter_metric: checks on low-stakes instructions
status: proposed
```

## 8. Related patterns
- [Unstructured procedures](../../response-structure/failures/unstructured-procedures.md): the closest page. It is about how a how-to answer is laid out (numbered steps, one action each). This page assumes the steps are well laid out and asks whether the user understood them. A clean numbered list can pass that page and fail this one.
- [Unstructured troubleshooting](unstructured-troubleshooting.md): a sibling in this family. It covers batching changes when the cause is unknown. This page covers known instructions where the risk is that the user misunderstood them.
- [Over-confirmation](../../dialogue-management/failures/over-confirmation.md): asking "are you sure?" on routine steps. It is the opposite risk to watch for if this fix is applied to everything.
- [Partial answers to multi-part questions](../../effort-and-memory/failures/partial-answers-to-multi-part-questions.md): the bot drops parts of what the user asked. Here the bot delivers every part, and no one checks that the user took them in.
- [No ask](no-ask.md): a sibling that is a missing next step in a sales chat, not a missing check.

## 9. Common questions
### Why does "Does that make sense?" not work in a chatbot?
It takes one word to answer, and a polite "ok" looks the same as understanding in the log. A request for the plan in the user's own words gives the bot something to compare with the steps. See rule 3 in [the fix](#5-the-fix).

### What is teach-back, and does it work for chatbots?
Teach-back is a human practice: you ask someone to restate what you told them. I found no study on chatbots, so the claim here is a hypothesis. The only outcome data I opened are from a human pilot, described in [why it matters](#4-why-it-matters).

### How many steps should a chatbot give at once?
Our starting point is three, with the costly step and its warning in the first chunk. That number is not from a source I opened. Tune it on your own traffic by watching the error rate at each step.

### Won't asking users to repeat the steps annoy them?
It can. That is why the fix applies only to instructions with a costly step, asks once per such step, and lets a confident user skip it. Watch the friction metric in section 7. See Don't over-correct in [the fix](#5-the-fix).

### What if the user explains the steps wrong?
Say the explanation was unclear, re-explain in different words or as a checklist, and ask once more. After two misses, offer a person with the log attached.

---
## Technical section

### T1. Solution architecture
```
instruction draft -> classify: step count, costly step flagged? (from a task config or a judge)
                  -> if costly and no open check: rewrite to a 3-step chunk + one open question
user reply        -> acknowledgment-only? ask the lighter check; else compare restatement to steps
                  -> pass: send next chunk | gap: re-explain in new words, count a miss | 2 misses: hand off
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| At most 3 steps per reply | Pre-send check | Test 1; metric rows 1 and 3 |
| Open check after a costly chunk | Pre-send check | Test 2; primary metric |
| "ok" is not understood | State plus pre-send check | Test 3 |
| Re-explain in new words after a gap | Pre-send check on near-duplicate text | Test 4 |
| No check on low-stakes tips | Task config | Test 7; over-correction metric |

### T3. Evals
- **Dataset:** 50 instruction requests to start across account changes, device setup, and forms. Include 15 with a costly step, 15 low-stakes, 10 where the user restates the plan wrongly, and 10 where the user replies only "ok".
- **Judge rubric:** how many steps are in the reply; is the costly step named with its consequence; does the reply end with an open question; does the follow-up compare the restatement with the steps; is a re-explanation in new words?
- **Release gate:** block a deploy if the primary metric falls under target or the over-correction metric rises past its alert (starting points, to tune).

### T5. Trade-offs
- More turns per task, and a flagged-costly-step list to maintain per task.
- Judging a free-text restatement will sometimes pass a wrong plan or fail a right one. Sampled review of misses catches the drift.

---
### Deep dive
- **Open question.** I found no study of chatbot teach-back. The evidence is one human pilot and two explanatory blogs.
- **Voice (PLANNED, not written).** A spoken reply cannot be re-read, so chunk size and check timing would need their own treatment. No voice data is used here.
- **References.** [Hesselink et al., 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8788250) (opened); [WebMD Ignite, teach-back method](https://webmdignite.com/blog/teach-back-method-communicating-more-effectively-patients-improve-health-outcomes) (opened); [Carpenter, Healthy Nurse, Healthy Nation, 2023](https://engage.healthynursehealthynation.org/blogs/8/4537) (opened).
