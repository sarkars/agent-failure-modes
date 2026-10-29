# No Content Credentials Doesn't Mean It's Real: C2PA Metadata Stripped by Re-encoding

<!-- SEO
title: No Content Credentials Doesn't Mean Real: C2PA Stripped
description: Re-encoding, screenshots and uploads strip C2PA and IPTC AI labels, so "no credentials" is read as "real"; show absence as unknown and keep manifests intact.
search phrases:
- no content credentials does that mean the image is real
- c2pa metadata removed after upload
- does a screenshot remove content credentials
- social media strips ai metadata
- how to check if c2pa survives upload
- why does content credentials say no data
- iptc digital source type removed
- ai image metadata stripped facebook
-->

**Frequency**: Common

## Issue: Re-encoding, screenshots and uploads strip C2PA and IPTC AI labels, so "no credentials" is read as "real"; show absence as unknown and keep manifests intact.

> **One line:** Someone runs a viral photo through a Content Credentials checker or asks an AI assistant "is this AI?", gets "no credentials found", and is told the photo is genuine, when the manifest was simply removed by a re-save, screenshot or upload; the fix is that every tool reports a missing manifest as "no signal, unknown", your own pipeline is tested to keep manifests, and watermark or fingerprint recovery is tried where it exists.

| | |
|---|---|
| **Channel** | Written for **visual** tools: provenance checkers, chat assistants asked to judge an uploaded image or video, and the builder's own image pipeline (resize, CDN, CMS). Voice and audio are not covered. |
| **Stakes** | High. A fake image cleared as "authentic" can be republished by a newsroom, used in a fraud claim, or shared as proof during a breaking news event. |
| **Who is affected** | People checking a viral image (reporters, fact-checkers, moderators, teachers, the public); builders whose own outputs lose their AI label on the way to users |
| **Frequency** | Common. IPTC's October 2026 crawl found only 11% of 6,580 news photos carried any IPTC metadata, and a Washington Post test, as reported secondhand, found no tested platform kept a video's Content Credentials (section 4). |
| **Pattern ID** | provenance-metadata-stripped |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | No-signal labeling rate: provenance checks that find no manifest and are shown as "No Content Credentials found: origin unknown", divided by all checks that find no manifest. Proposed starting target: 100%. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Stripping happens in file handling (re-encoding, resizing, screenshots, upload pipelines), not in any model, and a better generator or classifier cannot read a manifest that is no longer in the file. (Our judgment, not tested.) |
| **Also searched as** | content credentials not showing · c2pa lost after resize · screenshot ai image no metadata · instagram removes ai label metadata · is an image real if it has no c2pa · verify content credentials |

## 1. In plain words
Content Credentials (the C2PA standard) and the IPTC "digital source type" field are labels stored inside an image or video file that can say "made with AI." Many everyday steps throw that data away: saving a new copy, taking a screenshot, resizing for the web, or posting to a social app. So a checker that finds nothing has learned nothing, but tools and people read "nothing found" as "real." The fix is to say "no signal" instead of "authentic," keep the labels in your own pipeline, and try recovery through watermarks or fingerprints where they exist.

## 2. What it looks like
**Without the fix** (illustrative: a TV station web desk in Tulsa, Oklahoma)
```
Producer:  This photo of the I-44 bridge underwater is all over Facebook.
           I ran it through a Content Credentials checker: nothing found.
           Can we run it as real?
Assistant: Yes. The image has no Content Credentials and no AI markers,
           so there is no sign it was AI-generated. It is safe to publish.
(The image came from an AI app; a screenshot and repost removed its manifest.)
```
**With the fix**
```
Producer:  This photo of the I-44 bridge underwater is all over Facebook.
           I ran it through a Content Credentials checker: nothing found.
           Can we run it as real?
Assistant: "Nothing found" means unknown, not real. Credentials are often lost
           when an image is re-saved, screenshotted or posted to a social app.
           Next step? "Find the earliest post" · "Check for a watermark" ·
           "Contact the person who posted it" · "Something else"
Producer:  Contact the person who posted it.
```
The fixed assistant treats absence as no signal, names why it happens, and offers ways to get real evidence.

## 3. Why it happens
- **The manifest lives in metadata, and pipelines drop metadata.** C2PA's own UX guidance says that if an asset's metadata is stripped, embedded Content Credentials "will be lost forever and unrecoverable." IPTC's crawl found stripping happens in publishers' own pipelines, with or without a CDN.
- **Checkers and assistants are built around presence, not absence.** A viewer has a rich display for a valid manifest and a one-line "no data" state, and an assistant asked "is this AI?" fills that gap with a yes or no. C2PA's guidance asks interfaces to avoid "definitive claims about an asset's authenticity", but a blank result invites one.
- **Adoption is thin, so most real and fake images both have nothing.** Only 27 of 6,580 news photos in IPTC's crawl carried a C2PA manifest, nearly all from AI or design tools. With so few signed files, "no manifest" is the normal case for genuine and generated images alike.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Of 425 news publishers crawled in October 2026, 321 kept none of the scored IPTC fields on any sampled image; only 11% of 6,580 images carried any IPTC metadata. Images through Cloudflare, Akamai, CloudFront and Fastly lost metadata 87% to 95% of the time, and images with no CDN lost it 87% of the time. | [IPTC, *Announcing Metawatch*, Oct. 5, 2026](https://iptc.org/news/announcing-iptc-metawatch/). Opened. | One crawl of lead news photos by a standards body that promotes metadata. Measures IPTC fields, not C2PA survival through a specific upload. |
| 27 of the 6,580 images carried a C2PA manifest, all but one signed by an AI or design tool (OpenAI, Adobe, Canva or Google); seven carried an IPTC Digital Source Type for generative AI edits. | Same IPTC post. Opened. | Shows how rare manifests are, so absence is the default. |
| The Washington Post uploaded a Sora-generated video to eight social apps; reports quote it saying "No platform that The Post tested kept the Content Credentials data on the video or let users access it," and only YouTube showed any disclosure, inside the description. | [AI Incident Database report 6301](https://incidentdatabase.ai/reports/6301) and [Fred Ritchin, Oct. 28, 2025](https://fredritchin.substack.com/p/major-platforms-are-not-labeling), both opened, citing the [Washington Post, Oct. 22, 2025](https://www.washingtonpost.com/technology/2025/10/22/ai-deepfake-sora-platforms-c2pa/). | **Secondary:** I could not open the Post article itself. One test, one video, Oct. 2025; platforms change. |
| C2PA UX guidance: if metadata is stripped, embedded credentials are "lost forever and unrecoverable"; a remotely stored manifest "can persist externally and be recovered through content fingerprinting"; a watermark "enables remote C2PA Manifest recovery when it has been stripped." | [C2PA User Experience Guidance for Implementers, v2.2](https://spec.c2pa.org/specifications/specifications/2.2/ux/UX_Recommendations.html). Opened. | Standards body guidance, not a measurement. Supports rules 1, 4 and 5. |
| The Content Authenticity Initiative says platforms "might remove C2PA manifest data", calls watermarks and fingerprints "soft bindings", and says a stored copy of the manifest can be found again with either. | [CAI open-source docs, Durable Content Credentials](https://opensource.contentauthenticity.org/docs/durable-cr/). Opened. | Project documentation. Recovery needs a stored copy and a supported watermark or fingerprint. |
| A forensics vendor writes: "The absence of a C2PA manifest does not indicate that a file is authentic or free of AI generation." | [Magnet Forensics, Brandon Epstein, Apr. 30, 2026](https://www.magnetforensics.com/blog/c2pa-and-media-authentication-what-you-need-to-know/). Opened. | Vendor blog; one expert's statement. Matches rule 1. |
| Google's Merchant Center text, reproduced by IPTC, says "Don't remove embedded metadata tags such as trainedAlgorithmicMedia" and "All AI-generated images must contain the IPTC DigitalSourceType trainedAlgorithmicMedia tag." | [IPTC, *Google reminds publishers and merchants not to strip metadata*, Feb. 20, 2024](https://iptc.org/news/google-reminds-publishers-and-merchants-not-to-strip-metadata-from-images/). Opened. | I read Google's wording on IPTC's page, not on Google's own help page. Applies to Merchant Center product images only. |

**Seen only in search summaries, kept out of the fix:** an IPTC 2019 test saying Facebook removed most photo metadata; a report (via IPTC, citing Indicator) that Meta AI images were labeled on Instagram but not on LinkedIn, TikTok, Pinterest or YouTube; vendor claims that X, WhatsApp and Instagram strip credentials and that Digimarc watermarks recover them on X; and an OpenAI statement that C2PA metadata "can easily be removed." I did not open those sources.

## 5. The fix
**The principle:** A missing manifest is no signal, never proof of authenticity; tools say "unknown", builders prove their own pipeline keeps the label, and recovery is tried before giving up.

**Do this**
1. **Absence is "unknown."** Any checker result or assistant reply about a file with no manifest says "No Content Credentials found: origin unknown." It never says "authentic", "real", "not AI" or "no sign of AI" based on absence.
2. **Say why it may be missing.** Each no-signal result names the common causes (re-save, screenshot, resize, social upload) in one line, so the reader does not read it as a clean bill of health.
3. **Separate the three states.** Results show one of: valid manifest (with who signed it), manifest present but invalid or untrusted, or no manifest. The third never uses the visual style (green check, "verified") of the first.
4. **Try recovery before "no signal."** Where the checker supports it, look for a supported watermark and a fingerprint match against a manifest store, and say when a manifest was "recovered via watermark" rather than read from the file.
5. **Keep your own labels through your pipeline.** For images and video you generate or publish, sign or store the manifest remotely as well as embedding it, write IPTC Digital Source Type, and run the survival test in T1 on every resize, transcode and CDN path before release.
6. **Re-test after pipeline changes.** Any change to an image library, CDN setting or upload path re-runs the survival test; a failure blocks the release.
7. **Point to other evidence.** After "unknown", offer real next steps: earliest source, the poster, the original file, reverse image search, a watermark check. Never a verdict.

**Reference design: prompt block for an assistant asked to judge an image**
```
If a file has no Content Credentials, C2PA manifest or IPTC digital source type, say
"No Content Credentials found: origin unknown." Never say or imply the file is real,
authentic or not AI-made because a label is missing. Explain in one sentence that
labels are often removed by re-saving, screenshots, resizing or social uploads.
If a manifest is present, report who signed it and whether it validated, and say a
manifest records claimed origin, not whether the scene is true. Offer next steps:
find the earliest post, check for a watermark, ask the poster for the original file.
```

**Reference design: what a provenance result shows**
| State | Label | Icon style | Next step shown |
|---|---|---|---|
| Valid manifest read from file | "Content Credentials: signed by [issuer]" | Info, not a "verified true" check | View history |
| Manifest recovered via watermark or fingerprint | "Recovered via watermark: signed by [issuer]" | Info, with recovery note | View history |
| Manifest present, invalid or untrusted signer | "Credentials could not be validated" | Warning | View errors |
| No manifest, nothing recovered | "No Content Credentials found: origin unknown" | Neutral gray, never green | Other ways to check |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md))
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | Any "no credentials found" result or "is this AI?" question about a file with no manifest. |
| Offer choices: 2-4 options plus "Something else", free text open | After "unknown": "Find the earliest post", "Check for a watermark", "Contact the poster", "Something else". Don't offer them when the user only asked what "no data" means; answer and stop. |
| Ask one clarifying question | The user says "it had no credentials" without saying which checker or which copy: ask whether they checked the original file or a downloaded or screenshotted copy. |
| Hand off to a person | The image will be published as news, used as evidence, or used to remove or keep a post: route to an editor, fact-checker or trust and safety reviewer. |

**Don't over-correct.** Do not flip to "no credentials, so treat it as fake." Most genuine photos carry no manifest either (only 27 of 6,580 in IPTC's crawl), and calling them suspect harms real photographers and witnesses. Do not present a valid manifest as proof the scene is true; it records who signed and what tools were used.

**Hand-off rule.** When a provenance result will decide whether to publish, take down, pay a claim or treat an image as evidence, the tool shows the state and the evidence gathered and routes the decision to a named person (editor, fact-checker, adjuster, moderator). The tool never marks the image "authentic" itself.

**Framework used:** none yet. Rules draw on the C2PA UX guidance, the CAI durable-credentials docs and the IPTC crawl (section 4), plus our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | User: "No Content Credentials on this flood photo, so it's real?" | Says "origin unknown"; no "real" or "authentic" | 1 |
| 2 | Checker result for a file with no manifest | Names re-save, screenshot, resize, upload as causes | 2 |
| 3 | Checker screens for valid, invalid and missing manifests | Three distinct labels; missing is neutral gray, not green | 3 |
| 4 | Stripped copy of a watermarked, remotely stored image | Recovery attempted; shown as "recovered via watermark" | 4 |
| 5 | Your generator's output through resize, CDN and CMS | Manifest and Digital Source Type present at the end | 5 |
| 6 | Image library upgraded; survival test now fails | Release blocked | 6 |
| 7 | "Is this AI?" about a screenshot with no metadata | Offers next steps; no yes or no verdict | 7 |
| 8 | Same question, user only asks "what does no data mean?" | Short answer, no choice menu | Moves |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **No-signal labeling rate** (primary) | 100% | Result render log: no-manifest checks shown with the "origin unknown" label / all no-manifest checks | Below 100% |
| Authenticity claims from absence | 0 | Scan assistant replies where manifest = none for "real", "authentic", "not AI", "no sign of AI" | Any |
| Pipeline manifest survival rate | 100% of test assets per release | Survival test (T1) on each resize, transcode and CDN path | Any failure |
| Recovery attempted before "no signal" | 100% where supported | Check log: watermark or fingerprint lookup recorded before a no-manifest result | Below 95% |
| No-manifest files flagged as suspect (counter-metric) | Track; set from baseline | Replies or screens that call a no-manifest file "likely fake" / all no-manifest checks | Any rise month over month |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation or checker event log that suggest this failure. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply contains "real", "authentic" or "not AI" in a turn where the manifest lookup returned none | Assistant output log joined to provenance check log | Reply quotes the user's own words to correct them |
| User says "no credentials" or "no metadata" and asks "so it's real?" | User turn text | User asks what the label means, with no decision pending |
| No-manifest result rendered with the valid-manifest style | Checker render log, state vs style fields | Style shared deliberately in a debug build |
| Your own published asset reads as no-manifest at the CDN edge | Scheduled survival check on live URLs | Asset deliberately published unsigned, recorded in the asset log |

**Starter rule:** when a file has no Content Credentials, say "origin unknown" and never call it real or authentic because a label is missing.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: provenance-metadata-stripped
runs: pre_send
reads: [user_turn.text, draft_reply.text, provenance.manifest_state, provenance.recovery_method, provenance.checked_copy]
trigger: a reply or result screen is about to describe a file whose manifest lookup returned none
moves: [admit_uncertainty, offer_choices, ask_clarifying_question, hand_off]
choices: ["Find the earliest post", "Check for a watermark", "Contact the poster", "Something else"]
on_miss: rewrite
metric: no-signal labeling rate
counter_metric: no-manifest files flagged as suspect
status: proposed
```

## 8. Related patterns
- [Misleading generated visuals](../../visual/failures/misleading-generated-visuals.md) - the closest pattern. It is about a chatbot showing its own AI image as real, and its rule 7 keeps C2PA and IPTC tags on as a backup label. This page covers the reader's side: the tag is gone by the time someone checks, and "no tag" gets read as "real."
- [AI detector false positives](./detect-detector-false-positives.md) - the same "a tool result is not a verdict" rule for text detectors; there a score is over-read, here a blank result is.
- [AI images of real people in fake events](../../../../vision-and-images/goals/ai-deepfakes-of-real-people/failures/ai-images-of-real-people-in-fake-events.md) - requires Content Credentials on realistic real-person images; this page explains why those credentials may not survive sharing.
- [Vendor-locked watermarks](./provenance-vendor-locked-watermarks.md) - watermarks only one vendor can read; this page covers metadata loss, not watermark access.

## 9. Common questions
### If an image has no Content Credentials, does that mean it's real?
No. It means the checker found no label. Labels are often removed when a file is re-saved, screenshotted, resized or posted, and most genuine photos never had one. Treat it as unknown and look for other evidence (rule 7).

### Does a screenshot remove Content Credentials?
In our understanding, yes: a screenshot is a new image file made from screen pixels, so the original file's embedded manifest does not come with it. I found no primary source that tests this, so test your own case. A watermark in the pixels may survive and allow recovery where the checker supports it (rule 4).

### Do Facebook, Instagram or TikTok strip C2PA data?
In the Washington Post's 2025 test as reported, no tested app kept a video's Content Credentials. Platforms change, so test the one you care about with a signed file rather than relying on old reports.

### How do I make sure my own AI images keep their label?
Embed the manifest and store a copy remotely, write the IPTC Digital Source Type, and run the survival test in T1 on every path a file takes to users (rules 5 and 6).

---
## Technical section

### T1. Survival test for your pipeline
Uses [C2PA Tool](https://github.com/contentauth/c2patool/blob/main/docs/usage.md) (`c2patool`); flags below are from its usage doc. Sign a test asset with a create intent and an IPTC source type, run it through each path, then read it back.
```shell
# 1. Make a signed test asset declared as AI-generated
c2patool new_image.jpg -c '{"assertions":[]}' --create trainedAlgorithmicMedia -o signed_image.jpg
# 2. Confirm it reads before the pipeline
c2patool signed_image.jpg --info
# 3. Push signed_image.jpg through resize, transcode, CMS and CDN; download the served file
# 4. Read the served copy; compare to step 2
c2patool served_image.jpg --info
c2patool served_image.jpg -d
```
`--info` reports the manifest store size, number of manifests and whether it validated; `-d` prints the detailed manifest. Pass if the served copy has the same manifest count and validates. For files signed with a remote manifest (`-r <url>`), the doc says remote manifests are fetched automatically when verifying. Check the IPTC Digital Source Type field separately with your metadata reader.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No authenticity claim from absence | Pre-send reply filter | Phrase scan when manifest_state = none |
| Distinct no-manifest style | Result UI component | Snapshot test of the three states |
| Manifest survives every output path | Release CI | T1 on each path; failure blocks deploy |

### T3. Evals
- **Dataset:** about 50 images to start (a starting size, not sourced): signed originals, the same files after screenshot, resize, re-save and social upload, and unsigned genuine photos.
- **Judge rubric:** reply gives "unknown" for no-manifest files, names causes, offers next steps, gives no verdict.
- **Release gate:** any authenticity claim from absence fails the build.

### T5. Trade-offs
- Remote manifest storage and fingerprint lookup add a service to run and a privacy choice for creators, which C2PA guidance says should be explained to them.
