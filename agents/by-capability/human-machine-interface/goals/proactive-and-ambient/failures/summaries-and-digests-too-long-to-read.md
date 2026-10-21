# AI Daily Summary Longer Than the Email: Summaries and Digests Too Long to Read

<!-- SEO
title: AI Daily Digest Too Long to Read: How to Fix It
description: An assistant's daily summary that runs longer than the items it covers gets skipped. Lead with what needs action and make the rest optional.
search phrases:
- ai summary longer than the original email
- daily digest too long nobody reads it
- how long should an ai daily summary be
- chatbot morning briefing too long
- ai assistant digest what needs action first
- how to make an ai summary shorter
- notification digest best practices
-->

**Frequency**: Common

## Issue: An assistant's daily summary or digest runs longer than the items it summarizes, so the user skips it; the fix is to lead with what needs action and make everything else optional.

> **One line:** The assistant sends a "daily summary" that takes longer to read than the inbox it was meant to save the user from.

| | |
|---|---|
| **Channel** | Written for **chat** and in-app assistants that send a scheduled or event-based summary. Email, push and voice briefings: PLANNED, not written. |
| **Stakes** | Low to medium. High when a deadline or a decision is buried in a digest nobody reads. |
| **Who is affected** | Anyone who opted in to a daily or weekly summary: inbox, team chat, tickets, calendar, news |
| **Frequency** | Common (our judgment). I found no count of how often assistants send digests longer than their sources. |
| **Pattern ID** | summaries-and-digests-too-long-to-read |
| **Family** | Proactive and ambient ([family README](../README.md)) |
| **Goal** | Proactive and always-listening agents speak up only when invited or useful, and respect a no. |
| **Primary metric** | Digest open rate and action rate (share of digests where the user opens it, and share where the user acts on a flagged item). Starting target: set from your baseline, then aim to rise (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A model can write shorter, but what counts as "needs action", how many items to show, and which things must never wait for a digest are product rules. (Our judgment, not tested.) |
| **Also searched as** | AI summary longer than the email · digest too long · morning briefing too long · daily recap nobody reads · summary of summaries · inbox digest overload |

## 1. In plain words
The user asked for a daily summary to save time. The assistant lists every message, every ticket, every meeting, in order, each with a sentence of context. The one thing that needs an answer today sits in the middle. The user reads the first few lines, gives up, and next week stops opening it. The fix is to put the actions first, keep the list short, and let the user ask for the rest.

## 2. What it looks like
**Without the fix** (a work assistant, 7:00 AM digest)
```
Bot:  Good morning! Here is your daily summary. You received 31 emails yesterday. Marketing sent 6
      newsletters, including one about the fall webinar series. Finance shared the Q3 expense
      report template, and HR reminded everyone about open enrollment. Dana replied on the vendor
      thread, Priya updated the roadmap doc, and 4 Jira tickets changed status... (22 more lines)
User: (closes it; never sees that the Acme contract needs a signature by 5 PM today)
```
**With the fix**
```
Bot:  2 things need you today:
      1. Sign the Acme contract by 5 PM (Dana sent it Tuesday).
      2. Approve Priya's time-off request (she leaves Friday).
      29 other items need nothing from you. Want them? [Show a short list] [Skip today] [Something else]
User: Skip today.
```
The fixed digest puts the two actions first with their deadlines, says how much was left out, and lets the user choose. It is shorter than the 31 emails it covers.

## 3. Why it happens
These are our reading of the pattern, except where a source is named in section 4.
- **The summary is built by walking the source.** The assistant goes through the items in order and writes a line for each, so the digest grows with the inbox instead of with what matters.
- **Nothing ranks what needs action.** Without a rule for "this needs the user", every item looks equally worth mentioning, and leaving one out feels like an error.
- **Completeness is rewarded.** A digest is checked for missing items, rarely for being skipped, so teams add lines and never remove them.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A study of 628 AI email summaries (collected March and April 2026) found average summary length varied by platform: Microsoft Copilot 156.5 words, Gmail/Gemini 28.8 words. | [BuzzStream and Aira, AI-Generated Email Summaries](https://www.buzzstream.com/blog/ai-generated-email-summary/). Opened and read. | Summaries of outreach pitch emails, not digests of many items. Vendor study (the author works for BuzzStream); two addresses per provider per template; the article's own summary and body disagree on one figure. It does not show summaries longer than their source. |
| The same study found most summary content came from the opening of the email (Gemini 87.1%, Apple 82.5%, Copilot 65.4% of keyword matches from the earlier part). | Same page. Opened and read. | Same caveats. It supports "put the key point first", for machine summaries of one email. It is not a study of human readers. |
| PR Daily ran 12 control emails through AI summaries and found that in 7 of 12 tests, cutting words to shorten the email led the AI to drop important context. | [PR Daily, AI email summaries are rewriting your message](https://www.prdaily.com/ai-email-summaries-are-rewriting-your-message-heres-what-to-do-about-it/). Opened and read. | Small informal test of how AI summarizes a human's email. It argues against cutting needed detail, which is why the fix keeps the rest one tap away instead of deleting it. |
| A notification-platform guide says to put the most important updates at the beginning of a digest, keep it brief, cap the list at a set number of items, and send urgent messages at once instead of waiting for the next digest. | [SuprSend, best practices for batching a digest](https://docs.suprsend.com/docs/best-practices-for-batching-digest). Opened and read. | Vendor documentation, not research. No data on open rates. |

I found no controlled study that measures open or action rates of digests by length, and the searches for one returned patents, vendor documents and forum threads. A forum post titled "OpenAI summary of email is longer than the email itself" turned up in a search summary; its page redirected when I opened it, so I do not use its content. I also read about notification-volume studies only in search summaries (for example, a 2014 in-situ study of mobile notifications and a Florida State distraction study); I did not open their full text and do not use their numbers.

**Public incident.** No dated public incident found for this pattern.

## 5. The fix
**The principle:** A digest leads with what needs the user's action, stays shorter than what it covers, and makes everything else optional.

**Do this**
1. **Actions first.** The first block lists only items that need the user to do something, each with the deadline and the person. Check: the first lines of every digest are actions, or "Nothing needs you today."
2. **Count what you left out.** Say how many items were skipped and that none need action. Check: the digest states the skipped count.
3. **Cap the list.** Show a fixed small number of items (start at 3, tune), then offer more. Check: items shown never exceed the cap unless the user asked.
4. **Shorter than the source.** The digest has fewer words than the items it covers. Check: digest word count under source word count on every send.
5. **Make the rest optional.** Offer "Show a short list", "Skip today", and "Something else" with free text open. Do not send the long version by default.
6. **Don't hold urgent items for the digest.** A deadline due before the next digest goes out as its own message, when the user has allowed that kind of message, and not inside the digest.
7. **Say nothing when nothing needs the user.** If no item needs action and the user chose that setting, skip the send, or send one line.
8. **Let the user shape it.** One tap to change frequency, length, or to stop. A "no" is kept.

**Reference design**
```
Digest (max once per chosen schedule)
1. Needs you: items with a due time or a waiting person. Show up to 3. Each: what, by when, who.
2. One line: "N other items need nothing from you."
3. Choices: [Show a short list] [Skip today] [Change how often] [Something else]
4. If nothing needs you: one line, or no send if the user chose quiet days.
```
```
When you send a summary, list only the items that need the user to act, with the deadline, first.
Then state how many other items were left out. Keep the summary shorter than the items it covers.
Offer the rest as a choice. Never send urgent items only inside a digest.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | At the top of every digest: the items that need action, or "Nothing needs you today." |
| Offer choices: 2-4 options plus "Something else", free text open | After the action block: "Show a short list", "Skip today", "Change how often", "Something else". Do not offer a menu when nothing was left out. |

**Don't over-correct.** Do not drop an item that does need action to keep the digest short; PR Daily's test found shortening can lose needed context (section 4). Do not hide the skipped count. Do not shrink the digest to "You have messages." The user must still be able to see what was left out and open it.

**Hand-off rule.** If the user says the digest is wrong or missed something important, stop the digest, apologize once, and offer a way to review what was left out or to reach a person who owns the product. Do not keep sending.

**Framework used:** none yet.

## 6. How to test it (short version)
Tests are **not yet run**. Build a day of 30 to 40 mixed items (two with deadlines, the rest routine) and generate the digest.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Day with 2 items that need action and 30 that do not | The two actions are first, each with a deadline; the other 30 are a count (1, 2) |
| 2 | Day with 12 items that need action | Shows the cap, then offers the rest; does not list all 12 (3) |
| 3 | A source of 3 short items | Digest has fewer words than the 3 items together (4) |
| 4 | Day with nothing that needs action | One line or no send, per the user's setting (7) |
| 5 | An item due in 2 hours, digest due in 10 hours | Sent on its own if allowed; not left for the digest (6) |
| 6 | User picks "Skip today" | No long version follows; tomorrow's digest still sends (5, 8) |
| 7 | User says "stop the digest" | Stops and stays stopped (8) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Digest open rate and action rate** (primary) | Set from baseline, then rising | Opens and clicks on flagged items per digest sent | Falling two weeks in a row |
| Digests with actions listed first | 100% | Check the first block of each digest in a sample | Below 95% |
| Digests shorter than their source | 100% | Word count of digest vs. covered items, per send | Any digest longer |
| Items shown over the cap | 0 unless requested | Count of items per digest | Any |
| Unsubscribes or "stop" after a digest (counter) | Track; set from baseline | Opt-out events within 1 day of a send | Rising |
| Action items missed (counter) | 0 | Sampled review: items with a deadline that were left in the skipped count | Any |

### Detection signals (proposed, not yet calibrated)
Proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Digest word count exceeds the word count of the items it covers | Send event with digest length and source length | A digest of one very short item |
| Digest is unopened for several days in a row | Open events per recipient | User on leave |
| The user asks about an item the digest listed far from the top | A user question matching a digest item, with its position | The user wants more detail on a minor item |
| An item with a deadline appears in the skipped count | Digest content vs. item due dates | The item was already handled |
| The user taps "Skip today" or "stop" on several digests in a row | Choice events | A busy week |

**Starter rule:** every digest begins with the items that need the user to act (or says none do), states how many other items were left out, and is shorter than what it covers.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: summaries-and-digests-too-long-to-read
runs: pre_send
reads: [digest.text, digest.items, item.needs_action, item.due_at, source.word_count, user.digest_settings]
trigger: a scheduled digest is about to be sent
moves: [lead_with_answer, offer_choices]
choices: ["Show a short list", "Skip today", "Change how often", "Something else"]
on_miss: rewrite
metric: digest open rate and action rate
counter_metric: action items missed
status: proposed
```

## 8. Related patterns
- [Key details buried](../../response-structure/failures/key-details-buried.md): dates and amounts hidden inside one reply's paragraphs. This page is about a scheduled message that covers many items and is too long as a whole, so the user never opens it.
- [Answer buried](../../response-structure/failures/answer-buried.md): a reply to a question opens with filler. This page has no question; the assistant sends the message on its own.
- [Length mismatch with the user's effort](../../response-structure/failures/length-mismatch-with-the-user-s-effort.md): a short message gets a long reply. This page sizes the digest against the source items, not against a message the user typed.
- [No proactive updates](../../conversation-frameworks/failures/no-proactive-updates.md): the opposite problem, a bot that never volunteers status. This page covers a bot that volunteers too much in one message.
- [Proactive outreach overreach](../../relational-and-boundaries/failures/proactive-outreach-overreach.md): messages the user never asked for. This page assumes the user did opt in and asks how long the message is.
- Sibling pages in this family, named in plain text because they are written separately: interrupts at a bad moment, dismissed suggestions come back, ambient assistants act on overheard conversation, proactive action surprises the user.

## 9. Common questions
### How long should an AI daily summary be?
I found no study that sets a number. Shorter than what it covers is a rule you can check, and a cap on items is a starting point to tune (section 5, rules 3 and 4).

### Why is my AI summary longer than the original email?
The summary was written by walking the source and describing each part, with no limit. In the study I opened, Microsoft Copilot summaries averaged 156.5 words and Gemini's 28.8, so length varies a lot by tool ([BuzzStream and Aira](https://www.buzzstream.com/blog/ai-generated-email-summary/)). Set a limit and test it on your own data.

### Should a digest include everything?
No. List what needs action, count the rest, and offer them. One test found that cutting words can drop needed context, so keep the rest one tap away.

### Should urgent items wait for the daily digest?
No. A notification vendor's guide says urgent messages should be delivered instantly ([SuprSend](https://docs.suprsend.com/docs/best-practices-for-batching-digest)). That is vendor guidance, not research.

---
### Deep dive
- **Open question.** I found no study that measures how digest length changes open or action rates. The evidence here is about how AI summarizes email and about digest design guidance.
- **References.** [BuzzStream and Aira](https://www.buzzstream.com/blog/ai-generated-email-summary/) (opened); [PR Daily](https://www.prdaily.com/ai-email-summaries-are-rewriting-your-message-heres-what-to-do-about-it/) (opened); [SuprSend](https://docs.suprsend.com/docs/best-practices-for-batching-digest) (opened).
