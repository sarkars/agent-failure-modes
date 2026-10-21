# Chatbot Ignored What My Screenshot Showed: Conflicting Inputs Resolved Silently

<!-- SEO
title: Chatbot Ignored My Screenshot: Conflicting Inputs Resolved Silently
description: Why a chatbot picks the text or the image when they disagree, without saying so, and a fix: point out the conflict, show both values, and ask which is right.
search phrases:
- chatbot ignored my screenshot
- ai used the wrong order number from my photo
- chatbot trusts text over image
- vision language model text image conflict
- llm image and text contradict which does it believe
- chatbot answered from the picture not what I typed
- multimodal model conflicting inputs
(Phrases come from result titles and wording seen during research, not from volume data.)
-->

**Frequency**: Common

## Issue: The text says one thing and the attached image or file says another, and the assistant silently acts on one of them; the fix is to point out the conflict, show both values, and ask which one is right before acting.

> **One line:** You type order #4471, your photo shows order #4417, and the bot refunds one of them without telling you it saw two.

| | |
|---|---|
| **Channel** | Written for **chat** (text chat with an attached photo, screenshot or file: web chat, app chat, SMS/MMS). Voice and live-camera input are PLANNED, not written. |
| **Stakes** | Low to high. A wrong product description costs a retype; a refund, exchange or address change on the wrong order or size costs money and a second contact. |
| **Who is affected** | Anyone who attaches proof (a photo, receipt, cart screenshot, label) and also types the details, often from memory |
| **Frequency** | Common as a model behavior in research benchmarks (section 4). No study counts how often live support bots do it; that part is our judgment. |
| **Pattern ID** | conflicting-inputs-resolved-silently |
| **Family** | [Multimodal input](../README.md) |
| **Goal** | Whatever the person attaches, the assistant says what it received and works from what is really there. |
| **Primary metric** | Conflicts surfaced to the user in tests. Starting target: 100% of seeded text-versus-attachment conflicts that change the action (tune on your own data). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Larger models detect more conflicts in benchmarks, but which source to trust is a product decision, and only the user knows which value they meant. (Our judgment, not tested.) |
| **Also searched as** | bot used the number from my photo not my message · chatbot didn't notice my receipt was different · ai picked the wrong size from my screenshot · image and caption contradict llm · chatbot ignored my attachment |

## 1. In plain words
People type details from memory and attach a photo or screenshot as proof. Sometimes the two disagree: a different order number, size, date or amount. The bot reads both, quietly trusts one, and acts. The person never learns there was a mismatch, so a mistake in either one goes through.

## 2. What it looks like
Illustrative transcripts (invented for this page, not from a real product). "Harbor & Pine Home" is an invented home-goods retailer in Columbus, Ohio, with a support chat.

**Without the fix**
```
User: My order #4471 arrived broken. I want a refund. (attaches photo of a cracked lamp
      on top of a packing slip that reads "Order #4417")
Bot:  I'm sorry your lamp arrived damaged! I've issued a $89.00 refund for order #4417
      to your card ending 2203. You should see it in 5-7 business days.
User: 4417? That's my mom's order. Mine is 4471. Did you just refund her?
```

**With the fix**
```
User: My order #4471 arrived broken. I want a refund. (attaches the same photo)
Bot:  Thanks for the photo. I see a cracked lamp. One thing doesn't match: you typed
      order #4471, but the packing slip in the photo says #4417. Which order is this for?
      [#4471, what I typed] [#4417, on the slip] [Something else]
User: #4471. I used my mom's box to ship a return.
Bot:  Got it, order #4471. I'll start the damage claim on that order. Could you send one
      photo of the lamp's label or the slip that came with #4471?
```
The fixed bot names both values and where each came from, asks before acting, and keeps the parts that agree (a damaged lamp). The refund amounts, card and timeline are invented for the example.

## 3. Why it happens
- **Models lean toward one modality.** Research on mismatched image-text pairs finds that models often follow the text or the image, depending on the model and the task, instead of noticing the disagreement (section 4).
- **Nothing in the flow compares the two.** The text goes into an intent parser, the image goes into a vision call, and the action uses whichever field filled first. No step checks that the typed order number, size or amount matches the one read from the attachment.
- **Answering beats asking.** Assistants are tuned to finish the task in one turn, so a mismatch is smoothed over rather than raised, the same pull described in [guessing instead of asking](../../dialogue-management/failures/guessing-instead-of-asking.md).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| CLASH pairs COCO images with captions that contain object- or attribute-level contradictions. The paper reports GPT-5 and Gemini 2.5 Pro identifying conflicts 86.78% and 88.48% of the time in multiple choice, many open-source models below 5%, and strong image bias in some models (GPT-4.1 Mini 69.57%, Gemini 2.5 Flash Lite 74.98%) and text bias in others (mPLUG-Owl-2, 97.03% in open-ended). Diagnostic set: 1,289 human-verified cases. | [Popordanoska et al., CLASH, arXiv:2511.19199](https://arxiv.org/abs/2511.19199) (Nov 2025). Abstract opened 2026-10-21; result numbers read through a fetch tool summary of the [HTML version](https://arxiv.org/html/2511.19199v1). | Lab benchmark with captions written to contradict photos, not support chats. Numbers are from one paper and were read through a summary; recheck before quoting. |
| "Mixed Signals" built five datasets of mismatched image-text pairs. Models favored text on simpler queries and images as queries got harder; the gap between image- and text-preferred answers ranged from +56.8% (image favored) to -74.4% (text favored) by task and model. Three mitigation strategies had effects that varied significantly. | [Pezeshkpour et al., arXiv:2504.08974](https://arxiv.org/abs/2504.08974) (Apr 2025). Abstract opened 2026-10-21 (fetch tool summary). | Math, science and description tasks, not retail. Shows the direction of the lean is not predictable, so neither "trust text" nor "trust the image" is a safe default. |
| CrossCheck-Bench has 15k question-answer pairs from real-world artifacts with injected contradictions, tested on 13 vision-language models. Performance dropped as tasks moved from perceptual matching to logical contradiction detection; chain-of-thought and Set-of-Mark prompting gave only small gains. | [Tian et al., arXiv:2511.21717](https://arxiv.org/abs/2511.21717) (Nov 2025, rev. Feb 2026). Abstract opened 2026-10-21 (fetch tool summary). | Benchmark, single source. Suggests a prompt tweak alone will not close the gap; we did not test that on chat products. |
| MMIR has 534 samples with injected errors in webpages, slides and posters, and was used to test six multimodal models on spotting semantic mismatches. | [Yan et al., arXiv:2502.16033](https://arxiv.org/abs/2502.16033) (Feb 2025). Abstract opened 2026-10-21 (fetch tool summary). | Layout-rich documents, close to screenshots. Abstract only; no result numbers are used here. |
| A study of image-caption conflicts found models often favor one modality and that the preference shows in internal representations. A Stroop-style benchmark of 4,410 tasks across 47 models found larger models resolve conflicts better than smaller ones. | [Hua et al., arXiv:2507.01790](https://arxiv.org/abs/2507.01790) (Jul 2025); [Wang et al., arXiv:2505.18969](https://arxiv.org/abs/2505.18969) (May 2025, rev. Feb 2026). Abstracts opened 2026-10-21 (fetch tool summaries). | Why we say "Partly" in the header: scale helps detection, but neither paper is about asking the user. |
| Anthropic's vision docs say Claude "might hallucinate or make mistakes when interpreting low-quality, rotated, or very small images under 200 pixels" and advise to "carefully review and verify Claude's image interpretations, especially for high-stakes use cases." | [Anthropic, Vision](https://platform.claude.com/docs/en/build-with-claude/vision). Opened 2026-10-21 (full page text). | Vendor documentation. A conflict can come from a misread image, not a user error, which is why the fix asks instead of blaming either side. |
| OpenAI's Images and vision guide lists limitations including that the model "may misinterpret rotated or upside-down text and images" and "may generate incorrect descriptions or captions in certain scenarios." | [OpenAI, Images and vision](https://developers.openai.com/api/docs/guides/images-vision). Opened 2026-10-21 (fetch tool summary). | Vendor documentation; same point as the row above. |

**Public incident.** No public incident found. Searches run: multimodal LLM text-image conflict benchmark; vision-language model modality preference under conflict; OpenAI vision guide limitations; "Mixed Signals" vision-language conflict. Results were research papers and vendor docs, not a dated, sourced incident in a support chat.

## 5. The fix
**The principle:** When the text and an attachment disagree on a detail that changes the answer or action, say so, show both values and where each came from, and ask which is right before acting.

**Do this**
1. **Extract the key fields from both.** For each turn with an attachment, pull the action-relevant fields (order number, size, color, date, amount, address, account) from the text and from the attachment separately, and log both.
2. **Compare before acting.** If a field has two different values, mark it `conflict` and do not run any action that uses that field.
3. **Name the conflict in plain words.** The reply says which field differs, quotes both values, and says where each came from ("you typed ... the photo shows ...").
4. **Ask one question with the values as choices.** Offer the typed value, the attachment value, and "Something else" with free text open.
5. **Keep what agrees.** Say what matched (the damaged lamp, the product name) so the person does not have to repeat it.
6. **Don't blame either side.** Phrase it as "doesn't match", not "you made a mistake"; the image may have been misread (section 4).
7. **Act only on the confirmed value,** and repeat it in the action message ("Refund started for order #4471").
8. **Ignore differences that don't change the outcome.** A typed "lamp" against a photo of a "table lamp" is not a conflict.

**Reference design: comparison record and reply rule**
```json
{"fields": [
  {"name": "order_id", "from_text": "4471", "from_attachment": "4417",
   "attachment_ref": "photo_1: packing slip", "status": "conflict"},
  {"name": "item", "from_text": "lamp", "from_attachment": "lamp (cracked)", "status": "match"}
],
 "blocked_actions": ["refund", "replacement"]}
```
```
Before any action, compare each action field read from the user's text with the same field read
from their attachments. If they differ, do not act. Say which field differs, quote both values and
where each came from, and ask which one is right, with both values and "Something else" as choices.
Say what did match. Act only on the value the person confirms.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | One field differs between text and attachment and it changes the action: ask which value is right. Not when the difference doesn't change the answer. |
| Offer choices: 2-4 options plus "Something else", free text open | With that question: "[typed value]", "[attachment value]", "Something else". Skip them when the person already said which one in words. |
| Admit uncertainty and show how to check | The attachment is blurry, cropped or rotated and the value may be misread: say what was read and ask for a clearer photo. |
| Lead with the answer | Text and attachment agree, or differ only in ways that don't matter: answer directly. |
| Hand off to a person | The conflict is still open after two asks, or the claim is high stakes (a fraud-looking receipt, a large refund). Not if the person asked to stay with the bot. |

**Don't over-correct.** Do not raise every small wording gap as a conflict, and do not stop the whole conversation over one field: ask about the field that differs and keep going on the rest. Do not ask again once the person has chosen. Too many checks becomes [over-confirmation](../../dialogue-management/failures/over-confirmation.md).

**Hand-off rule.** If the conflict is not settled after two questions, or the stakes are high, offer a person and pass along both values, the attachment and what was confirmed, so nobody asks again ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
No full test file yet. Results: **not yet run**.

| # | Scenario | Pass if (fix rule) |
|---|---|---|
| 1 | Text says order #4471; photo of slip shows #4417; user asks for a refund | Reply names both numbers and their sources, asks which, and issues no refund yet (rules 2-4) |
| 2 | Text says "exchange for size 10"; cart screenshot shows size 9 | Size conflict raised with both sizes as choices plus "Something else" (rules 3, 4) |
| 3 | Same as 1; user answers "#4471" | Action runs on #4471 and the message repeats it; no second ask (rule 7, Don't over-correct) |
| 4 | Text says "lamp"; photo shows a table lamp, same order number | No conflict raised; bot answers directly (rule 8) |
| 5 | Blurry photo where the order number could be 4417 or 4471 | Bot says what it read, that it may be misread, and asks for a clearer photo or the number (rule 6) |
| 6 | Conflict on order number; product and damage agree | Reply says what matched and asks only about the order number (rule 5) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Conflicts surfaced to the user in tests** (primary) | 100% | Seeded test set of text-versus-attachment conflicts that change the action; count replies that name both values before any action | Below 95% |
| Actions run on a field marked `conflict` | 0 | Action events joined to the comparison record for that turn | Any |
| Corrections after an action on attachment turns | Track; set from baseline | User says "that's not my order", "wrong size" within 2 turns of an action | Rising |
| Conflicts raised on fields that matched or didn't matter (counter-metric) | Track; set from baseline | Sampled review of raised conflicts, test 4 style cases | Rising |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Written for text chat; voice and camera signals are PLANNED. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Comparison record has a `conflict` field and the next bot turn runs an action | `fields[].status = conflict` joined to an action event in the same turn | The person confirmed the value earlier in the conversation |
| Action uses a value found only in the attachment, or only in the text, when both were present | Action payload field compared with `from_text` and `from_attachment` | The other source was unreadable and the bot said so |
| User corrects the order number, size or amount right after an action | User turn with a correction phrase after an action event on an attachment turn | The user changed their mind, not a misread |
| Attachment turn with no comparison record logged | Turn with `attachment` event and no `fields` record | An attachment with no action fields (a general photo) |

**Starter rule:** before any action, compare each action field read from the user's text with the same field read from their attachments, and if they differ, say which field differs, quote both values and ask which one is right.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: conflicting-inputs-resolved-silently
runs: pre_send
reads: [attachment.type, fields.name, fields.from_text, fields.from_attachment, fields.status, draft_reply.text, draft_reply.action]
trigger: a reply or action is about to go out in a turn where a field read from text and from an attachment differ
moves: [ask_clarifying_question, offer_choices, admit_uncertainty, lead_with_answer, hand_off]
choices: ["[value I typed]", "[value in the attachment]", "Something else"]
on_miss: ask
metric: conflicts surfaced to the user in tests
counter_metric: conflicts raised on fields that matched or didn't matter
status: proposed
```

## 8. Related patterns
- [Guessing instead of asking](../../dialogue-management/failures/guessing-instead-of-asking.md): the closest page. It covers one ambiguous request with two readings. This page covers two inputs that each look clear but disagree, and the fix compares fields across text and attachment before asking.
- [Silent attachment failures](../../chat-interface/failures/silent-attachment-failures.md): the attachment was not read or only partly read. Here it was read, and the bot hid that it disagreed with the text.
- [Object hallucination](../../../../document-processing/goals/multimodal-reliability/failures/object-hallucination.md): the model reads a field that is not in the document. A misread like that can create a false conflict, which is why rule 6 asks instead of blaming.
- [Image contradiction](../../../../vision-and-images/goals/multi-image-understanding/failures/image-contradiction.md): two images disagree with each other. This page is text against attachment.
- [Source contradiction](../../../../knowledge-retrieval/goals/answer-synthesis/failures/source-contradiction.md): retrieved documents disagree and the agent picks one. The same failure shape, but the sources come from the system, not from the user.
- [Conflicting instructions](../../../../../cross-cutting/accuracy/goals/context-management/failures/conflicting-instructions.md): system and user instructions clash; this page is about facts the user supplied.
- [Voice notes and audio attachments ignored](voice-notes-and-audio-attachments-ignored.md): the sibling page for audio in the same family.
- [Over-confirmation](../../dialogue-management/failures/over-confirmation.md): the opposite failure to avoid.

## 9. Common questions
### Why did the chatbot use the order number from my photo instead of the one I typed?
Models often lean toward one input when text and image disagree, and research shows the lean goes different ways for different models and tasks ([section 4](#4-why-it-matters)). If nothing in the product compares the two, the bot just uses whichever it trusted. The fix is a comparison step before any action.

### Should a bot trust the text or the image when they conflict?
Neither by default. The person may have typed from memory, or the bot may have misread a blurry photo. Show both values and ask; see the Do this list in [section 5](#5-the-fix).

### Won't asking about every mismatch annoy customers?
Only if you ask about mismatches that don't matter. Ask when the differing field changes the action, such as an order number, size or amount, and ask once. See Don't over-correct in section 5.

### Can a better prompt fix this?
It helps, but one benchmark in section 4 found chain-of-thought style prompting gave only small gains on contradiction detection. A step that extracts fields from both inputs and compares them is more reliable to test.

### How do I test for this?
Seed test chats where the typed detail and the attachment disagree on something that changes the action, and check that the bot names both values before acting. The short test table is in [section 6](#6-how-to-test-it-short-version).

---
### Deep dive (optional)
- **Sources read through a fetch tool summary.** The CLASH result numbers, the Mixed Signals, CrossCheck-Bench, MMIR, Hua et al. and Wang et al. abstracts, and the OpenAI guide were opened with a fetch tool that returned summaries, not raw page text. The Anthropic vision page was read in full. Recheck numbers on the live pages before quoting them.
- **Read only in search summaries (unverified, not used in the fix):** a MAGMaR 2026 workshop benchmark (CMC-Bench) on cross-modal conflicts in multimodal retrieval; an ICML 2026 study reporting different text- or vision-following rates for LLaVA and Qwen models.
- **Modality notes.** Voice-plus-screen and live-camera conflicts are PLANNED and not written here.
