# Chatbot Animations and Flashing: Motion That Can Harm Users

<!-- SEO
title: Chatbot Animations and Flashing: Motion That Can Harm Users
description: How chat animations (confetti, bouncing dots, auto-playing GIFs, parallax, flashing effects) can trigger seizures or vestibular symptoms, and rules for honoring reduced-motion settings and the WCAG flash limit.
search phrases:
- chatbot animation accessibility
- prefers-reduced-motion chat widget
- chatbot confetti animation vestibular
- chat widget flashing seizure WCAG 2.3.1
- auto-playing GIF in chatbot accessibility
- reduce motion setting chatbot ignores
- chatbot typing animation motion sickness
- how to pause animations in a chat widget
-->

> **Read this first.** This page is design guidance for developers, not medical or legal advice. It cannot tell you whether a specific animation is safe for a specific person. Have an accessibility specialist review any animation, video or GIF your chat shows before release, and test with the OS reduce-motion setting on. Requirements are quoted only as far as I opened the W3C and MDN pages in section 4.

**Frequency**: Occasional

## Issue: A chat assistant plays animation the user did not ask for (confetti, bouncing dots, auto-playing GIFs or video, sliding and parallax effects, flashing alerts) and ignores the device's reduce-motion setting, so it can cause dizziness, nausea or, with flashing, seizure risk.

> **One line:** The bot celebrates with full-screen confetti, loops a generated GIF, or flashes a "new message" banner, even though the user turned on "reduce motion"; the fix is to treat motion as optional, honor that setting, never flash more than three times a second, and let the user stop anything that moves.

| | |
|---|---|
| **Channel** | Written for **chat** (a chat widget, rich cards, generative UI and media the assistant sends). Voice and web-page variants are PLANNED, not written. |
| **Stakes** | Medium to high for the affected users. WCAG says flashing content can cause seizures; its animation guidance says vestibular reactions can include dizziness, nausea and headaches. |
| **Who is affected** | People with vestibular disorders, photosensitive epilepsy or migraine, and anyone who set reduce-motion on a device |
| **Frequency** | Occasional as a design default. I found no study counting how many chat products animate without checking the setting. |
| **Pattern ID** | motion-and-flashing-harm |
| **Family** | [Visual](../README.md) |
| **Goal** | Motion is minimal, and reduced-motion settings are respected. |
| **Primary metric** | Share of animations and auto-playing media that respect `prefers-reduced-motion` (and can be paused). Starting target: 100% (a starting point; tune it). Read it next to flashing content, target 0 over the WCAG limit. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Animation comes from the widget's CSS and the media the product allows, not from the model's wording. A better model can still be asked to "generate a celebratory GIF". (Our judgment, not tested.) |
| **Also searched as** | chatbot confetti animation · reduce motion chat · chat widget flashing · animated GIF accessibility · parallax chat · motion sensitivity chatbot |

## 1. In plain words
Some people get dizzy or sick from motion on a screen, and a small group can have a seizure from flashing. A chat product can add motion without anyone deciding to: a confetti burst when a task finishes, a looping GIF the bot generated, bouncing dots, a chat window that slides and scales. The fix is to make motion optional. Check the user's reduce-motion setting before any non-essential animation, never flash fast, and give a way to stop what is moving.

## 2. What it looks like
**Without the fix** (illustrative scenario, fictional "Harbor Mutual" insurance assistant; the user's phone has Reduce Motion on)
```
User: Can you file my claim for the cracked windshield?
Bot:  Done! Your claim #48213 is filed.
      [full-screen confetti plays for 6 seconds]
User: Can you show me what happens next?
Bot:  Sure! Here is a quick video.
      [auto-playing looping GIF of a spinning progress wheel, flashing between red and white]
User: Please stop the moving thing.
Bot:  I'm not able to control the animation. Is there anything else I can help with?
```
**With the fix**
```
User: Can you file my claim for the cracked windshield?
Bot:  Your claim #48213 is filed. A repair shop will contact you within 2 business days.
      (no confetti: reduce-motion is on, so a static check mark shows instead)
User: Can you show me what happens next?
Bot:  Here are the three steps, as text. [Play the short video]    (not auto-played; has a pause control)
User: Please stop the moving thing.
Bot:  Motion is off now. I'll keep replies static. You can turn it back on in Settings > Display. [Something else]
```
The fixed version marks the outcome in text first, replaces decoration with a static mark when reduce-motion is on, makes the video start only when asked, and gives the user control.

## 3. Why it happens
- **Motion is added as polish, by different owners.** A designer adds the confetti, a front-end dev adds the slide-in, a prompt author lets the bot send GIFs. No one checks the whole screen against the user's setting.
- **The setting is a CSS query, and widgets and embedded media bypass it.** `prefers-reduced-motion` has to be handled in each stylesheet and script. A third-party widget, a canvas effect or a GIF file does not read it unless someone wires it up.
- **Generated media is not reviewed.** If the assistant can return an image, GIF or video from a tool or a model, the product may play it as is. No step measures flashing before display.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| WCAG 2.3.1 (Level A): "Web pages do not contain anything that flashes more than three times in any one second period, or the flash is below the general flash and red flash thresholds." The page says flashing content "can cause migraines, dizziness, nausea, and seizures." | [W3C, Understanding SC 2.3.1](https://www.w3.org/WAI/WCAG22/Understanding/three-flashes-or-below-threshold.html). Opened and read. | A web-content standard, not a chat-specific rule. Legal duty to follow it depends on where and for whom you operate; ask counsel. |
| The same page defines a general flash as a pair of opposing changes in relative luminance of 10% or more of the maximum (1.0), where the darker image is below 0.80, and a red flash as opposing transitions involving a saturated red. The area limit is about 341 x 256 pixels at a 1024 x 768 reference, a 10-degree field. | Same W3C page. Opened and read. | Measuring this takes a tool and review. I did not test any tool. |
| WCAG 2.3.3 (Level AAA): "Motion animation triggered by interaction can be disabled", unless essential. It says vestibular (inner ear) reactions "include dizziness, nausea and headaches", and names parallax scrolling as often non-essential. Another passage says reactions can be severe, including potentially needing bed rest to recover. | [W3C, Understanding SC 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html). Opened and read. | Level AAA is the highest, optional level. It is about interaction-triggered motion, which fits hover, scroll and click effects more than a bot's own message. |
| WCAG 2.2.2 (Level A): moving, blinking or scrolling content that starts automatically, lasts more than five seconds and sits beside other content needs a way to "pause, stop, or hide it", unless essential. Auto-updating content has the same need without the five-second exception. | [W3C, Understanding SC 2.2.2](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide). Opened and read (success criterion text only; I did not read the techniques). | Whether a looping chat GIF counts as "in parallel with other content" is a judgment call; treat it as yes. |
| MDN: `prefers-reduced-motion` detects whether the user "has enabled a setting on their device to minimize the amount of non-essential motion"; the values are `no-preference` and `reduce`. It says such animations "can trigger discomfort for those with vestibular motion disorders" and that scaling or panning large objects can be triggers. Its example swaps a scaling animation for an opacity-only one under `reduce`. | [MDN, prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion). Opened and read (first part of the page). | Reference documentation, not a study. I did not read the browser-support table; check it for your targets. |

I found no study of how often chat widgets break these rules, and no public incident of a chatbot animation causing harm, so this page has no prevalence figure.

**How this differs from the closest pages.** [Deceptive typing indicators](../../response-time/failures/deceptive-typing-indicators.md) is about animated dots that fake "thinking" time and mislead on honesty; this page is about the motion itself harming people, even when the indicator is honest. [Auto-scroll fights the reader](../../chat-interface/failures/auto-scroll-fights-the-reader.md) covers the view jumping while the user reads; this page covers decorative or media motion and flashing. [Accessibility in chat](../../fairness-and-identity/failures/accessibility-in-chat.md) is the broad pattern for disabled users; this page is the motion and flashing case. [Streaming text read out token by token](../../accessibility/failures/streaming-text-read-out-token-by-token.md) is about screen readers, not visual motion. [Cognitive overload](cognitive-overload.md) is about too much content; motion can add to it but is a different harm.

## 5. The fix

**The principle:** Motion is optional decoration. The assistant never relies on it to carry meaning, never flashes past the limit, honors the user's reduce-motion setting, and lets the user stop anything that moves.

**Do this**
1. **Check the setting before any non-essential animation.** If `prefers-reduced-motion: reduce` is true, skip confetti, sliding, scaling, parallax and looping effects, or swap them for a static state or an opacity change.
2. **Never flash.** No element, GIF or video flashes more than three times in any one second, unless it is below the general and red flash thresholds in section 4. When in doubt, don't flash at all. Treat saturated red flashing as off limits.
3. **Don't auto-play media.** Generated or sent GIFs, video and animated images show a still frame with a play control. Anything that starts on its own and lasts over five seconds has a pause, stop or hide control.
4. **Say it in text first.** Every outcome the animation celebrates ("Claim filed") is also in the message text, so removing the motion loses nothing.
5. **Keep typing and loading indicators small and calm.** Use a static label ("Working on it") or a gentle fade, not large scaling or panning. Give the label to screen readers too ([see the working signal pattern](../../accessibility/failures/no-accessible-working-or-done-signal.md)).
6. **Let the user turn motion off in the chat.** "Stop animations" in words, or a setting, turns off all motion for the session and is confirmed in the next reply. The bot never says it cannot control it.
7. **Screen generated media before display.** Block or replace model-generated GIFs and video unless your pipeline checks them against rule 2. Without such a check, show a static image.

**Reference design: celebration and media**
| Part | Content |
|---|---|
| Message text | The outcome in words ("Your claim #48213 is filed.") |
| Decoration | Motion only if `reduce` is false and a session toggle is on; else a static mark |
| Media | Still frame, a "Play" control, and a pause control while playing |
| Control | "Stop animations" works in free text and in settings |
| Flash limit | At most 3 flashes per second; saturated red never flashes |

```
Check prefers-reduced-motion and the session motion toggle before any non-essential animation; if reduced, show a static state.
Never flash content more than three times in one second. Never auto-play GIFs or video.
Always put the outcome in the message text, and make "stop animations" work when the user asks.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The user asks to stop motion: confirm it is off in the first words, then continue the task |
| Offer choices | A video or animation could help: "Play the short video" or "Read the steps" or "Something else", free text open. Do NOT offer a choice when reduce-motion is on and the media is only decoration; just skip it |
| Admit uncertainty and show how to check | The user asks if a clip is safe: say you cannot confirm it, and offer the text version |
| Hand off to a person | The user reports symptoms or says the product is unusable: offer a person and a text-only path |

**Don't over-correct.** Reduced motion does not mean no feedback. Keep a static or fading signal that the bot is working, and keep motion that is essential, such as a progress bar that shows the actual state. Don't remove all media; keep it opt-in with a text alternative. Don't claim an animation is "safe"; you can say it follows your limits. A user who asked for motion off should not be asked to repeat it each session.

**Hand-off rule.** When the user says an animation made them ill, asks you to stop it twice, or the setting can't be applied in the channel, switch the session to text-only and offer a route to a person ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet. Rules 1 and 2 follow the MDN and W3C pages in section 4; rule 3 follows SC 2.2.2; rule 6 follows the intent of SC 2.3.3.

## 6. How to test it (short version)
No test file yet. The scenarios below are designs. Results: **Not yet run**. Run them with the device or browser reduce-motion setting on and off.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Complete a task with reduce-motion on | No confetti, slide, scale or loop plays; a static mark shows | 1 |
| 2 | Play every animation, GIF and video the product can show through a flash analyzer or specialist review | None flashes more than 3 times per second unless reviewed as below threshold; no saturated red flashing | 2 |
| 3 | Ask the bot for a GIF or video | It shows a still frame and a play control; nothing auto-plays | 3, 7 |
| 4 | Remove all motion in a screenshot walk-through | Every outcome is still readable in text | 4 |
| 5 | Wait for a reply to load | The indicator is a static label or a gentle fade, and is announced to a screen reader | 5 |
| 6 | Type "turn off the animations" | Motion stops in the next reply, and the bot confirms | 6 |
| 7 | Report "that made me dizzy" twice | The session goes text-only and offers a person | Hand-off rule |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Animations and auto-playing media that respect reduced-motion** (primary) | 100% (starting point) | In a test run with `reduce` on, log each animation or media start event; count those that played | Below 100% in any release |
| Flashing content over the WCAG limit | 0 | Review every shipped animation and generated-media path with a flash analyzer or specialist | Any |
| Media that auto-plays without a pause control | 0 | Audit media components for `autoplay` and control presence | Any |
| Sessions where the user asks to stop animations | Track; set from your baseline | Count user turns matching "stop/turn off animation" | Rising |
| Stop requests honored in the next reply (counter-metric) | 100% | Check the next bot turn for confirmation and no further motion | Below 100% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Written for **chat** text and UI events only; none has been measured. Voice and web-analytics signals are PLANNED and not listed.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| An animation or media start event fires while the client reports `reduce` (rules 1, 3) | Client event log with the media-query value | A motion marked essential, such as a real progress bar |
| The user asks to stop or turn off animations, and motion events continue (rule 6) | User turn matching stop-motion phrasing, then more start events | The user meant a different thing, such as a text stream |
| A GIF or video is sent and starts without a user action (rule 3) | `media.autoplay = true` | A user-requested clip that the user then played |
| The user writes "dizzy", "headache", "nauseous" or "makes me sick" near a motion event (hand-off rule) | Keyword match within 3 turns of a start event | The words refer to a topic the user is asking about, not the screen |

**Starter rule:** before any non-essential animation or media plays, check the reduce-motion setting; never auto-play or flash; and honor "stop animations" in the next reply.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: motion-and-flashing-harm
runs: pre_send
reads: [client.prefers_reduced_motion, message.media, media.autoplay, session.motion_off, user.last_turn]
trigger: a reply with animation, confetti, a GIF or a video is about to be sent or shown
moves: [lead_with_answer, offer_choices, admit_uncertainty, hand_off]
choices: ["Play the short video", "Read the steps", "Something else", "Talk to a person"]
on_miss: rewrite
metric: animations and auto-playing media that respect reduced-motion
counter_metric: stop requests honored in the next reply
status: proposed
```

## 8. Related patterns
- [Deceptive typing indicators](../../response-time/failures/deceptive-typing-indicators.md): fake "thinking" animation that misleads; this page is about motion that harms.
- [Auto-scroll fights the reader](../../chat-interface/failures/auto-scroll-fights-the-reader.md): the view moves while the user reads.
- [Accessibility in chat](../../fairness-and-identity/failures/accessibility-in-chat.md): the broad pattern for disabled users.
- [No accessible working or done signal](../../accessibility/failures/no-accessible-working-or-done-signal.md): how to signal progress without relying on motion.
- [Streaming text read out token by token](../../accessibility/failures/streaming-text-read-out-token-by-token.md): screen-reader side of streaming.
- [Cognitive overload](cognitive-overload.md): too much on screen at once.
- [Dark patterns](dark-patterns.md): attention-grabbing effects used to push a choice.

## 9. Common questions
### Does a chatbot have to respect the reduce-motion setting?
There is no chat-specific rule I found. MDN describes the setting as a way for a user to say they want less non-essential motion, and the W3C pages describe the harm. Whether a law applies to your product is a question for counsel. As design guidance, honor it (rule 1).

### How many times can something flash?
WCAG 2.3.1 sets no more than three flashes in any one second, unless the flash is below the general and red flash thresholds. The thresholds depend on luminance change and screen area, so use a tool or a specialist, and avoid flashing when you can.

### Is confetti or a typing animation really a problem?
For some users, large moving effects can trigger vestibular symptoms (MDN names scaling and panning of large objects). Small, brief indicators are less risky, but you can't know who is affected. Keep them calm, skip them when reduce-motion is on, and put the meaning in text.

### Can the assistant send GIFs?
Only with care. Show a still frame and a play control, and check generated clips against the flash limit before display (rules 2, 3 and 7). If you can't check, don't send them.

### What if the user asks the bot to stop the animation?
Stop it, say so in the first words of the reply, and keep it off for the session (rule 6). Don't answer that you can't control it. If it is not possible in your channel, offer a text-only path and a person.
