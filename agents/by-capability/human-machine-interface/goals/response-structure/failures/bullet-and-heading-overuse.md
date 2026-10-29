# Chatbot Responses Use Too Many Bullet Points and Headers: Bullet and Heading Overuse

<!-- SEO
title: Chatbot Responses Too Many Bullet Points and Headers: Fix
description: Why chatbots break an explanation into bullets and headers, what vendor prompts and user reports show, and a rule to keep lists for list-shaped content.
search phrases:
- chatbot responses too many bullet points
- how to stop chatbot using bullet points
- chatbot uses headers in every answer
- how to make chatbot answer in paragraphs
- chatgpt bullet points everywhere fix
- chatbot answer broken into fragments
- system prompt no bullet points chatbot
- ai assistant over-formatting responses
-->

**Short answer:** Match the shape of the reply to the shape of the content. Explain reasoning, trade-offs and advice in connected sentences. Use a bullet list only for three or more parallel, independent items, after a one-sentence answer. Use headers only in replies over 250 words that cover several distinct topics, and no formatting in casual or emotional chats.

**Frequency**: Common

## Issue: The assistant answers a question that needs connected reasoning with headers and short bullets, so the "because" and "but" between the ideas are lost and the user must rebuild the argument.

> **One line:** The reply looks organized, but each bullet is a fragment, and the reasoning that links them is missing.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice is different: a listener cannot see bullets or headers (planned, not written). |
| **Stakes** | Low for a casual question. Medium when the user is deciding something (a plan, a trade-off, an explanation they must repeat to someone else). |
| **Who is affected** | Anyone asking "why", "should I" or "explain", and anyone in a casual or emotional conversation where a formatted reply reads as cold |
| **Frequency** | Common as a style default. User complaints are public (section 4). I found no study that counts how often chatbots over-format. |
| **Pattern ID** | bullet-and-heading-overuse |
| **Family** | [Response structure and closers](../README.md) |
| **Goal** | Replies are shaped so people can read, act on, and answer them, and short messages like "ok" and "bye" get the response the moment calls for. (Catalog row RS-08 states the goal as: structure serves the content.) |
| **Primary metric** | Judge rating of coherence by format, paired with the fragmentation rate (share of reasoning replies built from headers and bullets under 15 words). Starting target: coherence rated 4 or 5 of 5 on over 90% of sampled reasoning replies; fragmentation under 10% (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Vendors already steer their own models toward prose, and a prompt line works for many cases, but the default pull toward lists remains and rendering layers can add bullets the model did not write. Cause owner: the model's default style, plus the chat window. (Our judgment, not tested.) |
| **Also searched as** | chatgpt too many bullet points · chatbot formats everything as a list · bot uses headers in short answers · make chatbot write paragraphs · stop AI from over-formatting |

## 1. In plain words
Some content is a list: parallel, independent items. Other content is an argument: ideas that depend on each other. When the assistant puts an argument into headers and bullets, it keeps the nouns and drops the connectors ("because", "unless", "which means"). The reply looks tidy, and the user still has to work out how the pieces fit.

## 2. What it looks like

**Without the fix**
```
User: Should I pay off my car loan early or put the money in savings?
Bot:  ## Considerations
      - Interest rate on the loan
      - Interest rate on savings
      - Emergency fund
      ## Pros of paying off the loan
      - Guaranteed savings on interest
      ## Pros of saving
      - Liquidity
User: So which one should I do?
```

**With the fix**
```
User: Should I pay off my car loan early or put the money in savings?
Bot:  It depends mostly on two things. If your loan rate is higher than what your savings earn, paying
      it off wins, because every dollar you put toward it saves you more than it would earn. But if you
      have under three months of expenses saved, build that first, since cash you can reach quickly
      matters more than a few dollars of interest. What is the loan rate, and how much do you have saved?
```
The same considerations appear in both. The fixed reply keeps the links between them (higher rate, so pay off; thin cushion, so save first), gives a conditional answer, and asks for the two missing facts. It uses no headers and no bullets.

## 3. Why it happens
These are our reading of the pattern, supported where section 4 says so.
- **List-shaped output is a default.** Anthropic's published system prompt for Haiku 4.5 spends several paragraphs telling the model to use less formatting, which suggests the default needs steering. Users on a public forum report the same pull in another vendor's product.
- **The rule is missing or one-sided.** A prompt that says "be scannable" or "use markdown" without saying when not to produces lists for everything. A prompt that says only "don't use bullets" can fail to stick (see the n8n report in section 4).
- **The chat window adds formatting the model did not choose.** A widget that renders every line starting with a dash as a bullet makes plain text look like a list. That is a product bug, not a model choice, and it needs a different fix.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A user opened a thread on January 21, 2025 saying ChatGPT uses bullets in letters and narrative drafts: "Bullet points often break the narrative or argumentative structure." Later replies (December 2025 to February 2026) report the same on a newer model and in brainstorming, with answers of "more than 10 bullets". No fix is confirmed in the thread. | [OpenAI community thread, excessive bullet point formatting](https://community.openai.com/t/excessive-bullet-point-formatting-issue-in-chatgpt-responses/1097391). Opened and read. | A handful of users on a forum, no counts. It shows the complaint exists and persists. It does not show how common it is, and the posts are about drafting and brainstorming more than support chat. |
| Claude Haiku 4.5's published system prompt tells the model to avoid over-formatting with bold, headers, lists and bullets, to answer in sentences and paragraphs in typical conversations unless a list is asked for, to write lists inside prose, and to use bullets only when the person asks or the answer is multifaceted and lists are essential. | [Anthropic release notes, Claude Haiku 4.5 system prompts](https://platform.claude.com/docs/en/release-notes/system-prompts/claude-haiku-4-5). Opened and read. | Shows what one vendor chose to write into its prompt, not how well it works. Wording varies by model and version. It is a vendor's own product. |
| Anthropic's prompting guide suggests telling the model what to do ("flowing prose paragraphs") instead of what not to do, notes that the style of your prompt can influence the style of the answer, and gives a sample block that reserves markdown mainly for code and simple headings. | [Anthropic prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices). Opened and read. | Vendor guidance for its own models. It reports no measured improvement. |
| A developer reports that, with a system prompt saying not to use bullets, the n8n Web Chat still showed bullets on nearly every line. Replies in the thread blame Markdown rendering of lines starting with a dash, and streaming that drops blank lines. The issue is dated July 12, 2026; no fix is confirmed. | [n8n community thread](https://community.n8n.io/t/n8n-web-chat-interface-displays-unwanted-bullet-points-on-every-response-line/302999). Opened and read. | One bug report against one product and version. The cause is the reporters' suggestion, not a confirmed diagnosis. It shows why a log check must look at what the user saw. |
| NN/g lists bulleted lists among techniques for scannable web text, and reports the scannable version of a test site scored 47% better on measured usability. | [Nielsen, *How Users Read on the Web*, NN/g, September 30, 1997](https://www.nngroup.com/articles/how-users-read-on-the-web/). Opened and read. | A 1997 study of web pages with five versions of one site, where the scannable layout was one change among others. It supports lists for scannable content. It says nothing about reasoning, and it is the reason this page keeps lists for list-shaped content. |

A web search for a controlled study of bullets versus prose for reasoning in chat found none. The claim that fragmenting an argument hurts comprehension is our inference, not a measured result. I read the search summary on a policy-brief paper (Sci2Pol) and did not open it, so it is not used here.

**Public incident.** No public incident found. The three searches behind this page returned forum complaints and vendor documentation, not a dated event with harm.

## 5. The fix

**The principle:** Use bullets and headers only for content that is a list or has sections; keep reasoning in sentences that carry the "because" and "but".

**Do this**
1. **Answer questions that ask "why", "should I", "explain" or "what's the difference" in connected sentences.** Every claim that depends on another uses a connector word (because, so, unless, but). Check: no reply to these intents is made only of bullets.
2. **No headers in a reply of 250 words or fewer.** Check: header count is 0. (The 250 is a starting point to tune.)
3. **Use a bullet list only for parallel, independent items of 3 or more** (options, ingredients, requirements). Check: each list item can be reordered without changing meaning.
4. **Every bullet is a full thought or the whole list is plain short items; do not mix.** A fragment like "Liquidity" with no point is not allowed. Check: no bullet under 4 words in a reasoning reply.
5. **Keep a one-sentence takeaway in prose before any list.** The list follows the answer (see [answer buried](answer-buried.md)). Check: sentence 1 is not a header or bullet.
6. **Casual, emotional or advice chats get no formatting at all.** Check: zero bullets, headers or bold in replies tagged casual or emotional.
7. **Do what the user asks.** If the user asks for a list, a table or "no bullets", follow it for the rest of the conversation. Check: the next replies match the request.

**Reference design: format decision table**
| The content is... | Use |
|---|---|
| An argument, a trade-off, an explanation, advice | Sentences in one or two short paragraphs |
| Parallel independent items (3 or more) | A short bullet list, after a one-sentence answer |
| Ordered actions | Numbered steps (see [unstructured procedures](unstructured-procedures.md)) |
| Dates, amounts, deadlines to act on | Labeled lines (see [key details buried](key-details-buried.md)) |
| Several distinct topics in a long reply (over 250 words) | Headers, one per topic |
| Casual or emotional message | Plain sentences only |

```
Match the shape of the reply to the shape of the content.
Explain reasoning, trade-offs and advice in connected sentences using words like "because", "but" and "unless".
Use a bullet list only for 3 or more parallel, independent items, after a one-sentence answer.
Use no headers in replies under 250 words. Use no formatting in casual or emotional conversations.
If the user asks for a list, a table, or no bullets, follow that for the rest of the conversation.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | A reasoning question: give the conditional answer in the first sentence, in prose, then the because. |
| Offer choices | The user complains about the format or asks again: "Explain in a paragraph", "Give me a list", "Short version", "Something else". |

**Don't over-correct.** Do not remove lists the content needs. A list of requirements, a comparison across three plans, or a set of parallel options reads better as a list (the NN/g result above). Do not force long paragraphs: two or three sentences per idea, with a break between ideas. Do not ignore a user who asks for bullets.

**Hand-off rule.** This pattern needs no handoff to a person. If the user asks for a format the chat window cannot show (a table in plain-text SMS), say so and give the closest form, as in [channel fit](../../../solutions-library/channel-fit-matrix.md).

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
No full test file exists yet for this pattern. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | "Should I pay off my car loan early?" | Connected sentences with because/unless, no headers, one clarifying question (rules 1, 2) |
| 2 | Short answer of about 100 words | Zero headers (rule 2) |
| 3 | "List the documents I need for a passport renewal" | A bullet list of parallel items after a one-sentence answer (rule 3) |
| 4 | Reasoning reply from a bullet-heavy prompt | No bullet under 4 words (rule 4) |
| 5 | "My dog died this morning" | No bullets, headers or bold (rule 6) |
| 6 | User: "No bullets, please" then a second question | Both replies follow it (rule 7) |
| 7 | Reply of 400 words on three topics | Headers allowed, one per topic; sentence 1 is not a header (rules 2, 5) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Coherence rated by format** (primary) | 4 or 5 of 5 on over 90% of sampled reasoning replies | A judge, with a human-checked sample, rates "does the reply connect its ideas?" for prose and bulleted replies separately | Below 80%, or bulleted replies rated 0.5 points or more below prose |
| **Fragmentation rate** (primary, paired) | Under 10% of reasoning replies | Share of replies tagged why/should-I/explain whose text is mostly headers and bullets under 15 words, counted from the reply markup | Over 20% |
| Headers in replies of 250 words or fewer | Under 3% | Count header markup per reply in logs | Over 8% |
| Formatting in casual or emotional turns | Under 2% | Bullet, header or bold markup in replies tagged casual or emotional | Over 5% |
| Format requests honored on the next reply | Over 95% | Reply after "no bullets" or "use a list" matches the request | Below 85% |
| Lists wrongly turned into prose (counter-metric) | Under 5% | Labeled sample of list-shaped requests answered as paragraphs | Over 10% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. All are written for text chat; none is detected for voice.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply to a why/should-I/explain message has a header and 3 or more bullets, with no sentence over 20 words | Markup count and sentence lengths in the reply text | The user asked for a list or an outline |
| User asks "so which one?" or "what should I do?" right after a bulleted reply | Same intent restated in the next user turn | A user who wanted the options listed first, then a recommendation |
| User writes "no bullets", "in a paragraph" or "stop using lists" | Phrase match in the user turn | A user asking about bullets as a topic ("what is a bullet journal?") |
| Dash-started lines appear in the user's view but not in the model output log | Rendered text compared with the logged output | None; this points to the chat window, not the model |
| Reply to a casual or emotional message contains headers or bullets | Intent tag plus markup count | A user who asked for a plan in an emotional moment |

**Starter rule:** reasoning and advice replies are written as connected sentences, with lists only for 3 or more parallel items and no headers under 250 words.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: bullet-and-heading-overuse
runs: pre_send
reads: [draft_reply.text, draft_reply.markup_counts, user_turn.intent, session.format_request]
trigger: a reply to a reasoning, advice or casual message contains headers or fragment bullets
moves: [lead_with_answer, offer_choices]
choices: ["Explain in a paragraph", "Give me a list", "Short version", "Something else"]
on_miss: rewrite
metric: coherence rated by format
counter_metric: lists wrongly turned into prose
status: proposed
```

## 8. Related patterns
- [Wall of text](../../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/conversation-depth-mismatch.md): the opposite problem. A wall of text is a dense block with no breaks. This page is a reply cut into too many fragments. The wall of text section in that page covers the dense block; the fix for one can cause the other, so use both pages together.
- [Unstructured procedures](unstructured-procedures.md): there, ordered actions arrive as prose and need numbered steps. Here, reasoning arrives as bullets and needs sentences. The test is the content's shape: ordered actions get numbers, arguments get prose.
- [Key details buried](key-details-buried.md): there, a date or amount hides in a paragraph and needs its own line. Here, everything has its own line and the links are lost. Labeled lines are for facts to act on, not for every idea.
- [Answer buried](answer-buried.md): about order, not shape. A bulleted reply can still start with the answer, and a prose reply can still bury it.

## 9. Common questions
### Why does my chatbot use so many bullet points?
Two causes are common: the model's default style leans toward lists and headers, and some chat widgets render lines starting with a dash as bullets whatever the model meant. Check the raw model output against what the user sees. See [why it happens](#3-why-it-happens).

### How do I stop a chatbot from using bullet points?
Tell it what to do rather than what not to do: for example, "write reasoning in connected paragraphs; use a list only for 3 or more parallel items". Anthropic's prompting guide recommends this wording style, and says matching your prompt's style to the output you want can help. Test with the table in [the fix](#5-the-fix); a "no bullets" line alone did not stick in one n8n report.

### Is it wrong for a chatbot to use bullet points at all?
No. Lists suit parallel, independent items, and older web research found scannable layouts with bullets helped. The failure is putting an argument into a list. See [Don't over-correct](#5-the-fix).

### Is this the same as a wall of text?
No, it is the opposite failure. A wall of text has too little structure; this has too much. Use [the wall of text section](../../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/conversation-depth-mismatch.md) for the dense block and this page for fragmentation.

### Should the bot use headers in a short answer?
No. In this page's rule, replies of 250 words or fewer get no headers (a starting point to tune). Headers help a long reply with several topics, not a three-paragraph answer.

---
## Technical section

### T1. Solution architecture
```
draft reply -> intent tag (reasoning / list-shaped / procedure / casual) + user format request
            -> format check (markup counts, bullet lengths, sentence 1, header count)
            -> send, or regenerate with the format decision table
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No headers at 250 words or fewer | Output filter or prompt | Count header markup in logs |
| Reasoning intents are not only bullets | Output filter | Markup and sentence-length check |
| Format request persists in the session | Session state | Next-reply sample |
| Rendered text matches model output | Client logging | Compare displayed text to logged output |

### T3. Evals
- **Dataset:** 100 why/should-I/explain prompts, 50 list-shaped prompts, 30 casual or emotional messages, 20 with a format request, from your logs.
- **Judge rubric:** does the reply connect its ideas, is any bullet a bare fragment, are headers present in a short reply, and was a list kept when the content was list-shaped? Compare the same prompts answered as prose and as bullets.
- **Metrics and starting thresholds:** coherence 4 or 5 on over 90% of reasoning replies; fragmentation under 10%; lists wrongly turned into prose under 5%. Starting points to tune.
- **Release gate:** block a prompt or model change if fragmentation rises or if the list-shaped set drops.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Fragmentation rate | Over 15% | Over 25% | Review recent prompt, model or renderer changes |

### T5. Trade-offs
- A prose rule can make replies longer; keep the paragraph cap in rule 1 and offer the short version.
- A markup counter can miss formats such as plain-text lists with line breaks; add a sentence-length check.
- Judge ratings of coherence are model-based and should be spot-checked by people.

---
### Deep dive
- **Open question.** I found no controlled study comparing the same reasoning delivered as bullets and as prose in chat. The evidence is user reports, vendor prompts and 1997 web research.
- **References.** [OpenAI community thread](https://community.openai.com/t/excessive-bullet-point-formatting-issue-in-chatgpt-responses/1097391) (opened); [Claude Haiku 4.5 system prompts](https://platform.claude.com/docs/en/release-notes/system-prompts/claude-haiku-4-5) (opened); [Anthropic prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) (opened); [n8n community thread](https://community.n8n.io/t/n8n-web-chat-interface-displays-unwanted-bullet-points-on-every-response-line/302999) (opened); [Nielsen, NN/g, 1997](https://www.nngroup.com/articles/how-users-read-on-the-web/) (opened).
