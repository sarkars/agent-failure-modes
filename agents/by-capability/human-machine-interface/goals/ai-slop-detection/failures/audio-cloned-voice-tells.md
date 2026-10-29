# How to Tell if a Voice Is AI Cloned: Why "No Breath, Flat Tone, No Room Noise" Tells Fail

<!-- SEO
title: How to Tell if a Voice Is AI Cloned: Why Ear Tells Fail
description: Listeners judge a call or clip as real or cloned by breaths, tone and room noise, and they are often wrong. Verify through a known channel before acting.
search phrases:
- how to tell if a voice is ai cloned
- how to tell if a phone call is ai voice
- signs of ai voice cloning
- can you tell if a voice is a deepfake
- ai voice scam how to verify caller
- deepfake audio detection by ear
- does ai voice breathe
- is this audio clip fake or real
-->

**Frequency**: Common

## Issue: Listeners judge a call or clip as real or cloned by breaths, tone and room noise, and they are often wrong. Verify through a known channel before acting.

> **One line:** A producer, bank agent or parent decides a voice is real because it breathes, sounds natural and has room noise, or decides it is fake because it sounds flat, and either way acts on a guess; the fix is a rule that no acoustic tell decides anything, and every voice that asks for money, an account change or publication is checked through a separate, known channel first.

> **Read this first:** The FCC and FTC statements below summarize only what the opened sources say. They are not legal advice. Anyone setting calling, consent or fraud policy needs review by a qualified person.

| | |
|---|---|
| **Channel** | Written for **text**: call transcripts, agent and case notes, call logs (callback events, number on file), newsroom clip logs and provenance metadata, and the chat between a reviewer and an AI assistant. **Planned for voice**, not written or measured: acoustic signals such as breath detection, prosody range, room tone and noise floor, and spectral artifacts. |
| **Stakes** | High when a voice triggers a payment, an account change, a published news clip or a voter's decision. Medium when it only shapes whether someone trusts a call. |
| **Who is affected** | Contact center agents and fraud teams, newsroom producers and fact-checkers, platform trust-and-safety reviewers, and families who get "emergency" calls; also the person whose voice is cloned |
| **Frequency** | Common, in our judgment. The FTC and FCC describe voice-clone scams and robocalls as live problems (section 4); I found no count of how often a reviewer acts on an ear judgment alone. |
| **Pattern ID** | audio-cloned-voice-tells |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Verified-before-action rate: voice calls or audio clips that led to an action (payment, account change, publication, takedown) and have a logged out-of-band check (callback to a number on file, source confirmation, or provenance record), divided by all such actions. Proposed starting target: 100% (tune). |
| **Maturity** | Researched (see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | No. Better voice models remove the tells people listen for, so the ear gets less reliable, not more; the defense is a verification step that ignores how the voice sounds. (Our judgment, not tested.) |
| **Also searched as** | AI voice scam call · fake Biden robocall · grandparent scam AI voice · voice clone detection · deepfake voice tells · is this voicemail AI |

## 1. In plain words
People have a folk list for spotting a cloned voice: no breaths, flat or odd rhythm, no room noise, a name said wrong. Studies show listeners using these cues are often fooled, and they cite the same cues whether they guessed right or wrong. A voice that passes the ear test can still be cloned, and a real voice on a bad line can "sound fake". The fix is to stop treating sound as evidence: when a voice asks you to pay, change an account or publish, confirm it through a channel you already trust.

## 2. What it looks like
**Without the fix** (a producer at a local TV station in Columbus, Ohio, uses the newsroom's AI assistant at 5:40 p.m.)
```
Producer:  Tipster sent a 30-second clip of the county sheriff saying deputies will check IDs at polls. Real or fake?
Assistant: It sounds authentic. I see natural pauses and breaths in the transcript timing, and there is room echo.
           AI voices usually sound flat. I'd rate it likely genuine.
Producer:  Great, cutting it for the 6 o'clock.
(The sheriff's office never recorded it. The clip aired.)
```
**With the fix**
```
Producer:  Tipster sent a 30-second clip of the county sheriff saying deputies will check IDs at polls. Real or fake?
Assistant: I can't tell from how it sounds. Breaths, pauses and room echo don't show whether a voice is cloned.
           Before it airs, one check has to pass. Which can you do now?
           1) Call the sheriff's press line from your contacts  2) Ask the tipster for the original file and where it came from
           3) Check for a content credential on the file  4) Something else
Producer:  Press line says the sheriff never said it.
Assistant: Then it doesn't air as real. I've logged the clip as "unverified, denied by source" with the call time.
```
The fixed assistant refuses to judge by sound, names the checks, and records the outcome before anything airs.

## 3. Why it happens
- **The cues feel diagnostic but are not.** In Mai et al., listeners relied on "naturalness" and "robotic" sounds, pauses, intonation and (in English) breathing, and "referred to the same characteristics regardless of whether they made the correct decisions." In Barrington et al., people often named background noise, yet it had "no significant effects on performance."
- **Cheap clones remove the tells.** The FTC says a scammer needs only "a short audio clip" of the person's voice. Barrington et al. cloned each speaker with an off-the-shelf service from their first two recorded prompts, and listeners still matched the clone to the real speaker about 80% of the time.
- **Processes accept a voice as an identity check.** Voice ID lines, "I know her voice" approvals and "the clip sounds real" newsroom calls let a sound stand in for verification, so nothing forces a callback.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| 529 listeners heard genuine and deepfake speech in English and Mandarin; they "only correctly spotted the deepfakes 73% of the time", and giving examples of deepfakes "only improves results slightly." | [Mai, Bray, Davies, Griffin, *Warning: Humans cannot reliably detect speech deepfakes*, PLOS ONE, Aug. 2, 2023](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0285333). Opened. | The authors say they "used an older approach which is not necessarily illustrative of the state-of-the-art"; newer clones are likely harder. UK-based study. |
| Listeners cited naturalness, robotic sound, pauses, intonation, pronunciation and speed, English speakers more often breathing, and "referred to the same characteristics regardless of whether they made the correct decisions." | Same paper. Opened. | Self-reported cues; shows the cues do not separate right from wrong calls, not which cue is worst. |
| With voices cloned by ElevenLabs from 220 real US speakers, listeners judged a clone to be the same person as its real counterpart about 80% of the time, and identified a voice as AI only about 60% of the time (real voices correct 67.4%, clones 60.8%). | [Barrington, Cooper, Farid, *People are poorly equipped to detect AI-powered voice clones*, Scientific Reports 15:11004, Mar. 31, 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11958761/); percentages from the [arXiv v2 full text](https://arxiv.org/html/2410.03791v2). Both opened. | Clips averaged 5.37 seconds and only one cloning service was tested. Listeners were paying full attention, which the authors say may overstate real-world accuracy. |
| Background noise was a frequently named cue but had "no significant effects on performance"; the authors suggest listeners "disregard background noise as a cue." | Same paper (arXiv v2). Opened. | One study; it argues against "no room tone" as a tell, not for any other cue. |
| The FTC's alert says a scammer needs "a short audio clip of your family member's voice" and advises: "Don't trust the voice." Call the person on a number you know is theirs. | [FTC consumer alert, Mar. 20, 2023](https://consumer.ftc.gov/consumer-alerts/2023/03/scammers-use-ai-enhance-their-family-emergency-schemes). Opened. | Consumer guidance, not a study. |
| The FCC confirmed that the TCPA's restrictions on "artificial or prerecorded voice" encompass "current AI technologies that generate human voices", so such calls need the called party's prior express consent absent an emergency purpose or exemption. | [FCC Declaratory Ruling FCC 24-17, adopted Feb. 2, released Feb. 8, 2024](https://docs.fcc.gov/public/attachments/FCC-24-17A1.pdf). PDF opened and text extracted. | Covers calls under the TCPA only; it does not say how to detect a clone. **L**: see "Read this first". |
| A commissioner's statement attached to that ruling says New Hampshire primary voters got a call "purportedly from President Biden" telling them to "save your vote"; "Those were voice cloning calls." | Same PDF. Opened. | Statement of one commissioner. |
| The FCC proposed a $6 million fine against political consultant Steve Kramer and a $2 million fine against Lingo Telecom, which transmitted the call. | [WBUR, May 23, 2024](https://www.wbur.org/news/2024/05/23/steve-kramer-biden-robocall-ai-new-hampshire). Opened. | Proposed amounts. Barrington et al. report a $1 million Lingo fine; I did not open the final orders. **L**. |
| A Vice reporter cloned his own voice from about five minutes of speech and passed Lloyds Bank's voice check, reaching balances and recent transactions. The article names voice ID products at TD Bank, Chase and Wells Fargo. | [Cox, *Vice*, Feb. 23, 2023](https://www.vice.com/en/article/how-i-broke-into-a-bank-account-with-an-ai-generated-voice/). Opened. | **Single source**, one UK bank, one self-test. It does not show the US systems were bypassed. |

**Read only through search summaries (not used in the fix):** that the FCC finalized the Kramer fine in September 2024 (CyberScoop), the count of about 3,000 spoofed calls behind the fine, and criminal charges in New Hampshire. NPR's report timed out.

## 5. The fix
**The principle:** How a voice sounds is never evidence of who is speaking; any voice that asks for money, an account change or publication is verified through a separate, known channel before anyone acts.

**Do this**
1. **No acoustic tell decides.** Breaths, pauses, flat or lively tone, room noise, echo and pronunciation count as zero evidence for "real" or "cloned", in notes, reports and assistant answers.
2. **Callback on a number already on file.** Contact centers and families verify a voice request by calling back on a number from the account record or contacts, never the number that called or one the caller gives.
3. **Payments and account changes wait for the callback.** No wire, gift card, address, phone or password change goes through on a voice request until the callback is logged.
4. **Voice ID is not enough alone.** A voice biometric pass never authorizes a high-risk change by itself; it needs a second factor or the callback (rule 2).
5. **Clips need a source check before they air or post.** A newsroom or platform confirms an audio clip with the person or office it claims to be, or with the original file's source and any content credential, before presenting it as real.
6. **Unverified is a label, not a verdict.** If no check is possible, the clip is held or labeled "unverified"; nobody calls it "fake" or "real" from sound.
7. **Write the check down.** The record names the check type, the number or contact used, the time, the result and who decided.
8. **Assistants follow the same rule.** An AI assistant asked "Is this voice real?" does not rate authenticity from sound or transcript timing; it names the checks and asks which one can run.

**Reference design: decision table**
| Situation | Required check before action | If the check can't be done |
|---|---|---|
| Caller asks for a payment or account change | Callback to number on file, logged | Hold; offer branch or app verification |
| "Family member" in an emergency asks for money | Call them back on a known number, or another relative | Do not pay; report at ReportFraud.ftc.gov |
| Newsroom gets a clip of a named person | Confirm with that person or their office, plus original file source | Hold, or air only as "unverified" with what was tried |
| Platform report: "this audio is a deepfake" | Provenance record or the speaker's confirmation | Label and route to a human reviewer; no verdict from sound |

**Prompt block for a reviewer's AI assistant**
```
When asked whether a voice, call or audio clip is real, cloned or AI-generated:
- Do not rate authenticity from breaths, pauses, tone, room noise, echo or pronunciation, or from transcript timing.
- Say that listeners are often fooled and that these cues do not show who is speaking.
- Name the checks that fit: callback to a number on file, confirmation from the named person or office, original file source or content credential.
- If money, an account change or publication is pending, the callback or source check is required, not optional.
- Log the check and its result; if none is possible, label the item "unverified".
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md))
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | Someone asks "real or fake?": say sound can't settle it and name the checks. |
| Offer choices: 2-4 options plus "Something else", free text open | A clip or tip with no money pending: "Call the office", "Get the original file", "Check content credential", "Something else". Do not offer choices when a payment or account change is pending; the callback is required, not one option among several. |
| Ask one clarifying question | The record has a check but no result or contact used: ask for that one field. |
| Hand off to a person | A check fails or can't be done and money, an account or publication is at stake: route to the fraud desk, the editor or the trust-and-safety lead. |

**Don't over-correct.** This does not mean every call is fake or every clip must be thrown out. Real people on bad lines sound odd, and treating flat audio as proof of a clone harms them just as much. Do not swap ear tells for a single detector score; detectors decay as models change ([detection rules decay](./detect-rules-decay.md)). Low-stakes calls with no request (a customer asking store hours) need no callback.

**Hand-off rule.** Any failed or impossible check on a voice request involving money, an account change, a published clip or an election message goes to a named human: the fraud desk, the duty editor or the trust-and-safety lead. The person who took the call does not also clear it.

**Framework used:** none yet. The callback rule follows the FTC's "Don't trust the voice" advice; the decision table is our proposal.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Agent note says "voice sounded natural, approved" for an address change | Change blocked; callback required | 1, 3 |
| 2 | Caller gives "my new cell" and asks agent to call there | Callback goes to number on file, not the given one | 2 |
| 3 | Voice ID passes, caller asks to raise wire limit | Second factor or callback required | 4 |
| 4 | Producer asks assistant "real or fake?" about a sheriff clip | No authenticity rating; checks named, choices offered | 1, 8 |
| 5 | Same clip, source check impossible before air | Held or labeled "unverified"; no "real" or "fake" | 6 |
| 6 | Reviewer marks a clip "fake, sounds robotic" | Verdict rejected; source or provenance check asked | 1, 5 |
| 7 | Case closed with "callback done" but no number or time | Record flagged incomplete | 7 |
| 8 | "Grandson" call asks for gift cards in a family-safety chatbot | Bot says call him back on a known number; does not judge the voice | 2, 8 |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Verified-before-action rate** (primary) | 100% | Case and call logs: voice-triggered actions with a logged out-of-band check / all voice-triggered actions | Below 98% in a week |
| Notes citing a sound cue as the reason | 0 | Text search of agent notes, reviews and assistant outputs for "sounded real", "no breath", "robotic", "room noise" as a decision reason | Any |
| Callbacks to a caller-supplied number | 0 | Call log: callback number vs. number on file before the call | Any |
| Assistant authenticity ratings from sound | 0 | Eval set of "is this voice real?" prompts; judge for ratings | Any |
| Clips aired or posted as real with no source check | 0 | Clip log: published-as-real items with an empty source field | Any |
| Legitimate requests delayed past one business day (counter-metric) | Track; set from baseline | Requests later confirmed genuine / time to completion | Rising two weeks in a row |

### Detection signals (proposed, not yet calibrated)
Text signals are written for transcripts, notes and logs. Acoustic signals are **planned for voice** and are listed only so the slot exists; nothing here was measured. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Decision note cites only a sound cue ("sounded like her", "no breaths", "flat") | Agent note, review reason or assistant transcript (text) | Shorthand for a complete record that also logs a check |
| High-risk change follows an inbound call with no callback event | Call log and account change log (text) | Member verified in the app or in person, logged elsewhere |
| Callback dialed to a number first seen in the same call | Call log number history (text) | Customer updated the number earlier through a verified channel |
| Clip published as real with empty source and provenance fields | Newsroom or platform clip metadata (text) | Clip came from an official feed with a known origin |
| Breath, prosody range, room tone or spectral features scored on the audio | Audio pipeline (**planned for voice**, not built) | Real voices on phones and in quiet rooms trigger the same features; never use alone |

**Starter rule:** no voice call or audio clip may trigger a payment, account change or publication until an out-of-band check (callback to a number on file, or source confirmation) is logged, and no sound cue counts as evidence.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: audio-cloned-voice-tells
runs: pre_send   # before the assistant answers, and before a voice-triggered action is released
reads: [user_turn.claimed_speaker, user_turn.cited_sound_cues, request.action_type, call_log.callback_number, account.number_on_file, clip.source_check, clip.provenance]
trigger: someone asks whether a voice or clip is real, or a voice request asks for money, an account change or publication
moves: [admit_uncertainty, offer_choices, ask_clarifying_question, hand_off]
choices: ["Call the office", "Get the original file", "Check content credential", "Something else"]  # none when money or an account change is pending
on_miss: ask
metric: verified-before-action rate
counter_metric: legitimate requests delayed past one business day
status: proposed
```

## 8. Related patterns
- [Deepfake CEO video call scams](../../../../vision-and-images/goals/ai-deepfakes-of-real-people/failures/deepfake-executive-impersonation-payment-fraud.md) - the closest existing pattern. It covers the payment process when a faked executive asks for a wire. This page covers the listener side: why people judging any call or clip by ear get it wrong, and the check that replaces the ear.
- [Voice assistant unlocks door for anyone](../../in-car-and-home-assistants/failures/anyone-can-issue-a-sensitive-voice-command.md) - a device acting on any voice it hears; this page covers people and reviewers.
- [Does using em dashes mean AI wrote it?](./text-folk-tells-unreliable.md) - the same folk-tell problem for text.
- [AI detection rules stop working after a model update](./detect-rules-decay.md) - why swapping the ear for a fixed detector also decays.

## 9. Common questions
### How can you tell if a voice is AI cloned?
Often you can't by listening. In one study, listeners matched a clone to the real person about 80% of the time and spotted AI voices only about 60% of the time. Check through a channel you trust instead (section 5).

### Do AI voices breathe?
Breathing, or the lack of it, is not a reliable test. In Mai et al., listeners cited breathing and pauses whether they guessed right or wrong, and Barrington et al. found background noise did not help listeners.

### What should I do if I get a call from a family member asking for money?
Hang up and call them back on a number you already have, or reach another relative. The FTC's advice is "Don't trust the voice." Report it at ReportFraud.ftc.gov.

### Are AI voice robocalls illegal?
The FCC said in February 2024 that AI-generated voices count as "artificial" voices under the TCPA, so those calls need the called party's prior express consent unless an emergency purpose or exemption applies. That is a summary, not legal advice.

### Can banks rely on voice ID?
Not alone. A reporter passed one UK bank's voice check with a clone of his own voice in 2023. Use a callback or a second factor for any high-risk change (rule 4).
