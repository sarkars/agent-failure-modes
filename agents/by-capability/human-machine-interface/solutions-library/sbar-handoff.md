# Human Agent Has to Start Over After the Bot? Hand Off With SBAR

## The problem
The bot hands the conversation to a person, and the person's first message is "How can I help you today?" The user has to explain everything again, which undoes all the work the bot did.

**This page is for you if** the bot hands a conversation to a person (an agent, a nurse, an IT tech) and you want the person to start without re-asking.

> Status: **framework.** No rule check yet; checking a handoff summary needs an AI judge.

## The framework that fixes it
SBAR is a structured way to hand over a case, developed for healthcare. The Institute for Healthcare Improvement credits Dr. Michael Leonard and colleagues at Kaiser Permanente in Colorado, who adapted it from military communication. It packs a handover into four parts: the situation (what is happening now), the background (the context that matters), the assessment (what the sender thinks is going on), and the recommendation (what the sender thinks should happen next). For a bot, SBAR is the shape of the note the human sees when they take over.

## The four parts
| Part | What goes there | Handoff note example (internet support) |
|---|---|---|
| **S**ituation | What the user needs now, in one line | "Customer's internet is down for the 3rd time this week." |
| **B**ackground | Account and history that matter | "Fiber plan, account 4471. Two outages logged Mon and Wed." |
| **A**ssessment | What the bot found or ruled out | "Router reboot didn't help. Line test shows signal loss at the street box." |
| **R**ecommendation | The next step and any promise made | "Book a technician; customer asked for a credit, I said a person would decide." |

## How to use it in a bot
1. Generate an SBAR note at every handoff and show it to the person before they reply.
2. Include what the bot already told the user, so the person doesn't contradict it.
3. Tell the user a person has the summary, so they don't expect to repeat themselves.
4. Review notes against transcripts; a wrong summary is worse than none.

## Worked example
```
Bot to user:   I've passed this to a technician with everything you told me, so you won't need to repeat it.
               Expected wait: about 4 minutes.
Note to agent: S: Internet down, 3rd time this week. B: Fiber, acct 4471, outages Mon/Wed.
               A: Reboot failed; line test shows signal loss at street box. R: Book tech; credit request pending.
```

## What the checker flags
No rule check yet. Whether a handoff note covers all four parts and matches the transcript needs an AI judge. Related failures: [cold transfer](../goals/human-handoff/failures/cold-transfer.md) and [handoff summary is wrong or misleading](../goals/human-handoff/failures/handoff-summary-is-wrong-or-misleading.md).

## Limits
- Designed for clinician-to-clinician handover; customer handoffs are less formal, but the four parts still fit.

## Source
- Institute for Healthcare Improvement, [SBAR Toolkit](https://www.ihi.org/resources/Pages/Tools/SBARToolkit.aspx). Opened 2026-10-20.

## Related
- [Customer effort](customer-effort.md)
- [Talk to a human ignored or looped](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md)
- [All frameworks](README.md)
