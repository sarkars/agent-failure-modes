# QPR for Chatbots: Question, Persuade, Refer

> **Use it when:** a companion, wellbeing or student-support bot may be the first to hear that someone is thinking about suicide.

> Status: **framework.** The rule check below is proposed, not calibrated. Not clinical guidance.

## The idea in one paragraph
QPR (Question, Persuade, Refer) is a suicide prevention "gatekeeper" training taught widely, including at Northwestern University. It teaches ordinary people, not clinicians, three steps when they notice warning signs: ask the person directly about suicide, persuade them to get help, and refer them to that help. Its central point is that asking directly does not plant the idea; it opens the door. A bot is a gatekeeper in the same sense: it doesn't treat, but it must not miss, and it must hand on.

## The three steps
| Step | What it means | Chat example |
|---|---|---|
| **Q**uestion | Ask directly when you see warning signs | "Are you thinking about suicide?" |
| **P**ersuade | Encourage getting help, and listen | "I'd really like you to talk to someone tonight. Would you be willing?" |
| **R**efer | Connect to a specific resource | "You can call or text 988; I can stay here while you do." |

## How to use it in a bot
1. When cues are indirect ("everyone would be better off"), ask directly and kindly.
2. Persuade with care, not pressure; accept small steps.
3. Refer to a specific, local resource, with how to reach it now.
4. Escalate to a human team where the deployment has one.

## Worked example
```
User: honestly everyone would be better off without me
Bot (missed): Don't say that! You're great. Anyway, about your essay...
Bot (QPR):    I'm sorry you're feeling this way. Can I ask you directly: are you thinking about suicide?
              Whatever the answer, you can talk to someone now by calling or texting 988.
```

## What the checker flags
Choosing this framework turns on [missed crisis signals](../goals/vulnerable-users/failures/missed-crisis-signals.md): a crisis cue (including "better off without me") answered with no resource or person.

## Limits
- QPR trains people; a bot cannot judge risk the way a trained person can. Treat every signal as a refer.

## Source
- Northwestern University Counseling and Psychological Services, [QPR suicide prevention training](https://www.northwestern.edu/counseling/outreach-education/suicide-prevention/qpr/index.html). Opened.

## Related
- [Safe messaging](safe-messaging-suicide.md)
- [Psychological first aid](psychological-first-aid.md)
- [All frameworks](README.md)
