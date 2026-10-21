---
title: "ChatGPT Bug Shows Some Users Other Users' Chat Titles; Service Taken Offline"
date: 2023-03-20
source: "https://openai.com/index/march-20-chatgpt-outage/"
summary: "On March 20, 2023 a bug in an open-source library let some ChatGPT users see titles from another active user's chat history. OpenAI took the service offline and later said payment-related details of about 1.2% of active ChatGPT Plus subscribers in a nine-hour window may also have been exposed. Read from a copy of OpenAI's post, The Register, the Business and Human Rights Resource Centre, the AI Incident Database and the Italian Garante's press release."
categories:
  - Governance
patterns:
  - third-party-data-shared-by-users
---

**This page is a dated teardown of one public chatbot incident, for teams whose chat product shows a history list or account details.** It describes what the sources report and what OpenAI said. It makes no claim about anyone's intent. Every fact below comes from a page we opened (listed at the end), mostly through a fetch tool that returns summaries.

**Read this first.** This is design analysis, not legal or privacy advice. Whether an incident like this triggers a notice duty is a question for your own legal team.

## What happened (as reported)

- **Monday, March 20, 2023.** A bug let some ChatGPT users see parts of other users' data. OpenAI took ChatGPT offline that day (The Register, March 23, 2023; OpenAI's post).
- **The cause, as OpenAI stated it.** "A bug in an open-source library." The copy of OpenAI's post we opened does not name the library. The Register's added section on OpenAI's March 24 follow-up says the bug was in the Asyncio redis-py client for Redis Cluster, that a system change at 0100 PT caused a spike in activity, and that the cache returned wrong information until 1000 PT. We read that only through a summary of The Register.
- **Titles.** Some users saw titles from another active user's chat history. The first message of a newly created conversation may also have been visible to another user active at the same time (OpenAI's post).
- **Payment-related data.** While fixing the bug, OpenAI found it may also have exposed payment-related details for about 1.2% of ChatGPT Plus subscribers who were active during a nine-hour window before the shutdown. The post lists first and last name, email address, payment address, card type, last four digits and expiration date. It says "Full credit card numbers were not exposed at any time." The same post describes two routes: subscription confirmation emails sent to the wrong users, and the "Manage my subscription" page. The window was March 20, 1 a.m. to 10 a.m. Pacific.
- **March 24, 2023.** OpenAI published its account (Business and Human Rights Resource Centre, republishing CMS Wire; The Register).
- **March 30-31, 2023.** The Italian data protection authority (the Garante) ordered a temporary limit on processing Italian users' data by OpenAI. Its March 31 press release mentions the March 20 breach as background. It lists four other grounds (no notice to users, no legal basis for mass collection of training data, answers that do not always match facts, no age check). It does not list the breach as a ground (Garante press release, fetched summary). We could not open the order itself.

## What the user saw

- Chat titles in the history list that were not theirs. OpenAI's post says "titles from another active user's chat history." Altman: "A small percentage of users were able to see the titles of other users' conversation history. We feel awful about this." (Altman on Twitter, as quoted by The Register.)
- Some users could not reach their March 20 conversations. Altman said most users could not access them that day (The Register, summary). OpenAI later restored chat history "except for a few hours" (OpenAI's post, fetched summary).
- For the payment case, the sources say another person would have had to open a subscription confirmation email or the manage-subscription page in the window to see it (AI Incident Database, summarizing Mashable). OpenAI believes the number of users whose data was actually revealed to someone else is "extremely low."

## Where in the flow it broke

The history sidebar and account pages each trust the answer from a shared cache. When the cache returned another user's items, the interface showed them as if they were the signed-in user's own. Nothing on screen separated "mine" from "someone else's." The sources describe a software fault, not a design choice, and do not say whether the interface had any second check. The post we opened does not mention one.

## Pattern match

- **No direct match, partial at best.** We searched the [privacy and governance family](../goals/privacy-and-governance/README.md) and the failure taxonomy. The closest page is [Third-party data shared by users](../goals/privacy-and-governance/failures/third-party-data-shared-by-users.md) (pattern ID `third-party-data-shared-by-users`). It covers a user's own pasted details about another person being repeated or saved. This case is different: the system itself showed one user's data to another, with no user action. The overlap is the harm to a person who never agreed to the exposure. Treat this as an adjacent case. A page for cross-account data showing up in the interface does not exist yet; that is a candidate gap for the library.

## What to measure

Proposed checks for a team with a history list or account page. None come from OpenAI. Status: Not yet run.

| Metric | How to compute |
|---|---|
| Cross-account render checks | Count of automated checks that sign in as user A, load history and account pages, and fail if any item's owner is not A |
| Owner check at display time | Share of list and detail views that verify the item's owner ID against the session before drawing it |
| Time to stop | Minutes from the first report of someone else's data to the feature being switched off or the service taken offline |
| Time to notify | Hours from confirming exposure to telling affected users, and what the notice said they could do |

## What a team can change

Proposed rules, each a pass/fail check. Status: Not yet run.

1. **Check ownership where the data is drawn, not only where it is fetched.** Check: a view that receives an item with a different owner ID shows nothing and logs an error.
2. **Add a test that two users active at once never see each other's items.** Check: it runs under load and with cancelled requests.
3. **Have a one-step switch to hide history and billing views.** Check: you can turn the list off without taking the whole chat down.
4. **Say what was exposed in plain words.** Check: the notice names the fields (for example "name, email, last four digits") and the dates, as OpenAI's post did.

## What stays unknown

- Exactly how many users saw another person's titles. The sources say "a small percentage" (Altman).
- How many of the 1.2% Plus subscribers had data actually seen by someone else. OpenAI says "extremely low" and gives no count.
- The exact library fault. The copy of OpenAI's post we opened does not name it (see above for The Register's account).
- What the history list looked like during the fault, and whether any user screenshots exist in the sources we opened. We saw none.
- How the Garante treated the breach in the order itself. We opened only the press release.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://openai.com/index/march-20-chatgpt-outage/ | OpenAI | March 2023 (no date shown in the copy we read) | Direct fetch returned HTTP 403. Read through a fetch of a proxy copy of the page (r.jina.ai), returned as a summary with five verbatim excerpts. The copy omits the linked technical details. |
| https://www.theregister.com/2023/03/23/openai_ceo_leak/ | The Register | 2023-03-23, with later OpenAI update | Yes, via fetch summary |
| https://www.business-humanrights.org/en/latest-news/openai-takes-chatgpt-offline-due-to-data-breach | Business and Human Rights Resource Centre (CMS Wire republished) | 2023-03-24 | Yes, via fetch summary |
| https://incidentdatabase.ai/reports/2908 | AI Incident Database (Mashable report) | 2023 | Yes, via fetch summary |
| https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/9870847 | Italian Garante, press release | 2023-03-31 | Yes, via fetch summary (release only, not the order) |

Not opened: the March 24 technical details page; the Garante order text; the Mashable and CMS Wire articles directly.

Not verified (seen only in search summaries, kept out of the text above): that ChatGPT was down "about 4 hours" (Russian-language outlets in search results); a December 2024 fine of 15 million euros reported by Altroconsumo; any details of Garante's later findings about breach notification.

## Where sources disagree

- **Library name.** The copy of OpenAI's post says only "an open-source library"; The Register's added section names redis-py. We did not open the technical details page to compare.
- **Garante and the breach.** News coverage links the order to the breach; the Garante press release as fetched lists other grounds.

## Caveats

- Nearly everything is through fetch summaries. Quoted phrases are as those summaries returned them.
- The OpenAI text came from a proxy copy, because the direct page was blocked. The copy showed no byline or date.

## Corrections

If you have OpenAI's original page, a screenshot of what users saw or a better date, tell us and we will fix this page.
