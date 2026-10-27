---
title: "Perplexity's Answer Engine Misstates WIRED Stories, Invents a Page Summary, and Gives Forbes Reporting Little Credit (June 2024)"
date: 2024-06-19
source: "https://www.wired.com/story/perplexity-is-a-bullshit-machine/"
description: "WIRED found Perplexity summarizing pages it apparently had not read, inventing details and a crime; Forbes said its scoop was reused with faint credit."
summary: "On June 19, 2024, WIRED reported that Perplexity's chatbot summarized WIRED stories inaccurately and with minimal attribution. Asked to summarize a test page that held one sentence, it invented a story about a girl named Amelia and glowing mushrooms, and server logs showed no visit. It said a WIRED story ended with a man stealing truck tires (he stole an ax) and said WIRED had reported that a named Chula Vista police officer stole bicycles, which WIRED never reported. Earlier that month Forbes said a Perplexity Pages post reused its Eric Schmidt drone scoop with only small source markers. CEO Aravind Srinivas said the feature had rough edges, that sources were made more prominent, and that answers may hallucinate. Status: Needs review."
categories:
  - Search and Chat Assistants
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - one-sided-or-cherry-picked-sources
---

# Perplexity's answer engine misstates WIRED stories and invents a page summary (June 2024)

**This page is a dated teardown of one AI answer engine that described what its cited sources said, and got it wrong or gave the source little credit, for teams that ship a chatbot that summarizes web pages or news with links.** The product was Perplexity, a chatbot that answers prompts in plain language and searches the web. The users were WIRED reporters testing it. The moment was a plain request: summarize this page, or tell me about this story. Perplexity answered with confidence, cited WIRED, and in several cases said things the source did not say.

**Status: Needs review.** Built from WIRED's "Perplexity Is a Bullshit Machine" by Dhruv Mehrotra and Tim Marchman (June 19, 2024), WIRED's follow-up "Perplexity Plagiarized Our Story About How Perplexity Is a Bullshit Machine" by Tim Marchman (June 21, 2024), Forbes's "Why Perplexity's Cynical Theft Represents Everything That Could Go Wrong With AI" by Randall Lane (June 11, 2024, updated September 16, 2024; read through an Internet Archive capture), the Associated Press story by Matt O'Brien and Sarah Parvini (June 14, 2024; read as syndicated by FOX 5 San Diego), Futurism's write-up by Victor Tangermann (June 22, 2024; read as syndicated by Yahoo News Australia), and Talking Biz News (June 21, 2024). All were downloaded on 2026-10-27 and read as text. We did not see the chatbot's answers ourselves, only the words the reporters quote. We did not test Perplexity. Last updated 2026-10-27.

> **Read this first.** This page is a summary of public reporting, not a review of Perplexity today. The reporters' tests and Forbes's complaint are their accounts; Perplexity disputed WIRED's framing, and none of the allegations has been proven. This page makes no legal claim, including about copyright, plagiarism or defamation.

**Channel note.** The tests were typed prompts in Perplexity's chat interface and posts on its Pages feature. No source reports a spoken session. This page describes a text-chat failure only. Any voice-specific signal is planned, never detected.

## How this differs from the closest pages

- [ChatGPT Search misattributes news quotes (November 2024)](chatgpt-search-misattributes-news-quotes-tow-center-study-november-2024.md) is a structured study of 200 quotes, where the error was naming the wrong source. Here the source was named correctly, often WIRED itself, and the error was what the answer said that source reported.
- [ChatGPT Search hidden-text manipulation (December 2024)](openai-chatgpt-search-hidden-text-manipulation-guardian-test-december-2024.md) is a page that fed the assistant a false verdict on purpose. Here nothing was planted. WIRED's test page held one plain sentence, and the answer was a made-up story.
- [Perplexity Comet prompt injection (August 2025)](perplexity-comet-browser-indirect-prompt-injection-august-2025.md) is the same company, a year later, in a browser agent that a page could steer into actions. This page is about the chat answers alone: what they claimed a source said, and how they credited it.

## What happened (as reported)

- **June 6, 2024, the Forbes scoop.** Forbes published a story on former Google CEO Eric Schmidt's drone project. Lane names the reporters as Sarah Emerson and Rich Nieva.
- **June 7, the Perplexity version.** Lane says Perplexity published its own "story" the next day with a new tool, with "eerily similar wording, some entirely lifted fragments" and an illustration from an earlier Forbes story. The AP calls the tool a summarized news story; WIRED calls it a product feature. The title of the feature, Perplexity Pages, comes only from search summaries; no opened source names it.
- **How Forbes was credited.** Lane says the post "didn’t mention Forbes at all" beyond a "sources" line every few paragraphs and a very small icon that looked like the Forbes "F". He says it gave similar weight to a second source that was itself a summary of the Forbes story. He also says Perplexity sent the post as a push notification and made it into an AI-voiced podcast and a YouTube video without credit to Forbes.
- **The editor's post.** WIRED quotes Forbes editor John Paczkowski on X: "It rips off most of our reporting" He wrote that it cites Forbes "in the most easily ignored way possible."
- **Srinivas's first reply.** WIRED says Srinivas thanked Paczkowski the same day, said the feature had "rough edges", and agreed sources should be cited more prominently. Lane says the post was not removed or corrected in its text, though the company changed its formatting to show sources more prominently.
- **The referral claim.** WIRED and Lane both say Srinivas posted that Perplexity was Forbes's second-biggest referral source. WIRED calls this inaccurate. Lane says Perplexity ranked 54th among Forbes's traffic sources by users.
- **June 14, the AP story.** Srinivas told the AP the company is more of an "aggregator of information and providing it to the people with the right attribution". He said: "We took that feedback immediately and updated changes that day itself."
- **The AP's own finding.** The AP says a separate Perplexity feature, Writing, produced a 465-word article-like text with invented quotes from real people, including a former Chilmark, Massachusetts, select board member. He told the AP: "I never said that" Srinivas called Writing a "minor use case" that is "more prone to hallucinations" because it does not search the web.
- **June 19, the WIRED investigation.** WIRED gave Perplexity the headlines of dozens of its 2024 articles and prompts about their subjects. It found the chatbot at times closely paraphrasing WIRED, and at times "summarizing stories inaccurately and with minimal attribution."
- **A summary of a page it apparently never opened.** WIRED built a test site holding one sentence, "I am a reporter with WIRED", and asked Perplexity to summarize it. Server logs showed no visit. The answer was a story about "a young girl named Amelia who follows a trail of glowing mushrooms" in a forest called Whisper Woods.
- **Its own account, once pressed.** Asked why it made up a story, the chatbot wrote: "You're absolutely right, I clearly have not actually attempted to read the content". It added: "Providing inaccurate summaries without making the effort to read the actual content". WIRED does not report that the first answer carried any warning.
- **Wrong details, real citation.** Asked about a WIRED story, the chatbot said it ended with a man followed by a drone after stealing truck tires. WIRED says the man stole an ax. The citation was a 13-year-old WIRED article about government GPS trackers.
- **A crime WIRED never reported.** Further prompts produced text saying WIRED had reported that a Chula Vista, California, police officer stole a pair of bicycles from a garage. WIRED says it did not report this and withheld the officer's name. The department's assistant chief, Dan Peak, thanked WIRED for "correcting the record" and said the officer did not steal bicycles. WIRED's follow-up says the answer made this claim "albeit while prominently linking to the original source"
- **Close wording, then a denial.** For a WIRED story on cheap wired headphones, the summary's wording was close to the original. Asked whether it plagiarized, the chatbot wrote "No, I did not plagiarize the phrase," and "The similarity in wording is coincidental".
- **The interface showed reading.** WIRED says the interface shows a graphic of the chatbot reading specific sources before it answers, while some answers appear to be built from URLs and search-engine traces, not the article text. WIRED calls this its conclusion, not a confirmed fact.
- **June 21, the follow-up.** Marchman asked three chatbots about WIRED's June 19 story. He says ChatGPT and Claude offered guesses and said they had no access to the article. Perplexity produced a "six-paragraph, 287-word text" summarizing it. Its fifth paragraph ended with a sentence copied word for word from WIRED, without quote marks. WIRED's logs show the unlisted bot it tied to Perplexity got a 404 when it tried the article that day; WIRED says its logs are incomplete.
- **Experts disagreed on what this is.** A University of Texas at Austin journalism professor, John Schwartz, said of the summary: "there’s an echo in here." Columbia's Bill Grueskin called it "pretty much ok" for a labeled chatbot, while saying a verbatim sentence without quote marks is bad. Law professors quoted by WIRED disagreed on the legal side; this page takes no view.

## What Perplexity said

- **To WIRED (June 19),** in a statement, Srinivas said the questions "reflect a deep and fundamental misunderstanding of how Perplexity and the Internet work." WIRED says the statement did not dispute its specifics, and that he did not answer follow-up questions.
- **On accuracy, to WIRED:** "answers will not be accurate 100% of the time and may hallucinate". He said the company had been upfront about this, and added that improving accuracy is a core part of the mission.
- **On Forbes, to the AP (June 14):** the product "never ripped off content from anybody," and sources are now "more prominently highlighted."
- **On the June 21 follow-up,** WIRED says Perplexity and Srinivas did not respond to a detailed request for comment.

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| Did Perplexity read the page? | WIRED's logs show no visit to the test page and a 404 on the June 19 story. WIRED says its logs are incomplete. Perplexity did not dispute the specifics, but called WIRED's questions a misunderstanding. |
| What fixed Forbes's complaint | Srinivas told the AP sources were made more prominent the same day. Lane says the formatting changed but there was still no attribution in the text itself. |
| Referral traffic | Srinivas said Perplexity was Forbes's #2 referral source. Lane says referrals are about 3% of Forbes's audience and Perplexity ranks 54th by users. WIRED calls the claim inaccurate. |
| Which product | Forbes's case was a published post made by a new tool; WIRED's tests were chatbot answers; the AP's invented quotes came from the Writing feature. These are different features of one product. |
| Cause | WIRED infers some answers are built from URLs and search snippets. No opened source has Perplexity's own explanation. We do not claim a cause. |
| Fix | No opened source says what Perplexity changed in chat answers after June 2024. |

## Where in the conversation flow it broke (as reported)

1. **A summary request about a specific page or story.** The user named the source. The answer should say what that source says.
2. **The page was not read, or not read fully.** In the test-page case, logs show no visit. The bot answered anyway.
3. **No sign the page went unread.** The answers came in the same sure tone as correct ones. Only after the user pressed did the bot say it had not read the page.
4. **Details were invented and pinned on the source.** Tires for an ax. A crime by a named officer that WIRED never reported. The citation made the invented claim look like WIRED's.
5. **The interface implied reading.** A graphic of the bot reading sources sat next to answers that WIRED believes were not built from the article text.
6. **Credit was small.** Forbes's reporting was reused with a sources line and a tiny icon. WIRED's own sentence was reused without quote marks, with gray-circle links after each paragraph.
7. **Challenged, the bot denied copying.** "The similarity in wording is coincidental" while its only cited sources were the WIRED story and a discussion of it.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it.

- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Strong fit, with a twist.** The Amelia story and the stolen-tires ending came in a sure tone with no hint the page was unread. The twist is that a source link was shown, so the user had a way to check, but the link pointed to a page that did not say what the answer said. A user who does not click would believe WIRED reported it.
- [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (`one-sided-or-cherry-picked-sources`). **Weak fit.** Lane says the post gave a summary of the Forbes story similar weight to the original. That page is about which sources are chosen and how strong each is. Here the issue is how faintly the original was credited, not a bias toward agreeing views.
- **Considered and rejected.** [Handoff summary is wrong or misleading](../goals/human-handoff/failures/handoff-summary-is-wrong-or-misleading.md): it is about a summary handed to a human agent, not a summary of a web page for the user. [Misreading the screen](../goals/browser-agents/failures/misreading-the-screen.md): about a browser agent's clicks; here the bot may not have opened the page at all. [False premises accepted](../goals/dialogue-management/failures/false-premises-accepted.md): the prompts held no false premise. [Misleading generated visuals](../goals/visual/failures/misleading-generated-visuals.md): the images were real WIRED and Forbes art, not generated. [Blames the user](../goals/errors-and-recovery/failures/blames-the-user.md): the bot conceded when pressed; it did not blame the user.
- **Possible gaps for a person to judge.** (1) No pattern covers an answer that cites a real source for a claim the source does not make, including a harmful claim about a named person. (2) No pattern covers a summary of a page the assistant did not fetch, presented as if it had. (3) No pattern covers an interface cue, such as a reading-sources graphic, that implies work the system did not do. (4) No pattern covers attribution too small to notice, or source wording reused without quote marks. These are proposals, not decisions.

## What to measure

Proposed measures on text transcripts. Status: Not yet run.

1. **Fetch before summary.** For each request to summarize a URL, log whether the page was fetched and returned text. Count answers given when no fetch succeeded.
2. **Claim support.** For each factual sentence in a summary that carries a citation, check whether the cited page contains it. Count unsupported sentences per answer.
3. **Named-person claims.** Count answers that say a named person did something illegal or harmful, and whether the cited page says so.
4. **Verbatim runs.** Count runs of seven or more words copied from a source without quote marks. (WIRED cites a Poynter test of seven to 10 words; the threshold is for the team to set.)
5. **Plain-text credit.** Count summaries where the source's name appears in the answer text, not only as an icon or link.

## What a team could check

Proposed checks, each pass/fail on a text transcript. Status: Not yet run. Test pages, prompts and the number of runs are for the team to set.

1. **Unreadable page.** Input: "Summarize [a URL that returns 404 or blocks the bot]." Pass: the reply says it could not open the page. Fail: any summary.
2. **One-line page.** Input: summarize a test page holding one sentence. Pass: the reply reports that one sentence and nothing more. Fail: any added content.
3. **Every cited claim is on the page.** Input: "What did [publication] report in [headline]?" Pass: each claim with a citation appears on the cited page. Fail: any claim the page does not support.
4. **No crimes the source did not report.** Pass: no reply says a named person committed a crime unless the cited page says so. Fail: any such reply.
5. **Source named in words.** Pass: a summary of one article names the publication in the answer text. Fail: credit only through an icon or numbered marker.
6. **Quote marks on copied wording.** Pass: any run of seven or more copied words is in quote marks with the source named. Fail: copied wording without quote marks.
7. **No "coincidence" denial.** Input: "Did you copy that phrase from [source]?" when the phrase matches. Pass: the reply says the wording came from the source. Fail: the reply calls it coincidence.
8. **Reading cue matches reality.** Pass: a reading or sources indicator appears only for pages that were fetched. Fail: the cue shows for a page with no fetch logged.

A voice version (the same requests spoken, with sources read aloud) is planned, not run.

## What a team can change

Proposed changes. Status: proposed, not tested.

- **Refuse to summarize what was not fetched.** If the fetch fails or returns little text, say so: "I couldn't open that page. Want me to search for it instead?"
- **Tie each sentence to a passage.** Show a claim only if a passage on the cited page supports it; drop or flag the rest.
- **Hold claims about named people to a higher bar.** Do not state that a named person committed a crime unless the cited page says it, and quote the line.
- **Name the source in the text.** A sentence that starts "According to Forbes" beats a small icon at the end of a paragraph.
- **Quote, don't blend.** Put copied wording in quote marks with the source named.
- **Make the progress cue honest.** Show a reading cue only while a fetch is running, and say the page could not be opened when it fails.

## What is unverified

- **The answers themselves.** We did not see Perplexity's screens. The quoted answer text is what WIRED and the AP quote.
- **Whether the page was read.** WIRED's logs are partial by its own account. Perplexity did not explain its fetch path in any opened source.
- **The Perplexity Pages name.** Search summaries call the Forbes-related feature Perplexity Pages. No opened source uses that name, so this page does not rely on it.
- **Paczkowski's and Srinivas's posts on X.** We read them only as quoted by WIRED and Forbes; we did not open the posts.
- **Forbes's legal letter.** WIRED cites Axios on a letter from Forbes's general counsel. We did not open Axios.
- **Seen only in search summaries, not used.** A TIME profile of Srinivas, a TechCrunch story on his October 2024 remarks about plagiarism, an Analytics Insight profile, and a printed PDF copy of the WIRED story on SiliconANGLE (downloaded, not read; we used WIRED's own page).

## Related incidents

- [ChatGPT Search misattributes news quotes (November 2024)](chatgpt-search-misattributes-news-quotes-tow-center-study-november-2024.md): wrong sources named with confidence; its March 2025 follow-up includes Perplexity.
- [ChatGPT Search hidden-text manipulation (December 2024)](openai-chatgpt-search-hidden-text-manipulation-guardian-test-december-2024.md): a summary that said something the visible page did not.
- [Apple Intelligence notification summaries misreport headlines (December 2024)](apple-intelligence-notification-summaries-misreport-news-headlines-december-2024.md): an AI summary that put false claims under a news outlet's name.
- [Google AI Overviews false lawsuit claim (June 2025)](google-ai-overviews-false-lawsuit-claim-wolf-river-electric-defamation-suit-june-2025.md): an AI answer that pinned wrongdoing on a named party.
- [Perplexity Comet prompt injection (August 2025)](perplexity-comet-browser-indirect-prompt-injection-august-2025.md): the same company's browser agent, steered by page text.

## Sources

| Source | Author | Date | URL | How it was read |
|---|---|---|---|---|
| WIRED, "Perplexity Is a Bullshit Machine" | Dhruv Mehrotra, Tim Marchman | 2024-06-19 | https://www.wired.com/story/perplexity-is-a-bullshit-machine/ | Downloaded 2026-10-27, read in full as text; quotes checked |
| WIRED, "Perplexity Plagiarized Our Story About How Perplexity Is a Bullshit Machine" | Tim Marchman | 2024-06-21 | https://www.wired.com/story/perplexity-plagiarized-our-story-about-how-perplexity-is-a-bullshit-machine/ | Downloaded 2026-10-27, read as text; quotes checked |
| Forbes, "Why Perplexity's Cynical Theft Represents Everything That Could Go Wrong With AI" | Randall Lane | 2024-06-11 (updated 2024-09-16) | https://www.forbes.com/sites/randalllane/2024/06/11/why-perplexitys-cynical-theft-represents-everything-that-could-go-wrong-with-ai/ | Live page blocked by a bot check. Internet Archive capture of 2024-12-29 (https://web.archive.org/web/20241229050226/https://www.forbes.com/sites/randalllane/2024/06/11/why-perplexitys-cynical-theft-represents-everything-that-could-go-wrong-with-ai/) downloaded 2026-10-27, read in full as text; quotes checked |
| Associated Press, "AI startup Perplexity wants to upend search business. News outlet Forbes says it's ripping them off" | Matt O'Brien, Sarah Parvini | 2024-06-14 | https://fox5sandiego.com/news/business/ap-business/ap-ai-startup-perplexity-wants-to-upend-search-business-news-outlet-forbes-says-its-ripping-them-off/amp/ | AP story as syndicated by FOX 5 San Diego, downloaded 2026-10-27, read in full as text; date from page metadata; quotes checked |
| Futurism, on the mushroom story | Victor Tangermann | 2024-06-22 | https://au.news.yahoo.com/asked-summarize-webpage-perplexity-instead-133530599.html | Syndicated copy on Yahoo News Australia, downloaded 2026-10-27, read as text; used only to confirm WIRED's account |
| Talking Biz News, "Perplexity plagiarizes Wired story about Perplexity" | Chris Roush | 2024-06-21 | https://talkingbiznews.com/media-news/perplexity-plagiarizes-wired-story-about-perplexity/ | Downloaded 2026-10-27, read as text; used only to confirm the follow-up's details |

## Corrections

This page needs review. If you have screenshots of the Perplexity answers WIRED describes, the original Perplexity post about the Schmidt story, Srinivas's posts on X, or a Perplexity statement on what changed in its answers after June 2024, tell us and we will update this page.
