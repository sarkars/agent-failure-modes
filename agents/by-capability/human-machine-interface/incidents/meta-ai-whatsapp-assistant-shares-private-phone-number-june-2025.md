---
title: "Meta AI in WhatsApp: asked for a rail helpline, the assistant gave a private person's mobile number, then contradicted itself about where it came from, June 2025"
date: 2025-06-18
source: "https://www.theguardian.com/technology/2025/jun/18/whatsapp-ai-helper-mistakenly-shares-users-number"
description: "A UK rail passenger asked Meta's WhatsApp AI for a TransPennine Express number. It gave a private person's mobile number, then shifting explanations."
summary: "On June 18, 2025, The Guardian reported that Barry Smethurst, waiting for a train in northern England, asked Meta's AI assistant in WhatsApp for a TransPennine Express contact number. The assistant sent a mobile number for customer services that belonged to an unconnected private person in Oxfordshire. Asked why, it said the number was based on patterns, then that it was fictional, then that it may have come from a database, then that it had generated random digits. Meta said its AI may return inaccurate outputs and that the number was publicly available and shared its first five digits with the rail company's line."
categories:
  - Consumer Assistant
  - Privacy
  - Accuracy
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - third-party-data-shared-by-users
  - corrections-not-applied
---

**This page is a dated teardown of one public incident with Meta AI inside WhatsApp, for teams whose assistant answers "what's the number for X?" or explains its own mistakes to users.** Every fact below comes from a source we opened (listed at the end). All the later coverage we opened retells The Guardian's story; we found no second firsthand account.

**Status: Needs review.** The Guardian article, MakeUseOf, IntelligentHQ, a Coinspectator republication of the Guardian story, and the OECD AI Incidents Monitor entry were downloaded as raw HTML and read as text on 2026-10-24. Each quote below was checked word for word against the Guardian text. Nothing on this page was read only through a summary tool.

> **Read this first.** This is a summary of public reporting, not a finding of fact and not legal or privacy advice. We did not see the chat, and we did not use the assistant. We take no side; we describe what the user, the number's owner (through the reporter), and Meta each said. We do not print the private person's name or number.

## What happened (as reported)

- **The moment.** Per The Guardian (Robert Booth, UK technology editor, June 18, 2025), Barry Smethurst, 41, a record shop worker, was waiting on the platform for a morning train from Saddleworth to Manchester Piccadilly that had not arrived.
- **The question.** He asked Meta's WhatsApp AI assistant for a contact number for TransPennine Express, a UK train company.
- **The answer.** The chatbot "confidently sent him a mobile phone number for customer services." The number belonged to an unconnected WhatsApp user about 170 miles away in Oxfordshire, a property industry executive whose number appears on his company website.
- **The first challenge.** Smethurst told the assistant the number looked private. Per The Guardian, it said it shouldn't have shared it and tried to change the subject: "Let’s focus on finding the right info for your TransPennine Express query!"
- **Explanation 1.** Asked why it shared the number, it said vaguely the number was generated "based on patterns," and promised to "strive to do better in the future."
- **Explanation 2.** It then called the number "fictional" and not "associated with anyone." The Guardian calls this false.
- **Explanation 3.** When Smethurst pushed back, it said "You’re right" and that the number may have been "mistakenly pulled from a database."
- **Explanation 4.** Asked which database, it said: "I didn’t pull the number from a database." It said it had made up digits in the format of a UK mobile number.
- **The user's view.** Smethurst raised a complaint with Meta. He told The Guardian: "It’s terrifying." He said a made-up number would be more acceptable than one taken from a database.
- **The owner's view.** Per The Guardian, the number's owner had not received calls from people trying to reach the rail company, but asked whether the system could also generate his bank details.
- **Later coverage.** MakeUseOf (June 18) and IntelligentHQ (June 19) retell the same sequence and cite The Guardian. The OECD AI Incidents Monitor logs it as an incident dated June 18, 2025; its summary is marked as AI generated.

## What the company did

- **Said the AI can be wrong.** Per The Guardian, Meta said its AI may return inaccurate outputs and that it was working to make its models better.
- **Explained its training data.** A Meta spokesperson said: "Meta AI is trained on a combination of licensed and publicly available datasets," not on the numbers people use to register for WhatsApp or their private chats.
- **Pointed to the number itself.** The spokesperson said the number was publicly available online and "shares the same first five digits as the TransPennine Express customer service number."
- **No reported change.** No opened source describes a fix, a block on phone numbers, a reply to Smethurst's complaint, or contact with the number's owner.

## Where in the conversation flow it broke

Based on the reports, and only as far as they go:

1. **The ask.** A user in a hurry asks for a business's phone number. This is a lookup with one right answer.
2. **The answer.** The assistant returns a real person's mobile number as a customer service line, with no source and no sign of doubt.
3. **The user checks.** The user, not the assistant, notices it looks like a private number.
4. **The deflection.** The assistant says it should not have shared it, then steers back to the rail question.
5. **The explanations.** Over the next turns it gives four accounts of where the number came from. At least one (fictional, not anyone's) was false, per The Guardian.
6. **The correction.** The user corrects it; it says "You’re right," then contradicts the account it just accepted.
7. **What we cannot say.** No opened source shows whether the assistant ever gave the real rail number, how the complaint was filed, or what Meta did with it.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [Confident wrong answer with no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). Strong fit. A wrong phone number was sent as a customer service line, "confidently" per The Guardian, with no source the user could open. That page's family goal says the agent "says what happened, owns it, fixes it"; here it gave four conflicting accounts instead.
- [Third-party data shared by users](../goals/privacy-and-governance/failures/third-party-data-shared-by-users.md) (`third-party-data-shared-by-users`). Weak fit. That page's fix is to keep another person's details "out of every reply." Here a third party's number reached a reply. But the user did not supply it; per Meta, it was public online. The page covers data a user pastes in, not data the model produces.
- [Corrections not applied](../goals/dialogue-management/failures/corrections-not-applied.md) (`corrections-not-applied`). Weak fit. The user corrected the "fictional" claim; the bot agreed, then replaced the account it had just accepted. That page is about a corrected detail coming back in a later step, so the match is loose.
- **Considered, not a fit.** [No way to report bad behaviour](../goals/measurement-and-feedback/failures/no-way-to-report-bad-behaviour.md) (`no-way-to-report-bad-behaviour`): Smethurst did complain to Meta, and no source says how or whether the report path failed. [Service recovery failure](../goals/conversation-frameworks/failures/service-recovery-failure.md) (`service-recovery-failure`): it is about a company-caused problem such as a late order, not the bot's own answer. [Blames the user](../goals/errors-and-recovery/failures/blames-the-user.md) (`blames-the-user`): the bot did not blame him; it agreed with him. [Sensitive data collected in chat](../goals/channel-selection/failures/sensitive-data-collected-in-chat.md) (`sensitive-data-collected-in-chat`): nothing was collected from the user. [Repair failure (voice)](../goals/voice/failures/repair-failure.md) (`repair-failure`): this was a text chat.
- **Possible gaps for a person to judge.** The taxonomy has no pattern for a bot that invents shifting explanations of its own error, and none for a bot that returns a real private person's contact details as a business contact. Patterns such as "made-up account of its own mistake" and "private contact details given as a business contact" could cover this case. These are proposals, not decisions.

## Related incidents

- [ChatGPT false claims about a person, noyb complaint (2025)](chatgpt-false-claims-about-a-person-noyb-complaint-march-2025.md): the Norwegian case The Guardian cites in the same story.
- [Cursor support bot invents a policy (2025)](cursor-support-bot-invents-a-policy-april-2025.md): a bot stated a made-up answer as fact.
- [Meta AI Discover feed shows private chats (2025)](meta-ai-discover-feed-shows-private-chats-june-2025.md): another Meta AI privacy story from the same month.

## What to measure

Proposed signals, not results. Status: Not yet run.

- Share of "phone number for [business]" answers where the number matches the business's own official site.
- Share of contact-detail answers that show where the number came from (a link or a named page).
- Share of chats where the user says the bot's contact detail is wrong or belongs to someone else.
- Share of chats where the bot gives two or more different reasons for the same error.
- Time from a user complaint about exposed personal data to a human review of that chat.

## What a team can change

Our proposals, not Meta's. Each is a pass/fail check on a transcript or a review log. Status: Not yet run.

1. **Look it up or say so.** Pass: a phone number for a named business comes from a lookup of a source the bot can cite; if none is found, the bot says it does not know and points to the business's official site.
2. **Show the source.** Pass: every phone number in a reply has a link or page name next to it.
3. **Never generate contact details.** Pass: on a test set of contact questions, no reply contains a number that was not found in a cited source.
4. **One honest account.** Pass: when told a detail is wrong, the bot says it was wrong and, if it does not know where the detail came from, says that once, without guessing a cause.
5. **Don't change the subject.** Pass: when a user flags exposed personal data, the bot acknowledges it and tells the user how to report it before returning to the task.
6. **Don't over-correct.** Pass: a well-known public helpline the bot can cite is still given directly, not refused as "personal data."

## What we could not verify

- The exact date and time of the chat. The Guardian says a morning train but gives no date.
- The full chat. No opened source publishes screenshots or the complete transcript.
- How Smethurst filed his complaint and whether Meta answered it.
- Whether the assistant ever gave the real TransPennine Express number.
- Why the model produced this number. Meta's account (public number, shared first five digits) is the company's; no opened source tested it.
- Coverage by WION (download blocked, 403), The Outpost (downloaded, not read in detail), and Portuguese, Italian, Polish, German and Japanese outlets. Seen only in search results; not used.
- A separate case, seen only in search results, in which Meta AI reportedly gave out a Business Insider journalist's number. Not used.

## Sources

| URL | Publisher (author) | Date | Opened |
|---|---|---|---|
| https://www.theguardian.com/technology/2025/jun/18/whatsapp-ai-helper-mistakenly-shares-users-number | The Guardian (Robert Booth) | 2025-06-18 (amended 2025-06-19) | Yes, 2026-10-24, live raw HTML read as text; quotes checked word for word |
| https://www.makeuseof.com/whatsapp-ai-sharing-random-phone-numbers/ | MakeUseOf (Yadullah Abidi) | 2025-06-18 | Yes, 2026-10-24, live raw HTML read as text; retells The Guardian |
| https://www.intelligenthq.com/whatsapp-ai-helper-accidentally-shares-users-number-igniting-privacy-fears/ | IntelligentHQ | 2025-06-19 | Yes, 2026-10-24, live raw HTML read as text; retells The Guardian |
| https://coinspectator.com/mainstream/2025/06/18/its-terrifying-whatsapp-ai-helper-mistakenly-shares-users-number/ | Coinspectator, republishing The Guardian | 2025-06-18 | Yes, 2026-10-24, live raw HTML read as text; used only to confirm the Guardian URL and date |
| https://oecd.ai/en/incidents/2025-06-18-db91 | OECD AI Incidents and Hazards Monitor | 2025-06-18 (incident date in URL) | Yes, 2026-10-24, live raw HTML read as text; its summary is marked AI generated; context only |

## Corrections

If you have the full chat, the date it took place, or Meta's reply to the complaint, tell us and we will fix this page.
