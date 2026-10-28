# AI Code Duplication and Over-Engineering: Needless Abstraction and Duplicated Helpers

<!-- SEO
title: AI Code Duplication and Over-Engineering: How to Stop It
description: AI coding tools add one-use factories and wrappers and rewrite helpers your repo already has. Add a search-before-write rule and a duplicate check.
search phrases:
- ai generated code duplication
- claude code creates duplicate functions
- ai rewrites existing code instead of reusing it
- copilot over-engineering code
- cursor creates unnecessary abstractions
- stop ai from creating wrapper classes and factories
- gitclear ai code duplication
- llm agents ignore code reuse
-->

**Frequency**: Common

## Issue: AI coding tools add one-use factories, wrappers and interfaces and rewrite helpers the repo already has; add a search-before-write rule and a duplicate check on every diff.

> **One line:** You ask for one small change and the diff adds an interface, a factory, a config file and a fresh copy of a date helper that already lives two folders away; the fix is a rule to search and reuse before writing, plus a duplication and single-use-abstraction check before merge.

| | |
|---|---|
| **Channel** | Written for **generated code**: diffs and pull requests from Copilot, Cursor, Claude Code, Codex and similar tools. Chat answers with code snippets are in scope only when pasted into a repo. |
| **Stakes** | Medium. Each copy is one more place a bug fix must land; a reporter on one tool notes the agent "may only fix one of them" (section 4). Extra layers slow every later reader. |
| **Who is affected** | Reviewers, maintainers who inherit the code, and the next person (or agent) who fixes a bug in only one of the copies |
| **Frequency** | Common. A study accepted to MSR 2026 finds LLM agents "frequently disregard code reuse opportunities," and a vendor report (GitClear) shows duplicated blocks rising in 2024 (section 4). I found no rate per tool. |
| **Pattern ID** | code-needless-abstraction |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Reuse-clean diff rate: share of AI-assisted pull requests that add no new clone of existing code, no duplicate constant, and no single-implementation interface, factory or forwarding wrapper without a recorded reason. Target 95% before merge (proposed starting point; no catalog row yet). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A model can be told to keep solutions minimal, but whether a helper already exists is a fact about your repo it only learns by searching, so the search step and the diff check stay. (Our judgment, not tested.) |
| **Also searched as** | AI duplicate code · AI keeps rewriting existing functions · Claude Code ignores existing utilities · over-engineered AI code · interface with one implementation · DRY violations in AI code |

## 1. In plain words
You ask an AI tool for a small feature. It does not look for the helper your team already wrote, so it writes a second one. Then it wraps the new code in an interface, a factory and a config entry "for flexibility," though there is one use and no plan for a second. The code works, but the repo now has two versions of the same logic and three layers nobody needs. The fix: make the tool search the repo and reuse what exists before it writes, ban single-use layers unless asked, and run a duplicate check on every diff.

## 2. What it looks like
A developer at a dental group in Columbus, Ohio, asks Claude Code to text patients a reminder 24 hours before each appointment, in the clinic's local time. The repo already has `formatLocalTime()` in `src/utils/dates.ts`.

**Without the fix**
```
Dev:   Add an SMS reminder 24 hours before each appointment, shown in clinic local time.
Agent: Done! I created a flexible, extensible reminder system:
       + src/reminders/IReminderFormatter.ts       (interface, 1 implementation)
       + src/reminders/ReminderFormatterFactory.ts (returns DefaultReminderFormatter)
       + src/reminders/DefaultReminderFormatter.ts (new formatTime(), timezone logic)
       + src/config/reminderConfig.ts              (REMINDER_HOURS_BEFORE = 24)
       ~ src/jobs/sendReminders.ts                 (wires it all together)
Reviewer: formatTime() is a copy of formatLocalTime() in utils/dates.ts, minus the DST fix.
```
**With the fix**
```
Dev:   Add an SMS reminder 24 hours before each appointment, shown in clinic local time.
       Follow the reuse rules in CLAUDE.md.
Agent: Done in src/jobs/sendReminders.ts (+18 lines, no new files).
       Searched: "formatTime|localTime|timezone" -> reused formatLocalTime() from utils/dates.ts.
       Searched: "REMINDER|24 * 60" -> no existing constant; added REMINDER_LEAD_HOURS = 24 here.
       No interface or factory: there is one reminder type. Duplicate check: 0 new clones.
       One question: should the 24 hours differ by clinic, or is one value enough for now?
```
The fixed version reuses the existing helper (with its daylight saving fix), adds no single-use layer, reports what it searched, and asks instead of building configuration nobody asked for.

## 3. Why it happens
Our reading, supported by the sources in section 4.
- **The tool cannot reuse what it has not seen.** It works from the open files and what it chooses to read. GitClear's explanation, as quoted by DevClass: "It is less likely that the AI will propose reusing a similar function elsewhere in the code."
- **Writing new is easier than finding.** Inserting a fresh block costs one keystroke; finding the existing one costs a search the tool skips. One user reports a CLAUDE.md rule to "search for existing code before writing new code" was ignored repeatedly; a rule in a prompt is not a check.
- **Generality reads as quality.** Anthropic's own docs say some Claude models "overengineer by creating extra files, adding unnecessary abstractions, or building in flexibility that wasn't requested." An interface and a factory look like careful design even when there is one product.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Agent-authored pull requests: "LLM Agents frequently disregard code reuse opportunities," giving "higher levels of redundancy compared to human developers," while reviewers "tend to express more neutral or positive emotions" toward AI contributions. | [Huang et al., *More Code, Less Reuse*, arXiv 2601.21276, January 29, 2026, accepted to MSR 2026](https://arxiv.org/abs/2601.21276). Abstract opened and read. | I read the abstract only; it gives no numbers and does not name the dataset. A search summary said it uses the AIDev dataset; I did not confirm that. |
| GitClear (vendor) analyzed 211 million changed lines from 2020 to 2024; code blocks of five or more duplicated lines rose 8-fold in 2024; moved lines fell 39.9%; 2024 was the first year copy/pasted lines exceeded moved lines. | [DevClass, Tim Anderson, February 20, 2025](https://devclass.com/2025/02/20/ai-is-eroding-code-quality-states-new-in-depth-report/) and [LeadDev, Bill Doerrfeld, February 19, 2025](https://leaddev.com/software-quality/how-ai-generated-code-accelerates-technical-debt). Both opened and read. | Vendor research, read through press coverage; GitClear's own report page returned an error when I tried to open it. It measures all code in a period of rising AI use, not AI code alone. A summary of GitClear's page said "4x more code cloning"; seen only in a summary, not used. |
| GitClear's CEO: "Refactored systems, in general, and moved code in particular, are the signature of code reuse." | [LeadDev, February 19, 2025](https://leaddev.com/software-quality/how-ai-generated-code-accelerates-technical-debt). Opened and read. | A vendor's interpretation of its own metric. |
| LLM-generated Java had more code smells than professional reference solutions: an average increase of 63.34%, 73.35% for implementation smells and 21.42% for design smells, across Falcon, Gemini Pro, ChatGPT and Codex. | [Paul, Zhu and Bayley, *Investigating The Smells of LLM Generated Code*, arXiv 2510.03029, October 2025](https://arxiv.org/abs/2510.03029). Abstract opened and read. | Preprint, Java only, older models, single study. Smells in general, not abstraction or duplication alone. |
| A user reports Claude Code ignored a CLAUDE.md rule to "search for existing code before writing new code" and rebuilt an existing function from its parts "three times" instead of calling it. | [anthropics/claude-code issue #40542, opened March 29, 2026](https://github.com/anthropics/claude-code/issues/40542). Opened and read. | One user's report on one tool. Closed as not planned by an inactivity bot. |
| A user reports Claude Code "tends to define the same constants, paths, and logic in multiple files instead of referencing a single source." | [Issue #37137 on a claudeissues.com mirror, opened March 21, 2026](https://claudeissues.com/issue/37137-bug-claude-code-repeatedly-violates-ssot-creates-duplicate-constants-paths-acros). Opened and read. | Read on an unofficial mirror, not on GitHub. One user's report. |
| Anthropic docs (vendor) say Claude Opus 4.5 and 4.6 "have a tendency to overengineer" and give a sample prompt: "Don't create helpers, utilities, or abstractions for one-time operations." | [Claude prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices). Opened and read. | Vendor docs naming two models. Says a prompt helps; gives no rate. |
| Google's review guide calls over-engineering making code "more generic than it needs to be" and says to solve "the problem they know needs to be solved now." | [Google Engineering Practices, *What to look for in a code review*](https://google.github.io/eng-practices/review/reviewer/looking-for.html). Opened and read. | A style rule from one company, not a measurement. |

I found no study that counts single-implementation interfaces or one-use factories in AI code. The Columbus example is our illustration, not a logged case.

## 5. The fix
**The principle:** Before writing, the tool searches the repo and reuses what exists; it adds a layer only when a second use exists now; a diff check proves both before merge.

**Do this**
1. **Search before write.** Before adding a function, class, constant or file, search the repo for its likely names and two or three key terms. The reply lists each search and what it found. Check: the reply has a "Searched:" line per new symbol.
2. **Reuse, do not copy or rebuild.** If an existing helper does the job, call it as-is. Do not paste a modified copy, re-create it from its parts, or wrap it in a class that only forwards calls.
3. **No single-use layers.** No interface with one implementation, no factory that builds one type, no base class with one subclass, unless the task asks for it or a second implementation lands in the same diff.
4. **No config for a constant.** A value used in one place that nobody asked to make configurable stays a named constant next to its use, not a new config file or environment variable.
5. **One source per value.** Before defining a constant, path or URL, search for its literal value; reuse the existing definition if one exists.
6. **New files are reported and justified.** Every new file is listed in the reply with one reason. A request for one function adds no new file unless the reason says why.
7. **Check the diff.** A duplicate detector (jscpd or PMD CPD) and an abstraction scan run on changed files before merge and post results on the pull request.

**Reference design: project rule plus pre-merge checks**
```
Reuse rules (put in CLAUDE.md, AGENTS.md, .cursor/rules or .github/copilot-instructions.md):
- Before writing a new function, class, constant or file, search the repo for it. Start with src/utils, src/lib, shared/.
- If something already does the job, call it. Do not copy it, rebuild it, or wrap it.
- If it almost fits, tell me what would change and ask before editing a shared helper.
- No interface, factory or base class with only one implementation. No config entry for a value used once.
- In your reply, list what you searched, what you reused, and every new file with one reason.
```
| Check | Where | Fails when |
|---|---|---|
| jscpd (`--min-tokens`, `--min-lines`, `--threshold`) or PMD CPD (`--minimum-tokens`, `--ignore-identifiers`) on changed files against the whole repo | Pre-commit and CI | A new clone of existing code appears; set token size and threshold from your own baseline |
| Single-implementation scan: new interface, abstract class or factory with one implementer or one product in the repo | CI script | Any match without a reason in the PR description |
| Forwarding-wrapper scan: new class whose methods only call one other object | CI script | Any match without a reason |
| Duplicate literal scan: new constant whose value already exists as a named constant | CI script | Any match outside tests |
| Reviewer question: "Does this diff add anything the repo already had?" | PR template checkbox | Reviewer unchecks it |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md)). Adapted: the "conversation" is the developer prompting the tool, or the checker reporting on the PR.
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The reply opens with what changed, the line count, new files, and what was reused. |
| Ask one clarifying question | The tool is about to add configuration or a layer "for later": it asks once whether that later use is real. |
| Offer choices: 2-4 options plus "Something else", free text open | An existing helper almost fits: "Reuse it as-is", "Add an optional parameter to it", "Write a separate local function and say why", "Something else". |
| Hand off to a person | Reuse needs a change to a shared helper other teams call: the code owner decides. |

**Don't over-correct.** Do not merge code that only looks alike but changes for different reasons; two similar functions owned by different teams can be right, and a wrong shared helper is worse than a copy. Do not bend an existing helper's behavior for every caller to fit one new use. Keep interfaces the team needs as a test seam or a published API boundary, and duplicated setup in tests where it keeps each test readable. Allow-list generated code, migrations and vendored files in the duplicate check.

**Hand-off rule.** When reuse would change a shared helper with other callers, or the existing helper looks buggy, the tool does not edit it; it uses the helper as-is or writes a local function, flags the issue in the PR description, and asks the code owner.

**Framework used:** none yet.

## 6. How to test it (short version)
No test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Ask for a date-formatting feature in a repo that has a date helper | The reply lists a search and calls the existing helper | 1, 2 |
| 2 | Same request; inspect the diff | No copied, rebuilt or wrapped version of the helper | 2 |
| 3 | Ask for one new export format (CSV) | No interface, factory or base class with one implementation | 3 |
| 4 | Ask for a retry with 3 attempts | The 3 is a named constant at its use, no new config file or env var | 4 |
| 5 | Ask for a feature that needs an S3 bucket path already defined in `config/paths.ts` | The existing path constant is imported | 5 |
| 6 | Ask for a one-function change | No new file, or each new file is listed with a reason | 6 |
| 7 | Open a PR with a planted copy of an existing 20-line function | The duplicate check fails and names both locations | 7 |
| 8 | Ask for a change where the existing helper almost fits and has other callers | The tool asks before editing the shared helper | Hand-off |
| 9 | Ask for a feature next to two similar functions owned by different teams | The tool does not merge them unasked | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; none comes from a source.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Reuse-clean diff rate** (primary) | 95% (proposed) | Pre-merge checks on AI-assisted PRs; PRs with no new clone, duplicate constant or unexplained single-use layer / PRs checked | Below 90% |
| New clones of existing code per merged PR | Track; set from baseline | jscpd or PMD CPD report on changed files, stored per PR | Rising for 2 weeks |
| Single-implementation abstractions merged without a reason | 0 (proposed) | Abstraction scan on merged commits | Any |
| Searches reported per new symbol | 100% (proposed) | Parse the tool's reply or PR description for a "Searched:" line per new function, class or constant | Below 95% |
| Shared helpers changed in ways that broke other callers (counter-metric) | 0 (proposed) | Incidents and reverts traced to a helper edited to fit a new caller; sampled monthly | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a diff that suggest this failure. Proposed until checked against human-labeled reviews.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| New function whose body matches an existing function above the clone threshold | Duplicate detector on changed files | A deliberate fork where the two copies will diverge, noted in the PR |
| New interface, abstract class or factory with exactly one implementer or product | Abstraction scan of added files | A test seam, plugin point or public API the team asked for |
| New constant or path whose literal value already exists under another name | Duplicate literal scan | Same number with a different meaning (two different 24s) |
| Request for one function yields three or more new files | Diff stats per PR, joined to the prompt | A new module the user asked to scaffold |
| Reply has no search step before new symbols | Tool reply or PR description | A greenfield repo with nothing to reuse |

**Starter rule:** before an AI tool adds a function, class or constant, it searches the repo and reuses what exists, and no single-implementation layer passes the pre-merge check.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: code-needless-abstraction
runs: pre_send
reads: [diff.added_files, diff.added_symbols, clone_report.matches, abstraction_scan.single_impl, literal_scan.matches, reply.search_log, pr.description, allowlist.files]
trigger: the AI tool writes code or opens a PR, and a new symbol duplicates existing code or adds a single-use layer, or no search was reported
moves: [lead_with_answer, ask_clarifying_question, offer_choices, hand_off]
choices: ["Reuse it as-is", "Add an optional parameter to it", "Write a separate local function and say why", "Something else"]
on_miss: rewrite
metric: reuse-clean diff rate
counter_metric: shared helpers changed in ways that broke other callers
status: proposed
```

## 8. Related patterns
- No existing page in this library covers duplicated code or over-engineering by coding tools. The closest is [over-commented code](./code-over-commented.md): the same family and the same "rule plus diff check" fix, but it targets noise in comments, while this page targets extra code and layers that change what must be maintained.
- [Invented packages and APIs](../../coding-agents/failures/invented-packages-and-apis.md): the tool reaches for a dependency that does not exist; here it ignores code that does exist. Both are fixed by checking the repo or registry before writing.
- [Calls to APIs that don't exist](./code-nonexistent-apis.md): the sibling code tell in this family, for functions and methods the tool invents.
- [Fresh-session amnesia](../../effort-and-memory/failures/fresh-session-amnesia.md): each new session starts without knowing the codebase, one reason helpers get rewritten.
- Family overview: [AI slop detection](../README.md).

## 9. Common questions
### Why does AI write duplicate code instead of using my existing functions?
It only reuses what it has read, and it often writes before it searches. GitClear's explanation, reported by DevClass, is that the AI is less likely to propose reusing a similar function elsewhere in the code. Make searching a written step and check the diff (section 5).

### How do I stop Claude Code, Cursor or Copilot from over-engineering?
Put the reuse rules from section 5 in CLAUDE.md, AGENTS.md, `.cursor/rules` or `.github/copilot-instructions.md`. Anthropic's docs offer a similar "avoid over-engineering" prompt. One user reports the rule alone did not hold, so add a pre-merge check.

### Is an interface with one implementation always bad?
No. It earns its place as a test seam, a plugin point or a public API boundary the team chose. It is a tell when the tool adds it unasked, with one implementer and no reason in the PR.

### What tool finds duplicate code in a pull request?
jscpd covers many languages and can fail CI above a duplication percentage; PMD's Copy/Paste Detector does the same for many languages and can ignore renamed identifiers in Java and C++. Run either on changed files against the whole repo.

### Is all duplicated code bad?
No. Code that looks alike but changes for different reasons can stay separate, and tests often repeat setup on purpose. The problem is a second copy of logic that must stay in sync, written because nobody looked.
