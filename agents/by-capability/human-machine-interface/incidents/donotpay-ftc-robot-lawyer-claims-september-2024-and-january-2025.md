---
title: "DoNotPay and the FTC: 'Robot Lawyer' Claims Settled, Order Finalized"
date: 2025-01-16
source: "https://www.ftc.gov/news-events/news/press-releases/2025/02/ftc-finalizes-order-donotpay-prohibits-deceptive-ai-lawyer-claims-imposes-monetary-relief-requires"
summary: "In September 2024 the FTC alleged that DoNotPay's 'robot lawyer' service did not perform as advertised and had no testing against a human lawyer. DoNotPay agreed to a settlement without admitting or denying the allegations. The FTC voted to finalize the order on January 16, 2025 and announced it on February 11, 2025. The allegations are the FTC's; the company did not admit them."
categories:
  - Legal and professional advice
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - undisclosed-bot-identity
---

**This page is a dated teardown of one public enforcement case about an AI legal-help service, for teams that describe what their assistant can do.** Every fact below comes from a source we opened (listed at the end). The case is an FTC consumer-protection action about marketing claims. The FTC's statements are allegations; DoNotPay settled without admitting or denying them. We describe no chat transcripts, because none of the opened sources show any.

## Read this first

This page is design guidance, not legal advice. It does not say whether any company broke any law. Have a lawyer review your own claims and disclosures before use.

## What happened (as reported)

- **Sept 25, 2024.** An FTC press release announcing a set of actions on deceptive AI claims includes DoNotPay. It says DoNotPay marketed its subscription service as "the world's first robot lawyer," and that the FTC alleges the service did not match those claims.
- **Same date.** The FTC says the proposed order was voted 5-0 and was open to 30 days of public comment before a final decision.
- **Sept 30, 2024.** The ABA Journal (Debra Cassens Weiss) reports the settlement terms and a DoNotPay spokesperson's reply (below).
- **Jan 16, 2025.** The FTC says the Commission voted 5-0 to approve the final order, after receiving five public comments.
- **Feb 11, 2025.** The FTC publishes the press release announcing the final order. The vote date and the announcement date differ; both are from the FTC.

## What the FTC alleged

From the two FTC pages (our paraphrase):

- **Claims.** DoNotPay promised that users could sue for assault without a lawyer and produce valid legal documents quickly.
- **No testing.** The FTC alleges DoNotPay did not test whether its chatbot's output matched a human lawyer's level.
- **No attorneys.** The FTC alleges the company did not hire or retain attorneys to check the quality and accuracy of its legal features.
- **Business-site feature.** A feature that scanned small business websites for legal violations from an email address allegedly did not work effectively. The FTC says the company claimed it could find issues that could cost $125,000 in legal fees.
- **Training data.** The ABA Journal reports the FTC alleged none of the company's technologies was trained on a comprehensive database of federal and state laws, regulations and court decisions.

## What the order requires (as reported)

- **Money.** $193,000 in monetary relief.
- **Notice.** DoNotPay must notify consumers who subscribed between 2021 and 2023 about the limits of its law-related features.
- **Claims.** A ban on saying the service performs like a lawyer, or can replace a professional service, without supporting evidence.

## What the company said

The ABA Journal reports a spokesperson said DoNotPay was "pleased to have worked constructively" with the FTC, stressed it admitted no liability, and said the complaint involved a few hundred customers from several years ago and services since discontinued. That is the company's account; we found no independent check of it.

## Where the sources disagree or are silent

| Topic | What the sources say |
|---|---|
| Date of the order | The FTC gives Jan 16, 2025 as the vote and Feb 11, 2025 as the announcement. This page's front-matter date is the vote. |
| Scale | The company says a few hundred customers. The opened FTC pages give no customer count, and we found none. |
| Other legal actions | A search summary (not opened) mentioned a California State Bar notice. The ABA Journal piece we opened does not mention it. We use neither. |

## What the sources do not say

- What users typed, or what the chatbot answered, in any single conversation.
- How many customers were affected, or how many received a wrong or unusable legal document.
- Whether any user was harmed in court or lost money because of the output. The pages describe marketing claims, not individual outcomes.
- What the bot's own on-screen wording said about its limits at the time.
- Whether the current DoNotPay product differs from the one described. We did not open it.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). Partial fit. The FTC alleges the service was not checked against a human lawyer's work and had no attorney review. That is a missing check on answer quality. The pattern is about the tone of individual wrong answers in chat; no opened source shows any such answer.
- [Undisclosed bot identity](../goals/trust-and-rapport/failures/undisclosed-bot-identity.md) (`undisclosed-bot-identity`). Weak, partial fit. The pattern covers hiding limits from users, and the order requires a notice about limits. No source says the bot claimed to be human.

No existing pattern covers "marketing says the assistant can replace a professional." We do not force a match.

## Where in the flow it broke

Based on the FTC's allegations, and only as far as they go:

1. **Before the chat.** Ads and the site said the service could replace a lawyer for tasks such as drafting documents.
2. **In the product.** The FTC alleges no testing against a lawyer and no attorney review of the legal features.
3. **After use.** Users got documents or advice they were told were valid. The sources do not show what the chat itself said.
4. **Response.** An FTC complaint, a settlement, a refund-style payment, a notice to past subscribers and a ban on unsupported claims.

The reported cost is $193,000 plus a notice to past subscribers. We opened no figure for anything else.

## What to measure

Our proposals, not the FTC's. Status: Not yet run.

| Metric | How to compute from logs |
|---|---|
| Claim-evidence coverage | Capability claims in ads, site copy and bot greetings that link to a stored test result, divided by all such claims |
| Expert-review rate | Outputs in a high-stakes category (legal, medical, money) that a qualified person reviewed in a sample, divided by outputs sampled |
| Limits-notice rate | Sessions where the first reply or form states what the bot cannot do, divided by sessions |
| Advice-to-handoff rate | Sessions asking for a legal judgment that end with an offer of a human professional, divided by such sessions |

## What a team can change

Our proposals, not the FTC's. Status: Not yet run.

1. **Test before you claim.** Write each capability claim as a test on a fixed set of tasks, scored by a qualified reviewer. Check: no claim ships without a stored result.
2. **Use plain scope words.** Say "drafts a first version for you to check," not "replaces a lawyer," unless a test supports it. Check: a copy review flags any "replaces," "guaranteed" or "valid" without a linked test.
3. **State limits in the chat itself.** Put a one-line limit on the first reply and beside each generated document. Check: a scripted legal request shows the line.
4. **Offer a human for judgment calls.** If the user asks whether to sue or sign, offer a licensed professional. Check: a scripted set of such questions all show the offer.
5. **Keep customer quotes sourced.** Show only quotes you can trace to a real, named source. Check: each testimonial links to its origin.
6. **Don't over-correct.** A bot that refuses every legal topic fails users who only want a plain explanation. Run an ordinary-question set and require near-zero refusals.

## Sources

| URL | Publisher | Date | Status |
|---|---|---|---|
| https://www.ftc.gov/news-events/news/press-releases/2025/02/ftc-finalizes-order-donotpay-prohibits-deceptive-ai-lawyer-claims-imposes-monetary-relief-requires | Federal Trade Commission | 2025-02-11 | Opened 2026-10-20 (fetch tool returned a summary) |
| https://www.ftc.gov/news-events/news/press-releases/2024/09/ftc-announces-crackdown-deceptive-ai-claims-schemes | Federal Trade Commission | 2024-09-25 | Opened 2026-10-20 (summary) |
| https://www.abajournal.com/news/article/robot-lawyer-website-donotpay-settles-ftc-claims-it-couldnt-deliver-on-promises | ABA Journal (Debra Cassens Weiss) | 2024-09-30 | Opened 2026-10-20 (summary) |

Not opened / unverified, and not used as facts above: the FTC complaint and order text (docket not opened); Ars Technica, Above the Law, Quartz, MLex and other outlets seen only in search summaries; the California State Bar notice (search summary only); and DoNotPay's own site and product. Our fetch tool summarizes pages, so quotes are limited to short phrases attributed to the FTC or the company.

## Corrections

If you have the FTC complaint or order text, DoNotPay's current product description, or a better date, tell us and we will fix this page.
