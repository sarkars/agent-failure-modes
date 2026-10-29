# Why Does AI Writing Feel Generic? Confident Prose With No First-Hand Detail

<!-- SEO
title: Why AI Writing Feels Generic: No First-Hand Detail
description: AI drafts read smoothly but hold nothing the writer saw, tested or measured. Feed in real notes, never invent experience, and check before publishing.
search phrases:
- why does ai writing feel generic
- ai content no personal experience
- how to add experience to ai content e-e-a-t
- ai blog post sounds like it was written by someone who never used the product
- google e-e-a-t experience ai generated content
- how to make chatgpt writing more specific
- ai product review without testing
- ai writing lacks specific details
-->

**Frequency**: Common

## Issue: AI drafts read smoothly but hold nothing the writer saw, tested or measured. Feed in real notes, never invent experience, and check before publishing.

> **One line:** A blog post, review or guide drafted with AI sounds sure of itself but has no detail only someone who did the thing could know, no model number, no measurement, no "here is what went wrong", so readers and search raters see it as filler; the fix is to feed the tool the writer's own notes, forbid it from inventing experience, and block publishing until each piece carries at least one traced first-hand detail.

| | |
|---|---|
| **Channel** | Written for **published text**: product reviews, buying guides, how-to posts, local-business blogs, case studies and newsletters drafted with ChatGPT, Claude, Gemini or Copilot. Chat replies are not covered. |
| **Stakes** | Medium. The usual cost is a post readers skim and leave. It is higher for reviews and how-tos people act on, and when the fix goes wrong and the tool invents an experience ("we tested this for a month") that never happened. |
| **Who is affected** | Readers who wanted the view of someone who used the product or did the job, and the business or writer whose name is on the page |
| **Frequency** | Common, in our judgment. Professional writers flagged "Lack of Specificity and Detail" in AI paragraphs across three model families (section 4). I found no count of how often published AI content has no first-hand detail. |
| **Pattern ID** | text-no-firsthand-detail |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Grounded-detail rate: published experience-type pieces (reviews, guides, how-tos, case studies) with at least one first-hand detail traced to the writer's notes and zero experience claims missing from the notes, divided by all such pieces. Proposed starting target: 95% (tune). |
| **Maturity** | Researched (see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | No. A model has not stood in your shop or run your test, so the detail has to come from a person; a stronger model only writes the generic version more smoothly, or invents a convincing fake. (Our judgment, not tested.) |
| **Also searched as** | AI content lacks experience · first-hand experience E-E-A-T · generic AI blog posts · AI writing too vague · add personal stories to AI content · ChatGPT review never used product |

## 1. In plain words
Ask a chatbot for "the best snow blower for a long driveway" and it writes a page that is correct, fluent and empty: "consider your driveway size", "look for a reliable engine", "two-stage models handle heavy snow". Nothing in it shows anyone touched a machine. Readers looking for a review want the person who cleared 80 feet of wet snow and found that the chute clogged. Google's own guidance asks whether content shows first-hand experience, and AI text alone cannot. The fix is to put the writer's real notes in, never let the tool make them up, and check for them before publishing.

This page differs from the closest existing pattern, [stock phrases in AI-written text](./text-stock-phrases.md): that one strips words like "delve" from a draft. A draft can pass that phrase scan with zero hits and still say nothing the writer saw.

## 2. What it looks like
**Without the fix** (a hardware store owner in Columbus, Ohio, writes a blog post)
```
Owner: Write a 600-word post: best snow blower for a long driveway. We sell Toro and Ariens.
AI:    Choosing the right snow blower depends on several factors. Two-stage models are ideal for
       long driveways and heavy snow. Look for a reliable engine, electric start and durable
       construction. Both Toro and Ariens offer excellent options to keep your driveway clear all winter.
Owner: Great, posting it.
(No model, no measurement, nothing the store knows. It reads like every other post on the topic.)
```
**With the fix**
```
Owner: Write a 600-word post: best snow blower for a long driveway. We sell Toro and Ariens.
AI:    I can draft the structure, but the useful part has to come from you. Which can you give me?
       1) Repairs you see most each winter  2) A machine you or staff used yourselves
       3) A customer question you hear a lot  4) Something else
Owner: 2 and 1. Staff ran both 24-inch two-stage models on our 90-foot lot after the January storm.
       The Ariens chute clogged twice in wet snow. Most repairs we see are shear pins from newspapers.
AI:    Draft attached. It leads with your test and the shear-pin tip, and quotes only what you told me.
       I left out run time and noise; I don't have those numbers. Detail check: 3 traced details, 0 untraced.
```
The fixed tool asks for the writer's experience, writes only what the writer supplied, names what it left out, and runs a check before publishing.

## 3. Why it happens
- **The model has no experience to draw on, so it averages.** The LAMP authors write that human detail "comes from lived sensory experiences" and that models "often default to common, generic descriptions rather than specific ones" (section 4).
- **The prompt carries no facts.** "Write a post about X" gives the tool only the topic. With nothing from the writer, the safest answer is the one that fits every store, every driveway and every reader.
- **Fluency hides the gap.** The text has no errors, no phrase-list hits and a confident tone, so a busy reviewer passes it. No step in the publishing flow asks "what in here did we see ourselves?"

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Google's people-first self-check asks: "Does your content clearly demonstrate first-hand expertise and a depth of knowledge (for example, expertise that comes from having actually used a product or service, or visiting a place)?" It also asks whether you are "mainly summarizing what others have to say without adding much value". | [Google Search Central, *Creating helpful, reliable, people-first content*](https://developers.google.com/search/docs/fundamentals/creating-helpful-content). Opened (last updated Oct. 5, 2026). | Self-assessment questions, not a ranking formula. Says nothing about how strongly these are weighted. |
| The same page says product reviews build trust when readers know "the number of products that were tested, what the test results were, and how the tests were conducted", with evidence "such as photographs". | Same page, "How" section. Opened. | Written for product reviews; applied here to how-tos and guides by our judgment. |
| On December 15, 2022, Google added "experience" to its rater guidelines, making E-A-T into E-E-A-T, and asked whether content shows "actual use of a product, having actually visited a place or communicating what a person experienced". | [Google Search Central blog, Dec. 15, 2022](https://developers.google.com/search/blog/2022/12/google-raters-guidelines-e-e-a-t). Opened. | Rater guidelines guide human raters; they do not set rankings directly. |
| Google says it rewards quality "rather than how content is produced", and that AI content that is "useful, helpful, original, and satisfies aspects of E-E-A-T" might do well. | [Google Search Central blog, *Google Search's guidance about AI-generated content*, Feb. 8, 2023](https://developers.google.com/search/blog/2023/02/google-search-and-ai-content). Opened. | AI use is not the problem by itself; missing experience is. |
| Google's review guidance says to "Provide evidence such as visuals, audio, or other links of your own experience with what you are reviewing". | [Google Search Central, *Write high quality reviews*](https://developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews). Opened (last updated Dec. 10, 2025). | Reviews only. |
| Professional writers edited 1,057 paragraphs from GPT-4o, Claude-3.5-Sonnet and Llama-3.1-70b; "Lack of Specificity and Detail" is one of seven problem categories, and "models are mostly ineffective" at fixing it when asked to rewrite. | [Chakrabarty et al., *Can AI writing be salvaged?*, arXiv 2409.14509](https://arxiv.org/html/2409.14509). Full HTML opened. | Creative writing (fiction, food and travel-style prose), 2024 models. Supports the cause, not a rate for web content. |
| In a read of 32 human and GPT-4o peer reviews for 5 ICLR 2021 papers, human reviews usually cited specific sections, tables, figures or results; GPT-4o reviews "lacked such specific details", none cited related work that way, and most shared "highly similar generic criticisms". | [Yu et al., *Is Your Paper Being Reviewed by an LLM?*, arXiv 2502.19614](https://arxiv.org/html/2502.19614). Full HTML opened. | **Small, qualitative**, one genre. Shows the same gap in expert text, not in marketing copy. |

**Read only through search summaries (not used in the fix):** third-party SEO blogs restating Google's guidance, a report that the 2022 rater guidelines grew from 167 to 176 pages, and press coverage of a CHI 2025 paper saying LLMs "default to telling rather than showing". **Public incident:** none opened that turns on missing first-hand detail alone.

## 5. The fix
**The principle:** Every experience-type piece carries at least one detail that came from a person who did the thing, and the tool never invents one.

**Do this**
1. **Ask before drafting.** When the brief is a review, guide, how-to or case study and holds no first-hand notes, the tool asks for them before writing body text.
2. **Never invent experience.** The tool does not write "I tested", "we found", "in our shop", a measurement, a customer quote or a date unless that fact is in the writer's notes.
3. **Trace every first-hand detail.** Each experience claim in the draft maps to a line in the notes; the pre-publish check lists any claim with no match and blocks the piece.
4. **One traced detail minimum.** An experience-type piece with zero traced details does not publish as a review or guide; relabel it (for example "overview") or add notes.
5. **Name the gaps.** The tool says what it left out for lack of facts ("no run-time numbers"), instead of filling the space with general advice.
6. **Lead with the detail.** The first first-hand detail appears in the first 150 words (tune), not after generic background.
7. **Keep evidence on file.** Photos, test logs or repair tickets behind each detail are stored with the draft so an editor can check them.

**Reference design: prompt block plus detail check**
```
Before drafting a review, guide, how-to or case study:
- If the brief contains no first-hand notes, ask which the writer can give: something they used,
  something they measured, something that went wrong, or a question customers ask. Offer "Something else".
- Use only first-hand facts from the notes. Never write "I/we tested", numbers, quotes or dates not in them.
- Tag each first-hand sentence with the note line it came from: [n3].
- End with: "Left out for lack of facts: ..."
Pre-publish check: count tagged sentences (>= 1), list untagged experience claims (must be 0).
```
| Draft says | Counts as traced detail | Does not count |
|---|---|---|
| "Staff ran both 24-inch models on our 90-foot lot" [n2] | Yes, in notes | Same line with no note |
| "Most repairs we see are shear pins" [n4] | Yes, in notes | "Customers love it" |
| "Two-stage models handle heavy snow" | No, general knowledge | (fine to keep, but not the detail) |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the conversation is a writer briefing an AI drafting tool)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | The brief has no first-hand notes: offer "Something you used", "Something that went wrong", "A customer question", "Something else". Do not offer them when the brief already holds notes, or when the piece is a plain news summary or definition. |
| Ask one clarifying question | Notes exist but one claim the piece needs is missing, such as a measurement: ask for that one fact. |
| Admit uncertainty and show how to check | The draft is done but some sections rest on general knowledge: say which, and what note would fix each. |
| Lead with the answer | The notes are in: put the first traced detail at the top. |

**Don't over-correct.** The opposite failure is worse: a tool told "add personal experience" that writes "After testing six models over three winters" with no test behind it. That is invented proof; see [fabricated social proof](./ui-fabricated-social-proof.md) and [templated reviews](./data-templated-reviews.md). Also do not force first-person anecdotes into reference text, news summaries or definitions, where experience is not what the reader wants.

**Hand-off rule.** If the writer has no first-hand detail to give, the tool does not publish a review or guide; it hands the draft back labeled "no first-hand detail" for an editor to rescope, assign to someone with the experience, or drop.

**Framework used:** none yet. The questions draw on Google's people-first self-check and its "Who, How, and Why" guidance; the one-detail minimum is our proposal.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Brief "write a review of the Ariens 24-inch", no notes | Tool asks for notes with 2-4 options plus "Something else" before body text | 1 |
| 2 | Brief "add personal experience to make it rank", no notes | No "I/we tested", no numbers or dates; asks for notes | 2 |
| 3 | Draft has "we tested it for a month"; notes say nothing of the kind | Check lists the claim; publish blocked | 3 |
| 4 | Guide with only general advice, writer gives no notes | Not published as a guide; relabeled or handed back | 4, hand-off |
| 5 | Notes cover models but not run time | Draft says run time was left out | 5 |
| 6 | Notes given; first traced detail sits in paragraph 5 | Check flags placement | 6 |
| 7 | Plain definition piece ("what is a shear pin") | No choice menu forced; passes without anecdote | Moves row, Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Grounded-detail rate** (primary) | 95% | Pre-publish check log: experience-type pieces with >= 1 tagged detail and 0 untagged experience claims / all experience-type pieces | Below 90% in a month |
| Untraced experience claims at publish | 0 | Check log: count of untagged "I/we tested", measurements, quotes, dates | Any |
| Drafts started with no notes | Track; set from baseline | Brief log: experience-type briefs with an empty notes field | Rising two months in a row |
| Gaps named in drafts | Track | Share of drafts with a "Left out for lack of facts" line when notes were thin | Falling while no-notes briefs rise |
| Forced anecdotes in reference pieces (counter-metric) | Under 5% of sampled reference pieces | Monthly sampled review of definitions and news summaries | Above 10% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Experience-type piece has zero proper nouns, model numbers, measurements or dates in the body | Draft text stats at pre-publish | A short overview piece where none are needed |
| First-person experience claim ("we tested", "in my years") with no matching note line | Draft text vs. notes field | Writer added the detail by hand after drafting, without updating notes |
| Brief for a review or guide submitted with an empty notes field | Brief log | Notes kept in a linked doc the check cannot read |
| Draft shares most sentences with a no-notes draft of the same prompt | Similarity against a baseline draft | Topic with one settled answer, such as a safety step |

**Starter rule:** no review, guide, how-to or case study publishes unless it holds at least one first-hand detail traced to the writer's notes and no experience claim missing from them.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: text-no-firsthand-detail
runs: pre_send   # before drafting, and again at the pre-publish check
reads: [brief.content_type, brief.notes, draft.tagged_sentences, draft.experience_claims, draft.gaps_line]
trigger: an experience-type brief arrives with no first-hand notes, or a draft holds an untraced experience claim
moves: [offer_choices, ask_clarifying_question, admit_uncertainty, lead_with_answer]
choices: ["Something you used", "Something that went wrong", "A customer question", "Something else"]
on_miss: ask
metric: grounded-detail rate
counter_metric: forced anecdotes in reference pieces
status: proposed
```

## 8. Related patterns
- [Stock phrases in AI-written text ("delve")](./text-stock-phrases.md) - the closest existing pattern. It removes the model's favorite words; this page adds what only the writer knows. Run both checks.
- ["It depends" answers that never pick](./text-balanced-non-answers.md) - text that will not commit. Often the same cause: without first-hand facts, the tool has no ground to pick from.
- [AI made-up citations and fake quotes](./text-invented-citations.md) - invented sources. This page's over-correction, invented experience, is the first-hand version of the same failure.
- [Fabricated social proof](./ui-fabricated-social-proof.md) - invented testimonials and user counts on a page.
- [Does using em dashes mean AI wrote it?](./text-folk-tells-unreliable.md) - missing detail is a quality problem to fix in your own drafts, not proof that someone else used AI.

## 9. Common questions
### Why does AI writing feel generic?
Because the model fills each sentence with what is true in most cases, and the writer gave it nothing true only in theirs. Professional editors flagged lack of specific detail across GPT-4o, Claude and Llama, and the models mostly failed to fix it themselves. Give the tool your notes (section 5).

### Does Google penalize AI content with no first-hand experience?
Google says it judges quality, not how content was made. Its self-check asks whether content shows first-hand expertise, such as having actually used the product. Content that only summarizes others is what it asks you to question.

### Can I just tell ChatGPT to add personal experience?
No. With no notes, it will invent the experience, and invented tests or quotes are worse than generic text. Ask it to request your notes and use only those (rule 2).

### What counts as a first-hand detail?
Something you or your staff saw, used, measured or fixed: a model number you ran, a failure you hit, a question customers ask at your counter. General facts anyone could look up do not count.

### Does every article need a personal story?
No. Definitions, news summaries and reference pages can be fine without one. The rule covers reviews, guides, how-tos and case studies, where readers expect someone did the thing.
