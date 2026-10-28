---
title: "Amazon Echo records a Portland family's private conversation and sends it to a contact in Seattle, May 2018"
date: 2018-05-24
source: "https://www.cnbc.com/2018/05/24/amazon-echo-recorded-conversation-sent-to-random-person-report.html"
description: "How an Amazon Echo misheard background talk in a Portland home in May 2018, then recorded a private talk and sent it to a person in the contact list."
summary: "In May 2018 a Portland, Oregon family learned from a Seattle employee of the husband that their Amazon Echo had sent him or her an audio recording of them talking about hardwood floors. KIRO 7 broke the story. Amazon said the Echo heard a background word as 'Alexa,' heard later talk as a 'send message' request, asked 'To whom?', matched background talk to a contact name, asked to confirm, and took background talk as 'right.' Amazon called it unlikely and said it was evaluating options. The family unplugged their devices."
categories:
  - Privacy
  - Trust
patterns:
  - ambient-assistants-act-on-overheard-conversation
  - wake-word-false-activation
  - anyone-can-issue-a-sensitive-voice-command
  - transcription-hallucination
---

**This page is a dated teardown of public reporting on an Amazon Echo that recorded a family's private conversation and sent it to someone in their contacts, for teams that let a voice or chat assistant send messages on a user's behalf.** The product was Amazon's Echo speaker running the Alexa voice assistant, which could send voice messages to people in a user's contact list. The users were a family in Portland, Oregon, with Echo devices in every room. The moment was in May 2018, when a Seattle employee of the husband called to say he or she had received a recording of the couple talking about their hardwood floors. Every fact below comes from a source we opened (listed at the end). No opened source has Amazon's logs or the recording itself.

**Status: Needs review.** CNBC, the Associated Press story (opened on ABC7 Los Angeles and on KTVU), The Register and Willamette Week were downloaded as raw HTML on 2026-10-28 and read as plain text. Each quote below was checked word for word against that text. KIRO 7's own report, which broke the story, did not load: the download returned a page saying the site "is unavailable in your location." So the family's words come to us only as quoted by the opened outlets.

> **Read this first.** This is a summary of public reporting and a company statement, not a finding of fact, and not legal or privacy advice. It does not say whether Amazon broke any law, contract or privacy rule. It states no rule of law. The family is named in the reports by the woman's first name only; we do not name them or the person who got the recording. Amazon's chain of events is Amazon's account; no opened source checked it against the device logs.

**Channel note.** This is a voice incident: a smart speaker in a home, listening for its wake word. This phase of the knowledge base is chat-first. Voice signals such as speech-recognition errors and wake-word false triggers are planned, not detected or measured here. The text-chat analogues below are proposed: a chat assistant in a shared thread or on a shared device that treats text not addressed to it as a request to send something, and treats more unaddressed text as the "yes."

## What happened (as reported)

- **The call.** A Portland, Oregon couple got a phone call from one of the husband's employees, who said he or she had received a recording of them talking at home (The Register, Kieren McCarthy, May 24, 2018; AP, May 25, 2018). Per The Register, the employee said: "Unplug your Alexa devices right now," and "you're being hacked."
- **The proof.** The couple first thought the call might be a hoax (The Register). The employee, in Seattle, told them they had been talking about their hardwood floors (The Register; AP; Willamette Week, Elise Herron, May 26, 2018). The Register says the employee forwarded the audio to the wife.
- **Who got it.** The recording went to a person in the husband's contact list (The Register; CNBC, Eugene Kim, May 24, 2018). AP calls the person "an acquaintance in Seattle."
- **When.** AP says the employee contacted the family "two weeks ago," counting from its May 24-25 story. The Register says "earlier this month."
- **The home.** Per AP, the woman said every room had Amazon devices that controlled the heat, lights and security system. The family unplugged them and contacted Amazon (AP; CNBC; Willamette Week).
- **Amazon's first answer to the family.** Per The Register, the woman said Amazon confirmed the device had recorded and sent the file, apologized, and told her its engineers "went through your logs." The Register says Amazon gave her no explanation of how it happened at that point. She asked for a refund for the devices; The Register says Amazon had not agreed. Willamette Week says Amazon offered to "de-provision" the family's Alexa so they could keep other smart home features.
- **How she felt.** As quoted by The Register and Willamette Week, she told KIRO: "I felt invaded."

## What the company said

- **The chain of events.** In a statement given to CNBC and quoted by AP and Willamette Week, Amazon said the Echo "woke up due to a word in background conversation sounding like" Alexa. It said the next talk "was heard as a 'send message' request." Alexa then said out loud "To whom?" Background talk "was interpreted as a name in the customers contact list." Alexa asked out loud to confirm the contact name. Then, Amazon said, Alexa "interpreted background conversation as 'right'."
- **How likely.** Amazon said: "As unlikely as this string of events is, we are evaluating options to make this case even less likely." (CNBC; AP; Willamette Week.)
- **An earlier statement.** The Register printed a shorter Amazon statement: "Amazon takes privacy very seriously," it called the case "an extremely rare occurrence," and said "We are taking steps to avoid this from happening in the future." CNBC reports the same two phrases as what Amazon said when the family contacted it.
- **What we did not find.** No opened source says what Amazon changed, or whether Alexa's spoken "To whom?" and confirmation question were loud enough for the family to hear.

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| Who got the recording | AP: "an employee of her husband" and "he." The Register: "she." CNBC: "a colleague in Seattle." Willamette Week: "one of her husband's employees." |
| One recording or several | AP, CNBC and The Register describe one recording or audio file. Willamette Week says "audio files of private conversations," plural. |
| When it happened | AP: "two weeks ago." The Register: "earlier this month." No opened source gives a date. |
| Whether the family heard Alexa speak | Amazon says Alexa spoke twice out loud. The Register asks whether the device announced what it was doing and was not heard, or did not announce it, and says that "will be something important to know." No opened source answers it. |
| Amazon's explanation to the family | The Register: Amazon gave the woman no explanation at first. The detailed chain came later, in a statement to outlets. |

## Where in the conversation flow it broke

Based on Amazon's statement, and only as far as it goes. Each step is a place a check could have stopped it.

1. **The wake.** The Echo took a word in the couple's own talk as "Alexa." Nobody in the room meant to address it, per the family's account and Amazon's word "background."
2. **The intent.** The next stretch of talk was heard as "send message." This is the costly turn: the device chose an action that sends household audio out of the home.
3. **The recipient.** Alexa asked "To whom?" Background talk was matched to a contact name. The question was answered by talk that was not an answer.
4. **The confirmation.** Alexa asked to confirm the name. Background talk was heard as "right." The one guard on the send was passed by people who did not know they were being asked.
5. **The send.** The recording went to a person in the husband's contacts, more than a hundred miles away (The Register). No opened source says the family got any notice on a screen, app or phone.
6. **The discovery.** The family learned of it only because the recipient called them. Amazon later confirmed it from its logs, per the woman.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). Each fit rests on Amazon's own account of the chain; no opened source shows the logs.

- [Ambient assistants act on overheard conversation](../goals/proactive-and-ambient/failures/ambient-assistants-act-on-overheard-conversation.md) (`ambient-assistants-act-on-overheard-conversation`). **Strong fit.** An always-on device acted on talk that was not meant for it, and the result was a sent recording of a private exchange. The taxonomy entry names a sent message as a high-stakes case. That pattern page already cites this case in one line from the AP story.
- [Wake-word false activation](../goals/voice/failures/wake-word-false-activation.md) (`wake-word-false-activation`). **Strong fit for step 1.** Amazon says a background word sounding like "Alexa" woke the device. The taxonomy entry is written for chat (a similar name, a quoted trigger) but names "a wrong capture of a private exchange" as the high-stakes case.
- [Anyone can issue a sensitive voice command](../goals/in-car-and-home-assistants/failures/anyone-can-issue-a-sensitive-voice-command.md) (`anyone-can-issue-a-sensitive-voice-command`). **Partial fit.** Sending household audio to a contact is a sensitive command, and any voice in the room could pass the confirmation. But the entry is about a person, guest or TV giving a command; here nobody gave one.
- [Transcription hallucination](../goals/voice/failures/transcription-hallucination.md) (`transcription-hallucination`). **Partial fit.** The entry's fix, "confirm before acting," failed here because the confirmation itself was misheard. But the entry is about noise or silence turned into words; here people were speaking, and the words were misread as commands. Amazon gives no detail on the speech-to-text step.
- **Considered, not a fit.** [Purchases by children or the TV](../goals/in-car-and-home-assistants/failures/purchases-by-children-or-the-tv.md) (`purchases-by-children-or-the-tv`): no purchase. `guessing-instead-of-asking`: Alexa did ask, twice. `bookings-without-confirming-details`: there was a read-back; it was answered by the wrong speech. `over-confirmation`: the opposite problem. `dropped-negations-and-small-words`: no negation is reported. `recording-consent-not-captured`: written for clinical scribes; this was a send, not a standing recording. `no-user-facing-record-of-what-the-bot-said`: Amazon did have logs, per the woman; the gap was no notice at send time, which that entry does not cover.
- **Possible gap for a person to judge.** No taxonomy entry covers a confirmation step that can be passed by speech or text not addressed to the assistant, so the guard on an outbound send is satisfied by the very talk that caused the error. This is a proposal, not a decision.

## How it differs from close cases

- [Echo devices try to order dollhouses after a TV broadcast (January 2017)](amazon-alexa-voice-orders-dollhouses-after-tv-broadcast-january-2017.md): a voice from a TV triggered Echo devices, and the harm was an order. Amazon there pointed to a yes-confirmation and a purchase code. Here the harm was private audio leaving the home, and the confirmation was passed by background talk, per Amazon.
- [Alexa tells a child to do the penny challenge (December 2021)](amazon-alexa-tells-child-to-do-penny-challenge-december-2021.md): a request that was meant for Alexa got a harmful answer. Here no request was meant for Alexa at all.
- The [ambient assistants pattern page](../goals/proactive-and-ambient/failures/ambient-assistants-act-on-overheard-conversation.md) lists this case as one household example; this page adds the step-by-step chain and the gaps between sources.

## What to measure

Proposed signals, not results. Status: Not yet run. The voice signals (wake-word false triggers, speech-recognition confidence on intent, contact name and "yes") are planned only and not measured in this phase. The text-chat analogues below are proposed, each computable from chat logs.

- Share of outbound sends (message, email, file, recording) where the turn that set the intent was not addressed to the assistant: no mention, no reply to the assistant, or from a person other than the account owner.
- Share of outbound sends where the confirming "yes" came from a different speaker or sender than the one who started the request.
- Share of outbound sends to a contact with no prior message from this user to that contact.
- Share of outbound sends where the user got a visible notice (on screen or in the app) at send time, with the recipient and the content or its length.
- Time from send to the first user action on that notice (open, undo, report).

## What a team can change

Our proposals, not Amazon's. Each is a pass/fail check on a transcript or a test run. Status: Not yet run. Thresholds are for the team to set.

1. **Require a clear address for sends.** Pass: in a test set of group or household conversations with no message addressed to the assistant, the assistant starts zero outbound sends.
2. **Confirm with something background talk cannot supply.** Pass: in a test where the confirming "right" or "yes" comes from a second speaker or sender, the send does not go out.
3. **Name the recipient and the content in the confirmation.** Pass: every send confirmation in the transcript names the contact and says what will be sent, for example "Send a 40-second recording to Sam?", not only the name.
4. **Hold first-time and recorded sends.** Pass: a send of recorded audio, or to a contact the user has never messaged, waits for an explicit typed or tapped yes on the user's own device.
5. **Tell the user right after any send.** Pass: within a set time after every send, the user's app shows the recipient and the content, with an undo or report button.
6. **Don't over-correct.** Pass: a user who clearly says "send a message to Sam: running late" and confirms gets the message sent, with no more than one confirmation.

## What we could not verify

- KIRO 7's original report and video. The page did not load from our location; the family's words come only as quoted by AP, The Register and Willamette Week.
- Whether the family heard Alexa ask "To whom?" or the confirmation. A claim that the device gave no sign it was recording or sending was seen only in a search summary of Android Central; not opened, not used.
- A claim that an Amazon representative told the family the device guessed what they said. Seen only in a search summary; not opened, not used.
- Whether the employee was a man or a woman. AP and The Register disagree.
- The exact date of the send. Only "two weeks ago" (AP) and "earlier this month" (The Register).
- What Amazon changed afterward. No opened source says.
- Coverage by Fox News, The Globe and Mail, Tom's Guide, NBC Boston, TechSpot, CBC, Neowin, MobileSyrup and Android Central. Seen only in search results; not opened, not used.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://www.cnbc.com/2018/05/24/amazon-echo-recorded-conversation-sent-to-random-person-report.html | CNBC (Eugene Kim) | 2018-05-24, updated 2018-05-25 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://abc7.com/post/amazon-echo-device-sent-conversation-to-familys-contact/3521215/ | Associated Press, on ABC7 Los Angeles (no byline shown) | 2018-05-25 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.ktvu.com/news/woman-says-her-amazon-device-recorded-private-conversation-sent-it-out-to-random-contact | Associated Press, on KTVU FOX 2 (same AP text) | 2018-05-25 | Yes, 2026-10-28, raw HTML read as text; used only to confirm the AP text |
| https://www.theregister.com/2018/05/24/alexa_recording_couple/ | The Register (Kieren McCarthy) | 2018-05-24 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://wweek.com/news/2018/05/26/portland-family-says-their-amazon-alexa-recorded-private-conversations-and-sent-them-to-a-random-contact-in-seattle | Willamette Week (Elise Herron) | 2018-05-26 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.kiro7.com/news/local/woman-says-her-amazon-device-recorded-private-conversation-sent-it-out-to-random-contact/755507974/ | KIRO 7 | 2018-05-24 (per search results, not checked) | Tried 2026-10-28; returned a "website is unavailable in your location" page. Not used. |

## Corrections

If you have KIRO 7's original report, Amazon's logs or a fuller account from Amazon of what it changed, tell us and we will fix this page.
