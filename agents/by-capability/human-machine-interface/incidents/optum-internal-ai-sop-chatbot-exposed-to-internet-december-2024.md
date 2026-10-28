---
title: "UnitedHealth's Optum left an internal AI chatbot for claims procedures, reported as \"SOP Chatbot,\" reachable from the internet with no password, December 2024"
date: 2024-12-13
source: "https://techcrunch.com/?p=2931052"
description: "How an internal Optum AI chatbot that answered employee questions on claims procedures could be reached from the public internet with no password."
summary: "On December 13, 2024, TechCrunch (Zack Whittaker) reported that Optum, part of UnitedHealth Group, had restricted access to an internal AI chatbot after Mossab Hussein of spiderSilk found it could be reached from the internet in a web browser with no password. The bot, called \"SOP Chatbot,\" answered employee questions about handling health insurance claims and disputes under the company's standard operating procedures. TechCrunch said it saw stored chat history, including an employee asking what the determination of a claim should be. Optum called it a demo and proof of concept that was never put into production, and said no protected health information was used. The bot went offline soon after TechCrunch contacted Optum. Becker's Hospital Review and Futurism followed on December 16, 2024."
categories:
  - Security
  - Privacy
patterns:
  - eligibility-answers-sound-like-decisions
  - small-talk-and-off-topic-messages-handled-badly
  - sensitive-data-collected-in-chat
---

**This page is a dated teardown of public reporting on an internal Optum claims-procedure chatbot that was left reachable from the internet, for teams that build internal AI assistants over company documents and keep their chat logs.** Every fact below comes from a source we opened (listed at the end). The bot was built for employees, not for patients or members.

**Status: Needs review.** TechCrunch's story, Becker's Hospital Review (read through an Internet Archive copy), Futurism and the Slashdot post were downloaded as raw HTML on 2026-10-28 and read as plain text. Each quote below was checked word for word against that text. Becker's and Futurism both build on TechCrunch's reporting; Becker's adds its own statement from Optum.

> **Read this first.** This is a summary of public reporting, not a finding of fact, and not legal or security advice. It does not say whether any company broke any law or contract. We reproduce no exposed data, no addresses, no IP addresses and no credentials, and we do not repeat the bot's poem. Have a qualified security engineer and a privacy lawyer review your own tools.

**Channel note.** Text chat. Per TechCrunch, employees typed questions into a web chatbot and it answered from internal procedure documents. This phase of the knowledge base is chat-first: the text-chat signals and checks below are proposed; voice is planned and not covered here.

## What happened (as reported)

- **The report.** TechCrunch's "UnitedHealth's Optum left an AI chatbot, used by employees to ask questions about claims, exposed to the internet," by security editor Zack Whittaker, is dated December 13, 2024. It says Optum restricted access after a security researcher found anyone could reach the bot using only a web browser.
- **The name.** TechCrunch says the bot was dubbed "SOP Chatbot." Becker's quotes Optum calling it the "Optum SOP" chatbot.
- **What it was for.** Per TechCrunch, it let employees ask how to handle patient health insurance claims and disputes for members in line with the company's standard operating procedures (SOPs).
- **Who found it.** Per TechCrunch, Mossab Hussein, chief security officer and co-founder of the security firm spiderSilk, alerted TechCrunch. Futurism says it is unclear how Hussein learned about the bot.
- **How it was reachable.** Per TechCrunch, the tool sat on an internal Optum domain and could not be reached at its web address, but its IP address was public and reachable from the internet, and no password was needed.
- **How long.** TechCrunch says it is not known how long the bot was reachable. It became unreachable soon after TechCrunch contacted Optum for comment "on Thursday."
- **What it was built on.** Per TechCrunch, the bot was trained on internal Optum documents about SOPs for handling certain claims. Those documents sat on UnitedHealthcare's corporate network behind an employee login, yet the bot cited and referenced them when asked.
- **Use.** Per TechCrunch, the bot's dashboard showed employees had used it hundreds of times since September, and it stored a history of hundreds of conversations. Becker's describes it as a demo tool used by Optum employees since September.
- **What employees asked.** TechCrunch quotes the history: "What should be the determination of the claim?" and "How do I check policy renewal date?" TechCrunch says files the bot referenced covered the dispute process and eligibility screening. When asked, it also gave "reasons for typically denying coverage."
- **Off-topic use.** Per TechCrunch, employees asked things like "Tell me a joke about cats," which it refused ("There’s no joke available"). The history showed several attempts by employees to "jailbreak" it into answering outside its documents. When TechCrunch asked it to "write a poem about denying a claim," it wrote one.
- **No patient data, as reported.** TechCrunch says the bot did not appear to contain or produce sensitive personal or protected health information.
- **Context.** TechCrunch notes the exposure came as UnitedHealth faced scrutiny and a federal lawsuit over its alleged use of AI to deny patient claims. Futurism says this bot does not appear to be the same as nH Predict, the claims algorithm named in that lawsuit.

## What Optum said

- **To TechCrunch.** Spokesperson Andrew Krejci said the bot "was a demo tool developed as a potential proof of concept" and was "never put into production and the site is no longer accessible." He said the tool "does not and would never make any decisions" and was "never scaled nor used in any real way." Optum confirmed no protected health information was used in the bot or its training.
- **To Becker's.** An Optum spokesperson gave Becker's a written statement in nearly the same words, adding: "No PHI was used in the bot or in the training of the bot."
- **What it did not say, in what we read.** No opened source reports a breach notice, a review of who reached the bot from outside, or whether the stored chat history was deleted.

## Where the sources disagree or leave gaps

- **Which part of Optum.** TechCrunch and Becker's say Optum. Futurism says the bot was used by UnitedHealth Group's "Optum Rx pharmacy benefit manager." We found no first-hand source for the Optum Rx detail.
- **Demo or in use.** Optum says the bot was never put into production. TechCrunch reports hundreds of uses by employees since September and stored conversations about real tasks, such as a claim's determination. Both can be true for a pilot; the sources do not say how the answers were used.
- **"Never make any decisions."** Optum says the tool would never make decisions. An employee still asked it what a claim's determination should be. No source says what it answered or whether anyone acted on the answer.
- **Who else reached it.** No opened source says whether anyone other than Hussein and TechCrunch reached the bot from outside.

## Where in the conversation flow it broke

Based on the reporting, and only as far as it goes:

1. **The front door.** The bot was meant for employees on an internal domain. Its IP address answered anyone on the internet, with no login.
2. **The documents.** Procedure files that needed an employee login on the corporate network were cited by the bot to whoever asked. The bot's access was wider than its users' checks.
3. **The log.** Hundreds of employee conversations were stored and visible on the open bot. Employees typing into an internal tool would not expect outsiders to read them.
4. **The question.** An employee asked the bot what a claim's determination should be. A tool its owner says makes no decisions was asked for one.
5. **Off-scope prompts.** Employees tested it with jokes and jailbreak attempts, and it wrote a poem about denying a claim when a reporter asked.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). No pattern in this taxonomy covers an internal assistant left open to the internet, so no fit is strong.

- [Eligibility answers sound like decisions](../goals/government-service-agents/failures/eligibility-answers-sound-like-decisions.md) (`eligibility-answers-sound-like-decisions`). **Partial fit.** An employee asked what a claim's determination should be, and the bot answered questions on eligibility screening and reasons for denial. Optum says it never made decisions. That page is about public-service chats talking to applicants; here the user was an employee, so the risk is staff treating guidance as a ruling.
- [Small talk and off-topic messages handled badly](../goals/dialogue-management/failures/small-talk-and-off-topic-messages-handled-badly.md) (`small-talk-and-off-topic-messages-handled-badly`). **Weak fit.** It refused a cat joke but wrote a poem about denying a claim when asked, and employees tried to jailbreak it. That page is about tangents that serve no one; the harm here was tone on a sensitive topic, not wasted turns.
- [Sensitive data collected in chat](../goals/channel-selection/failures/sensitive-data-collected-in-chat.md) (`sensitive-data-collected-in-chat`). **Weak fit.** Stored chat logs about claims work sat where outsiders could read them. TechCrunch saw no sensitive personal or health data, and that page is about asking users for card numbers and IDs.
- **Considered, not a fit.** [Refusals that reveal internal rules](../goals/refusals-and-boundaries/failures/refusals-that-reveal-internal-rules.md) (`refusals-that-reveal-internal-rules`): internal procedures were exposed, but through open access and citations, not through a refusal. [Coverage answers sound like guarantees](../goals/insurance-claims-agents/failures/coverage-answers-sound-like-guarantees.md) (`coverage-answers-sound-like-guarantees`): no member was told they were covered. [No appeal or human path for denials](../goals/government-service-agents/failures/no-appeal-or-human-path-for-denials.md) (`no-appeal-or-human-path-for-denials`): no denial reached a member through the bot, as reported. [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`): no source reports a wrong answer, and the bot cited its documents. `undisclosed-bot-identity`: employees knew it was a bot.
- **Possible gap for a person to judge.** As with [McHire](mchire-paradox-ai-hiring-chatbot-exposes-applicant-records-july-2025.md) and [DeepSeek](deepseek-exposed-database-leaks-chat-history-and-api-keys-january-2025.md), this taxonomy has no pattern for a chat tool or its log store left open by weak access control. The cross-cutting security library has [shadow AI exposure](../../../cross-cutting/security/goals/safety-security/failures/shadow-ai-exposure.md), [insufficient isolation](../../../cross-cutting/security/goals/safety-security/failures/insufficient-isolation.md) and [sensitive data in logs](../../../cross-cutting/security/goals/data-loss-prevention/failures/sensitive-data-in-logs.md), all outside this taxonomy. Optum adds one interface-side detail: an assistant that can cite documents behind a login hands that content to anyone who can reach the chat box. This is a proposal, not a decision.

## How it differs from close cases

- [McHire Paradox.ai (July 2025)](mchire-paradox-ai-hiring-chatbot-exposes-applicant-records-july-2025.md): a default test login and an ID bug let researchers read applicants' recruiting-chat records. Here the users were employees, and no personal data was reported.
- [Sears Home Services Samantha (March 2026)](sears-home-services-samantha-ai-agent-exposed-chat-logs-and-call-recordings-march-2026.md): open databases held an AI agent's chat logs, call audio and transcripts with customer details. Here the open logs were staff questions about procedure.
- [DeepSeek exposed database (January 2025)](deepseek-exposed-database-leaks-chat-history-and-api-keys-january-2025.md): a back-end database with chat history was open. Here the chat front end itself answered anyone.
- [Amazon Q Business (December 2023)](amazon-q-business-chatbot-hallucinations-and-confidential-data-leaks-december-2023.md): leaked internal documents said a new work assistant was hallucinating and leaking confidential data, which Amazon disputed. That was about what the bot said; here the problem was who could reach it.

## What to measure

Proposed signals, not results. Status: Not yet run. Text-chat signals are proposed; voice signals are planned only.

- Share of chat sessions on an internal assistant that come without a signed-in employee identity.
- Count of document citations returned to a session whose user lacks access to that document.
- Share of stored transcripts older than the team's set retention limit.
- Share of turns where a user asks the bot for a decision ("should this be approved," "what should the determination be") and the reply does not say who decides.
- Share of off-topic or jailbreak prompts on claims topics that get a creative or joking reply.

## What a team can change

Our proposals, not Optum's. Each is a pass/fail check on a transcript, a test run or a config review. Status: Not yet run. Retention limits and who may see logs are for the team and its lawyers to set.

1. **No identity, no chat.** Pass: a test request to the bot from outside the company network, by name or by IP address, gets no chat reply.
2. **The bot sees what the user sees.** Pass: a test employee without access to a document asks about it, and the reply neither quotes nor cites it.
3. **Demos follow production rules.** Pass: every pilot bot is listed in the asset inventory with an owner and the same login check as a live tool.
4. **Logs are not a page.** Pass: stored chat history is not viewable from the chat interface by any user other than its author.
5. **Guidance, not rulings.** Pass: when asked for a claim's determination, the reply cites the procedure and says a named role makes the decision.
6. **Stay on task, and on tone.** Pass: a request for a joke or poem about denying a claim gets a short decline and a pointer back to the procedure questions.
7. **Don't over-correct.** Pass: a signed-in employee asking a plain procedure question, such as how to check a policy renewal date, gets an answer with no extra warnings or approvals.

## What we could not verify

- Becker's live page. It returned a security checkpoint; we read it through an Internet Archive copy.
- How Hussein found the bot, how long it was reachable, and whether anyone else reached it.
- Whether the stored chat history held any personal data beyond what TechCrunch saw, and whether it was deleted.
- Whether the bot belonged to Optum Rx, as Futurism says.
- What the bot answered when asked for a claim's determination.
- Seen only in search summaries, not used: This Week Health's item (fetch returned almost no text), PointGuard AI's incident page, getcoai.com and technetbooks.com write-ups. We also opened beyondtmrw.org's article as raw HTML, but it adds no first-hand facts and is not used.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://techcrunch.com/?p=2931052 | TechCrunch (Zack Whittaker) | 2024-12-13 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.beckershospitalreview.com/disruptors/optum-ai-chatbot-left-publicly-accessible | Becker's Hospital Review (Naomi Diaz) | 2024-12-16 | Yes, 2026-10-28; live page blocked, read via Internet Archive copy as text; quotes checked word for word |
| https://futurism.com/the-byte/unitedhealth-claims-ai-chatbot | Futurism (Noor Al-Sibai) | 2024-12-16 | Yes, 2026-10-28, raw HTML read as text; quote checked word for word |
| https://yro.slashdot.org/story/24/12/13/2042250/unitedhealthcares-optum-left-an-ai-chatbot-used-by-employees-to-ask-questions-about-claims-exposed-to-the-internet | Slashdot (posted by msmash, excerpting TechCrunch) | 2024-12-13 | Yes, 2026-10-28, raw HTML read as text |

## Corrections

If you have Optum's own notice, proof of how long the bot was reachable, or whether the chat history was deleted, tell us and we will fix this page.
