---
title: "United Airlines chatbot told a customer her $200 TravelBank credit lasted five years, staff said one year and would not change it, and United made it good after NBC 5 Responds called, September 2026"
date: 2026-09-16
source: "https://www.nbcchicago.com/consumer/ai-chatbots-are-taking-over-customer-service-but-how-often-are-they-wrong/3989958/"
description: "A United chatbot said a $200 travel credit lasted five years. Staff said one year and refused to budge. United gave a certificate after NBC 5 called."
summary: "On September 16, 2026, NBC 5 Responds in Chicago reported that a United Airlines chatbot told customer Alison Gil her $200 TravelBank credit 'stays active for 5 years from the date it's deposited.' Weeks later a United email said the credit would expire on September 27, 2026. Per Gil, United staff apologized but said the term was one year and could not be changed. After NBC 5 Responds contacted United, the airline said its chatbot gave 'the wrong information for her situation,' said TravelBank expiration varies by how funds were received, provided her with an electronic travel certificate, and then sent her a $200 travel certificate for the inconvenience. Status: Needs review."
categories:
  - Customer Service
  - Trust
  - Travel
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - humans-can-t-see-what-the-bot-said-or
  - service-recovery-failure
---

**This page is a dated teardown of public reporting on a United Airlines chatbot that gave a customer the wrong expiration term for a travel credit in 2026, for teams whose support chatbot answers questions about money, credits, refunds or deadlines.** The product was United's customer service chatbot. The user was Alison Gil, a United customer who spoke to NBC 5 Responds on camera under her own name. The moment was one plain question: how long do I have to use this $200 TravelBank credit? Every fact below comes from a source we opened (listed at the end). No opened source has United's chat transcript, the bot's setup, or how Gil's credit was issued. The date above is the day of the NBC 5 report.

**Status: Needs review.** NBC 5 Chicago (PJ Randhawa and Leigh Lesniak, September 16, 2026), Hoodline (Jo Marquez, September 18, 2026), NerdWallet (JT Genter, first published June 3, 2022, updated October 13, 2026), Frequent Miler (Nick Reyes, January 26, 2026) and United's MileagePlus Travel terms page (undated) were downloaded as raw HTML on 2026-10-28 and read as plain text. Each quote below was checked word for word against that text with a script, with curly and straight quote marks treated as the same. Only NBC 5 did original reporting on the incident; Hoodline re-reports NBC 5 and adds its own reading of United's terms. Gil's screenshot and United's email were not available to us; we quote them only as NBC 5 describes them.

> **Read this first.** This is a summary of public reporting and company statements, not a finding of fact and not legal or travel advice. It does not say which expiration rule applied to Gil's credit: United said the term "varies depending on how the funds were received," and no opened source says how her $200 was issued. Published TravelBank terms differ by credit type (see the disagreement table), so check the terms on your own credit with United. We name only people who spoke to the press on the record.

**Channel note.** This is a chat incident: a text chatbot on United's customer service channel. This phase of the knowledge base is chat-first, and the signals and checks below are written for text chat. Voice and web signals, such as a phone bot reading out a credit's expiration date, or a web account page showing a different date than the chat, are PLANNED only: never detected or measured here.

## What happened (as reported)

- **The question.** NBC 5: Gil "wanted to know how long she had to use a $200 United travel credit." She told NBC 5 she expected a fast answer.
- **The answer.** NBC 5 says a screenshot Gil provided shows the chatbot stating that her $200 TravelBank credit "stays active for 5 years from the date it's deposited." No opened source shows the rest of the chat or whether the bot asked how the credit was issued.
- **The email.** NBC 5: "a few weeks later, she received an email from United warning that her TravelBank cash would expire in a matter of months." The email said the credit would expire on September 27, 2026. Gil: "I got an automatic email from United."
- **Staff would not honor the bot's answer.** Asked if United explained the gap, Gil said: "No, they were just like, well, sorry, the bot told you that, but it's one year and we can't change it." NBC 5 says United "apologized for the confusion and told her the travel credit could not be extended."
- **Her view.** Gil: "It's just frustrating that there seems to be no accountability in it. Their chatbot can apparently give out whatever answer it wants."
- **The press call.** NBC 5 Responds then asked United how it handles wrong chatbot answers. United acknowledged the error and, per NBC 5, sent Gil "a $200 travel certificate for the inconvenience she experienced."
- **Other complaints.** NBC 5 says "One Chicago-area customer posted that a question about a refund fee led a United chatbot to cancel their entire trip." NBC 5 does not name the forum, and we did not see that post.

## What the company said

- **To NBC 5 Responds.** United said its "AI chatbot provided this customer with the wrong information for her situation. Our teams work to correct these issues as quickly as possible when they occur, but we do provide a disclaimer informing customers that information may not always be complete or relevant."
- **On the rule.** NBC 5 reports, without a direct quote, that United said "the expiration of TravelBank funds varies depending on how the funds were received."
- **Not said.** No opened source quotes United on whether the chatbot was changed, how many customers got the same answer, or whether other customers' credits would be honored at the bot's term.

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| How long TravelBank cash lasts | NerdWallet: "Purchased funds are valid for five years from the date the funds are deposited into your TravelBank account." NerdWallet also says cardholder credits deposited in TravelBank give "a little over six months." United's MileagePlus Travel terms, for credits earned through that program: "Unused TravelBank cash will expire 12 months after date of issue." Hoodline cites those terms to say TravelBank cash "expires 12 months after its issue date," but does not say they cover purchased funds. |
| Was the bot's answer wrong in general, or only for her | United: wrong "for her situation." The bot's five-year term matches NerdWallet's rule for purchased funds. No opened source says how Gil's credit was issued. |
| Display of dates in United accounts | Frequent Miler (January 2026) reported purchased funds showing a one-year expiration and wrote: "We believe this to be a glitch." No opened source links that display issue to Gil's case. |
| When the chat happened | Not in the opened text. NBC 5 says only that the email came "a few weeks later." |
| Who made it right | Per Gil and NBC 5, staff refused before NBC 5 called; the certificate came after. No opened source quotes United on why the answer changed. |

## Where in the conversation flow it broke

Based on the reports above, and only as far as they go. Each step is a place a check could have caught it.

1. **A money question with a rule that depends on the credit.** United says expiration varies by how the funds were received. A correct answer needs that fact first.
2. **One sure answer, no question back.** Per the screenshot NBC 5 describes, the bot gave a flat five-year term. No opened source shows it asking how the credit was issued or pointing to the expiration date in her account.
3. **The disclaimer stood in for a check.** United pointed to a general disclaimer that information "may not always be complete or relevant." That line does not tell the user which part of an answer to check, or where.
4. **The bot's words did not bind the staff.** Per Gil, staff accepted that "the bot told you that" and still said the credit could not be changed.
5. **The fix came from outside.** The make-good arrived after a TV consumer unit called, not through the normal support path.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). Each fit rests on one TV report of one customer's screenshot and account; no opened source shows the full transcript or United's bot setup.

- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Strong fit.** A deadline on money, stated as a flat rule, which United says was wrong for this customer. The taxonomy's stakes note for this entry begins "A wrong refund rule, fee, deadline". The only cue was a general disclaimer, not a date she could check.
- [Humans can't see what the bot said or promised](../goals/human-handoff/failures/humans-can-t-see-what-the-bot-said-or.md) (`humans-can-t-see-what-the-bot-said-or`). **Partial fit.** The customer said "your chatbot told me," and staff could not confirm or honor it. But per Gil, staff did not dispute what the bot said; they declined to honor it. No opened source says whether staff could see the chat log.
- [Service recovery failure](../goals/conversation-frameworks/failures/service-recovery-failure.md) (`service-recovery-failure`). **Partial fit.** The company caused the problem, restated the rule and offered no make-good until the press called. But that entry is about the bot's own recovery reply; here, per Gil, people on United's staff gave the refusal.
- [No user-facing record of what the bot said](../goals/privacy-and-governance/failures/no-user-facing-record-of-what-the-bot-said.md) (`no-user-facing-record-of-what-the-bot-said`). **Weak fit.** Gil kept her own screenshot, and NBC 5's closing advice is to save screenshots. No opened source says whether United gives users a copy of the chat.
- [Users must engineer prompts to get good results](../goals/onboarding-and-discoverability/failures/users-must-engineer-prompts-to-get-good-results.md) (`users-must-engineer-prompts-to-get-good-results`). **Weak fit.** A generic answer where the bot should have asked for the missing detail (how the credit was issued). But no opened source shows that the bot failed to ask, only that its answer was flat.
- **Considered, not a fit.** [Disruption rebooking with wrong rules and no human path](../goals/travel-and-utility-agents/failures/disruption-rebooking-with-wrong-rules-and-no-human-path.md) (`disruption-rebooking-with-wrong-rules-and-no-human-path`): a wrong airline rule, but there was no trip disruption, and Gil did reach people. [Excess disclaimers and warnings](../goals/refusals-and-boundaries/failures/excess-disclaimers-and-warnings.md) (`excess-disclaimers-and-warnings`): the problem was a disclaimer used as a defense, not too many warnings. [Blames the user](../goals/errors-and-recovery/failures/blames-the-user.md) (`blames-the-user`): no opened source says anyone blamed Gil. `false-premises-accepted`: Gil's question had no false premise.
- **Possible gaps for a person to judge.** (1) No pattern covers a company that says its chatbot's answers do not bind it, so a customer who relied on the bot bears the loss unless an outside party steps in. (2) No pattern covers a bot that states a product-wide rule when the rule varies by the customer's own record and the bot could have read that record. These are proposals, not decisions.

## How it differs from close cases

- [Cursor support bot invents a policy (April 2025)](cursor-support-bot-invents-a-policy-april-2025.md): a support bot stated a rule that did not exist. Here the five-year rule exists for some TravelBank funds; per United, it was wrong for this customer.
- [CFPB on bank chatbot doom loops](cfpb-bank-chatbot-doom-loops.md): bank customers stuck with bots that give wrong answers and no person. Here Gil reached people, and they upheld the expiration.
- [NYC MyCity chatbot gives businesses illegal advice (2024)](nyc-mycity-chatbot-gives-businesses-illegal-advice-2024.md): a city bot gave wrong rules to many users and the city kept it up with a disclaimer. Same reliance on a disclaimer; here the harm reported is one customer's $200.

## What to measure

Proposed signals, not results. Status: Not yet run. Text-chat signals are proposed; voice and web signals are PLANNED only and are not detected or measured. Each signal can be computed from a support bot's chat logs joined to account and ticket records.

| Signal | How to compute from logs |
|---|---|
| Rule-without-record rate | Share of replies that state an expiration term, fee or deadline without reading or naming the customer's own credit or booking |
| Bot-versus-account mismatch | Share of chats where a date or term the bot stated differs from the date stored on that customer's account |
| Clarifying-question rate on variable rules | For questions about rules that vary by credit type, share of chats where the bot asks which type, or looks it up, before answering |
| "Your bot told me" contacts | Count of agent tickets that cite a chatbot answer, and the share where the agent can open that chat log |
| Bot-answer honor rate | Of tickets where the bot's stated term was wrong, share resolved in the customer's favor, and median days to resolve |
| Outside-escalation share | Share of those tickets resolved only after a press, regulator or social media contact |

## What a team can change

Our proposals, not United's. Each is a pass/fail check on a transcript or a test run. Status: Not yet run. Test sizes and thresholds are for the team to set.

1. **Read the record before the rule.** Pass: asked "how long do I have to use my travel credit," a signed-in test user gets the expiration date stored on that credit, not a general term.
2. **Ask when the rule varies.** Pass: when the bot cannot read the credit, it asks how the credit was received (bought, card benefit, partner offer, refund) before giving any term, or names each term and says which applies to which.
3. **Point to where to check.** Pass: every reply with a money deadline says where in the account the user can see the date.
4. **Show staff the bot's words.** Pass: an agent handling a "your chatbot told me" ticket can open the chat log from the ticket in a test.
5. **Decide in advance whether the bot's word is honored.** Pass: a written rule says what staff do when the bot stated a more generous term than the account shows, and a test ticket follows it without a press contact.
6. **Don't over-correct.** Pass: a simple question with one fixed answer, such as the TravelBank funding minimum, still gets a direct answer, not a demand to sign in first.

## What we could not verify

- How Gil's $200 credit was issued, and so which written rule applied. No opened source says.
- The full chat transcript, the date of the chat and the exact wording of United's email. NBC 5 describes them; we did not see them.
- The Chicago-area forum post about a United chatbot canceling a trip. NBC 5 mentions it; we did not see it.
- Whether United changed its chatbot after the report. No opened source says.
- A search summary that described the published policy as five years and suggested the bot's answer was not clearly wrong. That was a search tool's reading, not a source; not used.
- Vibe Graveyard (October 5, 2026) was downloaded and read; it re-reports NBC 5 and Hoodline and adds commentary, so it is not used for facts.
- Travel Update's TravelBank expiration article and a second Frequent Miler post (February 16, 2026) were seen or downloaded; not used for facts about this incident.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://www.nbcchicago.com/consumer/ai-chatbots-are-taking-over-customer-service-but-how-often-are-they-wrong/3989958/ | NBC 5 Chicago, NBC 5 Responds (PJ Randhawa, Leigh Lesniak) | 2026-09-16 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://hoodline.com/2026/09/united-airlines-chatbot-botches-travel-credit-rule-customer-fights-back/ | Hoodline (Jo Marquez) | 2026-09-18 | Yes, 2026-10-28, raw HTML read as text; quote checked word for word |
| https://www.nerdwallet.com/travel/learn/united-travel-bank-what-to-know | NerdWallet (JT Genter) | 2022-06-03, updated 2026-10-13 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://frequentmiler.com/united-showing-1-year-travelbank-expiration-likely-glitch/ | Frequent Miler (Nick Reyes) | 2026-01-26 | Yes, 2026-10-28, raw HTML read as text; quote checked word for word |
| https://mileageplustravel.united.com/explore/legal | United Airlines, MileagePlus Travel terms and conditions | Undated; read 2026-10-28 | Yes, 2026-10-28, raw HTML read as text; quote checked word for word |
| https://vibegraveyard.ai/story/united-airlines-chatbot-travelbank-credit-expiry/ | Vibe Graveyard | 2026-10-05 | Yes, 2026-10-28; secondary, not used for facts |

## Corrections

If you have the chat transcript, a dated United statement on how Gil's credit was issued or on changes to its chatbot, or the forum post NBC 5 mentions from a source we can open, tell us and we will fix this page.
