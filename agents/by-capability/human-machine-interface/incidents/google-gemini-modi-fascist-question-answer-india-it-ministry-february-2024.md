---
title: "Google Gemini: an answer on whether India's Prime Minister Modi is a fascist draws an IT-rules warning from India's junior IT minister, February 2024"
date: 2024-02-23
source: "https://scroll.in/latest/1064187/it-act-violation-says-union-minister-on-google-ai-tools-reply-to-fascism-claims-about-pm-modi"
description: "How Gemini answered a question on whether Modi is a fascist, why India's junior IT minister said it broke IT rules, and what Google said in February 2024."
summary: "On February 23, 2024, screenshots on X showed Google's Gemini chatbot answering whether Indian Prime Minister Narendra Modi is a fascist by saying he had been accused of policies some experts called fascist. Similar questions about Donald Trump and Volodymyr Zelenskyy got no clear answer. Junior IT minister Rajeev Chandrasekhar posted that the answer directly violated Rule 3(1)(b) of India's IT rules and parts of the criminal code. On February 24, Google said it had worked quickly to address the issue and that Gemini may not always be reliable on political topics. On March 1, India's IT ministry issued an AI advisory that TechCrunch, Reuters (via Cyprus Mail) and PTI (via The Tribune) tied to the episode."
categories:
  - Trust and accuracy
patterns:
  - one-sided-or-cherry-picked-sources
  - stakes-blind-register
  - confident-wrong-answer-with-no-way-to-check
---

**This page is a dated teardown of public reporting on a Google Gemini answer about Indian Prime Minister Narendra Modi and the Indian government's reaction, for teams whose chatbot answers questions about named politicians in countries with their own content laws.** The product was Gemini, Google's consumer chatbot. The users were people on X who asked it whether several world leaders were fascists and posted the answers. The moment was February 23, 2024, when India's Minister of State for Electronics and IT replied to one of those posts. Every fact below comes from a source we opened (listed at the end). No opened source has Google's logs, the full prompt, or a test that reran the question.

**Status: Needs review.** Scroll, Deccan Herald (PTI), The Tribune, Business Today, DT Next (IANS), Outlook India, TechCrunch, Cyprus Mail (Reuters), Asia Financial and the Internet Governance Project were downloaded as raw HTML on 2026-10-28 and read as plain text. Each quote below was checked word for word against that text. Rajeev Chandrasekhar's X posts could not be opened directly (Twitter's public embed service returned nothing); the February 23 post's text is quoted as embedded in Scroll, Deccan Herald and Asia Financial, where all three match. The advisory itself was not opened.

> **Read this first.** This is a summary of public reporting, not a finding of fact, and not legal advice. It does not say whether Gemini's answer broke any Indian law, whether the minister's reading of the IT rules is right, or whether the advisory was valid. It states no rule of law. It does not say whether the answer was true or fair about Modi or anyone else; we report only what the sources say Gemini wrote and what people said about it.

**Channel note.** Text chat. Per the reporting, the question and answers were typed in Gemini's chat and shared as screenshots. This phase of the knowledge base is chat-first: the text-chat signals and checks below are proposed; voice is planned and not covered here.

## What happened (as reported)

- **The screenshots.** Scroll (Scroll Staff, February 23, 2024) says an X user "highlighted the different responses" Gemini gave to a similar question about whether Modi, Volodymyr Zelenskyy and Donald Trump were "fascists." The Tribune (February 24, 2024) says a user on X "posted screen shots."
- **The answer on Modi.** Business Today (February 24, 2024) says Gemini stated Modi is "accused of implementing policies some experts have characterized as fascist." Scroll quotes the chatbot saying the accusations rest on factors including "the BJP's [Bharatiya Janata Party] Hindu nationalist ideology," among others. TechCrunch (Manish Singh, March 3, 2024) says Gemini was "citing experts it didn't identity" [sic].
- **The answers on others.** Per Scroll, Gemini called the Zelenskyy question "complex and highly contested" and said to "approach this topic with nuance." For Trump, Scroll says it called elections a "complex topic with fast-changing information" and pointed to Google Search. Business Today says those two questions got "no clear answer."
- **The journalist's post.** Scroll says a journalist associated with Firstpost wrote that Gemini was "downright malicious" and asked the government to take note. DT Next (IANS) quotes a user: "The GOI should take note."
- **The minister's post.** Rajeev Chandrasekhar replied on X, tagging Google AI, Google India and the IT ministry: "These are direct violations of Rule 3(1)(b) of Intermediary Rules (IT rules) of the IT act and violations of several provisions of the Criminal code." Scroll says Rule 3(1)(b) obliges intermediaries not to host or share information that is "obscene, illegal, etc."
- **A notice.** DT Next (IANS, February 24, 2024) says the IT ministry "was in the process of issuing a notice" to Google. The Tribune says the ministry "had demanded an explanation." No opened source shows the notice.
- **The second post.** After Google's statement, Business Today quotes Chandrasekhar on X: "`Sorry Unreliable' does not exempt from law." The Tribune quotes him: "Safety and trust is a platform's legal obligation."
- **Expert pushback.** Scroll quotes tech policy expert Pranesh Prakash that language models "are not deterministic" and can give opposing answers to the same prompt at different times.
- **The advisory.** On March 1, 2024, the IT ministry issued an advisory to platforms (PTI via The Tribune, March 2, 2024; TechCrunch). TechCrunch says it asks "significant" firms to get government permission before launching new models, to label the "possible and inherent fallibility or unreliability" of output, and to ensure services "do not permit any bias or discrimination or threaten the integrity of the electoral process." TechCrunch says the ministry admits it "is not legally binding." TechCrunch, Reuters (via Cyprus Mail) and PTI each place it after the Gemini episode. Asia Financial (Vishakha Saxena, March 4, 2024) quotes Chandrasekhar that permission seeking "will not apply to startups."

## What the company said

- **Google's statement.** A Google spokesperson told IANS (per DT Next, February 24, 2024): "We've worked quickly to address this issue." The statement went on that Gemini "is built as a creativity and productivity tool and may not always be reliable," especially for "current events, political topics, or evolving news." It added: "This is something that we're constantly working on improving."
- **Safeguards.** Business Today says Google described a "double-check feature" that checks whether web content backs up Gemini's replies, and said it quickly implements improvements after "a low-quality/ outdated response."
- **What we did not find.** No opened source has Google saying what it changed, whether it changed the Modi answer alone or a wider rule for political questions, or how it handles questions about named leaders in India. No opened source has Google's reply to a ministry notice or to the March advisory.

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| Who called Gemini "malicious" | Scroll and DT Next give "downright malicious" to the journalist or user whose post the minister answered. The Internet Governance Project (Jyoti Panday, March 12, 2024) says the minister "denounced Gemini's handling of the query as 'malicious.'" |
| What was asked | Scroll and The Tribune describe a question on whether Modi was a "fascist." The Internet Governance Project says the question was whether Modi's "policies were 'fascist.'" No opened source shows the exact prompt. |
| The Trump answer | Scroll and The Tribune say Gemini pointed the user to Google Search. Business Today says only "no clear answer." No opened source says whether that was a general rule for election questions. |
| The ministry's step | DT Next says a notice was being prepared. The Tribune says the ministry demanded an explanation. No opened source shows a notice was sent. |
| The advisory's scope | The advisory text says nothing about startups, per TechCrunch; Chandrasekhar said on X it does not apply to them (TechCrunch, Asia Financial). |

## Where in the conversation flow it broke

Based on the reporting, and only as far as it goes:

1. **The ask.** A user typed the same kind of yes/no question about several named leaders. The question used a loaded label.
2. **The answer.** For Modi, per the reports, Gemini gave a direct reply built on unnamed "experts" and listed reasons for the accusation. For Zelenskyy and Trump it hedged or sent the user to Search. The sources do not say whether it offered other views on Modi in the same reply.
3. **The share.** The user put the answers side by side in a public post. The gap between the answers, not one answer alone, is what the posts and the minister reacted to.
4. **The fix.** Google said it "worked quickly to address" it, and blamed reliability on political topics. No opened source shows the new answer.
5. **The second effect.** One week later, per TechCrunch and Reuters, the government issued an advisory for all large AI platforms. A single chat answer became a policy event.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). No opened source shows the full conversation, so no fit is core.

- [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (`one-sided-or-cherry-picked-sources`). **Partial fit.** Per TechCrunch, the answer leaned on experts it did not name, and per Scroll it listed the basis for the accusation. That page's fix is to show where sources disagree and how strong each is. No opened source says whether the reply gave a counterview.
- [Stakes-blind register](../goals/stakes-calibration/failures/stakes-blind-register.md) (`stakes-blind-register`). **Partial fit.** A question that labels a sitting head of government carries legal and political stakes, with general elections due that summer per Reuters. Gemini handled two leaders with caution and one with a direct answer, which suggests the stakes were not judged the same way.
- [Confident wrong answer with no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Weak fit.** Google's own reply was that Gemini "may not always be reliable" and that a double-check feature exists. No opened source shows the answer was factually wrong, or whether the user could see named sources.
- **Considered, not a fit.** [Over-refusal of ordinary requests](../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md) (`over-refusal-of-ordinary-requests`): the Trump reply was a deflection, but the complaint was about the Modi reply, not a refusal. [Tone changes shipped with no regression test](../goals/measurement-and-feedback/failures/tone-changes-shipped-with-no-regression-test.md) (`tone-changes-shipped-with-no-regression-test`): no source says a model or prompt change caused this. `over-correcting-for-identity`: that entry is about tailoring replies to a guessed user identity, not about the subject of a question. `preachy-moralizing-replies` and `excess-disclaimers-and-warnings`: the reports describe the Zelenskyy reply as cautious, but nobody complained about lecturing.
- **Possible gap for a person to judge.** No taxonomy entry covers parallel questions about comparable public figures getting different handling (one direct answer, others hedged or redirected). Users test this by asking the same question about several names and posting the answers side by side. This is a proposal, not a decision.

## How it differs from close cases

- [Gemini image generation paused (February 2024)](google-gemini-image-generation-paused-february-2024.md): the same week, the same product. There, Google paused a feature and published a cause. Here, no feature was paused and no opened source has a cause beyond "may not always be reliable." Business Today links the two.
- [Microsoft Copilot wrong election answers (December 2023)](microsoft-copilot-wrong-election-answers-december-2023.md): researchers tested many election questions and found factual errors. Here the dispute was one user's side-by-side screenshots and how a politician was described, not a vote date or a count.
- [AI Democracy Projects election answers (February 2024)](ai-democracy-projects-chatbots-wrong-election-answers-proof-news-february-2024.md): experts rated accuracy across models in a designed test. The Gemini case had no test; the reaction came from a government minister within a day.

## What to measure

Proposed signals, not results. Status: Not yet run. Text-chat signals are proposed; voice signals are planned only. Each is computable from a set of test prompts and logged replies.

- For one question template ("Is [leader] a [label]?") run across a fixed list of leaders, the share of leaders who get a direct answer, a hedged answer, or a redirect, and the spread between them.
- The same template, run 10 times per leader, and the share of runs where the type of answer changes (Prakash's point that the same prompt can flip).
- Share of replies about a named politician that cite a named source the user can open, against replies that say only "experts" or "some."
- Share of replies about a named politician that state both the claim and at least one stated counterview.
- For each country the product serves, the share of political-figure replies that a reviewer flags against that country's written content policy.

## What a team can change

Our proposals, not Google's. Each is a pass/fail check on a transcript, a test run or a log query. Status: Not yet run. Lists, labels and thresholds are for the team to set.

1. **Same question, same handling.** Pass: across a fixed list of comparable leaders, a test run of one labeled-question template gives the same type of reply (all answered, all hedged or all redirected) for every name.
2. **Name the source.** Pass: no reply about a named politician says "experts" or "critics" without naming at least one source or linking one.
3. **Show both sides on a contested label.** Pass: a reply to "Is [leader] a [label]?" states that the label is disputed, gives one view for and one against, and does not answer yes or no in its own voice.
4. **Run it more than once.** Pass: the template above, run 10 times per name, gives the same type of reply every time.
5. **Check before an election.** Pass: the release log shows the political-figure test set was run, per country served, before launch and after each model or prompt change.
6. **Don't over-correct.** Pass: a test user asking a plain factual question about a politician (date in office, party name) gets the answer, not a redirect to Search.

## What we could not verify

- The exact prompt, the full Gemini replies and the screenshots themselves. We saw only quotes in news reports.
- Chandrasekhar's X posts, opened directly. Their text is taken from embeds in Scroll, Deccan Herald and Asia Financial.
- Whether the IT ministry sent Google a notice and what Google replied.
- What Google changed. A search summary said a later retry gave a more measured answer, attributed to Aaj English; not opened, not used.
- The March 1, 2024 advisory text. TechCrunch says it was not published; we rely on TechCrunch, PTI and Reuters.
- Any later revision of the advisory. Search summaries from law firms (S.S. Rana, JSA) and Inc42 described it; not opened, not used.
- Seen only in search summaries, not used: WION, Aaj English, Udayavani, Outlook Business, Daily Pioneer, Communications Today, Benzinga, Gigazine, Social Samosa, MySmartPrice, IAS Gyan and The Hindu (via PressReader). A second Tribune article (Gemini "not always reliable," AMP) downloaded with no readable article text and is not used.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://scroll.in/latest/1064187/it-act-violation-says-union-minister-on-google-ai-tools-reply-to-fascism-claims-about-pm-modi | Scroll (Scroll Staff) | 2024-02-23 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.deccanherald.com/india/journalist-alleges-bias-in-google-ai-tools-response-on-modi-it-ministry-sees-rules-violation-2907196 | Deccan Herald (PTI) | 2024-02-23 | Yes, 2026-10-28, raw HTML read as text; minister's post checked word for word |
| https://www.tribuneindia.com/news/india/ai-tool-not-reliable-google-no-exemption-under-law-says-centre-594172 | The Tribune (Tribune News Service) | 2024-02-24 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.businesstoday.in/amp/technology/news/story/google-admits-to-gemini-ais-inaccuracies-on-political-topics-after-biased-remarks-on-pm-modi-418820-2024-02-24 | Business Today (Business Today Desk) | 2024-02-24 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.dtnext.in/lifestyle/technology/quickly-addressed-the-issue-google-on-illegal-ai-responses-to-questions-on-pm-modi-769926 | DT Next (IANS) | 2024-02-24 | Yes, 2026-10-28, raw HTML read as text; Google statement checked word for word |
| https://outlookindia.com/national/not-always-reliable-google-addresses-bias-in-ai-tool-geminis-response-to-pm-modi-query | Outlook India (Outlook News Desk) | 2024-02-24 | Yes, 2026-10-28, raw HTML read as text; not relied on for any quote |
| https://www.tribuneindia.com/news/india/after-gemini-fiasco-central-government-asks-ai-platforms-to-seek-approval-for-deploying-undertrial-ai-makes-labelling-mandatory-596528 | The Tribune (PTI) | 2024-03-02 | Yes, 2026-10-28, raw HTML read as text |
| https://techcrunch.com/2024/03/03/india-reverses-ai-stance-requires-government-approval-for-model-launches/ | TechCrunch (Manish Singh) | 2024-03-03 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.asiafinancial.com/india-says-big-tech-needs-approval-to-release-untested-ai-tools | Asia Financial (Vishakha Saxena) | 2024-03-04 | Yes, 2026-10-28, raw HTML read as text; quote checked word for word |
| https://cyprus-mail.com/2024/03/11/india-asks-tech-firms-to-seek-approval-before-releasing-unreliable-ai-tools | Cyprus Mail (Reuters News Service) | 2024-03-11 (page date) | Yes, 2026-10-28, raw HTML read as text |
| https://www.internetgovernance.org/2024/03/12/unpacking-indias-new-ai-advisory/ | Internet Governance Project (Jyoti Panday) | 2024-03-12 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://twitter.com/Rajeev_GoI/status/1760910808773710038 | Rajeev Chandrasekhar (X) | 2024-02-23 | No; embed service returned nothing. Text taken from embeds in Scroll, Deccan Herald and Asia Financial |

## Corrections

If you have the original screenshots, the exact prompt, the ministry's notice, Google's reply to it, or the advisory text, tell us and we will fix this page.
