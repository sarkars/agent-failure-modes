# How to Watermark AI-Generated Images: Outputs Shipped With No AI Label, Watermark or Content Credentials

<!-- SEO
title: AI Images With No Watermark or Content Credentials: The Fix
description: Your AI image or video app ships files with no label, watermark or Content Credentials, so no one can tell they are AI. Mark every output path and test it.
search phrases:
- how to add c2pa content credentials to ai generated images
- how to watermark ai generated images in my app
- do ai image apis add watermarks
- gpt-image-1 c2pa metadata
- invisible watermark for ai images open source model
- ai generated image label requirement for developers
- synthid content credentials api outputs
-->

**Frequency**: Unknown

## Issue: A team builds an image or video generator into its own product, and the files it hands to customers carry no visible AI label, no invisible watermark and no Content Credentials (C2PA) manifest, so platforms, newsrooms and viewers downstream cannot tell they were AI-made. List every model and every export path, attach a signed manifest and a watermark to each output, offer a visible label, and block a release when a test file from any path comes out unmarked.

> **Read this first:** This page is product design guidance, not legal advice. Statements about the EU AI Act, California's AI Transparency Act (SB 942) or any other labeling duty summarize the opened sources as read on October 29, 2026. Whether your product is covered, which marks it must carry, by when, and with what exceptions needs review by a qualified person. The rules below are engineering choices, not a compliance standard.

> **One line:** A Phoenix virtual-staging app (an invented example) generates furnished rooms with an image API model that its vendor does not mark, then resizes each file to JPEG for download, so the listing photos it ships carry no label, no watermark and no manifest, and a buyer who checks one finds nothing; the fix is to mark every output on every path with a signed manifest plus a watermark, offer a visible "AI-staged" label, and test a sample file from each path before every release.

Status: Needs review

| | |
|---|---|
| **Covers** | Both. OpenAI's page describes signals for images and video; NIST AI 100-4 covers all content types; Indicator's test posts were images and videos (section 4). |
| **Channel** | Apps, sites and APIs that generate or edit images or video for customers: design tools, ad makers, virtual staging, avatar and product-photo apps, and the download, share and API paths that deliver the files |
| **Stakes** | High. An unmarked file can be passed off as a real photo or event, and a platform has nothing to read when it decides whether to label it (sections 3 and 4). |
| **Who is affected** | People who see the image or video downstream, platforms and newsrooms that check for provenance, the builder's own customers who expected a label, and the builder |
| **Frequency** | Unknown. No opened source counts products that ship unmarked outputs. Indicator found only 169 of 516 AI test posts labeled by five platforms (section 4), which shows the downstream gap, not its cause. |
| **Pattern ID** | ai-images-published-without-ai-label-watermark-or-content-credentials |
| **Family** | [AI Image Watermarks, Labels and Content Credentials](../README.md) |
| **Goal** | AI images and video carry provenance signals that reach the people and platforms who see them: a mark on every output, credentials that survive the trip, and labels that are read correctly. |
| **Primary metric** | Unmarked-output rate: sampled output files, across every model and export path, that carry neither a valid C2PA manifest nor a detectable watermark, divided by all sampled output files. Proposed starting target: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Marking is a step in the pipeline around the model: which vendor model you call, whether you add a manifest and a watermark, and whether export keeps them. OpenAI says some of its own API image models are not covered. (Our judgment, drawing on the cited sources.) |
| **Also searched as** | add content credentials to generated images · watermark ai output api · c2pa signing for my app · ai disclosure label for generated photos · unmarked ai images |

Tests: [AI images published without an AI label, watermark or Content Credentials test file](../../../tests/ai-images-published-without-ai-label-watermark-or-content-credentials.md).

## 1. In plain words
Some AI vendors hide a watermark in what their models make and attach a signed record, called Content Credentials, that says "made with AI." Neither one is automatic for everyone. A product that runs an open model on its own servers, calls a vendor model the vendor does not mark, or converts files on export can ship images with no mark at all. Then nobody downstream can tell. The fix is to mark every output yourself, check that the marks are there, and give people a visible label they can see without a tool.

## 2. What it looks like
The app, people and listing are invented.

**Without the fix**
```
Agent:     I'm posting these staged living rooms on our listing. Will they show as AI?
Assistant: Our images are standard high-quality JPEGs, ready to post anywhere.
Agent:     So the files say they're AI?
Assistant: You can add a note to your listing if you'd like.
(A buyer runs one photo through a Content Credentials check: no manifest. No watermark
 either. The app used an unmarked API model and re-saved every file at export.)
```
**With the fix**
```
Agent:     I'm posting these staged living rooms on our listing. Will they show as AI?
Assistant: Each file carries Content Credentials saying it was made with RoomRight's AI and
           an invisible watermark. Uploads and screenshots can remove them, so a visible label
           is the reliable way to tell buyers. Add one?
           "Add 'AI-staged' badge to all" · "Download without badge" · "Something else"
Agent:     Add the badge to all.
Assistant: Done: 12 files with the badge, credentials and watermark. Check any one at our verify page.
```
The fixed app marked every file, said plainly what the marks do and do not survive, and offered a visible label.

## 3. Why it happens
- **The vendor does not mark every model or path.** OpenAI's help page says its API outputs are covered "except for models planned for imminent deprecation, including gpt-image-1, gpt-image-1.5, and sora-2," and that coverage "may vary by product, model, export path, file type." A builder who picked one of those models ships unmarked files and may not know it.
- **On an open model you run, marking is your step, and it is easy to drop.** Hu et al. note that for open-source diffusion models "an attacker can easily remove the watermarking components" and generate non-watermarked images. A team that self-hosts an open model gets no vendor mark at all unless it adds one.
- **Machine marks are not labels.** NIST says recorded provenance data "is not necessarily displayed to users"; a person sees AI involvement only through a separate label. A product that adds a manifest but no visible label still leaves viewers with nothing to see.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| OpenAI says images from ChatGPT, Codex or the OpenAI API include Content Credentials and SynthID watermarks, but API outputs are covered "except for models planned for imminent deprecation, including gpt-image-1, gpt-image-1.5, and sora-2." Metadata "can carry detailed information, but platforms, editing tools, and file conversions may remove it." | [OpenAI Help Center, "Provenance signals in OpenAI-generated content"](https://help.openai.com/en/articles/8912793-c2pa-in-dall-e-3) (formerly "C2PA in DALL-E 3"). Opened Oct 29, 2026. | Vendor page; it changes often and showed "Updated: 8 hours ago" when read. Says nothing about other vendors. |
| NIST describes using a robust covert watermark, "unlikely to be stripped as the image travels across platforms," together with signed metadata; it says provenance data is not necessarily shown to users, and lists overt watermarks and interface disclaimers as labels. It also warns covert watermarks that embed sensitive information "may make privacy controls more difficult." | [NIST AI 100-4, "Reducing Risks Posed by Synthetic Content," Nov 2024](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-4.pdf). Full text opened Oct 29, 2026. | An overview of techniques, not a test of any product. NIST says there is "limited consensus" on how labels should be designed. |
| Duke researchers removed Meta's Stable Signature watermark from Stable Diffusion 2.1 by fine-tuning its decoder, so its images were "non-watermarked, while maintaining the visual quality." They note other watermark components in open models can "easily" be removed. | [Hu, Jiang, Guo and Gong, "Stable Signature is Unstable," arXiv 2405.07145](https://arxiv.org/pdf/2405.07145) (May 12, 2024). Full text opened Oct 29, 2026. | Preprint; one watermark method and one model. It is about deliberate removal, so it supports "add your own mark and test it," not a rate of unmarked products. |
| Indicator published 516 AI-made image and video posts on Instagram, LinkedIn, Pinterest, TikTok and YouTube; "only 169 posts, or just over 30% of the total, were correctly labeled." Google and Meta often failed to label content made with their own AI tools. | [Indicator, Mantzarlis and Dutta, Oct 23, 2025](https://indicator.media/p/tech-platforms-fail-to-label-ai-content-c2pa-metadata). Opened Oct 29, 2026. | The rest of the article is paywalled; which generators added marks was not readable. Measures platform labels, not the generators' own marking. |
| EU AI Act Article 50(2): providers of systems generating synthetic image, video, audio or text "shall ensure that the outputs of the AI system are marked in a machine-readable format and detectable as artificially generated or manipulated," with exceptions for assistive editing that does not substantially alter the input. The page says it applies from August 2, 2026. | [Article 50, artificialintelligenceact.eu](https://artificialintelligenceact.eu/article/50/). Opened Oct 29, 2026. | **Needs review (law).** A non-official reader site; check the Official Journal text and the Commission's guidance. Not legal advice. |
| California SB 942 covers providers of generative AI systems with over one million monthly users, publicly accessible in California; it requires a latent disclosure detectable by the provider's tool and an option for a visible ("manifest") disclosure, with fines "up to $5,000 per daily violation." Jones Day said it takes effect January 1, 2026. | [Jones Day, Oct 2024](https://www.jonesday.com/en/insights/2024/10/california-enacts-ai-transparency-law-requiring-disclosures-for-ai-content). Opened Oct 29, 2026. | **Needs review (law).** Law-firm summary; the bill text page returned 403. A later amendment (AB 853) reportedly moved the date to August 2, 2026: unverified (search summary only). |

**No public incident found** of a named product shipping unmarked AI images and being called out for it. Searches run: "AI image generator outputs no C2PA content credentials or watermark study 2025," "Grok image generator no watermark no C2PA metadata AI images." Claims about specific generators (such as Grok or Midjourney) shipping no marks came only from search summaries and vendor or resale sites, and are kept out of this page.

## 5. The fix
**The principle:** Every file your product hands out carries two machine marks (a signed manifest and a watermark) and can carry a visible label, and a release test proves it on every path.

**Do this**
1. **Map every output path.** For each model you call or host, list each way a file leaves the product: in-app download, share link, API response, batch export, plugin. Record which marks each path adds today.
2. **Attach a signed C2PA manifest at the last step.** Sign it after resizing, compressing or format conversion, so no later step in your own pipeline drops it. It says the file was made or edited with your AI tool, which tool, and when.
3. **Add a watermark too.** Use the vendor's where it covers your model; on a self-hosted or unmarked model, add one yourself. Two layers, because OpenAI and NIST both say metadata alone can be lost.
4. **Offer a visible label.** Give a visible "AI-generated" or "AI-edited" badge on downloads and public share pages, and make it a clear choice in the export dialog.
5. **Keep personal data out of the marks.** No user name, email or prompt text in the manifest or watermark payload unless the user chooses it (NIST privacy warning).
6. **Test before every release.** Generate a sample from each model and path, then check: does the C2PA check show a valid manifest, and does the watermark detector find the mark? Block the release if any path fails.
7. **Re-test on any model or vendor change.** A new model, a vendor's coverage change or a new export path reopens rule 1.
8. **Say what the file carries.** In the export dialog and help bot, name the marks on the file and that uploads or screenshots can remove them. Give a way to check.

**Reference design: release check per output path**
| Model | Path | Manifest valid | Watermark found | Visible label offered | Result |
|---|---|---|---|---|---|
| Vendor model A | Download (JPEG) | Yes | Yes | Yes | Pass |
| Vendor model B (not covered by vendor) | API response | Yes (own) | Yes (own) | n/a (API) | Pass |
| Self-hosted open model | Share link | No | Yes | Yes | **Block** |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | A customer asks "will these show as AI?": name the marks the file carries first |
| Admit uncertainty and show how to check | A customer asks if the marks will survive a platform upload: say they may not, and point to the verify page |
| Offer choices: 2-4 options plus "Something else", free text open | At export of a public-facing file: "Add AI badge," "Download without badge," "Something else." Don't offer them on internal drafts or when the customer already chose a default |
| Hand off to a person | A customer asks whether the law requires a label in their market: route to support with a pointer to their own counsel; the bot gives no legal answer |

**Don't over-correct.** Do not stamp a large visible label on a customer's real photo after a light fix such as color or crop; the EU text exempts some assistive edits (Needs review), and a false "AI" label misleads too. Do not tell customers a mark "proves" anything or cannot be removed; see [vendor-locked watermarks](../../../../human-machine-interface/goals/ai-slop-detection/failures/provenance-vendor-locked-watermarks.md). Do not put personal data in the marks (rule 5).

**Hand-off rule.** If a release test finds an unmarked path already in production, the release owner pauses that path or adds the marks the same day, and logs which files went out unmarked.

**Framework used:** none yet. Rules 2-3 follow OpenAI's and NIST's two-layer approach; rule 5 follows NIST; rules 1, 4 and 6-8 are our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-images-published-without-ai-label-watermark-or-content-credentials.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | List output paths for each model | Every path listed with its marks | 1 |
| 2 | Download a resized JPEG | Valid manifest still present | 2 |
| 3 | Same file, metadata removed | Watermark still found | 3 |
| 4 | Export a public share page | Visible label offered | 4 |
| 5 | Read the manifest | No user name, email or prompt | 5 |
| 6 | Switch to an unmarked vendor model | Release blocked until own marks added | 6, 7 |
| 7 | Customer asks "will it show as AI?" | Marks named, limits said | 8 |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unmarked-output rate** (primary) | 0 (proposed) | Weekly sample of output files from every model and path, run through a C2PA check and the watermark detector | Any |
| Path coverage | 100% (proposed) | Paths with a passing release check / all paths in the inventory | Below 100% |
| Visible-label offer rate | 100% of public-facing exports (proposed) | Export logs: label choice shown / public-facing exports | Below 100% |
| Personal data in marks | 0 (proposed) | Parse sampled manifests and watermark payloads for user fields | Any |
| Wrong-label complaints (counter-metric) | Track | Support tickets saying a lightly edited real photo was labeled AI | Rising month over month |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Sampled output with no manifest and no watermark | Release test or weekly sample | The file was checked after a third party re-saved it |
| A model or export path in production with no release-check row | Path inventory joined to deploy log | Path is internal-only and never reaches customers |
| Model or vendor version changed with no new release check | Deploy log | Vendor change was to a non-image model |
| Public share page served with no label choice logged | Export log | The customer set a saved default |
| Help-bot reply to "will it show as AI?" with no marks named | Chat transcript | Customer asked about something else |

**Starter rule:** no model or export path goes to production until a sample file from it shows a valid C2PA manifest and a detectable watermark.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-images-published-without-ai-label-watermark-or-content-credentials
runs: [pre_release, post_generation, pre_send]
reads: [model.id, model.vendor_coverage, export.path, file.c2pa_manifest_valid, file.watermark_detected, export.label_choice, manifest.fields, chat.reply_text]
trigger: unmarked sample file, path with no release check, model change with no re-test, public export with no label choice, or customer asks whether output shows as AI
moves: [lead_with_answer, admit_uncertainty, offer_choices, hand_off]
choices: ["Add AI badge", "Download without badge", "Something else"]
on_miss: block_release
metric: unmarked-output rate
counter_metric: wrong-label complaints
status: proposed
```

## 8. Related patterns
- [Watermarks only readable by the vendor that made them](../../../../human-machine-interface/goals/ai-slop-detection/failures/provenance-vendor-locked-watermarks.md) - the closest existing page. It covers the checker's side (a reviewer reads "no watermark found" as "not AI"); this page covers the builder's side (the product never added a mark).
- [Platforms rely on self-declared AI labels](../../../../human-machine-interface/goals/ai-slop-detection/failures/provenance-self-declared-labels.md) - the platform's label system downstream; this page is why many files reach it with nothing to read.
- [No record of the prompt, model and approver](../../ai-image-generation-business-risks/failures/no-record-of-prompt-model-and-approver-for-ai-images.md) - an internal record kept by the business; this page is about marks carried in the file itself.
- [AI-generated ad disclosure rules by market](../../ai-image-generation-business-risks/failures/ai-generated-ad-disclosure-rules-not-met.md) - a brand's per-market label duty for ads; this page is the product's duty to mark every output.
- [Generation artifacts](../../generation-artifacts/README.md) and [AI governance failures](../../../../../cross-cutting/governance/README.md) - the older image goal and the cross-cutting governance pages.

## 9. Common questions
### Do AI image APIs add a watermark automatically?
Not always. OpenAI says its API image outputs carry Content Credentials and SynthID, except for some models it plans to retire, including gpt-image-1. Check your vendor's page for your exact model and test a file.

### Is Content Credentials metadata enough?
No. OpenAI says platforms, editing tools and file conversions may remove metadata. Pair it with a watermark, and offer a visible label people can see without a tool.

### How do I watermark images from an open-source model I host?
The model adds no vendor mark, so add your own watermark and manifest in your pipeline, then test that they survive your export. Hu et al. show that one in-model watermark could be removed by fine-tuning, so do not treat any one mark as proof.

### Does the law require me to label AI images?
It may. The EU AI Act Article 50 and California's SB 942 set marking duties for some providers. Whether they cover your product is a question for a qualified lawyer; this page is not legal advice.
