---
title: "Google AI Overviews Explains Made-Up Idioms as Real Sayings"
date: 2025-04-23
source: "https://www.wired.com/story/google-ai-overviews-meaning/"
description: "In April 2025, Google AI Overviews explained invented sayings like you can't lick a badger twice as real idioms, and Google cited false premise searches."
summary: "In April 2025, people found that typing a made-up phrase plus the word meaning into Google Search often produced an AI Overview that explained the phrase as a real idiom, with a meaning and sometimes an origin. The best-known example was you can't lick a badger twice, posted on Bluesky by historian Greg Jenner on April 23, 2025. Google said nonsensical or false premise searches have little web content to draw on and that it works to limit AI Overviews on such data voids. No harm to a user was reported. Status: Needs review."
categories:
  - Search
  - Accuracy
  - Trust
patterns:
  - false-premises-accepted
  - confident-wrong-answer-with-no-way-to-check
---

**This page is a dated teardown of one public answer-engine incident, for teams that let an AI write a short answer at the top of a search, help or dictionary page.** It was a viral game, not a report of harm to one user. Every fact below comes from a source we opened (listed at the end).

**Status: Needs review.** On 2026-10-30 we downloaded each cited article as raw HTML, stripped it to text, and matched every quote below against that text. Three articles (Business Insider, CNET and Futurism) were read as syndicated copies on Yahoo Tech; Mashable was also read on Yahoo Tech, and that copy names no author. We did not open the original social posts on Threads or Bluesky; we know them only through the articles.

## What happened (as reported)

- **The trick.** Wired (Brian Barrett, April 23, 2025) describes it: type any made-up phrase into Google, add the word "meaning," and search. AI Overviews would often treat the phrase as a real saying and explain it.
- **Where it started.** Futurism (Victor Tangermann, April 23) and CNET (Jon Reed, April 25) say it may have started with a Threads post by author Meaghan Wilson-Anastasios. Futurism says she posted "over the weekend" and that her search for "peanut butter platform heels" returned a made-up story about a "scientific experiment."
- **The badger.** Android Authority (Aamir Siddiqui, April 24) embeds a Bluesky post by historian Greg Jenner dated April 23, 2025 at 3:45 PM (time zone not stated). Jenner told Business Insider (Katie Notopoulos, April 25) the phrase "just popped into my head." Futurism quotes the overview: "The idiom 'you can't lick a badger twice' means you can't trick or deceive someone a second time after they've been tricked once."
- **More examples.** Wired lists "a loose dog won't surf" and "wired is as wired does," and says the overview gave "never throw a poodle at a pig" a biblical origin. Futurism got a meaning for a phrase built from its own author's name. Business Insider got meanings for "You can't fit a duck in a pencil" and "The road is full of salsa." CNET got one for "blew up like a brook trout."
- **Tone.** Wired says the answers were "delivered with unwavering confidence" and that Google "even provides reference links in some cases, giving the response an added sheen of authority."
- **A clue on the page.** Android Authority says the same results page also said no results were found for the exact string. The only warning it saw was a note that "Generative AI is experimental."
- **Not every time.** Mashable (April 24) got "AI Overview is not available for this search." for one made-up phrase but a meaning for the next. CNET's search for "like glue on pizza meaning" did not trigger an overview. Gary Marcus told Wired his tests were "wildly inconsistent."
- **Other assistants.** Business Insider and CNET each asked ChatGPT about the badger phrase. Both say ChatGPT first said it was not a standard idiom, then offered a playful meaning anyway.

## What Google said

Google spokesperson Meghann Farnsworth gave this statement to Wired, Business Insider and others: "When people do nonsensical or 'false premise' searches, our systems will try to find the most relevant results based on the limited web content available." She added that "in some cases, AI Overviews will also trigger in an effort to provide helpful context." (Wording as printed by Business Insider; Wired and Android Authority differ only in punctuation and capitals.)

Android Authority's update of April 24 prints a longer version. It adds that AI Overviews "are designed to show information backed up by top web results, and their high accuracy rate is on par with other Search features like Featured Snippets." Android Authority and CNET also report, in their own words, that Google calls these cases "data voids," where little relevant content exists online, and that Google works to limit AI Overviews on them. Google's accuracy claim is its own; no opened source tests it.

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| Who started it | Futurism and CNET point to Meaghan Wilson-Anastasios on Threads. Android Authority credits Greg Jenner on Bluesky, whose own post says someone on Threads noticed it first. Business Insider says Jenner saw people talking about it on Threads. |
| Limits on data voids | Android Authority says Google "has rolled out improvements" to limit overviews on data voids. CNET says Google "is working on limiting" them. Neither gives a date or a test. |
| How often it happened | No source gives a rate. Wired, Mashable and CNET each saw some made-up phrases get no overview. |
| What changed after | No opened source reports a later change made because of this episode. |
| The model | CNET names Gemini as the model behind AI Overviews. Google's statement does not name a model. |

## Where in the flow it broke

1. **The query.** The user asks "X meaning," which assumes X is a real saying. The query carries a false premise.
2. **The lookup.** There is little or nothing on the web for X. Android Authority says the page itself showed no results for the exact string.
3. **The trigger.** An overview appears anyway. Google says overviews can "trigger in an effort to provide helpful context."
4. **The answer.** The model writes a fluent meaning and sometimes an origin, in the same voice it uses for real idioms. It does not say the phrase is unknown.
5. **The display.** The overview sits above results, sometimes with links, with only a general "experimental" note.

The cost reported is trust, not injury. Business Insider calls it "very low-stakes"; CNET says it "doesn't center on actionable advice"; Wired says it "seems ultimately harmless."

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- **[False premises accepted](../goals/dialogue-management/failures/false-premises-accepted.md)** (`false-premises-accepted`). Strong fit. Asking for the meaning of a phrase assumes the phrase exists. The overview accepted that and answered instead of saying the phrase is not a known saying. Google's own statement calls these "false premise" searches. The stakes here were low, which the pattern page allows for trivia.
- **[Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md)** (`confident-wrong-answer-with-no-way-to-check`). Strong fit on tone, partial on "no way to check." Wired reports "unwavering confidence" and no cue of doubt beyond a general disclaimer. But Wired says links appeared in some cases, and Android Authority says the page showed no exact-match results, so a careful user had some way to check.
- **Considered and rejected.** [Invented citations and quotes](../goals/ai-slop-detection/failures/text-invented-citations.md) (`text-invented-citations`): weak. The overviews invented meanings and origins, not citations, and that page covers writers publishing AI drafts. [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (`one-sided-or-cherry-picked-sources`): not matched. The problem was having almost no sources, not leaving out ones that disagree.
- **Possible gap for a person to judge.** No pattern covers answering into a data void: the system has no evidence for the thing asked about and writes an answer anyway. `false-premises-accepted` covers it when the query states a false assumption, but not when the user simply asks about an obscure or unknown term. This is a proposal, not a decision.

## Related incidents

- [Google AI Overviews odd and unsafe answers (May 2024)](google-ai-overviews-odd-and-unsafe-answers-may-2024.md): the launch-month problems with glue on pizza and eating rocks. Google then named nonsensical queries and data voids as causes and listed fixes; this episode, a year later, hit the same kind of query.
- [AI assistants misrepresent news: EBU and BBC study (October 2025)](ai-assistants-misrepresent-news-ebu-bbc-study-october-2025.md): found that assistants rarely refused and seldom said what was not known.
- [Google AI Overviews misleading health answers on liver tests (January 2026)](google-ai-overviews-misleading-health-answers-liver-tests-guardian-january-2026.md): the same feature in a higher-stakes topic.

## What to measure

Proposed signals, not results. Status: Not yet run.

| Signal | How to compute from logs |
|---|---|
| Made-up term answer rate | Run a fixed list of invented phrases with "meaning"; share that get an explanation instead of "not a known phrase" or no overview |
| Real term answer rate | Same run on a list of real idioms; share that still get a correct explanation (guards against over-blocking) |
| Zero-evidence trigger rate | Overviews shown when exact-match web results for the key phrase are zero, divided by all overviews on "meaning" queries |
| Invented origin rate | Answers that state a source or origin (biblical, a region, an era) for a phrase on the invented list |
| Consistency | Same invented phrase run 5 times; share of runs whose behavior (explain or decline) matches the first run |

## What a team can change

Our proposals, not Google's. Each is a pass/fail check on a transcript or results page. Status: Not yet run.

1. **Check the term exists before defining it.** If the phrase has no exact-match evidence, do not write a meaning. Pass: every phrase on a 50-item invented list gets no definition.
2. **Say so plainly.** When declining, say the phrase is not a known saying, as ChatGPT did per Business Insider and CNET. Pass: the reply contains a "not a known phrase" statement, not only silence.
3. **Mark guesses as guesses.** If the product offers a playful reading, label it as a guess before the text. Pass: any meaning given for an invented phrase is preceded by a guess label.
4. **No made-up origins.** Pass: no answer on the invented list names a source, era or culture for the phrase.
5. **Do not over-block.** Pass: real idioms, including rare regional ones, still get a correct meaning on a held-out list.
6. **Show the evidence state.** If exact-match results are zero, say that next to the answer, not only lower on the page. Pass: the answer box shows the evidence note whenever exact-match results are zero.

## What we could not verify

- Greg Jenner's and Meaghan Wilson-Anastasios's original posts. Not opened; described only through the articles.
- Engadget's coverage, which Android Authority cites. Not opened.
- Lily Ray's post on X calling it "AI-splaining," reported by Mashable. Not opened.
- Coverage seen only in search summaries (Search Engine Land, SAN, Engage Web, Doug Belshaw's blog and an aggregator site). Not used.
- Whether Google changed anything because of this episode, and when overviews stopped explaining the badger phrase, if they did.
- Google's claim that AI Overviews accuracy is on par with Featured Snippets. No opened source tests it.

## Sources

| URL | Publisher (author) | Date | Opened |
|---|---|---|---|
| https://www.wired.com/story/google-ai-overviews-meaning/ | Wired (Brian Barrett) | 2025-04-23 | Yes, 2026-10-30, raw HTML read as text |
| https://tech.yahoo.com/articles/t-lick-badger-twice-googles-181718841.html | Futurism via Yahoo Tech (Victor Tangermann) | 2025-04-23 | Yes, 2026-10-30, raw HTML read as text |
| https://www.androidauthority.com/google-search-ai-overviews-idiom-hallucination-3547757/ | Android Authority (Aamir Siddiqui) | 2025-04-24 | Yes, 2026-10-30, raw HTML read as text |
| https://tech.yahoo.com/articles/google-ai-overviews-explain-nonsense-170455727.html | Mashable via Yahoo Tech (no author shown) | 2025-04-24 | Yes, 2026-10-30, raw HTML read as text |
| https://tech.yahoo.com/ai/articles/googles-ai-answers-keep-telling-173023397.html | Business Insider via Yahoo Tech (Katie Notopoulos) | 2025-04-25 | Yes, 2026-10-30, raw HTML read as text |
| https://tech.yahoo.com/articles/googles-ai-overviews-badger-licking-120021614.html | CNET via Yahoo Tech (Jon Reed) | 2025-04-25 | Yes, 2026-10-30, raw HTML read as text |

## Corrections

If you have the original Threads or Bluesky posts, a Google statement on later changes, or a better date, tell us and we will fix this page.
