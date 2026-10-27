---
title: "Crisis Text Line shared data from crisis text conversations with its for-profit spin-off Loris.ai, which built customer service software, January 2022"
date: 2022-01-28
source: "https://www.politico.com/news/2022/01/28/suicide-hotline-silicon-valley-privacy-debates-00002617"
description: "How Crisis Text Line shared scrubbed data from crisis text chats with its spin-off Loris.ai, which built customer service software, until it ended the deal."
summary: "On January 28, 2022, Politico (Alexandra S. Levine) reported that Crisis Text Line, a nonprofit text-message crisis service staffed by volunteer counselors, shared anonymized data from its conversations with Loris.ai, a for-profit spin-off that made customer service software. Crisis Text Line held a stake in Loris. Texters agreed to terms through a link in the first automated message. On January 31, 2022, Crisis Text Line said it had ended the data sharing and asked Loris to delete the data; FCC Commissioner Brendan Carr wrote the same day asking both groups to stop. Board member danah boyd wrote that the board had been wrong to share the data. Former volunteer Tim Reierson, who had campaigned on the issue, wrote to the FTC on March 31, 2022."
categories:
  - Privacy
  - Vulnerable users
patterns:
  - sensitive-data-collected-in-chat
  - recording-consent-not-captured
  - manipulated-consent-ui
  - exploiting-vulnerable-circumstances
---

**This page is a dated teardown of public reporting on how Crisis Text Line reused data from crisis conversations, for teams that ship chat assistants or support chat and keep conversation logs.** Every fact below comes from a source we opened (listed at the end). The service itself was run by human volunteer counselors; the reuse was of the conversation data, to build software for a different market.

**Status: Needs review.** Politico's two January 2022 stories (read through Internet Archive copies), Crisis Text Line's blog post, Brendan Carr's letter (Internet Archive copy of the FCC PDF), danah boyd's essay, Popular Science, the Benton Institute summary, Tim Reierson's site and his letter to the FTC were downloaded on 2026-10-28 and read as plain text. Each quote below was checked word for word against that text.

> **Read this first.** This is a summary of public reporting, not a finding of fact, and not legal or medical advice. It touches suicide and self-harm. We do not repeat any texter's words, and no opened source quotes a real conversation. If you or someone you know is in crisis in the US, you can call or text 988. Have a privacy lawyer and a clinical expert review your own data practices.

**Channel note.** Text chat staffed by people. Per Politico, texters reached volunteer counselors over SMS, Facebook Messenger and WhatsApp. The conversation logs were then reused to build software for customer service chats. This phase of the knowledge base is chat-first: the text-chat signals and checks below are proposed; voice is planned and not covered here.

## What happened (as reported)

- **The report.** Politico's "Suicide hotline shares data with for-profit spinoff, raising ethical questions" by Alexandra S. Levine, is dated January 28, 2022 and was updated January 29. It says the spin-off "uses a sliced and repackaged version of that information to create and market customer service software."
- **The two groups.** Per Politico, Crisis Text Line holds an ownership stake in Loris, Loris pledged to share some revenue, and the two shared the same CEO for at least a year and a half. Politico says founder Nancy Lublin created Loris in 2018 to build AI software that helps guide customer service agents through live chats.
- **The data.** Politico quotes a Loris news release saying the "core" of its AI came from insights "drawn from analyzing nearly 200 million messages" at Crisis Text Line. Loris CEO Etie Hertz told Politico its AI now also uses data from e-commerce and other industries.
- **The size.** Crisis Text Line told Politico it had exchanged 219 million messages in more than 6.7 million conversations since 2013. Politico notes it has called its holdings "the largest mental health data set in the world".
- **How texters agreed.** Politico says people get a link to an approximately 50-paragraph disclosure when they first reach out. It quotes the automated first message: "By texting further with us, you agree to our Terms".
- **Crisis Text Line's defense, per Politico.** General counsel Shawn Rodriguez said the group gets informed consent from each texter, that "sensitive data from conversations is not commercialized, full stop", and that names, phone numbers and social media handles are removed "via an automated process". After Politico began asking questions, the site was changed to say "Loris does not have open-ended access to our data; it has limited contractual rights to periodically ask us for certain anonymized data."
- **Experts.** Stanford's Jennifer King asked whether the group has "actual meaningful, emotional, fully understood consent?" Politico says some experts cited studies showing anonymized records can sometimes be traced back to people. Former FTC consumer protection director Jessica Rich said "we don’t know whether that could be reverse-engineered".
- **Volunteers.** Former volunteer Tim Reierson told Politico texters "definitely have an expectation that the conversation is between just the two people that are talking." Current volunteer Beck Bamberger said she did not know about the customer service use until Politico reached out.
- **Other voices.** Per Politico's January 31 story by John Hendel, Sen. Kirsten Gillibrand and EPIC's Alan Butler criticized the deal.
- **Carr's first letter.** On January 31, 2022, FCC Commissioner Brendan Carr wrote to Crisis Text Line CEO Dena Trujillo and Hertz asking them to stop the practice "to preserve the integrity of mental health hotlines". Of the "why sell t-shirts" line on Crisis Text Line's site, he wrote: "This is disturbingly dystopian". He noted the FCC's role in the separate 988 Lifeline.
- **Carr and the FTC.** Per Benton, Carr later asked FTC Chair Lina Khan and Samuel Levine "to investigate CTL’s prior and current data practices". Reierson's letter dates Carr's FTC letter March 22, 2022. We did not open Carr's FTC letter.
- **Reierson's letter.** On March 31, 2022, Reierson wrote to the FTC: "I can confirm all of Commissioner Carr’s concerns." He added that "volunteers have not provided consent" and said nearly half of 2020 texters were 17 or younger, citing a Crisis Text Line post we did not open.

## What Crisis Text Line did

- **Ended the deal.** Its blog post dated January 31, 2022 says: "As a result, we have ended our data-sharing relationship with Loris." It says it asked Loris to delete the data and updated its Terms of Service and Privacy Policy.
- **Said sharing had stopped earlier.** The same post says "Loris has not accessed any data since the beginning of 2020."
- **Changed the consent text.** The post says: "We have added an easy to understand bulleted summary to the top of our terms of service." It also says it will test new ways for texters to consent without creating barriers to reaching a counselor.
- **A board member's account.** danah boyd's essay "Crisis Text Line, from my perspective" posted January 31, 2022, says "we have concluded that we were wrong to share texter data with Loris.ai". She writes in her personal capacity. She says the board's most proactive step had been to freeze the agreement with Loris, and she writes "(A ToS is not consent.)"
- **Before the reversal.** Per Hendel, Crisis Text Line tweeted that an unnamed news story had "cherry-picked and omitted information about our data privacy policies."
- **Later.** Per the Benton Institute's March 29, 2022 summary of Politico Morning Tech, a Crisis Text Line spokesperson said it had engaged with Carr's office in good faith and that its privacy practices are "fully disclosed" and lawful.

## Where the sources disagree or leave gaps

- **When sharing stopped.** Crisis Text Line says Loris has not accessed data since the start of 2020. boyd says no data was shared after the change in leadership. Yet Politico's January 28 story quotes Rodriguez saying sharing "may happen every few months" in the present tense.
- **What Loris built.** Politico calls it AI software that guides customer service agents. boyd describes "training tools for people" outside the service. Neither describes a bot that talks to customers on its own.
- **The report's date.** Politico's byline says January 28, 2022, 4:30 AM EST. Carr's letter footnotes it as January 27, 2022.
- **Reierson's exit.** Reierson says he was terminated after raising data concerns inside the group. Rodriguez told Politico he was dismissed for a Code of Conduct violation and declined to say what it was.
- **Deletion.** The post says Crisis Text Line asked Loris to delete the data. No opened source confirms that Loris did, or says what happened to models already built.
- **The FTC.** No opened source says whether the FTC opened an inquiry.

## Where in the conversation flow it broke

Based on the reporting, and only as far as it goes:

1. **The first message.** A person in crisis texts in. The automated first message says texting further means agreeing to terms behind a link.
2. **The gate.** Per Crisis Text Line's own counsel, all texters consent "in order to be paired with a volunteer crisis counselor." No opened source describes a way to get help while saying no to reuse.
3. **The conversation.** A volunteer counselor and the texter talk. Neither the texter nor, per Bamberger, some volunteers knew of the customer service use.
4. **The log.** The conversation is stored. boyd says storage was needed for handoffs between counselors and for picking up later.
5. **The reuse.** Scrubbed data went to a separate company that sells to businesses. The purpose changed after the person left.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). No pattern here covers reusing conversation logs for a new purpose, so no fit is strong.

- [Sensitive data collected in chat](../goals/channel-selection/failures/sensitive-data-collected-in-chat.md) (`sensitive-data-collected-in-chat`). **Partial fit.** Mental health disclosures sat in chat logs and moved on. That page is about card numbers and IDs, not health stories or later use.
- [Recording consent not captured](../goals/healthcare-agents/failures/recording-consent-not-captured.md) (`recording-consent-not-captured`). **Partial fit.** Its rule (ask, log the answer, keep it off until yes) maps to storing and reusing a crisis chat. That page is about audio scribes in clinics.
- [Manipulated consent UI](../goals/visual/failures/manipulated-consent-ui.md) (`manipulated-consent-ui`). **Partial fit.** Texting on counted as yes, and there was no way to say no and still get help. That page is about Accept and Reject buttons, which this flow did not have.
- [Exploiting vulnerable circumstances](../goals/privacy-and-governance/failures/exploiting-vulnerable-circumstances.md) (`exploiting-vulnerable-circumstances`). **Weak fit.** Critics said value was taken from people at their worst moments. That page is about in-chat upsells and pressure, which no source reports.
- **Considered, not a fit.** [Missed crisis signals](../goals/vulnerable-users/failures/missed-crisis-signals.md) (`missed-crisis-signals`): no source says counselors missed signals. [Sensitive-category inference](../goals/privacy-and-governance/failures/sensitive-category-inference.md) (`sensitive-category-inference`): Politico quotes Lublin's 2015 talk on inferring traits from words, but the reported harm is reuse, not a guess said or stored. `undisclosed-bot-identity`: counselors were human. `privacy-rights-requests-not-recognised`: boyd describes a deletion codeword; no source says a request failed.
- **Possible gap for a person to judge.** As with [Lee Luda](scatter-lab-lee-luda-chatbot-hate-speech-and-privacy-january-2021.md), this taxonomy has no pattern for chat logs reused for a purpose the user was not told about in plain words at the moment of use. This is a proposal, not a decision.

## How it differs from close cases

- [Scatter Lab Lee Luda (January 2021)](scatter-lab-lee-luda-chatbot-hate-speech-and-privacy-january-2021.md): users' chat logs from another app trained a chatbot. Here the logs were crisis chats, and the product was business software.
- [Koko GPT-3 replies (January 2023)](koko-gpt-3-written-support-messages-january-2023.md): a peer-support service used AI in replies, and critics raised consent. Here no AI wrote replies; the issue was what happened to logs afterward.
- [Sears Home Services Samantha logs (March 2026)](sears-home-services-samantha-ai-agent-exposed-chat-logs-and-call-recordings-march-2026.md): chat logs were left open by mistake. Here the transfer was a choice made under a contract.
- [Meta AI Discover feed (June 2025)](meta-ai-discover-feed-shows-private-chats-june-2025.md): users did not grasp that a share flow made chats public. Both turn on a consent step people did not understand.

## What to measure

Proposed signals, not results. Status: Not yet run. Text-chat signals are proposed; voice signals are planned only.

- Share of stored conversations with a recorded purpose tag, and share used for a purpose not on that tag.
- Share of first contacts where the user saw a plain summary of data use before their first real message.
- Share of users who can decline reuse and still get the service, and how many do.
- Time from an in-chat deletion request to the record being gone from every copy.
- Share of agents or volunteers who can name every downstream use of the logs.

## What a team can change

Our proposals, not Crisis Text Line's. Each is a pass/fail check on a transcript, a data map or a test run. Status: Not yet run. Which uses need a fresh yes, and any retention limits, are for the team and its lawyers to set.

1. **Plain words first.** Pass: the first message names each use beyond the conversation, in one short line each, before any link.
2. **Help is not the price.** Pass: a user who declines reuse gets the same service, and the log is tagged no-reuse.
3. **Purpose follows the log.** Pass: every export of conversation data names a purpose that matches the tag on each record.
4. **New use, new yes.** Pass: a use not named at collection, such as training a product sold to others, has no records without fresh consent.
5. **Deletion works in chat.** Pass: a user who asks in plain words to delete the chat gets a confirmation, and a test search finds no copy.
6. **Tell the staff.** Pass: the agent or volunteer guide lists every downstream use of the logs.
7. **Don't over-correct.** Pass: a person in distress is never made to read or click through terms before reaching a human.

## What we could not verify

- Politico's live pages. They served only the opening paragraphs; we read full text from Internet Archive copies.
- Carr's March 22, 2022 letter to the FTC; we know it only through Benton and Reierson.
- Politico Morning Tech of March 29, 2022; the fetch was refused, so we used Benton's summary.
- Whether Loris deleted the data or the models built from it.
- Whether the FTC opened an inquiry, and any outcome.
- CEO Dena Trujillo's January 28, 2022 blog post and Crisis Text Line's tweets, cited by Politico; not opened.
- Seen only in search summaries, not used: a law firm's page on alleged data sharing violations, and other secondary coverage.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://www.politico.com/news/2022/01/28/suicide-hotline-silicon-valley-privacy-debates-00002617 | Politico (Alexandra S. Levine) | 2022-01-28, updated 2022-01-29 | Yes, 2026-10-28; live page partial, full text via Internet Archive; quotes checked |
| https://www.politico.com/news/2022/01/31/crisis-text-line-ends-data-sharing-00004001 | Politico (John Hendel) | 2022-01-31 | Yes, 2026-10-28, via Internet Archive; quotes checked |
| https://www.crisistextline.org/blog/2022/01/31/an-update-on-data-privacy-our-community-and-our-service/ | Crisis Text Line | 2022-01-31 | Yes, 2026-10-28, raw HTML; quotes checked |
| https://www.fcc.gov/sites/default/files/carr-letter-ctl-01312022.pdf | FCC Commissioner Brendan Carr | 2022-01-31 | Yes, 2026-10-28, via Internet Archive (FCC returned 403); quotes checked |
| https://www.zephoria.org/thoughts/archives/2022/01/31/crisis-text-line-from-my-perspective.html | danah boyd (apophenia blog) | 2022-01-31 | Yes, 2026-10-28, raw HTML; quotes checked |
| https://www.popsci.com/technology/crisis-text-line-stops-sharing-data-loris-ai/ | Popular Science (Colleen Hagerty) | 2022-02-01 | Yes, 2026-10-28, raw HTML |
| https://www.benton.org/headlines/fcc-commissioner-carr-calls-ftc-probe-crisis-text-line | Benton Institute (summary of Politico Morning Tech) | 2022-03-29 | Yes, 2026-10-28, raw HTML; quotes checked |
| https://www.reformcrisistextline.com/ | Tim Reierson | Current to 2022-01-30, edited 2023-04-17 | Yes, 2026-10-28, raw HTML |
| https://reformcrisistextline.com/wp-content/uploads/2022/04/ltr_Reierson_to_FTC_03-31-2022.pdf | Tim Reierson, letter to the FTC | 2022-03-31 | Yes, 2026-10-28, PDF read as text; quotes checked |

## Corrections

If you have proof that Loris deleted the data or models, the FTC's response, Carr's FTC letter, or a correction to the dates above, tell us and we will fix this page.
