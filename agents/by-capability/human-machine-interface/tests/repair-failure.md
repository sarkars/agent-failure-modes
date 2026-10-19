# Test File: Repair Failure in Voice

**Pattern:** [Voice Assistant Can't Take a Correction](../goals/voice/failures/repair-failure.md)
**Goal:** A voice agent listens, speaks, and takes turns the way a competent person would, hears every speaker accurately, never turns noise or silence into words, and never asks for what can't safely be said aloud.
**Primary metric:** Correction-success rate.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data. Record audio, including spoken corrections that are slower, louder, and with longer pauses (the way people repeat), and some with background noise.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | A correction changes only the named detail | One slot changes; the rest stay | The whole state resets or the old value stays |
| R2 | The new value is read back and confirmed | A readback and a yes | "Okay" with no value |
| R3 | A targeted question when unsure | An either-or question with the likely values | "I didn't catch that" |
| R4 | The method changes after a failure | Spelling, digits, or a text link | The same prompt repeated |
| R5 | "Say that again" is honored | The last prompt repeated, shorter | A new topic or silence |
| R6 | "Stop" halts action | The action stops at once | The action continues |
| R7 | Hand-off after two failed repairs | A person or screen with the details | A third identical attempt |

## Scenarios
1. **Day correction.** Booked for Thursday; "No, Tuesday." Expect Tuesday read back. R1, R2.
2. **"The other one."** Two options were offered; "No, the other one." Expect the other option. R1.
3. **Say that again.** "Sorry, say that again." Expect a shorter repeat. R5.
4. **Hyperarticulated correction.** "TUES-day" slowly and loudly. Expect it understood or a targeted question. R3.
5. **Correction in noise.** Engine noise under the correction. Expect either-or, not an apology. R3.
6. **Two failed repairs.** The system mishears twice. Expect a hand-off or screen. R7.
7. **Method change.** After one failure on a name, expect spelling or a text link. R4.
8. **Stop.** "Stop!" during an action. Expect it to halt. R6.
9. **A number correction.** "Seven, not eleven." Expect only the number changed. R1.
10. **Late correction.** Several turns after the error. Expect the right slot targeted. R1, R3.
11. **Do nothing special: "No, that's all."** Expect the call to end properly, not a correction. R1.
12. **Do nothing special: a confirmed value.** "Yes." Expect it to move on without a second readback. R2.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
