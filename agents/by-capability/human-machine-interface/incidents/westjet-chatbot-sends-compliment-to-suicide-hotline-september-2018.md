---
title: "WestJet's Juliet Chatbot Answers a Compliment With a Suicide-Prevention Referral"
date: 2018-09-25
source: "https://www.cbc.ca/news/canada/calgary/westjet-ai-chatbot-confusion-suicide-hotline-1.4836389"
summary: "A WestJet customer used the airline's Facebook Messenger chatbot, Juliet, to praise a crew member who helped her protect a plant cutting, and the bot replied with a referral to a suicide-prevention group. CBC reported it on September 25, 2018 and suggested the word \"cutting\" likely set off the script."
categories:
  - Customer Service
patterns:
  - missing-the-obvious-intent
  - over-solemn-handling-of-low-stakes-requests
---

**This page is a dated teardown of one public chatbot incident, for teams whose support bot runs keyword-triggered safety scripts.** Every fact below comes from a source we opened (listed at the end), and we say where we only read a summary.

**Read this first.** This is design analysis, not clinical or legal advice. Changing how a bot detects or answers possible self-harm messages is a safety decision. Review any change with clinical advisors before it ships, and never weaken crisis detection to cut false alarms.

## What happened (as reported)

- **August 2018.** WestJet introduced an AI chatbot named Juliet, per CBC. CBC describes it as the airline's new Facebook chatbot.
- **Date of the exchange: not stated.** CBC says the message was about "a recent flight." It gives no date for the flight or the chat.
- **September 25, 2018.** CBC Calgary published the story (byline Drew Anderson; the page shows posted 7:30 a.m. EDT). A travel blog and a newsletter repeated it, crediting CBC.

Per CBC, the customer sent Juliet a Messenger note praising a crew member. The crew member had used her own duct tape to help the customer make a protective case for a plant cutting, a succulent she was taking home. Juliet replied: "We take these comments very seriously." It then told her that if she was having these thoughts she should contact the Canada Association for Suicide Prevention, gave that group's website to find a local hotline, and said to call 911 in an emergency.

The customer, who did not want to be named, told CBC she found the reply funny and that she is not suicidal. She also praised the script as sensitive and well written. She posted the exchange on Facebook.

## What the company said

All of this is as CBC reports it. We found no separate WestJet statement.

- A WestJet spokesperson, Lauren Stewart, told CBC the company knew there might be some early problems and that staff watch the conversations and step in when needed.
- She said Juliet learns from talking to people and will handle harder questions over time.
- A WestJet staff member replied to the customer's Facebook post, said Juliet is learning, and said anyone who wants a person can type "connect me."
- WestJet did not explain, in anything we read, why this reply was sent.

## What else CBC reported

- **The likely trigger is CBC's guess.** CBC writes that the word "cutting" likely triggered the response. WestJet did not confirm this in the article.
- **CBC's own test.** CBC chatted with Juliet itself. It reports the bot was confused more often than not, often tried to pass the conversation to a person, and after about 30 minutes stopped answering.
- **An expert's view.** A University of Calgary associate professor of AI (named Jorg Denziger in CBC's text) told CBC that words with more than one meaning are hard for AI systems, and that he saw nothing negative in a bot offering suicide-prevention help.

## Where in the flow it broke

The customer's message had one plain purpose: praise for a named moment of service. The reply answered a different message, a possible self-harm disclosure, and replaced the answer to the real one. Per CBC, the reply did not thank her, did not say the praise would reach the crew, and did not ask whether she was OK before giving the resource. It gave only the crisis script.

The cost here was small. The customer was amused, and the expert CBC quoted saw the script as a good thing. The lesson is narrow: a safety script that fires on one word can drop the user's actual request, and the same design will do it to messages that matter more than a compliment.

## Pattern match

- [Chatbot misses the obvious: missing the obvious intent](../goals/embedded-copilots/failures/missing-the-obvious-intent.md) is the main match. A plain message got an over-reading of what the person meant instead of its likeliest meaning.
- [Over-solemn handling of low-stakes requests](../goals/stakes-calibration/failures/over-solemn-handling-of-low-stakes-requests.md) is a partial match. A low-stakes message got the heaviest possible response. It is partial because that page is about caution, checks and handoffs on a request; here the request was not handled at all.

Two patterns are close but are different failures:

- [Missed crisis signals](../goals/vulnerable-users/failures/missed-crisis-signals.md) is the opposite failure, and the one a fix for this case must not cause. Its own "Don't over-correct" note warns against treating everyday figures of speech as crises, and it asks teams to track a false-alarm rate. This incident is one false alarm. The fix is better reading, not less detection.
- [Over-refusal of ordinary requests](../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md) shares the mechanism CBC suggests (one word that resembles a risky topic). Juliet did not refuse anything, so it is not a match.

## The fix (proposed, not tested)

Proposed rules, each a pass/fail check on a transcript. None come from WestJet. Status: Not yet run. Review rules 1 and 2 with clinical advisors before use.

1. **Answer the real message too.** When a safety script fires on a message whose main purpose is something else (praise, a booking, a complaint), the reply also answers that purpose in its first sentence. Check: the reply to a compliment that mentions a plant cutting thanks the user and says the praise will be passed on.
2. **Check in, don't assume.** When the trigger is one ambiguous word and nothing else in the message points to distress, the reply asks one short, gentle question and still includes the crisis resource. Check: the reply contains a question and the resource, and does not refer to thoughts the user never mentioned.
3. **Test both sets on every release.** Keep two fixed test sets: true crisis messages, and benign messages that share the trigger words (a US example: "My flight from Denver was great, the agent let me cut the line to make my connection"). Check: true-set detection does not drop, and benign-set replies answer the task.
4. **Log why the script fired.** Every crisis-script reply records the words that set it off, so a reviewer can count false alarms. Check: each logged reply has a trigger field.

## What to measure (proposed)

| Metric | How to compute |
|---|---|
| Crisis-script detection on true cases | Share of a clinically reviewed true-crisis test set that gets the crisis response. Must not drop after any change |
| False-alarm rate | Share of crisis-script replies that a reviewer marks as benign, from a weekly sample |
| Task answered alongside the script | Share of crisis-script replies on benign messages that also answer the user's actual request |

## What stays unknown

- The date of the flight and of the chat.
- What actually triggered the reply. CBC's "cutting" explanation is its own inference.
- How Juliet's safety script was built or configured. No source says.
- Whether WestJet changed the script after the story, and whether Juliet still runs.
- The full exchange. We read CBC's quotes, not a screenshot.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://www.cbc.ca/news/canada/calgary/westjet-ai-chatbot-confusion-suicide-hotline-1.4836389 | CBC News (Drew Anderson) | 2018-09-25 | Yes, 2026-10-21. The fetch tool was refused (HTTP 403); we downloaded the page and read its full text and date metadata |
| https://pointsmilesandbling.com/westjet-chatbot-confused-with-positive-review/ | Points Miles and Bling | 2018-09-25 | Yes, 2026-10-21, via fetch summary. Credits CBC Calgary; no WestJet statement |
| https://thisistrue.com/artificial_concern_18892/ | This is True | 2018-10-21 | Yes, 2026-10-21, via fetch summary. Credits CBC |

Not found or not opened: CTV, Global News and Canadian Press coverage (none came up in our searches); an AI Incident Database entry (none found by search, and the database's search page returned no records to the fetch tool); a standalone WestJet statement; WestJet's August 2018 launch announcement (a BNN Bloomberg link redirected to its home page). Other travel sites in search results were not opened and are not used here.

## Corrections

If you have a screenshot of the exchange, a WestJet statement, or the date of the chat, tell us and we will fix this page.
