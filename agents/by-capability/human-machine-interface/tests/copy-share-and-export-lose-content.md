# Test File: Copy, Share, and Export Lose Content

This file is a set of chat test conversations for people who build or review chat windows and want to check whether a reply keeps its tables, code, and links when it is copied, shared, or exported, and whether the user is told what each one leaves out.

**Pattern:** [Chatbot Table or Code Broke When I Copied It: Copy, Share, and Export Lose Content](../goals/chat-interface/failures/copy-share-and-export-lose-content.md)
**Pattern ID:** copy-share-and-export-lose-content
**Goal:** The chat window itself works: messages arrive, drafts and attachments are kept, history is findable, and nothing is silently lost.
**Primary metric:** Export fidelity pass rate on a sample of reply types (table, code block, links, bold and lists). Starting target on the pattern page: 95% (a starting point to tune, not a measured benchmark).
**Maturity:** Tests written; not yet run.

These tests check whether a chat window shows the failure. They are not a score for any product. All products, trips, accounts, and people below are invented and labeled fake. Text chat only. Most of this pattern lives in the client (the clipboard, the share page, the export file), so many items are marked "Needs a person": someone has to paste into Word, Google Docs, an email draft, or a text editor and look. A few items test what the bot says in the chat, and those can be judged from the transcript.

The fake product used throughout: "Maple Assistant (fake)", a general chat assistant with Copy, Share, and Export controls. The fixture reply used in most items: a comparison of Delta and Southwest carry-on and checked-bag fees for an Austin to Denver trip, with a 3-column table, a short Python snippet with nested indentation that totals the fees, bold text, a bulleted list, and two cited fee-page links. The fee values in the table are fake.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Copy puts rich text and Markdown on the clipboard together | The Copy button and a manual selection both paste as a real table, monospace code with its indentation, and live links in Word, Google Docs, and email, and as clean Markdown in a plain-text field. Needs a person | Pipes and dashes where the table was, flat code, asterisks for bold, or the button and the selection paste differently |
| R2 | 2. Links survive | Each cited source pastes as a full URL or a live link. Needs a person | A source is missing, or an internal marker such as "【9†source】" appears |
| R3 | 3. Offer the formats people use | The copy menu offers formatted text, Markdown, and plain text; export offers at least one editable file (for example .docx or Markdown) that keeps tables and code. Needs a person | A format is missing, or the only export is a file that loses tables or code |
| R4 | 4. State what the export includes | One line beside Copy, Share, and Export says what is left out (for example "attached files are not included"). Needs a person | A control with no line, or a line that claims more than the output holds |
| R5 | 5. Share shows a preview and the audience | Before the link is created, the snapshot is shown with who can open it ("anyone with the link") and whether later messages are added. Needs a person | The link is created first, or the audience or later-message behavior is not stated |
| R6 | 6. Run a fidelity check on every client release | A check record exists for each fixture type (table, code block, cited links, bold and lists, a long reply) through each copy, share, and export action and each supported destination, for the release under test. Needs the release records | No record, a missing fixture type, action, or destination, or a release shipped with failed cells and no note |
| R7 | 7. If an element cannot be carried, say so at the moment of export | A dropped element (an image, an attachment, a table pasted as plain text) is named when it happens, with where to get the full version. Needs a person | The element is dropped with no message |
| R8 | Don't over-correct | No warning dialog on every copy, no format picker on a plain-text reply, the "includes" line sits next to the control (not a pop-up), the last chosen format is remembered, and a share or export holds only what the user selected | Any of those missing, or a share that pulls in attachments or later messages the sender did not choose |
| R9 | Hand-off rule | After the user says an export failed twice, the bot offers the content as a single Markdown block in the reply or as a file, does not claim it repaired the client, and the failed action and destination are logged for the product team | The bot repeats the same steps, claims a fix it cannot make, or nothing is logged |

## Conversations
1. **Copy button into three destinations (R1).** Tag: copy-share-and-export-lose-content
   Setup: The fixture reply is on screen.
   Action: Click Copy and paste into Word, Google Docs, and an email draft.
   Expect: A real 3-column table with the same rows and columns, bold as bold, and the list as a list in all three. Needs a person. Pipes and dashes in any one fails.

2. **Manual selection pastes the same as the button (R1).** Tag: copy-share-and-export-lose-content
   Setup: The fixture reply is on screen.
   Action: Select the whole reply with the mouse, copy, and paste into Google Docs next to the Copy-button paste from item 1.
   Expect: The two pastes match in structure. Needs a person. A table from one path and flat text from the other fails.

3. **Nested code indentation (R1).** Tag: copy-share-and-export-lose-content
   Setup: The fixture reply's Python snippet has a loop inside a function.
   Action: Copy and paste into a Word document and into a plain text editor.
   Expect: Indentation and line breaks match the source in both; the document shows it in a monospace block. Needs a person. Code flattened onto one line fails.

4. **Plain-text field gets clean Markdown (R1).** Tag: copy-share-and-export-lose-content
   Setup: The fixture reply. The destination is a plain-text support-ticket field in a fake help desk.
   Action: Click Copy and paste.
   Expect: Clean Markdown with the table as Markdown rows and the code fenced. Needs a person. Stray HTML tags fail.

5. **Cited sources survive copy (R2).** Tag: copy-share-and-export-lose-content
   Setup: The fixture reply cites two fee pages as source chips.
   Action: Click Copy and paste into an email draft.
   Expect: Both URLs are present and clickable. Needs a person. Marker text such as "【9†source】" or a missing URL fails.

6. **The copy and export menus (R3).** Tag: copy-share-and-export-lose-content
   Setup: The fixture reply.
   Action: Open the Copy menu, then the Export menu.
   Expect: Copy offers formatted text, Markdown, and plain text; Export offers at least one editable file (for example .docx or Markdown), and that file keeps the table and code when opened. Needs a person. A PDF-only export fails this line.

7. **User asks how to get it into Word (R3, Moves).** Tag: copy-share-and-export-lose-content
   Setup: The fixture reply was just shown.
   User: "how do i get this into word without it breaking"
   Expect: The bot offers 2 to 4 options plus "Something else" with free text open, for example "Copy as formatted text", "Copy as Markdown", "Download as .docx", "Something else". Judge from the transcript. A long how-to with no options, or a list of more than four, fails.

8. **User already named the format (R3, R8).** Tag: copy-share-and-export-lose-content
   Setup: The fixture reply was just shown.
   User: "give me that table as markdown"
   Expect: The bot gives the table as Markdown with no menu of formats. Judge from the transcript. Asking "Which format do you want?" fails.

9. **"What this includes" line on each control (R4).** Tag: copy-share-and-export-lose-content
   Setup: A chat with the fixture reply and one attached PDF (a fake boarding pass).
   Action: Open Copy, Share, and Export in turn.
   Expect: Each has one line next to it saying what is left out, for example "attached files are not included" or "messages sent after sharing stay private". The line matches what the output really holds. Needs a person. A control with no line fails.

10. **Share preview and audience before the link exists (R5).** Tag: copy-share-and-export-lose-content
    Setup: The same chat with the attached PDF.
    Action: Click Share.
    Expect: Before any link is created, the snapshot is shown, the audience is stated ("anyone with the link"), and the window says whether later messages are added. Needs a person. A link copied to the clipboard on the first click fails.

11. **Share holds only what was selected (R8).** Tag: copy-share-and-export-lose-content
    Setup: The user shares the chat, then sends two more messages, one with a fake home address in Columbus, Ohio.
    Action: Open the share link in a signed-out browser.
    Expect: The shared page shows only what the sender chose, and the two later messages are not there unless the sender shared again. Needs a person. The later message with the address on the shared page fails.

12. **Fidelity check records for a release (R6).** Tag: copy-share-and-export-lose-content
    Setup: The team's records for the client release under test.
    Action: Look for one check record per fixture type (table, code block, cited links, bold and lists, a long reply) through each copy, share, and export action and each destination the product supports.
    Expect: Every cell has a record with its checks and a result. Needs the release records. A missing fixture, action, or destination fails. These tests do not supply the fixture results; record only what the records show.

13. **Image in the reply on export (R7).** Tag: copy-share-and-export-lose-content
    Setup: A reply that contains a chart image of the fake fee totals.
    Action: Export as .docx, then as Markdown.
    Expect: Each export either keeps the image or states, at the moment of export, that it was left out and where to get it. Needs a person. An export with the image silently gone fails.

14. **Table copied as plain text (R7).** Tag: copy-share-and-export-lose-content
    Setup: The fixture reply.
    Action: Choose "Copy as plain text".
    Expect: A note at the copy says the table was copied as plain text and how to keep the columns (for example "download the .docx to keep columns"). Needs a person. No note fails.

15. **Do nothing special: copy a plain-text reply (R8).** Tag: copy-share-and-export-lose-content
    Setup: The bot answered "What time zone is Phoenix in?" with two plain sentences, no table, code, or links.
    Action: Click Copy and paste into a text field.
    Expect: One click copies clean text. No warning dialog, no format picker, no pop-up. Needs a person. Any dialog or forced format choice fails.

16. **Do nothing special: second copy remembers the format (R8).** Tag: copy-share-and-export-lose-content
    Setup: The user chose "Copy as Markdown" on an earlier reply in the same session.
    Action: Copy the fixture reply.
    Expect: The menu starts on Markdown, or one click copies as Markdown, and the "includes" line stays next to the control rather than popping up. Needs a person. A pop-up on each copy fails.

17. **Export failed twice (R9).** Tag: copy-share-and-export-lose-content
    Setup: The fixture reply. The user's .docx export has failed.
    User: "the word download broke the table again, tried it twice"
    Expect: The bot offers the content as one Markdown block in the reply or as a file, and the failed action and destination (.docx export) are logged for the product team. Judge the reply from the transcript; the log needs a person. Telling the user to try the same download a third time fails.

18. **User asks the bot to fix the copy button (R9).** Tag: copy-share-and-export-lose-content
    Setup: The fixture reply.
    User: "can u just fix the copy button so the links stay"
    Expect: The bot says it cannot change the copy button from inside the chat, gives the content with full URLs as a workaround, and does not claim the button is now fixed. Judge from the transcript. "Done, the copy button will keep links now" fails.

## Cannot be judged from a transcript alone
- **Almost everything here.** What reaches the clipboard, the share page, and the export file is decided by the client. Pasting into the real destinations needs a person, or a harness that reads the clipboard's rich-text and plain-text forms.
- **Release checks (R6).** Need the team's check records for the release under test.
- **Logging (R9).** Needs the product's event or feedback log.
- **Production rates.** These tests do not measure the export fidelity pass rate. Use the metrics on the pattern page. This file sets no thresholds beyond the starting target stated there.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
