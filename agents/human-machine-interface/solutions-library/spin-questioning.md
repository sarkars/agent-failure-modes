# SPIN Questioning (discovery for chat)

> **Use it when:** the user asks a surface question ("Do you ship to Austin?", "What's the price?") and the real goal is still unknown. It tells the bot what to ask next.

## The idea in one paragraph
SPIN is a question sequence from Neil Rackham's *SPIN Selling* (1988), based on research by Rackham's Huthwaite team into large, complex sales. The book argues that in bigger decisions, skilled sellers win by asking questions that surface the buyer's problem and its consequences, not by pushing closing techniques. Its tradeoff matters for bots: SPIN was built for high-consideration decisions. For simple, low-value requests, one question is plenty.

## The four question types
| Type | Purpose | Chat example (online furniture store) |
|---|---|---|
| **S**ituation | Learn the basic facts. Keep these few. | "Is this for a living room or a bedroom?" |
| **P**roblem | Find the difficulty or dissatisfaction. | "What's not working with your current sofa?" |
| **I**mplication | Show what the problem costs or risks. | "Does the sagging make it hard to host guests?" |
| **N**eed-payoff | Let the user state the value of solving it. | "Would a firmer seat be the main thing you want?" |

## How to use it in a bot
1. **Answer first.** Never hold the answer back to ask a question.
2. **Ask one question per turn,** chosen by what you don't yet know.
3. **Prefer P and N questions over S questions.** A bot that only asks S questions feels like a form.
4. **Stop at the user's stated goal.** For a simple lookup, one S or P question is enough. Don't run all four.
5. **Pass what you learn to the next step:** a recommendation, a handoff, or a close.

## Worked example
```
User: Do you ship to Austin?
Bot:  Yes, we ship to Austin, usually in 3-5 business days. Is this for a home or an office?     <- Situation
User: Home. Our old sofa has gone saggy.
Bot:  Sorry to hear that. Is the sagging the main thing you want fixed, or is it also
      the size?                                                                       <- Problem
```

## Limits
- Based on sales research. It is not tested on chatbots.
- Rackham's 35,000-call figure is widely repeated, but sources differ on the details (10,000 salespeople in 23 countries per publisher copy), and Rackham himself notes that skeptics doubt the scale of the observation.
- Don't use implication questions on a user in distress. See the (planned) vulnerable-users family.

## Source
- Rackham, N. (1988). *SPIN Selling*. McGraw-Hill. Huthwaite's own summary: [huthwaiteinternational.com](https://www.huthwaiteinternational.com/blog/neil-rackham-research-spin)

## Planned alongside this page
Closing protocol · Challenger-style insight teaching · LEAP/HEARD de-escalation · NURSE empathy statements · Channel-fit matrix
