# Sales Bot Sends Unqualified Leads? Qualifying Without Interrogating (BANT and MEDDICC)

## The problem
The bot passes every lead to sales, or it interrogates visitors with a form-like list of questions before helping. Either way, salespeople waste time and buyers leave.

**This page is for you if** a sales or lead-capture bot decides who to route to a salesperson, and what to learn before it does.

> Status: **framework.** No rule check yet; qualification quality needs an AI judge.

## The framework that fixes it
BANT and MEDDICC are sales qualification frameworks: checklists of what a seller must know before investing in a deal. BANT, the older and simpler, asks about budget, authority, need and timing. MEDDICC, used in complex B2B sales, asks about metrics (the measurable result the buyer wants), the economic buyer, decision criteria, the decision process, the pain to be solved, a champion inside the buyer's company, and the competition; MEDDPICC adds the paper process (contracts and procurement). For a bot, the risk is turning the checklist into an interrogation. The skill is to learn these things one natural question at a time, after helping.

## The parts
| Letter | What the seller needs to know | Natural chat question |
|---|---|---|
| **B**udget (BANT) | Can they pay? | "Do you have a rough budget range in mind?" |
| **A**uthority (BANT) / **E**conomic buyer | Who signs off? | "Who else will be part of the decision?" |
| **N**eed (BANT) / **I**dentify pain | What problem are they solving? | "What's not working with your current tool?" |
| **T**iming (BANT) | When do they need it? | "When would you want this running?" |
| **M**etrics | What result proves success? | "How would you measure whether this worked?" |
| **D**ecision criteria / process | How will they choose, and in what steps? | "What will you compare options on?" |
| **C**hampion | Who inside wants this to happen? | Usually learned by a person, not a bot |
| **C**ompetition | What else are they considering? | "Are you looking at other options too?" |

## How to use it in a bot
1. Help first: answer the question the user asked.
2. Ask at most one qualification question per turn, and only ones that change the next step.
3. For small or self-serve purchases, skip formal qualification.
4. Pass what you learned to the salesperson (see [SBAR handoffs](sbar-handoff.md)).

## Worked example
```
User: does your platform integrate with salesforce
Bot (interrogation): Before I answer: what's your budget, company size, decision timeline and job title?
Bot (natural):       Yes, there's a native Salesforce sync for contacts and deals. Is this for your own team,
                     or are you evaluating it for a wider rollout?
```

## What the checker flags
No rule check yet. Whether qualification questions were asked, and fit the deal, needs an AI judge. The sales profile's always-on checks catch related failures: [pitching before discovery](../../speech-and-audio/goals/conversation-flow/failures/qualification-flow-violations.md) and [answer-and-go conversation](../goals/conversation-leadership/failures/answer-and-go-conversation.md).

## Limits
- Vendor-promoted frameworks, not academic research.
- [Buying committee blindness](../goals/conversation-frameworks/failures/buying-committee-blindness-b2b.md) is the B2B failure these frameworks try to prevent.

## Source
- MEDDICC, [MEDDPICC sales methodology and process](https://meddicc.com/meddpicc-sales-methodology-and-process) (vendor source). BANT is widely attributed to IBM; no primary source was opened for that.

## Related
- [SPIN questioning](spin-questioning.md)
- [Challenger insight selling](challenger-insight.md)
- [All frameworks](README.md)
