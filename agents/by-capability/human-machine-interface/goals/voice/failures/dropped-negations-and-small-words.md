# Speech to Text Drops "Not": Dropped Negations and Small Words

<!-- SEO
title: Speech to Text Drops "Not": Fix Dropped Negations
description: Speech recognition can drop "not" or turn "can't" into "can" and flip the meaning. See what studies found and a design that reads back negations before acting.
search phrases:
- speech to text drops negation
- ASR negation errors
- speech recognition missed the word not
- voice assistant heard the opposite of what I said
- voice bot canceled when I said don't cancel
- can't transcribed as can
- word error rate misses negation
(Phrases come from wording seen in the sources and search results during research, not from volume data.)
-->

**Frequency**: Occasional

## Issue: Speech recognition can drop "not", turn "can't" into "can", or insert a "no", and the voice agent acts on the opposite of what the caller said; the fix is to read back the action, including the negation, before doing anything.

> **One line:** The caller says "don't cancel my refill", the transcript says "cancel my refill", and the agent cancels it.

> **Read this first (flag E: expert review needed).** This page is design guidance, not legal, clinical, or other professional advice. A qualified reviewer (for example a pharmacist or a compliance lead for your line) must review the read-back wording, the list of protected actions, and the hand-off rule before use. I state a regulation or medical point only where a source I opened supports it; this page states no regulation.

| | |
|---|---|
| **Channel** | Written for **chat**: a bot that gets a transcript of a call or voice note as text and acts on it. Audio-level signals for live voice are **PLANNED**; no voice or web data was collected for this page. |
| **Stakes** | Medium to high. A flipped word can cancel a refill, close a dispute, or approve a charge. |
| **Who is affected** | Anyone who says a request with "not", "don't", "can't", or "never" in it, most of all in noisy rooms or on poor lines |
| **Frequency** | Occasional (our judgment). Studies below show dropped and inserted words in clinical dictation and negation flips in a simulated clinic test. I found no rate for production voice agents. |
| **Pattern ID** | dropped-negations-and-small-words |
| **Family** | [Voice](../README.md) |
| **Goal** | A voice agent listens, speaks, and takes turns the way a competent person would, hears every speaker accurately, never turns noise or silence into words, and never asks for what can't safely be said aloud. |
| **Primary metric** | Negation-error rate on a labelled set (share of test utterances whose negation or modal flips in the transcript). Target: set from your baseline, then drive it down; the aim for protected actions is 0 unconfirmed. Starting point to tune. |
| **Maturity** | Researched (no test file yet; see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | Partly. Better recognizers should flip fewer words, but no recognizer is perfect on one-word differences, so a check outside it is still needed. (Our judgment, not tested.) |
| **Also searched as** | speech to text drops negation · ASR negation errors · voice bot heard the opposite · can't heard as can · transcript missing the word not |
| **Flags** | R (needs research), E (expert review) |

## 1. In plain words
Speech recognition can lose or add short words. "Not", "no", "don't", and "can't" are short, but they flip the whole sentence. The transcript still reads like normal English, so nothing looks wrong. The fix is to protect a short list of risky actions: say back what was understood in plain words, with the negation spelled out, and wait for the caller to choose.

## 2. What it looks like
The call below is made up for this page. Lines in brackets are the transcript the agent received, shown as text.

**Without the fix**
```
Caller: Hi, it's about my lisinopril refill. Please don't cancel it.
        [transcript: "Hi, it's about my lisinopril refill. Please cancel it."]
Agent:  Done. Your lisinopril refill is canceled.
Caller: What? I said don't cancel it.
Agent:  Your refill was canceled at your request. Anything else?
Caller: (hangs up and drives to the pharmacy)
```

**With the fix**
```
Caller: Hi, it's about my lisinopril refill. Please don't cancel it.
        [transcript: "Hi, it's about my lisinopril refill. Please cancel it."]
Agent:  Before I change anything: I heard "cancel the lisinopril refill". Is that right?
        [Cancel it] [Keep it] [Talk to a pharmacist] [Something else]
Caller: Keep it. I said don't cancel.
Agent:  Got it. Your refill is kept and nothing was changed. Want me to check when it's ready?
```
The fixed agent could not see that a word was dropped. It did not rely on the transcript: it read back the action before a cancel, and the caller's choice caught the flip.

## 3. Why it happens
- **Short words carry little for the recognizer.** "Not", "no", and "can't" are brief and usually unstressed, so they are easy to lose or to add. This is our reading. The clinical dictation study below observed deleted and inserted words, including an inserted "no" and a missing "in-" prefix.
- **The usual score treats every word alike.** Word error rate counts a dropped "not" like any other dropped word, so a system can look good on average while flipping meaning. In the stress test below, noise raised word error rate by 0.71 points while the rate of unsafe outputs nearly doubled.
- **Fluent text hides the flip.** The agent, and any model after it, reads the transcript as what the caller said. A read-back that only echoes the transcript repeats the error.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In 217 physician-dictated notes from two US health systems (2016), the raw speech-recognition draft had a 7.4% error rate; 0.4% after transcriptionist editing; 0.3% after physician sign-off. Deletions were 34.7% and insertions 27.0% of draft errors. 5.7% of draft errors were clinically significant. | [Zhou et al., JAMA Network Open (2018), PMC6203313](https://pmc.ncbi.nlm.nih.gov/articles/PMC6203313). Opened and read. | Physician dictation, not a conversation with a voice agent. One back-end service (Dragon Medical 360 \| eScription). Small sample. Negation is not counted as its own category. |
| Meaning-reversing examples in that study: audio "Inadequate evaluation to exclude neoplasia" became "Adequate evaluation to exclude neoplasia"; an inserted negation turned "distal biliary obstruction observed" into "no distal biliary obstruction observed." | Same paper. Opened and read. | Two examples, not a rate. They show both directions: a word lost and a word added. |
| In a stress test of Whisper-large-v3 on simulated clinic dialogues, clean-audio word error rate was 16.54% and the negation error rate was 19.12%. With office, cafeteria, or traffic noise at 15 dB, word error rate rose by 0.71 points (to 17.25%) while unsafe outputs rose from 13.60% to 27.21%. At 5 dB with competing speech, word error rate was 54.68% and negation error rate 51.10%. | [Jiang et al., "Beyond WER", arXiv 2606.05909](https://arxiv.org/html/2606.05909v1) (listing: submitted 4 June 2026, accepted to INTERSPEECH 2026). Opened and read (HTML and abstract page). | Preprint I did not see peer-reviewed. Simulated patient-doctor dialogues, one recognizer, one downstream model. The negation error rate counts a dialogue as an error if any clinical entity flips negation status, so it is per dialogue, not per word. Not a target for your system. |
| Negation is rare in popular language-understanding datasets and is often unimportant there; transformers trained on them "obtain substantially worse results with instances that contain negation," most when the negation is important. | [Hossain et al., ACL 2022 short papers](https://aclanthology.org/2022.acl-short.81). Abstract page opened. | About text models, not speech. Relevant to the model that reads the transcript, not to the recognizer. No figures read. |

**Not used.** A recognition vendor's "no fever" example, a blog's claim about word accuracy and errors per turn, radiology-report error counts, and a Joint Commission safety alert were seen **only in search summaries**. I did not open them, so no number from them is on this page. I found no study that measures how often production voice agents drop or flip negations.

## 5. The fix
**The principle:** For any action that is hard to undo, never trust the transcript alone: say back the action in plain words, with the negation stated, and let the caller choose.

**Do this**
1. **Protect a list.** Name the actions that need a read-back (cancel, close, pay, authorize, dispute, delete, change a dose or a payment). Any request that matches one gets steps 2 to 4 before it runs.
2. **Read back the action, not the sentence.** Say what will happen in plain words, with the negation spelled out ("keep" vs "cancel"; "you did not make this charge"). Do not echo the transcript.
3. **Ask for a choice, not a bare yes.** Offer the two outcomes by name ("Cancel it" or "Keep it"). Never ask a yes/no question that contains a negation ("You don't want to cancel it?").
4. **Treat a correction as a failed transcript.** If the next turn says "no, I said don't", "that's not what I said", or repeats the request with a negation, undo or hold the action, say nothing was changed, and read back again.
5. **Mark negation cues.** For each protected request, log whether the transcript has a cue (not, no, never, don't, can't, cannot, without, n't) and a modal (can, must, should, may). Use it for review and for rule 6.
6. **Check against a second reading.** When a second transcript exists (another recognizer, or the same audio re-run), a difference in cues or modals makes the request "unverified": ask, do not act.
7. **Test negation on its own.** Keep a labelled set of negated and modal utterances; report the negation-error rate next to word error rate, with and without noise.

**Reference design: protected-action check**
| Condition | Agent does |
|---|---|
| Protected action, transcript clear | Reads back the action by name, offers the two outcomes, acts only on the caller's choice |
| Protected action, cues differ between two readings | Marks "unverified", asks one question naming both meanings |
| Caller corrects after an action | Says what changed, undoes if possible, reads back again |
| Not a protected action | Proceeds; no extra confirmation |

```
For cancel, close, pay, authorize, dispute, or delete requests: do not act on the transcript alone.
State what will happen in plain words, with the negation spelled out, and offer both outcomes by name.
Never ask a yes/no question that contains "not", "don't", or "can't".
If the caller says you got it wrong, say nothing was changed (or what was undone), then read back again.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | A protected action is pending or the two readings differ: one question naming both outcomes. Do not use it for harmless requests. |
| Offer choices: 2-4 options plus "Something else", free text open | The read-back: "Cancel it", "Keep it", "Talk to a pharmacist", "Something else". Do not use it when the caller already chose. |
| Hand off to a person | The caller rejects the read-back twice, or a protected action is still unconfirmed. Do not hand off if the caller wants to keep going with the agent. |

**Don't over-correct.** Reading back every sentence makes calls long and teaches people to say "yes" without listening. Keep read-backs to the protected list and unverified requests, keep them to one short turn, and track how often callers say yes to a read-back that was wrong (see the counter-metric).

**Hand-off rule.** If the caller rejects the read-back twice, or the action stays unconfirmed, pass a person the audio, every transcript, and what was done or undone ([cold transfer](../../human-handoff/failures/cold-transfer.md) shows what to avoid).

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
Results: **Not yet run**.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | "Please don't cancel my refill", transcript says "cancel my refill" | The agent reads back "cancel" vs "keep" and does not cancel before a choice (1, 2, 3) |
| 2 | "I did not authorize that charge", transcript says "I authorized that charge" | Read-back states which of the two the caller means; no dispute is closed before a choice (2, 3) |
| 3 | Read-back question wording | No confirmation question contains "not", "don't", or "can't" (3) |
| 4 | Caller says "no, I said don't cancel" after an action | The agent says what changed, undoes or holds, and reads back again (4) |
| 5 | Protected request with the cue logged | The cue and modal fields are present on every protected request (5) |
| 6 | Two transcripts differ on "can" vs "can't" | The request is marked unverified and the agent asks (6) |
| 7 | Labelled negation set, with and without noise | The negation-error rate is reported beside word error rate (7) |
| 8 | A harmless request ("what are your hours?") | No read-back is added (Don't over-correct) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Negation-error rate on a labelled set** (primary) | Set from your baseline, then lower | Run labelled negated and modal utterances each release; count transcripts where the negation or modal differs from the reference | Any rise from the last release; any flip in the protected-action subset |
| Protected actions run without a read-back and a choice | 0 | Log each protected action with its confirmation fields | Any |
| Read-backs that state the negation outcome by name | 100% | Sampled review of read-back turns | Below 95% |
| Caller rejects a read-back ("no, I said don't") | Track; each one is a caught error | Count read-back turns followed by a rejection | Rising |
| Callers who confirmed a wrong read-back (counter-metric) | Track; lower is better | Audit sample: compare audio, transcript, and final action | Any in the protected subset |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Written for text: the next user turn says "no, I said don't" or "that's not what I said" after a protected action | Next user turn text | The caller changed their mind |
| Written for text: a protected action is undone or reversed within 5 turns | Action log plus turn order | A deliberate reversal |
| Written for text: two transcripts of the same audio differ on a negation cue or modal | Transcript pair, if both are logged | A real difference in wording by the second recognizer |
| Written for text: a protected request has no negation cue, while the caller's earlier text turn in the same session had one | Earlier turns plus transcript | The caller dropped the earlier idea |
| PLANNED for voice: a negation word with low recognizer confidence, or a very short word segment | Needs word-level confidence and timing; none is recorded here | A fast, clear speaker |

**Starter rule:** for any protected action, read back the action with the negation spelled out and act only on the caller's choice.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: dropped-negations-and-small-words
runs: pre_send
reads: [transcript.text, transcript.alt_text, action.pending, action.protected, action.confirmed, turn.next_text]
trigger: a protected action is about to run from a transcript
moves: [ask_one_question, offer_choices, hand_off]
choices: ["Cancel it", "Keep it", "Talk to a person", "Something else"]
on_miss: ask
metric: negation-error rate on a labelled set
counter_metric: callers who confirmed a wrong read-back
status: proposed
```

## 8. Related patterns
- [Transcription hallucination](transcription-hallucination.md): the closest voice page. There, words come from silence or noise. Here, real words are heard but a small one is lost, added, or swapped.
- [Repair failure](repair-failure.md): the caller's spoken correction is not understood. Here, the correction ("no, I said don't") is how we catch the error, and rule 4 depends on repair working.
- [Negation and exceptions ignored](../../dialogue-management/failures/negation-and-exceptions-ignored.md): the text version. There, the transcript or message has the "not" and the model ignores it. Here, the speech-to-text step loses the "not" before the model sees it.
- [Background noise failures](../../../../speech-and-audio/goals/audio-handling/failures/background-noise-failures.md): noise lowers accuracy in general; this page is about the one-word flips that matter most.
- [Low confidence mishandling](../../../../speech-and-audio/goals/speech-recognition/failures/low-confidence-mishandling.md): confidence scores go unused. Word-level confidence on negations is a planned signal here.

## 9. Common questions
### Why does my voice bot hear the opposite of what I said?
Speech recognition can lose or add short words like "not" and "no". A clinical dictation study found deleted and inserted words, including an inserted "no" that flipped a finding. See [section 4](#4-why-it-matters).

### Is word error rate enough to judge a speech to text system?
No. In one 2026 stress test, noise raised word error rate by 0.71 points while unsafe outputs nearly doubled. Report a negation-error rate beside it.

### How do I stop a voice agent from canceling when the caller says "don't cancel"?
For cancel, close, pay, and similar actions, read back the action in plain words and ask the caller to pick "cancel it" or "keep it". Do not rely on the transcript alone. See [section 5](#5-the-fix).

### Why not just ask "Is that right?" after every sentence?
Callers learn to say yes without listening, and calls get long. Keep read-backs for the protected list and unverified requests.

### Does a better model fix dropped negations?
It should help, but no source I opened shows a recognizer that never flips a small word. Keep the read-back. Our judgment, not tested.

---
## Technical section

### T1. Solution architecture
```
audio -> recognizer(s) -> transcript(s) -> cue detector (negations, modals)
      -> intent + protected-action check -> read-back with choices -> action after the choice
```
### T3. Evals
- **Dataset:** pairs of utterances that differ only by a negation or modal ("cancel it" / "don't cancel it"; "I can pay" / "I can't pay"), in US accents, quiet and noisy. Start with 100 pairs (starting point). Label the reference by hand.
- **Judge rubric:** does the transcript keep the negation or modal? Does the action match the caller's meaning?
- **Metrics and starting thresholds:** negation-error rate reported with and without noise; protected actions without a choice = 0. Starting points to tune.
- **Release gate:** block a deploy if any protected action can run without a read-back and a choice, or if the negation-error rate rises over the last release.

### T5. Trade-offs
- A read-back adds one turn on protected actions. Keep it short and offer choices.
- Running two recognizers adds cost and latency; it is optional. The read-back works without it.

---
### Deep dive
- **Open question.** I found no measurement of how well a read-back with named outcomes catches dropped negations in live calls. Test it on your own set.
- **Modality notes.** Live voice (PLANNED): word-level confidence and word duration could flag a negation that the recognizer was unsure about. Reading choices aloud is limited to 2-4 short options.
- **References.** [Zhou et al. 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC6203313) (opened); [Jiang et al. 2026](https://arxiv.org/html/2606.05909v1) (opened; preprint); [Hossain et al. 2022](https://aclanthology.org/2022.acl-short.81) (abstract page opened).
