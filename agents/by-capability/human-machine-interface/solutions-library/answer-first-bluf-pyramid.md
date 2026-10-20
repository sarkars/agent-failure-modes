# Chatbot Buries the Answer? Put It First, With BLUF and the Pyramid Principle

## The problem
The reply is correct, but the user has to read four lines of background, caveats and "great question" before finding out whether they got an answer. On a phone, many won't get that far.

**This page is for you if** the bot's replies are correct but users have to read to the end to find out whether they got an answer.

> Status: **framework.** The rule check below is proposed, not calibrated.

## The framework that fixes it
Two writing traditions say the same thing: put the conclusion first. "Bottom line up front" (BLUF) is a convention of military and business writing: the first line states the decision, answer or request. Barbara Minto's *The Pyramid Principle*, written from her work at McKinsey, says to start with the answer and then work down through the supporting ideas, so the reader knows what the details are for. Minto's SCQ intro (situation, complication, question) exists only to set up the question that the main point answers. For a chatbot, the user's message already is the question, so the setup can usually be skipped and the reply can open on the answer.

## The shape of an answer-first reply
| Layer | What goes there | Chat example |
|---|---|---|
| Answer | The direct answer, or the decision, in the first sentence | "Yes, within 30 days of delivery, if they still work." |
| Support | Only the reasons or conditions the user needs | "Bring the box if you still have it." |
| Next step | One action or question | "Want me to start the return?" |

## How to use it in a bot
1. **First sentence = answer.** If the honest answer is "it depends", name the one thing it depends on and ask about it.
2. **No restating the question**, no "Great question", no background before the answer.
3. **Order support by importance**, not by the order the bot thought of it.
4. **Bad news is still the bottom line.** Put the "no" first, then the reason and the alternative (see [SPIKES](spikes-bad-news.md) for when to slow down).

## Worked example
```
User: Can I return opened headphones?
Bot (buried): When it comes to returns, there are a few things to know. Policies vary by product category,
      purchase date and condition. For electronics... So in short: yes, within 30 days.
Bot (answer first): Yes, within 30 days of delivery, if they still work. Want me to start the return?
```

## What the checker flags
Choosing this framework turns on [answer buried](../goals/response-structure/failures/answer-buried.md): after a user's question, a reply of 3 or more sentences whose first sentence is setup, such as "there are several", "when it comes to", "before we dive", "let me explain" or a restatement ("you're asking about"). Praise openers like "Great question" are caught by the always-on [filler](../goals/response-structure/failures/filler-and-padding.md) check.

## Limits
- BLUF assumes the answer is known. When the bot needs one fact first, asking for it is the answer-first move.
- Minto wrote for documents and presentations; short chat turns need far less structure.

## Source
- Minto, B. *The Pyramid Principle: Logic in Writing and Thinking*. Summary consulted: [Lessons from Barbara Minto](https://www.antoinebuteau.com/lessons-from-barbara-minto/) (secondary; the book was not opened).
- BLUF is a common writing convention; no single primary source was opened for it.

## Related
- [Grice's cooperative principle](grice-cooperative-principle.md)
- [Conversation moves: lead with the answer](conversation-moves.md)
- [All frameworks](README.md)
