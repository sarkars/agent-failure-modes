# Challenger Selling for Chatbots: Teach, Tailor, and Take Control

> **Use it when:** a sales bot answers product questions accurately but never tells the buyer anything they didn't know.

> Status: **framework.** No rule check yet; whether an insight was offered needs an AI judge.

## The idea in one paragraph
The Challenger approach comes from research by Matthew Dixon and Brent Adamson at the Corporate Executive Board (*The Challenger Sale*, 2011; "The End of Solution Sales", Harvard Business Review, 2012). They argued that buyers increasingly research on their own, so sellers who only respond to stated needs add little. Top performers "teach" the buyer a new way to think about their problem, "tailor" the message to the person's role and goals, and "take control" of the conversation, including talking about money. For a bot, the teachable part is the insight: a fact or comparison that reframes the user's problem, offered after answering.

## The three moves
| Move | What it means | Chat example (accounting software) |
|---|---|---|
| **Teach** | Offer an insight the buyer didn't have | "Most teams your size lose more time on receipt matching than on invoicing." |
| **Tailor** | Fit it to their role and goal | "For a finance lead, that's about 2 days of close each month." |
| **Take control** | Lead to a next step, including price | "Want to see how matching works on your own data? It's a 10-minute setup." |

## How to use it in a bot
1. Answer the question first.
2. Offer one insight only when it is true, sourced, and relevant to what the user said.
3. Don't argue with the user's goal; reframe the problem, not the person.
4. Never invent statistics to sound insightful.

## Worked example
```
User: how much is the pro plan
Bot (feature dump): Pro is $49/month and includes 20 features: dashboards, exports, API access, ...
Bot (challenger):   Pro is $49 a month. Since you mentioned month-end takes a week, the automatic bank
                    matching in Pro is usually where teams save the most time. Want me to show you that?
```

## What the checker flags
No rule check yet. Whether the bot offered a real, relevant insight needs an AI judge. Related library pattern: [feature dump instead of insight](../goals/conversation-frameworks/failures/feature-dump-instead-of-insight.md).

## Limits
- Built on B2B field sales. "Taking control" can tip into pressure; pair it with [ethical persuasion](cialdini-ethical-persuasion.md).
- An insight a bot makes up is worse than none.

## Source
- Adamson, B., Dixon, M. and Toman, N. (2012). [The End of Solution Sales](https://hbr.org/2012/07/the-end-of-solution-sales). *Harvard Business Review*.

## Related
- [SPIN questioning](spin-questioning.md)
- [BANT and MEDDICC](bant-meddicc-qualification.md)
- [All frameworks](README.md)
