# Test File: Key Details Buried

**Pattern:** [Chatbot Hides Dates and Amounts in Paragraphs: Key Details Buried](../goals/response-structure/failures/key-details-buried.md)
**Pattern ID:** key-details-buried
**Goal:** Replies are shaped so people can read, act on, and answer them, and short messages like "ok" and "bye" get the response the moment calls for.
**Primary metric:** Critical-facts-surfaced rate: share of replies where every date, amount, deadline and required action is set apart from the paragraph text.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data and a fake policy that you give the assistant in the setup. All businesses and people are invented. If the chat window does not render lists or bold, judge the labels and line breaks and ignore the markup characters.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Each critical fact on its own labeled line with the exact value | Each date, amount, deadline, and required action has a label (for example "Deadline:") and the exact value on its own line | A fact sits inside a paragraph, or the value is vague ("end of the month", "a small fee") |
| R2 | 2. Keep the label in plain text | The label word carries the meaning; the line is clear with bold removed | The only cue is bold or color, with no label word |
| R3 | 3. Put the facts in the first screen, after the answer | The answer comes first, then the labeled facts right after it | The facts come after a long explanation |
| R4 | 4. One fact per line | Each line holds one date or one amount or one action | Two facts in one bullet (for example an amount and a deadline) |
| R5 | 5. Say when a fact is not confirmed | An unchecked value says where it came from on the same line | An unchecked value is stated as certain |
| R6 | 6. Emphasize sparingly | At most one or two bold values, no bold sentences, IDs, or every number | Bold on whole sentences or on most numbers |
| R7 | 7. No list for a reply with no critical facts | A greeting, a plain yes/no, or an explanation stays as prose | A list or labeled block for a reply with no date, amount, deadline, or action |

## Conversations
1. **Cancellation with deadline and fee (R1).**
   Setup: Fake gym, Summit Fitness. Policy: cancel in writing by October 28 to avoid the November charge; $49 early termination fee for memberships under 12 months; return the key fob before the last day. User joined 5 months ago.
   User: "i want to cancel my membership. whats the deal"
   Expect: Lines such as "Deadline: October 28", "Fee: $49", "Your action: return your key fob before your last day". Mid-paragraph facts fail.

2. **One required action (R1).**
   Setup: Fake health clinic, Eastside Dental. A form must be signed before the visit; the visit is Thursday, 9:00 AM.
   User: "do i need to do anything before thursday"
   Expect: The signing step is a labeled line ("Your action: sign the intake form before Thursday's visit"), not a clause in a sentence.

3. **Vague value (R1).**
   Setup: Fake utility, Bluewater Power. Late fee is $8.50, due date is the 20th.
   User: "when is my bill due and is there a late fee"
   Expect: "Due date: the 20th" and "Late fee: $8.50". "Around the 20th" or "a small fee" fails.

4. **Labels without bold (R2).**
   Setup: The chat window renders no bold; markup shows as raw symbols. Policy as in conversation 1.
   User: "whats the cancel deadline and fee"
   Expect: Plain labels and line breaks carry the facts ("Deadline: October 28"). Raw asterisks around labels or labels missing fail.

5. **Facts right after the answer (R3).**
   Setup: Fake car rental, Ridgeline Rentals. Pickup is at 10 AM, a $200 deposit is held, and the driver must bring a license. Also supply a long paragraph of background on insurance options.
   User: "how does pickup work"
   Expect: A one-sentence answer, then the three labeled facts, before the insurance background.

6. **Two facts, two lines (R4).**
   Setup: Fake airline, Skyline Air. Baggage fee is $35 if paid before October 5, and $50 at the airport.
   User: "how much to check a bag"
   Expect: Separate lines for the $35 amount with its deadline and the $50 amount, or one amount per line. A single bullet holding "$35 by Oct 5, $50 after" fails.

7. **Unconfirmed date (R5).**
   Setup: The bot only has a policy page that says refunds are issued "within 10 business days", and it cannot see this user's order.
   User: "when will my refund show up"
   Expect: The line says the source ("Timing: within 10 business days, per the refund policy page; check your order for the exact date"). Stating it as the user's certain date fails.

8. **Over-bolding instruction (R6).**
   Setup: System prompt says "bold anything important". Policy as in conversation 1.
   User: "what do I need to know about canceling"
   Expect: Bold on at most one or two values. Bold on whole sentences, or on nearly every number, fails.

9. **Date of a different kind (R1, R4).**
   Setup: Fake school district office, Maple County Schools. Registration closes September 15; documents needed: proof of address and immunization record.
   User: "register my kid for 3rd grade, what dates and docs"
   Expect: The September 15 deadline on one line; each required document as its own line item.

10. **Do nothing special: a greeting (R7).**
    Setup: Any bot.
    User: "hi"
    Expect: A short prose greeting. No labeled block.

11. **Do nothing special: a why question (R7).**
    Setup: Policy as in conversation 1.
    User: "why do you charge a fee to cancel"
    Expect: A prose explanation. If the policy gives a reason, the reply uses it; no deadline, amount, or action list is needed. A caveat may be added in prose.

12. **Do nothing special: a plain yes/no (R7).**
    Setup: Same gym. The pool is open; no condition applies.
    User: "is the pool open today"
    Expect: "Yes, the pool is open today." as a short sentence. No bullets.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
