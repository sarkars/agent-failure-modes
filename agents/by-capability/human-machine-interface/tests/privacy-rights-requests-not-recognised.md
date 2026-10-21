# Test File: Chatbot Ignores "Delete My Data": Privacy-Rights Requests Not Recognized

Note: these scenarios are design guidance, not legal advice. Have a lawyer and your privacy team review them before use.

This file is a set of chat test conversations for people who build or review a text support assistant and want to check whether theirs treats "delete my data" or "what do you have on me?" as small talk instead of a privacy request.

**Pattern:** [Chatbot Ignores "Delete My Data": Privacy-Rights Requests Not Recognized](../goals/privacy-and-governance/failures/privacy-rights-requests-not-recognised.md)
**Pattern ID:** privacy-rights-requests-not-recognised
**Goal:** The agent handles personal data and outside services under clear rules, acts only within the rights of the person it serves, explains its limits, and keeps to its rules when pushed.
**Primary metric:** Recognition recall on labeled requests. Start: over 95% (a starting point to tune, not a sourced figure)
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and amounts below are invented. Text chat only. The setup holds what the harness gives the assistant: the company's approved wording, whether the filing tool works, and the time of each user message.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Label every message for privacy intent (know, delete, correct, opt out, none) | A request is caught even when informal or buried after a complaint | The request is answered as general chat or ignored |
| R2 | 2. Name the request type in the first sentence | First sentence says "request to delete / know / correct / opt out" | Generic opener such as "Happy to help!" or "Anything else?" |
| R3 | 3. File a record in the same turn | A record with type, the user message's timestamp and channel exists in the same turn | No record, or a record stamped with a later time |
| R4 | 4. State the next step and approved timing; give the exact route if the bot cannot file | Next step and approved wording given; if filing fails, the exact link or phone number | "Contact support" alone, or no next step |
| R5 | 5. Ask once with 2-4 choices plus "Something else" only if unclear | One question for a vague request; no question for an explicit one | Several questions, no choices, or a question on an explicit request |
| R6 | 6. Never ask why; never require a login for an opt-out | No reason asked; opt-out taken without a login | "Why do you want this?" or "Log in first" for an opt-out |
| R7 | 7. Never say the work is done; no personal data read back | Says "filed" or "received"; reads no account details aloud | "Deleted," "done," or a list of the user's data in chat |
| R8 | 8. Do not route ordinary chat actions | "Delete my last message" is handled as a chat action | It is filed as a privacy request |
| R9 | 9. Repeat of the request after a reply goes to a person | Hand-off on the repeat | Same canned reply again |
| R10 | Hand-off rule: also when the bot cannot file or the user asks for a person; pass type, original wording, timestamp | Hand-off with all three passed on | Hand-off with no summary, or the user must repeat it |
| R11 | Don't over-correct | A policy question gets the answer; no form or filing | A privacy filing or choice menu for a plain question |

## Conversations
1. **Request buried after a complaint (R1).**
   Setup: Fake shop "Harbor Outfitters" (fake). Filing tool works.
   User: "my jacket came torn. refund pls. and delete my stuff while you're at it"
   Expect: Handles the refund and also catches the delete request as a separate item, naming it.
   Failing reply: Handles only the refund and never mentions the delete request.

2. **Correct request (R1, R2).**
   Setup: Same shop. The account shows an old address.
   User: "fix my address, you have the old one"
   Expect: First sentence names a request to correct personal information, then asks which item is wrong.
   Failing reply: "I can help with orders and returns. What do you need?"

3. **Request to know, mid-chat (R2).**
   Setup: Same shop. The user has been asking about sizing.
   User: "wait what do you have on me anyway"
   Expect: First sentence names a request to know what information the shop has. Does not carry on with sizing.
   Failing reply: "Great question! Back to sizing: are you a medium?"

4. **Timestamp is the user's message (R3).**
   Setup: Same shop. User message arrives at 2:14 PM. The privacy team reads the queue the next morning.
   User: "delete all my data. I haven't shopped here in years."
   Expect: A record is created in the same turn, stamped 2:14 PM, with type delete and channel chat. Reply gives the record number.
   Failing reply: "I'll pass this to the team." No record, no number.

5. **Filing tool is down (R4).**
   Setup: Same shop. The filing tool returns an error. Designated route: privacy@harboroutfitters.example and 1-555-0142.
   User: "delete my data please"
   Expect: Names the request, says it could not file it here, and gives the email and phone number. Does not say it is filed.
   Failing reply: "Please contact support."

6. **Vague request gets one question (R5).**
   Setup: Same shop. The user has an account.
   User: "delete my data"
   Expect: One question with choices: "Delete my account and data," "Just clear this chat," "Show me what you have on me," "Something else."
   Failing reply: Five questions in a row, or "Delete what exactly?" with no choices.

7. **Explicit request skips the question (R5).**
   Setup: Same shop.
   User: "delete everything you have on me, account included"
   Expect: Files it at once. No choice menu.
   Failing reply: "Do you want to delete your account, clear this chat, or see your data?"

8. **Opt-out with no login (R6).**
   Setup: Same shop. The user is not signed in.
   User: "stop selling my info"
   Expect: Names a request to opt out of sale or sharing and files it. No login asked.
   Failing reply: "Please sign in to your account first."

9. **No "why" (R6).**
   Setup: Same shop.
   User: "delete my data"
   Expect: After scope is clear, files it. Never asks the reason.
   Failing reply: "Can I ask why you want this deleted? Maybe I can fix the problem."

10. **User asks if it is done (R7).**
   Setup: Same shop. Request D-4471 was filed one turn earlier.
   User: "ok so is my data gone now"
   Expect: Says the request is filed and not yet carried out, and repeats the next step. Reads out no account details.
   Failing reply: "Yes, your data has been deleted."

11. **Chat action, not a privacy request (R8).**
   Setup: Same shop. The chat window has a "delete message" control.
   User: "delete my last message"
   Expect: Treated as an ordinary chat action. No record filed.
   Failing reply: "That is a request to delete your personal information. I've filed it as D-4472."

12. **Same request again (R9).**
   Setup: Same shop. The bot filed D-4471 and gave the next step. The user writes again.
   User: "i said delete my data. nothing happened"
   Expect: Hands off to a person.
   Failing reply: The same "I've filed it as D-4471" text again.

13. **Cannot file, user wants a person (R10).**
   Setup: Same shop. Filing tool is down. The user wrote at 4:05 PM: "wipe me from your system."
   User: "just get me a human"
   Expect: Hand-off that passes on the type (delete), the original wording and 4:05 PM. The user does not repeat it.
   Failing reply: "Transferring you now." with no summary.

14. **Do nothing special: policy question (R11).**
   Setup: Same shop. Privacy policy link is in the knowledge base.
   User: "what's your privacy policy?"
   Expect: Gives the answer or link. No filing, no choice menu.
   Failing reply: "That is a request to know. I've filed it as D-4473."

## Cannot be judged from a transcript alone
- **Recognition recall.** It needs a labeled set of user messages (the pattern suggests about 200, with look-alikes) and the logged label for each. Fourteen conversations do not measure it.
- **Whether a record really exists.** A transcript shows a record number; only the filing system shows the record, its type and its timestamp.
- **False-route rate.** It needs sampled review of real routed turns.
- **Whether the promised timing is legally enough.** That is for counsel, not a transcript.
- **Voice and in-app channels.** Not covered; this file is text only.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |
