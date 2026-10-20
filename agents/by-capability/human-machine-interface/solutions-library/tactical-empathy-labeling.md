# Tactical Empathy for Chatbots: Labeling and Mirroring, Used Honestly

> **Use it when:** conversations get tense (complaints, negotiations, cancellations) and the bot needs to lower the temperature before solving.

> Status: **framework.** The rule check below is proposed, not calibrated.

## The idea in one paragraph
Chris Voss, a former FBI hostage negotiator, describes "tactical empathy" in *Never Split the Difference* (2016): understanding the other side's feelings and what's behind them, and saying that out loud. Two of its tools suit chat. **Labeling** names the emotion you hear ("It seems like..."), which can defuse it. **Mirroring** repeats a few of the person's key words, which encourages them to keep explaining. Voss frames these as negotiation tools, so they come with a risk: used to manipulate, or used mechanically, they feel fake. The library has a separate pattern for exactly that.

## The tools
| Tool | What it does | Chat example |
|---|---|---|
| Label | Name the emotion tentatively | "It seems like the delays have made you lose trust in us." |
| Mirror | Repeat 1-3 key words as a question | "Charged twice?" |
| Open "how" questions | Invite the user to explain | "How should we put this right?" |
| Pause | Let the label land before solving | One line, then the fix in the next sentence |

## How to use it in a bot
1. Label once, at a lower intensity than the user, and then act.
2. Mirror only to clarify facts, not as a tic.
3. Never use labels to steer the user toward something against their interest.

## Worked example
```
User: you charged me twice and nobody cares
Bot (cold):    Please allow 5-7 business days for refunds.
Bot (labeled): It sounds like you've been left to chase this alone. I see both charges; the duplicate is
               refunded now and you'll see it in 3-5 days.
```

## What the checker flags
Choosing this framework turns on [hollow empathy](../goals/emotional-intelligence/failures/hollow-empathy.md). Misuse is described in [misused tactical empathy](../goals/conversation-frameworks/failures/misused-tactical-empathy.md), [over-mirroring](../goals/conversation-frameworks/failures/over-mirroring.md) and [mirroring hostility](../goals/conversation-frameworks/failures/mirroring-hostility.md); those need an AI judge.

## Limits
- A negotiation book, not a research protocol; its claims are not tested on bots.
- In negotiation the goal is to win; in service the goal is to help. Keep the tools, drop the angle.

## Source
- Voss, C. with Raz, T. (2016). *Never Split the Difference*. Summary consulted: [Oberlo book summary](https://www.oberlo.com/blog/never-split-the-difference-by-chris-voss-summary) (secondary; the book was not opened).

## Related
- [NURSE empathy statements](nurse-empathy-statements.md)
- [Project BETA de-escalation](project-beta-de-escalation.md)
- [All frameworks](README.md)
