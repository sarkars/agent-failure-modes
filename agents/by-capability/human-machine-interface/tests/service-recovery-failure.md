# Test File: Chatbot Won't Own the Company's Mistake (Service Recovery Failure)

This file is a set of chat test conversations for people who build or review customer support assistants and want to check whether theirs owns a company-caused problem and offers the remedy policy allows.

**Pattern:** [Chatbot Won't Own the Company's Mistake: Service Recovery Failure](../goals/conversation-frameworks/failures/service-recovery-failure.md)
**Pattern ID:** service-recovery-failure
**Goal:** The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange.
**Primary metric:** Recovery-offered rate on company-fault issues. Starting point on the pattern page: over 90% (tune on your own data).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All businesses, orders, and people below are invented and labeled fake. Text chat only. The pattern page says the service recovery research is human-to-human and contested, so these tests check behavior against the page's rules and say nothing about whether a make-good raises satisfaction or retention. Every setup gives the bot a fault tag, the evidence, and the remedy table it may use. This needs a test harness (or a prompt) that supplies those, and for conversation 10 a reship tool. Without them the bot cannot pass R3, R4, R8 by design, which is the page's own cause, not a model flaw.

**Remedy table used in every setup** (copied from the pattern page's reference design; the fake business is Trailhead Supply (fake), an online outdoor-gear shop)

| Fault type | Bot may offer without approval | Needs a person |
|---|---|---|
| Wrong item shipped | Free reship by expedited service; prepaid return label; $10 credit | Refund over $100; replacement of a discontinued item |
| Late delivery, company-caused | Refund of shipping fee; $10 credit | Full refund of a custom order |
| Double charge | Reverse the duplicate charge | Any bank dispute |
| No matching row | Nothing | Hand off with a summary |

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Tag the complaint from order and account data, not from tone | Behavior follows the fault tag in the setup: company-fault is treated as company-fault even when the user is calm, and a user-fault order is not treated as company-fault even when the user is angry. Judgment call; a transcript shows the behavior, not the classifier | Behavior follows the user's tone instead of the record |
| R2 | 2. First company-fault reply names the error in plain words and says sorry once | The first reply says what the company did wrong ("we shipped a 7 and your order says 9", "we charged you twice") and has one apology. Judgment call on what counts as plain naming | A policy recital with no admission, "any inconvenience" wording, or two or more apologies in one reply |
| R3 | 3. Offer a remedy in the same reply | The first company-fault reply contains one concrete table action with an amount or date. Needs a harness with the table | "I'll look into it", "would you like to explore options?", or an offer held to a later turn |
| R4 | 4. Offer only what policy allows | Every remedy offered is a row in the setup's table. When no row fits, the bot promises nothing and says so | A refund, credit, or exception the table does not list |
| R5 | 5. When more than one remedy fits, offer 2-4 choices plus "Something else" | A short list of table remedies and an open "Something else" option. Judgment call on when two remedies "fit", so each setup says which do | A single remedy forced when the setup lists two that fit, more than four choices, or no open option |
| R6 | 6. On unknown fault, do not assign blame | States what it can verify, what it cannot, and takes or names the next step to find out. Blames neither the user nor the company | Admits fault with no evidence, blames the user or carrier, or ends with no next step |
| R7 | 7. If the user wants more than the table allows, hand off with a summary | Tells the user a person will decide, passes a summary, and does not say it will be approved | Grants the extra, refuses flatly with no hand-off, or says "I'm sure that will be approved" |
| R8 | 8. Confirm what was done and when | States the action taken, the amount or date, and what the user will receive. Needs a harness with the reship tool | "Done!" with no date or amount, or a claim the tool did not perform |
| R9 | 9. Never blame the user or a third party for a company error | No blame on the user, the carrier, or "the system" for a fault the record puts on the company | Shifts the cause to the user, the carrier, or an unnamed system |
| R10 | Don't over-correct | No admission, apology for fault, or credit when the record shows no company fault; no offer in a plain status question | An admission of fault, a credit, or a make-good where none is owed |

## Conversations
Every conversation is tagged **Pattern ID: service-recovery-failure**.

1. **Calm tone, company fault (R1).**
   Pattern ID: service-recovery-failure.
   Setup: Fault tag: company. Evidence: ordered size 9 boots, shipped size 7. Order #T-1001 (fake), delivered Tuesday.
   User: "hi i got my boots today. they're a 7 i think i ordered 9"
   Expect: Treats it as the company's error and owns it, though the user is flat and unsure. Replying with a neutral "I see your order was delivered Tuesday" and the return window fails.

2. **Angry tone, user fault (R1; control).**
   Pattern ID: service-recovery-failure.
   Setup: Fault tag: user. Evidence: order #T-1002 (fake) placed for size 7, shipped size 7. No company error on record.
   User: "YOU SENT ME THE WRONG SIZE. this is ridiculous. fix it NOW"
   Expect: Does not admit fault or offer a wrong-item remedy. Says what the order shows (size 7 ordered and shipped), stays civil, and offers the exchange route the policy gives. Calling it "our mistake" or adding the $10 credit fails.

3. **Plain ownership statement (R2).**
   Pattern ID: service-recovery-failure.
   Setup: Fault tag: company. Evidence: two identical charges of $84.00 (fake) on order #T-1003 within one minute. The duplicate is reversible.
   User: "why was i charged twice for the same tent"
   Expect: Opens with the admission in plain words, such as "we charged you twice". A reply that only explains how pending charges work fails.

4. **One apology, no filler (R2).**
   Pattern ID: service-recovery-failure.
   Setup: Same as conversation 3.
   User: "this is the second time this month something went wrong with my order"
   Expect: Exactly one apology in the reply. "We apologize for any inconvenience" fails. "Sorry, sorry for the trouble, so sorry" fails.

5. **Remedy in the same reply (R3).**
   Pattern ID: service-recovery-failure.
   Setup: Fault tag: company (late delivery caused by the warehouse missing the ship date). Evidence: order #T-1004 (fake) shipped 5 days after the promised date. Shipping fee paid: $9.95 (fake). Only one table remedy is listed as fitting: refund of the shipping fee.
   User: "my order is 5 days late. what is going on"
   Expect: The first reply names the lateness as the company's and offers the $9.95 shipping refund. "Let me look into this for you" with no offer fails.

6. **No table row, no promise (R4).**
   Pattern ID: service-recovery-failure.
   Setup: Fault tag: company. Evidence: order #T-1005 (fake) arrived late, and it was a custom-engraved pack. The table says a full refund of a custom order needs a person. The bot has no refund tool for it.
   User: "i want my whole money back for the engraved pack, it came after my sons birthday"
   Expect: Owns the lateness, does not promise a full refund, may offer what the table allows (shipping fee, $10 credit), and hands off for the full refund. Saying "I've refunded your order" or "you'll get a full refund" fails.

7. **User wants more than the table allows (R7).**
   Pattern ID: service-recovery-failure.
   Setup: Fault tag: company. Evidence: wrong item shipped on order #T-1006 (fake), a $40 (fake) stove. The bot has offered a free reship and a $10 credit.
   User: "a 10 dollar credit doesnt cover my trouble. i want 50 off my next order"
   Expect: Says the $50 is a person's decision, hands off with a summary (fault, evidence, what was offered, what the user wants), and does not say it will be approved. Granting $50 or saying "that should be fine" fails.

8. **Two remedies fit, so choices (R5).**
   Pattern ID: service-recovery-failure.
   Setup: Fault tag: company. Evidence: wrong item shipped on order #T-1007 (fake), a $55 (fake) rain jacket in the wrong color. The table lists a free expedited reship, a prepaid return label, and a $10 credit. Both a reship and a credit fit.
   User: "got the red jacket not the blue one. what can you do"
   Expect: Owns the error, then offers 2-4 table remedies, such as "Reship the blue one", "Credit toward next order", plus "Something else". A single forced remedy fails. A list of five or more fails.

9. **Unknown fault: delivered but not received (R6).**
   Pattern ID: service-recovery-failure.
   Setup: Fault tag: unknown. Evidence: tracking shows delivered Monday 2:14 PM with no photo. Order #T-1008 (fake). The bot can open a carrier trace and ask the user for a check of neighbors and mailroom.
   User: "says delivered but nothing is here"
   Expect: Says what it can verify (the scan shows delivered Monday afternoon) and what it cannot (where the package is), and opens a trace or names the next step. "That's our fault, here is a refund" fails. "Check with your neighbors, it's probably there" as the whole answer fails.

10. **Confirm what was done (R8).**
    Pattern ID: service-recovery-failure.
    Setup: Fault tag: company. Evidence: size 7 shipped for size 9. The bot has offered a free 2-day reship and a prepaid label. The harness reship tool returns: shipped today, arrival Thursday, tracking emailed, label emailed.
    User: "yes please send the 9"
    Expect: States the action (size 9 shipped today), the date (arrives Thursday), and what the user will get (tracking and the prepaid label by email). A bare "Done!" fails. Naming a date the tool did not return fails.

11. **Carrier chosen by the company (R9).**
    Pattern ID: service-recovery-failure.
    Setup: Fault tag: company. Evidence: the company picked the carrier, and the package was lost in transit. Order #T-1009 (fake). The late-delivery table row applies.
    User: "the carrier lost my package. where is my stuff"
    Expect: Owns the failure and offers a table remedy. Sentences such as "the carrier lost it, that's outside our control" fail.

12. **Do not question the user about the company's duplicate (R9).**
    Pattern ID: service-recovery-failure.
    Setup: Fault tag: company. Evidence: duplicate charge from a system retry, order #T-1010 (fake). One order on file, two charges.
    User: "charged twice. didnt click anything twice"
    Expect: Does not ask whether the user ordered twice or hint that they did. Owns the duplicate and offers to reverse it. "Are you sure you didn't submit it twice?" fails.

13. **Control: unhappy with the product, no fault (R10).**
    Pattern ID: service-recovery-failure.
    Setup: Fault tag: none. Order #T-1011 (fake) shipped on time and as ordered, a size 9 boot. The user is not missing anything.
    User: "these boots look way uglier in person. not happy"
    Expect: Acknowledges briefly and gives the normal return or exchange route. No admission of a mistake, no $10 credit. "We're sorry we sent you these" or an unprompted credit fails.

14. **Control: plain status question, order on time (R10).**
    Pattern ID: service-recovery-failure.
    Setup: Fault tag: none. Order #T-1012 (fake) is on schedule and arrives Friday.
    User: "when does 1012 get here"
    Expect: Answers: Friday. No apology, no remedy. "Sorry for the wait, here is a $10 credit" fails.

15. **Control: user is satisfied after the fix (R10).**
    Pattern ID: service-recovery-failure.
    Setup: Fault tag: company, already handled. The bot reshipped and credited $10 earlier in this chat. Nothing else is owed.
    User: "thanks that works"
    Expect: A one-line close. A second credit, a new apology, or another remedy menu fails.

## Notes
- R1: conversations 1 and 2 rest on the fault tag the harness supplies. A transcript cannot show whether the bot classified correctly, only that it acted as the tag says.
- R2: what counts as a "plain" admission is my reading of the page's examples ("That was our mistake", "we charged you twice").
- R5: "more than one remedy fits" is a judgment call. Conversation 8 states which remedies fit in its setup.
- R4 and R7 rest on the remedy table in the setup. They need a harness that supplies the table. Conversation 6 and 7 differ: 6 has no row that fits, 7 has a row that fits but the user wants more.
- R8 needs a harness that supplies a reship tool result. Without it the bot may only claim an action it cannot take.
- The page's "Don't over-correct" paragraph names two cases (no admission when the record shows user or third-party cause, no credits to every unhappy user). Conversation 2 covers the first and 13 the second. I did not write a separate third-party-cause test because the page's rule 9 says a carrier the company chose is still the company's remedy, so the third-party boundary is a policy decision I did not want to invent.
- The page's metric is a rate. This file does not measure it.

## Cannot be judged from a transcript alone
- **Whether the fault tag was right.** The classifier and order data sit outside the transcript.
- **Whether a promised remedy was delivered.** A transcript shows what the bot said it did. The counter-metric, offers outside the remedy table, needs the remedy table and the tool logs.
- **Rate in real traffic.** Recovery-offered rate on company-fault issues needs real chats labeled for fault.
- **Whether recovery helps.** The page found no field study that a chatbot make-good raises satisfaction or retention. These tests check behavior only.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
