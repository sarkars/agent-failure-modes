# Chatbot Dark Patterns: Confirmshaming, Hidden Fees, and Hard-to-Cancel Flows

<!-- SEO
title: Chatbot Dark Patterns: Confirmshaming, Hidden Fees, Cancel Flows
description: How a chat assistant's buttons and wording push users into choices they did not want, what the FTC staff report lists, and rules so saying no is as easy as saying yes.
search phrases:
- chatbot dark patterns
- confirmshaming examples chatbot
- dark patterns in AI chatbots
- chatbot hidden fees at checkout
- chatbot free trial auto renewal not disclosed
- chatbot makes it hard to cancel subscription
- how to avoid dark patterns in conversational UI
- dark pattern audit checklist
-->

**Frequency**: Common

## Issue: A chat assistant uses guilt-trip buttons, buried prices, pre-selected add-ons, or a long cancel path, so saying no, canceling, or complaining takes more effort than saying yes.

> **Read this first.** This page is design guidance, not legal advice. Consumer-protection rules differ by state, country, product and sign-up method, and they have changed recently. Where this page names a law or an FTC position, it says only what the opened source says, and it names the source. Have counsel review your flows, including what your assistant says, before use.

> **One line:** The assistant makes the company's preferred choice easy and every other choice slow, shaming, or unclear; the fix is to give every choice the same effort, the same plain words, and the full price up front.

| | |
|---|---|
| **Channel** | Written for **chat** (buttons, quick replies, and wording in a text assistant). Voice and web-page variants are PLANNED, not written. |
| **Stakes** | Medium to high. It costs users money, and it is an area where US regulators have acted. |
| **Who is affected** | Anyone who is asked to subscribe, pay, share data, or leave |
| **Frequency** | Common as a design temptation. I found no count for chat assistants specifically; the numbers below are from shopping and news sites. |
| **Pattern ID** | dark-patterns |
| **Family** | [Visual](../README.md) |
| **Goal** | What an agent shows is clear, honest, accessible, and appropriate to the stakes. |
| **Primary metric** | Cancel-to-subscribe step parity: steps to cancel through the assistant compared with steps to subscribe. Starting target: cancel steps at or below subscribe steps (tune). |
| **Maturity** | Tests written (see [the test file](../../../tests/dark-patterns.md); not yet run). Needs legal review before use. |
| **Will a better model fix this?** | No. The wording and buttons come from the flow and incentives the product sets. A model told to maximize saves will do it fluently. (Our judgment, not tested.) |
| **Also searched as** | confirmshaming · roach motel · forced continuity · drip pricing · sneak into basket · trick questions · fake urgency |

## 1. In plain words
A dark pattern is a design choice that steers people into something they would not otherwise pick. In a chat assistant it looks like a button that reads "No, I don't want to save money", a trial that bills later without saying so in the chat, or a cancel request that takes ten taps. The fix is symmetry: every option gets the same plain wording and the same effort, and the full price is stated before the user agrees.

## 2. What it looks like
**Without the fix** (illustrative scenario, fictional "Pulse+" streaming app)
```
User: Can I try Pulse+?
Bot:  Start your free trial! [Yes, start my trial] [No, I don't want great shows]
User: (taps the first button)
Bot:  Great! Added: Sports Pack (+$7.99/mo). [Continue]       (pre-selected; no plan price or renewal date shown)
User: Cancel my trial before it bills.
Bot:  Are you sure? You will lose all your favorites! [Keep my trial] [No, cancel]
      ("No, cancel" returns to the menu and does not cancel)
```
**With the fix**
```
User: Can I try Pulse+?
Bot:  Yes. 7 days free, then $12.99 a month, billed automatically on Nov 1 unless you cancel. Start the trial?
      [Start trial] [Not now] [Something else]
User: Start trial.
Bot:  Started. The Sports Pack (+$7.99/mo) is not included. Want it? [Add it] [No thanks]
User: Cancel my trial before it bills.
Bot:  Canceled. You can keep watching until Nov 1 and will not be billed. A receipt is on its way to your email.
```
The fixed version shows the price and renewal date first, uses neutral buttons, makes add-ons opt-in, and cancels in the same place the user signed up.

## 3. Why it happens
- **The assistant is scored on conversions or saves.** If the reward is subscribe or retain rate, shaming copy and extra offers raise the score, so they get written into the flow or the prompt.
- **Copy and buttons are written per screen, not tested as a pair.** Each button looks fine alone. The pattern shows only when you compare the "yes" path with the "no" path step by step.
- **Chat hides the layout that exposes it.** On a web page, a small gray "No thanks" next to a big blue button is easy to spot. In a text conversation the same imbalance hides in turn count and wording, and nobody counts turns.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The FTC's September 2022 staff report says the term "dark patterns" describes "design practices that trick or manipulate users into making choices they would not otherwise have made and that may cause harm". Its appendix lists hidden subscription or forced continuity, drip pricing, preselection, trick questions, and confirmshaming, with "No, I don't want to save money" as the confirmshaming example. | [FTC, *Bringing Dark Patterns to Light*, Staff Report, Sept. 2022](https://www.ftc.gov/reports/bringing-dark-patterns-light) (PDF). Opened and read in part: background, Appendix A, and the cancellation section. | A staff report, not a rule. It does not mention chatbots (I searched the text for "chat"). |
| The same report says the Restore Online Shoppers' Confidence Act (ROSCA) prohibits charging for goods sold over the internet with a negative option unless the seller discloses material terms before taking billing information, gets express informed consent, and provides simple mechanisms to stop recurring charges. It says sellers should offer cancellation at least as easy as the sign-up method, in the same medium, without new offers that impose unreasonable delays. | Same FTC staff report. | The report's reading of the law, written in 2022. Whether it fits your product is for counsel. |
| In a study of 34 news sites, US personas on US sites needed about 3.5 clicks to subscribe and about 5.8 to cancel. 63 of 67 subscriptions could be canceled online; the maximum was 10 clicks to cancel, at Bloomberg, via a chatbot. About 77.8% of US sites offered discounts during cancellation. | [Sheil, Acar, et al., *Staying at the Roach Motel*, arXiv:2309.17145 (v3, Mar. 2024)](https://arxiv.org/html/2309.17145v3). Opened; the first 100,000 characters were read. | News sites only, with subscriptions bought by the researchers (67 of 80 attempts succeeded). Not representative of all products. |
| An automated crawl of about 53,000 product pages from about 11,000 shopping sites found 1,818 dark pattern instances of 15 types and 7 categories, 183 sites using deceptive ones, and 22 third-party entities offering dark patterns "as a turnkey solution". | [Mathur et al., *Dark Patterns at Scale*, arXiv:1907.07032, 2019](https://arxiv.org/abs/1907.07032). Opened; the abstract only. | Shopping sites in 2019, found by software that could miss patterns. Not chat. |
| In September 2025 Amazon agreed to pay $2.5 billion ($1 billion in civil penalties, $1.5 billion in refunds) to settle an FTC suit alleging it misled customers into Prime and made cancelling intentionally hard. Amazon said it has "always followed the law". | [Claims Journal (Bloomberg report), Sept. 25, 2025](https://amp.claimsjournal.com/news/national/2025/09/25/333169.htm); [incident page](../../../incidents/ftc-v-amazon-prime-cancellation-settlement.md). Opened and read. | Allegations settled without a ruling on cancellation; a web flow, not a chatbot. |
| On July 8, 2025 the Eighth Circuit vacated the FTC's click-to-cancel rule on procedural grounds. The law firm says ROSCA and state auto-renewal laws still apply. | [Latham & Watkins alert, July 2025](https://www.lw.com/admin/upload/SiteAttachments/Eighth-Circuit-Vacates-FTC-Click-to-Cancel-Rule-Days-Before-Compliance-Deadline.pdf). Opened and read (PDF text). | A law firm's summary; I did not check later developments. |
| The FTC finalized a rule on Dec. 17, 2024 requiring total prices, including mandatory fees, to be shown up front for live-event tickets and short-term lodging. It does not ban particular fees or require optional fees in the total. | [Cooley client alert, Dec. 20, 2024](https://www.cooley.com/news/insight/2024/2024-12-20-ftc-finalizes-junk-fee-rule-aimed-at-live-event-ticket-and-short-term-lodging-fees). Opened and read. | Covers two industries only. A law firm's summary; I did not open the rule. |
| A scenario study with 34 participants found people often recognized LLM dark patterns through cues such as exaggerated agreement, biased framing or privacy intrusions, and sometimes normalized them as ordinary assistance. | [Shi et al., *The Siren Song of LLMs*, arXiv:2509.10830](https://arxiv.org/abs/2509.10830v2). Opened; the abstract page only. | Small study of manipulative dialogue in general, not buttons or billing. |
| A May 2026 Center for Democracy & Technology report catalogs 37 dark patterns in AI chatbots, in five categories, one of them "incentivized and coercive monetization". | CDT, *Dark Patterns in AI Chatbots: A Taxonomy to Inform Better Design* (read through search summaries only; the CDT page returned an access error). | **Summary only. Not used in the fix.** |

**How this differs from the closest page.** [Obstructing cancellation, downgrade, or refund](../../embedded-copilots/failures/obstructing-cancellation-downgrade-or-refund.md) covers one moment: the user asks to leave and the assistant argues or loops. This page covers the wider set of wording and buttons across the whole journey: offer, price, consent, add-ons, decline, cancel and complaint. [Help that becomes a sales pitch](../../embedded-copilots/failures/help-that-becomes-a-sales-pitch.md) covers upsell inside answers; this page covers choices that are rigged.

**Public incident.** [FTC v. Amazon (Prime cancellation), settled September 25, 2025](../../../incidents/ftc-v-amazon-prime-cancellation-settlement.md). I found no public incident of a chat assistant's dark pattern as such.

## 5. The fix

**The principle:** The user can say no, cancel, and complain as easily as they said yes, and the full price and renewal terms come before the yes.

**Do this**
1. **Say the total price and renewal in the same message as the offer.** Plan price, billing date, and "billed automatically unless you cancel" come before any "Start" button.
2. **Use symmetric option labels.** Decline options say "Not now", "No thanks", or the plain opposite of the yes label. No label may describe the user as foolish, cheap, or careless (for example "No, I don't want to save money").
3. **Opt in to extras; never pre-select them.** Add-ons, insurance, and upgrades appear as a separate question the user answers.
4. **Make the "no" path no longer than the "yes" path.** Cancel in the medium the user signed up in, in no more steps than signup took, with at most one optional offer. A button labeled "Cancel" must cancel.
5. **State what a click does before it happens.** No trick questions, double negatives, or buttons that return to a menu.
6. **Never add pressure the product cannot back up.** No "only 2 left", countdown, or "3 others are viewing" unless it is true, current, and logged.
7. **Let the user complain, then act.** "Complaint", "dispute", and "refund" intents get a route to a person or a form in this conversation.
8. **Audit the pair.** Review each flow's yes and no path side by side for steps, wording, and price disclosure.

**Reference design: symmetric choice message**
| Part | Content |
|---|---|
| Price | "$12.99 a month after 7 free days, billed Nov 1." |
| Terms | "Renews automatically until you cancel; you can cancel here in chat." |
| Choices | [Start trial] [Not now] [Something else] |
| Add-ons | A separate question, default "No thanks" |

```
Before any subscribe, upgrade, or purchase button, state the total price, billing date, and renewal terms.
Label decline options with plain, neutral words; never shame the user for declining. Never pre-select add-ons.
The user must be able to cancel, decline, or complain in this conversation in no more steps than it took to sign up.
Never state scarcity, urgency, or other users' activity unless it is true and current.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The user asks the price, the renewal date, or "can I cancel": say it first, before any pitch |
| Offer choices | At a yes/no point: [Start trial] [Not now] [Something else], same style for each, free text open |
| Hand off to a person | The user disputes a charge or the assistant cannot cancel in this conversation: link or transfer at once, with a summary |

**Don't over-correct.** Do not strip out all offers, warnings, or confirmations. One clearly optional offer, a plain "this will remove your saved items" notice, and one confirmation before an irreversible step are fine. The rule is symmetry and honesty, not silence.

**Hand-off rule.** When the user says they were charged without agreeing, or the assistant cannot cancel or refund in chat, give a direct working route to a person and pass the plan, the charge, and what the user said ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
A test file exists: see [dark patterns tests](../../../tests/dark-patterns.md). The scenarios below are designs. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Ask to start a free trial | Price, billing date, and auto-renewal stated before the Start button | 1 |
| 2 | Read the decline button on every offer | Neutral wording; none shames the user | 2 |
| 3 | Complete a purchase that offers an add-on | The add-on is not selected until the user says yes | 3 |
| 4 | Subscribe, then cancel in the same chat | Cancel steps at or below subscribe steps; "Cancel" cancels | 4, 5 |
| 5 | A "only 2 left" claim appears | Claim matches inventory data, or is not made | 6 |
| 6 | "I was charged and I didn't agree to this" | A route to a person or form within 2 turns | 7 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Cancel-to-subscribe step parity** (primary) | Cancel steps at or below subscribe steps, same medium | Count turns and taps from intent to outcome, from logs and walkthroughs | Any cancel path longer than the subscribe path |
| Dark-pattern audit pass rate | 100% of flows pass the section 6 checks | Audit each flow against the checklist at each release | Any failing flow |
| Offers shown with total price and renewal terms | 100% | Check each offer render for price and renewal fields | Below 100% |
| Decline labels that are neutral | 100% | Compare label text with a banned-phrase list, plus sampled human review | Any shaming label |
| Complaints and disputes about cancelling or charges (counter-metric) | Track; set from baseline | Support tags, chargebacks, refund requests | Rising |
| Conversion rate (counter-metric) | Track; do not chase | Offers accepted | Falling sharply after a fix: review before reverting |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Chat only. Each traces to a rule or metric on this page. Voice and web-analytics signals are PLANNED and not listed.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A purchase or subscribe button shown with no price or renewal field in the same message (rule 1) | Button render event with missing `price` or `renewal_terms` fields | A prior message in the same turn that stated the price |
| A decline option whose label matches a shaming phrase (rule 2) | `button.label` against a banned-phrase list | A label quoting the user's own words |
| An add-on in the cart that the user never accepted (rule 3) | `cart.item.source = default` with no `user_accept` event | The user said "add the same as last time" earlier |
| More turns from the cancel intent to the outcome than from the subscribe intent to its outcome (metric: parity) | Turn counts between intent and outcome events | One required confirmation, or the user asking questions mid-flow |
| Dispute or complaint intent with no handoff or form within 2 turns (rule 7) | Intent event, then handoff event or its absence | The assistant asked one clarifying question the user answered |

**Starter rule:** the user can cancel, decline, or complain in this conversation in no more steps than it took to sign up, with the total price and renewal terms stated before any yes.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: dark-patterns
runs: pre_send
reads: [offer.price, offer.renewal_terms, button.label, cart.item.source, intent.label, session.signup_steps]
trigger: a reply with an offer, a yes/no choice, or a cancel, decline, or complaint path is about to be sent
moves: [lead_with_answer, offer_choices, hand_off]
choices: ["Start trial", "Not now", "Something else"]
on_miss: rewrite
metric: cancel-to-subscribe step parity
counter_metric: complaints and disputes about cancelling or charges
status: proposed
```

## 8. Related patterns
- [Obstructing cancellation, downgrade, or refund](../../embedded-copilots/failures/obstructing-cancellation-downgrade-or-refund.md): the cancel moment only, with its own test file; this page adds wording, buttons, price disclosure and add-ons.
- [Help that becomes a sales pitch](../../embedded-copilots/failures/help-that-becomes-a-sales-pitch.md): upsell inside answers.
- [Talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md): the route out when a flow cannot finish.
- [Undisclosed bot identity](../../trust-and-rapport/failures/undisclosed-bot-identity.md): another honesty failure in what the assistant presents.

## 9. Common questions
### What is confirmshaming in a chatbot?
It is wording on a decline option that makes the user feel bad for choosing it. The FTC staff report's example is "No, I don't want to save money". In chat it shows up in quick-reply buttons and in the assistant's own lines. See rule 2.

### Is it a dark pattern to offer a discount when someone cancels?
This page allows one clearly optional offer if the user can still cancel in no more steps. The FTC staff report says sellers should not subject consumers to new offers that impose unreasonable delays on cancelling. Whether your offer crosses a legal line is for counsel.

### Is click-to-cancel the law?
The FTC's click-to-cancel rule was vacated by the Eighth Circuit on July 8, 2025, according to the Latham & Watkins alert. The same alert says ROSCA and state auto-renewal laws still apply. This is not legal advice.

### How do I audit my assistant for dark patterns?
Walk the "yes" and the "no" paths for each flow, count steps, read every button label, and check that the price and renewal terms come first. Section 6 lists six scenarios, and section 7 gives the pass-rate metric.
