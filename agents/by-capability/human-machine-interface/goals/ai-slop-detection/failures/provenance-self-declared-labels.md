# Why Isn't This AI Video Labeled? Platforms Rely on Self-Declared AI Labels

<!-- SEO
title: Why Isn't This AI Video Labeled? Self-Declared AI Labels
description: Platforms rely on uploaders ticking an AI box, so undeclared AI posts get no label and look real; add provenance checks, review and clear wording.
search phrases:
- why isn't this ai video labeled
- does no ai label mean it's real
- how does tiktok know if a video is ai
- youtube altered or synthetic content checkbox
- meta ai info label how does it work
- ai generated content not labeled instagram
- what happens if you don't label ai content on youtube
- etsy ai disclosure listing
-->

**Frequency**: Common

## Issue: Platforms rely on uploaders ticking an AI box, so undeclared AI posts get no label and look real; add provenance checks, review and clear wording.

> **One line:** A video app, social network or marketplace shows an "AI-generated" label only when the uploader ticks a box or a file still carries a provenance tag, so an AI clip from an uploader who skips the box goes out with no label, and viewers read the missing label as "real"; the fix is to treat the box as one input among several (provenance reads, detectors, account history, viewer reports), route mismatches to review, and word the label system so "no label" never reads as "human-made."

> **Read this first:** The YouTube, Meta and Etsy rules below summarize platform pages and news reports as read on October 29, 2026. A platform rule is not a law, and this page does not describe any law. It is design guidance, not legal advice. Anyone setting a labeling or disclosure policy, or deciding what a missing label means for a takedown, needs review by a qualified person.

| | |
|---|---|
| **Channel** | Written for **visual and workflow**: the upload form, the label shown on posts and listings, and the trust-and-safety review queue. Chat assistants asked "is this labeled AI?" are covered by rule 6. Voice is not covered. |
| **Stakes** | High. Viewers use the label to decide what to believe and share; a missing label on an AI storm clip or a fake product photo reads as a pass. |
| **Who is affected** | Viewers and buyers on video apps, social networks and marketplaces; honest creators whose labeled posts are doubted next to unlabeled fakes; trust-and-safety teams |
| **Frequency** | Common. AI Forensics, as reported by ANSA, found only half of AI content on TikTok and 23% on Instagram "adequately labelled" in a June 2025 sample (section 4). |
| **Pattern ID** | provenance-self-declared-labels |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Undeclared-AI catch rate (proposed): in a monthly sample of posts reviewers judge AI-made, the share that carries an AI label from any source (uploader box, provenance read, detector or review). Proposed starting target: 90%, tune on your own sample. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Better detectors catch more undeclared posts, but the label still depends on an honest box and on tags that uploads strip, and the "no label means real" reading is a wording problem no model fixes. (Our judgment, not tested.) |
| **Also searched as** | ai label missing on video · how do platforms detect ai content · made with ai label · creator didn't disclose ai · is unlabeled content real · ai disclosure toggle |

## 1. In plain words
Most platforms label AI content in two ways: the uploader says so, or the file carries a machine-readable tag such as Content Credentials. Anyone who skips the box and strips the tag gets no label. Viewers then see a labeled AI post next to an unlabeled one and assume the unlabeled one is real. The fix is to check more than the box, send mismatches to review, and tell viewers plainly that no label means "not declared," not "human-made."

## 2. What it looks like
**Without the fix** (illustrative: a video app's label policy during a Gulf Coast hurricane)
```
Upload form:  "Is this AI-generated? [ ] Yes"   (uploader leaves it blank)
Post shown:   "Flooding in downtown Houston right now"   (no label)
Viewer:       The other storm clip says "AI-generated." This one doesn't,
              so this one's real. Sharing it.
Help bot:     There is no AI label on this video, so it was not marked as
              AI-generated.
(The clip came from an AI app; the uploader also posts only AI clips.)
```
**With the fix**
```
Upload form:  "Is this AI-generated? Yes / No"   (uploader picks No)
System:       Detector and account history disagree with "No"; held for review.
Post shown:   "AI-generated (added by review)"   after a reviewer confirms
Viewer:       Is a video with no label real?
Help bot:     Not necessarily. "No label" means nobody declared AI and our
              checks found none, not that a person filmed it. Next step?
              "See where it was first posted" · "Report as AI" · "Something else"
```
The fixed platform checks the box against other signals, and the fixed bot says what a missing label does and does not mean.

## 3. Why it happens
- **The box is the cheapest signal, so it carries the most weight.** Meta said in 2024 its labels would be added "when we detect industry standard AI image indicators or when people disclose" ([Meta newsroom](https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/)). An uploader who skips the box and has no tag left in the file falls through both.
- **The label system has two states, so silence gets read as the other one.** Posts show "AI" or nothing. Nothing on the screen says what nothing means, so viewers fill it in with "real."
- **Skipping the box costs little until someone notices.** YouTube's penalties apply to creators "who consistently choose not to disclose," so a single undeclared upload can stay unlabeled unless a system or reviewer catches it ([YouTube Help](https://support.google.com/youtube/answer/14328491)).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| "Participants tended to rely heavily on the presence or absence of a label," and "unlabeled content was more likely to be perceived as true" even when false. True content with an AI label "was more often doubted." Over 1,300 survey participants from the US and Europe. | [CISPA press release on the CHI 2026 paper](https://cispa.de/user-study-ai-labels), opened; paper at [ACM DL](https://dl.acm.org/doi/full/10.1145/3772318.3791006), not opened. | I read the institute's summary, not the paper's numbers. Simulated news posts in a study, not a live platform. Supports rules 2 and 4. |
| In June 2025 searches for 13 hashtags in Germany, Spain and Poland, "only half of AI-generated content on TikTok is adequately labelled"; the Instagram figure was 23%, and labels were "completely non-existent for Instagram's desktop users." | [ANSA, Sept. 5, 2025](https://www.ansa.it/english/news/2025/09/05/tiktok-instagram-flooded-by-unlabelled-ai-content_8947d377-e517-4cf2-923c-5282a27e3013.html), reporting an AI Forensics study. Opened. | **Secondary and non-US:** I could not open the AI Forensics report (file too large). One sample, mid-2025; platforms change. |
| YouTube requires creators "to disclose AI-generated or altered content that seems realistic" through a Yes/No "AI use" choice in Studio, may add a label itself for content with C2PA metadata or content its systems detect, and says creators who "consistently choose not to disclose" may get a manual label or penalties. | [YouTube Help, Disclosing use of altered or synthetic content](https://support.google.com/youtube/answer/14328491). Opened Oct. 29, 2026. | Platform rule, not a law. Shows a self-declaration plus provenance plus detection design; the page does not say what a missing label means. |
| Meta's 2024 labels were based on "industry-shared signals of AI images or people self-disclosing"; in July 2024 Meta said labels from these indicators "weren't always aligned with people's expectations" and renamed "Made with AI" to "AI info"; in September 2024 it said labels would "share whether the content is labeled because of industry-shared signals or because someone self-disclosed." | [Meta, Our approach to labeling AI-generated content, Apr. 5, 2024, with updates](https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/). Opened. | Company announcement, not a measurement. Supports rule 3 (say where a label came from). |
| Etsy: "Sellers must disclose within their listing description if an item is created with the use of AI." | [TechCrunch, July 9, 2024](https://techcrunch.com/2024/07/09/etsy-new-seller-policy-2024-generative-ai), quoting Etsy. Opened. | **Secondary:** Etsy's own policy page returned 403. Shows a marketplace relying on seller text alone. |

**Seen only in search summaries, kept out of the fix:** TikTok's help page on AI-generated content (the site refused connections), including its auto-labeling from Content Credentials; an Indicator audit (Oct. 2025, Mar. 2026) saying platforms often failed to label test AI posts and YouTube missed half of Veo videos; a report that Etsy removed over 17,000 listings for AI disclosure violations in early 2025; and a PNAS Nexus "implied truth effect" study on partial false-news labels. I did not open those sources.

## 5. The fix
**The principle:** The uploader's box is one signal, never the whole label; every other signal can add a label, mismatches go to review, and the screen says that no label means "not declared," not "human-made."

**Do this**
1. **Read more than the box.** On every upload, record the uploader's answer and also run the provenance read (C2PA, IPTC digital source type) and any detector you have. Store all of them on the post.
2. **Any positive signal labels.** A provenance tag, a confirmed detector hit or a reviewer's finding adds the AI label even when the uploader said No. An uploader's No never removes a label another source added.
3. **Say where the label came from.** Each label names its source: "declared by uploader," "from Content Credentials," "added by review."
4. **Name the empty state.** Posts with no label link to one line: "No AI label: not declared and not detected. This does not mean a person made it." Never use "verified," "real" or a check mark for unlabeled posts.
5. **Make the box a required choice.** The upload form asks Yes or No with no default, and gives one realistic example of each, so skipping is a choice that gets logged.
6. **Mismatches go to review.** Uploader says No but a detector, account history (an account whose other posts are labeled AI) or viewer reports say AI: hold reach or queue for review before the post is promoted.
7. **Repeat skippers lose self-declaration.** An account with confirmed undeclared AI posts gets labels applied by review on new uploads until a reviewer clears it.

**Reference design: label decision table**
| Uploader box | Provenance or detector | Account history | Label shown | Action |
|---|---|---|---|---|
| Yes | Any | Any | "AI-generated (declared by uploader)" | Publish |
| No | AI tag or confirmed hit | Any | "AI-generated (from Content Credentials)" or "(detected)" | Publish with label; log mismatch |
| No | Weak or possible hit | Prior undeclared AI | None yet | Hold reach; review queue |
| No | Nothing found | Clean | No label; empty-state line on tap | Publish; sample for audit |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md))
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | A viewer or a help bot is asked "no AI label, so it's real?": say what "no label" means and point to the earliest post or report button. |
| Offer choices: 2-4 options plus "Something else", free text open | After that answer: "See where it was first posted," "Report as AI," "Something else." Don't offer them when the viewer only asked what the label means; answer and stop. |
| Ask one clarifying question | An uploader asks "do I need to tick the AI box?" about edited footage: ask whether AI made a realistic scene or only cleaned up audio or color. |
| Hand off to a person | A mismatch on a post about a breaking event, an election or a product claim: route to a trust-and-safety reviewer before it is promoted. |

**Don't over-correct.** Do not label every unlabeled post "possibly AI" or bury real footage in warnings; the CISPA study found AI labels made true content doubted more often, so false labels hurt real witnesses and sellers. Do not punish a first honest mistake like deliberate evasion. A detector hit alone is not proof; see [vendor-locked watermarks](./provenance-vendor-locked-watermarks.md).

**Hand-off rule.** Any mismatch between the uploader's box and another signal, on a post about news, elections, health or a sale, goes to a named reviewer before the post is promoted; the reviewer's call and reason are logged on the post.

**Framework used:** none yet. Rules draw on YouTube's and Meta's published designs and the CISPA study (section 4), plus our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Upload an AI clip with Content Credentials and the box set to No | Label shown, source "from Content Credentials" | 1, 2, 3 |
| 2 | Viewer asks the help bot "no label, so it's real?" | Says "not declared and not detected," no "real" | 4 |
| 3 | Open the upload form | Yes/No with no default; skipping is blocked or logged | 5 |
| 4 | Box No, detector possible hit, account has prior undeclared AI | Post held from promotion and queued | 6 |
| 5 | Account with a confirmed undeclared AI post uploads again | Label set by review, not by the box | 7 |
| 6 | Viewer only asks "what does AI info mean?" | Short answer, no choice menu | Moves |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Undeclared-AI catch rate** (primary) | 90% | Monthly reviewer sample of posts judged AI-made: share with an AI label from any source | Below 80% |
| Box-only label share | Track | Labeled AI posts whose only source is the uploader box / all labeled AI posts | Rising month over month |
| Mismatch review rate | 100% for news, election, health, sale posts | Review log: mismatched posts reviewed before promotion / all such mismatches | Below 95% |
| Unlabeled-as-real replies | 0 | Scan help-bot replies on unlabeled posts for "real," "authentic," "not AI" | Any |
| Real posts labeled AI on appeal (counter-metric) | Track; set from baseline | Appeals upheld that removed a wrong AI label / all AI labels applied by system or review | Any rise month over month |

### Detection signals (proposed, not yet calibrated)
Signals in an upload, label or help-bot event log that suggest this failure. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Upload with box No and a C2PA or IPTC AI tag present | Upload log, declaration vs provenance fields | Tag from a minor AI edit the policy does not cover |
| Box No on an account whose other posts are labeled AI | Account label history | A creator who posts both real footage and AI art |
| Viewer "Report as AI" reports on a post with no label | Report log joined to label state | Pile-on against a real creator ([false accusations](./detect-false-accusations-by-readers.md)) |
| Help-bot reply says "real" or "not AI" on an unlabeled post | Bot output log joined to label state | Reply quoting the user's own words to correct them |

**Starter rule:** an uploader's "No" never removes an AI label that a provenance tag, detector or reviewer added, and an unlabeled post is described as "not declared," never "real."

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: provenance-self-declared-labels
runs: pre_send
reads: [upload.declared_ai, provenance.manifest_state, detector.result, account.undeclared_ai_count, post.label_source, user_turn.text, draft_reply.text]
trigger: a post is about to be published or promoted, or a reply describes a post's AI label state
moves: [admit_uncertainty, offer_choices, ask_clarifying_question, hand_off]
choices: ["See where it was first posted", "Report as AI", "Something else"]
on_miss: rewrite
metric: undeclared-AI catch rate
counter_metric: real posts labeled AI on appeal
status: proposed
```

## 8. Related patterns
- [No Content Credentials doesn't mean it's real](./provenance-metadata-stripped.md) - the closest pattern. It covers the tag being stripped from the file and a checker reading absence as "real." This page covers the platform's label system: the uploader's box is the main input, and the platform's own "no label" state is misread.
- [Vendor-locked watermarks](./provenance-vendor-locked-watermarks.md) - one vendor's detector finding nothing; here a detector is one of several inputs to the label.
- [AI clips passed off as real news footage](./video-synthetic-clips-as-real.md) - the newsroom or moderator checking one clip's source; this page is the platform-wide label design those reviewers see.
- [Ad platforms that reject or label AI-generated ads](../../../../vision-and-images/goals/ai-image-generation-business-risks/failures/ad-platforms-reject-or-label-ai-generated-ads.md) - the advertiser setting the disclosure toggle; this page is the platform deciding what to do when the toggle is wrong.

## 9. Common questions
### If a video has no AI label, does that mean it's real?
No. On most platforms a label appears when the uploader declares AI or a tag or detector finds it. A missing label means none of those happened, not that a person filmed it. Check where it was first posted (rule 4).

### How does YouTube or TikTok know a video is AI?
Mostly from the creator's answer at upload, plus tags such as Content Credentials and their own detection. YouTube's help page lists all three. If the creator says no and the tags are gone, the system may not know (section 4).

### What happens if I don't label AI content on YouTube?
YouTube says creators who consistently skip the disclosure may get a label added by YouTube or penalties such as removal or suspension from the Partner Program. Rules change, so read the current help page.

### Why do labeled real photos get doubted?
Labels tell people to doubt, and false or over-broad labels spread that doubt to real content. The CISPA study found true content with an AI label was doubted more often, which is why rule 2 needs a confirmed signal (section 5).
