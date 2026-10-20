# Test File: Link and Resource Dumps

This file is a set of chat test conversations for people who build or review help-center and search-style assistants and want to check whether theirs answers a question or just sends links.

**Pattern:** [Chatbot Just Sends Links Instead of Answering: Link and Resource Dumps](../goals/response-structure/failures/link-and-resource-dumps.md)
**Pattern ID:** link-and-resource-dumps
**Goal:** Replies are shaped so people can read, act on, and answer them. For this pattern: answer first, with links as support.
**Primary metric:** Share of replies that are mostly links (a link-only or link-led reply with no answer in the first two sentences). Target on the pattern page: under 2% (tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. The company Northfield Internet (fake), its help-center pages, and all fees are invented. In each setup, give the assistant the retrieved pages as written, because the tests depend on what the pages say. Text chat only.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Answer in sentence one | Sentence one holds the answer or next step | Opens with "Here are some resources" or a list of links |
| R2 | 2. Never send a link-only reply | States what the retrieved page says about the user's case, in the reply text | Only links, or links with a generic line like "this may help" |
| R3 | 3. Cap links at one to three, each labeled | At most three links, each says what the user will find | More than three, or bare titles or URLs |
| R4 | 4. Name the one link that matters most | Says which link covers the user's case | Several links with no ranking |
| R5 | 5. When no page answers it, say so in sentence one | "I couldn't find a policy for that", then a person or one question; no list of near-misses | Lists near-miss articles to look helpful |
| R6 | 6. When the question is unclear, ask one question | One clarifying question | A link for each possible meaning |
| R7 | 7. Keep links as support | Deadlines, fees, and required steps are in the reply text | A must-know fact appears only behind a link |
| R8 | Don't over-correct | Gives a link when a link is the answer; keeps a source link; gives the part that applies, not the whole page | Refuses to link, pastes a whole page, or states a policy the pages do not support |

## Conversations
1. **Answer on one page (R1).**
   Setup: Northfield Internet (fake) help bot. Retrieved page "Refund policy": duplicate charges are refunded in full, usually in 5-7 business days.
   User: "i was charged twice for march can i get one back"
   Expect: Sentence one says yes, a duplicate charge is refunded. "I found some resources that may help" as the opener fails.

2. **Not link-only (R2).**
   Setup: Same bot. Retrieved page "Find your invoice": sign in, open Billing, choose Invoices, pick the month.
   User: "where do i find my invoice"
   Expect: The steps are written in the reply, with the link after. A reply that is only the link fails.

3. **Five articles match (R3).**
   Setup: Same bot. Five pages are retrieved on "router problems" (setup, reset, lights, Wi-Fi name, firmware).
   User: "router keeps dropping"
   Expect: At most three links, each labeled by content ("Router lights, what the red light means"). Five links or bare titles fails.

4. **Name the one that matters (R4).**
   Setup: Same bot. Same five pages. The user's message says the router shows a red light.
   User: "router has a red light and no internet"
   Expect: Says which page covers the red light and what it says. Five equal links fails.

5. **No page answers (R5).**
   Setup: Same bot. Retrieval returns only near-misses: "Payment methods" and "Billing overview", neither mentions gift cards.
   User: "can i pay my bill with a gift card"
   Expect: Sentence one says the bot couldn't find a policy on that, then offers a person or one question. Listing the two near-misses as "resources" fails.

6. **Unclear question (R6).**
   Setup: Same bot. Pages exist for "Cancel service", "Cancel a technician visit", and "Cancel a late fee". No order context.
   User: "how do i cancel"
   Expect: One question: what does the user want to cancel. Three links, one per meaning, fails.

7. **Deadline behind a link (R7).**
   Setup: Same bot. Retrieved page "Return the modem": return within 30 days of canceling; a $15 fee applies after that.
   User: "i canceled yesterday, what do i do with the modem"
   Expect: The 30 days and the $15 fee are in the reply text. "See the Return the modem page" alone fails.

8. **Do nothing special: the user asks for a link (R8).**
   Setup: Same bot. Page "Moving form" holds the form.
   User: "can u send me the moving form"
   Expect: The link, with a short label. Refusing to link and typing out the form fails.

9. **Do nothing special: answer plus one source link (R8).**
   Setup: Same bot. Retrieved page "Refund policy" as in conversation 1.
   User: "ok and how long does the refund take"
   Expect: The answer first (usually 5-7 business days), then one labeled source link. Dropping the link altogether fails.

10. **Do nothing special: pages are silent, do not guess (R8).**
    Setup: Same bot. Pages say nothing about refunds to a new card.
    User: "will the refund go to my new card"
    Expect: Says the pages do not say, gives the one best link, and says what to look for or offers a person. Stating "yes, to the new card" fails.

11. **Do nothing special: long page, short answer (R8).**
    Setup: Same bot. The retrieved page "Outage credits" runs eight paragraphs; only one paragraph applies to a 4-hour outage.
    User: "i lost internet for 4 hours, do i get a credit"
    Expect: Gives the applicable rule in a few sentences. Pasting the full page fails.

12. **Asked "which one?" twice (R5).**
    Setup: Same bot. The bot has sent a link list; the user asked "which one?" and got links again.
    User turn 1: "which one"
    User turn 2: "so what do i do"
    Expect: After the second ask, hands off to a person and passes along the question and pages tried. A third link list fails. (Maps to R5 and the page's hand-off rule; see the note below.)

## Cannot be judged from a transcript alone
- **Link click events.** Two detection signals use click data, which a transcript lacks.
- **Rate.** The primary metric (under 2%) is measured over real replies, not in one run.
- **Conversation 12.** The page states the "twice" hand-off in the hand-off rule, not as a numbered fix rule. It is mapped to R5; a reviewer should confirm the mapping.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | |
