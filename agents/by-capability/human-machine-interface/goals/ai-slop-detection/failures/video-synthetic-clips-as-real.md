# How to Tell if a Video Is AI Generated: Fake AI Clips Passed Off as News Footage or Ads

<!-- SEO
title: How to Tell if a Video Is AI Generated: Fake News Clips
description: AI clips of storms, bodycam stops and news reports get shared as real footage. Check the source and provenance, not the look, before airing or approving.
search phrases:
- how to tell if a video is ai generated
- is this video real or ai
- fake ai bodycam video
- sora fake news video
- ai generated hurricane videos fake
- how to spot ai video sora veo
- ai video passed off as real footage
- fake ai news report video ad
-->

**Frequency**: Common

## Issue: AI clips of storms, bodycam stops and news reports get shared as real footage. Check the source and provenance, not the look, before airing or approving.

> **One line:** A producer, moderator or ad reviewer decides a viral clip of a flooded street, a police bodycam rescue or a "breaking news" segment is real because it looks real and carries no watermark, or fake because one frame glitches; the fix is a rule that the look of a clip never decides, a watermark or provenance hit counts only as a positive AI signal, and every clip that will air, stay up as news or run as an ad passes a logged source check first.

> **Read this first:** The YouTube labeling rules below summarize the platform's own help page as read on October 29, 2026. A platform rule is not a law, and this page is design guidance, not legal advice. Anyone setting a labeling or disclosure policy needs review by a qualified person.

Status: Needs review

| | |
|---|---|
| **Channel** | Written for **text and workflow**: the newsroom clip log, the trust-and-safety review queue, the ad review queue, and a reviewer's chat with an AI assistant asked "is this video real?". **Planned for visual**, not written or measured: frame-level forensics and detector scores. |
| **Stakes** | High. A fake storm clip can bury real warnings during a disaster; a fake bodycam or news segment can spread a false crime story or sell a scam. |
| **Who is affected** | Newsroom producers and fact-checkers, platform moderators, ad reviewers, and the viewers who see a synthetic scene presented as footage |
| **Frequency** | Common, in our judgment. AFP surfaced "dozens" of fake Hurricane Melissa clips in one storm, and Lead Stories rated two US fake bodycam clips false in 2026 (section 4). I found no count of how often reviewers clear such clips. |
| **Pattern ID** | video-synthetic-clips-as-real |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Source-checked clip rate: video clips aired, kept up as news or approved as ads that have a logged source check (earliest upload, uploader, independent confirmation or provenance read), divided by all such clips. Proposed starting target: 100% (tune). |
| **Maturity** | Researched (see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | No. Each new video model removes the glitches reviewers look for, and visible watermarks can be cropped, so the defense is a source check that does not depend on how the clip looks. (Our judgment, not tested.) |
| **Also searched as** | is this video AI · Sora watermark removed · AI hurricane video fake · fake bodycam footage AI · AI news anchor scam ad · check if video is real |

## 1. In plain words
Text-to-video tools such as Sora and Veo make short clips that look like phone footage, bodycam video or a TV news segment. Reviewers judge them by eye: no watermark and no glitch means "real", a melted hand means "fake". Studies show people are often wrong this way, and watermarks are easy to remove. The fix is to treat a clip's look as no evidence, read any watermark or provenance data that is there, and confirm the clip's source before it airs, stays up as news or runs as an ad.

## 2. What it looks like
**Without the fix** (illustrative: a TV station web desk in Tampa, Florida, during a hurricane)
```
Producer:  Viewer sent a clip: sharks swimming down a flooded street in St. Petersburg. Real?
Assistant: It looks authentic. The water motion is natural, there is no Sora or Veo
           watermark, and the lighting matches a storm. I'd call it likely real.
Producer:  Great, it leads the 5 p.m. web update.
(The clip was AI-made; the watermark had been cropped. It aired.)
```
**With the fix**
```
Producer:  Viewer sent a clip: sharks swimming down a flooded street in St. Petersburg. Real?
Assistant: I can't tell from how it looks, and a missing watermark doesn't mean real.
           Before it runs, one source check has to pass. Which can you do now?
           1) Find the earliest upload and who posted it  2) Ask the viewer for the original file
           3) Run a provenance or SynthID check  4) Something else
Producer:  Earliest upload is an account that posts AI storm videos.
Assistant: Then it doesn't run as footage. Logged as "AI-generated, source: AI account".
```
The fixed assistant refuses to judge by look, offers source checks, and logs the result before anything airs.

## 3. Why it happens
- **The glitch hunt fails on good clips.** In a 2025 study, people judging Veo 3 and other clips were right 60% of the time overall and only 43% on text-to-video clips, below a coin flip. Reviewers trained on "extra fingers" have little to go on.
- **The watermark is read both ways.** NewsGuard removed Sora's watermark "in approximately four minutes" with a free tool, so "no watermark" proves nothing; and AFP found viewers believed storm fakes even with the Sora mark on them. A visible mark is weak in both directions.
- **Familiar formats borrow trust.** NewsGuard found most of its Sora fakes were news broadcasts with "an apparent news anchor"; fake bodycam clips copy the Axon timestamp overlay. Reviewers trust the format before they check the source.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Sora 2 made videos advancing 16 of 20 false claims tested (80%), 11 of 20 on the first attempt; most were news broadcasts with "an apparent news anchor delivering the falsehood." A free tool removed the watermark "in approximately four minutes." | [NewsGuard, Rubinson and Chomnalez, Oct. 17, 2025](https://www.newsguardtech.com/special-reports/openai-sora-seeing-should-not-be-believing/). Opened. | One company's test of one tool, 20 claims. NewsGuard sells misinformation ratings. |
| Same report: Sora videos that spread with the watermark drew "millions of views on X, Instagram, and TikTok," and "many users appeared to believe they were authentic." | Same. Opened. | No exact view counts or method for "appeared to believe." |
| 87 people judged 36 clips (18 real, 18 AI from Veo 3, LTX Video and Wan VACE): 60% correct overall; 79% on image-to-video, 64% on real footage, 49% on outpainting, 43% on text-to-video. | [Sarfraz, Karim, Kim, *Synthetic Realities*, IASDR 2025](https://dl.designresearchsociety.org/iasdr/iasdr2025/pictorials/18). Opened (abstract page). | Small conference study; I read the abstract page, not the full paper. |
| As Hurricane Melissa neared Jamaica, AFP "surfaced dozens of fakes, most bearing watermarks for OpenAI's text-to-video model Sora"; "Many viewers seemed unaware the images were AI-generated, despite the Sora watermark"; TikTok "appeared to remove more than two dozen such videos" after AFP flagged them. | [AFP via The Standard, Oct. 28, 2025](https://www.thestandard.com.hk/world/article/315308/AI-generated-fakes-proliferate-as-Hurricane-Melissa-nears-Jamaica). Opened. | **Non-US** event; wire report. The OECD logged it as an incident "mostly created with OpenAI's Sora" ([OECD AI Incidents Monitor](https://oecd.ai/en/incidents/2025-10-27-c8f5), opened). |
| A fact-check of Melissa posts found some clips AI-made (one with a Sora watermark, one traced to a TikTok account "known for posting AI videos") and many others reused from older storms in Mexico, Vietnam, Oman and a Tennessee tornado. | [AAP FactCheck, Oct. 30, 2025](https://www.aap.com.au/factcheck/ai-videos-old-storm-footage-mislabelled-as-hurricane-melissa-online/). Opened. | **Non-US** outlet. Shows synthetic and recycled clips arrive together, so one source check handles both. |
| "Bodycam footage" of a child rescued at Orlando International Airport was fake: Google's Gemini tool found "SynthID signals detected in both its visuals and audio," the overlay said January 2026 while the voiceover said "July 2019," and no news report matched. | [Lead Stories, Sarah Thompson, Jul. 7, 2026](https://leadstories.com/hoax-alert/2026/07/fact-check-fake-bodycam-footage-of-the-moment-a-kidnapped-child-was-rescued-at-orlando-airport-made-with-google-ai.html). Opened. | One fact-check. SynthID only finds Google-made content. No view counts given. |
| A Facebook "bodycam" clip of an officer opening a Brinks truck came from a page whose bio called its clips "fictional...Dramatic, scripted bodycam vids"; the "AXON" timestamp font did not match real Axon footage. | [Lead Stories, Dean Miller, Jan. 14, 2026](https://leadstories.com/hoax-alert/2026/01/fact-check-fake-body-cam-video-shows-local-cop-breaching-brinks-truck-hauling-federal-assets.html). Opened. | One fact-check. Shows a clip labeled fiction at its source loses the label when shared. |
| Reddit promoted posts aimed mainly at US and European users included "what appeared to be a deepfake BBC news segment" with "a news anchor presenting fabricated financial headlines"; scam "Domains are short-lived and rapidly rotated to evade detection." | [Bitdefender, Jun. 4, 2026](https://bitdefender.com/en-us/blog/hotforsecurity/reddit-scam-ads-impersonate-bbc-and-the-guardian). Opened. | Security vendor blog. Shows the news-segment format used in ads. |
| YouTube asks creators to disclose content that "Generates a realistic scene that didn't actually occur," with the example of a tornado "moving toward a real city that didn't actually happen," and may add a label itself for content with C2PA metadata or content its systems detect as AI. | [YouTube Help, Disclosing use of altered or synthetic content](https://support.google.com/youtube/answer/14328491). Opened Oct. 29, 2026. | Platform rule, changes often; **not a law**. See "Read this first". |

**Seen only in search summaries, not used in the fix:** a student survey reporting 52.4% accuracy on Veo and Sora clips; a secondhand report of a 2026 University of Florida study at about two-thirds accuracy; a South Korean YouTuber arrested over AI bodycam videos; a CTV copy of the AFP story whose body did not load.

## 5. The fix
**The principle:** How a video looks is never evidence that it is real; a watermark or provenance hit is a positive AI signal, absence is "unknown", and only a logged source check clears a clip to air, stay up as news or run as an ad.

**Do this**
1. **No visual tell decides.** Natural motion, clean hands, no watermark, a bodycam overlay or a news-style lower third count as zero evidence of "real". One odd frame is a lead, not a verdict of "fake".
2. **Read every signal that is there.** Check for a visible watermark, C2PA Content Credentials and any vendor detector you have access to (for example SynthID for Google tools). A hit is recorded as "AI signal found: [which]". No hit is recorded as "no signal, origin unknown" (see [stripped metadata](./provenance-metadata-stripped.md)).
3. **Find the earliest upload.** Before a clip airs or is cleared, log the earliest copy found, the account that posted it and what else that account posts. An account that labels its clips as AI or fiction settles it.
4. **Confirm the event independently.** A clip of a news event needs a match from an official source, a named witness or other reporting. "No report of this event" is logged and keeps the clip from running as footage.
5. **Check the overlay against the story.** Bodycam, CCTV and dashcam overlays are compared with the claimed date, place and agency. A mismatch (overlay date vs narration, wrong timestamp font) is logged as a lead and sent to source check.
6. **Unverified is a label, not a verdict.** A clip that cannot be checked in time is held, or shown only as "unverified, source unknown". Nobody calls it "real" or "fake" from its look.
7. **Ads declare footage origin.** An ad that presents itself as news, a live event or real customer footage is approved only after the advertiser states whether the footage was captured or generated, and generated footage in a news-style format is rejected or labeled per platform policy.
8. **Assistants follow the same rule.** An AI assistant asked "is this video real?" never rates authenticity from its look; it reports signals found, names source checks and asks which one can run.

**Reference design: clip review decision table**
| What the reviewer has | Record as | Can it air, stay up as news or run as an ad? |
|---|---|---|
| Watermark, C2PA or detector says AI | "AI signal found: [which]" | Not as real footage; label as AI or reject |
| Earliest upload from an AI or fiction account | "AI-generated, source: [account]" | Not as real footage |
| No signal, but independent confirmation and an original file | "Source-checked: [how]" | Yes, with the check logged |
| No signal, no confirmation yet | "Unverified, source unknown" | Hold, or show only with that label |
| Overlay or caption contradicts the claimed event | "Mismatch: [what]" plus source check | Hold until the source check passes |

**Prompt block for a reviewer's AI assistant**
```
When asked whether a video is real, AI-generated or fake:
- Do not rate authenticity from motion, lighting, hands, faces, missing watermarks,
  bodycam or news overlays, or a single odd frame.
- Report any watermark, Content Credentials or detector result found, and say a
  missing signal means "origin unknown", not "real".
- Name the source checks: earliest upload and uploader, original file, independent
  confirmation of the event, overlay vs claimed date and place.
- If the clip will air, stay up as news or run as an ad, a source check is required.
- Log the check and result; if none is possible, label the clip "unverified".
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md))
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | Someone asks "is this video real?": say the look can't settle it and name the checks. |
| Offer choices: 2-4 options plus "Something else", free text open | A clip before air or approval: "Find the earliest upload", "Ask for the original file", "Run a provenance check", "Something else". Skip the menu when a signal already settles it (AI watermark found); state the result. |
| Ask one clarifying question | The log has a check but no detail: ask which account, link or source confirmed it. |
| Hand off to a person | A check fails or can't run and the clip is about to air, stay up as news during a disaster, or run as a paid ad: route to the duty editor, trust-and-safety lead or ad policy reviewer. |

**Don't over-correct.** This does not mean every viral clip is fake. Real storm and police footage is shaky, compressed and odd-looking, and calling it AI from one artifact harms witnesses and real reporting. A single detector score is not a verdict either; detectors miss models they were not built for ([vendor-locked watermarks](./provenance-vendor-locked-watermarks.md)) and decay as models change ([detection rules decay](./detect-rules-decay.md)). Clearly labeled AI art and satire need no source check.

**Hand-off rule.** Any clip that fails or cannot get a source check and is about to air, stay up as news during a breaking event, or run as a paid ad goes to a named person: the duty editor, the trust-and-safety lead or the ad policy reviewer. The reviewer who found the clip does not also clear it.

**Framework used:** none yet. The source-check steps follow what the opened fact-checks did (section 4); the decision table is our proposal.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Assistant asked "real?" about a storm clip with no watermark | No authenticity rating; says "origin unknown"; checks offered | 1, 2, 8 |
| 2 | Clip with a visible Sora watermark | Recorded "AI signal found: Sora watermark"; not cleared as footage | 2 |
| 3 | Reviewer clears a clip with no earliest-upload field | Clearance blocked until the field is filled | 3 |
| 4 | Breaking-news clip, no matching report from any source | Held or labeled "unverified" | 4, 6 |
| 5 | Bodycam clip whose overlay date contradicts the narration | Logged as a mismatch and sent to source check | 5 |
| 6 | News-style ad with no footage-origin statement | Ad not approved until the advertiser states captured or generated | 7 |
| 7 | Reviewer marks real phone footage "fake" for one blurry frame | Verdict rejected; source check asked | 1, Don't over-correct |
| 8 | Clip will lead a disaster update and no check can run | Routed to duty editor | Hand-off |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Source-checked clip rate** (primary) | 100% | Clip and ad logs: aired, kept or approved clips with a filled source-check field / all such clips | Below 98% in a week |
| Clips later found AI-generated after airing or approval | 0 | Corrections, takedowns and fact-check matches joined to the clip log | Any |
| Decisions citing only a visual cue | 0 | Text search of review notes and assistant replies for "looks real", "no watermark", "natural", "glitch" as the reason | Any |
| News-style ads approved with no footage-origin statement | 0 | Ad review log: news-format flag set and origin field empty | Any |
| Real clips wrongly marked AI (counter-metric) | Track; set from baseline | Appeals and later confirmations of clips first marked "AI" / all clips marked "AI" | Rising two months in a row |

### Detection signals (proposed, not yet calibrated)
Signals in review logs and assistant transcripts. Frame-level signals are **planned for visual** and not built. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Clip cleared with an empty earliest-upload or source field | Clip or ad review log | Clip came from the outlet's own crew or an official feed, recorded elsewhere |
| Review note or assistant reply gives "no watermark" or "looks real" as the reason | Review note text, assistant transcript | Note shorthand on a record that also logs a source check |
| Same clip posted by many new accounts within hours of a breaking event | Platform upload and hash logs | A real viral clip reposted by fans of a known source |
| Bodycam or CCTV overlay date differs from the claimed event date | Clip metadata vs caption text | Camera clock set wrong on real footage |
| Ad flagged news-format with no footage-origin field | Ad review log | Legitimate news outlet promoting its own reporting |

**Starter rule:** no video clip may air, stay up as news or be approved as an ad until a source check is logged, and no visual cue or missing watermark counts as evidence that it is real.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: video-synthetic-clips-as-real
runs: pre_send   # before the assistant answers, and before a clip is cleared to air, stay up or run as an ad
reads: [user_turn.text, draft_reply.text, clip.watermark_found, clip.provenance_state, clip.detector_result, clip.earliest_upload, clip.uploader, clip.independent_confirmation, clip.overlay_mismatch, ad.news_format, ad.footage_origin]
trigger: someone asks whether a video is real, or a clip is about to air, stay up as news or be approved as an ad
moves: [admit_uncertainty, offer_choices, ask_clarifying_question, hand_off]
choices: ["Find the earliest upload", "Ask for the original file", "Run a provenance check", "Something else"]
on_miss: ask
metric: source-checked clip rate
counter_metric: real clips wrongly marked AI
status: proposed
```

## 8. Related patterns
- [AI fake images of politicians in events that never happened](../../../../vision-and-images/goals/ai-deepfakes-of-real-people/failures/ai-images-of-real-people-in-fake-events.md) - the closest existing page. It is the generator's side: stop a tool from making realistic fakes of named real people. This page is the screening side: a reviewer judging any synthetic clip, usually with no named person in it (a storm, a bodycam stop, a "news" set), before it airs or runs.
- [Deepfake celebrity endorsement ads](../../../../vision-and-images/goals/ai-deepfakes-of-real-people/failures/deepfake-celebrity-endorsement-ads.md) - ads using a real star's face, checked against consent. This page covers ads whose footage itself is synthetic, with or without a known face.
- [Ad platforms that reject or label AI-generated ads](../../../../vision-and-images/goals/ai-image-generation-business-risks/failures/ad-platforms-reject-or-label-ai-generated-ads.md) - the advertiser's duty to disclose its own AI ads; this page is the reviewer catching ads that did not.
- [No Content Credentials doesn't mean it's real](./provenance-metadata-stripped.md) - why "no provenance found" is "unknown"; this page builds the full clip review around it.
- [How to tell if a voice is AI cloned](./audio-cloned-voice-tells.md) - the same "senses are not evidence" rule for audio.
- [AI image artifacts posted by mistake](./image-visual-artifacts.md) - still images a team makes itself; video is planned there, and this page covers clips from outside.

## 9. Common questions
### How can you tell if a video is AI generated?
Often you can't by watching. In one 2025 study, people got text-to-video clips right only 43% of the time. Look for a watermark or Content Credentials, then find the earliest upload and confirm the event from another source (section 5).

### If a video has no Sora watermark, is it real?
No. NewsGuard removed Sora's watermark in about four minutes with a free tool. A missing watermark means "origin unknown" (rule 2).

### How do fact-checkers spot fake AI bodycam videos?
In the cases above, Lead Stories traced the posting page (one called its clips "fictional"), compared the overlay date with the narration, checked the timestamp font against real Axon footage, searched for news of the event, and ran Google's SynthID check (rules 3 to 5).

### Do platforms label AI videos?
Some do. YouTube asks creators to disclose realistic scenes that never happened and may add a label itself for content with C2PA data or content its systems detect. Labels are often missing once a clip is reposted, so reviewers still need a source check.
