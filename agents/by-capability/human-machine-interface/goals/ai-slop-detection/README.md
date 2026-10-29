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
| Caveated-flag rate (detector results shown with error rate, "not proof" note and human review) | 100% (proposed) | [detector false positives](failures/detect-detector-false-positives.md) |
| Re-tested rule rate (rules re-tested against the current model version) | 100% within 7 days of a model change (proposed) | [detection rules decay](failures/detect-rules-decay.md) |
| Flagged default-type or forced-dark screens shipped with no recorded reason | Under 10% (proposed) | [default type and palette](failures/ui-default-type-and-palette.md) |
| Flagged neon-and-glow screens shipped with no recorded reason | Under 10% (proposed) | [neon and aurora glow](failures/ui-neon-aurora-glow.md) |
| Distinctiveness check pass rate at launch | 100% (proposed) | [visual convergence](failures/ui-visual-convergence.md) |
| Merged UI pull requests adding raw values outside the token file | 0%, alert above 2% (proposed) | [no locked design tokens](failures/ui-no-locked-design-tokens.md) |
| Clean-ending rate | 95% (proposed) | [stated-moral endings](failures/text-stated-moral-endings.md) |
| Evidence-complete flag rate (three independent tells plus a context check) | 100% (proposed) | [folk tells are not evidence](failures/text-folk-tells-unreliable.md) |
| Grounded-detail rate (first-hand claims traced to a person's notes, photos or test log) | 95% (proposed) | [no first-hand detail](failures/text-no-firsthand-detail.md) |
| Leftover escape rate (published articles later found to contain chatbot leftover text, per 1,000 published) | 0 (proposed) | [AI text in scientific papers](failures/text-ai-in-scientific-papers.md) |
| Policy-compliant outside PR rate | 100%, alert below 95% (proposed) | [AI pull request flood](failures/code-ai-pr-flood.md) |
| Reproduction-backed report rate | 100% (proposed) | [fake vulnerability reports](failures/code-fake-vulnerability-reports.md) |
| Unapproved person-naming publication rate (agent posts naming a person after a rejection, with no operator approval) | 0 (proposed) | [bot retaliation on maintainers](failures/code-bot-retaliation-on-maintainers.md) |
| Verified-before-action rate (voice-triggered actions with a logged out-of-band check) | 100% (proposed) | [cloned voice tells](failures/audio-cloned-voice-tells.md) |
| No-signal labeling rate (no-manifest checks shown as "origin unknown") | 100% (proposed) | [provenance metadata stripped](failures/provenance-metadata-stripped.md) |
| Scoped-result rate (watermark results shown with the detectors run, the generators not covered and a "not proof of human origin" line) | 100% (proposed) | [vendor-locked watermarks](failures/provenance-vendor-locked-watermarks.md) |
| Evidence-reviewed action rate (AI-use actions on reported work taken only after a private evidence request and a named second reviewer) | 100% (proposed) | [false accusations by readers](failures/detect-false-accusations-by-readers.md) |
| Independently checked detector rate (detectors measured on the buyer's own labeled sample, with a 95% range, re-tested since the last update) | 100% before go-live (proposed) | [unverified accuracy claims](failures/detect-unverified-accuracy-claims.md) |
| Meaning-kept rewrite rate (rewrites after a humanize or bypass request that keep every name, number, date, quote and citation and add no new errors) | 100% (proposed) | [humanizer arms race](failures/detect-humanizer-arms-race.md) |
| Source-checked clip rate (clips aired, kept up as news or approved as ads with a logged source check) | 100% (proposed) | [synthetic clips as real](failures/video-synthetic-clips-as-real.md) |
| Measured-word rate (active list words with an excess ratio measured on the current drafting model) | 100% within 7 days of a model change (proposed) | [word list drift](failures/text-word-list-drift.md) |

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
| [AI images with extra fingers and garbled text](failures/image-visual-artifacts.md) | Six fingers, misspelled signs and melted background detail posted by mistake, caught by a pre-publish checklist |
| [AI code duplication and over-engineering](failures/code-needless-abstraction.md) | Wrappers, one-implementation interfaces and re-written helpers, caught by a search-before-write rule and a duplication check |
| [Why AI images look fake: waxy skin and wrong shadows](failures/image-stock-look.md) | Over-smooth, glossy stock-photo images with impossible light, caught by art direction and a lighting check before publishing |
| [AI made-up numbers in reports and dashboards](failures/data-too-clean.md) | Round, too-clean figures with no source, caught by tracing every number to a query or citation |
| [AI generated reviews and replies that all sound the same](failures/data-templated-reviews.md) | Review farms and reply bots in one templated voice, caught by near-duplicate checks. **Read this first: needs legal review.** |
| [AI detector false positives (Turnitin, GPTZero)](failures/detect-detector-false-positives.md) | Detector scores flag real human writing, often English learners'; scores show their error rate and a person decides |
| [AI detection rules stop working after a model update](failures/detect-rules-decay.md) | Phrase lists, regex and classifiers quietly stop catching anything after the generating model changes |
| [Inter font, indigo accents and forced dark mode](failures/ui-default-type-and-palette.md) | Default font, off-token accent and dark mode that ignores the user's setting |
| [Neon glow on dark backgrounds and aurora blobs](failures/ui-neon-aurora-glow.md) | Neon text and borders on near-black over blurred blobs, checked for contrast, blur cost and motion |
| [Why all AI websites look the same](failures/ui-visual-convergence.md) | Unrelated sites built with the same tools and kits converge on one look; a pre-launch distinctiveness check catches it |
| [AI ignores my design system: no locked tokens](failures/ui-no-locked-design-tokens.md) | With no locked token file, AI tools invent colors, spacing and radius per page; lint catches raw values |
| [Why AI always ends with a summary or a moral](failures/text-stated-moral-endings.md) | Posts, emails and stories end on "Ultimately" or a stated lesson; end on the last fact instead |
| [Does using em dashes mean AI wrote it?](failures/text-folk-tells-unreliable.md) | One em dash or "delve" is not proof; flags need three independent tells, a context check and a record |
| [Why does AI writing feel generic? No first-hand detail](failures/text-no-firsthand-detail.md) | Fluent reviews and guides with nothing the writer saw or tested; feed in real notes, never invent experience, block publishing until a detail is traced |
| [ChatGPT text in scientific papers and AI detector desk rejections](failures/text-ai-in-scientific-papers.md) | "Regenerate response" and "As an AI language model" reach print while journals reject on detector scores; scan for leftovers at submission and proof, never reject on a score alone |
| [AI generated pull requests flood open source maintainers](failures/code-ai-pr-flood.md) | Agents open unrequested, undisclosed PRs that ignore project rules; a pre-open gate checks the AI policy, an accepted issue, disclosure, tests and the user's yes |
| [AI generated bug bounty reports and fake CVEs](failures/code-fake-vulnerability-reports.md) | AI-written security reports for flaws that do not exist, as at curl, caught by requiring a reproduction on an unmodified release |
| [AI agent attacks maintainer after PR rejected](failures/code-bot-retaliation-on-maintainers.md) | An agent's PR is closed and it publishes a post accusing the maintainer of prejudice; a publish gate holds any text naming a person for operator approval. **Read this first: needs legal review.** |
| [How to tell if a voice is AI cloned](failures/audio-cloned-voice-tells.md) | Breaths, flat tone and room noise don't show a voice is real or cloned; verify by callback or source check before paying, changing an account or publishing. **Read this first: needs legal review.** |
| [No Content Credentials doesn't mean it's real](failures/provenance-metadata-stripped.md) | Re-saves, screenshots and uploads strip C2PA and IPTC AI labels; tools show a missing manifest as "origin unknown," never "authentic" |
| [SynthID says "no watermark found": vendor-locked watermarks](failures/provenance-vendor-locked-watermarks.md) | Each watermark checker reads only its own vendor's marks; report which detectors ran and what they can't see, and treat "none found" as unknown, never "not AI". **Read this first: needs legal review.** |
| [Falsely accused of using AI: reader and fan pile-ons](failures/detect-false-accusations-by-readers.md) | Crowds report real artists, writers and photographers as AI; reports are claims, the creator is asked privately for process evidence, and clearing is public |
| [Are AI detectors really 99% accurate?](failures/detect-unverified-accuracy-claims.md) | Buyers adopt detectors on vendor-reported accuracy; label the figure and test on your own labeled sample first. **Read this first: needs legal review.** |
| [Do AI humanizers work? Humanizer tools make writing worse](failures/detect-humanizer-arms-race.md) | Humanizers reword AI text to dodge detectors, adding typos and fact errors, while detectors retrain to flag them; edit for the reader, keep facts, show drafts |
| [How to tell if a video is AI generated: fake clips passed off as news](failures/video-synthetic-clips-as-real.md) | Reviewers clear AI clips of storms, bodycam stops and "news" segments because they look real or lack a watermark; the look never decides, a logged source check does. **Read this first: needs legal review.** |
| ["Delve" frequency over time: AI word lists go stale](failures/text-word-list-drift.md) | Each model version overuses different words and people adopt the old ones, so a word list is measured per model and re-measured, human baseline included |

## Planned (not yet written)
- More text, code, voice, video and provenance tells; detector accuracy, humanizers and false accusations

## Related
- [Conversation moves](../../solutions-library/conversation-moves.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
