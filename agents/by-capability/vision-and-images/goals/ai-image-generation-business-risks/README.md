# Business Risks of AI Image and Video Generation

<!-- SEO
title: Business Risks of AI Image and Video Generation: Failures and Fixes
description: How businesses get hurt when they publish AI-made images and video: misleading product shots, missing review, backlash and legal exposure, and the workflow rules that prevent it.
-->

**Businesses publish AI-made images and video that misstate their products, skip review or disclosure, and expose them to refunds, backlash and regulators.** Each page below names one way this happens, the reports behind it, and the rule inside the workflow that stops it, with a test file you can run.

> **Read this first:** Every page in this goal is **Needs review**. Statements about advertising law, regulators, rulings and disclosure rules summarize the cited news reports, regulator pages and law-firm summaries. Several incidents are outside the US and are marked as such. None of this is legal advice, and it needs review by a qualified person before anyone relies on it.

**Goal:** AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm.

## Patterns

| Pattern | Covers | One line | Tests |
|---|---|---|---|
| [AI product images that show features it does not have](failures/ai-product-images-show-features-it-does-not-have.md) | Both | An AI product shot or event ad shows features the real thing lacks, and buyers pay for the picture | [Tests](../../tests/ai-product-images-show-features-it-does-not-have.md) |
| [AI images in ads published without review](failures/ai-images-in-ads-published-without-review.md) | Image | Brand ads run AI-altered images nobody approved; require sign-off on the live version and keep platform AI edits off | [Tests](../../tests/ai-images-in-ads-published-without-review.md) |
| [AI ads backlash for replacing artists with AI](failures/ai-ads-backlash-for-replacing-artists-with-ai.md) | Both | A brand runs AI ads or AI models where people expect artists, actors or models, and the backlash is about who lost the work; review the roles AI replaced, credit the humans, label it and name an owner before launch | [Tests](../../tests/ai-ads-backlash-for-replacing-artists-with-ai.md) |
| [AI image mistakes in ads that go viral](failures/ai-image-mistakes-in-ads-go-viral.md) | Both | An ad shows an extra tower, a backward foot or a two-handled bike and the public finds it first; check real things against a reference and pull and correct every copy the same day | [Tests](../../tests/ai-image-mistakes-in-ads-go-viral.md) |
| [AI fake receipts and claim photos used to defraud a business](failures/ai-fake-receipts-and-claim-photos-fraud.md) | Image | Expense, refund, claims and KYC teams pay on AI-made receipts, damage photos or IDs; check outside data, ask for originals, never accuse on image tells | [Tests](../../tests/ai-fake-receipts-and-claim-photos-fraud.md) |
| [Confidential files uploaded to AI image tools](failures/confidential-files-uploaded-to-ai-image-tools.md) | Both | Staff upload unreleased renders, client photos or floor plans to consumer image tools that are public or train by default; classify files and allow each class only on approved tools and tiers | [Tests](../../tests/confidential-files-uploaded-to-ai-image-tools.md) |
| [Ad platforms that reject or label AI-generated ads](failures/ad-platforms-reject-or-label-ai-generated-ads.md) | Both | AI-made ads go live without the disclosure each platform asks for, or get rejected; check each platform's current rule before launch and after every duplicate | [Tests](../../tests/ad-platforms-reject-or-label-ai-generated-ads.md) |
| [AI-generated ad disclosure rules not met](failures/ai-generated-ad-disclosure-rules-not-met.md) | Both | One AI-made creative runs in several markets and misses one market's AI labeling law; match every market to a counsel-kept register before launch | [Tests](../../tests/ai-generated-ad-disclosure-rules-not-met.md) |

All tests are **Not yet run**. All detection signals and Guide specs are proposed.

## Planned (not yet written)
- Regulated claims in images: health, finance, food, before-and-after
- Cultural, religious or local errors in images made for other markets
- Employees' or models' likeness reused beyond what they agreed to
- No model release or likeness rights for generated people who resemble real people

## Related
- [Generation artifacts](../generation-artifacts/README.md): the older goal on image generation failures, including [semantic drift](../generation-artifacts/failures/semantic-shift.md) and [consistency failure](../generation-artifacts/failures/consistency-failure.md)
- [Misleading generated visuals](../../../human-machine-interface/goals/visual/failures/misleading-generated-visuals.md): a chat assistant showing a render as the real product; this goal covers what the business itself publishes
- [AI image copyright and trademark risks](../ai-image-copyright-and-trademark/README.md): who owns the output; this goal covers what the output claims
- [Content marketing](../../../../by-use-case/content-marketing/README.md)
- [Governance](../../../../cross-cutting/governance/goals/governance/README.md)
- [Vision and images goals](../README.md)
