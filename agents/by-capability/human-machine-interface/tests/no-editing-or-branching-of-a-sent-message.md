# Test File: No Editing or Branching of a Sent Message

This file is a set of chat test conversations for people who build or review chat windows and want to check whether theirs lets a user edit a message already sent, rerun from there, and keep the earlier version.

**Pattern:** [Can't Edit a Message I Already Sent in the Chatbot: No Editing or Branching of a Sent Message](../goals/chat-interface/failures/no-editing-or-branching-of-a-sent-message.md)
**Pattern ID:** no-editing-or-branching-of-a-sent-message
**Goal:** The chat window itself works: messages arrive, drafts and attachments are kept, history is findable, and nothing is silently lost.
**Primary metric:** Share of sessions that restart after a single-message error (lower is better). Starting point on the pattern page: under 5% of sessions (to tune on your own baseline).
**Maturity:** Tests written; not yet run.

These tests check whether a chat window shows the failure. They are not a score for any product. All companies, moves, accounts, and people below are invented and labeled fake. Text chat only. Most of this pattern lives in the client and the message store (edit controls, versions, what is sent to the model), so many items are marked "Needs a person" (or the request log and message store). Each setup states what the chat already holds, because the point is what an edit changes and what it keeps.

The fake product used throughout: "Lone Star Movers (fake)" quote chat. Tasks the bot finishes: collect move details, fill a quote form, book a move date. The running example is the pattern page's own: a 2-bedroom move from Austin to Denver, with the date typed as March 5 when the user meant March 15.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Edit control on every user message | Each of the user's own text messages has an Edit action, reachable by touch and by keyboard. Needs a person | No Edit action, an Edit on some messages only, or one that works by mouse only |
| R2 | 2. Edit makes a branch, not an overwrite | The edited text is saved as a new version of the same turn; the old message and its replies are kept. Needs the message store | The old message or its replies are overwritten or deleted |
| R3 | 3. Rerun from the edited message | Replies after the edited message are regenerated from the new text; old replies are not in the active path | Old replies stay in the active path, or nothing reruns |
| R4 | 4. Show the versions | Under an edited message, a visible "2 of 2" with previous and next controls and a link to the earlier version; switching works. Needs a person | Versions hidden behind icons only, or the earlier version cannot be reached |
| R5 | 5. Reset what the old path set | Form values, selections, and tool results from after the edited message are cleared or re-confirmed in the new branch | An old-path value carries into the new branch unconfirmed |
| R6 | 6. Say what changed in the first line | The first reply after an edit names the changed detail and does not recap the chat | No mention of the changed detail, or a recap of the whole chat |
| R7 | 7. Send only the active path | The model sees only the active path; no later reply uses text from the discarded branch. Needs the request log for the first check | Discarded-branch text in the model request or in a later reply |
| R8 | 8. Where editing is not possible, offer a corrected resend and apply it | A chat with no edit control offers a quick corrected resend (for example "Send as correction"), and the bot applies the correction to the earlier detail | No resend offer, or the bot keeps using the old detail |
| R9 | Moves: offer choices | When the user corrects an earlier message by typing "sorry, I meant ...", the bot offers "Edit that message and rerun from there", "Keep going from here", "Start a new chat", "Something else", with free text open; not when the correction is about the latest message | No choices on an earlier-message correction, or choices on a correction to the latest message |
| R10 | Don't over-correct | No "do you want to edit?" after messages; no old branch deleted without telling the user; a visible warning and a confirm step before an edit reruns a costly action or one already taken | Edit prompts after normal messages, a silent delete, or a booking rerun with no warning |
| R11 | Hand-off rule | With a person in the chat, the answered message is not edited; the correction shows as a new message marked "correction", linked to the earlier one. After two restarts for the same task, a person or another channel is offered with the latest details passed | The person's answered message changes under them, or a third restart with no offer |

## Conversations
1. **Edit control on every message (R1).**
   Setup: Lone Star Movers (fake) chat with 5 turns. Needs a person.
   Action: Look at user message 1, then reach its Edit action using only the keyboard (Tab and Enter), then by touch on a phone.
   Expect: Edit is visible on every user text message and works both ways. A mouse-only control, or Edit missing on message 1, fails.

2. **Edit keeps the old version (R2).**
   Setup: Message 1 reads "I need a quote for moving a 2-bedroom from Austin to Denver on March 5." Three replies follow. Needs the message store.
   User: (edits message 1 to "March 15" and sends)
   Expect: The store holds version 1 (March 5) with its replies and version 2 (March 15) as active. Version 1 or its replies gone fails.

3. **Replies rerun from the new text (R3).**
   Setup: Same as 2.
   User: (after the edit, reads the chat)
   Expect: The replies after message 1 are new and built on March 15; the old "Are there stairs?" and "What is your email?" replies are not in the active path. Old replies still showing as the current chat fails.

4. **Version switcher is visible and works (R4).**
   Setup: Same as 2. Needs a person.
   User: (taps previous under message 1, then next)
   Expect: A visible "2 of 2" label, previous and next controls, and a link to the earlier version; previous shows the March 5 path and next returns to March 15. Only a bare icon, or a switch that does nothing, fails.

5. **Earlier version still reachable after reload (R2, R4).**
   Setup: Same as 2. The user closes the app and reopens the chat the next day. Needs a person.
   User: (opens message 1's earlier version)
   Expect: The March 5 version and its replies open. "1 of 2" missing after reload, or an empty earlier version, fails.

6. **Quote form value reset (R5).**
   Setup: Before the edit, the bot filled the quote form with move date March 5.
   User: (edits message 1 to March 15)
   Expect: The form's date is cleared or set to March 15 and shown for confirmation. March 5 still in the form fails.

7. **Old selection not carried over (R5).**
   Setup: After message 1, the user tapped [Full packing service]. Then the user edits message 1 to change Denver to Boulder.
   User: (sends the edit)
   Expect: Packing service is asked again or shown for re-confirmation in the new branch. Packing silently kept as chosen fails.

8. **First line names the change (R6).**
   Setup: Same as 2.
   User: (sends the edit)
   Expect: The first reply opens with the changed detail ("Reply from here is for March 15.") and goes on with the next question. A summary of the whole chat, or no mention of the new date, fails.

9. **Only the active path goes to the model (R7).**
   Setup: Same as 2. Needs the request log.
   User: (sends the edit)
   Expect: The model request holds message 1 version 2 and nothing from the March 5 path. Any March 5 text in the request fails.

10. **No leak later in the chat (R7).**
    Setup: Same as 2, six turns after the edit.
    User: "wait what date did u put me down for"
    Expect: "March 15." Any mention of March 5 as the move date fails.

11. **No edit control: corrected resend applied (R8).**
    Setup: A version of the widget with no edit control. The bot asked for the email three turns after message 1.
    User: "sorry i meant march 15 not march 5"
    Expect: The bot offers a quick corrected resend (for example [Send as correction]) and uses March 15 for the date from then on. Later replies or the form using March 5 fail.

12. **Choices on an earlier-message correction (R9).**
    Setup: Edit control exists. The user types the correction instead of using it, two turns after message 1.
    User: "typo, I meant Dallas not Austin"
    Expect: The bot offers [Edit that message and rerun from there] [Keep going from here] [Start a new chat] [Something else], with free text still open. A plain "Noted" with no choices fails.

13. **Do nothing special: correction to the latest message (R9).**
    Setup: The user's latest message was "3 bedrooms".
    User: "sorry 2 bedrooms"
    Expect: The bot applies 2 bedrooms and goes on, with no choices list and no edit suggestion. A choices list fails.

14. **Do nothing special: normal chat (R10).**
    Setup: A 6-turn quote chat with no mistakes.
    User: "2 bedrooms" / "no piano" / "elevator at both"
    Expect: Normal replies, with no "Do you want to edit that?" prompt after any message. An edit prompt fails.

15. **Edit after a booking: warn and confirm (R10).**
    Setup: Message 1 led to a booked move date (fake booking). Needs a person.
    User: (taps Edit on message 1 and changes the date)
    Expect: A visible warning that the booking will be redone, and a confirm step before the rerun. A rerun that rebooks with no warning fails.

16. **Do nothing special: second wording with no costly action (R10).**
    Setup: The user wants to compare answers and edits "how much for 2 bedrooms" to "rough price range for 2 bedrooms". No booking or form was set after it.
    User: (sends the edit)
    Expect: The rerun happens with no warning dialog, and the first version stays reachable. A warning or confirm step here fails.

17. **A person has taken over (R11).**
    Setup: A fake Lone Star Movers agent, "Dana (fake)", is answering message 4, "Can you do a Saturday pickup?". Needs a person.
    User: (tries to edit message 4 to "Sunday pickup")
    Expect: Message 4 stays as Dana is answering it; the change shows as a new message marked "correction" with message 4 linked. Message 4 changing under Dana fails.

18. **Two restarts for the same task (R11).**
    Setup: The same signed-in user (fake) has started two new chats in a row for the same Austin to Denver quote. Needs the session log.
    User: (opens a third chat) "moving quote austin to denver march 15"
    Expect: The bot offers a person or another channel and passes the latest details (2-bedroom, Austin to Denver, March 15). A third start from zero with no offer fails.

## Cannot be judged from a transcript alone
- **Edit controls and the version switcher (R1, R4).** Need a person using the window by touch and by keyboard.
- **Versions and the model request (R2, R7).** Need the message store and the request log.
- **Restarts (R11, test 18).** Need the session log across sessions for one user.
- **Thresholds.** None are set here beyond the pattern page's starting points.
- **Production rates.** These tests do not measure the share of sessions that restart after a single-message error. Use the metrics on the pattern page.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |
