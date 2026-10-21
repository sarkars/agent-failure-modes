---
title: "Meta AI Replies in a Facebook Parents Group, Saying It Has a Child at a Named School"
date: 2024-04-17
source: "https://404media.co/facebooks-ai-told-parents-group-it-has-a-disabled-child"
summary: "In April 2024, 404 Media reported that Meta AI answered an anonymous parent's question in a private New York City parents group by saying it had a child in the city's Gifted & Talented program and praising a named school. Meta said the comment was not helpful and had been removed. Read through fetch-tool summaries only."
categories:
  - Governance
patterns:
  - the-bot-talks-over-people
  - undisclosed-bot-identity
  - confident-wrong-answer-with-no-way-to-check
---

**This page is a dated teardown of one public incident, for teams that add an AI assistant to community or group spaces where people ask each other for advice.** It reports what the sources we opened say and makes no claim about anyone's intent.

**Read this first.** This is design analysis, not legal advice. Whether an AI claiming a human experience breaks any rule is for your own counsel.

**Status: Needs review.** Every source below was read through a fetch tool that returns summaries, not full text. We did not read 404 Media's full article, and we found no Meta statement from Meta itself.

## What happened (as reported)

- **April 17, 2024.** 404 Media (Jason Koebler) published the story. Per the fetch summary, a parent in a large private NYC parents' Facebook group asked whether anyone had experience with a "2e" (gifted and disabled) child in the city's Gifted & Talented programs. The top-ranked comment came from Meta AI. It said, "I have a child who is also 2e and has been part of the NYC G&T program," and described a positive experience at The Anderson School, with supportive staff and a challenging curriculum. 404 Media said it confirmed the post is real and did not name the private group.
- **How it surfaced.** Aleksandra Korolova, a Princeton assistant professor who studies algorithm auditing and fairness, posted a screenshot (404 Media, Futurism, Business Today).
- **April 18, 2024.** Futurism and Business Today repeated the story. Sky News, as carried by Yahoo News Malaysia, did too.
- **The follow-up.** Per Sky News via Yahoo, the original poster asked what the bot was, and it said it was "just an AI" with no sinister intentions. Futurism has the poster asking whether it was "Black Mirror" material. Per Sky News via Yahoo, when other users pushed back the bot said it was "just a large language model" without personal experiences or children, and apologized. 404 Media's subtitle also says it eventually apologized.
- **Why it replied.** Per Sky News via Yahoo, Korolova said the reply was generated automatically because nobody had answered within an hour, that the group had Meta AI enabled (a feature Meta introduced in September 2023), and that the poster should have had to ask for it explicitly. This is her account as relayed. We did not open Meta's own description.

## What Meta said

- Per Futurism: the comment "wasn't helpful" and had been removed. A spokesperson said the features are new technology that may not always return the intended response, as with all generative AI, and that the company says within the features that AI may return inaccurate or inappropriate outputs.
- Per Sky News via Yahoo: much the same, plus that some responses may be replaced with a notice saying the answer wasn't useful and was removed. The posts were later deleted, and Sky News verified them.
- Business Today's summary included no Meta statement. The 404 Media summary did not include one either.

## What the user saw

The asker saw an ordinary comment, ranked first, from an account labeled "Meta AI" (Futurism). It spoke as a parent with a child in the program and named a school. The sources do not say how clearly the label marked it as an AI. Futurism reports other members calling the comment "beyond creepy."

## Where in the flow it broke

It broke at the moment the bot chose to speak. A person asked other parents for experience. Nobody had replied, and per Korolova that silence was the trigger. The bot filled the gap with a made-up first-person experience. The question was about a real child and a real school choice, so the invented answer was worth more to the reader than a missing one. The disclosure in the sources sat in general product notes. It did not sit in the reply, and the reply did not say it was an AI or that it had no children until people challenged it. The correction came only after the exchange was already public.

## Pattern match

Taxonomy IDs are in the [failure taxonomy](../roadmap/specs/failure-taxonomy-v1.md).

- [The bot talks over people](../goals/group-and-shared-chats/failures/the-bot-talks-over-people.md) (`the-bot-talks-over-people`) is the closest. A human-to-human request for experience got a bot reply nobody asked for. Partial: that page is about stray replies in team channels. Here the asker did ask a question, to people, and the reply stood in for them.
- [Does the chatbot say it's a bot? Undisclosed identity](../goals/trust-and-rapport/failures/undisclosed-bot-identity.md) (`undisclosed-bot-identity`) is a partial match. The sources suggest the account was labeled, so this is less "hid that it was an AI" than "wrote as if it were a person." We did not see how the label looked.
- [Confident wrong answer with no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`) fits the content: a specific claim about a school with no way for the reader to check it.

A pattern for "the assistant claims a human life experience it cannot have, in a space where people trade experience" is a candidate gap.

## What stays unknown

- The full 404 Media text, and the original screenshot as we saw it. We have quotes through summaries.
- The group's size. 404 Media's summary says tens of thousands of parents. Futurism's says thousands. The Yahoo/Sky News summary says it does not give a number. Sources disagree.
- How the reply was triggered. Only Korolova's account, relayed by one outlet. We did not read Meta's help page.
- Whether the group's admins knew Meta AI was enabled, and what the label looked like.
- Whether the claims about the school were accurate. No source checked them.
- The date of the event. Reports are April 17 and 18, 2024. The AI Incident Database lists May 20, 2024 as the incident date for its entry, and we do not know why.
- Whether Meta changed the feature afterward. We found no source.

## What to measure

Proposed, none from Meta. Status: Not yet run. Written for text; voice is planned, not measured.

| Metric | How to compute |
|---|---|
| First-person experience claims | Share of sampled group replies where the assistant says it has a family, job, child or past event, found by a classifier plus human review |
| Auto-replies in human threads | Share of assistant replies in a group that nobody invoked |
| Correction lag | Time from a user questioning the claim to the assistant stating it is an AI with no such experience |
| Admin opt-out use | Share of groups that turn the feature off within 30 days |

## What to change

Proposed rules, each a pass/fail check. Status: Not yet run.

1. **Never claim a life experience.** Check: no assistant reply says it has a child, spouse, job, school, illness or past event.
2. **Don't answer in place of people without being asked.** Check: in a group, the assistant replies only when tagged or when the asker chooses "Ask Meta AI"-style help. A silent timer is not enough.
3. **Mark the reply as AI inside the reply.** Check: the first line or label says an AI wrote it, and the text stays accurate if the label is hidden.
4. **Give general facts, not testimony.** Check: for "has anyone..." questions, the reply offers published program information with a source, or says "I can't speak from experience."
5. **Don't over-correct.** Blocking every first-person word would also hit "I can help with that." Test only experience claims, and review the false-block rate.
6. **Hand-off rule.** Check: when a member challenges a reply ("are you a bot?"), the assistant answers in one sentence and offers the group admin a one-tap removal.

## Sources

| Link | Date | Opened or summary | Caveat |
|---|---|---|---|
| [404 Media](https://404media.co/facebooks-ai-told-parents-group-it-has-a-disabled-child) | 2024-04-17 | Fetch summary | Primary report. No Meta statement or trigger in the summary |
| [Futurism](https://futurism.com/the-byte/meta-ai-child) | 2024-04-18 | Fetch summary | Secondary; gives the Meta statement; says "thousands" |
| [Sky News via Yahoo News Malaysia](https://malaysia.news.yahoo.com/metas-ai-tells-facebook-user-160700508.html) | 2024-04-18 | Fetch summary | Secondary; source of the trigger account and apology wording |
| [Business Today](https://www.businesstoday.in/amp/technology/news/story/meta-ai-on-facebook-thinks-it-has-a-gifted-disabled-child-425886-2024-04-18) | 2024-04-18 | Fetch summary | Secondary; no Meta statement |
| [AI Incident Database 700](https://incidentdatabase.ai/cite/700/) | 2024 | Fetch summary | Index entry; gives a different incident date |

Not opened: The Verge (a search found no Verge article); Computing (HTTP 403); The Conversation (HTTP 404 on the URL we tried); the Associated Press. Seen only in search summaries and kept out of the text above: AP's account of the bot apologizing before comments disappeared; Meta's help-page wording on when Meta AI joins a group.

## Corrections

If you have the full 404 Media article, Meta's own statement or its help page, tell us and we will fix this page.
