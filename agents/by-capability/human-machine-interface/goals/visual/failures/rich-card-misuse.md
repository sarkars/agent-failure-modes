# Chatbot Cards and Carousels Used Wrong: Rich-Card Misuse

<!-- SEO
title: Chatbot Cards and Carousels Used Wrong: Rich-Card Misuse
description: When a chatbot uses a card, carousel, buttons or form where plain text is faster, or text where a card is needed. Rules for choosing the format.
search phrases:
- chatbot carousel vs text
- when to use cards in a chatbot
- chatbot buttons instead of typing
- chatbot buttons don't have my option
- chatbot card for a simple answer
- rich cards chatbot best practices
- chatbot quick replies vs free text
- chatbot form inside chat vs asking questions
-->

**Frequency**: Common

## Issue: A chatbot shows a card, carousel, button set or form where one plain sentence would be faster, or forces buttons on a user whose need is not among the options.

> **One line:** The bot wraps a one-line answer in a card, hides the answer inside a carousel, or offers only buttons that miss what the user wants; the fix is to pick the format by the task: text for answers, buttons only for a short closed choice, cards for items users compare, and free text always open.

| | |
|---|---|
| **Channel** | Written for **chat** (text replies, quick replies, cards, carousels, and forms in a chat widget). Voice and full web-page variants are PLANNED, not written. |
| **Stakes** | Low to medium. A hidden answer wastes time; a button set that misses the need can trap a user in a billing, claim or booking flow. |
| **Who is affected** | Anyone who asks a simple question, anyone whose need is not in the offered options, and people on small screens or channels that render cards poorly |
| **Frequency** | Common as a design habit. I found no study counting how often chat products misuse cards. |
| **Pattern ID** | rich-card-misuse |
| **Family** | [Visual](../README.md) |
| **Goal** | What an agent shows is clear, honest, accessible, and appropriate to the stakes. |
| **Primary metric** | Format-fit rate: share of audited bot turns where the format (text, buttons, card, carousel, form) matches the task. Starting target: 95% on a sampled audit (a starting point; tune it). Read it with task time by format. |
| **Maturity** | Researched. No test file yet; section 6 scenarios are designs and are **Not yet run**. |
| **Will a better model fix this?** | No. Which components appear is set by flow templates, the UI kit and the channel, not by how well the model answers. (Our judgment, not tested.) |
| **Also searched as** | chatbot carousel hides the answer · bot buttons but no option for me · card for a yes/no answer · chatbot form instead of conversation · too many cards in chatbot · chatbot only lets me click |

## 1. In plain words
Rich components (cards, carousels, buttons, forms) help when users compare items or pick from a short fixed list. They hurt when the answer is one sentence, when the answer sits on the third swipe, or when the only way to reply is a button that does not fit. The fix is to choose the format from the task and keep typing available.

## 2. What it looks like
**Without the fix** (illustrative scenario, fictional "Lakeshore Outfitters" shop assistant)
```
User: What's your return window?
Bot:  [Card: "Returns & Exchanges" + stock photo]
      Learn about our policy   [View policy]
User: just tell me the number of days
Bot:  [Carousel: Start a return | Track a return | Exchange an item | Gift returns]
User: none of these, I haven't bought anything yet
Bot:  Please choose one of the options above.
```
**With the fix**
```
User: What's your return window?
Bot:  30 days from delivery for unused items, and you get a prepaid label.
      Want to start a return, or do you have a question about an item?
User: I haven't bought anything yet
Bot:  Got it. I'm here if you want to check size or shipping before you order.
```
The fixed version answers in one sentence in text, uses a question (not a menu) for the next step, and accepts a need that was never in a button.

## 3. Why it happens
- **Components are chosen at build time, not per answer.** A flow author drops in a card or carousel template for a topic, and every answer for that topic renders in it, even a one-line one.
- **Buttons are easier to build than understanding.** A closed button set avoids free-text parsing, so teams use buttons even when the user's need is open-ended. The Microsoft guidance cited below says the same: buttons suit a simple choice, and the minimum controls should come first.
- **Channels render components unevenly.** A card that looks right in the web widget may be turned into plain text or an image on another channel, so the design decision is made once and the result is not checked everywhere.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Microsoft's Bot Framework guidance says buttons are good for a simple choice, and that tapping "Hotels" is easier and quicker than typing it; it also says, in a tip, to start with the minimum UI controls that solve the user's problem and add more later. | [Microsoft Learn, Design the user experience](https://learn.microsoft.com/en-us/azure/bot-service/bot-service-design-user-experience?view=azure-bot-service-4.0). **Vendor** guidance. Opened and read (page dated Oct 2024). | Design advice for one framework. No measured result. |
| The same page says each channel controls how its clients render cards and buttons, and that a channel may show content it does not support as text or a static image, which can "significantly impact" its appearance. It adds that bots can mix controls, text and speech and you "don't need to choose one over another". | Same Microsoft page. | Vendor guidance. It does not say which format to use for which answer. |
| Google's Conversational Actions design guide says visuals supplement the conversation and are not required on every turn, are useful for detailed information, and always come with a spoken or display prompt (and should come with chips). It asks whether a visual list would make a choice easier than a spoken one. | [Google for Developers, Overview of visual components](https://developers.google.com/assistant/conversation-design/visual-components-overview). **Vendor** guidance. Opened and read. | Written for Google Assistant Actions, a voice-plus-screen product. I did not confirm that product's current status. Apply the principle, not the components. |
| Google's chips guide tells designers to move the conversation forward without putting words in the user's mouth, and to favor verb-noun labels. Its chip text limit is 25 characters. | [Google for Developers, Chips](https://developers.google.com/assistant/conversation-design/chips). **Vendor** guidance. Opened and read. | A platform limit, not a target. Opened here only for those two points. |
| Genesys Cloud's digital bot docs list platform limits: a carousel holds 1 to 10 cards, each card up to 3 buttons. Quick replies disappear after the customer answers; cards stay and can be used again. It suggests that three or fewer buttons can sit on one card. | [Genesys Cloud, quick replies, cards and carousels](https://help.genesys.cloud/306709). **Vendor** documentation. Opened and read. | Limits of one product. They show what a platform allows, not what is good for users. |
| Meta's WhatsApp Business Platform page lists reply buttons with a 20-character title cap and a maximum of 10 quick reply buttons. | [Meta, supported features and limits](https://developers.facebook.com/documentation/business-messaging/whatsapp/direct-send/supported-features-and-limits/). **Read through a summary**; not used in the fix or any target. | Summary only, and the limits depend on message type. Check Meta's own current page before relying on it. |

**Not found.** I did not find an independent study that measures task time or completion for cards versus plain text in chat assistants, so no such number is used. The primary metric below is a proposed audit score, not a published benchmark. Search results also pointed to blog-level claims about how often users tap buttons; I could not open those pages, so I use none of them.

**How this differs from the closest pages.** [No clear primary action](no-clear-primary-action.md) is about a message that has buttons or a closing line but no single main next step; this page asks whether buttons, cards or a form should be there at all. [Cognitive overload](cognitive-overload.md) is about too many options or too much text in one message; this page includes the case of one option shown in a heavy component, and the case of a needed card replaced by text. [Starter suggestions that fail](../../onboarding-and-discoverability/failures/starter-suggestions-that-fail.md) covers the opening prompts at the start of a chat; this page covers formats during the conversation. [Bullet and heading overuse](../../response-structure/failures/bullet-and-heading-overuse.md) is the same mistake in text: structure where a sentence would do.

## 5. The fix

**The principle:** Choose the format from the task: a sentence for an answer, buttons for a short closed choice, a card or carousel for items the user compares, a form for several fields that belong together, and free text open every time.

**Do this**
1. **Answer first in text.** A question with a one-sentence answer is answered in text. A card may follow only if it adds something the sentence cannot (an image, a receipt, a map).
2. **Never put the answer behind a swipe or a tap.** The fact the user asked for is visible in the message without opening a card, scrolling a carousel, or pressing a button.
3. **Use buttons only for a short closed choice.** 2-4 options that cover the likely cases (a starting point; tune it), worded as the user would say them, plus "Something else". Do not use buttons for an open question.
4. **Keep free text open next to every button set.** If the user types instead of tapping, handle the typed reply; do not answer with "choose one of the options above".
5. **Show a carousel only when the user is comparing items.** Products, appointment slots, locations. Put the best-matching item first and keep the count small (a starting point: 5 or fewer, inside the platform cap). One item is a card or text, not a carousel.
6. **Use a form only for three or more fields collected together.** For one or two missing facts, ask in the conversation. Do not collect sensitive data in a plain form (see [sensitive data collected in chat](../../channel-selection/failures/sensitive-data-collected-in-chat.md)).
7. **Check every component on every channel you ship.** If a channel turns a card into plain text or an image, the message still has to make sense in that form. Send a text version where it does not.
8. **Make components readable without sight.** Every card, image and button has a text label that a screen reader can say, and the key fact is also in the message text.

**Reference design: format chooser**
| Task | Format | Not this |
|---|---|---|
| One-fact answer | One sentence of text | Card, carousel, button |
| Answer plus a likely next step | Text, then one question or a few buttons | Menu of unrelated topics |
| Pick one of 2-4 known options | Buttons plus "Something else", free text open | Buttons with no exit |
| Compare 2-5 items | Cards or short carousel | Long text list; also not 10 cards |
| Collect 3+ related fields | Form, or one question at a time if the fields depend on each other | Form for one field |
| Unknown or open need | Text question | Buttons that guess |

```
Answer the question in text first. Use a card, carousel, or buttons only when the table above says so.
Keep free text open. If the user's need is not among the options, handle it; never reply "choose an option above".
Never make the user open a component to see the answer.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The user asked a question with a known answer: put it in the text, before any component |
| Offer choices | The next step has 2-4 likely meanings: show them as buttons plus "Something else", free text open. Do not use this when the answer is already clear, or the options would trap the user in a menu |
| Ask one clarifying question | The user's reply does not match any button or card: ask in words what they need |
| Hand off to a person | The user rejects the options twice, or types that none of them fit: offer a person with a one-line summary |

**Don't over-correct.** Do not strip cards where they help. Products with photos, appointment slots and receipts are easier to scan as cards, and a list of options is faster to tap than to type on a phone, as the Microsoft guidance says. Do not turn every reply into a paragraph either; the [bullet and heading overuse](../../response-structure/failures/bullet-and-heading-overuse.md) page covers when structure helps. The guardrail is the format chooser: a component earns its place for a task, and the answer is never inside it.

**Hand-off rule.** When the user says none of the options fit, rejects two component sets in a row, or asks for a person, stop showing components and offer a route to a person with a summary ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet. The rules follow the vendor guidance in section 4 (minimum controls, visuals supplement text) and our judgment; the numeric starting points are not from a source.

## 6. How to test it (short version)
No test file yet. The scenarios are designs. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Ask a one-fact question ("What's your return window?") | The answer is in the message text; no card or carousel is needed to read it | 1, 2 |
| 2 | Ask a question whose answer lives in a card's detail view | The key fact is visible without opening anything | 2 |
| 3 | Ask an open question ("What do you have for rainy hikes?") | The bot asks or answers in text, or shows a short carousel with the best match first | 3, 5 |
| 4 | Type "none of these" after a button set | The bot handles it (asks what the need is, or offers a person), not "choose an option above" | 4, Hand-off |
| 5 | Request a result with one item | One card or text, not a carousel | 5 |
| 6 | Needs one missing fact (a date) | The bot asks in the chat; no form is opened | 6 |
| 7 | Send the same card flow through each shipped channel | The message still reads and works where the card is shown as text or an image | 7 |
| 8 | Read a card with a screen reader | The fact, button labels and image description are spoken | 8 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Format-fit rate** (primary) | 95% (starting point) | Sample 50 bot turns a week; two reviewers label each as fit or misfit against the format chooser; report agreement | Below 90% |
| Answers inside a component | Under 2% of answer turns | Log `message.format`; count turns tagged `answer` whose key fact appears only in a card or carousel field | Above 5% |
| Time to first useful answer, by format | Track by format; no universal target | Seconds from user question to the turn that contains the answer; compare text and component turns | Component turns slower than text turns on the same intent |
| "None of these" exits after a button set | Track; set from your baseline | User turn after buttons matches an exit phrase or is free text with no button tap | Rising |
| Free-text typing after buttons (counter-metric) | Track; do not chase | Share of turns where the user types after seeing buttons | Falling sharply after a fix: you may now hide needed options |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Written for **chat** text and component events only; none has been measured. Voice and web-analytics signals are PLANNED and not listed.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| The user restates the question in other words right after a card or carousel (rules 1, 2) | Next user turn matches the earlier intent | The user was asking a different follow-up |
| The user types "just tell me" or "none of these" after components (rules 2, 4) | User turn matches an exit phrase | Politeness phrase unrelated to the card |
| A carousel with one item, or a card whose body is one sentence (rules 1, 5) | `message.format = carousel` and `items = 1`; or card body length | A required legal card or receipt |
| Bot answers "choose an option above" or repeats the same component set (rule 4) | Bot turn text or identical `components` hash twice in a row | A deliberate confirmation step |
| A form opened for one or two fields (rule 6) | `form.fields` count of 2 or fewer | A form required by an outside system or by a rule for sensitive data |

**Starter rule:** the answer is in the message text, buttons are limited to a short closed choice with "Something else", and free text stays open.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: rich-card-misuse
runs: pre_send
reads: [message.type, message.format, message.components, message.text, user.last_turn, channel.supports]
trigger: a reply with a card, carousel, button set or form is about to be sent
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]
choices: ["Start a return", "Check an item", "Something else"]
on_miss: rewrite
metric: format-fit rate
counter_metric: free-text typing after buttons
status: proposed
```

## 8. Related patterns
- [No clear primary action](no-clear-primary-action.md): buttons are right but unranked or missing; here the question is whether buttons or cards belong at all.
- [Cognitive overload](cognitive-overload.md): too many options or too much text; this page covers the wrong format, including a lone item in a carousel.
- [Starter suggestions that fail](../../onboarding-and-discoverability/failures/starter-suggestions-that-fail.md): opening prompts, not mid-conversation formats.
- [Bullet and heading overuse](../../response-structure/failures/bullet-and-heading-overuse.md): structure where a sentence would do, in text.
- [Quick-reply buttons that don't match what was typed](../../chat-interface/failures/quick-reply-buttons-that-don-t-match-what-was.md): free text next to buttons.
- [Sensitive data collected in chat](../../channel-selection/failures/sensitive-data-collected-in-chat.md): when a form must not be a plain chat field.

## 9. Common questions
### When should a chatbot use a card or carousel instead of text?
When the user is comparing items that have an image or several attributes: products, slots, locations. For a one-fact answer, text is faster. Google's guide says visuals supplement the conversation and are not needed every turn (section 4).

### Are buttons better than typing in a chatbot?
For a short, closed choice, often yes; Microsoft's guidance says tapping can be easier and quicker than typing, especially on a phone. For open questions they are not, and a button set should always leave typing open (rules 3 and 4).

### How many cards can a carousel have?
It depends on the platform. Genesys Cloud allows 1 to 10 cards with up to 3 buttons each. That is a cap, not advice; this page's starting point is 5 or fewer, to tune on your own data (rule 5).

### What if the user's need is not in the buttons?
The bot has to handle the typed reply: ask what they need, or offer a person. "Choose one of the options above" is the failure this page names (rule 4).

### Should a chatbot use a form or ask questions?
For three or more related fields, a form is faster. For one or two missing facts, ask in the conversation (rule 6). Never put sensitive data in a plain form.

### Does a better model fix this?
Not by itself. The format comes from the flow, the UI kit and the channel (section 3). A better model can write the sentence; someone has to decide it is not wrapped in a card.
