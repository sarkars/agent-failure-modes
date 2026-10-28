---
title: "Amazon Alexa reads a student paramedic a Wikipedia-sourced passage telling her to stab herself in the heart, December 2019"
date: 2019-12-20
source: "https://www.gearbrain.com/why-alexa-cannot-trust-wikipedia-2641657297.html"
description: "How an Echo Dot read a UK student a self-harm passage it credited to Wikipedia, text she could not find there, and what answer teams should check first."
summary: "In December 2019, Danni Morritt, a 29-year-old student paramedic from Doncaster, England, asked her Amazon Echo Dot about the cardiac cycle while studying. Alexa began with heart facts, then read a passage saying the heartbeat is bad for the planet and telling her to stab herself in the heart 'for the greater good.' Alexa credited the answer to Wikipedia. Morritt said she could not find the text on Wikipedia. The Wikipedia page's history shows a burst of edits on June 18-19, 2019 whose text has since been hidden, one with an edit summary saying it removed text urging suicide. An Amazon spokesperson told Newsweek: 'We have investigated this error and it is now fixed.'"
categories:
  - Trust and accuracy
  - General-Purpose Assistants
patterns:
  - stakes-blind-register
  - confident-wrong-answer-with-no-way-to-check
  - wrong-explanations-taught-as-fact
---

**This page is a dated teardown of one public incident in which a home voice assistant read an adult student a self-harm instruction from an open-edit web source, for teams whose assistant answers by reading or quoting retrieved third-party text.** The product was Alexa on an Amazon Echo Dot. The user was Danni Morritt, a student paramedic in England, who spoke to the press under her own name. The moment was a study question about the heart. Every fact below comes from a source we opened (listed at the end). No opened source has Amazon's own account of how the passage was chosen.

**Status: Needs review.** GearBrain (Alistair Charlton, December 20, 2019), Newsweek (James Crowley, December 24, 2019), Inquisitr (Anna Harnes, December 22, 2019), International Business Times Singapore (byline "Manthan C.," December 21, 2019) and Beebom (Subin B, December 28, 2019) were downloaded as raw HTML on 2026-10-28 and read as plain text. The revision history of the English Wikipedia article "Cardiac cycle" was read on 2026-10-28 through the MediaWiki API as raw JSON (revision IDs, times, sizes, edit summaries and, where not hidden, text). Each quote below was checked word for word against that text. The Sun, the Daily Mail and the Manchester Evening News, which the opened outlets credit, were not read: The Sun returned a bot-check page, and we found no working link to the other two. Their reporting appears here only as the opened outlets describe it.

> **Read this first.** This page involves an instruction to self-harm. It is design analysis, not medical, clinical or legal advice, and not a finding of fact. It summarizes press reports and a public edit history. We quote the passage only in short fragments and give no method detail beyond what the headline already names. No opened source reports that anyone was hurt. If you or someone you know is in crisis in the US, call or text 988, the Suicide & Crisis Lifeline; outside the US, contact a local crisis line. A clinician or crisis-line expert should review any rule here before it ships.

**Channel note.** This is a voice incident: a smart speaker read retrieved text aloud. This phase of the knowledge base is chat-first. The signals and checks below are written for text, such as the request, the retrieved passage and the answer text an assistant already logs. Voice signals, such as checking the spoken audio against the answer text, are PLANNED only: never detected or measured here.

## What happened (as reported)

- **The question.** GearBrain says Morritt "asked her Amazon Echo Dot a question related to her studies during a revision session." Newsweek says she asked Alexa to explain the "cardiac cycle of the heart."
- **The start of the answer.** GearBrain says Alexa "answered normally" first, with a typical heart rate. IBTimes quotes a different opening line about how long one cardiac cycle takes. See the gaps section.
- **The turn.** Every opened outlet reports that the answer went on to say the heartbeat is bad for the planet, because it keeps people alive to use up natural resources. It ended by telling her to kill herself by stabbing herself in the heart "for the greater good." GearBrain and IBTimes say Alexa then asked, "Would you like me to continue?"
- **The credited source.** Newsweek: "Alexa cited at the time that she was reciting from the 'cardiac cycle' Wikipedia page." GearBrain says Alexa's usual phrasing for such answers names the Wikipedia article it is reading from.
- **The recording.** Inquisitr and IBTimes say she recorded it on video; IBTimes says she asked Alexa to repeat itself so she could record it. Newsweek says a YouTube video "uploaded on December 19 purports to capture the comment."
- **Her reaction.** Newsweek quotes her, via the Manchester Evening News: "I'd only [asked for] an innocent thing to study for my course, and I was told to kill myself." Inquisitr says she "looked through multiple entries and did not find anything that even slightly matched" the words. Inquisitr says some people accused her of tampering with the device and that she denied it.
- **The household.** Newsweek says she removed an Echo from her seven-year-old son's room. Inquisitr says it was an Echo Dot.
- **Where it started.** GearBrain: "This incident comes from the Kennedy News & Media agency and was first reported by The Sun newspaper."

## What the company said

- **To Newsweek.** "We have investigated this error and it is now fixed," an Amazon spokesperson said, in a statement Newsweek dates to "Tuesday" in a story published December 24, 2019.
- **As others report it.** Inquisitr: an Amazon spokesperson "said that the company has already investigated the matter and that it had been fixed." Beebom says a spokesperson told the Daily Mail the error was fixed. Both are paraphrases.
- **What no opened source says.** What the fix was; why Alexa read text that was not on the live page; whether the fix covered one article, one question, or all Wikipedia answers; and whether Amazon screened answer text for self-harm wording. GearBrain guesses the fix "likely means pointing Alexa to a different Wikipedia article"; that is its guess, not Amazon's word.

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| The opening line | GearBrain: "A typically healthy heart rate is 70 to 75 beats per minute". IBTimes: "Each cardiac cycle or heartbeat takes about 0.8 seconds to complete the cycle". Both may be in the clip; we did not watch it. |
| The wording of the passage | The outlets' transcripts differ in small words ("beating of heart" or "beating of the heart"; "living in this world" or "living in this works"). IBTimes ends the instruction with a question mark. None publishes a transcript from Amazon. |
| Was the text on Wikipedia? | Morritt (via Inquisitr and Newsweek) could not find it. Newsweek says the revision history showed "a few months ago, the page did contain the disturbing message" and that someone edited it in June. Beebom states flatly that someone edited the page. |
| What the edit history shows us | On June 18, 2019, edits from anonymous addresses began at 18:11 UTC, with summaries such as "lol." The text of every revision from then until 15:24 UTC on June 19 is hidden from public view, so we cannot read it. The June 19 edit's summary says it deleted text telling readers to kill themselves. A June 30 edit reverted the page to the last version before those edits (18:06 UTC, June 18). |
| Why Alexa read it in December | If the June text was the source, Alexa read it about six months after it left the live page. Newsweek reports Outer Places' theory that Alexa read an older version of the page. Amazon has not said. |
| Which outlet broke it | GearBrain: Kennedy News & Media, then The Sun. Inquisitr and IBTimes cite The Sun. Newsweek cites the Manchester Evening News. Beebom cites the Daily Mail. |

## Where in the conversation flow it broke

Based on the reports above and the edit history, and only as far as they go. Amazon has not described its pipeline.

1. **The request.** An adult asked a plain study question about the heart. Nothing in it touched self-harm.
2. **Retrieval.** Alexa matched the question to the Wikipedia article on the cardiac cycle (as Alexa itself said, per Newsweek).
3. **A stale or tainted copy.** The text read aloud was not on the live page in December, by Morritt's account. The edit history is consistent with vandal text added and removed in June 2019, but the hidden revisions mean we cannot match the words.
4. **No screen on the passage.** An instruction to self-harm was read out in the same voice as the heart-rate fact before it. No opened source says any filter looked at it.
5. **"Would you like me to continue?"** Per GearBrain and IBTimes, the passage ended with an offer to read more, as if nothing unusual had been said.
6. **A credit the user could not check.** Alexa named Wikipedia. The user opened Wikipedia and found nothing. The credit pointed her to a page that no longer held the words.
7. **The user caught it, not the product.** She recorded it and went to the press. Amazon says it then fixed the error.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). Each fit rests on press reports and an edit history with hidden text; no opened source shows Amazon's logs.

- [Stakes-blind register](../goals/stakes-calibration/failures/stakes-blind-register.md) (`stakes-blind-register`). **Partial fit.** A self-harm instruction was delivered in the same flat answer format as a heart-rate fact, then followed by "Would you like me to continue?" The entry's point, notice high stakes and raise the bar, applies. It is partial because the entry is mostly about tone, and the failure here was what was said.
- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Partial fit.** The answer was false and harmful, and the source it named did not contain it when the user checked. It is partial because Alexa did name a source, which the entry treats as the fix; here the citation itself misled.
- [Wrong explanations taught as fact](../goals/education-agents/failures/wrong-explanations-taught-as-fact.md) (`wrong-explanations-taught-as-fact`). **Weak fit.** A student studying for a course got false content in the same voice as true content. It is weak because Alexa is not a tutor and the text was vandalism, not a mistaken explanation.
- **Considered, not a fit.**
  - [Missed crisis signals](../goals/vulnerable-users/failures/missed-crisis-signals.md) (`missed-crisis-signals`): the user gave no crisis signal; the assistant produced the harmful text unprompted. The entry's 988 and hand-off rules still apply to any team's output screen.
  - [Child user treated as adult](../goals/age-adaptation/failures/child-user-treated-as-adult.md) (`child-user-treated-as-adult`): the user was an adult. Her concern for the speaker in her son's room is reported, but no child heard this answer in any opened source.
  - [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (`one-sided-or-cherry-picked-sources`): about balance across sources. Here one source was used, and its text was tainted.
  - `no-way-to-report-bad-behaviour`: no opened source says Morritt tried to report it in the app or failed to.
- **Possible gaps for a person to judge.** (1) No taxonomy entry covers retrieved third-party text that has been vandalized or poisoned being read to the user as the assistant's answer. (2) No entry covers a cached or stale copy of a source that no longer matches the live page the assistant credits. (3) No entry covers screening every chunk of a long retrieved passage, including the "continue" chunks, for self-harm wording. These are proposals, not decisions.

## How it differs from close cases

- [Alexa reads a child the "penny challenge," December 2021](amazon-alexa-tells-child-to-do-penny-challenge-december-2021.md): the same device and the same "found on the web" answer path. There, Alexa lifted a real sentence out of a warning article and dropped its frame. Here, the source text itself appears to have been vandalized, and the user was an adult.
- [Alexa says the 2020 election was stolen, October 2023](amazon-alexa-says-2020-election-stolen-washington-post-october-2023.md): Alexa read claims from low-quality sources and Amazon fixed the flagged questions. That case is about false political claims; this one is about a direct instruction to self-harm.
- [Google AI Overviews odd and unsafe answers, May 2024](google-ai-overviews-odd-and-unsafe-answers-may-2024.md): an answer engine passed on jokes and unreliable text as fact. That was text on a screen with links the reader could see; this was one spoken passage the listener could not check.

## What to measure

Proposed signals, not results. Status: Not yet run. Text signals are proposed; voice signals are PLANNED only and are not detected or measured. Each can be computed from logs of an assistant that answers from retrieved text. Thresholds are for the team to set; we propose none.

- Share of answers built from retrieved third-party text whose text, including any "continue" chunks, matches the team's self-harm and violence instruction list.
- Share of answers that credit a named source where the quoted passage is not found in the source's current live version.
- Age of the retrieved copy: share of answers read from a cached copy older than the team's freshness window.
- Share of retrieved passages that came from a revision later reverted or hidden by the source site, where the source exposes that history.
- After a fix: the same question and ten paraphrases rerun, with a count of answers that still match the instruction list.
- Planned for voice only, not measured: whether the spoken audio matches the logged answer text.

## What a team can change

Our proposals, not Amazon's. Each is a pass/fail check on a text transcript or a test run. Status: Not yet run.

1. **Screen every chunk before it is read.** Pass: no answer built from retrieved text, including the parts offered after "continue," contains an instruction to self-harm. If one is found, the chunk is dropped and the answer ends.
2. **Read only what the source says now.** Pass: before a passage is read, it is matched against the current live version of the credited page; if it is not found, the passage is not used.
3. **Skip text the source has removed.** Pass: for open-edit sources that publish history, a passage that came from a revision later reverted or hidden is never served.
4. **Make the credit checkable.** Pass: the answer names the article, and in a test the user can find the passage there. If not, rule 2 failed.
5. **Fix the class, not the question.** Pass: after a fix, the original question and at least ten paraphrases about the same topic are rerun, and none returns instruction-list text. Record the results.
6. **Don't over-correct.** Pass: "Explain the cardiac cycle" still gets a plain, factual answer, and a question about suicide statistics or prevention still gets a factual answer with a crisis line such as 988, not a refusal (see [Missed crisis signals](../goals/vulnerable-users/failures/missed-crisis-signals.md)).

## What we could not verify

- **The words in the June 2019 edits.** Their text is hidden in Wikipedia's public history, so we cannot match them to what Alexa said. We rely on the edit summaries, Newsweek's report, and the outlets' transcripts.
- **The audio.** We did not watch the YouTube clip or the Daily Mail video. All wording comes from the outlets' transcripts, which differ slightly.
- **How Alexa got the text.** No opened source says whether Amazon used a cached copy, a data dump, or another feed. Outer Places' theory is reported only through Newsweek.
- **The fix.** See above. We found no opened source that tested Alexa's answer after the fix.
- **The Sun, Daily Mail and Manchester Evening News reports, and the Kennedy News & Media copy.** Seen only as described by other outlets; not opened.
- **Seen only in search summaries and not used:** coverage by AOL, Albawaba, Asianet Newsable, OrissaPOST, NewsBytes, Digit, Le Tribunal du Net and a later Sun roundup of Alexa bugs. A Beebom line about the user's health is personal and is not repeated here.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://www.gearbrain.com/why-alexa-cannot-trust-wikipedia-2641657297.html | GearBrain (Alistair Charlton) | 2019-12-20 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.ibtimes.sg/alexas-ai-goes-rogue-asks-woman-kill-herself-humans-are-bad-planet-36329 | International Business Times Singapore (Manthan C.) | 2019-12-21 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.inquisitr.com/rogue-amazon-alexa-stab/ | Inquisitr (Anna Harnes) | 2019-12-22 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.newsweek.com/amazon-echo-tells-uk-woman-stab-herself-1479074 | Newsweek (James Crowley) | 2019-12-24 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://beebom.com/alexa-told-woman-to-stab-herself/ | Beebom (Subin B) | 2019-12-28 | Yes, 2026-10-28, raw HTML read as text; used only for its Daily Mail attribution |
| https://en.wikipedia.org/w/index.php?title=Cardiac_cycle&action=history | Wikipedia, "Cardiac cycle" revision history | Revisions of 2019-06-04 to 2019-12-30 | Yes, 2026-10-28, through the MediaWiki API as raw JSON; edit times, summaries and hidden-text flags checked; text of revisions 902420184 to 902545653 is hidden |

Not opened: The Sun (bot-check page returned), the Daily Mail, the Manchester Evening News, the YouTube clip, and Outer Places.

## Corrections

If you have Amazon's account of where Alexa got this passage or what the fix changed, the original Sun or Manchester Evening News report, or a dated test of Alexa's answer to the same question, tell us and we will fix this page.
