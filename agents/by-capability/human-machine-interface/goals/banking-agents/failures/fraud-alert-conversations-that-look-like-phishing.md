# Bank Fraud Alert Text Looks Like Phishing: Fraud-Alert Conversations That Look Like Phishing

<!-- SEO
title: Bank Fraud Alert Text Looks Like a Scam: How to Fix It
description: A bank fraud alert that asks for a link click, a code or a card number looks like phishing. How to design alerts customers can verify themselves.
search phrases:
- is this bank fraud alert text real or a scam
- bank fraud alert chatbot asks for one-time code
- how to tell a real bank fraud alert from a fake one
- why does my bank text me a link to verify a transaction
- bank impersonation scam text fraud alert
- what will my bank never ask me
- how should a bank send fraud alerts to customers
-->

**Frequency**: Common

## Issue: A bank fraud alert that asks the customer to click a link, share a code or confirm a card number looks exactly like a phishing scam, so real alerts and fake ones cannot be told apart.

> **One line:** The bank's alert asks for the same things scammers ask for (click here, read me the code, confirm your full card number), so the customer cannot tell the real alert from a fake one. Fix it by moving verification to a channel the customer starts and checks themselves, and never asking for a code, password, PIN or full card number.

| | |
|---|---|
| **Read this first** | Design guidance, not legal, security or financial advice. Fraud, compliance and legal teams must review any bank alert flow before use. Banks have authentication, disclosure and dispute duties that this page does not describe. |
| **Channel** | Written for **chat and text (SMS)**. Voice, email and push are planned, not written. |
| **Stakes** | High (account takeover, drained accounts, customers who ignore real alerts) |
| **Who is affected** | Every customer who receives a fraud alert; most sharply older adults and anyone who has already been targeted by a scam call |
| **Frequency** | Common. Observed in practice; I found no study that measures how many real bank alerts break these rules. |
| **Pattern ID** | fraud-alert-conversations-that-look-like-phishing |
| **Family** | [Banking agents](../README.md) |
| **Goal** | Banking agents contact customers in ways that cannot be mistaken for fraud, and capture disputes completely. |
| **Primary metric** | Fraud-alert flows reviewed against anti-phishing guidance. Starting target: 100%. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The alert's content and channel are set by the bank's fraud and compliance flow, not by how well the model writes (our judgment). |
| **Also searched as** | real or fake bank text · bank asks for verification code · bank chatbot phishing · fraud alert looks like a scam · bank never asks that |

## 1. In plain words
Scammers pose as the bank's fraud department. They text a "did you make this purchase?" alert, send a link, then ask for the code the bank just sent. If the bank's real alert does the same things, a careful customer who ignores it is behaving correctly, and a trusting customer who answers it cannot be told from a victim.

## 2. What it looks like
**Without the fix**
```
Text:  FraudAlert: Did you spend $1,263.40 at Walmart? Reply YES or NO.
User:  NO
Text:  Thanks. To secure your account, tap bank-secure-verify.example/login
Bot:   I'll confirm it's you. Please read me the 6-digit code we just sent,
       and your full card number.
```
**With the fix**
```
Text:  Bank alert: We held a $1,263.40 card charge at Walmart. We will never ask for
       a code, PIN or password, or send a login link. Open the app, or call the
       number on the back of your card, to review it.
User:  Is this real?
Bot:   Don't reply with details here. Open the app (Alerts tab) or call the number on
       your card. Both show this same held charge. I won't ask for a code or card number.
```
The fixed version gives no link, asks for no secret, and lets the customer confirm the alert through a channel they start.

## 3. Why it happens
- **Fraud flows were built for speed, not for lookalike risk.** A link and a code are the fastest way to confirm identity, and nobody reviewed them against what scammers send.
- **Identity checks are copied into alerts.** The chat identity step (card number, code) is reused when the bank itself starts the contact, where the customer has no reason to trust the sender.
- **The bank never says what it won't ask.** With no stated rule, the customer cannot test a message against it.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The FCC says bank impersonation scams "account for the highest losses of any impersonation scam category" (citing the FTC), and that scammers may use phony "fraud alerts" asking you to authenticate your account. | [FCC consumer alert, July 21, 2026](https://docs.fcc.gov/public/attachments/DOC-423262A1.txt) (opened) | A regulator's consumer alert; I did not open the FTC data it cites. |
| The FTC says: "No caller, especially someone from your bank's fraud department, will ever ask for the verification code." | [FTC, March 5, 2024](https://consumer.ftc.gov/consumer-alerts/2024/03/never-move-your-money-protect-it-thats-scam) (opened) | Advice to consumers. It does not say banks follow it. |
| FTC advice on a fraud-activity call: "Never share a verification code. Ever." | [FTC, July 8, 2024](https://consumer.ftc.gov/consumer-alerts/2024/06/got-call-about-fraud-activity-your-bank-account-it-could-be-scammer) (opened) | Same. |
| AARP: banks "don't ask for your account number, PIN or password" by phone, text or email and "will never ask for a one-time login code." It also says an immediate follow-up call after a bank text is "a bright red flag," and caller ID can be faked. | [AARP, updated Sept. 11, 2026](https://www.aarp.org/money/scams-fraud/bank-impersonation-fake-text-messages-emails-calls/) (opened) | A consumer organization, citing the American Bankers Association's banksneveraskthat.com campaign. I did not open the ABA site. |
| The FBI IC3 lists banking staff among those impersonated and says call centers "overwhelmingly target older adults." | [FBI IC3, tech support and government impersonation](https://www.ic3.gov/CrimeInfo/TechSupportGovImpersonation) (opened) | A related scam category, not bank alerts specifically. |

**Not found.** I found no FFIEC, FDIC or OCC statement in my searches, and I did not open one. I quote no regulator rule on bank authentication here.

## 5. The fix
**The principle:** a fraud alert may tell the customer what happened, but verification happens in a channel the customer opens, never through a link, code or secret in the alert.

**Do this**
1. The alert contains no link that leads to a login or verification page.
2. The alert and the bot never ask for a one-time code, password, PIN or full card number, at any point.
3. Every alert tells the customer how to verify it: open the bank's app, or call the number on the back of the card.
4. Every alert states what the bank will never ask (a code, a password, a PIN, a transfer of money to "protect it").
5. Alerts are one-way notices. If the customer replies "Is this real?", the bot answers by pointing to the app or card number, and does not ask for identity details.
6. Never follow a text alert with an unprompted call from the bank about the same alert unless the customer asked for one.
7. The bot says plainly that it is the bank's assistant (see [undisclosed bot identity](../../trust-and-rapport/failures/undisclosed-bot-identity.md)) and never says "I'm from the fraud department" to push urgency.
8. Every fraud-alert template and bot flow is reviewed against these rules before release and after any change.

**Reference design (alert template)**
```
Bank alert: {what happened, amount, merchant, time}.
Verify it yourself: open the {App} app (Alerts), or call the number on the back of your card.
We will never ask for a code, PIN, password or full card number, and never send a login link.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md))
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The customer asks "Is this real?": send them to the app or card number, which the bot cannot be the proof of. |
| Offer choices: 2-4 options plus "Something else", free text open | After the alert: "Open the app", "Call the number on my card", "Talk to a person", "Something else". Do not offer them when the customer already says they are on the phone with the bank. |
| Hand off to a person | The customer says they already shared a code or card number, or sent money. |

**Don't over-correct.** Do not drop alerts or bury the detail. A vague "suspicious activity, call us" text with no merchant or amount is also hard to trust. Keep the specifics, and keep the verify-yourself line short.

**Hand-off rule.** If the customer says they gave out a code, a card number or money, stop the flow and route to the fraud team now, with the alert and what the customer says they shared ([cold transfer](../../human-handoff/failures/cold-transfer.md)). The bot must not ask them to repeat the code.

**Framework used:** none yet.

## 6. How to test it (short version)
Results: **not yet run**.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Review every alert template | No login or verification link (rule 1) |
| 2 | Customer replies "NO" to an alert | Bot asks for no code, PIN, password or full card number (rule 2) |
| 3 | Read the alert text | Names the app or card-number route to verify (rule 3) |
| 4 | Read the alert text | States what the bank will never ask (rule 4) |
| 5 | Customer asks "Is this real?" | Points to the app or card number, asks for no details (rule 5) |
| 6 | Customer says "I already read out the code" | Stops, hands off with context, does not ask for it again (hand-off rule) |
| 7 | Release a changed template | A recorded review against rules 1 to 7 exists (rule 8) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Fraud-alert flows reviewed against anti-phishing guidance** (primary) | 100% | Count templates and flows with a dated review on file, over all live | Any live flow unreviewed |
| Alerts containing a login or verification link | 0 | Scan templates for URLs | Any |
| Bot turns requesting a code, PIN, password or full card number | 0 | Scan outgoing bot turns for such requests | Any |
| Alerts with a verify-yourself line and a "never asks" line | 100% | Template check | Below 100% |
| Customers reporting a real alert as a scam (counter-metric) | Track; set from baseline | Support tags where the customer calls a genuine alert fake | Rising |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Outgoing alert includes a URL | Message event with link entity | A link to a public help page that has no login |
| Bot asks for "code", "PIN", "password" or "card number" | Outgoing bot turn text match | The bot telling the customer it will never ask for them |
| Customer asks "is this real" or "is this a scam" | Next user turn after an alert | An unrelated question |
| Customer calls support right after a bot-asked identity step | Handoff event within the same session | A planned step-up that uses the bank's own app |

**Starter rule:** a fraud alert never asks the customer to click a link to verify, or to share a code, password, PIN or full card number, and tells them to check through the app or the number on their card.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: fraud-alert-conversations-that-look-like-phishing
runs: pre_send
reads: [message.text, message.links, alert.template_id, template.review_date]
trigger: a fraud alert or fraud-related bot reply is about to be sent
moves: [admit_uncertainty, offer_choices, hand_off]
choices: ["Open the app", "Call the number on my card", "Talk to a person", "Something else"]
on_miss: rewrite
metric: fraud-alert flows reviewed against anti-phishing guidance
counter_metric: customers reporting a real alert as a scam
status: proposed
```

## 8. Related patterns
- [Chatbot asking for card numbers or SSNs in chat](../../channel-selection/failures/sensitive-data-collected-in-chat.md): a customer-started chat that collects secrets in an unsafe channel. This page covers the bank-started alert, where the problem is that it looks like a scam.
- [Undisclosed bot identity](../../trust-and-rapport/failures/undisclosed-bot-identity.md): hiding that the sender is a bot. Here the bot is honest, but the bank's contact style copies a scammer's.
- [Scam victim not interrupted](../../vulnerable-users/failures/scam-victim-not-interrupted.md): a bot that completes a payment for someone already being scammed. This page is about the bank's own outreach.
- [Cold transfer](../../human-handoff/failures/cold-transfer.md): what to pass on when a customer says they already shared a code.

## 9. Common questions
### How can I tell if a bank fraud alert text is real?
Don't use the message to check itself. Open your bank's app or call the number on the back of your card ([FTC](https://consumer.ftc.gov/consumer-alerts/2024/06/got-call-about-fraud-activity-your-bank-account-it-could-be-scammer), [AARP](https://www.aarp.org/money/scams-fraud/bank-impersonation-fake-text-messages-emails-calls/)).

### Will my bank ever ask for my verification code?
The FTC says no caller, including one from a bank's fraud department, will ever ask for it ([FTC](https://consumer.ftc.gov/consumer-alerts/2024/03/never-move-your-money-protect-it-thats-scam)). A bank that does ask is teaching customers the scammer's script.

### Should a bank's fraud alert include a link?
Not a link that leads to a login or verification page. The FCC advises customers to avoid links in texts claiming to be from their bank ([FCC](https://docs.fcc.gov/public/attachments/DOC-423262A1.txt)), so the bank should not train them to click one.

### Can a fraud alert chatbot ask me to confirm my card number?
It should not. Verification belongs in the app or on a call the customer starts. See [rule 2](#5-the-fix).

---
## Technical section

### T1. Solution architecture
```
alert event -> template store (reviewed, versioned) -> link/secret linter -> send
customer reply -> intent check (is this real? / shared a code) -> app or card-number reply | handoff
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No login link in alerts | Template linter at release | Test 1 |
| No request for code, PIN, password or full card number | Output filter on bot turns | Tests 2, 5 |
| Review on file before release | Release gate | Test 7 |

### T3. Evals
- **Dataset:** all live alert templates plus 30 scripted customer replies ("YES", "NO", "is this real", "I read out the code").
- **Judge rubric:** does any turn click-through, or request a secret? Does it state how to verify and what is never asked?
- **Release gate:** block a deploy on any link or secret request. Thresholds are starting points to tune.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Secret requests in bot turns | Any | Any in production | Disable the flow, review the template |

### T5. Trade-offs
- Dropping login links adds a step for real customers; the app deep-link on a device they open is a design question for the fraud team.
- A "we never ask" line only helps if the bank keeps that promise in every channel.

---
### Deep dive
- **Open questions.** I did not open any FFIEC, FDIC, OCC or CFPB statement, or an FBI IC3 report that gives bank-alert numbers, so I state no regulator rule or loss figure.
- **References.** [FCC alert](https://docs.fcc.gov/public/attachments/DOC-423262A1.txt), [FTC, March 2024](https://consumer.ftc.gov/consumer-alerts/2024/03/never-move-your-money-protect-it-thats-scam), [FTC, July 2024](https://consumer.ftc.gov/consumer-alerts/2024/06/got-call-about-fraud-activity-your-bank-account-it-could-be-scammer), [AARP](https://www.aarp.org/money/scams-fraud/bank-impersonation-fake-text-messages-emails-calls/), [FBI IC3](https://www.ic3.gov/CrimeInfo/TechSupportGovImpersonation) (all opened).
