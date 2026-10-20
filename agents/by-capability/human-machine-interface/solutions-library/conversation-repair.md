# Conversation Repair for Chatbots: How People Fix Misunderstandings, and How Bots Should

> **Use it when:** the bot misunderstands users, or users have to say the same thing twice. Repair is what keeps a misunderstanding from becoming a dead end.

> Status: **framework.** The rule check below is proposed, not calibrated.

## The idea in one paragraph
Conversation analysis studies how real talk is organized, turn by turn. In a 1977 paper, Emanuel Schegloff, Gail Jefferson and Harvey Sacks showed that people handle trouble in speaking, hearing or understanding through "repair", and that it follows a pattern: the speaker usually gets the first chance to fix their own trouble, and when the other person starts the repair, they usually do it with a targeted question ("Friday this week?") rather than a blanket "What?". Self-repair is strongly preferred. For a bot, that means two things: a good repair names what was missed, and the same blanket "I didn't get that" twice is not repair at all.

## Repair moves
| Move | What it does | Chat example |
|---|---|---|
| Targeted question | Names the part that was missed | "Which order: the one from May 3 or May 10?" |
| Candidate understanding | Offers a guess to confirm | "Do you mean the blue jacket?" |
| Partial repeat | Repeats what was understood, asks for the rest | "Moving your booking to Friday, and what time?" |
| Narrowing | Each retry gets more specific | Open question, then choices, then a person |
| Blanket "huh?" | Says nothing about what failed | "Sorry, I didn't get that." (weakest) |

## How to use it in a bot
1. **Never send the same fallback twice.** The second try narrows: offer 2-4 choices.
2. **Say what you did understand** and ask only about the missing part.
3. **Offer a candidate** when you have one ("Did you mean X?").
4. **After two failed repairs, hand off** or offer a different channel.

## Worked example
```
User: change it to the 14th
Bot (no repair):  Sorry, I didn't understand. Could you rephrase?
Bot (repair):     Move your dentist booking from the 12th to Thursday the 14th? Same time, 3 PM?
```

## What the checker flags
The [dead-end "I don't understand" check](../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md) is always on: it flags the same fallback twice in a row. Choosing this framework shows it as the basis for that check. Whether a repair targets the right part needs an AI judge.

## Limits
- Conversation analysis describes human talk; bots can't read tone or pauses, so they must ask more explicitly.

## Source
- Schegloff, E. A., Jefferson, G. and Sacks, H. (1977). "The Preference for Self-Correction in the Organization of Repair in Conversation." *Language* 53(2): 361-382. Citation consulted: [EMCA wiki](https://emcawiki.net/Schegloff1977) (the paper itself was not opened).

## Related
- [Google conversation design: lightweight reprompts](google-conversation-design.md)
- [Talk to a human ignored or looped](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md)
- [Conversation moves: offer choices](conversation-moves.md)
- [All frameworks](README.md)
