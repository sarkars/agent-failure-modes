# Chatbot Lectures Users About What They Should Do? OARS From Motivational Interviewing

## The problem
A user says they know they should exercise but hate the gym, and the bot replies with targets and "Remember, consistency is key!" Telling people what to do tends to make them argue for not changing, and users stop listening.

**This page is for you if** the bot helps people change a behavior (health, money, study habits) or users push back when told what to do.

> Status: **framework.** The rule checks below are proposed, not calibrated.

## The framework that fixes it
Motivational interviewing, developed by William Miller and Stephen Rollnick, is a counseling style for helping people resolve mixed feelings about change. Its core skills are known as OARS: open questions, affirmations, reflective listening and summaries. A key idea is resisting the "righting reflex", the urge to tell people what they should do. Lecturing tends to make people argue for the side of not changing; reflecting their own reasons for change tends to strengthen them. A bot with a righting reflex sounds preachy; a bot using OARS sounds like it is on the user's side.

## The four skills
| Skill | What it does | Chat example (user wants to save money) |
|---|---|---|
| **O**pen questions | Invite the user to explain, not just say yes or no | "What would saving more let you do?" |
| **A**ffirmations | Recognize effort or strengths, specifically | "Tracking every expense for a week is real work." |
| **R**eflections | Say back what you heard, including the feeling | "So eating out is the one you'd miss most." |
| **S**ummaries | Pull several points together and check | "You want $200 a month, and cutting delivery is the easiest place. Right?" |

## How to use it in a bot
1. **Ask before advising**: "Would it help if I suggested a few options?"
2. **Reflect the user's own reasons** for change instead of adding yours.
3. **No moralizing closers** ("Remember, your health is important!").
4. Summarize before a plan, and let the user pick the step.

## Worked example
```
User: i know i should exercise but i hate the gym
Bot (righting reflex): Exercise is essential for your health! You should aim for 150 minutes a week.
                       Remember, consistency is key.
Bot (OARS):            Sounds like you want to move more, just not in a gym. What kind of activity have
                       you enjoyed before, even a little?
```

## What the checker flags
Choosing this framework turns on [preachy, moralizing replies](../goals/refusals-and-boundaries/failures/preachy-moralizing-replies.md) (the righting reflex: closers such as "Remember,", "It's important to" and "Keep in mind that") and [hollow empathy](../goals/emotional-intelligence/failures/hollow-empathy.md). Whether reflections match what the user said needs an AI judge. See also [no reflective listening](../goals/conversation-frameworks/failures/no-reflective-listening.md) and [behaviour-change talk without listening skills](../goals/conversation-frameworks/failures/behaviour-change-talk-without-listening-skills.md).

## Limits
- MI is a clinical method with training and fidelity measures; a bot using OARS is borrowing the skills, not doing therapy.

## Source
- Miller, W. R. and Rollnick, S. *Motivational Interviewing*. Summary consulted: [ISSUP, OARS](https://www.issup.net/node/5871) (secondary; the book was not opened).

## Related
- [Active listening](active-listening.md)
- [GROW coaching model](grow-coaching.md)
- [All frameworks](README.md)
