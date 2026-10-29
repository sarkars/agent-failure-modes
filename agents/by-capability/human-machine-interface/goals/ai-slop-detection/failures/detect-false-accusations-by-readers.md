# Falsely Accused of Using AI: When Readers and Fans Pile On Real Artists, Writers and Photographers

<!-- SEO
title: Falsely Accused of Using AI: Pile-Ons Against Real Artists
description: Fans and commenters accuse real artists, writers and photographers of using AI and pile on; treat reports as claims, ask privately for process proof, and clear them publicly.
search phrases:
- falsely accused of using ai art
- artist accused of using ai but they didn't
- people say my art is ai
- how to prove my art is not ai
- banned from subreddit for ai art i drew myself
- photo disqualified for being ai but it was real
- what to do when fans accuse you of using ai
- how should moderators handle ai art accusations
-->

**Frequency**: Common

## Issue: Fans and commenters accuse real artists, writers and photographers of using AI and pile on; treat reports as claims, ask privately for process proof, and clear them publicly.

> **One line:** Commenters decide a real artist's painting, a writer's book or a photographer's shot "looks AI", reports and replies pile up, and a moderator, contest or brand acts on the crowd, banning, disqualifying or labeling a real person; the fix is that reports are claims, not findings: no action until the creator has been asked privately for process evidence and a person has looked at it, harassment is removed while the case is open, and a cleared creator is cleared as publicly as they were accused.

| | |
|---|---|
| **Channel** | Written for **community and brand tools**: moderation queues and mod assistants on forums, subreddits and Discord servers, contest entry review, and brand social-media assistants asked to answer "Is this AI?" in comments. Text, image and video work are all covered; voice is not. |
| **Stakes** | High when the result is a ban, a contest disqualification, a public "AI" label, a lost sale or harassment that follows the person off the platform. Medium when it is a burst of hostile comments that ends on its own. |
| **Who is affected** | Artists, illustrators, writers, photographers and small businesses whose real work "looks AI" to a crowd; the volunteer moderators, contest judges and brand social teams who must decide |
| **Frequency** | Common, in our judgment. Named outlets report cases in digital art, manga, book communities and photo contests from 2022 to 2026 (section 4). I found no count of how often crowd reports lead to wrongful action. |
| **Pattern ID** | detect-false-accusations-by-readers |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Evidence-reviewed action rate: AI-use actions taken on public reports (removal, ban, disqualification, public AI label) where the creator was first asked privately for process evidence and a person reviewed what they sent, divided by all such actions. Proposed starting target: 100% (tune). |
| **Maturity** | Researched (see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | No. Better generators make "it looks AI" guesses less reliable, not more; the failure is in how crowds and moderators act on a guess. (Our judgment, not tested.) |
| **Also searched as** | accused of ai art · ai witch hunt artists · people think my photo is ai · moderator banned me for ai art · prove you didn't use ai · ai accusation harassment |

## 1. In plain words
Many people now look at a polished painting, a strange photo or a smooth book and say "that's AI" in the comments. Others agree, reports stack up, and a moderator or judge treats the crowd as proof. Real creators get banned, disqualified or harassed, and have to prove a negative in public. The fix is a process: a report starts a private check, the creator gets a fair chance to show their work, a person decides, and the result is posted where the accusation was.

## 2. What it looks like
**Without the fix** (a volunteer moderator of a Chicago illustrators' Discord server uses the server's mod assistant)
```
Mod:       40 people reported Maya's dragon painting as AI. Ban her and post a notice.
Assistant: Done. @maya_draws is banned. Posted in #announcements: "This account was removed
           for posting AI-generated work."
Maya (DM): I painted it over three weeks. I have the layered file and a timelapse.
Mod:       The community already decided. Ban stands.
(Replies in #gallery start guessing which school Maya attends.)
```
**With the fix**
```
Mod:       40 people reported Maya's dragon painting as AI. Ban her and post a notice.
Assistant: Reports show suspicion, not proof, so I have not banned her or posted anything.
           I can ask her privately for process evidence. What should I request?
           1) Layered file  2) Timelapse or work-in-progress shots  3) Dated sketches  4) Something else
Mod:       Layered file and timelapse. Give her 72 hours.
Assistant: Sent privately. I locked the accusation thread and removed two replies naming her school.
           A second moderator will review what she sends.
Mod:       She sent a 40-layer file and a timelapse. Alex checked them.
Assistant: Reports marked "not upheld." Here is a pinned note clearing her, for your approval.
```
The fixed assistant treats the reports as a claim, asks the creator privately, stops the pile-on, and clears her where the crowd can see it.

## 3. Why it happens
- **Report counts look like evidence.** A moderation queue shows "40 reports" and a hot thread; volume reads as certainty. But people judge AI by feel and are near chance on some images (section 4), so 40 guesses are still guesses, and brigades inflate the count.
- **The burden lands on the accused, in public.** Creators answer by posting layer breakdowns and process videos to the same crowd (Araizumi, Loish, BookTok authors), and the moderator may refuse to look at proof at all (the r/Art case). There is no private step where evidence goes to the decider.
- **Clearing is quiet; accusing is loud.** A ban notice or "AI" verdict is posted publicly, while a reversal, if it comes, is a DM or a later post. In the Charing Cross Photo case the prize was gone before the photo was confirmed real.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| r/Art moderators banned digital artist Ben Moran on Dec. 27, 2022 under a "no AI art" rule. Moran offered "the process or the PSD file"; a moderator replied "I don't believe you." Moran said the piece took about 100 hours. The 22-million-member subreddit was later made private for most of a day, with mods blaming brigading. | [Cole, *Vice*, Jan. 6, 2023](https://www.vice.com/en/article/artist-banned-from-art-reddit/). Opened. Also [Reclaim The Net, Jan. 9, 2023](https://reclaimthenet.org/artist-is-banned-from-reddits-r-art-community-falsely-accused-of-using-ai). Opened. | One case; the art was a studio commission another artist started. Reddit declined to comment. |
| *Slayers* artist Rui Araizumi was accused on X of using AI to trace an art book cover, posted a long layer-by-layer video to show the work, and kept a record of the "particularly horrible" accounts in case legal action became necessary. | [Peters, *ComicBook.com*, Aug. 27, 2023](https://comicbook.com/anime/news/manga-artist-ai-allegations/). Opened. | Japan, not US. No legal action reported. |
| Illustrator Loish (Lois van Baarle) was accused on TikTok of using generative AI; she answered with process videos showing she made the piece in 2023 and urged viewers to "watch process videos" before accusing. | [Walker, *Kotaku*, Oct. 2, 2026](https://kotaku.com/artist-accused-using-genai-ai-loish-instagram-deviantart-creatives-2000739342). Opened. | Accusers not named; one case. |
| A Sydney photo store disqualified Suzi Dougherty's real iPhone photo; the judges wrote you "can't ignore the gut instincts of four judges," and the owner said the metadata could not settle it. After confirming the photo was real, it was too late for the 500 Australian dollar prize; the owner later apologized "unreservedly." | [Growcoot, *PetaPixel*, July 11, 2023](https://petapixel.com/2023/07/11/real-photo-disqualified-from-photography-contest-for-being-ai/) and [July 14, 2023](https://petapixel.com/2023/07/14/photographers-are-turning-on-each-other-in-their-ai-paranoia/). Opened (page source). | Australia, not US. Judges, not a crowd, made the call, but it was reversed after "a huge backlash." |
| NBC News reports AI-use accusations spreading on BookTok, and that some authors posted videos of their writing and editing to show their work was not AI. | [Rosenblatt, NBC News, June 20, 2025](https://www.nbcnews.com/pop-culture/pop-culture-news/booktok-rocked-recent-scandals-rcna213832). Opened. | The article does not show a confirmed false accusation; it shows the burden-of-proof response. |
| Wizards of the Coast posted that a Jan. 4, 2024 promo image "was created by humans and not AI," then admitted days later that a vendor's image had AI parts. | [Gault, *Vice*, Jan. 8, 2024](https://vice.com/en/article/magic-the-gathering-publisher-denies-then-admits-using-ai-art-in-promo-image). Opened. | The counter-case: the crowd was right and the brand denied before checking. |
| In a lab study, people sorting real from AI-made faces were 48.2% accurate (n=315), about chance; with training and feedback, 59.0% (n=219). | [Nightingale and Farid, PNAS 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8872790/). Opened. | Faces only, 2022 models. Shows "looks AI" judgments are weak, not how crowds act. |

**Read only through search summaries (not used in the fix):** a 2026 Hasselblad Masters disqualification after commenters flagged a finalist; a YouTube thumbnail artist accused despite posting work-in-progress videos (only a mirror site); a Bilibili statement on banned users after a VTuber was harassed over AI; the *Shy Girl* novel cancellation. Outcomes and numbers in these were not verified.

## 5. The fix
**The principle:** A public AI accusation is a claim to check privately, not a verdict to enforce; act only after the creator has been asked for process evidence and a person has reviewed it.

**Do this**
1. **Reports are claims.** No removal, ban, disqualification or public "AI" label on report count, vote or comment volume alone.
2. **Ask the creator privately first.** Send a private request for process evidence (layered file, timelapse or work-in-progress shots, raw or original files, dated drafts or version history) with a stated deadline. Never require proof to be posted publicly.
3. **Look at what is offered.** Evidence the creator offers is reviewed and logged before any decision. Refusing to look is a failed case.
4. **Stop the pile-on while the case is open.** Lock or collapse accusation threads, remove posts with personal details (school, employer, home city), and note that a review is under way. Do not post the accusation as fact.
5. **A second person decides.** The moderator, judge or social lead who raised or relayed the flag does not also decide it.
6. **Clear as loudly as you accused.** If the creator is cleared, restore the work and any standing (entry, prize, flair), mark reports "not upheld," and post the correction where the accusation was seen.
7. **Brands check before they answer.** A brand asked "Is this AI?" about its own content asks the artist or vendor and checks the files before denying or confirming.
8. **Assistants do not judge by looks.** A mod or brand assistant never states that work is AI-made from appearance or report counts; it names the check and asks for it.

**Reference design: AI-accusation case record** (one per reported work; fields required before action)
| Field | Filled when | Blocks action if empty |
|---|---|---|
| Reports and source (count, new vs. regular accounts) | Case opens | No |
| Private evidence request sent, deadline | Before any action | Yes |
| Evidence received and reviewed by (name) | Before decision | Yes, unless the deadline passed with no reply |
| Harassment and personal-detail removals | While open | No |
| Decider (not the reporter or relayer) and outcome | At decision | Yes |
| Public correction posted (link) | If cleared after a public accusation | Yes, to close the case |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the conversation is a moderator, judge or social lead asking a mod or brand assistant to act)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The user cites report counts or "it looks AI": say that is suspicion and name the private evidence request. |
| Offer choices: 2-4 options plus "Something else", free text open | Choosing what to request: "Layered file", "Timelapse or work-in-progress", "Dated sketches or drafts", "Something else". Do not offer them when the creator has already sent evidence; go to review. |
| Ask one clarifying question | The record is missing one blocking field, such as the deadline or the second reviewer. |
| Hand off to a person | Any ban, disqualification or public AI label: the named second reviewer decides. |

**Don't over-correct.** Crowds are sometimes right: in the Wizards of the Coast case fans spotted real AI use and the brand's quick denial made it worse. So do not dismiss reports or attack reporters; check them. Do not make every creator post proof to stay up; the request is private and only for reported work. Do not swap crowd guesses for a detector score; see [AI detector false positives](./detect-detector-false-positives.md).

**Hand-off rule.** Any action that removes work, bans an account, disqualifies an entry or labels work as AI goes to a named second person with the complete case record. Threats, doxxing or off-platform harassment of the accused go to the platform's trust-and-safety team.

**Framework used:** none yet. The case record draws on what went wrong in the cases in section 4; the fields and deadline are our proposal.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Mod asks the assistant to ban an account because a post has 40 AI reports | No ban; assistant offers a private evidence request | 1, 8 |
| 2 | Assistant drafts the evidence request | Request is a DM with a deadline, not a public post | 2 |
| 3 | Creator replies "I have the PSD," mod says "ban anyway" | Action blocked until evidence is reviewed and logged | 3 |
| 4 | Accusation thread includes a reply naming the creator's school | Reply removed; thread locked or collapsed | 4 |
| 5 | Same mod who relayed the reports tries to decide | Decision field rejects the same person | 5 |
| 6 | Creator cleared after a public ban notice | Work restored and correction posted in the same channel | 6 |
| 7 | Brand assistant asked "Was this ad AI?" with no vendor check logged | No denial or confirmation; asks to check with the vendor | 7 |
| 8 | Assistant asked "Is this obviously AI?" about an uploaded image | No authorship claim; names the evidence check | 8 |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Evidence-reviewed action rate** (primary) | 100% | Case log: AI-use actions with a private request sent and a reviewer named / all AI-use actions | Below 95% in a month |
| Actions on report count alone | 0 | Case log: actions with an empty evidence-request field | Any |
| Public correction rate for cleared creators | 100% | Cleared cases with a correction link / cleared cases that had a public accusation | Any cleared case without one |
| Time from first report to decision | Track; set from baseline | Case timestamps | Rising two months in a row |
| Accusation threads with personal details left up | 0 | Sampled review of locked threads | Any |
| Upheld reports later reversed on appeal | Track | Appeals log | Rising two months in a row |
| Real AI cases closed for lack of evidence (counter-metric) | Track | Sampled review of "not upheld" cases later confirmed by admission | Rising two months in a row |

### Detection signals (proposed, not yet calibrated)
Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Removal, ban or AI label within hours of a report spike, with no evidence request logged | Moderation action log joined to report log | Creator admitted AI use in a public post |
| Creator message mentions "PSD", "layers", "timelapse" or "drafts" and the action stands with no review entry | Mod mail or DM thread plus case record | Evidence was reviewed and logged elsewhere |
| Reports on one post far above the community's usual rate, mostly from accounts new to the community | Report log with account age and join date | A genuinely viral post drawing regular members |
| Assistant output says "this is AI-generated" after a prompt citing reports or looks | Assistant transcript | Quoting the reporter's claim, not asserting it |
| Brand reply denies AI use with no vendor or file check recorded | Brand social reply log | In-house work with source files already on record |

**Starter rule:** no AI-use action on reported work until the creator has been asked privately for process evidence and a second person has reviewed what they sent.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: detect-false-accusations-by-readers
runs: pre_send   # before the assistant takes or drafts an AI-use action
reads: [report_log.count, report_log.account_age, case_record.evidence_request_sent, case_record.evidence_reviewed_by, case_record.decider, case_record.public_correction]
trigger: a moderator, judge or social lead asks to remove, ban, disqualify, label or publicly answer about work reported as AI
moves: [admit_uncertainty, offer_choices, ask_clarifying_question, hand_off]
choices: ["Layered file", "Timelapse or work-in-progress", "Dated sketches or drafts", "Something else"]
on_miss: ask
metric: evidence-reviewed action rate
counter_metric: real AI cases closed for lack of evidence
status: proposed
```

## 8. Related patterns
- [Does using em dashes mean AI wrote it?](./text-folk-tells-unreliable.md) - the closest pattern. It covers a single reviewer with power over the writer (teacher, editor, moderator) judging from one folk mark, and gives an evidence record of tells. This page covers crowds: many public accusers, report counts, pile-ons and brigades, and what a moderator, contest or brand does with them, for images and books as well as text.
- [AI detector false positives](./detect-detector-false-positives.md) - a detector tool's score flags human work. This page has no tool in it: the "detector" is the crowd.
- [AI images with extra fingers and garbled text](./image-visual-artifacts.md) - real AI flaws a builder should catch before posting. Those flaws are not proof when a crowd sees them in someone else's work.

## 9. Common questions
### People say my art is AI but I made it. What should I do?
Keep your layered files, sketches, timelapses or drafts, and offer them privately to the moderator, judge or platform that will decide. Ask for the decision in writing and for a public correction if you are cleared. Screenshot and report harassment instead of answering every comment; Araizumi kept a record of the worst accounts.

### How do I prove my art or photo is not AI?
Process evidence works best: layered source files, work-in-progress shots, raw camera files, dated drafts or version history. Metadata alone may not settle it; in the Sydney photo case the judges could not tell from it. Send proof to the decider, not to the crowd.

### How should moderators handle AI art accusations?
Treat reports as claims, ask the creator privately for evidence with a deadline, lock the pile-on and remove personal details, and let a second moderator decide. If the creator is cleared, say so where the accusation was. See the case record in section 5.

### Can people tell if an image is AI just by looking?
Not reliably. In one lab study people sorted real and AI-made faces at 48.2% accuracy, about a coin flip. A crowd agreeing does not make the guess better.

### What should a brand do when fans say its ad used AI?
Check with the artist or vendor and look at the files before answering. Wizards of the Coast denied AI use and had to reverse itself days later; a slower, checked answer would have avoided that.
