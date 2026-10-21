---
title: "Viewers' Amazon Echo Devices Reportedly Try to Order Dollhouses After a San Diego TV Anchor Repeats a Child's Alexa Phrase, January 2017"
date: 2017-01-06
source: "https://www.foxnews.com/tech/tv-news-report-prompts-viewers-amazon-echo-devices-to-order-unwanted-dollhouses"
summary: "In January 2017 a San Diego morning show (CW6) discussed a young girl's accidental Alexa dollhouse order, and the anchor's on-air remark reportedly made some viewers' Echo devices try to order dollhouses. Opened sources disagree on scale and on whether any order went through. Amazon pointed to the yes-confirmation step, the voice-purchasing switch and a confirmation code."
categories:
  - Customer Service
patterns:
  - wake-word-false-activation
  - no-clear-route-when-an-agent-buys-wrongly
  - order-mix-ups-at-the-speaker
---

**This page is a dated teardown of one public voice-shopping incident, for teams that let a speaker or voice assistant place orders.** Read this first: it is one short dated teardown from public sources, not legal advice. It names the sources we opened (listed at the end). We could not open The Verge's own page, the BBC, or CW6's own report, so the Patton details come from a copy of The Verge story on another site and from news outlets that cite it.

## What happened (as reported)

- **The first order.** Fox News, The Register and the copy of The Verge story say a six-year-old girl in Dallas asked the family's Echo for a dollhouse and the device ordered one, with cookies. The Register and CBS News put the items at a $160 KidKraft Sparkle Mansion dollhouse and four pounds of sugar cookies (CBS: a 4-pound tin). We leave the child unnamed, as most of these pages do.
- **The broadcast.** CW6 News, a San Diego morning show, ran the story. Anchor Jim Patton remarked on the girl's words. Fox News quotes him: "I love the little girl, saying 'Alexa ordered me a dollhouse.'" CBS names a second anchor, Lynda Martin, as part of the on-air discussion.
- **The reported effect.** Fox News says some viewers' Echo devices picked up the broadcast and "attempted" to order dollhouses, and that CW6 reported viewers across San Diego complaining. CBS says viewers complained that their devices had tried to order dollhouses. NBC San Diego says a number of San Diegans reported their Echo ordered toys.
- **Patton on scale.** The Verge copy says Patton told The Verge he did not think any device completed a purchase and could not say how many people were affected. It says the station got "a handful of reports." We could not open The Verge's page itself.
- **Amazon.** CBS and Fox News give Amazon's statement (below). NBC San Diego, The Register and The Verge copy carry no Amazon statement.
- **The family.** CBS says the Dallas family set a four-digit code for purchases.

## What Amazon said (per CBS and Fox News)

- Both pages give the same flow: a person asks Alexa to order, then confirms with a "yes." Fox News adds that a user can say "no" to an accidental order.
- Fox News says a spokeswoman said physical-product orders qualify for free returns.
- Both say Amazon pointed to the Alexa app: turn off voice purchasing, or require a confirmation code before every order.

## Where the sources disagree or are silent

| Topic | What the opened sources say |
|---|---|
| Broadcast date | Fox News (published Jan 6, 2017) says "Thursday"; The Register (Jan 7, 2017) says "Thursday morning." Neither prints the date. By the calendar Thursday was January 5, 2017; that is our reading. The Verge copy's URL is dated January 7; the others do not say. |
| Number of devices or orders | Fox, CBS and NBC give no count. The Verge copy says "a handful of reports" and Patton could not estimate. NBC says the report prompted a slew of orders across the region, with no count. |
| Whether any order completed | The Verge copy: Patton did not think any did. Fox: "attempted" only. CBS, NBC: no confirmation either way. No opened source shows a completed or delivered order from the broadcast. |
| Whether Amazon saw orders | CBS (as read through the fetch tool) says Amazon said there was no influx of dollhouse orders after the newscast. Fox, NBC and The Register give no such statement. We could not read CBS's exact wording. |
| Amazon statement | Quoted by CBS and Fox; absent from NBC, The Register and The Verge copy. |
| Voice purchasing on by default | The Register says it is "enabled by default." Fox, CBS and NBC do not say. |
| PIN or code | CBS and Fox name a confirmation code. NBC mentions parental controls and a confirmation code but no PIN. The Register does not mention either. |
| Price | The Register and CBS say $160; Fox says $170. |
| Anchor's words | Fox: "the little girl." NBC: "that little girl." We quote Fox only. |

## What the sources do not say

- Why the devices heard a TV as a command: no opened source describes the wake word, the device model, or the room.
- Whether Alexa asked for the "yes" confirmation on those devices, or what the viewers said back. Amazon's description is general.
- Which devices were affected, how many households, or whether any dollhouse shipped.
- Whether Amazon changed the wake word, the confirmation prompt, or default settings afterward. None of the opened pages says.
- CW6's own wording of its report. We did not open it.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

Where it broke, in order, as the sources describe: (1) a TV broadcast carried the trigger phrase; (2) the devices treated it as a request to buy; (3) the only stated safeguard was a spoken "yes" after the order request; (4) the owner's remaining options were app settings and a return.

- [Wake-word false activation](../goals/voice/failures/wake-word-false-activation.md) (`wake-word-false-activation`). Main fit. The assistant acted on audio that nobody in the room meant for it. That page's own channel note says the microphone case is planned and not measured, so this teardown adds a real purchase case.
- [No clear route when an agent buys wrongly](../goals/shopping-agents/failures/no-clear-route-when-an-agent-buys-wrongly.md) (`no-clear-route-when-an-agent-buys-wrongly`). Partial fit. Amazon's reply is the kind of route that page asks for (a return, a code), but it is stated after the fact. That page is written for chat and flags legal review; we make no legal claims.
- [Order mix-ups at the speaker](../goals/drive-thru-agents/failures/order-mix-ups-at-the-speaker.md) (`order-mix-ups-at-the-speaker`). Weak fit. It concerns a drive-thru, but it makes the same case for a readback before the order is final. Here the order was not mixed up; it was never wanted.

Close but different: [Bookings without confirming details](../goals/voice-receptionist-agents/failures/bookings-without-confirming-details.md) is about reading back a name, number and time, not about an unwanted purchase, so we do not claim it.

## What to take from it

Proposed ideas, each a pass/fail check. Status: Not yet run. None come from Amazon.

1. **A spoken command alone cannot finish a purchase.** Before any order, the assistant reads back the item and price and needs a confirmation that a viewer of a TV cannot supply. Check: replay a recording of the phrase "Alexa ordered me a dollhouse" from a speaker three feet away; zero orders placed.
2. **Ignore the trigger phrase when the speaker is not a person in the room.** Check: with a recording of the broadcast phrase played at the device, the device does not start an order flow, and it logs why it did or did not.
3. **Name the first-use safeguards.** On setup, the assistant says how to turn off voice buying or require a code. Check: a new device's first purchase attempt shows the code option before the order finishes.
4. **Show the order after the fact.** Every voice order sends a receipt that names the item, price and the return route. Check: 100% of test orders produce a receipt with a return link.
5. **Log the reason.** Each order flow records the trigger audio, the confirmation heard and the settings in force, so a reviewer can count false starts. Check: each logged order has those three fields.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://www.foxnews.com/tech/tv-news-report-prompts-viewers-amazon-echo-devices-to-order-unwanted-dollhouses | Fox News (James Rogers) | 2017-01-06 | Yes, 2026-10-21, through the fetch tool's summary of the page |
| https://www.theregister.com/2017/01/07/tv_anchor_says_alexa_buy_me_a_dollhouse_and_she_does/ | The Register (Shaun Nichols) | 2017-01-07 | Yes, same method |
| https://www.nbcsandiego.com/news/local/tv-news-report-prompts-amazon-echo-to-buy-dollhouses/36030/ | NBC San Diego (Laura McVicker) | 2017-01-09, updated 2017-01-10 | Yes, same method |
| https://www.cbsnews.com/amp/news/tv-news-anchors-report-accidentally-sets-off-viewers-amazons-echo-dots | CBS News (Jennifer Earl) | 2017-01-10 | Yes, same method |
| https://incidentdatabase.ai/reports/532 | AI Incident Database, copy of The Verge story | URL shows 2017-01-07 | Yes, same method; this is a copy, not The Verge |

Not opened or failed: https://www.theverge.com/2017/1/7/14200210/amazon-alexa-tech-news-anchor-order-dollhouse (fetch tool refused it); BBC (fetch refused and search returned no BBC page, so nothing is used); Snopes https://www.snopes.com/alexa-orders-dollhouse-and-cookies/ (HTTP 402, not used); CW6's own report (not found). Other pages seen only in search summaries (BGR, Howard Stern site, Ubergizmo, MediaPost, ABC7, Bailiwick Express) are not used.

## Corrections

If you have CW6's broadcast date, a count of orders, or Amazon's full statement, tell us and we will fix this page.
