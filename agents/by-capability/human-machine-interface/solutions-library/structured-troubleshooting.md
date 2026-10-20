# Support Bot Dumps Every Fix at Once? One Step, One Check (Structured Troubleshooting)

## The problem
A user says their Wi-Fi keeps dropping, and the bot replies with a list of every fix from restarting the router to reinstalling the operating system. The user doesn't know which step worked, or whether any did.

**This page is for you if** an IT help desk or product support bot walks users through fixing something.

> Status: **framework.** Built from the library's own patterns, not an outside standard. The rule check below is proposed, not calibrated.

## The framework that fixes it
Good troubleshooting is a loop: gather the symptoms, try the most likely and least disruptive fix, check whether it worked, and only then move on, saying what has been ruled out. Bots tend to break the loop by sending every step at once, never checking the result, or restarting from step one when the user returns. This page collects the rules from the library's troubleshooting patterns into one framework, and pairs naturally with [teach-back](teach-back.md) for checking steps and [Five Whys](five-whys.md) for finding the cause.

## The loop
| Step | What the bot does | Chat example (Wi-Fi drops) |
|---|---|---|
| Gather | Ask for the one symptom that splits the cases | "Does it drop on every device, or just the laptop?" |
| Try | Give one step, least disruptive first | "Turn Wi-Fi off and on from the menu bar." |
| Check | Ask for the result, in observable terms | "Does the icon show full bars now?" |
| Record | Say what's ruled out | "So it's not the router; it's this laptop." |
| Escalate | After a set number of failed steps, hand off | Pass the steps tried to the tech (see [SBAR](sbar-handoff.md)) |

## How to use it in a bot
1. Send one step at a time when each depends on the last; a numbered list only when the user asks for all steps.
2. After any list of 3+ steps, ask what the user sees now.
3. Keep a running "tried so far" list and never repeat a step.
4. Stop and escalate if a step risks data loss.

## Worked example
```
User: wifi keeps dropping on my laptop
Bot (unstructured): Try these: 1. Restart router 2. Update drivers 3. Reset network settings 4. Reinstall OS.
Bot (structured):   Does it drop on your phone too, or only the laptop?
```

## What the checker flags
Choosing this framework turns on [instructions without comprehension checks](../goals/conversation-frameworks/failures/instructions-without-comprehension-checks.md): 3 or more steps with no question to confirm the result. Whether the steps were in a sensible order needs an AI judge; see [unstructured troubleshooting](../goals/conversation-frameworks/failures/unstructured-troubleshooting.md).

## Limits
- Our synthesis of the library's patterns, not an external standard.

## Source
- [Unstructured troubleshooting](../goals/conversation-frameworks/failures/unstructured-troubleshooting.md) and [symptom fixed, root cause missed](../goals/conversation-frameworks/failures/symptom-fixed-root-cause-missed.md), with their cited sources.

## Related
- [Five Whys](five-whys.md)
- [Teach-back](teach-back.md)
- [All frameworks](README.md)
