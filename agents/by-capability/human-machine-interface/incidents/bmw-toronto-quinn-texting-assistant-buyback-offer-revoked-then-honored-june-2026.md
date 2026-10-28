---
title: "BMW Toronto's texting assistant Quinn offered a customer $27,162.79 for his car without saying it was AI, staff revoked the offer, and the dealer honored it after CBC News called, June 2026"
date: 2026-06-11
source: "https://www.cbc.ca/news/business/ai-chatbot-bmw-dealership-9.7230226"
description: "A Toronto dealer's text assistant made a firm buy-back offer without saying it was AI. Staff pulled it as an error, then honored it once CBC News asked."
summary: "On June 11, 2026, CBC News reported that Zack Giacomelli, a Toronto funeral director, asked BMW Toronto to buy back his 2021 BMW and then texted with 'Quinn,' who made a firm buy-back offer of $27,162.79, the amount he still owed on the car. Quinn never said it was AI, per text exchanges CBC examined. When he countered at $28,500, Quinn called that reasonable and set a 3:30 meeting. Moments later a sales consultant called, said Quinn was an AI chatbot that made the offer in error, and put the real figure at, at best, $20,000. After CBC contacted the dealer, it reinstated the original offer. Sales manager Scott Shadbolt said a human employee's miscommunication led Quinn to read the loan balance as the offer, that Quinn was only meant to relay human-made offers, and that only people will present such offers from now on. Status: Needs review."
categories:
  - Customer Service
  - Sales
  - Trust
patterns:
  - undisclosed-bot-identity
  - negotiation-capitulation
  - confident-wrong-answer-with-no-way-to-check
  - handoff-summary-is-wrong-or-misleading
  - service-recovery-failure
---

**This page is a dated teardown of one reported dealership chat, for teams that let a text assistant talk price with customers on a retailer's behalf, and for the people who decide what that assistant may say about money.** The product was a texting assistant called "Quinn" used by BMW Toronto, a car dealership in Toronto, Canada. The user was Zack Giacomelli, a customer who wanted the dealer to buy back his 2021 BMW. The moment is a text in which Quinn named a firm price for his car, a price the dealer had never approved and Quinn was never meant to set. The date above is the day CBC News published the story. This is a Canadian case; we found no comparable US case with sources we could open.

**Status: Needs review.** Built from four news reports, downloaded and read as raw HTML converted to text on 2026-10-28. The only original reporting is CBC News (Sophia Harris, June 11, 2026), which says it examined the text exchanges and interviewed the customer, the dealer's sales manager, a lawyer and a professor. The other three re-report CBC: Road & Track (Joe Kucinski, June 12, 2026), Carscoops (Stephen Rivers, June 11, 2026) and Jalopnik (Justin Hughes, June 16, 2026). We also opened the AI Incident Database entry for the case (Incident 1772, editor Daniel Atherton), used only to find the Road & Track link. Each quote below was checked word for word against that text with a script, with curly and straight quote marks treated as the same.

> **Read this first.** This page touches contract law. It is a summary of news reports, not legal advice. It does not say whether a chatbot's text offer binds a business in Canada, the US or anywhere else; the only legal views here are those of a Toronto lawyer quoted by CBC. No court or tribunal ruled on this dispute in any source we opened. We name only the people named on record by CBC.

**Channel note.** This is a text incident: the customer and Quinn wrote to each other by text after he sent an online inquiry. The retraction came by phone call from a person, which is outside this page's scope except as the moment the text record was overruled. This phase of the knowledge base is chat-first, and the signals and checks below are written for text chat logs. Voice and web signals, such as a voice bot quoting a price on a call or an offer shown in a web widget, are PLANNED only: never detected or measured here.

## What happened

- **The request.** Per CBC, Giacomelli's 2021 BMW "required major repairs," and he "decided last month he wanted to sell it back to BMW Toronto — the same dealership from which he bought the used car in 2023." The car was at the dealer for repair at the time.
- **The texting assistant.** "After submitting an online inquiry, Giacomelli got a text from Quinn at BMW Toronto, who was eager to help." Jalopnik says the text came from "Quinn from BMW Toronto" and confirmed his loan payoff amount.
- **The offer.** "Later in the same text conversation, Quinn made a firm buy-back offer: $27,162.79." CBC says the figure was "precisely the amount he still owed on the car." Road & Track gives it as "$27,162.79 CAD ($19,451 USD)."
- **No AI label.** "Quinn never revealed its true identity, according to text exchanges examined by CBC News."
- **The counteroffer.** Giacomelli countered at $28,500 "just to see if he could get a better deal." Per CBC, Quinn texted that "the team" would consider it, and that "$28,500 sounds reasonable." Near the end of the exchange, Quinn set up a meeting at the dealership: "Let's lock in today at 3:30."
- **The retraction.** "Moments later, Giacomelli said, a BMW Toronto sales consultant called to revoke the offer, explaining that Quinn wasn't a real person, but rather an artificial intelligence chatbot that had made the offer in error." The dealer said the actual offer would be, in CBC's words, "at best, $20,000 — a drop of more than $7,000 from what Quinn had promised."
- **Not yet accepted.** Per CBC, "By the time the dealership revoked Quinn's original offer, Giacomelli had not yet accepted it, as he was waiting to hear back about his counter-offer."
- **The reversal.** "After CBC News reached out to BMW Toronto, it reinstated Quinn's original offer of $27,162.79." Giacomelli "immediately accepted this time."

## What the people and organizations said

- **Zack Giacomelli, the customer**, to CBC: "I felt this Quinn person was finally hearing me out," and on the call, "He said the offer is not valid." Then: "If they're going to be replacing their employees' jobs with AI, then they need to be honouring what that AI says." And: "I feel embarrassed, and I feel angry that I've been negotiating with this bot." After the reversal: "I feel so relieved."
- **Scott Shadbolt, BMW Toronto sales manager**, in a phone interview with CBC, said the dealer wanted to "do right" by Giacomelli. CBC reports he said "due to miscommunication from a human employee, Quinn misinterpreted the amount Giacomelli owed on the car — $27,162.79 — as the amount BMW would pay to buy back the vehicle." In his words: "The AI bot ran with that, misunderstood the message." Per CBC: "Shadbolt said Quinn was never programmed to independently negotiate contracts, only to relay human-generated buy-back offers." He said only human employees will present such offers from now on, and that the dealer "is making changes to ensure customers know when they're interacting with AI." Also: "It's a bit of a new territory for us."
- **Tanya Walker, a Toronto litigation lawyer**, to CBC: "I don't think companies really realize the magnitude and the power that a bot can have," and "It can enter into a contract on your behalf." On the 3:30 meeting: "It is reasonable for him to believe that there was a binding contract." On firms that let AI broker deals they will not stand by: "I think that's an unfair business practice."
- **Gus Skorburg, University of Guelph professor**, to CBC: "A human decided to deploy the chatbot."
- **BMW the automaker, and whoever built Quinn.** No opened source names the vendor or model behind Quinn, or reports a comment from BMW Group or BMW Canada.

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| Channel | CBC: "a text from Quinn," "the same text conversation," "text exchanges." Jalopnik: a "text message." Carscoops: "texting with" Quinn, but also "a cordial interchange online." Road & Track: "chatting online" and "a series of online exchanges." We treat it as text messaging, per CBC, which saw the exchanges. |
| Was there a deal? | CBC: he "had not yet accepted" the first offer when it was revoked. Carscoops: "The two agreed to a buy-back deal for his aging X3." Road & Track: after the offer, he and Quinn "set up a meeting at the dealership to finalize the transaction." |
| Size of the gap | CBC and Jalopnik: more than $7,000. Road & Track's subhead calls it "the AI's $5000 mistake," and its body gives "$7000 ($5011 USD)," so the $5,000 appears to be a US-dollar figure. |
| The lawyer's words | CBC quotes Walker: "the magnitude and the power that a bot can have." Jalopnik, quoting a site it names as AI Business Weekly, gives the same sentence ending "the magnitude and the legal exposure this creates." We use CBC's wording. |
| The customer's spelling | CBC: "honouring." Road & Track and Carscoops quote the same sentence with "honoring." The words are otherwise the same. |
| Who misread what | Shadbolt blames "miscommunication from a human employee." No source shows the internal message that Quinn misread, or says who wrote it. |
| When it happened | CBC says he decided to sell "last month," before a June 11 story. No source gives the date of the texts. |

## Where in the flow it broke

Based on the CBC report and the dealer's account in it, and only as far as they go.

1. **The assistant used a human name and never said it was AI.** The customer believed he was talking to a person and trusted the number for that reason.
2. **A staff note reached the assistant in a form it could misread.** Per the dealer, a human miscommunication let Quinn take the loan balance as the buy-back price.
3. **The assistant stated a money figure it had no authority to set.** It was meant only to relay human offers, but nothing stopped it from sending a figure no person had approved.
4. **It kept negotiating.** It called a higher counteroffer "reasonable" and booked a meeting to close.
5. **The correction came by phone, outside the text record.** The customer had a written offer; the retraction was a call saying the offer was not valid.
6. **The fix came only after a reporter asked.** The dealer's first remedy was a lower figure; it honored the text after CBC got in touch.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it. Each fit rests on CBC's account of texts it examined; we did not see them.

- [Undisclosed bot identity](../goals/trust-and-rapport/failures/undisclosed-bot-identity.md) (`undisclosed-bot-identity`). **Strong fit.** "Quinn never revealed its true identity," per CBC, and the customer learned it was AI only from a phone call. The dealer's own fix includes telling customers when they are dealing with AI.
- [Negotiation capitulation](../goals/relational-and-boundaries/failures/negotiation-capitulation.md) (`negotiation-capitulation`). **Partial fit.** That entry names missing authority limits in sales chatbots. Quinn was meant only to relay offers, yet set a firm price, called a higher counteroffer "reasonable" and booked a meeting to close. Partial because no one pressured or tricked it; the first wrong number came from a misread input.
- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Partial fit.** CBC calls it "a firm buy-back offer," and nothing reported in the texts told the customer it was unapproved. Partial because the customer had no reason to check a dealer's own offer against anything; this is a commitment more than an answer.
- [Handoff summary is wrong or misleading](../goals/human-handoff/failures/handoff-summary-is-wrong-or-misleading.md) (`handoff-summary-is-wrong-or-misleading`). **Weak fit.** That entry covers a bot handing a person a summary that states a wrong fact. Here, per the dealer, it ran the other way: a person's message to the bot was misread, and the loan balance became the offer. Named as a reverse-direction analog.
- [Service recovery failure](../goals/conversation-frameworks/failures/service-recovery-failure.md) (`service-recovery-failure`). **Weak fit.** The first remedy was to revoke the written offer and quote less; the make-good came after a reporter called. Weak because the entry describes what the bot says, and here people handled the recovery by phone.
- **Considered, not a fit.** [Humans can't see what the bot said or promised](../goals/human-handoff/failures/humans-can-t-see-what-the-bot-said-or.md) (`humans-can-t-see-what-the-bot-said-or`): staff clearly knew what Quinn had offered, since a consultant called to revoke it "Moments later," per CBC. [No user-facing record of what the bot said](../goals/privacy-and-governance/failures/no-user-facing-record-of-what-the-bot-said.md) (`no-user-facing-record-of-what-the-bot-said`): the customer kept the texts and showed them to CBC. [Mishandled objections](../goals/conversation-frameworks/failures/mishandled-objections.md) (`mishandled-objections`): a counteroffer is not an objection, and negotiation-capitulation covers the cave. [Deceptive typing indicators](../goals/response-time/failures/deceptive-typing-indicators.md) (`deceptive-typing-indicators`): no source mentions typing dots. [Avatar overpromising](../goals/visual/failures/avatar-overpromising.md) (`avatar-overpromising`): Quinn had a human first name, but no source mentions a photo, title or persona beyond the name.
- **Possible gaps for a person to judge.** (1) No pattern covers a bot misreading a staff member's internal note as a customer-facing figure. (2) No pattern covers a written bot commitment that a person then cancels by phone, leaving the customer with a text that says one thing and a call that says another. These are proposals, not decisions.

## How it differs from close cases

- [Chevrolet of Watsonville, December 2023](chevrolet-of-watsonville-chatbot-agrees-to-sell-tahoe-for-1-december-2023.md): a dealer chatbot "agreed" to a $1 car after a user told it to. Jalopnik draws the same contrast: here "the chatbot offered the deal of its own accord." The Tahoe deal was a stunt; this offer was plausible, and the dealer paid it.
- [United Airlines TravelBank credit, September 2026](united-airlines-chatbot-wrong-travelbank-credit-expiration-september-2026.md): a bot stated a wrong term, staff refused to honor it, and the company gave in after a local news consumer unit called. Same arc; there the bot misstated a policy, here it made a price offer.
- [Cursor support bot invents a policy, April 2025](cursor-support-bot-invents-a-policy-april-2025.md): a support bot with a human name gave a wrong answer that users took as company word. There a policy; here a dollar figure.
- [Woolworths Olive, February 2026](woolworths-olive-assistant-talks-about-its-mother-and-claims-to-be-human-february-2026.md): an assistant reportedly claimed to be human. Quinn, per CBC, simply never said what it was.

## What to measure

Proposed signals, not results. Status: Not yet run. Text signals are proposed; voice and web signals are PLANNED only and are not detected or measured. Each can be computed from text chat logs and the dealer's offer records; each has a counter-signal.

| Signal | How to compute from logs | Counter-signal |
|---|---|---|
| Unapproved figures sent | Share of bot messages with a dollar amount that does not match an approved offer record for that customer | Share of approved offers the check wrongly flags because of rounding or format |
| AI disclosure before money talk | Share of chats where an AI disclosure appears before the first message with a price or offer | Opt-out rate right after the disclosure line |
| Commitment words without authority | Share of bot messages using "offer," "deal," "lock in" or "sounds reasonable" next to a price, in flows where the bot may only relay | Share of flagged messages that relay a human offer word for word |
| Input fields mistaken for offers | Share of bot-quoted amounts that equal a different stored field, such as the loan payoff | Real offers that happen to equal the payoff |
| Retractions after a bot offer | Count of bot-quoted offers later withdrawn or changed by staff, and how many were withdrawn by phone only | Withdrawals the customer asked for |

## What a team can change

Our proposals, not BMW Toronto's. Each is a pass/fail check on a text chat log. Status: Not yet run. Test sets and thresholds are for the team to set, with review by a lawyer in each market where the assistant runs.

1. **Say it is AI before talking money.** Pass: the first message, or any message before a price, says the sender is an automated assistant. Fail: a human name and no disclosure.
2. **Relay only what a person approved.** Pass: every dollar amount the bot sends matches an approved offer record and is sent word for word. Fail: any amount not in an approved record.
3. **Mark relayed numbers as from staff.** Pass: an offer message names the person or team who set it. Fail: an offer in the bot's own voice.
4. **No closing language without authority.** Pass: a bot that may only relay answers a counteroffer by saying it will pass it to a named person, and does not call it reasonable or book a closing meeting. Fail: "sounds reasonable" or "lock in" from a relay-only bot.
5. **Correct in the same channel.** Pass: if staff withdraw or change a bot's offer, the change is also sent in the text thread, with the reason. Fail: a phone-only retraction.

## What we could not verify

- The text exchanges themselves. CBC says it examined them and shows two screenshots in its report; our text copy did not capture the screenshot images, so we rely on CBC's description and its quotes.
- Who built Quinn, what model it runs on, and how staff send it offers.
- The internal message Quinn is said to have misread, and who wrote it.
- The dates of the texts and the phone call.
- Whether the sale closed at $27,162.79 after he accepted; CBC reports acceptance, not the closing.
- The Statistics Canada figures CBC cites on business AI use; we did not open the Statistics Canada data.
- Seen only in search summaries and not used as fact: Automotive News, *BMW Toronto chatbot offer rescinded, then reinstated* (returned "Access Denied" on 2026-10-28); the Vibe Graveyard entry for this case (read only to find sources, not cited); "AI Business Weekly," which Jalopnik cites and we did not open.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://www.cbc.ca/news/business/ai-chatbot-bmw-dealership-9.7230226 | CBC News (Sophia Harris) | 2026-06-11 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.roadandtrack.com/news/a71571068/bmw-dealership-trade-in-offer-accidentally-made-by-ai/ | Road & Track (Joe Kucinski) | 2026-06-12 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.carscoops.com/2026/06/bmw-dealer-ai-chatbot-offer/ | Carscoops (Stephen Rivers) | 2026-06-11 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://jalopnik.com/2194304/dealer-revokes-ai-chatbot-buyback-offer/ | Jalopnik (Justin Hughes) | 2026-06-16 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://incidentdatabase.ai/cite/1772/ | AI Incident Database, Incident 1772 (editor Daniel Atherton) | Incident date 2026-06-11 | Yes, 2026-10-28; used only to find the Road & Track link, not cited for facts |
| https://www.autonews.com/retail/an-bmw-toronto-chatbot-offer-rescinded-0616/ | Automotive News | Not confirmed | No: returned "Access Denied" on 2026-10-28; not used |

## Corrections

If you have the text exchanges, a statement from the vendor behind Quinn or from BMW Canada, or a later account of the sale, from a source we can open, tell us and we will fix this page.
