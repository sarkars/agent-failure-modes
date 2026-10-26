# Test File: Generative UI Instability

This file is a set of chat test conversations for people who build or review chat assistants that pick and fill their own cards and widgets, and want to check whether theirs keeps the layout still, shows only valid components, and falls back to plain text when a component fails.

**Pattern:** [Generative UI Layout Shifts and Broken Components: Generative UI Instability](../goals/visual/failures/generative-ui-instability.md)
**Pattern ID:** generative-ui-instability
**Goal:** What an agent shows is clear, honest, accessible, and appropriate to the stakes. (Row goal: generated interfaces are stable and valid.)
**Primary metric:** Layout-shift measure; component-schema validity. Target: 100% (starting point; tune it). Schema validity is the share of rendered components that pass their schema; the shift measure is the score defined in section 7.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people, flights and prices below are invented and labeled (fake). Text chat only, with cards and widgets rendered inside the chat window; the voice and full web-app variants on the pattern page are planned and are not tested here. "The pattern page" below means the page linked above, and "section 7" in the primary metric is that page's section 7.

The setup holds the fake product, the component registry, each component's schema and reserved slot, the tool result the assistant receives, any fault the tester injects (a missing field, a wrong type, a delay, a token cutoff, a blocked widget script), whether a person is available for hand-off, and the earlier turns. The default fake product is "Ridgeway Trips" (fake), a travel chat run by "Ridgeway Travel Co." (fake) that books flights on "Northwind Air" (fake). Its registry has three components:

- `flight_card`: required fields `origin`, `destination`, `depart_time`, `price_usd`, `book_action`; one optional field, `aircraft`. Reserved slot: minimum height 168px, full message width, with a skeleton. Field order top to bottom: route, departure time, price, aircraft (if present), then a "Book" button bottom right and a "Details" link bottom left.
- `price_table`: a list of fares with the same fields, one row per flight, used when the user asks to compare.
- `trip_status_card`: a live status card for a booked trip (on time, delayed, gate), with its own reserved slot.

The slot sizes and field order are test settings taken from the pattern page's reference contract, which calls its numbers placeholders to tune. They are not a claim about any real product.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Closed component registry | Only `flight_card`, `price_table` or `trip_status_card` ever renders; a component name not on the list never renders, and the reply is plain text | An unknown component renders, a blank frame appears where it would be, or the reply shows a raw error |
| R2 | 2. Schema check before render | Every rendered component has every required field present, with the right type and an allowed value; a failed check blocks only that component, and the rest of the reply still arrives | A component renders with a missing or wrong-typed required field, or one failed component blocks the whole reply |
| R3 | 3. Reserve the space first | A skeleton holds the component's slot before it fills; text above and below does not move when the component lands; nothing is inserted above text the user is reading unless the user asked | Text jumps when the component arrives, or a component appears above text the user had started reading with no request |
| R4 | 4. Render once, complete | The component appears once, after its schema passes, with all fields filled; it is not swapped for another component type after it appears | Fields fill in one by one inside a visible card, a partial card shows after a cutoff, or a card is replaced by a different component type |
| R5 | 5. Same task, same component | A repeat of the same request gives the same component, the same field order and the same control positions | The same request gives a card one time and a table the next, or the "Book" button moves between runs |
| R6 | 6. Fall back to text on failure | On a failed check, an unknown name, a refusal or a cutoff, the reply is plain text with the key facts; no "undefined", "NaN" or empty card is ever on screen | "undefined", "NaN", an empty card, or a reply with no answer at all |
| R7 | 7. Key facts in text, labeled for a screen reader | The message text states the key facts (route, time, price) even when the component never loads; each control has a text label a screen reader can read | The facts live only inside the widget, or a control has no label ("button") |
| R8 | 8. Keep tap targets still | A control is disabled until its card is final, and no control moves within 500 ms before a tap lands | A tap meant for "Book" lands on another control because the card moved, or "Book" is active while the card is still loading |
| R9 | Hand-off rule | When the same component fails validation twice in one conversation on a booking or payment step, the bot stops rendering it, gives the facts in text and offers a person with a summary | The bot keeps retrying the broken component, or never offers a person after the second failure |
| R10 | Don't over-correct | Components still render when they pass; a live status card may update inside its reserved slot after a clear event; a missing optional field does not block the component; a user's own request to change the layout is followed | Every reply is locked to text, a live card is frozen, a valid card is blocked over an optional field, or the bot refuses a layout the user asked for |

**Don't over-correct.** The fix is not "never show a component." A valid card in its reserved slot is the right answer. Locking every reply to text, freezing a live status card, or blocking a card because an optional field is empty are failures too (R10).

## Metrics and detection signals
These are copied from the pattern page. The targets there are starting points to tune, and the signals are proposed, not yet calibrated. Nothing below has been measured.

| Metric | Target on the pattern page |
|---|---|
| Component-schema validity (primary) | 100% of rendered components pass |
| Layout-shift measure (primary) | 0.1 or less at the 75th percentile, the web.dev "good" level borrowed for chat and not validated for it |
| Fallback-to-text rate | Track; set from your baseline |
| Same-intent layout consistency | 100% (starting point) |
| Taps lost to a moving control (counter-metric) | Track |

| Detection signal (proposed) | Where it shows | Rubric line |
|---|---|---|
| A component payload fails its schema or names an unknown component | `component.valid = false` or `component.unknown` | R1, R2 |
| A layout shift above the target while a message streams | Layout-shift entry tied to a message id | R3 |
| Same intent returns a different component than before | Component name differs across turns for one intent | R5 |
| The user repeats the request right after a card | Same intent in the next user turn | R5, R6 |
| A visible "undefined", "NaN" or empty field in a rendered card | Text scan of rendered component strings | R6 |

## Conversations
1. **Unknown component name (R1, R6).**
   Setup: Ridgeway Trips (fake). The tester forces the model to call a component named `seat_map_3d`, which is not in the registry. The tool result has two flights from Chicago to Denver on Friday and says the 7:05 a.m. flight has window seats left in rows 12 to 18.
   User: "show me seats on the friday denver flight"
   Expect: No `seat_map_3d` renders and no blank frame appears. The reply is plain text, for example: "I can't show a seat map here. The 7:05 a.m. Northwind Air flight (fake) has window seats left in rows 12 to 18." Free text stays open.
   Failing reply: An empty gray box where the seat map would be, with "Component not found: seat_map_3d" under it.

2. **Missing required field (R2, R6).**
   Setup: Ridgeway Trips (fake). The tool result for one flight has no `depart_time`.
   User: "flights to denver friday"
   Expect: The `flight_card` for that flight is blocked. The text gives the facts it has and says which one is missing: "The $189 nonstop to Denver on Friday is listed, but I don't have its departure time yet. Want me to check again?"
   Failing reply: A rendered card reading "Departs: undefined   Price: $189".

3. **Wrong type in a price field (R2, R6).**
   Setup: Ridgeway Trips (fake). The tool result sends `price_usd` as the text "two hundred twelve" instead of a number.
   User: "how much is the 7am to denver"
   Expect: Validation fails, so no card renders. The text says the price could not be confirmed and offers to check again. No "NaN" anywhere on screen.
   Failing reply: A `flight_card` showing "Price: $NaN" with an active "Book" button.

4. **Slow component on a throttled connection (R3).**
   Setup: Ridgeway Trips (fake). The tester delays the `flight_card` by 3 seconds on a throttled connection. The text reply streams first: one sentence above the card, one sentence below it.
   User: "find me a flight to denver on friday"
   Expect: A skeleton holds the card's slot (full width, at least the setup's 168px) between the two sentences from the start. When the card fills it, neither sentence moves.
   Failing reply: Both sentences stream together, then the card pops in between them and pushes the second sentence, "Want the cheaper one?", off the bottom of the screen.

5. **Content dropped above text the user is reading (R3).**
   Setup: Ridgeway Trips (fake). The bot has sent a long text answer about baggage rules, and the user has scrolled to the middle of it. A late `price_table` from the earlier fare search finishes loading.
   User: (no new message; the user is reading)
   Expect: The table does not appear above the paragraph the user is reading. It fills its own reserved slot below, or waits until the user asks for it.
   Failing reply: The table lands at the top of the message and the paragraph the user was reading jumps down by the height of the table.

6. **Cutoff at a low token limit (R4, R6).**
   Setup: Ridgeway Trips (fake). The tester sets a low token limit so the component payload is cut off after `origin` and `destination`.
   User: "cheapest flight chicago to denver friday"
   Expect: No partial card is ever shown. The reply is plain text with whatever facts are complete, says the rest could not load, and offers to try again.
   Failing reply: A card with "Chicago to Denver" filled in and the time, price and "Book" button slots left blank.

7. **Component swapped after it appears (R4).**
   Setup: Ridgeway Trips (fake). The model first emits a `flight_card`, then later in the same reply decides a `price_table` fits better.
   User: "what are my options to denver friday"
   Expect: One component appears, once, and stays. If the model's later choice differs, the first component is kept for this reply.
   Failing reply: A `flight_card` shows for about a second, then disappears and a `price_table` with different row heights takes its place.

8. **Same request five times (R5).**
   Setup: Ridgeway Trips (fake). The tester sends the same request in five fresh chats with the same tool result.
   User: "flights to denver on friday"
   Expect: All five replies use `flight_card` with the same field order (route, time, price, then "Book" bottom right and "Details" bottom left).
   Failing reply: Run 1 shows a `flight_card`, run 3 shows a `price_table`, and run 5 shows a card with the price above the route and "Book" on the left.

9. **Widget script blocked (R7).**
   Setup: Ridgeway Trips (fake). The tester blocks the widget script, so no component can load.
   User: "find me a flight to denver on friday"
   Expect: The message text alone carries the answer: "Two nonstop options on Friday. The 7:05 a.m. is $212, the 1:40 p.m. is $189. Want the cheaper one?" (fake fares).
   Failing reply: "Here are your options:" followed by an empty space where the card should be.

10. **Screen reader reads the card (R7).**
    Setup: Ridgeway Trips (fake). The user, "Dana Whitfield" (fake), uses a screen reader. The `flight_card` renders and passes its schema.
    User: "read me the friday options"
    Expect: The text states the route, time and price, and each control has a label that says what it does, such as "Book the 7:05 a.m. flight to Denver, $212" and "Details for the 7:05 a.m. flight".
    Failing reply: The screen reader hears "button, button, link" with no label, and the price appears only inside the card.

11. **Tap as the card finishes (R8).**
    Setup: Ridgeway Trips (fake). The `flight_card` skeleton is showing. The tester taps where "Book" will be just as the card fills.
    User: (taps "Book")
    Expect: "Book" was disabled until the card was final, and nothing moved in the 500 ms before the tap. The tap either does nothing or lands on "Book" for the flight the user saw.
    Failing reply: The card shifts as it fills, and the tap lands on "Details" for another flight, or on a "Cancel" control that moved under the finger.

12. **Same component fails twice on a booking (R9).**
    Setup: Ridgeway Trips (fake). The user is booking the 1:40 p.m. flight. The booking `flight_card` failed validation once already in this chat (missing `book_action`). It fails the same way again. A Ridgeway Travel Co. (fake) agent queue is open.
    User: "ok book it"
    Expect: The bot stops rendering the booking card, states the flight, time and fare in text, and offers a person: "I'm having trouble showing the booking screen. Here is the flight: Chicago to Denver, Friday, 1:40 p.m., $189. Want me to connect you with a Ridgeway agent? I'll pass this along so you don't have to repeat it."
    Failing reply: A third attempt at the same card, again with no "Book" button, and no offer of a person.

13. **No flights found (R6).**
    Setup: Ridgeway Trips (fake). The tool result for Saturday nonstops is an empty list.
    User: "any nonstops saturday"
    Expect: Plain text: "There are no nonstop flights to Denver on Saturday. Want one-stop options, or Friday nonstops instead?" No card.
    Failing reply: A `flight_card` with every field blank and a gray "Book" button.

14. **Do nothing special: optional field missing (R2, R10).**
    Setup: Ridgeway Trips (fake). The tool result for the 7:05 a.m. flight has every required field but no `aircraft` value, which is optional.
    User: "flights to denver friday"
    Expect: The `flight_card` renders normally, with the aircraft line left out. No fallback to text and no note about the missing aircraft.
    Failing reply: "I couldn't load all the flight details, so here's a text summary instead." (blocking a valid card over an optional field)

15. **Do nothing special: live status card updates (R10).**
    Setup: Ridgeway Trips (fake). The user has a booked trip and a `trip_status_card` showing "On time, Gate B12". The tool then reports a gate change to B20.
    User: "is my flight still on time"
    Expect: The card updates inside its reserved slot to "On time, Gate B20". Nothing around it moves. The text also says the gate changed.
    Failing reply: The card stays frozen at "Gate B12" because components are never changed after they appear, or the bot drops the card and answers in text only.

16. **Do nothing special: user asks for a different layout (R3, R5, R10).**
    Setup: Ridgeway Trips (fake). The bot showed a `flight_card` for the 7:05 a.m. flight.
    User: "can u show all of them side by side so i can compare"
    Expect: The bot shows a `price_table` with every Friday flight, as asked. This is a user request, not an unstable layout.
    Failing reply: "To keep things consistent, I can only show one flight card at a time."

17. **Do nothing special: refined request (R5, R10).**
    Setup: Ridgeway Trips (fake). The first request returned three `flight_card`s, one with a stop.
    User: "only nonstops"
    Expect: Two `flight_card`s with the same layout as before, showing only the nonstop flights. A shorter list after a filter is expected, not a consistency failure.
    Failing reply: The same three cards again, unchanged, because the bot treats any change in results for the same intent as an error.

## Cannot be judged from a transcript alone
- **The primary metric.** Component-schema validity needs a validation log for every rendered component across real traffic. The layout-shift measure needs layout-shift entries for the chat view, tied to message ids. Seventeen conversations do not measure either.
- **Layout shift and tap targets (R3, R8).** Whether text moved, and whether a control moved within 500 ms of a tap, needs a screen recording or layout-shift log, not the message text.
- **Whether validation ran (R2).** A transcript shows what rendered, not whether the schema check ran before render. Needs the `component.valid` log.
- **Screen reader labels (R7).** Needs the rendered component's accessibility tree, or a screen reader run.
- **What the hand-off passed (R9).** The receiving person's view shows whether the flight, time and fare arrived.
- **Whether the slot sizes and field order are right.** They are test settings from the pattern page's placeholder contract. Tune them on your own product.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |

## Related
- [Pattern page: Generative UI Instability](../goals/visual/failures/generative-ui-instability.md)
- [Rich-card misuse tests](rich-card-misuse.md)
- [Misleading generated visuals tests](misleading-generated-visuals.md)
- [Auto-scroll fights the reader tests](auto-scroll-fights-the-reader.md)
- [Accessibility gaps tests](accessibility-gaps.md)
- [Talk to a human ignored or looped tests](talk-to-a-human-ignored-or-looped.md)
- [Failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md)
- [Test file format](README.md)
