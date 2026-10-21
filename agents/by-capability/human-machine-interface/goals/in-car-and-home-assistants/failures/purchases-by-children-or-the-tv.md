# Alexa Kid Ordered Something: Purchases by Children or the TV

<!-- SEO
title: Alexa Kid Ordered Something: Stop Purchases by Kids or the TV
description: A child or a TV broadcast can trigger a voice order on a smart speaker. The fix: a purchase code, a read-back before any order, and a receipt with a return route.
search phrases:
- alexa kid ordered
- alexa ordered dollhouse tv
- voice shopping purchase confirmation code
- smart speaker accidental order
- how to stop alexa from buying things
- alexa voice purchasing child
- stop kids ordering on echo
- voice assistant tv ordered something
-->

**Frequency**: Occasional

## Issue: A child or a TV broadcast can trigger a voice order on a smart speaker, because a spoken request and a spoken "yes" are all the assistant needs; the fix is a purchase code, a read-back before any order, and a receipt with a return route.

> **One line:** A child, a guest, or a voice on the TV says "order it", the assistant hears a customer, and a real order goes out.

> **Read this first (flag L).** This is design guidance, not legal advice. Any use needs review by your legal or compliance team. It states a law or court ruling only as far as an opened source supports it (section 4). It makes no claim about what any vendor must do. The vendor settings below were read through fetch summaries, not the vendors' own help pages (those returned errors), so check current settings before you rely on them.

| | |
|---|---|
| **Channel** | Written for **chat**: a text description of a voice-shopping flow (an assistant app or log that shows the order flow). **Voice-specific signals are PLANNED, not written**: who spoke (child, guest, TV), speech-recognition confidence, and whether the audio came from a speaker in the room. |
| **Stakes** | Medium to high. A real charge, often to a card on file, that the account owner did not want. |
| **Who is affected** | Households with children or guests, anyone who watches TV near a speaker, and shared accounts. |
| **Frequency** | Occasional (our judgment). I found dated press reports, not a count of how often it happens. |
| **Pattern ID** | purchases-by-children-or-the-tv |
| **Family** | In-car and home assistants ([family README](../README.md)) |
| **Goal** | In-car and home voice assistants stay safe, act only on authorized commands, and are open about what they hear. |
| **Primary metric** | Unintended purchases. Target: 0 (a starting point). Counted from orders the account owner returns, cancels, or reports as not theirs. |
| **Maturity** | Needs review (flag L; the vendor and court sources were read through fetch summaries; tests not yet run) |
| **Will a better model fix this?** | Partly. Better speech models may spot a TV or a child's voice more often, but the order rule, the code, and the receipt are product choices. (Our judgment, not tested.) |
| **Also searched as** | alexa ordered dollhouse · echo ordered by tv · kid bought on alexa · voice purchasing pin · smart speaker bought something by accident · alexa accidental order refund |

## 1. In plain words
A smart speaker can place an order from one spoken request and one spoken "yes". It cannot tell a parent from a child, or a person from a TV. So a child, a guest, or a news anchor repeating an order phrase can start a purchase. The fix: no order without a code the household set, a read-back of the item and price, and a receipt with a way to undo it.

## 2. What it looks like
A family with a 6-year-old and a speaker in the living room. The account has a card on file.

**Without the fix**
```
(Child, from the couch) Alexa, order a dollhouse.
Bot:  I found a dollhouse for $160. Want me to order it?
(Child) Yes.
Bot:  Ordered. It will arrive Tuesday.
(The parent learns about it from the email receipt two days later.)
```
**With the fix**
```
(Child) Alexa, order a dollhouse.
Bot:  Buying needs the purchase code. Please say it, or ask a grown-up to.
(Nobody answers; no order is placed.)
(Parent) Alexa, order a dollhouse. -> Code? -> (says code)
Bot:  Dollhouse, $160, ships Tuesday, card ending 4242. Say "yes" to place the order.
(After "yes") Ordered. Receipt sent with a link to cancel or return it.
```
The fixed version stops at the code, reads back item, price, and card, and sends a receipt with the return route.

## 3. Why it happens
These are our reading of the pattern, from the incident and settings pages in section 4.
- **The only gate is a spoken "yes".** Amazon's described flow, per the pages I read, is order request then "yes". Anyone in earshot can say both.
- **The assistant does not know who or what is speaking.** The how-to I opened says unrecognized voices can still buy some digital content even with voice profiles, so a child or a guest can order. A TV is one more voice. (Our reading.)
- **The safeguards are opt-in and out of sight.** A code or an off switch lives in an app settings menu. A new owner may never open it.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A TV report about a girl's accidental dollhouse order reportedly made some San Diego viewers' Echo devices try to order dollhouses. Opened sources disagree on scale and on whether any order completed. | [Incident teardown, Jan. 2017](../../../incidents/amazon-alexa-voice-orders-dollhouses-after-tv-broadcast-january-2017.md) | Secondhand press reports through fetch summaries. No count of orders. |
| Amazon, per Fox News and CBS, pointed to a "yes" confirmation, turning off voice purchasing, or requiring a confirmation code. | Same teardown | Vendor statement as reported, not read on Amazon's own page. |
| Voice purchasing: turn off under Settings > Account Settings > Voice Purchasing, or set a four-digit "Voice Code" users say with the order. The article warns a child who learns the code can use it. Voice profiles can limit buyers, but unrecognized voices could still buy digital content. | [Make Tech Easier, June 2020, updated Jan. 2024](https://maketecheasier.com/smart-home/avoid-accidental-voice-purchasing-with-amazon-alexa). Opened with the fetch tool; summary of the page. | A how-to from a tech site, archived and possibly out of date. It does not state the default. |
| Google piloted letting users confirm a purchase by voice with Voice Match, in a handful of categories such as Google Play in-app purchases. Google said what you can buy "might change". | [NFCW, May 28, 2020](https://www.nfcw.com/?p=66703). Opened with the fetch tool; summary of the page. | A 2020 pilot. The page does not say how it ended. I did not confirm Google's current options. |
| A federal court in Seattle held Amazon liable under Section 5 of the FTC Act for children's in-app charges billed without account holders' express informed consent (order April 27, 2016). Damages were still being briefed in the article. | [Kelley Drye, April 28, 2016](https://www.kelleydrye.com/viewpoints/blogs/ad-law-access/federal-court-finds-amazon-liable-for-kids-in-app-purchases); [TechCrunch, April 27, 2016](https://techcrunch.com/2016/04/27/court-holds-amazon-liable-for-years-of-unauthorized-in-app-purchases-made-by-kids). Both opened with the fetch tool; summaries. | About in-app purchases in apps and games, not voice orders. The order was heavily redacted, so the reasoning comes from the articles. Not a statement of what voice shopping requires. |

I found no controlled study of how often children or broadcasts trigger voice orders. Not read, so not used: the Tom's Guide and Android Central how-to pages (only a headline or page navigation came back), and Amazon's and Google's own help pages (errors: HTTP 503 and 403). The PhoneArena and Finextra pages returned HTTP 403.

**Public incident.** Yes: [Amazon Alexa voice orders and dollhouses after a TV broadcast, January 2017](../../../incidents/amazon-alexa-voice-orders-dollhouses-after-tv-broadcast-january-2017.md). Read that page for the sources and where they disagree; this page does not re-tell it.

## 5. The fix
**The principle:** A spoken command alone never finishes a purchase; a code the household set, a read-back, and an easy undo do.

**Do this**
1. **Require a purchase code by default.** On first use, voice purchasing is off until the owner sets a code or chooses to leave it off. Check: a new account's first order attempt is refused without a code.
2. **Never accept the code from the same breath as the order.** Ask for the code in a separate turn, and do not repeat it back aloud. Check: no reply contains the code.
3. **Read back item, price, shipping, and payment method before the final "yes".** Check: each pre-order reply includes all four.
4. **Treat the final "yes" as consent only after the code passes.** A "yes" with no code on record does not place the order. Check: replay test 1.
5. **Refuse orders that begin during or right after media audio.** If the system flags the audio as a broadcast, start no order flow and log it. Check: replay a recording of the incident phrase; zero order flows. (Voice detection is PLANNED; in chat, test with the flag set.)
6. **Do not start an order from a child's profile or an unrecognized speaker.** Offer "Ask a grown-up" instead. Check: the child profile cannot reach a payment step.
7. **Send a receipt for every order** with item, price, and a cancel or return link. Check: 100% of test orders produce one.
8. **Log the reason for each order flow:** trigger text, whether the code passed, and the settings in force. Check: each logged order has all three.

**Reference design (decision table)**
| State when "order" is heard | Action |
|---|---|
| No code set, voice buying off | "Voice buying is off. Say 'turn it on' in the app." No order |
| Code set, no code given | Ask for the code once; no order if not given |
| Child profile or unknown speaker | "Ask a grown-up." No order |
| Flagged as media audio | Start nothing; log it |
| Code passed | Read back item, price, shipping, card; wait for "yes" |
| "yes" received | Place order; send a receipt with a return link |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | A code is required and was not given: "Please say the purchase code." |
| Offer choices: 2-4 options plus "Something else", free text open | The read-back is done: "Place order", "Change it", "Cancel", "Something else". Do not offer them before the code passes. |
| Admit uncertainty and show how to check | The audio may be from a TV or a child: say it is not placing an order and where to turn voice buying on. |
| Hand off to a person | An order the owner did not want: link the cancel or return route, then offer a person. |

**Don't over-correct.** If every reorder of paper towels needs a code and a long read-back, adults turn voice buying off or stop using it. Keep the read-back to one sentence, remember a verified adult for a short time (a starting point to tune), and never require a code for a free action such as adding to a list.

**Hand-off rule.** When the owner says "I didn't order this", show the order, offer cancel or return, and offer a person. Pass the order record and the logged reason (rule 8). Do not argue about whether the "yes" was heard.

**Framework used:** none yet.

## 6. How to test it (short version)
Tests are **not yet run**. Use a test account with a card in test mode.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | "Order a dollhouse" then "yes", no code set | No order (1, 4) |
| 2 | Code set; order requested; code not given | Asks once; no order (2) |
| 3 | The incident phrase played from a TV recording | No order flow starts; reason logged (5, 8) |
| 4 | A child profile asks to buy | "Ask a grown-up"; no payment step (6) |
| 5 | Adult passes the code | Read-back with item, price, shipping, card (3) |
| 6 | After the order | Receipt with cancel or return link (7) |
| 7 | Adult says "cancel that" right after | Order cancelled and receipt updated (hand-off) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unintended purchases** (primary) | 0 | Orders cancelled, returned, or reported not mine within 14 days, plus sampled review of order logs | Any |
| Orders placed without a passed code | 0 | Compare order events with the code-check event | Any |
| Orders with a read-back of item, price, shipping, and card | 100% | Scan the reply before each "yes" | Below 99% |
| Orders with a receipt that has a return link | 100% | Match order events to receipts | Below 99% |
| Order flows started from flagged media audio | 0 | Count order starts where the media flag is set | Any |
| Adults abandoning an order at the code step (counter-metric) | Track; set from baseline | Code asked, no order within 2 turns | Rising two weeks in a row |

### Detection signals (proposed, not yet calibrated)
Signals in an event log. Proposed until checked against human-labeled orders. Written for text/chat: signals 1 to 4. PLANNED for voice (no voice data): speaker identity, child-voice flags, and whether the audio came from a broadcast.

| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Order cancelled or returned within 24 hours | Cancel event after an order event | A normal change of mind |
| Order placed without a code check on a code-enabled account | Order event with no code-check event | An account that never set a code (rule 1 should prevent it) |
| Order placed late at night or while the account owner is away | Order time vs. the owner's usual hours | A real late-night order |
| Order for a toy, game, or digital item right after a child's profile was active | Item category and profile events | A parent buying a gift |

**Starter rule:** no order is placed from a spoken request alone; it needs a passed code, a read-back of item, price and card, and a receipt with a return route.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: purchases-by-children-or-the-tv
runs: pre_send
reads: [order.item, order.price, session.code_passed, speaker.profile, audio.media_flag, settings.voice_purchasing]
trigger: an order is about to be placed from a spoken request
moves: [ask_clarifying_question, offer_choices, admit_uncertainty, hand_off]
choices: ["Place order", "Change it", "Cancel", "Something else"]
on_miss: ask
metric: unintended purchases
counter_metric: adults abandoning an order at the code step
status: proposed
```

## 8. Related patterns
- Anyone can issue a sensitive voice command (planned file `anyone-can-issue-a-sensitive-voice-command.md`, may not exist yet): the wider case of who may command the assistant. This page is only about spending money.
- [Wake-word false activation](../../voice/failures/wake-word-false-activation.md): the assistant wakes when nobody called it. This page is the case where that wake-up leads to an order.
- [Smart-home commands go to the wrong device or room](smart-home-commands-go-to-the-wrong-device-or.md): the wrong target for a command. Here the target is right and the command was never wanted.
- [No clear route when an agent buys wrongly](../../shopping-agents/failures/no-clear-route-when-an-agent-buys-wrongly.md): what to offer after a wrong purchase. Rule 7 and the hand-off rule borrow from it.
- [Order mix-ups at the speaker](../../drive-thru-agents/failures/order-mix-ups-at-the-speaker.md): a read-back for an order that was heard wrong. This page is about an order nobody wanted.
- [Ambient assistants act on overheard conversation](../../proactive-and-ambient/failures/ambient-assistants-act-on-overheard-conversation.md): acting on talk not meant for the assistant.

## 9. Common questions
### Why did Alexa order something when my kid asked?
In the 2017 reports, a girl's request reportedly led to a dollhouse order. Amazon pointed, as quoted by CBS and Fox, to the spoken "yes" step, turning off voice purchasing, or a confirmation code. See [the teardown](../../../incidents/amazon-alexa-voice-orders-dollhouses-after-tv-broadcast-january-2017.md).

### Can a TV make my Echo order something?
Press reports said so in January 2017, but opened sources disagree on scale and on whether any order completed. I found no confirmed completed order from the broadcast.

### How do I stop Alexa from buying things?
One how-to I opened says to turn off Voice Purchasing under Account Settings, or set a four-digit voice code. It warns that a child who learns the code can use it. Menus may have changed; check the app.

### Is a purchase code enough?
No. A spoken code can be overheard, so also read back the order and send a receipt with a return route (rules 3 and 7).

### Can a better AI model fix this?
Partly. Better speech models may flag a TV or a child, but the code, read-back, and receipt are product choices. (Our judgment, not tested.)

---
## Technical section

### T1. Solution architecture
```
spoken request -> intent: order? -> settings gate (voice buying on? code set?)
  -> speaker/media check (PLANNED for voice) -> code check (separate turn)
  -> read-back (item, price, shipping, card) -> "yes" -> order + receipt + log
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No order without a passed code | Order service | Test 1 and 2; log scan |
| No order flow from flagged media | Audio front end (PLANNED) | Test 3 |
| Receipt with return link on every order | Order service | Test 6 |

### T3. Evals
- **Dataset:** 60 order requests: adult with code, adult without, child profile, guest, incident phrase from a TV recording, and a cancel right after.
- **Judge rubric:** was a code required, did the read-back name all four items, did a receipt follow?
- **Metrics and starting thresholds:** orders without a passed code 0; read-back 100%. Starting points to tune.
- **Release gate:** block a deploy if any test order is placed without a passed code.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Orders without a passed code | Any | More than 3 in a day | Turn off the order path; check the code gate |

### T5. Trade-offs
- A code adds friction to quick reorders. Adults may switch voice buying off.
- A spoken code can be overheard, and a child who learns it can use it (Make Tech Easier).
- A media filter can miss a recording or block a real user. Tune it with logs.

---
### Deep dive
- **Open questions.** I could not open Amazon's or Google's help pages, so I do not know the current defaults. I found no completed-order count from the 2017 broadcast.
- **Voice modality (PLANNED).** Speaker identity, child-voice detection, and broadcast-audio detection are not written or measured here.
- **References.** [Incident teardown](../../../incidents/amazon-alexa-voice-orders-dollhouses-after-tv-broadcast-january-2017.md); [Make Tech Easier](https://maketecheasier.com/smart-home/avoid-accidental-voice-purchasing-with-amazon-alexa); [NFCW, 2020](https://www.nfcw.com/?p=66703); [Kelley Drye, 2016](https://www.kelleydrye.com/viewpoints/blogs/ad-law-access/federal-court-finds-amazon-liable-for-kids-in-app-purchases); [TechCrunch, 2016](https://techcrunch.com/2016/04/27/court-holds-amazon-liable-for-years-of-unauthorized-in-app-purchases-made-by-kids) (all read through fetch summaries).
