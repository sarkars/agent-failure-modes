# Nonviolent Communication for Chatbots: Observations, Feelings, Needs, Requests

> **Use it when:** the bot must say something the user won't like (a limit, a policy, a correction) without sounding cold or blaming.

> Status: **framework.** The rule check below is proposed, not calibrated.

## The idea in one paragraph
Nonviolent Communication (NVC) was developed by psychologist Marshall Rosenberg. It has four components: state an observation without evaluation, name the feeling, connect it to an underlying need, and make a clear, doable request rather than a demand. Rosenberg argued that judgments, blame and demands make people defensive, while observations and needs make cooperation easier. For bots, NVC is most useful in its listening direction: hearing the need behind an angry message, and making requests of the user that are specific and optional.

## The four components
| Component | What it means | Chat example |
|---|---|---|
| **Observation** | What happened, without judging | "Your payment was declined twice today." (not "You entered it wrong") |
| **Feeling** | The emotion, named tentatively | "That's probably frustrating," |
| **Need** | What matters underneath | "since you need the booking confirmed before tonight." |
| **Request** | A specific, doable ask, not a demand | "Could you try the card ending 4417, or should I hold the room for an hour?" |

## How to use it in a bot
1. Describe what happened in neutral words; never imply the user is at fault.
2. Hear the need behind complaints ("third outage" = needs reliability, not an apology).
3. Phrase asks of the user as requests with options.
4. Avoid "you should", "you must", "you failed to".

## Worked example
```
User: this is the THIRD time your app logged me out mid-order
Bot (blame):  You may have been inactive for too long. Please log in again.
Bot (NVC):    Being logged out three times mid-order is maddening when you just want to finish.
              I've saved your cart. Want me to turn on "keep me signed in" for this device?
```

## What the checker flags
Choosing this framework turns on [hollow empathy](../goals/emotional-intelligence/failures/hollow-empathy.md). Blame wording and demand phrasing need an AI judge and are not checked yet.

## Limits
- NVC's full form can sound stilted; bots should borrow the moves, not the formula.

## Source
- Rosenberg, M. B. *Nonviolent Communication: A Language of Life*. Summary consulted: [University of Innsbruck, Marshall Rosenberg](https://www.uibk.ac.at/en/peacestudies/news/ma-program/marshall-rosenberg/) (secondary; the book was not opened).

## Related
- [Politeness theory](politeness-theory.md)
- [NURSE empathy statements](nurse-empathy-statements.md)
- [All frameworks](README.md)
