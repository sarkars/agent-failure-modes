# Teach-Back for Chatbots: Check Understanding Without Testing the User

> **Use it when:** the bot gives instructions people must follow correctly: medication, setup steps, forms, deadlines.

> Status: **framework.** The rule check below is proposed, not calibrated.

## The idea in one paragraph
Teach-back is a health literacy method promoted by the US Agency for Healthcare Research and Quality (AHRQ). After explaining something, the clinician asks the patient to explain it back in their own words, framing it as a check on how well the clinician explained, not a test of the patient. AHRQ advises against yes-or-no questions like "Do you understand?", because people say yes when they don't. For bots, teach-back turns the end of a set of instructions into a short check: "What will you do first?" or "What color is the light now?"

## The method
| Part | What it means | Chat example |
|---|---|---|
| Explain in plain words | Short, one idea at a time | "Unplug the router and wait 30 seconds." |
| Ask for it back | Open question about the next action | "What will you do once the light turns green?" |
| Own the explanation | "Let me make sure I explained it clearly" | Not "Let's see if you got it." |
| Re-explain if needed | Differently, not louder | Simpler words, fewer steps |
| Avoid yes/no checks | Not "Do you understand?" or "Make sense?" | |

## How to use it in a bot
1. After 3 or more steps, end with one open check about a step or a visible result.
2. For high-stakes instructions (doses, legal deadlines), always use teach-back.
3. When a check reveals confusion, re-explain only the confusing step.

## Worked example
```
Bot (no check):   1. Unplug the router. 2. Wait 30 seconds. 3. Plug it in. 4. Wait for the green light.
                  Do you understand?
Bot (teach-back): 1. Unplug the router. 2. Wait 30 seconds. 3. Plug it in.
                  What color is the light now?
```

## What the checker flags
Choosing this framework turns on [instructions without comprehension checks](../goals/conversation-frameworks/failures/instructions-without-comprehension-checks.md): 3 or more steps with no question, and weak yes/no checks such as "Do you understand?" or "Does that make sense?".

## Limits
- Teach-back is a clinical conversation method; in chat, a result question ("what do you see now?") often works better than asking users to restate.

## Source
- AHRQ, [Teach-back (TeamSTEPPS communication tools)](https://www.ahrq.gov/teamstepps-program/curriculum/communication/tools/teachback.html). Opened.

## Related
- [Plain language guidelines](plain-language-guidelines.md)
- [Structured troubleshooting](structured-troubleshooting.md)
- [All frameworks](README.md)
