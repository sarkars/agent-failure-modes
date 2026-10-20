# Chatbot Screen Reader Loading Status: No Accessible "Working" or "Done" Signal

<!-- SEO
title: Chatbot Screen Reader Loading Status: Announce Working and Done
description: A blind user can't tell if a chatbot is thinking, stuck, or finished. Put working and done in a status region that screen readers read, and test it.
search phrases:
- chatbot accessibility screen reader loading status
- aria-live chat widget
- screen reader doesn't announce chatbot response
- chatbot typing indicator accessibility
- role status vs role log chat messages
- wcag 4.1.3 status messages chatbot
- how to announce loading state to screen reader
-->

**Frequency**: Common

## Issue: A blind user can't tell whether the assistant is thinking, stuck, or finished, because the "working" and "done" cues exist only on screen.

> **One line:** The dots and spinner are pictures, so a screen-reader user hears nothing until the answer shows up, and may never learn that it did.

| | |
|---|---|
| **Channel** | Chat (a web chat widget read by a screen reader) is written. Voice is planned only; nothing here is voice-tested. |
| **Stakes** | Low to medium. Users resend, abandon, or give up on the assistant. Higher when the wait is for a payment or a claim. |
| **Who is affected** | People who use screen readers. The W3C page I opened also names a possible benefit for users with cognitive disabilities. |
| **Frequency** | Common in chat widgets that show animated dots. I found no count, so this is our judgment. |
| **Pattern ID** | no-accessible-working-or-done-signal |
| **Family** | [Accessibility](../README.md) |
| **Goal** | People who use screen readers, keyboards, captions, relay services, or plain-language support can use every part of the agent. |
| **Primary metric** | Status announcements present in the accessibility tree. Target: 100% (starting point to tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The status cue comes from the page markup, not the model. (Our judgment, not tested.) |
| **Also searched as** | chatbot silent for screen reader · aria-live chatbot · typing dots not read · chat widget accessibility · is the bot frozen blind user |

This is design guidance. It is not a conformance claim and not legal advice.

## 1. In plain words
Sighted users see dots or a spinner and know the assistant is working. A screen reader does not read an animation. If nothing is written into text the screen reader can reach, a blind user hears silence, then maybe a reply, and cannot tell whether the wait ended. The fix is a short text status ("Working on your request", "Reply ready") in a place assistive technology watches.

## 2. What it looks like
**Without the fix** (screen reader user, bank chat widget)
```
User:  (types, presses Enter) What is the fee for a wire transfer?
Bot:   (three animated dots, no text; the screen reader says nothing)
User:  (waits 20 seconds, listens to the page; still nothing)
User:  Hello? Are you there?
Bot:   (the first reply is now in the log, unannounced; a second reply follows)
```
**With the fix**
```
User:   What is the fee for a wire transfer?
Status: Working on your request.
Status: Still working. Checking the fee schedule.
Status: Reply ready.
Bot:    A domestic wire is $25 and an international wire is $45. Want the steps to send one?
User:   (reads the reply; focus stayed in the message box)
```
The fixed version puts working, a step change, and done into one status region. The dots are hidden from the accessibility tree because the text now says the same thing. (The fees are invented for the example.)

## 3. Why it happens
- **The cue is an animation.** Dots and spinners are drawn in CSS or SVG with no text, so the accessibility tree has nothing to read.
- **The live region is missing or late.** MDN says assistive technology will generally announce only dynamic changes, so a region added at the same moment as its text may stay silent.
- **Streaming has no end marker.** Text arrives in pieces and nobody writes a "finished" state, so the user cannot tell a pause from a stop.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| WCAG 2.2 SC 4.1.3 (Level AA): status messages must be "programmatically determined through role or properties" so assistive technology can present them without focus. A status message includes "the waiting state of an application" and "the progress of a process". | [W3C, Understanding SC 4.1.3](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html). Opened and read. | Whether a given chat widget must conform is a judgment for your accessibility lead. This page does not make it. |
| The same page lists techniques: `role=status` (ARIA22), `role=log` for sequential updates (ARIA23), and a live region for a progress bar (ARIA25). It notes that when a "busy" message disappears, non-sighted users may miss the change, so a non-visible message such as "system available" can help. | Same W3C page. Opened and read. | Techniques are examples, not the only way to pass. |
| MDN: `aria-live="polite"` speaks "whenever the user is idle"; assertive "will interrupt any announcement" and "should only be used sparingly". `role="status"` and `role="log"` are implicit live regions; add a redundant `aria-live="polite"` for compatibility. | [MDN, ARIA live regions](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions). Opened and read. | Reference documentation, not a test of any chat product. MDN says behavior varies by browser and assistive technology pairing. |
| MDN: "Establish the live region before updating its content. Start with an empty live region"; the most reliable way is to include it in the initial markup. | Same MDN page. Opened and read. | General advice. Test it in your own widget. |
| GOV.UK's Government Digital Service (9 Dec 2016) used live regions to tell users when an adviser is typing, and warned not to "overwhelm your user with too many notifications". VoiceOver for Safari interrupted the screen reader; NVDA on Firefox and IE11 queued the message. | [Vararu, GDS Accessibility blog](https://accessibility.blog.gov.uk/2016/12/09/patterns-for-accessible-webchats/). Opened and read. | Practitioner write-up from 2016 on human webchat, with old browser and screen reader versions. Do not assume today's behavior; test it. |
| Orange's accessibility guideline for chatbots says received messages appear on screen but "the screen reader does not automatically read them by default"; its fix is `aria-live="polite"` on the message container. | [Orange accessibility guidelines, chatbot](https://a11y-guidelines.orange.com/en/articles/chatbot/). Opened and read. | One company's guideline (practitioner). It does not cover typing or loading indicators. |

I found no controlled study of working or done signals for blind users of AI chat. I used no search-result summary of any other vendor blog in a rule.

**Public incident.** No public incident found. Searches run: "WCAG 2.2 Understanding Success Criterion 4.1.3 Status Messages"; "MDN ARIA live regions role=status aria-live polite"; "chatbot accessibility screen reader typing indicator aria-live chat widget".

## 5. The fix
**The principle:** Every working, step, stuck, failed, and done state has a text status in a live region, and the animation that shows it on screen is hidden from assistive technology.

**Do this**
1. **Put one status region in the page at load.** `role="status"` plus a redundant `aria-live="polite"`, empty, in the initial markup, not created on first send (MDN).
2. **Write "working" within 1 second of send.** Example: "Working on your request." The 1 second is a starting point to tune.
3. **Hide the dots and spinner from the accessibility tree.** Use `aria-hidden="true"`. Do not put `aria-live` on the animation.
4. **Announce a change in step, not every token.** Write a new status only when the step changes, and at most once every 15 seconds on long work (starting point). Never announce streamed text word by word.
5. **Write "done" when the reply is complete.** "Reply ready." Keep it in the region until the next send, so the end of the wait is not missed (the W3C page notes the disappearing-message gap).
6. **Say so when the wait is long or stuck.** At 30 seconds with no progress (starting point): "This is taking longer than usual." plus one next step (wait, retry, or reach a person).
7. **Put the reply in a log region, and do not move focus.** Use `role="log"` with a redundant `aria-live="polite"`. Focus stays in the message box.
8. **Keep one meaning on screen and in text.** The visible indicator and the status text name the same state.
9. **Reserve assertive for a failed send.** Use `role="alert"` or `aria-live="assertive"` only when the user's message was not sent and needs action now (MDN: use sparingly).
10. **Test with the screen readers your users have.** Record at least two screen reader and browser pairs per release. Behavior differs by pair (GDS), so the team must test it.

**Reference design: status and log regions**
```html
<div role="status" aria-live="polite" aria-atomic="true" id="chat-status"></div>
<div role="log" aria-live="polite" id="chat-log"></div>
<span class="typing-dots" aria-hidden="true"></span>
<!-- on send:  chat-status.textContent = "Working on your request."      -->
<!-- on step:  chat-status.textContent = "Still working. Checking fees." -->
<!-- on done:  append reply to chat-log; status = "Reply ready."         -->
<!-- on stuck: status = "This is taking longer than usual. Wait, or ..." -->
```
`aria-atomic="true"` makes the whole message read, not a changed fragment (MDN).

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The wait passes the stuck limit: say it is taking longer, and what the user can do. |
| Offer choices: 2-4 options plus "Something else", free text open | At the stuck limit: "Keep waiting", "Try again", "Talk to a person", "Something else". Do not offer them for ordinary waits under the limit; a status line is enough. |
| Hand off to a person | After two stuck or failed waits in one conversation. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Announcement spam is the opposite failure: a status per token, a "still working" every second, or assertive messages for ordinary waits. GDS warns against too many notifications and MDN calls assertive "extremely annoying and disruptive". Cap updates (rule 4) and track them (section 7). Do not add a status for sub-second replies.

**Hand-off rule.** After two stuck or failed waits, offer a person and pass the conversation so far, as in [cold transfer](../../human-handoff/failures/cold-transfer.md). Offer a route that works without sight (for example, chat with a person or a phone callback).

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
Results: **Not yet run.** Each test maps to a rule number.

| # | Scenario (rule) | Pass if |
|---|---|---|
| 1 | Load the page with no messages (1) | The status region and log exist in the accessibility tree, empty |
| 2 | Send a message (2) | Status text "working" appears within 1 second |
| 3 | Inspect the typing dots (3) | Dots are `aria-hidden`; no `aria-live` on them |
| 4 | A 40-second multi-step task (4) | Status changes on steps; at most one write per 15 seconds; no per-token writes |
| 5 | A reply completes (5, 7) | Status reads "done"; reply is in the log; focus did not move |
| 6 | A task passes 30 seconds with no progress (6) | A "taking longer" status with one next step appears |
| 7 | Send fails (9) | The alert is announced; the typed message is still in the box |
| 8 | Run tests 2-6 with two screen reader and browser pairs (10) | Each state is spoken, or the differences are recorded |
| 9 | Compare the visible indicator with the status text (8) | Same state named in both |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Status announcements present in the accessibility tree** (primary) | 100% | Scripted runs per release: for each state in tests 2-6, read the accessibility tree; count states whose expected text is present, over states expected | Below 100% on any release |
| Waits over 10 seconds with a status write | Over 95% | Client log of status-region writes per turn, joined to turn start and end times | Below 90% |
| Completed turns with a "done" write | 100% | Log the write at reply completion against completed turns | Below 98% |
| Status writes per 15 seconds of wait (counter-metric) | 1 or fewer | Count writes per turn from the client log | Over 2 |
| Assertive messages that are not failed sends (counter-metric) | 0 | Count `role=alert` writes and their reasons | Any |
| Screen reader pairs tested per release | 2 or more | Release checklist record | Fewer than 2 |

A DOM write is not proof that a screen reader spoke it. The primary metric checks the tree; spoken output needs test 8.

### Detection signals (proposed, not yet calibrated)
Signals are for text chat. Voice signals are planned and not defined here.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Typing indicator shown with no status-region write | Client event: indicator on, status writes 0 | A reply under 1 second that needed no status |
| Status region first created after the first send | Region creation time later than first send time | A lazy-loaded widget whose first send is blocked until it loads |
| Reply appended with no "done" write | Reply event with no matching status write | A reply that arrived with an error state already announced |
| Wait over 10 seconds, no status change | Send-to-reply time, status writes 0 | A background task with a status shown elsewhere in the page |
| More than 2 status writes in 15 seconds | Status write timestamps | A fast multi-step task with real step changes |

**Starter rule:** every send writes a "working" status within 1 second and a "done" status at completion, in a live region present at page load.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: no-accessible-working-or-done-signal
runs: post_turn
reads: [turn.send_ts, turn.reply_ts, ui.status_region_writes, ui.indicator_shown, turn.error]
trigger: the wait passes the stuck limit with no progress
moves: [admit_uncertainty, offer_choices, hand_off]
choices: ["Keep waiting", "Try again", "Talk to a person", "Something else"]
on_miss: log
metric: status announcements present in the accessibility tree
counter_metric: status writes per 15 seconds of wait
status: proposed
```

## 8. Related patterns
- [Silent long-running work](../../response-time/failures/silent-long-running-work.md): no status at all, for anyone. This page covers a status that exists on screen but not in text a screen reader reads.
- [Deceptive typing indicators](../../response-time/failures/deceptive-typing-indicators.md): dots shown to look human. This page asks that real dots have a text equivalent.
- [Silent failure and timeout](../../response-time/failures/silent-failure-and-timeout.md): every failure needs a visible end state. This page adds that it must also be text.
- [Generic error messages](../../errors-and-recovery/failures/generic-error-messages.md): what to say when it fails.
- [Cold transfer](../../human-handoff/failures/cold-transfer.md): what to pass on to a person.

## 9. Common questions
### How do I make a chatbot loading state accessible to screen readers?
Put an empty `role="status"` region in the page at load, write short text into it when work starts, changes step, and finishes, and hide the animated dots. See [the fix](#5-the-fix).

### Should I use aria-live or role=status for a chat widget?
Use `role="status"` for working and done, and `role="log"` for the message list. MDN says both are implicit live regions and suggests a redundant `aria-live="polite"`.

### Does WCAG require a chatbot to announce that it is working?
SC 4.1.3 covers status messages, which include waiting state and progress, so it is relevant. Whether your widget must conform is for your accessibility lead or counsel to decide. This page is not legal advice.

### Will every screen reader read the status the same way?
Not necessarily. GDS saw VoiceOver interrupt and NVDA queue in 2016, and MDN says behavior varies by pair. I found no current test data, so test your own widget.

### Should the status announce every streamed word?
No. Announce the start, a change in step, and the finish (rule 4).

---
## Technical section

### T1. Solution architecture
```
client send -> write "working" (1 s) -> step events -> throttle (1 per 15 s) -> status region
reply complete -> append to log region -> write "done" -> log all writes with timestamps
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Region exists at load (1) | Page template | Test 1 on every release |
| Dots are `aria-hidden` (3) | Widget component | DOM test (test 3) |
| Throttle on status writes (4) | Status writer function | Test 4 |
| Focus does not move on reply (7) | Reply renderer | Test 5 |

### T3. Evals
- **Dataset:** 5 scripted conversations (fast reply, 40-second task, stuck task, failed send, two quick sends in a row). Add real ones after review.
- **Judge rubric:** a human reviewer with a screen reader notes, per state, spoken or not spoken, and whether the order was clear.
- **Metrics and starting thresholds:** the section 7 table; starting points.
- **Release gate:** block a release if the primary metric is under 100% or fewer than two pairs were tested.
