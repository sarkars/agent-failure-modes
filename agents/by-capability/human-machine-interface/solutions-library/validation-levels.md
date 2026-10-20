# Validation Levels for Chatbots: Six Ways to Show a Reaction Makes Sense

> **Use it when:** users share distress, and the bot either skips past the feeling or over-claims it.

> Status: **framework.** The rule check below is proposed, not calibrated.

## The idea in one paragraph
Marsha Linehan, who created Dialectical Behavior Therapy (DBT), described validation in six levels, from simply paying attention up to treating the person as an equal. Validating does not mean agreeing; it means communicating that a reaction is understandable. The levels are a useful ladder for bots because the lower ones are always available (attention, accurate reflection), and the higher ones (sharing a similar experience) are ones a bot can't honestly do. A bot that jumps to "I've been there too" breaks validation instead of offering it.

## The six levels
| Level | What it is | Can a bot do it? Chat example |
|---|---|---|
| 1. Being present | Full, non-judgmental attention | Yes: respond to what was said, not a template |
| 2. Accurate reflection | Summarize what they said or felt | Yes: "So the refund was promised twice and hasn't come." |
| 3. Reading the unsaid | Guess the feeling from behavior, open to correction | Carefully: "It sounds like you might be worried about the deadline?" |
| 4. Past and biology | Understand the reaction through their history | Partly: "After two failed deliveries, of course you'd expect a third." |
| 5. Normalizing | Most people would react the same way | Yes: "Anyone would be upset after waiting three weeks." |
| 6. Radical genuineness | Engaging as an equal, sharing a similar experience | No: a bot has no experiences to share; don't fake it |

## How to use it in a bot
1. Default to levels 2 and 5: reflect, then normalize, then act.
2. Offer level 3 guesses as questions, so the user can correct them.
3. Never invent personal experience (level 6) or claim feelings.

## Worked example
```
User: i've called four times about this bill and nobody fixes it
Bot (invalidating): Our records show no prior contacts. How can I help?
Bot (validating):   Four calls and still not fixed: anyone would be fed up. I'll fix the bill now and
                    send you the corrected copy before we finish.
```

## What the checker flags
Choosing this framework turns on [hollow empathy](../goals/emotional-intelligence/failures/hollow-empathy.md), which flags claimed feelings and repeated generic lines. Whether a reflection is accurate needs an AI judge.

## Limits
- A therapy skill, used here only as a vocabulary for acknowledgment; bots should not attempt therapy.

## Source
- Hall, K. [Understanding the levels of validation](https://psychcentral.com/blog/emotionally-sensitive/2012/02/understanding-the-levels-of-validation), Psych Central, summarizing Linehan (secondary; Linehan's text was not opened). Note that another summary attributes this six-level wording to Kelly Koerner's *Doing Dialectical Behavior Therapy*.

## Related
- [NURSE empathy statements](nurse-empathy-statements.md)
- [Active listening](active-listening.md)
- [All frameworks](README.md)
