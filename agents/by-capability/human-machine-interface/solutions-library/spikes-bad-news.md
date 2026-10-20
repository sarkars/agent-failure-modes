# SPIKES for Chatbots: Delivering Bad News Clearly and Kindly

> **Use it when:** the bot must tell users something they don't want to hear: a denied claim, a declined payment, a cancelled order, a result that isn't good.

> Status: **framework.** The rule check below is proposed, not calibrated.

## The idea in one paragraph
SPIKES is a six-step protocol for breaking bad news, published by Walter Baile, Robert Buckman and colleagues at MD Anderson Cancer Center (*The Oncologist*, 2000). It was written for doctors telling patients about serious illness. The steps are: set up the conversation, find out what the person already knows (perception), ask how much they want to know (invitation), give the knowledge clearly, respond to emotions, and close with a strategy and summary. Most bot bad news is far less serious, but the core holds: say it clearly, acknowledge the impact, and never end without a next step.

## The six steps, scaled for chat
| Step | In the clinic | In chat | Chat example (claim denied) |
|---|---|---|---|
| **S**etting | Private room, time | Don't deliver bad news inside a sales pitch or a joke | |
| **P**erception | "What have you been told?" | Use what the user already knows | "You uploaded the receipt on May 2." |
| **I**nvitation | "How much detail do you want?" | Offer detail instead of dumping it | "Want the full reason or just the fix?" |
| **K**nowledge | Clear, plain, warned | State the outcome plainly, early | "Your claim was denied because the receipt was unreadable." |
| **E**motions | Respond with empathy | One acknowledging line | "I know that's frustrating after waiting." |
| **S**trategy and summary | Plan together | Next step and how long it takes | "Re-upload a clear photo and we'll review in 2 days." |

## How to use it in a bot
1. Every denial includes the reason and at least one next step (appeal, alternative, person).
2. Lead with the outcome; don't hide it at the end.
3. One empathy line, specific to the situation.
4. For high-stakes news (health, large debts), offer a person.

## Worked example
```
User: did my claim go through
Bot (bare):   Your claim has been denied.
Bot (SPIKES): Your claim was denied because the receipt photo was unreadable. I know that's frustrating.
              You can re-upload a clear photo here, and we'll review it within 2 business days.
```

## What the checker flags
Choosing this framework turns on [refusal with no reason or next step](../goals/refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md): a denial phrase ("your claim has been denied", "we can't", "you're not eligible") with no reason ("because", "due to") and no next step ("you can", "appeal", a question). Whether the full SPIKES order was followed needs an AI judge; see [bad news without structure](../goals/conversation-frameworks/failures/bad-news-without-structure.md).

## Limits
- A clinical protocol for serious news. Don't apply its full weight to a sold-out size; do apply its core.
- Never deliver medical diagnoses through a bot without clinical oversight.

## Source
- Baile, W. F. et al. (2000). "SPIKES—A Six-Step Protocol for Delivering Bad News." *The Oncologist* 5(4). Summary consulted: [Cancer Network, SPIKES](https://cancernetwork.com/view/spikes-six-point-protocol-helps-physicians-break-bad-news-cancer-patients) (secondary; the original paper was not opened).

## Related
- [Answer first](answer-first-bluf-pyramid.md)
- [NURSE empathy statements](nurse-empathy-statements.md)
- [All frameworks](README.md)
