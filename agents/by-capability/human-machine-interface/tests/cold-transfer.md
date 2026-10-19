# Test File: Cold Transfer

**Pattern:** [Cold Transfer: Chatbot Hands Off and the Agent Asks Everything Again](../goals/human-handoff/failures/cold-transfer.md)
**Goal:** A person is reachable when needed, and arrives informed, without the customer repeating themselves.
**Primary metric:** Re-ask rate after handoff: the share of handoffs where the person asks for something the customer already gave.

These tests check whether a handoff shows the failure. They are not a score for any product. Use fake data only. They need access to both the bot conversation and what the receiving person sees.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | A handoff packet exists | The packet holds the goal, key facts, what was tried, and promises made | Only an ID or subject travels |
| R2 | The person sees it before connecting | Packet and transcript are visible before the first message | The person must ask the customer or search for the chat |
| R3 | The customer can correct the summary | The bot shows the summary and a correction reaches the person | No chance to correct, or the correction is lost |
| R4 | Verification is not repeated | The person does not re-run verification the bot already did | The person asks the customer to verify again |
| R5 | The person starts from the packet | The first message uses facts from the chat | The first message asks an open "how can I help?" |
| R6 | Redaction keeps meaning | Redacted values show a placeholder | The field is blank and the story is lost |
| R7 | Failed transfers keep the packet | A retry does not lose the packet | The customer must start over |

## Scenarios
1. **Ten-turn chat, then handoff.** Expect the packet and a first message that uses chat facts. R1, R5.
2. **Packet visibility.** Check the agent tool before connect. Expect packet and transcript. R2.
3. **Wrong fact in the summary.** The customer says "the order number is wrong". Expect the correction to reach the person. R3.
4. **Already verified.** The bot verified by order number and email. Expect no second verification. R4.
5. **Redacted card.** The customer gave a card number that is redacted. Expect "card ending 1234 (provided, redacted)" or similar. R6.
6. **Bot promise.** The bot said a refund would arrive in 5 days. Expect the promise in the packet. R1.
7. **Transfer fails once.** The first transfer errors; retry succeeds. Expect no lost packet and no repeated questions. R7.
8. **Customer adds a detail.** After the summary, the customer adds a date. Expect it in the packet. R3.
9. **Urgent mood.** The customer said "I need this today". Expect urgency in the packet. R1.
10. **Packet too long.** A 60-turn chat. Expect a short packet with the transcript one click away. R1, R2.
11. **Do nothing special: no prior chat.** The customer opens a new chat with a person directly. Expect no packet and no fake summary. R1.
12. **Do nothing special: one-turn chat.** The customer's only message was "agent". Expect an honest, minimal packet with no invented facts. R1.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
