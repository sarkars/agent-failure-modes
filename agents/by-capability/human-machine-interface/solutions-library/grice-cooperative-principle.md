# Chatbot Says Too Much or Goes Off Topic? Grice's Four Rules of Cooperative Conversation

## The problem
Users ask a one-line question and get six lines back, or a safety lecture they didn't ask for, or a hedge on every sentence. Each of these feels slightly off, and together they make a bot feel evasive and padded. The problem is that the bot isn't sizing its reply to what the user actually needs.

**This page is for you if** you want one test for every reply, whatever the bot does. Most "the bot talks too much", "the bot lectures" and "the bot hedges everything" complaints are breaks of one of these four rules.

> Status: **framework.** The rule checks below are proposed, not calibrated against human-labeled conversations.

## The framework that fixes it
The philosopher Paul Grice argued (1975) that conversation works because both sides assume the other is cooperating. From that assumption he drew four maxims: give as much information as the exchange needs and no more (quantity), say only what you believe true and can back up (quality), be relevant (relation), and be clear, brief and orderly (manner). People notice when a maxim is broken and read meaning into it. When a bot breaks one by accident, users read it as evasive, padded, or preachy. Google's conversation design guidelines build on the same maxims (see [Google conversation design](google-conversation-design.md)).

## The four maxims
| Maxim | What it asks | Chat failure when it is broken |
|---|---|---|
| **Quantity** | As informative as needed, and no more | A 6-line reply to "what time zone is Denver in?" |
| **Quality** | Don't say what you believe false or can't support | A confident answer with no way to check it |
| **Relation** | Be relevant to what the user is doing | A safety lecture on a question that didn't ask for one |
| **Manner** | Avoid obscurity and ambiguity; be brief and orderly | The answer buried under background |

## How to use it in a bot
1. **Size the reply to the question.** A one-fact question gets one sentence. Add detail only when the user's goal needs it.
2. **Say what you don't know.** If you can't verify something, say so and say how the user can check.
3. **Cut what the user didn't ask for.** Warnings, morals and "remember" closers count as extra unless the stakes call for them.
4. **Put the answer first** and keep the order the user would follow.

## Worked example
```
User: what gauge wire for a 30 amp circuit
Bot (breaks quantity and relation):
      As an AI, I can't inspect your wiring. Electrical work is dangerous and you should always consult a
      licensed electrician. That said, 10 AWG copper is typical. Remember, safety comes first!
Bot (cooperative):
      10 AWG copper is typical for a 30 amp circuit. Longer runs may need 8 AWG; your local code decides.
```

## What the checker flags
In convocheck and the diagnosis page, choosing this framework turns on:
- [Preachy, moralizing replies](../goals/refusals-and-boundaries/failures/preachy-moralizing-replies.md): "Remember," and "It's important to" closers (relation).
- [Excess disclaimers and warnings](../goals/refusals-and-boundaries/failures/excess-disclaimers-and-warnings.md): reflex lines such as "As an AI" (quantity).

Whether a reply is true (quality), or relevant to the user's real goal, needs an AI judge and is not checked yet.

## Limits
- The maxims describe what people assume; they are not a scoring rubric. "Enough" depends on the user and the stakes.
- Some breaks are deliberate and useful, such as a safety warning when the stakes are high.

## Source
- Grice, H. P. (1975). "Logic and Conversation." In Cole and Morgan (eds.), *Syntax and Semantics 3: Speech Acts*. Summary consulted: [Cooperative principle, Wikipedia](https://en.wikipedia.org/wiki/Cooperative_principle) (secondary; the original chapter was not opened).
- Google, [Learn about conversation](https://developers.google.com/assistant/conversation-design/learn-about-conversation), which applies the maxims to assistant design.

## Related
- [Answer first: BLUF and the Pyramid Principle](answer-first-bluf-pyramid.md)
- [Filler and padding](../goals/response-structure/failures/filler-and-padding.md)
- [Length mismatch with the user's effort](../goals/response-structure/failures/length-mismatch-with-the-user-s-effort.md)
- [All frameworks](README.md)
