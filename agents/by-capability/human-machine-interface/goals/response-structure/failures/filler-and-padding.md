# Chatbot Filler Phrases: Great Question Openers, Restated Questions and Closing Recaps

<!-- SEO
title: Chatbot Filler Phrases: Remove "Great Question" Openers
description: Why chatbots open with "Great question!", restate your question, and end with a recap, and rules plus a prompt block to cut filler from AI replies.
search phrases:
- chatbot filler phrases
- remove great question from AI responses
- how to stop chatbot saying great question
- chatbot restates my question before answering
- stop AI from repeating my question back
- chatbot closing summary recap unnecessary
- how to make chatbot responses concise no fluff
- reduce tokens before the answer in LLM response
-->

**Frequency**: Very Common

## Issue: The assistant wraps the answer in sentences that carry no information: a compliment, a restatement of the question, and a closing recap of what it just said.

> **One line:** Every sentence before and after the answer that the user could delete without losing anything is filler, and the fix is to delete it before sending.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice is a different case: spoken filler cannot be skipped (see [verbosity despite brevity instructions](../../../../speech-and-audio/goals/conversation-flow/failures/verbosity-despite-brevity-instructions.md)). Voice signals here are PLANNED, not detected. |
| **Stakes** | Low in a single reply. Medium when filler pushes a deadline, fee, or safety step down the screen, or when the opener is flattery that sets up agreement (see sycophancy below). |
| **Who is affected** | Everyone, most of all people on a phone, and teams paying for output tokens |
| **Frequency** | Very common as a style default. I found no study that counts filler openers across chat products. The sources below show the behavior exists and is measurable. |
| **Pattern ID** | filler-and-padding |
| **Family** | [Response structure and closers](../README.md) |
| **Goal** | Every sentence earns its place. (Family goal: replies are shaped so people can read, act on, and answer them, and short messages like "ok" and "bye" get the response the moment calls for.) |
| **Primary metric** | Filler-phrase rate: share of replies with a filler opener, a restatement of the question, or a closing recap (rule or judge check). Starting target: under 5% (tune). Paired with tokens before the answer. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A model can be told to skip filler, and a prompt rule works for most of it, but the habit comes from training and returns when the prompt changes. Cause owner: the model's default style. (Our judgment, not tested.) |
| **Also searched as** | chatbot fluff · AI says great question every time · bot repeats my question · chatbot recap at the end · remove preamble from LLM output · chatbot too wordy |

## 1. In plain words
The answer is fine, but it arrives inside a wrapper. The bot praises the question, says the question back, answers, and then summarizes the answer it just gave. The user reads two or three sentences before the useful one and one more after it.

## 2. What it looks like

**Without the fix**
```
User: How do I reset my router?
Bot:  Great question! Resetting a router is a common task. You asked how to reset your router, so let me walk you through it.
      Hold the small reset button on the back for 10 seconds until the lights blink. Then wait two minutes.
      In summary, to reset your router, hold the reset button for 10 seconds and wait two minutes.
      I hope this helps! Let me know if you have any other questions.
```

**With the fix**
```
User: How do I reset my router?
Bot:  Hold the small reset button on the back for 10 seconds, until the lights blink. Then wait two minutes.
      A reset erases your Wi-Fi name and password. Do you want the steps to set those up again?
```
Same answer. The opener, the restatement, the recap and the sign-off are gone, and the one fact the user could miss (the reset erases their Wi-Fi settings) moved into the space they freed.

## 3. Why it happens
These are our reading of the pattern, with the sourced part marked.
- **Length and warmth get rewarded in training.** The YapBench paper says preference-based training and LLM-judged evaluation can reward longer answers even when quality is the same. A tuned-warm default also produces an opening compliment.
- **Nothing in the prompt says what to leave out.** "Be helpful and thorough" with no rule on openers or recaps produces both. A restatement can look like proof the model understood.
- **The closer is a habit from long-form writing.** Essays end with a summary and a sign-off; the model carries that shape into a two-line answer.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A benchmark of 304 English prompts where a brief reply is ideal found an order-of-magnitude spread in median excess length across 76 assistant models. The paper names a restated request, generic caveats, and boilerplate preambles as extra content, and gives a "Great question!" opener as an example of a boilerplate preamble. | [Borisov et al., *Do Chatbot LLMs Talk Too Much? The YapBench Benchmark*, arXiv 2601.00624](https://arxiv.org/abs/2601.00624). Abstract and full text (HTML) opened and read. | A preprint. It measures excess length on short-answer prompts, not whether users were hurt. The text I read gives the model count inconsistently in places (76 in the abstract and leaderboard); I use the abstract's figure. |
| Nielsen Norman Group found 79% of test users always scanned a new page and 16% read word by word. In its test, a version written with about half the word count scored 58% better on measured usability. | [Nielsen, *How Users Read on the Web*, NN/g, 1997](https://www.nngroup.com/articles/how-users-read-on-the-web/). Opened and read. | A 1997 study of web pages, not chat. The link to chat replies is our inference. |
| OpenAI rolled back a GPT-4o update in late April 2025. TechCrunch reports OpenAI said the update was informed too much by short-term feedback and skewed toward responses that were overly supportive but disingenuous. | [TechCrunch, *OpenAI explains why ChatGPT became too sycophantic*, April 29, 2025](https://techcrunch.com/2025/04/29/openai-explains-why-chatgpt-became-too-sycophantic). Opened and read. OpenAI's own post returned an error (403) when I tried to open it, so I rely on TechCrunch's account. | An incident about sycophancy, not about filler. It shows that a warm, agreeable style can be reinforced by short-term approval. It does not show that "Great question!" openers caused harm. |

I did not find a chat study that tests whether removing openers, restatements or recaps changes task success, satisfaction or token cost. A search for system prompt wording that bans praise openers returned forum and blog posts; I could not open a primary source for the wording, so I do not quote any.

**Public incident.** No public incident found about filler specifically. The GPT-4o rollback above is the nearest dated case, and it is a sycophancy incident.

## 5. The fix

**The principle:** Delete any sentence the user could skip without losing information or a next step. The answer starts the reply and the reply ends when the content does.

**Do this**
1. **No praise opener.** The first sentence is not a compliment on the question, the user, or the idea ("Great question", "Good point", "Excellent").
2. **Do not restate the question.** Quote the user's words back only to confirm a detail that changes the answer ("You mean the 2024 plan?").
3. **No announcement of the answer.** Delete "Let me walk you through it", "Here is what I found", "I'd be happy to help".
4. **No closing recap on a short reply.** Do not summarize a reply that is under about 150 words (tune); the answer is already the summary. A long reply may end with one line that repeats the decision.
5. **No empty sign-off.** Delete "I hope this helps" and "Let me know if you have other questions". If there is a real next step, offer that one step instead.
6. **Acknowledge only when it carries meaning.** "Done, your order is canceled" is content. "Absolutely!" is not.
7. **The first sentence of the reply is the answer or the next step** (see [answer buried](answer-buried.md)).

**Reference design: filler checklist** (run on the draft before sending)
| Slot | Test | If it fails |
|---|---|---|
| Opener | Does sentence one answer or act? | Delete it |
| Restatement | Does it repeat the user's words without adding a fact? | Delete it |
| Middle | Does each sentence add a fact, condition or step? | Delete it |
| Closer | Is it a recap or a sign-off with no new step? | Delete it, or replace with the one real next step |

```
Start with the answer or the next step. Do not open with praise, a greeting, or a restatement of the question.
Do not announce what you are about to do. Do not summarize a short reply, and do not end with a sign-off.
Add a closing line only if it is a real next step. Keep warmth in the wording of the answer, not in extra sentences.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every clear question: sentence one is the answer or the next step, with no opener and no restatement in front of it. |
| Ask one clarifying question | The message is minimal or ambiguous ("help", "it's not working"): ask the one question instead of filling the space with general advice. Do not ask when the answer is the same either way. |
| Offer choices: 2-4 options plus "Something else", free text open | In place of a recap or sign-off, when there is a real next step: "Set up Wi-Fi again", "Show the full steps", "Something else". Do not add them to a one-line reply with one obvious next step. |

**Don't over-correct.** Do not make replies curt or cold. A short human touch is not filler when the user is upset, so keep one real acknowledgment for an emotional message (see [family patterns on emotion](../../emotional-intelligence/README.md)). Do not strip a needed caveat, safety line, or confirmation that an action finished. Do not drop the reply to "thanks" (see [no reply to acknowledgments and closers](no-reply-to-acknowledgments-and-closers.md)). A greeting at the start of a conversation is allowed once.

**Hand-off rule.** Filler does not need a handoff. If removing it exposes that the bot has no answer, say so in sentence one and route the user to a person ([escalates too early or too late](../../human-handoff/failures/escalates-too-early-or-too-late.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
No full test file exists yet for this pattern. Results: **not yet run**.

| # | Scenario | Rule | Pass if |
|---|---|---|---|
| 1 | "How do I reset my router?" | 1, 2, 3 | Sentence one is the instruction; no praise, no restatement |
| 2 | User asks a yes/no policy question | 2, 7 | Sentence one is yes or no plus the condition |
| 3 | A 60-word answer | 4 | No closing recap |
| 4 | Any answer with no real next step | 5 | No "hope this helps" or "let me know" line |
| 5 | Ambiguous message: "it's not working" | 2 | One clarifying question, no generic advice block |
| 6 | Upset user: "my package is lost again" | 6 | One real acknowledgment; no praise opener |
| 7 | Completed action (cancellation) | 6 | Confirmation of the action stays |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Filler-phrase rate** (primary) | Under 5% | Phrase list for openers, sign-offs and announcements, plus a judge check for restatement and recap on a labeled sample | Over 10% |
| Tokens before the answer | Set from baseline; track the median | Count tokens before the first sentence tagged as the answer or next step | Rising two weeks in a row |
| Replies opening with praise | Under 2% | Match the first sentence against a praise-opener list | Over 5% |
| Replies under 150 words ending in a recap | Under 5% | Judge check on a labeled sample | Over 10% |
| Needed caveats or confirmations removed (counter-metric) | Under 2% | Labeled sample of replies where a caveat or action confirmation was required | Over 5% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. All are written for text chat; none is detected for voice.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| First sentence matches a praise or announcement list | Match on the first sentence of the reply | A user who asked for a warm tone, or an upset-user acknowledgment |
| First sentence repeats most of the user's words with no new fact | Token overlap between the user turn and sentence one | A confirmation of a detail that changes the answer |
| Last sentence summarizes an answer under 150 words | Judge check on the last sentence against the body | A long answer where one repeated decision line helps |
| Last sentence is a generic sign-off | Match on the final sentence | A real next step phrased politely |
| User cuts in with "just tell me" or "short answer" | Phrase match in the next user turn | A user who wants the long version |

**Starter rule:** Do not open with praise, restate the question, end with a recap, or sign off; if there is a real next step, offer that one step.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: filler-and-padding
runs: pre_send
reads: [draft_reply.text, user_turn.text, draft_reply.word_count]
trigger: a draft reply opens with praise or a restatement, or ends with a recap or sign-off with no new step
moves: [lead_with_answer, ask_clarifying_question, offer_choices]
choices: ["Do the next step", "Show the full details", "Something else"]
on_miss: rewrite
metric: filler-phrase rate
counter_metric: needed caveats or confirmations removed
status: proposed
```

## 8. Related patterns
- [Answer buried](answer-buried.md): the closest pattern. That page is about order: the answer sits below a preamble. This page is about the sentences that carry nothing, before and after the answer. A reply can open with the answer and still end with a recap, or be filler-free and bury the answer in a long middle.
- [Verbosity despite brevity instructions](../../../../speech-and-audio/goals/conversation-flow/failures/verbosity-despite-brevity-instructions.md): over-long replies, where the model ignores a length instruction. Filler is one cause of long replies, but a long reply made only of useful sentences is not filler, and a short reply can still open with "Great question!".
- [Sycophancy](../../../../../cross-cutting/accuracy/goals/reasoning-quality/failures/sycophancy.md): the agent agrees with a wrong claim. A praise opener is the mild, stylistic cousin: it flatters but changes no answer. Sycophancy is judged by whether the content gives way; filler by whether the sentence adds anything. Flattery openers can come from the same training pressure, which is why the two often show up together.
- [No reply to acknowledgments and closers](no-reply-to-acknowledgments-and-closers.md): the user's own "ok" and "thanks"; this page covers the bot's closing lines.

## 9. Common questions
### How do I stop a chatbot from saying "Great question!"?
Add a rule to the system prompt: no praise or greeting before the answer, and the first sentence must be the answer or the next step. Then check it with a first-sentence phrase match. See [the fix](#5-the-fix).

### Why does my AI restate my question before answering?
It is a trained habit that reads as proof of understanding. The YapBench paper lists prompt restatement as extra content. Tell the model to restate only when confirming a detail that changes the answer.

### Is a friendly tone the same as filler?
No. Warmth in the wording of the answer is fine. The target is sentences with no content: the compliment, the echo, the recap and the sign-off. For an upset user, one real acknowledgment is content.

### Should a chatbot end with a summary?
Not on a short reply. The answer is the summary. On a long reply, one closing line that repeats the decision can help, as long as it is not a second copy of the whole reply.

### Is this the same as a chatbot giving a long answer?
No. [Answer buried](answer-buried.md) covers order, and the verbosity page above covers total length. This page is about sentences that add nothing, whatever the length.

---
## Technical section

### T1. Solution architecture
```
draft reply -> filler check (first-sentence praise/announcement match, overlap with user turn,
                             last-sentence recap/sign-off match, word count)
            -> pass: send
            -> fail: regenerate with the rule, or strip the flagged sentence if the rest still reads correctly
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No praise or announcement as sentence one | Prompt plus output filter | Phrase match in logs |
| No restatement without a new fact | Judge check | Labeled sample |
| No recap or sign-off on short replies | Output filter | Word count plus last-sentence match |
| Required caveats and action confirmations are kept | Rewrite step | Compare caveat tags before and after |

### T3. Evals
- **Dataset:** 150 real replies from logs, spread across short factual, how-to, ambiguous, and upset-user turns, plus 30 where a caveat or confirmation is required.
- **Judge rubric:** does sentence one answer or act, does any sentence repeat without adding, does the closer add a step, and was a required caveat kept?
- **Metrics and starting thresholds:** filler-phrase rate under 5%; needed caveats removed under 2%. Starting points to tune.
- **Release gate:** block a prompt or model change if the filler-phrase rate rises or tokens before the answer grow on the eval set.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Filler-phrase rate | Over 8% | Over 15% | Check recent prompt or model changes |

### T5. Trade-offs
- A strict filter can cut a useful acknowledgment; keep the upset-user exception and test it.
- Regenerating costs latency and tokens; stripping one sentence is cheaper but can leave a broken flow.
- Phrase lists drift as models change their habits; refresh them from your own logs.

---
### Deep dive
- **Open questions.** I found no chat study of whether filler changes completion, satisfaction or cost, and no primary source for system prompt wording that bans praise openers.
- **References.** [Borisov et al., YapBench, arXiv 2601.00624](https://arxiv.org/abs/2601.00624) (opened); [Nielsen, NN/g, 1997](https://www.nngroup.com/articles/how-users-read-on-the-web/) (opened); [TechCrunch, April 29, 2025](https://techcrunch.com/2025/04/29/openai-explains-why-chatgpt-became-too-sycophantic) (opened). OpenAI's post "Expanding on sycophancy" could not be opened (403).
