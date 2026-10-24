---
title: "DeepSeek Left a Log Database Open on the Internet, Exposing Chat History and API Keys, January 2025"
date: 2025-01-29
source: "https://www.wiz.io/blog/wiz-research-uncovers-exposed-deepseek-database-leak"
description: "Wiz Research found an open, unauthenticated DeepSeek database whose logs held users' chat messages in plain text, API keys and backend details."
summary: "On January 29, 2025, Wiz Research said it found a publicly accessible ClickHouse database belonging to DeepSeek, open with no login, holding over a million log lines with chat history, secret keys and backend details. Wired reported the database was locked down within a half hour of Wiz's contact attempts. No opened source says whether anyone else got the data. The Italian Garante's January 30 order, which we opened, does not mention the exposure. Status: Needs review."
categories:
  - Security
  - Governance
patterns:
  - sensitive-data-collected-in-chat
  - third-party-data-shared-by-users
---

**This page is a dated teardown of one public security finding about a consumer chatbot, for teams that log what users type into a chat and store those logs in an analytics or debugging system.** It describes what the sources report. It makes no claim about anyone's intent. Every fact below comes from a source we opened (listed at the end).

**Read this first.** This page summarizes public reporting. It is design analysis, not legal or security advice. It does not say whether DeepSeek broke any law; the only regulator text we cite is an order we opened, and that order does not address this exposure. Have a qualified security engineer review your own logging and databases. We do not reproduce any leaked key, secret, hostname detail or log line; we describe only the types of data.

**Status: Needs review.** The Wiz post, Wired, BleepingComputer, The Hacker News, TechCrunch and the Garante order were downloaded as raw HTML on 2026-10-24 and read as text. Each quote below was checked word for word against that text. Nothing presented as read was read only through a summary tool.

## What happened (as reported)

- **The finding.** Wiz Research (post by Gal Nagli, dated January 29, 2025) says it found a publicly accessible ClickHouse database linked to DeepSeek, "completely open and unauthenticated." Wiz says it was found "Within minutes" of starting to map DeepSeek's internet-facing systems. It was reachable on two DeepSeek subdomains on non-web ports.
- **What it held.** Wiz says the exposure included "over a million lines of log streams containing chat history, secret keys, backend details, and other highly sensitive information." One table held over 1 million log entries, with timestamps from January 6, 2025. Wiz says its columns included plaintext logs with chat history, API keys, backend details, operational metadata and directory structures.
- **How it could be read.** Wiz says the database's web interface allowed arbitrary SQL queries from a browser, with no login. It says the access allowed full database control and "potential privilege escalation" inside DeepSeek's environment.
- **What Wiz did not do.** Wiz writes: "We did not execute intrusive queries beyond enumeration to preserve ethical research practices."
- **January 29, 2025 (Wednesday).** Wired (Lily Hay Newman and Matt Burgess) reports that Wiz sent its findings to every DeepSeek email address and LinkedIn profile it could find or guess. Wired says that "within a half hour of their mass contact attempt, the database they found was locked down." Wired says the researchers had not received a reply. Wiz's post says DeepSeek "promptly secured the exposure."
- **The chat content.** Wired says the logs held "the users’ prompts and other interactions with the service," and that "The prompts the researchers saw were all in Chinese." TechCrunch (January 30), citing Wired, says the chat logs were in Chinese "but easily translated."
- **January 30, 2025.** BleepingComputer, The Hacker News and TechCrunch reported the finding. TechCrunch: "DeepSeek did not respond to a request for comment." Wired says DeepSeek "did not immediately respond" to its request.
- **Same week, separate events.** The Hacker News says DeepSeek had paused registrations after what DeepSeek called "large-scale malicious attacks." BleepingComputer says registrations were suspended for nearly 24 hours. No opened source links those attacks to the open database.
- **January 30, 2025, Italy.** The Italian data protection authority (the Garante) ordered an urgent, immediate limit on DeepSeek's processing of data of people in Italy (order n. 33, which we opened). The order says DeepSeek's January 29 reply stated the companies "had not entered and had not planned to enter the Italian market." It finds breaches of GDPR Articles 31, 12, 13, 14, 6, 32 and 27 and of Chapter III rights. It cites the privacy policy's statement that data are stored in China. **The order's text does not mention the Wiz finding, a database or logs.** We do not link the order to the exposure.

## What the user saw

Nothing. No opened source says users were told their chats had been in an open database. A user typing into the DeepSeek chatbot had no sign that the message was also written, in plain text, to a log store reachable from the internet. No source quotes a notice to users.

## Where in the flow it broke

1. **The user types a message.** Wired says prompts and other interactions were in the logs.
2. **The backend logs the full message.** Per Wiz, chat text went into a log table in plain text, next to API keys and backend details.
3. **The log store is open.** Per Wiz, the database needed no login and accepted queries from a browser.
4. **No one notices until outsiders do.** Wiz found it within minutes. Wired says it was locked down within a half hour of Wiz's contact attempts.
5. **No account to users.** No opened source shows DeepSeek telling users what was exposed, for how long, or whether anyone else read it.

The sources describe an infrastructure fault, not a model behavior fault. No source says the chatbot's answers were wrong. The chat-design lesson is in step 2: what the product chose to keep from each chat, and where.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [Sensitive data collected in chat](../goals/channel-selection/failures/sensitive-data-collected-in-chat.md) (`sensitive-data-collected-in-chat`). **Partial fit.** That pattern is about a bot asking for card numbers, SSNs or passwords. DeepSeek's bot did not ask for those, per the sources. The overlap: whatever users typed was kept in plain text in a log store, and that store was exposed. The pattern's lesson, keep only what the task needs and protect what you keep, applies directly to chat logs.
- [Third-party data shared by users](../goals/privacy-and-governance/failures/third-party-data-shared-by-users.md) (`third-party-data-shared-by-users`). **Weak fit.** If users pasted other people's details into chats, those details sat in the same logs. No opened source says such data was seen. We include it because the logging choice puts people who never used the product at risk too.
- **Considered, not mapped.** [Copy, share, and export lose content](../goals/chat-interface/failures/copy-share-and-export-lose-content.md) (`copy-share-and-export-lose-content`): used for the Meta AI and ChatGPT shared-link cases, but here no user shared anything. [Privacy-rights requests not recognised](../goals/privacy-and-governance/failures/privacy-rights-requests-not-recognised.md) (`privacy-rights-requests-not-recognised`): the Garante cites Chapter III rights, but no source shows a user request the bot missed. [No user-facing record of what the bot said](../goals/privacy-and-governance/failures/no-user-facing-record-of-what-the-bot-said.md) (`no-user-facing-record-of-what-the-bot-said`): the problem was too much record in the wrong place, not too little for the user.
- **Possible gaps for a person to judge.** (1) No pattern covers full chat text written to operational or debug logs, outside the chat store users can see and delete. (2) As the [McHire teardown](mchire-paradox-ai-hiring-chatbot-exposes-applicant-records-july-2025.md) notes, no pattern covers weak access control around a chat store. (3) No pattern covers a chat product that says nothing to users after their chats were exposed. Proposals, not decisions.

## Related incidents

- [ChatGPT chat-titles bug (March 2023)](openai-chatgpt-bug-exposes-other-users-chat-titles-march-2023.md): chat history shown to the wrong users through a cache fault.
- [Meta AI Discover feed (June 2025)](meta-ai-discover-feed-shows-private-chats-june-2025.md): private-looking chats made public through a share flow.
- [ChatGPT shared links indexed (July 2025)](chatgpt-shared-links-indexed-by-search-engines-july-2025.md): shared chats found in search results.
- [McHire and Paradox.ai (2025)](mchire-paradox-ai-hiring-chatbot-exposes-applicant-records-july-2025.md): recruiting-chat records exposed by weak access control.

## What to measure

Proposed signals, not results. Status: Not yet run.

| Signal | How to compute |
|---|---|
| Chat text in logs | Share of log tables, outside the main chat store, whose fields contain raw user message text. Target: zero, or a named and approved exception. |
| Secrets in logs | Count of log lines matching key or token formats in a daily scan. Target: zero. |
| Open data stores | Count of databases or admin consoles reachable from the internet without a login, from an outside scan of every subdomain and port. Target: zero. |
| Log age | Oldest record holding user chat text in any non-chat store, in days, against the stated retention. |
| Time to close | Minutes from the first outside report to the store being unreachable. |
| Time to tell users | Days from confirming exposure to a notice that names the data types and dates. |

## What a team can change

Our proposals, not DeepSeek's. Each is a pass/fail check. Status: Not yet run.

1. **Do not log full chat text by default.** Pass: debug and analytics logs store a message ID and length, not the message, unless a reviewed exception says otherwise.
2. **Strip secrets before writing logs.** Pass: a test that sends a fake key in a request finds no copy of it in any log.
3. **No data store without a login.** Pass: an outside scan of every subdomain and port finds no database or admin console that answers without credentials.
4. **Keep chat logs on the same delete and retention rules as the chat.** Pass: when a user deletes a chat, a search of every log store for its ID returns nothing after the stated period.
5. **Publish a security contact.** Pass: a researcher can find one address for reports in under a minute. Wired says Wiz had to guess.
6. **Tell users in plain words.** Pass: after an exposure, the notice names the data types (for example "chat messages you typed"), the dates, and what users can do.

## What is unverified

- **Whether anyone else accessed the data.** Wired, BleepingComputer, The Hacker News and TechCrunch all say this is unknown.
- **How long the database was open.** TechCrunch says it is not known. Wiz gives log timestamps from January 6, 2025, which is not the same as the exposure start.
- **How many users' chats were in the logs.** Sources count log lines (over a million), not users.
- **Whose keys were exposed.** Wired says "users’ API authentication tokens"; BleepingComputer describes "keys used by backend systems to authenticate API calls." Wiz says "API Keys" and "secret keys." We did not resolve this.
- **Any DeepSeek statement.** We found none. Wiz says DeepSeek secured the database; no source quotes DeepSeek.
- **Any user notice or regulator action about this exposure.** We opened none. The Garante order does not mention it.
- **The Garante order's date of the privacy policy.** The order we opened says the policy was "updated as of 5 December 2025," which is after the order's date. We did not resolve this; we do not use that date.
- **Later events.** BleepingComputer's page links a later story headlined as a DHS ban on DeepSeek products across US federal civilian agencies. We did not open it. Not used.

## Sources

| URL | Publisher (author) | Date | Opened |
|---|---|---|---|
| https://www.wiz.io/blog/wiz-research-uncovers-exposed-deepseek-database-leak | Wiz Research (Gal Nagli) | 2025-01-29 | Yes, 2026-10-24, raw HTML read as text; quotes checked word for word |
| https://www.wired.com/story/exposed-deepseek-database-revealed-chat-prompts-and-internal-data/ | Wired (Lily Hay Newman, Matt Burgess) | 2025-01-29 | Yes, 2026-10-24, raw HTML read as text; quotes checked word for word |
| https://www.bleepingcomputer.com/news/security/deepseek-exposes-database-with-over-1-million-chat-records/ | BleepingComputer (Bill Toulas) | 2025-01-30 | Yes, 2026-10-24, raw HTML read as text; quotes checked word for word |
| https://thehackernews.com/2025/01/deepseek-ai-database-exposed-over-1.html | The Hacker News (Ravie Lakshmanan) | 2025-01-30 | Yes, 2026-10-24, raw HTML read as text; quotes checked word for word |
| https://techcrunch.com/2025/01/30/deepseek-exposed-internal-database-containing-chat-histories-and-sensitive-data/ | TechCrunch (Zack Whittaker) | 2025-01-30 | Yes, 2026-10-24, raw HTML read as text; quotes checked word for word |
| https://www.garanteprivacy.it/home/docweb/-/docweb-display/print/10098477 | Italian Garante, order n. 33 (Italian and English text) | 2025-01-30 | Yes, 2026-10-24, raw HTML read as text; quotes checked against the English text |

Seen only in search results, so kept out of the text: CyberInsider, Silicon Canals, Security Affairs, Futurism, BGR and a second BleepingComputer story. The Garante's January 28 and 30 press releases are linked from the order page but were not opened. Reuters and AP coverage did not appear in our searches.

## Corrections

If you have a DeepSeek statement, a user notice, or a regulator decision about this exposure, tell us and we will fix this page.
