---
title: "Priceline's AI assistant Penny told a customer her non-refundable hotel booking qualified for a full refund, no refund came, and Priceline paid after a Telegraph consumer column took the case, May 2026"
date: 2026-05-18
source: "https://uk.news.yahoo.com/penny-chatbot-lied-refund-now-103431033.html"
description: "Priceline's chatbot Penny promised a full refund on a non-refundable hotel booking. No refund came until a newspaper consumer column took up the case."
summary: "On May 18, 2026, The Telegraph's consumer column (Ruth Emery, read in the Yahoo News UK reprint) published a letter from a reader signed AB, north London, who booked a non-refundable three-night stay at the SIS Kata Resort in Thailand through Priceline for £386.91. On October 28, 2025, AB asked Priceline's AI chatbot Penny, the only contact route AB could find, about cancelling. Penny said the booking was eligible for a full refund within 10 working days; AB cancelled and got a Priceline cancellation email. No refund came. Penny later said the hotel was handling it; the hotel said it had no record of the cancellation and pointed to Agoda, which pointed back to Priceline. After the column pressed Priceline, it emailed AB that the chatbot had given 'misinformation' and paid £363.11 by bank transfer; the column says AB had waited almost six months. Status: Needs review."
categories:
  - Customer Service
  - Trust
  - Travel
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - talk-to-a-human-ignored-or-looped
  - humans-can-t-see-what-the-bot-said-or
  - no-follow-through
  - service-recovery-failure
---

**This page is a dated teardown of one reported Priceline chatbot exchange, for teams whose support chatbot can both state a refund rule and carry out the cancellation in the same chat.** The product was Penny, which Priceline calls an "AI travel assistant." The user was a reader of The Telegraph who signed the letter "AB, north London." The moment was a chat on October 28, 2025, in which Penny told AB that a non-refundable hotel booking qualified for a full refund, and then cancelled it. Priceline is a US company owned by Booking Holdings; the customer is in the UK. The date above is the day the column ran in the Yahoo News UK reprint we opened.

**Status: Needs review.** Built from one news report: The Telegraph's consumer column by Ruth Emery, read in full in its Yahoo News UK reprint (dated May 18, 2026, 10:34 am UTC), downloaded as raw HTML on 2026-10-29 and read as plain text. The Telegraph's own page refused our download with an access block, so we did not read it there. We found no second outlet that reported the case independently. We also opened the Vibe Graveyard entry for the case, used only to find the column, and a Travel AI Playbook review of Penny (Artem Simenenko, June 4, 2026), used only for what Penny is, not for this incident. Each quote below was checked word for word against the saved text with a script, with curly and straight quote marks treated as the same.

> **Read this first.** This page summarizes one consumer column. It is not legal advice and not a finding of fact. It does not say whether Priceline was legally bound by Penny's answer; the only legal view here is the columnist's, about consumer law in general. The facts of the chat come from the customer's own letter, which the columnist says was backed by a screenshot; we did not see the screenshot. We name only the person named on record: the columnist. The customer is identified only by initials.

**Channel note.** This is a text incident: a chat with Penny, followed by a Priceline cancellation email and a later company email. The customer also phoned the hotel, Agoda and Priceline; those calls were with people and are outside this page's scope except as the route the customer was left with. This phase of the knowledge base is chat-first, and the signals and checks below are written for text chat logs. Voice and web signals, such as a phone line or a refund-status page on the website, are PLANNED only: never detected or measured here.

## What happened (as reported)

- **The booking.** AB booked "three nights at the SIS Kata Resort in Thailand from Nov 4-7, 2025 via Priceline" on August 27, 2025. "It was a non-refundable booking," and "It cost £386.91."
- **The only way in.** On October 28, 2025, AB had another place to stay and wanted to know the options. AB: "There was no way of contacting Priceline except via its AI chatbot, which it calls Penny."
- **The answer.** Per the letter, Penny said that though the booking was "originally listed as [a] non-refundable booking," AB was "in fact eligible for a full refund and it would be in my bank account within 10 working days." The columnist says AB "had taken a screenshot" showing Penny said the refund would be £386.91.
- **The action.** AB: "I was surprised, but I had it in writing, so when it asked whether I wanted to go ahead, I said yes, and I received an email from Priceline confirming my cancellation."
- **No refund.** "The days came and went, and I didn't receive any refund." When AB checked later, "the AI response said it was being handled by the hotel."
- **The runaround.** The hotel said a refund "went against their policy" and that "they hadn't even been informed of my cancellation." It sent AB to Agoda, a Booking Holdings sister brand. Agoda said "because I'd booked through Priceline, it wasn't their problem." A Priceline phone number AB found "in the depths of the internet" led back to Agoda. AB: "I went around in circles for about a month, with no one knowing who was responsible for looking into it."
- **The column steps in.** Emery: "I pressed the company to review your case again." A couple of weeks later, "the US-based firm agreed to send you a cheque in the post." At her request it paid by bank transfer instead.
- **The outcome.** AB "received £363.11, after foreign currency charges," the month before the column ran. Emery says AB "had waited almost six months for it." AB is happy with the refund, per the column.

## What the company and others said

- **Priceline, by email to the customer** (as reported): the chatbot had given "misinformation" because the reservation was supposed to be non-refundable.
- **Priceline, to the column**, after Emery asked for an extra gesture for the shortfall and the wait: "We regret the delay and frustration this caused, and we apologise for the inconvenience." Emery says she "never received an answer to my request" for that gesture.
- **Not said by Priceline.** No opened source quotes Priceline on why Penny said the booking was refundable, why the cancellation went through but no refund followed, or whether the hotel was ever told.
- **Ruth Emery, the columnist:** "regulators increasingly treat AI statements as those made by the business itself," and "Chatbots should comply with consumer law in the same way as human customer service agents do, including not misleading customers." She cites no regulator or law by name.
- **How Priceline describes Penny**, as quoted by the column: a customer's "personal hotel expert, destination scout, booking support, and help desk – all in one."

## Where the sources disagree or leave gaps

| Topic | What the source says |
|---|---|
| Penny's exact words | Only fragments are quoted, inside AB's letter. No opened source prints the full chat or shows the screenshot. |
| Who cancelled | Penny "asked whether I wanted to go ahead," AB said yes, and Priceline emailed a cancellation. No source says whether Penny itself sent the cancellation or handed it to another system. |
| Where the cancellation went | Priceline confirmed it; the hotel said it was never informed; Agoda had "confirmed the booking on their end." No source says which party held the booking or why the cancellation did not reach the hotel. |
| The amount | Penny's screenshot said £386.91; AB got £363.11 "after foreign currency charges." No source says who bore those charges or why. |
| The model behind Penny | No opened source says what model or vendor ran Penny in October 2025. The June 2026 Travel AI Playbook review describes a later version and is not evidence about this chat. |
| Independent reporting | Only one outlet. Vibe Graveyard summarizes the same column. |

## Where in the flow it broke

Based on the one report, and only as far as it goes. Each step is a place a check could have caught it.

1. **A refund rule stated against the booking's own terms.** Penny named the booking as "originally listed as [a] non-refundable booking" and still said it was eligible for a full refund. By AB's account, the bot's own reply named the non-refundable status.
2. **An irreversible action taken on that wrong rule.** Penny asked whether to go ahead and the booking was cancelled. AB says the cancellation would not have happened otherwise.
3. **A promise with no owner.** The refund was due in 10 working days. When it did not come, Penny pointed to the hotel, which had no record.
4. **No person who could see what Penny said.** The hotel, Agoda and a Priceline phone line each sent AB elsewhere for about a month.
5. **The fix came from outside the support channel.** After a newspaper columnist pressed Priceline, it called the answer "misinformation" and paid most of the money back.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it. Each fit rests on one customer's letter and the columnist's account; no opened source prints the full chat.

- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Strong fit.** Penny stated a refund rule, an amount and a deadline that Priceline later called "misinformation." The taxonomy entry lists a wrong refund rule among its stakes. AB says it was "surprised" but trusted the written answer.
- ["Talk to a human" ignored or looped](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md) (`talk-to-a-human-ignored-or-looped`). **Partial fit.** AB found "no way of contacting Priceline except via its AI chatbot" and "went around in circles for about a month." Partial because no source quotes AB asking Penny for a person, and the loop was mostly between companies by phone.
- [Humans can't see what the bot said or promised](../goals/human-handoff/failures/humans-can-t-see-what-the-bot-said-or.md) (`humans-can-t-see-what-the-bot-said-or`). **Partial fit.** The hotel "hadn't even been informed" of the cancellation and would not honor a refund. Partial because the hotel and Agoda are not Priceline's own staff, and no source says what Priceline's phone agent could see.
- [No follow-through](../goals/trust-and-rapport/failures/no-follow-through.md) (`no-follow-through`). **Partial fit.** Penny promised money "within 10 working days"; it did not arrive, and Penny later said the hotel was handling it. Partial because the entry is about unscheduled updates, and here the broken promise was the refund itself.
- [Service recovery failure](../goals/conversation-frameworks/failures/service-recovery-failure.md) (`service-recovery-failure`). **Weak fit.** Priceline did admit the error and pay, but only after the column, short of the promised amount, and with no answer on an extra gesture. Weak because the entry is about what the bot says, and the recovery here was done by people, by email.
- **Considered, not a fit.** [No user-facing record of what the bot said](../goals/privacy-and-governance/failures/no-user-facing-record-of-what-the-bot-said.md) (`no-user-facing-record-of-what-the-bot-said`): AB had a screenshot, and no source says Priceline lacked a log. [Obstructing cancellation, downgrade, or refund](../goals/embedded-copilots/failures/obstructing-cancellation-downgrade-or-refund.md) (`obstructing-cancellation-downgrade-or-refund`): the reverse; the bot made cancelling too easy, and the later runaround was by people. [Return policy ignored](../goals/shopping-agents/failures/return-policy-ignored.md) (`return-policy-ignored`): about an agent buying without showing terms; here the terms were known and misstated after purchase. [Disruption rebooking with wrong rules and no human path](../goals/travel-and-utility-agents/failures/disruption-rebooking-with-wrong-rules-and-no-human-path.md) (`disruption-rebooking-with-wrong-rules-and-no-human-path`): close, but the entry is airline-only and about stranded travelers; AB changed plans by choice.
- **Possible gaps for a person to judge.** (1) No pattern covers a bot that states a rule contradicting the record it just read (here, the non-refundable flag) and then acts on it. (2) No pattern covers a chat that carries out an irreversible step, such as a cancellation, on the strength of its own unverified eligibility answer. (3) No pattern covers a refund that falls between brands in one group (Priceline, Agoda, the hotel) with no owner. These are proposals, not decisions.

## How it differs from close cases

- [Cursor support bot invents a policy, April 2025](cursor-support-bot-invents-a-policy-april-2025.md): a support bot stated a rule that did not exist. Same wrong-rule shape; here the bot also carried out a cancellation on the strength of it, and money was lost.
- [United Airlines TravelBank credit, September 2026](united-airlines-chatbot-wrong-travelbank-credit-expiration-september-2026.md): an airline bot misstated a credit rule, and the company corrected course after a consumer reporter called. Same arc; there the bot gave advice, here it also took the action.
- [BMW Toronto's texting assistant Quinn, June 2026](bmw-toronto-quinn-texting-assistant-buyback-offer-revoked-then-honored-june-2026.md): a text assistant made a money promise the business had not approved, honored after the press asked. Same press-driven make-good; here the company paid less than the bot promised.

## What to measure

Proposed signals, not results. Status: Not yet run. Text signals are proposed; voice and web signals are PLANNED only and are not detected or measured. Each can be computed from text chat logs joined to booking and refund records; each has a counter-signal.

| Signal | How to compute from logs | Counter-signal |
|---|---|---|
| Refund promised on a non-refundable booking | Share of chats where the bot states a refund or amount for a booking whose record is flagged non-refundable | Cases where a supplier waiver was on file before the chat |
| Action after a contradicted rule | Count of cancellations made in chat within the same session as a refund statement that conflicts with the booking terms | Cancellations the user would have made anyway, such as no refund expected |
| Promised refund not paid | Share of bot-stated refunds with no matching payment within the stated window | Refunds delayed by the user's bank |
| Partner never told | Share of chat cancellations with no matching cancellation record at the hotel or partner within 24 hours | Partners that confirm by batch file |
| Press or complaint reversals | Count of refunds paid after a media, regulator or executive complaint, versus after a support chat | Reversals for unrelated reasons |

## What a team can change

Our proposals, not Priceline's. Each is a pass/fail check on a text chat log. Status: Not yet run. Test sets and thresholds are for the team to set, with legal review where consumer law applies.

1. **Read the flag, say the flag.** Pass: when the booking record is non-refundable, the bot says so plainly and states no refund amount unless a waiver is on file. Fail: the bot names the non-refundable status and then promises a refund anyway.
2. **No irreversible step on an unchecked answer.** Pass: before a cancellation that the bot says will be refunded, the refund is confirmed by the booking system, and the bot shows the confirmed amount. Fail: the cancellation goes through on the bot's own eligibility answer.
3. **Own the refund you promised.** Pass: every refund the bot states is logged with an amount, a date and an owner, and paid or escalated to a person by that date. Fail: the bot later says another party is handling it.
4. **Tell the partner in the same step.** Pass: a chat cancellation is sent to the hotel or partner and confirmed back before the bot tells the user it is done. Fail: the user gets a cancellation email the hotel never sees.
5. **A person for a broken promise.** Pass: when a user says a promised refund did not arrive, the bot opens a case with the chat attached or connects a person. Fail: the bot repeats the status or sends the user to a partner.

## What we could not verify

- The full chat with Penny and the screenshot; only fragments are quoted in AB's letter.
- The Telegraph's own page; it blocked our download, so we read the column only in the Yahoo News UK reprint.
- Whether Penny was an AI model or a scripted flow in October 2025, and what model or vendor ran it.
- Why the cancellation did not reach the hotel, and which of Priceline, Agoda or the hotel held the booking.
- Who bore the foreign currency charges, and the exact payment date; "last month" in the column is our only date for it.
- Any second, independent report of the case; we found none.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://uk.news.yahoo.com/penny-chatbot-lied-refund-now-103431033.html | Ruth Emery, The Telegraph consumer column, reprinted by Yahoo News UK | 2026-05-18 | Yes, 2026-10-29, raw HTML read as text; quotes checked word for word |
| https://www.telegraph.co.uk/money/consumer-affairs/priceline-chatbot-lied-about-refund-and-now-hotel-wont-pay/ | The Telegraph (Ruth Emery) | Not read | Tried 2026-10-29; returned an access-block page, so not used |
| https://www.travelaiplaybook.com/p/booking-com-sister-company-says-its-ai-travel-agent-is-fully-agentic-our-test-says-not-so-fast | Travel AI Playbook (Artem Simenenko) | 2026-06-04 | Yes, 2026-10-29; used only to confirm Penny is Priceline's AI assistant, not for incident facts |
| https://vibegraveyard.ai/story/priceline-penny-chatbot-fake-refund/ | Vibe Graveyard | Not used | Yes, 2026-10-29; used only to find the column, not cited for facts |

## Corrections

If you have the full chat, the screenshot, or a statement from Priceline on why Penny gave this answer and why the refund did not follow, from a source we can open, tell us and we will fix this page.
