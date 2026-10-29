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
| Register-match rate (published AI-drafted pieces with no unreviewed register flag against the writer's own baseline) | 95% (proposed) | [hedged list register](failures/text-hedged-list-register.md) |
| Receiver-ready rate (AI-assisted work products shared with colleagues that pass the 4-item send check) | 90%, alert below 80% (proposed) | [workslop](failures/work-workslop.md) |
| Anchored-critique rate (sampled AI-written reviews naming at least one issue tied to a line, section or number, or listing what was checked and found clean) | 95% (proposed) | [sycophantic feedback](failures/work-sycophantic-feedback.md) |
| Anchored-and-verified review rate (sampled reviews where every criticism names a location in the work and none is contradicted or cites a nonexistent source) | 95%, alert below 90% (proposed) | [AI peer reviews](failures/work-ai-peer-reviews.md) |
| Confirmed-claim rate (exported resume and cover-letter drafts where every skill, tool, number and title traces to candidate input the candidate confirmed) | 100% (proposed) | [undefendable resume claims](failures/hiring-undefendable-ai-resume-claims.md) |
| Process-evidence decision rate (AI-use findings on student or applicant essays recording a notice, the student's response and a decider other than the accuser) | 100% (proposed) | [AI essays](failures/education-ai-essays.md) |
| Provenance-tagged record rate (records with source, collection date and origin label / all records in a training run) | 100% (proposed) | [model collapse](failures/data-model-collapse-contamination.md) |
| Reviewed-before-index rate (translated pages published or indexed only after a fluent review of that language) | 100% (proposed) | [machine-translated duplicates](failures/data-machine-translated-duplicates.md) |
| Condition-labeled result rate (detector results shown with the input's size, re-compression and crop/screenshot condition; degraded low scores shown as "inconclusive") | 100% (proposed) | [image detector fragility](failures/detect-image-detector-fragility.md) |
| Scoped-negative rate (negative detector results shown with tested-generator list, last test date and "origin unknown, not proof of human origin" line) | 100% (proposed) | [unseen generators](failures/detect-unseen-generator-failure.md) |
| Group-audited detector rate (detectors in use with a current per-group, per-length false-positive audit on local known-human writing) | 100% before go-live (proposed) | [biased false positives](failures/detect-biased-false-positives.md) |
| Gated release rate (releases and publishes that passed the full slop gate or carry a recorded override) | 100% (proposed) | [no release gate](failures/detect-no-release-gate.md) |
| Scoped text-watermark result rate (results shown with state, length and edit caveat, never an authorship verdict) | 100% (proposed) | [text watermark erased](failures/provenance-text-watermark-erased.md) |
| Unreviewed young-or-unlisted dependency rate (new dependencies that are young, from a single-package publisher or off the allowlist, merged with no review) | 0 (proposed) | [slopsquatting](failures/code-slopsquatting.md) |
| Tagged-and-scanned AI change rate (merged AI-written changes with a provenance trailer or label and a passing security scan) | 100% (proposed) | [untracked AI vulnerabilities](failures/code-untracked-ai-vulnerabilities.md) |
| Ungated new-package run rate (agent installs of names not in lockfile/allowlist with no lookup and human yes) | 0 (proposed) | [agent installs hallucinated packages](failures/code-agent-installs-hallucinated-packages.md) |
| Flagged-source-only fact rate (news claims stated as fact when every cited source is unrated or flagged) | 0 (proposed) | [AI content farms posing as news](failures/web-ai-content-farms-as-news.md) |
| Unreviewed flagged-domain spend share (open-web spend on flagged domains with no reviewed decision / all open-web spend, weekly) | Under 1% (proposed) | [ads fund content farms](failures/web-ads-fund-content-farms.md) |
| Labeled-or-held rate (recommended artists failing the profile check shown with a plain-words label or held back) | 100% (proposed) | [fake AI artists](failures/music-fake-ai-artists.md) |
| Reviewed-before-payout rate (flagged tracks whose royalties were held and decided by a named human before the payout run) | 100% (proposed) | [AI music stream fraud](failures/music-ai-stream-fraud.md) |
| Undeclared-AI catch rate (sampled posts judged AI-made that carry an AI label from any source) | 90% (proposed) | [self-declared labels](failures/provenance-self-declared-labels.md) |
| Evidence-only report rate (suspected AI persona reports with two linked behavior signals, "suspected, not confirmed", a named human decider and no verdict words) | 100% (proposed) | [covert AI persuasion accounts](failures/social-covert-ai-persuasion-accounts.md) |

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
| [AI writing style: "-ing" clauses, abstract nouns and "including" lists](failures/text-hedged-list-register.md) | AI drafts slip into a dense report voice even when told to match a style; compare grammar rates with your own baseline before publishing |
| [Workslop: AI work that looks finished but makes more work](failures/work-workslop.md) | Memos, decks and summaries with no ask, no conclusion and unsourced numbers push the real work onto the receiver; a 4-item send check stops them |
| [Sycophantic AI feedback: reviews that only agree](failures/work-sycophantic-feedback.md) | AI reviews of plans, code and drafts echo what the author signals they like and get forwarded as sign-off; every review names an anchored issue or says what was checked |
| [AI-written peer reviews of papers and code](failures/work-ai-peer-reviews.md) | Fluent AI reviews miss the paper or the diff; anchor every point to the work, check it there, and keep the verdict with a named human |
| [AI resume claims candidates can't defend in the interview](failures/hiring-undefendable-ai-resume-claims.md) | AI tools add skills, numbers and titles the candidate never gave; write only confirmed claims, and employers check claims by asking, not by detector score. **Read this first: needs legal review.** |
| [AI-written student and admissions essays: penalized or missed](failures/education-ai-essays.md) | Schools act on a score or a hunch, penalizing honest students while lightly edited AI essays pass; use drafts, version history and an oral follow-up, and keep accuser and decider apart. **Read this first: needs legal review.** |
| [Model collapse: training on AI-generated data](failures/data-model-collapse-contamination.md) | Retraining on scraped or user data that is increasingly AI-written loses rare cases; tag provenance and keep a human reference set |
| [Machine-translated duplicate pages: sites auto-translated with no fluent review](failures/data-machine-translated-duplicates.md) | AI agents mass-translate sites into many languages with no fluent review; publish only reviewed languages and filter text found in many MT languages from datasets |
| [AI image detector says "real" after a screenshot: detectors break after crop, resize or recompress](failures/detect-image-detector-fragility.md) | Screenshots, crops, resizes and re-saves wipe the traces detectors read; results name the copy's condition and a low score on a degraded copy is "inconclusive" |
| [AI detector says "human" on new AI models: unseen generators](failures/detect-unseen-generator-failure.md) | Detectors trained on older generators score new-model images and text as human; show the tested generators and date, word low scores "not detected", and check the source |
| [AI detectors biased against English learners and Black students](failures/detect-biased-false-positives.md) | Detectors and teachers falsely flag English learners, Black students and short texts more often than others; audit false flags per group and length on local human writing. **Read this first: needs legal review.** |
| [AI slop checks run once, not on every release](failures/detect-no-release-gate.md) | Slop checks run once at launch or only warn in CI, so placeholders, chatbot leftovers and fake citations come back; run one suite on every path, block on errors, record every override |
| [Can a text watermark survive paraphrasing? Text watermarks erased by rewrites](failures/provenance-text-watermark-erased.md) | Paraphrase, translation or rewording erases text watermarks and marks can be forged; show state and length, never "human-written," decide nothing on the mark alone. **Read this first: needs legal review.** |
| [Slopsquatting: attackers register package names AI keeps inventing](failures/code-slopsquatting.md) | Attackers register package names AI tools keep inventing, so "exists on npm" passes; a gate holds young, unlisted packages and a scan cleans invented install commands from docs and skills |
| [AI-generated code vulnerabilities with no record AI wrote them](failures/code-untracked-ai-vulnerabilities.md) | AI-written code with known flaws merges with no record that AI wrote it; tag every AI commit and PR, and block merge until a security scan passes. **Read this first: needs legal review.** |
| [AI agent installs a package that doesn't exist](failures/code-agent-installs-hallucinated-packages.md) | Agents and skills run npm/npx/pip installs with no one reading the name; a gate holds every name not in the lockfile or allowlist for a registry check and a human yes |
| [AI content farms posing as local news sites](failures/web-ai-content-farms-as-news.md) | Chatbots, aggregators and RAG pipelines cite AI content farms posing as local papers; check domain history, leftovers and bylines, and never state a claim as fact from unverified sites alone. **Read this first: needs legal review.** |
| [Brand ads on AI-generated sites: programmatic buying funds content farms](failures/web-ads-fund-content-farms.md) | Open-exchange buys pay AI content farms the advertiser never picked; buy from an inclusion list, check the seller path, review placements weekly, and lead every campaign summary with flagged spend. **Read this first: needs legal review.** |
| [Is this band AI? Fake AI music artists with huge catalogs and no history](failures/music-fake-ai-artists.md) | Recommenders and music assistants surface AI-made "artists" with dozens of tracks in weeks, no members and no shows as real bands; check the profile and catalog, then label in plain words or hold them back. **Read this first: needs legal review.** |
| [AI music streaming fraud: bots play mass-uploaded AI tracks for royalties](failures/music-ai-stream-fraud.md) | Bot accounts spread plays across thousands of AI tracks to drain the royalty pool; flag on upload, play and account behavior, hold the payout for a named reviewer, and never word a flag as an accusation. **Read this first: needs legal review.** |
| [Why isn't this AI video labeled? Platforms rely on self-declared AI labels](failures/provenance-self-declared-labels.md) | Platforms label AI mostly when the uploader ticks a box, so undeclared AI posts look real; combine the box with provenance, detectors and review, and word "no label" as "not declared," never "human-made." **Read this first: needs legal review.** |
| [AI bots posing as real people on Reddit: covert persuasion accounts](failures/social-covert-ai-persuasion-accounts.md) | AI accounts invent identities ("as a trauma counselor") and tailor persuasive forum replies without disclosure, as in the Zurich r/changemyview experiment; never deploy them, and moderation tools report linked behavior signals as "suspected, not confirmed" for a human to decide. **Read this first: needs legal review.** |

## Planned (not yet written)
- More text, code, voice, video and provenance tells; detector accuracy, humanizers and false accusations

## Related
- [Conversation moves](../../solutions-library/conversation-moves.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
