# Cialdini's Persuasion Principles for Chatbots: Use Them Honestly, Flag Their Misuse

> **Use it when:** a sales or retention bot uses urgency, social proof or "only a few left", and you need to know where persuasion ends and manipulation starts.

> Status: **framework.** The rule check below is proposed, not calibrated.

## The idea in one paragraph
Psychologist Robert Cialdini described principles that make people more likely to say yes: reciprocity, scarcity, authority, consistency (commitment), liking and social proof, later adding unity. His own organization says they should be used ethically: real scarcity, real expertise, real social proof. A bot can apply them at scale and without judgment, so the line matters more. True scarcity ("2 left in your size") helps the user decide; invented scarcity or pressure ("act now!") is manipulation and, in many places, a consumer-protection problem (see [dark patterns](ftc-dark-patterns.md)).

## The principles, and how bots misuse them
| Principle | Honest use | Misuse to avoid |
|---|---|---|
| Reciprocity | Give real help first | Gifts that create guilt to push a sale |
| Scarcity | State real stock or deadlines | "Only 2 left!" when it isn't true; fake countdowns |
| Authority | Cite real experts or standards | Invented credentials or "doctors recommend" |
| Consistency | Remind users of their stated goal | Trapping users with small commitments |
| Liking | Be warm and genuine | Flattery to lower guard |
| Social proof | Real reviews and numbers | Fake reviews, "everyone is buying" |
| Unity | Shared identity, honestly | "People like us" pressure |

## How to use it in a bot
1. Only state scarcity, deadlines and counts that come from live data.
2. No pressure words: "act now", "hurry", "don't miss out", "last chance".
3. Never use these principles on users showing distress or on children.
4. Make declining as easy as accepting.

## Worked example
```
User: how much is the alder sofa
Bot (pressure): It's $899, but only 2 left at this price, so act now!
Bot (honest):   It's $899. The gray is in stock and ships in 5 days; the green is back-ordered until June.
                Want fabric samples first?
```

## What the checker flags
Choosing this framework turns on [manipulative closing](../../speech-and-audio/goals/conversation-flow/failures/vague-consent-exploitation.md): pressure phrases such as "only 2 left", "act now", "hurry", "don't miss out", "last chance", "limited time" and "selling fast". The check can't tell real scarcity from fake, so "only 2 left" is flagged for review even when true.

## Limits
- Cialdini's work describes influence; it is not a code of conduct.

## Source
- Influence at Work (Cialdini's organization), [The Science of Persuasion](https://www.influenceatwork.com/6-principles-of-persuasion/).

## Related
- [Dark patterns (FTC)](ftc-dark-patterns.md)
- [Upsell at the wrong moment](../goals/conversation-frameworks/failures/upsell-at-the-wrong-moment.md)
- [All frameworks](README.md)
