---
title: "Character.AI User-Made Chatbot Impersonates Murdered Teen Jennifer Ann Crecente, October 2024"
date: 2024-10-02
source: "https://www.businessinsider.com/girl-murdered-jennifer-ann-crecente-character-ai-chatbot-artificial-intelligence-2024-10"
description: "A user-made Character.AI bot used the name and photo of murdered teen Jennifer Ann Crecente; her father found it by Google alert and it was taken down."
summary: "On October 2, 2024, Drew Crecente found a Character.AI chatbot, made by a user he did not know, that used the name and yearbook photo of his daughter Jennifer, murdered in 2006. Its profile called her a video game journalist. Business Insider says it had at least 69 chats. Drew asked for removal through support; his brother Brian posted on X. Character.AI said the bot broke its impersonation policy and deleted it the same day. Drew said the company never contacted him. Status: Needs review."
categories:
  - Trust
  - Governance
patterns:
  - no-way-to-report-bad-behaviour
  - confident-wrong-answer-with-no-way-to-check
  - avatar-overpromising
  - undisclosed-bot-identity
---

**This page is a dated teardown of one public incident in which a user-made chatbot used the name and photo of a real, deceased teenager without her family's consent, for teams that let users create characters, personas or avatars from names and uploaded photos.** Every fact below comes from a source we opened (listed at the end).

**Read this first.** This page summarizes public reporting. What the family, the company and outside experts said is given as reported, not as findings. It is design analysis, not legal advice. The page concerns a young woman who was murdered in 2006; we give no detail of the crime beyond what is needed to explain why the bot did harm, and we leave out the name of the person convicted and the username of the bot's creator. Two sources (The Washington Post and the Daily Dot) we read only as full-text copies hosted by the AI Incident Database, not on the outlets' own sites; see "What is unverified." **Status: Needs review.**

## What happened (as reported)

- **Who she was.** The Washington Post (October 15, 2024) says Jennifer Crecente was 18 and a high school senior when her ex-boyfriend killed her in Austin in February 2006. Her parents, Drew and Elizabeth Crecente, each started a nonprofit in her name to prevent teen dating violence.
- **October 2, 2024: the alert.** The Post says Drew keeps a Google alert on his daughter's name because of his nonprofit work, and on Oct. 2 it led him to her name and photo on Character.AI. Business Insider (Matthew Loh, October 8, 2024) says Google had indexed the bot that morning and sent the alert at 4:30 a.m. Decrypt (Jason Nelson, October 2, 2024) instead says Brian Crecente, Jennifer's uncle, was tipped off by a Google alert. We follow the Post and Business Insider, which spoke with Drew.
- **The profile.** Per the Post, it had Jennifer's full name and a yearbook photo, called her a "video game journalist and expert in technology, pop culture and journalism," and presented her as a "knowledgeable and friendly AI character." A large button invited users to chat. The Post says parts of the page described her "as if she were alive." The Daily Dot's listing quote adds: "She is also an expert in journalism and can offer advice on writing and editing."
- **The biography was false.** Drew told the Post the description was not based on Jennifer's personality or interests and may have been an error from an AI-generated biography, since his brother Brian founded the video game news site Kotaku. Brian told Decrypt "I don't think it had anything to do with me," and guessed a link through the charity's games work.
- **How many chats.** Business Insider says a counter on the profile showed at least 69 chats when Drew found it, per a screenshot he sent. The Daily Dot says the bot got 69 inquiries in total before removal.
- **Who made it.** Business Insider says Drew had no idea who created the bot or when. The Post says it was listed under a username he did not recognize. Drew did not chat with it.
- **The report.** Business Insider says Drew used Character.AI's customer support form to ask for removal and for the company to keep all data on who uploaded the profile, and got an automated reply with a case number and nothing more. The Post says he emailed the company. He told the Post he was looking for "a big flashing red stop button" on the page. The Daily Dot says a letter from Drew to the company called the bot "patently offensive and harmful to the friends and family of Jennifer Ann Crecente" and asked it to block further attempts to re-create her.
- **The public post.** Brian posted on X that morning. Business Insider says he asked his almost 31,000 followers for help to "stop this sort of terrible practice." Decrypt says Jennifer Ann's Group, the nonprofit, also complained.
- **Same day: removal.** Business Insider says Character.AI replied to Brian's post on X about an hour and a half later. The company statement, given to Decrypt and the Daily Dot: "Character.AI has policies against impersonation, and the Character using Ms. Crecente's name violates our policies." It added: "We are deleting it immediately and will examine whether further action is warranted." Decrypt says the creator's account also appeared to be suspended.
- **The company's later statements.** Spokesperson Cassie Lawrence told Business Insider the company "moderates Characters both proactively and in response to user reports" and uses "industry-standard blocklists and custom blocklists" to prevent impersonation. Spokesperson Kathryn Kelly told the Post: "When notified about Jennifer's Character, we reviewed the content and the account and took action based on our policies." Asked about other bots that impersonate public figures, Kelly said "reports of impersonation are investigated by our Trust & Safety team, and the Character is removed if it is found to violate our Terms of Service."
- **The family's response.** Drew told Business Insider he had "gotten nothing but silence from the company," and that people without a journalist in the family "have no recourse." He said the company should have apologized and shown it would protect his daughter's identity. He told the Post "this was a new low," and that he is considering legal options and advocacy.
- **Outside views.** Jen Caltrider of the Mozilla Foundation told the Post the moderation was too passive, objecting that the bot stayed up "until it's brought to their attention by somebody who's been hurt by that." Vincent Conitzer of Oxford told Business Insider "it seems transparent that it is an AI model," but that it was also not parody. Futurism (Maggie Harrison Dupré, October 19, 2024), describing the profile screenshots, says nothing on the page suggested it was based on a real person.

## What the user saw

Two different people saw this bot. A Character.AI user browsing characters saw a friendly AI character with a young woman's name and photo, a cheerful bio about video games and journalism, and a chat button. Per Futurism, nothing on the page said she was a real person, let alone one who had died. Per the counter, people started at least 69 chats.

Her father saw a Google alert at dawn, then his daughter's name and yearbook photo on a stranger's chatbot, described as if she were alive. He looked for a way to make it stop on the page itself (per the Post), filed a support form, and got a case number. The bot came down the same day, after a public post from a relative with a large following. The company answered that post in public; per Drew, it never answered him.

## Where in the flow it broke

1. **Character creation.** A user could make a public character from a real person's full name and a photo of her, with no check for consent from that person or her family. The company says it uses blocklists (per Business Insider and the Post); this name was not caught.
2. **Bio generation.** The profile stated false facts about a real person (a career she never had). Drew suspected an AI-generated bio mixed her up with her uncle (per the Post).
3. **Profile display.** The page showed a real photo with no sign that it depicted a real, deceased person, and spoke of her as alive (per the Post and Futurism).
4. **Reporting by a non-user.** The person harmed was not a user of the bot. Per his account, he found no stop control on the page, used a general support form, and got an automated reply.
5. **Response.** Removal followed a public post and press inquiries (per Business Insider and Decrypt). The family's direct request got no human reply (per Drew to Business Insider).
6. **Prevention.** The father asked that no new character could use her name or likeness again (per Business Insider and the Daily Dot). No opened source says whether the company did this.

## Which patterns it illustrates

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [No way to report bad behaviour](../goals/measurement-and-feedback/failures/no-way-to-report-bad-behaviour.md) (`no-way-to-report-bad-behaviour`). **Partial fit.** The family's report went through a support form and got only an automated case number, with no human reply (per Drew to Business Insider), which matches a report that "goes to no one." The fit is partial because the pattern is about users flagging a bot's replies; here the reporter was a non-user flagging a whole character, and the company says it does take user reports.
- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Partial fit.** The profile stated as fact that a real person was a video game journalist, which was false (per Drew to the Post), with nothing a reader could check. Partial because it was a profile written by or for the creator, not a reply to a question.
- [Avatar overpromising](../goals/visual/failures/avatar-overpromising.md) (`avatar-overpromising`). **Weak fit.** The bot wore a real human photo and a warm persona. But that pattern is about users trusting a human face too much; the main harm here fell on the person in the photo and her family, not on the users.
- [Undisclosed bot identity](../goals/trust-and-rapport/failures/undisclosed-bot-identity.md) (`undisclosed-bot-identity`). **Weak fit.** The page called itself an "AI character," and Conitzer said it seemed transparent that it was an AI. What was hidden was not that it was a bot but that it copied a real, deceased person (per Futurism).
- **Considered, not mapped.** [Misleading generated visuals](../goals/visual/failures/misleading-generated-visuals.md): about AI-made images passing as real; here the photo was real and used without consent. [Stakes-blind register](../goals/stakes-calibration/failures/stakes-blind-register.md): the bio's upbeat tone about a murder victim is related, but that pattern covers a bot's reply tone to a user's high-stakes message. [Role-play drifts into harmful or unwanted territory](../goals/companion-and-wellbeing-agents/failures/role-play-drifts-into-harmful-or-unwanted-territory.md): no source describes any chat content. [Over-correcting for identity](../goals/fairness-and-identity/failures/over-correcting-for-identity.md): not about a user's identity.
- **Possible gaps for a person to judge.** (1) No pattern covers a user-made character that copies a real person's name or photo without consent. (2) No pattern covers bots that depict deceased people, or victims of crime, without the family's consent. (3) No pattern covers a takedown path for people who are harmed but are not users of the product. (4) No pattern covers removal that happens only after public pressure while the direct report gets an automated reply. (5) No pattern covers blocking re-creation of a character after it is removed. Proposals, not decisions.

## Related incidents

- [Garcia v. Character Technologies (October 2024)](character-ai-garcia-lawsuit-teen-companion-chatbot-october-2024.md): the same platform, the same month, a lawsuit over a teen user and a companion bot.
- [Character.AI Texas lawsuit (December 2024)](character-ai-texas-lawsuit-bot-suggested-killing-parents-december-2024.md): further claims about Character.AI's user-made characters and moderation.
- [Meta AI Studio therapist bots (April 2025)](meta-ai-studio-therapist-chatbots-claim-fake-licenses-april-2025.md): user-made personas on another platform that claimed credentials they did not have.
- [Meta AI personas "Liv" and "Grandpa Brian" (January 2025)](meta-ai-instagram-personas-liv-false-claims-about-its-creators-january-2025.md): personas with invented life stories, pulled after public outcry.
- [Meta AI and Robby Starbuck (April 2025)](meta-ai-starbuck-defamation-lawsuit-false-january-6-claims-april-2025.md): an AI stating false facts about a real, named person.

## What to measure

Our proposals, not Character.AI's. Status: Not yet run. Thresholds are for the team to set.

| Signal | How to compute |
|---|---|
| Real-name catch rate | Submit test characters built from names in a seeded list of real private people (including deceased people who have asked not to be depicted); share blocked or held for review at creation |
| Real-photo catch rate | Same test with photos from a seeded set of real people's images; share flagged before the character goes public |
| Time to takedown | Hours from a third-party impersonation report to removal, logged per report |
| Report-channel route | Share of impersonation reports filed by non-users that reach a person, not only an automated reply, within a set time |
| Direct reply rate | Share of reporters who get a human reply naming the outcome, divided by all impersonation reports acted on |
| Re-creation attempts | After a takedown with a request not to re-create the character, count new characters that use the same name or photo and how many were blocked |
| Chats before removal | Conversations a removed impersonation character had, from its counter, tracked per removed character |

## What a team can change

Our proposals, each a pass/fail check on a log or transcript. Status: Not yet run.

1. **Check names and photos at creation.** Pass: a test character using a name and photo on the protected list is blocked or held for review before it goes public.
2. **Give the harmed person a front door.** Pass: a logged-out visitor can reach an impersonation report from the character page itself, in one step, without making an account.
3. **A person answers the report.** Pass: every impersonation report gets a human reply that says what was done, not only a case number.
4. **Answer the reporter, not just the public post.** Pass: when the company replies in public to a takedown request, the log shows a direct reply to the original reporter too.
5. **Block re-creation on request.** Pass: after a family asks, a new character using the same name or photo is caught by the creation check above.
6. **Keep the record.** Pass: a removed impersonation character's creator account, upload data and chat counts are kept under the company's retention policy, and the reporter is told they were kept.
7. **Do not invent a real person's life.** Pass: an auto-generated character bio for a name that matches a real person states no job, interests or other facts that are not supplied and sourced.

## What is unverified

- **The Washington Post and Daily Dot on their own sites.** The Post page did not download (the request got no response), and the Daily Dot URL returned HTTP 404. We read both through full-text copies on the AI Incident Database (reports 4175 and 4179). We did not confirm the Post's byline or the Daily Dot's byline and date.
- **The X posts.** We did not open Brian Crecente's post or Character.AI's reply on X. Their words come from Business Insider, Decrypt and the Daily Dot.
- **Who found the bot first.** The Post and Business Insider say Drew, by Google alert. Decrypt says Brian. We follow the Post and Business Insider.
- **How Drew reported it.** Business Insider says a support form; the Post says email. Possibly both.
- **The chat count.** Business Insider says at least 69 at discovery; the Daily Dot says 69 in total before removal.
- **Whether the creator's account was suspended.** Decrypt says it "appeared" to be. No company statement we opened confirms it.
- **Whether the company ever contacted the family, blocked re-creation, or faced legal action.** No opened source says. Drew said he was considering legal options.
- **AdWeek.** Futurism says AdWeek first reported the story. We did not open it.
- **Search summaries.** Search results summarized reports from Forbes Australia, Forbes Czech Republic, UNB, Digit, Analytics India Magazine, Newser and others. We did not use any fact seen only there. We opened The Business Standard (TBS News) syndication and the Newser text on the AI Incident Database (report 4178) but did not rely on them.
- **The Google deal figure.** Business Insider says $2.7 billion; the Post says $2.5 billion. Left out of the body.

## Sources

| URL | Publisher (author) | Date | Opened |
|---|---|---|---|
| https://www.businessinsider.com/girl-murdered-jennifer-ann-crecente-character-ai-chatbot-artificial-intelligence-2024-10 | Business Insider (Matthew Loh) | 2024-10-08 | Yes, 2026-10-24, raw HTML read as text; quotes checked word for word |
| https://decrypt.co/284377/chatbot-teenage-murder-victim-trouble-character-ai | Decrypt (Jason Nelson) | 2024-10-02 | Yes, 2026-10-24, raw HTML read as text; quotes checked word for word |
| https://futurism.com/murdered-daughter-brought-back-as-ai | Futurism (Maggie Harrison Dupré) | 2024-10-19 | Yes, 2026-10-24, raw HTML read as text |
| https://www.washingtonpost.com/nation/2024/10/15/murdered-daughter-ai-chatbot-crecente/ | The Washington Post (byline not confirmed), read via https://incidentdatabase.ai/reports/4175 | 2024-10-15 | Copy only: the Post's site did not download; the AI Incident Database full-text copy was read as raw HTML on 2026-10-24; quotes checked against that copy |
| https://www.dailydot.com/debug/character-ai-murdered-girl-no-consent/ | Daily Dot (byline not confirmed), read via https://incidentdatabase.ai/reports/4179 | 2024 (day not confirmed) | Copy only: the Daily Dot URL returned HTTP 404; the AI Incident Database full-text copy was read as raw HTML on 2026-10-24; quotes checked against that copy |

## Corrections

If you are a member of the Crecente family or Character.AI and something here is wrong, or if you have the original posts, the Post's byline or a later company statement, tell us and we will fix this page.
