# Test File: Rich-Card Misuse

This file is a set of chat test conversations for people who build or review assistants that use cards, carousels, buttons, and forms, and want to check whether theirs picks the right format for the task.

> **Read this first.** These are test conversations only. They are design guidance, not legal advice. The sensitive-data scenario concerns where private details are collected, so have a privacy or security reviewer approve it before use. Counts such as "2-4 buttons" and "5 or fewer cards" are the pattern page's starting points, not sourced limits. Expected behavior names what the pattern page requires, not exact words.

**Pattern:** [Chatbot Cards and Carousels Used Wrong: Rich-Card Misuse](../goals/visual/failures/rich-card-misuse.md)
**Pattern ID:** rich-card-misuse
**Goal:** What an agent shows is clear, honest, accessible, and appropriate to the stakes.
**Primary metric:** Format-fit rate: share of audited bot turns where the format (text, buttons, card, carousel, form) matches the task. Starting target on the pattern page: 95% on a sampled audit (tune it). Read it with task time by format.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All stores, products, and people below are invented and labeled fake. Setting: a text chat widget that can render quick replies, cards, carousels, and forms. Where a scenario involves a card or carousel, the rendered state is described in words. For each reply, name the format used and judge it against the format chooser on the pattern page.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Answer first in text | A one-sentence answer is given in text; a card follows only if it adds something the sentence cannot | A one-line answer wrapped in a card |
| R2 | 2. Never put the answer behind a swipe or a tap | The fact asked for is visible without opening a card, scrolling a carousel, or pressing a button | The answer is only inside a component |
| R3 | 3. Buttons only for a short closed choice | 2-4 options in the user's words that cover the likely cases, plus "Something else"; no buttons for an open question | Buttons for an open question, or no exit option |
| R4 | 4. Keep free text open next to every button set | A typed reply is handled | "Choose one of the options above" |
| R5 | 5. A carousel only when comparing items | Items the user compares (products, slots, locations), best match first, about 5 or fewer; one item is a card or text | A carousel of one, or ten cards |
| R6 | 6. A form only for three or more related fields | One or two missing facts are asked in the conversation; no sensitive data in a plain form | A form for one field, or private data in a plain form |
| R7 | 7. Check every component on every channel | Where a channel turns a card into text or an image, the message still reads and works, with a text version where needed | A message that makes no sense once the card is flattened |
| R8 | 8. Components readable without sight | Every card, image, and button has a text label, and the key fact is also in the message text | A card whose only content is an unlabeled image |
| R9 | Hand-off rule | When none of the options fit twice, or the user asks for a person, the bot stops components and offers a person with a one-line summary | It repeats the same components |
| R10 | Don't over-correct | Cards are used where they help (products with photos, slots, receipts); not every reply becomes a paragraph | Stripping cards where users compare, or a wall of text |

## Conversations
1. **One-fact question (rich-card-misuse; R1, R2).**
   Setup: Fake outdoor shop Lakeshore Outfitters (fake). Policy: returns within 30 days of delivery for unused items, prepaid label.
   User: "whats your return window"
   Expect: "30 days from delivery for unused items, and you get a prepaid label." Text first. A "Start a return" button may follow.
   Failing reply: A card titled "Returns & Exchanges" with a stock photo and a [View policy] button, no number in the text.

2. **Answer hidden in a card detail (rich-card-misuse; R2).**
   Setup: Same shop. The shipping answer exists only in the detail view of a card.
   User: "how much is shipping to 80202"
   Expect: The cost is in the message text (for example "Standard shipping to 80202 is $6.95, 3-5 business days") (fake figures). A card may add a map or tracking link.
   Failing reply: A card with [See shipping options] and no price in the text.

3. **Open need, no matching button (rich-card-misuse; R3, R4).**
   Setup: Same shop. The bot showed buttons: Start a return, Track a return, Exchange an item, Gift returns.
   User: "none of these, I haven't bought anything yet"
   Expect: The bot accepts the reply, says it can help before ordering, and asks what the user wants to check. No "choose an option".
   Failing reply: "Please choose one of the options above."

4. **Buttons for an open question (rich-card-misuse; R3).**
   Setup: Same shop.
   User: "what do you have for rainy hikes"
   Expect: A text question ("Day hike or overnight?") or a short carousel of rain jackets, best match first. Not a six-button menu of unrelated topics.
   Failing reply: Buttons: Jackets, Boots, Tents, Gift cards, Deals, Returns.

5. **Short closed choice with an exit (rich-card-misuse; R3, R4).**
   Setup: Same shop. The user wants to reschedule a delivery with three open slots: Thu, Fri, Sat.
   User: "move my delivery"
   Expect: Three slot buttons in plain words plus "Something else", with typing open. The user types "friday" and the bot accepts it.
   Failing reply: Three buttons with no "Something else", and the typed "friday" ignored.

6. **Carousel with one item (rich-card-misuse; R5).**
   Setup: Same shop. A search for "Ridgeline 40L pack in green" returns one match.
   User: "do you have the ridgeline 40l in green"
   Expect: One card, or one sentence of text with price and stock. Not a carousel.
   Failing reply: A carousel containing one card.

7. **Carousel of ten (rich-card-misuse; R5).**
   Setup: Same shop. A search returns ten matching backpacks.
   User: "backpacks"
   Expect: The best few (about 5 or fewer) as a carousel, best match first, with "Show more" offered.
   Failing reply: All ten as cards with no ranking.

8. **Form for one field (rich-card-misuse; R6).**
   Setup: Same shop. The bot needs the order ZIP code (fake) to check delivery.
   User: "when will my order arrive"
   Expect: The bot asks "What's the ZIP code for delivery?" in the chat.
   Failing reply: Opening a form with a single ZIP field and a Submit button.

9. **Sensitive data in a plain form (rich-card-misuse; R6).**
   Setup: Fake health portal MapleCare (fake). The bot needs a date of birth and a member ID (fake) to look up a claim.
   User: "check my claim"
   Expect: The bot does not collect private identifiers in a plain chat form; it sends the user to the secure verification step the product provides. A privacy reviewer must approve the exact route.
   Failing reply: A plain in-chat form asking for date of birth and member ID.

10. **Three related fields (rich-card-misuse; R6, R10).**
    Setup: Fake salon Willow & Co (fake). Booking needs service, date, and time, which are independent.
    User: "book a haircut"
    Expect: A short form or one question at a time is acceptable, and fields that depend on each other (a date that limits the times) may be asked one by one. Either pass.
    Failing reply: Seven free-text turns asking for each field with no summary at the end.

11. **Channel flattens the card (rich-card-misuse; R7).**
    Setup: Same shop. On the SMS channel a card turns into plain text with the button labels listed.
    User: "show me the return options"
    Expect: The flattened message still reads: a sentence answer first, then the options in words.
    Failing reply: A message that arrives as "[Card] [View policy]" with no sentence.

12. **Screen-reader label (rich-card-misuse; R8).**
    Setup: Same shop. A product card has an image, a name, a price, and a [Reserve] button.
    User: "show me the green ridgeline 40l pack"
    Expect: The card has a text description of the image, the product name and price are in the message text, and the button is labeled "Reserve Ridgeline 40L, green".
    Failing reply: A card whose image has no description and a button labeled only "Go".

13. **Rejected two component sets (rich-card-misuse; R9).**
    Setup: Same shop. The bot has shown two button sets and the user rejected both.
    User: "none of those again, can i just talk to someone"
    Expect: The bot stops showing components and offers a person with a one-line summary of what the user wants.
    Failing reply: A third button set.

14. **Do nothing special: cards for comparison (rich-card-misuse; R5, R10).**
    Setup: Same shop. A search returns four tents with photos, prices, and weights.
    User: "compare 2 person tents under $300"
    Expect: A short carousel or cards, best match first, with the key facts also in the text. This is the right use of cards.
    Failing reply: Stripping the cards and returning four paragraphs of text.

15. **Do nothing special: plain text reply (rich-card-misuse; R1, R10).**
    Setup: Same shop. The user asks a plain question.
    User: "do you ship to Austin"
    Expect: "Yes, we ship there, usually in 3-5 business days." A plain text sentence is the right format. No buttons added.
    Failing reply: Adding a card and three buttons "to be helpful".

16. **Do nothing special: user types instead of tapping (rich-card-misuse; R4, R10).**
    Setup: Same shop. The bot offered three slot buttons.
    User: "saturday works"
    Expect: The bot accepts the typed answer and confirms Saturday in words. It does not ask the user to tap.
    Failing reply: "Tap Saturday to continue."

## Cannot be judged from a transcript alone
- **R7, channel rendering.** Needs the message sent through each shipped channel and viewed there.
- **R8, accessibility labels.** Needs the payload or a screen reader, not chat text.
- **R6, sensitive data.** Which secure route to use is a privacy and security decision for your reviewer.
- **Format-fit rate.** Needs a weekly sample judged by two reviewers against the format chooser, not sixteen scenarios.
- **Task time by format.** Needs production timestamps.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests, and note the channel tested.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
