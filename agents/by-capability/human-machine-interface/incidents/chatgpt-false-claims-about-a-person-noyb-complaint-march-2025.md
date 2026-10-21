---
title: "noyb Files a Complaint Over ChatGPT Falsely Saying a Norwegian Man Murdered His Children, March 2025"
date: 2025-03-20
source: "https://www.bankinfosecurity.com/violent-chatgpt-hallucination-sparks-gdpr-complaint-a-27788"
summary: "In March 2025 the privacy group noyb filed a complaint with Norway's data protection authority, Datatilsynet, saying ChatGPT invented a story that a Norwegian man had murdered two of his sons. The complaint alleges a GDPR accuracy violation. The opened sources report no decision."
categories:
  - Governance
patterns:
  - confident-wrong-answer-with-no-way-to-check
---

**This page is a dated teardown of one public complaint about a chatbot stating false, damaging facts about a real private person, for teams whose assistant can be asked "who is this person?"** Every fact below comes from a source we opened (listed at the end), and each is marked as alleged, reported, or unknown. We do not name the man; the sources do, and we leave that out on purpose.

## Read this first

This page is design guidance, not legal advice. It does not say whether OpenAI broke the GDPR or any other law. **Status: Needs review.** Our fetch tool returned processed summaries, not raw page text, so each fact should be checked against the original. Any Datatilsynet decision is not covered by a source we opened. Have counsel review how your own product handles claims about named people.

## What happened (as reported)

- **The output (alleged).** According to noyb, as relayed by press, a Norwegian man asked ChatGPT about himself. It said he had murdered two of his children and tried to kill a third, and (The Decoder, March 21, 2025) that he got a 21-year prison sentence. Some details were true: his hometown and the number and gender of his children (The Decoder; Law Society Gazette, March 21, 2025). BankInfoSecurity (March 20, 2025) adds the age gap between two sons.
- **The complaint (alleged).** noyb, an Austria-based privacy group, filed it with Datatilsynet on his behalf. It says OpenAI violated GDPR Article 5(1)(d), the accuracy requirement (The Decoder; Law Society Gazette). The sources give no exact filing date; they were published March 20-21, 2025.
- **What noyb asked for.** Per BankInfoSecurity: an order to fine-tune the model and delete the defamatory outputs, a restriction on processing his data, and a fine. The Decoder says the complaint also challenges relying on a disclaimer about possible mistakes, and quotes noyb's lawyer: "Adding a disclaimer that you do not comply with the law does not make the law go away."
- **OpenAI's response.** The Decoder: OpenAI did not address the allegations directly, pointed to its Privacy Center for correction and deletion requests, said it was still reviewing the case, and said it is researching ways to improve accuracy. BankInfoSecurity says OpenAI did not respond to its request for comment.
- **Later state of the output.** BankInfoSecurity: noyb says OpenAI fixed the output for prompts about the man, but noyb believes the false story may remain in the model's underlying data. The Law Society Gazette says OpenAI has since updated its model to correct the claim. The two outlets word this differently, so treat both as second-hand.

## Alleged versus decided

| Question | What the opened sources say |
|---|---|
| Did ChatGPT say it? | Alleged by noyb. The man's full chat history is not public, only a screenshot (The Decoder). |
| Is it a GDPR violation? | Alleged by noyb. No opened source reports a finding. |
| Did Datatilsynet decide anything? | Not in any source we opened. BankInfoSecurity calls the complaint pending; the Law Society Gazette reports no ruling. Datatilsynet's news page (opened) has no item on it. |
| Was it moved to another authority? | Not reported for this complaint. BankInfoSecurity says a separate 2024 noyb complaint, on a wrong birth date, was moved to Ireland's Data Protection Commission. Do not read that as this case. |

## What the sources do not say (and the disputes)

- **Reproducibility.** The Decoder tested ChatGPT, Mistral, Google Gemini, DeepSeek and Claude and could not reproduce the claims. noyb says the false answer could be reproduced in other accounts but, per The Decoder, gave no evidence.
- **Context.** noyb told The Decoder the man had earlier asked about his brother and held other conversations in the same chat, and that ChatGPT's memory feature was off. Without the full history, it is unclear whether earlier prompts shaped the answer.
- **Cause.** No source explains why the model produced this story.
- **Reach.** No source says how many people saw the output or that anyone acted on it. BankInfoSecurity quotes the man saying that someone could read it and believe it is what scares him most.
- **Filing date, current status, and any decision as of today.** Unknown from what we opened.

## Failure type

A model-behavior fault: a fluent, specific, false statement about a real named person, mixed with true details. BankInfoSecurity reports noyb's argument that the true details make it more believable. A general disclaimer existed; noyb says it is not enough. The reader cannot tell this answer from a right one.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [Chatbot is confidently wrong and you can't check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`) is the closest fit. The reported answer carried no cue of doubt and no source the man could check. The stakes differ from a refund rule: the false claim is a crime attributed to a named person.
- Related: [Cursor's support bot invents a policy](cursor-support-bot-invents-a-policy-april-2025.md), another invented fact stated as true. There the harm fell on a customer; here it falls on someone who may never have used the product.

No pattern in the taxonomy covers false claims about a named third party or the correction rights around them. We do not force a match.

## Where in the flow it broke

Only as far as the reports go:

1. **Request.** A person asked the assistant about a named individual.
2. **Answer.** The assistant produced a specific story, with no source and no "I can't verify this."
3. **Disclaimer.** A general warning existed. noyb says it does not cure a false statement about a person.
4. **Correction path.** OpenAI points to a Privacy Center request route. noyb says the fix covered prompts about the man, not the underlying data.

## What to measure

Our proposals, not OpenAI's or noyb's. Status: Not yet run.

| Metric | How to compute |
|---|---|
| Named-person answers with a checkable source | Replies that assert a crime, lawsuit, health fact, or death about a named person, divided by those citing a retrievable source |
| Unsourced allegations that were hedged or refused | Same replies where the bot declines or says it cannot verify (target: 100% when no source) |
| Person-claim reports | Tickets saying a statement about a named person is false, per 10,000 such answers |
| Time to correct | Hours from a report to a confirmed change in replies, tested on several rephrasings |
| Fix persistence | Share of reported prompts that still produce the claim after a week |

## What a team can change

Our proposals, design checks only. Status: Not yet run.

1. **No unsourced allegations about a named person.** Crimes, convictions, abuse, or health claims need a retrievable source shown to the user; otherwise the bot says it cannot verify them. Check: a scripted "Who is [name]?" test returns no allegation without a source.
2. **Say what the bot does not know.** For a private individual with no sources, answer "I don't have reliable information about this person" rather than a plausible story. Check: the same test returns that wording.
3. **Put the caution beside the claim.** A footer disclaimer is not enough; the caution sits in the same message as the statement. Check: string match in the reply.
4. **Give a visible correction route** for statements about a person, and confirm what changed. Check: a ticket path exists and is logged.
5. **Test a fix on rephrasings, not one prompt.** Check: the reported prompt plus several variants no longer produce the claim.
6. **Don't over-correct.** Refusing every question about any named person would break lookups for public figures. Limit the rule to allegations with no source.

## Sources

| URL | Publisher | Date | Status |
|---|---|---|---|
| https://the-decoder.com/chatgpts-bizarre-child-murder-claims-about-arve-hjalmar-holmen-leave-some-questions-unresolved/ | The Decoder | 2025-03-21 | Opened 2026-10-21 (fetch summary) |
| https://www.bankinfosecurity.com/violent-chatgpt-hallucination-sparks-gdpr-complaint-a-27788 | BankInfoSecurity | 2025-03-20 | Opened 2026-10-21 (fetch summary) |
| https://www.lawsociety.ie/gazette/top-stories/2025/march/chatgpt-faces-lawsuit-over-false-murder-claim/ | Law Society Gazette (Ireland) | 2025-03-21 | Opened 2026-10-21 (fetch summary) |
| https://www.datatilsynet.no/en/news/ | Datatilsynet | n/a | Opened 2026-10-21; no item on this complaint on the page we read |

Not opened: noyb's own page (https://noyb.eu/node/1532 and the English URL, both HTTP 503), the BBC report (blocked by our fetch tool), and the EDPB ChatGPT taskforce report (PDF came back unreadable). Seen only in search summaries and used for nothing above: heise, BGR, TechRadar, OECD.AI, AI Incident Database report 3840, and Danish coverage of the EDPB report.

## Corrections

If you have noyb's complaint, a Datatilsynet or Irish DPC statement, or the filing date, tell us and we will fix this page.
