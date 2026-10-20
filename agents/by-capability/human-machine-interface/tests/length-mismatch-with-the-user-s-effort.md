# Test File: Length Mismatch With the User's Effort

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs answers a few typed words with several paragraphs.

**Pattern:** [Chatbot Reply Too Long for a Short Message: Length Mismatch With the User's Effort](../goals/response-structure/failures/length-mismatch-with-the-user-s-effort.md)
**Pattern ID:** length-mismatch-with-the-user-s-effort
**Goal:** Reply scale tracks the user's message and urgency.
**Primary metric:** Reply-to-message length ratio distribution. Starting target on the pattern page: the share of turns above a per-intent ratio cap stays under 5% (tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, orders, amounts, and people are invented (fake). Text chat only. The band (1-2 sentences for a message of 1-10 words) and the 5x multiple are the page's starting points to tune; record the values you use before you judge.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Set a length band from the user's message | For a clear message of 1-10 words, the reply is 1-2 sentences (or your recorded band) | The reply runs well past the band with no need for it |
| R2 | 2. Answer in the first sentence | Sentence one holds the answer or the next step | Sentence one is setup, a restatement, or background |
| R3 | 3. Offer the long version, do not send it | The short answer plus one line offering more | The full long answer is sent, or the short answer ends the matter and an offer is added anyway |
| R4 | 4. Shrink when the user signals urgency | Shortest form that still answers after "quick", "asap", "in a hurry", "just tell me", or a one-word reply | The reply keeps its usual length |
| R5 | 5. Grow when the user writes more | A detailed message gets a fuller reply, answer first, within your recorded multiple of the user's length (page example: 5x) or trimmed with an offer | A one-line reply to a detailed message, or a draft far past the multiple sent whole |
| R6 | 6. Do not mirror blindly | A fragmentary message still gets a complete, clear answer | The reply copies the fragment style, or leaves out what the user needs to act |
| R7 | 7. Ask one question when a short message is vague | One short clarifying question when two meanings give different answers | A long reply that covers both meanings |
| R8 | Don't over-correct | A required warning, fee, or deadline stays in the short answer; an asked-for long answer is given; no question is asked when the answer is the same either way | A required warning is cut to hit the band, a requested long answer is shortened, or a needless question is asked |

## Conversations
1. **Short clear message (R1, R2).**
   Setup: Fake store Lakeview Outfitters. Order 88213 (fake): refund of $64.20 issued Oct 14. Policy: banks usually post it in 5-10 business days.
   User: "refund status?"
   Expect: 1-2 sentences, answer first (issued, amount, date). No "Great question", no policy essay.

2. **Answer first (R2).**
   Setup: Same store. Open Sunday 10 AM to 4 PM.
   User: "do you open sunday"
   Expect: Sentence one is yes plus the hours. Background about holiday schedules before the answer fails.

3. **Offer, do not send (R3).**
   Setup: Same store. The full returns process has six stages and runs about 350 words in the knowledge base.
   User: "how do returns work"
   Expect: A short answer (the main route and the window) and one offer line such as "Want the full process?" Sending all six stages fails.

4. **Urgent wording (R4).**
   Setup: Same store. Pickup counter closes at 4 PM today.
   User: "quick, in a hurry: can i pick up order 88213 today"
   Expect: Shortest form that answers (yes or no and the cutoff), then at most one offer. A reply at the bot's usual length fails.

5. **"Just tell me" after a long answer (R4).**
   Setup: Same store. The previous bot turn was a long shipping explanation. The user then writes the next line.
   User: "just tell me when it arrives"
   Expect: The delivery date in one sentence. Repeating the shipping explanation fails.

6. **Detailed message earns a fuller reply (R5).**
   Setup: Same store. The user writes six sentences: bought a tent on Oct 2, one pole snapped on the first trip, kept the receipt, the box is gone, wants a replacement not a refund, and is camping again Oct 25. The tester writes the six sentences once and reuses the same words each run.
   User: (the six-sentence message)
   Expect: A fuller reply that answers first (can a replacement arrive in time), covers the missing box, and stays within your recorded multiple. A one-line reply fails. A reply far past the multiple, sent whole, fails.

7. **Fragments, complete answer (R6).**
   Setup: Same store. Order 88213 was charged twice, $64.20 each (fake). A duplicate charge is refunded 3-5 business days after it is reported.
   User: "charged 2x. 64.20. order 88213. fix"
   Expect: A complete answer: it will be refunded, how long, and what the bot did or needs. A reply in fragments that omits the timing fails.

8. **Vague short message (R7).**
   Setup: Same store. The user has one open order (88213) and one active Rewards membership. Canceling each works differently.
   User: "cancel?"
   Expect: One short question: the order or the membership? A reply that explains both cancellations fails.

9. **Do nothing special: the user asks for length (R8).**
   Setup: Same store. Full refund process in the knowledge base.
   User: "walk me through the whole refund process step by step"
   Expect: The full reply. The user asked for length; trimming it to two sentences fails.

10. **Do nothing special: required fee stays (R8).**
    Setup: Same store. Opened mattresses can be returned within 30 days with a $75 restocking fee (fake policy).
    User: "can i return an opened mattress"
    Expect: Short, with the $75 fee in it. Dropping the fee to stay short fails.

11. **Do nothing special: a short message asking for long output (R8).**
    Setup: Same store with a general writing-help feature.
    User: "write a 3 paragraph email to my landlord about the broken heater"
    Expect: Three paragraphs. A two-sentence reply fails.

12. **Do nothing special: no question when the answer is the same (R7, R8).**
    Setup: Same store. One phone number serves every department.
    User: "phone number?"
    Expect: The number. Asking "which department?" fails.

13. **Do nothing special: no offer when the short answer ends it (R3, R8).**
    Setup: Same store. Order 88213 was delivered Oct 14.
    User: "did 88213 arrive"
    Expect: "Yes, delivered Oct 14." Adding "Want the full delivery timeline?" fails; the page says not to offer options when the short answer already ends the matter.

14. **Do nothing special: short question, longer answer (R8).**
    Setup: Same store. Changing a delivery date needs a request before 2 PM the day before, costs $5 after the first change, and cannot be done once the order is out for delivery (fake policy).
    User: "can i change my delivery date"
    Expect: More than two sentences is allowed because the deadline and fee are needed to act. Cutting the deadline or fee to fit a band fails.

## Cannot be judged from a transcript alone
- **Ratio distribution and per-intent caps.** The page's primary metric is a share of turns across a log. These tests show single replies, not a rate.
- **The band and multiple.** The page marks both as starting points to tune. Record your values per setup.
- **"Required warning present."** A reviewer must know from the knowledge base which warning, fee, or deadline is required.
- **Hand-off rule.** The page treats a repeated "stop sending me long answers" followed by another long reply as a product defect for the prompt owner, not chat behavior. This pack does not test it.

## Rules without a scenario yet
None. Every rule in the fix (1 to 7) has at least one conversation above.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | |
