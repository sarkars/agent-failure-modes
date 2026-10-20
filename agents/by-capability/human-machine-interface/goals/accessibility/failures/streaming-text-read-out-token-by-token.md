# Chatbot Screen Reader Announces Every Token: Streaming Text Read Out Token by Token

<!-- SEO
title: Chatbot Screen Reader Reads Every Token: Fix Streaming
description: When a chat reply streams into a live region, a screen reader can stutter through fragments. Announce a short status, then the full reply once it is complete.
search phrases:
- chatbot screen reader announces every token
- aria-live streaming chat
- screen reader reads streaming text word by word
- accessible streaming AI chat response
- aria-live polite chatbot response keeps repeating
- how to make an AI chat accessible to screen readers
- role="status" vs role="log" for chat messages
-->

**Frequency**: Common

## Issue: A screen reader stutters through fragments as a chat reply streams in, so a blind user hears broken pieces instead of the answer.

> **One line:** The reply is poured into a live region token by token, so the screen reader tries to speak every change; announce a short status while it streams, and the full reply once it is complete.

| | |
|---|---|
| **Channel** | Chat (a web chat widget read by a screen reader). Voice is planned, not written. |
| **Stakes** | Medium. The user can lose the answer; in a medical or money chat the stakes are higher. |
| **Who is affected** | People who use screen readers on a streaming chat |
| **Frequency** | Common, by practitioner account only. The sources say a plain `aria-live` wrapper around streamed text is a typical build; I found no measured count of how many chat products do it. |
| **Pattern ID** | streaming-text-read-out-token-by-token |
| **Family** | [Accessibility](../README.md) |
| **Goal** | People who use screen readers, keyboards, captions, relay services, or plain-language support can use every part of the agent. |
| **Primary metric** | Manual screen-reader test results (NVDA, JAWS, VoiceOver) on streamed replies. Starting point: every cell of your test matrix passes (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The model produces text; the page markup decides what a screen reader speaks. (Our judgment, not tested.) |
| **Also searched as** | screen reader reads chat word by word · aria-live chatbot · chatbot not accessible to blind users · streaming response accessibility · screen reader repeats chat message |

*This page is design guidance, not a conformance claim and not legal advice. Evidence is from practitioner write-ups and one standards document, not peer-reviewed studies. Screen readers differ; test with the ones your users use.*

## 1. In plain words
Chat replies often appear a few words at a time. If that text sits inside a live region, the screen reader may try to speak each change, so a blind user can hear fragments or repeats. The fix is to keep the streaming text out of the spoken channel, say one short status ("Generating a response"), and expose the whole reply once when it is done.

## 2. What it looks like
What the user hears, in a pharmacy refill chat, with the reply streamed into a live region. The exact stutter depends on the screen reader and browser; this is an illustration of the failure the sources describe, not a recording.

**Without the fix**
```
User: (types) Can I refill my lisinopril early? I leave for Phoenix on Friday.
Screen reader: "Yes"
Screen reader: "Yes you"
Screen reader: "Yes you can"
Screen reader: "Yes you can refill"   (keeps adding words; the user hears the start again and again)
Screen reader: (falls behind or drops words; the user cannot tell when the reply ended)
User: (types) Sorry, what did you say?
```

**With the fix**
```
User: (types) Can I refill my lisinopril early? I leave for Phoenix on Friday.
Screen reader: "Generating a response."
              (the text streams on screen; nothing else is spoken; focus stays in the input)
Screen reader: "Response complete. Yes. You can refill it up to 7 days early if your plan allows.
               Want me to check your plan?"
User: (types) Yes, check it.
```
The fixed version speaks two things: a status at the start and the finished reply once. The same words are on screen for sighted users.

## 3. Why it happens
- **Streamed text is written into a live region.** Each new token changes the region, and the region is how the page tells a screen reader to speak a change. Tian Pan's write-up says `aria-atomic="true"` makes it re-read the whole response on every token. MDN confirms that setting re-announces the whole region on each update, though not the streaming effect.
- **Streaming was built for the eyes only.** Teams test with the screen on, and automated checkers cannot judge a live stream. One practitioner source says no standard defines "accessible streaming" (a search-summary claim; see section 4).
- **The state of the reply is not announced.** The only cue is a blinking cursor or dots, which carry no text, so teams reach for the live region to fill the gap. The Chainlit pull request describes exactly this cursor.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| WCAG 2.2 SC 4.1.3 (Level AA) says status messages must be programmatically determinable through role or properties so assistive technology can present them without receiving focus. A status message gives information on the result of an action, a waiting state, progress, or errors. | [W3C, Understanding SC 4.1.3 Status Messages](https://w3c.github.io/wcag/understanding/status-messages.html). Opened and read. | A standard for status messages. It does not mention streamed AI replies, so applying it here is our reading. |
| The same page warns live regions carry "a risk of making an application too chatty" and recommends user testing to find the right level of feedback. It lists no numeric limit. | Same W3C page. Opened and read. | General guidance, not chat-specific. |
| MDN: use `polite` normally; `assertive` is for time-sensitive notices and "can be extremely annoying and disruptive". Establish the live region, empty, before updating it; the most reliable way is to include it in the initial markup. | [MDN, ARIA live regions](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions). Opened and read. | Reference documentation; MDN says behavior varies across browser and assistive technology combinations. |
| A practitioner write-up says that with `aria-atomic="true"` the screen reader re-reads the entire response on every token, and recommends short static status messages ("Generating response...", "Response ready"), announcing the reply once at completion, and not moving focus. It gives no measured update rate and no per-screen-reader results. | [Tian Pan, "When Streaming Tokens Meet the Screen Reader", June 29, 2026](https://tianpan.co/blog/2026-06-29-streaming-tokens-meet-the-screen-reader). Opened and read. | Single practitioner blog. I do not use its figures (such as "dozens of times per second" or alt-text percentages); it cites no source for them. |
| A developer tested a sample with VoiceOver and Chrome on macOS: "Generating a response" was announced once, the streaming body was not read, "Response complete" was announced once, and focus stayed in the input. He reports that shadcn/ui chat components held announcements during generation and then read them all at once after completion with the same setup. He also cites an OpenClaw issue where NVDA with Firefox reportedly announced responses token by token or chunk by chunk (reported, not tested by him). | [azukiazusa, "Accessible streaming chat UI", Aug 11, 2026](https://azukiazusa.dev/en/blog/accessible-streaming-chat-ui). Opened and read; page is machine-translated from Japanese. | One person's test on one screen reader. The OpenClaw report is secondhand; I could not find the issue itself. |
| A Chainlit pull request added a visually hidden `role="status"` region driven by the same loading value as the cursor, and `role="alert"` on error messages. It says wrapping streamed content in a live region "makes assistive technology re-read the partial message on every chunk". The author checked the DOM, not a screen reader. | [Chainlit pull request #3014](https://www.cubic.dev/pr/Chainlit/chainlit/pull/3014). Opened and read; closed and labeled stale; no exact date shown. | A proposed change in one open-source project, verified by DOM inspection only. |

**Public incident.** No public incident found for this failure as a dated, sourced event. Searches run: "aria-live streaming chatbot response screen reader announces every token"; "accessible AI chat streaming responses screen reader live region best practice"; "WCAG 2.2 Understanding 4.1.3 Status Messages"; "OpenClaw issue NVDA Firefox screen reader announces response token by token chunk". The reports above are developer write-ups and a code change, not an incident.

**What I could not verify.** I found no peer-reviewed or user-study evidence on how NVDA, JAWS, or VoiceOver treat streamed chat. Do not rely on any claim about a named screen reader; run the tests in section 6.

## 5. The fix

**The principle:** Keep the streaming text out of the spoken channel; announce a short status, then the full reply once.

**Do this**
1. **Put the status in its own region, in the page from the start.** One empty `role="status"` element with `aria-live="polite"`, in the initial markup, separate from the reply (MDN: establish the region before updating it).
2. **While the reply streams, the reply body is not a live region.** Mark the transcript so changes are not spoken (`aria-live="off"`); nothing from the stream goes into the status region.
3. **Announce "Generating a response" once per reply**, when streaming starts. No repeats and no per-token or per-sentence updates.
4. **Expose the complete reply in one update** when streaming ends. The final text is in the normal document, reachable by heading or arrow keys.
5. **Announce completion once.** For a reply under your length cap (starting point: 600 characters, tune), put the full reply text in the status region in a single write. For a longer reply, announce "Response complete" plus the length, and let the user read it in the transcript. Do not read very long replies aloud unprompted.
6. **Never move focus** when text arrives. Focus stays in the input box.
7. **Announce failure once, as a complete message.** "Reply failed. Your message is saved. Retry." Use `assertive` or `role="alert"` for failures only (see [generic error messages](../../errors-and-recovery/failures/generic-error-messages.md)). Say "saved" only if it is true.
8. **Test the live stream with the real screen readers**, not only the finished page (see section 6).

**Reference design: a markup and status-message design (one practitioner's sample, adapted; test it yourself)**
```html
<div id="messages" role="log" aria-live="off" aria-label="Chat history" tabindex="0"></div>
<div id="chat-status" class="sr-only" role="status" aria-live="polite" aria-atomic="true"></div>
```
| Moment | Status region text | Transcript |
|---|---|---|
| User sends | (empty) | Focus stays in input |
| Stream starts | "Generating a response." | Text appears visually; not spoken |
| Stream ends, short reply | "Response complete. [full reply]" | Final reply in the transcript |
| Stream ends, long reply | "Response complete. About 400 words." | Final reply in the transcript |
| Failure | "Reply failed. Your message is saved. Retry." | Error message, one write |

The azukiazusa sample clears the status text, then sets the new text after a short timeout (100 ms in the sample) so a repeated message registers as a change. Treat that as a starting point and test.

```
Do not write streamed text into any region a screen reader treats as live.
Announce "Generating a response" once. When the reply is done, place it in the page in one update and announce "Response complete".
Never move focus when text arrives.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The completed reply opens with the answer, so the first thing heard after "Response complete" is the answer. Do not use it when the bot is unsure what was asked. |
| Offer choices: 2-4 options plus "Something else", free text open | A long reply: "Short summary", "Read the full reply", "Something else". Do not offer them for a short reply, or in place of the reply itself. |
| Hand off to a person | The user says twice that they cannot read or hear the replies. Offer the answer by email or a person. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Do not go silent: a page that announces nothing leaves a blind user not knowing a reply is coming (the status in rule 3 matters). Do not announce every sentence "to be safe", which brings back the chatter W3C warns about. Do not remove streaming for sighted users; this fix changes only what is spoken. Do not use `assertive` for ordinary replies.

**Hand-off rule.** If the user says twice that the replies are unreadable or repeat, offer the answer by another route (email, text, phone) or a person ([when a bot should hand off](../../human-handoff/failures/escalates-too-early-or-too-late.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
Full test file: not written. Results: **Not yet run**. Run each test with NVDA, JAWS, and VoiceOver on the browsers your users have, and record results per pairing.

| # | Scenario | Rule | Pass if |
|---|---|---|---|
| 1 | Send a 150-word question and listen to the stream | 2, 3 | Status spoken once; no token fragments spoken during streaming |
| 2 | Same, then listen to the end | 4, 5 | Reply spoken or reachable once, complete, with "Response complete" |
| 3 | Inspect the page before the first message | 1 | Status region exists and is empty in the initial markup |
| 4 | Send a message and watch focus during the stream | 6 | Focus stays in the input from send to finish |
| 5 | Break the connection mid-reply | 7 | Failure spoken once, with what is saved and the next step |
| 6 | Reply longer than the length cap | 5 | Length announced; full text not read aloud unprompted |
| 7 | Send two messages in a row | 3, 5 | Each reply gets one start and one finish announcement; none dropped or doubled |
| 8 | Repeat tests 1-2 on every supported screen reader and browser | 8 | Each pairing has a recorded pass or fail |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Manual screen-reader test results (NVDA, JAWS, VoiceOver) on streamed replies** (primary) | Every matrix cell passes tests 1-8 | Run section 6 each release, per screen reader and browser; log pass or fail | Any failed cell in a release test |
| Spoken-region writes during a stream | 0 body writes; 1 status write | In a browser test, count DOM changes to live regions between stream start and end | Over 1 status write, or any body write |
| Replies with one start status and one completion announcement | 100% in tests | Count status writes per reply in the automated browser test | Below 100% |
| Focus moves while text arrives | 0 | Test script logs `document.activeElement` changes during streaming | Any |
| Screen-reader complaints about the chat | Track; set from baseline | Count support tickets or feedback that mention reading word by word or repeats | Rising two weeks in a row |
| Silent replies (counter-metric) | 0 | Replies that complete with no completion announcement in the test | Any |

### Detection signals (proposed, not yet calibrated)
All are for text chat. Voice signals are planned and not written. Do not try to detect screen-reader use in production; no source I opened says that is reliable, and it is a privacy risk. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| More than one status write, or any reply-body write, to a live region during a stream | Test-harness event: live-region writes per reply | A page that streams into a non-live element correctly |
| Stream-end event with no completion announcement event | Client event pair per reply | A telemetry gap |
| Next user turn asks to repeat ("what did you say", "say that again") after a streamed reply | User turn text after a completed reply | A user who was interrupted, or who wanted a recap |
| Support ticket or feedback text mentions a screen reader plus "reads", "repeats", or "stutters" | Tagged feedback | A different accessibility issue, such as an unreachable control |

**Starter rule:** the streamed reply is never written to a live region; announce "Generating a response" once, then the complete reply or "Response complete" once.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: streaming-text-read-out-token-by-token
runs: post_turn
reads: [reply.stream_start_ts, reply.stream_end_ts, live_region.writes, focus.changes, reply.length]
trigger: a reply finishes streaming
moves: [lead_with_answer, offer_choices, hand_off]
choices: ["Short summary", "Read the full reply", "Something else"]
on_miss: log
metric: manual screen-reader test results (NVDA, JAWS, VoiceOver) on streamed replies
counter_metric: silent replies
status: proposed
```

## 8. Related patterns
- [Streaming stalls](../../../../../cross-cutting/operations/goals/real-time-performance/failures/streaming-stalls.md): closest existing page. It is about text that pauses or arrives in bursts, a speed problem anyone sees. This page is about what a screen reader speaks, which can fail even when streaming is smooth. The "streaming that rewrites itself" case (RT-12) has only an example there; a corrected stream can also trigger repeated speech, so test it here.
- [Silent long-running work](../../response-time/failures/silent-long-running-work.md): showing status for long waits. This page covers how that status must be spoken.
- [Pacing mismatch](../../response-time/failures/pacing-mismatch.md): when text is shown. This page is about what is spoken.
- [Deceptive typing indicators](../../response-time/failures/deceptive-typing-indicators.md): a visual cue that may carry no text for a screen reader.
- Accessibility gaps in general (VI-04) and the "working or done" signal (AX-02) are planned pages; none exists yet. See the [visual modality](../../../modalities/visual/README.md).

## 9. Common questions
### Why does my chatbot's screen reader announce every token?
Streamed text is probably inside a live region, so each change is a spoken update. Keep the body out of any live region and use a separate status region (rules 1-2).

### Should I use aria-live polite or assertive for a chat reply?
Polite. MDN says assertive interrupts and should be used sparingly, for time-sensitive notices. Use assertive or `role="alert"` for failures only (rule 7).

### Do I need aria-busy?
Two practitioner sources say not to rely on it alone because support varies. I found no tested source that shows it fixes this, so test it with your screen readers if you add it.

### Is this a WCAG requirement?
SC 4.1.3 requires status messages to be exposed to assistive technology without focus. It does not mention streamed replies, and this page is not legal advice or a conformance claim. Ask your accessibility specialist how it applies to you.

### Does this work the same in NVDA, JAWS, and VoiceOver?
Unknown. The one tested result I found is VoiceOver with Chrome on one sample. Test each pairing yourself.

---
## Technical section

### T1. Solution architecture
```
stream start -> status region: "Generating a response."
token stream -> transcript element (aria-live off), no spoken updates
stream end   -> one DOM update of final text -> status region: "Response complete." (+ text if short)
error        -> one complete message -> alert
```
### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Status region in initial markup, empty | Page template | Test 3 |
| No streamed text in live regions | Chat component | Browser test counts live-region writes |
| Focus unchanged during stream | Chat component | Test 4 |

### T3. Evals
- **Dataset:** 10 prompts: short, long, list, link-heavy, error, and two back-to-back sends. Start there.
- **Judge rubric:** a human tester records what is spoken and when, per screen reader and browser.
- **Metrics and starting thresholds:** all cells pass; status writes per reply equal 1. Starting points to tune.
- **Release gate:** block a release when any section 6 test fails on a supported pairing.

### T5. Trade-offs
- A short status plus a late full reply makes blind users wait for the end while sighted users read as it streams. Consider a user setting for a settled reply, and test it.
- Upkeep: every chat library upgrade can change markup; rerun the matrix.

---
### Deep dive
- **Open question.** No peer-reviewed study on streamed chat and screen readers found. Testing with blind users would settle length caps and wording.
- **Modality notes.** Voice: PLANNED, not written.
- **References.** [W3C SC 4.1.3](https://w3c.github.io/wcag/understanding/status-messages.html) (opened); [MDN live regions](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions) (opened); [Tian Pan, 2026](https://tianpan.co/blog/2026-06-29-streaming-tokens-meet-the-screen-reader) (opened); [azukiazusa, 2026](https://azukiazusa.dev/en/blog/accessible-streaming-chat-ui) (opened); [Chainlit PR #3014](https://www.cubic.dev/pr/Chainlit/chainlit/pull/3014) (opened).
