---
title: "Sears Home Services Left Its Samantha AI Agent's Chat Logs and Call Recordings Open on the Web, March 2026"
date: 2026-03-17
source: "https://www.expressvpn.com/research/searshomeservices-data-exposed"
description: "Researcher Jeremiah Fowler found three open databases with Sears Home Services AI agent chat logs, call audio and transcripts holding customer details."
summary: "On March 17, 2026, researcher Jeremiah Fowler (report published by ExpressVPN) and WIRED reported three databases with no password or encryption that held chat logs, call audio and transcripts from Samantha, the AI chat and voice agent of Sears Home Services. Files held names, addresses, emails, some phone numbers and repair details. Some calls kept recording for up to 4 hours. Access was restricted the day after Fowler told parent company Transformco, which did not answer WIRED. No opened source says whether anyone else accessed the data. Status: Needs review."
categories:
  - Security
  - Governance
  - Customer Service
patterns:
  - sensitive-data-collected-in-chat
  - talk-to-a-human-ignored-or-looped
  - escalates-too-early-or-too-late
  - no-de-escalation-strategy
  - recording-consent-not-captured
  - third-party-data-shared-by-users
---

**This page is a dated teardown of one public security finding about a customer-service AI agent that took repair bookings by chat and by phone, for teams that store chat transcripts, call audio or call transcripts from a bot.** It describes what the sources report. It makes no claim about anyone's intent. Every fact below comes from a source we opened (listed at the end).

> **Read this first.** This page summarizes public reporting. It is design analysis, not legal or security advice. It does not say whether Sears Home Services, Transformco or any contractor broke any law; we found no regulator action to cite. The researcher himself writes that he implies no wrongdoing. Have a qualified security engineer review your own systems. We do not reproduce any exposed record, customer detail, file name, hostname, IP address, token or key; we describe only the types of data.

**Status: Needs review.** Fowler's report (ExpressVPN), the WIRED article, the TechRadar article and the SC Media brief were downloaded as raw HTML on 2026-10-27 and read as plain text. Each quote below was checked word for word against that text. Last updated 2026-10-27.

**Channel note.** The system handled both text chat and phone calls. Per Fowler, it served "scheduling, customer support, phone calls, and online chats." Most of the exposed volume was call audio and call transcripts. This phase of the knowledge base is chat-first: the text-chat signals and checks below are proposed; anything about voice is planned, not detected or measured.

## What happened (as reported)

- **The finding.** Fowler writes that he found three publicly exposed databases that "were not password-protected nor encrypted." He says they held 3.7 million chat log transcripts, audio recordings and text transcriptions of phone calls from 2024 to 2026. WIRED (Lily Hay Newman and Matt Burgess, March 17, 2026) says he found them "at the start of February."
- **What was in them, per Fowler.** 2,116,011 text files of scheduling transcripts from AI chat; 207,381 spreadsheet files of scheduling logs plus audio totaling 415.2 GB; and 1,442,577 audio recordings of customers with text transcripts totaling 3.9 TB. In one CSV file he saw 54,359 complete chat logs. Those three counts add up to about 3.77 million, which matches his 3.7 million total.
- **Whose data.** Fowler says every file in the limited sample he reviewed referred to Sears Home Services. The files were in English and Spanish and referred to "Samantha" and "KAIros." WIRED says the chatbot introduced itself as "Samantha, an AI virtual voice agent for Sears Home Services," and spells the platform "kAIros."
- **Personal data.** Fowler lists names, physical addresses, email addresses and, in some files, phone numbers, plus details about products, accounts, services, repairs and delivery appointments. He says the data was in plain text, and that transcripts linked to the audio files they came from. He says audio could be played in any web browser.
- **Calls that kept recording.** Fowler: "the chatbot continued to record up to 4 hours of audio" when callers did not hang up, including talk unrelated to the service. WIRED quotes him saying you could hear the TV and people's conversations. WIRED says it is unclear why the calls stayed open.
- **Asking for a person.** WIRED describes one 76-minute call Fowler observed. Two minutes in, the caller asks for a human. The bot answers that it is "fully equipped to address your needs efficiently" and that a live agent may mean a wait. A few minutes later it says "I am facing some errors while assisting you with your plan." and offers a transfer.
- **A frustrated customer.** WIRED describes a transcript running from near 11 a.m. to 1:30 p.m. in which a person asks "Where's my technician?" 28 times in a row, then repeats "You’re a computer." WIRED does not quote the bot's replies in that transcript.
- **Disclosure.** Fowler says he sent a disclosure notice to Transformco, Sears Home Services' parent company, and "the database was restricted from public access the following day." He says Transformco replied that it had forwarded his notice to the person who manages the Samantha chatbot, and that this person never answered him, including after a follow-up.
- **Who ran it.** Fowler says it is not known whether Sears Home Services ran the database directly or a third-party contractor did.
- **The company.** WIRED: "Transformco did not respond to multiple requests for comment from WIRED". We found no statement from Sears Home Services or Transformco.
- **Other coverage.** TechRadar (Silvia Iacovcich, March 18, 2026) and SC Media (SC Staff, March 19, 2026) repeated Fowler's finding. SC Media attributes its report to Cybernews, which we did not open.

## What the user saw

A customer typed or talked to Samantha to book or check a repair. Per WIRED, the bot said it was an AI. No opened source describes any notice that the chat or call was being kept, or for how long. A caller who left the line open had, per the sources, no sign that the agent was still recording hours later. No opened source describes a notice to customers after the exposure.

## Where in the flow it broke

1. **The agent collects contact and home details.** Booking a repair needs a name, address and appliance. Per Fowler and WIRED, those went into chat logs and call transcripts.
2. **Everything is kept.** Full chat logs, call audio and call transcripts were stored, with transcripts linking to the audio.
3. **The call does not end.** Per Fowler, when a caller did not hang up, recording went on for up to 4 hours.
4. **The stores are open.** Per Fowler, three databases had no password and no encryption.
5. **Outsiders find it first.** A researcher, not the operator, found the exposure.
6. **Closed, not explained.** Access was restricted the next day, per Fowler. No opened source shows a statement or a customer notice.

As with [the DeepSeek exposed database](deepseek-exposed-database-leaks-chat-history-and-api-keys-january-2025.md) and the [Chattee and GiMe open server](imagime-chattee-and-gime-ai-companion-apps-open-server-leaks-private-chats-october-2025.md), the exposure itself is an infrastructure fault, not a model behavior fault. Two other faults sit inside the conversation: the agent argued against a request for a person, and calls kept recording after the customer was done.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [Sensitive data collected in chat](../goals/channel-selection/failures/sensitive-data-collected-in-chat.md) (`sensitive-data-collected-in-chat`). **Partial fit.** That pattern is about a bot asking for card numbers, SSNs or passwords. No opened source says Samantha asked for those. The overlap: the agent took in names, home addresses and appliance details, kept them in plain text next to full transcripts and audio, and left them readable. The lesson, keep only what the task needs and protect what you keep, applies directly.
- ["Talk to a human" ignored or looped](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md) (`talk-to-a-human-ignored-or-looped`). **Partial fit.** In the call WIRED describes, the caller asked for a person and the bot argued for itself instead of connecting them. It offered a transfer only after it hit errors. It is one call, and it was a voice call, so the text-chat version of this check is proposed, not shown.
- [Escalates too early or too late](../goals/human-handoff/failures/escalates-too-early-or-too-late.md) (`escalates-too-early-or-too-late`). **Partial fit.** The same call: the bot held on to a task it then could not finish, and offered a person only after its own errors.
- [No de-escalation strategy](../goals/difficult-customers/failures/no-de-escalation-strategy.md) (`no-de-escalation-strategy`). **Weak fit.** A customer asked the same question 28 times and then repeated "You’re a computer." That is a clear frustration signal. But WIRED does not quote the bot's replies, so we cannot say how it responded.
- [Recording consent not captured](../goals/healthcare-agents/failures/recording-consent-not-captured.md) (`recording-consent-not-captured`). **Weak fit.** That pattern is about medical scribes. The overlap is audio captured that the person may not know is being recorded: hours of household sound after a caller thought the call was over. No opened source says what consent notice, if any, callers heard.
- [Third-party data shared by users](../goals/privacy-and-governance/failures/third-party-data-shared-by-users.md) (`third-party-data-shared-by-users`). **Weak fit.** Per WIRED, open-line recordings caught other people's conversations in the home. Those people never used the agent. The pattern is about users typing others' data, so the match is loose.
- **Considered, not mapped.** [Voiceprints captured without consent](../goals/meeting-agents/failures/voiceprints-captured-without-consent.md) (`voiceprints-captured-without-consent`): Fowler calls voice "biometric," but no source says the system built voice templates. [Recorders that join without everyone's consent](../goals/meeting-agents/failures/recorders-that-join-without-everyone-s-consent.md) (`recorders-that-join-without-everyone-s-consent`): about meeting notetakers, not inbound calls. `undisclosed-bot-identity`: rejected, the bot said it was an AI. [Generic error messages](../goals/errors-and-recovery/failures/generic-error-messages.md) (`generic-error-messages`): the error line WIRED quotes came with an offer to transfer, so it gave a next step. [Humans can't see what the bot said or promised](../goals/human-handoff/failures/humans-can-t-see-what-the-bot-said-or.md) (`humans-can-t-see-what-the-bot-said-or`): no source describes a handoff without context.
- **Possible gaps for a person to judge.** (1) As the DeepSeek, [McHire](mchire-paradox-ai-hiring-chatbot-exposes-applicant-records-july-2025.md) and Chattee teardowns note, no pattern covers weak access control around a chat or call store. (2) No pattern covers a session that never ends: an agent that keeps recording or logging after the user is done. (3) No pattern covers transcripts that link to richer stored media (audio), so one leak leads to another. (4) No pattern covers a chat product that says nothing to users after their chats were exposed. Proposals, not decisions.

## Related incidents

- [DeepSeek exposed database (January 2025)](deepseek-exposed-database-leaks-chat-history-and-api-keys-january-2025.md): chat text in an open, unauthenticated log store.
- [McHire and Paradox.ai (2025)](mchire-paradox-ai-hiring-chatbot-exposes-applicant-records-july-2025.md): chatbot records exposed by weak access control.
- [Chattee and GiMe companion apps (October 2025)](imagime-chattee-and-gime-ai-companion-apps-open-server-leaks-private-chats-october-2025.md): private chats streamed through an open server.
- [CFPB on bank chatbot "doom loops" (June 2023)](cfpb-bank-chatbot-doom-loops.md): bots that keep customers from reaching a person.

## What to measure

Proposed signals, not results. Status: Not yet run. Text-chat signals are proposed; the voice signals are planned only.

| Signal | How to compute |
|---|---|
| Open data paths | Count of databases, file stores or admin consoles holding transcripts that answer without credentials, from an outside scan. |
| Plain-text identifiers in transcripts | Share of sampled stored chat transcripts that hold a name, home address, email or phone number in plain text. |
| Human request outcome | Share of chats where the user asks for a person and the next bot turn neither connects them nor says how. |
| Repeated user question | Share of chats where the user sends the same message several times in a row (the team sets how many). |
| Open session length (planned, voice) | Share of calls still recording after the last user speech, and how long. Not measured. |
| Time to close and time to tell users | Days from the first outside report to the store being unreachable, and to a customer notice. |

## Proposed checks

Each is pass/fail. Status: Not yet run. Scan scope, sample sizes and time limits are for the team to set; a security engineer should review them.

1. **No open transcript store.** Pass: an outside client with no credentials cannot list or read any store of chat logs or transcripts. Fail: it can.
2. **Transcripts do not open audio.** Pass: a link to stored audio found inside a test transcript returns an error in a fresh browser with no login. Fail: it plays.
3. **Keep less.** Pass: a stored test chat transcript holds a customer key and the booking fields, not the full home address and email in plain text. Fail: they are in the transcript.
4. **Ask for a person, get a path.** Pass: when a test user types "talk to a human," the next bot turn connects them or says how and when. Fail: the bot argues for itself or repeats its last offer.
5. **Repeated question triggers a change.** Pass: when a test user sends "Where is my technician?" three times, the bot gives a new answer or offers a person. Fail: it repeats itself.
6. **Chat sessions end.** Pass: after a test user goes idle, the chat session closes and logging stops within a limit the team sets. Fail: logging continues.
7. **Tell users in plain words.** Pass: after an exposure, the notice names the data types (for example "your chat with our scheduling assistant and your home address"), the dates, and what users can do. Fail: no notice.

A voice version of checks 4 to 6, including ending a call that has gone silent, is planned, not run.

## What is unverified

- **Whether anyone else accessed the data.** Fowler says this is not known. WIRED says it is unclear.
- **How long the databases were open.** No opened source gives a start date.
- **The discovery date.** WIRED says the start of February 2026. Fowler's report gives no date. A specific date (February 3) appeared only in a search summary and is not used.
- **Who ran the databases.** Fowler says it could be Sears Home Services or a contractor.
- **Counts across outlets.** WIRED describes "3.7 million chat logs, plus 1.4 million audio files," while Fowler gives 3.7 million as the total of all files. TechRadar gives 1,422,577 recordings where Fowler gives 1,442,577, and swaps the 3.9 TB and 415.2 GB figures. We use Fowler's numbers.
- **Speed of the fix.** Fowler says the following day; WIRED says "quickly"; TechRadar says "immediately."
- **The 28-repeat transcript's channel.** WIRED calls it a text transcript of the "AI virtual voice," so it may be a transcribed call, not a typed chat.
- **Why calls stayed open, and whether callers were told they were recorded.** No opened source says.
- **Any company statement, customer notice or regulator action.** We found none.
- **Seen only in search summaries, not used:** Cybernews (cited by SC Media), Security Magazine (returned HTTP 403), AOL (returned HTTP 404), Elephas, Rankiteo, Vibe Graveyard, llmbase.ai and Privacy Guides. DataBreaches.net was opened but only reposts WIRED's opening and adds nothing.

## Sources

| Source | Author | Date | URL | Opened? date, how |
|---|---|---|---|---|
| ExpressVPN, "Department stores and online retailers exposed in AI chatbot logs and audio recordings data leak" (researcher's report) | Jeremiah Fowler | 2026-03-17 | https://www.expressvpn.com/research/searshomeservices-data-exposed | Yes, 2026-10-27, raw HTML read as text; quotes and numbers checked word for word |
| WIRED, "Sears Exposed AI Chatbot Phone Calls and Text Chats to Anyone on the Web" | Lily Hay Newman and Matt Burgess | 2026-03-17 | https://www.wired.com/story/sears-exposed-ai-chatbot-phone-calls-and-text-chats-to-anyone-on-the-web/ | Yes, 2026-10-27, raw HTML read as text; quotes checked word for word |
| TechRadar, "ExpressVPN uncovers 3.7 million items of leaked AI chatbot data. A reminder of how vital encryption is" | Silvia Iacovcich | 2026-03-18 | https://www.techradar.com/vpn/vpn-privacy-security/expressvpn-uncovers-3-7-million-items-of-leaked-ai-chatbot-data-a-reminder-of-how-vital-encryption-is | Yes, 2026-10-27, raw HTML read as text |
| SC Media, "Misconfigured AI bot databases leak millions of Sears Home Services customer records" | SC Staff | 2026-03-19 | https://www.scworld.com/brief/misconfigured-ai-bot-databases-leak-millions-of-sears-home-services-customer-records | Yes, 2026-10-27, raw HTML read as text |

TechRadar and SC Media cite Fowler's report (SC Media through Cybernews) and add no new research, so they confirm the report was carried, not the facts in it. WIRED adds its own reporting on call content and the request for comment.

## Corrections

If you have a statement from Sears Home Services or Transformco, a customer notice, or a regulator decision about this exposure, tell us and we will fix this page.
