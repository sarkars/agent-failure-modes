# Plan: Image and Video Generation Failures

> **Status: proposed plan, 2026-10-29.** Asked for by the owner. Nothing here is written, built or published yet. This work is an independent part of the failure pattern library; the chat library stays the first priority. No statistic, quote or study is used in this plan; every fact a page uses later comes from a source opened at the time it is written.

## 1. What the work is
Failure pages for products that **make** images and video with AI: text-to-image, image editing and inpainting, image-to-video and text-to-video. Each failure gets a page in the same shape as the chat library: what it looks like, why it happens, how to fix it, and a short test that shows the fix holds. Real incidents back the pages.

**Where the pages go (owner, 2026-10-29: reuse existing).** No new category. The pages go into the existing [vision-and-images](../vision-and-images/README.md) category, which already covers models that read images and has a [Generation Artifacts](../vision-and-images/goals/generation-artifacts/README.md) goal. This folder holds only this plan; it gets no README, so the site never publishes it as a category. Topics that apply to every AI system stay in `cross-cutting/` and are linked, not copied.

**Image and video stay together.** Most failures are the same for both. Each new page states which it covers: image, video, or both.

The last phase adds a free check page for readers who want to know whether an image or video carries signs of AI generation (section 7). It comes after the failure pages.

## 2. What already exists
[vision-and-images, goal Generation Artifacts](../vision-and-images/goals/generation-artifacts/README.md) has 7 short pages in the older format (Issue, Mitigation, References):

| Existing page | Use in this work |
|---|---|
| [Artifact Accumulation in Regeneration](../vision-and-images/goals/generation-artifacts/failures/artifact-accumulation.md) | Covers part of goal C |
| [Consistency Failure: Identity Loss Across Generations](../vision-and-images/goals/generation-artifacts/failures/consistency-failure.md) | Covers part of goal C |
| [Model Collapse in Generation](../vision-and-images/goals/generation-artifacts/failures/model-collapse.md) | Model training, not a product failure; link only |
| [Quality Drift in Generated Images](../vision-and-images/goals/generation-artifacts/failures/quality-drift.md) | Covers part of goal B |
| [Safety Filter Bypass in Image Generation](../vision-and-images/goals/generation-artifacts/failures/safety-filter-bypass.md) | Covers part of goal E |
| [Semantic Drift in Generated Images](../vision-and-images/goals/generation-artifacts/failures/semantic-shift.md) | Covers part of goal A |
| [Token Limit Artifacts in Conditional Generation](../vision-and-images/goals/generation-artifacts/failures/token-limit-artifacts.md) | Covers part of goal A |

Other existing goals reused: [Multi-Image Understanding](../vision-and-images/goals/multi-image-understanding/README.md) for identity across frames when a model reads video, and [Adversarial Robustness](../vision-and-images/goals/adversarial-robustness/README.md) for the prompt tricks behind filter bypass.

Rules: never move, rename or delete these pages (their URLs are live). New pages link to them instead of repeating them. Where a new page and an old one cover the same failure, the overlap goes to a person as a merge proposal, marked Needs review. The [vision-and-images README](../vision-and-images/README.md) states figures with no source (for example a 20 to 40 point calibration gap); that is logged for a person to check, not copied here.

## 3. Goals and first patterns
Nine groups. Pattern names are working titles; each becomes a page only after a source is found (section 5). A pattern with no public source is dropped, not written from general knowledge.

Placement in vision-and-images: A, B and C go into the existing `generation-artifacts` goal. D to I are new goal folders under `vision-and-images/goals/` (working names `generation-representation`, `generation-likeness-and-harm`, `generation-provenance`, `generation-copyright`, `generation-business-use`, `generation-brand`), because the category has no goal for them.

**A. The output does not match the request (prompt adherence)**
- Wrong count of objects
- Wrong placement (left and right, on and under, in front and behind)
- Attributes attached to the wrong object (the red hat ends up on the other person)
- Text inside the image misspelled or garbled
- Negative requests ignored ("no people" still shows people)
- Edit changes parts of the image the user did not ask to change

**B. The output is broken (visual quality)**
- Wrong anatomy: hands, fingers, teeth, limbs
- Impossible objects and physics: melted shapes, broken reflections and shadows
- Video motion that breaks physics: objects pass through each other, liquids and gravity behave wrongly

**C. The output does not stay the same across frames or images (consistency)**
- A person's face, clothes or body change between frames or shots
- Objects appear, vanish or change between frames
- Flicker and texture crawl in video
- A character or product is not the same across a set of images

**D. People are shown wrongly (representation and accuracy)**
- Stereotyped defaults when the request names no detail (who appears as a doctor, a nurse, a criminal)
- Historically wrong images from a diversity rule applied without context
- Real places, flags, logos and documents shown wrongly but presented as accurate

**E. Fake images of real people (likeness, personality abuse, harm)**
- Sexual or degrading images of a real person made without consent
- Realistic images of real people in false events (public figures, elections, news)
- Fake endorsements: a celebrity or public figure shown promoting a product or scam they never backed
- Executive impersonation: a fake image or video of a company leader used to order payments or move markets
- Harassment and bullying with fake images of private people (classmates, coworkers, ex-partners)
- Images of a named person made from a few uploaded photos, with no check that the uploader has consent
- Deceased people recreated without the estate's consent
- Safety filters bypassed by rewording (links to the existing page)
- Harmless requests refused (over-refusal), including refusals that differ between equivalent requests

**G. Copyright, trademark and ownership**
- Copyrighted characters and scenes reproduced on request, or without being asked
- Near-copies of training images, including stock-photo watermarks showing in outputs
- An artist's distinctive style copied by name
- Trademarks and logos placed in outputs (brand confusion, false affiliation)
- Training on images without permission or against a site's terms (lawsuit side, linked, not argued)
- Unclear ownership: a company assumes it owns or can register an output it may not
- Vendor terms or indemnity that do not cover how the business uses the output

**H. Business use (corporate failures)**
- Product shown with features, sizes or results it does not have (false advertising risk)
- AI images in ads, listings or reports published without review or disclosure
- Public backlash when a brand replaces artists, models or photographers with AI images
- Confidential material (unreleased products, customer photos, internal documents) uploaded to an outside image tool
- Cultural, religious or local errors in images made for other markets
- Employees' or models' likeness reused beyond what they agreed to
- Fake receipts, IDs, damage photos or documents made with generators to defraud a business (insurance, refunds, expenses, account checks)
- Regulated claims in images: health, finance or food results, before-and-after shots
- Required disclaimers missing or unreadable in the image
- Age-restricted products (alcohol, gambling) shown with people who look underage
- AI disclosure rules of each market not met
- Ad platforms rejecting AI-made creative or requiring a label
- No model release or likeness rights for generated people who resemble real people
- Text baked into images with no alt text (accessibility)
- An approved image cannot be made again: same prompt, different output
- The vendor updates its model and the approved style changes
- No record of the prompt, model, settings and approver behind a published asset
- No approval step: anyone who generates an image can publish it
- Uploaded brand assets used to train the vendor's model
- Employees using image tools the company has not approved
- Vendor terms, prices or model retirement changing under a live campaign
- Regenerations and video runs costing far more than budgeted
- Text in images not translated, in the wrong script, or laid out wrong for right-to-left languages
- A visible AI mistake in an ad spreading widely (extra fingers on a model)

**I. Brand guidelines**
- Brand rules broken: logo distorted, recolored or crowded, wrong fonts, colors, tone or photo style
- Competitor logos, products or look appearing in the output
- Brand shown next to unsafe content (sexual, violent, political)
- Garbled text on packaging, labels or signs in product shots
- Brand reference images or style guides ignored by the generator
- A campaign where the product looks different from image to image (links to goal C)

**F. The output cannot be traced (provenance and labeling)**
- No AI label, watermark or Content Credentials on the output
- Credentials or metadata stripped when the file is edited, resized or uploaded
- A label that misleads: real photos flagged as AI, or AI images that pass as real

Links out: E links to `cross-cutting/security` and `cross-cutting/governance`; F and G link to `cross-cutting/governance`; H and I link to `by-use-case/content-marketing` and, for document fraud, to `by-use-case/insurance` and `by-use-case/financial-services`; voice cloning stays in `speech-and-audio` and is linked from E and F.

Statements about law in goals E, F, G and H (consent, likeness rights, copyright, trademark, advertising, election rules, labeling duties) stay **Needs review** by a qualified person.

## 4. Page format
New pages use the chat library's pattern template ([hmi-pattern.md](../human-machine-interface/_templates/hmi-pattern.md)) adapted for media: a symptom a user can see, the cause, the fix inside the product (prompt rewriting, guidance settings, reference images, filters, labeling), and a short test with a pass line and a fail line. Tests are prompts or edit requests a team can run on their own generator; results stay "Not yet run" until a run is recorded.

Folder layout is the one vision-and-images already uses, so the site importer picks pages up without a code change: `goals/<goal>/failures/<pattern>.md` and a `README.md` per goal. New goal READMEs for D, E and F are written with their first pages. The vision-and-images README gets the new goals and counts added at the end of phase 2.

## 5. Sources and incidents
- Every page needs at least one source opened and read at the time of writing: an incident report from a named outlet, a vendor's own documentation or policy, a court filing, or a paper. Search summaries alone are not enough.
- No statistic, quote or study unless it appears in an opened source, with the source named next to it.
- Incident candidates to research first. These are leads only, named here so they are not forgotten; none has been opened for this plan and each must be checked before use:
  - Google pausing Gemini's images of people in February 2024 (goal D)
  - Sexual deepfake images of Taylor Swift spreading in January 2024 (goal E)
  - Grok image generation and editing controversies (goal E)
  - Lawsuits by studios, artists and Getty Images against image generator makers (goal G)
  - A Hong Kong company employee paying out after a video call with deepfaked executives, reported in early 2024 (goals E and H)
  - Deepfake celebrity ads, for example a fake Tom Hanks dental plan ad he warned about in 2023 (goal E)
  - The Glasgow "Willy Wonka" event in 2024 whose AI-made ads did not match the real event (goal H)
  - Backlash to AI-made brand holiday ads in 2024 (goal H)
- Pages and incidents are marked Needs review until a person approves them.

## 6. Phases
| Phase | Work | Done when |
|---|---|---|
| 1 | Search for sources for each pattern in section 3; drop patterns with none; list kept patterns with their sources in this plan | Every kept pattern has at least one opened source |
| 2 | Write pages, highest-harm first (E, then G, H, I, D, F, A, C, B), into vision-and-images; new goal READMEs for D to I; update the vision-and-images README goal table and counts | Pages pass the five check scripts |
| 3 | Incident pages for the candidates in section 5 that check out | Each incident links to its patterns |
| 4 | Publish: the site importer picks up the new pages in the existing category; check the build and that no live URL is lost | New pages live; public URL list updated |
| 5 | Layer 1 check page (section 7) | Page live and tested on files with and without Content Credentials |

## 7. Last phase: Layer 1 check page
A free page on the site where a reader drops an image or video and sees which signals of AI generation it carries. It runs in the reader's browser; the file is never uploaded. It shows signals, never a "fake" or "real" verdict.

- **Content Credentials (C2PA):** read with the open-source `@contentauth/c2pa-web` library: who signed it, which tool made it, whether it says AI made it, and whether the signature is valid.
- **File metadata:** camera make and model, editing software, the IPTC "digital source type" field, and prompts that some generators write into PNG files.
- **Reverse image search:** links to Google Lens, TinEye and Bing Visual Search, with a note that using them sends the image to that service.
- **Always shown:** missing signals prove nothing. Most real photos and most AI images carry neither credentials nor revealing metadata, and metadata is easy to strip or fake.

Paid detection APIs (Layer 2) are not planned.

## 8. Owner decisions
1. Who writes the pages. **Answered (owner, 2026-10-29): the hourly run, as its Part M, doing as much per run as the rules allow** (all goals sourced in parallel in phase 1, up to 6 pages per run in phase 2, up to 2 incidents per run in phase 3). Part D publishes only media pages the run added or changed (deploy.md step 5b). Phase 5 is not in the hourly run; it waits for the owner. Status per phase is tracked in section 6.
