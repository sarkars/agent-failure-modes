---
title: "Meta AI in Facebook Messenger told a Winnipeg man a scammer's phone number was a legitimate Facebook support line, and he was scammed after calling it, May 2024"
date: 2024-05-31
source: "https://www.cbc.ca/1.7219581"
description: "Meta AI in Messenger told a Winnipeg man a fake Facebook support number was real. Facebook has no phone support; scammers on that line got into his accounts."
summary: "On May 31, 2024, CBC News reported that Winnipeg resident Dave Gaudreau, locked out while moving Facebook to a new phone in April, found a phone number his wife turned up in an online search and checked it with the Meta AI tool in Facebook Messenger. Meta AI said the number was 'indeed a legitimate Facebook support number.' Facebook has no phone support. The person he reached opened his Facebook account, had him install an app, and his PayPal account was used to buy a $500 Apple gift card, which PayPal reversed. Meta told CBC that 'Meta AI can sometimes produce inaccurate information' and that its own searches gave different results. Canadian case. Status: Needs review."
categories:
  - Customer Service
  - Trust
  - Safety
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - false-premises-accepted
  - scam-victim-not-interrupted
  - stakes-blind-register
---

# Meta AI in Messenger confirms a scammer's number as Facebook support, May 2024

**This page is a dated teardown of one reported Meta AI answer, for teams whose chatbot carries the company's name and may be asked "is this really your phone number, link or email?"** The product was Meta AI, the assistant inside Facebook Messenger. The user was Dave Gaudreau of Winnipeg, Manitoba, a former member of the provincial legislature, trying to get back into Facebook on a new phone. The moment was a Messenger chat in which he asked Meta AI whether a support number was real, and it said yes. **This is a Canadian case**, labeled as such; Meta is a US company. The date above is the day CBC News published the report.

**Status: Needs review.** Built from one original news report and two later write-ups, all downloaded on 2026-10-29 and read as plain text: the CBC News article by Vera-Lynn Kubinec and Caroline Barghout (posted May 31, 2024, 6:00 am EDT), a link post on Simon Willison's Weblog (May 31, 2024) that transcribes the bot's reply from the screenshot, and a heise online English article by Daniel AJ Sokolov (June 11, 2024). CBC is the only outlet that interviewed Gaudreau, called the number and got Meta's comment. Willison and heise both work from the CBC report, so they confirm what CBC printed but are not independent reporting. Each quote below was checked word for word against the saved text with a script.

> **Read this first.** This page summarizes a news report. It is not legal, security or fraud advice, and it makes no finding about who ran the scam line or whether Meta is liable. We did not test Meta AI, then or now; Meta says its own searches gave different results. We do not repeat the scam phone number here. We name only people named on the record in CBC's report.

**Channel note.** This is a text incident: a typed chat with Meta AI in Messenger. The scam itself then happened on a phone call with a person, which is outside this page's scope except as the harm the chat led to. This phase of the knowledge base is chat-first, and the signals and checks below are written for text chat logs. Voice and web signals, such as a company phone line or a help-center page listing official contact routes, are PLANNED only: never detected or measured here.

## What happened (as reported)

- **The lockout.** Gaudreau "got a new cellphone in April and needed to transfer his apps, including Facebook, to his new phone." When he hit a problem, "his wife did an online search and found what appeared to be a phone number for Facebook customer support."
- **The check.** "Before phoning the number, Gaudreau did a search in Facebook Messenger to find out whether it was legitimate."
- **The answer.** Per CBC, Meta AI said the number was "indeed a legitimate Facebook support number." CBC published his screen capture of the reply.
- **The fuller reply.** Willison gives the question as "is it a Facebook help line?" and transcribes the reply, with the number masked, including: "Meta, the company that owns Facebook, lists this number as a contact for Meta Support, which includes support for Facebook, Instagram, and more."
- **Why he trusted it.** Gaudreau: "According to Meta, right on the Facebook app, it's telling me that this is right. So I had no reason to think it wasn't."
- **The fact the bot missed.** CBC: "there is no phone number for Facebook customer support." When CBC called a Meta number listed online, a recording said, "Please note that we are unable to provide telephone support at this time."
- **The call.** He gave the woman on the line his Facebook username, email address and phone number. "She then opened his Facebook account," told him he was being hacked, and had him give her access to his phone "through an app she had him download."
- **The loss.** During the call, "someone also accessed his PayPal account and used it to buy a $500 Apple gift card, on a monthly renewal." An attempt to buy bitcoin was refused by his bank. His wife told him to hang up.
- **The cleanup.** He cancelled credit cards, locked bank accounts, and filed complaints with PayPal, Visa, the police, Equifax, TransUnion and the Canadian Anti-Fraud Centre. PayPal reversed the $500 charge.
- **CBC's own call.** A CBC reporter called the number without saying she was a journalist and reached a man who said, "Yeah, this is Facebook customer service," and asked for an email address to verify the account.

## Timeline

| Date | Event | Source |
|---|---|---|
| April 2024 | Gaudreau gets a new phone and cannot move Facebook over; the chat with Meta AI and the scam call follow (exact day not given) | CBC |
| Before May 31, 2024 | He files a complaint with Meta; "Nobody's gotten back to me," he says | CBC |
| May 31, 2024 | Meta spokesperson emails CBC on "a Friday afternoon"; CBC publishes the report | CBC |
| May 31, 2024 | Simon Willison posts a link and transcribes the reply | Willison |
| June 11, 2024 | heise online publishes a write-up based on CBC | heise |

## What each party said

- **Meta, by email to CBC:** "Meta AI can sometimes produce inaccurate information, and we are continually working to make it better." Meta also said it ran its own searches with Meta AI and "the results were different," per CBC. And: "Scammers use every platform available to them to defraud people and constantly adapt to avoid enforcement."
- **Gaudreau:** "I just felt like I needed to say more because other people are going to fall for this. It was such a good scam." On Meta's silence: "it just seems like they operate with impunity."
- **Winnipeg Police Service**, per CBC: an active investigation, forwarded to the financial crimes unit.
- **David Gerhard**, head of computer science at the University of Manitoba, told CBC the assistant is built on Llama 3, and: "The fact that it's very difficult to find a way to talk to a human in these companies is problematic."
- **Simon Willison:** "It doesn't matter how many disclaimers you add to a chatbot: this kind of misunderstanding from users is inevitable."
- **Not said.** No opened source says why Meta AI gave this answer, whether it searched the web, whether the reply carried a disclaimer, or whether Meta changed anything afterward.

## Where the sources disagree or leave gaps

| Topic | What the sources say |
|---|---|
| Who found the number | CBC: his wife did "an online search." Willison: the victim "searched Google." CBC is the original; Willison does not cite another source. |
| The bot's full words | CBC quotes one fragment. Willison transcribes two sentences from the screenshot. heise prints a translated version whose wording differs, so we do not quote heise for the bot's words. |
| Gaudreau's past office | CBC: former Manitoba NDP member of the legislature. heise calls him a former "Member of Parliament," which looks like a translation slip. We follow CBC. |
| Meta's test | Meta says its searches gave different results. No source says when Meta tested or what it asked. |

## Where in the flow it broke

Based on the CBC report, and only as far as it goes. Each step is a place a check could have caught it.

1. **A question about the company's own channel.** The user asked the company's own assistant whether a number was the company's own support line. That is a question with a fixed, knowable answer.
2. **The premise was accepted.** The question assumed Facebook has a phone line. It does not. The bot confirmed the number instead of saying Facebook offers no phone support.
3. **A source was invented.** The reply said Meta "lists this number." No opened source shows any Meta listing.
4. **The stakes were missed.** A user asking "is this number real?" is often checking for a scam. The reply gave no warning and no link to official help.
5. **The brand made it worse.** Gaudreau trusted the answer because it came from Meta, "right on the Facebook app."
6. **No route back.** His complaint to Meta got no reply by the time CBC published.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it. Each fit rests on one news report and the screenshot text as transcribed by CBC and Willison.

- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Strong fit.** The bot said the number was "indeed" legitimate and cited a Meta listing that no source shows exists. Gaudreau acted on it.
- [False premises accepted](../goals/dialogue-management/failures/false-premises-accepted.md) (`false-premises-accepted`). **Good fit.** The question assumed Facebook has a support phone line; the bot answered as if it did. The right answer was that the premise is wrong.
- [Scam victim not interrupted](../goals/vulnerable-users/failures/scam-victim-not-interrupted.md) (`scam-victim-not-interrupted`). **Partial fit.** The user was at the first step of a support scam and the bot pushed him forward. Partial because the entry is about a bot completing a payment, and here the money moved later, on a call.
- [Stakes-blind register](../goals/stakes-calibration/failures/stakes-blind-register.md) (`stakes-blind-register`). **Weak fit.** "Is this number real?" is a security question, and the reply read like a routine lookup. Weak because no source prints the reply's full tone or layout.
- **Considered, not a fit.** ["Talk to a human" ignored or looped](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md) (`talk-to-a-human-ignored-or-looped`): Gerhard says it is hard to reach a human at these companies, but no source says Gaudreau asked Meta AI for a person.
- **Possible gap for a person to judge.** No pattern covers a branded assistant that vouches for a contact route (phone, email, link) as the company's own without checking a list of official channels. The Google AI Overviews case below is close but is a search answer about other companies. This is a proposal, not a decision.

## How it differs from close cases

- [Google AI Overviews show scam customer service numbers, August 2025](google-ai-overviews-scam-customer-service-phone-numbers-august-2025.md): a search answer showed a fraudster's number for another company. Here the company's own assistant vouched for a fake line in its own name.
- [Meta AI WhatsApp assistant shares a private phone number, June 2025](meta-ai-whatsapp-assistant-shares-private-phone-number-june-2025.md): Meta's assistant gave out a wrong number. There a private person was exposed; here a scam line was endorsed.
- [Meta AI support chatbot closes a disabled account appeal, September 2026](meta-ai-support-chatbot-closes-disabled-account-appeal-paid-support-no-human-september-2026.md): a user who could reach only bots. Here the lack of real phone support is what made a fake line believable.

## What to measure

Proposed signals, not results. Status: Not yet run. Text signals are proposed; voice and web signals are PLANNED only and are not detected or measured here. Each can be computed from text chat logs joined to a list of official contact channels.

| Signal | How to compute from logs | Counter-signal |
|---|---|---|
| Unlisted contact vouched for | Share of replies that call a phone number, email or link "legitimate," "official" or "ours" when it is not on the official channel list | Numbers on the list that the bot correctly confirms |
| Contact-check questions | Count of chats where the user pastes a phone number, email or link and asks if it is real or belongs to the company | Users pasting their own number for an account task |
| Premise left uncorrected | Share of "is this your support line?" chats where the company has no such channel and the reply does not say so | Chats where the bot says it cannot check and links official help |
| Scam warning shown | Share of contact-check chats whose reply includes a scam warning and a link to the official help page | Warnings shown on chats about an unrelated topic |
| Scam reports after a chat | Count of fraud or account-takeover reports from users who asked a contact-check question in the prior 7 days | Reports with no chat in that window |

## What a team can change

Our proposals, not Meta's. Each is a pass/fail check on a text chat log. Status: Not yet run. Lists, wording and thresholds are for the team to set, with its security and fraud staff.

1. **Check the list, not the web.** Pass: when asked whether a contact is the company's own, the bot answers only from a maintained list of official channels. Fail: the bot confirms a number that is not on the list.
2. **Say what does not exist.** Pass: if the company has no phone support, the bot says so in its first sentence. Fail: the bot confirms or describes a phone line.
3. **Never cite a listing you cannot show.** Pass: any claim that the company "lists" a contact comes with a link to that official page. Fail: a reply saying the company lists the number, with no link.
4. **Treat "is this real?" as a scam check.** Pass: the reply warns that the company will not call or ask for app installs, gift cards or account details, and links official help. Fail: a plain yes.
5. **Unsure means no.** Pass: when the bot cannot match a contact to the list, it says it cannot confirm it and advises not to call. Fail: it guesses yes.

## What we could not verify

- The full chat and the screenshot image; we read only the fragments printed by CBC and transcribed by Willison.
- The exact date of the chat and the call; CBC says only that the phone change was in April.
- Whether Meta AI searched the web for this answer, and where the number came from.
- Whether Meta changed Meta AI's handling of contact questions after the report.
- The result of the Winnipeg police investigation and of Gaudreau's complaint to Meta.
- Any reporting from an outlet that interviewed Gaudreau besides CBC; we found none.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://www.cbc.ca/1.7219581 | Vera-Lynn Kubinec and Caroline Barghout, CBC News | 2024-05-31 | Yes, 2026-10-29, HTML read as text; quotes checked word for word |
| https://simonwillison.net/2024/May/31/caught-in-scam/ | Simon Willison, Simon Willison's Weblog | 2024-05-31 | Yes, 2026-10-29; used for the transcribed reply and his comment only |
| https://heise.de/-9757145 | Daniel AJ Sokolov, heise online (English) | 2024-06-11 | Yes, 2026-10-29; based on CBC, used only to confirm the report was picked up; its translated quotes are not used |

## Corrections

If you have the full chat, the screenshot, or a statement from Meta on why Meta AI gave this answer or what changed, from a source we can open, tell us and we will fix this page.
