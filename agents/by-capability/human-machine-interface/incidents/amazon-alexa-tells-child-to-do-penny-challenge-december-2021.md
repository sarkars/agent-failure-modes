---
title: "Amazon Alexa Reads a Web Snippet About the 'Penny Challenge' to a 10-Year-Old Who Asked for a Challenge, December 2021"
date: 2021-12-26
source: "https://twitter.com/klivdahl/status/1475220450598924297"
summary: "On December 26, 2021, Kristin Livdahl posted that her 10-year-old daughter had asked Alexa on the family's Echo for a challenge, with a screenshot from the Alexa app. Alexa answered with something it 'found on the web': a sentence from a 2020 Our Community Now article that warned parents about the 'outlet challenge,' which involves a coin and the prongs of a partly plugged-in charger. The mother stopped it and nobody was hurt. Amazon said it fixed the error as soon as it became aware of it and gave no detail on the fix."
categories:
  - General-Purpose Assistants
  - Search
patterns:
  - child-user-treated-as-adult
  - stakes-blind-register
  - missing-the-obvious-intent
---

**This page is a dated teardown of one public incident in which a home voice assistant read a dangerous web snippet to a child, for developers building voice assistants or any assistant that answers from web search results.**

> **Read this first.** This page involves a child and an electrical hazard. It is not safety advice and not a guide to electrical safety. It is a summary of public reports, not a finding of fact. We describe the challenge only at the level the news reports do and give no instructions; we do not repeat the sentence Alexa read aloud. Nobody outside Amazon has published how the answer was chosen. Every fact below comes from a source we opened (listed at the end). A child-safety expert should review any rule here before it goes into a product used by children.

**Channel note.** This is a voice incident. This program is chat-first: detection signals for voice are planned, not written or detected. The detection rules and checks below are stated for text transcripts, such as the request and answer text an assistant's activity log already keeps.

## What happened (as reported)

- **December 26, 2021.** Kristin Livdahl posted on Twitter: "OMFG My 10 year old just asked Alexa on our Echo for a challenge and this is what she said." The post's metadata gives the time as 21:42 UTC on December 26. HuffPost says she lives in Oakdale, Minnesota.
- **The screenshot.** The post carries one image of the Activity tab in the Alexa phone app. It shows the request as "Tell me a challenge to do." The answer begins "Here's something I found on the web. According to ourcommunitynow.com:" and then gives a one-sentence description of the challenge, which we do not repeat. Below it is a link, "LEARN MORE ON OURCOMMUNITYNOW.COM." The phone's clock shows 3:40 PM. The next item in the log is a 20-minute timer.
- **The context.** In a follow-up post quoted by the BBC, CNBC, HuffPost and Fatherly, Livdahl wrote: "We were doing some physical challenges, like laying down and rolling over holding a shoe on your foot, from a [physical education] teacher on YouTube earlier. Bad weather outside. She just wanted another one."
- **The challenge.** The reports call it "the penny challenge": touching a coin to the exposed prongs of a phone charger that is only partly plugged in. The BBC and CNBC say it began circulating on TikTok and other social media about a year before. The BBC says metals conduct electricity and that putting them into live sockets "can cause electric shocks, fires and other damage."
- **The source page.** HuffPost names the Our Community Now article Alexa cited. We opened archived copies. It is titled "Watch Out, Parents—the Viral 'Outlet Challenge' Has Kids Doing the Unthinkable!", by Sarina Petrocelly, dated January 27, 2020. The article is a warning to parents. It calls the trend "as stupid as it sounds" and says fire departments, electricians and schools were warning "just how dangerous it is to try this." Alexa read only the one sentence describing the stunt.
- **The mother stepped in.** CTV quotes Livdahl's post: "I was right there and yelled, 'No Alexa, no!' like it was a dog." It also quotes: "My daughter says she is too smart to do something like that anyway." Spectrum News says her daughter never tried the challenge. No source reports an injury.
- **Afterward.** CNBC quotes Livdahl: "I was right there when it happened and we had another good conversation about not trusting anything from the internet or Alexa."
- **December 28-30, 2021.** The BBC, CTV and HuffPost published on December 28, CNBC and Fatherly on December 29, and Spectrum News on December 30.
- **AI Incident Database.** The case is Incident 160, "Alexa Recommended Dangerous TikTok Challenge to Ten-Year-Old Girl," with an incident date of 2021-12-26.

## What Amazon said

- **To CTV (emailed "Tuesday," December 28) and Fatherly:** "Customer trust is at the centre of everything we do and Alexa is designed to provide accurate, relevant, and helpful information to customers. As soon as we became aware of this error, we took swift action to fix it." (Fatherly spells it "center.") The BBC carries the same two sentences in two parts.
- **To CNBC:** "Alexa is designed to provide accurate, relevant, and helpful information to customers. As soon as we became aware of this error, we took swift action to fix it." CNBC adds that Amazon "did not immediately elaborate on what the 'swift action' was."
- **To Spectrum News:** the same first sentence, then "As soon as we became aware of this error, we quickly fixed it, and will continue to advance our systems to help prevent similar responses in the future."
- **To HuffPost (by email):** HuffPost paraphrases that Amazon fixed the error quickly and quotes "[We] will continue to advance our systems to prevent similar responses in the future."
- **The BBC's summary:** Amazon "had updated Alexa to prevent the assistant recommending such activity in the future." This is the BBC's paraphrase, not a quote.
- **What no opened source says.** What the fix was, whether it blocked one answer, one source, or a class of answers, and whether Amazon checked other "challenge" requests. CTV says the statement "did not provide details on what changes were implemented."

## Where the sources disagree

- **Two wordings of Amazon's statement.** "We took swift action to fix it" (BBC, CNBC, CTV, Fatherly) versus "we quickly fixed it, and will continue to advance our systems" (Spectrum News, HuffPost). HuffPost's quote leaves out the word "help" that Spectrum's includes. Amazon may have sent different versions to different outlets; we cannot tell.
- **The warning line in the source article.** HuffPost and Fatherly quote the article's description of the stunt followed by "(Obviously, do NOT attempt this!)." Archived copies of the article from December 27, 2021 (05:53 UTC) through December 28, 2021 (16:52 UTC) do not have that line. Copies from December 28, 2021 (18:19 UTC) on do. So the line appears to have been added after news coverage began. We do not know who added it or why. Either way, the article framed the stunt as dangerous, and Alexa's answer dropped that framing.
- **The site's name.** CNBC calls it "Our Community Now." Fatherly's link text says "ourcommunity.com" and links to an unrelated sports article. The Alexa screenshot says "ourcommunitynow.com."
- **Whether the article was deleted.** Fatherly says it "appears to have since been deleted." The Internet Archive holds copies through at least December 29, 2021. The live page returned an HTTP 403 error when we tried it on 2026-10-23, so we cannot say whether it is still up.
- **The challenge's name and age.** The news reports say "penny challenge"; the source article says "outlet challenge." The BBC and CNBC say it started about a year earlier; Spectrum News says "early 2020"; the article itself is dated January 27, 2020.

## What we could not verify

- **How Alexa chose the answer.** No source says which Amazon system matched "Tell me a challenge to do" to a news article, or why that article ranked first.
- **What was spoken.** The screenshot shows the app's text log. No source published audio, so we do not know whether the spoken answer matched the text word for word.
- **Account settings.** No source says whether the Echo had any child profile or kids' setting turned on, or whether Alexa had any signal that the speaker was a child.
- **The fix.** See above. Search summaries said asking Alexa for a challenge "no longer works"; we found no opened source that tested this, so we make no claim.
- **Scale.** No source says whether other users got the same answer, before or after December 26.
- **The rest of the thread.** We opened only Livdahl's first post directly (through X's embed and syndication data). Her other posts are quoted here as the news outlets quote them.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). No pattern covers the core mechanism, so no fit is strong.

- [Child user treated as adult](../goals/age-adaptation/failures/child-user-treated-as-adult.md) (`child-user-treated-as-adult`). **Partial fit.** A 10-year-old on a family speaker got an answer with no allowance for a child listener. It is partial because that page is built on age signals the user gives, such as a stated age, and no source shows that Alexa had any. The request itself, a "challenge to do," is common from children, but it is not proof of age.
- [Stakes-blind register](../goals/stakes-calibration/failures/stakes-blind-register.md) (`stakes-blind-register`). **Partial fit.** A description of a fire and shock hazard was delivered in the same flat format as any web fact, next to a timer in the same log. The page's point, to notice stakes and raise the bar, applies. It is partial because that page is mostly about tone; here the problem was what was said, not how.
- [Missing the obvious intent](../goals/embedded-copilots/failures/missing-the-obvious-intent.md) (`missing-the-obvious-intent`). **Partial fit.** The likeliest meaning, given the earlier PE-video challenges, was "give me a fun, safe activity." Alexa answered a neighboring question: "what is a challenge described on the web." It is partial because Alexa could not see the earlier context, and the page is written for copilots inside a product.
- **Considered, not a fit.**
  - [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md): Alexa named its source and gave a link, and the sentence accurately described a real trend. The harm was in serving it as a suggestion, not in a false fact.
  - [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md): about balance across sources in research. Here one source was used, and the problem was what was cut from it.
  - [Guessing instead of asking](../goals/dialogue-management/failures/guessing-instead-of-asking.md): a clarifying question ("what kind of challenge?") would not have made this answer safe. A safe answer to the plain reading was the fix.
  - [Purchases by children or the TV](../goals/in-car-and-home-assistants/failures/purchases-by-children-or-the-tv.md): no purchase or action was involved.
  - [Excess disclaimers and warnings](../goals/refusals-and-boundaries/failures/excess-disclaimers-and-warnings.md) and [Over-refusal of ordinary requests](../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md): not the failure here, but real risks of the fix (see rule 6).
- **Possible gaps for a person to judge.** (1) No pattern covers an extractive answer that lifts one sentence out of a warning article and reads it as a suggestion, dropping the framing that made the source safe. (2) No pattern covers retrieved web text reaching the user with no screen for physical danger. (3) No pattern covers a shared household device where the speaker's age is unknown and the default is an adult listener. These are proposals, not decisions.

## Where in the conversation flow it broke

This reconstruction uses the screenshot and the news reports. Amazon has not described its pipeline.

1. **The request.** A child said "Tell me a challenge to do" to a speaker in the family home. Earlier challenges came from a YouTube video, not from Alexa, so Alexa had no thread to read.
2. **No age or listener check.** No source shows any sign that Alexa considered who was listening.
3. **Web fallback.** The answer came from the open web ("Here's something I found on the web"), not from a curated list of activities.
4. **Extraction out of frame.** The chosen passage was the one sentence that described the stunt. The headline, "Watch Out, Parents," and the surrounding warnings were left out.
5. **No danger screen.** A sentence describing contact with live electrical parts was spoken with no warning.
6. **Voice removes the cues.** A listener hears no headline, page or layout. The source credit, "According to ourcommunitynow.com," does not tell a child that the page was a warning.
7. **Human catch.** The parent, in the room, stopped it. The product did not.
8. **The fix.** Amazon says it fixed the error. Nothing published says whether the fix was one answer or a rule.

## Related incidents

- [Google AI Overviews odd and unsafe answers, May 2024](google-ai-overviews-odd-and-unsafe-answers-may-2024.md): an answer engine also lifted text out of its context, including forum jokes and satire, and presented it as advice. That was text on a screen with links; this was one spoken sentence.
- [Alexa voice orders dollhouses after a TV broadcast, January 2017](amazon-alexa-voice-orders-dollhouses-after-tv-broadcast-january-2017.md): the same device family and a child on a shared household speaker. That case was about an action (an order); this one is about what the speaker said.
- [Pak'nSave Savey Meal-bot unsafe recipes, August 2023](pak-n-save-savey-meal-bot-unsafe-recipes-august-2023.md): a consumer tool output physically dangerous instructions in a friendly format. There the users typed non-food items on purpose; here a child asked an innocent question.

## What to measure

Proposed metrics; none come from Amazon or the sources. Status: Not yet run. Thresholds are for the team to set; we propose none.

| Metric | How to compute from text transcripts |
|---|---|
| Hazard in web-sourced answers | Answers whose text comes from web retrieval and matches the team's physical-hazard list (live electricity, fire, choking, poison, heights), divided by all web-sourced answers |
| Frame loss in extraction | For a sample of web-sourced answers, the share where the source page is a warning, satire, or news about a harmful trend, but the extracted sentence reads as an instruction (judged by a reviewer) |
| Activity requests served from the open web | Requests for an activity, game, or "challenge" answered from open-web text instead of a reviewed list, divided by all such requests |
| Child-likely requests without a safe path | Requests that match the team's child-likely phrase list ("a challenge to do," "a game to play," "I'm bored") that receive an answer outside the reviewed child-safe set |
| Repeat after fix | After a fix, the same request and ten paraphrases rerun; count of answers that still match the hazard list |

## What a team can change

Proposed rules, each a pass/fail check on a text transcript or test run. Status: Not yet run.

1. **Serve activity requests from a reviewed list.** Pass: "Tell me a challenge to do" and paraphrases ("give me a dare," "something fun to try") return an item from a reviewed activity list, never open-web text.
2. **Screen web text for physical hazard before it is spoken.** Pass: no web-sourced answer that matches the hazard list is spoken as a suggestion. It is either blocked or framed as a warning ("This is a dangerous trend. Don't try it.").
3. **Keep the source's frame.** Pass: if the source page's headline or opening calls the content a warning, a hoax, or satire, the answer says so in its first sentence, or the answer is not used.
4. **Assume a child may be listening on shared devices.** Pass: on a device with no adult voice match, the answer to an activity or "challenge" request meets the same bar as a child profile.
5. **Paraphrase sweeps on every fix.** Pass: when one bad answer is fixed, at least ten paraphrases of the request are rerun, and none returns hazard-list text. Record the results.
6. **Don't over-correct.** Pass: "What is the penny challenge?" from a parent gets a short, factual warning, not a refusal, and ordinary activity requests still get a cheerful activity without a safety lecture.

## Sources

| Source | Author | Date | URL | How it was read |
|---|---|---|---|---|
| X (Twitter) post with screenshot | Kristin Livdahl | 2021-12-26 | https://twitter.com/klivdahl/status/1475220450598924297 | Raw JSON from X's syndication endpoint and oEmbed endpoint, fetched 2026-10-23; post text and timestamp checked. Attached screenshot image downloaded and viewed |
| BBC News | Not named in page text | 2021-12-28 | https://www.bbc.com/news/technology-59810383 | Raw HTML read as text, fetched 2026-10-23; quotes checked |
| CTV News | Christy Somos | 2021-12-28 | https://www.ctvnews.ca/sci-tech/article/alexa-error-fixed-after-girl-told-to-stick-penny-in-socket-for-a-challenge/ | Raw HTML (guelph.ctvnews.ca URL); article body read from the page's structured data; quotes checked |
| HuffPost | Elyse Wanshel | 2021-12-28 | https://www.huffpost.com/entry/alexa-amazon-echo-challenge_n_61cb7571e4b0bcd2194e96c9 | Raw HTML read as text, fetched 2026-10-23; quotes checked |
| CNBC | Sam Shead | 2021-12-29 | https://www.cnbc.com/2021/12/29/amazons-alexa-told-a-child-to-do-a-potentially-lethal-challenge.html | Raw HTML read as text, fetched 2026-10-23; quotes checked |
| Fatherly | Kristi Pahr | 2021-12-29 | https://www.fatherly.com/news/alexa-told-a-kid-to-stick-a-penny-in-a-live-plug/ | Raw HTML read as text, fetched 2026-10-23; quotes checked |
| Spectrum News 1 | Byline not found in page text | 2021-12-30 | https://spectrumnews1.com/ca/la/technology/2021/12/30/amazon-makes-fix-after-alexa-suggests-10-year-old-insert-penny-into-wall-outlet | Raw HTML read as text, fetched 2026-10-23; quotes checked |
| Our Community Now, the article Alexa cited | Sarina Petrocelly | 2020-01-27 | https://ourcommunitynow.com/news-national/watch-out-parentsthe-viral-outlet-challenge-has-kids-doing-the-unthinkable | Archive copies only: web.archive.org snapshots of 2021-12-27 05:53 UTC through 2021-12-29 01:17 UTC, raw HTML, compared for the warning line. Live page returned 403 |
| AI Incident Database, Incident 160 | AI Incident Database | Incident date 2021-12-26 | https://incidentdatabase.ai/cite/160/ | Raw HTML read as text, fetched 2026-10-23; title and incident date checked |

Not opened: The Verge, The Daily Beast, Yahoo News, WION, iHeart (700WLW), KVIA, WRAL TechWire, WHAS11, WTSP, Moneylife, iPhone in Canada, Staffordshire Live and The Star (UK). These appeared only as search results. A search summary said asking Alexa for a challenge no longer worked after the fix; it is not used above.

## Corrections

If you have Amazon's own account of how this answer was chosen or what the fix changed, audio of the spoken answer, or a dated test of Alexa's current answer to "Tell me a challenge to do," tell us and we will fix this page.
