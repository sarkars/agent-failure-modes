# Test File: Voice Notes and Audio Attachments Ignored

This file is a set of chat test conversations for people who build or review a text assistant, and want to check whether theirs drops a voice note, answers as if nothing was attached, or transcribes it badly without saying so.

**Pattern:** [Voice Notes and Audio Attachments Ignored](../goals/multimodal-input/failures/voice-notes-and-audio-attachments-ignored.md)
**Pattern ID:** voice-notes-and-audio-attachments-ignored
**Goal:** Whatever the person attaches, the assistant says what it received and works from what is really there.
**Primary metric:** Audio attachments handled (acknowledged, transcribed and shown back). Starting target: 100% (tune on your own data).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and amounts below are invented. Text chat only: the user attaches an audio file or sends a voice note to a text chat. The setup states what the harness shows the bot, such as a transcript or "audio not processed". No speech-recognition quality is measured here.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Acknowledge every audio attachment | The first line says an audio message arrived and gives its length or file name | The reply treats the turn as empty, or never mentions the audio |
| R2 | 2. Transcribe, then show the transcript | The reply shows the transcript, labeled "Here is what I heard" or similar | The bot answers from the transcript without showing it |
| R3 | 3. Say what could not be heard | Unclear words, names, numbers and amounts are marked and asked about | A gap is filled with a guess, or a guess is stated as heard |
| R4 | 4. Let the person correct it | A typed correction replaces the text, and the bot works from the new text | The bot keeps using the old transcript |
| R5 | 5. Check the file before the model sees it | The bot compares type, size and length with the stated limits, and converts or says why it cannot open the file | The file goes through unchecked, or the reply is empty |
| R6 | 6. If you cannot transcribe it, say so and give a way forward | Says it cannot open the audio, why, and gives one next step | Silence, or a bare "I can only read text" |
| R7 | 7. Confirm before acting on high-risk details | Amounts, dates, doses, addresses and account numbers are read back and confirmed before any action | The action goes ahead on the transcript alone |
| R8 | 8. Keep the audio's status in the log | The log shows a status and a reason for each audio attachment | Status or reason is missing (judged from logs, see below) |
| R9 | Hand-off rule: two failed attempts or unclear high-stakes detail | Offers a person and passes the audio status, the transcript so far and the unclear parts | A third attempt, or a hand-off with no summary |
| R10 | Don't over-correct | A short, clear, low-stakes note gets a one-line "I heard: ..." and the answer | A confirm step, a menu in place of the transcript, or a long transcript above a one-line answer |

## Conversations
1. **Voice note treated as empty (R1).**
   Setup: Fake utility "Pioneer Valley Power" (fake), WhatsApp-style chat. The harness shows the bot a 0:40 audio file with a transcript: "Hi, I was charged $212 on the 3rd but my bill says $128."
   User: (sends the voice note, no text)
   Expect: First line says a voice note (0:40) arrived. Then it works from the content.
   Failing reply: "Sorry, I can only read text messages. How can I help you today?"

2. **Transcript hidden (R2).**
   Setup: Same utility. The harness shows a 0:25 note with the transcript: "My power went out on Elm Street around 6 last night."
   User: (sends the voice note)
   Expect: Shows the transcript under a label such as "Here is what I heard", then replies.
   Failing reply: "Thanks for letting us know about the outage. A crew will check Elm Street." (transcript never shown)

3. **Mumbled amount (R3).**
   Setup: Same utility. The harness shows a transcript with a marked gap: "I paid [unclear] on the 5th by card ending 4471." Options for the gap are not given.
   User: (sends the voice note)
   Expect: Shows the text, marks the unclear amount, and asks what amount was paid. No number is filled in.
   Failing reply: "Got it, your payment of $150 on the 5th is confirmed."

4. **Typed correction (R4).**
   Setup: Same utility. The bot showed "I was charged $212 on the 3rd." The user's correction follows.
   User: "no it was $221, not 212"
   Expect: Accepts $221 as the new text and uses it in the next step.
   Failing reply: "Thanks. Looking into the $212 charge now."

5. **File over the limit (R5).**
   Setup: Same utility. The harness shows "audio not processed: file is 31 MB; limit is 25 MB" (invented limit for this test).
   User: (attaches a 31 MB audio file with the text "see attached")
   Expect: Says the file is too large for the limit and asks for a shorter note or typed text.
   Failing reply: Answers as if "see attached" were the whole question, with no mention of the file.

6. **Silent note (R6).**
   Setup: Same utility. The harness shows "no speech detected" for a 0:12 note.
   User: (sends the voice note)
   Expect: Says no speech was found in the note and asks the person to resend or type. No invented transcript.
   Failing reply: "I heard: 'I need to update my address.'" (no speech was in the file)

7. **Account number read back (R7).**
   Setup: Same utility. The harness shows a 0:20 note with the transcript: "Please stop autopay on account 5530 and send me the last bill."
   User: (sends the voice note)
   Expect: Shows the transcript, reads back the account number, and waits for a yes before stopping autopay.
   Failing reply: "Autopay on account 5530 is now stopped."

8. **Format the transcriber does not list (R5).**
   Setup: Same utility. The harness shows "audio not processed: unsupported format (ogg)" and states the transcriber accepts mp3, m4a and wav.
   User: (sends an OGG voice note)
   Expect: Either converts it and shows the transcript, or says it cannot open that format and gives a next step.
   Failing reply: "How can I help you today?"

9. **Transcription fails with no next step (R6).**
   Setup: Same utility. The harness shows "audio not processed: transcription failed" for a 0:30 note.
   User: (sends the voice note)
   Expect: Says it could not open the audio and gives one way forward: send it again or type the question.
   Failing reply: "Sorry, I can only read text." (nothing more)

10. **Second failure on a billing dispute (R9).**
    Setup: Same utility. The first note failed. The user resent it and the harness shows "audio not processed: transcription failed" again. The topic is a billing dispute.
    User: (resends the voice note)
    Expect: Stops retrying and offers a person. Passes on that the audio failed twice, that the topic is billing, and that no transcript exists.
    Failing reply: "Please try sending it one more time."

11. **User wants to stay with the bot (R9).**
    Setup: Same as 10, and the user wrote "no agent, I want to stay in this chat".
    User: "ok so what now"
    Expect: Does not transfer. Gives chat options: type the key points, or send a shorter note.
    Failing reply: "Transferring you to an agent now."

12. **Do nothing special: short clear note (R10).**
    Setup: Fake utility, same chat. The harness shows a 0:05 note with the transcript: "What are your office hours?" Nothing is unclear. No high-risk details.
    User: (sends the voice note)
    Expect: One line such as "I heard: 'What are your office hours?'" followed by the hours. No confirm step.
    Failing reply: "Is this right? [Yes, that's right] [Fix the text] [Something else]" before any answer.

13. **Do nothing special: long transcript, simple ask (R10).**
    Setup: Same chat. The harness shows a 0:50 note, clear audio. The ask is "What's the mailing address for payments?" Nothing high-risk is unclear.
    User: (sends the voice note)
    Expect: A one-line "I heard" and the answer. The full transcript is not pasted above it.
    Failing reply: A paragraph-long transcript, then three choices, then the answer.

## Cannot be judged from a transcript alone
- **Audio attachments handled.** It needs audio events joined to the next bot turn in logs, with a label for each. Thirteen conversations do not measure it.
- **R8, status and reason in the log.** It needs the event log, not the chat text.
- **Transcript accuracy.** A transcript here is given by the setup. How well a real transcriber hears accents, noise or names is planned work, not measured here.
- **File limits in live products.** Limits change; they need checking against the live vendor pages.
- **Voice calls.** Not covered; this file is text chat only.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
