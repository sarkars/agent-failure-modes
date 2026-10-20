# A Trauma-Informed Approach for Chatbots: SAMHSA's Six Principles

> **Use it when:** many users may have experienced trauma or hardship: debt collection, benefits, housing, health, victim services, companion apps.

> Status: **framework.** No rule check yet; these principles need an AI judge.

## The idea in one paragraph
The US Substance Abuse and Mental Health Services Administration (SAMHSA) set out a trauma-informed approach in 2014. A trauma-informed service realizes how widespread trauma is, recognizes its signs, responds by building that knowledge into practice, and seeks to avoid re-traumatizing people. SAMHSA names six principles: safety; trustworthiness and transparency; peer support; collaboration and mutuality; empowerment, voice and choice; and cultural, historical and gender issues. For a bot, the most practical are transparency (say what will happen next and why) and choice (let the user control pace and options).

## The six principles in chat
| Principle | In a bot | Chat example (debt collection) |
|---|---|---|
| Safety | Calm, predictable, no threats | No "Failure to pay will result in..." as an opener |
| Trustworthiness and transparency | Say what happens next, and why you ask | "I'm asking about income only to find a plan you can afford." |
| Peer support | Point to people with similar experience where relevant | Support groups, advocates |
| Collaboration and mutuality | Work with the user, not on them | "Let's find a plan together." |
| Empowerment, voice and choice | Offer options; let the user set pace | "Would you rather set this up now or get the options by email?" |
| Cultural, historical and gender issues | Avoid assumptions, respect differences | No assumed family structure |

## How to use it in a bot
1. Explain every request for personal information.
2. Offer choices about pace and channel.
3. Avoid threat language and surprise consequences.
4. Let users stop and resume without penalty.

## Worked example
```
User: i lost my job and cant pay this month
Bot (not trauma-informed): Missed payments incur a $35 late fee and may be reported to credit agencies.
Bot (trauma-informed):     Thanks for telling me; that's a hard spot. There are options, including pausing
                           payments for up to 3 months. Want me to walk you through them, or send them to
                           read later?
```

## What the checker flags
No rule check yet. Whether the bot gave the user choice and explained its asks needs an AI judge.

## Limits
- An organizational framework, not a conversation script; the chat translations here are ours.

## Source
- youth.gov, [SAMHSA's concept of trauma and guidance for a trauma-informed approach](https://youth.gov/feature-article/samhsas-concept-trauma-and-guidance-trauma-informed-approach) (secondary; SAMHSA's 2014 publication was not opened).

## Related
- [Psychological first aid](psychological-first-aid.md)
- [Nonviolent Communication](nonviolent-communication.md)
- [All frameworks](README.md)
