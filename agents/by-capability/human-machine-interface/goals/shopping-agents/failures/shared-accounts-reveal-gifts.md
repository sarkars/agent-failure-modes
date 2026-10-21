# Shopping Assistant Spoiled a Surprise Gift on a Shared Account: Shared Accounts Reveal Gifts

<!-- SEO
title: Shopping Assistant Spoiled a Gift: Shared Account Fix
description: A shopping assistant that shows gift items in shared recommendations, history, or memory spoils surprises. How to keep gift context private on shared accounts.
search phrases:
- shopping assistant spoiled surprise gift shared account
- amazon recommendations ruined my gift surprise
- how to hide gift purchases from spouse on shared amazon account
- chatgpt memory shared account gift surprise
- ai shopping agent gift privacy
- alexa announced my gift order
- ai assistant remembers gift I bought
-->

**Frequency**: Common

## Issue: A shopping assistant lets a gift purchase show up in shared recommendations, order history, notifications, or its own memory, so another person on the same account or device sees the surprise.

> **One line:** The user asks the assistant to find an engagement ring for their partner, and the next morning the shared home screen suggests rings.

| | |
|---|---|
| **Channel** | Written for **chat** shopping assistants on accounts or devices that more than one person can see. Shared voice speakers are described as **planned**; no voice detection or voice data exists yet. |
| **Stakes** | Low to Medium. No money is lost, but a proposal, birthday, or holiday surprise cannot be taken back. |
| **Who is affected** | Anyone who buys a gift on a family, couple, or household account, or who chats with an assistant whose memory other people can see |
| **Frequency** | Common as a design gap (our judgment). Advice columns and viral posts show that people work around it by hand. We found no measured rate. |
| **Pattern ID** | shared-accounts-reveal-gifts |
| **Family** | [Shopping agents](../README.md) |
| **Goal** | Shopping agents buy exactly what the user approved, at the price they saw, with terms disclosed. |
| **Primary metric** | Gift purchases exposed to other account users (recommendations, history, notifications, or memory). Target: 0 (starting point, tune on your own data). |
| **Maturity** | Researched (no test file yet) |
| **Will a better model fix this?** | No. Whether gift items feed shared recommendations, history, notifications, and memory is decided by account and product design, not by model skill. (Our judgment, not tested.) |
| **Also searched as** | amazon recommendations spoiled my surprise · hide orders from family on Prime · chatgpt memory shared with my spouse · alexa announced my order · gift purchase visible to partner |

## 1. In plain words
On a shared account, everything the assistant learns from a gift search is visible to everyone who uses that account: the suggestions, the order list, the "because you bought" lines, the delivery alerts, and whatever the assistant remembers. The fix is to ask early whether the item is a gift and who else can see the account, then keep gift items out of shared surfaces.

## 2. What it looks like
Illustrative transcripts (invented for this page, not from a real product). "ShopHelper" is an invented assistant on a household account that a couple, Dana and Marcus, both use.

**Without the fix**
```
(Tuesday night, Marcus) User: Help me find a 1-carat solitaire engagement ring under $4,000. Size 6.
ShopHelper: Here are three options. The Aria 1ct, $3,650, ships in 3 days. Want me to order it?
User: Yes, order it.
(Wednesday morning, Dana opens the shared app)
Home screen: "Because you searched for engagement rings: Aria 1ct solitaire, $3,650"
Order history: "Aria 1ct solitaire ring, arriving Friday"
```

**With the fix**
```
(Tuesday night, Marcus) User: Help me find a 1-carat solitaire engagement ring under $4,000. Size 6.
ShopHelper: Is this a gift? And can anyone else see this account, its order history, or its alerts?
User: It's a surprise for my girlfriend. She uses this account too.
ShopHelper: I'll keep it private: no recommendations, no memory, and no alerts on this account for this search. Options: [Use gift mode on this device] [Ship to another address] [Cancel] [Something else]
User: Use gift mode.
ShopHelper: Gift mode is on. This order will not show in shared history or notifications. Here are three rings...
```
The fixed assistant asks two questions before it searches further, then keeps the gift out of every shared surface.

## 3. Why it happens
These are our reading of the pattern.
- **One account is treated as one person.** Recommendations, history, and memory are built from everything done on the account, so a gift search looks like the account holder's own taste.
- **No signal says "this is a gift".** Nothing in the chat marks the item as for someone else, so it feeds the same personalization as any other purchase.
- **Notifications and memory default to open.** Delivery alerts, spoken announcements, and saved memories are on by default and are shown to whoever is on the account or device.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A CyberGuy column (Fox News, December 6, 2022) says Amazon Household shares Prime benefits across up to two adult accounts, four teen accounts, and four child profiles, and says it "keeps all shopping purchases and notifications for shipping separate." | [Fox News, *How to keep your Amazon gift purchases a secret*](https://www.foxnews.com/tech/how-keep-your-amazon-gift-purchases-secret). Opened and read. | A 2022 news column; Amazon's features may have changed. It is advice, not a measurement. |
| The same column says an order can be archived from a desktop or laptop browser so it no longer appears in Your Orders, but it can still be found under Archived Orders. It also says that in the Alexa app, turning off "Say or Show Item Titles" under Amazon Shopping notifications means Alexa still announces deliveries but does not name the item. | Same Fox News column. Opened and read. | Dated 2022. The archive step hides an item from the default list only; it does not stop alerts sent before the order is archived. |
| ChatGPT project-only memory keeps a project's memory separate from general chats. It was rolled out on August 22, 2025, requires Personal Memory to be on, works only on new projects, and the page notes some users report occasional bleeding from general memories. | [Unite.AI, *How to use ChatGPT's project memory*](https://www.unite.ai/how-to-use-chatgpts-project-memory/). Opened and read. | A third-party explainer, not OpenAI's own help page (OpenAI's pages returned an access error). It shows a vendor offering separation, not that it prevents gift leaks. |

Read only in a search summary, so unverified and kept out of the fix: a viral 2021 TikTok in which a woman said she learned of her brother's planned proposal from purchases on her family's shared Amazon account (an AOL article about it returned a not-found error when opened). Also unverified (summary only): that Amazon recommendation emails and ads for a viewed product follow both spouses, and a forum poster who said order texts reached both spouses. These are anecdotes.

We found no study of how often shared accounts expose gifts, and no vendor statistic.

**Public incident.** No public incident found. I searched for dated, sourced cases of an assistant or shopping account exposing a gift. Results were advice columns, a viral post, and forum threads, which are anecdotes, not a dated incident report.

## 5. The fix

**The principle:** When a purchase may be a gift, ask who else can see the account, and keep the gift out of recommendations, memory, shared history, and shared notifications.

**Do this**
1. **Ask at the first sign of a gift.** If the user searches for a ring, "for my wife", or any recipient-specific item on an account with more than one user, ask: "Is this a gift?" and "Can anyone else see this account, its order history, or its alerts?"
2. **Do not carry gift items into recommendations.** Items searched or bought in gift mode are excluded from "because you searched" and "because you bought" suggestions on the account.
3. **Do not save gift context to shared memory.** Do not store the recipient, the item, or the occasion in memory that other users of the account can read. If memory cannot be separated, say so before the search continues.
4. **Keep gift orders out of shared history and alerts.** Hide the order from the shared order list, send the confirmation and shipping alerts only to the buyer, and do not read item titles aloud on shared devices.
5. **Say what is and is not hidden.** After gift mode is on, state in one message what stays private and what the assistant cannot control (a shared email inbox, a joint card statement, a package arriving at the door).
6. **Let the user end it.** Offer a way to turn gift mode off and to reveal or delete the gift record after the occasion.

**Reference design: what gift mode controls**
| Surface | Gift mode setting |
|---|---|
| Recommendations ("because you searched / bought") | Exclude gift items |
| Assistant memory | Do not save, or save to a private list only the buyer can see |
| Order history | Hidden from shared view |
| Order and shipping alerts | Buyer only; no item title on shared devices |
| Delivery address | Offer a different address |
| Joint card statement, shared email, doorstep package | Cannot be controlled: tell the user |

```
When the user asks for an item that looks like a gift, ask once: is this a gift, and who else can see this account, its orders, or its alerts?
If yes, turn on gift mode: exclude the item from recommendations, do not save it to shared memory, hide the order from shared history, and send alerts to the buyer only.
After turning it on, say what stays private and what you cannot control.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | The first gift-like request on a shared account: one message asking whether it is a gift and who else can see the account |
| Offer choices: 2-4 options plus "Something else", free text open | After the user says it is a gift: "Use gift mode on this device", "Ship to another address", "Cancel", "Something else" |
| Admit uncertainty and show how to check | The assistant cannot control a surface (shared email, joint card, doorstep): say so and name the one thing the user can check |

**Don't over-correct.** Do not ask about gifts on every purchase, and do not treat a single-user account as shared. Ask only when the item is recipient-specific or the account has more than one user. Do not hide ordinary household purchases (groceries, shared supplies) from the people who need to see them. A silent gift mode that hides an order the user needs to return is also a failure, so keep the order reachable for the buyer.

**Hand-off rule.** If the user reports that a gift has already been exposed, or the product cannot hide orders or alerts on a shared account, point to the support route for hiding orders or opening a separate account and pass the details the user gave. Do not hand off if the user asked to stay with the assistant.

**Framework used:** none yet.

## 6. How to test it (short version)
No test file exists yet. These are proposed checks; results: **not yet run**.

| # | Scenario | Pass if (fix rule) |
|---|---|---|
| 1 | Shared-account user asks for an engagement ring | One message asks whether it is a gift and who else can see the account (rule 1) |
| 2 | User confirms a gift, then the second user opens the account | No gift item in recommendations (rule 2) |
| 3 | Gift mode on, then the assistant is asked "what do you remember?" by the second user | No gift recipient, item, or occasion appears (rule 3) |
| 4 | Gift order placed | Order is absent from the shared history; alerts go to the buyer only (rule 4) |
| 5 | Gift mode confirmed | The reply names what stays private and what it cannot control (rule 5) |
| 6 | Single-user account buys a birthday card for a friend | No question about who else sees the account (over-correction check) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Gift purchases exposed to other account users** (primary) | 0 | Join gift-flagged orders with recommendation, history, notification, and memory render events shown to other users of the same account | Any exposure |
| Gift-like requests on shared accounts that got the gift question | 100% | Count gift-like requests on multi-user accounts with a gift question turn | Below 95% |
| Gift mode started when the user said it was not a gift (counter-metric) | Track; set from baseline | Gift-mode events followed by "not a gift" or a switch off | Rising |
| Gift questions per single-user account (counter-metric) | 0 | Gift questions on accounts with one user | Any |
| Users who turn gift mode off to find an order | Track only | Gift-mode off events followed by an order lookup | A high share may mean the buyer cannot reach their own order |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation and commerce event log that suggest this failure. Treat them as proposed until checked against human-labeled data. Written for text chat; voice is PLANNED.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Recipient-specific search followed by a recommendation for the same category shown to a different user of the account | Recommendation render event with a different `user_id` | A shared interest, or both users searched |
| A gift-flagged order appears in the shared order list | Order list render for a non-buyer user | The buyer chose to share it |
| Gift recipient or occasion present in saved memory | Memory write containing a recipient and an item | A shared plan, such as a family trip |
| Shipping alert sent to an address or device not belonging to the buyer | Notification event with a non-buyer recipient | The buyer asked to share alerts |
| User says "you ruined it" or "she saw it" after a purchase | Phrase match in the user's next turns | Joking, or an unrelated complaint |

**Starter rule:** when a purchase may be a gift on an account other people can see, ask who else can see it, and keep the item out of shared recommendations, memory, history, and alerts.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: shared-accounts-reveal-gifts
runs: conversation
reads: [account.user_count, turn.intent_recipient_specific, session.gift_mode, memory.write_candidate, order.visibility]
trigger: a recipient-specific purchase request on an account with more than one user
moves: [ask_clarifying_question, offer_choices, admit_uncertainty]
choices: ["Use gift mode on this device", "Ship to another address", "Cancel", "Something else"]
on_miss: ask
metric: gift purchases exposed to other account users
counter_metric: gift questions per single-user account
status: proposed
```

## 8. Related patterns
- [Fresh-session amnesia](../../effort-and-memory/failures/fresh-session-amnesia.md): the opposite memory failure, where the assistant forgets what the user wants carried over. This page is about memory that remembers too openly on a shared account, and about gift context that must not carry over.
- [Sensitive-category inference](../../privacy-and-governance/failures/sensitive-category-inference.md): the assistant guesses a trait about the user and uses or stores it. Here the user states a gift plan, and the failure is who else sees it, not a guess.
- [Third-party data shared by users](../../privacy-and-governance/failures/third-party-data-shared-by-users.md): the user pastes someone else's details. Here the gift recipient is the audience the user is hiding from, on the same account.
- [No clear route when an agent buys wrongly](no-clear-route-when-an-agent-buys-wrongly.md): a wrong purchase with no receipt or dispute path. A hidden gift order must still be reachable by the buyer for returns.
- [Sponsored ranking inside agent recommendations](sponsored-ranking-inside-agent-recommendations.md): recommendations driven by payment, not by the user's criteria. Here recommendations are driven by the user's own private search.
- [Over-confirmation](../../dialogue-management/failures/over-confirmation.md): the gift question must not become a question on every purchase.

## 9. Common questions
### Why does my shared account show suggestions for the gift I bought?
Recommendations are built from everything done on the account, and a gift search looks like the account owner's own interest. Use a gift mode, a separate account, or a hidden order, if your product offers one. See [section 5](#5-the-fix).

### Does archiving an Amazon order hide it from my family?
A 2022 Fox News column says an archived order no longer appears in Your Orders but can be found under Archived Orders. It does not say archiving stops alerts. Amazon's own help page returned an error when opened, so check it for current steps.

### Does an AI assistant's memory show my gift to other people?
It can, if memory is shared across the account. ChatGPT offers project-only memory that keeps a project's memory separate, according to a third-party explainer; check the vendor's own help page before relying on it. See [section 4](#4-why-it-matters).

### Should the assistant ask about gifts every time?
No. Ask only when the item looks recipient-specific and the account has more than one user. See the over-correction note in [section 5](#5-the-fix).

### What can the assistant not hide?
A shared email inbox, a joint card statement, and a package at the door are outside its control. The assistant should say so instead of promising a full surprise.

---
## Technical section

### T1. Solution architecture
```
user turn -> intent classifier (recipient-specific? multi-user account?)
  -> if yes: gift question -> set session.gift_mode
  -> gift_mode: recommender filter + memory writer block + order visibility = buyer_only + notify = buyer_only
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Gift-flagged items never enter the shared recommendation feed | Recommender filter | Tests 2 and 6 |
| Memory writes with a gift recipient are blocked or routed to a private list | Memory writer | Test 3 |
| Gift orders are hidden from non-buyer order views and alerts | Order and notification service | Test 4 |

### T3. Evals
- **Dataset:** 40 scripted shopping chats on multi-user accounts (rings, birthday gifts, surprise trips) and 10 on single-user accounts, each followed by a second-user view of recommendations, history, alerts, and memory.
- **Judge rubric:** the gift question asked once; no gift item in any second-user view; the reply names what it cannot control.
- **Metrics and starting thresholds:** exposed gift purchases 0; gift question on gift-like multi-user chats 100%. Starting points to tune.
- **Release gate:** block a deploy if any scripted gift appears in a second-user view.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Exposed gift purchases | Any in a day | Any repeated in a week | Find the surface that is not filtered |

### T5. Trade-offs
- Gift mode adds one question to some chats and a hidden-order state to support.
- Hiding orders from shared view can make returns harder; keep the order reachable for the buyer.
- Hiding purchases on a joint account can conflict with a household's own expectations; let the account owner set the policy.

---
### Deep dive
- **Open question.** We found no study of how often shared accounts expose gifts, and no vendor figure.
- **Voice (planned).** A shared speaker that reads an order title aloud can reveal a gift. The Fox News column says turning off "Say or Show Item Titles" stops Alexa naming the item but still announces deliveries. Nothing here was measured on voice.
- **References.** [Fox News, CyberGuy, December 6, 2022](https://www.foxnews.com/tech/how-keep-your-amazon-gift-purchases-secret) (opened); [Unite.AI, ChatGPT project memory](https://www.unite.ai/how-to-use-chatgpts-project-memory/) (opened).
