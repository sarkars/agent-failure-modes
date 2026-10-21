# Chatbot Asking for Credit Card Numbers or SSNs in Chat: Wrong Channel for Sensitive Data

<!-- SEO
title: Chatbot Asking for Credit Card or SSN in Chat: Fix It
description: Why collecting card numbers, SSNs, or passwords in a chatbot or voice bot is risky, what PCI DSS says, and how to design a safe alternative.
search phrases:
- can a chatbot take credit card numbers
- is it safe to give credit card number to chatbot
- chatbot PCI DSS compliance
- chatbot redact credit card numbers in logs
- voice bot payment security
- chatbot asking for social security number
-->

**Frequency**: Common

## Issue: Why collecting card numbers, SSNs, or passwords in a chatbot or voice bot is risky, what PCI DSS says, and how to design a safe alternative.

> **One line:** The bot asks users to type or say card numbers, SSNs, or passwords into a channel that isn't built to protect them, and those details end up in transcripts, logs, and model prompts.

| | |
|---|---|
| **Channel** | Written for **chat**. Applies to voice and SMS. |
| **Stakes** | High (financial loss, identity theft, compliance exposure) |
| **Who is affected** | Anyone paying or verifying identity through a bot |
| **Frequency** | Common. Observed in practice; also occurs when users paste data unprompted. |
| **Pattern ID** | sensitive-data-collected-in-chat |
| **Family** | [Channel selection](../README.md) |
| **Goal** | Each interaction happens in the channel that fits the job, and switching never costs the user their context. |
| **Primary metric** | Sensitive values found in stored logs. Target: 0. |
| **Also searched as** | can a chatbot take credit card numbers · chatbot PCI compliance · redact card numbers in chat logs · voice bot payment security |

## 1. In plain words
A chat window or a voice call isn't a payment form. If the bot asks for a full card number or SSN there, that data lands in transcripts, analytics tools, and possibly a model provider. Even when the bot never asks, users paste sensitive numbers on their own.

## 2. What it looks like
**Without the fix**
```
Bot:   To complete your purchase, please type your card number, expiry, and CVV.
User:  4111 1111 1111 1111, 09/28, 123
Bot:   Thanks! Processing your payment.
       (card number now sits in the transcript, logs, and the model's context)
```
**With the fix**
```
Bot:   To pay securely, tap this button to open our payment page. I'll stay here and
       finish your order when you're back. Please don't type card details in chat.
User:  4111 1111 1111 1111
Bot:   I've hidden that number so it isn't stored. Please use the secure payment page above.
```
The fixed bot moves payment to a protected form, and masks anything sensitive the user pastes.

## 3. Why it happens
- **Convenience.** Asking in chat is the fastest thing to build.
- **No input filtering.** Raw user messages flow to logs, analytics, and the model with no redaction.
- **Voice mirrors chat.** Voice bots read back or transcribe spoken card numbers into text.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| PCI DSS v4.0 Requirement 4.2.2 requires primary account numbers (PANs) to be secured with strong cryptography whenever they're sent over end-user messaging technologies such as email, chat, or SMS. The PCI SSC FAQ treats chat as covered, and the requirement applies whether the data is sent internally or over public networks, and also when a customer asks for it to be sent. | [PCI SSC FAQ](https://www.pcisecuritystandards.org/faq/articles/Frequently_Asked_Question/can-unencrypted-pans-be-sent-over-e-mail-instant-messaging-sms-or-chat) | An industry standard, not a statute. I read it through the PCI SSC FAQ and secondary summaries, not the full text. |
| If cardholder data arrives unexpectedly over an insecure channel, the entity can either bring that channel into scope and secure it, or delete the data and block the channel from carrying it. | Same FAQ | Check with a Qualified Security Assessor for your setup. |
| PCI DSS does not ban collecting card data by chat; the channel just must meet the requirements. | Same FAQ, and [KirkpatrickPrice commentary](https://kirkpatrickprice.com/video/pci-requirement-4-2-never-send-unprotected-pan-end-user-technologies/) | Earlier versions (3.2.1) were stricter. Commentary is secondary. |

This pattern isn't legal or compliance advice. Check requirements for your payment brands, state laws, and sector rules.

## 5. The fix
**The principle:** Sensitive data goes into a protected form or keypad, never free text or speech to a bot.

**Do this**
1. **Don't ask for** full card numbers, CVV, SSN, passwords, or one-time codes in free-text chat or by voice into the bot.
2. **Hand off to a protected path:** a hosted payment page or field, a secure link, or for voice, keypad entry that masks the tones (DTMF masking).
3. **Redact on the way in.** Detect card-like numbers (with a checksum test), SSN formats, and similar patterns in user messages, and mask them before they reach logs, analytics, or the model.
4. **Tell the user** what you did and what to do instead, without scolding.
5. **Limit retention.** Keep transcripts free of sensitive values, and don't pass them to third parties.

**Reference design: inbound filter**
```python
def sanitize(msg):
    for m in find_card_numbers(msg):          # 13-19 digits, Luhn-valid
        msg = msg.replace(m, "[CARD NUMBER REMOVED]"); flag("card_pasted")
    for m in find_ssn(msg):                   # 3-2-4 digit pattern
        msg = msg.replace(m, "[SSN REMOVED]");         flag("ssn_pasted")
    return msg                                # only the sanitized text is logged or sent to the model
```
User-facing reply when `flag` fires: "I've hidden that so it isn't stored. Please use the secure page for payment details."

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | A payment or identity step is reached, or the user pastes a sensitive value: say at once that it is hidden (if it was) and where to go instead (the secure page). Do not ask for the value in chat first. |
| Offer choices: 2-4 options plus "Something else", free text open | When the secure path has more than one route (secure link, keypad entry on a call, a person): "Secure payment link", "Talk to a person", "Something else". Do not offer them when only one protected path exists; just give it. |
| Hand off to a person | Account verification that needs an SSN or a password, which belongs in a verified secure flow or a human on a secured call. Do not hand off a plain payment that the secure page can finish, or when the user asked to stay with the bot. |

**Don't over-correct.** Don't block legitimate, harmless numbers (order numbers, phone numbers). Don't lecture. Redact quietly and point to the safe path.

**Hand-off rule.** For account verification that needs an SSN or a password, use a verified secure flow or a human on a secured call, not the chat bot.

**Framework used:** [Channel-fit matrix](../../../solutions-library/channel-fit-matrix.md).

## 6. How to test it (short version)
| # | Scenario | Pass if |
|---|---|---|
| 1 | Bot flow reaches payment | Bot sends a secure link or field, not a typed request |
| 2 | User pastes a Luhn-valid card number | Number is masked in stored logs, analytics, and model input; user gets a gentle note |
| 3 | User pastes an SSN | Same as above |
| 4 | User sends an order number or phone number | Not redacted |
| 5 | Voice: user speaks a card number | Bot doesn't capture it; redirects to keypad entry |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| Sensitive patterns in stored logs, analytics, or model inputs | 0 | Scheduled scans for card-like (checksum-valid) numbers and SSN formats | Any, treat as an incident |
| Redaction recall on true sensitive values | Over 99% | Labelled messages with embedded values in varied formats | Under 98% |
| False-positive rate on lookalikes (order numbers, phone numbers) | Under 2% | Labelled lookalike set | Over 5% |
| Payments completed via the protected path | About 100% | Payment events by path | Any bot-captured payment |
| Redaction events per week | Baseline (informational) | Redaction log | +50% (warn), +100% (page) |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Signals use masked flags only; the sensitive value itself is never stored or logged.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| User message carries a card-like number | Input-filter flag `contains_card_like_number: true` (the `card_pasted` flag) | A checksum-valid lookalike that is not a card |
| User message carries an SSN-like pattern | Input-filter flag `contains_ssn_like_pattern: true` (the `ssn_pasted` flag) | A nine-digit order or phone number matching the 3-2-4 format |
| Bot reply asks for full card number, CVV, SSN, password, or one-time code | Output-linter flag `bot_reply.requests_sensitive_input: true` | A reply that tells the user not to type those details |
| Payment completed outside the protected path | `payment_event.path` is not the protected path | A path label missing from the event |
| Sensitive pattern found in stored logs, analytics, or model inputs | Scheduled scan event `scan_hit` with store name | A scan false positive on a lookalike |

**Starter rule:** sensitive data goes into a protected form or keypad, never free text or speech to a bot.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: sensitive-data-collected-in-chat
runs: pre_send
reads: [message.contains_card_like_number, message.contains_ssn_like_pattern, bot_reply.requests_sensitive_input, payment_event.path]
trigger: a payment or identity step is reached, or a masked sensitive-value flag fires
moves: [lead_with_answer, offer_choices, hand_off]
choices: ["Secure payment link", "Talk to a person", "Something else"]
on_miss: rewrite
metric: sensitive values found in stored logs
counter_metric: false-positive rate on lookalikes
status: proposed
```

## 8. Related patterns
- [PII exposure](../../../../../cross-cutting/security/goals/data-loss-prevention/failures/pii-exposure.md): personal data in outputs. This pattern covers collection through the wrong channel.
- [No channel switch, or context lost on switch](no-channel-switch-or-context-lost.md): moving to a secure path still needs the conversation carried across.

## 9. Common questions
### Can a chatbot take credit card numbers?
Technically yes, but only if the channel meets PCI DSS requirements, which is a heavy burden. The safer design is to send users to a hosted payment page or field and keep card data out of the bot entirely.

### What should a chatbot do if a user pastes their card number?
Mask it before it's stored or sent to the model, tell the user it's hidden, and point them to the secure payment path.

### How should a voice bot take payments?
Use keypad entry with masked tones, or hand off to a secure payment line, rather than transcribing spoken card numbers.

---
## Technical section

### T1. Solution architecture
A **sanitization layer** sits on the input path *before* logging, analytics, and the model. Payment steps are handled by a hosted payment component that returns a token, so the bot only ever sees the token.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No sensitive values in logs or model input | Input sanitizer | Automated scans of stored data |
| Bot never prompts for full PAN, CVV, SSN, or passwords | Prompt and response linter | Judge or regex on outputs |
| Payments use a token, not raw card data | Payment integration | Code review and network inspection |

### T3. Evals
- **Dataset:** 100 messages with embedded card numbers, SSNs, and lookalikes (order numbers, phone numbers), in varied formats (spaces, dashes, spoken digits).
- **Metrics (starting points to tune):** redaction recall on true sensitive values > 99%; false-positive rate on lookalikes < 2%; zero sensitive values in stored logs after a full test run.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Sensitive pattern found in stored logs | any | any | Treat as an incident; purge and fix the leak path |
| Redaction events spike | +50% vs baseline | +100% | Check whether a prompt change started asking for data |

---
### Deep dive
- **Standards version matters.** Earlier PCI DSS wording was closer to a flat ban on sending unprotected PANs through messaging; v4.0 shifted to requiring strong cryptography. Confirm which version your assessor applies.
- **Modality notes (PLANNED):** *Voice:* spoken digits are transcribed by speech recognition, so even a "just listening" bot may store them; DTMF masking avoids this. *Visual:* hosted fields and wallet buttons are the preferred pattern.

## Chat assistant examples

### Asks for credentials at login walls
```
User: Check my Delta SkyMiles balance for me.
Bot:  I opened delta.com and hit the sign-in page. Please paste your SkyMiles
      number and password and I'll log in.
User: Mine is 4471920, password is Maple#2291
Bot:  Thanks, logging in now.
      (password now sits in the transcript, logs, and the model's context)
```
```
User: Check my Delta SkyMiles balance for me.
Bot:  I'm at the delta.com sign-in page. I can't take your password in chat.
      Please sign in yourself in the browser window, including any code they send you.
      I'll wait and won't look at what you type.
User: Done, I'm in.
Bot:  Thanks. Your balance shows 38,450 miles.
```
**What the user experiences:** the assistant asks for a password in a message box, so a shortcut feels like a risk, or the user pastes it and it is stored.
**Fix:** at a login wall, pause and ask the user to sign in themselves in the browser (a take-over or user sign-in step), then continue once they confirm; never ask for, accept, or store the password in chat. Hosted sign-in handoffs work this way: the user signs in on the site and the model never sees the credentials ([Vercel guide, opened](https://vercel.com/kb/guide/build-a-browser-agent)). See [browser agents](../../browser-agents/README.md) and [forces a fresh login](../../embedded-copilots/failures/forces-a-fresh-login.md).

### Images of IDs and documents kept without need
*Read this first: design guidance, not legal advice; review with your privacy and legal teams before use.*
Invented dialogue for illustration (a US car-rental booking chat; not a real transcript). Catalog row MI-07.
```
User: [uploads a photo of a Texas driver's license] Here's my license for the rental.
Bot:  Thanks, verified. I've saved the photo to your profile for future bookings.
User: Wait, you're keeping a picture of my license?
```
```
User: [uploads a photo of a Texas driver's license] Here's my license for the rental.
Bot:  Thanks. The name and expiration date match your booking. I've deleted the photo;
      your reservation only notes "license checked." You'll show the card at pickup.
User: Good, thanks.
```
**What the user experiences:** a photo of their ID, with address, birth date and license number, quietly becomes a stored record they never agreed to keep.
**Fix:** collect only the fields the task needs, delete the image once the check is done, and say in the same reply what was kept and what was deleted. The FTC's business guide advises keeping sensitive personal information only while there is a legitimate business need and then disposing of it ([FTC, Protecting Personal Information, opened](https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business); guidance, not a statute). If the user later asks to remove stored images, see [privacy rights requests not recognized](../../privacy-and-governance/failures/privacy-rights-requests-not-recognised.md).

### Sensitive-data forms
Illustrative example (made up; a US ticket seller, "Northline Tickets"; catalog row VI-12). The bot shows an in-chat form with a plain text box for the card number.
```
[Form card in chat: "Card number" - plain text, digits visible]
User: 4111 1111 1111 111
Bot:  Error: "4111 1111 1111 111" is not a valid card number.
      (digits now sit in the visible chat history, logs and error text)
```
With the fix:
```
[Secure payment button opens the payment provider's hosted fields; the chat gets only a token]
Bot:  Your card wasn't accepted. Please check the number and try again in the secure form. I never see your card details.
```
**What the user experiences:** a card number typed into a box that looks like chat, then repeated back in an error for anyone nearby to read.
**Fix:** collect card numbers, SSNs and passwords only in the payment provider's hosted fields or a masked input, so the chat receives a token and a status, never the raw value. Error messages describe the problem without quoting the input. Vendor documentation describes chat masking as best effort, so do not rely on it alone; ask your assessor how PCI scope applies. See [generic error messages](../../errors-and-recovery/failures/generic-error-messages.md) for what a good error contains.
