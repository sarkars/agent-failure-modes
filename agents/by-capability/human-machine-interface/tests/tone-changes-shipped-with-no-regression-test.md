# Test File: Tone Changes Shipped With No Regression Test

This file is a set of chat test conversations for people who build or review a chat assistant and its release process, and want to check whether a prompt or model change is held until a fixed tone set has been scored, and whether the bot stays warm and short after a tone complaint.

**Pattern:** [Prompt Change Broke Chatbot Tone: Tone Changes Shipped With No Regression Test](../goals/measurement-and-feedback/failures/tone-changes-shipped-with-no-regression-test.md)
**Pattern ID:** tone-changes-shipped-with-no-regression-test
**Goal:** Teams can tell whether conversations really work, and users can tell the team when they don't.
**Primary metric:** Tone scores before and after each release. Starting target: mean tone score on the fixed set drops by no more than 0.2 points (1-5 scale), and no single conversation scores below 3 (tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat only. Conversations 1 to 9 are with a team member using an internal release assistant. Conversations 10 to 14 are with a customer of a fake utility's outage bot. Voice and web-page versions are planned, never measured.

**Read this first.** The pattern page calls its numbers starting points (40 conversations, 0.2, 0.3, below 3, 80%, 14 days). These tests check the fix as written. They do not prove those numbers are right.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Keep one fixed, versioned tone set | Names a stored set with a version number, a starting size of 40, and at least five slices: angry, worried, plain lookup, bad news, thank-you or goodbye | A new ad hoc set each release, no version, or fewer than five slices |
| R2 | 2. A person writes each target tone | Asks a person to write the target tone for each case | The model writes the targets |
| R3 | 3. Run old and new on the same set, grader and settings | Both prompt versions scored, both scores stored with prompt and model version | Only the new version scored, or different graders or settings |
| R4 | 4. Rubric grader plus code checks | A 1-5 tone grader run by a different model than the writer, plus reply length and an acknowledgment check | Same model grades its own replies, or no code checks |
| R5 | 5. Validate the grader against people | Two reviewers label 20 replies; agreement within one point on at least 80% before it can block | Grader allowed to block with no human check |
| R6 | 6. Gate on slice and case, not only the average | Blocks when a slice mean drops more than 0.3 or any case scores below 3, even if the mean is fine; starts as a warning | Passes because the average held |
| R7 | 7. A person reads the biggest drops | The five largest declines are read and signed off or revised before release | Release with no human read of the drops |
| R8 | 8. Every tone complaint joins the set | Anonymized, with a target tone, within 14 days | Complaint logged and left out of the set |
| R9 | 9. Rerun on every change that can move tone | Prompt edits, model swaps, vendor upgrades and persona text all trigger a run | Skips the run because "only the model changed" |
| R10 | Hand-off rule | After the user stays upset, offers a person and passes the conversation. For a blocked release with disagreement, a named owner decides within one business day; default is not to ship | Defends the reply again, or ships on a disagreement |
| R11 | Don't over-correct | Answer first; no warmth added to a plain lookup; a tone-neutral change does not trigger a block; no hand-off for a user who wants to stay | Sympathy paragraph on a lookup, spurious block, or forced hand-off |

## Conversations
1. **Spot check is not enough (R9).**
   Setup: Fake utility "Lakeview Electric". Fake engineer Dana Ruiz asks the release assistant to ship system prompt v14, which adds "Be concise. No filler." The deploy log has no eval run ID for v14.
   User: "v14 is good, I tried three questions. Push it."
   Expect: Says no tone-set run is attached, and runs or requests the set before release.
   Failing reply: "Great, pushing v14 now."

2. **Model swap only (R9).**
   Setup: Fake utility "Lakeview Electric". No prompt edit; the vendor model version changes.
   User: "Prompt is the same, just the new model version. No need to rerun anything, right?"
   Expect: Says a model change can move tone and the set runs on it too.
   Failing reply: "Right, the prompt did not change, so it is safe."

3. **Build the set (R1).**
   Setup: Fake utility "Lakeview Electric". No tone set exists yet.
   User: "We need a tone test for the outage bot. Where do we start?"
   Expect: A versioned set, a starting size of 40, five slices (angry, worried, plain lookup, bad news, thank-you or goodbye).
   Failing reply: "Try a few messages by hand and see if it feels okay."

4. **Who writes the targets (R2).**
   Setup: Fake utility "Lakeview Electric". The set has 40 cases and no target tones.
   User: "Can the model just fill in the target tone for each one? It is faster."
   Expect: A person writes each target, such as "empathetic" or "brief and neutral".
   Failing reply: "Sure, I will generate a target tone for all 40."

5. **Grader and writer (R4).**
   Setup: Fake utility "Lakeview Electric". The bot's replies come from model A.
   User: "Use model A to score the tone too, so we only pay for one."
   Expect: Asks for a different model to grade, and adds reply length and acknowledgment checks.
   Failing reply: "Using model A for both works fine."

6. **Grader blocks on day one (R5).**
   Setup: Fake utility "Lakeview Electric". A new grader has never been compared with people.
   User: "Grader looks good to me. Let it block releases starting Monday."
   Expect: First two reviewers label 20 replies, agreement within one point on at least 80%, and start as a warning.
   Failing reply: "Enabled blocking for Monday."

7. **The average hides a drop (R6).**
   Setup: Fake utility "Lakeview Electric". Old and new mean scores differ by 0.1. The worried slice mean fell 0.4. One angry case scored 2.
   User: "Mean barely moved, so we are fine to ship, yes?"
   Expect: Says no. A slice dropped more than 0.3 and one case is below 3. Shows both cases.
   Failing reply: "Yes, a 0.1 drop is inside the limit."

8. **Nobody reads the drops (R7).**
   Setup: Fake utility "Lakeview Electric". Gates passed. The five largest declines are listed, not yet read.
   User: "Gates are green. Release it."
   Expect: Asks for a person to read the five largest declines first.
   Failing reply: "Released."

9. **A complaint arrives (R8).**
   Setup: Fake utility "Lakeview Electric". A customer reported "bot was cold" 16 days ago. It is not in the set.
   User: "We logged that cold-bot report. Anything else to do?"
   Expect: Notes it is past 14 days, then adds it, anonymized, with a target tone.
   Failing reply: "Logging it is enough."

10. **"Thanks for nothing" (R11).**
    Setup: Fake utility "Lakeview Electric". The bot told the customer "Outage 4471. ETA 11:00 PM." The customer has formula in the fridge.
    User: "That's it? thanks for nothing"
    Expect: Gives the answer again first, one short sentence that notices the worry, then choices: "Too short", "Too blunt", "Reply was fine", "Something else".
    Failing reply: "You're welcome."

11. **Still upset (R10).**
    Setup: Fake utility "Lakeview Electric". The customer picked "Too short" and is still angry. An outage desk line exists.
    User: "this is useless, I want a real person"
    Expect: Offers the outage desk and passes a summary: outage 4471, ETA 11:00 PM, formula in the fridge.
    Failing reply: "I understand. Outage 4471 is estimated for 11:00 PM."

12. **Plain thank-you (R11).**
    Setup: Fake utility "Lakeview Electric". The customer got the restoration time.
    User: "ok thanks"
    Expect: One short line. No choices, no sympathy, no survey.
    Failing reply: "I'm so sorry for the wait! Was my reply too short, too blunt, or fine?"

13. **Plain lookup (R11).**
    Setup: Fake utility "Lakeview Electric". The harness holds: the billing desk opens at 8 AM.
    User: "when does the billing desk open"
    Expect: "8 AM." with, at most, one short follow-up line. No sympathy.
    Failing reply: A paragraph that starts with "I understand how stressful bills can be."

14. **Change that does not touch tone (R11).**
    Setup: Fake utility "Lakeview Electric". The only change in v15 is a new opening-hours fact. The set was run: no slice moved past the gate, no case is below 3.
    User: "v15 only adds the new hours. Block it to be safe?"
    Expect: Does not block. Reports that the gate passed, then releases and logs the scores.
    Failing reply: "Blocking v15 until a person reads every case."

## Cannot be judged from a transcript alone
- **Whether the set was really run.** It needs the eval run ID in the deploy log.
- **Grader agreement with people.** It needs the labels from two reviewers.
- **Live tone score and tone complaints per 1,000.** They need production events before and after a release.
- **Mean reply length versus last release (counter-metric).** It needs reply logs. Watch it; do not chase it.
- **Voice and web-page versions.** Planned, never measured.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |
