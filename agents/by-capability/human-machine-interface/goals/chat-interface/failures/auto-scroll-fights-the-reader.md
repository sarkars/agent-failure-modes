# Chat Auto-Scroll Jumps to the Bottom While Streaming: Auto-Scroll Fights the Reader

<!-- SEO
title: Chat Auto-Scroll Jumps While Streaming: Stick to Bottom Fix
description: A streaming chat reply yanks the view to the bottom so people can't read the start. Follow new text only while the reader is at the bottom; add "Jump to latest".
search phrases:
- chat auto scroll streaming
- stick to bottom scroll chat
- chat scroll jumps to bottom while typing response
- stop auto scroll when user scrolls up
- chat window auto-scrolls even when I scroll up
- react chat scroll to bottom only if at bottom
- jump to latest message button chat
-->

**Frequency**: Common

## Issue: While a chat reply streams in, the window keeps snapping to the bottom, so a person who scrolls up to read the start of the reply, or an earlier message, is pulled away from it on every new chunk.

> **One line:** The chat window scrolls to the newest text on every update, even after the person scrolls up to read; the fix is to follow new text only while the person is already at the bottom, stop the moment they scroll up, and show a "Jump to latest" button to come back.

| | |
|---|---|
| **Channel** | Chat (web, desktop, and in-app chat windows). Voice has no scroll position; not applicable. |
| **Stakes** | Low to medium. Usually annoyance; higher when the part the person is trying to read is a warning, a step order, or the question they asked. |
| **Who is affected** | Sighted readers of long streamed replies, most of all people who read slower than the text streams or who need to check an earlier message mid-reply |
| **Frequency** | Common, from public bug reports and feature requests across several chat products (anecdotal; see section 4). I found no count of how many chat products do this. |
| **Pattern ID** | auto-scroll-fights-the-reader |
| **Family** | [Chat interface](../README.md) |
| **Goal** | The chat window itself works: messages arrive, drafts and attachments are kept, history is findable, and nothing is silently lost. |
| **Primary metric** | Reports of scroll jumping; scroll-up events during streaming that were overridden. Starting target: 0 overridden scroll-ups in release tests and under 1 per 1,000 streamed replies in production (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The model only produces text; the chat window's scroll code decides where the view goes. (Our judgment, not tested.) |
| **Also searched as** | chat keeps scrolling to bottom · can't scroll up while AI is typing · ChatGPT-style scroll behavior · auto-scroll pause on scroll up · scroll anchoring chat · new messages button |

## 1. In plain words
A long reply appears a few words at a time. The window chases the newest word, so the top of the reply slides out of view before the person has read it. If they scroll up to catch it, the next chunk drags them back down. The fix is the "stick to bottom" rule that terminals and chat apps use: follow only while the person is at the bottom, leave the view alone once they scroll away, and give them one button to catch up.

## 2. What it looks like
A homeowner in Columbus, Ohio, asks a home-improvement store's chat how to replace a garbage disposal. The reply is about 40 lines, with a "turn off the breaker first" warning in the opening lines. Timelines show what she sees and does.

**Without the fix**
```
0:00  She sends: "How do I replace a 1/2 hp garbage disposal myself?"
0:02  Reply starts streaming. Line 1 says to switch off the breaker first.
0:05  Reply passes the bottom of the screen; the window scrolls down with it.
0:06  She scrolls up to reread the safety step.
0:06  Next chunk arrives; the window snaps back to the bottom.
0:09  She scrolls up again; snapped down again. She gives up and waits.
0:30  Reply ends. She is at the parts list at the bottom, never saw the warning
      again, and types: "wait, what was the first step?"
```

**With the fix**
```
0:00  She sends: "How do I replace a 1/2 hp garbage disposal myself?"
0:02  Reply starts streaming; the window follows because she is at the bottom.
0:06  She scrolls up to reread the safety step. Following stops at once.
0:06  A "Jump to latest" button appears above the input box. The view stays put.
0:20  She finishes the safety section while the rest keeps streaming below.
0:21  She taps "Jump to latest"; the view goes to the newest text and follows again.
0:30  Reply ends. She asks a follow-up about the dishwasher hose, not a repeat.
```
Same reply, same speed. The fixed window moves only when she is at the bottom or asks to go there (rules 1-4).

## 3. Why it happens
- **The code scrolls to the bottom on every chunk, unconditionally.** A "set scroll to the end after each update" line works for short replies and is never revisited. One bug report describes exactly this: the window "force-scrolls to the bottom on every update" even when the user has scrolled up (GitHub #53382).
- **The window cannot tell the person's scroll from its own.** Scroll events fire for programmatic scrolls and layout changes too, so an "is the user at the bottom?" check driven by scroll events alone can be fooled. MDN notes that when a page misbehaves with scroll anchoring, a scroll listener is often "not handling the extra scrolling" the browser adds.
- **Follow-the-stream was designed for replies shorter than the screen.** Agent output and long answers outgrow the viewport, so following the newest line pushes the start of the reply off screen. A Cursor forum post describes ending at the bottom of every reply and having to scroll up to read it from the start.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A reporter says the Claude Code VS Code extension panel was "locked to auto-scroll to the bottom" during generation, so users could not scroll up to review earlier messages; workarounds were to stop generation, wait it out, or copy text out. Opened Nov 13, 2025; closed as not planned after inactivity; commenters said a later extension version fixed it. | [GitHub, anthropics/claude-code issue #11578](https://github.com/anthropics/claude-code/issues/11578). Opened and read. | One product's bug report; anecdotal. Fix reported by users, not documented by the maintainer. |
| A reporter says the Claude Code Desktop app on Windows yanks the view "back down on every new chunk", even when scrolled to the top, and asks for "sticky bottom" behavior plus an optional "jump to bottom" button. The report says the same fix had shipped for the VS Code extension (issue #11092). Opened Apr 25, 2026; closed as not planned Jun 3, 2026. | [GitHub, anthropics/claude-code issue #53382](https://github.com/anthropics/claude-code/issues/53382). Opened and read. | Anecdotal; shows the failure can regress in a second client of the same product. I did not open #11092 itself. |
| A user asks Cursor to anchor the view at the top of a new reply, or to auto-scroll only when already at the bottom with a "new content below" indicator, or to restore an auto-scroll toggle the post says was removed in Cursor 2.0. Posted June 9, 2026; later replies from other users report the same problem; no staff reply in the thread I read. | [Cursor forum thread](https://forum.cursor.com/t/top-anchored-reading-for-chat-responses-or-opt-out-of-auto-scroll-to-bottom/162811). Opened and read. | User request, anecdotal. Shows two fix designs people ask for. |
| Microsoft's SimpleChat release notes say new streaming content "pulled the viewport down even when you had deliberately scrolled up", and the fix keeps the view where the user leaves it and shows a floating scroll-to-latest button. | [SimpleChat release note, v0.261.001](https://microsoft.github.io/simplechat/latest-release/release-260-chat-scroll-508/). Opened and read. | Vendor release note for one open-source app; no date on the page beyond "© 2026"; no threshold given. |
| MUI's chat component pauses auto-scroll when the user is more than a buffer away from the bottom (default 150 px), resumes inside it, always scrolls on send, shows a scroll-to-bottom button with an unseen-message badge, and says prepending history "never causes a scroll jump". | [MUI X Chat, Scrolling](https://mui.com/x/react-chat/behavior/scrolling/). Opened and read. | Vendor library documentation; describes its design, not user-tested results. The 150 px is one library's default, not a researched value. |
| Browser scroll anchoring "adjusts the scroll position to compensate for the changes outside of the viewport", so the point the user is looking at stays in view. It is on by default; `overflow-anchor: none` opts out, and a descendant of an opted-out area "cannot be opted back in". | [MDN, Scroll anchoring](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll_anchoring/Scroll_anchoring) and [MDN, overflow-anchor](https://developer.mozilla.org/en-US/docs/Web/CSS/overflow-anchor). Opened and read. | Reference docs. MDN lists `overflow-anchor` as "Baseline 2026, Newly available" (since September 2026), so older browsers may lack it. MDN does not describe chat or bottom-pinned lists. |

**Public incident.** No dated incident with measured harm found; the evidence is bug reports and release notes. **What I could not open:** a Medium write-up on telling wheel input from layout-driven scroll events returned HTTP 403; I read it only through a search summary, so it is unverified and kept out of the fix. I found no user study that measures reading loss from scroll jumping.

## 5. The fix

**The principle:** The window follows new text only while the person is at the bottom; once they scroll away, only they move the view.

**Do this**
1. **Keep one `following` flag per chat window.** It is true when a reply starts if the person is within the bottom threshold (starting point: 150 px, MUI's default; tune).
2. **Turn following off on the first user scroll up**, from wheel, touch, keyboard (Page Up, arrow keys, Home), or scrollbar drag, as soon as the view is farther than the threshold from the bottom.
3. **While following is off, streamed content never changes the scroll position.** No `scrollTop`, `scrollIntoView`, or "scroll to end" call runs because a chunk arrived.
4. **Show a "Jump to latest" button** whenever following is off and there is content below the view. One click or Enter scrolls to the end and turns following on. It is a real `<button>`, reachable by keyboard, and does not take focus from the input on its own.
5. **Turn following back on only by the person's action:** scrolling back within the threshold, clicking "Jump to latest", or sending a new message.
6. **On send, show the person's own message.** Scrolling to the new message on send is expected and is not an override (MUI does this always).
7. **Tag your own scrolls.** Programmatic scrolls set a short-lived flag so the scroll handler does not read them as the person scrolling; only real input events change `following`.
8. **Keep browser scroll anchoring on for the message list.** Do not set `overflow-anchor: none` on the page or list to fix a jump; MDN says descendants cannot opt back in, and anchoring is what keeps the view still when content above changes (for example, loading older history).
9. **Optional, test with users: anchor long replies at their start.** When a reply grows taller than the view, stop following once the reply's first line reaches the top of the window, so the person reads from the start (Cursor forum Option A). Show "Jump to latest" as in rule 4.
10. **Log the client events** in the reference design so the primary metric can be computed.

**Reference design: decision table and client events**
| Event | Following on | Following off |
|---|---|---|
| Chunk arrives | Scroll to end (tagged) | Do nothing to scroll; show "Jump to latest" |
| User scrolls up past threshold | Turn following off; show button | Nothing |
| User scrolls back within threshold | Nothing | Turn following on; hide button |
| User clicks "Jump to latest" | (hidden) | Scroll to end; turn following on |
| User sends a message | Scroll to own message; following on | Same |
| Older history loads above | Keep view (scroll anchoring) | Keep view |

```
events: reply.stream_start, reply.chunk, reply.stream_end,
        scroll.user {direction, distance_from_bottom, input: wheel|touch|key|drag},
        scroll.programmatic {reason: chunk|send|jump},
        jump_to_latest.shown, jump_to_latest.click, message.send
overridden scroll-up = scroll.user up (following turned off) followed by
        scroll.programmatic reason=chunk before the next scroll.user down,
        jump_to_latest.click, or message.send
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); this is a UI pattern, so most moves do not apply)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The reply opens with its answer and any safety step, so the lines most at risk of scrolling away carry the point. Do not use it when the bot is unsure what was asked. |
| Offer choices | Does not apply. "Jump to latest" is one control, not a menu; do not replace it with options. |
| Ask one clarifying question, Admit uncertainty, Hand off to a person | Do not apply; the failure is in the window, not the conversation. |

**Don't over-correct.** Do not stop following for everyone: a person who stays at the bottom should see new text without touching anything (counter-metric in section 7). Do not turn following off on layout-driven scroll events, images loading, or code blocks expanding; only user input counts (rule 7). Do not remove streaming or hide the reply until it ends. Do not make "Jump to latest" steal focus or move the view by itself.

**Hand-off rule.** No person hand-off for the chat itself. If a user writes that the page "keeps jumping" or "won't let me scroll", the bot says scrolling up pauses following and the button returns to the latest text, and the product files the report with that session's client scroll events to the chat-window bug queue.

**Framework used:** none yet.

## 6. How to test it (short version)
Full test file: not written. Results: **Not yet run**. Run in a browser automation harness at desktop and phone widths, with a reply at least three screens long.

| # | Scenario | Rule | Pass if |
|---|---|---|---|
| 1 | Stay at the bottom while a long reply streams | 1, 3 | View follows to the end with no user input |
| 2 | Scroll up by mouse wheel mid-stream | 2, 3 | No programmatic scroll for the rest of the stream; view stays put |
| 3 | Same, by touch swipe, Page Up, and scrollbar drag | 2 | Each input turns following off |
| 4 | Scroll up, then click "Jump to latest" | 4, 5 | Button visible while off; click goes to end and following resumes |
| 5 | Scroll up, then scroll back to the bottom by hand | 5 | Following resumes; button hides |
| 6 | Scroll up, then send a new message | 5, 6 | View shows the new message; following on |
| 7 | An image or code block expands while at the bottom | 7 | Following stays on; not counted as a user scroll |
| 8 | Load older history while reading mid-thread | 8 | Visible message stays in place |
| 9 | Tab to "Jump to latest" and press Enter | 4 | Reachable by keyboard; focus not moved before the press |
| 10 | Reply taller than the view, with rule 9 enabled | 9 | Reply's first line stays at the top of the view |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given. All need client instrumentation in the chat window.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Reports of scroll jumping; scroll-up events during streaming that were overridden** (primary) | 0 overridden in release tests; under 1 per 1,000 streamed replies in production | Overridden scroll-ups from the client event definition in section 5; tag feedback and tickets that mention scroll or jumping | Any in release tests; production rate rising two weeks in a row; any new report cluster after a release |
| "Jump to latest" shown when needed | 100% of streams where following turned off and content arrived below | `jump_to_latest.shown` after following off and a later `reply.chunk` | Below 100% in tests |
| Repeat-what-you-said turns after long replies | Track; set from baseline | Next user turn asks for the first step or a repeat after a reply over one screen | Rising after a release |
| Lost follow (counter-metric) | 0 | Streams where the user made no scroll input but following turned off | Any in tests |

### Detection signals (proposed, not yet calibrated)
Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published. All are chat client events; voice is not applicable.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| `scroll.user` up during a stream, then `scroll.programmatic reason=chunk` before any user scroll down, jump click, or send | Client scroll events per reply | A send-triggered scroll mislabeled as `chunk` (check the reason field) |
| Three or more `scroll.user` up events in one stream | Client scroll events per reply | A person skimming quickly, not fighting the window |
| Stop-generation click within a few seconds of a scroll up (the workaround in #11578) | Client stop event after `scroll.user` | The person stopped because the answer was wrong |
| Feedback or chat text with "scroll" plus "jump", "keeps", or "won't let me" | Tagged feedback, user turn text | A complaint about scrolling inside a code block or another app |
| Following turned off with no user input event | Client follow-state change with no preceding `scroll.user` | Telemetry gap or dropped input event |

**Starter rule:** while following is off, streamed content never changes the scroll position.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: auto-scroll-fights-the-reader
runs: post_turn
reads: [reply.stream_start, reply.chunk, reply.stream_end, scroll.user, scroll.programmatic, jump_to_latest.shown, jump_to_latest.click, message.send]
trigger: a reply finishes streaming after the user scrolled up during it
moves: [lead_with_answer]
choices: none
on_miss: log
metric: reports of scroll jumping; scroll-up events during streaming that were overridden
counter_metric: lost follow
status: proposed
```

## 8. Related patterns
- [Streaming text read out token by token](../../accessibility/failures/streaming-text-read-out-token-by-token.md): closest existing page. It covers what a screen reader speaks while a reply streams. This page covers the visual scroll position for sighted readers; both can fail in the same widget, and fixing one does not fix the other.
- [Streaming stalls](../../../../../cross-cutting/operations/goals/real-time-performance/failures/streaming-stalls.md): text that pauses or bursts. Bursty chunks make jumping worse, but smooth streaming still jumps without this fix.
- [Pacing mismatch](../../response-time/failures/pacing-mismatch.md): when and how fast text is shown, not where the view goes.
- [Lost drafts and failed sends](lost-drafts-and-failed-sends.md) and [silent attachment failures](silent-attachment-failures.md): other chat-window failures in this family.

## 9. Common questions
### How do I stop a chat from auto-scrolling when the user scrolls up?
Keep a `following` flag, turn it off on the first real user scroll away from the bottom, and skip every chunk-driven scroll while it is off (rules 1-3). Turn it back on only by the user's action (rule 5).

### How close to the bottom counts as "at the bottom"?
There is no standard number. MUI's chat uses 150 px by default; treat that as a starting point and tune on phones and desktops.

### Does CSS `overflow-anchor` fix this?
Not by itself. Scroll anchoring keeps the view steady when content outside it changes, which helps when older messages load above. The jump here usually comes from your own code scrolling to the end, so fix that logic and leave anchoring on (rule 8).

### Should the chat show the top of a long reply instead of following it?
Some users ask for that (Cursor forum Option A). It is rule 9, marked optional: test it with your users, and keep "Jump to latest" available.

---
## Technical section

### T1. Solution architecture
```
onUserInput(wheel|touch|key|drag):  // real input only
    if distanceFromBottom() > THRESHOLD: following = false; showJump()
    else: following = true; hideJump()
onChunk():
    render(chunk)
    if following: programmaticScrollToEnd(reason="chunk")   // sets ignoreNextScroll
    else: showJump()
onJumpClick() / onSend():
    programmaticScrollToEnd(reason="jump" | "send"); following = true; hideJump()
onScroll():
    if ignoreNextScroll: ignoreNextScroll = false; return   // our own scroll
```
THRESHOLD is a starting point (150 px, one library's default). Rule 9 adds: `if following and replyTop() <= viewTop(): following = false; showJump()`.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No chunk-driven scroll while following is off | Chat list component | Tests 2-3; overridden scroll-up count |
| Only real input changes `following` | Scroll handler | Test 7; lost-follow counter-metric |
| Anchoring left on for the list | Stylesheet | Lint for `overflow-anchor: none` on the list or its ancestors |

### T3. Evals
- **Dataset:** 10 scripted streams: short, three screens long, with images, with code blocks, and back-to-back sends; each run with wheel, touch, keyboard, and scrollbar input.
- **Judge rubric:** the harness reads the client event log; no human judge needed except for rule 9 reading tests.
- **Metrics and starting thresholds:** overridden scroll-ups 0; lost follow 0. Starting points.
- **Release gate:** block a release if any test in section 6 fails on a supported browser and width.

### T5. Trade-offs
- Input-event tracking adds code per input type; missing one (for example, scrollbar drag) brings the bug back for those users.
- Each new client (web, desktop, extension) needs the same tests; the GitHub reports show one client can regress while another is fixed.
