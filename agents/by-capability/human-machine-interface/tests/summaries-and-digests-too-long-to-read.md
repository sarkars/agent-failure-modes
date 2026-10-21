# Test File: AI Daily Summary Longer Than the Email: Summaries and Digests Too Long to Read

This file is a set of chat test conversations for people who build or review a text assistant that sends scheduled or event-based summaries, and want to check whether its digests lead with what needs action, stay shorter than their source, and make the rest optional.

**Pattern:** [Summaries and Digests Too Long to Read](../goals/proactive-and-ambient/failures/summaries-and-digests-too-long-to-read.md)
**Pattern ID:** summaries-and-digests-too-long-to-read
**Goal:** Proactive and always-listening agents speak up only when invited or useful, and respect a no.
**Primary metric:** Digest open rate and action rate (share of digests where the user opens it, and share where the user acts on a flagged item). Starting target: set from your baseline, then aim to rise (tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and amounts below are invented. Text chat only. The setup holds what the harness shows the agent: the user's digest settings, the source items with their due times and word counts, and earlier turns. Email, push and voice digests are planned and are not covered.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Actions first | The first lines list only items that need the user to act, each with the deadline and the person, or say "Nothing needs you today." | Routine items come first, or an action item sits in the middle |
| R2 | 2. Count what you left out | The digest states how many items were skipped and that none need action | No skipped count, or a count that hides an item with a deadline |
| R3 | 3. Cap the list | Items shown stay at or under the cap (the setup states it; the page suggests starting at 3) unless the user asked for more | More items shown than the cap, with no request from the user |
| R4 | 4. Shorter than the source | The digest has fewer words than the items it covers | The digest is as long as or longer than its source |
| R5 | 5. Make the rest optional | Choices offered: "Show a short list", "Skip today", "Change how often", "Something else", with free text open; no long version sent by default | The long version is sent by default, or no way to skip or ask for the rest |
| R6 | 6. Don't hold urgent items for the digest | An item due before the next digest goes out as its own message when the user allowed that kind of message, and is not left inside the digest | The urgent item waits for the digest, or is sent when the user did not allow it |
| R7 | 7. Say nothing when nothing needs the user | One line, or no send if the user chose quiet days | A full digest of routine items on a day with no action |
| R8 | 8. Let the user shape it | One tap or one sentence changes frequency, length or stops the digest; a "no" is kept | The change is ignored, takes several steps, or the digest comes back |
| R9 | Hand-off rule: the user says the digest is wrong or missed something important | The digest stops, one apology, and an offer to review what was left out or reach a person who owns the product | The bot keeps sending, or argues that the digest was complete |
| R10 | Don't over-correct | No action item dropped to save words; the skipped count is shown; the digest is more than "You have messages."; the rest can still be opened | An item that needs action is cut, the count is hidden, or the digest says nothing useful |

## Conversations
1. **Two actions among thirty-one items (R1, R2, R4).**
   Setup: Fake company "Brightwell Logistics" (fake). The 7:00 AM digest is due. Source: 31 emails and updates. Two need the user: Dana Whitfield's vendor contract needs a signature by 5 PM today, and Priya Raman's time-off request needs approval before she leaves Friday. The other 29 are newsletters, status changes and reminders. Cap is 3. The source is about 1,900 words.
   User: (no message; the scheduled digest is generated)
   Expect: The two actions come first, each with the deadline and the person. Then one line says 29 other items need nothing from you. The digest is well under 1,900 words. Choices follow.
   Failing reply: "Good morning! Here is your daily summary. You received 31 emails yesterday. Marketing sent 6 newsletters about the fall webinar series..." with the contract mentioned in the middle.

2. **Twelve items need action, cap is 3 (R3, R5).**
   Setup: Same company. Twelve items need the user, each with a due date this week. Cap is 3. Items are ordered by due time.
   User: (scheduled digest)
   Expect: The 3 items with the nearest deadlines, a line that 9 more need you, and a choice to show a short list. The digest does not list all 12.
   Failing reply: A numbered list of all 12 items, each with a paragraph of context.

3. **Three short items (R4).**
   Setup: Same company. Source: three one-line Slack posts, 40 words in total. None need action.
   User: (scheduled digest)
   Expect: One short line or a short note under 40 words, with the skipped count. Not a restated version of each post.
   Failing reply: A greeting, a heading, three bullets that repeat each post, and a closing offer, totaling more than 40 words.

4. **Nothing needs action, user chose quiet days (R7).**
   Setup: Same company. User settings: "send nothing on days with no action." Source: 18 routine items. None need the user.
   User: (scheduled digest)
   Expect: No send. The harness logs no digest for the day.
   Failing reply: "Good morning! Nothing needs you today, but here are 18 updates..." sent anyway.

5. **Nothing needs action, user did not choose quiet days (R7, R1).**
   Setup: Same company. User settings: send every day. Source: 18 routine items. None need the user.
   User: (scheduled digest)
   Expect: One line: "Nothing needs you today." It may add that 18 other items need nothing, with the choices.
   Failing reply: A list of the 18 items with no mention that none need action.

6. **Item due in 2 hours, digest in 10 hours (R6).**
   Setup: Same company. The user allowed urgent messages. At 8:00 AM an item appears: Tom Okafor needs a yes or no on a shipping quote by 10:00 AM. The next digest is due at 6:00 PM.
   User: (no message; the event arrives)
   Expect: A separate message at 8:00 AM that names the item, the person and the deadline. It is not saved for the 6:00 PM digest.
   Failing reply: Silence until 6:00 PM, then the item appears at position 5 of the digest, after the deadline.

7. **Item due soon, user did not allow urgent messages (R6, R8).**
   Setup: Same company. The user's settings allow only the daily digest, no separate messages. An item is due in 2 hours. The digest is due in 10 hours.
   User: (no message; the event arrives)
   Expect: No separate message. The item is held for the next digest, where it sits first with its deadline.
   Failing reply: A push-style message sent anyway, against the setting.

8. **User picks "Skip today" (R5, R8).**
   Setup: Same company. The digest has just been sent with choices.
   User: "Skip today."
   Expect: A short acknowledgment. No long version follows. Tomorrow's digest still sends on schedule.
   Failing reply: "Here is the full list anyway so you don't miss anything..." followed by 29 items.

9. **User picks "Show a short list" (R5, R3, R10).**
   Setup: Same company. The digest listed 2 actions and said 29 other items need nothing. Cap is 3.
   User: "Show a short list."
   Expect: A list of up to 3 of the other items, with a line that 26 remain and can be opened. The two actions are not repeated as new news.
   Failing reply: All 29 items dumped at once.

10. **User asks to change how often (R8).**
    Setup: Same company. The digest is sent daily.
    User: "Make this weekly."
    Expect: One reply that confirms weekly, with the day and time. No further question about why, and no menu.
    Failing reply: A list of five frequency options and a request to fill in a form.

11. **User says stop (R8).**
    Setup: Same company. The digest was sent this morning.
    User: "stop the digest"
    Expect: It stops, confirms in one line, and tells the user how to turn it back on. The next scheduled time passes with no send.
    Failing reply: "Are you sure? You'll miss important updates!" followed by a digest the next day.

12. **Digest missed something important (R9).**
    Setup: Same company. This morning's digest counted 28 other items as needing nothing. One of them was a contract renewal notice from Marlow Office Supply due today.
    User: "Your digest missed the Marlow renewal. This is useless."
    Expect: The digest pauses. One apology. An offer to review what was left out and to reach a person who owns the product. No further digests until the user decides.
    Failing reply: "Our digest includes the most important items. The Marlow notice was low priority." Or a new digest the next morning.

13. **Shortening must not drop an action item (R10, R1).**
    Setup: Same company. Source: 40 items. Four need the user: two due today, two due Friday. Cap is 3. The source is about 2,400 words.
    User: (scheduled digest)
    Expect: The three nearest items listed with deadlines, a line that one more needs you (with a way to see it), and a count of the other 36 items that need nothing. The fourth action item is not folded into "nothing needed."
    Failing reply: Three action items listed, and "37 other items need nothing from you," which hides the fourth action item.

14. **Digest that says too little (R10).**
    Setup: Same company. Source: 25 items. One needs the user: sign a form by Thursday.
    User: (scheduled digest)
    Expect: The form, the deadline and the person who sent it, then the skipped count and the choices. Short, and still useful.
    Failing reply: "You have messages."

## Cannot be judged from a transcript alone
- **Digest open rate and action rate.** They need real sends and open events over time. Fourteen conversations do not measure them.
- **Word-count comparison at scale.** It needs a check of digest length against source length on every send in logs.
- **Items missed.** It needs a sampled review of deadline items left in the skipped count, across many days.
- **Unsubscribes and "stop" after a digest.** They need opt-out events compared with a baseline.
- **Whether the cap of 3 is the right number.** It is a starting point to tune on your own data.
- **Email, push, voice and web digests.** Not covered; this file is text chat only. Those signals are planned, never measured.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
