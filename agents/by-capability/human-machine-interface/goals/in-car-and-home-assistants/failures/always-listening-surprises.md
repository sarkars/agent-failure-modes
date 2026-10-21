# Smart Speaker Recordings: Review and Delete, and the Always-Listening Surprise

<!-- SEO
title: Smart Speaker Recordings: Review and Delete What It Heard
description: People learn later that a home or car voice assistant recorded and kept their voice. Show what was heard and let people delete it, in one step.
search phrases:
- smart speaker recordings review delete
- voice assistant accidental recording
- how to see what alexa recorded
- delete google assistant voice recordings
- does my smart speaker keep recordings
- alexa recorded something I didn't say to it
- always listening assistant privacy design
-->

**Frequency**: Common

## Issue: People learn later that a home or car voice assistant recorded and kept their voice; the fix is to show what was heard and let them delete it.

> **Read this first.** This page is design guidance for testing your own product. It is not legal advice. Privacy, children's-data, recording and consent rules differ by state and country, and a retention or deletion design needs counsel's review before use (flag L: legal review needed). The only legal-adjacent facts here are what the FTC said in one 2023 press release and what vendor help pages say about their own products. Whether your product complies with any law is not answered here.

> **One line:** The assistant keeps what it heard, nobody tells the household, and the history is hard to find or hard to delete.

| | |
|---|---|
| **Channel** | Written for what a person can read: a history screen or app, the transcript of each entry, and a delete control (text-observable). Voice signals (false wake-ups, audio-clip logs, "delete what I just said" by voice) are **PLANNED**, not written or measured here. |
| **Stakes** | Medium to high. Kept audio of a private moment, a guest, or a child cannot be taken back once shared or used. |
| **Who is affected** | Owners, and also guests, children and partners who never set the device up |
| **Frequency** | Common (our judgment). One peer-reviewed survey found many owners did not know recordings were kept (section 4); I found no rate for how often devices keep audio nobody meant to send. |
| **Pattern ID** | always-listening-surprises |
| **Family** | [In-car and home assistants](../README.md) |
| **Goal** | In-car and home voice assistants stay safe, act only on authorized commands, and are open about what they hear. |
| **Primary metric** | Households that review or delete at least one history entry in 90 days. Starting point: 20% (an unsourced guess to tune on your own data; read it with the complaint counter-metric in section 7). |
| **Maturity** | Researched (no test file yet; see the [content program](../../../roadmap/content-program.md)). Flag L: legal review needed. |
| **Will a better model fix this?** | No. What is kept, for how long, and whether people can see and delete it are product and policy choices, not model quality. (Our judgment, not tested.) |
| **Also searched as** | alexa history · google assistant activity audio · speaker recorded us without asking · voice assistant keeps recordings · delete my voice data · unexpected recording complaint |
| **Flag** | L |

## 1. In plain words
A speaker in the kitchen or an assistant in the car turns some of what it hears into stored audio and transcripts. The surprise is finding out later, from a news story, a family member or a settings page nobody opened. The fix is a plain-words history of what was heard and kept, shown without being asked, with a delete button on every entry.

## 2. What it looks like
Made-up household and assistant, for illustration.

**Without the fix**
```
[Saturday. A guest asks the owner why the speaker's light came on during dinner.]
Guest: Does that thing keep what we say?
Owner: No idea. It only records when you say its name, I think.
(Weeks later the owner opens the app's privacy section, buried three screens deep: 214 entries, including
 dinner-party audio, a child's voice, and "no speech detected" clips. Delete is "all history" or nothing.)
```

**With the fix**
```
Assistant (first setup, and monthly): I keep a record of what I hear after my name, so you can review it.
  This month: 41 requests, 3 clips I may have caught by mistake. Nothing else is stored.
  [Review] [Delete the 3 mistakes] [Delete everything] [Change how long I keep things]
Owner (later): "What did you keep from Saturday?"
Assistant: Two requests, the timer at 6:10 PM and a song at 7:30 PM. One clip at 8:45 PM I think was
  a mistake. Say "delete the 8:45 clip" or tap Delete.
```
The fixed version says what is kept without being asked, flags likely mistakes, and makes a single entry deletable with its confirmation naming what went.

## 3. Why it happens
- **The history is a settings page, not part of the product.** Retention exists for the vendor's reasons (answering requests, improving recognition), so the review and delete screens are built last and buried.
- **Default is keep.** Many products keep by default and offer deletion as an opt-in chore, so the household's first sight of the record is by accident.
- **No one told the guests.** The person who set the device up consented; the child and the dinner guest did not, and nothing on the device tells them.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a survey of 116 owners of Amazon and Google smart speakers, almost half "did not know that their recordings were being permanently stored and that they could review them." Only about a quarter reported reviewing their interactions, and very few had ever deleted any. Participants were more protective of recordings of others, such as children and guests. | [Malkin et al., *Privacy Attitudes of Smart Speaker Users*, PoPETs 2019](https://par.nsf.gov/biblio/10109137-privacy-attitudes-smart-speaker-users). I read the abstract on the NSF record; the full PDF would not extract. | 116 people, self-reported, 2019 products. The quotes and fractions are the abstract's; I did not check the paper's body. |
| On May 31, 2023 the FTC announced a complaint and proposed order against Amazon over Alexa. It alleged Amazon kept children's voice recordings indefinitely unless a parent asked for deletion, and that after a parent asked, transcripts of what children said stayed in some databases. The proposed order carries a $25 million civil penalty, deletion of certain recordings and inactive child accounts, and notice to users about retention and deletion controls. The release says the order "must be approved by the federal court to go into effect." | [FTC press release, May 31, 2023](https://www.ftc.gov/news-events/news/press-releases/2023/05/ftc-doj-charge-amazon-violating-childrens-privacy-law-keeping-kids-alexa-voice-recordings-forever). Opened and read. | Allegations in a complaint plus a proposed settlement, not findings of fact. About children's data under one law; I did not verify whether the court entered the order, and Amazon's response is not in the text I read. |
| Google's help page says audio in Web and App Activity can be played back by item, deleted per item or in bulk, and auto-deleted on a schedule; turning the setting off stops new saves but does not delete earlier audio; and "audio may be saved" when a device wrongly detects an activation. | [Google Account Help: Manage audio recordings in your Web & App Activity](https://support.google.com/accounts/answer/6030020). Opened and read (paraphrased). | Vendor documentation of one product. Shows the controls exist; says nothing about how many people find or use them. Bulk delete also removes non-audio activity. |

I could not open the FTC page's full order or the complaint PDF, Amazon's own help page (it returned a 503), or the Northeastern misactivation paper. A YouGov survey on awareness of voice storage appeared only in a search summary; I read it through a summary only and did not use its numbers.

**Public incident.** The FTC matter above is the dated, public case about kept voice recordings and deletion. The related [Amazon Alexa dollhouse purchases](../../../incidents/amazon-alexa-voice-orders-dollhouses-after-tv-broadcast-january-2017.md) page covers a purchase triggered by a broadcast, which this page does not.

## 5. The fix

**The principle:** The household can see what the assistant heard and kept, in plain words, and can delete any of it in one step.

**Do this**
1. **Tell people what is kept, before they ask.** At setup and again on a schedule you choose (starting point: monthly), say in one line what is stored (audio, transcript, or neither) and for how long.
2. **Show a history of what was heard.** Each entry shows time, device or room, the words heard, what the assistant did, and whether audio is kept.
3. **Flag likely mistakes.** Mark activations with no clear request ("heard, no request found") so a person can delete them first.
4. **Delete one entry in one step**, by voice ("delete that") or by tap, with no menu hunt. The confirmation names what was removed and what remains (for example, "Deleted the 8:45 PM clip and its transcript").
5. **Offer delete-all and auto-delete next to the history,** and say that turning off future saving does not remove what is already stored.
6. **Keep nothing from a dismissed or timed-out activation.** Store at most the fact that it happened.
7. **Make the history reachable by the people recorded.** Guests and children can ask the device "what did you keep?" and the answer comes from the same record, not a hidden one.
8. **Never claim deletion that did not happen.** If a copy remains (a backup, a training set), say so and when it will go.

**Reference design: what the household sees**
| Moment | What the assistant shows or says |
|---|---|
| Setup and monthly | "I keep [audio and transcripts / transcripts only / nothing] for [N days]. Review or change this: [Review] [Change]" |
| Open the history | A list: time, room, words heard, action, kept or not; mistakes flagged first |
| "What did you keep today?" | Counts, then the entries, then the delete options |
| "Delete that" | Removes the latest entry; says what was removed |
| Delete all | One confirmation; then states what, if anything, remains and until when |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Someone asks "what did you keep?": start with the count and the entries, then the options. |
| Admit uncertainty and show how to check | The assistant cannot tell whether a clip was a mistake: say so, point to the history entry, and keep the delete control visible. |
| Offer choices: 2-4 options plus "Something else", free text open | A flagged mistake or the monthly summary: "Delete the mistakes", "Review them", "Keep them", "Something else". Do not offer them on a plain, requested timer or song. |
| Hand off to a person | Someone says a recording of a child or a private moment was kept and wants it gone beyond what the history shows: route to support or the account owner, with the entry. |

**Don't over-correct.** A daily recap, a prompt after every request, or a confirmation before each command will teach people to dismiss the notices and may push them to turn the device off. Summarize on a schedule, interrupt only for likely mistakes, and keep a counter-metric on complaints and on the rate of switching the device off.

**Hand-off rule.** When a person says something was kept that should not be, show the entry, delete it on their request, and offer a route to support. Questions about law, or requests about a child's data, go to the account owner and counsel, not to the assistant.

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
Results: **Not yet run.** These are designed scenarios.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Run setup on a new device | The assistant says what is kept and for how long before first use | 1 |
| 2 | Make five requests and one background wake-up, then open the history | All six appear with time, words, action and kept status; the mistake is flagged | 2, 3 |
| 3 | Say "delete that" after the mistake | One step; the confirmation names the clip and transcript removed | 4 |
| 4 | Ask "what did you keep?" as a guest | The answer comes from the same record and starts with counts | 7, Moves |
| 5 | Dismiss an activation and let it time out | No audio or transcript is kept | 6 |
| 6 | Turn off future saving, then check old entries | The assistant says earlier entries remain and offers to delete them | 5 |
| 7 | Delete all while a backup copy exists | The assistant says what remains and until when | 8 |
| 8 | A plain timer request | Done with no extra prompt (no over-correction) | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Households that review or delete at least one entry in 90 days** (primary) | 20% (starting point, unsourced) | Count households with a history-open or delete event in 90 days over active households | Below 5%, or a drop of half against the prior quarter |
| Kept recordings that appear in the history | 100% | Compare stored recording IDs to history entries | Below 100% |
| Complaints about unexpected recording | Track; set from baseline | Support tickets and app reviews tagged "recorded without knowing" | Rising two weeks in a row |
| Deletes that fully remove audio and transcript | 100% | Check storage 24 hours after each delete event | Any miss |
| Audio kept from dismissed or timed-out activations | 0 | Retention check on activations with no request | Any |
| Switch-off or unplug rate after a notice (counter-metric) | Track; set from baseline | Devices muted or disconnected within 7 days of a notice | Rising |

### Detection signals (proposed, not yet calibrated)
Signals in an app or history event log. Proposed until checked against human-labeled cases. Audio signals (wake-word score, clip length, speaker not recognized) are PLANNED for voice.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Delete within minutes of an activation | Delete event after an activation entry | A routine delete of an ordinary request |
| Delete-all with no history view first | Delete-all event with no preceding history-open event | A scheduled clean-up the owner always does |
| Support ticket or review says "recorded" or "listening" | Tag on text of ticket or review | A question about how the feature works |
| History entry with no words heard | Transcript field empty or "no speech" | A one-word command such as "stop" |
| Recording in storage with no history entry | Join of storage and history tables | A record still syncing |

**Starter rule:** every recording or transcript the assistant keeps appears in a history the household can open, and each entry can be deleted in one step.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: always-listening-surprises
runs: conversation
reads: [history.entries, history.kept_flag, user.delete_event, user.history_open_event, activation.has_request]
trigger: setup, the scheduled summary, a "what did you keep" question, or a delete request
moves: [lead_with_answer, admit_uncertainty, offer_choices, hand_off]
choices: ["Delete the mistakes", "Review them", "Keep them", "Something else"]
on_miss: ask
metric: households that review or delete at least one entry in 90 days
counter_metric: switch-off rate after a notice
status: proposed
```

## 8. Related patterns
- [Wake-word false activation](../../voice/failures/wake-word-false-activation.md) (library row VO-21): the closest pattern. It covers whether the device should have woken at all. This page starts after that: what was kept, whether the household can see it, and whether they can delete it.
- [AI disclosure failures](../../../../speech-and-audio/goals/conversation-flow/failures/ai-disclosure-failures.md) and [no data retention control](../../../../../cross-cutting/governance/goals/governance/failures/no-data-retention-control.md) (library row GV-12): the notice that a conversation is recorded, and the retention policy in general. This page is the household-facing record and delete flow in a home or car assistant.
- [Ambient assistants act on overheard conversation](../../proactive-and-ambient/failures/ambient-assistants-act-on-overheard-conversation.md): the assistant acts (sends, orders) on talk not meant for it. Here nothing is sent; the surprise is what is kept.
- [No user-facing record of what the bot said](../../privacy-and-governance/failures/no-user-facing-record-of-what-the-bot-said.md): the same idea for chat transcripts.
- [Privacy rights requests not recognised](../../privacy-and-governance/failures/privacy-rights-requests-not-recognised.md): when "delete my data" is typed as a request and ignored.
- [Smart-home commands go to the wrong device or room](smart-home-commands-go-to-the-wrong-device-or.md): a sibling in this family about command targets, not records.

## 9. Common questions
### Does my smart speaker record everything I say?
I found no source in what I opened that says so. Google's help page says audio may be saved when a device wrongly detects an activation ([section 4](#4-why-it-matters)), so mistakes are kept in some cases. Check your own product's history.

### How do I see and delete what my smart speaker recorded?
In Google's account help (the one I opened), open Web and App Activity, play items with the audio icon, and delete one item or all of it ([section 4](#4-why-it-matters)). Other products differ; look in the assistant's app under privacy or history.

### If I turn off saving, are old recordings deleted?
Not on Google's help page: turning the setting off stops new saves, and earlier audio must be deleted separately. A product should say this plainly ([rule 5](#5-the-fix)).

### Do voice assistants keep children's recordings?
The FTC alleged in 2023 that Amazon did, indefinitely by default ([section 4](#4-why-it-matters)); those are allegations in a proposed settlement. Rules for children's data are a question for counsel.

### Will a better model stop this?
No. Retention and the history screen are product decisions (our judgment, not tested).

---
## Technical section

### T1. Solution architecture
```
activation -> invitation gate -> (invited) request handled -> history write {time, room, words, action, kept?}
                           \-> (not invited) -> discard audio; history write {time, "no request", kept: none}
history store -> app and voice query ("what did you keep?") -> delete(entry) -> storage purge + history tombstone
scheduler -> monthly summary from history counts
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No stored audio without a history entry | Storage layer | Join of storage to history (metric 2) |
| Delete purges audio and transcript | Delete service | Test 3; storage check at 24 hours |
| Uninvited activations keep nothing | Activation logger | Test 5; retention check |

### T3. Evals
- **Dataset:** 100 scripted household days with 5 to 20 requests each, plus 20 mistaken activations and 10 delete requests (single, delete-all, by voice).
- **Judge rubric:** every kept item is in the history; mistakes are flagged; confirmations name what was removed; no false deletion claims.
- **Metrics and starting thresholds:** history coverage 100%; false deletion claims 0. Starting points to tune.
- **Release gate:** block a deploy if any new storage path writes audio with no history entry.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Kept recordings missing from history | Any | Any in a child profile | Stop the write path; reconcile and notify the owner |
| Failed delete (audio remains) | Any | Over 1% of deletes | Roll back the delete service; purge manually |

### T5. Trade-offs
- A readable history stores words in plain form, which is itself sensitive data; protect it and let the owner shorten retention.
- Monthly notices can be ignored; schedule and wording need testing on real households.

---
### Deep dive (optional)
- **Modality notes (PLANNED):** false wake-up rates, clip-length logs and spoken "delete that" accuracy are voice signals; none is written or measured here. The history, notice and delete flow apply today.
- **Open question.** I found no open study of how many households use review and delete controls after a redesign. The only user-behavior evidence here is one 116-person survey.
- **References.** [Malkin et al., PoPETs 2019](https://par.nsf.gov/biblio/10109137-privacy-attitudes-smart-speaker-users) (abstract opened); [FTC press release, May 31, 2023](https://www.ftc.gov/news-events/news/press-releases/2023/05/ftc-doj-charge-amazon-violating-childrens-privacy-law-keeping-kids-alexa-voice-recordings-forever) (opened); [Google Account Help](https://support.google.com/accounts/answer/6030020) (opened). Not opened: the PoPETs PDF body, Amazon's help page (503), the FTC complaint PDF, the YouGov survey (search summary only).
