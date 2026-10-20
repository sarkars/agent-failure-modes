# Chatbot Doesn't Restate Your Request: No Reflective Listening

<!-- SEO
title: Chatbot Doesn't Restate Your Request: How to Fix It
description: Why a chatbot acts on a complex request without restating it, and how to paraphrase it so users can correct a misread, without over-confirming.
search phrases:
- chatbot doesn't understand what I'm asking
- chatbot ignores part of my request
- chatbot answers the wrong question
- how to make a chatbot confirm it understood
- chatbot paraphrase user request
- reflective listening chatbot
- active listening for AI assistants
- when should a chatbot restate what the user said
-->

**Frequency**: Common

## Issue: On a long, many-part, or emotional request, the bot starts acting without restating what it understood, so a misreading is only discovered after the wrong answer or action.

> **One line:** The user gives a request with several parts, the bot silently picks its own version and acts on it; the fix is to restate the request in one or two sentences the user can correct, but only when the request is complex or ambiguous.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice and visual are PLANNED, not written. |
| **Stakes** | Low for a wrong answer to read; medium to high when the misreading triggers a cancellation, a charge, or advice on money, health, or a contract. |
| **Who is affected** | Users who write more than one constraint, a negation, or a feeling in a single message, and anyone whose request has two plausible meanings |
| **Frequency** | Common. This is our judgment from how assistants are built to answer first; I found no study that counts how often live bots skip a restatement. |
| **Pattern ID** | no-reflective-listening |
| **Family** | [Conversation frameworks](../README.md) (row FW-M07) |
| **Goal** | The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange. |
| **Primary metric** | Paraphrase present on complex requests. Start: over 80% (tune). Reported with user-correction acceptance. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A strong model can write a good paraphrase when told to (section 4), but deciding when a request is complex enough to need one depends on the product's risk, so it has to be a rule. (Our judgment, not tested.) |
| **Also searched as** | chatbot doesn't listen · bot ignored half my message · chatbot never confirms what I asked · AI assistant answered a different question · chatbot paraphrasing |

> **Read this first.** Reflective listening comes from human counseling and communication practice. I found no study that tests it on chatbot users, so treat the fix as a hypothesis to test on your own traffic. The one controlled study I opened (section 4) found that paraphrasing did not make people feel more understood. The case for this page is catching misreadings early, not building rapport.

## 1. In plain words
A person gives a long request: three conditions, a "don't do X," and a worry. A good listener says it back in a sentence: "So you want A and B, but not C. Right?" The bot skips that and answers its own version. If it read the request wrong, the user finds out only after a full wrong reply. The fix is to restate the request when it is complex or unclear, and to answer straight away when it is not.

## 2. What it looks like
Illustrative transcript (invented for this page, not from a real product). Summit Fiber is a made-up internet provider.

**Without the fix**
```
User: I'm moving from Denver to Austin on Nov 15, but my sister keeps the Denver apartment until
      January. I don't want to cancel anything, I just don't want to pay for two plans.
Bot:  To cancel your Summit Fiber service, go to Account > Plans > Cancel Service.
User: I said I don't want to cancel.
Bot:  Sorry about that! To move service, enter your new address under Account > Move Service.
User: That ends Denver. My sister still needs it until January.
Bot:  I understand. Cancellation steps are under Account > Plans.
User: (closes the chat)
```
**With the fix**
```
User: I'm moving from Denver to Austin on Nov 15, but my sister keeps the Denver apartment until
      January. I don't want to cancel anything, I just don't want to pay for two plans.
Bot:  So you want service at the new Austin address from Nov 15, you want Denver to keep running
      for your sister, and you don't want to pay for both. Is that right?
User: Close. She'll pay for Denver herself from Dec 1.
Bot:  Got it: Austin starts Nov 15, and the Denver account moves to your sister's name on Dec 1.
      Which should I start with: "Set up Austin", "Move Denver to my sister", or "Something else"?
```
The fixed bot restated three parts of the request, including the "don't cancel," got one correction from the user, and acted on the corrected version.

## 3. Why it happens
These are our reading of the pattern, not measured causes.
- **Models are built to answer.** The default is to produce a helpful reply to the last message. Restating first feels like a delay, so it only happens if a rule asks for it.
- **No rule says what counts as complex.** Without a test such as "several constraints, a negation, a feeling, or two readings," the bot either restates everything (annoying) or nothing.
- **Teams fear sounding robotic.** A restatement can read as scripted, so designers drop it. The real fix is a short, specific restatement used when it earns its place.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In an experiment with 180 undergraduates, a listener who paraphrased the speaker's message was rated more socially attractive than one who gave a simple acknowledgment. Paraphrasing did not change conversational satisfaction or the speaker's sense of being understood. | [Weger, Castle and Emmett, *International Journal of Listening* 24(1), 2010](https://stars.library.ucf.edu/scopus2010/1477). Opened; abstract page read, not the full paper. | Human peer conversation about exam policy, not a bot and not a service task. It argues against promising rapport from paraphrasing. It does not test error catching. |
| Motivational interviewing teaching material separates simple reflections (repeating or rephrasing, staying close to the original) from complex ones (paraphrasing that infers meaning, reflection of feeling, double-sided reflection, summarizing). It describes reflections as guesses: if the client balks, you have "jumped too far too fast," and stock openers such as "it sounds like" can sound like counselor speak if overused. | [UNC Center for AIDS Research, *Core Interviewing Skills in MI: Reflective Listening*](https://www.med.unc.edu/cfar/2025/11/core-interviewing-skills-in-mi-reflective-listening/). Opened; page read. | Training page for human counselors. It gives no outcome numbers and no rule for when to reflect. It supports the idea that a restatement is a guess the other person can correct. |
| IBM's Carbon design system says a chatbot should confirm its understanding of user input when appropriate, by paraphrasing. It also says to summarize complex input so the user can verify the bot's interpretation. | [Carbon Design System, *Chatbot: content*](https://v10.carbondesignsystem.com/community/patterns/chatbot/content). Opened; page read. | Design guidance, not an experiment. "When appropriate" is not defined. |
| Nuance's Mix guide lists when to confirm: the system probably, but not definitely, has the right meaning; an irreversible operation; or the application wants to assure the user it understood. It also warns that unnecessary confirmation can double the length of an interaction and frustrate users. | [Nuance Mix, *Requesting confirmation*](https://docs.nuance.com/mix/best-practices/dialog-planning/confirm/). Opened; page read. | Vendor guidance, no data on the page. Written for voice and chat dialogs. |
| A paper on automating MI reflections reports that GPT-4 with zero-shot prompting writes reflections at near-100% success, and fine-tuned GPT-2 models reach 83% and 90% on a hold-out test set. | [Brown et al., *Generation, Distillation and Evaluation of MI-Style Reflections*, EACL 2024 (arXiv 2402.01051)](https://arxiv.org/abs/2402.01051). Opened; abstract read, not the full paper. | Measures whether a model can generate a reflection, not whether users benefit. The chatbot is the motivation, not a user trial. |

I found no study that tests restatement or paraphrase with chatbot users, and none that measures how often users correct a bot's paraphrase. I did not search for dated incidents; none turned up in the searches I ran. **Public incident.** No public incident found.

## 5. The fix
**The principle:** When a request is complex or ambiguous, restate it in one or two sentences before acting, and make the restatement easy to correct. When it is simple and clear, just answer.

**Do this**
1. **Decide first: is the request complex?** Treat a request as complex if any of these is true (starting definition, tune it): it holds three or more separate constraints, it contains a negation or exception ("don't cancel," "except Fridays"), it mixes a feeling with a request, it could mean two different things with different results, or the action that follows is costly or hard to undo.
2. **If it is complex, restate before acting.** One or two sentences that say what the user wants and what they do not want, in your own words, ending with a short check such as "Is that right?"
3. **Restate in your own words, not theirs.** Do not echo their phrases back (that is a separate failure, over-mirroring, FW-M02). Keep the parts the answer depends on: amounts, dates, names, and every "don't."
4. **Keep it to what they said.** Do not add facts, motives, or feelings they did not state. If you name a feeling, offer it as a guess they can correct (labeling feelings badly is FW-M08).
5. **Make the correction cheap.** End with a yes/no check or "what did I miss?" and accept "close, but not quite" as an answer. Apply the correction in the next reply without repeating the whole restatement.
6. **When the request is simple, do not restate.** One clear ask, one reading, low cost: answer it. "Do you ship to Austin?" gets "Yes, usually in 3-5 business days," not "You are asking whether we ship to Austin."
7. **Restate once per request.** After a correction, use one line to show you applied it, then act. Do not restate the same request again unless the user adds a new part.
8. **If the request has two readings, offer them.** Name the readings as choices instead of picking one.
9. **If you can answer part of it safely, answer that part first.** Then restate the remaining parts.

**Reference design: the restate block (paste into the system prompt)**
```
Before acting on a user message, check whether it is complex: three or more constraints, a "don't" or
exception, a feeling plus a request, two possible readings, or a costly or hard-to-undo action.
If it is complex, write one or two sentences that restate what the user wants and does not want, in your
own words, and end with a short check ("Is that right?"). Do not act until they answer, unless part of the
request is safe to answer now.
If they correct you, apply it and say so in one line. Do not add facts or feelings they did not state.
If the message is simple and clear, answer it and do not restate it.
```
State to keep: `{ "complex": true, "paraphrase_made": true, "user_corrected": true, "correction_applied": true, "restates_this_request": 1 }`

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | A complex request: restate it, and end with one short check. If one part is unclear, ask only about that part. |
| Offer choices: 2-4 options plus "Something else", free text open | The restatement has two real readings: "Move my service", "Keep both addresses", "Something else". Do not offer them when the request has one clear reading or when the user just corrected you and the next step is obvious. |
| Lead with the answer | A simple, clear request, or the safe part of a complex one. Answer first and do not restate. |
| Hand off to a person | The user corrects the restatement twice in a row, or a misreading would be costly and the request still cannot be pinned down. Pass the summary. |

**Don't over-correct.** The opposite failure is restating everything, which turns every exchange into a quiz. That is [over-confirmation](../../dialogue-management/failures/over-confirmation.md). Do not restate a one-part request, a request the user just clarified, or a message that is only "thanks" or "ok." Do not restate in the same reply that already contains the answer to a simple question. The guardrail is the complexity test in rule 1: no complexity signal, no restatement. Also vary the wording: openers like "It sounds like" on every turn read as scripted (section 4, UNC row).

**Hand-off rule.** If two restatements in a row are corrected by the user, or the request involves a costly action and the bot still cannot state it back correctly, offer a person and pass the user's words, the bot's last restatement, and the corrections.

**Framework used:** none yet. Candidate: reflective listening from motivational interviewing practice (section 4), a human-counseling hypothesis. See the [conversation moves](../../../solutions-library/conversation-moves.md) page for the move wording.

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | The Summit Fiber move message (three parts and a "don't cancel") | The first reply restates all three parts, including "don't cancel," and ends with a check; no cancellation steps | 1, 2 |
| 2 | "Do you ship to Austin?" | Reply answers; no restatement | 6, Don't over-correct |
| 3 | User answers the restatement with "Close, but she pays from Dec 1" | Next reply applies the correction in one line and does not restate the full request again | 5, 7 |
| 4 | Restatement contains a fact the user never gave | Fails: sampled review flags an added fact | 4 |
| 5 | A request with two readings ("move my appointment" with two bookings) | Reply names the readings as choices plus "Something else" | 8 |
| 6 | User corrects two restatements in a row | Bot offers a person with a summary | Hand-off rule |
| 7 | User writes "ok thanks" after an answer | No restatement | Don't over-correct |
| 8 | A request with a safe, answerable part and an unclear part | Reply answers the safe part, then restates the rest | 9 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Paraphrase present on complex requests** (primary) | Start: over 80% | A request is complex if a rule check finds a complexity signal from rule 1. Divide complex requests whose first bot reply contains a restatement by all complex requests. Confirm the check on a sample judged by a person. | Below 65% |
| User-correction acceptance | Track; set from baseline | Of restatements the user corrected, the share where the next bot reply applies the correction, checked on a sampled review | Falling for two weeks |
| Paraphrase on simple requests (counter-metric) | Under 5% (tune) | Restatements in replies to requests with no complexity signal, found by rule check | Over 10% |
| Restatements that add a fact the user did not state | 0 | Sampled review of restatements | Any in a 20-chat sample |
| Same request restated twice | 0 | The same restatement within three bot turns | Any |
| Complex requests followed by "I said that" from the user | Trend down | Count user turns that repeat a stated constraint within two turns after a complex request | Up 20% vs baseline |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Complex request followed by a bot reply with instructions or an action and no restatement | `user_turn.complexity_flag` set and `bot_reply.has_restatement` false | The request was complex but the answer is safe and the user then confirmed it fits |
| User repeats a constraint they already gave, within two turns | Same constraint text in turn N and turn N+1 or N+2 | The user is adding emphasis or a new part |
| Bot reply contradicts a negation in the request ("don't cancel" then cancellation steps) | Negation phrase in the user turn; opposite action in the draft | The user changed their mind in a later turn |
| User opens the next turn with "no," "I said," or "that's not what I asked" | Opening words of the user turn after a bot answer | A "no" that answers a yes/no question the bot asked |

**Starter rule:** when a request has three or more constraints, a negation, a feeling plus a request, or two readings, restate it in one or two sentences and end with a check before acting; when it is simple, answer it without restating.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: no-reflective-listening
runs: pre_send
reads: [user_turn.complexity_flag, user_turn.has_negation, user_turn.reading_count, session.paraphrase_made, session.user_corrected, draft_reply.has_restatement, session.stakes]
trigger: a reply is about to be sent for a complex or ambiguous request and the draft does not restate it
moves: [ask_clarifying_question, offer_choices, lead_with_answer, hand_off]
choices: ["Move my service", "Keep both addresses", "Something else"]
on_miss: rewrite
metric: Paraphrase present on complex requests
counter_metric: paraphrase on simple requests
status: proposed
```

## 8. Related patterns
- [Guessing instead of asking](../../dialogue-management/failures/guessing-instead-of-asking.md): the closest page. It covers a bot that picks one reading of an ambiguous request and answers, when one short question would settle it. This page covers a complex request where the bot has many parts to get right and never says back what it understood; the restatement is the check, and it is needed even when the request is clear but long.
- [Over-confirmation](../../dialogue-management/failures/over-confirmation.md): the opposite failure. It asks "is that right?" on routine steps. This page's fix works only if the complexity test keeps restatements rare.
- [Fixing before listening](../../emotional-intelligence/failures/fixing-before-listening.md): a bot that skips the acknowledgment of a feeling and jumps to steps. This page covers restating the whole request, with or without feeling.
- [Hollow empathy](../../emotional-intelligence/failures/hollow-empathy.md): a stock warm phrase with no specifics. A restatement must be specific, which is the test that page applies.
- Over-mirroring (FW-M02), misused tactical empathy (FW-M08) and instructions without comprehension checks (FW-C09): sibling rows in the [conversation frameworks catalog](../../../roadmap/conversation-frameworks.md), not yet written. M02 is verbatim parroting, M08 is wrong emotion labels, and C09 is checking that the user understood the bot's instructions. This page is the bot checking that it understood the user.

## 9. Common questions
### Why does my chatbot answer the wrong question on long requests?
It usually picks the most likely reading of the last message and answers. A long request with several constraints and a "don't" gives it more ways to drop a part. A short restatement lets the user catch that early. See [the fix](#5-the-fix), rules 1 and 2.

### Should a chatbot always repeat back what I asked?
No. Restating every message doubles the exchange and reads as scripted. Restate only when the request is complex or ambiguous, or the action that follows is costly (section 4, Nuance row). A simple question gets an answer.

### How do I tell a complex request from a simple one?
Use a short rule: three or more constraints, a negation or exception, a feeling plus a request, two readings, or a costly action. These thresholds are starting points; tune them on your own transcripts.

### Does restating the request make users feel understood?
Not shown here. In the one experiment I opened, paraphrasing did not change how understood the speaker felt (section 4, Weger row). The reason to restate is to catch misreadings early. I found no chatbot study either way.

### How is this different from the bot asking a clarifying question?
A clarifying question asks for a missing fact. A restatement says what the bot thinks it heard and lets the user fix it. Use both: restate, then ask only about the part that is unclear. See [guessing instead of asking](../../dialogue-management/failures/guessing-instead-of-asking.md).

---
## Technical section

### T1. Solution architecture
```
user message -> complexity check (rules: constraint count, negation, mixed feeling, reading count, action cost)
  -> state: complex, paraphrase_made, user_corrected, restates_this_request
draft reply -> restate check: complex and no restatement? -> rewrite as restatement + one check
              simple and restatement present? -> rewrite to the answer alone
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Complex request with no restatement triggers a rewrite | Pre-send check | Tests 1 and 8 |
| Restatement on a simple request is removed | Pre-send check | Test 2; counter-metric |
| Restatement adds no fact the user did not state | Judge on a sample | Test 4 |
| Correction is applied without a second full restatement | State | Test 3 |

### T3. Evals
- **Dataset:** 100 user messages to start: 40 complex, 40 simple, 20 with two readings or a negation. Add the 8 scenarios above as fixed cases.
- **Judge rubric:** does the restatement cover every constraint and every "don't"; does it add nothing the user did not say; is it in the bot's own words; does it end with a way to correct?
- **Metrics and starting thresholds:** the table in section 7; these are starting points, not results.
- **Release gate:** block a deploy if restatements on simple requests or added facts exceed your target.

### T5. Trade-offs
- A complexity check will misjudge some messages. The counter-metric catches over-restating; the "I said that" metric catches under-restating.
- Each restatement adds a turn. Skip it where the cost of a misreading is low and the user can see the result.

---
### Deep dive
- **Open question.** No chatbot study of restatement was found. The human evidence is mixed (section 4), and the bot-side evidence shows only that models can write reflections.
- **Modality notes.** Voice: PLANNED. A spoken restatement costs more time than a typed one, so the complexity test would likely need to be stricter. Not written.
- **References.** [Weger et al., 2010](https://stars.library.ucf.edu/scopus2010/1477) (opened); [UNC, MI reflective listening](https://www.med.unc.edu/cfar/2025/11/core-interviewing-skills-in-mi-reflective-listening/) (opened); [Carbon, chatbot content](https://v10.carbondesignsystem.com/community/patterns/chatbot/content) (opened); [Nuance Mix, requesting confirmation](https://docs.nuance.com/mix/best-practices/dialog-planning/confirm/) (opened); [Brown et al., arXiv 2402.01051](https://arxiv.org/abs/2402.01051) (abstract opened).
