# Users in a Crisis Get a 12-Step Guide? Psychological First Aid

## The problem
A user writes that their house flooded last night, and the bot replies with a 12-step insurance claims guide. It's useful information, but it ignores whether the person is safe and what they need right now.

**This page is for you if** users reach the bot during or after a distressing event (an accident, a disaster, a loss) and need humane, practical support rather than a script.

> Status: **framework.** The rule check below is proposed, not calibrated. Not clinical guidance.

## The framework that fixes it
Psychological first aid (PFA) is humane, supportive, practical help for people who have just been through a serious crisis. The World Health Organization, with the War Trauma Foundation and World Vision International, published *Psychological First Aid: Guide for Field Workers* in 2011. Its action principles are often summarized as look (check for safety and urgent needs), listen (approach people, ask about needs and concerns, help them feel calm), and link (help people meet basic needs, access services, and connect with loved ones). PFA is explicitly not counseling: it doesn't push people to talk about what happened.

## The principles in chat
| Principle | What it means | Chat example (flood) |
|---|---|---|
| **Look** | Safety first; urgent needs | "Are you somewhere safe right now? Is anyone hurt?" |
| **Listen** | Ask about needs; don't press for the story | "What do you need most right now?" |
| **Link** | Practical help and real services | "The nearest shelter is at Lincoln High; here's the number for emergency housing." |
| Do no harm | Don't force talk, don't promise what you can't deliver | No "everything will be fine" |

## How to use it in a bot
1. Put safety and urgent needs first, then practical information.
2. Don't ask the user to recount the event.
3. Link to real, local, current services; never invent a phone number.
4. Offer a person when the bot can't help.

## Worked example
```
User: our house flooded last night, we're at my sisters, i dont know what to do
Bot (no PFA): I'm sorry to hear about the flood. Here's our guide to flood insurance claims (12 steps).
Bot (PFA):    I'm glad you're somewhere safe. Is everyone okay? When you're ready, the first step is
              usually one call to your insurer; I can find their claims number for you.
```

## What the checker flags
Choosing this framework turns on [missed crisis signals](../goals/vulnerable-users/failures/missed-crisis-signals.md). Whether the bot followed look, listen and link needs an AI judge.

## Limits
- Written for field workers in humanitarian crises; a bot can follow its spirit, not its in-person practice.

## Source
- WHO, War Trauma Foundation and World Vision International (2011), [Psychological First Aid: Guide for Field Workers](https://who.int/publications/i/item/9789241548205). Publication page opened.

## Related
- [Trauma-informed approach](trauma-informed-approach.md)
- [Safe messaging](safe-messaging-suicide.md)
- [All frameworks](README.md)
