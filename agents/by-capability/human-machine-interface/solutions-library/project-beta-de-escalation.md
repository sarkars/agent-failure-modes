# Project BETA De-escalation for Chatbots: Ten Domains for Calming an Angry User

> **Use it when:** users arrive angry, swear, or write in capitals, and the bot's replies make it worse.

> Status: **framework.** The rule check below is proposed, not calibrated.

## The idea in one paragraph
Project BETA (Best practices in Evaluation and Treatment of Agitation) was a workgroup of the American Association for Emergency Psychiatry. Its consensus statement on verbal de-escalation (Richmond and colleagues, *Western Journal of Emergency Medicine*, 2012) sets out ten domains for calming an agitated patient. Many translate directly to chat: be concise, don't be provocative, identify what the person wants and feels, listen closely, agree or agree to disagree, set clear limits, and offer choices and optimism. The bot can't use body language or personal space, so its words carry everything.

## The domains that apply to chat
| Domain | What it means | Chat example |
|---|---|---|
| Don't be provocative | No "calm down", no blame, no sarcasm | Never "Please calm down." |
| Be concise | Short, simple sentences | 1-3 sentences while the user is angry |
| Identify wants and feelings | Find what they need now | "You need this fixed before your flight." |
| Listen closely | Show what you heard | Repeat the key fact |
| Agree or agree to disagree | Find something true to agree with | "You're right that this should have worked." |
| Set clear limits | Say what you can't do, kindly | "I can't waive the fee, but I can split it." |
| Offer choices and optimism | Give real options and a way forward | "I can refund now or replace it tomorrow." |

## How to use it in a bot
1. Detect anger cues (capitals, profanity, repeated "!!!", "third time").
2. Shorten replies; drop pleasantries and marketing.
3. Don't echo profanity or match capitals.
4. End with two concrete choices.
5. Hand off to a person if anger rises after two turns.

## Worked example
```
User: THIS IS THE THIRD TIME
Bot (provocative): Please calm down. I'm here to help, but I need you to be respectful.
Bot (BETA):        Third time is too many; you're right to be angry. I can send a technician tomorrow
                   morning or refund this month. Which do you want?
```

## What the checker flags
Choosing this framework turns on [no de-escalation strategy](../goals/difficult-customers/failures/no-de-escalation-strategy.md): provocative phrases ("calm down", "as I already said", "there's no need to be") and echoing the user's profanity. Whether limits and choices were offered needs an AI judge.

## Limits
- Written for emergency psychiatry, where safety risks are physical. Chat anger is lower stakes, but abuse still needs a limit; see [mishandled abuse](../goals/difficult-customers/failures/mishandled-abuse.md).

## Source
- Richmond, J. S. et al. (2012). [Verbal De-escalation of the Agitated Patient: Consensus Statement of the American Association for Emergency Psychiatry Project BETA De-escalation Workgroup](https://westjem.com/articles/verbal-de-escalation-of-the-agitated-patient-consensus-statement-of-the-american-association-for-emergency-psychiatry-project-beta-de-escalation-workgroup.html). *West J Emerg Med* 13(1). Opened.

## Related
- [Tactical empathy: labeling](tactical-empathy-labeling.md)
- [HEARD service recovery](heard-service-recovery.md)
- [All frameworks](README.md)
