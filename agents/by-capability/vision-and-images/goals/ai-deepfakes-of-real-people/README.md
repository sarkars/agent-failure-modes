# AI Deepfake Images and Videos of Real People

<!-- SEO
title: AI Deepfakes of Real People: Failures and Product Fixes
description: How AI image and video tools end up making sexual, false or fraudulent depictions of real people, and the product rules that stop them.
-->

**AI image and video tools make sexual, false or fraudulent pictures and videos of real people who never agreed to them.** Each page below names one way this happens, the incidents behind it, and the rule inside the product that stops it, with a test file you can run.

> **Read this first:** Every page in this goal is **Needs review**. Statements about law, police reports and platform rules summarize the cited news reports and documents. They are not legal advice and need review by a qualified person before anyone relies on them.

**Goal:** AI image and video tools never make sexual, false or harmful depictions of real people without their consent, and the person shown has a fast way to get them removed.

## Patterns

| Pattern | Covers | One line | Tests |
|---|---|---|---|
| [Nonconsensual sexual deepfakes of real people](failures/nonconsensual-sexual-deepfakes-of-real-people.md) | Both | Generators and photo editors make sexual images of named people with no consent | [Tests](../../tests/nonconsensual-sexual-deepfakes-of-real-people.md) |
| [Fake images of politicians in events that never happened](failures/ai-images-of-real-people-in-fake-events.md) | Image | Realistic arrests, hospital stays and election scenes, despite the vendor's own policy | [Tests](../../tests/ai-images-of-real-people-in-fake-events.md) |
| [Deepfake celebrity endorsement ads](failures/deepfake-celebrity-endorsement-ads.md) | Both | A star's face and voice sell a product or giveaway they never backed | [Tests](../../tests/deepfake-celebrity-endorsement-ads.md) |
| [Deepfake CEO video call payment fraud](failures/deepfake-executive-impersonation-payment-fraud.md) | Both | A faked executive on a call orders staff to wire money | [Tests](../../tests/deepfake-executive-impersonation-payment-fraud.md) |
| [AI nude images of classmates](failures/ai-nude-images-of-classmates.md) | Image | Students turn ordinary photos of classmates into fake nude images | [Tests](../../tests/ai-nude-images-of-classmates.md) |
| [Uploaded photos edited with no consent check](failures/photo-upload-deepfakes-without-consent-check.md) | Both | A tool refuses a real person's name but edits or animates an uploaded photo of them | [Tests](../../tests/photo-upload-deepfakes-without-consent-check.md) |
| [Real-person filters bypassed by rewording](failures/deepfake-filters-bypassed-by-rewording.md) | Both | A blocked name still gets through as a description, a photo or a faked identity check | [Tests](../../tests/deepfake-filters-bypassed-by-rewording.md) |
| [AI videos of deceased people without family consent](failures/ai-videos-of-deceased-people-without-consent.md) | Both | Videos of dead celebrities and historical figures made with no way for the family to say no | [Tests](../../tests/ai-videos-of-deceased-people-without-consent.md) |
| [Harmless image requests refused as unsafe](failures/ai-image-generator-refuses-harmless-requests.md) | Image | Ordinary prompts blocked as risky, or refused in one product and allowed in another | [Tests](../../tests/ai-image-generator-refuses-harmless-requests.md) |

All tests are **Not yet run**. All detection signals and Guide specs are proposed.

## Related
- [Safety filter bypass](../generation-artifacts/failures/safety-filter-bypass.md): the closest older page; these pages cover real people specifically
- [Output filtering and moderation](../../../../cross-cutting/security/goals/output-filtering-moderation/README.md)
- [Governance](../../../../cross-cutting/governance/goals/governance/README.md)
- [Vision and images goals](../README.md)
