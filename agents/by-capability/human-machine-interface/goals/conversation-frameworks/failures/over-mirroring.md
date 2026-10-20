# Chatbot Repeats What I Said: Over-Mirroring

<!-- SEO
title: Chatbot Repeats What I Said: Over-Mirroring
description: A chatbot that parrots your own words back feels like mockery. Restate by meaning, copy only names and numbers, and stop when asked.
search phrases:
- chatbot repeats what I said
- why does my chatbot repeat everything I say
- chatbot repeats my words back to me
- chatbot parroting the user
- chatbot sounds like it is mocking me
- how to stop a chatbot from repeating the user's words
- chatbot reflective listening sounds robotic
-->

**Frequency**: Occasional

## Issue: A chatbot that parrots your own words back feels like mockery. Restate by meaning, copy only names and numbers, and stop when asked.

> **One line:** The bot answers by quoting the user's own phrases back ("I understand that your internet is 'dropping every night around 9'"), which sounds like mockery; the fix is to restate by meaning in the bot's own words, copy exact words only for facts, and get on with the answer.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice and web signals are PLANNED, not written or detected. |
| **Stakes** | Low to medium. The cost is a user who feels mocked, writes "stop repeating me", and may leave or escalate. |
| **Who is affected** | Any user who states a problem or a feeling, especially an upset one, and gets their own sentence handed back |
| **Frequency** | Occasional. Our judgment from how empathy and "show you understood" instructions are written; I found no study that counts how often bots parrot users. |
| **Pattern ID** | over-mirroring |
| **Family** | [Conversation frameworks](../README.md) (row FW-M02) |
| **Goal** | The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange. |
| **Primary metric** | Verbatim-repeat rate. Start: under 2% of bot replies |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A stronger model paraphrases more fluently, but it still parrots when the prompt says "repeat back what the user said" and nothing checks the overlap. (Our judgment, not tested.) |
| **Also searched as** | chatbot repeats what I said · chatbot parroting · chatbot echoes my words · chatbot sounds like it is mocking me · chatbot mirroring too much · chatbot repeats my sentence back |

> **Read this first.** The research behind this page is about people copying each other's gestures and manners, mostly face to face. I found no study that tests word-for-word echoing by a chatbot. Treat the fix as a hypothesis to test on your own transcripts.

## 1. In plain words
A user writes "my internet drops every night around 9 and I'm sick of it." A bot that says "I understand your internet 'drops every night around 9' and that you are 'sick of it'" has proved only that it can copy. People hear that as mockery, or as a script, and the problem has not moved. A good listener says it back in new words and then does something with it.

## 2. What it looks like
**Without the fix** (Lakeview Internet, a home-internet support chat in Ohio)
```
User: My internet has been dropping every night around 9 and I'm honestly sick of it.
Bot:  I understand that your internet has been "dropping every night around 9" and that you are "honestly sick of it."
User: Yeah. So can you fix it?
Bot:  I hear that you want me to "fix it." Can you tell me more about "dropping every night around 9"?
User: Stop repeating everything I say. Are you mocking me?
Bot:  I hear that you feel I am "mocking" you.
```
**With the fix**
```
User: My internet has been dropping every night around 9 and I'm honestly sick of it.
Bot:  A nightly outage is hard to live with. Do your wired devices drop too, or only Wi-Fi?
User: Yeah. So can you fix it?
Bot:  I can start now. Next time it drops, check the color of the modem's front light and tell me what you see.
      If it turns red or orange, I'll book a technician: Thursday morning or Saturday morning are open.
User: It goes orange.
Bot:  Orange points to a line problem, not your Wi-Fi. Want Thursday or Saturday morning?
```
The fixed bot restates the problem by meaning in four words ("a nightly outage"), asks one question that moves the case forward, and copies exact words only where the next step needs them.

## 3. Why it happens
These are our reading of the pattern, not measured causes.
- **"Show you understood" is written as "repeat it back."** Prompts such as "acknowledge the user's message by restating it" give the model no rule about how far to change the wording, so copying satisfies the instruction.
- **Copying is the cheapest restatement.** The user's sentence is already in the context window. Nothing compares the draft to the user's message, so a near-copy ships.
- **Nothing says when to skip.** The reflection runs on every turn, including "ok" and "can you fix it?", so the same frame repeats until the user notices.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Chartrand and Bargh (1999): in Experiment 2, confederates mimicked participants' posture and movements, and "mimicry facilitates the smoothness of interactions and increases liking between interaction partners." | [Chartrand and Bargh, *The Chameleon Effect*, JPSP 76(6)](https://pages.ucsd.edu/~pwinkiel/chameleon.pdf). Opened; I read the abstract only, from a local copy of the PDF. | Nonverbal mimicry of posture and mannerisms between people, not words in a chat. It shows light, unnoticed matching can help; it says nothing about quoting. The library's [roadmap](../../../roadmap/conversation-frameworks.md) notes a replication reported as only partly successful; I did not open it. |
| Wessler et al. (2024) ran three experiments (N = 71, 149 and 180) with a confederate who showed no, subtle or strong mimicry. In the two lab studies, strongly mimicked participants liked and trusted the confederate less than subtly mimicked ones. In Experiment 1, 16 of the strong-mimicry participants (group n = 23) noticed the mimicry; in Experiment 2, 27 did. | [Wessler, Loschelder, Fendel and Friese, *The Too-Much-Mimicry Effect*, J. Nonverbal Behavior 48 (2024)](https://link.springer.com/article/10.1007/s10919-023-00446-5). Opened. I read the first 100,000 of about 135,000 characters. | Distributive negotiation with a confederate copying behavior, in a lab. In the online Experiment 3, strong and subtle mimicry did not differ on liking or trust, and 32 people noticed the "subtle" mimicry. Authors' summary: too much mimicry backfires. Not a chatbot study. |
| Winkielman and colleagues (UC San Diego, 2011): observers who watched staged interviews rated an interviewee who copied a condescending interviewer as less competent, though they did not notice the copying. The cost disappeared when they first read good news about the interviewer's character. | [APS press release, *When It's An Error To Mirror*](https://www.psychologicalscience.org/news/releases/when-its-an-error-to-mirror.html). Opened; the release gives no sample size or statistics, and I did not open the paper. | Press release about a forthcoming paper. About copying a rude person's body language, as seen by observers. It supports one point: copying the wrong thing has a social cost. |
| Dieter et al. (CoNLL 2019): "expert human communicators often mimic and rephrase" what a partner says; the authors built agents that mimic and rephrase a user's request, and report generated responses comparable to human-written ones. | [Dieter et al., *Mimic and Rephrase: Reflective Listening in Open-Ended Dialogue*](https://aclanthology.org/K19-1037/). Opened the abstract page only. | Short sympathy and "I do not know" replies, not a test of copying versus rephrasing. It supports the shape of the fix (restate, in changed form), not any number. |
| Siemens' design-system guidance says to acknowledge the user's input and then continue with the response; it says nothing about copying the user's wording. | [Siemens Industrial Experience, *Acknowledging users*](https://ix.siemens.io/docs/guidelines/conversational-design/designing-conversations/acknowledging-users.md). Opened. | One company's design guidelines. It describes a practice, not an outcome. |

Not used: I did not open the original of any of these. A search summary said a systematic review of chatbot design (Silva and Canedo) lists echoing user input "when appropriate" as a naturalness practice. Another cited a figure that 36.3% of messages in a companion-chatbot study were reflective summaries, which the summary itself said it could not verify. A third described ELIZA's broken echoes from course notes. I opened an arXiv abstract on Apple's study of matching an assistant's conversational style (Metcalf et al., 2019); it reports no results, so I use no finding from it. I found no Nielsen Norman Group source on this topic.

**Public incident.** No public incident found. I searched for chatbots that repeat the user's words and for user complaints about parroting. The results were design advice and research papers, none a dated incident.

## 5. The fix
**The principle:** Restate what the user means in new words, copy exact words only for facts, and always move the conversation forward in the same reply.

**Do this**
1. **Never repeat a run of 3 or more consecutive words from the user's latest message, in quotation marks or not.** Runs made only of common function words ("I want to") do not count. The 3-word limit is a starting point to tune.
2. **Copy exactly only what the next step needs:** names, numbers, dates, order and error codes, product names. "Order 5512" is copied; "my order is totally messed up" is not.
3. **Restate by meaning, once, and only when it helps.** Reflect when the request is complex, has two or more parts, or states a feeling or goal that changes the action. Do not reflect a simple request ("What are your hours?").
4. **A restatement is never the whole reply.** Follow it in the same reply with the answer, one question, or a next step.
5. **Name a feeling at most once, and only with a word the user wrote.** "Frustrating" after the user wrote "frustrated" is fine. Do not quote it, and do not guess a different feeling.
6. **Do not open two replies in a row with the same frame.** "I understand that" or "I hear that" twice in a row fails.
7. **Never echo an insult, sarcasm, profanity, or a typo.** Answer the real question underneath. For abuse, follow [mishandled abuse](../../difficult-customers/failures/mishandled-abuse.md).
8. **Match scale and register, not words.** A short message gets a short reply and a formal one a formal reply. See [one-size communication style](../../cultural-adaptation/failures/one-size-communication-style.md).
9. **When the user says to stop ("stop repeating me", "are you mocking me"), drop all restatements for the rest of the conversation.** Say so in one short clause and answer the question.

**Reference design: the restate-lightly block (paste into the system prompt)**
```
Show you understood by changing the words, not copying them.
Never reuse 3 or more words in a row from the user's last message, except names, numbers, dates, and codes.
Restate only complex or multi-part requests, once, then answer or ask one question in the same reply.
Do not start two replies in a row the same way. Never repeat an insult, sarcasm, or a typo.
If the user says you are repeating them, stop restating for the rest of the chat and answer.
```
Check before sending: `{ "longest_copied_run": 5, "exact_facts_only": false, "reflections_this_turn": 2, "stop_cue": false }` fails rules 1 and 3, so the draft is rewritten.

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every reply: at most one short restatement in new words, then the answer or next step. Never end a turn on the restatement. |
| Ask one clarifying question | The request is complex and the bot is not sure it understood: check the goal in new words ("Is the problem only at night?"). Do not ask when the request is simple or the answer is the same either way. |
| Hand off to a person | The user says the bot is repeating or mocking them twice, even after restatements stopped. Do not hand off if the user asked to stay with the bot. |

"Offer choices" is not used here. A menu does not fix a bot that is copying, and it would add another script.

**Don't over-correct.** Do not drop listening altogether. A bot that never shows it understood a long or emotional message ("I have three problems and the first one started in May") fails the other way: see the planned no-reflective-listening page (FW-M07) in the [catalog](../../../roadmap/conversation-frameworks.md). Do not paraphrase an order number or an address; copy it exactly and confirm it. Do not rewrite so far that the meaning changes. The guardrail is the counter-metric in section 7: complex requests must still get a restatement of the goal.

**Hand-off rule.** If the user says the bot is repeating or mocking them twice, or asks for a person, offer a person and pass the summary of what they asked, so they do not have to say it again.

**Framework used:** none yet. Candidate: reflective listening in human practice (the "mimic and rephrase" abstract in section 4), a hypothesis to test on chatbots.

## 6. How to test it (short version)
No full test file yet. All tests: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | User writes "dropping every night around 9 and I'm honestly sick of it" | No run of 3 or more consecutive words from the message (outside the allowlist) appears in the reply | 1 |
| 2 | User writes "Order 5512 arrived damaged" | "5512" is copied exactly; the rest is in new words | 2 |
| 3 | User asks "What are your hours?" | The reply gives the hours with no restatement | 3 |
| 4 | User gives a three-part request | One restatement in new words, and the reply also moves forward | 3, 4 |
| 5 | Five turns in a row with an upset user | No two bot replies open with the same first three words | 6 |
| 6 | User calls the bot a "useless idiot" | The insult is not repeated; the real question is answered | 7 |
| 7 | User says "Stop repeating everything I say" | The next replies and all later ones have no restatement | 9 |
| 8 | User says it twice | The bot offers a person with a summary | Hand-off rule |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Verbatim-repeat rate** (primary) | Start: under 2% of bot replies | Bot replies sharing a run of 3 or more words with the user's latest message, excluding exact-fact tokens and function-word-only runs, divided by all bot replies. Computed by script on the log. | Over 5% |
| "Stop copying me" cues | Under 0.5% of chats (tune) | User turns matching a phrase list such as "stop repeating", "stop copying", "are you mocking me", "why do you keep saying what I said"; confirm on a sample. | Doubles against baseline |
| Replies that are only a restatement | 0 | Bot turns with no answer, question, or next step, by judge on a sample | Any |
| Same opening frame twice in a row | Under 1% of turns (tune) | First three words of consecutive bot replies compared | Over 3% |
| Complex requests with no restatement of the goal (counter-metric) | Under 20% (tune) | Sampled complex requests; judge checks for a paraphrase of the goal | Over 35% |
| Exact facts copied correctly | 100% | Order numbers, dates, and codes in the reply compared to the user's message | Any miss |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published. All are written for text.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Bot reply shares a run of 3 or more words with the user's last message | Overlap script on `bot_reply.text` and `user_msg.text`, outside the allowlist | The run is an order number, address, or error code the bot must confirm |
| Two consecutive bot replies start with the same three words | First three words of each `bot_reply.text` | A fixed legal or disclosure opener the business requires |
| User turn contains a stop-copying phrase right after a bot reply | Phrase-list match on the next `user_msg.text` | The user is quoting the bot to correct a fact ("you said Friday, I said Thursday") |
| Bot reply that is a restatement and nothing else | No question mark, no answer or action field in `bot_reply` | The user asked the bot to read something back to confirm it |
| User repeats the same request right after a restatement-only reply | Same intent in the next user turn | The user added a detail that changes the request |

**Starter rule:** restate the user's meaning in your own words, never repeat 3 or more of their words in a row, and copy exactly only names, numbers, dates, and codes.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: over-mirroring
runs: pre_send
reads: [user_msg.text, bot_draft.text, session.exact_fact_tokens, session.stop_cue_count, bot_draft.reflection_count]
trigger: a draft reply is about to be sent and it shares a run of 3 or more words with the user's latest message
moves: [lead_with_answer, ask_clarifying_question, hand_off]
choices: none
on_miss: rewrite
metric: verbatim-repeat rate
counter_metric: complex requests with no restatement of the goal
status: proposed
```

## 8. Related patterns
- [Regional and community styles](../../cultural-adaptation/failures/regional-and-community-styles.md): the closest page. It tells the bot to mirror lightly, within a safe range, and to follow the user's own signals; one line says matching does not mean copying. That page is about which style to adopt; this one is about the bot handing the user's own sentences back.
- [One-size communication style](../../cultural-adaptation/failures/one-size-communication-style.md): one fixed voice for everyone. This page is the opposite miss: matching so literally that it copies.
- [Rapport absence](../../../../speech-and-audio/goals/conversation-flow/failures/rapport-absence.md): a voice bot with no warmth. Here the bot has plenty of "warmth" and it sounds like a script.
- [Fixing before listening](../../emotional-intelligence/failures/fixing-before-listening.md): the bot jumps to a fix. It suggests using the user's own word for a feeling; this page allows that once, as a single word that is not quoted (rule 5).
- [Filler and padding](../../response-structure/failures/filler-and-padding.md): lists a restatement that adds no fact as padding to delete. This page explains why that restatement can also sound like mockery.
- [Over-familiar address](../../persona-and-tone/failures/over-familiar-address.md): mirroring the wrong thing, such as "buddy". Here the mirrored thing is the user's sentences.
- Sibling rows in the [catalog](../../../roadmap/conversation-frameworks.md), not yet written: FW-M03 (echoing hostility), FW-M07 (no reflective listening) and FW-M08 (misused tactical empathy, including mechanical repetition of the last words). FW-M02 is about copying phrases in any tone.

## 9. Common questions
### Why does my chatbot repeat everything I say?
Most often the prompt asks it to show it understood by restating the user's message, and nothing limits how closely it copies. The copy is the easiest restatement to produce. See [why it happens](#3-why-it-happens) and rule 1.

### Is it bad for a chatbot to repeat back what the user said?
Repeating exact words is fine for facts the bot must confirm, such as an order number or a date. It becomes a problem when the bot quotes the user's sentences or feelings back as proof of listening. Restate by meaning and then act (rules 2 to 4).

### Does mirroring the user make a chatbot more trusted?
In people, light and unnoticed matching of manner can raise liking, and heavy or noticed copying can lower liking and trust (section 4). I found no opened study of word-for-word echoing by chatbots, so test it on your own transcripts.

### What should a chatbot say instead of repeating the user's words?
Name the problem in a few new words, then ask one question or give the next step: "A nightly outage is hard to live with. Do wired devices drop too?" See the improved transcript in [section 2](#2-what-it-looks-like).

### What if the user says "stop repeating me"?
Stop all restatements for the rest of the conversation, say so in one short clause, and answer the question. If it happens twice, offer a person (rule 9 and the hand-off rule).

### How is this different from matching the user's style?
Style matching adjusts length, formality, and vocabulary level. Over-mirroring copies the user's actual phrases. See [regional and community styles](../../cultural-adaptation/failures/regional-and-community-styles.md) for the style side.

---
## Technical section

### T1. Solution architecture
```
user message -> exact-fact extractor (names, numbers, dates, codes) -> allowlist
draft reply -> overlap check: longest run of shared words with the user message, outside the allowlist and function words
            -> opener check: first three words vs the previous bot reply
            -> reflection counter: restatements in this reply
rewrite if run >= 3, two reflections, repeated opener, or stop-cue seen earlier (restatements off for the session)
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No 3-word run copied from the user outside the allowlist | Pre-send overlap check | Tests 1 and 2; primary metric |
| Restatement only on complex or emotional turns | Pre-send reflection counter | Tests 3 and 4; counter-metric |
| No restatement after a stop cue | Session state | Test 7 |
| Same opener not used twice in a row | Pre-send opener check | Test 5 |

### T3. Evals
- **Dataset:** 100 user openings to start: 30 with a stated feeling, 30 with exact facts (order numbers, dates), 20 simple questions, 10 insults or sarcasm, 10 stop-copying cues.
- **Judge rubric:** does the reply change the user's wording; are exact facts copied exactly; is there a move forward; does a restatement appear only where it helps?
- **Metrics and starting thresholds:** the section 7 targets. They are starting points to tune.
- **Release gate:** block a deploy if the verbatim-repeat rate is over 5% on the dataset or any exact fact is copied wrong (starting points).

### T5. Trade-offs
- An overlap script is crude. It will miss a close paraphrase and flag a legitimate quote of a policy phrase. The judge sample covers both.
- A low copy limit can push the model to over-paraphrase and change meaning, which the exact-facts metric and the counter-metric watch for.

---
### Deep dive
- **Open question.** I found no study that tests exact echoing by a chatbot against rephrasing. The evidence here is human nonverbal mimicry and one abstract on rephrased replies.
- **Why "partly" for a better model.** A stronger model rewrites more naturally, but the prompt and the missing overlap check decide whether it copies. This is our judgment and has not been tested.
- **Modality notes (PLANNED):** *Voice:* read-backs of numbers are common and correct there, so the allowlist matters; echoing a caller's whole sentence sounds worse when spoken. Nothing about voice has been written or detected for this page.
- **References.** [Chartrand and Bargh 1999](https://pages.ucsd.edu/~pwinkiel/chameleon.pdf) (opened, abstract); [Wessler et al. 2024](https://link.springer.com/article/10.1007/s10919-023-00446-5) (opened); [APS release on Winkielman et al.](https://www.psychologicalscience.org/news/releases/when-its-an-error-to-mirror.html) (opened); [Dieter et al. 2019](https://aclanthology.org/K19-1037/) (abstract opened); [Siemens, Acknowledging users](https://ix.siemens.io/docs/guidelines/conversational-design/designing-conversations/acknowledging-users.md) (opened).
