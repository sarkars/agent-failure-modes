# Customer Effort for Chatbots: Make It Easy Instead of Trying to Delight

> **Use it when:** you run a support bot and need to decide what to measure and fix first.

> Status: **framework.** No rule check yet; effort needs an AI judge or user survey.

## The idea in one paragraph
In "Stop Trying to Delight Your Customers" (Harvard Business Review, July 2010), Matthew Dixon, Karen Freeman and Nicholas Toman of the Corporate Executive Board reported on a study of more than 75,000 customer interactions. Their finding: going above and beyond rarely pays off, while making customers work hard to get a problem solved strongly drives disloyalty. Customers mostly want a quick, simple fix. They proposed the Customer Effort Score as a better predictor of loyalty than satisfaction. For bots, effort shows up as repeating information, being transferred, switching channels, and coming back because the first answer didn't solve it.

## Where effort comes from in chat
| Source of effort | What it looks like | Fix |
|---|---|---|
| Repeating information | "What's your order number?" after the user gave it | Carry details across turns and to the person who takes over |
| Transfers | Bounced to another bot or queue with no context | Warm handoff with a summary (see [SBAR](sbar-handoff.md)) |
| Channel switching | "Please call us" for something chat could do | Finish in chat, or say why it can't be done there |
| Repeat contacts | The fix didn't hold; the user comes back | Anticipate the next issue and head it off |
| Extra steps | Menus, forms, "please rephrase" | Ask one question at a time, accept free text |

## How to use it in a bot
1. Ask at the end: "How easy was it to get this sorted?" (a 1-7 scale is common) and track it.
2. Log every time the bot asks for something already given; drive it to zero.
3. When handing off, pass the summary so the person never re-asks.
4. Prefer solving the next likely problem over adding warmth.

## Worked example
```
Bot (high effort):  I can't change addresses here. Please call 1-800-... between 9 and 5.
Bot (low effort):   Done: your order now ships to 22 Elm St. Your next delivery uses the same address.
```

## What the checker flags
No rule check yet. Whether the user had to repeat themselves or switch channels needs an AI judge across the whole conversation. The always-on [talk-to-a-human check](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md) catches one common effort trap.

## Limits
- The study is from phone and web service; it is not tested on chatbots.
- Effort and warmth are not opposites: an empathetic line costs the user nothing. The finding is that warmth doesn't replace an easy fix.

## Source
- Dixon, M., Freeman, K. and Toman, N. (2010). [Stop Trying to Delight Your Customers](https://store.hbr.org/product/stop-trying-to-delight-your-customers/R1007L). *Harvard Business Review*. Product summary page opened; the full article is paywalled.

## Related
- [Re-asks for known information](../goals/embedded-copilots/failures/re-asks-for-known-information.md)
- [Cold transfer](../goals/human-handoff/failures/cold-transfer.md)
- [HEARD service recovery](heard-service-recovery.md)
- [All frameworks](README.md)
