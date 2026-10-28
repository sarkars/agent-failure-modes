---
title: "Amazon Alexa tells users the 2020 election was stolen, citing Rumble and Substack, October 2023"
date: 2023-10-07
source: "https://www.washingtonpost.com/technology/2023/10/07/amazon-alexa-news-2020-election-misinformation/"
description: "How Alexa told users in October 2023 that the 2020 election was stolen, citing Rumble and Substack, and why blocking only flagged questions fell short."
summary: "On October 7, 2023, The Washington Post (Cat Zakrzewski) reported that Amazon's Alexa, asked about fraud in the 2020 presidential race, said it was stolen, citing Rumble, quoted Substack on irregularities, and said Trump won Pennsylvania, citing an Alexa Answers contributor. Amazon called the answers errors delivered a small number of times and quickly fixed. After The Post contacted Amazon, the flagged questions got a refusal, but other questions still produced fraud claims. Senator Amy Klobuchar and Representative Joseph Morelle wrote to Jeff Bezos on October 19, 2023. In June 2024 The Post found Alexa still gave odd answers to variations of the question."
categories:
  - Trust and accuracy
  - General-Purpose Assistants
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - false-premises-accepted
  - one-sided-or-cherry-picked-sources
  - refusal-with-no-reason-or-next-step
---

**This page is a dated teardown of public reporting that Amazon's Alexa told users the 2020 US presidential election was stolen, for teams building voice or chat assistants that answer factual questions from web, licensed or user-contributed sources.** The product was Amazon Alexa, the voice assistant on Echo speakers and other devices. The users were people asking Alexa about the 2020 election. The moment was early October 2023, when The Washington Post found that some questions about fraud got a spoken answer that the election was stolen, with a named source such as Rumble. Every fact below comes from a source we opened (listed at the end). No opened source has Amazon's logs, its source lists, or the exact questions The Post asked.

**Status: Needs review.** We opened and read as plain text: The Washington Post's October 7, 2023 article by Cat Zakrzewski, from two Internet Archive snapshots (October 8 and October 19, 2023), because the Post's own site refused our requests; The Post's June 16, 2024 follow-up by Caroline O'Donovan and Cat Zakrzewski, from an Internet Archive snapshot of June 17, 2024; the October 19, 2023 letter from Senator Amy Klobuchar and Representative Joseph Morelle, as a PDF hosted by Reclaim The Net (the Senate site returned 403); and coverage that relays The Post from Audacy (Stephanie Raymond), The Daily Beast via Yahoo (Kelly Weill), Raw Story (David McAfee), The Decoder (Matthias Bastian), Reclaim The Net (Tom Parker), Straight Arrow News, and short excerpts at Election Law Blog, Daring Fireball, Political Wire and Electoral-vote.com. All were downloaded on 2026-10-28. Each quote below was checked word for word against that text; the sources use curly quote marks and we use straight ones. Every news account we opened traces back to The Post's own testing. We found no outlet that tested Alexa on its own in October 2023, so the incident rests on one reporting source plus the lawmakers' letter. Details seen only in search summaries are listed under "What we could not verify."

> **Read this first.** This is design analysis of how an assistant chose and spoke its sources. It is not a finding of fact about anyone's intent, takes no political side, and is not legal advice. Multiple investigations found no evidence of fraud in the 2020 election, as The Post reported; this page repeats Alexa's false answers only to show what users heard. The Post discloses that Amazon founder Jeff Bezos owns it and that its interim CEO sat on Amazon's board. The September 2024 case in which Alexa answered "why vote for" questions differently for two candidates is covered on its own page, [Amazon Alexa gives different answers for Harris and Trump (September 2024)](amazon-alexa-different-answers-for-harris-and-trump-voting-question-september-2024.md), and is not repeated here.

**Channel note.** This is a voice incident: users spoke a question and Alexa spoke the answer, naming its source aloud ("citing Rumble"). The signals on this page are written for text: they read the transcribed question, the answer text Alexa produced, and the source label attached to it, all of which can be logged. Signals about how the spoken answer was heard, such as whether a listener caught the source name, how it was stressed, or whether it could be replayed, are PLANNED for voice and are not detected or measured here. No opened source has audio.

## What happened (as reported)

- **The product.** Amazon Alexa, sold in home speakers, headphones, TVs and cars, per The Post. The Post wrote that Amazon promotes Alexa as a reliable election news source "to more than 70 million estimated users," and cited Insider Intelligence for a forecast that more than 75 million people in the US would use Alexa at least once a month in 2024.
- **The stolen-election answer.** Per The Post (October 7, 2023), asked about fraud in the 2020 race, Alexa said it was "stolen by a massive amount of election fraud," citing Rumble, which The Post called "a video-streaming service favored by conservatives."
- **The irregularities answer.** Per The Post, Alexa said the 2020 races were "notorious for many incidents of irregularities and indications pointing to electoral fraud taking place in major metro centers," referencing Substack, a subscription newsletter service.
- **The Pennsylvania answer.** Per The Post, "Alexa contended that Trump won Pennsylvania, citing 'an Alexa answers contributor.'"
- **Correct answers to other wordings.** The Post wrote that "The system is not always incorrect." Asked "Who won the 2020 election?" Alexa answered "Democrat Joe Biden," citing Reuters. Asked if the results were fraudulent, it said "There is no evidence of widespread fraud in the 2020 election — in Pennsylvania or anywhere else," referencing CNN. The Post wrote that "Changing the phrasing of a question can elicit different responses, which are at times accurate."
- **How Alexa finds answers, per The Post.** Speech is turned into text, and automated systems pull the most relevant information from a variety of sources. Amazon also crowdsources answers from customers and says it moderates them "with automation, trained moderators and customer feedback."
- **Other assistants.** In The Post's tests, Google Home and Siri pointed to sources disputing the fraud claims, and ChatGPT disputed election theft. The Post called Alexa "an outlier."
- **How long.** The Post wrote that it is "unclear how long" Alexa had been giving these answers.
- **After The Post called Amazon.** Alexa's responses changed. "To questions The Post had flagged to the company," Alexa answered with a refusal (worded "I'm sorry, I'm not able to answer that." in the October 8 snapshot and "I'm sorry. I'm not able to answer that." in the October 19 snapshot). The Post added: "Other questions still prompt the device to say there was election fraud in 2020."
- **The letter.** On October 19, 2023, Klobuchar, chair of the Senate Rules Committee, and Morelle, ranking member of the Committee on House Administration, wrote to Jeff Bezos citing The Post. The letter said "it appears that some answers were provided by contributors instead of verified news sources." It asked for answers by November 3, 2023 on Amazon's policy for election misinformation on Alexa, how Amazon vets contributor responses, what it would add before the 2024 elections, and how users can report misinformation shared by Alexa.
- **Eight months later.** The Post (June 16, 2024) wrote that "Seven months ago, Amazon said it fixed the problem," and Alexa did answer that Biden won in its recent tests. But The Post also reported that when asked who won the 2020 election, Alexa replied on multiple occasions "Donald Trump is the front-runner for the Republican Nomination at 89.3%," citing RealClearPolitics. Variations such as whether Trump won in 2020 got answers about the 2024 Iowa primary or "I don't know who will win the 2020 U.S. presidential election."

## What the company said

- **The statement.** Amazon spokeswoman Lauren Raemhild told The Post: "These responses were errors that were delivered a small number of times, and quickly fixed when brought to our attention." She added: "We continually audit and improve the systems we have in place for detecting and blocking inaccurate content."
- **Sources.** Raemhild said that during elections Alexa works with "credible sources" like Reuters, Ballotpedia and RealClearPolitics, and that Alexa draws data from "Amazon, licensed content providers and websites like Wikipedia."
- **Attribution.** Raemhild said: "During elections, we provide source and media outlet attribution so that customers know exactly where election information is coming from."
- **What Amazon declined to say.** Per The Post, Amazon "declined to explain why its voice assistant draws 2020 election answers from unvetted sources."
- **June 2024.** Amazon spokesperson Kristy Schmidt told The Post that customer trust is "paramount," and said: "If we identify that a response is not meeting our high accuracy bar, we quickly block the content."
- **What no opened source says.** Whether or how Amazon answered the Klobuchar and Morelle letter; what changed in Alexa's source rules; whether Alexa Answers contributions were still used for election questions.

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| Was it fixed? | Amazon (October 2023): "quickly fixed." The Post (same article): flagged questions now refused, other questions still gave fraud claims. The Post (June 2024): Amazon said it fixed the problem seven months earlier, yet variations still gave wrong or off-topic answers. |
| "Error" or "bug" | Amazon, per The Post: "errors." The Decoder paraphrases Amazon as calling it a bug. No opened source has an Amazon technical explanation. |
| Cause | The Post: Amazon declined to explain. NYU professor Meredith Broussard, quoted by The Post, suggested the answers "could reflect" pulling from sources across the spectrum for balance, or neglect of the old Alexa. The Decoder, in its own analysis, said it was most likely unrelated to Amazon's new large-language-model Alexa and seemed to be a source problem. None of these is confirmed. |
| When Amazon said it was fixed | The Post (June 16, 2024): "Seven months ago." Straight Arrow News, summarizing that article, says November. We use The Post's wording. |
| Framing | The Post, Audacy, Raw Story and The Daily Beast call the answers misinformation. Reclaim The Net calls the lawmakers' letter a demand to censor Alexa and notes Bezos owns The Post; The Post discloses the same ownership itself. |
| The questions asked | The Post quotes Alexa's answers but gives the exact question only for the correct "Who won the 2020 election?" answer. For the stolen answer it says only "Asked about fraud in the race." |

## Where in the conversation flow it broke

Based on The Post's account, and only as far as it goes. Each step is a place a check could have caught it.

1. **The question.** A user asked about fraud in the 2020 race. The wording itself leaned toward fraud; The Post's exact question is not given.
2. **Speech to text to lookup.** Per The Post, Alexa turned the speech into text and pulled the most relevant item it could find. Nothing in the reports suggests a transcription error; the words were heard and the wrong content was found.
3. **The source gate.** For this wording, the item came from Rumble, Substack or an Alexa Answers contributor, not from the "credible sources" Amazon named for elections. No opened source says how those items passed.
4. **The spoken answer.** Alexa stated a false claim as fact, then named a source. On a speaker, the user hears one answer and one source name, with no list of other views, no link and no way to see the page.
5. **Wording decides the answer.** "Who won" got Biden. "Fraudulent" got "no evidence." "Fraud in the race" got "stolen." The same fact got opposite answers depending on how the question was asked.
6. **The patch.** After The Post's call, the flagged questions got a bare refusal with no reason and no pointer to results. Other wordings still gave the old claims.
7. **Still uneven later.** In June 2024, per The Post, "who won" sometimes returned a 2024 primary poll, and "did Trump win" returned off-topic answers. Blocking answer by answer had not made the topic consistent.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). Each fit rests on The Post's reporting; no opened source shows Alexa's logs.

- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Strong fit.** Alexa stated "stolen by a massive amount of election fraud" in the same sure voice as a right answer. It named a source, but on a speaker the user could not open it or compare it, so a spoken name was not a real way to check.
- [False premises accepted](../goals/dialogue-management/failures/false-premises-accepted.md) (`false-premises-accepted`). **Partial fit.** A question "about fraud" got an answer that took fraud as given, while a neutral "who won" question got the right answer. Partial because The Post does not print the exact question, so we cannot show the premise word for word.
- [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (`one-sided-or-cherry-picked-sources`). **Partial fit.** Each answer gave one source and one side, with no sign that the claim was disputed. Partial because that page is about a research assistant choosing which sources agree; here the failure was letting low-trust sources answer at all, and Broussard's balance theory is unconfirmed.
- [Refusal with no reason or next step](../goals/refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md) (`refusal-with-no-reason-or-next-step`). **Partial fit, for the patch.** The fix for flagged questions was "I'm sorry, I'm not able to answer that," with no reason and no pointer to official results.
- [No way to report bad behaviour](../goals/measurement-and-feedback/failures/no-way-to-report-bad-behaviour.md) (`no-way-to-report-bad-behaviour`). **Weak fit.** The lawmakers asked what procedures let users report misinformation from Alexa, and the problem was fixed after a newspaper flagged it. No opened source says whether users could or did report it, so this stays weak.
- **Considered, not a fit.** [Symptom fixed, root cause missed](../goals/conversation-frameworks/failures/symptom-fixed-root-cause-missed.md) (`symptom-fixed-root-cause-missed`): the idea matches the patch, but the entry is about a support bot and a returning user, not a product team's fix. [Clean-lab testing](../goals/measurement-and-feedback/failures/clean-lab-testing.md) (`clean-lab-testing`): it is about typos and noisy input, not reworded questions. [Over-refusal of ordinary requests](../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md) (`over-refusal-of-ordinary-requests`): "who won" was still answered, and no source shows a blocked safe request. `transcription-hallucination`: no report suggests the speech was misheard. `wrong-explanations-taught-as-fact`: that entry is about tutors. `dialect-and-name-quality-gap`: the answers did not change with the user's name or dialect.
- **Possible gap for a person to judge.** No taxonomy entry covers (a) the same fact getting opposite answers depending on how the question is worded, (b) low-trust web or user-contributed content reaching an authoritative spoken answer on a high-stakes topic, or (c) a fix that blocks only the exact questions someone reported. These are proposals, not decisions.

## How it differs from close cases

- [Amazon Alexa different answers for Harris and Trump (September 2024)](amazon-alexa-different-answers-for-harris-and-trump-voting-question-september-2024.md): the same product a year later, but there the problem was one question getting different policies for two names. Here it was one fact getting different answers for different wordings, with false claims drawn from named low-trust sources.
- [Microsoft Copilot wrong election answers (December 2023)](microsoft-copilot-wrong-election-answers-december-2023.md): researchers found wrong facts about European elections through systematic testing of a text chatbot with links. Here a newspaper's tests of a voice assistant found a false claim about a past US election, spoken with a single source name.
- [AI Democracy Projects: chatbots' wrong election answers (February 2024)](ai-democracy-projects-chatbots-wrong-election-answers-proof-news-february-2024.md): experts rated model answers to voter questions on how to vote. Here the question was about a settled past result, and the false answer echoed a known political claim.

## What to measure

Proposed signals, not results. Status: Not yet run. Each is computable from transcribed questions, answer text and source labels. Thresholds are for the team to set; we propose none.

| Metric | How to compute from logs |
|---|---|
| Paraphrase disagreement rate | For a fixed set of settled facts (such as who won a past election), group test questions that ask the same thing in different words, including leading wordings ("fraud in the race"). Count groups where the answers do not all state the same fact, divided by all groups. |
| Low-trust source share on civic topics | Election answers whose source label is not on the team's approved list for that topic (for example, a video site, newsletter platform or user-contributed answer), divided by all election answers. |
| Contributor-answer share on civic topics | Election answers drawn from user-contributed content, divided by all election answers. |
| Patch coverage | After a flagged answer is blocked, run paraphrases of each flagged question. Count paraphrases that still return the flagged claim, divided by all paraphrases tried. |
| Premise check rate | Questions that presuppose a claim the approved sources reject, where the answer says the premise is false, divided by all such questions. |
| Bare refusal rate | Refusals on civic topics that give no reason and no pointer to an official source, divided by all refusals on civic topics. |

PLANNED for voice, not detected or measured: whether listeners could repeat the source name they heard; whether they took a named source as Amazon's own view (a risk The Post cites from a King's College London paper we did not open).

## What a team can change

Our proposals, not Amazon's. Each is a pass/fail check on a transcript or a test run. Status: Not yet run.

1. **An allow list for settled civic facts.** Pass: in a test set of 2020 election questions, every answer's source label is on the approved list for elections; none comes from a video site, newsletter platform or user-contributed answer.
2. **Same fact, every wording.** Pass: every question in a paraphrase set for "who won the 2020 election," including leading ones about fraud or stealing, states that Biden won.
3. **Correct the premise.** Pass: a question that assumes fraud gets an answer that says no evidence of widespread fraud was found and names the approved source, rather than a refusal or an agreement.
4. **Fix the topic, not the sentence.** Pass: after any blocked answer, the paraphrase set for that topic is rerun, and the fix is not closed until all paraphrases pass.
5. **Refuse with a next step.** Pass: any refusal on an election question says in one sentence that Alexa cannot answer it and names an official place to check, the same for every question.
6. **Keep contributor answers off high-stakes topics.** Pass: in a test set tagged as civic, health or legal, no answer is drawn from user-contributed content.
7. **Don't over-correct.** Pass: ordinary election questions such as "who won the 2020 election" and "when is Election Day" still get direct answers.

## What we could not verify

- The Washington Post's own site. It refused our direct requests; we read the October 2023 and June 2024 articles only from Internet Archive snapshots. The October article changed between snapshots (for example "reached out to" became "contacted," and the refusal's punctuation changed); we quote the October 8 snapshot unless noted.
- The exact questions The Post asked, the devices it used, and how many users heard the false answers. Amazon said "a small number of times"; no opened source gives a number, and we give none.
- Whether Amazon answered the Klobuchar and Morelle letter. We found no response in what we opened.
- Senator Klobuchar's press release on the letter. The Senate page returned 403; we read the letter itself from the PDF hosted by Reclaim The Net.
- Amazon's 2018 blog post on election updates and the King's College London paper on voice assistants, both cited by The Post. Not opened.
- A search summary claiming that Alexa "began to decline to answer if the 2020 election had been stolen." Seen only in a summary; The Post's opened text says only that the flagged questions got a refusal.
- Coverage by The Messenger (403), BizPac Review (downloaded, not read), The Gateway Pundit, Madhyamam, DT Next, TipRanks and Xataka. Seen only in search results; not used.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://www.washingtonpost.com/technology/2023/10/07/amazon-alexa-news-2020-election-misinformation/ | The Washington Post (Cat Zakrzewski; Shira Ovide contributed) | 2023-10-07 | Yes, 2026-10-28, via Internet Archive snapshots of 2023-10-08 and 2023-10-19 (direct request refused), raw HTML read as text; quotes checked word for word |
| https://www.washingtonpost.com/technology/2024/06/16/ai-chatbots-alexa-2020-election-results/ | The Washington Post (Caroline O'Donovan, Cat Zakrzewski) | 2024-06-16 | Yes, 2026-10-28, via Internet Archive snapshot of 2024-06-17, raw HTML read as text; quotes checked word for word |
| https://media.reclaimthenet.org/docs/lawmakers-alexa-misinformation-rumble-substack-letter-a.pdf | Letter from Sen. Amy Klobuchar and Rep. Joseph Morelle to Jeff Bezos, hosted by Reclaim The Net | 2023-10-19 | Yes, 2026-10-28, PDF converted to text; quotes checked word for word |
| https://www.audacy.com/kdwn/news/amazons-alexa-says-2020-race-was-stolen | Audacy (Stephanie Raymond) | 2023-10-09 | Yes, 2026-10-28, raw HTML read as text; relays The Post |
| https://finance.yahoo.com/news/amazon-alexa-told-users-2020-175637401.html | The Daily Beast via Yahoo (Kelly Weill) | 2023-10-07 | Yes, 2026-10-28, raw HTML read as text; relays The Post |
| https://www.rawstory.com/alarming-alexa-trump/ | Raw Story (David McAfee) | 2023-10-07 | Yes, 2026-10-28, raw HTML read as text; relays The Post |
| https://the-decoder.com/amazons-alexa-cites-an-unverified-source-claiming-the-2020-election-was-stolen/ | The Decoder (Matthias Bastian) | 2023-10-08 | Yes, 2026-10-28, raw HTML read as text (visible opening only); relays The Post plus its own analysis |
| https://reclaimthenet.org/lawmakers-amazon-alexa-misinformation-rumble-substack | Reclaim The Net (Tom Parker) | 2023-10-20 | Yes, 2026-10-28, raw HTML read as text; opinion framing |
| https://san.com/cc/ai-chatbots-struggle-to-answer-who-won-the-2020-election/ | Straight Arrow News (Karah Rucker) | 2024-06-18 | Yes, 2026-10-28, raw HTML read as text; relays The Post's June 2024 article |
| https://electionlawblog.org/2023/amazons-alexa-has-been-claiming-the-2020-election-was-stolen/ | Election Law Blog (Rick Hasen) | 2023-10-07 | Yes, 2026-10-28; excerpt of The Post only |
| https://daringfireball.net/linked/2023/10/22/ | Daring Fireball (John Gruber) | 2023-10-22 | Yes, 2026-10-28; excerpt of The Post plus comment |
| https://politicalwire.com/2023/10/07/amazons-alexa-says-the-2020-election-was-stolen/ | Political Wire | 2023-10-07 | Yes, 2026-10-28; excerpt of The Post only |
| https://www.electoral-vote.com/evp2023/Items/Oct09-9.html | Electoral-vote.com | 2023-10-09 | Yes, 2026-10-28; commentary relaying The Post |
| https://www.klobuchar.senate.gov/public/index.cfm/2023/10/klobuchar-morelle-call-on-amazon-for-answers-after-reports-of-alexa-spreading-election-misinformation | Office of Sen. Amy Klobuchar | 2023-10 | No; 403. Not used |
| https://themessenger.com/news/ai-alert-alexa-tells-users-2020-election-was-rigged-report | The Messenger | 2023-10 | No; 403. Not used |

## Corrections

If you have Amazon's reply to the Klobuchar and Morelle letter, the exact questions The Post asked, or a dated test of Alexa's current answers about the 2020 election, tell us and we will fix this page.
