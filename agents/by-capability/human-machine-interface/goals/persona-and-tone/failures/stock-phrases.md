# Chatbot Stock Phrases: "I'd Be Happy to Help" and "As an AI" Openers on Every Reply

<!-- SEO
title: Chatbot Stock Phrases: Stop "I'd Be Happy to Help" Openers
description: Why chatbots open every reply with "I'd be happy to help!" or "As an AI...", and rules, a prompt block and metrics to vary and trim stock openers.
search phrases:
- chatbot says "I'd be happy to help" every time
- stop chatgpt saying "as an AI language model"
- how to stop chatbot repeating the same opening phrase
- chatbot sounds robotic same phrases every reply
- AI assistant canned phrases
- remove "certainly" and "absolutely" from chatbot replies
- chatbot opener list to ban in system prompt
-->

**Frequency**: Very Common

## Issue: The assistant opens reply after reply with the same canned line, such as "I'd be happy to help!" or "As an AI...", so the user reads a sentence that says nothing before the answer, and reads the same one again next turn.

> **One line:** The same stock opener sits in front of every answer; the fix is to start with the answer, and to use any acknowledgment or "I'm an AI" statement only when it tells the user something new.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice and web-widget signals are PLANNED, not detected. |
| **Stakes** | Low in one reply. Medium when the opener is "As an AI, I can't..." in front of a refusal, or when a cheerful line sits in front of bad news (see [stakes-blind register](../../stakes-calibration/failures/stakes-blind-register.md)). |
| **Who is affected** | Anyone in a multi-turn chat, because the repetition shows by the third reply |
| **Frequency** | Very common as a style default. I found no study that counts how often products open with a given phrase. |
| **Pattern ID** | stock-phrases |
| **Family** | [Persona and tone](../README.md) |
| **Goal** | The agent keeps one fitting character: on-brand, respectful, and never talking down or trying too hard. |
| **Primary metric** | Share of replies that open with a stock phrase (phrase-list match on sentence one). Starting target: under 5% (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A prompt rule removes most of it, and one vendor's published prompt shows a ban on praise openers, but the habit returns when the prompt or model changes. (Our judgment, not tested.) |
| **Also searched as** | chatbot robotic phrases · AI canned responses · chatbot repeats itself · "as an AI" disclaimer · chatbot sounds scripted · same greeting every message |

## 1. In plain words
Open a long chat and read only the first sentence of each reply. If they all start "Certainly!", "Absolutely!" or "I'd be happy to help with that!", the bot sounds like a script. Each opener is a small thing; the repetition is what the user notices. "As an AI..." is the same habit in a different costume: a statement about the bot, put in front of an answer that did not need it.

## 2. What it looks like

**Without the fix**
```
User: What's the return window on the Hartley standing desk?
Bot:  I'd be happy to help with that! The return window is 30 days from delivery.
User: Does that include the shipping fee?
Bot:  Certainly! I'd be happy to clarify. The original shipping fee is refunded only if the item arrived damaged.
User: Can I do the return at a UPS Store?
Bot:  Absolutely! As an AI, I don't have access to your location, but I'd be happy to help. Yes, UPS Stores accept it.
```

**With the fix**
```
User: What's the return window on the Hartley standing desk?
Bot:  30 days from delivery.
User: Does that include the shipping fee?
Bot:  Only if it arrived damaged; otherwise the original shipping fee isn't refunded.
User: Can I do the return at a UPS Store?
Bot:  Yes. Print the prepaid label from your order page and drop the box at any UPS Store.
```
Same facts. Three openers and a self-reference are gone, and each reply starts with its answer. The words "I'm an AI" appear nowhere because nothing in this exchange needed them.

## 3. Why it happens
These are our reading of the pattern, with the sourced part marked.
- **Training makes a polite default.** Models are tuned to sound helpful and warm, and "I'd be happy to help" is the shortest way to sound it. One benchmark paper (YapBench) says preference-based training can reward longer answers without better quality; that is the nearest sourced cause, and it covers length, not these exact phrases.
- **Disclosure phrases are a safety habit.** "As an AI..." began as a way to stay honest about what the model is and cannot do. It gets attached to answers where no limit was in play.
- **Nothing in the prompt names the phrases.** "Be friendly and helpful" invites the openers. A rule that bans a named list is checkable; a mood word is not.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A benchmark paper names "Great question!" and "As an AI language model" as examples of boilerplate preambles and counts them as avoidable verbosity; a sample reply to "Who discovered penicillin?" opens with "That's an excellent question!". | [Borisov et al., *Do Chatbot LLMs Talk Too Much? The YapBench Benchmark*, arXiv 2601.00624](https://arxiv.org/abs/2601.00624). Abstract and full text (HTML, sections 1 and C.2) opened and read. | A preprint. It measures excess length, not user reaction. The abstract itself does not mention preambles; the examples are in the body text. |
| Anthropic's published system prompt for Claude Sonnet 4 (May 22, July 31 and August 5, 2025 entries) states that Claude never starts a response by calling a question, idea or observation good, great, fascinating, profound, excellent or any other positive adjective, and "skips the flattery and responds directly". | [Anthropic, *Claude Sonnet 4 system prompts*](https://platform.claude.com/docs/en/release-notes/system-prompts/claude-sonnet-4). Opened and read. | Vendor document. It shows one vendor wrote a rule against praise openers; it does not show the rule's effect, and it does not mention "I'd be happy to help" or "As an AI". |
| A practitioner blog lists "As an AI language model..." among "obvious ChatGPT phrases" that suggest a text was AI-written, and says such phrases do not prove it. | [Dan Li, *The most overused ChatGPT words*, PlusAI, Dec. 15, 2025](https://plusai.com/blog/the-most-overused-chatgpt-words). Opened and read. | Practitioner blog, about text people paste into documents, not about chat openers. It shows the phrase is widely seen as a tell. |

I found no study that tests whether removing stock openers changes satisfaction, task success or trust. A search for complaints about "I'd be happy to help" returned forum posts and articles on other repetitive phrases; I did not open any as evidence, so none is used.

**Public incident.** No public incident found for stock phrases as such. I ran three searches (queries listed in the run report); results were forum complaints and style guides, not a dated, sourced event.

## 5. The fix

**The principle:** Sentence one is the answer or the next step. A stock opener, or a statement that the bot is an AI, appears only when it adds a fact the user needs.

**Do this**
1. **Keep a banned-opener list and check sentence one against it.** Start with: "I'd be happy to help", "Certainly", "Absolutely", "Sure thing", "Of course", "Great question", "As an AI".
2. **Start with the answer or the next step.** If the reply is a yes or a number, say that first.
3. **Say "As an AI" only when the user needs the fact.** Allowed: the user asks what the bot is, or the bot is about to state a real limit ("I can't see your account from here"). State the limit, not the label.
4. **Confirm by doing.** "Done, I canceled order 4417" is an acknowledgment that carries information. "Absolutely!" is not.
5. **Never use the same opening words on two replies in a row.** If the first three words match the previous reply, rewrite.
6. **Allow one greeting at the start of a conversation.** Keep it to a line, then answer.
7. **Use the brand's own phrase list only if it is varied.** If the brand mandates a line, keep the line but do not repeat it on every turn (see Hand-off rule).

**Reference design: opener check** (run on the draft before sending)
| Slot | Test | If it fails |
|---|---|---|
| Sentence one | Does it match the banned list? | Delete it, or rewrite to start with the answer |
| AI statement | Is it about a limit that matters to this request? | Replace "As an AI" with the plain limit, or delete |
| Repeat | Do the first three words match the last reply? | Rewrite the opener |
| Acknowledgment | Does it say what was done? | Keep it if yes; delete it if it only agrees |

```
Start every reply with the answer or the next step. Do not begin with "I'd be happy to help", "Certainly", "Absolutely", "Of course", "Great question" or "As an AI".
Mention that you are an AI only if the user asks, or if a limit of yours changes what they should do; then state the limit in plain words.
Do not start two replies in a row with the same words. Confirm an action by saying what was done.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every clear request: the stock opener is replaced by the answer or the next step. |
| Admit uncertainty and show how to check | The bot has a real limit that changes the answer: state the limit and one way to check ("I can't see your order status here; the order page shows it"), instead of "As an AI, I can't...". Do not use it when the bot can answer. |
| Ask one clarifying question | The message is minimal ("help"): ask the one question ("What do you need help with: an order, a return, or something else?") instead of "I'd be happy to help!". Do not ask when the request is already clear. |

**Don't over-correct.** Do not strip warmth. A first message from an upset user can get one real acknowledgment ("Sorry, a damaged desk is a bad start. Let's fix it."), which is content. Do not hide that the user is talking to an AI when they ask, or when a rule or law requires disclosure; this page governs unprompted labels, not honest answers to "Am I talking to a person?". Do not swap one fixed opener for another ("Got it!" on every turn is the same failure).

**Hand-off rule.** Stock phrases do not need a person. If removing the opener exposes that the bot has no answer, say so in sentence one and route the user to a person ([escalates too early or too late](../../human-handoff/failures/escalates-too-early-or-too-late.md)). If a brand mandates a scripted line, take that to the owner of the script, not the model.

**Framework used:** none yet.

## 6. How to test it (short version)
No full test file exists yet for this pattern. Results: **Not yet run**.

| # | Scenario | Rule | Pass if |
|---|---|---|---|
| 1 | "What's the return window?" | 1, 2 | Sentence one is the answer; no listed opener |
| 2 | A five-turn chat of factual questions | 5 | No two consecutive replies share their first three words |
| 3 | "Can you see my account?" (bot cannot) | 3 | States the limit in plain words; no "As an AI" |
| 4 | "Am I talking to a real person?" | 3 | Says it is an AI plainly |
| 5 | User cancels an order | 4 | Names what was done; no "Absolutely!" |
| 6 | First message: "hi" | 6 | One short greeting, then one question |
| 7 | Upset user: "my desk arrived cracked" | 4 | One real acknowledgment; no "I'd be happy to help" |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Share of replies that open with a stock phrase** (primary) | Under 5% | Match sentence one against the banned-opener list; refresh the list from your own logs | Over 10% |
| Consecutive replies with the same first three words | Under 3% of reply pairs | Compare first three words of each reply with the previous reply in the same session | Over 8% |
| Unprompted "As an AI" statements | Under 1% of replies | Phrase match on "as an AI" and "as a language model" where the user did not ask what the bot is | Over 3% |
| Honest AI-status answers when asked (counter-metric) | 100% | Labeled sample of "are you a person?" turns; the reply must say it is an AI | Any miss |
| Needed limits or confirmations removed (counter-metric) | Under 2% | Labeled sample of replies where a limit or action confirmation was required | Over 5% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. All are written for text chat; none is detected for voice or web widgets (PLANNED).
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| First sentence matches the banned-opener list | Phrase match on sentence one of the reply | A user who asked for a warm or formal style, or a mandated first-turn greeting |
| First three words equal those of the previous reply | Reply-pair comparison within a session | A numbered list, where each item starts alike |
| "As an AI" appears where no limit follows | Phrase match plus a check for a stated limit in the same sentence | The user asked what the bot is |
| User cuts in with "just answer" or "stop saying that" | Phrase match in the next user turn | A user asking for a shorter reply on a different point |

**Starter rule:** the first sentence of a reply is the answer or the next step, not a stock opener or an unprompted "As an AI".

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: stock-phrases
runs: pre_send
reads: [draft_reply.text, previous_reply.text, user_turn.text]
trigger: sentence one of a draft reply matches the banned-opener list, or repeats the first three words of the previous reply
moves: [lead_with_answer, admit_uncertainty, ask_clarifying_question]
choices: none
on_miss: rewrite
metric: share of replies that open with a stock phrase
counter_metric: honest AI-status answers when asked
status: proposed
```

## 8. Related patterns
- [Filler and padding](../../response-structure/failures/filler-and-padding.md): the closest pattern. That page covers sentences with no content before and after the answer: praise, restatement, recap, sign-off, in any reply. This page is narrower and about repetition and self-reference: the same stock line, and the "As an AI" label, appearing reply after reply. A reply can have no filler and still open "Certainly:" with the answer next; a filler-heavy reply can use a different opener each time.
- [Answer buried](../../response-structure/failures/answer-buried.md): about the position of the answer. A stock opener is one way to bury it, but a buried answer can be buried by content.
- [Stakes-blind register](../../stakes-calibration/failures/stakes-blind-register.md): a cheerful tone in the wrong situation. A stock "I'd be happy to help!" in front of bad news is the same mismatch, but this page is about the phrase repeating on every reply, not its fit to the moment.
- [Refusal with no reason or next step](../../refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md): "As an AI, I can't..." often opens a refusal; that page covers what a refusal must contain.
- [Condescending or patronizing tone](condescending-or-patronizing-tone.md): talking down to the user. A stock opener that praises a plain question is one way to sound patronizing.
- [Sycophancy](../../../../../cross-cutting/accuracy/goals/reasoning-quality/failures/sycophancy.md): agreeing with a wrong claim. A praise opener is the stylistic cousin; this page does not judge whether content gives way.

## 9. Common questions
### How do I stop ChatGPT from saying "I'd be happy to help"?
Name the phrases in the system prompt and require the first sentence to be the answer. Check it with a phrase match on sentence one. See [the fix](#5-the-fix).

### Why does my chatbot say "As an AI language model" so often?
It is a trained habit, likely from safety-minded disclosure. I found no source that explains the cause. Tell the bot to state the actual limit instead and to mention what it is only when asked.

### Is a friendly greeting a stock phrase?
One short greeting at the start of a conversation is fine. The failure is the same line on every reply, or a greeting that stands in for the answer.

### Should a chatbot hide that it is an AI?
No. This page is about the unprompted label. When a user asks, or when a rule or law requires disclosure, answer plainly; I have not checked any specific law, so check yours.

### Is this the same as filler?
Close, but no. [Filler and padding](../../response-structure/failures/filler-and-padding.md) is about content-free sentences of any kind. This page is about the same canned line recurring, and the "As an AI" label.

---
## Technical section

### T1. Solution architecture
```
draft reply -> opener check (banned-list match on sentence one, first-three-words match vs previous reply,
                             "as an AI" match with limit check)
            -> pass: send
            -> fail: regenerate with the opener rule, or drop the opener sentence if the rest still reads correctly
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No banned opener as sentence one | Prompt plus output filter | Phrase match in logs |
| No repeated first three words on consecutive replies | Output filter with session memory | Reply-pair comparison |
| "As an AI" only with a stated limit or when asked | Output filter | Phrase match plus labeled sample |
| Honest answer to "are you an AI?" | Prompt, never filtered out | Test 4 |

### T3. Evals
- **Dataset:** 150 real replies from logs, including first turns, factual follow-ups, refusals, completed actions and upset users, plus 20 "are you a person?" turns.
- **Judge rubric:** does sentence one answer or act, does it match the banned list, is any AI statement tied to a limit, and was the AI-status question answered honestly?
- **Metrics and starting thresholds:** stock-opener rate under 5%; honest AI-status answers 100%. Starting points to tune.
- **Release gate:** block a prompt or model change if the stock-opener rate rises on the eval set or any AI-status answer fails.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Stock-opener rate | Over 8% | Over 15% | Check recent prompt or model changes |

### T5. Trade-offs
- A fixed banned list gets gamed: the model swaps "Certainly" for "Sure thing". Keep the list from your own logs and keep the repetition check.
- Regenerating costs latency and tokens; dropping the opener sentence is cheaper but can leave a clipped reply.
- A brand may want a signature line. Allow it once per conversation, not once per reply.

---
### Deep dive
- **Open questions.** I found no chat study of whether stock openers change satisfaction, completion or trust, and no source that measures how often products use them. The evidence above shows the phrases are named as boilerplate in a benchmark paper and addressed in one vendor's prompt.
- **Not opened.** Search summaries mentioned secondhand reporting on Anthropic's Claude 4 prompts; I read Anthropic's own page instead and use no secondhand claim.
- **Voice and web widgets.** PLANNED. In voice, a spoken stock opener cannot be skipped, so the cost is higher; see the verbosity page linked from [filler and padding](../../response-structure/failures/filler-and-padding.md).
- **References.** [Borisov et al., YapBench, arXiv 2601.00624](https://arxiv.org/abs/2601.00624) (opened); [Anthropic, Claude Sonnet 4 system prompts](https://platform.claude.com/docs/en/release-notes/system-prompts/claude-sonnet-4) (opened); [PlusAI, Dec. 2025](https://plusai.com/blog/the-most-overused-chatgpt-words) (opened).
