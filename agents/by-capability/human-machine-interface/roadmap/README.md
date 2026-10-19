# HMI Roadmap: Catalog of Patterns, Goals, and Metrics

> **Status: an exhaustive catalog, not written patterns.** Each row names a failure, the goal it protects, and a primary metric with a starting target. The library today has **14 written HMI patterns** (see the [area README](../README.md)) plus about 1,280 older patterns elsewhere in `agents/`. This catalog is checked against that library.

> **Execution plan.** The order in which these get written, and the procedure a scheduled run follows (patterns every hour, each held to a quality gate), is in [execution-plan.md](execution-plan.md). The catalog tables stay the source of goals and metrics.

## Audit: what already exists
The first version of this roadmap did not check the library, and several rows turned out to duplicate existing patterns (voice turn-taking, ASR names and noise, sycophancy, and more). This version checks **every row** against the library, by file name and keyword search across all failure files, and by reading the closest matches. The last column of each table says what I found:

| Label | Meaning | What to do |
|---|---|---|
| **Covered** | A pattern already exists | Don't write a new one. Link to it. |
| **Extends** | An existing pattern covers the technical failure | Write only the experience or design angle and a fix, and link to the existing pattern |
| **New** | No matching pattern found by file-name and keyword search | Search again before writing. This is a name-and-keyword check, not a full read of every file |

<!-- BEGIN:result -->
**Result: 493 rows, of which 30 are Written, 214 are New, 188 Extend an existing pattern, and 61 are already Covered.**
<!-- END:result -->

<!-- BEGIN:root-cause -->
## Root cause and the model question
Every row carries two extra labels: its **primary root cause**, and whether **a better model alone would fix it**. They are my judgments, one label per row, not measurements. The catalog leans toward human-interface, design, and policy failures, so a catalog of raw model failures would show a higher model share.

| Primary root cause | Rows | Share |
|---|---|---|
| Model: a stronger model plausibly reduces it | 119 | 24% |
| Reliability: state, verification, enforcement, evals, latency | 120 | 24% |
| Business context: your data, entitlements, rules, workflows, UX | 193 | 39% |
| Governance: incentives, law, and decisions | 61 | 12% |

| Better model alone? | Rows | Share |
|---|---|---|
| Yes, largely | 6 | 1% |
| Partly: helps, residual remains | 192 | 39% |
| No: persists with a perfect model | 295 | 60% |

If every "Partly" were solved, models would fix up to 40%. If none were, 1%. A one-page list of all rows is in the [index](index.md).
<!-- END:root-cause -->

## Before writing any pattern
1. Search the library for the topic (file names and keywords, under `agents/`).
2. Read the closest existing pattern.
3. If it's **Covered**, add a link and stop. If it **Extends**, write only the new angle. If it's **New**, write it with the [pattern template](../_templates/hmi-pattern.md).
4. Update the row's status here.

## How to read the tables
- **Targets are starting points to tune on your own data.** Where a number comes from a source, the Flags column says so.
- **Flags:** **V** grounded in a source I verified in research for this catalog · **R** needs more research before writing · **L** needs legal review · **E** needs expert review (clinical, accessibility, linguistics).
- **IDs** are stable handles for planning, not file names.

## What's in the catalog
<!-- BEGIN:catalog-table -->
| File | Area | Rows | Written | New | Extends | Covered |
|---|---|---|---|---|---|---|
| [chat-and-core.md](chat-and-core.md) | Remaining chat and core families, plus channel selection | 21 | 2 | 13 | 5 | 1 |
| [embedded-copilots.md](embedded-copilots.md) | Embedded copilots: upselling, context, first response, obvious questions | 23 | 8 | 5 | 9 | 1 |
| [response-time.md](response-time.md) | Speed, waiting, and pacing, all channels | 14 | 2 | 5 | 6 | 1 |
| [response-structure-and-length.md](response-structure-and-length.md) | Reply structure, length, chunking, and closers such as 'ok' and 'bye' | 18 | 2 | 8 | 8 | 0 |
| [language-and-locale.md](language-and-locale.md) | Language, reading level, and locale | 16 | 0 | 8 | 7 | 1 |
| [conversation-frameworks.md](conversation-frameworks.md) | Sales, support, style matching, and other frameworks | 32 | 0 | 19 | 12 | 1 |
| [voice.md](voice.md) | Voice agents: timing, speaking, safety, and bridging channels | 24 | 1 | 7 | 7 | 9 |
| [voice-listening-and-transcription.md](voice-listening-and-transcription.md) | Voice listening and transcription | 22 | 0 | 4 | 11 | 7 |
| [privacy-governance-and-access.md](privacy-governance-and-access.md) | Privacy, governance, ethics, access control, and external services | 42 | 0 | 6 | 13 | 23 |
| [effort-completeness-and-memory.md](effort-completeness-and-memory.md) | Effort, completeness, and memory | 25 | 3 | 3 | 9 | 10 |
| [emerging-surfaces.md](emerging-surfaces.md) | Emerging surfaces: agentic commerce, browser agents, tool ecosystems, meetings, companions, hiring, pricing incentives | 25 | 0 | 7 | 15 | 3 |
| [visual-and-oversight.md](visual-and-oversight.md) | Visual design and human-oversight UI for agents | 32 | 0 | 17 | 12 | 3 |
| [agent-types.md](agent-types.md) | Failures by agent type (coding, data, IT, finance, healthcare, and more) and cross-agent additions | 61 | 1 | 26 | 33 | 1 |
| [conversation-design.md](conversation-design.md) | Dialogue mechanics, refusals and boundaries, and error recovery | 33 | 6 | 12 | 15 | 0 |
| [interface-and-persona.md](interface-and-persona.md) | Persona and tone, onboarding, chat interface, accessibility, and multimodal input | 41 | 0 | 30 | 11 | 0 |
| [handoff-measurement-and-operations.md](handoff-measurement-and-operations.md) | Human handoff, measurement, model changes, proactive agents, and group chats | 28 | 3 | 16 | 9 | 0 |
| [service-and-vertical-patterns.md](service-and-vertical-patterns.md) | Drive-thru, in-car, government, travel, banking, insurance, health scheduling, real estate, and outbound rules | 36 | 2 | 28 | 6 | 0 |
| | **Total** | **493** | **30** | **214** | **188** | **61** |
<!-- END:catalog-table -->

## Suggested priority
> Superseded for ordering by the execution plan. Kept here as the original rationale.

| Tier | Why | Start with |
|---|---|---|
| 1 | High harm, evidence exists, and the library has a gap | Generic first response · re-asking known information · forced re-login · help that turns into a sales pitch · purchases without clear authorisation · browser-agent hijacking · lazy completion and deferring work to the user · no warning of context loss · skipped steps with no receipt · transcription hallucination · non-speech heard as speech · names with no repair path · acknowledgments and closers (RS-14 to RS-16) · answer buried and wall of text · scam victims and romantic or parasocial dependence · slow first response and silent long waits · dark patterns · approval fatigue · pitching before discovery · per-resolution pricing incentives |
| 2 | Common failures with solid frameworks, or conversation-facing governance gaps | Remaining sales, support, and style-matching patterns · privacy-rights requests · memory the user can't see or control · weak identity verification · denial messages that leak · locale formatting · reading level · accessibility |
| 3 | Valuable but needs more research or expert input | Emotion inferred from voice · explanation faithfulness · regional styles · pacing and "natural delay" research · sensitive-category inference |

## Framework and source register
"Verified" means I confirmed the source exists and its basic claims through search, usually via secondary summaries. It does not mean the framework is proven to work for chatbots. Most were developed for human-to-human settings.

| Framework or source | Domain | Status |
|---|---|---|
| SPIN Selling (Rackham, 1988) | Sales discovery | Verified. Sales research; the 35,000-call figure varies by source. |
| The Challenger Sale (Dixon & Adamson, 2011) | Sales, insight-led | Verified, but I found no source for a "6,000 reps" figure; sources give different numbers. |
| BANT, MEDDIC and MEDDPICC | Sales qualification | Found in vendor blogs only. Origins and element lists differ by source. |
| Sandler Selling System | Sales | **Not verified.** No usable source found. |
| Getting to Yes (Fisher & Ury, 1981) | Negotiation | Verified |
| Tactical empathy, mirroring, labeling (Voss) | Negotiation | Verified through summaries. Developed in hostage negotiation. |
| Cialdini's principles of persuasion | Influence | **Not verified in this session** |
| SPIKES (Baile et al., 2000) | Delivering bad news | Verified. Clinical origin; not formally trialled, per its authors' description. |
| NURSE statements | Empathy wording | **Wording not verified.** Probably from Back, Arnold et al. (oncology communication). |
| Motivational interviewing and OARS (Miller & Rollnick) | Behaviour change | Verified |
| Customer Effort Score (Dixon, Freeman & Toman, HBR 2010) | Support | Verified through secondary sources. Critics say it overreaches. |
| Linguistic style matching (Niederhoffer & Pennebaker, 2002) | Style copying | Verified abstract. Matching reflects engagement, not necessarily liking. |
| Chameleon effect (Chartrand & Bargh, 1999) | Mimicry | Verified. A replication was reported to be only partly successful. |
| "Okay" in conversation (Beach, 1993; Oloff, 2019) | Closers and acknowledgments | Verified through bibliographic and summary sources. **No chatbot-specific study found.** |
| Media richness theory (Daft & Lengel, 1986) | Channel choice | Verified, and contested |
| Response-time limits 0.1 / 1 / 10 s (Miller 1968; Nielsen 1993) | Response time | Verified |
| Turn-taking across 10 languages (Stivers et al., 2009) | Voice timing | Verified. Gaps stay within 250 ms of the cross-language mean; the exact average is **not verified**, so don't quote 200 ms. |
| ASR racial disparities (Koenecke et al., 2020) | Voice recognition | Verified. Average word error 0.35 vs. 0.19 across five commercial systems. |
| Careless Whisper (Koenecke et al., FAccT 2024) | Transcription hallucination | Verified. About 1% of transcriptions had invented phrases, 38% of those harmful. The later-improvement claim is the lead author's and unverified. |
| Word error rate limits on names and entities | Transcription evaluation | Trade and vendor sources only. Treat as leads. |
| Length correlations in RLHF (Singhal et al., 2023) | Response length | Verified through the abstract and summaries |
| "GPT-4 getting lazier" (OpenAI, Dec 2023) | Lazy completion | Verified from the company's post as reported. Root cause never published. |
| Underthinking in o1-like models (Wang et al., 2025) | Under-effort | Verified. Covers open reasoning models only. |
| LLMs Get Lost in Multi-Turn Conversation (Laban et al., 2025) | Multi-turn reliability | Verified. About 39% average drop; mostly unreliability. |
| Lost in the Middle (Liu et al., 2023) | Long-context recall | Verified |
| FTC "Bringing Dark Patterns to Light" (2022) | Visual and flow design | Cancellation-maze point verified. The full tactic list is **not verified**. |
| WCAG 2.2 | Accessibility | Target size (2.5.8, 24 by 24 CSS px) verified. Contrast (1.4.3) **not verified** here; check the W3C page. |
| Automation complacency and bias (Parasuraman & Manzey, 2010) | Human oversight | Verified. Occurs in experts too and isn't prevented by training or instructions. |
| OWASP Top 10 for LLM Applications 2025 | Security and privacy | Verified list names (LLM02, LLM06, LLM07 among ten). Definitions **not read**. |
| NIST AI 600-1 Generative AI Profile (2024) | Governance | Verified: 12 risks listed. Definitions not read in full. |
| CCPA as amended by CPRA | Privacy rights | Verified through summaries. Response timelines differ by source. |
| tau-bench (Yao et al., 2024) | Policy following | Verified. Strong models inconsistent across repeated runs. |
| Coding-agent production-database incident (July 2025) | External services | Press and incident-database reports. Record counts differ by source. |
| CFPB guidance withdrawal (May 2025) | Regulation | Verified: 67 documents withdrawn, pending review. Status of the 2023 chatbot spotlight **unconfirmed**. |
| DarkBench (ICLR 2025) and related dark-pattern studies | Manipulation in assistants | Verified existence and scope (sycophancy, anthropomorphism, emotional manipulation). **No study of upselling found.** |
| Ads in ChatGPT (announced Jan 2026; tests from Feb 2026) | Conflicts of interest | Reported by vendor, marketing, and opinion sources. OpenAI's own principles not read. |
| Salesforce State of the Connected Customer | Repeating information | Figures read via secondary articles; they vary by edition and region |
| Gartner: 40% of enterprise apps to include task-specific agents by end-2026 | Market size | Reported through secondary sources; original not checked |
| Agentic commerce protocols and market size (Juniper, others) | Commerce | Vendor, trade, and preprint sources; dates and details conflict |
| AI browser prompt injection (OpenAI, Brave statements) | Browser agents | Verified through press and security-blog coverage; no 2026 primary disclosure found |
| MCP security reporting (2025 to 2026) | Tool ecosystems | Vendor and research-blog sources; counts of vulnerabilities differ |
| Otter.ai and Fireflies suits (2025) | Meeting recorders | Allegations in filings as reported; current status unchecked |
| Illinois AI therapy law (Aug 2025) | Wellbeing | Verified through news coverage |
| Mobley v. Workday (2025) | AI hiring | Verified through law-firm summaries; merits pending |
| Per-resolution pricing (Intercom Fin, Decagon, Sierra) | Incentives | Third-party analyses; Fin's $0.99 figure best supported, others estimates |
| FCC ruling on AI voices under the TCPA (Feb 2024) | Voice outreach | Verified for 2024; claims of newer 2026 rules unconfirmed |
| Grice's maxims, peak-end rule, Hofstede, Culture Map, HEARD, LAST, GDPR Art. 22 | Various | **Not verified in this session** |

## Next steps
1. Follow the execution plan. (Or pick a tier and a family by hand.) Run the "before writing" steps for each row.
2. For each pattern, research the **R** flags first, and get **L** and **E** reviews before publishing.
3. Add a family README for each new family when its first pattern lands.
