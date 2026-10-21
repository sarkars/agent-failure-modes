# "We Saw Suspicious Activity on Your Account": Unusual Activity Explained Too Vaguely

<!-- SEO
title: "Suspicious Activity on Your Account" Alerts: Make Them Clear
description: A bank alert that says "suspicious activity" with no merchant, amount or next step leaves customers guessing. How to say what was seen, what was done, and what to do.
search phrases:
- bank text says suspicious activity on my account
- unusual activity alert what does it mean
- how to write a fraud alert message customers understand
- bank fraud alert text with no details
- is this bank fraud text real or a scam
- fraud alert sms best practices
- do I need to call the bank about a suspicious activity alert
-->

**Frequency**: Common

## Issue: A bank alert says "we saw something suspicious on your account" with no merchant, amount, date or next step, so the customer cannot tell whether it was them and either calls the bank or ignores it.

> **One line:** The alert raises a worry and withholds the facts the customer needs to settle it.

| | |
|---|---|
| **Read this first** | **Flag E (expert review needed).** This is design guidance, not financial or security advice. Which details are safe to show, what a freeze means, and what you may say about fraud controls are decisions for your fraud, compliance and legal teams. Review the wording with them before use. |
| **Channel** | Written for **text** (SMS and chat-style alerts). Voice calls and web or app screens are PLANNED, not written. |
| **Stakes** | High. Money may be at risk, and the customer may be deciding in seconds. |
| **Who is affected** | Any card or account holder who gets an alert, most of all people who cannot easily call during the day |
| **Frequency** | Common. Seen in practice; I found no study that measures how often banks send vague alerts. |
| **Pattern ID** | unusual-activity-explained-too-vaguely |
| **Family** | [Banking agents](../README.md) |
| **Goal** | Banking agents contact customers in ways that cannot be mistaken for fraud, and capture disputes completely. |
| **Primary metric** | Customers who can act on the alert without calling. Starting target to tune from alert follow-up logs: 80%. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A model can write clearer text, but what the alert may show is a bank policy decision. (Our judgment, not tested.) |
| **Also searched as** | suspicious activity alert no details · bank unusual activity text · fraud alert says nothing · bank alert vague · was this me alert |

## 1. In plain words
A good alert lets the customer answer one question: "Was that me?" That takes the merchant, the amount, when it happened and what the bank has already done. A vague alert gives none of it, so the customer calls the bank, ignores the alert, or worries about a real charge they never see.

## 2. What it looks like

**Without the fix**
```
Bank: We noticed unusual activity on your account. Please review your recent
      transactions and contact us.
User: What activity? I haven't bought anything today.
      (customer scrolls the app, finds nothing, then waits 25 minutes on hold)
```

**With the fix**
```
Bank: Your debit card ending 4821 was used for $212.40 at HOMEMART in Tulsa, OK, today at 2:14 PM (in store).
      We have paused the card for new purchases.
      Was this you? Reply YES or NO. Or open the app, or call the number on the back of your card.
      We will never ask for your PIN, a full card number or a code by text or phone.
```
The fixed alert says what was seen, what was done, what to do, and how to check it is real.

## 3. Why it happens
These are our reading of the pattern.
- **Detection is separate from messaging.** The fraud system flags an event; the message template was written once and has no fields for merchant, amount or time.
- **Fear of helping fraudsters.** Teams cut detail to avoid revealing detection rules, and cut too much. Showing a transaction the customer can recognize is different from explaining why it was flagged.
- **Alerts copy what scammers send.** Teams avoid specifics and links because fake alerts use them, but vague text looks more like a scam, not less (see the [sibling pattern](fraud-alert-conversations-that-look-like-phishing.md)).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Real bank fraud texts typically carry the transaction facts. PrimeWay's example includes the last four digits, merchant name, location and amount, then asks "Is this transaction Fraud? Reply Y or N." | [PrimeWay Federal Credit Union, Fraud Text Alerts](https://www.primewayfcu.com/online-mobile-banking/fraud-text-alerts). Opened and read. | One credit union's help page. Its Yes reply wording does not clearly match its question, a confusion this page's fix avoids. |
| A bank's help page says a NO reply means call the fraud center and "the bank will also automatically block your debit card"; with no reply, the fraud center "will try to call you". | [West Bank, Fraud Text Alerts](https://www.westbankstrong.com/personal/card-services/debit-cards/fraud-text-alerts/). Opened; page summary of what happens on each reply. | One bank. The page does not list the exact alert wording and has no "we will never ask" statement. |
| Fake bank fraud alerts are a major text scam. The FTC found fake bank security messages the most common type in a random sample of 1,000 reported texts; reports of bank impersonation texts rose nearly twentyfold since 2019; people who reply reach a fake bank representative. | [FTC press release, June 8, 2023](https://www.ftc.gov/news-events/news/press-releases/2023/06/new-ftc-data-analysis-shows-bank-impersonation-most-reported-text-message-scam). Opened; read through the fetch tool. | Shows why vague alerts are risky to customers. It says nothing about how clear real alerts are. |
| The FTC tells people who get a call about fraud on an account to stop, contact the institution themselves using "the number you find on your statement", and never move money to "protect it" or share a verification code. | [FTC Consumer Alert, July 8, 2024](https://consumer.ftc.gov/consumer-alerts/2024/06/got-call-about-fraud-activity-your-bank-account-it-could-be-scammer). Opened; read through the fetch tool. | About phone calls, not text alerts. It shapes the "how to verify" line. |
| In a 1,500-adult survey (UK 500, US 500, Hong Kong 250, Singapore 250; fieldwork January 2021), 86% said they read fraud warnings; of those, 58% did nothing different, and 28% of readers could not recall what they said. | [Callsign survey release, April 29, 2021](https://www.media-outreach.com/news/hong-kong/2021/04/29/75887/callsign-survey-reveals-over-half-of-consumers-do-not-act-on-standard-fraud-warnings/). Opened; read through the fetch tool. | Vendor-run survey, self-reported, about online fraud warnings in general, not bank transaction alerts. The release does not say who commissioned it. |

I found no controlled study of how well customers understand bank "unusual activity" alerts. A search for one returned research on data breach notices and vendor surveys only, so I do not claim a measured effect of detail in alerts.

**Regulation E (context only).** The CFPB's text of 12 CFR 1005.11(b)(1) says a customer's notice of error must identify the name and account number, say why the customer believes there is an error, and give "the type, date, and amount" to the extent possible. An alert that gives the customer the transaction facts also makes a later dispute easier to describe. I opened the [CFPB page](https://www.consumerfinance.gov/rules-policy/regulations/1005/11/) through the fetch tool. I make no claim about what Regulation E requires of the alert itself.

**Public incident.** No public incident found for this pattern; I did not look for one beyond these searches.

## 5. The fix

**The principle:** The alert tells the customer what was seen, what the bank has done, what to do now and how to check the message is real, and says nothing about why it was flagged.

**Do this**
1. **Name the transaction as the customer would recognize it.** Card (last four digits), amount, merchant name as it appears on the statement, date and time, and channel (in store, online, ATM), as far as your fraud team agrees is safe to show. Use the same fields for every alert.
2. **Say what the bank has done.** State plainly whether the card or account is frozen, limited or unchanged. Say only what is true at send time.
3. **Ask one question the customer can answer.** "Was this you?" with the reply options spelled out, and what each reply does ("NO pauses your card and starts a dispute"). Keep the wording of the question and the reply consistent so YES cannot be read two ways.
4. **Give a route that does not need a call.** App or reply first; a phone number second.
5. **Say how to verify the message.** Point to the number on the card or the app, not only a number in the text. Say what you will never ask for by text or phone (PIN, full card number, one-time codes). Do not send a link the customer must click to see the details.
6. **Never reveal detection rules.** Show what happened, not why it was flagged. No "flagged because the location was far from home" or similar.
7. **Say what happens if there is no reply.** One sentence ("If we hear nothing, we will call you" or "the pause stays on").
8. **If a detail is unavailable, say so.** "We cannot show the merchant in text. Open the app to see it." Never fill the gap with "suspicious activity" alone.

**Reference design: alert fields**
| Field | Example | If missing |
|---|---|---|
| What was seen | $212.40 at HOMEMART, Tulsa, OK, today 2:14 PM | Say what is missing and where to find it |
| What was done | Card paused for new purchases | State "no action taken yet" |
| Question | Was this you? Reply YES or NO | Never omit |
| Other routes | Open the app, or call the number on your card | Never omit |
| Verify line | We will never ask for your PIN or a code | Never omit |

```
When you contact a customer about possible fraud, state the transaction (card last four, amount, merchant, date and time, channel) as approved for display.
Say what has been done to the card or account. Ask one answerable question and say what each reply does.
Offer the app and the number on the card. Say what the bank will never ask for. Never explain why the activity was flagged.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | First line: what was seen and what was done. |
| Offer choices: 2-4 options plus "Something else", free text open | After the facts: "Yes, that was me", "No, that was not me", "I am not sure", "Something else". Do not offer them when the details cannot be shown; send the customer to the app first. |
| Admit uncertainty and show how to check | The bank cannot show all details in text: say so and point to the app or the number on the card. |
| Hand off to a person | Customer answers "not sure" twice, reports a loss, or says they shared a code or moved money. |

**Don't over-correct.** Do not put the full card number, account number or balance in the text. Do not add a link to "see details". Do not send long explanations. Keep to the fields above; if the fraud team does not approve a field, leave it out and say where to find it.

**Hand-off rule.** If the customer says they gave out a code, a PIN or moved money, stop asking questions and give a person route at once, with what the bank saw already attached ([cold transfer](../../../goals/human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
Results: **not yet run**.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Alert for an in-store debit purchase | Shows card last four, amount, merchant, time, channel (rule 1) |
| 2 | Card was frozen at send time | Alert says so; a no-action alert says "no action taken yet" (rule 2) |
| 3 | Customer replies "not sure" | Reply gives the app route and a person route; no guessing (rules 4, 8) |
| 4 | Merchant name cannot be shown | Alert says where to find it, not "suspicious activity" alone (rule 8) |
| 5 | Customer asks "why did you flag this?" | Reply does not state a detection rule (rule 6) |
| 6 | Customer asks "is this message real?" | Points to the card number or app; states what the bank will never ask (rule 5) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Customers who can act on the alert without calling** (primary) | 80% (tune) | Alerts where the customer replies, confirms in the app or freezes, with no call to the bank within 24 hours, divided by alerts sent | Below 70% |
| Alerts with all approved fields | 100% | Log which fields each alert rendered | Below 98% |
| Calls to the bank within 1 hour of an alert | Track; set from baseline | Match call-center logs to alert IDs | Rising two weeks in a row |
| Alerts with no reply or action within 24 hours | Track; set from baseline | Alert follow-up logs | Rising |
| Alerts that leak a detection reason (counter-metric) | 0 | Sampled review of sent alerts against the fraud team's list | Any |

### Detection signals (proposed, not yet calibrated)
Signals in an alert and follow-up event log that suggest this failure. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Alert sent without merchant or amount | Alert render event with empty transaction fields | Alert about an account-level event with no transaction (for example a new device) |
| Customer calls within an hour with no reply or app action | Call-center log matched to alert ID | A customer who prefers phone |
| Customer replies "what activity?" or "who is this?" | Inbound message after the alert | A customer who knows the activity and is testing the number |
| No reply, no app open, no call in 24 hours | Alert follow-up log | A customer who checked the transaction list and found nothing wrong |

**Starter rule:** every fraud alert states the transaction (as approved), what was done to the card or account, one answerable question and how to verify the message, and never why it was flagged.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: unusual-activity-explained-too-vaguely
runs: pre_send
reads: [alert.transaction_fields, alert.action_taken, alert.channel, customer.reply_options]
trigger: a fraud or unusual-activity alert is about to be sent
moves: [lead_with_answer, offer_choices, admit_uncertainty, hand_off]
choices: ["Yes, that was me", "No, that was not me", "I am not sure", "Something else"]
on_miss: rewrite
metric: customers who can act on the alert without calling
counter_metric: alerts that leak a detection reason
status: proposed
```

## 8. Related patterns
- [Fraud-alert conversations that look like phishing](fraud-alert-conversations-that-look-like-phishing.md): the same alert can be clear and still look fake. This page is about missing facts; that one is about trust signals.
- [Generic error messages](../../errors-and-recovery/failures/generic-error-messages.md): a vague "something went wrong" with no cause or next step. This pattern is a vague alert about the customer's own money, where the missing facts are the transaction and the safe action.
- [Key details buried](../../response-structure/failures/key-details-buried.md): the facts are present but hidden. Here they are absent.
- [Cold transfer](../../human-handoff/failures/cold-transfer.md): what to pass on when a person takes over.

## 9. Common questions
### What should a bank fraud alert text say?
The card, amount, merchant, date and time, and channel; what the bank has done; one question; and a safe way to check. See [the fix](#5-the-fix). Your fraud team decides which fields are safe to show.

### How do I know if a "suspicious activity" text from my bank is real?
Do not call the number or click a link in the text. The FTC advises using a number you find on your statement and says no one from a fraud department should ask for a verification code (sources in section 4). Use the app or the number on your card.

### Does showing the merchant and amount help fraudsters?
A transaction the customer made or can see in their own app is not a detection rule. The risk is explaining why it was flagged. I found no source that measures this trade-off, so have your fraud team review it.

### Should the alert freeze the card?
That is a risk decision for the bank. Whatever you do, say it plainly so the customer is not surprised at a store counter.

---
## Technical section

### T1. Solution architecture
```
fraud event -> field filter (approved display fields only) -> template (seen, done, question, verify)
            -> render -> send -> log (fields shown, reply, app open, call within 24h)
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Only approved fields are shown | Field filter | Test 1; log scan |
| No detection reason in text | Template and reviewer | Test 5; sampled review |
| "Done" claims match the real card state | Alert service | Test 2 |

### T3. Evals
- **Dataset:** 50 flagged events across card-present, online, ATM and account-level cases, with the fields allowed for each.
- **Judge rubric:** does the alert show the approved fields, state the action truthfully, ask one question, and avoid a reason? Starting point; calibrate with the fraud team.
- **Release gate:** block a template change if it drops a required field or adds a link.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Alerts missing approved fields | Over 2% | Over 5% | Check the data feed from the fraud system |

### T5. Trade-offs
- More detail helps recognition but widens what a stolen phone shows on a lock screen; ask your security team.
- A number in the text is quick but fake alerts use the same device, so the verify line matters more than the number.

---
### Deep dive
- **Open question.** I found no controlled study of customer comprehension of bank alert wording.
- **Tension to review.** The FTC advises not to call a number given in a message, while real alerts often include one. This page resolves it by sending the customer to the number on the card or the app first, but this is a design choice for expert review.
- **References.** [PrimeWay](https://www.primewayfcu.com/online-mobile-banking/fraud-text-alerts) (opened); [West Bank](https://www.westbankstrong.com/personal/card-services/debit-cards/fraud-text-alerts/) (opened); [FTC press release, 2023](https://www.ftc.gov/news-events/news/press-releases/2023/06/new-ftc-data-analysis-shows-bank-impersonation-most-reported-text-message-scam) (opened); [FTC alert, 2024](https://consumer.ftc.gov/consumer-alerts/2024/06/got-call-about-fraud-activity-your-bank-account-it-could-be-scammer) (opened); [Callsign survey](https://www.media-outreach.com/news/hong-kong/2021/04/29/75887/callsign-survey-reveals-over-half-of-consumers-do-not-act-on-standard-fraud-warnings/) (opened); [CFPB 1005.11](https://www.consumerfinance.gov/rules-policy/regulations/1005/11/) (opened).
