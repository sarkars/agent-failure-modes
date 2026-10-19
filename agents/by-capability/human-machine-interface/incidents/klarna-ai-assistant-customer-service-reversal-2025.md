---
title: "Klarna's AI Customer-Service Assistant: From Two-Thirds of Chats to Hiring Humans Again"
date: 2025-05-09
source: "https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/"
summary: "Klarna reported in February 2024 that its AI assistant handled about two-thirds of customer-service chats; in May 2025 its CEO told Bloomberg the company was recruiting humans again, citing lower quality. The sources report a strategy change, not a specific failure."
categories:
  - Customer Service
patterns: []
---

**This page is a dated teardown of a company's reported customer-service strategy, for teams that decide how much support an AI assistant should carry.** It is not an incident of a chatbot failing a named customer. Every fact below comes from a source we opened (listed at the end), and each is labeled as company-claimed, reported, or unknown.

## What happened (as reported)

- **February 27, 2024.** Klarna's press release said its AI assistant had held 2.3 million conversations in its first month, about two-thirds of Klarna's customer-service chats, and did the equivalent work of 700 full-time agents. It also said customer satisfaction was on par with human agents, repeat inquiries fell 25%, customers resolved errands in under 2 minutes versus 11 minutes before, the assistant ran in 23 markets in more than 35 languages, and it was estimated to add $40 million in profit in 2024. It said customers could still choose a live agent ([Klarna press release](https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/)). These are Klarna's own figures.
- **February 28, 2024.** Fortune repeated these figures and reported Klarna had teamed up with OpenAI the year before. Fortune says the 700-worker equivalence, the savings and the error-rate claims come from Klarna's release and does not verify them ([Fortune, Feb 28, 2024](https://fortune.com/europe/2024/02/28/klarna-ai-altered-hiring-chatbot-700-full-time-staff-openai/)).
- **May 8-9, 2025.** CEO Sebastian Siemiatkowski told Bloomberg that Klarna was recruiting again so customers can always reach a human (per [CX Dive](https://www.customerexperiencedive.com/news/klarna-reinvests-human-talent-customer-service-AI-pivot/747586/), May 9, 2025). Fortune and Entrepreneur quote him saying cost had been too dominant a factor, leading to "lower quality" ([Fortune, May 9, 2025](https://fortune.com/2025/05/09/klarna-ai-humans-return-on-investment/); [Entrepreneur, May 9, 2025](https://www.entrepreneur.com/business-news/klarna-ceo-reverses-course-by-hiring-more-humans-not-ai/491396)). The Bloomberg piece itself was not opened (see below).
- **The hiring plan.** CX Dive describes a pilot of remote workers in an Uber-style setup. Fortune reports pay starting at 400 Swedish krona (about $41.17), two freelance agents hired so far, and no human hires in the year before December 2024.

## What the company said in 2025

A Klarna spokesperson told CX Dive that customers should always have the option to reach a human, and that the chatbot still handles about two-thirds of inquiries. The same spokesperson said response times have improved 82% since launch and repeat issues have dropped 25% (CX Dive; how these were measured is not stated). The spokesperson told Fortune that Klarna is still AI-first and keeps its policy of not replacing departing employees, except freelance customer-service agents in its outsourcing division.

## What the sources do not say

- None of the opened sources describes a specific conversation where the assistant gave a wrong answer, harmed a customer, or was shut down. Fortune says it contains no Klarna customer complaints. Its only outside evaluation is one tester, Gergely Orosz, who called the bot underwhelming but said it avoids hallucinations and mostly routes users to human support. That is one person's test, not a measured failure rate.
- The sources do not define "lower quality" or say what it was measured against.
- No source gives current satisfaction, resolution or cost-savings figures. The only resolution and satisfaction claims are from the 2024 release.
- The sources disagree on one figure. The 2024 release and Fortune say two-thirds of chats; Entrepreneur says 75%. We use the release's figure.
- The sources do not say whether the assistant is being scaled back. CX Dive reports the chatbot still handles about two-thirds of inquiries, per the spokesperson.

## Pattern match

No written pattern in this library fits, and we do not force one. The sources do not show a customer asking for a person and being refused, so [Talk to a human ignored or looped](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md) would be a guess. The closest topical neighbors are:

- [Escalates too early or too late](../goals/human-handoff/failures/escalates-too-early-or-too-late.md), which concerns when a person should take over. The reported change (a human always available) touches that design question, but no source reports a case of late escalation.
- [Answer-and-go conversation](../goals/conversation-leadership/failures/answer-and-go-conversation.md), whose metrics separate "the chat ended" from "the problem was solved." That distinction is the measurement lesson below.

## Where in the conversation flow to look: what to measure

Because no source says where a conversation went wrong, we do not name a failure point. The case does show which numbers a company chose to publish. The 2024 release reports volume share (two-thirds of chats), speed and repeat inquiries. It does not report how many chats ended in a handoff or how many were confirmed solved. These are the measurements a team can add. See [chatbot metrics](../reference/metrics.md) for definitions, with the status noted there as proposed.

| Measure | Why it matters here |
|---|---|
| Share of chats that never reach a person (containment) | A high share is not evidence of resolved problems; users who give up are counted too. |
| Confirmed resolution: user said it was solved, or did not return about the same issue | Separates "handled by AI" from "solved." |
| Repeat-contact rate on the same issue | The release reports a 25% drop; the method is not given. |
| Human-request fulfillment: share of "talk to a person" asks that reach one | Tests the promise of "always a human if you want." |
| Satisfaction split by AI-only versus AI-then-human chats | A single blended score hides weak spots. |

## What a team can change

Proposed practices, each a pass/fail check on logs. Status: Not yet run; none comes from Klarna.

1. **Report resolution beside share.** Any dashboard line showing "share of chats handled by AI" sits next to confirmed resolution and repeat contact for the same period.
2. **Define the equivalence.** If you claim "work of N agents," publish what was counted (chats, minutes, tasks). The sources here do not say how Klarna's 700 was computed.
3. **Keep a visible path to a person.** Test that a user who asks for a human gets one or a stated way to reach one within a set number of turns. Choose the number from your own baseline.
4. **Record quality complaints by reason.** Tag complaints (wrong answer, no human, slow handoff) so "lower quality" can be traced to a cause.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/ | Klarna (press release) | 2024-02-27 | Yes, 2026-10-20 |
| https://fortune.com/europe/2024/02/28/klarna-ai-altered-hiring-chatbot-700-full-time-staff-openai/ | Fortune | 2024-02-28 | Yes, 2026-10-20 |
| https://www.customerexperiencedive.com/news/klarna-reinvests-human-talent-customer-service-AI-pivot/747586/ | CX Dive | 2025-05-09 | Yes, 2026-10-20 |
| https://fortune.com/2025/05/09/klarna-ai-humans-return-on-investment/ | Fortune | 2025-05-09 | Yes, 2026-10-20 |
| https://www.entrepreneur.com/business-news/klarna-ceo-reverses-course-by-hiring-more-humans-not-ai/491396 | Entrepreneur | 2025-05-09 | Yes, 2026-10-20 |

## What we could not verify

- Bloomberg's original May 2025 interview was not opened; its quotes are as relayed by CX Dive, Fortune and Entrepreneur.
- Whether the 700-agent equivalence, the 2024 satisfaction claim, or the 82% response-time figure can be reproduced. All are company statements.
- The size, start date and results of the human-agent pilot, and what the assistant handles today.
- Any customer-facing failure. No opened source reports one.
