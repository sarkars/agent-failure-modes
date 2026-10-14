# Roadmap: Visual Design and Human-Oversight UI Failures

> **Family goal:** What an agent shows is clear, honest, accessible, and appropriate to the stakes, and people overseeing an agent can see what it's doing and stop it.

**Grounding (verified):**
- **System status:** about 10 s is the limit for holding attention, so longer waits need progress feedback (Miller 1968; Nielsen 1993).
- **Dark patterns:** the FTC's September 2022 staff report treats hard-to-cancel flows as a dark pattern, including cancellation mazes. I did not verify the report's full list of tactics.
- **Accessibility:** WCAG 2.2 sets a minimum pointer target of 24 by 24 CSS pixels (SC 2.5.8, Level AA), with exceptions. I did not verify the contrast criterion (SC 1.4.3) in this research; check the W3C page before citing it.
- **Human oversight:** automation complacency and bias occur in experts as well as novices, and aren't prevented by training or instructions (Parasuraman & Manzey, 2010).

Flags: **V** verified source · **R** needs research · **L** legal review · **E** expert review. See the [roadmap README](README.md). The [visual placeholder](../modalities/visual/README.md) lists the first eight in short form.

## A. Visual design
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags |
|---|---|---|---|---|---|
| VI-01 | Cognitive overload | Too many options, cards, or text at once | The user can decide without being overwhelmed | Time to first action; options per screen against a target set from user tests; abandonment | R |
| VI-02 | No clear primary action | A screen has no obvious next step, or several competing ones | Each screen has one clear primary action | Screens with exactly one primary action. Target: 100%; dead-end screen rate | |
| VI-03 | Dark patterns | Hard-to-cancel flows, confirmshaming, hidden fees, forced continuity | Users can say no, cancel, and complain as easily as they said yes | Steps to cancel vs. steps to subscribe (parity); dark-pattern audit pass rate | V, L |
| VI-04 | Accessibility gaps | Poor contrast, missing text alternatives, no keyboard or screen-reader support | Critical flows meet WCAG 2.2 AA | Automated plus manual WCAG 2.2 AA pass rate on critical flows. Target: 100% | V, L, E |
| VI-05 | Motion and flashing harm | Animation or flashing triggers vestibular or seizure problems | Motion is minimal, and reduced-motion settings are respected | Reduced-motion honoured. Target: 100%; flashing content: 0 (verify the WCAG threshold) | E, R |
| VI-06 | Colour-only encoding | Meaning depends on colour alone | Information is understandable without colour | Items conveyed without colour. Target: 100% | E |
| VI-07 | Small targets and small screens | Tiny tap targets, overflow, horizontal scrolling | Controls are usable on phones | Target-size pass rate (WCAG 2.5.8); horizontal-scroll rate | V |
| VI-08 | Misleading generated visuals | Invented product images or charts that don't match the data | Generated visuals are labelled and faithful to the source | Generated-visual disclosure. Target: 100%; chart-to-source mismatches: 0 | L |
| VI-09 | Unlabelled synthetic faces and avatars | AI faces, voices, or avatars with no AI label | Synthetic content is clearly marked | AI label present. Target: 100% | L |
| VI-10 | Avatar overpromising | A humanlike avatar suggests abilities the bot lacks | Appearance matches capability | Capability-expectation mismatch rate in user tests | R |
| VI-11 | Rich-card misuse | Cards where text is faster, or text where cards are needed | The format fits the task | Task time by format; format-fit audit score | |
| VI-12 | Sensitive-data forms | No hosted fields or masking; errors leak data | Sensitive fields use protected components | Sensitive fields on hosted components. Target: 100% (see the [channel pattern](../channel-selection/failures/sensitive-data-collected-in-chat.md)) | L |
| VI-13 | Stakes-blind visual style | Confetti or playful styling on a denial or a bereavement | Visual style follows the stakes | Style-by-stakes compliance on audited screens | |
| VI-14 | Misleading charts | Truncated axes or misleading scales | Charts represent the data fairly | Chart-lint pass rate; misread rate in user tests | |
| VI-15 | Missing loading, empty, and error states | Blank screens or spinners with no explanation | Every async view has loading, empty, and error states | States defined on 100% of async views; blank-screen rate 0 | V |
| VI-16 | Generative UI instability | Layouts shift or components vary unpredictably | Generated interfaces are stable and valid | Layout-shift measure; component-schema validity. Target: 100% | R |
| VI-17 | Visuals that don't localise | Icons, colours, gestures, or mirrored layouts confuse in other locales | Visuals work in each supported locale | RTL render pass; icon comprehension in test locales | R |
| VI-18 | Notification overload | Too many pushes or alerts | Notifications are rare, useful, and controllable | Notifications per user per week; opt-out rate | L |
| VI-19 | Manipulated consent UI | Accept is prominent and reject is hidden | Accept and reject have equal prominence | Prominence parity. Target: 100% | L |
| VI-20 | Fake urgency and trust cues | Countdown timers, "3 people viewing", or fake badges | No fabricated urgency or credibility cues | Fabricated urgency or trust elements. Target: 0 | L |

## B. Human oversight of agents
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags |
|---|---|---|---|---|---|
| OV-01 | Approval fatigue | Reviewers click "approve" without reading | Approvals that people actually evaluate | Catch rate on seeded errors; approvals under a minimum read time; override rate. Grounded in automation-complacency research | V |
| OV-02 | Hidden agent actions | The user can't see what the agent did | Every agent action is visible and searchable | Action-log coverage. Target: 100%; users able to find action history in tests | |
| OV-03 | No undo for consequential actions | Irreversible actions run without a confirmation or an undo | Consequential actions are reversible or confirmed | Reversible-or-confirmed share of consequential actions. Target: 100%; undo success rate | |
| OV-04 | Poor action previews | The approval screen doesn't show the consequence | The user sees the effect before approving | Previews on 100% of consequential actions; post-approval regret rate | |
| OV-05 | Miscalibrated confidence display | Everything looks equally certain, or uncertainty is hidden | Confidence shown matches how often the agent is right | Calibration error of displayed confidence | R |
| OV-06 | No provenance | Claims appear without sources | Factual claims link to their sources | Citation presence on high-stakes claims. Target: 100%; source click-through | |
| OV-07 | Invisible long-running status | A task runs for minutes with no status | Tasks over about 10 s show progress, and stalls are detected | Status shown on 100% of tasks over 10 s; stall-detection time | V |
| OV-08 | No stop or takeover | The user can't interrupt the agent or take control | Stop and takeover always work | Time from stop request to halt; takeover success rate | |
| OV-09 | Permission fatigue or under-asking | Too many prompts, or too few for risky actions | Ask for permission in proportion to risk | Prompts per task; unnecessary-prompt rate; unauthorised actions (target 0) | |
| OV-10 | Misleading explanations | The stated reason isn't the real reason | Explanations reflect what actually drove the decision | Explanation-faithfulness audit score | R |
| OV-11 | No audit trail | Nobody can tell who or what decided | Decisions record the actor, time, and reason | Decisions with actor, time, and reason. Target: 100% | L |
| OV-12 | Confusion over who is acting | In multi-agent UIs, users can't tell which agent or person acted | The acting party is always clear | Users who correctly identify the acting party in tests. Start: over 90% | |
