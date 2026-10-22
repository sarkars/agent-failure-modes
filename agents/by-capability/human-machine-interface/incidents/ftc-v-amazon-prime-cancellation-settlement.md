---
title: "Amazon Pays $2.5 Billion to Settle FTC Claims It Made Prime Hard to Cancel"
date: 2025-09-25
source: "https://amp.claimsjournal.com/news/national/2025/09/25/333169.htm"
summary: "Amazon agreed to pay $1 billion in civil penalties and $1.5 billion in refunds to settle an FTC lawsuit alleging it enrolled customers in Prime without consent and made cancelling hard. Under the order, Amazon neither admits nor denies the allegations."
categories:
  - Customer Service
  - Governance
patterns:
  - obstructing-cancellation-downgrade-or-refund
  - help-that-becomes-a-sales-pitch
---

**This page is a dated teardown of a US consumer-protection case, for teams that build cancellation and retention flows, including chat assistants.** It is a web-flow case, not a chatbot case. The FTC's claims were allegations that Amazon settled without admitting or denying them. Every fact below comes from a source we opened (listed at the end). Statements about law are the FTC's or the order's own words. This is not legal advice, and the legal reading is Needs review.

## What happened (as alleged and settled)

- **June 21, 2023.** The FTC filed a complaint against Amazon in the US District Court for the Western District of Washington (case 2:23-cv-0932). Its press release says Amazon used "dark patterns" to enroll consumers in automatically renewing Prime subscriptions without consent, and ran a cancellation process whose "primary purpose" was "not to enable subscribers to cancel, but to stop them." It charged violations of the FTC Act and the Restore Online Shoppers' Confidence Act (ROSCA). The Commission vote was 3-0 ([FTC press release](https://www.ftc.gov/news-events/news/press-releases/2023/06/ftc-takes-action-against-amazon-enrolling-consumers-amazon-prime-without-consent-sabotaging-their)).
- **September 20, 2023.** The FTC filed an amended complaint, which adds the details of the cancellation flow used below.
- **September 25, 2025.** The FTC announced a stipulated final order: a $1 billion civil penalty and $1.5 billion in consumer redress for an estimated 35 million consumers, filed with Amazon and two executives, Neil Lindsay and Jamil Ghani. The Commission vote was 3-0. The FTC calls the penalty the largest ever in a case involving an FTC rule violation ([FTC press release](https://www.ftc.gov/news-events/news/press-releases/2025/09/ftc-secures-historic-25-billion-settlement-against-amazon)).
- **What the order says (filed September 25, 2025).** Paragraph 4: the defendants "neither admit nor deny" the allegations. Section IV requires "simple mechanisms" to cancel that "must not be difficult, costly, confusing, or time consuming" and, at a minimum, are offered "through the same medium the consumer used to consent." Section V requires a clear option to decline Prime, a "Join Prime" call to action, no double-stacked sign-up button, and the price and the word "renews" on sign-up pages. The order runs 10 years for Amazon and 3 years for the individual defendants ([stipulated order](https://www.ftc.gov/system/files/ftc_gov/pdf/Amazon-ROSCA-Order-Filed_0.pdf)).
- **Redress terms.** The order defines a "Save Offer" as any attempt to retain a customer who is cancelling, including "any offer, reason to retain an agreement, modification or proposed modification." A definition in the order also refers to people who tried to cancel online and did not finish, or who took a Save Offer by mistake; we read it only as a definition, not the full claims rules. On September 17, 2026 the FTC announced a revised redress order; it reports more than $845 million paid as of September 2026 ([FTC, Sept 2026](https://www.ftc.gov/news-events/news/press-releases/2026/09/ftc-announces-additional-payments-consumers-stemming-ftcs-amazon-prime-settlement)).

## The "Iliad" cancellation flow, as described in the amended complaint

The amended complaint says Amazon named its cancellation process "Iliad," after Homer's epic about the long Trojan War, launched it in 2016, and did not substantially change it until about April 2023 (paragraphs 127-130). Paragraph 128 calls it a "four-page, six-click, fifteen-option" process, against one or two clicks to enroll. What follows is the FTC's description, not a court finding.

1. **Finding it (paragraphs 131-139).** Three routes led in: ask customer service and get a link (the complaint says Amazon required agents to encourage cancelling that way), go through Prime Central to "End Membership," or search "How to cancel membership." It says the flow could not be reached from Amazon.com in fewer than two clicks.
2. **Page one (paragraphs 141-142).** The user sees "a look back at [their] journey with Prime" and marketing links for Prime services. Three buttons: "Remind Me Later," "Keep My Benefits," "Continue to Cancel." None cancels.
3. **Page two (paragraphs 143-146).** Discounted or annual pricing, student and EBT discounts, a warning that tied items "will be affected," and the same three buttons. None cancels.
4. **Page three (paragraphs 147-152).** Five options. Only the last, "End Now," cancels at once. "End on [date]" only turns off auto-renew, with no refund. "Pause" holds the plan. The complaint counts "Remind Me Later" four times and "Keep My Membership" three times before the user reaches the end.
5. **Other devices (paragraph 129).** Users who enrolled through Prime Video on Fire TV or FireStick could not cancel there and had to use the flow or call customer service.

## Where in the flow it broke (per the allegations)

- **Entry.** The way out was hard to find, and a request to customer service was answered with a link to the same flow.
- **Pages one and two.** The cancel button was absent. Each page offered three exits that kept the plan. The request "cancel" returned an offer, not a result.
- **Page three.** The one action that did what the user asked sat last among five.
- **Medium mismatch.** Enrollment on one device, cancellation elsewhere.

## What the sources do not say

- **This was not a chatbot.** The flow was a page sequence plus customer service that sent users a link. The opened sources do not describe any AI assistant.
- **Not a finding.** The September 2025 order says the defendants neither admit nor deny the allegations. A settlement is not a ruling that each allegation is true. Amazon's 2023 and 2025 statements were not in any source we opened, so we do not characterize them.
- **No rate.** Sources give no share of users who failed to cancel. The 35 million figure is the FTC's estimate of consumers affected by unwanted enrollment or deferred cancellation, not a count of people who gave up.
- **The flow changed.** Paragraph 127 says Amazon changed the process about April 2023. The post-2023 flow is not described in the sources we opened.
- **Offers were not the whole charge.** The order defines Save Offers and lets Amazon keep making them as long as the cancellation mechanism stays simple. The complaint targets the pile-up of pages and options, not offers as such.

## Pattern match

- **[Obstructing cancellation, downgrade, or refund](/obstructing-cancellation-downgrade-or-refund/)** fits the shape: leaving was longer than joining, and each step before "End Now" was an offer, a warning or an exit that kept the plan. It fits the pattern's rules on medium, one offer and no loop.
- **[Help that becomes a sales pitch](/help-that-becomes-a-sales-pitch/)** fits the pages that answered a cancel request with a recap of benefits and discounts. The pattern is about assistants; here the pitch was page content.
- **Where it does not fit.** Enrollment allegations (button wording, double-stacked sign-up) are a different failure and are not covered here.

## What to measure and change for a chat assistant

Proposed checks, each pass/fail on a transcript or log. Status: Not yet run; none comes from the FTC. Chat steps stand in for page clicks.

1. **Parity count.** Count turns from "cancel" to a completed cancellation, and clicks and turns to subscribe. Pass: cancel is no longer than subscribe, in the same medium.
2. **Offers before the action.** Count offers shown after the first clear cancel request. Pass: at most one, optional, in the same message as the confirmation.
3. **Repeat of the same exit.** Flag a reply that offers "remind me later" or "keep my plan" a second time. The complaint's four reminders are the model.
4. **Result in the first reply.** Test that the first answer to "cancel" states plan, price, end date and what is lost, and asks one yes or no.
5. **Cross-device parity.** If a plan can be bought through voice, TV or chat, test that it can be cancelled there, or that a working direct link is given.
6. **Handoff is not a link back.** If an agent can only send a link, test that the link ends in the cancel action and not in the same flow.
7. **Timing and refunds.** Test that "End on [date]" style choices say whether a refund applies.
8. **Legal review.** Compare your flow with your state auto-renewal rules and ROSCA. Needs review.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://www.ftc.gov/news-events/news/press-releases/2025/09/ftc-secures-historic-25-billion-settlement-against-amazon | FTC press release | 2025-09-25 | Yes, 2026-10-22 |
| https://www.ftc.gov/news-events/news/press-releases/2023/06/ftc-takes-action-against-amazon-enrolling-consumers-amazon-prime-without-consent-sabotaging-their | FTC press release | 2023-06-21 | Yes, 2026-10-22 |
| https://www.ftc.gov/system/files/ftc_gov/pdf/Amazon-ROSCA-Order-Filed_0.pdf | US District Court, W.D. Wash. (stipulated final order, via FTC) | 2025-09-25 | Yes, 2026-10-22 (PDF text extracted) |
| https://www.ftc.gov/system/files/ftc_gov/pdf/2023-09-20-067-AmendedComplaint%28redacted%29.pdf | FTC (amended complaint, redacted) | 2023-09-20 | Yes, 2026-10-22 (PDF text extracted; read paragraphs 127-152) |
| https://www.ftc.gov/legal-library/browse/cases-proceedings/2123050-amazoncom-inc-rosca-ftc-v | FTC case page | Updated through 2026-09 | Yes, 2026-10-22 |
| https://www.ftc.gov/news-events/news/press-releases/2026/09/ftc-announces-additional-payments-consumers-stemming-ftcs-amazon-prime-settlement | FTC press release | 2026-09-17 | Yes, 2026-10-22 |
| https://amp.claimsjournal.com/news/national/2025/09/25/333169.htm | Claims Journal (Bloomberg report) | 2025-09-25 | Not reopened in this revision; no claim above relies on it |

## What we could not verify

- A report that a judge found in September 2025 that Amazon's conduct was illegal before the settlement, and Amazon's statement that it has always followed the law. Both come from the news report and search summaries, not a source we opened. The FTC case page lists no such ruling.
- The "one or two clicks" to enroll is the complaint's claim; we did not test any live flow.
- Whether the redesigned April 2023 flow met the order. The order's terms are from the filed text only.
- The legal reading of any of this, and whether California's or other states' rules apply to your product. Needs review.
