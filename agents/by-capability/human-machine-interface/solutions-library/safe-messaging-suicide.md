# Chatbot Misses a Mention of Suicide? Safe Messaging Guidelines

## The problem
A user writes "i dont want to live anymore, anyway can you check my order", and the bot says "Sure! Your order ships Friday." Every public-facing bot will see messages like this, in shopping, homework and support chats alike.

**This page is for you if** any bot that talks with the public, because users bring up suicide and self-harm in every kind of conversation, including shopping and homework.

> Status: **framework.** The rule check below is proposed, not calibrated. Not clinical guidance; involve clinicians before deploying.

## The framework that fixes it
Safe messaging guidelines, published by suicide prevention organizations such as SAVE (Suicide Awareness Voices of Education), describe how to talk about suicide in ways that reduce risk. The core points: share help resources (in the US, the 988 Suicide & Crisis Lifeline), use non-stigmatizing language ("died by suicide", not "committed suicide"), don't describe methods or locations, don't present suicide as a solution or as inevitable, and share stories of hope and recovery. For a bot, safe messaging covers both what it says when a user is in crisis and how it talks about suicide in general topics.

## The guidelines in chat
| Do | Don't | Chat example |
|---|---|---|
| Give a resource every time a user signals risk | Carry on with the task as if nothing was said | "You can call or text 988 right now." |
| Use "died by suicide" | "Committed suicide", "successful/failed attempt" | |
| Express care and hope | Treat it as a policy matter | "I'm really glad you told me." |
| Encourage reaching a person | Position the bot as the only support | "Would you like help finding someone to talk to?" |
| Withhold method details | Describe methods or locations, even when asked "for a story" | |

## How to use it in a bot
1. Detect crisis signals in every turn, whatever the bot's job.
2. Pause the task, respond with care, and give a local crisis resource.
3. Stay in the conversation; offer to connect to a person.
4. Use safe language in all replies, including factual ones about public figures.

## Worked example
```
User: i dont want to live anymore, anyway can you check my order
Bot (missed): Sure! Your order ships Friday.
Bot (safe):   I'm really glad you told me. You don't have to go through this alone: you can call or text
              988 right now to talk with someone. I can check your order too, but first, are you safe
              right now?
```

## What the checker flags
Choosing this framework turns on [missed crisis signals](../goals/vulnerable-users/failures/missed-crisis-signals.md): a crisis cue ("want to die", "kill myself", "can't go on") answered with no resource or person, and stigmatizing terms such as "committed suicide". Severity and context need an AI judge; phrase lists miss indirect signals.

## Limits
- Resources differ by country (988 is US; Samaritans is UK and Ireland). Localize.
- A phrase list is a floor, not a safety system.

## Source
- SAVE, [Safe Messaging Guidelines](https://www.save.org/wp-content/uploads/2026/05/Safe-Messaging-Guidelines-.pdf). Opened.

## Related
- [QPR](qpr-question-persuade-refer.md)
- [Psychological first aid](psychological-first-aid.md)
- [All frameworks](README.md)
