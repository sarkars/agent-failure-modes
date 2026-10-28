# Words That Make Text Sound AI-Written ("Delve", "It's Important to Note"): Stock Phrases in Published Text

<!-- SEO
title: Words That Make Text Sound AI-Written, and How to Lint Them
description: Why AI-drafted emails and posts use "delve" and "I hope this email finds you well", and a prompt rule plus phrase-list check to catch them first.
search phrases:
- words that make text sound like ai wrote it
- chatgpt overused words list
- how to tell if something was written by chatgpt
- why does chatgpt say delve
- i hope this email finds you well ai
- remove ai phrases before publishing
- vale rule for ai writing tells
- phrase list linter for ai slop
-->

**Frequency**: Very Common

## Issue: An AI-drafted email, post or page goes out full of stock phrases such as "delve", "it's important to note" and "I hope this email finds you well", and readers spot it as AI text.

> **One line:** Text published straight from a chatbot carries the model's favorite phrases, readers recognize them and discount the message; the fix is a prompt rule that bans the phrases plus a phrase-list check that blocks the draft before it is sent or published.

| | |
|---|---|
| **Channel** | Written for **published text**: emails, newsletters, blog posts, product pages, support macros and reports drafted with ChatGPT, Claude, Gemini or Copilot. Chat replies are covered by the persona pages linked in section 8. |
| **Stakes** | Low to medium. A cliché in a newsletter costs some attention. It costs more when it is a customer apology, a price change or a cover letter, where a reader who spots "AI wrote this" may also doubt the sender. |
| **Who is affected** | Readers of the published text, and the sender or brand whose name is on it |
| **Frequency** | Very common, by our reading. Kobak et al. estimate at least 10% of 2024 PubMed abstracts were processed with LLMs, using excess style words (section 4). I found no count for emails or marketing copy. |
| **Pattern ID** | text-stock-phrases |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Stock-phrase-free publish rate: published or sent pieces whose pre-publish scan finds zero unwaived phrase-list hits, divided by all published pieces. Proposed starting target: 95%. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Newer models drop some old favorites, but each model has its own, so a list kept from your own drafts is still needed. (Our judgment, not tested.) |
| **Also searched as** | ChatGPT words to avoid · AI writing tells · sounds like ChatGPT · delve ChatGPT · AI email clichés · humanize AI text |

## 1. In plain words
A chatbot reaches for the same words again and again: "delve", "underscore", "tapestry", "It's important to note", "In today's fast-paced world", "I hope this email finds you well". One of them alone proves nothing. Three in one email, and the reader thinks "a bot wrote this", stops reading carefully, and trusts the sender a little less. The builder can catch the phrases with a list before anyone else sees them.

## 2. What it looks like
**Without the fix**
```
Manager: Draft an email to our customers. Furnace tune-ups go from $89 to $109 on March 1. We're in Denver.
AI tool: Subject: Delving Into Our Commitment to Your Comfort
         I hope this email finds you well! In today's fast-paced world, your home's comfort is paramount.
         It's important to note that, effective March 1, our tune-up price will be adjusted to $109.
         This change underscores our unwavering commitment to quality. Don't hesitate to reach out!
Manager: Looks fine. Sending to 4,200 customers.
(Replies that afternoon: "Did a robot write this?" and "Just tell me the new price.")
```
**With the fix**
```
Manager: Draft an email to our customers. Furnace tune-ups go from $89 to $109 on March 1. We're in Denver.
AI tool: Subject: Furnace tune-ups will cost $109 starting March 1
         Starting March 1, a furnace tune-up costs $109, up from $89. Visits booked before then keep the old price.
         I left one gap: why the price changed. Give me the reason in a sentence, or I'll leave it out.
Manager: Parts and labor went up. Say that.
Phrase check: 0 hits in subject and body (list v12, 64 phrases). Ready to send.
```
The fixed draft starts with the change, uses no listed phrase, asks for the one fact it lacks instead of padding, and a check confirms zero hits before sending.

## 3. Why it happens
- **The model's vocabulary drifts toward a small set of style words.** Kobak et al. found that the 2024 excess vocabulary in PubMed abstracts was almost all style words, such as "delves", "showcasing" and "underscores", not content words. Why training produces these exact words is not established in the sources I read.
- **The prompt gives the model no facts to fill the space.** "Write a friendly email about the price change" leaves room for a greeting, a thesis line and a sign-off, and stock phrases fill it. (Our reading.)
- **Nobody reads the draft as a stranger would.** The sender skims for the price and the date, which are correct, and sends. No check looks for the phrases. (Our reading.)

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A study of 14 million PubMed abstracts from 2010 to 2024 found excess words in 2024 that were "almost entirely" style words; "delves" appeared about 28 times as often as expected, and "showcasing" and "underscores" about 10 times. It estimates "at least 10% of 2024 abstracts were processed with LLMs", up to 30% in some sub-corpora. | [Kobak, González-Márquez, Horvát, Lause, *Delving into ChatGPT usage in academic writing through excess vocabulary*, arXiv 2406.07016 v4, Feb. 2025](https://arxiv.org/abs/2406.07016v4). Abstract and HTML full text opened. | Scientific abstracts, not emails or marketing. A search summary said a 25x figure and Science Advances publication; I could not open the journal page (403), so I use the arXiv text (28.0). Single study. |
| Wikipedia's "Signs of AI writing" guide says "delve" was "famously overused by ChatGPT in 2023 and early 2024", lists "Certainly!" and "let me know" as words to watch in chatbot-style text, and notes that older models added "important to note" disclaimers. | [Wikipedia, *Wikipedia:Signs of AI writing*](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). Opened and read in parts (about 200,000 of 250,000 characters). | Editor advice, not a study; the page says it is not policy and "Not all text featuring these indicators is AI-generated." Its example uses "I hope this message finds you well", not "email". |
| The same guide says detection tools "have non-trivial error rates" and that "Humans are notoriously bad at distinguishing human and LLM-generated text." | Same Wikipedia page. Opened. | Editor guidance, not a measured result. It is why this page checks phrases instead of scoring "AI-ness". |
| TechCrunch called the guide the best resource for checking suspicions of AI writing and reports that the editors say automated detection tools are essentially useless for this. | [Brandom, *The best guide to spotting AI writing comes from Wikipedia*, TechCrunch, Nov. 20, 2025](https://techcrunch.com/2025/11/20/the-best-guide-to-spotting-ai-writing-comes-from-wikipedia/). Opened. | Secondary press coverage of the same guide. |
| In three experiments, people rated Airbnb hosts as less trustworthy when they believed the profile was AI-written, but only when they saw a mix of AI and human profiles; the authors call this the "Replicant Effect". | [Jakesch, French, Ma, Hancock, Naaman, CHI 2019](https://sml.stanford.edu/publications/hancock-jt/ai-mediated-communication-how-perception-profile-text-was-written-ai). Abstract page opened; the PDF did not render, so I did not read sample sizes. | Profiles, not emails; 2019, before ChatGPT. It shows that suspected AI text can cost trust, not that stock phrases cause the suspicion. |
| Vale, an open-source prose linter, has an "existence" check that flags listed tokens, each a phrase or a regular expression. | [Vale docs, *existence*](https://docs.vale.sh/checks/existence). Opened. | Tool documentation. Shows the check is buildable with existing tools; says nothing about results. |

I found no study I could open that tests whether removing stock phrases from emails changes reply or trust rates. Search results on "I hope this email finds you well" were blogs and vendor pages calling it a cliché; I did not use them as evidence.

**Public incident.** No dated incident opened for stock phrases in published text. Leftover chatbot text in print and in product listings is covered in [placeholder data left in](./ui-placeholder-data-left-in.md).

## 5. The fix
**The principle:** No AI-drafted text is sent or published while it contains a listed stock phrase that nobody chose on purpose.

**Do this**
1. **Zero unwaived hits before sending.** Every AI-drafted piece is scanned with the phrase list below; any hit not on the waiver list blocks the send or publish step.
2. **Sentence one carries the news.** The first sentence of an email or post states the change, the answer or the request, with its date, price or name.
3. **Ask for missing facts, don't pad.** When the draft lacks a reason, a date or a number, the AI tool names the gap and asks once; it does not fill the space with a general sentence.
4. **Keep the list from your own drafts.** Start with the list below, add any phrase that appears in 3 or more drafts in a month (tune), and record the list version with each scan.
5. **Scan everything that ships.** Subject lines, preview text, headings, alt text, meta descriptions and email signatures, not only the body.
6. **Count weak tells, block strong ones.** Single words such as "crucial" or "robust" are counted and shown; whole stock phrases block. A piece with 3 or more weak tells is sent back for a rewrite (tune).
7. **Re-check after edits.** A human edit or a second AI pass re-runs the scan.

**Reference design: pre-publish phrase list** (case-insensitive; starting list, our judgment plus the Wikipedia guide)
| Group | What to match | Default action |
|---|---|---|
| Email openers and closers | "I hope this email finds you well", "I hope this message finds you well", "don't hesitate to reach out", "I hope this helps", "let me know if you have any questions" | Block |
| Throat-clearing | "It's important to note", "It is worth noting", "In today's fast-paced world", "In the ever-evolving landscape of", "Let's dive in" | Block |
| Chatbot leftovers | "Certainly!", "Great question", "As an AI", "Here is a draft" | Block |
| Inflated nouns and verbs | "delve", "tapestry", "testament to", "underscores", "showcasing", "navigate the complexities" | Block |
| Weak tells (count only) | "crucial", "robust", "seamless", "pivotal", "Moreover", "Furthermore", "In summary" | Count; rewrite at 3 or more |

**Prompt block for the AI tool**
```
Start with the news: what changes, when, and what it costs or means for the reader.
Do not use these phrases: [paste the Block rows of your list].
If you lack a fact (reason, date, number, name), say which one and ask; do not write a general sentence in its place.
No greeting line, no "don't hesitate to reach out" closer. End with the one action the reader can take.
```

**Vale rule** (one way to run the check in CI or an editor)
```yaml
extends: existence
message: "AI stock phrase: '%s'. Rewrite with a fact."
level: error
ignorecase: true
tokens:
  - I hope this (?:email|message) finds you well
  - it's important to note
  - in today's fast-paced world
  - delv(?:e|es|ing)
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the conversation is the sender prompting the AI tool, or the checker reporting to the sender)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The draft's first sentence is the news (the new price and date), not a greeting or a "commitment" line. |
| Ask one clarifying question | The draft lacks one fact the reader needs (why the price changed): the tool asks for it instead of padding. |
| Offer choices: 2-4 options plus "Something else", free text open | The checker reports a hit: "Rewrite this sentence", "Delete it", "Keep it on purpose (waive)", "Something else". |
| Admit uncertainty and show how to check | The checker counts weak tells but cannot say whether a human wrote them: it reports the count and the lines, and does not call the text "AI-written". |

**Don't over-correct.** Do not run the draft through a "humanizer" that swaps "delve" for "dig into" on every line; the stock sentence is still empty. Do not treat a hit as proof that a person used AI: people write "crucial" too, and the Wikipedia guide warns against accusing on signs alone. Do not ban a word that is your product's real term (a mortgage lender may need "navigate" in a real feature name); waive it with a reason. Do not strip courtesy from an apology; one plain line of regret is content.

**Hand-off rule.** When a hit sits in legal, medical, financial or apology text, the checker routes the draft to the named owner of that message for a human rewrite instead of auto-fixing it. When the checker is used to judge whether a third party (a student, a job applicant) used AI, it hands the decision to a person and shows its counts as weak evidence only.

**Framework used:** none yet. The list draws on Kobak et al. and the Wikipedia guide (section 4) plus our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Customer email opening "I hope this email finds you well" | Send is blocked and the line is named | 1 |
| 2 | Price-change email | Sentence one names the new price and the date | 2 |
| 3 | Prompt gives no reason for the change | The tool asks for the reason; no "commitment to quality" sentence | 3 |
| 4 | "Delving" in the subject line only | Scan finds it | 5 |
| 5 | Draft with "crucial", "robust" and "Moreover" | Rewrite requested; not blocked | 6 |
| 6 | "Navigate" in a waived product name | Pass; waiver reported | 1 |
| 7 | Clean draft, then an editor adds "It's important to note" | Re-scan blocks | 7 |
| 8 | A phrase seen in 4 drafts this month | Added to the next list version | 4 |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Stock-phrase-free publish rate** (primary) | 95% | Pre-publish scan log: pieces with zero unwaived Block hits / all published pieces | Below 90% in a week |
| Block hits per 1,000 words, at draft | Track; set from baseline | Scan of AI drafts before editing | Rising two weeks in a row |
| Weak tells per 1,000 words, at publish | Set from baseline | Same scan, count-only rows | 50% above baseline |
| Reader replies that mention AI or a bot | Track; set from baseline | Phrase match ("robot", "ChatGPT", "AI wrote") in replies to sent emails | Any rise after a template change |
| Waivers per 100 pieces | Track | Count waived hits | Rising two months in a row |
| Scan false-positive rate (counter-metric) | Under 10% | Monthly review of 50 hits, labeled real tell or legitimate use | Over 20% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A Block phrase in the subject, preview or first sentence | Pre-publish scan of the draft fields | A quote or an article about AI writing |
| Three or more weak tells in one piece | Scan count per piece | A writer whose house style uses these words |
| The draft was pasted from an AI tool and sent within a few minutes with no edits | Editor or CMS event log: paste, then send | A reviewed template reused on purpose |
| A reader reply says "robot", "ChatGPT" or "AI wrote this" | Inbound reply text | A reader joking about an unrelated topic |

**Starter rule:** block sending or publishing any AI-drafted piece that contains a phrase from the Block list that is not on the waiver list.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: text-stock-phrases
runs: pre_send
reads: [draft.subject, draft.preview_text, draft.body, draft.meta, phrase_list.version, waiver_list]
trigger: an AI-drafted piece is about to be sent or published, or the AI tool is about to report a draft as done
moves: [lead_with_answer, ask_clarifying_question, offer_choices, admit_uncertainty]
choices: ["Rewrite this sentence", "Delete it", "Keep it on purpose (waive)", "Something else"]
on_miss: rewrite
metric: stock-phrase-free publish rate
counter_metric: scan false-positive rate
status: proposed
```

## 8. Related patterns
- [Chatbot stock phrases](../../persona-and-tone/failures/stock-phrases.md) - the closest existing pattern. It covers a chatbot opening each live reply with "I'd be happy to help" or "As an AI"; this page covers published text (emails, posts, pages) that readers recognize as AI-written, and the pre-publish phrase check that catches it.
- [Filler and padding](../../response-structure/failures/filler-and-padding.md) - content-free sentences around an answer in chat. Stock phrases are often filler, but this page is about the recognizable words and a list-based check, not sentence count.
- [Placeholder data left in](./ui-placeholder-data-left-in.md) - unreplaced dummy content and chatbot leftovers such as "As an AI language model" on live pages; its checklist shares the "AI leftovers" row.
- [Generic hero layout](./ui-generic-hero-layout.md) - stock headline copy on AI-built landing pages; the same habit in a page's hero.

## 9. Common questions
### What words make text sound like ChatGPT wrote it?
Words such as "delve", "underscores" and "showcasing" rose sharply in scientific abstracts after ChatGPT (Kobak et al.), and Wikipedia's guide lists more. Phrases like "It's important to note" and "I hope this email finds you well" add to the effect. See [the phrase list](#5-the-fix).

### Can I prove someone used AI because their text says "delve"?
No. People use these words too, and the Wikipedia guide says not all text with these signs is AI-generated. Treat a hit as a reason to read closely, never as proof.

### Do AI detectors work better than a phrase list?
Wikipedia's guide says detection tools have "non-trivial error rates". A phrase list does not judge authorship at all; it only finds wording you decided not to publish, which is the builder's real need.

### Is "I hope this email finds you well" always bad?
It is not wrong, but it carries no information and readers know it as a template line. Start with the reason you are writing.

### Will asking ChatGPT to "sound human" fix it?
Usually not, by our reading: it swaps one set of stock words for another. Ban named phrases, give the model the facts, and run the scan.
