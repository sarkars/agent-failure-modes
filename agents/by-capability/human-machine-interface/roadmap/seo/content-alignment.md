# Aligning Search Queries to Our Content

> **Superseded (2026-10-19): the audience is now developers. See [developer-search-plan.md](developer-search-plan.md). This consumer-oriented mapping is kept as a record.**

> **What this is.** A mapping from real search suggestions (see [queries.md](queries.md)) to the content this library already has, with an honest rating of how well our content answers each query. It shows where a search asset can be written now, where research is missing, and where our content does not fit and should not be forced. The queries are Google autocomplete suggestions pulled on 2026-10-19; they are not volumes. Written 2026-10-19.

## How to read the fit
- **Strong:** our existing content answers what a searcher is likely to want, with sources I opened. A search asset can be written from it now.
- **Partial:** we have the explanation but not the fix or how-to the query probably wants. Research is needed before a page.
- **Weak:** the query wants something we do not have (a vendor fix, a user workaround). Do not write a page that implies we do.

## The mapping, in order of how ready each is
| # | Target query (as suggested) | Cluster | Reader | Our content that answers it | Fit | What is missing |
|---|---|---|---|---|---|---|
| 1 | ai drive thru mistakes | AI drive-thru | Curious reader, restaurant operator | [Order mix-ups at the speaker](../../goals/drive-thru-agents/failures/order-mix-ups-at-the-speaker.md); site incident page on McDonald's | **Strong** | Needs a plain timeline (McDonald's, Taco Bell, Wendy's) with what each source says; accuracy figures stay marked unverified |
| 2 | airline chatbot lawsuit | Airline and bank chatbots | Curious reader, customer-service lead | Site incident page on Air Canada; [Confident wrong answer with no way to check](../../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) | **Strong** | Open the ruling or a legal summary beyond the site page; no legal advice; flag L |
| 3 | chatgpt is lazy | ChatGPT forgets, memory, lazy | ChatGPT user | [Lazy completion](../../goals/effort-and-memory/failures/lazy-completion.md); [GPT-4 Turbo laziness incident](../../incidents/openai-gpt-4-turbo-laziness-reports.md) | **Strong** | The sources are about 2023 to 2024; the query may refer to newer models, so say what the sources cover and when |
| 4 | chatgpt memory full | ChatGPT forgets, memory, lazy | ChatGPT user | [No warning of context loss](../../goals/effort-and-memory/failures/no-warning-of-context-loss.md); [ChatGPT memory incident](../../incidents/chatgpt-memory-missing-memories-november-2025.md) | **Partial** | Our evidence describes the problem, not how to clear memory; a how-to needs the vendor's own help page, which I have not opened |
| 5 | chatgpt forgets instructions | ChatGPT forgets, memory, lazy | ChatGPT user | [No warning of context loss](../../goals/effort-and-memory/failures/no-warning-of-context-loss.md); the long-context research it cites | **Partial** | Why it happens is covered (context limits, middle-of-context loss); practical fixes for users are not yet researched |
| 6 | how to get past automated phone systems | Reach a human | Caller | [Talk to a human ignored or looped](../../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md); [CFPB doom loops incident](../../incidents/cfpb-bank-chatbot-doom-loops.md) | **Partial** | Our content is for builders. A caller's guide needs sourced tips (for example regulator guidance); none gathered yet |
| 7 | chatbot fallback message | Builders | Builder | [Dead-end "I don't understand" replies](../../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md) | **Strong** | Reframe as a how-to with example messages; the pattern's research already supports it |
| 8 | ai agent failure modes | Builders | Builder | [Gap analysis](../gap-analysis.md); [per-agent-type gap analysis](../agent-type-gap-analysis.md); the library's patterns | **Partial** | MAST and others already rank for this; our angle is the human-facing failures, with the tested-behaviors list from the [L0 spec](../l0-base-spec.md) |
| 9 | alexa doesn't understand my accent | Voice assistants | Smart-speaker user | [Repair failure](../../goals/voice/failures/repair-failure.md) | **Weak** | Our pattern is a design guide; the query wants a user fix or an explanation of accent bias, which I have not researched |
| 10 | can't cancel a subscription | Cancel or refund blocked | Consumer | [Obstructing cancellation](../../goals/embedded-copilots/failures/obstructing-cancellation-downgrade-or-refund.md); the FTC and Amazon incident | **Partial** | Flagged L; consumer how-to needs regulator pages I could not open; no legal advice |
| 11 | chatgpt something went wrong | ChatGPT errors | ChatGPT user | [Generic error messages](../../goals/errors-and-recovery/failures/generic-error-messages.md) | **Weak** | The query wants a fix or outage status. We only explain why messages are vague; do not claim to fix a vendor's product |

## What this shows
- **Four of eleven queries have a Strong match and five a Partial one; two are Weak.** The Strong ones are where we already hold a sourced incident or a researched pattern: AI drive-thru mistakes, the airline chatbot lawsuit, ChatGPT being lazy, and chatbot fallback messages. Those are the first pages to write.
- **The patterns are written for builders, but most queries come from people using a product.** A search asset for those readers is a different page from a pattern: shorter, answer first, in plain words, with the pattern linked for the builder who wants depth.
- **We have no content for "how do I fix it" queries** (ChatGPT errors, phone-menu tips, accent problems, memory clearing). Those need new, sourced research, and a page there must not read as support for a product we do not run.
- **Builder queries match well** ("chatbot fallback message", "ai agent failure modes"), but are fewer and more competitive.

## What a search asset looks like here (proposed, one page per row)
1. **Title is the query phrase**, written as a person types it.
2. **The first two sentences answer it,** with the source named.
3. **A short, sourced explanation** from the opened sources, and what is not known.
4. **One next step for the reader** (what to try, what to ask for, or what a builder should do).
5. **A link to the pattern, incident, and test** for depth.
6. **A record of the query evidence** in [queries.md](queries.md), and a note when Search Console data replaces it.

## Open decisions for the owner
- Who the first assets are for: people using a product (most queries) or builders (best fit to our content).
- Whether to write about vendors' products (ChatGPT, airlines, restaurants) at all, and under what accuracy and legal rules; rows 2, 6, and 10 are flagged for review.
- Search Console access or an export, so these suggestions can be replaced by real impressions.

## Related
- [Search queries](queries.md) · [SEO README](README.md) · [Content program](../content-program.md) · [L0 base spec](../l0-base-spec.md)
