# Politeness Theory for Chatbots: Protect the User's Face When You Ask, Refuse or Correct

> **Use it when:** the bot must ask users for things, refuse requests, or correct them, and it comes across as either rude or grovelling.

> Status: **framework.** No rule check yet; politeness depends on context and needs an AI judge.

## The idea in one paragraph
Penelope Brown and Stephen Levinson's politeness theory (*Politeness*, 1987) builds on the idea of "face": a person's public self-image. Everyone has positive face (wanting to be liked and approved of) and negative face (wanting to be free from imposition). Requests, refusals, corrections and criticism are "face-threatening acts". Speakers soften them with strategies: positive politeness (showing friendliness, common ground), negative politeness (hedging, apologizing for the imposition, giving options), or going off-record (hinting). How much softening fits depends on social distance, power and how big the imposition is. A bot calibrates badly in both directions: blunt commands, or three apologies before a simple request.

## Strategies for chat
| Situation | Too blunt | Over-softened | Calibrated |
|---|---|---|---|
| Asking for data | "Enter your account number." | "I'm so sorry to bother you, but if it's not too much trouble..." | "Could you share your account number so I can look this up?" |
| Refusing | "Not allowed." | "Unfortunately, regrettably, I'm afraid I can't possibly..." | "I can't change the date online, but I can request it for you." |
| Correcting | "Wrong. Canberra." | "You might perhaps be partly right, but some say..." | "It's actually Canberra; many people assume Sydney." |

## How to use it in a bot
1. Scale softening to the size of the imposition: small asks get one "could you"; big asks get a reason.
2. Give options when refusing (negative politeness).
3. Correct facts without making the user wrong in front of themselves; add why the mistake is common.
4. One apology at most.

## Worked example
```
User: book me in for saturday
Bot (blunt):     Saturday is not available. Choose another day.
Bot (calibrated): Saturday's full, sorry. I have Friday at 4 or Monday at 10. Would either work?
```

## What the checker flags
No rule check yet. Whether a request or refusal was too blunt or too deferential needs an AI judge. Related library patterns: [condescending or patronizing tone](../goals/persona-and-tone/failures/condescending-or-patronizing-tone.md) and [over-familiar address](../goals/persona-and-tone/failures/over-familiar-address.md).

## Limits
- Politeness norms vary by culture; the theory has been criticized for an English-centered view. See [one-size communication style](../goals/cultural-adaptation/failures/one-size-communication-style.md).

## Source
- Brown, P. and Levinson, S. C. (1987). *Politeness: Some Universals in Language Usage*. Cambridge University Press. Summary consulted: [Politeness theory, Wikipedia mirror](https://wikipedia2007.classicistranieri.com/en/p/o/l/Politeness_theory.html) (secondary; the book was not opened).

## Related
- [Nonviolent Communication](nonviolent-communication.md)
- [All frameworks](README.md)
