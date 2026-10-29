# Truth Social's "Truth Search AI" draws on a narrow, unlabeled set of news sources and contradicts the platform owner's public claims, August 2025

<!-- SEO
title: Truth Search AI: Narrow Unlabeled Sources, Owner Contradicted
description: Truth Social's Perplexity-powered Truth Search AI cited mostly Fox News without saying sources were limited, and its answers contradicted the platform owner's claims.
search phrases:
- truth social truth search ai sources
- perplexity source selection hidden from users
- ai search tool limited to a few news outlets
- chatbot contradicts the company that runs it
- answer engine source restriction not disclosed
-->

**This page is a dated teardown of one US social platform's AI answer tool, for teams that put a licensed answer engine inside their own product and restrict where it draws its answers.** The product was Truth Search AI, a search box on the web version of Truth Social, run by Trump Media and Technology Group (TMTG) and powered by Perplexity's technology. The users were Truth Social members asking news and fact questions. TMTG announced a "public Beta" on Aug. 6, 2025. Within days, Axios found the tool's answers cited a narrow set of mostly Fox News sources that the announcement never mentioned, and The Washington Post, The Telegraph and others reported answers that contradicted public claims by President Donald Trump, whose company runs the platform. The date in the title is the month of the launch and the first reports.

**Status: Needs review.** Built from seven pages, all downloaded on 2026-10-30 and read as text through a text-reader proxy (r.jina.ai); for Axios and The Telegraph we also read the page HTML to get the byline. (1) TMTG's press release on GlobeNewswire, Aug. 6, 2025, the primary launch statement. (2) Axios, by Ben Berkowitz, Aug. 6, 2025, which ran seven matched questions on Truth Social and on public Perplexity. (3) The Washington Post, by Drew Harwell, Aug. 10, 2025; only the headline, summary line and first two paragraphs were readable, the rest is behind a sign-in wall and unread. (4) The Telegraph, by Kieran Kelly per the page metadata, Aug. 11, 2025, read in its Yahoo News syndicated copy, which ran its own question. (5) Straight Arrow News (SAN), by Evan Hummel and Karah Rucker, Aug. 11, 2025, which retells the Post's findings, including its quotes from Perplexity and TMTG. (6) The Independent, by Anthony Cuthbertson, Aug. 12, 2025, read on AOL. (7) The Independent, by Brendan Rascius, Nov. 11, 2025, read on AOL, which retells a test by The Bulwark. Every quote below was checked word for word against the saved text with a script.

> **Read this first.** This page is design guidance, not legal advice and not a view on any political question, on Mr. Trump, on tariffs, elections or crime, or on which news outlets are reliable. It reports what news outlets and TMTG wrote. It makes no finding about TMTG, Truth Social, Perplexity or any person. We do not judge whether the tool's answers were right; the design failure we describe is that a source limit was applied without telling users, and that the tool's answers and its host's public messaging pulled in opposite directions with no label saying whose view the tool gave. We did not use the tool ourselves. We cannot say whether it still works this way.

**Channel note.** This is a text incident: a search and answer box on the web version of Truth Social, per the press release. The opened sources describe no voice version. This phase of the knowledge base is chat-first, and the signals and checks below are written for text chat logs. Voice and web signals are PLANNED only: never detected or measured here.

## What happened (as reported)

- **What was promised.** TMTG's release said Truth Search AI is "Powered by Perplexity" and would "exponentially increase the amount of information available to its users." Perplexity's business chief, quoted in the release, promised "direct, reliable answers with transparent citations that allow anyone to dig deeper." The release called it "public Beta testing" on the web version, with the iOS and Android apps to follow.
- **One outlet family in the citations.** Axios asked seven matched questions on a logged-in Truth Social account and on the free, logged-out Perplexity site. Its finding: "In all seven responses on Truth Social, FoxNews.com either was the most common, or the only, listed source of information." Other sources were Fox Business, the Washington Times or Epoch Times. Public Perplexity cited Wikipedia, Reddit, YouTube, NPR, Esquire and Politico, and "there was no source overlap."
- **The answers themselves were mostly the same.** Axios: "In most cases, the responses were generally similar — but the sources linked to the answers were not."
- **The limit was not announced.** Axios: "Truth Social did not mention any restrictions in its announcement." A Perplexity spokesperson told Axios that any customization, like limiting sources, "would happen entirely on the Truth Social side."
- **What Perplexity said about the limit.** Per SAN, Perplexity spokesperson Jesse Dwyer told the Post it is likely the tool uses a "source selection" feature, but he could not fully confirm it, since Perplexity does not monitor what clients do. His words, quoted by SAN: "This is their choice for their audience, and we are committed to developer and consumer choice."
- **Answers that contradicted the owner.** The Post's summary line says the tool "says the 2020 election wasn’t stolen, tariffs aren’t boosting the stock market and Barack Obama is seen favorably." Asked about Jan. 6, 2021, it called the riot violent and linked to Trump's "baseless claims of widespread election fraud," per the Post. Per SAN, asked about the president's tariff and stock market claim, it said "the evidence does not support the claim."
- **A newspaper's own test.** The Telegraph asked who is the most popular president of the century and got Barack Obama. It adds: "All five sources listed by the chatbot were Fox News."
- **TMTG's response.** Per SAN, the White House declined to comment on the Post's report, and TMTG spokesperson Shannon Devine called it one of the "transparently asinine stories" from "irrelevant partisan hacks." Axios and The Independent (Aug. 12) say TMTG did not respond to their requests for comment.
- **Three months later.** The Independent (Nov. 11) reports that The Bulwark asked five questions. Asked whether tariffs cost Americans money, the tool said "Yes" and that costs "are borne mainly by American businesses and consumers." We did not open The Bulwark's piece.

## Timeline

| Date | Event | Source |
|---|---|---|
| Aug. 6, 2025 | TMTG announces public Beta of Truth Search AI on Truth Social's web version | GlobeNewswire release |
| Aug. 6, 2025 | Axios publishes its seven-question comparison | Axios |
| Aug. 10, 2025 | The Washington Post reports the tool contradicting the president | Washington Post (partly read); SAN |
| Aug. 11, 2025 | The Telegraph runs its own question; SAN retells the Post, with TMTG's statement | Telegraph via Yahoo; SAN |
| Aug. 12, 2025 | The Independent reports; says TMTG did not respond to it | Independent via AOL |
| Nov. 11, 2025 | The Independent retells a five-question test by The Bulwark | Independent via AOL |

## Where the sources disagree or leave gaps

| Topic | What the sources say |
|---|---|
| Was a source limit confirmed? | Axios shows the pattern in citations. SAN says Perplexity called a "source selection" feature "likely" but could not confirm it. The Telegraph's copy says Truth Social "had used" the feature. No opened source has TMTG confirming or denying a limit. |
| Which sources were allowed | No opened source lists them. Axios saw Fox News, Fox Business, the Washington Times and Epoch Times; the Post, per SAN, saw Fox News, Newsmax and the Washington Times. |
| Were citations shown? | Axios and The Telegraph describe listed sources. SAN says the tool "didn’t specifically reveal which sources it had drawn its conclusions from." These may describe different things (links shown versus the pool they were picked from); we cannot tell. |
| Were answers "wrong"? | Not the claim of any opened source. The reports frame the answers as contradicting the platform's owner. We report that conflict, not a verdict on the facts. |
| Social media examples | The Independent mentions users sharing replies (Obama, the family's crypto ventures). We saw none of those posts. |

## Where in the flow it broke

1. **The source pool was narrowed with no label.** Answers came from a short list of outlets, while the public version of the same engine drew on many. Nothing in the opened sources shows the box telling users their answers came from a filtered pool.
2. **The launch promise did not match the setup.** The release promised "transparent citations." Citations were shown, but the rule that picked them was not, so a user could see links without knowing what had been left out.
3. **Same engine, different answer basis, same brand promise.** A user comparing Truth Search AI with Perplexity's site would get similar text built on sources with no overlap, per Axios, and no note saying why.
4. **The tool and its host pulled apart in public.** The answers contradicted the owner's public claims while the host's spokesperson attacked the reporting. No opened source shows a label in the box saying the answers do not speak for the platform, so users and the press read them as the platform's own voice.
5. **A "Beta" with no stated limits.** The release said the company would "refine and expand" the tool from feedback, but the opened sources show no note in the product about what the beta covered or left out.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it. Each fit rests on reporters' descriptions and quoted replies; we saw no chat logs.

- [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (`one-sided-or-cherry-picked-sources`). **Good fit** for the source side. Every Axios answer leaned on one outlet family, and the user was not told what was left out. The entry is written for research assistants that call a summary balanced; here the narrowing seems to have been a setting, not the model's choice, which makes it easier to disclose.
- [Undisclosed bot identity](../goals/trust-and-rapport/failures/undisclosed-bot-identity.md) (`undisclosed-bot-identity`). **Partial fit.** Users knew it was AI and that Perplexity powered it. What was hidden was a limit on what it could draw from, which the entry covers under bots that "hide their limits." The entry centers on bots that pass as human, which this did not.
- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Weak fit.** No opened source shows a wrong answer, and links were shown. The overlap is narrower: a user could check each link, but not the filter that chose them.
- **Considered, not a fit.** [Paid content blended into answers](../goals/embedded-copilots/failures/paid-content-blended-into-answers.md) (`paid-content-blended-into-answers`): no source reports payment for placement. [AI content farms posing as news sites](../goals/ai-slop-detection/failures/web-ai-content-farms-as-news.md) (`web-ai-content-farms-as-news`): the cited outlets are established news sites.

## How it differs from close cases

- [Realfood.gov sends users to Grok, February 2026](realfood-gov-nutrition-site-sends-users-to-grok-off-topic-answers-and-sign-up-wall-february-2026.md): there, too, a licensed general chatbot disagreed with the site that hosted it. Realfood.gov set no scope at all; Truth Social set a source limit but did not say so.
- [xAI's Grok "white genocide" replies, May 2025](xai-grok-white-genocide-replies-unauthorized-prompt-change-may-2025.md): a hidden instruction change pushed one topic into answers. Here the reported change was to sources, not to instructions, and the answers did not follow the owner's line.
- [Perplexity misstates and invents WIRED stories, June 2024](perplexity-answer-engine-misstates-and-invents-wired-stories-june-2024.md): the same engine, with errors about specific articles. On Truth Social, the reports concern which sources were used, not invented content.

## What to measure (proposed)

Proposed signals, not results. Status: Not yet run. Each can be computed from text chat logs and citation records the operator holds.

| Signal | How to compute from logs | Counter-signal |
|---|---|---|
| Source concentration | Per answer, share of cited links from the single most-cited domain; flag answers at 100% | Questions where one official source is the right answer |
| Source overlap with the base engine | For a fixed question set, share of cited domains shared with the unfiltered engine | Questions on topics the filter is meant to narrow on purpose |
| Filter disclosed in answer | Share of answers on a filtered pool that carry a visible line saying the sources are limited | None expected |
| Host-voice conflict | Share of answers on the operator's own public claims that a reviewer marks as disagreeing, with no label saying the answer does not speak for the operator | Answers that carry such a label |

## What a team can change

Our proposals, not TMTG's or Perplexity's. Each is a pass/fail check on a text log or a config. Status: Not yet run.

1. **Say the source limit where the answer is.** Pass: an answer drawn from a restricted list carries one line naming the limit and a link to the list. Fail: links shown with no word that the pool was filtered.
2. **Publish the list.** Pass: the allowed domains are listed on a page users can open. Fail: users must infer the list from citations.
3. **Make the launch copy match the setup.** Pass: if sources are filtered, the announcement says so. Fail: "transparent citations" with an unstated filter.
4. **Label whose voice it is.** Pass: the box says the answers are generated by the tool and do not state the platform's or its owner's positions. Fail: no label, so each reply reads as the platform speaking.
5. **Run a matched-question check before launch.** Pass: the team compares its filtered answers with the base engine on a fixed set and records source overlap. Fail: the first comparison is a newsroom's.

## A cheap test

Status: Not yet run. Write 20 questions: 10 on news topics, 5 on the operator's own public claims, and 5 neutral questions (sports, weather, movies). Ask each in the product and in the unfiltered base engine at the same time. Record the domains cited, the share from one outlet, whether any answer names a source limit, and whether any answer says it does not speak for the operator.

## What we could not verify

- The full text of The Washington Post's article, which is behind a sign-in wall. Its quotes from Perplexity and TMTG reach us through SAN and The Telegraph.
- The Bulwark's own article; we have only The Independent's retelling.
- Whether a source limit was set, which domains it allowed, and who chose them. No opened source has TMTG on the record about it.
- The exact dates each newsroom ran its questions, and how many questions the Post asked.
- Whether the tool, its sources or its labels changed after these reports, or whether it reached the mobile apps.
- Seen only in search summaries, and kept out of the page text: coverage by Newstalk ZB, Maldita.es, Il Foglio and WinFuture.
- Whether anyone acted on an answer and was harmed. No opened source reports harm.

## Sources

| Outlet / author | Date | URL | How opened |
|---|---|---|---|
| TMTG press release, GlobeNewswire | 2025-08-06 | https://www.globenewswire.com/news-release/2025/08/06/3128331/0/en/Trump-Media-Begins-Public-Beta-Testing-AI-Search-Engine.html | Text via r.jina.ai 2026-10-30, read in full |
| Axios, Ben Berkowitz | 2025-08-06 | https://www.axios.com/2025/08/06/trump-truth-social-perplexity | Text and HTML via r.jina.ai 2026-10-30, read in full |
| The Washington Post, Drew Harwell | 2025-08-10 | https://www.washingtonpost.com/technology/2025/08/10/truth-social-trump-ai-chatbot-perplexity/ | Text via r.jina.ai 2026-10-30; headline, summary and first two paragraphs only, rest unread |
| The Telegraph (Yahoo News copy), Kieran Kelly per page metadata | 2025-08-11 | https://www.yahoo.com/news/articles/trump-truth-social-ai-chatbot-090858203.html | Text and HTML via r.jina.ai 2026-10-30, read in full |
| Straight Arrow News, Evan Hummel and Karah Rucker | 2025-08-11 | https://san.com/cc/new-truth-social-ai-chatbot-contradicts-trumps-long-held-claims-report/ | Text via r.jina.ai 2026-10-30, read in full; secondary (retells the Post) |
| The Independent (AOL copy), Anthony Cuthbertson | 2025-08-12 | https://www.aol.com/news/trump-ai-chatbot-keeps-fact-190144098.html | Text via r.jina.ai 2026-10-30, read in full |
| The Independent (AOL copy), Brendan Rascius | 2025-11-11 | https://www.aol.com/news/trump-own-truth-social-ai-213636671.html | Text via r.jina.ai 2026-10-30, read in full; secondary (retells The Bulwark) |

## Corrections

If you have a newer test of Truth Search AI, its source list, or a statement from TMTG about how its sources are chosen, tell us and we will fix this page.
