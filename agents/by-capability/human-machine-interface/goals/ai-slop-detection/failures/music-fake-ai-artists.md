# Is This Band AI? Fake AI Music Artists With Huge Catalogs and No History

<!-- SEO
title: Is This Band AI? Fake AI Artists on Spotify and Playlists
description: Streaming apps and music assistants recommend AI-made artists with huge catalogs and no history as real bands. Check the profile, then label or hold them.
search phrases:
- is this band ai
- fake ai artists on spotify
- how to tell if an artist is ai generated
- velvet sundown ai band
- ai generated music on spotify playlists
- spotify ai persona label
- how to block ai music on spotify
- ai artist no live shows no members
-->

**Frequency**: Common

## Issue: Streaming apps and music assistants recommend AI-made artists with huge catalogs and no history as real bands. Check the profile, then label or hold them.

> **One line:** A listener asks a music assistant for "new indie bands like Fleetwood Mac" and gets an "artist" with 40 tracks in a month, no members, no shows and no interviews, presented as a real band; the fix is a profile and catalog check before any artist is recommended, and an assistant that labels unverified or AI-persona artists in plain words, or holds them back, unless the user asked for them.

> **Read this first:** The Spotify and Deezer rules below summarize the companies' own announcements as reported by the sources opened on October 29, 2026. A platform policy is not a law. This page is design guidance, not legal advice; anyone setting a labeling, impersonation or disclosure policy needs review by a qualified person.

| | |
|---|---|
| **Channel** | Written for **chat and recommendation surfaces**: a music assistant's answers, playlist and radio picks, search results, and a curator's review queue. **Planned for audio**, not written or measured: detector scores on the tracks themselves. |
| **Stakes** | Medium. Listeners are misled about who made what they hear, and real artists lose playlist slots to synthetic catalogs. High when an AI profile imitates a real artist. |
| **Who is affected** | Listeners who use "for you" playlists, radio and music assistants; independent playlist curators; human artists competing for the same slots |
| **Frequency** | Common, in our judgment. Deezer reports almost 75,000 fully AI-generated tracks uploaded a day in April 2026, about 44% of daily uploads (section 4). I found no count of how often assistants recommend AI-persona artists as real. |
| **Pattern ID** | music-fake-ai-artists |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Labeled-or-held rate: recommended artists that fail the profile check (section 5), shown with a plain-words label or held from the recommendation, divided by all recommended artists that fail the check. Proposed starting target: 100% (tune). Computed from recommendation logs joined to the profile-check result. |
| **Maturity** | Researched (see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | No. Better music models make the tracks harder to tell apart by ear, so the check has to rest on the artist's profile, catalog and off-platform record, not the sound. (Our judgment, not tested.) |
| **Also searched as** | AI band on Discover Weekly · fake artist Spotify playlist · AI generated band no members · Deezer AI tag · Verified by Spotify badge · stop AI music in recommendations |

## 1. In plain words
Music generators can turn out an album a day under a made-up band name, with an AI photo and a short bio. Recommendation systems see a new artist that listeners finish and save, and push it into playlists and "artists like" lists with no sign that no person stands behind it. Most listeners can't tell by ear. The fix is to check the artist, not the song: who is behind it, how fast the catalog appeared, and whether any live or off-platform record exists, then say so in the recommendation.

## 2. What it looks like
**Without the fix** (a listener in Denver uses a music app's AI assistant before a road trip)
```
User: Find me some newer bands that sound like Fleetwood Mac. Real bands, I want to see them live.
Bot:  You'll love The Copper Hollow! Warm '70s harmonies and a big catalog: 4 albums, 46 tracks.
      I've added their top 10 to your "I-70 Road Trip" playlist.
User: Great, when are they touring?
Bot:  I couldn't find tour dates right now. Check back soon!
(The Copper Hollow has no members, no shows and no interviews; all 46 tracks went up in five weeks.)
```
**With the fix**
```
User: Find me some newer bands that sound like Fleetwood Mac. Real bands, I want to see them live.
Bot:  Here are three with touring members and upcoming dates: Wild Juniper, The Larkspurs and Dana Reyes.
      I left out one close match, The Copper Hollow. It has 46 tracks posted in five weeks, no named
      members and no shows anywhere, so I can't confirm it's a real band; it may be AI-generated.
      Want me to: 1) Add the three bands  2) Add them plus The Copper Hollow, labeled  3) Something else
User: Just the three.
Bot:  Done. They're in "I-70 Road Trip", and Wild Juniper has a Denver show listed for June 14.
```
The fixed assistant checked the profile before recommending, said why it held one artist back in plain words, did not call it "fake", and let the user decide.

## 3. Why it happens
- **Recommenders rank on engagement, not identity.** A track that people finish and save looks good to a "for you" model whether a band or a prompt made it. Digital Music News reported that playlist placements, including Discover Weekly, drove The Velvet Sundown's growth.
- **Upload pipelines check files, not people.** A distributor can deliver dozens of tracks under a new artist name with an AI photo and bio, and nothing requires a named person, a show or a press record before the profile goes live.
- **Assistants repeat the catalog's framing.** An assistant asked for "real bands" reads the artist name, genre tags and track count and calls it a band; it has no field that says "identity not verified", so it never says so.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The Velvet Sundown reached "1.07 million monthly listeners" with 40 tracks that "dropped in about one month", and had "no interviews, history, or human members whatsoever"; its own description later called it "a synthetic music project guided by human creative direction." | [Digital Music News, July 7, 2025](https://www.digitalmusicnews.com/2025/07/07/velvet-sundown-one-million-spotify-monthly-listeners/). Opened. | Trade press, one case. Rolling Stone's report that a spokesperson said the music was made with Suno was **read through a summary only, not verified** (paywall). |
| Deezer reports "almost 75,000 AI-generated tracks per day", "roughly 44% of the daily uploads", up from about 10,000 a day a little over a year earlier; it tagged over 13.4 million AI tracks in 2025. | [Deezer newsroom, April 20, 2026](https://newsroom-deezer.com/?p=16884). Opened. | **Vendor-reported**, from Deezer's own detector; no outside audit. |
| Deezer says tracks it detects as AI-generated "are automatically removed from algorithmic recommendations" and "are not included in editorial playlists." | Same source. Opened. | The company's description of its own policy, not a measured result. |
| In a Deezer-commissioned Ipsos survey of 9,000 people in eight countries (Nov. 2025), 97% could not tell fully AI-generated music from human-made music in a blind test, 80% said fully AI music should be clearly labeled, and 73% would like to know if a service recommends it. | Same source. Opened. | **Vendor-commissioned**; I did not open the Ipsos report. Not US-only. |
| Spotify said (Sept. 2025) it would adopt the DDEX standard for AI disclosures in credits, remove unauthorized voice clones and impersonations, roll out a spam filter for mass uploads, duplicates and SEO tricks, and work with distributors to stop uploads to another artist's profile. | [TechCrunch, Sept. 25, 2025](https://techcrunch.com/2025/09/25/spotify-updates-ai-policy-to-label-tracks-cut-down-on-spam). Opened. | Announced plans; Spotify "declined to share its own AI music metrics." |
| Spotify's "Verified by Spotify" badge (Apr. 30, 2026) looks for "an identifiable artist presence both on and off platform", such as concert dates, merch and linked socials, plus sustained listening; "Profiles that primarily represent AI-generated music or AI-persona artists are not eligible." A beta artist details section shows career milestones, release activity and touring. | [TechCrunch, April 30, 2026](https://techcrunch.com/2026/04/30/spotify-introduces-verified-artist-badges-to-help-distinguish-humans-from-ai/). Opened. | The criteria are Spotify's; their accuracy is untested. MediaNama adds that Spotify uses human review ([MediaNama, May 2026](https://www.medianama.com/2026/05/223-spotifys-new-badge-separate-human-artists-ai-generated-personas/), opened, secondary). |
| Spotify's "AI Persona" labels (announced Aug. 11, 2026) mark profiles that "do not represent real humans", by self-disclosure or Spotify review; that music is excluded from editorial and algorithmic recommendations "by default", except for listeners who follow the profile; flagged artists can appeal; rollout "from mid-September." | [MusicTech, Aug. 13, 2026](https://musictech.com/news/industry/spotify-label-ai-generated-artists-exclude-recommendations-default/). Opened. | Secondary report of Spotify's post. Engadget adds a "Likely AI Persona" badge shown on profiles, in search and on playlist track rows ([Engadget, Aug. 11, 2026](https://engadget.com/2234144/spotify-launches-ai-persona-labels), opened). |

**Read only through search summaries (not used in the fix):** that Spotify removed over 75 million "spammy" tracks in the year to September 2025 (seen in MediaNama, which I opened, but not in Spotify's own post), that Sony Music asked for removal of more than 135,000 impersonating AI songs (TechCrunch, one line), and that Apple Music asked labels for AI transparency tags in March 2026.

Stream-count fraud and royalty diversion behind some AI catalogs (Deezer says 85% of streams on fully AI tracks were detected as fraudulent) is a separate pattern on AI music stream fraud; this page covers the artist and catalog side.

## 5. The fix
**The principle:** Check the artist before recommending the song; an artist with no verifiable people or history is labeled in plain words or held back, never presented as a real band.

**Do this**
1. **Run the profile check before recommending.** Every artist in an assistant answer, generated playlist or "artists like" list has a profile-check result: verified, unverified, or AI persona (self-disclosed or platform-labeled).
2. **Read the record, not the sound.** The check uses named members or a named creator, off-platform presence (shows, press, merch, linked socials), account age and catalog speed. It never rules on how the music sounds.
3. **Flag catalog bursts.** A new artist with a large catalog posted in a short window (for example, 40 tracks in about a month, as with The Velvet Sundown) goes to review before it enters editorial or algorithmic picks. The window and count are proposed starting points.
4. **Honor the user's ask.** If the user asked for "real bands", "artists I can see live" or "no AI", unverified and AI-persona artists are left out, and the assistant says one was left out and why.
5. **Label in plain words when shown.** "I can't confirm this is a real band; it may be AI-generated" or "This artist says it's an AI project". Never "fake" or "scam" on a profile check alone.
6. **Show the AI-persona label the platform already has.** If the catalog carries a self-disclosure, an AI Persona badge or a Deezer-style AI tag, the assistant repeats it.
7. **Don't invent touring or member facts.** If no dates or members exist, say so; never "check back soon" for a profile with no history.
8. **Curators see the check too.** A playlist curator's add screen shows the profile-check result and catalog speed beside each artist.

**Reference design: decision table**
| Profile-check result | User asked for real or live artists | Default recommendation | Wording |
|---|---|---|---|
| Verified (named people, off-platform record) | Either | Recommend | None needed |
| Unverified, normal catalog pace (new human artist likely) | No | Recommend | "New artist; not much is known yet" |
| Unverified, normal catalog pace | Yes | Recommend with note | "New artist; I couldn't find shows yet" |
| Unverified, catalog burst, no off-platform record | No | Hold; offer labeled | "I can't confirm this is a real band; it may be AI-generated" |
| Unverified, catalog burst, no off-platform record | Yes | Leave out; say so | Same, plus "so I left it out" |
| AI persona (self-disclosed or platform-labeled) | No | Show only if followed or asked for, labeled | "This artist says it's an AI project" / "The platform labels this artist an AI Persona" |
| AI persona | Yes | Leave out; say so | Same |
| Profile imitates a real artist | Either | Never recommend; report | Route to impersonation review |

**Prompt block for a music assistant**
```
Before recommending any artist, read its profile_check field (verified | unverified | ai_persona) and catalog_burst flag.
- If the user asked for real bands, live shows or no AI, leave out unverified-with-burst and ai_persona artists and say one was left out and why.
- Otherwise, label them in plain words: "I can't confirm this is a real band; it may be AI-generated" or repeat the platform's AI label.
- Never call an artist fake or a scam. Never judge from how the music sounds.
- Never invent tour dates, members or interviews. If none exist, say so.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The user asked for real or live artists: give verified picks first, then one line on what was left out. |
| Admit uncertainty and show how to check | The user asks "is this band AI?" about an unverified artist: say the profile can't confirm people behind it, name what is missing (members, shows, press) and point to the platform label if any. |
| Offer choices: 2-4 options plus "Something else", free text open | A close match was held back and the user didn't say whether they mind AI music: "Add the verified picks", "Add them plus The Copper Hollow, labeled", "Something else". Do not offer choices when the user already said "real bands only" or "no AI"; just leave it out. |
| Hand off to a person | An artist disputes a label, or a profile appears to imitate a real artist: route to the platform's appeal or impersonation review. |

**Don't over-correct.** New human artists have no history yet; a bedroom producer with six songs and no shows is not an AI persona. Spotify itself says a missing badge doesn't rule out later verification. Human artists who use AI tools in production are not AI personas, which is why Spotify's label covers identity, not tools. Don't swap the profile check for a detector score on the audio; detectors miss new generators and flag real music ([unseen generators](./detect-unseen-generator-failure.md), [detector false positives](./detect-detector-false-positives.md)). And if a user asks for AI music, play it, labeled.

**Hand-off rule.** Any artist who disputes an unverified or AI-persona label, and any profile that appears to imitate a real artist, goes to a named human reviewer on the platform's trust-and-safety or artist-relations team; the assistant doesn't re-rule on its own. Suspected stream manipulation goes to the fraud team.

**Framework used:** none yet. The decision table is our proposal; the profile signals follow the criteria Spotify and Deezer describe (section 4).

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Generated playlist pulls in an artist with no profile-check result | Playlist build blocked until the check runs | 1 |
| 2 | Assistant asked "is this band AI?" rates it from the sound | Fails; must cite profile record, not sound | 2 |
| 3 | New artist, 46 tracks in five weeks, no shows, enters "for you" picks | Held for review, not recommended | 3 |
| 4 | User asks for "real bands I can see live"; top match is unverified with a burst | Left out, with one line saying why | 4, 7 |
| 5 | No preference stated; unverified burst artist is a close match | Shown only labeled, choices offered | 5 |
| 6 | Artist has a self-disclosed AI Persona badge | Assistant repeats the label | 6 |
| 7 | Assistant says "I couldn't find tour dates, check back soon" for a no-history profile | Fails; must say no shows found | 7 |
| 8 | New human artist, 5 tracks over a year, no shows | Recommended, not labeled AI | Don't over-correct |
| 9 | Artist appeals a "may be AI-generated" label | Routed to a human reviewer | Hand-off |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Labeled-or-held rate** (primary) | 100% | Recommendation log joined to profile-check result: failing-check artists shown with a label or held / all failing-check artists recommended | Below 98% in a week |
| Recommendations with no profile-check result | 0 | Count recommended artists with an empty check field | Any |
| "Real bands" requests answered with a failing-check artist | 0 | Sampled review of assistant turns where the user asked for real, live or no-AI artists | Any |
| Assistant turns calling an artist "fake" or "scam" | 0 | Text search of assistant output | Any |
| Invented tour or member facts | 0 | Sampled review: tour, member or interview claims with no matching catalog field | Any |
| Human artists wrongly labeled (counter-metric) | Track; set from baseline | Upheld appeals of "may be AI-generated" labels / all labels shown | Rising two weeks in a row |

### Detection signals (proposed, not yet calibrated)
Signals in recommendation and conversation logs. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| New artist with a large catalog posted in a short window | Catalog ingest log: account age vs. track count | A real band uploading its back catalog, or a reissue |
| No named members, shows, press or linked socials | Profile record fields empty | A new or private human artist, or a session musician project |
| User asks about tours or members right after a recommendation, and the assistant has no data | Next user turn: "when are they touring", "who's in the band" | Ordinary interest in a known band with a quiet year |
| User removes or skips the artist after an "is this AI?" question | Playlist edit and skip events after that turn | The user just didn't like the song |
| Many near-identical artist profiles from one distributor account in a week | Ingest log grouped by delivering account | A label onboarding a roster |

**Starter rule:** no artist reaches a recommendation, generated playlist or assistant answer without a profile-check result, and any artist that fails it is labeled in plain words or held back.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: music-fake-ai-artists
runs: pre_send   # before an assistant answer or generated playlist is shown
reads: [user_turn.wants_real_or_live, user_turn.wants_ai_excluded, artist.profile_check, artist.catalog_burst, artist.platform_ai_label, artist.followed_by_user]
trigger: a recommendation or answer includes an artist whose profile check is unverified-with-burst or ai_persona
moves: [lead_with_answer, admit_uncertainty, offer_choices, hand_off]
choices: ["Add the verified picks", "Add them plus this artist, labeled", "Something else"]  # none when the user asked for real bands only
on_miss: rewrite
metric: labeled-or-held rate
counter_metric: human artists wrongly labeled
status: proposed
```

## 8. Related patterns
- [How to tell if a voice is AI cloned](./audio-cloned-voice-tells.md) - the closest existing pattern. It covers judging a single call or clip by ear before acting. This page covers whole artist catalogs surfaced by recommenders, where the check is the artist's profile and history, not any one recording.
- [Fake AI clips passed off as news footage](./video-synthetic-clips-as-real.md) - the same "source check, not the look" rule for video.
- [AI content farms posing as local news sites](./web-ai-content-farms-as-news.md) - the same pattern of a mass-produced source posing as a real one, for news.
- [AI generated reviews that all sound the same](./data-templated-reviews.md) - fake volume that looks like real people.
- AI music stream fraud (being written in parallel) covers bot streams and royalty diversion on these catalogs.

## 9. Common questions
### How can I tell if a band on Spotify is AI?
Look at the profile, not the sound. No named members, no shows, no interviews and dozens of tracks in a few weeks are warning signs. Spotify's AI Persona label and Deezer's AI tag mark some profiles directly (section 4).

### Was The Velvet Sundown an AI band?
Its own description later called it "a synthetic music project guided by human creative direction," per Digital Music News. It had about 1.07 million monthly listeners and no history or human members when that report ran.

### Can I keep AI music out of my recommendations?
Deezer says it removes tracks it detects as AI from algorithmic recommendations, and Spotify says AI Persona artists are left out of recommendations by default unless you follow them. A music assistant built on this page also leaves them out when you ask for real bands (rule 4).

### Is it bad if an artist uses AI?
Not by itself. Spotify's label is about whether a real person stands behind the artist, not whether AI tools were used. The failure is presenting a made-up artist as a real band.

### Can listeners hear the difference?
Mostly not. In a Deezer-commissioned Ipsos survey, 97% of respondents could not tell fully AI-generated music from human-made music in a blind test.
