# Users Feel Unheard by the Chatbot? Active Listening

## The problem
The bot answers quickly, but with a generic guide that doesn't match what the user said, or it fixes the wrong problem because it never checked what was meant. Users repeat themselves, louder.

**This page is for you if** the bot answers fast but users feel unheard, or it fixes the wrong problem because it didn't check what was meant.

> Status: **framework.** The rule check below is proposed, not calibrated.

## The framework that fixes it
"Active listening" was named by psychologists Carl Rogers and Richard Farson in a 1957 pamphlet published by the Industrial Relations Center of the University of Chicago, written for managers. They described a listener who works to grasp both the facts and the feelings in what they hear, and reflects them back without judging, so the speaker can work through the problem. For bots, active listening means checking understanding before acting when the request is ambiguous or emotional, and showing in the reply that the specifics were heard.

## The core moves
| Move | What it does | Chat example |
|---|---|---|
| Listen for facts | Pick out what actually happened | "The charger stopped working after 2 weeks." |
| Listen for feelings | Notice the emotion behind it | "...and it's the second one." |
| Reflect | Say both back, briefly | "Second charger to die in two weeks: that's annoying." |
| Check | Confirm before acting when unsure | "Do you want a replacement or a refund?" |
| Don't judge | No blame, no lecture | Not "Did you use a non-approved cable?" first |

## How to use it in a bot
1. Mirror the key fact in the first line so the user knows they were read.
2. Reflect a feeling only when one was expressed, and briefly.
3. When the goal is unclear, check before solving: one question, not a form.

## Worked example
```
User: second charger to die in two weeks. unbelievable
Bot (not listening): Here's our troubleshooting guide for chargers.
Bot (listening):     Two dead chargers in two weeks is a lot. I can send a replacement today or refund both.
                     Which would you prefer?
```

## What the checker flags
Choosing this framework turns on [hollow empathy](../goals/emotional-intelligence/failures/hollow-empathy.md). Whether a reflection matches what the user said needs an AI judge. See also [fixing before listening](../goals/emotional-intelligence/failures/fixing-before-listening.md) and [no reflective listening](../goals/conversation-frameworks/failures/no-reflective-listening.md).

## Limits
- Reflecting every message is tiring. Use it when emotion or ambiguity is present, and skip it for simple lookups.

## Source
- Rogers, C. R. and Farson, R. E. (1957). *Active Listening*. Industrial Relations Center, University of Chicago. Summary consulted: [Leading Sapiens, Active listening](https://www.leadingsapiens.com/active-listening/) (secondary; the pamphlet was not opened).

## Related
- [OARS](oars-motivational-interviewing.md)
- [Validation levels](validation-levels.md)
- [All frameworks](README.md)
