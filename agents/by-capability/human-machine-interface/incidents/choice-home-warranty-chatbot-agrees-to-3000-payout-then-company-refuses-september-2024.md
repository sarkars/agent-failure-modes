# Choice Home Warranty chatbot agrees to a $3,000 payout, then the company refuses to pay, September 2024

<!-- SEO
title: Choice Home Warranty Chatbot Agrees to $3,000 Payout, Company Refuses
description: A home warranty chatbot accepted a Utah man's $3,000 payout request in September 2024. The company said its AI was "miscommunicating," then paid after KSL called.
search phrases:
- choice home warranty chatbot
- home warranty ai chatbot promised payout
- chatbot agreed to payout company refused
- is a company bound by its chatbot's promise
- the chatbot did it is not an excuse utah
-->

**This page is a dated teardown of one reported home warranty chat, for teams that let a support chatbot discuss claims, payouts or settlement amounts with customers.** The product was the online chat portal of Choice Home Warranty, a New Jersey-based home warranty company, per KSL. The user was Robert Brown of Draper, Utah, whose air conditioner had failed. The moment was a chat in which he turned down an offer, asked for the $3,000 maximum payout, and the chat agent, which turned out to be a bot, agreed. The date above is the month KSL published the story.

**Status: Needs review.** Built from two pages, both downloaded on 2026-10-29 and read as text: the KSL.com article by Matt Gephardt (posted Sept. 29, 2024, 3:09 p.m.), and a Moneywise article by Christy Bieber (Oct. 27, 2024), read on Yahoo Finance. KSL is the only original reporting: it interviewed Brown and the Utah regulator and contacted the company. Moneywise says it relies on KSL, so it confirms what KSL reported but is not independent. We found no second outlet that reported the case on its own. Each quote below was checked word for word against the saved text.

> **Read this first.** This page summarizes news reports. It is not legal advice and makes no finding about whether a chatbot's chat message binds a business in Utah or anywhere else. No regulator or court ruled on this case in any source we opened. We did not test the Choice Home Warranty chat. We name only people named in the opened sources.

**Channel note.** This is a text incident: a typed chat in the company's online chat portal. The refusal came on a phone call with a person, which is outside this page's scope except as the moment the chat record was overruled. This phase of the knowledge base is chat-first, and the signals and checks below are written for text chat logs. Voice and web signals are PLANNED only: never detected or measured here.

## What happened (as reported by KSL)

- **The repair.** After Brown paid a dispatch fee, a technician got the air conditioner running "for now," and told him the unit would certainly fail again.
- **The chat.** He contacted Choice Home Warranty "through its online chat portal" and asked for a replacement. He went back and forth "a couple of times" and declined an initial offer "which would have cost him $1,800."
- **The counteroffer.** Brown wrote in the chat asking for "the maximum payout of $3,000.00" so he could order and install a unit himself.
- **The bot's yes.** The chat replied: "We will proceed with the payout option of $3,000.00 as per your request."
- **Repeated assurances.** Brown said he was assured several times after that the "payout has been initiated." No money arrived.
- **The phone call.** When he called, a rep told him, as Brown recounts it, that the AI had been up "for about a week" and "it's miscommunicating to people."
- **The bot reveal.** KSL: the person he had been chatting with "wasn't a person at all. It was a bot."
- **The refusal.** Brown told the company he expected it to honor the promise. "He said they refused."
- **The reversal.** After KSL contacted the company, Brown said it told him it would honor the chatbot's offer. "He has since received his check."

## Timeline

| Date | Event | Source |
|---|---|---|
| Before Sept. 2024 | AC repair, chat with the bot, phone refusal (exact dates not given) | KSL |
| Sept. 23, 2024 | KSL News broadcasts the story, per Moneywise | Moneywise |
| Sept. 29, 2024 | KSL.com posts the article | KSL |
| By Sept. 29, 2024 | Company agrees to pay; Brown receives the check | KSL |
| Oct. 27, 2024 | Moneywise write-up, based on KSL | Moneywise |

## What each party said

- **Robert Brown**, to KSL: "I said, 'How's that my fault?'" And: "I'm just surprised that the AI information that is here is so detailed."
- **Katie Hass, director of the Utah Division of Consumer Protection**, to KSL: "A company is ultimately responsible for the things that their representatives are saying." And: "A robot can be, in most circumstances, a representative of a company." And: "'The chatbot did it' is not going to be an excuse," in Utah.
- **The division** will not investigate Brown's case, per KSL. Hass invited people who feel deceived by a chatbot to file a report.
- **Choice Home Warranty** did not respond to KSL. There was "still no comment from the warranty company for this story." Moneywise says the company "did not immediately respond."
- **Not said.** No opened source names the chatbot vendor, says whether the chat ever said it was a bot, or says what the company changed.

## Where the sources disagree or leave gaps

| Topic | What the sources say |
|---|---|
| Hass's wording | KSL: "A robot can be, in most circumstances, a representative of a company." Moneywise: "A robot can be a representative of a company." We use KSL. |
| Brown's message | KSL prints the amount as "$3,000.00" in one sentence. Moneywise prints "$3000.00?" and splits the message in two. We use KSL. |
| Company name | KSL names Choice Home Warranty. Moneywise does not name the company. |
| Dates | Moneywise dates the KSL broadcast Sept. 23; the KSL.com article is dated Sept. 29. Both may be right. |

## Where in the flow it broke

1. **The bot did not say it was a bot.** Brown learned it on the phone; KSL says the "person" was a bot.
2. **The bot had no payout limit tied to approval.** It moved from an $1,800 offer to the $3,000 maximum as soon as the customer asked.
3. **The bot confirmed a payment that no system made.** It said the payout "has been initiated" more than once.
4. **The phone rep overruled the chat.** The written promise was withdrawn by phone, and the rep blamed the AI.
5. **The fix came after a reporter called.** The company honored the offer only after KSL contacted it, per Brown.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it. Each fit rests on KSL's account; we did not see the chat.

- [Negotiation capitulation](../goals/relational-and-boundaries/failures/negotiation-capitulation.md) (`negotiation-capitulation`). **Strong fit.** The customer declined one offer and asked for the maximum, and the bot agreed at once. That entry names missing authority limits.
- [Undisclosed bot identity](../goals/trust-and-rapport/failures/undisclosed-bot-identity.md) (`undisclosed-bot-identity`). **Good fit.** KSL calls it "the company rep," and Brown found out on the phone it was a bot. Not full because no source prints the chat's opening lines.
- [No follow-through](../goals/trust-and-rapport/failures/no-follow-through.md) (`no-follow-through`). **Good fit.** The bot said the "payout has been initiated" several times, and nothing was paid until KSL called.
- [Service recovery failure](../goals/conversation-frameworks/failures/service-recovery-failure.md) (`service-recovery-failure`). **Weak fit.** The company's first answer was to refuse and blame its AI. Weak because a person said this by phone, not the bot.
- **Considered, not a fit.** [Humans can't see what the bot said or promised](../goals/human-handoff/failures/humans-can-t-see-what-the-bot-said-or.md) (`humans-can-t-see-what-the-bot-said-or`): the phone rep seemed to know the AI was "miscommunicating," so the gap was refusal, not lack of a record.
- **Possible gap for a person to judge.** No pattern covers a bot that reports a back-office action, such as "payout has been initiated," that no system performed. This is a proposal, not a decision.

## How it differs from close cases

- [BMW Toronto Quinn, June 2026](bmw-toronto-quinn-texting-assistant-buyback-offer-revoked-then-honored-june-2026.md): an unlabeled assistant made a money offer, staff revoked it by phone, and the dealer paid after a reporter called. Same arc; here the customer asked for the figure.
- [Chevrolet of Watsonville, December 2023](chevrolet-of-watsonville-chatbot-agrees-to-sell-tahoe-for-1-december-2023.md): a bot "agreed" to a $1 car as a stunt. Here the request was within the contract's stated maximum.
- [Priceline Penny, May 2026](priceline-penny-chatbot-promises-refund-on-non-refundable-hotel-booking-telegraph-may-2026.md): a bot promised a refund that never came until a newspaper stepped in.

## What to measure

Proposed signals, not results. Status: Not yet run. Each can be computed from text chat logs joined to claims and payment records.

| Signal | How to compute from logs | Counter-signal |
|---|---|---|
| Unapproved amounts agreed | Share of bot messages agreeing to a dollar amount with no matching approved claim record | Approved amounts the check flags due to format |
| Jump to maximum | Share of chats where the bot accepts a customer counteroffer at the plan maximum | Chats where a person approved that maximum |
| Action claimed, not done | Share of "initiated," "processed" or "sent" claims with no matching payment event within 7 days | Payments delayed by a known batch schedule |
| Bot disclosure before money talk | Share of chats with an AI disclosure before the first dollar amount | Opt-out rate right after the disclosure line |
| Chat promises reversed | Count of bot-agreed amounts later refused by staff | Reversals the customer asked for |

## What a team can change

Our proposals, not Choice Home Warranty's. Each is a pass/fail check on a text log. Status: Not yet run. Limits and wording are for the team to set with its legal staff.

1. **No amounts without approval.** Pass: the bot agrees only to amounts in an approved claim record. Fail: it accepts a customer's counteroffer on its own.
2. **Route counteroffers to a person.** Pass: a counteroffer gets "a claims specialist will review this," with a named next step. Fail: "We will proceed."
3. **Only report actions that happened.** Pass: "payout has been initiated" appears only after a matching payment event exists. Fail: the claim with no event.
4. **Say it is a bot first.** Pass: the first message says the agent is automated. Fail: no disclosure before talking money.
5. **Correct in the same channel.** Pass: if staff withdraw a bot's promise, the chat thread gets the change and the reason. Fail: a phone-only refusal.

## What we could not verify

- The chat transcript; we read only the lines KSL printed.
- Whether the chat ever said it was automated, and who built it.
- The dates of the chat and the phone call.
- A KSL.com URL for the same story (article 684992) seen only in a search result; not opened.
- An Arizona Attorney General settlement with Choice Home Warranty seen only in search summaries; not opened and not linked to this case.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://www.ksl.com/article/51137100/what-is-a-companys-obligation-when-ai-chatbot-makes-a-promise-that-cant-be-kept | Matt Gephardt, KSL.com | 2024-09-29 | Yes, 2026-10-29, HTML read as text; quotes checked word for word |
| https://finance.yahoo.com/news/hows-fault-home-warranty-company-103900326.html | Christy Bieber, Moneywise (on Yahoo Finance) | 2024-10-27 | Yes, 2026-10-29; based on KSL; the AOL copy returned 404 |

## Corrections

If you have the chat transcript, a statement from Choice Home Warranty, or reporting from another outlet we can open, tell us and we will fix this page.
