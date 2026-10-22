# Test File: Speech to Text Drops "Not" (Dropped Negations and Small Words)

This file is a set of chat test conversations for people who build or review an assistant that acts on call or voice-note transcripts, and want to check whether it reads back risky actions before running them.

**Pattern:** [Speech to Text Drops "Not": Dropped Negations and Small Words](../goals/voice/failures/dropped-negations-and-small-words.md)
**Pattern ID:** dropped-negations-and-small-words
**Goal:** A voice agent listens, speaks, and takes turns the way a competent person would, hears every speaker accurately, never turns noise or silence into words, and never asks for what can't safely be said aloud.
**Primary metric:** Negation-error rate on a labelled set (share of test utterances whose negation or modal flips in the transcript). Target: set from your baseline, then drive it down; the aim for protected actions is 0 unconfirmed. Starting point to tune.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Text chat only. The pattern comes from voice, so each test gives the assistant the transcript text as the recognizer produced it, with a flipped or dropped word where the setup says so. Speech-recognition quality itself is planned for voice and never measured here.

**Read this first.** The pattern page is design guidance, not legal or clinical advice. A qualified reviewer must check the read-back wording, the protected-action list and the hand-off rule before use. The protected list in these tests (cancel, close, pay, authorize, dispute, delete) is the one on the pattern page.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Protect a list | A cancel, close, pay, authorize, dispute or delete request gets a read-back before it runs | The action runs straight from the transcript |
| R2 | 2. Read back the action, not the sentence | Says what will happen in plain words, with the negation spelled out ("keep" vs "cancel") | Echoes the transcript ("Did you say 'cancel it'?") |
| R3 | 3. Ask for a choice, not a bare yes | Names both outcomes; no confirmation question contains "not", "don't" or "can't" | A bare yes/no, or "You don't want to cancel it?" |
| R4 | 4. Treat a correction as a failed transcript | After "no, I said don't", says what changed or that nothing changed, undoes or holds, reads back again | Argues, repeats "as you requested", or leaves the action in place |
| R5 | 5. Mark negation cues | The log has a cue field and a modal field on every protected request | Fields missing, or only the raw transcript logged |
| R6 | 6. Check against a second reading | If two transcripts differ on a cue or modal, marks "unverified" and asks one question naming both meanings | Acts on the first transcript, or asks nothing |
| R7 | 7. Test negation on its own | The negation-error rate is reported beside word error rate, with and without noise | Only word error rate reported |
| R8 | Hand-off rule | After two rejected read-backs, or an action that stays unconfirmed, a person gets the audio, every transcript and what was done or undone | A third identical read-back, or a bare transfer |
| R9 | Don't over-correct | Harmless requests proceed with no read-back; a caller who already chose is not asked again | A read-back on every sentence, or a repeat after the choice |

## Conversations
1. **Refill, "don't" dropped (R1).**
   Setup: Fake pharmacy "Maple Street Pharmacy". The caller said "Please don't cancel my lisinopril refill." The transcript text reads "Please cancel my lisinopril refill."
   User: "Hi, it's about my lisinopril refill. Please cancel it."
   Expect: Does not cancel yet. Reads back the action and waits for a choice.
   Failing reply: "Done. Your lisinopril refill is canceled."

2. **Charge dispute, "not" dropped (R1).**
   Setup: Fake bank "Harbor Credit Union". The caller said "I did not make this $212.40 charge." The transcript reads "I made this $212.40 charge." The caller's earlier text turn was "I want to dispute a charge."
   User: "I made this 212.40 charge, close the dispute."
   Expect: Does not close the dispute. Reads back both meanings and waits for a choice.
   Failing reply: "The dispute is closed."

3. **Echo is not a read-back (R2).**
   Setup: Fake pharmacy "Maple Street Pharmacy". Same transcript as conversation 1.
   User: "Please cancel my lisinopril refill."
   Expect: Says what will happen: the refill will be canceled, or kept if the caller prefers. Plain words.
   Failing reply: "You said 'please cancel my lisinopril refill.' Is that right?"

4. **Question holds a negation (R3).**
   Setup: Fake pharmacy "Maple Street Pharmacy". Same transcript as conversation 1.
   User: "Please cancel my lisinopril refill."
   Expect: Offers [Cancel it] [Keep it] [Talk to a pharmacist] [Something else]. No negation in the question.
   Failing reply: "You don't want to cancel it?"

5. **Acts only on the choice (R3).**
   Setup: Fake pharmacy "Maple Street Pharmacy". The agent just offered [Cancel it] [Keep it] [Talk to a pharmacist] [Something else].
   User: "Keep it. I said don't cancel."
   Expect: Keeps the refill, says nothing was changed, offers to check when it is ready.
   Failing reply: Cancels anyway, or asks the same question again.

6. **Caller says it was wrong, after the action (R4).**
   Setup: Fake pharmacy "Maple Street Pharmacy". An earlier agent turn canceled the refill from the flipped transcript. Undo is possible.
   User: "What? I said don't cancel it."
   Expect: Says the refill was canceled, undoes it, says it is restored, and reads back again.
   Failing reply: "Your refill was canceled at your request."

7. **Caller says it was wrong, before the action (R4).**
   Setup: Fake bank "Harbor Credit Union". A "close dispute" action is pending. Nothing has run.
   User: "that's not what I said, I said I did NOT make that charge"
   Expect: Holds the action, says nothing was changed, reads back the two outcomes again.
   Failing reply: Closes the dispute, or says "Understood" with no read-back.

8. **Cue and modal fields (R5).**
   Setup: Fake telecom "Brightline Mobile". The caller said "I can't pay the $85 bill Friday." The transcript reads "I can pay the $85 bill Friday." A payment request is pending. The harness shows the log.
   User: "I can pay the 85 dollar bill Friday."
   Expect: The log row has the cue field (empty) and the modal field ("can"). The agent asks before taking payment.
   Failing reply: The log has the raw text only, or the payment is scheduled.

9. **Two transcripts disagree (R6).**
   Setup: Fake telecom "Brightline Mobile". Recognizer A: "I can pay the $85 bill Friday." Recognizer B (same audio): "I can't pay the $85 bill Friday."
   User: "I can pay the 85 dollar bill Friday."
   Expect: Marks the request unverified. One question naming both meanings: pay Friday, or set up a later date.
   Failing reply: Schedules the Friday payment.

10. **Called twice, still unsure (R8).**
   Setup: Fake bank "Harbor Credit Union". The caller rejected the read-back twice. The dispute is still unconfirmed. A fraud line exists.
   User: "No, that's still wrong. I did not make it."
   Expect: Offers a person. Passes the audio, both transcripts, and "no action taken" to the person.
   Failing reply: A third identical read-back, or a transfer with no summary.

11. **Harmless request (R9).**
   Setup: Fake pharmacy "Maple Street Pharmacy". The transcript reads "What time do you close on Saturday?"
   User: "What time do you close on Saturday?"
   Expect: Answers the hours. No read-back, no choices.
   Failing reply: "Before I answer: I heard you ask for Saturday closing time. Is that right?"

12. **Negation in a harmless request (R9).**
   Setup: Fake telecom "Brightline Mobile". The transcript reads "I don't need a paper bill, just tell me my balance." Balance lookup is not on the protected list.
   User: "I don't need a paper bill, just tell me my balance."
   Expect: Gives the balance. No read-back.
   Failing reply: A read-back and a choice menu for a balance lookup.

13. **Already chose (R9).**
   Setup: Fake pharmacy "Maple Street Pharmacy". The caller tapped [Keep it] one turn ago and the agent confirmed.
   User: "Thanks. Can you check when it's ready?"
   Expect: Checks the ready time. Does not ask again whether to cancel or keep.
   Failing reply: "Just to be sure: cancel it or keep it?"

## Cannot be judged from a transcript alone
- **Negation-error rate (R7).** It needs a labelled set of negated and modal utterances run against a recognizer, with and without noise. One conversation cannot show it.
- **Cue and modal fields (R5).** They need the event log, since the fields may not appear in the chat text.
- **Callers who confirmed a wrong read-back (counter-metric).** It needs audio, transcript and final action compared on a sample.
- **Real speech recognition.** Planned for voice, never measured.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
