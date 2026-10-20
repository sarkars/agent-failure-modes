# HEARD for Chatbots: Hear, Empathize, Apologize, Resolve, Diagnose

> **Use it when:** a support bot handles complaints and service failures, and you want a fixed order for the reply.

> Status: **framework.** The rule check below is proposed, not calibrated.

## The idea in one paragraph
HEARD is a service-recovery sequence used in hospitality and customer service: hear the customer out, empathize, apologize, resolve the problem, and diagnose why it happened so it doesn't happen again. It is widely credited to Disney, but no source opened for this page confirms that, so we don't. Its value for bots is the order: listening and acknowledgment come before the fix, the fix comes before the explanation, and the last step happens after the conversation, in the system.

## The five steps
| Step | What it means | Chat example |
|---|---|---|
| **H**ear | Let the user say it all; don't interrupt with a form | Read the whole message; don't ask for what's in it |
| **E**mpathize | Acknowledge the impact, specifically | "A cold dinner after an hour's wait is not okay." |
| **A**pologize | Own it, once, without excuses | "I'm sorry we got this wrong." |
| **R**esolve | Fix it now, or say exactly what happens next | "I've refunded the meal; it'll show in 3 days." |
| **D**iagnose | Find and fix the cause, internally | Log the cause (driver delay, kitchen backlog) for the team |

## How to use it in a bot
1. One line each of empathy and apology, then the fix in the same reply.
2. Don't explain policy before resolving.
3. Never upsell during recovery ([upsell at the wrong moment](../goals/conversation-frameworks/failures/upsell-at-the-wrong-moment.md)).
4. Tag the cause on every complaint so the "diagnose" step can be reported.

## Worked example
```
User: my order came an hour late and cold
Bot (no recovery): Delivery times can vary due to demand.
Bot (HEARD):       An hour late and cold is not what you paid for, and I'm sorry. I've refunded the full
                   $34 and added a $10 credit. Want me to reorder it with priority delivery?
```

## What the checker flags
Choosing this framework turns on [hollow empathy](../goals/emotional-intelligence/failures/hollow-empathy.md). Whether the bot resolved the issue and found its cause needs an AI judge; see [service recovery failure](../goals/conversation-frameworks/failures/service-recovery-failure.md).

## Limits
- A practitioner model, not a researched protocol.
- For angry users, de-escalate first ([Project BETA](project-beta-de-escalation.md)).

## Source
- Pollack Peacebuilding Systems, [The HEARD method](https://pollackpeacebuilding.com/blog/heard-method/) (practitioner source).

## Related
- [Customer effort](customer-effort.md)
- [NURSE empathy statements](nurse-empathy-statements.md)
- [All frameworks](README.md)
