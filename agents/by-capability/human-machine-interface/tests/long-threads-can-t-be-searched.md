# Test File: Long Threads Can't Be Searched

This file is a set of chat test conversations for people who build or review chat assistants and want to check whether a person can find last week's answer in the chat history by what was said, by a title that names the topic, or from a pinned list.

**Pattern:** [Can't Find an Old Chat or Answer from Last Week: Long Threads Can't Be Searched](../goals/chat-interface/failures/long-threads-can-t-be-searched.md)
**Pattern ID:** long-threads-can-t-be-searched
**Goal:** The chat window itself works: messages arrive, drafts and attachments are kept, history is findable, and nothing is silently lost.
**Primary metric:** Time to find a past answer in a usability test. Starting point on the pattern page: median under 60 seconds, with at least 9 of 10 test participants finding it (not sourced, not measured).
**Maturity:** Tests written; not yet run.

These tests check whether a chat history shows the failure. They are not a score for any product. All products, accounts, chats, and people below are invented and labeled fake. Text chat only. Most of this pattern lives in the sidebar, the search index, and the title generator, so many items are marked "Needs a person": someone has to search, pin, rename, and look. Items 17 to 19 test what the bot says when asked to find an earlier chat, and only apply to products where the bot can look up past chats; those can be judged from the transcript.

The fake product used throughout: "Pinecrest Assistant (fake)". The seeded test account (fake) has 200 chats, as on the pattern page's metrics table, including one titled "Roll over old Fidelity 401(k) to IRA" that contains the line "ask for a direct rollover so no 20% is withheld", a project named "Denver move" with its own chats, and some archived chats.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Search covers titles and message text | One search box in the history finds a word that appears only in a message; each result shows the chat title, date, and the matching line. Needs a person | Title-only search, no search box, or results with no matching line |
| R2 | 2. Say what search does not cover | When nothing matches, the screen names the scope not searched (another project, archived, past a retention window) and links to it. Needs a person | A bare "No results" |
| R3 | 3. Titles name the topic, not the category | The title is generated after a few turns, again if the topic changes, and the user can rename it in one step. Needs a person | "Finance question" style titles, a title fixed from the first message, or a rename that takes more than one step |
| R4 | 4. Pinning on every chat | Any chat can be pinned in no more than two taps, and it sits at the top of the list and stays there. Needs a person | No pin, more than two taps, or a pinned chat that moves or is lost on reload or another device |
| R5 | 5. Search inside one long chat | In a thread longer than a screenful, a find-in-conversation control jumps to each match. Needs a person | No find control, or it misses matches |
| R6 | 6. Keep archived chats searchable, or say clearly when they are not | An archived chat is found by search, or the results say archived chats are not covered | An archived chat silently missing |
| R7 | 7. Don't make the user recall the date | A chat can be found without knowing when it happened; date grouping, if shown, is not the only way in. Needs a person | Scrolling by date is the only route |
| R8 | Don't over-correct | Titles do not flip on every turn, a title the user edited is never overwritten, there is no "pin this" prompt after every reply, and results are ranked with the top few shown and the rest one click away | Any of those broken |
| R9 | Hand-off rule | For a high-stakes thread (a support dispute, a medical or legal question) after two failed searches, the bot offers to email the full transcript or to connect a person who can retrieve it, and passes the search terms tried | Keeps suggesting new keywords, offers no other route, or the person has to repeat the search terms |
| R10 | Moves for the bot's own replies (section 5 Moves table) | One match: says which chat, gives the line, links it. Several matches: up to 3 by title and date plus "Something else". A scope the bot cannot search: says so and says where to look | A vague answer with no chat named, a long list, a choice menu when exactly one matches, or a guess when the scope is not searchable |

## Conversations
1. **Phrase only in a reply (R1).** Tag: long-threads-can-t-be-searched
   Setup: The seeded 200-chat account. The phrase "direct rollover" appears in a bot reply, not in any title.
   Action: Type "direct rollover" in the history search box.
   Expect: "Roll over old Fidelity 401(k) to IRA" appears. Needs a person. No result, or only title matches, fails.

2. **Result row shows the matching line (R1).** Tag: long-threads-can-t-be-searched
   Setup: Same search as item 1.
   Action: Read the result row.
   Expect: Title, date, and the line "...ask for a direct rollover so no 20% is withheld...". Needs a person. A title with no date or line fails.

3. **Term that exists only in a project (R2).** Tag: long-threads-can-t-be-searched
   Setup: The word "U-Haul" appears only in a chat inside the "Denver move" project.
   Action: Search "uhaul" from the main screen.
   Expect: If project chats are not covered, the empty screen says chats inside Projects were not searched and links to searching in the project. Needs a person. A bare "No results" fails.

4. **Chat past the retention window (R2).** Tag: long-threads-can-t-be-searched
   Setup: A workspace account (fake) with a retention window; the chat the user wants is older than it.
   Action: Search a word from that chat.
   Expect: The empty screen says older chats past the retention window are not available. Needs a person. A bare "No results" fails.

5. **Ten chats with the same opening line (R3).** Tag: long-threads-can-t-be-searched
   Setup: Ten new chats each start "I have a question about my account" and then go to different topics (a late fee, a new card, a mailing address change, and so on).
   Action: Read the titles after three turns.
   Expect: Each title names its topic, for example "Dispute late fee on October statement". Needs a person. Ten titles like "Account question" fail.

6. **Topic changes mid-chat (R3).** Tag: long-threads-can-t-be-searched
   Setup: A chat starts on a Chicago weekend itinerary, then spends most of its turns on renewing a US passport.
   Action: Read the title after the topic change.
   Expect: The title is regenerated to name the passport topic, or both. Needs a person. A title still reading "Chicago weekend ideas" fails.

7. **Rename in one step (R3).** Tag: long-threads-can-t-be-searched
   Setup: Any chat in the list.
   Action: Rename it to "Roth IRA limits".
   Expect: One action (for example a rename field on the title) changes it. Needs a person. A rename buried in several menus fails.

8. **User's rename survives a new topic (R3, R8).** Tag: long-threads-can-t-be-searched
   Setup: The user renamed a chat "Roth IRA limits", then keeps chatting about mortgage rates.
   Action: Read the title after several more turns.
   Expect: "Roth IRA limits" is kept. Needs a person. A system title over the user's rename fails.

9. **Pin, reload, open on a phone (R4).** Tag: long-threads-can-t-be-searched
   Setup: The seeded account.
   Action: Pin "Roll over old Fidelity 401(k) to IRA", reload the web page, then sign in on a phone.
   Expect: The chat is first in the list on both. Needs a person. A pin lost on reload or on the phone fails.

10. **Pin in two taps or fewer (R4).** Tag: long-threads-can-t-be-searched
    Setup: Any chat, on web and on the app.
    Action: Count the taps to pin it.
    Expect: Two or fewer on both. Needs a person. Three or more fails.

11. **Find a line in a 150-message thread (R5).** Tag: long-threads-can-t-be-searched
    Setup: A fake 150-message chat about planning a kitchen remodel in Raleigh; the word "permit" appears in four messages.
    Action: Use find-in-conversation for "permit".
    Expect: The control jumps to each of the four matches. Needs a person. No control, or fewer than four matches, fails.

12. **Archived chat (R6).** Tag: long-threads-can-t-be-searched
    Setup: The chat "Rollover paperwork checklist" (fake) is archived.
    Action: Search "1099-R".
    Expect: The archived chat appears, or the results say archived chats are not covered and how to search them. Needs a person. A silent miss fails.

13. **User knows the topic, not the date (R7).** Tag: long-threads-can-t-be-searched
    Setup: The seeded account. The participant is told only "find the chat about rolling over the old 401(k)".
    Action: Find it without being told when it happened.
    Expect: Search by topic gets there; the participant never has to scroll date groups. Needs a person. Date groups as the only route fail.

14. **Do nothing special: a new chat on a new topic (R8).** Tag: long-threads-can-t-be-searched
    Setup: No earlier chat is about pickleball.
    User: "whats a good pickleball paddle for a beginner"
    Expect: A normal answer. No "pin this chat" prompt and no "did you mean your earlier chat" line. Judge from the transcript. Either prompt fails.

15. **Do nothing special: short back-and-forth (R8).** Tag: long-threads-can-t-be-searched
    Setup: A five-turn chat on one topic (fixing a leaky faucet).
    Action: Watch the title and the replies across the five turns.
    Expect: The title settles once and does not change each turn, and no reply ends with a pin prompt. Needs a person. A title that flips every turn, or a pin prompt after each reply, fails.

16. **Many matches, ranked and short (R8).** Tag: long-threads-can-t-be-searched
    Setup: The seeded account has dozens of chats that mention "tax".
    Action: Search "tax".
    Expect: Results ranked by match with the top few shown and the rest one click away. Needs a person. One long unranked list fails.

17. **Bot finds one matching chat (R10).** Tag: long-threads-can-t-be-searched
    Setup: The product lets the bot look up past chats. Exactly one chat matches.
    User: "what did we decide about the rollover?"
    Expect: The bot names the chat "Roll over old Fidelity 401(k) to IRA", gives the line about the direct rollover, and links the chat, with no choice menu. Judge from the transcript.

18. **Bot finds several matching chats (R10).** Tag: long-threads-can-t-be-searched
    Setup: Same product. Three chats mention the rollover.
    User: "find my rollover chat"
    Expect: Up to 3 chats by title and date plus "Something else", with free text open. Judge from the transcript. Guessing one, or listing more than three, fails.

19. **Bot cannot search that scope (R10, R2).** Tag: long-threads-can-t-be-searched
    Setup: Same product. The bot's lookup does not cover the "Denver move" project.
    User: "what moving company did we pick in my denver move project"
    Expect: The bot says it cannot search inside that project from here and says to search inside the project. Judge from the transcript. A made-up company name fails.

20. **High-stakes thread, two searches failed (R9).** Tag: long-threads-can-t-be-searched
    Setup: A user is disputing a fake charge with "Pinecrest Mobile (fake)" and needs the support chat where an agent promised a refund. Two history searches ("refund", "pinecrest credit") found nothing.
    User: "i need that chat for my dispute and i cant find it anywhere"
    Expect: The bot offers to email the full transcript or to connect a person who can retrieve it, and passes "refund" and "pinecrest credit" along so the user does not repeat them. Judge the reply from the transcript; the hand-off record needs a person. A third "try other keywords" with no other route fails.

## Cannot be judged from a transcript alone
- **Most items (R1-R8).** Search, titles, pinning, and find-in-chat live in the client and the index. Needs a person working through the seeded account.
- **The primary metric.** Time to find a past answer comes from a moderated or unmoderated usability test with the seeded 200-chat account, timed from the first tap to opening the right chat. These conversations do not produce that number.
- **Thresholds.** Only the pattern page's starting points are used (60 seconds, 9 of 10, three turns, two taps, two searches). They are not researched values.
- **Production rates.** These tests do not measure searches with no results or re-asked questions. Use the metrics on the pattern page.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
