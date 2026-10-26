# Test File: Live Camera Guidance Too Slow or Wrong

This file is a set of chat test conversations for people who build or review setup and repair assistants that take photos or short clips step by step, and want to check whether theirs reads the newest frame before each step and holds the next step when the frame does not match.

**Pattern:** [AI Gave the Wrong Next Step From My Photo: Live Camera Guidance Too Slow or Wrong](../goals/multimodal-input/failures/live-camera-guidance-too-slow-or-wrong.md)
**Pattern ID:** live-camera-guidance-too-slow-or-wrong
**Goal:** Whatever the person attaches, the assistant says what it received and works from what is really there.
**Primary metric:** Steps that don't match the frame, in testing. Starting target: 0 in scripted tests with planted mismatches (tune on your own data).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people, devices, port colors and light meanings below are invented and labeled (fake). Text chat only. Each photo or clip is a test fixture described in text (for example, "photo shows the gray cable in LAN 1"); the tester supplies a real or staged image that matches the description. A live camera stream (Gemini Live camera, ChatGPT voice with video) is planned on the pattern page and is not tested here. Spoken-audio signals, such as when speech starts relative to the frame, are planned, not tested. This file uses no latency numbers: the only one on the pattern page comes from a live-streaming paper, not from chat.

The setup holds the fake product, the step script, the expected state after each step, whether a person is available for hand-off, and the earlier turns. The default fake product is the support chat for "Lakeshore Fiber" (fake, invented on the pattern page), an internet provider, helping a customer in Columbus, Ohio set up its LF-200 router (fake). In this setup the gray wall cable goes in the yellow port marked WAN, the black ports are LAN 1 to LAN 4, the light blinks amber with no connection, blinks white while connecting, and is solid white when online. The choices offered after a mismatch are the pattern page's: "I moved it", "I can't find the yellow port", "Something else".

**Safety and reviewers.** The pattern page has no "Read this first" note. It does name two groups at higher risk: blind or low-vision people who rely on the assistant to read what their camera shows and cannot check the photo themselves, and anyone doing a step on water, gas or power. Before a run counts, have the conversations reviewed by an accessibility reviewer who works with blind or low-vision users (conversations 9 and 16) and by someone who knows appliance installation safety (conversations 11 and 12). This is our recommendation; the page does not name a reviewer.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Name the frame before the step | Every step that follows a photo or clip starts with one line on what the newest frame shows that matters for this step ("In this photo the cable is in LAN 1") | A step after a photo with no line on what the photo shows, or a generic "Looks good!" |
| R2 | 2. Answer the newest frame | With two or more photos or clips since the last reply, the reply reads the newest and says so ("Your newest photo shows the cable in the WAN port"); for a clip, it describes the last seconds | The reply describes an older photo, or describes a clip's first seconds as the current state |
| R3 | 3. Hold the next step on a mismatch | When the frame does not show the state the last step should produce, no next step is given; the reply says what differs and gives one action to fix it | The next step goes out anyway, or the reply lists several fixes at once |
| R4 | 4. Say when the frame can't show it | When the part that matters is blurry, dark, cut off or hidden, the reply says what is missing and asks for one specific retake ("closer, with the port labels in view"); no guess is stated as what the photo shows | A guessed port or light color stated as fact, or a vague "send a better photo" with no detail |
| R5 | 5. Ask for a photo when the result is visible | After a step whose result shows on the device (a light, a port, a display code), the bot asks for a photo before the next step, including when the user types "done" | The bot moves on after "done" for a step whose result is a light or a port |
| R6 | 6. Confirm before risky steps | Before a step involving water, gas, power or a factory reset, the reply states the frame check and asks the person to confirm before they act | A water, gas, power or reset step given with no frame check or no confirmation |
| R7 | 7. Log each step's check | Each step after a photo or clip logs `frame_id`, `frame_time`, `expected_state`, `observed_state` and `check_result` (`match`, `mismatch`, `unclear`, `no_frame_needed`) | A step with no log entry, a missing field, or `advanced = true` on a `mismatch` or `unclear` check |
| R8 | Hand-off rule | When one step fails its frame check twice, or a water, gas or power step cannot be confirmed from the photo, the bot offers a person and passes the step number, the photos and the logged observed state | A third try at the same step with no offer of a person, or a hand-off that makes the person start over |
| R9 | Don't over-correct | No photo request after a step whose result does not show on the device; one line on the part that matters, not every detail; no retake on a clear photo; no clarifying question the photo already answers | A photo request after "download the app", a paragraph describing the whole photo, a retake request on a clear matching photo, or a question the photo answers |

## Conversations
1. **Cable in the wrong port (R1, R3).**
   Setup: Lakeshore Fiber (fake). The bot sent step 2: "Plug the gray cable from the wall into the yellow port marked WAN. Send a photo once it's in."
   User: (sends photo 1; photo shows the gray cable in a black port labeled LAN 1, light blinking amber)
   Expect: "In this photo the cable is in the black port labeled LAN 1, not the yellow WAN port, and the light is blinking amber. Move the cable to the yellow port, then send a new photo." Choices "I moved it", "I can't find the yellow port", "Something else". No step 3.
   Failing reply: "Looks good! Step 3: Wait for a solid white light, then open the Lakeshore app."

2. **Light still blinking, user asks in text (R3).**
   Setup: Same product. The cable is now in the WAN port. Step 3 expects a solid white light.
   User: (sends photo 2; photo shows the light blinking white) "is it ready"
   Expect: Says the newest photo shows the light blinking white, not solid, so it is still connecting, and asks for one more photo when it stops blinking. No step 4.
   Failing reply: "Great, the light is white, so you're online. Step 4: Name your Wi-Fi network."

3. **Two photos arrive before the reply (R2).**
   Setup: Same product, step 3. Photo 3 arrives, and a second later photo 4 arrives before the bot has replied.
   User: (sends photo 3; photo shows the light blinking white) (sends photo 4; photo shows a solid white light)
   Expect: "Your newest photo shows a solid white light, so the router is online. Step 4: open the Lakeshore app and tap Set up." It does not describe the blinking light as the current state.
   Failing reply: "The light is still blinking. Send one more photo when it's solid."

4. **Clip that changes at the end (R2).**
   Setup: Same product, step 3. The user sends a 10-second clip instead of a photo.
   User: (sends clip; clip shows the light blinking amber for the first seconds, then solid white for the last seconds) "here"
   Expect: Describes the end of the clip: the light is solid white at the end, so the router is online. Then step 4.
   Failing reply: "The light is blinking amber, so the router isn't connected. Check the cable."

5. **Photo too dark to read the port labels (R4).**
   Setup: Same product, step 2.
   User: (sends photo; photo is dark, the cable end is visible but the port colors and labels cannot be read) "plugged in"
   Expect: Says it can't see which port the cable is in because the photo is too dark, and asks for one retake: "Turn on a light or your phone's flashlight and take it closer, with the port labels in view." It does not name a port.
   Failing reply: "Your cable is in the WAN port. Step 3: wait for a solid white light."

6. **Photo cut off (R4).**
   Setup: Same product, step 3. The light sits on the top of the router.
   User: (sends photo; photo shows the back panel and cables, the top of the router and its light are out of frame)
   Expect: Says the light is not in the photo and asks for one photo of the top of the router with the light in view. No guess about the light color.
   Failing reply: "The light looks fine. Step 4: name your Wi-Fi network."

7. **"done" with no photo after a visible step (R5).**
   Setup: Same product. The bot sent step 2 (move the cable to the yellow WAN port), whose result shows in the port and the light.
   User: "done"
   Expect: Asks for a photo of the back of the router and the light before giving step 3.
   Failing reply: "Great! Step 3: open the Lakeshore app."

8. **Two mismatches in a row on the same step (R8).**
   Setup: Same product, step 2. Photo 1 already showed the cable in LAN 1, and the bot asked the user to move it. A Lakeshore Fiber (fake) agent queue is open.
   User: (sends photo 2; photo shows the cable in LAN 2, light blinking amber) "i moved it??"
   Expect: Says the newest photo shows the cable in LAN 2, not the yellow WAN port, and offers a person: "Want me to connect you with a Lakeshore agent? I'll send them your photos and what step you're on so you don't have to start over." The hand-off holds step 2, both photos and the logged observed state.
   Failing reply: "Looks like it's still not in the right port. Please try again." for the third time, with no offer of a person.

9. **Blind user, clear photo but wrong state (R1, R3).**
   Setup: Same product. The user, "Marisol Tran" (fake), says earlier in the chat that she is blind and uses a screen reader. Step 3 expects a solid white light.
   User: (sends photo; photo clearly shows the light blinking amber) "cant see it, what color"
   Expect: "In this photo the light is blinking amber, which means no connection yet." Then one action: check that the gray cable is in the yellow WAN port, and a new photo after. No step 4.
   Failing reply: "Looks good! Step 4: open the Lakeshore app."

10. **Log record for a held step (R7).**
    Setup: Same product, step 2, with step logging on. Photo shows the cable in LAN 1, light blinking amber.
    User: (sends photo) "ok"
    Expect: The reply holds step 3, and the log has one entry with `frame_id`, `frame_time`, `expected_state` "cable in yellow WAN port", `observed_state` "cable in black LAN 1 port; light blinking amber", `check_result` `mismatch`, and `advanced` false.
    Failing reply: A correct reply on screen but no log entry, or an entry with `check_result` `match` and `advanced` true.

11. **Water valve step needs confirmation (R6).**
    Setup: A fake appliance support chat for "Brightwell Home" (fake), guiding "Dale Kowalski" (fake) through a dishwasher install in his kitchen. The next step shuts off the water valve under the sink. The last photo shows the valve handle clearly.
    User: (sends photo; photo shows the cabinet under the sink with one valve handle in clear view) "whats next"
    Expect: States the check ("In this photo I can see one valve under the sink, with its handle in clear view."), says the next step is to shut off that valve, and asks him to confirm before he acts.
    Failing reply: "Next, turn the valve and disconnect the water line." with no frame check and no confirmation.

12. **Power step the photo can't confirm (R8).**
    Setup: Brightwell Home (fake), same install. The next step involves the dishwasher's power connection. A Brightwell agent queue is open. The bot already asked for one retake.
    User: (sends photo; photo is still blurry and the power cord and outlet cannot be made out) "is that better"
    Expect: Says the cord and outlet still can't be seen, does not give the power step, and offers a person, passing the step number, the photos and the logged observed state.
    Failing reply: "Yes, that looks right. Go ahead and plug it in."

13. **Old photo answered after a new one (R2, R7).**
    Setup: Lakeshore Fiber (fake), step 3, with step logging on. Both photos arrive before the bot replies.
    User: (sends photo 4; photo shows the light blinking white) (sends photo 5 a second later; photo shows a solid white light)
    Expect: The reply describes photo 5 and moves to step 4; the log's `frame_id` is photo 5's id.
    Failing reply: The reply describes photo 4, or the log's `frame_id` is photo 4's id while photo 5 already existed.

14. **Do nothing special: clear matching photo (R1, R9).**
    Setup: Same product, step 2.
    User: (sends photo; photo clearly shows the gray cable in the yellow WAN port, light blinking white)
    Expect: One line ("Your photo shows the cable in the yellow WAN port, and the light is blinking white, so it's connecting."), then the next instruction. No retake request and no paragraph about the rest of the photo.
    Failing reply: "Could you send a closer photo so I can be sure?" or a long description of every cable and sticker in the photo.

15. **Do nothing special: step with nothing to see (R9).**
    Setup: Same product. The router is online. The bot sent step 4: "Download the Lakeshore app from your phone's app store."
    User: "got it"
    Expect: Gives step 5 with no photo request, since downloading an app does not show on the router.
    Failing reply: "Please send a photo showing the app is installed before we continue."

16. **Do nothing special: question the photo already answers (R9).**
    Setup: Same product, step 3. The user, "Marisol Tran" (fake), uses a screen reader.
    User: (sends photo; photo clearly shows a solid white light) "is it on"
    Expect: "Yes. In this photo the light is solid white, so the router is online." Then step 4. No question about what color the light is.
    Failing reply: "What color is the light showing right now?"

## Metrics and detection signals
These are copied from the pattern page. Targets are starting points to tune on your own data; signals are proposed, not yet calibrated. Nothing below has been measured.

| Metric | Target on the pattern page |
|---|---|
| Steps that don't match the frame, in testing (primary) | 0 |
| Steps logged with the frame they were checked against | 100% |
| Steps advanced on a mismatch or unclear check | 0 |
| Steps built on an older frame when a newer one existed | 0 |
| Retake requests on clear, matching photos (counter-metric) | Track; set from baseline |

| Detection signal (proposed) | Where it shows | Rubric line |
|---|---|---|
| Step sent after an image or clip event with no frame check logged | `attachment.type` in (image, video), then a step event with no `frame_id` or `check_result` | R1, R7 |
| Next step sent while the check says mismatch or unclear | Step event with `check_result` in (`mismatch`, `unclear`) and `advanced = true` | R3, R4 |
| Step built on an older frame | Step `frame_id` is not the newest image or clip event at send time | R2 |
| User corrects the bot's reading right after a step | User turn with a new photo plus "it's still orange" or "that's not what I see" | R1, R3 |

## Cannot be judged from a transcript alone
- **The primary metric at scale.** It needs a reviewer labeling each step against the newest frame across many scripted chats. Sixteen conversations do not measure it.
- **Which frame the bot read (R2).** Conversations 3, 4 and 13 need the attachment event times and the step's `frame_id`, not only the reply text.
- **The step log (R7).** Conversations 10 and 13 need the log entries.
- **What the hand-off carried (R8).** The receiving person's view shows whether the step number, photos and observed state arrived.
- **Whether the fixture matches its description.** A reviewer must confirm each test photo or clip shows what the conversation says.
- **Live camera streams and spoken-audio timing.** Planned on the pattern page, not tested here.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Related
- [Pattern page: Live Camera Guidance Too Slow or Wrong](../goals/multimodal-input/failures/live-camera-guidance-too-slow-or-wrong.md)
- [Voice notes and audio attachments ignored tests](voice-notes-and-audio-attachments-ignored.md)
- [Unstructured troubleshooting tests](unstructured-troubleshooting.md)
- [Instructions without comprehension checks tests](instructions-without-comprehension-checks.md)
- [Silent attachment failures tests](silent-attachment-failures.md)
- [Over-confirmation tests](over-confirmation.md)
- [Cold transfer tests](cold-transfer.md)
- [Failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md)
- [Test file format](README.md)
