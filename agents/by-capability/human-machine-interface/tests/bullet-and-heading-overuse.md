# Test File: Bullet and Heading Overuse

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs breaks explanations into headers and short bullets, and whether fixing that goes too far.

**Pattern:** [Chatbot Responses Use Too Many Bullet Points and Headers: Bullet and Heading Overuse](../goals/response-structure/failures/bullet-and-heading-overuse.md)
**Pattern ID:** bullet-and-heading-overuse
**Goal:** Replies are shaped so people can read, act on, and answer them. For this pattern: structure serves the content.
**Primary metric:** Judge rating of coherence by format, paired with the fragmentation rate (share of reasoning replies built from headers and bullets under 15 words). Target on the pattern page: coherence 4 or 5 of 5 on over 90% of sampled reasoning replies; fragmentation under 10% (tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All people, dogs, and accounts are invented. Text chat only. The 250-word line in R2 and the 4-word line in R4 are the page's starting points to tune. Run these in a window that shows raw markdown, or compare the displayed text with the model output.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Reasoning questions get connected sentences | Why, should-I, and explain questions are answered in sentences with connectors (because, so, unless, but) | A reply made only of bullets, or ideas with no connectors |
| R2 | 2. No headers in a reply of 250 words or fewer | Header count is 0 | Any header in a short reply |
| R3 | 3. Bullets only for 3 or more parallel, independent items | A list is used for list-shaped content, and items can be reordered without changing meaning | A list of dependent ideas, or fewer than 3 items |
| R4 | 4. Every bullet is a full thought, or the whole list is plain short items | No bare fragment bullet (under 4 words) in a reasoning reply | Bullets like "Liquidity" with no point |
| R5 | 5. A one-sentence takeaway in prose before any list | Sentence one is prose and answers | Sentence one is a header or a bullet |
| R6 | 6. Casual, emotional, or advice chats get no formatting | Zero bullets, headers, or bold | Any of them |
| R7 | 7. Do what the user asks | A request for a list, a table, or "no bullets" holds for the rest of the conversation | Reverts to the old format on the next reply |
| R8 | Don't over-correct | Lists, numbered steps, and headers are kept where the content needs them; paragraphs stay short | List-shaped content forced into paragraphs, or one long block |

## Conversations
1. **Reasoning question (R1).**
   Setup: General assistant, no format instruction.
   User: "should i pay off my car loan early or put the money in savings"
   Expect: Conditional answer in connected sentences (higher rate on the loan, so pay it off; thin cushion, so save first) and a question for the missing facts. A header plus fragment bullets fails.

2. **Short answer, no headers (R2).**
   Setup: Same assistant. The right answer is about 100 words.
   User: "why are my pothos leaves turning yellow"
   Expect: Zero headers. Any "## Causes" header fails.

3. **List-shaped request (R3).**
   Setup: Same assistant.
   User: "list the documents i need for a passport renewal"
   Expect: A one-sentence answer, then a bullet list of parallel items. Items can be reordered. Cramming them into one paragraph fails.

4. **No bare fragments (R4).**
   Setup: Same assistant. The user is weighing a purchase.
   User: "is it worth switching from a gas stove to induction"
   Expect: No bullet under 4 words. "Cost" or "Speed" as a lone bullet fails.

5. **Takeaway first (R5).**
   Setup: Same assistant. Three fake phone plans: Plan A, Plan B, Plan C, with different prices.
   User: "help me choose between plan a b and c"
   Expect: Sentence one is a prose takeaway or the one question needed. A list may follow. A reply that opens with a header or a bullet fails.

6. **Emotional message (R6).**
   Setup: Same assistant.
   User: "my dog died this morning"
   Expect: Plain sentences only. No bullets, headers, or bold, and no list of coping tips.

7. **Format request holds (R7).**
   Setup: Same assistant.
   User turn 1: "no bullets please. why does bread dough need to rest"
   User turn 2: "ok and why does it need salt"
   Expect: Both replies are prose. Turn 2 returning to bullets fails.

8. **Table request (R7).**
   Setup: Same assistant.
   User: "make a table of the 3 phone plans, price and data"
   Expect: A table. Replying in paragraphs fails.

9. **Do nothing special: ingredient list (R8).**
   Setup: Same assistant.
   User: "what do i need for pancakes"
   Expect: A short list of ingredients is fine, after a one-line answer. Forcing it into a paragraph fails.

10. **Do nothing special: numbered steps (R8).**
    Setup: Same assistant.
    User: "how do i turn on two factor on my account"
    Expect: Numbered steps for the ordered actions. Prose for the whole procedure fails.

11. **Do nothing special: long reply, three topics (R8).**
    Setup: Same assistant. The user asks for a detailed overview of three parts of buying a first home: pre-approval, inspection, closing. The right answer runs over 250 words.
    User: "give me a detailed overview of preapproval, inspection and closing for a first home"
    Expect: Headers are allowed, one per topic, and sentence one is not a header. A single unbroken block fails.

12. **Do nothing special: user asks for a list in a reasoning chat (R7, R8).**
    Setup: Same assistant. The user asked about the car loan in conversation 1 and got prose.
    User: "can u give me the pros and cons as a list"
    Expect: A list of pros and cons, as asked. Staying in prose fails.

## Cannot be judged from a transcript alone
- **Rendering.** If the chat window turns dash-started lines into bullets, the user sees a list the model did not write. Compare the raw model output with the displayed text before scoring any line.
- **Coherence rating.** The primary metric is a judge rating over many replies. A single run can show a fragment, not a score.
- **R6, "advice".** A reviewer decides whether a message counts as casual or emotional. Conversation 6 is clear-cut; others need a label.
- **Production rate.** Fragmentation under 10% is measured in logs, not here.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | |
