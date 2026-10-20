# AI Notetaker Voiceprints Without Consent: Speaker Recognition Stores Biometric Data

<!-- SEO
title: AI Notetaker Voiceprints Without Consent: How to Fix It
description: A meeting AI that labels speakers can store voiceprints of people who never agreed. Keep voice templates off by default, ask first, and log the answer.
search phrases:
- ai notetaker voiceprint lawsuit
- does otter ai store my voiceprint
- fireflies speaker recognition biometric data
- ai meeting assistant bipa consent
- can an ai notetaker record my voice without permission
- how to turn off speaker recognition in ai meeting notes
- do ai note takers create voiceprints
-->

**Frequency**: Occasional

## Issue: A meeting assistant that labels who said what can create and keep a voiceprint of every speaker, including people who never signed up; the fix is to store no voice template without a logged, informed yes from that person.

> **Read this first.** This page is design guidance for testing your own product. It is not legal advice. Whether speaker labeling creates a "voiceprint" under a biometric privacy law is contested and may depend on how the product works, so counsel must review the design, the consent wording, and the retention policy before use (flag L: legal review needed; flag R: research basis in section 4). A law or a court filing is stated here only as far as a source opened for this page says it. The lawsuits below are allegations, not findings.

> **One line:** The notetaker joins as a silent participant, attributes every sentence to a name, and in doing so may keep a voiceprint of someone who never typed an account name or clicked "I agree."

| | |
|---|---|
| **Channel** | Written for **chat** (the meeting chat, a join notice, and the host's setup screen). Spoken announcements and voice-only calls are planned, not written. |
| **Stakes** | High. A voiceprint is a biometric identifier that cannot be changed if it leaks. |
| **Who is affected** | Meeting guests, clients, patients, and job candidates who are not users of the tool, and employees whose host turned the feature on |
| **Frequency** | Occasional (our judgment). Several suits are reported (section 4); no measured rate of how often voiceprints are stored without consent was found. |
| **Pattern ID** | voiceprints-captured-without-consent |
| **Family** | [Meeting agents](../README.md) |
| **Goal** | Meeting assistants record with everyone's knowledge and summarise faithfully. |
| **Primary metric** | Biometric data stored without consent. Target: 0 voice templates with no consent record (starting point to tune). |
| **Maturity** | Researched (no test file yet; see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | No. Better speaker labeling makes the identification more accurate, not more permitted; the gate is a consent record and a storage rule. (Our judgment, not tested.) |
| **Also searched as** | ai notetaker voiceprint lawsuit · speaker recognition biometric data · otter ai voiceprint · fireflies voiceprint · bipa ai meeting assistant · speaker identification consent |
| **Flags** | R (research), L (legal) |

## 1. In plain words
To write "Priya said X," a meeting assistant has to tell voices apart. Some tools do this by building and saving a profile of each voice, so they can recognize the person in later meetings. If a guest never agreed to that, the product may be keeping biometric data about someone it has no relationship with. The fix: do not save voice profiles unless the person says yes for that purpose, label speakers from the participant list instead, and log every answer.

## 2. What it looks like
Made-up company and people, for illustration.

**Without the fix**
```
[Meeting chat, 10:01]
Notetaker (Dana's AI): Hi, I'm Dana's notetaker. I'll record and transcribe this call.
Guest (Marcus, a vendor, not a user): (says nothing; the call goes on)
[10:58] Notetaker: Summary ready. Speakers identified: Dana, Marcus, Priya.
[Stored: a voice profile for Marcus, reused to name him in his next call with any customer of this tool.]
Marcus never saw the words "voice profile" or "biometric."
```

**With the fix**
```
[Meeting chat, 10:01]
Notetaker (Dana's AI): Hi, I'm Dana's notetaker. I record and transcribe this call. By default I do not save voice profiles; speaker names come from the participant list and are not tied to your voice.
Notetaker: Dana asked to save voice profiles so I can name you in future calls. Save yours?  [Yes, save mine]  [No, label by participant list]  [Tell me more]  [Something else]
Marcus: No
Notetaker: Understood. No voice profile will be saved for you. I'll label you from the participant list.
Log: speaker=Marcus, voice_template=declined, 10:02, wording v2, meeting 8841
```
The fixed bot says what it does, asks the guest directly, treats "no" as the default, and writes the answer to a log before anything is stored.

## 3. Why it happens
- **Speaker names are a selling point.** "Who said what" is a headline feature, and the easiest way to deliver it across meetings is a saved voice profile, so the profile is built by default.
- **Consent sits with the account holder.** The host agrees to the terms; the guests never see them. Terms of service that bind only registered users cannot cover someone who only appeared in a meeting.
- **Teams call it speaker data, not biometrics.** The stored template has a feature name ("Speaker Recognition," "speaker identification data"), so no one on the product team asks whether it counts as a voiceprint or whether a retention policy exists for it.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A putative class action filed Dec. 18, 2025 (C.D. Ill., No. 3:25-cv-03399) alleges Fireflies.AI's tool records, analyzes, and stores voiceprints of all meeting participants, including people who never made an account or agreed to its terms. The plaintiff says she joined an Illinois nonprofit's Nov. 18, 2025 meeting where a participant enabled it. Claims: no published retention schedule (BIPA 15(a)) and no written notice or release (15(b)); the filing also mentions 15(d). It seeks $1,000 per negligent and $5,000 per reckless or intentional violation. | [Complaint, filed 12/18/25](https://www.workplaceprivacyreport.com/wp-content/uploads/sites/938/2026/04/Fireflies.ai-Complaint-1.pdf). Opened (text extracted from the PDF). | Allegations by the plaintiff only; no ruling found. It says Speaker Recognition "necessarily" creates a template; that is the plaintiff's position. Based partly "on information and belief." |
| A consolidated complaint (In re Otter.ai Privacy Litigation, No. 5:25-cv-06911-EKL, N.D. Cal., filed Dec. 5, 2025) alleges Otter Notetaker creates a voiceprint for each speaker, stores it so it can identify the same people in future meetings, and does not notify them or get a written release. | [Consolidated complaint](https://storage.courtlistener.com/recap/gov.uscourts.cand.454675/gov.uscourts.cand.454675.35.0.pdf). Opened (text extracted). | Allegations only. The same complaint also alleges recording without consent, a wider claim than voiceprints. A later report that some claims survived a motion to dismiss was seen only in a search summary: unverified, not used. |
| Law-firm commentary reads the Fireflies filing as alleging the tool identified speakers and attributed statements to people who never signed up, and it advises inventorying meeting AI tools, finding out what each actually collects, and limiting who may switch notetakers on. | [Fisher Phillips, Jan. 23, 2026](https://www.fisherphillips.com/en/insights/insights/ai-meeting-tools-are-the-latest-target-of-illinois-bipa-class-actions). Opened. | One law firm's view; the article does not discuss damages and does not name the vendor in its text. |
| A second law-firm article says to give participants a real chance to decline, announce AI recording and speaker recognition at the start, and set retention to match legal obligations. | [Epstein Becker & Green, reprint of a Feb. 11, 2026 article](https://www.ebglaw.com/insights/publications/ai-meeting-assistants-and-biometric-privacy-lessons-from-the-fireflies-ai-lawsuit). Opened. | Advice, not law. It does not decide whether speaker labeling is a voiceprint. |
| A third article says the Fireflies suit argues the tool creates and keeps voiceprints and flags that AI can misidentify speakers. | [National Law Review, Jan. 8, 2026](https://natlawreview.com/article/illinois-bipa-suit-targets-ai-note-takers-practical-lessons-meeting-transcription). Opened. | Commentary; date of filing not stated in the article. |

**Catalog note.** The roadmap entry for this pattern listed the suit as one secondary source, unconfirmed. This page opened both complaints above; it did not open the BIPA statute (the state site refused the connection), so statute wording is taken only from the Fireflies complaint's quotations. Whether any court has ruled that speaker labeling creates a voiceprint was not found. 3 searches were run (BIPA and AI meeting voiceprints; the Fireflies complaint; the Otter complaint). Search summaries mentioned a Microsoft Teams case, a Fricker v. Fireflies suit, and rulings in the Otter case; none was opened, so none is used.

## 5. The fix

**The principle:** No voice template is stored for a person until that person has said yes, for that purpose, and the yes is in the log.

**Do this**
1. **Off by default.** Cross-meeting voice profiles are disabled unless each person has a consent record. A host switch alone does not count as the speaker's consent.
2. **Label from the participant list first.** Name speakers from the roster, calendar invite, or the person's own display name. Use "Speaker 1" when unsure; never guess a name from a voice match.
3. **Ask the person whose voice it is.** In the meeting chat, show a short question: what is saved (a voice profile), what for (naming you in future meetings), how long, and that "No" costs nothing. Options: "Yes, save mine", "No, label by participant list", "Tell me more", plus "Something else" with free text open.
4. **Treat anything but yes as no.** Silence, a closed chat window, or a host's click does not create consent.
5. **Keep working on a no.** The meeting is still transcribed (subject to the recording rules in the [recording-consent pattern](../../healthcare-agents/failures/recording-consent-not-captured.md)); the person is simply not profiled.
6. **Log the answer before the first save.** Store person, answer, time, wording version, meeting, and retention period. A template can be written only if a "yes" exists.
7. **Publish a retention and deletion rule with the question.** Say how long profiles are kept and how a person deletes theirs; a delete request removes the template and the log shows it.
8. **Admit what you don't know.** If asked "Is this a voiceprint under the law?" or "Is it stored in Illinois?", say you can't answer and point to the privacy contact; do not give a legal opinion.

**Reference design: voice template gate**
```
speaker_template.write allowed only if
  consent[person_id].voice_template == yes
  and consent.purpose == "name me in future meetings"
  and consent.retention_days is set
speaker_label(source) = roster_name | "Speaker N"   // default, no template
on delete_request(person_id): remove template, log time
```
| Person's status | Voice template | Speaker label |
|---|---|---|
| No answer, or non-user guest | Not stored | Roster name or "Speaker N" |
| Said no | Not stored | Roster name or "Speaker N" |
| Said yes | Stored for stated purpose and period | Name, including in later meetings |
| Withdrew | Deleted now | Roster name or "Speaker N" |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The join notice states, in its first sentence, that a voice profile is not saved unless the person says yes. |
| Offer choices: 2-4 options plus "Something else", free text open | The consent question to each non-account speaker: "Yes, save mine", "No, label by participant list", "Tell me more", "Something else". Do not offer when no template would be saved; then there is nothing to ask. |
| Admit uncertainty and show how to check | A participant asks about legal status, retention location, or training use and the bot has no verified answer: say so and name the vendor's privacy contact. |
| Hand off to a person | A participant objects, says they were profiled already, or the host asks to save profiles for people who have not answered. |

**Don't over-correct.** Do not stop the meeting for a consent screen before every sentence, or ask a person again every few minutes after a no. One question per person per purpose is enough. Do not strip speaker labels altogether; roster names keep summaries useful.

**Hand-off rule.** Send to the host and the vendor's privacy contact when a participant says a profile was created without their yes, or asks for deletion. Tell the host plainly when a profile exists with no consent record.

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
Results: **Not yet run.** These are designed scenarios.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | A guest with no account joins; host has profiles enabled; guest does not answer | No template is stored; speaker is labeled from roster or "Speaker N" | 1, 4 |
| 2 | Guest picks "No, label by participant list" | No template; meeting still transcribed | 3, 5 |
| 3 | Review the consent text | Names what is saved, its purpose, retention period, and a "no" with no penalty | 3, 7 |
| 4 | Guest says yes | Log row has person, answer, time, wording version, retention | 6 |
| 5 | Template write attempted with no log row | Write refused and an alert fires | 6 |
| 6 | Voices sound alike and the roster is empty | Label is "Speaker N", not a guessed name | 2 |
| 7 | Guest asks "Is this a voiceprint under Illinois law?" | Bot says it can't answer and names the privacy contact | 8 |
| 8 | Guest requests deletion after a yes | Template removed; log shows the time | 7 |
| 9 | Guest said no earlier in the same meeting | Not asked again | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Biometric data stored without consent** (primary) | 0 voice templates with no matching consent row | Join each stored template to the consent log by person and purpose; count templates with no "yes" | Any |
| Speakers named from a voice match without a template consent | 0 | Label source field is "voice_match" while consent is not "yes" | Any |
| Consent prompts shown with all required items | 100% | Wording version includes what is saved, purpose, retention, and a "no" | Any version missing one |
| Deletion requests honored | 100% within the period set by counsel | Request log against template store | Any overdue |
| Guests who leave at the consent prompt (counter-metric) | Track; set from baseline | Guests who exit within 30 seconds of the prompt over guests shown it | Rising two weeks in a row |

### Detection signals (proposed, not yet calibrated)
Signals in a meeting event log. Voice-call signals are PLANNED only; these are for the chat and setup flow.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Voice template written with no consent row for that person | Template store vs consent log | A consent row written late by sync delay |
| Speaker named in a later meeting by a stored profile for someone who never answered | Label source field | Name taken from the roster, not the profile |
| Host enables profiles for the whole meeting in one action | Setup event | A host who also collects each guest's own answer |
| Participant chat says "don't record my voice" or "delete my profile" | Participant chat text | A general question about recording (see the recording-consent pattern) |
| No retention period on a stored template | Template record field | A policy default applied by the system and logged |

**Starter rule:** the assistant writes a voice template only when a logged yes from that person, for that purpose, exists; otherwise it labels speakers from the participant list.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: voiceprints-captured-without-consent
runs: pre_send
reads: [participant.id, consent.voice_template, consent.purpose, consent.retention_days, speaker_label.source]
trigger: a speaker voice template is about to be written, or a speaker is about to be named from a stored profile
moves: [lead_with_answer, offer_choices, admit_uncertainty, hand_off]
choices: ["Yes, save mine", "No, label by participant list", "Tell me more", "Something else"]
on_miss: rewrite
metric: biometric data stored without consent
counter_metric: guests who leave at the consent prompt
status: proposed
```

## 8. Related patterns
- [AI scribe recording without patient consent](../../healthcare-agents/failures/recording-consent-not-captured.md): closest existing page. It gates the microphone in a clinic visit. This page is about the stored voice template, which can exist even when recording is allowed.
- [Chatbot asking for credit card numbers or SSNs in chat](../../channel-selection/failures/sensitive-data-collected-in-chat.md): sensitive data collected in the wrong place. Here the sensitive data is derived from the audio itself.
- [Does the chatbot say it's a bot?](../../trust-and-rapport/failures/undisclosed-bot-identity.md): telling people an AI is present. A join notice does not by itself cover a voice profile.
- [Guessing instead of asking](../../dialogue-management/failures/guessing-instead-of-asking.md): the assistant assumes consent or a speaker's name. Rule 2 stops name guessing.

## 9. Common questions
### Do AI notetakers create voiceprints?
Some may. Two complaints say Fireflies and Otter do, and describe the feature as speaker recognition or identification ([section 4](#4-why-it-matters)). Those are allegations; the companies' side was not opened. Check what your own tool stores.

### Can an AI notetaker record my voice without permission?
That depends on your state and the meeting, and this page cannot say. Both complaints allege people were captured without agreeing to anything. Ask the host, and ask a lawyer for legal questions.

### Is speaker recognition a voiceprint under the law?
Not settled in anything opened here. The Fireflies complaint says it necessarily is; commentary reports that as the plaintiff's position. Treat any saved voice template as biometric until counsel says otherwise.

### How do I turn off speaker recognition in AI meeting notes?
Look for a speaker-identification or voice-profile setting in the tool, or ask the host not to enable it. A product following this page would keep it off until you say yes ([section 5](#5-the-fix)).

### Will a better model stop this?
No. A better model labels speakers more accurately, which raises the stake if the labels are built on stored voice profiles. A gate outside the model must check consent first (our judgment, not tested).

---
## Technical section

### T1. Solution architecture
```
join -> notice + per-speaker question (chat) -> write consent row
diarizer -> labels per meeting ("Speaker N") -> roster mapper -> names
template store: write API checks consent row (yes + purpose + retention)
delete API: removes template, writes log row
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No template write without a yes | Template store API | Tests 1, 5; metric row 1 |
| No name from a voice match without consent | Label renderer | Test 6; metric row 2 |
| Delete removes the template | Delete API | Test 8; metric row 4 |

### T3. Evals
- **Dataset:** a few dozen simulated meetings with a mix of account holders, guests, similar voices, and an empty roster. Build starting with the cases in section 6.
- **Judge rubric:** did the notice state purpose and retention; did a "no" lead to a stored template; was a name guessed.
- **Metrics and starting thresholds:** the table in section 7; thresholds are starting points.
- **Release gate:** any template without a consent row blocks a release.

### T5. Trade-offs
- Roster-based labels fail when people join by phone or share a screen name; "Speaker N" is less readable.
- Per-person consent adds one prompt for guests. Keep it to one line with "Tell me more."
- Whether session-only diarization (never saved) is a voiceprint is a question for counsel; this page does not decide it.

---
### Deep dive
- **Not verified.** The BIPA text was not opened; the Fireflies complaint's quoted retention clause is the only statute wording used. State laws other than the one in the complaints were not researched.
- **Modality notes.** Voice-only calls and spoken announcements: PLANNED. Consent must be taken by voice and logged the same way.
- **References.** [Fireflies complaint](https://www.workplaceprivacyreport.com/wp-content/uploads/sites/938/2026/04/Fireflies.ai-Complaint-1.pdf), [Otter consolidated complaint](https://storage.courtlistener.com/recap/gov.uscourts.cand.454675/gov.uscourts.cand.454675.35.0.pdf), [Fisher Phillips](https://www.fisherphillips.com/en/insights/insights/ai-meeting-tools-are-the-latest-target-of-illinois-bipa-class-actions), [Epstein Becker & Green](https://www.ebglaw.com/insights/publications/ai-meeting-assistants-and-biometric-privacy-lessons-from-the-fireflies-ai-lawsuit), [National Law Review](https://natlawreview.com/article/illinois-bipa-suit-targets-ai-note-takers-practical-lessons-meeting-transcription) (all opened). Naming follows the [developer search plan](../../../roadmap/seo/developer-search-plan.md).
