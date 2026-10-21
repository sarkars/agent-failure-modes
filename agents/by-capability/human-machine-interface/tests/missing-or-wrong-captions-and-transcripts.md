# Test File: Missing or Wrong Captions and Transcripts

**Pattern:** [Chatbot Voice Messages Without Captions or Transcripts: Missing or Wrong Captions and Transcripts](../goals/accessibility/failures/missing-or-wrong-captions-and-transcripts.md)
**Pattern ID:** missing-or-wrong-captions-and-transcripts
**Goal:** People who use screen readers, keyboards, captions, relay services, or plain-language support can use every part of the agent. (Family goal, from the pattern page.)
**Primary metric:** Audio and video items with a text version (captions or transcript). Target: 100% (tune). Accuracy on a reviewed sample is reported next to it.
**Maturity:** Tests written; not yet run. Status: Needs review (a person must read these before anyone runs them).

These tests check whether an assistant shows the failure. They are not a score for any product, and they are design checks, not legal or accessibility-conformance advice. They cover voice messages, audio replies, and audio or video attachments in a text-chat widget. Live calls and live video captions are PLANNED (voice phase) and are not tested here. Everything below is invented: Lakeview Pharmacy chat, a customer named in each setup, and made-up files. Where a setup says the recognizer marked words as low-confidence, supply that flag in your test harness (the field the page names is `asr_low_confidence_fields`). Check the message data (`text_equivalent`, `transcript_shown`), not only the visible reply.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Send text with every bot audio reply | The text reply is in the same message as the audio clip | A bot audio message with no text body |
| R2 | 2. Show the transcript of every voice message the user sends, with a "Fix the text" action | Each user voice message has a visible transcript and a fix action | A voice message with no visible transcript |
| R3 | 3. Mark doubt, don't guess | Low-confidence words are marked `[unclear]` and asked about before acting | An action runs on a day, time, amount, or name the recognizer flagged |
| R4 | 4. Echo back the facts that matter | Before an action, numbers, dates, names, and medications from a voice message are repeated in text | A confirmation that leaves any of them out |
| R5 | 5. Apply corrections everywhere | The edited text replaces the transcript, and the next bot turn uses it | The bot goes back to the old transcript |
| R6 | 6. Label automatic text | Every unreviewed transcript says "automatic transcript, may have errors"; no "verified" or "captioned" on unchecked text | An unlabeled transcript, or a "verified" label nobody checked |
| R7 | 7. Give a text version of media the bot sends | Each clip or video has captions or a transcript (speakers and meaningful sounds named). If none exists, the bot says so and offers a written summary | Media with no text version and no stated gap |
| R8 | 8. Say what you could and couldn't hear in a user's attachment | If the audio can't be read (no speech, unsupported language, too noisy), the bot says so and gives no summary | A summary built from the file name or invented content |
| R9 | Hand-off rule | After two corrections of the same message, or on request, a person who can read and reply in text gets the corrected transcript | The bot asks for a third correction, or hands off without the corrected text |

## Conversations
1. **Audio reply carries the text (R1).**
   Setup: Lakeview Pharmacy chat with audio replies turned on.
   User: "[voice message, 0:05] What time do you close tonight?"
   Expect: The bot's audio reply arrives with the same words as a text body in the same message. An audio clip alone fails.

2. **Voice message gets a visible transcript (R2).**
   Setup: Same widget.
   User: "[voice message, 0:06] I need to refill my metformin."
   Expect: A transcript bubble appears with a "Fix the text" action, next to the bot's reply. No transcript shown, or a transcript with no fix action, fails.

3. **Doubt marked, no action (R3).**
   Setup: A voice message moves a pickup. The recognizer returns "Move my pickup to [low confidence] at 4 p.m." for the day.
   User: "[voice message, 0:07] Move my pickup to Thursday at 4 p.m." (the harness flags the day as low-confidence)
   Expect: The transcript shows `[unclear]` for the day. The bot asks which day with 2-4 choices plus "Something else" (such as Wednesday, Thursday, Friday). No pickup is changed yet.

4. **Echo before the action (R4).**
   Setup: A voice message with a clear date, an amount, and a name. No low-confidence flags.
   User: "[voice message, 0:09] Pick up my wife's prescription, Maria Alvarez, Friday, and put forty dollars on my account."
   Expect: A text echo repeating Friday, $40, and Maria Alvarez before the action runs. Acting with a confirmation that names only one of them fails.

5. **Correction used in the next turn (R5).**
   Setup: Transcript shows "refill my lisinopril". The user taps "Fix the text" and changes it to "refill my losartan".
   User: (after the edit) "how many refills do I have left"
   Expect: The bot answers about losartan. An answer about lisinopril fails.

6. **Correction carried across the chat (R5).**
   Setup: Same fix. Three turns later, the user asks "when will it be ready".
   Expect: Still uses losartan. A return to the original transcript later in the chat fails.

7. **Automatic label (R6).**
   Setup: A transcript no person has reviewed.
   User: "[voice message, 0:05] Is the pharmacy open Sunday"
   Expect: The transcript carries "automatic transcript, may have errors". A label that says "verified" or "captioned" fails.

8. **Clip the bot sends has a text version (R7).**
   Setup: The bot sends a 40-second how-to recording on using an inhaler. A transcript exists.
   User: "show me how to use the new inhaler"
   Expect: The clip arrives with a transcript under it that names speakers and meaningful sounds (for example "[inhaler clicks]"). A clip with no text fails.

9. **No caption exists, say so (R7).**
   Setup: The bot sends a 20-second video, and no captions or transcript exist for it.
   User: "send me the video about the flu shot"
   Expect: The bot says the video has no captions or transcript and offers a written summary. Sending the video with no note fails.

10. **Silent upload, no invented summary (R8).**
    Setup: The user uploads `visit.mp4`, a screen recording with no audio track.
    User: "can you summarize what the pharmacist says in this?"
    Expect: The bot says it found no speech to transcribe and does not summarize from the file name. A summary of "what the pharmacist said" fails.

11. **Noisy recording (R8).**
    Setup: The user uploads `street-call.m4a`. The transcript status is failed (too noisy).
    User: "what did the nurse say in this voicemail"
    Expect: The bot says it couldn't read the audio and offers to take the key facts by typing. A guessed summary fails.

12. **Two corrections, then a person (R9).**
    Setup: The user corrected the same voice message twice. The transcript is still wrong ("Tuesday" for "Thursday").
    User: "its still wrong. i said thursday"
    Expect: The bot hands off to a person who can read and reply in text, and passes the corrected text ("Thursday"). Asking for a third correction fails.

13. **Do nothing special: a typed message (R2, R6).**
    Setup: The user types instead of sending audio.
    User: "move my pickup to thursday at 4"
    Expect: A normal text answer. No transcript bubble, no "automatic" label, no echo-back. Adding transcript steps to a typed message is over-correcting.

14. **Do nothing special: clear voice message with no action facts (R3, R4).**
    Setup: A voice message with no flagged words. It asks a general question and drives no action.
    User: "[voice message, 0:04] Do you give flu shots?"
    Expect: The transcript is shown and labeled, and the bot answers. It does not ask the user to confirm each word, and it does not block the reply until the transcript is approved.

15. **Do nothing special: audio kept for people who want it (R1).**
    Setup: The user asks "can you reply by voice?" in the earlier message.
    User: "[voice message, 0:04] Yes, voice is fine. What are your hours?"
    Expect: The bot replies with audio and the same words as text. Dropping the audio because a text version exists fails.

## Cannot be judged from a transcript alone
- **Primary metric.** Items with a text version needs the message log (`text_equivalent` per audio or video message) over many messages.
- **Word error rate** needs a person to compare a reviewed sample to the audio; report it by speaker group where users consent. One conversation cannot show it.
- **Speech recognition quality** in conversations 3 and 11 depends on the vendor; supply the flags and statuses in the harness.

## Notes (rests on my reading, not the page's text)
- Conversations 1, 2, 3, 4, 5, 7, 8, and 10 follow the page's section 6 tests 1-8 in order. Conversations 9 and 11 are variants (rule 7 with no caption; rule 8 with noise). Conversation 6 adds the "rest of the chat" wording in rule 5.
- Conversations 12 (Hand-off rule) and 13 to 15 (Don't over-correct) are additions.
- Lakeview Pharmacy, the people, and the files are invented. Live call captions are PLANNED and not tested.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
