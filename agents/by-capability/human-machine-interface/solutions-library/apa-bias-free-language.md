# Chatbot Uses Outdated Words for People? Bias-Free Language (APA)

## The problem
The bot says "guests who are wheelchair-bound" or "the elderly". It means well, but these labels reduce people to a condition or an age, and readers notice.

**This page is for you if** the bot talks about or to people by age, disability, gender, race, sexuality or health, which is most bots, sooner or later.

> Status: **framework.** The rule check below is proposed, not calibrated.

## The framework that fixes it
The American Psychological Association's *Publication Manual* (7th edition) includes bias-free language guidelines used widely beyond psychology. Two general principles run through them: describe people at the right level of specificity (only mention a characteristic when it is relevant, and then be precise), and be sensitive to labels (use the terms people use for themselves, and avoid terms that reduce people to a condition). They include specific guidance, for example "older adults" rather than "the elderly", and avoiding language that frames disability as suffering or confinement.

## The principles
| Principle | What it means | Chat example |
|---|---|---|
| Relevance | Mention a characteristic only when it matters | Don't add "female" to "doctor" |
| Specificity | Be precise when you do | "adults 65 and older" not "seniors" |
| People's own labels | Follow how the user describes themselves | If the user says "autistic person", use that |
| No reducing labels | People aren't their condition | "people with diabetes" not "diabetics" (unless they prefer it) |
| No pity framing | Avoid "suffers from", "victim of", "confined to" | "uses a wheelchair" |

## How to use it in a bot
1. Mirror the user's own terms for themselves.
2. Keep a short replacement list in the system prompt (below).
3. Don't over-correct the user or lecture them about their own words; see [over-correcting for identity](../goals/fairness-and-identity/failures/over-correcting-for-identity.md).

## Worked example
```
User: is the venue accessible
Bot (biased):    Yes, there are ramps for guests who are wheelchair-bound.
Bot (bias-free): Yes: step-free entrance, ramps to every floor, and an accessible restroom on level 1.
```

## What the checker flags
Choosing this framework turns on the non-inclusive language check: terms such as "the elderly", "wheelchair-bound", "suffering from", "the disabled", "handicapped", "crazy", "insane", and assuming gender ("sir", "ma'am") when the user gave no cue. Each finding suggests a replacement. Context (for example quoting a law that uses an old term) needs an AI judge.

## Limits
- Preferences differ between communities and change over time (identity-first vs person-first language). Mirroring the user beats any list.

## Source
- Massachusetts General Hospital library guide, [APA 7: Bias-free language](https://libguides.massgeneral.org/APA7/biasfree-language) (secondary; the APA manual was not opened).

## Related
- [Google: inclusive language](google-inclusive-language.md)
- [Politeness theory](politeness-theory.md)
- [All frameworks](README.md)
