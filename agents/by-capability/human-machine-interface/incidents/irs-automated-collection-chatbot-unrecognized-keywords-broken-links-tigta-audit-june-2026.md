# IRS Automated Collection chatbot missed 44 of 53 test keywords and sent taxpayers to broken links, TIGTA audit, June 2026

<!-- SEO
title: IRS Chatbot Audit: Missed Keywords and Broken Links (TIGTA)
description: A June 2026 TIGTA audit found the IRS collection chatbot missed 44 of 53 test keywords, sent some users to broken links, and dropped its survey answers.
search phrases:
- irs chatbot tigta audit 2026
- irs chatbot not recognizing questions
- government chatbot broken links audit
- chatbot feedback survey not collected
- irs automated collection chatbot spanish version
-->

**This page is a dated teardown of one public audit of a government text chatbot, for teams that run a menu-and-keyword chatbot on a public website, especially one that handles bills, balances or payment plans.** The product was the IRS Automated Collection System (ACS) automated chatbot, which TIGTA says began in December 2021 and runs on four IRS web pages, such as the payments page. The users were taxpayers with balances due or late returns. The moment: TIGTA auditors typed 53 keyword terms into the chatbot's search box in March 2025, and 44 "were not recognized or had an insufficient response" by the bot. The date in the title is the month TIGTA issued the report.

**Status: Needs review.** Built from three sources. (1) The Treasury Inspector General for Tax Administration (TIGTA) final audit report, "Opportunities Exist to Improve the Quality of Chat Applications" (Report Number 2026-308-029), dated June 15, 2026, signed by Diana M. Tengesdal, Deputy Inspector General for Audit. We downloaded the PDF from oversight.gov on 2026-10-29 and read it as extracted text. This is the original source. (2) FedScoop, by Matt Bracken (June 18, 2026), downloaded on 2026-10-29 and read as text. (3) Accounting Today, by Michael Cohn (June 22, 2026), read on 2026-10-29 only through a fetch tool's summary, so we quote nothing from it. Every quote below was checked word for word against the saved text with a script.

> **Read this first.** This page is design guidance, not legal or tax advice. It summarizes a federal audit report and makes no legal finding about the IRS, its vendor, or any taxpayer. TIGTA's report names laws and an OMB rule; we repeat what TIGTA wrote and do not judge compliance ourselves. We did not use the IRS chatbot. If you owe the IRS money, use official IRS channels.

**Channel note.** This is a text incident: a web chatbot with preset options and a typed search box, which can end in a live chat with an IRS employee. TIGTA says the same function also runs voice bots on the phone, but "we limited our testing to the ACS function's chat applications and did not include testing of the voice bots." This phase of the knowledge base is chat-first, and the signals and checks below are written for text chat logs. Voice and web signals are PLANNED only: never detected or measured here.

## What happened (as reported)

- **What the bot is.** TIGTA: the chatbot "provides preprogrammed responses to questions, automated self-help options for taxpayers to make one-time payments, clarification on notices, etc." Per IRS officials, "This technology does not include the use of Generative Artificial Intelligence (AI)." So this is not an LLM failure. It is a scripted bot failure.
- **Why it matters.** TIGTA: "if chat applications do not provide accurate and sufficient information, it could lead taxpayers to file an inaccurate tax return or require them to contact the IRS again."
- **Weak responses.** In March 2025, TIGTA found "29 (14 percent) responses within the 206 process flows we tested could be improved." Its examples: "some of the responses directed taxpayers to a broken hyperlink." In another, "the response provided a link to download an IRS form but lacked instructions for completing the form."
- **Missed words.** TIGTA: "44 (83 percent) of the 53 keyword terms we tested were not recognized or had an insufficient response by the ACS automated chatbot when typed into the search box." Examples it gives: "Terms, such as Debit Card and Tax Pro Account, were not recognized and restated the initial prepopulated options." Some "Terms were not recognized by the chatbot and instead provided computer programming code." Others got "Responses that redirected the taxpayer to another web page that required further research."
- **Spanish gap.** TIGTA: "the Spanish version of the automated chatbot does not offer the taxpayer the option to search for information by typing keywords and questions into a search box." Spanish users are limited to the preset options.
- **Feedback that went nowhere.** At the end of a bot-only session, the bot asks a two-question survey with no written comment box. Its last line is "Thank you for your feedback. We are collecting the information to help improve our service." But when TIGTA asked for the results, "IRS officials stated that they do not collect or review these responses."
- **No measures.** TIGTA: "the IRS has not analyzed its chat applications and does not have any performance measures."
- **The IRS response.** TIGTA told the IRS about the chatbot in June 2025 (Recommendation 9). Per the report, "The IRS stated it corrected the broken links and the insufficient responses in the word bank." It also said it asked its vendor to add typed search to the Spanish version. The IRS agreed with all nine recommendations.

## Timeline

| Date | Event | Source |
|---|---|---|
| December 2021 | IRS launches the ACS automated chatbot, in English and Spanish | TIGTA |
| August 2024 to September 2025 | TIGTA audit period | TIGTA |
| March 2025 | TIGTA tests 206 process flows and 53 keyword terms | TIGTA |
| June 2025 | TIGTA notifies IRS of its chatbot concerns | TIGTA |
| November 2025 | IRS adds a chatbot notice that taxpayers need an active online account before a live assistor gives account information | TIGTA |
| June 15, 2026 | TIGTA issues the final report | TIGTA |
| June 18 and June 22, 2026 | FedScoop and Accounting Today report on it | FedScoop; Accounting Today (summary only) |

## Where the sources disagree or leave gaps

| Topic | What the sources say |
|---|---|
| Did TIGTA call the service effective? | FedScoop says the watchdog "noted" the live chat functions provide an "effective and efficient service to help taxpayers meet their tax obligations." In the report, that wording comes from the audit's objective ("We determined if the IRS’s chatbot and live chat applications provided effective and efficient service"), and the findings say the IRS has not evaluated effectiveness. We follow the report. |
| Name of the function | The report says "Automated Collection System" in its body and "Automated Collection Service" on the highlights page. We use "System." |
| Were the fixes checked? | The report gives the IRS's statement that it fixed the links and responses. No opened source says TIGTA retested the bot. |

## Where in the flow it broke

1. **Typed words the bot did not know.** A taxpayer typed a plain term such as "Debit Card." The bot did not recognize it and showed the opening menu again. That is a dead end dressed as a restart.
2. **Odd output instead of an answer.** For some unrecognized terms, the bot "instead provided computer programming code." The user saw system text, not help.
3. **An answer that pointed away.** Some replies sent the user to a broken link, a form with no instructions, or another page "that required further research."
4. **One language got less.** Spanish users could not type a question at all. They had only the preset options.
5. **The feedback loop was cut.** The bot thanked users and said it was collecting their answers. Per IRS officials, no one collected or reviewed them, so the team had no user signal about steps 1 to 4.
6. **The next step was often a person, then the phone.** Live chat comes at the end of a bot session. TIGTA counted 345,503 unresolved live chats in 2023 and 2024 (abandoned, disconnected, or told to call). It says data weaknesses mean it "could not determine the precise number," and "The IRS cannot determine why chats are unresolved because the reasons are not documented."

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it. Each fit rests on TIGTA's written examples; we saw no transcripts.

- [Dead-end "I don't understand" replies](../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md) (`dead-end-i-don-t-understand-replies`). **Good fit.** Unknown terms "restated the initial prepopulated options" with no help rephrasing. TIGTA does not say whether a route to a person was shown at that step.
- [No way to report bad behaviour](../goals/measurement-and-feedback/failures/no-way-to-report-bad-behaviour.md) (`no-way-to-report-bad-behaviour`). **Good fit.** The taxonomy describes a feedback click that says thanks "and then goes to no one". Here the bot said "We are collecting the information", and officials said they do not collect or review it.
- [Plain-language and language access gaps](../goals/government-service-agents/failures/plain-language-and-language-access-gaps.md) (`plain-language-and-language-access-gaps`). **Partial fit.** The Spanish bot exists but lacks typed search, so Spanish users get less of the service. Also, a form link "lacked instructions for completing the form."
- [Link and resource dumps](../goals/response-structure/failures/link-and-resource-dumps.md) (`link-and-resource-dumps`). **Partial fit.** Replies sent users to "another web page that required further research", and some links were broken. TIGTA does not say the bot sent lists of links.
- [IVR-style menu maze](../goals/voice/failures/ivr-style-menu-maze.md) (`ivr-style-menu-maze`). **Partial fit.** English had a search box, but a miss sent users back to the menu. The Spanish bot had menus only.
- **Considered, not a fit.** [Mixed-language experience](../goals/language-and-locale/failures/mixed-language-experience.md) (`mixed-language-experience`): TIGTA reports a missing feature in Spanish, not replies that mix languages. ["Talk to a human" ignored or looped](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md) (`talk-to-a-human-ignored-or-looped`): a live chat is offered at the end of a bot session, and TIGTA does not report requests for a person being ignored.

## How it differs from close cases

- [Canada Revenue Agency Charlie chatbot, October 2025](canada-revenue-agency-charlie-chatbot-wrong-tax-answers-october-2025.md): also a national auditor testing a tax agency's bot. Charlie gave wrong answers; the IRS bot mostly failed to recognize the question at all.
- [TurboTax and H&R Block AI tax assistants, March 2024](turbotax-and-hr-block-ai-tax-assistants-wrong-or-irrelevant-answers-march-2024.md): generative tax bots giving wrong answers. The IRS bot uses no generative AI, so its failures were misses and dead links, not invented facts.
- [CFPB report on bank chatbot doom loops](cfpb-bank-chatbot-doom-loops.md): a regulator describing bots that send people in circles on money problems; here the money problem is a tax balance.

## What to measure

Proposed signals, not results. Status: Not yet run. Each can be computed from text chat logs.

| Signal | How to compute from logs | Counter-signal |
|---|---|---|
| No-match rate on typed text | Share of typed search entries that get no matched topic and return the opening menu | Entries that match a topic and the user moves on |
| Menu-repeat after a miss | Count of sessions where the opening menu is shown again right after a typed entry | Users who chose to restart from a menu button |
| Dead links served | Share of bot replies whose links return an error when checked | Links that work but go to the wrong page |
| Raw system text in replies | Share of replies containing markup or code instead of prose | Replies that show a code the user needs, such as a notice number |
| Feature parity by language | For each language, which entry paths (typed search, menus) exist | Paths the team has chosen to drop in every language |
| Survey answers stored and read | Share of survey answers written to storage, and whether anyone reviewed them in a set period | Sessions where the user skipped the survey |

## What a team can change

Our proposals, not the IRS's. Each is a pass/fail check on a text log or a config. Status: Not yet run.

1. **A miss gets help, not the menu.** Pass: when typed text is not recognized, the bot says so, suggests close topics or asks one question, and names the way to a person. Fail: it shows the opening menu again with no comment.
2. **Never show code.** Pass: no reply contains markup or program text. Fail: any reply does.
3. **Check every link on a schedule.** Pass: an automated check opens every link the bot can send and flags any error. Fail: a broken link reaches a user.
4. **Same paths in every language.** Pass: each supported language offers the same entry paths. Fail: one language lacks typed search.
5. **Do not say "we are collecting" unless you are.** Pass: survey answers are stored and a named team reviews them on a set schedule. Fail: the bot says it is collecting feedback and the answers are not kept.
6. **Retest after a fix.** Pass: the keywords that failed are rerun after each fix, and the results are saved. Fail: a fix is reported with no rerun.

## A cheap test

Status: Not yet run. List 50 plain words your users type, such as "debit card" or "payment plan". Type each into your bot, in each language you offer. Record whether the bot matched a topic, repeated the menu, or showed system text, and open every link it returns.

## What we could not verify

- The list of 53 keyword terms and 206 process flows TIGTA tested, beyond the examples in the report.
- Which terms produced "computer programming code", and what that code looked like.
- Whether the IRS fixes have been retested; the report gives only the IRS statement.
- Whether the Spanish typed search has been added.
- The IRS management response in Appendix II: those pages extracted as blank text, so we used only the responses quoted in the report body.
- The oversight.gov report landing page returned error 406; we used the PDF directly.
- Accounting Today's article, read only as a tool summary; we use none of its wording.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://www.oversight.gov/sites/default/files/documents/reports/2026-06/2026308029fr.pdf | TIGTA, memo from Diana M. Tengesdal | 2026-06-15 | Yes, PDF downloaded 2026-10-29, read as extracted text |
| https://fedscoop.com/irs-live-chat-apps-chatbots-report/ | Matt Bracken, FedScoop | 2026-06-18 | Yes, HTML downloaded 2026-10-29, read as text |
| https://www.accountingtoday.com/news/irs-chatbot-results-may-be-wrong | Michael Cohn, Accounting Today | 2026-06-22 | Read 2026-10-29 through a fetch tool's summary only; no quotes used |
| https://www.oversight.gov/reports/audit/opportunities-exist-improve-quality-chat-applications | Oversight.gov | Not checked | Tried 2026-10-29; error 406. Not used. |

## Corrections

If you have the IRS's retest results, the keyword list, or a later TIGTA follow-up, tell us and we will fix this page.
