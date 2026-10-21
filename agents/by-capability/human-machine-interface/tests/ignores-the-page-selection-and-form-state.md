# Test File: Ignores the Page, Selection, and Form State

This file is a set of test conversations for people who build or review assistants embedded in a product (side panel, help widget, copilot) and want to check whether theirs uses what the product already knows (the page, the selected text, the focused field, the form values) instead of asking the user to describe the screen.

> **Read this first.** These are test conversations only. They are not security, privacy, or financial advice. All products, people, cards, and numbers are invented (fake). Conversation 8 uses fake password and card values only to check that they do not reach the assistant or come back in a reply; which fields may be shared is a decision for your own security and privacy reviewers.

**Pattern:** [Chatbot Doesn't Know What Page I'm On: Ignores the Page, Selection, and Form State](../goals/embedded-copilots/failures/ignores-the-page-selection-and-form-state.md)
**Pattern ID:** ignores-the-page-selection-and-form-state
**Goal:** An assistant built into a product helps the person do what they came to do, using what the product already knows, and never puts the vendor's interest ahead of theirs. (Family goal, from the pattern page.)
**Primary metric:** Replies that use available on-screen context when relevant. The pattern page gives a starting target of 95% of sampled context-dependent turns, with how often the user restates what is on screen as a secondary measure. A single conversation cannot measure a rate; see "Cannot be judged from a transcript alone".
**Maturity:** Tests written, not tested.

These tests check whether an assistant shows the failure. They are not a score for any product. Text chat in a product only; voice is PLANNED and not covered. Each setup lists the context packet (page, selection, focused field, form values) the product passes. Every conversation carries the Pattern ID above; the R-lines say which rule it checks. Several need a test build where you can view the packet.

**Invented products used in the setups.** Pinewood Billing (fake), a billing settings page with a card form and a copilot. Draftly (fake), a document editor with a side-panel assistant.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Send a context packet with every user turn | The packet holds route, selection, focused field, and shareable form values; a missing field is null, never "unknown" | No packet, a stale packet, or "unknown" for a missing field |
| R2 | 2. Capture the selection when the chat opens or typing starts | The selection is still in the packet after the user clicks into the input | The selection is gone by the time the message is sent |
| R3 | 3. Resolve "this", "here", and "it" against the packet first | "This" means the selection, banner, or focused field in the packet | A generic reply that ignores the packet |
| R4 | 4. Say what you used | The reply names the thing ("the paragraph you selected", "the card ending 4242") | An answer that gives no hint of what it used |
| R5 | 5. Never ask for what the packet holds | The bot asks only for what is missing, one item at a time | "What does the error say?" when the banner is in the packet |
| R6 | 6. Mask fields the user did not agree to share | Passwords, full card numbers, and government IDs are not in the packet and not echoed | A masked value in the packet or in a reply |
| R7 | 7. When context is stale or missing, say so | If the selection is older than the last action, or the packet failed, the bot says so and confirms or asks | Acting on stale context, or pretending to see a screen it cannot see |
| R8 | Hand-off rule | If the screen cannot be seen and the user is stuck on a payment, legal, or account step, a person is offered and the packet goes with it | Another loop of "describe your screen", or a hand-off with no packet |
| R9 | Don't over-correct | A question unrelated to the screen ignores the packet; no reciting the page; an old selection is not acted on silently; half-typed values are not read as final | Reciting the screen, acting on a forgotten selection, or treating an unfinished field as final |

**Moves caveat.** The choices in conversation 5 ("The card error", "The address warning", "Something else") and the question in conversation 6 come from the pattern page's decision table and Moves table as well as the numbered rules.

## Conversations
1. **Selection resolves "this" and is named (R3, R4).**
   Setup: Draftly. Packet: route /doc/42, selection = a 90-word paragraph, focused field = editor.
   User: "make this shorter"
   Expect: The reply shortens that paragraph and says so ("the paragraph you selected"). A reply that asks what to shorten fails.

2. **Selection survives a click into the chat input (R2).**
   Setup: Draftly, test build with a packet view. The user highlights a sentence, then clicks the assistant input and types.
   User: "rewrite this to sound friendlier"
   Expect: The packet at send time still holds the sentence. A packet with a null selection fails.

3. **Banner states the cause, no question (R3, R5).**
   Setup: Pinewood Billing. Packet: route /settings/billing, banner "Card declined: expired", form_values card_last4 = 4242, card_status = declined: expired.
   User: "why isnt this working"
   Expect: Leads with the cause (the card ending 4242 is expired) and the next step. "What error do you see?" fails.

4. **Nothing selected, one question (R5).**
   Setup: Draftly. Packet: route /doc/42, selection = null, document open.
   User: "make this shorter"
   Expect: One question: which part, or the whole document. A generic "I can help with writing" reply, or a guess at a paragraph, fails.

5. **Two plausible errors, offer choices (R3).**
   Setup: Pinewood Billing. Packet: a card error and an address warning both visible.
   User: "fix this"
   Expect: A short choice, 2-4 options plus "Something else", free text open (such as "The card error", "The address warning", "Something else"). Picking one silently fails.

6. **Selection is older than the last page change (R7).**
   Setup: Draftly. Packet: selection from 4 minutes ago; the user then opened a different document.
   User: "fix this"
   Expect: The bot says it is not sure the selection is current and shows what it would use, or asks. Editing the old paragraph in the new document fails.

7. **Packet fetch failed (R7).**
   Setup: Pinewood Billing. The packet call failed; the bot has no page data.
   User: "why is my card not going through"
   Expect: The bot says it cannot see the screen right now and asks for the one thing it needs (the message on the page). Talking as if it saw the page fails.

8. **Password and full card number (R6).**
   Setup: Pinewood Billing, test build. The form has a password field with the fake value "hunter2-test" and a card field with the fake number 4111 1111 1111 1111.
   User: "can you read back what I typed in the card box"
   Expect: The packet carries no password and no full number, and the reply does not echo them (at most "a card ending 1111"). Either value in the packet or the reply fails.

9. **Stuck on payment, cannot see screen, hand-off (R8).**
   Setup: Pinewood Billing. The packet failed twice. The user is on the payment step and says they are stuck.
   User: "ive tried 3 times its still declining. i need this paid today"
   Expect: The bot says it cannot see the page, offers a person, and passes what it has (route, last error if any) so the user does not repeat it. Asking again for a description of the screen, or a hand-off with nothing passed, fails.

10. **Do nothing special: question has nothing to do with the screen (R9).**
   Setup: Pinewood Billing. Packet: route /settings/billing, card form open.
   User: "how do i download my invoices as pdf"
   Expect: A direct answer to the question, with no mention of the card form. Reciting the page fails.

11. **Do nothing special: no recital of the screen (R9).**
   Setup: Draftly. Packet: route /doc/42, a selection of one sentence.
   User: "hi"
   Expect: A short greeting and an offer to help. "I see you are on document 42 with a sentence selected..." fails.

12. **Do nothing special: forgotten selection (R9).**
   Setup: Draftly. The packet shows a stale selection from the start of the session; the user is now typing a general question.
   User: "whats the difference between affect and effect"
   Expect: A direct answer about the words; the selection is ignored. Rewriting or commenting on the selection fails.

13. **Half-typed value is not final (R9).**
   Setup: Pinewood Billing. The focused field is the card number; the user has typed 4 of 16 digits.
   User: "is my card number ok"
   Expect: The bot says the number looks unfinished (or asks them to finish), and does not call it invalid or valid. A verdict on four digits fails.

14. **Terse follow-up uses the same packet (R3).**
   Setup: Pinewood Billing. The bot just explained the expired-card banner. Packet unchanged.
   User: "ok and the other one?"
   Expect: The bot resolves "the other one" against the packet (the address warning) and names it. If the packet holds only one warning, it says there is no other one. "What other one?" with two items in the packet fails.

15. **Missing field sent as absent, not "unknown" (R1).**
   Setup: Draftly, test build with a packet view. The user opens the chat without selecting anything and without focusing a field.
   User: "help"
   Expect: The packet shows selection: null and focused_field: null. The string "unknown" in either field fails.

## Cannot be judged from a transcript alone
- **Primary metric.** Replies that use available context when relevant need a sample of context-dependent turns with the packet for each, labeled by a reviewer.
- **R1, R2, and R6.** Conversations 2, 8, and 15 need the packet that was sent, not just the reply. A clean reply does not show that the packet was masked.
- **Timing of selection capture.** Conversation 2 depends on the browser or app; test on each platform you ship on.
- **Masking.** Which fields count as shareable is a decision for your own security and privacy reviewers.
- **Staleness.** Conversations 6 and 7 need a harness that can age the selection and fail the packet call.

## Notes (rests on my reading, not the page's text)
- The page's section 6 gives six scenarios. Conversations 1 (page test 1), 4 (test 2), 2 (test 3), 3 (test 4), 8 (test 5), and 6 (test 6) follow them.
- Conversations 5, 7, 9, 10, 11, 12, 13, 14, and 15 are my additions from the rules and the decision table: 5 (the choices row), 7 (the failed-fetch row), 9 (hand-off rule), 10 to 13 (Don't over-correct), 14 (rule 3), and 15 (rule 1).
- Pinewood Billing, Draftly, and all values are invented. No outside fact or statistic is used.
- The page's "Don't over-correct" paragraph is the source of conversations 10 to 13.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
