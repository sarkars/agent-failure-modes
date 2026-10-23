---
title: "Google's Gemini Super Bowl Ad Says Gouda Is '50 to 60 Percent' of the World's Cheese Consumption, February 2025"
date: 2025-02-07
source: "https://www.fortune.com/2025/02/09/google-gemini-ai-super-bowl-ad-cheese-gouda"
summary: "A Google Workspace with Gemini ad made for the February 2025 Super Bowl showed Gemini writing a gouda description for Wisconsin Cheese Mart that said gouda accounts for 50 to 60 percent of the world's cheese consumption. Critics called it false. Google's Jerry Dischler said it was not a hallucination because web sites carried the figure, and the ad was quietly edited to drop the number."
categories:
  - Governance
  - Accuracy
patterns:
  - confident-wrong-answer-with-no-way-to-check
---

**This page is a dated teardown of one wrong number in an AI ad, for teams that show an assistant's drafts in a demo, an ad or a product page, or that let users publish AI-written copy as their own.** Every fact below comes from a page we opened (listed at the end). Where we only have a second-hand account, we say so.

**Status: Needs review.** Every source was read through a fetch-tool summary, not as a full page. Quotes from Fortune, Android Central and WPR were checked in a second fetch of the same page; the WISN, 9to5Google and McGraw Hill wording was not re-checked. We could not open Google's or Dischler's own posts, The Verge, Business Insider or the Wayback Machine, so details seen only there or in search summaries are listed under "What we could not verify" and kept out of the claims.

## What happened (as reported)

- **The campaign.** 9to5Google (Abner Li, January 30, 2025) reported that "Google Workspace with Gemini" would get Super Bowl airtime, with a different commercial in each of the 50 states spotlighting a local small business. Fortune (Irina Ivanova, February 9, 2025) describes "50 videos—one for each state—featuring customers using its Workspace software suite."
- **The Wisconsin spot.** Android Central (Brady Snyder, February 8, 2025, via Yahoo) gives the ad's title as "Wisconsin Cheese Mart: Gemini in Google Docs." WPR (Hope Kirwan, February 7, 2025) says Wisconsin Cheese Mart is a Milwaukee shop owned by Ken McNulty. WISN 12 (Paula Vansack, February 7, 2025) says McNulty uses AI to write product descriptions for his shop.
- **The claim.** In the early version, per Fortune, the Gemini copy said gouda "is one of the most popular cheeses in the world, accounting for 50 to 60 percent of the world's cheese consumption."
- **The call-out.** Fortune and WISN report that travel blogger Nate Hake called the claim "unequivocally false" on X. Fortune quotes him: "Cheddar & mozzarella would like a word."
- **What experts said, per Fortune.** Cornell agricultural economist Andrew Novakovic: "While Gouda is likely the most common single variety in world trade, it is almost assuredly not the most widely consumed." Fortune says Matt Herrick of the International Dairy Foods Association cited USDA data ranking mozzarella, then cheddar and cream cheese, as the most popular U.S. cheeses, with gouda not in the top 10.
- **Where the text came from.** Fortune says Wisconsin Cheese Mart first published the figure on its own website. WPR reports McNulty said the statistic was "pulled from another website," not made up by Gemini. Android Central says the same text appeared in the shop's website description "as early as 2020," linking a Wayback Machine snapshot dated 2020 by its URL. We could not open that snapshot.
- **The edit.** Fortune says the ad "has been quietly edited to remove the number." The new line, per Fortune: "Gouda, a Dutch cheese, is one of the most popular cheeses in the world." Android Central: "Google quietly edited the advertisement to remove the incorrect claim from Gemini's response." WPR says McNulty asked Google to change the ad after hearing about the mistake.
- **Timing.** McGraw Hill's education blog (February 10, 2025, credited to "NickelsMcHughMcHugh") says the error surfaced "just days before the big game" and that Google corrected the ad before it aired. No other opened source states the order this clearly.

## What Google said

- **Jerry Dischler, on X.** Fortune names him as Google's president of cloud applications and quotes his reply to Hake: "Hey Nate—not a hallucination," then "Gemini is grounded in the Web—and users can always check the results and references. In this case, multiple sites across the web include the 50-60% stat." Android Central quotes the same "not a hallucination, Gemini is grounded in the Web."
- **Spokesperson Jenny Thomson, per Fortune.** "To clarify, the AI didn't hallucinate, it drew on a website that was wrong." She said Google, following the shop owner's suggestion, "updated the UI to reflect what the business would do."
- **What Google did not say, in opened sources.** No opened source quotes Google on whether Gemini wrote the shown text in a live session, which site it drew on, or whether any citation was shown to the user in Docs.

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| Who wrote the line | Google says Gemini drew on a wrong website. Fortune says the shop's own site carried the figure. Android Central's headline says the response was "faked entirely" for the ad, based on the 2020 snapshot. No opened source settles it. |
| When the ad changed | McGraw Hill says before it aired. Fortune and Android Central say "quietly edited" with no date. |
| Product name | 9to5Google: "Google Workspace with Gemini." Android Central: "Gemini in Workspace" and "Gemini in Google Docs." |

## Where in the flow it broke

Based on the reports, and only as far as they go:

1. **The request.** A shop owner uses the assistant to write a product description.
2. **The draft.** The draft states a precise world market share as fact, inside ordinary sales copy. No opened source describes a source link or hedge next to it.
3. **The source.** Per Google, the number came from "a website that was wrong." A figure from that page was treated as good enough to repeat.
4. **The review.** The opened reports describe the error being flagged publicly by a blogger, not caught in Google's or the shop's review.
5. **The response.** Google's first public answer argued about the word "hallucination" and pointed to the web, and put the check on users ("users can always check"). The fix was to delete the number.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- **[Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md)** (`confident-wrong-answer-with-no-way-to-check`). Strong fit for what viewers saw: a wrong number stated flatly, with no visible source or doubt. Dischler's "users can always check the results and references" is the very gap that page names: a check only helps if the screen shows it. The one gap in the fit: if the line was copied from the shop's 2020 page, the failure is the ad's, not the model's.
- **Considered, weak fit.** [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (`one-sided-or-cherry-picked-sources`). Google's account is that Gemini relied on a weak web source. That pattern is about a research summary that hides disagreement, not a marketing draft, so we do not list it.
- **Related incident.** [Google's Bard launch demo and the Webb telescope claim](google-bard-launch-demo-wrong-jwst-claim-february-2023.md), an earlier Google showcase with a wrong fact in the example answer.

## What to measure

Our proposals, not Google's. Status: Not yet run.

| Metric | How to compute from logs |
|---|---|
| Unsourced-number rate | Drafts that contain a percentage, ranking or market share with no source shown next to it, divided by drafts with any such figure |
| Single-source fact rate | Factual figures in drafts backed by only one retrieved page, divided by all figures backed by retrieval |
| Showcase fact-check rate | Ad, demo or launch examples whose factual claims were checked against a primary source before release, divided by all such examples |

## What a team can change

Our proposals, each a pass/fail check on a transcript. Status: Not yet run.

1. **Numbers carry a source on screen.** Ask for a product description that invites a statistic. Pass: any figure in the draft has a visible source link, or the draft leaves the figure out.
2. **No market share from one page.** Pass: a "percent of the world" style figure appears only when two independent sources agree, or it is marked as unverified.
3. **Flag the risky line to the writer.** Pass: the draft view highlights factual claims the user should confirm before publishing.
4. **Check showcase copy like ad copy.** Pass: every factual claim in a demo or ad script has a logged check against a primary source before release.
5. **Don't over-correct.** Pass: plain descriptive copy ("smoky, nutty, aged") is not hedged or footnoted.

## What we could not verify

- Dischler's X post itself, and its date. X returned HTTP 402; we rely on Fortune's and Android Central's quotes.
- The Verge's reporting, which search summaries say first flagged the issue and traced the figure to a low-quality site. Our fetch tool could not open theverge.com.
- Business Insider's report and a quoted Google spokesperson line about consulting the owner. The Business Insider page redirected to its home page.
- That cheese.com carries the same figure. Seen only in search summaries.
- The 2020 Wayback Machine capture of the shop's gouda page. Our fetch tool could not open web.archive.org.
- Ars Technica's point that the new video replaced the old one at the same YouTube URL. Seen only in search summaries; Boing Boing, which quoted it, returned HTTP 403.
- The exact air date and whether the original version ever aired on TV.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://www.fortune.com/2025/02/09/google-gemini-ai-super-bowl-ad-cheese-gouda | Fortune (Irina Ivanova) | 2025-02-09 | Yes, 2026-10-23, fetch-tool summary; quotes re-checked |
| https://www.yahoo.com/news/googles-incorrect-gemini-response-actually-003802460.html | Android Central via Yahoo (Brady Snyder) | 2025-02-08 | Yes, 2026-10-23, fetch-tool summary; quotes re-checked |
| https://wpr.org/news/wisconsin-cheese-mart-super-bowl-ad-commercial-google | WPR (Hope Kirwan) | 2025-02-07, updated 2025-02-08 | Yes, 2026-10-23, fetch-tool summary; quotes re-checked |
| https://www.wisn.com/article/entertainment-milwaukee-cheese-market-in-super-bowl-ad/63704585 | WISN 12 (Paula Vansack) | 2025-02-07 | Yes, 2026-10-23, fetch-tool summary |
| https://9to5google.com/2025/01/30/google-workspace-gemini-super-bowl-2025/ | 9to5Google (Abner Li) | 2025-01-30 | Yes, 2026-10-23, fetch-tool summary |
| https://tech.yahoo.com/general/articles/google-fumbles-gemini-super-bowl-000000805.html | TechRadar via Yahoo (Eric Hal Schwartz) | 2025-02-08 | Yes, 2026-10-23, fetch-tool summary; no direct Dischler quote, so used only as background |
| https://www.mheducation.com/highered/blog/2025/02/google-corrects-its-ai-super-bowl-ad-before-the-game | McGraw Hill blog ("NickelsMcHughMcHugh") | 2025-02-10 | Yes, 2026-10-23, fetch-tool summary; used only for timing |
| https://www.techradar.com/computing/artificial-intelligence/google-fumbles-gemini-super-bowl-ads-cheese-statistic | TechRadar | 2025-02 | Opened, but returned only navigation text |
| https://www.businessinsider.nl/google-tweaks-super-bowl-ad-that-showed-its-ai-giving-an-incorrect-answer-about-gouda-cheese/ | Business Insider | Not known | No. HTTP 301 to home page |
| https://boingboing.net/2025/02/07/googles-ai-generated-super-bowl-ad-is-no-gouda-and-gets-a-secret-re-edit.html | Boing Boing | 2025-02-07 | No. HTTP 403 |
| https://www.aol.com/google-tweaks-super-bowl-ad-220454345.html | AOL copy | Not known | No. HTTP 404 |
| The Verge article (URL not confirmed) | The Verge | Not known | No. Fetch tool blocked |

## Corrections

If you have Dischler's post, Google's dated statement, or proof of who wrote the original line, tell us and we will fix this page.
