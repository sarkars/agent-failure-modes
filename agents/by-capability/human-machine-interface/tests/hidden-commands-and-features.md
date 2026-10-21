# Test File: Hidden Commands and Features

This file is a set of chat test conversations for people who build or review chat assistants and want to check whether theirs names a faster feature at the right moment, or keeps it hidden in a menu.

**Pattern:** [Chatbot Feature Discoverability: Slash Commands and Features Users Never Find](../goals/onboarding-and-discoverability/failures/hidden-commands-and-features.md)
**Pattern ID:** hidden-commands-and-features
**Goal:** People know what the assistant can do and how to start, without needing to guess or to engineer prompts.
**Primary metric:** Share of active users who used a given feature, tracked per feature. Starting target on the pattern page: set from your own baseline, then track the lift after hints ship.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, users, receipts, and amounts below are invented and labeled fake. Text chat only. The setup in each conversation states the feature map, the user's history, and the plan, because the hint depends on them. Items marked "Needs a person" need the feature map, the event log, or the interface, not just a transcript.

The fake product used throughout: "Ledgerly (fake)", a bookkeeping assistant for small businesses. Features in its map: `/import` (log many expenses from a CSV or card statement; trigger: 3 manual entries in a session; button "Import a file"), `/template` (saved recurring entries; Pro plan only), and `/export` (monthly report).

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Keep a feature map | Each hinted feature has what it does, the exact command and button, and a trigger. Needs a person (read the map) | A hint for a feature missing from the map, or a map entry with no trigger |
| R2 | 2. Do the task first | The requested action or answer comes first; the hint follows in the same reply | The hint replaces or delays the task |
| R3 | 3. Hint only on a trigger | A hint appears only after the mapped trigger fires | A tip at the start of a chat, at login, or with no trigger |
| R4 | 4. One hint per reply, one line | One line that says what it does and how to call it; one feature per reply; at most two unrequested hints per session (starting cap, tune) | Two features in one reply, a multi-line pitch, or a third unrequested hint in a session |
| R5 | 5. Never hint a used or dismissed feature | No hint for a feature used in the last 90 days or one the user dismissed | A repeat of a used or dismissed hint |
| R6 | 6. Only features that exist and are on for this user | Not hinted, or hinted with the plan requirement stated plainly | A hint for a feature that is off on the user's plan, with no plan note |
| R7 | 7. Accept plain words | "import my card statement" works like `/import` | The command is the only way in |
| R8 | 8. Keep the full list findable | "/" (anywhere in the message) lists commands with one-line descriptions and arguments; "what can you do here?" answers from the feature map | No list, or a list with no descriptions |
| R9 | Don't over-correct: no tip on every reply, no stacking, no upsell, keep the slow way working | After "Keep going here" the bot keeps doing the task one by one without comment; no hint when nothing is left to speed up | A tip on every reply, two stacked tips, a sales pitch, or refusing the slow way |
| R10 | Hand-off rule | If the feature fails twice or the user cannot find the setting, a person is offered with the feature name, the error, and what was tried | Keeps suggesting the feature, or offers a person with none of that passed on |

## Conversations
1. **Third manual entry (R1, R2, R3).** [hidden-commands-and-features]
   Setup: Two manual entries already logged this session (fake). `/import` never used.
   User: "Log $88.00, Ferguson, 10/15, job supplies"
   Expect: The entry is logged first, then one line naming `/import` with an "Import a file" button. A hint before the entry fails.
2. **Hint is one line with command and button (R4).** [hidden-commands-and-features]
   Setup: Same trigger as 1.
   User: "log 16.50 shell 10/15 fuel"
   Expect: One line: what it does, the `/import` command, a button, and a way to ignore it. A paragraph on all features fails.
3. **No trigger, first message (R3).** [hidden-commands-and-features]
   Setup: New chat, no actions yet.
   User: "hey"
   Expect: A normal greeting and no feature tip. A tip about `/import` fails.
4. **Two triggers fire at once (R4).** [hidden-commands-and-features]
   Setup: The `/import` trigger and the `/export` trigger (fake: user asked for the same report three times) fire on the same reply.
   User: "log $42.18 Home Depot 10/14 supplies"
   Expect: The entry is logged and only one feature is mentioned. Two features in one reply fail.
5. **Feature used recently (R5).** [hidden-commands-and-features]
   Setup: The user ran `/import` 20 days ago. Three manual entries this session.
   User: "log $9.99 Staples 10/15 office"
   Expect: Entry logged, no `/import` hint. Needs a person (read the usage history).
6. **Dismissed hint stays quiet (R5, R9).** [hidden-commands-and-features]
   Setup: The user chose "Keep going here" earlier this session.
   User: "log $31.00 Lowes 10/15 supplies"
   Expect: Entry logged, no repeat hint. A second hint fails.
7. **Plan does not include the feature (R6).** [hidden-commands-and-features]
   Setup: Free plan. `/template` is Pro only. The user logs the same $1,200 rent entry (fake) for the third month in a row.
   User: "log $1200 rent 10/01"
   Expect: No `/template` hint, or a hint that states plainly it needs Pro. A hint that implies it works on Free fails.
8. **Plain words work like the command (R7).** [hidden-commands-and-features]
   Setup: `/import` is enabled for the user.
   User: "can i import my card statment"
   Expect: Same result as `/import`: it asks for the file and says it will show the rows before saving. "Please use /import" fails.
9. **Slash typed mid-message (R8).** [hidden-commands-and-features]
   Setup: Feature map has three commands.
   User: "I need to do a thing / "
   Expect: A list of commands with one-line descriptions and arguments. Needs a person (interface check). A bare list of names fails.
10. **"what can you do here?" (R8).** [hidden-commands-and-features]
    Setup: Mid-session, no trigger.
    User: "what can u do here"
    Expect: An answer built from the feature map. A tip is allowed here since the user asked. A generic "I can help with many things" fails.
11. **"Is there a faster way?" (R8, R7).** [hidden-commands-and-features]
    Setup: User has logged two entries by hand.
    User: "is there a faster way to do this"
    Expect: Names `/import` and how to call it, in one or two lines. "No" fails.
12. **Do nothing special: one-off entry (R3, R9).** [hidden-commands-and-features]
    Setup: New chat. The user logs one entry and says that is all.
    User: "log $14.00 parking 10/15. thats it"
    Expect: Entry logged, a short close, and no tip. A tip about `/import` fails.
13. **Do nothing special: user in a hurry (R9).** [hidden-commands-and-features]
    Setup: Third manual entry, but the user writes "quick, closing in 5 min".
    User: "log 55 fuel 10/15 quick"
    Expect: Entry logged with no hint, since the page says not to offer choices to a user in a hurry. A hint fails.
14. **Do nothing special: keep going (R9).** [hidden-commands-and-features]
    Setup: The user just tapped "Keep going here".
    User: "log $22 lunch 10/16 client"
    Expect: Logged one by one without comment. A reminder fails.
15. **Hint every reply (R9, R4).** [hidden-commands-and-features]
    Setup: Five manual entries in a row, hint already shown once and ignored (not dismissed).
    User: five more entries, one at a time
    Expect: No more than two unrequested hints in the whole session (starting cap, tune). A hint on every reply fails.
16. **Hint becomes an upsell (R9, R6).** [hidden-commands-and-features]
    Setup: Free plan, trigger fires for `/import` (available on Free).
    User: "log $70 Ferguson 10/16 supplies"
    Expect: Entry logged and an `/import` hint. No mention of upgrading. A "Go Pro for more" line fails.
17. **Feature fails twice (R10).** [hidden-commands-and-features]
    Setup: `/import` returned "file not read" twice for a fake file card_oct.csv.
    User: "its still not working"
    Expect: Offers a person and passes the feature name, the error, and what was tried. Offering `/import` again fails.

## Cannot be judged from a transcript alone
- **Feature map and eligibility (R1, R5, R6).** Needs the map, the plan, and the usage and dismissal history.
- **Session counts (R4).** Counting hints per session needs the event log.
- **Layout (R8).** The "/" list in the composer needs the interface.
- **Production rates.** These tests do not measure feature use. Use the metrics on the pattern page. Thresholds taken from the page: 0 hints on used or dismissed features; 2 or fewer unrequested hints per session. Everything else: record the product's own setting.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
