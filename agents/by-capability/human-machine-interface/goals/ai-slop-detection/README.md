# AI Slop Detection: Goal, Metrics, and Patterns

> **Goal:** People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do.

## Why this family exists
AI coding and design tools fill every blank they are not given with the most common answer they have seen. The result ships fast and looks like every other AI-built page: the same purple gradient, the same three cards, the same "Supercharge your workflow" hero, filler left in, and sometimes invented proof. Each pattern here names one of these tells, says why the tool produces it, and gives a prompt rule plus a pre-ship check the builder can run.

The first patterns cover web UI. Writing, code, image and data patterns are planned.

## How we measure it
Shared metrics the patterns below report against. Targets are proposed starting points to tune on your own data; no catalog row exists for this family yet.
| Metric | Target | Defined in |
|---|---|---|
| Flagged default-look screens shipped with no recorded reason | Under 10% (proposed) | [default gradient look](failures/ui-default-gradient-look.md) |
| Template card-grid rate | Under 10% of pages (proposed) | [template card grids](failures/ui-template-card-grids.md) |
| Hero specificity pass rate | 95% before ship (proposed) | [generic hero layout](failures/ui-generic-hero-layout.md) |
| Emoji-clean file rate | 100% (proposed) | [emoji as icons](failures/ui-emoji-as-icons.md) |
| Placeholder-free deploy rate | 100% (proposed) | [placeholder data left in](failures/ui-placeholder-data-left-in.md) |
| Unbacked social-proof elements at deploy | 0 (proposed) | [fabricated social proof](failures/ui-fabricated-social-proof.md) |

## Patterns
| Pattern | One line |
|---|---|
| [AI generated website purple gradient](failures/ui-default-gradient-look.md) | Purple gradients and frosted-glass cards because no brand tokens were given |
| [Identical card grids and icon-in-circle feature rows](failures/ui-template-card-grids.md) | Every feature gets the same card, so none stands out |
| [Stock hero copy and template section order](failures/ui-generic-hero-layout.md) | A headline any company could use, sections in template order |
| [Emoji as icons and decorative bullets](failures/ui-emoji-as-icons.md) | Rockets and sparkles on headings, bullets and buttons; screen readers read their names |
| [Placeholder data left in](failures/ui-placeholder-data-left-in.md) | Lorem ipsum, John Doe, 555 numbers and TODO text ship to production |
| [Fabricated social proof](failures/ui-fabricated-social-proof.md) | Invented testimonials, logos and user counts shipped as real. **Read this first: needs legal review.** |
| [Stock phrases in AI-written text ("delve")](failures/text-stock-phrases.md) | Words readers now read as AI-written, caught by a phrase-list scan before publishing |
| [Em dashes, lists of three and "not X, it's Y"](failures/text-rhythm-tells.md) | Sentence-shape tells, checked in combination, never one sign alone |
| ["It depends" answers that never pick](failures/text-balanced-non-answers.md) | Hedged, balanced text that leaves the reader to decide |
| [Headings, bold and bullets on everything](failures/text-uniform-structure.md) | Every genre gets the same report shape |
| [AI made-up citations and fake quotes](failures/text-invented-citations.md) | Cases, papers and quotes that do not exist, blocked at a citation gate. **Read this first: needs legal review.** |
| [Over-commented code and tutorial-style comments](failures/code-over-commented.md) | Comments that restate the code or talk to the chat |
| [AI code calls functions that don't exist](failures/code-nonexistent-apis.md) | Invented methods, keyword arguments, flags, config keys and packages, caught by resolving every new name before merge |

## Planned (not yet written)
- Code tells: needless abstraction and more
- Image and data tells

## Related
- [Conversation moves](../../solutions-library/conversation-moves.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
