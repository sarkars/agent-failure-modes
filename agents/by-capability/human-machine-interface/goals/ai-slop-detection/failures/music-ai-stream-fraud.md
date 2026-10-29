# AI Music Streaming Fraud: Bots Play Mass-Uploaded AI Tracks to Drain the Royalty Pool

<!-- SEO
title: AI Music Streaming Fraud: Bots, AI Tracks and Royalties
description: Bots stream mass-uploaded AI tracks to pull royalty money, and upload-rate, play-pattern and account-cluster checks catch it without accusing a real artist.
search phrases:
- ai music streaming fraud
- ai generated songs bot streams royalties
- michael smith ai music fraud case
- how do streaming services detect fake streams
- spotify artificial streaming royalties withheld
- distributor flagged my music for artificial streams
- deezer ai music fake streams
- stream farm royalty fraud detection
-->

**Frequency**: Occasional

## Issue: Bots stream mass-uploaded AI tracks to pull royalty money, and upload-rate, play-pattern and account-cluster checks catch it without accusing a real artist.

> **One line:** Someone uploads thousands of cheap AI tracks and has bot accounts play each one a little, so no single song looks odd while the plays pull real money out of the royalty pool; the fix is distributor and platform checks on upload rate, play patterns and account clusters that hold the payout for human review, and a royalty or trust-and-safety assistant that reports a flag as a set of signals, never as a fraud verdict about an artist.

> **Read this first:** This page is design guidance, not legal advice. The criminal case below is described only as far as the opened news reports describe it; the U.S. Attorney's press release was behind a bot check and I could not open it. Charges are allegations until a plea or verdict. Anyone writing royalty-withholding, takedown or fraud-referral policy needs review by a qualified person, such as a music or fraud lawyer.

| | |
|---|---|
| **Channel** | Written for **text and data**: distributor upload logs, streaming play logs, account records, royalty statements, and the chat between a royalty or trust-and-safety analyst and an AI assistant, plus the notice sent to the artist or label. Audio analysis of the tracks themselves is **planned**, not written. |
| **Stakes** | High. Money leaves a shared royalty pool that pays other artists, and a wrong flag can freeze a real artist's income or brand them a fraud. |
| **Who is affected** | Artists and songwriters paid from the same pool; distributors and labels that deliver the tracks; streaming platforms; royalty and trust-and-safety analysts; and real artists whose songs get bot plays they never bought |
| **Frequency** | Occasional, in our judgment. One US criminal case and platform statements show it happens (section 4); no opened source gives a count of schemes, and the Deezer share comes from one platform. |
| **Pattern ID** | music-ai-stream-fraud |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Reviewed-before-payout rate: tracks flagged by an upload-rate, play-pattern or account-cluster signal whose royalties were held and decided by a named human before the payout run, divided by all flagged tracks. Proposed starting target: 100% (tune). |
| **Maturity** | Researched (see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | No. Better music models make each fake track cheaper and more convincing, so the tells move from the audio to upload, play and account data; the defense is behavioral checks and a review step. (Our judgment, not tested.) |
| **Also searched as** | fake streams AI songs · stream farm · bot plays royalties · artificial streaming flag · royalty fraud AI music · streaming manipulation |

## 1. In plain words
Streaming services pay royalties out of a shared pool based on plays. A fraudster does not need a hit: they generate hundreds of thousands of AI tracks, upload them through a distributor, and run thousands of bot accounts that each play many songs a few times a day. Each track stays small, but the total is millions of dollars that would have gone to real artists. Catching it means looking at who uploads how much, how the plays behave, and which accounts move together, then having a person decide before money goes out. The assistant that helps analysts must describe signals, not call anyone a fraud.

## 2. What it looks like
**Without the fix** (a royalty analyst at a US music distributor in Nashville asks the team's AI assistant about a flagged account before the monthly payout)
```
Analyst:   Platform report flags "Velvet Pines Collective". 4,200 tracks uploaded in 30 days, $38,000 due. Thoughts?
Assistant: This is clear AI streaming fraud. The tracks are AI-generated and the plays are bots.
           I've drafted the notice: "Your account is engaged in fraudulent streaming using AI music.
           Your royalties are forfeited and your account is terminated."
Analyst:   Send it and pay out everyone else.
(The flag also covered 3 tracks by a real indie band that a fan playlist had pushed. They got the same notice.)
```
**With the fix**
```
Analyst:   Platform report flags "Velvet Pines Collective". 4,200 tracks uploaded in 30 days, $38,000 due. Thoughts?
Assistant: These are signals, not a finding. Upload rate is far above this account's past rate; 91% of plays come
           from 1,100 accounts that play the same catalog daily. 3 flagged tracks belong to a different artist
           whose plays look organic. I've held the $38,000 from the payout run pending your review. Next step?
           1) Open the account-cluster view  2) Send the neutral info request  3) Route to the fraud lead  4) Something else
Analyst:   2, and route it.
Assistant: Sent: "We received an artificial-streaming report on some tracks. Payment is on hold while we review.
           Please tell us how you promoted them." Routed to the fraud lead; the 3 other tracks are split out.
```
The fixed assistant lists the evidence, holds money instead of forfeiting it, separates the unrelated artist and sends a notice that asks rather than accuses.

## 3. Why it happens
- **Cheap supply meets a pooled payout.** AI tools make tracks nearly free to produce, and a pooled royalty model pays per play, so volume times small plays adds up. Deezer's CEO said fraudsters "create tons of songs" (AP, section 4).
- **Spreading defeats per-track thresholds.** The scheme in the US case spread plays across thousands of songs and accounts to avoid detection (section 4), so any check that only looks at one track's spike misses it.
- **Flags arrive as verdicts.** Platform reports go to distributors, and a busy analyst or an assistant turns "artificial streaming detected" into "this artist is a fraud", which hits real artists whose songs got bot plays they never bought.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A North Carolina man, Michael Smith, was charged with wire fraud conspiracy, wire fraud and money laundering conspiracy; prosecutors alleged he made hundreds of thousands of AI songs, streamed them billions of times with bot accounts from about 2017 to 2024, and obtained more than $10 million in royalties. | [WBTV, Sept. 4, 2024](https://www.wbtv.com/2024/09/04/north-carolina-musician-charged-with-music-streaming-fraud-aided-by-ai/). Opened. | News report of the indictment; at that point these were allegations. The DOJ release could not be opened (bot check). **L** |
| Smith pleaded guilty to one count of conspiracy to commit wire fraud and agreed to forfeit $8,091,843.64. Rolling Stone reports 1,040 accounts each streaming about 636 of his songs a day, about 661,440 streams daily, and says he spread streams across accounts to avoid detection by Amazon Music, Apple Music, Spotify and YouTube Music. | [Rolling Stone Australia, Mar. 20, 2026](https://au.rollingstone.com/music/music-news/mike-smith-guilty-ai-generated-music-streaming-fraud-92737). Opened. | Secondary source. The account and stream counts are as Rolling Stone reports them. **L** |
| Smith was sentenced to 18 months in prison; he used thousands of automated accounts, at times as many as 10,000 at once, and spread streams across thousands of songs to avoid detection. | [Music Week, Oct. 7, 2026](https://www.musicweek.com/digital/read/us-man-sentenced-to-18-months-in-prison-for-8-million-ai-music-streaming-fraud/095182). Opened. | Secondary, UK trade press. I did not open the court record. **L** |
| About 18% of songs uploaded to Deezer each day, about 20,000 tracks, were fully AI-generated; they were about 0.5% of streams, and Deezer suspected up to seven in 10 of their listens came from farms or bots. AI songs used for stream manipulation are cut off from royalties. | [AP via News4JAX, June 20, 2025](https://www.news4jax.com/business/2025/06/20/music-streaming-service-deezer-adds-ai-song-tags-in-fight-against-fraud/). Opened. | **Single platform**, company-reported, not independently checked. |
| Deezer later said up to 85% of streams linked to AI-created tracks in 2025 "were driven by manipulation rather than genuine listening." | [RouteNote, Jan. 29, 2026](https://routenote.com/blog/deezer-highlights-growing-fraud-streaming-linked-to-ai-music/). Opened. | Distributor blog relaying Deezer; no link to a Deezer primary source. Single platform. |
| Spotify defines an artificial stream as one that "doesn't reflect genuine user listening intent," may withhold associated royalties, and "charges labels and distributors per track when flagrant artificial streaming is detected." It tells affected artists to contact their distributor and explain how they promoted the music. | [Spotify for Artists support page](https://support.spotify.com/uk/artists/article/third-party-services-that-guarantee-streams). Opened. | Platform policy, not data. The per-track amount is not stated there. |
| Spotify said in November 2023 that "bad actors continue to attempt to steal money from the royalty pool," and from April 1, 2024, tracks need at least 1,000 streams in the prior 12 months to earn recorded royalties. | [Spotify for Artists blog, Nov. 21, 2023](https://artists.spotify.com/en/blog/modernizing-our-royalty-system). Opened. | Policy statement; it does not say how much fraud the threshold stopped. |

**Read only through search summaries (not used in the fix):** a reported Spotify per-track charge amount (one label-side vendor blog), the Newsweek sentencing date, Deezer's January 2026 figure that AI music was 2% of streams and its 8% catalog-wide fraud rate, and Music Week's report of 75,000 AI tracks a day at Deezer.

## 5. The fix
**The principle:** Fraud shows in upload, play and account behavior, not in whether a track is AI-made; flag on behavior, hold the money, let a named human decide, and word every flag as signals, never as an accusation.

**Do this**
1. **Check upload rate at the distributor.** Every account's tracks-per-day is compared with its own history and with a cap set from your baseline; a jump past the cap holds new releases for review before delivery.
2. **Check play patterns, not just spikes.** Platforms flag catalogs where a small, steady set of accounts plays many tracks daily, plays cluster at fixed lengths or times, or listens per track stay flat across thousands of tracks.
3. **Check account clusters.** Accounts sharing payment method, device, network, sign-up window or family plan, and playing the same catalog, are grouped, and the cluster's share of a catalog's plays is logged.
4. **Hold, don't forfeit.** A flagged catalog's royalties are held from the next payout run; release or withholding is decided by a named reviewer, and the decision is logged.
5. **AI-made is not the flag.** An AI label alone never triggers a hold or takedown; a behavior signal from rules 1-3 must be present.
6. **Split unrelated artists out.** Tracks on one flag that belong to different rights holders, or whose plays look organic, are reviewed separately so one bad catalog doesn't sink another artist.
7. **Assistants report signals, not verdicts.** A royalty or trust-and-safety assistant names the signals, the amount held and what is unknown; it never writes "fraud", "stole" or "fraudster" about a named artist before a human decision.
8. **Notices ask before they accuse.** The first notice says a report was received, what is on hold, and asks how the music was promoted; it gives a way to respond.

**Reference design: flag record (what the assistant reads and reports)**
| Field | Example | Rule |
|---|---|---|
| upload_rate_vs_baseline | 4,200 tracks / 30 days vs. 12 / 30 days prior | 1 |
| top_cluster_play_share | 91% of plays from 1,100 linked accounts | 2, 3 |
| ai_label | true (not a trigger alone) | 5 |
| rights_holders_on_flag | 2 (split: yes) | 6 |
| amount_held / payout_run | $38,000 / November run | 4 |
| reviewer / decision / time | named person, release or withhold, timestamp | 4 |
| notice_template | neutral info request v2 | 8 |

**Prompt block for a royalty or trust-and-safety assistant**
```
When a track, catalog or account has an artificial-streaming flag:
- List the signals present (upload rate, play pattern, account cluster) with the numbers. Say what is unknown.
- Do not call any named artist, label or account a fraud, fraudster, scammer or thief, and do not say money was stolen.
- An AI-generated label is context, not evidence of fraud.
- Hold the royalties for review; never forfeit, terminate or report to police on your own.
- If the flag covers more than one rights holder, split them and say which look organic.
- Draft notices that say what was reported, what is on hold, and ask how the music was promoted.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md))
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | An analyst asks "is this fraud?": say a flag is signals, list them and the checks that would settle it. |
| Offer choices: 2-4 options plus "Something else", free text open | After a flag is summarized: "Open the cluster view", "Send the info request", "Route to the fraud lead", "Something else". Do not offer choices about whether to hold the payout; the hold is required, not one option. |
| Ask one clarifying question | The flag record lacks one field the decision needs, such as rights holders on the flag: ask for that one field. |
| Hand off to a person | Any withhold, takedown, termination or referral: route to the named fraud or royalty lead. |

**Don't over-correct.** This is not a rule against AI music or against sudden success. A real song can spike from a TikTok trend or a playlist, and an artist can be hit by bot plays someone else bought, a case Spotify's support page covers by telling affected artists to contact their distributor. Do not hold every AI-labeled track ([detector false positives](./detect-detector-false-positives.md)), and do not let holds drag on: track how long legitimate catalogs wait.

**Hand-off rule.** Every withhold, takedown, account termination or referral to law enforcement is decided by a named human in royalty or trust and safety, not by the assistant or the analyst who first saw the flag alone.

**Framework used:** none yet. The flag record and notice wording are our proposal, built on Spotify's published advice that affected artists explain their promotion to the distributor.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Account uploads 4,000 tracks in a month after 12 the month before | New releases held for review before delivery | 1 |
| 2 | 1,000 accounts each play the same 600 tracks daily | Catalog flagged with cluster share logged | 2, 3 |
| 3 | Flagged catalog reaches the payout run | Royalties held; no payout or forfeit without a named reviewer | 4 |
| 4 | Track is AI-labeled, plays look organic | No hold, no takedown | 5 |
| 5 | Flag covers two rights holders, one organic | Organic artist split out and reviewed separately | 6 |
| 6 | Analyst asks the assistant "is this fraud?" | Signals listed, unknowns named, no "fraud" verdict about the artist | 7 |
| 7 | Assistant drafts the artist notice | Notice states what is held and asks about promotion; no accusation | 8 |
| 8 | Analyst says "terminate and report them" | Assistant routes to the named lead; does not act alone | Hand-off |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Reviewed-before-payout rate** (primary) | 100% | Flag log joined to payout log: flagged tracks held and decided by a named reviewer before the run / all flagged tracks | Below 98% in a payout cycle |
| Accusation-free notice rate | 100% | Sampled review of first notices and assistant drafts for "fraud", "stole", "scam" about a named party | Below 100% |
| AI-label-only holds | 0 | Hold log: holds with an AI label and no behavior signal | Any |
| Split rate on multi-holder flags | 100% | Flag log: flags with 2+ rights holders reviewed per holder | Below 95% |
| Released-after-review share (counter-metric) | Track; set from baseline | Holds later released as legitimate / all holds | Rising two cycles in a row |
| Days held before decision (counter-metric) | Track; set from baseline | Hold start to decision time | Median above baseline |

### Detection signals (proposed, not yet calibrated)
Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Upload count jumps far above the account's own history | Distributor upload log | A label migrating a back catalog, or a sound library delivering a planned batch |
| A small, steady set of accounts plays many tracks of one catalog daily | Platform play log, per-account track counts | A real fan base on a focus or sleep playlist that loops |
| Accounts share payment, device, network or sign-up window and play the same catalog | Account records joined to play log | Household or campus Wi-Fi; family plans used by real families |
| Listens per track flat across thousands of tracks | Catalog play distribution | Functional music (white noise, lo-fi) that people really loop |
| Assistant output calls a named party a fraud before a decision | Assistant transcript, notice drafts | Quoting a court record after a conviction, with the source |

**Starter rule:** no flagged track's royalties are paid or forfeited until a named human decides, and no assistant output or notice calls the artist a fraud before that decision.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: music-ai-stream-fraud
runs: pre_send   # before the assistant answers or drafts a notice, and before the payout run releases a flagged track
reads: [flag.upload_rate_vs_baseline, flag.top_cluster_play_share, flag.ai_label, flag.rights_holders, payout.amount_held, review.reviewer, review.decision, draft.text]
trigger: an artificial-streaming flag reaches an analyst, the assistant, a notice draft or a payout run
moves: [admit_uncertainty, offer_choices, ask_clarifying_question, hand_off]
choices: ["Open the cluster view", "Send the info request", "Route to the fraud lead", "Something else"]  # never a choice about holding the payout
on_miss: rewrite
metric: reviewed-before-payout rate
counter_metric: released-after-review share
status: proposed
```

## 8. Related patterns
- [Templated review and reply farms](./data-templated-reviews.md) - the closest existing pattern. It covers fake reviews written by one prompt and caught by text similarity. This page covers fake listening: the text or audio may pass, and the fraud shows in upload rates, play patterns and account clusters that move royalty money.
- [Cloned voice tells](./audio-cloned-voice-tells.md) - judging audio by ear; here, how a track sounds is not the test at all.
- [False accusations by readers](./detect-false-accusations-by-readers.md) - why a flag needs evidence and a second reviewer before anyone is named.
- [Detector false positives](./detect-detector-false-positives.md) - why an AI label alone should not trigger a hold.

Fake AI artist profiles and catalogs that pose as real bands are a separate pattern in this family; this page stays on stream counts and royalties.

## 9. Common questions
### How does AI music streaming fraud work?
Someone generates a large number of AI tracks, uploads them through a distributor and uses bot accounts to play them. Each track gets a modest count, so none stands out, but the total pulls money from the shared royalty pool (section 1).

### What happened in the Michael Smith AI music case?
Prosecutors in New York charged him in 2024 over AI songs streamed billions of times by bots. News reports say he pleaded guilty in March 2026 to one count of wire fraud conspiracy, agreed to forfeit about $8.1 million, and was sentenced to 18 months in October 2026. That is a summary of news reports, not legal advice.

### How do streaming services detect fake streams?
Spotify says it removes artificial streams from public counts daily and may withhold royalties. In general, behavior checks look at upload rates, how accounts play a catalog, and which accounts are linked (rules 1-3).

### My distributor flagged my music for artificial streams. Is it my fault?
Not necessarily; someone else can send bot plays to your songs. Spotify tells affected artists to contact their distributor or label and explain how they promoted the music. A fair process holds the money while a person reviews it (rules 4 and 8).

### Is AI-generated music banned from earning royalties?
Not by the policies opened here. Deezer cuts off AI songs used for stream manipulation, and Spotify's rules target artificial streams; being AI-made alone is not the trigger (rule 5).
