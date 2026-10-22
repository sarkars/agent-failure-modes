---
title: "CFPB Documents Bank Chatbot 'Doom Loops' With No Route to a Person"
date: 2023-06-06
source: "https://files.consumerfinance.gov/f/documents/cfpb_chatbot-issue-spotlight_2023-06.pdf"
summary: "The CFPB's June 2023 chatbot report quotes complaints of bank bots looping customers with no route to a person and warns this can lead to law violations."
categories:
  - Customer Service
  - Governance
patterns:
  - talk-to-a-human-ignored-or-looped
  - chatbot-loop-without-human-escalation-path
---

**This page is a dated teardown of a US regulator's report on bank chatbots, for teams that run chatbots at banks, lenders or other regulated customer-service desks.** It is a report built from consumer complaints and market review, not a ruling against a named bank. Every fact below comes from a source we opened (listed at the end). Statements about law are the CFPB's own words. This is not legal advice, and the legal reading is Needs review.

## What happened (as reported)

- **June 6, 2023.** The Consumer Financial Protection Bureau (CFPB) published *Chatbots in consumer finance*, a 22-page issue spotlight, with a press release the same day titled "Poorly deployed chatbots can impede customers from resolving problems" ([press release](https://www.consumerfinance.gov/about-us/newsroom/cfpb-issue-spotlight-analyzes-artificial-intelligence-chatbots-in-banking), [report PDF](https://files.consumerfinance.gov/f/documents/cfpb_chatbot-issue-spotlight_2023-06.pdf)).
- **Adoption.** The report says each of the 10 largest US commercial banks had deployed a chatbot. It says over 98 million users, about 37% of the US population, engaged with a bank chatbot in 2022, with a projection of 110.9 million by 2026. It cites a 2017 industry projection of $8 billion a year in savings, about $0.70 per interaction, as one possible driver. It names Capital One's Eno and Bank of America's Erica as examples.
- **What the CFPB drew on.** It says it reviewed consumer complaints and the market. It does not say how many complaints it reviewed or how it picked them.
- **Doom loops.** The report uses the term "doom loops" for chatbot answers that lead customers around repetitive, unhelpful text with no way out to a human representative. It says these loops often happen when the issue falls outside the bot's narrow abilities, and that several customers had filed complaints about them.
- **Complaints it quotes (company names are redacted in the report).**
  - A credit card holder, in a complaint dated July 2, 2022, said a payment was due that day, the virtual assistant kept sending them in circles, and they expected a late fee and a late mark on their credit report.
  - A person with a debt collection notice (complaint dated June 24, 2020) said the phone line and chat both sent them in loops to log in, though they had no account.
  - A person (complaint dated January 26, 2023) said chat agents promised a dispute and a conditional credit, but no dispute was opened, and they found no way to reach a person who could fix it.
  - Other complaints describe a chatbot that froze on the typing screen, one that asked the same account question forever, and a two-week failure to reach anyone about a credit report freeze that blocked a mortgage refinance.
- **Disputes.** The report says a bot may only recognize a dispute when specific words are used, and that repeating back the data the customer is disputing does not resolve it.
- **Human access.** It cites a survey (the source is not clear in the text we read) saying 80% of consumers who used a chatbot left more frustrated and 78% then needed a human. It also says long waits to reach a person can block the way out.
- **Stated risks.** The report lists three: breaking federal consumer financial law, losing customer trust when human support shrinks, and harming people through wrong information or unresolved disputes.
- **The CFPB's position.** The conclusion says the CFPB is monitoring the market, expects chatbot use to fit customer and legal obligations, and says deficient chatbots that block live human support can lead to law violations, lower service quality and other harms. It invites people who cannot get answers for lack of human contact to file a complaint. A footnote says the spotlight does not impose obligations or define rights and is not an interpretation of any regulation or statute. The press release adds that institutions should not make a chatbot the primary channel when it clearly cannot meet customer needs.

## What the sources do not say

- No named bank, no penalty and no enforcement action. The report redacts company names in the quoted complaints.
- How common doom loops are. No count of complaints, no rate, no share of chats.
- Whether any quoted complaint was checked or found true. They are customer accounts.
- Which technology (rule-based or large language model) caused each quoted loop.
- Whether the cost-savings figure, the 98 million figure or the survey figures hold up. They are cited from other sources the CFPB lists.
- Which specific law each example would break. The report speaks of obligations in general terms.
- Any later outcome at the banks named in the adoption section.

## Pattern match

- **[Talk to a human ignored or looped](/talk-to-a-human-ignored-or-looped/)** fits the complaints where the customer needs a person and the bot offers none: the late-fee complaint and the dispute complaint.
- **[Chatbot Loop Without Human Escalation Path](/chatbot-loop-without-human-escalation-path/)** fits the design fault the CFPB describes: a bot with no off-ramp when the issue is outside its scope, or when the bot itself is broken.
- **Where it does not fit.** Some complaints show a customer who never asked for a person and was only stuck (the frozen screen and the repeated account question). Those are loops, not ignored requests. The report's points on wrong answers, phishing and data security are other failure types and are not covered here.

## What a team could do

Tied to the fix: treat a request for a person, or a stuck conversation, as a routing event with a defined answer. Proposed checks, each pass/fail on logs or test scripts. Status: Not yet run; none comes from the CFPB.

1. **Always have an exit.** Test that a request for a person gets a transfer, a callback, or a stated route with a stated time, within a turn limit you set from your own baseline.
2. **Detect loops.** Flag a chat where the bot gives the same answer or asks the same question twice, and offer a person at that point.
3. **Disputes and deadlines.** Test that dispute wording, payment due dates and fee worries move to a person or a case record, and that the customer gets a case ID.
4. **No login wall for non-customers.** Test that someone with no account can still reach a person.
5. **Broken bot fallback.** If chat fails to load or freezes, show a phone number or another channel.
6. **Measure it.** Track the share of "talk to a human" asks that reach one, repeat contacts on the same issue, and chats that end with no confirmed resolution.
7. **Ask counsel.** Have your compliance team review which rules apply to your products. Needs review.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://files.consumerfinance.gov/f/documents/cfpb_chatbot-issue-spotlight_2023-06.pdf | CFPB (report) | 2023-06 | Yes, 2026-10-22 (full text, downloaded and extracted) |
| https://www.consumerfinance.gov/about-us/newsroom/cfpb-issue-spotlight-analyzes-artificial-intelligence-chatbots-in-banking | CFPB (press release, archived page) | 2023-06-06 | Yes, 2026-10-22 |
| CNN, Banking Dive, PYMNTS, Fox Business, Compliance Week and law-firm client alerts on the report | Various | June 2023 | No. Seen only in search summaries; no claim above relies on them |

## What we could not verify

- Whether the CFPB's text or the cited survey and cost figures are current or correct; we only report what the report says.
- Any outcome after June 2023, such as changes at banks or later CFPB action.
- The legal reading of any of this. This is not legal advice. Needs review.
- Industry reaction to the report. Search summaries mention pushback, but we did not open those articles.
