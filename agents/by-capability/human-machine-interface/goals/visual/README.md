# Visual: Goal, Metrics, and Patterns

> **Goal:** What an agent shows is clear, honest, accessible, and appropriate to the stakes.

## Why this family exists
An assistant's buttons, prices, and cancel paths shape what a user does as much as its words do. This family covers failures in what the assistant shows and how it frames a choice.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Cancel-to-subscribe step parity | Cancel steps at or below subscribe steps, same medium | [dark patterns](failures/dark-patterns.md) |
| Time to first action | Set from your baseline | [cognitive overload](failures/cognitive-overload.md) |
| Decision messages and cards with exactly one primary action | Set from your baseline | [no clear primary action](failures/no-clear-primary-action.md) |
| WCAG 2.2 AA pass rate on critical flows | 100% (starting point) | [accessibility gaps](failures/accessibility-gaps.md) |
| Animations that respect reduced motion | 100% (starting point) | [motion and flashing harm](failures/motion-and-flashing-harm.md) |
| Status items with a non-color cue | 100% (starting point) | [colour-only encoding](failures/colour-only-encoding.md) |
| Target-size pass rate (WCAG 2.5.8) | 100% (starting point) | [small targets and small screens](failures/small-targets-and-small-screens.md) |
| Generated visuals labeled AI-generated | 100% (starting point) | [misleading generated visuals](failures/misleading-generated-visuals.md) |
| Capability-expectation mismatch in user tests | under 10% (starting point) | [avatar overpromising](failures/avatar-overpromising.md) |
| Format-fit rate on audited turns | 95% (starting point) | [rich-card misuse](failures/rich-card-misuse.md) |
| Chart-lint pass rate | 100% (starting point) | [misleading charts](failures/misleading-charts.md) |
| States defined on async views | 100% of async views; blank-screen rate 0 | [missing loading, empty and error states](failures/missing-loading-empty-and-error-states.md) |
| Rendered components passing schema; layout-shift score | 100%; 0.1 or less (starting point) | [generative UI instability](failures/generative-ui-instability.md) |
| RTL render pass | 100% (starting point) | [visuals that don't localise](failures/visuals-that-don-t-localise.md) |
| Notifications per user per week; opt-out rate | Cap per type from baseline (starting point) | [notification overload](failures/notification-overload.md) |
| Prominence parity | 100% of consent prompts (starting point) | [manipulated consent UI](failures/manipulated-consent-ui.md) |
| Fabricated urgency or trust elements | 0 | [fake urgency and trust cues](failures/fake-urgency-and-trust-cues.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Dark patterns](failures/dark-patterns.md) | Guilt-trip buttons, buried prices, and long cancel paths make "no" cost more than "yes" |
| [Cognitive overload](failures/cognitive-overload.md) | Too many options, cards, or text at once make the user stall; cap the choices and lead with a pick |
| [No clear primary action](failures/no-clear-primary-action.md) | A reply or card ends with no obvious next step, or several equal buttons |
| [Accessibility gaps](failures/accessibility-gaps.md) | The chat widget, cards and generated visuals fail contrast, text-alternative, focus and announcement checks, so critical flows fail WCAG 2.2 AA |
| [Motion and flashing harm](failures/motion-and-flashing-harm.md) | Unrequested animation, auto-playing GIFs and flashing that ignore reduce-motion settings can cause dizziness or seizure risk |
| [Colour-only encoding](failures/colour-only-encoding.md) | Status chips, charts and tables carry meaning by color alone, so color-blind and screen-reader users miss it |
| [Small targets and small screens](failures/small-targets-and-small-screens.md) | Chips, card buttons and carousels too small or crowded to tap on a phone cause mis-taps and unreadable options |
| [Misleading generated visuals](failures/misleading-generated-visuals.md) | An AI-generated render, diagram or chart looks like the real product or data and the user acts on it |
| [Avatar overpromising](failures/avatar-overpromising.md) | A human photo, title or emotive persona makes users expect understanding or authority the assistant lacks |
| [Rich-card misuse](failures/rich-card-misuse.md) | Cards, carousels or buttons where a plain sentence is faster, or buttons that miss the user's need |
| [Misleading charts](failures/misleading-charts.md) | Charts that start above zero, stretched scales and mismatched axes make a small gap look large; start bars at zero, label any cut, print the values |
| [Missing loading, empty and error states](failures/missing-loading-empty-and-error-states.md) | A card, list or widget shows a blank box or endless spinner, so the user cannot tell if it is loading, empty or failed |
| [Generative UI instability](failures/generative-ui-instability.md) | Model-chosen cards that shift layout, vary between identical requests or arrive broken; closed component list, schema check, text fallback |
| [Visuals that don't localise](failures/visuals-that-don-t-localise.md) | Icons, arrows, colors and layouts built for one locale confuse users in others; mirror only direction icons, label every icon, test each locale |
| [Notification overload](failures/notification-overload.md) | Too many pushes, badges and digests get the assistant muted; cap the weekly volume, ask first, label urgency honestly, one switch per type |
| [Manipulated consent UI](failures/manipulated-consent-ui.md) | Accept is large and one tap while Reject is small, buried or missing, so consent is not a real choice |
| [Fake urgency and trust cues](failures/fake-urgency-and-trust-cues.md) | Countdown timers that reset, made-up viewer or stock counts and badges nobody awarded; show a cue only when a logged source proves it true now |

## Planned (not yet written)
The rest of the family is listed in the [roadmap](../../roadmap/visual-and-oversight.md).

## Related
- [Accessibility](../accessibility/README.md): what screen-reader and keyboard users get
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
