# AI Code Calls Functions That Don't Exist: Plausible but Nonexistent APIs and Options

<!-- SEO
title: AI Code Calls Functions That Don't Exist: Catch It Pre-Merge
description: AI coding tools call functions, flags, options and packages that do not exist. Check each new name against installed versions before you merge.
search phrases:
- ai code calls function that doesn't exist
- copilot made up a method
- chatgpt invented parameter unexpected keyword argument
- ai hallucinated api
- llm hallucinated cli flag
- slopsquatting how to prevent
- how to check ai generated code before merge
-->

**Frequency**: Common

## Issue: AI coding tools call functions, flags, options and packages that do not exist. Check each new name against installed versions before you merge.

> **One line:** The diff looks finished, but it calls a method, keyword argument, CLI flag, config key or package that the installed version does not have; the fix is a pre-merge check that resolves every new name against the lockfile, the installed library and its docs, then runs the type checker and tests.

| | |
|---|---|
| **Channel** | Written for **generated code**: diffs and pull requests from Copilot, Cursor, Claude Code, ChatGPT and similar tools. Chat-time package suggestions are covered by the closest page (section 8). |
| **Stakes** | Medium to high. A made-up option crashes at runtime or is silently ignored; a made-up package name can be registered by an attacker and run code at install. |
| **Who is affected** | Reviewers, on-call engineers who hit the crash, and developers working in a library or version they do not know well |
| **Frequency** | Common. Studies find invented packages and invalid API calls at measurable rates across models (section 4). I found no rate for merged code. |
| **Pattern ID** | code-nonexistent-apis |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Resolved-name merge rate: share of AI-assisted pull requests whose new imports, packages, attributes, keyword arguments, CLI flags and config keys all resolve against the lockfile, the installed version or its docs. Target 100% (proposed starting point). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A 2026 re-test of newer models still found 4.62% to 6.10% invented packages, so a lookup outside the model is still needed. (Our judgment, not tested.) |
| **Also searched as** | AI made up a function · unexpected keyword argument from ChatGPT code · Copilot hallucinated method · fake CLI flag from AI · package hallucination · slopsquatting |

## 1. In plain words
You ask an AI tool to change some code. It writes a call that reads well, such as an option named `skip_bad_rows=True`, but that option is not in the library you have installed. Sometimes the code crashes on the first run; sometimes a config tool ignores the unknown key and nobody notices. The fix: before merge, every name the diff adds that the repo did not already use is checked against the lockfile, the installed version and its docs, and the type checker and tests run on the diff.

**How this differs from the closest page.** [Invented packages and APIs](../../coding-agents/failures/invented-packages-and-apis.md) covers the **chat reply**: an assistant hands you an install command for a package it made up. This page covers the **diff**: invented names that are already written into code or config, the tells a reviewer can spot, and the pre-merge check that catches them.

## 2. What it looks like
An illustrative case: a developer at a bakery chain in Portland, Oregon asks Cursor to make the nightly order import skip broken rows. The project pins pandas 2.x.

**Without the fix**
```python
# orders/import_job.py (added lines)
df = pd.read_csv(path, skip_bad_rows=True, encoding="utf-8")
```
```
Reviewer: LGTM, ship it.
On-call (2:10 a.m.): TypeError: read_csv() got an unexpected keyword argument 'skip_bad_rows'
```
**With the fix**
```python
df = pd.read_csv(path, on_bad_lines="skip", encoding="utf-8")  # pandas 2.x option name
```
```
Assistant: Done in orders/import_job.py. Name check against your pinned pandas 2.x:
           on_bad_lines is in the installed read_csv signature; skip_bad_rows is not.
           0 new packages. mypy and pytest pass on the diff.
           Should skipped rows be logged somewhere, or dropped silently?
```
The fixed diff uses only names that resolve in the installed version, the reply says what was checked, and the open question goes to the developer instead of a guess.

## 3. Why it happens
- **The model writes the name that fits, not the name that exists.** An option called `skip_bad_rows` reads like pandas. Studies find models do worst on rarely used APIs (section 4), where a guess is most likely.
- **The model does not know your version.** It mixes names from other versions and other libraries unless it reads your lockfile or the installed signatures.
- **Review reads the logic, not the names.** A reviewer checks whether the change makes sense; few open the docs for each keyword argument, and unknown config keys often fail silently.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Across 576,000 code samples from 16 models in two languages, the average share of hallucinated packages was at least 5.2% for commercial models and 21.7% for open-source models. | [Spracklen et al., *We Have a Package for You!*, arXiv 2406.10279, v3 March 2, 2025, USENIX Security 2025](https://arxiv.org/abs/2406.10279v3). Abstract opened and read. | 2024-era models and research prompts, not merged code. I read the abstract only. |
| A 2026 re-test of five newer models on 199,845 paired Python and JavaScript prompts found overall rates "between 4.62% (Claude Haiku 4.5) and 6.10% (GPT-5.4-mini)." | [Churilov, *The Range Shrinks, the Threat Remains*, arXiv 2605.17062, May 16, 2026, v3 August 9, 2026](https://arxiv.org/abs/2605.17062). Abstract opened. | Single independent author; preprint; abstract only. |
| On CloudAPIBench (AWS and Azure APIs), GPT-4o made valid calls 38.58% of the time for low-frequency APIs and 93.66% for high-frequency ones; other code models scored 12.36% to 34.83% on rare APIs. Retrieving docs only when needed improved GPT-4o by 8.20 points. | [Jain et al., *On Mitigating Code LLM Hallucinations with API Documentation*, arXiv 2407.09726, July 2024](https://arxiv.org/html/2407.09726v1). Abstract and Table 1 opened. | Amazon authors; cloud SDKs only; 2024 models. |
| A benchmark built from recent Java repositories targets calls to non-existent APIs and misuse of real ones; the authors' MARIN method reduced API hallucination against a RAG baseline on six models. | [Chen et al., arXiv 2505.05057, May 2025](https://arxiv.org/abs/2505.05057v1). Abstract opened. | Self-reported by the method's authors. Sample counts and percentage reductions appeared only in a search summary, so I leave them out. |
| A research note reports that `unused-imports`, a name models suggest in place of `eslint-plugin-unused-imports`, was malicious and still drew about 233 weekly downloads in early February 2026 despite an npm security hold; it also reports `react-codeshift` spreading through 237 repositories via AI-generated agent skills. | [Cloud Security Alliance research note, April 2026](https://labs.cloudsecurityalliance.org/research/csa-research-note-slopsquatting-ai-supply-chain-20260419/). Opened. | Secondary: the note credits Aikido Security for both cases. I did not open Aikido's posts. |
| The same note recommends lockfile pinning and hash checks in CI, registry checks of each AI-recommended dependency, and no agent installs without human review or an allowlist. | Same note. Opened. | Recommendations, not measured results. |
| `npm ci` requires an existing lockfile and "will exit with an error" if the lockfile and `package.json` do not match. | [npm Docs, *npm ci*](https://docs.npmjs.com/cli/v10/commands/npm-ci). Opened. | Vendor docs; catches drift, not whether a new name is real. |
| mypy "checks that an attribute is defined in the target class or module" (`attr-defined`) and that "the number and names of arguments match the called function" (`call-arg`). | [mypy docs, *Error codes enabled by default*](https://mypy.readthedocs.io/en/latest/error_code_list.html). Opened. | Works only where type stubs exist; untyped libraries pass silently. |

I found no study that counts invented APIs in merged pull requests, and none that measures how much a pre-merge name check reduces them. The pandas example in section 2 is ours, not from a dataset.

## 5. The fix
**The principle:** No name enters the main branch until something outside the model shows it exists in the version the project runs.

**Do this**
1. **List every new name.** For each diff, list imports, packages, attributes, keyword arguments, CLI flags and config keys that the repo did not already use.
2. **Resolve each name against the project's own versions.** Package: in the lockfile or confirmed on the registry. Function or option: found in the installed signature, type stubs, `--help` output or the docs page for the pinned version.
3. **No new package without a lockfile entry and a human yes.** A new dependency is pinned, shows up in the lockfile diff, and a person approves it in review.
4. **Run the checks that catch the rest.** Type checker, linter and the test suite run on the diff; a call with a made-up argument fails `call-arg` or a test, not production.
5. **Fail loudly on unknown config keys.** Where the tool supports it, turn on strict schema validation so an invented key is an error, not a silent no-op.
6. **Say what was checked.** The assistant's reply or PR description names each new name and where it was confirmed, or says "not verified".
7. **Don't merge an unresolved name.** Any name that could not be confirmed blocks merge until a person checks it or it is removed.

**Reference design: pre-merge name check**
| New name in the diff | Check against | Pass if | If it fails |
|---|---|---|---|
| Package or import | Lockfile, then registry page | In lockfile, or real on the registry and approved in review | Block; ask which package was meant |
| Function, method, attribute | Installed module or type stubs (mypy `attr-defined`, TypeScript `tsc`) | Resolves | Block; replace with the documented name |
| Keyword argument or parameter | Installed signature (mypy `call-arg`, `inspect.signature`) | Name is in the signature | Block; replace or remove |
| CLI flag | `tool --help` for the pinned version | Flag is listed | Block; cite the help output |
| Config key | The tool's schema for the pinned version | Key is in the schema | Block; remove or fix |

```
Project rule (CLAUDE.md, AGENTS.md, .cursor/rules or .github/copilot-instructions.md):
- Before you use a function, option, flag or config key the repo does not already use,
  check it against the installed version (signature, --help, or the docs for the pinned version).
- Never add a package without asking. If you add one, pin it and show the lockfile change.
- In your reply, list every new name and where you confirmed it, or write "not verified".
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md)). Adapted: the "conversation" is the developer and the assistant, or the checker reporting on the PR.
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The reply and the checker report open with what changed and how many new names resolved or failed, with file:line. |
| Admit uncertainty and show how to check | A name could not be confirmed: say "not verified" and give the `--help` command or docs page to check. |
| Ask one clarifying question | A new package is needed, or a real name sits close to the one written: ask which is meant before adding it. |
| Offer choices: 2-4 options plus "Something else", free text open | For each failed name: "Use the documented name", "Remove the option", "Add the dependency (needs approval)", "Something else". |
| Hand off to a person | The unresolved name is a new dependency in production or security-sensitive code. |

**Don't over-correct.** Do not block every name the checker cannot see: private packages, generated clients and plugins loaded at runtime are real but invisible to a registry lookup; keep an allowlist. Do not slap `# type: ignore` on a failing line to get green; a suppression on a new line counts as unresolved. Do not ban new dependencies; ask and pin them. And "exists on the registry" is not "safe": a slopsquatted name exists too.

**Hand-off rule.** When a new package or an unresolved name touches production, auth, payments or build scripts, the assistant stops, leaves the name out, and asks the code owner to approve it in review.

**Framework used:** none yet.

## 6. How to test it (short version)
No test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Ask for "skip bad rows" in a pandas 2.x project | Uses an option found in the installed signature, or says "not verified" | 1, 2 |
| 2 | Plant a call with an invented keyword argument in a PR | Type check or tests fail and name the line | 4, 7 |
| 3 | Ask for a feature that needs a new library | Asks first; lockfile diff shows a pinned entry | 3 |
| 4 | Ask for a CLI script using a rarely used flag | Flag appears in the pinned tool's `--help`, or is marked unverified | 2, 6 |
| 5 | Add an invented key to a config file with strict validation on | Config load fails in CI | 5 |
| 6 | Read the reply after any change | Every new name is listed with where it was confirmed | 6 |
| 7 | Use an internal package not on the public registry | Passes via the allowlist, no false block | Don't over-correct |
| 8 | Silence a new `attr-defined` error with `# type: ignore` | The check still flags the name | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; none comes from a source.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Resolved-name merge rate** (primary) | 100% (proposed) | Pre-merge name check on AI-assisted PRs; PRs with every new name resolved / PRs merged | Below 98% |
| New packages merged without lockfile entry and approval | 0 (proposed) | Diff of manifest vs. lockfile plus review approval log | Any |
| Runtime errors naming a missing attribute or argument | Track; set from baseline | Error tracker: `AttributeError`, `unexpected keyword argument`, "unknown option" within 7 days of a deploy | Rising week over week |
| New-line type suppressions | Track; set from baseline | Count of `type: ignore` and `@ts-ignore` added per PR | Rising for 2 weeks |
| Real names blocked (counter-metric) | Under 5% of blocks (proposed) | Sampled review of 20 blocked names a month; share that were real | Above 10% |

### Detection signals (proposed, not yet calibrated)
Signals in diffs, CI and error logs that suggest this failure. Proposed until checked against human-labeled pull requests.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Import or package in the diff not in the lockfile | Manifest and lockfile diff | A dependency the PR adds on purpose, with approval |
| Type checker `attr-defined` or `call-arg` error on an added line | CI type-check output | Missing or stale type stubs for a real library |
| New `type: ignore` or `@ts-ignore` on an added line | Diff | A known stub gap documented in the repo |
| CLI flag or config key absent from the pinned tool's help or schema | Name-check job output | A flag added in a newer version the PR also upgrades to |
| `unexpected keyword argument` or `has no attribute` error soon after deploy | Error tracker | A dependency upgrade that removed a real name |

**Starter rule:** every new import, attribute, argument, flag and config key in an AI-assisted diff resolves against the project's installed versions before merge, or the PR is blocked.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: code-nonexistent-apis
runs: pre_send
reads: [diff.added_lines, diff.new_names, lockfile.packages, typecheck.errors, cli.help_output, config.schema, allowlist.names, pr.description]
trigger: an AI-assisted diff adds a package, attribute, argument, CLI flag or config key that does not resolve against the lockfile, installed version or docs
moves: [lead_with_answer, admit_uncertainty, ask_clarifying_question, offer_choices, hand_off]
choices: ["Use the documented name", "Remove the option", "Add the dependency (needs approval)", "Something else"]
on_miss: rewrite
metric: resolved-name merge rate
counter_metric: real names blocked
status: proposed
```

## 8. Related patterns
- [Invented packages and APIs](../../coding-agents/failures/invented-packages-and-apis.md): the closest page. It covers a chat assistant suggesting a made-up package or install command; this page covers invented names already in a diff, including keyword arguments, flags and config keys, and the pre-merge check.
- [Over-commented code](./code-over-commented.md): another tell in the same AI diffs; a heavily commented call can still use an option that does not exist.
- [Confident wrong answer with no way to check](../../errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md): the general case of a sure-sounding wrong answer.
- [Supply chain attacks](../../../../../cross-cutting/security/goals/safety-security/failures/supply-chain.md): a real dependency is compromised; here the name was never real until someone registered it.
- Family overview: [AI slop detection](../README.md).

## 9. Common questions
### Why does Copilot or ChatGPT make up functions that don't exist?
It writes the name that fits the pattern of the code, and nothing checks it against your installed version. Studies find this is worst for rarely used APIs (section 4).

### How do I check if AI-generated code uses real APIs?
Run your type checker and tests on the diff, compare new imports against the lockfile, and check any new option or flag against the installed signature or `--help` output. The decision table in section 5 lists the check for each kind of name.

### What is slopsquatting?
Registering a package name that AI tools tend to invent, so anyone who installs the suggested name gets the attacker's code. A Cloud Security Alliance note reports cases on npm in 2026 (section 4).

### Will a type checker catch hallucinated methods?
Often, when type stubs exist: mypy flags missing attributes and wrong argument names. It misses untyped libraries, CLI flags and config keys, so pair it with tests and a name check.

### Do newer models still invent packages?
Yes, at lower rates. A 2026 re-test found 4.62% to 6.10% across five newer models, one preprint's figure.
