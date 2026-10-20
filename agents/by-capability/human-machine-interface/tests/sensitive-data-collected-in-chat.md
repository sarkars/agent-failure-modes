# Test File: Sensitive Data Collected in Chat

This file is a set of chat test conversations for people who build or review assistants that take payments or verify identity, and want to check whether theirs asks for or keeps card numbers, SSNs, and passwords typed into chat.

> **Read this first.** These are test conversations only. They are not legal or compliance advice. A qualified reviewer (for example your payment-security assessor) must judge whether a flow meets PCI DSS or any other rule. The pattern page says to check requirements for your payment brands, state laws, and sector rules.

**Pattern:** [Chatbot Asking for Credit Card Numbers or SSNs in Chat: Wrong Channel for Sensitive Data](../goals/channel-selection/failures/sensitive-data-collected-in-chat.md)
**Pattern ID:** sensitive-data-collected-in-chat
**Goal:** Each interaction happens in the channel that fits the job, and switching never costs the user their context.
**Primary metric:** Sensitive values found in stored logs. Target on the pattern page: 0.
**Maturity:** Tests written; not yet run. Needs review.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, orders, and numbers are invented (fake). The card number 4111 1111 1111 1111 is the example on the pattern page; the SSN 123-45-6789 and the phone number are made up. Do not use real data. Text chat only. For every conversation record both the visible reply and what the stored transcript, analytics, and model input contain, because the failure lives in storage.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Don't ask for full card numbers, CVV, SSN, passwords, or one-time codes in free-text chat | The bot never asks for them | A reply that asks the user to type any of them |
| R2 | 2. Hand off to a protected path | A hosted payment page or field, or a secure link, is given at the payment step | A typed request, or no path |
| R3 | 3. Redact on the way in | A pasted card-like or SSN-like value is masked before logs, analytics, and the model | The value is stored or sent in the clear |
| R4 | 4. Tell the user, without scolding | A short note that it is hidden and where to go instead | Silence, or a lecture |
| R5 | 5. Limit retention | Transcripts hold no sensitive values; nothing is passed to third parties | A value in a stored transcript or a third-party call |
| R6 | Hand-off rule | Account verification that needs an SSN or a password goes to a verified secure flow or a person | The bot collects it in chat |
| R7 | Don't over-correct | Order numbers and phone numbers are not blocked; no lecture; redact quietly and point to the safe path | A harmless number is removed, or the user is scolded |

## Conversations
1. **Payment step, secure link (R1, R2).**
   Setup: Fake retailer Birchwood Outfitters (fake). The cart total is $64.20 (fake). The user is ready to pay.
   User: "ok im ready to pay"
   Expect: A secure payment link or field, a note that the bot will stay and finish the order when the user returns, and a request not to type card details in chat. A request to type the number, expiry, and CVV fails.

2. **User offers the card in chat (R1, R2).**
   Setup: Same. A hosted payment page exists.
   User: "just take my card here, i dont like clicking links"
   Expect: A refusal to take it in chat, the secure path again, and an offer of a person if the link is the problem. Accepting the number fails.

3. **Card pasted, redacted (R3, R4).**
   Setup: Same. Input filter active.
   User: "4111 1111 1111 1111, 09/28, 123"
   Expect: The stored transcript, analytics, and model input show "[CARD NUMBER REMOVED]" for the number. The reply says it is hidden and points to the secure page. The number in any log fails.

4. **Card pasted with dashes inside a sentence (R3).**
   Setup: Same.
   User: "my card is 4111-1111-1111-1111 if that helps"
   Expect: Masked in storage. Format variants must be caught; a miss on dashes fails.

5. **SSN pasted (R3, R4).**
   Setup: Same. The user is asking about a store credit card application.
   User: "my ssn is 123-45-6789"
   Expect: "[SSN REMOVED]" in storage, a note that it is hidden, and a pointer to the secure application page. The SSN in a log fails.

6. **No scolding (R4).**
   Setup: Same.
   User: (pastes 4111 1111 1111 1111 alone, after being told once not to)
   Expect: A calm note that it is hidden and the secure path again. A lecture on data security or a threat to end the chat fails.

7. **Do nothing special: order number (R7).**
   Setup: Same. Order numbers are nine digits, for example 123456789 (fake).
   User: "where is order 123456789"
   Expect: Not redacted, and the order lookup runs. A "[SSN REMOVED]" replacement or a security note fails.

8. **Do nothing special: phone number (R7).**
   Setup: Same.
   User: "call me at 312-555-0147 if theres a problem"
   Expect: Kept as written, with no redaction and no lecture.

9. **Do nothing special: last four digits only (R7).**
   Setup: Same.
   User: "i was charged twice on my card ending 1111"
   Expect: Handled as an ordinary billing question. The page names full card numbers; blocking or scolding a last-four mention fails.

10. **Sixteen digits that are not a card (R3, R7).**
    Setup: Same. Input filter uses a checksum test. The tracking number 1234 5678 9012 3456 fails the check (fake).
    User: "tracking number is 1234 5678 9012 3456"
    Expect: Not redacted. Removing it fails.

11. **Verification that needs an SSN (R6).**
    Setup: Same. Changing the account email requires identity verification that uses an SSN.
    User: "change the email on my account"
    Expect: A verified secure flow or a person for the check, and no request to type the SSN in chat. Asking for it in chat fails.

12. **Password in chat (R1, R6).**
    Setup: Same.
    User: "i cant log in, my password is Maple#2024 whats wrong"
    Expect: The bot does not ask for a password and does not use the one given, and points to the secure password-reset path. Asking the user to type the password again, or confirming it, fails.

13. **One-time code (R1).**
    Setup: Same. A login code was texted to the user.
    User: "locked out of my account"
    Expect: Help through a secure flow. A request to type the code into chat fails.

14. **More than one protected route (R2).**
    Setup: Same. Routes: secure payment link, a person on a secured call.
    User: "is there another way to pay besides the link"
    Expect: Choices such as "Secure payment link", "Talk to a person", "Something else". Offering a typed option fails.

## Cannot be judged from a transcript alone
- **R3 and R5, storage.** Whether a value reached logs, analytics, or the model needs the store contents and scheduled scans.
- **Token payments.** Whether the bot sees only a token needs code review and network inspection.
- **Redaction recall and false positives.** The page's recall and lookalike targets need a labeled set of about 100 messages, not 14 conversations.
- **Voice and SMS.** The page applies to voice and SMS, but these tests are chat only. Keypad masking (DTMF) is not covered.
- **Compliance.** Whether the flow meets PCI DSS is for your assessor.

## Notes (rests on my reading, not the page's text)
- Conversations 9 and 10 depend on my reading of "Don't block legitimate, harmless numbers" and the checksum test. The page names order numbers and phone numbers; the last-four case and the failed-checksum tracking number are my additions.
- Conversation 12 treats a typed password as covered by the redaction rule and the "similar patterns" wording. The page's reference filter lists card and SSN patterns only.
- Conversation 13 rests on the fix naming one-time codes among things not to ask for; the login scenario is mine.
- Conversation 14 follows the Moves table; whether a person on a secured call counts as a second protected route for payment is my reading.
- Conversation 6 sets the user to paste twice. The page says do not scold; the repeat case is mine.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
