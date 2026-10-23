---
title: "X's Grok Turns Basketball Slang Into a False Trending Story That Klay Thompson Vandalized Houses, April 2024"
date: 2024-04-16
source: "https://www.engadget.com/xs-ai-bot-is-so-dumb-it-cant-tell-the-difference-between-a-bad-game-and-vandalism-172707401.html"
summary: "After Klay Thompson went 0 for 10 in the Warriors' April 16, 2024 play-in loss to the Sacramento Kings, Grok wrote a story for X's trending section saying he had been accused of vandalizing houses in Sacramento with bricks. The claim was false; fans had joked that he was 'throwing bricks,' slang for missed shots. Engadget reported it as the #5 trending story, under a notice that Grok 'can make mistakes.'"
categories:
  - General-Purpose Assistants
  - Governance
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - profanity-and-slang-handling
  - false-premises-accepted
---

**This page is a dated teardown of one public incident in which an AI feature turned sports jokes into a false news story about a named person, for teams that let a model write headlines or summaries from user posts and show them to the public.**

**Status: Needs review.** Built from five news reports and one incident database entry, all opened as raw page text. Not from a test of the feature, and not from any statement by X or xAI.

> **Read this first.** This is a summary of public reports, not a finding of fact. It involves a real person who was falsely described. Klay Thompson was not accused of vandalism and did not vandalize anything; every source we opened says the story was false. We repeat the false text only as far as needed to show what the feature produced. Nothing here is legal advice. Every fact below comes from a source we opened (listed at the end).

## What happened (as reported)

- **Tuesday, April 16, 2024: the game.** The Golden State Warriors lost to the Sacramento Kings in the NBA Play-In Tournament, ending their season (Awful Announcing, Sportskeeda, Engadget). Thompson missed all 10 of his shots and did not score (Awful Announcing, Engadget, Sportskeeda). The AI Incident Database dates the incident to 04/16/2024.
- **The jokes.** In basketball slang, a badly missed shot is a "brick." Engadget says users posted that Thompson was "shooting bricks." Futurism says fan accounts of the Kings and the Los Angeles Lakers sarcastically accused him of "throwing bricks." Futurism quotes one Lakers fan account's mock report that its house was "vandalized by bricks" and that the culprit was Thompson. Awful Announcing says the story was "apparently fueled" by a viral post from a Lakers fan account. Sportskeeda says "several NBA satire accounts" began reporting him for vandalism.
- **The story Grok wrote.** Engadget (April 17) says Grok "generated a trending story" claiming Thompson was vandalizing homes with bricks. Engadget, Futurism and Awful Announcing quote the same opening text, which began "In a bizarre turn of events, NBA star Klay Thompson has been accused of vandalizing multiple houses with bricks in Sacramento." In the same quoted text the story said authorities were investigating, windows had been shattered, Thompson had not issued a statement, no one was hurt, and the motive "remains unclear." None of this was true.
- **The headline.** Awful Announcing says the trending topics tab described a "Bizarre Brick-Vandalism Spree." No other source we opened gives a headline.
- **Where it ranked.** Engadget says it was "the #5 trending story at the time of writing." The Decoder says Grok placed it at number five on the trending list.
- **How long it stayed.** Futurism (April 19) says the story had "been live for days" and was "still live" at the time of writing.
- **The notice.** Engadget says fine print beneath the story read "Grok is an early feature and can make mistakes. Verify its outputs." Futurism quotes a notice reading "This story is a summary of posts on X and may evolve over time" and "Grok can make mistakes, verify its outputs."
- **The reaction.** Engadget says fans began "memeing" on the story with posts that sarcastically verified it. Sportskeeda quotes fans mocking it.
- **Not a one-off, per two outlets.** The Decoder's original April 15 article describes Grok turning user jokes about the solar eclipse into a news report. Awful Announcing says the feature had also published inaccurate headlines about NASCAR, professional wrestling and O.J. Simpson's death. We did not check those cases.

## What X and xAI said

Nothing, in any source we opened. No outlet we read quotes X, xAI or Elon Musk on this story, or says it was corrected or removed. The only words from X are the on-screen notice quoted above. The Decoder notes that X "does point out" the feature can generate errors.

## Where the sources disagree

- **The notice text.** Engadget (April 17) quotes "Grok is an early feature and can make mistakes. Verify its outputs." Futurism (April 19) quotes a notice that the story "is a summary of posts on X and may evolve over time." Awful Announcing (April 17) matches Engadget. The sources do not say whether the notice changed between those dates or whether two notices were shown.
- **Who started the joke.** Awful Announcing points to one Lakers fan account. Futurism names fan accounts of both the Kings and the Lakers. Sportskeeda says "several NBA satire accounts." The sources do not say which posts Grok actually used.
- **Which product.** Sportskeeda calls it "Twitter AI" and never names Grok. Engadget, Futurism, Awful Announcing, The Decoder and the AI Incident Database name Grok.
- **The incident date.** The AI Incident Database uses April 16, the game date. No source gives the time the story first appeared; Engadget's "last night" framing on April 17 suggests it appeared on the night of the game or the next morning, but no source says so.

## What we could not verify

- **The story itself.** We did not see the trending story or the screenshots. We rely on the text that three outlets quote identically.
- **Why it happened.** The outlets say Grok misread the slang. That is their reading; X and xAI have not explained it in any source we opened. The sources do not explain how stories were picked, written or ranked.
- **Reach.** No source gives views, the time the story stayed in the top five, or how many users saw it.
- **Correction or removal.** No opened source says when, or whether, the story was taken down or corrected, or whether Thompson or the Warriors responded.
- **X's help text.** We did not open any X help page describing how AI-written trending stories work. The notice wording above comes only from the news reports.
- **Search-only claims.** Search summaries mentioned an Ars Technica report, an SF Gate report (both cited by Futurism), a Yahoo copy of the Futurism story, and coverage by Mashable, Gizmodo and The Verge. We opened none of them, and nothing above relies on them. A final score appeared in a search summary and in a related-story teaser on the Sportskeeda page, not in its article; it is not used.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All three Pattern IDs below appear in it.

- [Confident wrong answer with no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Strong fit.** The story stated a crime accusation, a police investigation and broken windows in a flat news voice, with no named source a reader could open. The only cue of doubt was a general notice under every story. It differs from the pattern page in one way: no user asked a question. The feature pushed the claim to everyone browsing the trending section.
- [Profanity and slang handling](../goals/language-and-locale/failures/profanity-and-slang-handling.md) (`profanity-and-slang-handling`). **Partial fit.** The page covers a bot that misreads everyday slang. "Shooting bricks" is sports slang, and the reports say the model read it literally. It is partial because the page is about replying to one user's message, and its main concern is profanity, not slang inside third-party posts used as source material.
- [False premises accepted](../goals/dialogue-management/failures/false-premises-accepted.md) (`false-premises-accepted`). **Weak fit.** The joke posts asserted something untrue, and the feature repeated it as fact instead of checking. It is weak because the pattern is about a user's question that assumes something false, not about posts the system gathered on its own.
- **Considered, not a fit.**
  - [Typos, shorthand, and noisy input](../goals/language-and-locale/failures/typos-shorthand-and-noisy-input.md): the posts were not misspelled; the problem was meaning and sarcasm, not noise.
  - [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md): the feature did not pick sides in a dispute. It took jokes as facts.
  - [Handoff summary is wrong or misleading](../goals/human-handoff/failures/handoff-summary-is-wrong-or-misleading.md): it is about a summary handed to a human agent, not one published to the public.
  - [Excess disclaimers and warnings](../goals/refusals-and-boundaries/failures/excess-disclaimers-and-warnings.md): there was one notice, not too many. The issue is that a general notice sat under a specific false accusation.
  - [Missing the obvious intent](../goals/embedded-copilots/failures/missing-the-obvious-intent.md): no user made a request whose meaning was missed.
- **Possible gaps for a person to judge.** (1) No pattern covers an AI that writes news-style stories from user posts and publishes them unasked to everyone. (2) No pattern covers sarcasm, jokes and memes in source material being taken as fact. (3) No pattern covers a false accusation of a crime against a named, real person by an assistant; the defamation incidents in this folder are matched to general patterns too. (4) No pattern covers a general "can make mistakes" notice standing in for review of a high-stakes claim. These are proposals, not decisions.

## Where in the conversation flow it broke

This reconstruction uses the reports only. X has not published how the feature works.

1. **Input.** Fans post jokes after a bad game, some written as mock police reports.
2. **Reading.** The feature, per the reports, reads the slang and the mock reports literally. No source shows a check for sarcasm or for whether any news outlet reported a crime.
3. **Writing.** Grok writes a news-style story. Some details, such as police and a broken window, appear in the joke post Futurism quotes. Others, such as no statement from Thompson and no injuries, do not appear in any post quoted by the sources.
4. **No gate for accusations.** A story that accuses a named person of a crime is published with no sign of human or automated review in any source.
5. **Ranking.** The story reaches #5 in the trending section, per Engadget.
6. **Notice instead of a source.** Readers get a general "can make mistakes" line, not a link to the posts the story came from.
7. **Users can't correct it.** Fans' sarcastic replies "verifying" the story added more joke posts about the same claim. No source says a report or correction path existed or was used.

## Related incidents

- [Google AI Overviews odd and unsafe answers, May 2024](google-ai-overviews-odd-and-unsafe-answers-may-2024.md): a search feature also surfaced joke or satirical content as fact, weeks later.
- [Apple Intelligence notification summaries misreport news headlines, December 2024](apple-intelligence-notification-summaries-misreport-news-headlines-december-2024.md): an AI summary told the public something false about a named person under a trusted label.
- [ChatGPT false embezzlement claim, Walters v. OpenAI, May 2025](chatgpt-false-embezzlement-claim-walters-v-openai-defamation-ruling-may-2025.md) and [ChatGPT false claims about a person, noyb complaint, March 2025](chatgpt-false-claims-about-a-person-noyb-complaint-march-2025.md): an assistant invented a crime about a real person. There it answered one user; here it was pushed to every trending-tab reader.
- [Grok wrong ballot deadline answers, August 2024](xai-grok-wrong-ballot-deadline-answers-august-2024.md), [Grok "white genocide" replies, May 2025](xai-grok-white-genocide-replies-unauthorized-prompt-change-may-2025.md) and [Grok antisemitic posts after an update, July 2025](xai-grok-antisemitic-posts-after-update-july-2025.md): later public failures of the same product on X.

## What to measure

Proposed metrics; none come from X, xAI or the sources. Status: Not yet run. Thresholds are for the team to set; we propose none.

| Metric | How to compute from logs |
|---|---|
| Accusation rate | Generated stories that say a named person did, or is accused of, a crime, divided by all generated stories |
| Unsupported accusation rate | Of those, stories where no linked source post is from a news outlet or official body the team lists, divided by all accusation stories |
| Detail not in sources | Factual claims in a story (investigation, injuries, statements) that appear in none of the source posts, divided by all factual claims checked |
| Sarcasm-cluster flag | Stories whose source posts the team's joke or sarcasm check flags as a majority, divided by all stories |
| Time to takedown | For stories later marked false, time from first display to removal |

## What a team can change

Proposed rules, each a pass/fail check on a generated story or a test run. Status: Not yet run.

1. **Hold crime claims about named people.** Pass: a story that says a named person committed or is accused of a crime is not shown until a person reviews it, or until it cites a source on the team's list of news outlets and official bodies.
2. **Never add facts the posts lack.** Pass: every factual claim in a story (investigation, injuries, statements) can be traced to a quoted source post; a claim with no trace is removed.
3. **Test on slang and jokes.** Pass: a test set built from sports slang ("bricks"), mock police reports and other jokes produces no story that states the joke as fact.
4. **Show where it came from.** Pass: each story links to the posts it summarizes, so a reader can see they were jokes.
5. **Write the notice for the claim.** Pass: a story built mostly from posts flagged as jokes or unverified says so in the story text, not only in a general notice.
6. **Give readers a report button that reaches a person.** Pass: a "this is false" report on a story about a named person is logged and reviewed, and the review outcome is recorded.
7. **Don't over-correct.** Pass: ordinary sports stories ("Thompson goes 0 for 10 as Warriors are eliminated") still publish without review.

## Sources

| Source | Author | Date | URL | How it was read |
|---|---|---|---|---|
| Engadget, "X's AI bot is so dumb it can't tell the difference between a bad game and vandalism" | Sam Rutherford | 2024-04-17 | https://www.engadget.com/xs-ai-bot-is-so-dumb-it-cant-tell-the-difference-between-a-bad-game-and-vandalism-172707401.html | Raw HTML read as text, fetched 2026-10-24; story text, notice, #5 rank and 0-for-10 checked |
| Futurism, "Elon Musk's AI Publicly Accuses NBA Player of Criminal Vandalism" | Victor Tangermann | 2024-04-19 | https://futurism.com/the-byte/elon-musk-ai-accuses-nba-player-criminal-vandalism | Raw HTML read as text, fetched 2026-10-24; quotes, notice and "still live" checked |
| Awful Announcing, "X/Twitter's AI accuses Klay Thompson of vandalism with bricks after 0-10 performance" | Ben Axelrod | 2024-04-17 | https://awfulannouncing.com/twitter/klay-thompson-vandalism-bricks-ai.html | Raw HTML read as text, fetched 2026-10-24; headline, story text and notice checked; linked X post not opened |
| Sportskeeda, "This actually happened": NBA fans in splits as Twitter AI accuses Klay Thompson of brick vandalism | Juan Paolo David | Modified 2024-04-17 | https://www.sportskeeda.com/basketball/news-this-actually-happened-nba-fans-splits-twitter-ai-accuses-klay-thompson-brick-vandalism-following-0-for-10-outing | Raw HTML read as text, fetched 2026-10-24; game details and "satire accounts" checked |
| The Decoder, "Elon Musk's Grok AI chatbot turns viral X jokes into fake news" | Matthias Bastian | 2024-04-15, updated 2024-04-20 | https://the-decoder.com/elon-musks-grok-ai-chatbot-turns-viral-x-jokes-into-fake-news/ | Raw HTML read as text, fetched 2026-10-24; April 20 update and April 15 eclipse example checked |
| AI Incident Database, Incident 1183 | Editor: Daniel Atherton | Incident date 2024-04-16; ID created 2025-08-22 | https://incidentdatabase.ai/cite/1183/ | Raw HTML read as text, fetched 2026-10-24; description, date and cited Engadget report checked |

Not opened: Ars Technica, SF Gate, Yahoo, Mashable, Gizmodo, The Verge, X's help pages, and the X posts the reports link to. These appeared only as search results or links and are not used above.

## Corrections

This page needs review. If you have X's or xAI's account of how the story was made, when it came down, or how trending stories were reviewed in April 2024, tell us and we will fix this page.
