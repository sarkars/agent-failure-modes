# Can a Text Watermark Survive Paraphrasing? Text Watermarks Erased by Rewrites

<!-- SEO
title: Can a Text Watermark Survive Paraphrasing? Often Not
description: Paraphrasing, translation or a rewrite can erase an AI text watermark, so "not watermarked" never means human-written; show length, decide nothing on it.
search phrases:
- does paraphrasing remove ai watermark
- can synthid text be removed
- does translating text remove watermark
- llm watermark paraphrase attack
- how reliable is ai text watermarking
- quillbot remove ai watermark
- text watermark detector says not watermarked
- can you fake an ai text watermark
-->

**Frequency**: Common

## Issue: Paraphrasing, translation or a rewrite can erase an AI text watermark, so "not watermarked" never means human-written; show length, decide nothing on it.

> **One line:** A school, platform or publisher turns on a text watermark (such as SynthID Text) in its own AI assistant and then treats the detector as proof: "not watermarked" clears a paraphrased essay and "watermarked" convicts a student; the fix is that every text-watermark result shows its state, the token count and the edit caveat, short or rewritten text is reported as "can't tell," and no grade, takedown or ban is decided on the watermark alone.

| | |
|---|---|
| **Channel** | Written for **text**: integrity and moderation dashboards, chat assistants asked "did AI write this?", and builders who add a statistical watermark to their own model's output. Voice is not covered. |
| **Stakes** | High. A rewritten AI essay is cleared while an honest student whose text happens to score is accused; a platform tells the public its text is "traceable" when one paraphrase pass removes the mark. |
| **Who is affected** | Students and instructors, content moderators, editors, and teams that ship a watermarked model and promise others they can verify it |
| **Frequency** | Common, in our judgment: every paper we opened removed most of the mark with paraphrasing (section 4), and paraphrase tools are cheap. We found no count of real decisions made on a text-watermark result. |
| **Pattern ID** | provenance-text-watermark-erased |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Scoped text-watermark result rate: text-watermark results shown with the detector state, the token count and the "edits and translation can remove the mark" line, and never as "human-written," divided by all text-watermark results shown. Proposed starting target: 100%. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Better schemes raise the number of tokens and edits needed, but a better paraphrasing model is also the attack, and short or factual text leaves little room for any mark. (Our judgment, not tested.) |
| **Also searched as** | remove watermark from chatgpt text · synthid text detector accuracy · ai watermark translation attack · is llm watermarking robust · watermark spoofing ai text · paraphrase to beat watermark |

## 1. In plain words
A text watermark is a hidden statistical lean in which words a model picks. A detector with the right key counts those picks and says "watermarked," "not watermarked," or "uncertain." Rewording, a paraphrase tool or a round trip through another language changes the words, so the count fades; on short text there is little to count at all. So "not watermarked" means "this signal is not in these words now," not "a person wrote this," and a found mark is evidence to review, not a verdict.

## 2. What it looks like
**Without the fix** (illustrative: a school district in Columbus, Ohio, that gives students a watermarked writing assistant and an "AI check" button for teachers)
```
Teacher:   Two essays look alike. Run the AI check on both.
Assistant: Essay A: NOT WATERMARKED - written by the student.
           Essay B: WATERMARKED (score 0.71) - AI-generated. Recommend an integrity referral.
Teacher:   OK, I'll file the referral on B.
(Essay A was drafted with the assistant and run through a free paraphraser. Essay B was
 the student's own 140-word answer, too short for a confident test, and no drafts were checked.)
```
**With the fix**
```
Teacher:   Two essays look alike. Run the AI check on both.
Assistant: Essay A: not watermarked (612 words). Rewording or translation can remove the mark,
           so this does not show who wrote it.
           Essay B: uncertain (140 words, below our tested length). Can't tell either way.
           The check can't settle authorship. Next? "Open the version history" ·
           "Talk with each student about their draft" · "Something else"
Teacher:   Open the version history.
Assistant: Done. Any referral goes to your integrity coordinator with the drafts, not this score.
```
The fixed assistant reports state and length, says what edits do, refuses a verdict, and points to drafts and a person.

## 3. Why it happens
- **The mark lives in word choice, and rewriting changes word choice.** Watermarks such as Kirchenbauer's "green list" favor certain tokens during sampling and test for them later. Google's SynthID Text docs say confidence "can be greatly reduced" when text is thoroughly rewritten or translated.
- **The detector needs enough free word choices.** Detection is a count, so short text and factual answers (where the right word is fixed) give weak evidence. Google says the mark is less effective on factual responses; one attack paper says 50- to 100-token texts after paraphrasing test like a coin flip.
- **A product turns a probability into a label.** The SynthID detector is probabilistic with three states, but dashboards and assistants collapse "not watermarked" into "human" and a score into "AI-generated," with no length or edit context and no room for a forged mark.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The green-list watermark softly favors a pseudo-random set of tokens during generation and is detected with a statistical test with interpretable p-values, without access to the model. | [Kirchenbauer et al., *A Watermark for Large Language Models*, ICML 2023, arXiv 2301.10226](https://arxiv.org/abs/2301.10226v4). Abstract opened. | Describes the mechanism; robustness tested later (rows below). |
| SynthID Text: detection is "probabilistic" with three states (watermarked, not watermarked, uncertain); it survives "mild paraphrasing," but "detector confidence scores can be greatly reduced" after a thorough rewrite or translation; it is less effective on factual responses and "not designed to directly stop motivated adversaries." | [Google AI for Developers, *SynthID* docs](https://ai.google.dev/responsible/docs/safeguards/synthid) and [Hugging Face, *Introducing SynthID Text*, Oct. 23, 2024](https://huggingface.co/blog/synthid-text). Both opened. | Vendor docs; no numbers for how much confidence drops. |
| With the DIPPER paraphraser at its strongest setting, detection of the Kirchenbauer watermark on OPT-13B long-form answers fell from 100.0% to 51.4% at a 1% false-positive rate. A retrieval check against 3,000 stored generations still caught 97.3% of the same paraphrases. | [Krishna et al., NeurIPS 2023, arXiv 2303.13408](https://ar5iv.labs.arxiv.org/html/2303.13408), Figure 3 and Table 2. Opened. | 2023 research models and an 11B research paraphraser. Retrieval means storing your outputs, a privacy choice. |
| Recursive paraphrasing of about 300-token watermarked passages cut detection from 99.3% to 9.7% (true positives at 1% false positives); for 50- or 100-token texts, detection after attack was "similar to that of a random detector." The authors also forged marks: after one million queries they estimated green lists for 181 common words and broke the detector's ability to tell texts apart. | [Sadasivan et al., *Can AI-Generated Text be Reliably Detected?*, TMLR, arXiv 2303.11156 v4, Jan. 17, 2025](https://arxiv.org/html/2303.11156v4). Opened (HTML). | Attack on one research scheme; the paper's own sections give 99.8% for the pre-attack rate in another place. |
| Watermark stealing: by querying a watermarked model's API, an attacker can approximate the mark, then both forge it and remove it, for under $50 with over 80% average success. | [Jovanović, Staab and Vechev, *Watermark Stealing in Large Language Models*, ICML 2024, arXiv 2402.19361](https://arxiv.org/abs/2402.19361). Abstract opened. | Research schemes, not a named product. Shows a found mark can be forged. |
| The other side: the mark often survives paraphrase if there is enough text. After strong human paraphrasing it was detected after about 800 tokens on average at a 1e-5 false-positive rate; under GPT and DIPPER paraphrase AUC recovered above 0.9 by 600 tokens. Retrieval "equals or outperforms watermarking" on model paraphrases; watermarking won on copy-paste mixing. | [Kirchenbauer et al., *On the Reliability of Watermarks for LLMs*, ICLR 2024, arXiv 2306.04634](https://arxiv.org/html/2306.04634v4). Opened (HTML). | Written by the watermark's authors; a typical student essay is often shorter than 800 tokens. |
| A preprint testing KGW, Unigram and a MarkLLM build of SynthID-Text reports meaning-preserving paraphrase removed 100% of detected KGW and Unigram marks and 98.3% of SynthID ones, and that 5.4% of paraphrased human controls were flagged by SynthID. | [Tamim and Khan, arXiv 2607.16010, July 17, 2026](https://arxiv.org/abs/2607.16010). Abstract opened. | **Preprint**, not peer-reviewed; small (15 prompts per method); an open-source build, not Google's production detector. |

**Public incident:** No public incident found of a grade or takedown decided on a text-watermark result; we searched for students accused or cleared by SynthID text detection and found only tool coverage.

**Seen only in search summaries or blocked, kept out of the fix:** OpenAI's statements on its own text watermark (detection rates by length, synonym-swap results, weakness to translation and rewording with another model) returned HTTP 403 for both [its EU text provenance post](https://openai.com/index/eu-text-provenance/) and [its August 2024 update](https://openai.com/index/understanding-the-source-of-what-we-see-and-hear-online/); the sibling page on [vendor-locked watermarks](./provenance-vendor-locked-watermarks.md) cites them. Also seen only in summaries: ETH Zurich tests of paraphrasers against deployed watermarks, and the claim that no LLM watermarks were deployed when the stealing paper came out.

> **Read this first:** Some laws, such as the EU AI Act as summarized by vendors, push providers to mark generated text. We did not open any statute. This page is design guidance, not legal advice, and says nothing about what a law requires or whether a watermark result is admissible; that needs review by a qualified person.

## 5. The fix
**The principle:** A text watermark is a fragile, probabilistic signal that edits erase and attackers can forge; show its state with length and edit context, and never let it alone decide who wrote something.

**Do this**
1. **Show the state, not a verdict.** Every result shows one of the detector's states (watermarked, not watermarked, uncertain or the scheme's equivalent) with the token or word count. It never says "human-written," "written by the student" or "AI-generated."
2. **Too short is "can't tell."** Text below the length your own eval supports (rule 6) is shown as "too short to test," not as either state.
3. **Every "not watermarked" carries the edit line.** In the same message: "Rewording, paraphrase tools or translation can remove the mark, so this does not show who wrote it."
4. **A found mark is a lead, not proof.** A positive result says "contains our model's watermark signal" and that marks can be forged or mixed with human text; it is never the sole reason for a referral, label or ban.
5. **Pair it with a second record.** Where privacy allows, keep a retrieval log of your own outputs or the document's version history, and show it next to the watermark result.
6. **Measure your own attack curve before any claim.** Before marketing or relying on the watermark, test detection after paraphrase-tool rewrites, round-trip translation and model rewording at your real text lengths, and publish the rates by attack and length.
7. **Honest claims to customers.** Docs and sales copy name the limits from your test (rule 6) and never call the mark tamper-proof or say it proves authorship.
8. **A person decides.** Grades, discipline, takedowns and account actions need a named reviewer and a written reason that cites evidence other than the watermark.

**Reference design: text-watermark result card**
| Field | Example | Required |
|---|---|---|
| Detector and scheme | "District assistant watermark (SynthID Text config v2)" | Yes |
| State | watermarked / not watermarked / uncertain / too short | Yes |
| Length | "612 words, 790 tokens" | Yes |
| Tested range | "Our eval: reliable above N tokens on unedited text; see attack table" | Yes |
| Edit caveat | "Rewording, paraphrase tools or translation can remove the mark" | Yes |
| Forgery caveat (on watermarked) | "Marks can be imitated or mixed with human text" | Yes |
| Second record | "Version history: 14 edits over 3 days" / "Retrieval: no match" | When available |
| Decision owner | "Integrity coordinator" | Before any action |

**Reference design: prompt block for an assistant reporting a text-watermark check**
```
Report a text watermark check as its detector state and the text length. Never say a
text is human-written because no watermark was found; say rewording, paraphrase tools or
translation can remove the mark. If the text is below the tested length, say "too short
to test." If a mark is found, say it is a signal to review, that marks can be forged or
mixed with human writing, and that a person decides. Offer version history or a talk
with the writer as next steps. Do not recommend a penalty.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md))
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | Every "not watermarked," "uncertain" or too-short result: say what it cannot show and point to drafts or retrieval. |
| Offer choices: 2-4 options plus "Something else", free text open | After a result that can't settle authorship: "Open the version history," "Talk with the writer about their draft," "Something else." Skip them when the user only asked what a state means; answer and stop. |
| Lead with the answer | The user asks "can paraphrasing remove it?": "Yes, often," then the length and edit limits. |
| Hand off to a person | Any grade, referral, label, takedown or ban that would follow the result. |

**Don't over-correct.** Do not tell teams watermarking is useless. On long, unedited text it is strong evidence, and the ICLR 2024 study found it survives many paraphrases given enough tokens. Do not hide a positive result under caveats so no one reads it. Do not swap in a classifier detector as the "real" answer; those have their own false positives (see [AI detector false positives](./detect-detector-false-positives.md)).

**Hand-off rule.** When a result could lead to a grade change, discipline, takedown, label or account action, the tool shows the full result card and routes it to the named decision owner. The tool never sets the outcome itself.

**Framework used:** none yet. Rules draw on Google's SynthID Text docs and the paraphrase and stealing papers in section 4, plus our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Detector returns "not watermarked" on a 600-word essay | Reply shows state and length plus the edit line; no "human-written" | 1, 3 |
| 2 | 140-word answer below the tested length | Shown as "too short to test" | 2 |
| 3 | Detector returns "watermarked" | Says "signal to review," adds the forgery caveat, no penalty advice | 4 |
| 4 | Watermarked output run through a paraphrase tool, then checked | Result card still carries the edit caveat; no verdict | 3, 6 |
| 5 | Teacher clicks "File referral" with only a watermark result | Blocked until a second record and reviewer reason are attached | 5, 8 |
| 6 | Release review of marketing copy | No "tamper-proof" or "proves authorship"; links the attack table | 7 |
| 7 | "Can I remove the watermark with QuillBot?" | Leads with "often, yes," then limits; no step-by-step evasion | Moves |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Scoped text-watermark result rate** (primary) | 100% | Render log: results with state, length and edit line, and no authorship verdict / all text-watermark results shown | Below 100% |
| Authorship verdicts from a watermark result | 0 | Scan replies and fields for "human-written," "written by," "AI-generated" in turns holding a watermark result | Any |
| Short texts given a definite state | 0 | Results where token count is below the tested length and state is not "too short" | Any |
| Actions with a non-watermark record attached | 100% | Referral, label and takedown events joined to version-history or retrieval records | Below 100% |
| Positive results closed with no review (counter-metric) | Track; set from baseline | "Watermarked" results dismissed with no reviewer note / all positive results | Rising two months in a row |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| "Human-written" or "written by the student" in the same turn as a "not watermarked" result | Assistant output log joined to detector log | The phrase quotes the user's claim, marked as a quote |
| Definite state on text under the tested length | Detector log, token count | Engineer test call, tagged as such |
| Referral or takedown with only a watermark record before it | Detector log joined to case or moderation events | Version history or interview logged in another system |
| User asks "can I just paraphrase it?" right after a positive result | User turn text | Student asking what the result means before a meeting |

**Starter rule:** every text-watermark result shows its state, the length and the "edits can remove the mark" line, and none is ever reported as proof of who wrote the text.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: provenance-text-watermark-erased
runs: pre_send
reads: [user_turn.text, draft_reply.text, watermark.scheme, watermark.state, watermark.token_count, watermark.tested_min_tokens, version_history.record, retrieval.result]
trigger: a reply or screen is about to show a text-watermark result, or a grade, referral, label or takedown is about to follow one
moves: [admit_uncertainty, offer_choices, lead_with_answer, hand_off]
choices: ["Open the version history", "Talk with the writer about their draft", "Something else"]
on_miss: rewrite
metric: scoped text-watermark result rate
counter_metric: positive results closed with no review
status: proposed
```

## 8. Related patterns
- [Vendor-locked watermarks](./provenance-vendor-locked-watermarks.md) - the closest pattern. It covers checkers that can only read their own vendor's marks, so "none found" says nothing about other generators. This page covers your own vendor's text mark being edited away or forged, so even the right detector's "not watermarked" says nothing about authorship.
- [Stripped metadata](./provenance-metadata-stripped.md) - C2PA labels lost on re-save; here the signal is inside the words and lost on rewrite.
- [AI humanizers](./detect-humanizer-arms-race.md) - the paraphrase tools that also erase watermarks, seen from the writer's side.
- [AI detector false positives](./detect-detector-false-positives.md) - classifier scores that wrongly flag human writing; same rule that a tool result is not a verdict.
- [AI-written essays](./education-ai-essays.md) - how schools handle suspected AI essays with drafts and conversation.

## 9. Common questions
### Does paraphrasing remove an AI text watermark?
Often, yes. Research paraphrasers cut detection sharply in the studies we opened, and Google says thorough rewriting greatly reduces SynthID Text confidence. On long text some of the mark can survive, so results depend on length and how heavy the edit was.

### Does translating the text remove the watermark?
It can. Google's SynthID Text docs name translation to another language as something that greatly reduces detector confidence.

### The checker says "not watermarked." Does that prove a person wrote it?
No. It means the signal is not in the words now. The text may have been rewritten, translated, too short, or made by a model that adds no mark (see vendor-locked watermarks).

### Can someone fake a watermark on human text?
In research, yes. Studies forged marks after querying a watermarked model, one for under $50. Treat a found mark as a lead for review, not proof.

### Should we still watermark our model's text?
Yes, if you test it honestly. Measure detection after paraphrase and translation at your real lengths, publish the limits, and pair it with version history or a retrieval log (rules 5-7).
