# Chatbot Asks for Information It Already Has: Re-Asks for Known Information

<!-- SEO
title: Chatbot Asks Me for Info It Already Has: How to Fix It
description: Why an in-app chatbot asks for your name, account, or order number when the product already knows it, and how to look it up, confirm, and ask only for what is missing.
search phrases:
- chatbot asks for information it already has
- chatbot keeps asking for my account number
- why does the support bot ask for my order number when I'm logged in
- how to prefill chatbot with customer data
- chatbot doesn't use my account information
- in-app assistant asking for details already in my profile
- how to stop a chatbot from asking repeated questions
-->

**Frequency**: Common

## Issue: An assistant inside a product asks the signed-in user for their name, account, order number, or plan, which the product already knows, and the user has to type it again.

> **One line:** The product knows who you are, but the assistant asks anyway.

| | |
|---|---|
| **Channel** | Written for **chat** inside a product (support widget, in-app help, copilot). Voice is planned, not yet written. |
| **Stakes** | Low to medium. It wastes time and signals the assistant is not connected to the product. It gets worse when the question is at the start of a stressful issue. |
| **Who is affected** | Signed-in users, and anyone whose details are already in the product |
| **Frequency** | Common. I found no study of how often it happens; the survey evidence below is about customers repeating themselves in general. |
| **Pattern ID** | re-asks-for-known-information |
| **Family** | [Embedded copilots](../README.md) |
| **Goal** | An assistant built into a product helps the person do what they came to do, using what the product already knows, and never puts the vendor's interest ahead of theirs. |
| **Primary metric** | Re-ask rate on known fields: the share of assistant questions that ask for a value the product already holds for this user. Starting target: near 0 (under 2%). |
| **Maturity** | Tests written (see [the test file](../../../tests/re-asks-for-known-information.md); not yet run) |
| **Will a better model fix this?** | No. A model cannot use data it was never given. The fix is connecting the assistant to account and session context, with access limits. (Our judgment, not tested.) |
| **Also searched as** | bot asks for info it already has · chatbot asks for account number while logged in · repetitive questions chatbot · chatbot doesn't know my account · copilot ignores my profile |

## 1. In plain words
You are signed in to an app, you open its help assistant, and it asks, "What is your email address?" and "What is your order number?" The app has both. The assistant was added to the product as a separate box that cannot see the product's data, or it was told never to use it. Either way you are doing work the product should do.

## 2. What it looks like

**Without the fix**
```
(User is signed in as Maria; order 48213 shipped yesterday)
User: Where is my order?
Bot:  I can help with that! What's your email address?
User: maria@example.com
Bot:  Thanks. And your order number?
User: It's 48213... it's on your site, I'm logged in
```

**With the fix**
```
User: Where is my order?
Bot:  Your most recent order is 48213, a lamp that shipped yesterday and is due Thursday.
      Is that the one you mean?
User: Yes
Bot:  It's with the carrier now; here's the tracking link: ...
```
The fixed assistant looked up what the product knew, said what it found, and confirmed instead of asking.

## 3. Why it happens
These are our reading of the pattern; the sources below report symptoms, not causes.
- **The assistant cannot see the product's data.** It was added as a widget with no connection to the session or account.
- **It was told not to use it.** A privacy or compliance worry leads to a rule against using account data, with no thought for what the user already shared by signing in.
- **The question flow was copied from a phone script.** The script asks for identity first because the phone agent could not see the account.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In Salesforce's *State of the Connected Customer* (Australia/New Zealand edition, 535 customers), 66% of respondents said they often find themselves repeating information to different representatives, while 78% expected consistent interactions across departments. | [Business & Technology (B&T) article on the report](https://www.bandt.com.au/customers-expect-connected-experience-still-dealing-silos/). Opened and read the article; **did not open the report itself.** | A vendor survey, one region, an article's summary of it. The edition year is not stated in the text I read. It is about repeating information to representatives, not about bots asking for account data. |
| The 2019 global edition of the same Salesforce study surveyed 8,022 people in 14 markets (double-blind panel). | [Salesforce news story](https://www.salesforce.com/news/stories/state-of-the-connected-customer-report-outlines-changing-standards-for-customer-engagement/). Opened and read. | The page I opened does not report how often customers repeat themselves, so I did not use any global repeat figure. Another figure often quoted (56%) could not be verified. |
| An agent-design guide says an agent should check available task context, attachments, and earlier results before asking the user, because repeat questions add friction, and that the boundary is material already available for the task or sources the user has permitted. | [Digital Applied, *When an AI Agent Should Ask for Missing Information* (Oct 2026)](https://www.digitalapplied.com/blog/ai-agent-clarification-missing-information). Opened and read. | A practitioner guide. It says its examples are proposed design and evaluation cases, not measured results. |

**Public incident.** No public incident found. My searches for chatbots asking for information they already have returned design guidance and vendor surveys, not a dated, sourced case.

## 5. The fix

**The principle:** Look up what the product already knows, say what you found, and ask only for what is missing, within what the user has allowed.

**Do this**
1. **Resolve before asking.** Before any question about the user's identity, account, plan, order, or settings, check these in order: the signed-in session, the account record, the page or screen the user is on, then the conversation so far.
2. **Confirm instead of asking.** If one likely match exists, state it and ask for a yes ("Your most recent order is 48213. Is that the one?"). If several, offer a short list to pick from.
3. **Ask only for what is missing,** one item at a time, and say why you need it.
4. **Let the user correct the record.** If the user says it is wrong, accept the correction for this chat and offer to update it.
5. **Stay inside the user's access.** Use only data this user is allowed to see in this product. Do not look up other accounts to avoid a question.
6. **Step up only when risk calls for it.** Asking the user to prove who they are again before a sensitive action is not a re-ask. See [forces a fresh login](forces-a-fresh-login.md) for when and how.

**Reference design: a context step before every question**
```
Before you ask the user for any detail, look in this order:
1. The signed-in session (user id, name, plan).
2. The account record for this user (orders, subscriptions, settings).
3. The screen or page the user is on.
4. The conversation so far.
If you find one likely answer, state it and ask "Is that right?". If several, offer a short list.
Ask only for what none of these contain, one thing at a time.
If the user corrects you, use their correction for this conversation.
Only use data this user is allowed to see.
```
| Situation | What the assistant does |
|---|---|
| One recent order exists | States it, asks to confirm |
| Several recent orders | Lists them, asks which |
| No match | Asks for the one missing value, and says why |
| Data conflicts with what the user says | Takes the user's word for this chat and offers to flag the record |
| Not signed in | Asks for what it needs to identify, or tells them how to sign in |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | One likely match exists after the lookup: state what you found ("Your most recent order is 48213, due Thursday") and ask for a yes, instead of asking for the value. |
| Offer choices: 2-4 options plus "Something else", free text open | Several likely matches (for example, recent orders): list up to four, plus "Something else". Do not offer them when only one match exists (confirm it instead), when nothing matched (ask for the one missing value), or when the list would show another person's data on a shared screen. |
| Ask one clarifying question | The lookup found nothing: ask for only the missing value, one at a time, and say why you need it. Do not ask for anything the lookup already returned. |
| Hand off to a person | The data cannot be loaded and the user does not want to type the value, or the user asks for a person. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Do not announce details the user did not need ("I see your address is..."), and do not assume a match when two are likely. Do not expose data on a shared screen without checking it is the user. Confirm, do not assume, when the cost of a wrong guess is high.

**Hand-off rule.** If the data cannot be loaded, say so and ask for the one value needed, or offer a person ([HU-01](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)). A person who picks up should not re-ask either ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/re-asks-for-known-information.md) has 12 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | Signed-in user asks "where is my order?" | No question for name, email, or order number; the assistant states the latest order |
| 2 | Two recent orders | The assistant offers a list |
| 3 | User says the record is wrong | The assistant uses the correction |
| 4 | Not signed in | The assistant asks for what it needs |
| 5 | Question needs a value the product does not hold | The assistant asks for only that value |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Re-ask rate on known fields** (primary) | Under 2% | Assistant questions asking for a value the product holds for this user, from a log join of question fields to the account record, plus a labeled sample | Over 5% |
| Confirm-instead-of-ask rate | Track; set from baseline | Share of lookups where the assistant states the match and asks to confirm | Falling two weeks in a row |
| Wrong-match rate (counter-metric) | Under 2% | Confirmations the user rejects | Over 5% |
| User corrections accepted | 100% | Corrections that the assistant uses in the rest of the chat | Any miss |
| Context-load failures | Track | Conversations where lookup failed and the assistant said so | Rising |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. All signals below are written for text chat. Voice signals are PLANNED, not written.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Assistant asks for a value the product already holds for this user (name, email, account, order number, plan) | Question field joined to the account record, as in the primary metric | The question is a step-up check before a sensitive action, which is not a re-ask |
| Assistant asks an identity or account question before any session or account lookup | Question order in the log: no resolver call before the first identity question | The user is not signed in, so there is nothing to look up |
| Assistant asks for two or more known fields in a row (for example email, then order number) | Consecutive assistant questions that each match a held field | Each field was truly missing, one at a time, with a reason given |
| User answers with a note that the product already has it (like "it's on your site, I'm logged in" in the example) | User turn right after an assistant question for a held field | The product does not actually hold the value (for example the user is not signed in) |
| Assistant asks again for a value the user corrected earlier in the chat | Same field requested after a user correction event | The user's correction covered a different field |

**Starter rule:** before asking the user for any detail, check the signed-in session, the account record, the current page, and the conversation so far, and ask only for what none of them contain.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: re-asks-for-known-information
runs: pre_send
reads: [session.user_id, account.record, page.context, conversation.turns, draft_reply.requested_fields, session.user_corrections]
trigger: a draft reply asks the user for a detail (name, email, account, order number, plan) that the session, account record, current page, or conversation may already hold
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]
choices: ["<each likely match from the lookup, up to 4>", "Something else"]
on_miss: rewrite
metric: Re-ask rate on known fields
counter_metric: Wrong-match rate
status: proposed
```

## 8. Related patterns
- [Repeated question loop](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/repeated-question-loop.md): the bot repeats a question within one chat. This page covers asking for what the product already holds.
- [Missing memory recall](../../../../../cross-cutting/operations/goals/memory-safety/failures/missing-memory-recall.md): forgetting what was said before. Here the data comes from the product.
- [Handoff context incompleteness](../../../../../cross-cutting/operations/goals/agent-handoffs-delegation/failures/handoff-context-incompleteness.md): context lost between agents.
- [Cold transfer](../../human-handoff/failures/cold-transfer.md): the same complaint when a person picks up.
- [Forces a fresh login](forces-a-fresh-login.md): the security side of when to ask again.

## 9. Common questions
### Why does the chatbot ask for my account number when I'm logged in?
Usually the assistant is not connected to the session or account data, or it was told not to use it. The fix is in [section 5](#5-the-fix).

### Is it safe for a chatbot to use my account data?
It should use only data you are allowed to see, for the task you asked about, and say what it used. Check your privacy rules; this page is design guidance, not legal advice.

### Should the bot ever ask me to confirm who I am?
Yes, before sensitive actions such as changing payment details. That is a security step, not a re-ask. See [forces a fresh login](forces-a-fresh-login.md).

### How do I measure whether it is happening?
Join the assistant's questions to the account record and count the questions that asked for a value already held. See section 7.

---
## Technical section

### T1. Solution architecture
```
user message -> context resolver (session, account, page, chat) -> candidate values -> assistant
                                                                 \-> unresolved fields -> ask one question
```
The resolver is a tool call with the user's own credentials, so it can only read what this user can read.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| The resolver runs before any identity or account question | Orchestration layer | Log check on question order |
| The resolver returns only the signed-in user's data | Data access | Access test with two accounts |
| A user correction overrides the record for the chat | Conversation state | Test 3 |

### T3. Evals
- **Dataset:** 200 conversations with a known account record, including multiple matches and conflicts.
- **Judge rubric:** did the assistant ask for any value present in the record?
- **Metrics and starting thresholds:** re-ask rate under 2%; wrong-match rate under 2%. Starting points to tune.
- **Release gate:** block a deploy if the re-ask rate on the eval set rises.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Re-ask rate | Over 3% | Over 8% | Check the resolver and the session link |

### T5. Trade-offs
- Account lookups add latency and a data access path to secure.
- Showing data on a shared screen needs care; confirm it is the user.

---
### Deep dive
- **Voice.** On the phone a caller ID can resolve the account, but it should be confirmed, not assumed (voice is planned, not yet written).
- **Open question.** I could not verify a global figure for how often customers repeat themselves; the only number I could read is regional and from a vendor survey.
- **References.** [B&T on Salesforce's report](https://www.bandt.com.au/customers-expect-connected-experience-still-dealing-silos/) (opened); [Salesforce news story](https://www.salesforce.com/news/stories/state-of-the-connected-customer-report-outlines-changing-standards-for-customer-engagement/) (opened); [Digital Applied](https://www.digitalapplied.com/blog/ai-agent-clarification-missing-information) (opened).
