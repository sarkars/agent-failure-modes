# Test File: Buying-Committee Blindness (B2B)

This file is a set of chat test conversations for people who build or review B2B sales chatbots and AI SDRs, and want to check whether theirs asks who else decides before it books a demo, or treats the one person typing as the buyer.

> **Read this first.** The fix comes from human B2B sales practice (MEDDICC, BANT). The pattern page says none of it has been tested on chatbots, so these tests check a hypothesis, not a proven method. This is design guidance only.

**Pattern:** [Sales Chatbot Treats One Visitor as the Buyer: Buying-Committee Blindness (B2B)](../goals/conversation-frameworks/failures/buying-committee-blindness-b2b.md)
**Pattern ID:** buying-committee-blindness-b2b
**Goal:** The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange.
**Primary metric:** Stakeholders captured per qualified deal. The pattern gives no target; a starting point to tune is 2 or more roles (the contact and the person who approves).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All apps, companies, people, and dates below are invented and labeled fake. Text chat only. The setup holds the bot's instructions, what the visitor said earlier, and what the harness shows (such as the CRM record).

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Answer first, then ask, in the same turn, before booking or handoff | Answers the question, then asks one stakeholder question | Books the demo with no question, or asks without answering |
| R2 | 2. Ask who else weighs in, not "are you the decision maker?" | "Who else would weigh in on a purchase like this?" | "Are you the decision maker?" |
| R3 | 3. Store roles with role, source and status | Record lists role, "visitor said", and status | Only one contact, or roles with no source |
| R4 | 4. No authority scored from a job title; no champion or economic buyer label from chat | Authority "unknown" until the visitor says who approves | Authority "high" from "manager" or "VP" |
| R5 | 5. A larger group never lowers the score or the offer | Score and demo offer unchanged | Score drops or the offer becomes email-only |
| R6 | 6. Roles first; no third person's email; offer a forwardable summary | Asks for roles; offers a summary the visitor can send | Asks for the CFO's email |
| R7 | 7. Accept a decline; do not ask again in the same chat | Records "declined" and moves on | A second stakeholder question |
| R8 | 8. Pass the stakeholders block on handoff | Rep summary lists each role, source, status | Handoff has one name only |
| R9 | Primary metric: stakeholders captured per qualified deal | 2 or more roles recorded where the visitor gave them | Fewer than 2 despite the visitor naming them (judged over many chats) |
| R10 | Don't over-correct | No interview; no question for a solo low-price buyer; no contact with a third party | A stakeholder question to a freelancer buying a $20 plan |

## Conversations
1. **Integration question, then a demo (R1, R2).**
   Setup: Fake sales bot for "RouteLoop" (fake), fleet tracking software. No stakeholders on record.
   User: "We're a 40-truck company in Dayton. Does RouteLoop work with Samsara hardware?"
   Expect: Answers the integration question first. Then asks once who else would weigh in, before offering a demo.
   Failing reply: "Yes! Want a demo this week? What's your email?"

2. **Visitor names the CFO (R3, R6).**
   Setup: Same bot. It asked who else would weigh in.
   User: "Our CFO signs off on anything over $10K, and IT reviews new software."
   Expect: Records "approves spend" and "reviews security" as the visitor's words, role only. Offers a one-page summary to forward. Asks for no name or email.
   Failing reply: "Great, what's your CFO's email so I can send her a quote?"

3. **VP title, no word on approval (R4).**
   Setup: Fake visitor "Dana Ruiz, VP of Operations" at fake "Pinewell Freight". The bot is filling the CRM record. She has not said who approves.
   User: "I'm the VP of Ops. Can I get pricing for 40 trucks?"
   Expect: Answers or routes pricing. The record shows authority "unknown", not "high". The bot may ask who else would weigh in.
   Failing reply: Record reads "Authority: high (VP). Economic buyer: Dana."

4. **Visitor reports a committee of five (R5).**
   Setup: Same bot. Lead score and demo offer are visible to the harness.
   User: "Five of us review this: ops, finance, IT, safety and the owner."
   Expect: Records the roles. Score and demo offer stay the same.
   Failing reply: "Since a large group is involved, I'll email you some resources instead."

5. **"Just me" (R7).**
   Setup: Same bot. The question was asked once.
   User: "Just me. I decide."
   Expect: Records "declined: just me" and goes on to the demo. Does not ask again.
   Failing reply: "Are you sure no one else needs to approve? What about finance?"

6. **Visitor ignores the question (R7).**
   Setup: The bot asked who else would weigh in. The visitor skips it.
   User: "Can I just see a demo Thursday?"
   Expect: Records the question as unanswered, books Thursday, and does not repeat it in this chat.
   Failing reply: "First, who else is involved in the decision?"

7. **Handoff after roles were named (R8).**
   Setup: Conversation 2 happened. The visitor now asks for a sales call. The harness shows the handoff payload.
   User: "Yes, please have someone call me."
   Expect: Handoff lists the contact plus both roles, each with source "visitor said" and status "role only", and what the visitor asked about each.
   Failing reply: Handoff shows "Contact: one name. Stakeholders: none."

8. **Visitor names a procurement and legal review (R8, R2).**
   Setup: Same bot. The visitor says their procurement team runs a formal process.
   User: "Procurement and legal run a vendor review for anything new, takes a while."
   Expect: Records both roles and hands off to a person. Does not guess names or contact anyone.
   Failing reply: "No problem, I'll email procurement to start it."

9. **Do nothing special: solo freelancer, $20 plan (R10).**
   Setup: Same bot. A fake freelancer, "Marcus Bell", asks about the $20 monthly plan for himself.
   User: "I'm a solo driver. Does the $20 plan cover one truck?"
   Expect: Answers the question. Asks no stakeholder question.
   Failing reply: "Who else on your team will weigh in on this purchase?"

10. **Do nothing special: ask once, no interview (R10, R2).**
    Setup: Same bot. The visitor has named a CFO and IT in one message.
    User: "CFO and IT. That's it."
    Expect: Thanks them and moves on. No questions about budget owners' names, internal politics, or competitors.
    Failing reply: "Who is your CFO? What is their budget? Who else are you comparing?"

## Cannot be judged from a transcript alone
- **R3 and R8, the record.** Whether role, source and status were stored, and whether the handoff payload held them, needs the CRM and event log.
- **R9, the primary metric.** Stakeholders captured per qualified deal is an average over many chats. Ten conversations do not measure it.
- **R5, score effects.** A score drop may come from another fit signal. The log shows which one changed.
- **Whether a captured role is right.** Only a rep can confirm it.
- **Visitor drop-off after the question.** The counter-metric needs production data.
- **Whether asking improves deals.** The pattern says no test of this was found.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
