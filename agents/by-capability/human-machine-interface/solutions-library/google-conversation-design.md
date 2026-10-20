# Chatbot Stacks Questions or Leaves Users Stuck? Google's Conversation Design Rules

## The problem
The bot fires three questions in one turn, re-asks something the user already said, or answers "no" and stops there. Users don't know what to say next, so they give up or start over.

**This page is for you if** you are designing the turn-by-turn flow of an assistant: how long each turn is, when the bot asks, and what it does after a "no" or a misunderstanding.

> Status: **framework.** The rule check below is proposed, not calibrated.

## The framework that fixes it
Google's conversation design guidance for the Assistant starts from Grice's cooperative principle and turns it into practical rules for bots. Its main points: keep turns brief and relevant from the user's point of view, because extra detail loads the user's short-term memory; accept the extra details cooperative users volunteer instead of making them repeat; signal clearly when it's the user's turn, usually with a question; ask one question at a time; when input isn't understood, reprompt lightly instead of with a long error; and after bad news, offer alternatives so the conversation moves forward instead of ending.

## The main rules
| Rule | What it means | Chat example |
|---|---|---|
| Brief and relevant | Short turns, focused on what the user needs now | "Your table for 4 is booked for 7 PM." |
| One question at a time | Don't stack questions or options in one turn | "What time works?" not "What time, how many people, and any allergies?" |
| Clear turn-taking | End with a cue that it's the user's turn | Close with a question when you need an answer |
| Accept volunteered details | Don't re-ask what the user already said | User said "for 4 at 7"; don't ask "how many?" |
| Lightweight reprompts | Short, specific retry after a misunderstanding | "Sorry, which day: Friday or Saturday?" |
| Move forward | After a "no", offer an alternative | "7 is full. 6:30 or 8:15?" |
| Plain words | "If you wouldn't say it, neither should your persona." | |

## How to use it in a bot
1. Write every prompt so it ends in one question or one clear next step.
2. Parse everything the user volunteered before asking anything.
3. Write two or three short reprompts for each question, each narrower than the last.
4. Never end on bad news alone; pair it with the nearest alternative.

## Worked example
```
User: book a table for 4 at 7 on friday
Bot (breaks the rules): How many people will be dining, and what time would you like? Also, do you have any
      dietary requirements or a seating preference?
Bot (follows them):     7 on Friday is full. I can do 6:30 or 8:15 for 4. Which one?
```

## What the checker flags
Choosing this framework turns on [answer-and-go conversation](../goals/conversation-leadership/failures/answer-and-go-conversation.md), which flags a reply that answers and stops with no next step, and a reply that stacks two questions. The [dead-end "I don't understand" check](../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md) is always on.

## Limits
- Written for voice and the Google Assistant, where turns must be even shorter than in chat. In a text chat, a short list is fine where voice would need one item at a time.

## Source
- Google for Developers, [Learn about conversation](https://developers.google.com/assistant/conversation-design/learn-about-conversation). Opened 2026-10-20.

## Related
- [Grice's cooperative principle](grice-cooperative-principle.md)
- [Conversation repair](conversation-repair.md)
- [Conversation moves](conversation-moves.md)
- [All frameworks](README.md)
