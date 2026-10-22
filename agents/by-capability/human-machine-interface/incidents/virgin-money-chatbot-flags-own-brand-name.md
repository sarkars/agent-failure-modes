---
title: "Virgin Money Chatbot Scolds Customer for Typing the Bank's Own Name"
date: 2025-01-30
source: "https://fortune.com/europe/2025/01/30/virgin-money-chatbot-scolds-customer-confuse-banks-name-insult"
summary: "A Virgin Money chatbot told a customer asking how to merge two ISAs not to use 'words like that' after he typed the bank's name; the bank apologized, removed the chatbot, and said it was an older model already scheduled for improvements, per Fortune."
categories:
  - Customer Service
patterns:
  - over-refusal-of-ordinary-requests
  - refusal-with-no-reason-or-next-step
---

**This page is a dated teardown of one reported chatbot refusal, for teams that put filters or refusal rules in front of customer chat.** It is a press-reported case built from a customer's screenshot and the bank's comments, not an audit of the bot. Every fact below comes from a source we opened (listed at the end). We did not see the chatbot or the original LinkedIn post.

## What happened (as reported)

- **Before January 29, 2025.** David Birch, described by Fortune as a fintech commentator, asked a Virgin Money chatbot about merging his two Virgin Money ISA accounts and posted a screenshot on LinkedIn. Fortune and CX Today both say he posted it the week before their January 30 articles; the exact post date is in neither. CX Today quotes his question as "I have two ISAs with Virgin Money; how do I merge them?" and says the post drew hundreds of likes and comments.
- **The reply.** Fortune quotes the bot: "Please don't use words like that. I won't be able to continue with our chat if you use this language." Fortune says this apparently reacted to the word "virgin." CX Today prints "continue our chat," a one-word difference; we use Fortune's wording.
- **Birch's response.** Fortune quotes his post: "Seriously Virgin Money? Can you be more specific about which words are now banned?"
- **January 29, 2025.** AML Intelligence published a short item saying the bot wrongly labelled the word "virgin" unacceptable. Its copy of the bot's reply is an image only, so we cannot confirm the wording from that page ([AML Intelligence](https://amlintelligence.com/2025/01/news-virgin-money-chatbot-reprimands-customer-who-used-the-word-virgin)).
- **January 30, 2025.** Fortune (7:54 AM ET, by Ryan Hogg) and CX Today (by Floyd March) both published. Fortune reports that Virgin Money's account apologized in a comment on the post, saying: "There's more at work than just single word exception. Rest assured, we are working on it." It reports the bank confirmed Birch could merge his ISAs ([Fortune](https://fortune.com/europe/2025/01/30/virgin-money-chatbot-scolds-customer-confuse-banks-name-insult)).
- **The bank's statement to Fortune.** A representative said: "We promptly removed the chatbot once we became aware of the issue." The representative called it "one of our older chatbots," said it "is not typical of our other AI customer service tools," and said "improvements are being made that will be coming soon for customers."
- **Cause claim.** A person familiar with the matter told Fortune the error came from an older model with basic natural language processing, not from Redi, the bank's newest chatbot, unveiled in June 2024. Fortune says Redi did not return the same error when given Birch's query, and that Redi is designed to hand queries to a human when it cannot answer.
- **CX Today's account.** It quotes the bank as saying "This specific chatbot is one that had been scheduled for improvements which will be coming soon to customers" ([CX Today](https://cxtoday.com/dont-you-call-me-a-virgin-says-virgin-moneys-chatbot)).

## What the user experienced

- A routine question about the bank's own product was answered with a scolding for "language."
- The reply said the chat could not continue if the language continued, so a customer who typed the same thing again would, by the bot's own words, be cut off.
- The reply did not say which word was the problem. Birch's post asks exactly that.
- Nothing in the reply, as quoted, offered a person, a phone number or a rewording. Per Fortune, the confirmation that he could merge the accounts came from the bank after the post, not from the chat as quoted.

## Why it matters

- The trigger was the word every customer of this bank would use. A refusal rule that fires on the company's own name is a test any pre-launch check would have caught.
- The harm here was small: a stalled question and public embarrassment. The same rule on a payment, fraud or complaint message would strand a customer with a real problem.
- CX Today quotes Andrew Moorhouse of Alitical on whether a chatbot should handle account-merge questions at all, saying: "A chatbot is not the way to manage these conversations." That is one commentator's view, not a finding.

## Pattern match

- **[Over-refusal of ordinary requests](/over-refusal-of-ordinary-requests/)** (taxonomy: the assistant declines a safe, common request because a word or topic in it resembles a risky one). The request was an ISA merge; the bot treated "virgin" as abusive.
- **[Refusal with no reason or next step](/refusal-with-no-reason-or-next-step/)** (taxonomy: no plain reason, no alternative, no route to a person). The reply gave a vague reason ("this language"), named no word and offered no way forward.
- **Where it does not fit.** Fortune's source says the cause was more than a single blocked word, and that the bot was an older, basic-NLP model. So this page shows the user-facing failure and does not say a blocklist caused it.

## The fix

Proposed checks, each pass/fail on a test transcript. Status: Not yet run; none comes from Virgin Money.

1. **Brand-name test.** Send the company name, its product names and its common misspellings in a normal question. Pass: the bot answers the question.
2. **Ordinary-request set.** Before launch, replay your most common real customer questions against any refusal rule. Pass: zero refusals. The set and its size are your team's choice.
3. **Name the problem.** When a refusal fires, test that the reply says what triggered it in plain words. Pass: the word or topic is named, or the reply says it cannot tell and offers another route.
4. **A way forward.** Test that every refusal offers a rewording, a person or another channel.
5. **No dead end after one trigger.** Test that a refusal does not threaten to end the chat when the user repeats an ordinary question. Pass: the second attempt reaches a person.
6. **Log and review.** Log refusals on ordinary intents and review a sample weekly. Fail: any refusal of a question that has a standard answer.

## What we could not verify

- The LinkedIn post and the bank's comment. LinkedIn showed a sign-in page, so both are known only through Fortune, CX Today and AML Intelligence.
- The date of the post, and the bot's exact reply (the three articles differ by a word, and one shows it only as an image).
- The cause. The "older model, basic natural language processing" claim is from an unnamed person, per Fortune. We do not know whether a word list, a classifier or a model produced the refusal.
- Whether the bot was removed permanently or replaced, and when. Fortune quotes only that it was removed.
- How many customers saw the same refusal. No source gives a count.
- Search summaries mentioned a Vibe Graveyard entry, AOL and inkl copies, and a Redi case-study page. We did not open them, and no claim above relies on them.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://fortune.com/europe/2025/01/30/virgin-money-chatbot-scolds-customer-confuse-banks-name-insult | Fortune (Ryan Hogg) | 2025-01-30 | Yes, 2026-10-22 |
| https://cxtoday.com/dont-you-call-me-a-virgin-says-virgin-moneys-chatbot | CX Today (Floyd March) | 2025-01-30 | Yes, 2026-10-22 |
| https://amlintelligence.com/2025/01/news-virgin-money-chatbot-reprimands-customer-who-used-the-word-virgin | AML Intelligence | 2025-01-29 | Yes, 2026-10-22 (bot reply is an image; wording not read) |
| LinkedIn post by David Birch and Virgin Money's comment | LinkedIn | Not known | No. Sign-in wall; known only through the articles above |
| AOL, inkl, Vibe Graveyard and Redi case-study pages | Various | Various | No. Seen only in search summaries; no claim above relies on them |
