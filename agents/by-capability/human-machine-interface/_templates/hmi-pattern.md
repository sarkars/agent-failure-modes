<!--
HMI PATTERN TEMPLATE

READABILITY RULES
1. A reader must understand the failure and the fix in 60 seconds, from the top of the file.
2. Sections 1-9 are the "quick read". The Technical section and Deep dive are optional depth.
3. The Fix (section 5) is REQUIRED and must contain a reference design a team can copy.
4. Cite only sources you could verify. Say when a number is vendor-reported, secondhand, or from a different
   setting (e.g. human-to-human research). Never invent statistics.
5. Keep example transcripts short (6-10 lines). Show the failure and the fixed version side by side.

SEARCH (SEO) RULES
6. Write the way people search, not the way engineers label. Use "chatbot", "AI agent", "bot", plus the symptom
   ("chatbot doesn't ask follow-up questions", "chatbot dead end"), not only internal jargon.
7. The H1 contains the phrase people search. Pattern name goes after it or in the first line.
8. Answer the question in the first two sentences (the One line + section 1), before any detail.
9. Use question-style headings in "Common questions" (section 9), each answered in 2-4 sentences.
10. Use descriptive link text ("the SPIN questioning guide"), never "click here".
11. One page per problem. If two patterns would answer the same query, link them and explain the difference.
12. Fill in the SEO comment block below. It is invisible on GitHub and kept for the published site.
13. Search phrases come from reviewing what people write and what ranks, not from keyword-volume tools. Say so
    if you add volume data later.

TECHNICAL SECTION RULES
14. Include the Technical section only when the fix needs engineering (a policy layer, classifier, gate, eval
    harness). Skip it for fixes that are purely wording or design.
15. Sections 6 and 7 are the plain-language summary of testing and monitoring. The Technical section holds the
    detail (datasets, judge rubrics, thresholds, alert levels). Don't repeat; point to it.
16. Every threshold is a starting point to tune, unless you cite a source. Say so.

GOAL AND METRIC RULES
17. Every pattern states the GOAL it protects (one sentence, matching its family README) and ONE primary metric
    with a starting target, in the header table.
18. Section 7 is a metrics table: Metric | Target | How to measure | Alert at. Every row must be measurable
    from logs, evals, or sampled review. Say how.
19. Each family has a README that states the family goal and the shared metrics its patterns report against.
20. Dashboards and health checks are optional; put them in the Technical section.

SITE COMPATIBILITY RULES (the published Astro site imports this file)
21. Line 1 of a pattern is the H1. The importer drops the first line of the file, so anything else there leaks
    into the page.
22. Keep the machine-readable line "**Frequency**: <word>" (Very Common, Common, Occasional, or Rare) and the
    line "## Issue: <one sentence>". The site reads them for badges and cards. The header table is for readers.
23. Patterns live at goals/<family>/failures/<name>.md so the importer finds the capability, goal, and category.
    Other folders (tests, incidents, roadmap) are not imported as patterns.
-->

# [Searched phrase]: [Pattern name]

<!-- SEO
title: [<=60 chars, starts with the searched phrase]
description: [<=155 chars, answers the question]
search phrases:
- [real query 1]
- [real query 2]
-->

**Frequency**: [Very Common / Common / Occasional / Rare]

## Issue: [One sentence, the same as the SEO description; the published site uses it on cards]

> **One line:** [What goes wrong, in one sentence a non-engineer would understand.]

| | |
|---|---|
| **Channel** | Chat / Voice / Visual / All (say which are written, which are planned) |
| **Stakes** | Low / Medium / High / Any |
| **Who is affected** | [All users / a specific group / a specific situation] |
| **Frequency** | Very common / Common / Occasional / Rare, plus how you know |
| **Family** | [e.g. conversation-leadership] (link to the family README) |
| **Goal** | [One sentence: what success looks like. Must match the family README.] |
| **Primary metric** | [One metric, with a starting target to tune. Example: confirmed-resolution rate, gap to containment under 10 points] |
| **Maturity** | Researched / Tests written / Tested / Verified (see the [content program](../roadmap/content-program.md)) |
| **Will a better model fix this?** | Yes / Partly / No, one sentence on why, and whether that is "our judgment" or "tested" |
| **Also searched as** | [3-6 phrases people use for this problem] |

## 1. In plain words
[2-3 sentences. No jargon.]

## 2. What it looks like
**Without the fix**
```
User: ...
Bot:  ...
```
**With the fix**
```
User: ...
Bot:  ...
```
[One sentence on what changed.]

## 3. Why it happens
- [Cause 1]
- [Cause 2]
- [Cause 3 at most]

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| [Verified finding] | [link] | [e.g. human-to-human study; vendor survey] |

## 5. The fix
**The principle:** [one sentence]

**Do this**
1. [Concrete, testable rule]
2. [...]

**Reference design** [prompt block, state schema, flow, decision table, or improved transcript]

**Don't over-correct** [the opposite failure this fix can cause, and the guardrail]

**Hand-off rule** [when to move to a human or another channel]

**Framework used:** [link to solutions-library page]

## 6. How to test it (short version)
*Flagship patterns also link a full test file in `tests/` and, where one exists, an incident in `incidents/`. See the [content program](../roadmap/content-program.md).*

| # | Scenario | Pass if |
|---|---|---|
| 1 | | |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| [Primary metric] | | [Log field, eval, or sampled review] | |

## 8. Related patterns
- [link] - [how it differs]

## 9. Common questions
### [Question written the way people ask it?]
[2-4 sentence answer. Link to the section with detail.]

### [Question 2?]
[...]

---
## Technical section (optional: include when the fix needs engineering)

### T1. Solution architecture
[Components and where they sit in the request path. A small diagram or pseudo-code.]

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|

### T3. Evals
- **Dataset:** [how to build it, size to start with]
- **Judge rubric:** [what graders look for]
- **Metrics and starting thresholds:** [table; say these are starting points]
- **Release gate:** [what blocks a deploy]

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|

### T4b. Dashboard and health checks (optional)
- **Dashboard panels:** [the 3-5 charts that show this goal at a glance]
- **Health check:** [one query or test that proves the guardrail is live]

### T5. Trade-offs
- [Cost, latency, risk, or complexity of the fix]

---
### Deep dive (optional)
- Root-cause detail
- Edge cases
- Modality notes (voice / visual: what changes; mark as PLANNED if not yet written)
- References
