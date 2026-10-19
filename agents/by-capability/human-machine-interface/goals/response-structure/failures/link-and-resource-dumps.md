# Chatbot Just Sends Links Instead of Answering: Link and Resource Dumps

<!-- SEO
title: Chatbot Just Sends Links Instead of Answering: How to Fix It
description: Why a chatbot replies with a pile of links instead of an answer, what research says about it, and rules for answer-first replies with links as support.
search phrases:
- chatbot just sends links instead of answering
- chatbot gives me a list of articles instead of an answer
- ai assistant provides resources not answers
- chatbot redirects to faq instead of answering
- how to make a rag chatbot answer instead of listing links
- chatbot "here are some resources" reply
- support bot only links to help center articles
-->

**Frequency**: Common

## Issue: The assistant answers a question with a list of links or "resources" and leaves the user to open them and find the answer themselves.

> **One line:** The user asked a question and got a reading list; the bot should give the answer first and use links only as support.

| | |
|---|---|
| **Channel** | Written for **chat**, mostly support and search-style assistants. Voice is not covered; a spoken list of URLs does not work at all, and any voice signals would be PLANNED, not detected. |
| **Stakes** | Low to medium. It wastes time and sends people to other channels. It rises when the user is in a bind (a bill, a deadline) or the linked pages do not fit their case. |
| **Who is affected** | Everyone, most of all people who came to the bot because they could not find the answer in the help center |
| **Frequency** | Common in practice. I found no study that counts how often it happens. The sources below show that it is reported and that users dislike it. |
| **Pattern ID** | link-and-resource-dumps |
| **Family** | [Response structure and closers](../README.md) |
| **Goal** | Replies are shaped so people can read, act on, and answer them, and short messages like "ok" and "bye" get the response the moment calls for. (Family goal; for this pattern: answer first, with links as support.) |
| **Primary metric** | Share of replies that are mostly links, meaning a link-only or link-led reply with no answer in the first two sentences. Starting target: under 2% (tune). |
| **Maturity** | Researched (no test file yet) |
| **Will a better model fix this?** | Partly. A stronger model can read the pages and write the answer, but a prompt, a retrieval setup, or a deflection target that rewards "send the article" will still produce link piles. (Our judgment, not tested.) |
| **Also searched as** | bot just links me to the FAQ · "here are some resources" · chatbot resources not answers · help center deflection bot · RAG answer is just a list of sources |

## 1. In plain words
The user asks a question. The bot replies "Here are some resources that may help:" and lists three to five links. The answer might be on one of those pages, but the user has to open them, read them, and decide which applies. The fix is to read the page for them: state the answer, then link the source as proof or for more.

## 2. What it looks like

**Without the fix**
```
User: I was charged twice for my March invoice. Can I get one refunded?
Bot:  I found some resources that may help:
      - Billing and invoices overview
      - Refund policy
      - How to update your payment method
      - Contact support
User: Which one has the answer?
```

**With the fix**
```
User: I was charged twice for my March invoice. Can I get one refunded?
Bot:  Yes. A duplicate charge is refunded in full, usually in 5-7 business days. I can start it now.
      Which charge should I refund: the $49.00 on March 3 or the $49.00 on March 4?
      (Policy: Refund policy, "Duplicate charges")
```
The fixed reply puts the answer and the next step first, asks for the one fact it needs, and keeps a single link as the source.

## 3. Why it happens
- **Retrieval output becomes the reply.** In a help-center or RAG setup, the retrieved pages are easy to show. If the prompt does not say "read these and answer," the bot passes the list along. (Our reading.)
- **A deflection target counts a sent link as a win.** When the success metric is "conversation ended without a human," a link looks like resolution even if the user gave up. See [answer-and-go conversation](../../conversation-leadership/failures/answer-and-go-conversation.md), which names this metric problem.
- **Links feel safe.** The bot avoids stating a policy it might get wrong, so it points to the page instead. This is a reasonable instinct taken too far; the fix keeps the link and adds the answer. (Our reading.)

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a two-week diary study (18 participants, 425 logged conversations, May and June 2023), a Bing-specific complaint was "Bing provides resources, not answers": participants felt Bing did only the first part of information foraging by showing links instead of extracting the answer. | [NN/g, *Information Foraging with Generative AI: A Study of 3 Chatbots*, Sept 24, 2023](https://www.nngroup.com/articles/generative-ai-diary/). Opened and read. | General-purpose AI search chats, not a company's support bot. Small sample; the complaint is about one of the three tools. |
| In a usability study with 8 US participants, a user who refined "Belt" to "Women's belt" was asked to choose from links, "none of them matching what she was trying to find." The same article says links and buttons worked best when clearly signaled. | [NN/g, *The User Experience of Chatbots*, Nov 25, 2018](https://www.nngroup.com/articles/chatbots/). Opened and read. | Eight participants, 2018 chatbots, and the bot lacked the task rather than choosing links over an answer. It shows the cost of a link list, not the cause. |
| In a 2026 study (9 participants, 8 site chatbots), the article says bots should, where possible, answer directly "instead of sending them elsewhere," and that "A longer answer was not a better answer." In one example the bot told a user to check his own insurance, the host's policies, and the booking page; he found it vague and preferred a person. | [NN/g, *Less Chat, More Answer*, April 17, 2026](https://www.nngroup.com/articles/less-chat-more-answer/). Opened and read. | Nine participants. The article does not treat links as a standalone design question, and one participant said she prefers links in responses. |
| The CFPB (June 6, 2023) says some bots offer little beyond "directing customers to policies or FAQs," and warns that a chatbot that is "little more than a gateway into the company's public policies or FAQs" can leave customers without recourse. It quotes a complaint that the app "redirected me to their FAQ webpage," which did not address the customer's situation. | [CFPB, *Chatbots in consumer finance*, 2023](https://www.consumerfinance.gov/data-research/research-reports/chatbots-in-consumer-finance/chatbots-in-consumer-finance/). Opened and read. | A regulator's review of banking chatbots and complaints. Complaints are self-reported and not a count of how often this happens. See also the library's [CFPB incident page](../../../incidents/cfpb-bank-chatbot-doom-loops.md). |

**Public incident.** The CFPB report above is the closest dated public source; it covers FAQ redirects and loops, not a single named link-dump event. No public incident found for a company link pile specifically. I ran four searches (news, complaints, regulator material, UX research) and found studies and a regulator report, not a named incident.

I did not open the vendor surveys and blog posts that turned up in searches, and I use none of their numbers.

## 5. The fix

**The principle:** Read the page for the user. The first sentence answers the question or states the next step; links come after, as the source or for more.

**Do this**
1. **Answer in sentence one.** A reply to a clear question never opens with "Here are some resources" or a list of links.
2. **Never send a link-only reply** when the bot can retrieve the page. If it retrieved it, it states what the page says about the user's case.
3. **Cap links at one to three, and label each** with what the user will find ("Refund policy, section on duplicate charges"), not a bare title or URL.
4. **Name the one link that matters most** when several are shown ("The first one covers your case").
5. **When no retrieved page answers it, say so in sentence one** ("I couldn't find a policy for that") and offer a person or a clarifying question. Do not list near-misses to look helpful.
6. **When the question is unclear, ask one question** instead of returning a spread of links for each possible meaning.
7. **Keep links as support.** A link is added after the answer, not in place of it. Do not hide a must-know fact (deadline, fee) behind a link.

**Reference design: answer-first with links as support**
| Slot | Content |
|---|---|
| 1 | The answer or next step, in one sentence |
| 2 | The one condition or the one fact you need |
| 3 | One to three labeled links: "Source:", "Details:" |
| 4 (optional) | An offer of more or a person |

```
Read the retrieved pages and answer the user's question in your own words. Start with the answer or the next step.
Never reply with only links. Include at most three links, each labeled with what it covers, after the answer.
If the pages do not answer the question, say so in your first sentence and offer a person or one clarifying question.
Put deadlines, fees, and required steps in the reply text, not only behind a link.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Retrieved pages answer the question: sentence one is the answer or next step, with links after it as the source. |
| Ask one clarifying question | The pages could mean several things and one fact picks between them. Ask it instead of returning a link per meaning. |
| Admit uncertainty and show how to check | The pages are close but do not settle the user's case: say what is not clear, give the one best link, and say what to look for in it. |
| Offer choices: 2-4 options plus "Something else", free text open | A real fork remains after the answer, for example which charge to refund. Do not turn the link list into the menu. |
| Hand off to a person | No retrieved page answers it, or the user has asked "which one?" twice. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Do not drop links altogether: a source link lets the user check the answer, and some tasks (a form, a download) need one. Do not paste the whole page into the chat; give the part that applies. Do not state a policy the pages do not support just to avoid sending a link; when the pages are silent, say so.

**Hand-off rule.** If no retrieved page answers the question, or the user asks "which one?" or "so what do I do?" twice, move to a person ([escalates too early or too late](../../human-handoff/failures/escalates-too-early-or-too-late.md)). Pass along the question and the pages already tried.

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
No test file exists yet. The scenarios below are a design, not results; none has been run.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | A clear question whose answer is on one help-center page | Sentence one holds the answer; no link-only reply | 1, 2 |
| 2 | A question matching five articles | At most three links, each labeled | 3 |
| 3 | Five articles match and one covers the user's case | The reply names which link matters most and says why | 4 |
| 4 | A question the pages do not answer | Sentence one says so and offers a person or one question | 5 |
| 5 | An ambiguous question | One clarifying question, not a link per meaning | 6 |
| 6 | A deadline that appears only on the linked page | The deadline is in the reply text | 7 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Share of replies that are mostly links** (primary) | Under 2% | Count replies where the first two sentences hold no answer and the link count is 1 or more; confirm on a labeled sample | Over 5% |
| "Which one?" follow-ups | Under 1% of conversations | Next-turn phrase match ("which one", "which of these", "I don't see it") | Rising two weeks in a row |
| Link-only replies | 0% | Reply text minus links is under about 10 words | Any |
| Replies with more than three links | Under 5% | Count links per reply | Over 15% |
| Answer-first rate (counter-metric, shared with [answer buried](answer-buried.md)) | Over 90% | Labeled sample | Below 80% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. All are written for text chat.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply has links and no answer in the first two sentences | Turn-level link count plus a judge check on sentences 1-2 | A user who asked for a link or a document ("send me the form") |
| Reply opens with "Here are some resources" or "I found these articles" | Pattern match on the opener | A search-style product where a result list is the request |
| User replies "which one?" or "I don't see it" right after a reply with links | Same-intent or phrase match on the next user turn | A user comparing options on purpose |
| User asks the same question again within 3 turns after a link reply | Repeated intent in the next turns | A deliberate rephrase to add detail |
| User clicks no link, then asks for a person | Link click event, then a handoff request | A user who read the reply and decided the case needs a person |

**Starter rule:** no reply to a clear question is only links; the first sentence holds the answer or next step, and links follow as support.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: link-and-resource-dumps
runs: pre_send
reads: [draft_reply.first_two_sentences, draft_reply.link_count, retrieved_pages, user_turn.intent]
trigger: a reply with links is about to be sent
moves: [lead_with_answer, ask_clarifying_question, admit_uncertainty, offer_choices, hand_off]
choices: ["Start the next step", "Show the full policy", "Talk to a person", "Something else"]
on_miss: rewrite
metric: share of replies that are mostly links
counter_metric: answer-first rate
status: proposed
```

## 8. Related patterns
- [Answer buried](answer-buried.md): the answer is in the reply but sits below a preamble. Here the answer is not in the reply at all; the user is sent elsewhere to find it. Both fixes lead with the answer.
- [Chatbot tells you to do it yourself](../../effort-and-memory/failures/deferring-work-to-the-user.md): the bot has a tool or the data and explains how the user could do it. A link pile is the same effort-shifting, with pages in place of instructions.
- [Answer-and-go conversation](../../conversation-leadership/failures/answer-and-go-conversation.md): names the deflection and containment metric that rewards ending the chat, a common cause of this pattern.
- [Dead-end "I don't understand" replies](../../conversation-leadership/failures/dead-end-i-don-t-understand-replies.md): a fallback that offers no path; a link list can be one.
- [Talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md): where users end up after repeated link replies.
- [Missing citations](../../../../knowledge-retrieval/goals/citation-accuracy/failures/missing-citations.md): the opposite RAG fault, an answer with no source. This page's fix keeps the source link and adds the answer.
- [Over-retrieval](../../../../knowledge-retrieval/goals/retrieval-quality/failures/over-retrieval.md): too many documents retrieved. A bot that passes them all through becomes a link dump, but the retrieval fault sits upstream.

## 9. Common questions
### Why does my chatbot just send links instead of answering?
Usually the retrieved pages become the reply, or the bot is tuned to deflect and a link counts as done. Both are fixable with an instruction to read the pages and answer, plus a metric that counts resolution, not conversations ended. See [why it happens](#3-why-it-happens).

### Is it wrong for a RAG chatbot to show links?
No. Sources let users check the answer, and the NN/g study notes links work when clearly signaled. The failure is when the links replace the answer. Put the answer first and one to three labeled links after it.

### How is this different from a buried answer?
In [answer buried](answer-buried.md) the answer is in the reply, below a preamble. In a link dump it is not in the reply; the user is sent to find it.

### What should the bot say when the help center has no answer?
Say so in the first sentence ("I couldn't find a policy for that") and offer a person or one clarifying question. Do not list near-miss articles to look helpful.

---
## Technical section

### T1. Solution architecture
```
question -> retrieve pages -> generate draft from page text
         -> link-dump check (answer in first two sentences? link count <= 3? labels present?)
         -> send, or regenerate with the rule, or hand off if no page supports an answer
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Reply is never only links | Output check (text outside links is over a minimum length) | Log count of link-only replies |
| First two sentences hold an answer, next step, or "not found" | Judge check on the draft | Labeled sample |
| At most three labeled links | Output filter | Count links per reply |
| Must-know items appear in reply text | Judge check on tagged intents | Test 6 |

### T3. Evals
- **Dataset:** 150 real help-center questions from logs, each with a label for the answer and the page that holds it. Include questions the pages do not answer.
- **Judge rubric:** is the answer in the first two sentences, are links labeled and capped, and does the bot say so when the pages are silent?
- **Metrics and starting thresholds:** link-led reply share under 2%; answer-first over 90%. Starting points to tune.
- **Release gate:** block a prompt, retrieval, or deflection-target change if link-led share rises on the eval set.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Share of replies that are mostly links | Over 3% | Over 8% | Check recent prompt, retrieval, or tuning changes |

### T5. Trade-offs
- Writing an answer from the pages costs more tokens and adds a risk of misstating a policy; keep the source link so users can check.
- A strict link cap can hide a second relevant page; the "Show more" offer in the choices covers that.

---
### Deep dive
- **Open question.** I found no study that measures how often assistants reply with links only, or that tests answer-plus-link against link-only in chat. The sources above are qualitative studies and a regulator's review.
- **References.** [NN/g, 2023](https://www.nngroup.com/articles/generative-ai-diary/) (opened); [NN/g, 2018](https://www.nngroup.com/articles/chatbots/) (opened); [NN/g, 2026](https://www.nngroup.com/articles/less-chat-more-answer/) (opened); [CFPB, 2023](https://www.consumerfinance.gov/data-research/research-reports/chatbots-in-consumer-finance/chatbots-in-consumer-finance/) (opened).
