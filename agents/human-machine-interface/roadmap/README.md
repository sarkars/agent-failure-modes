# HMI Roadmap: Planned Patterns, Goals, and Metrics

> **Status: names, goals, and metrics only.** None of these patterns is written yet. Each row says what goes wrong, the goal it protects, and the primary metric with a starting target. Patterns already written are in the [area README](../README.md).

## How to read this
- **Targets are starting points to tune on your own data.** Where a number comes from a source, the Flags column says so.
- **Flags:** **V** grounded in a source I verified in research for this plan · **R** needs more research before writing · **L** needs legal review · **E** needs expert review (clinical, accessibility, linguistics).
- **IDs** are stable handles for planning, not file names.

## What's planned
| File | Area | Planned patterns |
|---|---|---|
| [chat-and-core.md](chat-and-core.md) | Remaining chat and core families, plus channel and chat mechanics | 23 |
| [response-time.md](response-time.md) | Speed, waiting, and pacing, all channels | 14 |
| [language-and-locale.md](language-and-locale.md) | Language, reading level, and locale | 16 |
| [conversation-frameworks.md](conversation-frameworks.md) | Sales, support, style matching, and other frameworks | 32 |
| [voice.md](voice.md) | Voice agents | 24 |
| [visual-and-oversight.md](visual-and-oversight.md) | Visual design, and the human-oversight UI for agents | 32 |
| | **Total planned** | **141** |

Already written: 14 chat patterns (see the [area README](../README.md)).

## Suggested priority
| Tier | Why | Start with |
|---|---|---|
| 1 | High harm, or core to the "leading HMI repo" claim, and evidence exists | Sycophantic agreement · romantic or parasocial dependence · scam victims · slow first response and silent long waits · voice dead air and barge-in · ASR accent gaps · spoken card data · dark patterns · approval fatigue · pitching before discovery |
| 2 | Common failures with solid frameworks | The remaining sales and support framework patterns · style-matching patterns · locale formatting · reading level · accessibility |
| 3 | Valuable but needs more research or expert input | Emotion detection from voice · explanation faithfulness · regional styles · pacing and "natural delay" research |

## Framework register (what the planned patterns lean on)
"Verified" means I confirmed the existence and basic claims through search for this plan, usually via secondary summaries. It does not mean the framework is proven to work for chatbots. Most were developed for human-to-human settings.

| Framework or source | Domain | Status |
|---|---|---|
| SPIN Selling (Rackham, 1988) | Sales discovery | Verified. Sales research; the 35,000-call figure varies by source. |
| The Challenger Sale (Dixon & Adamson, 2011) | Sales, insight-led | Verified, but I found no source for the "6,000 reps" figure; sources give different numbers. |
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
| Media richness theory (Daft & Lengel, 1986) | Channel choice | Verified, and contested |
| Response-time limits 0.1 / 1 / 10 s (Miller 1968; Nielsen 1993) | Response time | Verified |
| Turn-taking across 10 languages (Stivers et al., 2009) | Voice timing | Verified. Gaps stay within 250 ms of the cross-language mean; the exact average is **not verified**, so don't quote 200 ms. |
| ASR racial disparities (Koenecke et al., 2020) | Voice recognition | Verified. Average word error 0.35 vs. 0.19 across five commercial systems. |
| FTC "Bringing Dark Patterns to Light" (2022) | Visual and flow design | Cancellation-maze point verified. The full tactic list is **not verified**. |
| WCAG 2.2 | Accessibility | Target size (2.5.8, 24 by 24 CSS px) verified. Contrast (1.4.3) **not verified** here; check the W3C page. |
| Automation complacency and bias (Parasuraman & Manzey, 2010) | Human oversight | Verified. Occurs in experts too and isn't prevented by training or instructions. |
| Grice's maxims, peak-end rule, Hofstede, Culture Map, HEARD, LAST | Various | **Not verified in this session** |

## Next steps
1. Pick a tier and write patterns in the [pattern template](../_templates/hmi-pattern.md).
2. For each pattern, research the **R** flags first, and get **L** and **E** reviews before publishing.
3. Add a family README for each new family when its first pattern lands (as done for the existing ones).
