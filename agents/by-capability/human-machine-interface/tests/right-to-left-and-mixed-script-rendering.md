# Test File: Right-to-Left and Mixed-Script Rendering

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs draws Arabic and Hebrew replies correctly: each message block takes its own direction, numbers and names stay in place, codes sit on their own left-to-right line, and stray direction characters do not change the layout.

> **Read this first.** These are test conversations only. This failure lives in the display layer, so almost every conversation needs the real chat UI and a screenshot or DOM check, not a transcript. Sample text below is limited to a few short, simple words (hello, thanks, and similar), marked "check with a native reader". Where a longer Arabic or Hebrew message is needed, the file describes it by script and meaning, and a native reader should write and review the real text before the first release. All stores, orders, and codes are invented (fake).

**Pattern:** [Chatbot Arabic or Hebrew Text Shows Backwards or Left-Aligned: Right-to-Left and Mixed-Script Rendering](../goals/language-and-locale/failures/right-to-left-and-mixed-script-rendering.md)
**Pattern ID:** right-to-left-and-mixed-script-rendering
**Goal:** Text displays correctly in every supported script. (Family goal, from the pattern page.)
**Primary metric:** RTL render-test pass rate. Starting target on the pattern page: 100% (a starting point to tune on your own data).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. Text chat only; voice is PLANNED, not written. Every conversation carries the Pattern ID above; the R-lines say which rule or Moves row it checks.

**Shared setup.** Maple & Co. (fake), a U.S. online retailer, runs a support chat. The customer, a fictional "Customer A" in Dearborn, Michigan, writes in Arabic or Hebrew or English as each conversation says. The chat renders markdown. Tracking numbers look like 1Z999AA10123456784 (an invented-format string). Orders are numbered like 4471 (fake).

**Sample words (check with a native reader).** Arabic: مرحبا (hello), شكرا (thanks). Hebrew: שלום (hello), תודה (thanks). Longer Arabic or Hebrew sentences are described by meaning below, not written out.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Set direction per block, not for the whole chat | An Arabic or Hebrew paragraph, list item, heading, or table cell is right-aligned, with bullet or list number on the right; an English block in the same reply stays left-aligned | Any right-to-left block drawn left-aligned, or one fixed direction for the whole panel |
| R2 | 2. Isolate embedded opposite-direction text | A number, amount, name, or product name inside a sentence of the other direction stays in place; the colon and period stay with the words they follow | Number or punctuation lands beside the wrong word |
| R3 | 3. Code, URLs, commands, and IDs on a left-to-right line | The value reads left to right, is selectable, does not split a sentence, and copies intact | The value is in the middle of a right-to-left sentence, reversed, or split |
| R4 | 4. Markup, not hidden direction characters; strip stray ones | A message with an unpaired direction character shows it removed or visible, and the neighboring layout is unchanged. The model is not asked to insert such characters | Layout of the rest of the message changes, or the model output carries hand-placed direction characters |
| R5 | 5. Keep stored text in logical order | The stored text and the text sent to the model equal what the user typed, character for character | The string was reversed or altered to look right |
| R6 | 6. Keep direction when text leaves the window | Pasted into a plain-text note and a document, the order of words and numbers matches the chat | Order differs after copy, share, or export |
| R7 | 7. Test every supported right-to-left script on each release | Not judged from a transcript. It needs the release process and the pass-rate report | Not judged here |
| R8 | Moves row: Admit uncertainty and show how to check | When the user says text looks scrambled, the bot says it cannot see its own display, restates the key values on separate lines, and says where they are | The bot claims it looks fine, or says nothing about not seeing the screen |
| R9 | Moves row: Offer choices (2-4 plus "Something else", free text open) | After a "looks wrong" report, 2-4 options such as resend on separate lines, send as plain text, talk to a person, plus "Something else" | A single forced fix, or no way to say something else |
| R10 | Hand-off rule | On the second "looks wrong" report, the bot offers a person, logs the message ID, and attaches the stored text; no fix date is promised | A third resend with no person offered, or "this will be fixed next week" |
| R11 | Don't over-correct | A mostly-English or English-only reply stays left-aligned with no isolates added; whole chat is not forced right-to-left because the user writes Arabic; code, URLs, and numbers are not reversed by hand; digit style is not changed | Left-to-right messages shown right-to-left, every word isolated, or digits converted unasked |

## Conversations
1. **Reply entirely in Arabic with a three-item numbered list (R1).**
   Setup: Maple & Co. chat. The user writes in Arabic. The bot's reply is a short Arabic opening line and a three-item numbered list of return steps. (A native reader supplies the real text.)
   User: Starts with مرحبا, then asks, in Arabic, how to return a jacket.
   Expect: Screenshot or DOM: every block is right-aligned; list numbers and bullets sit on the right. A left-aligned reply, or numbers on the left, fails.

2. **Arabic sentence with an order number and a dollar amount (R2).**
   Setup: Same. The bot's Arabic reply states that order 4471 will be refunded $39.99.
   User: Asks in Arabic where the refund for order 4471 is.
   Expect: Order number 4471 and the amount stay together and in place; the period and colon stay with the Arabic words they follow. A number or the "$" jumping to the other end of the sentence fails.

3. **Hebrew sentence ending with an English product name and "!" (R1, R2).**
   Setup: Same. The bot's Hebrew reply (a native reader supplies the sentence) ends with the English product name "Maple Pro" and an exclamation mark.
   User: Starts with שלום, then asks in Hebrew about the Maple Pro warranty.
   Expect: The block is right-aligned and the "!" sits at the end side of the sentence, not beside the first word. A "!" at the wrong edge fails.

4. **Tracking number inside an Arabic reply (R3).**
   Setup: Same. The reply is Arabic text plus the 20-character tracking number 1Z999AA10123456784.
   User: Asks in Arabic where the package is.
   Expect: The number is on its own left-to-right line or code span, in order, and copies intact (select it and paste to check). A number in the middle of an Arabic sentence, reversed, or split across two lines fails.

5. **Unterminated override character in the user's message (R4).**
   Setup: Same. The tester types a short Arabic message and inserts an unpaired U+202E (right-to-left override) before a number. Insert it by hand in the test harness.
   User: (sends the message with the stray character)
   Expect: The character is removed or shown visibly, and the words next to it keep their layout. If the whole message or the next message is reversed, it fails.

6. **Stored text equals typed text (R5).**
   Setup: Same. The tester types a short mixed message: the Arabic word شكرا, then a space, then order 4471, with no direction control characters.
   User: (sends it; then read the stored message and the text sent to the model)
   Expect: Stored text and model input match the typed text, character for character. Any reordered or reversed string fails. (Keep this separate from 5: here nothing is stripped, because nothing stray was typed.)

7. **Copy to a plain-text note (R6).**
   Setup: Same. Use the bot's reply from conversation 2.
   User: (copies the reply and pastes it into a plain-text note)
   Expect: Order of words and numbers, and the amount, match what the chat showed. A changed order fails.

8. **Copy to a document (R6).**
   Setup: Same. Use the reply from conversation 4 (with tracking number).
   User: (copies the reply into a word-processor document)
   Expect: The tracking number is in order and intact beside its label. A reversed or split number fails.

9. **Mixed reply: Arabic paragraph, English paragraph, Arabic list (R1).**
   Setup: Same. The bot's reply has an Arabic paragraph, one English sentence quoting the store's English return policy title, and an Arabic list.
   User: Asks in Arabic for the return policy.
   Expect: Arabic blocks right-aligned; the English sentence left-aligned in its own block. A single direction for the whole reply fails.

10. **User says the text looks scrambled (R8, R9).**
    Setup: Same. After the bot's reply with order 4471 and the $39.99 refund, the user writes in English, as a short typo-laden message.
    User: "the numbers r backwards on my phone"
    Expect: The bot says it cannot see how the message looks on the user's screen, restates order 4471 and $39.99 on separate lines, says where they are, and offers 2-4 choices (for example resend on separate lines, send as plain text, talk to a person) plus "Something else", free text open. "It looks fine on my end" fails. A single forced fix with no "Something else" fails.

11. **Second "looks wrong" report (R10).**
    Setup: Same as 10. The user got the separate-lines resend and the numbers still look wrong. A tracking number must be read to a carrier today.
    User: "still wrong. i cant read the number"
    Expect: The bot offers a person, passes along the message ID and the stored text, and promises no fix date. A third resend alone, or "should be fixed soon," fails.

12. **Do nothing special: English-only reply (R11).**
    Setup: Same. The user writes in English. The bot's reply is English with an order number.
    User: "where's order 4471"
    Expect: Left-aligned, no isolates or direction changes in the DOM. A right-to-left reply fails.

13. **Do nothing special: mostly English with one Arabic word (R11).**
    Setup: Same. The user writes in English and asks how to say "thanks" in Arabic. The bot replies in English and includes the word شكرا once.
    User: "how do u say thanks in arabic"
    Expect: The reply is a left-aligned English block; the single Arabic word is drawn correctly inline. The whole block drawn right-to-left, or the Arabic word wrapped in a heavy workaround, fails.

14. **Do nothing special: Arabic user, English-language request (R11).**
    Setup: Same. The user's phone is set to Arabic, but the user writes in English and asks for an English reply.
    User: "pls reply in english, my arabic is rusty"
    Expect: The English reply is left-aligned. The chat chrome (menus, buttons) may follow the UI language, but the message does not flip because of the user's language. A flipped English message fails.

15. **Do nothing special: digit style (R11).**
    Setup: Same. The user types an Arabic message that includes order 4471 in Arabic-Indic digits (the tester types them with the keyboard).
    User: (sends it)
    Expect: The reply shows the number in the style the data uses, with no unasked conversion; if the bot repeats the user's number, it uses the user's digits. A silent conversion to the other style fails.

16. **Code line the bot must not reverse (R3, R11).**
    Setup: Same. The user asks, in English, for the shell command the store's API doc gives to check a package: a one-line command with a URL.
    User: "what command checks a package"
    Expect: The command is in a left-to-right code block, exactly as stored, left-aligned. A command reversed, mirrored, or edited by hand to look right fails.

## Cannot be judged from a transcript alone
- **Everything about rendering.** Alignment, punctuation side, and number position need a screenshot or a DOM check (the pattern page's section 6 says so). A native Arabic or Hebrew reader should judge the first release.
- **R7, test each release.** Whether the section 6 cases run on every release and report a pass rate is a process check.
- **Primary metric.** The pass rate is a count over a test set; these are single cases.
- **Real text.** The pattern page's sample Arabic sentences are not reused here because I cannot verify them. Longer Arabic and Hebrew prompts must be written by a native reader. The words مرحبا, شكرا, שלום, and תודה: check with a native reader.
- **Other scripts.** Persian and Urdu are named on the pattern page as affected; no test here uses them. Add them with a native reader.
- **Voice.** PLANNED, not covered.

## Notes (rests on my reading, not the page's text)
- The page's section 6 gives eight scenarios. Conversations 1, 2, 3, 4, 5, 6, 7, and 12 follow them. The rest are my additions: 8 (second export target), 9 (mixed blocks, rule 1), 10 and 11 (the Moves rows and the hand-off rule), 13, 14, 15, and 16 (Don't over-correct).
- R8 and R9 rest on the Moves table rows, not on a numbered rule. R10 rests on the Hand-off rule. R11 rests on the Don't over-correct paragraph. R7 is a numbered rule but has no conversation.
- Conversations 5 and 6 are split on purpose: the page asks both that stray controls be removed (rule 4) and that stored text equal typed text (rule 5). I read rule 5 as applying to text with nothing stray in it. A reviewer should confirm that reading.
- Conversation 15 rests on one line in the reference design ("Do not convert digit style unless the user asks"). What to do when the bot repeats the user's digits is my reading.
- Conversation 16 follows rule 3 and the Don't over-correct line about code; the example command is invented.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |
