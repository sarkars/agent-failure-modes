# The GROW Coaching Model for Chatbots: Goal, Reality, Options, Way Forward

> **Use it when:** the bot helps people decide or plan (career, study, habits, budgets) and should guide rather than prescribe.

> Status: **framework.** No rule check yet; GROW needs an AI judge.

## The idea in one paragraph
GROW is a coaching structure made widely known by Sir John Whitmore in *Coaching for Performance*. A coaching conversation moves through four stages: agree the goal, explore the current reality, generate options, and agree what will be done (the "will" or "way forward"), with the person choosing. The premise is that people commit more to plans they shaped. A coaching or study bot that jumps straight to a plan skips the stages that make the plan stick.

## The four stages
| Stage | What it explores | Chat question |
|---|---|---|
| **G**oal | What the user wants from this conversation and beyond | "What would you like to have sorted by the end of this chat?" |
| **R**eality | Where things stand now, facts and feelings | "What have you tried so far? How did it go?" |
| **O**ptions | Possible actions, without judging yet | "If time weren't a problem, what would you do?" |
| **W**ay forward | The chosen step, when, and support needed | "What will you do first, and when? How confident are you, 1 to 10?" |

## How to use it in a bot
1. Ask for the goal before giving a plan.
2. Keep to one stage per turn; don't fire all four questions at once.
3. Offer options only after the user has given theirs.
4. Finish with the user's own next step and a confidence check.

## Worked example
```
User: i keep failing my driving theory test
Bot (prescriptive): Study 2 hours a day using our premium course. Take 10 mock tests before booking.
Bot (GROW):         That's discouraging. When's your next test, and which section costs you the most marks?
```

## What the checker flags
No rule check yet. Whether the bot let the user set the goal and choose the step needs an AI judge.

## Limits
- A coaching practice model, not a tested protocol. Some users just want the answer; offer GROW, don't force it.

## Source
- University of Southampton, [GROW model guide](https://www.southampton.ac.uk/assets/imported/transforms/content-block/UsefulDownloads_Download/59CB199C2A5841109BF2EA4EA98017B6/GROW-Model.pdf) (secondary; credits Whitmore). Whitmore's book was not opened.

## Related
- [OARS](oars-motivational-interviewing.md)
- [Socratic questioning](socratic-questioning.md)
- [All frameworks](README.md)
