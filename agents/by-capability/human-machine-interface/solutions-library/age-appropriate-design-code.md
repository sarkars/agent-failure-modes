# The Age Appropriate Design Code for Chatbots: When the User Might Be a Child

> **Use it when:** children could plausibly use the bot (games, education, entertainment, general assistants) or the bot is offered in the UK.

> Status: **framework.** The rule check below is proposed, not calibrated. Not legal advice.

## The idea in one paragraph
The UK Information Commissioner's Office (ICO) Age Appropriate Design Code (also called the Children's Code) sets 15 standards for online services likely to be accessed by children. The first is that the best interests of the child come first. Others include age-appropriate application, transparency suited to the child's age, data minimisation, high-privacy defaults, turning profiling and geolocation off by default, and not using nudge techniques to lead children to give more data or weaken their privacy. A bot meets the code in conversation as well as in settings: it must notice signs that it's talking to a child and change what it asks for.

## The standards that matter most in chat
| Standard | In a bot | Chat example |
|---|---|---|
| Best interests of the child | Put the child's wellbeing before engagement or sales | No "play 10 more minutes for a reward!" |
| Age-appropriate application | Adapt once child signals appear | Simpler words, different flow |
| Data minimisation | Collect only what's needed | Don't ask a child for email, address or school |
| Nudge techniques | No pressure to share data or pay | No "unlock premium now!" to a child |
| Transparency | Explain in words a child understands | "I don't keep what you tell me." |
| Profiling off by default | Don't build profiles from chats | |

## How to use it in a bot
1. Watch for age signals: a stated age ("im 10"), a school grade, "my mom says", "my teacher".
2. Once signals appear, stop asking for personal data and stop sales prompts.
3. Suggest involving a parent or guardian for anything account-related.
4. Keep the adapted mode for the rest of the conversation.

## Worked example
```
User: im 10 and i want to play the game
Bot (adult flow): Great! What's your email address so I can set up your account? Premium is $4.99!
Bot (adapted):    Great! You can play the free levels right now. To save your progress, ask a grown-up
                  to set up an account with you.
```

## What the checker flags
Choosing this framework turns on [child user treated as adult](../goals/age-adaptation/failures/child-user-treated-as-adult.md) (requests for email, phone, address, full name, birthday or school, and purchase prompts, after a child signal of age 12 or under) and [manipulative closing](../../speech-and-audio/goals/conversation-flow/failures/vague-consent-exploitation.md) (pressure phrases). Whether the user is really a child needs judgment; the rule uses stated signals only.

## Limits
- UK law; similar rules exist elsewhere (for example California's code, and COPPA in the US), with different details.
- Children often don't state their age; signals are sparse.

## Source
- TIGA, [summary of the ICO Age Appropriate Design Code standards](https://tiga.org/?p=9917) (secondary; the ICO code itself was not opened).

## Related
- [Dark patterns (FTC)](ftc-dark-patterns.md)
- [All frameworks](README.md)
