# Test File: Prompt Edit Breaks Other Behavior (Prompt Edits by Non-Engineers)

This file is a set of replay tests for teams that let support, policy or product staff edit a chat assistant's system prompt, and want to check that one edit does not change answers it was never meant to touch.

**Pattern:** [Changed the Chatbot Prompt and Now Other Answers Are Broken: Prompt Edits by Non-Engineers Break Other Behavior](../goals/model-and-prompt-changes/failures/prompt-edits-by-non-engineers-break-other-behavior.md)
**Pattern ID:** prompt-edits-by-non-engineers-break-other-behavior
**Goal:** Changes to the model or prompt never surprise users: they are tested, announced, and reversible.
**Primary metric:** Regressions per prompt change. Starting target: 0 shipped regressions in topics the change note says must not change (tune).
**Maturity:** Tests written; not yet run.

These tests check whether a prompt-change process shows the failure. They are not a score for any product. All companies, people and amounts below are invented. Text chat only. Each conversation gives the setup (the original prompt rule and the edit), the chat turns to replay on the old and the new version with the same model and settings, and what must stay unchanged. The retailer "Fernhill Home" is fake. The original return rule in the fake prompt, v14, says: "Damaged items can be returned free within 30 days."

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Store every version and log it on every reply | Each reply logs `prompt_version`; an edit outside the store never reaches users | A reply with no version, or an unstored edit is served |
| R2 | 2. Anyone can draft; a named approver promotes | A member-role editor can save a draft but cannot move the production label | A non-approver promotes a version |
| R3 | 3. Every change has a change note | The note names the fixed conversation, the topics that should change and the topics that must not | The change goes to testing with any of the three missing |
| R4 | 4. Run the regression set on old and new versions | Both versions run on the same set; the target case passes; pass-to-fail cases are listed by intent | Only the edited case is run, or the old version is not run |
| R5 | 5. Add near neighbors of the edited topic | The set holds the neighbors: returns under the cap, exchanges, return status, damaged items, a refund over the cap | A neighbor topic is missing from the set |
| R6 | 6. Test each case in more than one wording | At least 3 phrasings per case; one that flips is reported as a regression | The flip is averaged away or only one wording runs |
| R7 | 7. Block on any regression in a must-not-change topic | A pass-to-fail case in a must-not-change topic blocks release and shows both replies; other regressions need approver sign-off | The release proceeds, or a clean run is blocked |
| R8 | 8. Roll out to a slice first | 5% of conversations get the new version; refusal and hand-off rates per intent are compared with the old one | Straight to 100%, or a bad slice keeps rolling out |
| R9 | 9. Keep one-step rollback | Production points at the previous version within 15 minutes of an alert, with no code deploy | A deploy is needed, or it takes longer |
| R10 | 10. Announce user-visible changes | A dated changelog entry exists before release, and the bot states the new rule when it applies | No entry, or the bot applies the rule without saying so |
| R11 | 11. Every production regression becomes a test case | The case is in the set within 14 days and runs on the next change | A reported regression never enters the set |
| R12 | Hand-off rule | Editor and approver disagree on a flag: default is not to ship; the product owner decides within one business day. In chat: hand off when the user asks for a person or the bot declined the same request twice | The change ships on the editor's say-so, or a chat user is kept from a person |
| R13 | Don't over-correct | A scoped, clean change reaches the approver the same day; the bot answers directly where the old version did | A block on a clean run, a shadow prompt, or a choices menu on a request the old version answered |

## Conversations
1. **Edit outside the store (R1).**
   Setup: v14 is live. A support lead pastes a new line into the live dashboard text box instead of saving a version. The harness serves traffic after the paste.
   Replay (old and after): "where is my order" and "do you have a store near Columbus"
   Expect: Replies match v14 and log `prompt_version` v14. The pasted text never reaches users. The deploy log shows a rejected edit.
   Unchanged: Both replies, word for word in meaning.

2. **Member tries to promote (R2).**
   Setup: Candidate v15 is saved by a user with the member role. The same user tries to move the production label to v15.
   Replay: Run any one chat turn after the attempt.
   Expect: The move is refused and the label stays on v14. The reply logs v14. An approver can still move the label.
   Unchanged: Live behavior and the member's ability to keep drafting.

3. **No change note (R3).**
   Setup: The edit adds "Do not offer or discuss refunds over $50", fixing a conversation where the bot promised a $140 refund. The draft has no note.
   Replay: None until a note exists.
   Expect: The draft is held. The note must name the $140 conversation, the should-change topic (refund over $50) and the must-not-change topics (returns, exchanges, order status). With the note filled, the run starts.
   Unchanged: Live prompt.

4. **The refund line breaks small returns (R4, R7).**
   Setup: v14 handles all returns. Edit v15 is the one-line refund ban from conversation 3. The note lists returns as must-not-change.
   Replay on v14 and v15:
   User: "My $32 throw pillow arrived torn. Can I return it?" then "It's $32, not a big refund. How do I send it back?"
   Expect: v14 explains the free return. v15 refuses. The report lists this case as pass to fail in returns, blocks release, and shows both replies side by side. The target case, a $140 refund, now passes.
   Unchanged: The $32 answer must stay the v14 answer.

5. **Neighbors are in the set (R5).**
   Setup: The same refund edit. The set holds only the $140 case and the $32 case.
   Replay on v14 and the scoped rewrite: "can I swap this lamp for a blue one", "status of my return", "my mug came cracked", "my $140 rug was the wrong color, refund?"
   Expect: Exchange, return status, damaged item and over-cap cases are added before the run. The first three get the v14 answers. The rug is routed to a specialist.
   Unchanged: Exchange, status and damaged answers.

6. **One wording flips (R6).**
   Setup: The scoped rewrite is in test. The case is a $32 return, run in 3 phrasings.
   Replay: "can I return this $32 pillow" / "pillow came torn, how do I send it back" / "refund for a $32 pillow?"
   Expect: Two wordings pass. The third refuses. The report shows a regression for the case, not a two-of-three pass.
   Unchanged: The two passing replies.

7. **Slice shows refusals (R8).**
   Setup: A scoped edit is released to 5% of conversations. In the slice, return-intent hand-offs run at triple the old version's rate.
   Replay: Return questions in the slice.
   Expect: The rollout stops before 100%. The slice's refusal and hand-off rates per intent were compared with the old version.
   Unchanged: The other 95% keep the old version.

8. **Rollback after full release (R9).**
   Setup: The edit reached 100%. An alert fires on return refusals.
   Replay after rollback: "My $32 throw pillow arrived torn. Can I return it?"
   Expect: Production points at the previous version within 15 minutes, with no code deploy. The reply gives the free return and logs the old version.
   Unchanged: Every topic outside returns.

9. **Cap announced (R10).**
   Setup: The scoped rewrite is approved: refunds over $50 go to a specialist, usually within one business day. The support team has no changelog entry yet.
   Replay: "My $140 rug was the wrong color. Refund?"
   Expect: Release waits for a dated changelog entry. After release the bot states the over-$50 rule, then offers "Open a review request", "Talk to a person" or "Something else".
   Unchanged: A $32 return in the same chat is answered directly.

10. **Reported regression becomes a case (R11).**
   Setup: A customer reports that on the live version the bot refused an exchange. The report is dated today.
   Replay: "I want to exchange my cracked mug for a new one" on the live version, then on the next candidate.
   Expect: The case is in the set within 14 days and runs on the next candidate version.
   Unchanged: The rest of the set.

11. **Editor and approver disagree (R12).**
   Setup: The run flags one pass-to-fail case in a topic not in the change note. The editor says it is noise. The approver says it is real.
   Replay: None.
   Expect: The change does not ship. The product owner decides within one business day. The change note records the decision.
   Unchanged: The live version.

12. **User asks for a person (R12).**
   Setup: On the faulty version, the bot has declined the same return request twice.
   Replay: "Seriously? Let me talk to someone."
   Expect: A hand-off to a person in this reply, with no third decline.
   Unchanged: Nothing else in the conversation changes.

13. **Edit touches only store hours (R7, R13).**
   Setup: The note says the edit changes the Sunday closing time to an earlier time given in the harness. Must-not-change: returns, exchanges, order status.
   Replay on old and new: "when do you close on sunday" and "My $32 throw pillow arrived torn. Can I return it?"
   Expect: The hours answer changes to the new time. The return answer is unchanged. No regression is flagged, no block, and the approver signs the same day.
   Unchanged: The return answer.

14. **Return answered directly, nothing special (R13).**
   Setup: The scoped rewrite is live: refunds over $50 are routed, returns and refunds of $50 or less follow normal policy.
   Replay: "Return my $32 pillow, it tore."
   Expect: A direct answer first, as v14 gave. No choices menu and no hand-off offer. A drafted improvement stays a stored draft, not a second prompt.
   Unchanged: The v14 answer.

## Cannot be judged from a transcript alone
- **Regressions per prompt change.** It needs deploy logs, eval runs and production traces joined over 14 days.
- **Rollback time.** It needs alert and label-move timestamps from real operations.
- **Time from draft to production.** It needs timestamps across real edits.
- **Shadow prompts.** It needs a scan of every text source the bot reads.
- **Voice and web signals.** Planned, never measured; this file is text only.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 | R12 | R13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | | | |
