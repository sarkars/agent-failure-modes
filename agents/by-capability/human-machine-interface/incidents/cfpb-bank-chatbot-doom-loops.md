---
title: "CFPB Documents Bank Chatbot 'Doom Loops' With No Route to a Person"
date: 2023-06-06
source: "https://files.consumerfinance.gov/f/documents/cfpb_chatbot-issue-spotlight_2023-06.pdf"
summary: "The CFPB's June 2023 report on chatbots in consumer finance quotes customer complaints about being sent around in circles by bank chatbots with no way to reach a person, and warns that chatbots that block access to live support can lead to law violations."
categories:
  - Customer Service
  - Governance
patterns:
  - talk-to-a-human-ignored-or-looped
  - chatbot-loop-without-human-escalation-path
---

On June 6, 2023, the US Consumer Financial Protection Bureau (CFPB) published *Chatbots in consumer finance*. It reports that each of the ten largest US commercial banks had deployed a chatbot, and quotes complaints from customers who said the chat feature sent them "in circles". One complaint, dated July 2, 2022, says a credit card payment was due that day and the virtual assistant gave "an endless loop with no way out". The report calls this pattern "doom loops": "continuous loops of repetitive, unhelpful jargon or legalese without an offramp to a human customer service representative".

The report also says deficient chatbots that prevent access to live, human support "can lead to law violations, diminished service, and other harms". It encourages people who cannot get answers because of a lack of human interaction to file a complaint with the CFPB. The source does not count how many complaints it reviewed, and it covers consumer finance only.

**Pattern match:** [Talk to a human ignored or looped](/talk-to-a-human-ignored-or-looped/) is the failure: customers ask for a person, or need one, and the bot offers no route. It is the same loop as [Chatbot Loop Without Human Escalation Path](/chatbot-loop-without-human-escalation-path/), seen from the customer's request.

**The fix:** treat a request for a person as a routing event, and answer it with a transfer, a callback, or a stated route and time.
