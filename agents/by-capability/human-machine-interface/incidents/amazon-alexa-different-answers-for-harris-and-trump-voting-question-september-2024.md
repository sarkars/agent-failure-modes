---
title: "Amazon Alexa gives reasons to vote for Harris but declines the same question about Trump, September 2024"
date: 2024-09-03
source: "https://variety.com/2024/digital/news/alexa-vote-trump-kamala-harris-amazon-error-1236128793/"
summary: "On September 3, 2024, videos shared on social media showed Amazon Alexa declining to say why someone should vote for Donald Trump while listing reasons to vote for Kamala Harris. An Amazon spokesperson called it an error that was quickly fixed. Senator Lindsey Graham and House Judiciary Committee Chair Jim Jordan wrote to Amazon's CEO. In October 2024, Fox Business reported, citing one unnamed source, that Amazon told House Judiciary staff it had manual overrides for Biden and Trump but not for Harris."
categories:
  - Governance
  - General-Purpose Assistants
patterns:
  - one-sided-or-cherry-picked-sources
  - dialect-and-name-quality-gap
  - refusal-with-no-reason-or-next-step
  - confident-wrong-answer-with-no-way-to-check
---

**This page is a dated teardown of one public incident in which a voice assistant answered the same question differently for two presidential candidates, for developers building assistants that get asked about elections, candidates or other contested topics.** Every fact below comes from a source we opened (listed at the end). The cause rests on one unnamed source quoted by Fox Business; Amazon did not explain the cause in any statement we opened.

**Status: Needs review.** Variety, The Register, Fox News and two Fox Business articles were downloaded as raw HTML and read as plain text. Each quote below was checked word for word against that text. The sources use curly quote marks; we use straight ones. Details we saw only in search summaries are listed under "What we could not verify" and kept out of the claims.

**Read this first.** This is design analysis of a product consistency failure. It takes no political side and makes no claim about anyone's intent. It is not legal advice. Have your own counsel and policy team review how your assistant handles election content.

## What happened (as reported)

- **The product.** Amazon Alexa, the voice assistant on Echo speakers and other Amazon devices. The user speaks a question and Alexa answers aloud.
- **The videos.** Variety (Todd Spangler, September 3, 2024) says that "On Tuesday" (September 3) users on social media shared videos of Alexa answering "Why should I vote for Donald Trump?" and "Why should I vote for Kamala Harris?" differently.
- **The Trump answer.** Variety quotes Alexa: "I cannot provide content that promotes a specific political party or a specific candidate." The Register (Brandon Vigliarolo, September 4, 2024), citing a Fox Business video, quotes a different wording: "I cannot provide responses that endorse any political party or its leader." Fox News (Julia Johnson, September 4, 2024) quotes the answer Fox News Digital got: "I cannot promote content that supports a certain political party or a specific politician." It added a line saying it could not give information about U.S. government policies.
- **The Harris answer.** Variety says Alexa "in some cases" gave a detailed list of reasons. In one video Variety quotes, Alexa called Harris a "strong candidate with a proven track record of accomplishment." Fox News quotes another answer that began "While there are many reasons to vote for Kamala Harris," and said "she is a woman of color who has overcome numerous obstacles to become a leader in her field."
- **The answers varied.** Variety and Fox Business say Fox News Digital found the responses depended on the model of Amazon device. The sources quote at least three different refusal wordings and several different Harris answers.
- **After the fix.** Fox Business (Eric Revell and Hillary Vaughn, September 12, 2024) says that once Amazon addressed the issue, Alexa answered the Harris question with "I cannot provide content that promotes a specific political party or specific candidate," as Fox News Digital confirmed at the time.
- **Senate letter.** Fox News says Senator Lindsey Graham, ranking member of the Senate Judiciary Committee, wrote to Amazon CEO Andrew Jassy putting him "on notice that I will not allow this to go unaddressed." He asked for a "prompt reply as to what happened here and what corrective actions will be taken in the future."
- **House letter.** Fox Business (September 12, 2024) says House Judiciary Committee Chair Jim Jordan wrote to Jassy that day. The letter, as quoted, said "Recent reporting has indicated that Amazon may now be selectively censoring information about the 2024 presidential election on Alexa." It asked for a staff briefing and for answers on, among other things, how Amazon learned of the issue, how long it lasted, and how Amazon generated the Harris content before the fix. Fox Business says Jordan tied the request to a February 2023 committee subpoena to Amazon.
- **The briefing, per one source.** Fox Business (Eric Revell, Hillary Vaughn and Chase Williams, October 24, 2024) reports, citing "a source familiar with the briefing," that Amazon briefed House Judiciary staff. Per that source:
  - Alexa answers some prompts with pre-programmed manual overrides written by Amazon's information team.
  - Before the video, Amazon had overrides for Biden and Trump only. It had not added Harris "because very few users were asking Alexa about reasons to vote for her."
  - From July 21 (when Harris entered the race) to September 2, users asked for reasons to vote for Trump 14,000 times and for Harris 225 times.
  - Alexa generated the Harris response before any override existed for her.
  - Amazon learned of the issue within one hour of the video going viral and added a Harris override within two hours of it going up.
  - Amazon apologized and said that "obviously we are here today because we did not meet that bar in this incident."
  - Amazon has since audited the system and has overrides for all candidates and a number of election-related prompts.

## What Amazon said

- **The statement.** To Variety, The Register and Fox News, an Amazon spokesperson said: "This was an error that was quickly fixed."
- **More, per Variety and The Register.** Amazon said it makes continual changes to its systems for detecting and blocking content that violates its policies, and has teams dedicated to preventing similar situations. The Register says Amazon gave no further detail on why the disparity happened. Fox Business (September 12) says Amazon also told Fox News Digital that Alexa does not have political opinions.
- **At the briefing.** Only through Fox Business's unnamed source (above). We found no on-record Amazon statement about overrides, query counts or the cause.
- **What no opened source says.** Which software produced the Harris answers. Whether Amazon tested the overrides against every candidate before the fix. Whether Amazon answered Graham or Jordan in writing.

## Where in the conversation flow it broke

Based on the Fox Business source's account, and only as far as it goes:

1. **The request.** The user asked a voice assistant a persuasion question about a named candidate. The same template, "why should I vote for X," was asked for two candidates.
2. **The routing.** Per the source, a hand-written override list caught this question for some names. Names on the list got a fixed refusal. Names not on the list fell through.
3. **The stale list.** The candidate field changed on July 21. Per the source, Harris was not added because few users asked about her. The list tracked traffic, not the set of candidates.
4. **The fallback.** For a name off the list, Alexa generated an answer. That answer argued for the candidate in Alexa's own voice, with no source and no sign it was an opinion.
5. **The asymmetry.** One user, one template, two names, two policies. Neither answer, heard alone, shows the user that the other candidate is treated differently.
6. **Device and wording drift.** The refusal itself came in at least three wordings, and answers varied by device. No single reply could tell a user what the rule was.
7. **The fix.** Per the source, the fix was another override, then an audit adding overrides for all candidates. The rule still depends on someone keeping a list current.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). No pattern in this taxonomy covers "same question, different named subject, different policy," so no fit is strong.

- [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (`one-sided-or-cherry-picked-sources`). Partial fit. The Harris answers gave only the case for one side, in the assistant's voice, with no counterpoint or source. It is partial because that page is about a research assistant citing sources; Alexa cited none, and the deeper failure was the mismatch across two answers, not one answer's balance.
- [Dialect and name quality gap](../goals/fairness-and-identity/failures/dialect-and-name-quality-gap.md) (`dialect-and-name-quality-gap`). Partial fit. Its fix, paired tests that change only one name and compare outcomes, is exactly the test that would have caught this: swap "Trump" for "Harris" and compare. It is partial because that page is about the user's own name or dialect, not the name of the subject asked about.
- [Refusal with no reason or next step](../goals/refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md) (`refusal-with-no-reason-or-next-step`). Weak fit. The refusals named a policy but, in the wordings quoted, offered no next step, such as where to find candidate positions. It is weak because a refusal was Amazon's stated intent, and the incident was about where the refusal was missing.
- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). Weak fit. The Harris answers stated persuasive claims in the same sure tone as a fact, with no source. It is weak because the problem was not a checkable wrong fact but an answer the product's own policy said it should not give.
- **Considered, not a fit.** [Over-refusal of ordinary requests](../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md): the Trump refusal matched Amazon's stated policy, so it was not over-refusal by the product's own rule. [Silent sandbagging](../goals/refusals-and-boundaries/failures/silent-sandbagging.md): the refusals said they were refusals. [Excess disclaimers and warnings](../goals/refusals-and-boundaries/failures/excess-disclaimers-and-warnings.md), [Preachy, moralizing replies](../goals/refusals-and-boundaries/failures/preachy-moralizing-replies.md) and [Refusals that reveal internal rules](../goals/refusals-and-boundaries/failures/refusals-that-reveal-internal-rules.md): none of the quoted answers show these.
- **Possible gap for a person to judge.** This taxonomy has no pattern for a guardrail that applies to some named entities and not others, so the same request gets a different policy by name. A related gap: a hand-kept list of names that goes stale when the real-world set changes, as the candidate field did on July 21. These are proposals, not decisions.

## Related incidents

- [xAI Grok wrong ballot deadline answers (August 2024)](xai-grok-wrong-ballot-deadline-answers-august-2024.md): after the same July 2024 change in candidates, Grok gave a wrong fact about ballot deadlines. That was a wrong civic fact. This case is an inconsistent policy across two candidates, with no single checkable fact at stake.
- [Microsoft Copilot wrong election answers (December 2023)](microsoft-copilot-wrong-election-answers-december-2023.md): researchers found factually wrong answers about European elections through systematic testing. This case surfaced through viral videos of a paired question, and the issue was treatment, not accuracy.
- [Meta AI Trump shooting answers (July 2024)](meta-ai-trump-shooting-answers-july-2024.md): Meta set its assistant not to answer about one event, and some answers wrongly denied it happened. Both cases involve a deliberate rule not to answer; there the rule's fallback produced false denials, here the rule's coverage missed one name.

## What to measure

Our proposals, not Amazon's. Status: Not yet run. Thresholds are ones the team sets; we propose none.

| Metric | How to compute from logs |
|---|---|
| Paired-subject disagreement rate | Pairs of test prompts that differ only in the named candidate or party, where one gets a refusal and the other a substantive answer, divided by all pairs |
| Policy coverage gap | Candidates on an official current ballot list who have no matching rule in the election policy layer, divided by all candidates on that list |
| Fallthrough rate on election prompts | Election-related prompts answered by the general generator instead of the election policy path, divided by all election-related prompts |
| Refusal wording drift | Distinct refusal texts returned for the same prompt template across devices and versions, counted per template |
| Persuasion-in-own-voice rate | Answers that argue for or against a candidate without attributing the argument to a named source, divided by all candidate answers |

## What a team can change

Our proposals, each a pass/fail check on a transcript. Status: Not yet run.

1. **One rule per topic, not per name.** Pass: the election policy triggers on the question type ("why should I vote for X") for any person, not on a list of names. A test with a made-up candidate name gets the same treatment as a real one.
2. **Paired tests before release and on every change.** Pass: for each prompt template, every pair of candidates in the current race gets the same kind of response (both refuse, or both answer in the same format).
3. **Tie name lists to the real ballot, not to traffic.** Pass: when an official candidate list changes, an alert fires and the paired tests rerun the same day. No candidate is left off because few users ask about them.
4. **Safe fallback for unmatched political prompts.** Pass: an election prompt that matches no rule gets the refusal or neutral answer, not a freely generated one.
5. **Same words everywhere.** Pass: the refusal text for a given template is identical across devices and app versions.
6. **A next step in the refusal.** Pass: the refusal names a neutral place to compare candidates, such as each campaign's own site or an official voter guide, the same for every candidate.
7. **Don't over-correct.** Pass: factual questions such as "when is the election" or "who is running for president" still get direct answers.

## What we could not verify

- **The Washington Post's report on the cause.** Search summaries say a September 5, 2024 Washington Post article, citing internal documents, blamed software called "Info LLM" added to Alexa in late 2023, and reported other politics-related errors. The page (https://www.washingtonpost.com/technology/2024/09/05/amazon-alexa-ai-trump-harris-election-bias/) did not load for us. We keep this out of the claims.
- **Graham's letter itself.** The Senate Judiciary Committee PDF returned 403. We rely on Fox News's quotes from it.
- **Jordan's letter itself.** We did not find it on the House Judiciary Committee's site in search; we rely on Fox Business's quotes.
- **The briefing.** All details come from one unnamed source via Fox Business. No opened source has an on-record account from Amazon or the committee.
- **VERIFY's own test.** Search summaries say VERIFY (on KGW and KENS5) tested Echo devices and confirmed the difference. Both pages returned 403.
- **AllSides' test.** A search summary says AllSides found the results not always reproducible. The page returned 403.
- **A Trump campaign spokesperson's comment.** Seen only in search summaries.
- **Whether Alexa still refuses all candidate questions.** A Fox Business photo caption says it does; we found no later test.
- **How many users heard the Harris answers.** No opened source says, and we give no number.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://variety.com/2024/digital/news/alexa-vote-trump-kamala-harris-amazon-error-1236128793/ | Variety (Todd Spangler) | 2024-09-03 | Yes, 2026-10-23, raw HTML read as text; quotes checked word for word |
| https://www.theregister.com/2024/09/04/error_amazon_alexa_k/ | The Register (Brandon Vigliarolo) | 2024-09-04 | Yes, 2026-10-23, raw HTML read as text; quotes checked word for word |
| https://www.foxnews.com/politics/lindsey-graham-puts-amazon-on-notice-over-alexas-potential-election-interference | Fox News (Julia Johnson) | 2024-09-04 | Yes, 2026-10-23, raw HTML read as text; quotes checked word for word |
| https://www.foxbusiness.com/politics/rep-jim-jordan-requests-amazon-briefing-over-alexas-trump-censorship | Fox Business (Eric Revell, Hillary Vaughn) | 2024-09-12 | Yes, 2026-10-23, raw HTML read as text; quotes checked word for word |
| https://www.foxbusiness.com/politics/amazon-alexas-pro-harris-responses-werent-pre-programmed-source | Fox Business (Eric Revell, Hillary Vaughn, Chase Williams) | 2024-10-24 | Yes, 2026-10-23, raw HTML read as text; quotes checked word for word. Relies on one unnamed source |
| https://www.washingtonpost.com/technology/2024/09/05/amazon-alexa-ai-trump-harris-election-bias/ | The Washington Post | 2024-09-05 | No; request timed out. Not used for claims |
| https://www.judiciary.senate.gov/download/graham-letter-to-amazon-ceo?download=1 | Senate Judiciary Committee (Sen. Lindsey Graham) | 2024-09 | No; 403. Not used for claims |
| https://www.kgw.com/article/news/verify/elections-verify/yes-amazon-alexa-gave-reasons-to-vote-for-harris-but-not-trump/536-f7c694a1-2a95-42df-8123-7af16106798d | VERIFY via KGW | 2024-09 | No; 403 (KENS5 copy also 403). Not used for claims |
| https://www.allsides.com/blog/alexa-responds-trump-harris-questions-differently | AllSides | 2024-09 | No; 403. Not used for claims |

## Corrections

If you have Amazon's or the House Judiciary Committee's own account of the briefing, the text of either letter, or a dated test of Alexa's current answers, tell us and we will fix this page.
