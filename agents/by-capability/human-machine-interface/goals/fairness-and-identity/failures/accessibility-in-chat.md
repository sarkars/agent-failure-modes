# How to Make an AI Chatbot Accessible (Screen Reader, Keyboard, Zoom, Speech Input): Accessibility in Chat

<!-- SEO
title: How to Make an AI Chatbot Accessible: Chat-Wide Checklist
description: A chatbot can pass each widget check and still fail users of screen readers, zoom, speech input, or switches. A chat-wide test plan and the gaps the single-barrier pages miss.
search phrases:
- how to make an ai chatbot accessible
- chatbot widget accessibility wcag
- is my chatbot screen reader accessible
- accessible chatbot best practices
- chatbot accessibility testing checklist
- ai chat interface accessibility keyboard screen reader
- chatbot accessibility for low vision users
-->

**Frequency**: Common

## Issue: A chatbot can pass each single accessibility check and still leave people who use screen readers, zoom, speech input, or plain-language support unable to finish the task; the fix is to test whole journeys with those users and close the gaps in replies that component checks miss.

> **One line:** The chat window may be accessible part by part, but the person still can't finish the task.

> **Read this first.** This page is design guidance for testing your own product. It is not legal, clinical, or professional advice, and it has not been reviewed by an accessibility specialist or a lawyer. Have one review it before you rely on it. I cite the W3C's WCAG success criteria only as a standard I opened. I opened no statute, regulation, or case, so I make no claim about which laws apply to your product.

| | |
|---|---|
| **Channel** | Written for **chat** (text). Voice, phone, and web-signal checks are PLANNED; the [voice-only flows](../../accessibility/failures/voice-only-flows-with-no-text-alternative.md) page covers voice today. |
| **Stakes** | Any. High when the task is a bill, a claim, a medication, or an account. |
| **Who is affected** | People with vision, hearing, motor, speech, or cognitive needs who use assistive technology (AT) or plain-language support |
| **Frequency** | Common. One vendor-run test of 30 AI tools found 80% fell short for a blind screen-reader user; one tester only (section 4). No count for support chatbots. |
| **Pattern ID** | accessibility-in-chat |
| **Family** | [Fairness and identity](../README.md); detail pages sit in the [accessibility family](../../accessibility/README.md) |
| **Goal** | Everyone can complete the task in chat. (The catalog's wording. The fairness family README's goal is about dialect and name, so it needs a line for this row.) |
| **Primary metric** | Task-completion parity for AT users: their completion rate divided by the baseline rate on the same journeys. Target 0.9 or higher (a starting point, our heuristic). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Access depends on the widget, the formatting of replies, and how the product is tested, which a better model does not change. (Our judgment, not tested.) |
| **Also searched as** | chatbot WCAG compliance · screen reader chatbot · accessible chat widget · chatbot for blind users · chatbot low vision zoom · chatbot a11y testing |

## 1. In plain words
Accessibility problems in chat come from many small choices: a button, a status line, a table, an emoji, a timer. Each has its own page in this library. This page is the chat-wide view. It says to test whole tasks, end to end, with people who use assistive technology, and it fills four gaps the single-barrier pages leave open: images and charts in replies, emoji and formatting, zoom and touch targets, and speech-input control names.

**What this page adds, and what it does not repeat**
| Already covered on its own page | Page |
|---|---|
| Screen reader stutters through a streaming reply | [Streaming text read out token by token](../../accessibility/failures/streaming-text-read-out-token-by-token.md) |
| No spoken "working" or "done" | [No accessible working or done signal](../../accessibility/failures/no-accessible-working-or-done-signal.md) |
| Chips, copy, stop, thumbs not reachable by Tab | [Controls unreachable by keyboard](../../accessibility/failures/controls-unreachable-by-keyboard.md) |
| Idle timer ends the chat too soon | [Timeouts too short for assistive technology](../../accessibility/failures/timeouts-too-short-for-assistive-technology.md) |
| Idioms, long sentences, shifting terms | [Language that is hard for people with cognitive disabilities](../../accessibility/failures/language-that-is-hard-for-people-with-cognitive-disabilities.md) |
| CAPTCHA or voice check as the only way in | [Identity checks that exclude disabled users](../../accessibility/failures/identity-checks-that-exclude-disabled-users.md) |
| Audio or video with no or wrong text | [Missing or wrong captions and transcripts](../../accessibility/failures/missing-or-wrong-captions-and-transcripts.md) |
| Phone or voice with no text path | [Voice-only flows with no text alternative](../../accessibility/failures/voice-only-flows-with-no-text-alternative.md) |

**New here:** (1) a journey-by-need test matrix and one parity metric across all barriers; (2) text versions of images, charts, and tables in replies; (3) emoji and decorative formatting; (4) zoom, reflow, and target size; (5) control names for speech input; (6) a way to ask for another format; (7) a barrier-report route.

## 2. What it looks like
**Without the fix**
```
User: I use a screen reader. When are my last three refills due?
Bot:  Here you go! 🎉💊✅
      [image: refill calendar]
      | Drug | Due |  (a table of 14 rows)
      Tap the green button to reorder.
User: What green button? I can't see a calendar.
```
**With the fix**
```
User: I use a screen reader. When are my last three refills due?
Bot:  Your next three refills: lisinopril, May 3; metformin, May 9; atorvastatin, May 20.
      I can send the full list as plain text, or as short steps. Which do you want?
      [Plain text] [Short steps] [Talk to a person] [Something else]
User: Short steps.
Bot:  Step 1: Select the button labeled "Reorder lisinopril". (Stays in this format for the rest of the chat.)
```
The fixed reply puts the answer first, has no image or emoji, names the control by its visible label, and offers formats. The user never has to describe their need again.

## 3. Why it happens
These are our reading of the pattern.
- **Checks run per component.** A team tests the launcher, the status region, and the Tab order one at a time. Nobody tries the whole task with a screen reader, zoom, or speech input.
- **Replies are free-form generated text.** The model can add an image, chart, table, or emoji row that no widget rule anticipated.
- **No access-need signal or route.** The product has no way for users to ask for another format or report a barrier, so the team never hears about the failure.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| One blind tester with a screen reader and keyboard scored 30 AI tools on 10 tasks (sign in, send a prompt, read the response, copy it, stop or regenerate, and others). The report says "80% of the AI tools we tested fell short of basic accessibility for a blind screen reader user." Six scored A, 13 B-C, 11 D-F. | [AccessibilityChecker.org report, Sept. 2026](https://www.accessibilitychecker.org/ai-accessibility-study-2026/). Opened and read. | Published by a company that sells WCAG audits. One tester, one screen reader, one browser; a friction score, not a WCAG audit; free tiers; excludes low vision, cognitive, speech input. Treat as indicative. |
| SC 1.1.1 (Level A): non-text content needs "a text alternative that serves the equivalent purpose." For charts it allows short and long text, and the long one should give the chart type and a high-level summary of the data. | [W3C, *Understanding SC 1.1.1*](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html). Opened and read. | A standard for web content; it does not say how often chat replies miss it. |
| SC 1.4.10 Reflow (Level AA): content works "without scrolling in two dimensions" at a width of 320 CSS pixels, except parts that need two-dimensional layout (such as data tables). | [W3C, *Understanding SC 1.4.10*](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html). Opened and read. | A standard; no chat-specific data. |
| SC 2.5.8 Target Size (Minimum) (Level AA): pointer targets are at least 24 by 24 CSS pixels unless spacing, an equivalent control, or another exception applies. It helps people with tremors, one-handed use, and limited fine motor control. | [W3C, *Understanding SC 2.5.8*](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html). Opened and read. | A standard; chips and icon buttons are my application of it. |
| SC 2.5.3 Label in Name (Level A): a control's accessible name contains its visible text, so speech-input users can "navigate by speaking the visible text labels." | [W3C, *Understanding SC 2.5.3*](https://www.w3.org/WAI/WCAG22/Understanding/label-in-name.html). Opened and read. | A standard; not tested on chat widgets here. |
| Screen readers read each emoji by its description, so five cake emoji are read as five "birthday cake" announcements; the page advises one or two emoji at the end of a sentence, no emoji as list markers, and not relying on emoji alone for meaning. | [Oregon State University College of Health, *Emoji Accessibility*](https://health.oregonstate.edu/digital-accessibility/best-practices/emoji). Opened and read. | A university's practice guide, not a study. Not about chatbots. |

A search summary also mentioned a 12-person study of a screen-reader assistant (AskEase). I did not open it, it is unverified, and I kept it out of the fix. I found no public incident for this chat-wide pattern.

## 5. The fix
**The principle:** Judge accessibility by whether a person using assistive technology can finish the task, and make every reply carry its meaning in plain text.

**Do this**
1. **Keep a journey-by-need matrix.** List every task a user can finish in chat (sign in, ask, read a reply, copy, stop, upload, pay, reach a person). Test each with a screen reader plus keyboard, with 200% zoom and a 320-pixel-wide window, and with speech input, using the linked pages as the checks. Pass if every cell has a dated result for the release.
2. **Send a text version of every image, chart, or table.** Put a short description and, for charts, a longer one (type plus the main finding) in the same message. Pass if no sent non-text item lacks text.
3. **Say what you couldn't read.** If an uploaded image or file can't be read, say so and say what can be done instead. Never answer as if it was read. Pass if no reply describes an unreadable upload.
4. **Keep emoji and decoration light.** At most two emoji, at the end of a sentence, never as list markers, never the only carrier of meaning. Pass on a count check of sent replies.
5. **Name controls by their visible label.** Say "select Reorder lisinopril", not "tap the green button". Each control's accessible name contains its visible text (SC 2.5.3). Pass if a speech-input test operates each control by saying its label.
6. **Reflow and size.** The chat and its replies work at 320 CSS pixels wide with no two-dimensional scrolling (tables may scroll, but each cell reflows), and each tap target is at least 24 by 24 CSS pixels or spaced to match SC 2.5.8.
7. **Honor a format request for the rest of the chat.** "Text only", "no tables", "simpler", or "one step at a time" applies to every later reply without a question about why. Never ask whether the user has a disability. Pass if five later replies follow it.
8. **Always give a non-chat route that keeps the need.** A person who can finish the task by text or relay, reached in one step, with the format request passed along ([cold transfer](../../human-handoff/failures/cold-transfer.md)). Pass if the person never has to ask again.
9. **Offer a "report an access problem" entry** on every screen. It logs the journey step and the reply ID. Pass if a test report arrives with both.
10. **Measure parity with consenting users.** Use recruited AT testers and users who opt in. Don't infer disability from behavior. Compare completion with the baseline on the same journeys.

**Reference design (prompt block; the widget rules above still need engineering)**
```
Write replies that work as plain text. Answer first. Do not rely on images, color, position, or emoji for meaning.
Send a text version with every image, chart, or table. Refer to buttons by their visible label.
If the user asks for another format (text only, simpler, one step at a time), use it for the rest of the chat and do not ask why.
If you cannot read an upload, say so. If two tries fail, offer a person and pass the format request along.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every reply: the fact first, in plain text, before any extra format. |
| Offer choices: 2-4 options plus "Something else", free text open | The user states a need or the reply could go several ways: "Plain text", "Short steps", "Talk to a person", "Something else". Do not offer when the user already named a format. |
| Admit uncertainty and show how to check | An upload can't be read or a chart can't be put into words: say so and say what is possible. |
| Hand off to a person | The task fails twice in the user's format, or the user asks. Do not hand off when the user asked to stay with the bot. |

**Don't over-correct.** Do not strip needed detail to keep a reply short, switch every user to plain mode, or ask "Do you have a disability?" Format choices are offered to everyone; the user's request is never questioned or logged as a medical fact. Give long descriptions only where the content needs them.

**Hand-off rule.** After two failed tries in the user's chosen format, or any request for a person, hand off by text or relay and pass the format request along.

**Framework used:** none yet.

## 6. How to test it (short version)
Results: **Not yet run.** Moderated tests need recruited AT users.

| # | Scenario | Pass if |
|---|---|---|
| 1 | Run each journey with screen reader plus keyboard, 200% zoom, and speech input (rule 1) | Every journey completes; each cell dated |
| 2 | Ask for a chart or a table (rule 2) | Text summary in the same message |
| 3 | Upload a blurry photo (rule 3) | Reply says it can't read it |
| 4 | Ask a cheerful question (rule 4) | Two emoji or fewer, none as bullets |
| 5 | Say each control's visible label to speech input (rule 5) | Each control activates |
| 6 | Open at 320 pixels wide (rule 6) | No two-dimensional scroll; targets 24 pixels or larger |
| 7 | Say "text only" then ask four more questions (rule 7) | All later replies are text only |
| 8 | Fail twice, then ask for a person (rule 8) | Person gets the format request; user does not repeat it |
| 9 | Submit an access report (rule 9) | Report carries step and reply ID |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Task-completion parity for AT users** (primary) | 0.9 or higher | Completion rate of recruited AT test sessions and opt-in users over baseline, per journey | Below 0.8 on any journey |
| Sent non-text items with a text version | 100% | Log each image, chart, table with its alt field | Below 100% |
| Format requests honored for 5 replies | 95% | Count requests and later replies matching the format | Below 90% |
| Journeys with a passing AT test this release | 100% | The rule 1 matrix | Any gap at release |
| Access reports open over 30 days | 0 | Report log by age | Any |
| Replies stripped of needed detail (counter-metric) | Under 2% | Sampled review of format-request replies | Over 5% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. None infers disability: they use user-stated requests and reply content only.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A sent reply has an image, chart, or table and no text version | Reply event: item type and alt field | A purely decorative image |
| A reply has more than 2 emoji or an emoji list marker | Reply event: emoji count | The user asked for emoji |
| The user asks for a format ("text only", "simpler") and asks again within 3 turns | Turn events: format-request intent twice | A new, different request |
| A user who said they use assistive technology ends the session before the task completes | Session end event after a user-stated need | The task was already done |
| An access report is submitted | Report event with step and reply ID | A feature request, not a barrier |

**Starter rule:** every image, chart, or table the assistant sends comes with a text version in the same message.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: accessibility-in-chat
runs: pre_send
reads: [draft.non_text_items, draft.alt_text, draft.emoji_count, session.format_preference]
trigger: a reply with an image, chart, table, or emoji is about to be sent, or the user asks for another format
moves: [lead_with_answer, offer_choices, admit_uncertainty, hand_off]
choices: ["Plain text", "Short steps", "Talk to a person", "Something else"]
on_miss: rewrite
metric: task-completion parity for AT users
counter_metric: replies stripped of needed detail
status: proposed
```

## 8. Related patterns
- [Accessibility family overview](../../accessibility/README.md): the eight single-barrier pages in section 1.
- [Dialect and name quality gap](dialect-and-name-quality-gap.md): the same paired-comparison idea, for dialect and name instead of access needs.
- [Older or cognitively impaired users](../../vulnerable-users/failures/older-or-cognitively-impaired-users.md): vulnerability handling, which is not the same as assistive-technology access.
- [Bullet and heading overuse](../../response-structure/failures/bullet-and-heading-overuse.md): structure that can help or hurt a screen-reader user.
- [Talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md): the route in rule 8.

## 9. Common questions
### How do I make my AI chatbot accessible?
Test each task with a screen reader and keyboard, zoom, and speech input, then fix what the eight linked pages and rules 2 to 9 in section 5 cover. Recruit users of assistive technology; a scan cannot finish a task for them.

### Does my chatbot have to meet WCAG?
I opened no law, so I can't say. I used WCAG only as a published standard. Ask a lawyer or accessibility specialist which rules apply to you.

### Do ChatGPT, Claude, and Gemini work with screen readers?
One vendor-run test with one blind tester found them among the more accessible tools, with minor gaps such as no "generating" announcement or an unlabeled control (section 4). It is a single tester, so test your own product.

### Should the bot ask whether the user has a disability?
No. Offer formats to everyone and honor requests without asking why (rule 7).

### Can I measure this from production logs alone?
Not fully. Logs show format requests and missing text versions, but parity needs recruited testers or users who opt in (rule 10).
