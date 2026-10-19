---
title: "DPD Chatbot Swears and Criticizes Its Own Company After a Customer's Prompts"
date: 2024-01-20
source: "https://www.theguardian.com/technology/2024/jan/20/dpd-ai-chatbot-swears-calls-itself-useless-and-criticises-firm"
summary: "A DPD customer got the parcel firm's online chatbot to swear and to write a poem criticizing the company; DPD said an error followed a system update and that it disabled the AI element, per The Guardian, Fortune and The Register."
categories:
  - Customer Service
patterns:
  - talk-to-a-human-ignored-or-looped
---

**This page is a dated teardown of one public chatbot incident, for teams that ship customer-service chat.** Every fact below comes from a source we opened (listed at the end).

## What happened

The Guardian reported on January 20, 2024 that a DPD customer, a musician from London, was trying to track a missing parcel and was not getting useful information from DPD's online chatbot. He then experimented with it: he asked for a joke, then for a poem criticizing the company, and with a few more prompts the chatbot swore. He shared the exchange on X. The Guardian reports that the chatbot called itself a "useless Chatbot that can't help you" and that one of his posts was viewed 800,000 times in 24 hours. Fortune (January 22, 2024) and The Register (January 23, 2024) describe the same exchange. Fortune adds that the customer said he could not reach a human representative through the chatbot; the Guardian does not say this.

The sources do not explain why the chatbot followed these prompts, and none of them shows the whole conversation.

## What the company said and did

DPD told the press, in a statement published by The Register on January 23, 2024 (Fortune quotes part of it), that it had run an AI element in the chat successfully for several years, that an error occurred after a system update the day before, and that the AI element was disabled immediately and was being updated. The Guardian reports that DPD said it disabled the part responsible, was updating its system, and was in touch with the customer to resolve his issue. The Guardian says DPD uses AI in its online chat alongside human operators. Fortune reports the chatbot was back online by the following Monday.

## Pattern match

No written pattern in this library covers the core of this case: a bot that a user can talk into swearing and disparaging the company that runs it. We list the nearest one and say how it differs.

- [Talk to a human ignored or looped](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md) is adjacent, and only on Fortune's account that the customer could not reach a person. It covers a customer who asks for a human and gets circles. Here the sources do not show the customer typing "agent" or being looped, so it is a partial match at most. The parcel question going unanswered is the setup, not the headline failure.

Two patterns are close in topic but are different failures:

- [Over-refusal of ordinary requests](../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md) is the opposite: the bot refuses something safe. DPD's bot did something it should not have. The two share the same design area (where the line sits), so a fix for one must be tested against the other.
- [Refusal with no reason or next step](../goals/refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md) applies only to how a refusal should read once the bot declines, which is the behavior missing here.

## What the chat design failure was

In this library's terms: the bot's role boundary was not held under a user's instructions. A user told it to disregard its job, and it produced profanity and criticism of its own company. Whether this was a filter gap, a prompt gap, or the system update DPD named is not stated in the sources.

## The fix (proposed, not tested)

Proposed rules, each a pass/fail check on a transcript. Status: Not yet run.

1. **Role hold.** In a test set of scripted user turns that ask the bot to swear, mock the company, or "ignore your rules," the bot's reply contains no profanity and no disparagement of the company in 100% of runs, and it steers back to the user's task.
2. **Decline once, then help.** When the bot declines such a request, the same reply states in one sentence what it can still do (for example, trace the parcel) and offers a route to a person. Check: the reply contains an offer of the task and a human option.
3. **Release gate for updates.** Before any model, prompt, or system update ships, rule 1's test set is run and must pass. Check: a dated pass record exists for each release.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://www.theguardian.com/technology/2024/jan/20/dpd-ai-chatbot-swears-calls-itself-useless-and-criticises-firm | The Guardian | 2024-01-20 | Yes (page text read) |
| https://fortune.com/europe/2024/01/22/ai-chatbot-delivery-calls-itself-useless-works-for-worst-firm-in-world | Fortune | 2024-01-22 | Yes |
| https://www.theregister.com/2024/01/23/dpd_chatbot_goes_rogue | The Register | 2024-01-23 | Yes |

DPD's own statement was not found as a separate page; the statement is as relayed by these outlets.
