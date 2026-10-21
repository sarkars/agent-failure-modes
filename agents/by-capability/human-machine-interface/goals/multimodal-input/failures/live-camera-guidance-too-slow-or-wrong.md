# AI Gave the Wrong Next Step From My Photo: Live Camera Guidance Too Slow or Wrong

<!-- SEO
title: AI Gave the Wrong Next Step From My Photo: Camera Guidance Fix
description: Why a setup or repair assistant gives the next step before checking your newest photo or clip, and a fix: check the current frame before each step.
search phrases:
- point your camera and ask ai what's wrong
- ai step-by-step guidance fixing coffee machine camera
- ai repair assistant real-time voice instructions
- gemini live camera troubleshooting
- chatgpt video screen share help
- be my ai describe photo
- ai assistant ignored my photo and gave the next step
- router setup support chat send a photo of the lights
(Phrases come from result titles and wording seen during research, not from volume data.)
-->

**Frequency**: Occasional

## Issue: In a step-by-step setup or repair chat, the user sends a photo or short clip after each step, and the assistant gives the next step from its script or an older photo instead of what the newest one shows; the fix is to check the current frame before each step and say what it shows.

> **One line:** The photo shows the cable in the wrong port and an amber light, and the bot says "Looks good! Now open the app."

| | |
|---|---|
| **Channel** | Written for **chat** where the user sends photos or short video clips step by step (support chat, web chat, messaging apps). A live camera stream (Gemini Live camera, ChatGPT voice with video) is PLANNED, not written, and no live-stream signal on this page is detected or measured. |
| **Stakes** | Low to high. A wrong router step costs a call to support; a wrong step on water, gas, or power during an appliance install can cost a repair bill or be unsafe. |
| **Who is affected** | People setting up or fixing a device with a support assistant, and blind or low-vision people who rely on an AI to read what their camera shows and cannot check the photo themselves |
| **Frequency** | Occasional (our judgment). Research benchmarks (section 4) show streaming video models struggle with timing, but no study counts how often a chat assistant gives a step that does not match the user's photo. |
| **Pattern ID** | live-camera-guidance-too-slow-or-wrong |
| **Family** | [Multimodal input](../README.md) |
| **Goal** | Whatever the person attaches, the assistant says what it received and works from what is really there. |
| **Primary metric** | Steps that don't match the frame, in testing. Starting target: 0 in scripted tests with planted mismatches (tune on your own data). |
| **Maturity** | Needs review |
| **Will a better model fix this?** | Partly. Better vision reads a photo more accurately, but answering the newest photo and holding the next step until the photo shows the right state are flow rules the product has to set; a model cannot check a frame it was not given. (Our judgment, not tested.) |
| **Also searched as** | ai ignored my photo · bot says looks good but it isn't · chatbot answered my old picture · setup assistant skipped a step · ai camera help gave wrong instructions |

## 1. In plain words
Step-by-step help only works if each step starts from where the person really is. In a photo-by-photo chat, the bot often runs its script ("step 3 comes after step 2") and treats the photo as a formality. Or two photos arrive close together and the bot answers the older one. Either way the next step is built on a state the device is not in, and the person cannot tell the bot never looked.

## 2. What it looks like
Illustrative transcripts (invented for this page, not from a real product). "Lakeshore Fiber" is an invented internet provider; a customer in Columbus, Ohio is setting up its LF-200 router in the support chat.

**Without the fix**
```
Bot:  Step 2: Plug the gray cable from the wall into the yellow WAN port on the router.
User: (sends photo 1: cable in a black port labeled LAN 1; light blinking amber)
Bot:  Looks good! Step 3: Wait for a solid white light, then open the Lakeshore app.
User: (sends photo 2: light still blinking amber)
User: it's still orange?
Bot:  Great, the light is white, so you're online. Step 4: Name your Wi-Fi network.
User: it's NOT white. forget it, I'll call.
```

**With the fix**
```
Bot:  Step 2: Plug the gray cable from the wall into the yellow port marked WAN. Send a photo once it's in.
User: (sends photo 1: cable in a black port labeled LAN 1; light blinking amber)
Bot:  In this photo the cable is in the black port labeled LAN 1, not the yellow WAN port, and the light
      is blinking amber. Move the cable to the yellow port, then send a new photo.
      [I moved it] [I can't find the yellow port] [Something else]
User: (sends photo 2: cable in the yellow port; light blinking white)
Bot:  Your newest photo shows the cable in the yellow WAN port. The light is still blinking, not solid.
      Send one more photo when it stops blinking.
User: (sends photo 3: solid white light)
Bot:  Solid white in this photo, so the router is online. Step 3: open the Lakeshore app and tap Set up.
```
The fixed bot says what the newest photo shows before each step, holds the next step until the photo matches, and names the one thing to change. (Port colors and light meanings are invented for the example.)

## 3. Why it happens
- **The script moves on its own clock.** Setup flows are written as an ordered list. If "user sent a photo" counts as "step done," the next step goes out whatever the photo shows, and the model fills the gap with "Looks good!"
- **The frame the bot reads is not the newest one.** Photos and clips arrive while a reply is being written, or a clip is summarized from its first seconds. The reply is built on an earlier state. Streaming research names the same timing gap: benchmarks that pause video at fixed moments leave "streaming predictions untested" (section 4).
- **Unclear photos are treated as clear.** Photos taken for help are often blurry, dark, or miss the part that matters, and a model will still describe something. Without a rule to say "I can't see the port labels," a guess becomes the observed state.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Over 31,000 visual questions from blind people, each a phone photo plus a spoken question; the images "are often poor quality" and "often visual questions cannot be answered." | [Gurari et al., VizWiz Grand Challenge, arXiv:1802.08218](https://arxiv.org/abs/1802.08218) (2018). Abstract opened 2026-10-21 (fetch tool summary). | Photos from blind photographers, collected before current chat models. It shows photos sent for help often cannot answer the question; it does not test step-by-step guidance. |
| VIAssist says users struggle with "capturing the desirable images," that often the target object is not fully or partially in the image, and that its system "can identify undesired images and provide detailed actions." | [Yang et al., VIAssist, arXiv:2404.02508](https://arxiv.org/abs/2404.02508) (April 2024). Abstract opened 2026-10-21 (fetch tool summary). | One research prototype; only the abstract was read. It supports asking for a specific retake, not any rate for products. |
| SPOT-Bench says existing online video benchmarks "pause the video at fixed timestamps" and score only then, which "leaves streaming predictions untested." It reports that offline models "spam predictions unprompted" and that training for silence "induces unresponsiveness." The page lists 940 videos and 68 hours of footage. | ["Don't Pause! Every prediction matters in a streaming video", arXiv:2604.24317](https://huggingface.co/papers/2604.24317) (2026). Hugging Face paper page opened 2026-10-21 (fetch tool summary; the dataset figures came from the page body, and only part of the page was read). | Live video, which is PLANNED on this page. It shows timing is a known, separate weakness of video models; it does not measure wrong repair steps. |
| VSAS-Bench says "existing VLM frameworks predominantly assess models in offline settings," uses over 18,000 annotations, and argues streaming performance depends on proactiveness and consistency, not only video understanding. | [Vasu et al., VSAS-Bench, arXiv:2604.07634](https://arxiv.org/abs/2604.07634) (April 2026, CVPR Findings 2026 per the page). Abstract opened 2026-10-21 (fetch tool summary). | Benchmark design paper; the abstract gives no latency or error rate we can use here. |
| A paper on real-time video for AI assistants says current real-time communication causes "latency spikes and accuracy drops," and reports its own system improves accuracy by 15.12% and cuts latency by 135.31 ms. | [Wu et al., Artic, arXiv:2602.12641](https://arxiv.org/abs/2602.12641) (February 2026). Abstract opened 2026-10-21 (fetch tool summary). | The authors' own system; the abstract does not name the baseline. Live streaming only. It shows lag and accuracy trade off; it is not a chat result. |
| Be My Eyes announced its GPT-4 visual assistant (now Be My AI) on March 14, 2023 as a closed beta, saying that when the tool "is unable to answer a question, it will automatically offer users the option to be connected via the app to a sighted volunteer." | [Be My Eyes announcement](https://www.bemyeyes.com/?p=1012), March 14, 2023. Opened 2026-10-21 (fetch tool summary). | A launch post, not a study. It shows one visual-assistance product built a hand-off to a person into the design; it says nothing about accuracy. |

**Public incident.** No public incident found. Searches run: Gemini Live camera limitations; Be My AI limitations; streaming video LLM latency benchmarks; Gemini camera help page; ChatGPT voice video FAQ; VizWiz image quality; Gemini Live camera announcement; Be My AI announcement; AI live camera assistant wrong repair step. No dated, sourced report of a wrong step given because the assistant did not check the user's camera.

## 5. The fix
**The principle:** Check the current frame before each step: say what the newest photo or clip shows that the step depends on, and give the next step only when it matches.

**Do this**
1. **Name the frame before the step.** Every step that follows a photo or clip starts with one line on what the newest frame shows that matters for this step ("In this photo the cable is in LAN 1").
2. **Answer the newest frame.** If more than one photo or clip arrived since the last reply, check the newest one and say so ("Your newest photo shows the cable in the WAN port"). For a clip, check its last seconds, since that is the current state.
3. **Hold the next step on a mismatch.** If the frame does not show the state the previous step should produce, do not give the next step. Say what differs and give one action to fix it.
4. **Say when the frame can't show it.** If the part that matters is blurry, dark, cut off, or hidden, say what is missing and ask for one specific retake ("closer, with the port labels in view"). Never state a guess as what the photo shows.
5. **Ask for a photo when the result is visible.** After a step whose result shows on the device (a light, a port, a display code), ask for a photo before the next step.
6. **Confirm before risky steps.** Before a step involving water, gas, power, or a factory reset, state the frame check and ask the person to confirm before they act.
7. **Log each step's check.** Record `frame_id`, `frame_time`, `expected_state`, `observed_state`, and `check_result` (`match`, `mismatch`, `unclear`, `no_frame_needed`).

**Reference design: step check and reply rule**
```json
{"step": 2, "frame_id": "img_0412", "frame_time": "2026-10-21T14:14:05-04:00",
 "newest_frame": true, "expected_state": "cable in yellow WAN port",
 "observed_state": "cable in black LAN 1 port; light blinking amber",
 "check_result": "mismatch", "advanced": false}
```
```
Before giving a step after the person sends a photo or clip: look at the newest one. Say in one line
what it shows that matters for this step. If it matches the state the last step should produce, give
the next step. If it does not, say what differs and give one action to fix it. If you cannot see the
part that matters, say what is missing and ask for one specific new photo. Never describe a guess as
what the photo shows.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The newest frame matches: one line on what it shows, then the next step. |
| Admit uncertainty and show how to check | The frame is blurry, dark, or cut off: say what cannot be seen and what photo would show it. |
| Ask one clarifying question | One fact the photo cannot show changes the step (for example, which outlet the cord goes to). Not when the photo answers it. |
| Offer choices: 2-4 options plus "Something else", free text open | After a mismatch: "I moved it", "I can't find the yellow port", "Something else". Skip them when the person already sent a new photo. |
| Hand off to a person | The same step fails its frame check twice, or the step involves water, gas, or power and the frame stays unclear. Not if the person asked to stay with the bot. |

**Don't over-correct.** Do not ask for a photo after steps whose result does not show on the device ("download the app"), and do not describe every detail of a photo. One line on the part that matters is enough. A retake request on a clear photo is its own failure: it is the [over-confirmation](../../dialogue-management/failures/over-confirmation.md) cost line, and the counter-metric in section 7 tracks it.

**Hand-off rule.** If one step fails its frame check twice, or a water, gas, or power step cannot be confirmed from the photo, offer a person and pass along the step number, the photos, and the logged observed state, so the person does not start over ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** [Structured troubleshooting](../../../solutions-library/structured-troubleshooting.md) (one change, then check the result).

## 6. How to test it (short version)
No full test file yet. Results: **not yet run**.

| # | Scenario | Pass if (fix rule) |
|---|---|---|
| 1 | Photo after step 2 shows the cable in the wrong port | Reply names the wrong port and gives no next step (rules 1, 3) |
| 2 | Two photos arrive before the bot replies; the newer one shows a changed light | Reply says it is reading the newest photo and describes that one (rule 2) |
| 3 | A 10-second clip starts with an amber light and ends solid white | Reply describes the end state (rule 2) |
| 4 | Photo is too dark to read the port labels | Reply says what cannot be seen and asks for one specific retake; no guessed port (rule 4) |
| 5 | Step result shows on a light, and the user types "done" with no photo | Bot asks for a photo before the next step (rule 5) |
| 6 | Next step shuts off the dishwasher water valve | Bot states the frame check and asks for confirmation first (rule 6) |
| 7 | Clear photo that matches the expected state | One line on what it shows, then the next step; no retake request (Don't over-correct) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Steps that don't match the frame, in testing** (primary) | 0 | Scripted test chats with planted mismatches (wrong port, stale photo, end-changing clip); a reviewer labels each step as matching or not matching the newest frame | Any |
| Steps logged with the frame they were checked against | 100% | Step events with a `frame_id` and `check_result`, out of steps that follow a photo or clip | Below 95% |
| Steps advanced on a mismatch or unclear check | 0 | Step events with `check_result` in (`mismatch`, `unclear`) and `advanced = true` | Any |
| Steps built on an older frame when a newer one existed | 0 | Step `frame_id` compared with the newest image or clip event before the reply was sent | Any |
| Retake requests on clear, matching photos (counter-metric) | Track; set from baseline | Sampled review of retake requests where the reviewer could see the part that mattered | Rising |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Written for photo and clip chat; live camera-stream signals are PLANNED. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Step sent after an image or clip event with no frame check logged | `attachment.type` in (image, video) followed by a step event with no `frame_id` or `check_result` | A step that needs no visual check, logged as `no_frame_needed` |
| Next step sent while the check says mismatch or unclear | Step event with `check_result` in (`mismatch`, `unclear`) and `advanced = true` | The user said in text that they already fixed it and a photo is on the way |
| Step built on an older frame | Step `frame_id` is not the newest image or clip event at send time | The user asked about the earlier photo on purpose |
| User corrects the bot's reading right after a step | User turn after a step with a new photo plus a correction ("it's still orange", "that's not what I see") | The user misread their own device |

**Starter rule:** check the current frame before each step: say what the newest photo or clip shows that the step depends on, and give the next step only when it matches.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: live-camera-guidance-too-slow-or-wrong
runs: pre_send
reads: [attachment.type, attachment.id, attachment.time, step.frame_id, step.expected_state, step.observed_state, step.check_result, draft_reply.text]
trigger: a step is about to be sent in a chat where the person has sent a photo or clip since the last step
moves: [lead_with_answer, admit_uncertainty, ask_clarifying_question, offer_choices, hand_off]
choices: ["I moved it", "I can't find the yellow port", "Something else"]
on_miss: rewrite
metric: steps that don't match the frame, in testing
counter_metric: retake requests on clear, matching photos
status: proposed
```

## 8. Related patterns
- [Unstructured troubleshooting](../../conversation-frameworks/failures/unstructured-troubleshooting.md): the closest page. It covers a bot that hands over many fixes at once instead of one change and a check. This page assumes one step at a time and covers the check itself: the bot must read the newest photo or clip, and hold the next step when it does not match.
- [Instructions without comprehension checks](../../conversation-frameworks/failures/instructions-without-comprehension-checks.md): checks that the person understood a step. This page checks that the device is in the state the step needs, from the photo.
- [Misreading the screen](../../browser-agents/failures/misreading-the-screen.md): a browser agent misreads the page it acts on. Here the person acts, and the bot misreads or skips their photo.
- [Object hallucination](../../../../document-processing/goals/multimodal-reliability/failures/object-hallucination.md) and the [vision object hallucination page](../../../../vision-and-images/goals/visual-hallucination/failures/object-hallucination.md): the model reports things not in the image. Rule 4 covers that case when it happens inside a setup flow.
- [Silent attachment failures](../../chat-interface/failures/silent-attachment-failures.md): a file that was never fully read. Here the photo was read, but too late or not checked against the step.
- [Voice notes and audio attachments ignored](voice-notes-and-audio-attachments-ignored.md): the audio sibling in this family.
- [Stale state use](../../../../../cross-cutting/operations/goals/state-tracking/failures/stale-state-use.md): the general failure of acting on old state.
- [Over-confirmation](../../dialogue-management/failures/over-confirmation.md): the opposite failure to avoid when adding photo checks.

## 9. Common questions
### Why did the AI say "looks good" when my photo showed a problem?
Many setup flows treat "a photo arrived" as "the step is done" and move to the next step. The fix in [section 5](#5-the-fix) makes the bot say what the newest photo shows first and hold the next step if it does not match.

### I sent two photos and the bot answered the first one. Why?
The second photo likely arrived while the reply was being written, so the reply was built on the older one. Rule 2 says to check the newest photo and say which one is being answered.

### Does this apply to Gemini Live or ChatGPT video?
The same idea applies, but this page is written for chats with photos and short clips. Live camera streams add timing problems that research benchmarks are only starting to measure (section 4); those signals are PLANNED here.

### Should the bot ask for a photo after every step?
No. Ask when the step's result shows on the device, such as a light, a port, or a display code. For steps like "download the app," a photo adds nothing.

### What if the photo is too blurry?
The bot should say what it cannot see and ask for one specific new photo, not guess. Research on photos sent by blind users found they are often poor quality (section 4), so this case is common for some users.

---
## Technical section

### T1. Solution architecture
```
photo or clip arrives -> attach to the current step; mark the newest frame             (rule 2)
draft step reply -> load newest frame (clip: last seconds) -> extract observed_state
                 -> compare with expected_state: match | mismatch | unclear            (rules 1, 3, 4)
                 -> mismatch: hold step, one fix action; unclear: one specific retake
                 -> risky step (water, gas, power, reset): confirm first               (rule 6)
                 -> log step event with frame_id, frame_time, check_result             (rule 7)
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No step goes out on a mismatch or unclear check | Pre-send step gate | Tests 1, 4; production metric |
| Reply reads the newest frame | Frame selection before drafting | Tests 2, 3 |
| Every step after a photo logs its check | Step logger | Logging-coverage metric |

### T3. Evals
- **Dataset:** 30 scripted setup chats to start (starting point): wrong port, stale second photo, clip whose state changes at the end, dark photo, cropped photo, risky valve step, and clear-match controls.
- **Judge rubric:** does each step name what the newest frame shows; is a mismatch held; is an unclear frame stated as unclear; is a clear match answered without a retake?
- **Release gate:** block a deploy if any scripted step does not match the newest frame (starting point).

### T5. Trade-offs
- A frame check adds a vision call per step and some delay; a short "checking your photo" line can go out first.
- Asking for more photos adds turns; limit it to steps whose result is visible.

---
### Deep dive (optional)
- **Modality notes.** In a live camera stream, the frame the model reads and the moment it speaks can drift apart, and the user keeps moving. Frame timestamps, speech start times, and "step spoken after the scene changed" signals are PLANNED, not written.
- **Sources read through a fetch tool summary.** All sources in section 4 were opened with a fetch tool that returned summaries, not raw page text. Recheck quotes and numbers on the live pages before quoting them.
- **Read only in search summaries (unverified, not used in the fix):** that OpenAI's ChatGPT voice FAQ says video and screen sharing work only in the mobile apps for eligible subscribers in Advanced voice, not the newer Live option (the help page returned 403); that a Google help article, as reported by 9to5Google, says the Gemini Live camera turns off when the screen locks or the user leaves the app; that Google's Gemini Live page gives step-by-step coffee machine guidance as an example and tells users to check responses for accuracy (the page we opened was served in Kannada); that a 2024 paper reports 28% of VizWiz photos labeled "Unanswerable."
