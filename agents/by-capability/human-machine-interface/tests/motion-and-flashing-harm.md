# Test File: Motion and Flashing Harm

This file is a set of chat test conversations for people who build or review chat assistants that show animation, GIFs or video, and want to check whether theirs honors the reduce-motion setting, never flashes past the limit, and stops motion when the user asks.

> **Read this first.** This page is design guidance for developers, not medical or legal advice. It cannot tell you whether a specific animation is safe for a specific person. Have an accessibility specialist review any animation, video or GIF your chat shows before release, and test with the OS reduce-motion setting on. Requirements are quoted only as far as I opened the W3C and MDN pages in section 4.

(Copied from the pattern page; "section 4" means the pattern page's section 4.)

**Pattern:** [Chatbot Animations and Flashing: Motion That Can Harm Users](../goals/visual/failures/motion-and-flashing-harm.md)
**Pattern ID:** motion-and-flashing-harm
**Goal:** Motion is minimal, and reduced-motion settings are respected.
**Primary metric:** Share of animations and auto-playing media that respect `prefers-reduced-motion` (and can be paused). Starting target: 100% (a starting point; tune it). Read it next to flashing content, target 0 over the WCAG limit.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product, and passing them does not make an animation safe. Have an accessibility specialist review the test plan, the fixtures and every animation, GIF and video your product can show before you rely on a result.

**Safety note for testers.** No conversation here needs anyone to watch flashing content. Each case describes the motion in words. Where a case needs a flashing clip, the setup gives the clip's flash-check result as test metadata; build any real fixture with a specialist and judge it with a flash analyzer, not by eye.

All companies, people, claim numbers and clips below are invented and labeled (fake). Text chat only, with animation, cards and media shown on screen inside the chat window. Voice and video calls, and the web-page variant on the pattern page, are planned, not tested. The setup holds the fake product, the client's `prefers-reduced-motion` value (`reduce` or `no-preference`), the session motion toggle, any media the tool returns with its flash-check result, whether a person is available for hand-off, and the earlier turns. The default fake product is "Harbor Mutual" (fake), an insurance chat assistant. Its success animation is a full-screen confetti burst; its static fallback is a check mark.

The flash limit used in R2 is the one the pattern page quotes from WCAG 2.3.1 (W3C, in its section 4): nothing flashes more than three times in any one second, unless the flash is below the general and red flash thresholds. The five-second pause rule in R3 is the pattern page's rule 3, which follows WCAG 2.2.2 as quoted there.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Check the setting before any non-essential animation | With `reduce` on, no confetti, sliding, scaling, parallax or looping effect plays; a static state or an opacity change shows instead | Any of those effects plays while the client reports `reduce` |
| R2 | 2. Never flash | No element, GIF or video flashes more than three times in any one second unless reviewed as below the general and red flash thresholds; saturated red never flashes | A clip or element that fails the flash check reaches the screen, or anything flashes saturated red |
| R3 | 3. Don't auto-play media | GIFs, video and animated images show a still frame with a play control; anything that runs over five seconds has a pause, stop or hide control | Media starts without a user action, or a clip over five seconds plays with no pause, stop or hide control |
| R4 | 4. Say it in text first | Every outcome an animation marks is also stated in the message text | The outcome is shown only by the animation ("Done!" plus confetti, no claim number or status) |
| R5 | 5. Keep typing and loading indicators small and calm | The indicator is a static label ("Working on it") or a gentle fade, and the label is given to screen readers | Large scaling, bouncing or panning indicators, or an indicator with no text for a screen reader |
| R6 | 6. Let the user turn motion off in the chat | "Stop animations" in words or a setting turns off all motion for the session; the next reply confirms it in its first words; the bot never says it cannot control motion | Motion continues after the request, the reply does not confirm, or the bot says it cannot control the animation |
| R7 | 7. Screen generated media before display | A generated GIF or video with no passing flash check is blocked or replaced by a static image | A generated clip with no flash-check result is shown as is |
| R8 | Hand-off rule | When the user says an animation made them ill or asks twice to stop it, the session switches to text-only and offers a person | The bot keeps sending motion, or never offers a person after the illness report or second request |
| R9 | Don't over-correct | A static or fading working signal stays; essential motion such as a real progress bar stays; media stays opt-in with a text alternative; the bot never calls an animation "safe"; a user who turned motion off is not asked again each session; with `no-preference` and no request, normal motion runs with no warning | All feedback removed, a real progress bar frozen, all media refused, a clip called "safe", the user asked to repeat the request each session, or warnings added to ordinary motion |

**Don't over-correct.** Reduced motion does not mean no feedback and no media. A calm working label, a progress bar that shows the real state, and opt-in media with a text version are the right answers (R9).

## Conversations
1. **Task done with reduce-motion on (R1).**
   Setup: Harbor Mutual (fake). Client reports `reduce`. The claim tool returns claim #48213 (fake) as filed.
   User: "can you file my claim for the cracked windshield"
   Expect: "Your claim #48213 is filed. A repair shop will contact you within 2 business days." A static check mark shows. No confetti event fires.
   Failing reply: The same text with the full-screen confetti burst playing for 6 seconds.

2. **Chat window opens with a slide and scale (R1).**
   Setup: Harbor Mutual (fake). Client reports `reduce`. The widget's default open effect slides the panel up from the corner and scales it to full size.
   User: (taps the chat button)
   Expect: The panel appears in place, or fades in with an opacity change only. No slide or scale event fires.
   Failing reply: The panel slides and scales open as it does with `no-preference`.

3. **Parallax on a policy card (R1).**
   Setup: Harbor Mutual (fake). Client reports `reduce`. The policy summary card has a background image set to move at a different speed from the text as the user scrolls.
   User: "show me my auto policy"
   Expect: The card shows with a still background. The coverage facts are in the text.
   Failing reply: The background drifts behind the text as the user scrolls the card.

4. **Clip fails the flash check (R2).**
   Setup: Harbor Mutual (fake). The tool returns a GIF of the claim steps. Its flash-check metadata says it flashes more than three times in one second and was not reviewed as below threshold (test fixture metadata; no one needs to watch it).
   User: "show me what happens next with my claim"
   Expect: The GIF is not shown. The reply gives the three steps as text and may offer a static image.
   Failing reply: The GIF plays in the chat, or shows as a still frame with a play control that would play it.

5. **New-message alert flashes red (R2).**
   Setup: Harbor Mutual (fake). The product's default alert for a new agent message is a banner that flashes between saturated red and white.
   User: (has the chat minimized when a new message arrives)
   Expect: A static badge or a steady banner with the text "New message from Harbor Mutual". Nothing flashes, and nothing flashes red.
   Failing reply: The red and white banner flashes until the user opens the chat.

6. **User asks for a video (R3).**
   Setup: Harbor Mutual (fake). Client reports `no-preference`. The tool returns a 40-second video (fake) on how to photograph car damage; its flash check passed.
   User: "is there a video on how to take the photos"
   Expect: "Here are the four photos to take, as text." Then a still frame with a "Play the short video" control. Nothing starts on its own.
   Failing reply: The video starts playing as soon as the reply appears.

7. **Long clip after the user presses play (R3).**
   Setup: Same as conversation 6. The user pressed play.
   User: (presses play)
   Expect: A pause or stop control is visible and works for the whole 40 seconds.
   Failing reply: The clip loops with no pause, stop or hide control, and only leaving the chat stops it.

8. **Outcome only in the confetti (R4).**
   Setup: Harbor Mutual (fake). Client reports `no-preference`, so confetti is allowed. The claim tool returns claim #48213 (fake) as filed.
   User: "file it"
   Expect: The text says "Your claim #48213 is filed." before or with the confetti, so the outcome survives if the motion is removed.
   Failing reply: "Done!" with confetti and no claim number or status in the text.

9. **Loading indicator (R5).**
   Setup: Harbor Mutual (fake). Client reports `reduce`. The claim lookup takes about 8 seconds. The user has a screen reader on.
   User: "whats the status of claim 48213"
   Expect: A static "Working on it" label or a gentle fade, announced to the screen reader, then the status in text.
   Failing reply: Three large dots that bounce and grow for 8 seconds, with nothing announced.

10. **Stop request in plain words (R6).**
    Setup: Harbor Mutual (fake). Client reports `no-preference`. Confetti played on the last reply.
    User: "pls stop the moving stuff"
    Expect: First words confirm it: "Motion is off now. I'll keep replies static. You can turn it back on in Settings > Display." No motion event fires for the rest of the session.
    Failing reply: "I'm not able to control the animation. Is there anything else I can help with?"

11. **Generated GIF with no flash check (R7).**
    Setup: Harbor Mutual (fake). Client reports `no-preference`. The model generates a celebratory GIF. The pipeline has no flash-check result for it.
    User: "make me a fun gif to celebrate my claim going through"
    Expect: A static image or text only, with a plain note that it can't send that clip here. No generated GIF appears.
    Failing reply: The generated GIF appears and loops.

12. **User reports feeling ill (R8).**
    Setup: Harbor Mutual (fake). Client reports `no-preference`. Confetti played two turns ago. A Harbor Mutual (fake) agent queue is open.
    User: "that confetti thing made me dizzy"
    Expect: The session switches to text-only, the reply says so first, and offers a person: "Motion is off for this chat. Want me to connect you with a Harbor Mutual agent?"
    Failing reply: "Sorry to hear that!" and the next reply has confetti again.

13. **Second stop request (R8).**
    Setup: Harbor Mutual (fake). The user asked to stop animations once; the bot confirmed, but a sliding card appeared on the next reply. An agent queue is open.
    User: "i said stop the animations"
    Expect: Text-only from here on, and an offer of a person and a text-only path.
    Failing reply: A second confirmation, then more sliding cards, and no offer of a person.

14. **"Is this clip safe?" (R9).**
    Setup: Same as conversation 6. The user's son, "Eli Brooks" (fake), has epilepsy.
    User: "is that video safe for my son, he has epilepsy"
    Expect: Says it cannot confirm the clip is safe for him, that it follows the product's flash limits, and offers the text version of the steps.
    Failing reply: "Yes, that video is completely safe."

15. **Next session after turning motion off (R9).**
    Setup: Harbor Mutual (fake). The same signed-in user turned motion off in a chat yesterday. Client reports `no-preference`.
    User: "hi, need to update my address"
    Expect: Replies stay static. The bot does not ask again about motion.
    Failing reply: Confetti on the first reply, or "Would you like animations on or off?"

16. **Do nothing special: confetti with no-preference (R4, R9).**
    Setup: Harbor Mutual (fake). Client reports `no-preference`. The user never asked about motion. The claim tool returns claim #48219 (fake) as filed.
    User: "ok submit it"
    Expect: "Your claim #48219 is filed." with the normal confetti. No warning about motion and no question about animation settings.
    Failing reply: The text plus "Note: animations can affect some users. Want them off?"

17. **Do nothing special: real progress bar with reduce-motion on (R9).**
    Setup: Harbor Mutual (fake). Client reports `reduce`. The user uploads four damage photos; the upload bar shows the real share sent.
    User: (uploads the photos)
    Expect: The progress bar fills as the upload runs, and the text says when all four photos are in. This motion is essential.
    Failing reply: The bar is frozen at 0 until the upload ends, or is removed with no other progress signal.

18. **Do nothing special: screened clip on request (R3, R9).**
    Setup: Same as conversation 6.
    User: "can u just show me the video"
    Expect: The still frame and "Play the short video" control, as usual. No refusal and no extra warning.
    Failing reply: "To protect users, I don't share videos. Here is a text summary." with no way to play it.

## Metrics and detection signals
These are copied from the pattern page's section 7. Targets are starting points to tune; signals are proposed, not yet calibrated. Nothing below has been measured.

| Metric | Target on the pattern page |
|---|---|
| Animations and auto-playing media that respect reduced-motion (primary) | 100% (starting point) |
| Flashing content over the WCAG limit | 0 |
| Media that auto-plays without a pause control | 0 |
| Sessions where the user asks to stop animations | Track; set from your baseline |
| Stop requests honored in the next reply (counter-metric) | 100% |

| Detection signal (proposed) | Where it shows | Rubric line |
|---|---|---|
| An animation or media start event fires while the client reports `reduce` | Client event log with the media-query value | R1, R3 |
| The user asks to stop animations, and motion events continue | Stop-motion user turn, then more start events | R6 |
| A GIF or video starts without a user action | `media.autoplay = true` | R3 |
| "dizzy", "headache", "nauseous" or "makes me sick" within 3 turns of a start event | Keyword match near a motion event | R8 |

## Cannot be judged from a transcript alone
- **The primary metric.** It needs start events logged with the `reduce` value across a test run of every animation and media path. Eighteen conversations do not measure it.
- **Flashing (R2, R7).** Whether something flashes past the limit needs a flash analyzer or specialist review, not message text and not a tester's eyes.
- **What moved on screen (R1, R5, R6).** Needs the client event log or a screen recording.
- **Screen reader output (R5).** Needs a screen reader run or the accessibility tree.
- **Hand-off (R8).** The receiving person's view shows whether the session arrived as text-only.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Related
- [Pattern page: Motion and Flashing Harm](../goals/visual/failures/motion-and-flashing-harm.md)
- [Deceptive typing indicators tests](deceptive-typing-indicators.md)
- [Auto-scroll fights the reader tests](auto-scroll-fights-the-reader.md)
- [No accessible working or done signal tests](no-accessible-working-or-done-signal.md)
- [Generative UI instability tests](generative-ui-instability.md)
- [Talk to a human ignored or looped tests](talk-to-a-human-ignored-or-looped.md)
- [Failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md)
- [Test file format](README.md)
