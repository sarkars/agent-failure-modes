# Slopsquatting: Attackers Register the Package Names AI Keeps Inventing

<!-- SEO
title: Slopsquatting: Block Package Names AI Keeps Inventing
description: Attackers register package names that AI tools invent again and again. Gate new packages on publish date, publisher and an allowlist, not on "it exists".
search phrases:
- slopsquatting
- what is slopsquatting
- ai hallucinated package registered by attacker
- how to prevent slopsquatting
- react-codeshift npm
- huggingface-cli fake package
- block newly published npm packages
- hallucinated package names repeat
-->

**Frequency**: Occasional

## Issue: Attackers register package names that AI tools invent again and again. Gate new packages on publish date, publisher and an allowlist, not on "it exists".

> **One line:** AI tools invent the same fake package name over and over, someone registers it, and every check that only asks "is this name on npm or PyPI?" now says yes; the fix is a dependency gate that holds any newly published, unknown-publisher or unlisted package for a person, and a scan that finds invented names in your own docs and skill files before someone else claims them.

| | |
|---|---|
| **Channel** | Written for **the dependency path**: install gates, package proxies, CI checks and the docs, READMEs and agent skill files that carry install commands. Chat suggestions and pre-merge diffs are covered by the pages in section 8. |
| **Stakes** | High. A package installed under a claimed name runs the owner's code on developer machines and CI runners; through `npx` it runs after a single "Ok to proceed?" prompt, which the Aikido researcher notes agents approve (section 4). |
| **Who is affected** | Security and platform teams that run dependency checks; developers and coding agents that install what a doc or skill file says; open source projects whose READMEs carry an invented install command |
| **Frequency** | Occasional. Invented names are common and often repeat; public cases of a claimed name are few: one malicious npm package and two researcher placeholders in the sources opened (section 4). |
| **Pattern ID** | code-slopsquatting |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Unreviewed young-or-unlisted dependency rate: share of new dependencies reaching a lockfile that were first published under 30 days ago, or are off the allowlist, with no recorded human review. Target 0 (proposed starting point). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Better models invent fewer names, but invented names already sit in skill files, READMEs and forks, and the attacker acts at the registry, not in the model. (Our judgment, not tested.) |
| **Also searched as** | slopsquatting attack · AI package hallucination attack · hallucinated npm package registered · fake pip package from ChatGPT · npx hallucinated package · package squatting AI |

## 1. In plain words
Coding tools sometimes invent a package name that sounds right. The same tool often invents the same name again for the same kind of question, so the name is predictable. Anyone can register it on npm or PyPI and wait for installs. Once it is registered, the usual check, "does this package exist?", passes. The fix moves the check from "exists" to "is this the package we meant, is it old enough, and who published it", and cleans invented names out of your own files first.

## 2. What it looks like
The package name below is made up for this page. It may be registered by the time you read this, which is the point.

**Without the fix** (a CI dependency check comments on a pull request a coding agent opened)
```
Dev:  Agent added a codemod step per our react-upgrade skill. Can this merge?
Bot:  Dependency check passed.
      react-hooks-migrate: found on npm. No known vulnerabilities.
      All 1 new dependencies verified. Lockfile updated.
Dev:  Great, merging.
      (The package was first published 6 days ago by an account with no other packages.)
      (From now on every CI runner installs it on each build.)
```

**With the fix**
```
Dev:  Agent added a codemod step per our react-upgrade skill. Can this merge?
Bot:  Held for review: react-hooks-migrate is not on our allowlist.
      First published 6 days ago. Publisher has no other packages. No repository link.
      It was named in our skill file before it existed on npm, so it may be an invented name someone claimed.
      Known codemod tools on our allowlist: jscodeshift, react-codemod.
      Do you want to (1) switch to an allowlisted tool, (2) request a security review, or (3) Something else?
Dev:  1. And fix the skill file.
```
The fixed gate does not treat "found on npm" as verified, says which checks failed, ties the name to the file that introduced it, and offers a safe path.

## 3. Why it happens
- **Invented names repeat, so they can be claimed.** A name a model produces once tends to come back for the same prompt, which turns a one-off error into a target list (section 4).
- **Checks stop at "the name resolves."** Existence and known-vulnerability lookups pass for a fresh package nobody has reported yet. Registry similarity filters catch near-copies of real names, but most invented names are not near-copies (section 4; the link between the two is our reading).
- **Invented names outlive the chat.** Install commands go into READMEs, agent skill files and forks, where they keep firing for months, often through `npx`, which fetches and runs a package after one yes.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Across 16 models and 576,000 code samples, hallucinated packages averaged 5.2% for commercial and 21.7% for open-source models, with 205,474 unique invented names. | [Spracklen et al., USENIX Security 2025 presentation page](https://www.usenix.org/conference/usenixsecurity25/presentation/spracklen). Opened. | Research prompts in Python and JavaScript, 2024-era models; not live product traffic. |
| When 500 prompts that produced a hallucination were re-run 10 times, 43% of the invented packages came back in all 10 runs, 58% more than once, and 39% never repeated. 8.7% (6,705/76,489) of invented Python names were real npm packages. | [Spracklen et al., arXiv 2406.10279v3, section 5.3 and 5.4](https://arxiv.org/html/2406.10279v3). Opened (HTML version; last 14% of the page not read). | Same lab setting. Repetition was measured per prompt, not across users. |
| The same paper found 38% of invented names were conflations of real ones, 13% typo variants and 51% pure fabrications. | [Cloud Security Alliance research note, April 19, 2026](https://labs.cloudsecurityalliance.org/research/csa-research-note-slopsquatting-ai-supply-chain-20260419/) and [Aikido, February 20, 2026](https://www.aikido.dev/blog/slopsquatting-ai-package-hallucination-attacks). Both opened. | Secondary: I did not find this split in the part of the paper I read. |
| PyPI rejects a new project whose "ultranormalized" name matches an existing one (example: `py-fo0` when `py-foo` exists); there was no mechanism to delay a new name's visibility. | [William Woodruff, discuss.python.org, April 4, 2024](https://discuss.python.org/t/pypi-typo-squatting-is-there-any-mechanism-to-delay-new-package-name-visibility/50195). Opened. | Forum reply, not official policy; may have changed since 2024. |
| `react-codeshift` (a mash-up of `jscodeshift` and `react-codemod`) first appeared in an October 17, 2025 commit of 47 LLM-generated agent skills, spread to 237+ repositories, and was claimed by an Aikido researcher as an empty placeholder on January 14, 2026. It still drew about 74 downloads on day 0 and a few a day after, which the author attributes to agents running `npx`. | [Charlie Eriksen, Aikido, January 21, 2026](https://www.aikido.dev/blog/agent-skills-spreading-hallucinated-npx-commands). Opened. | Vendor blog (Aikido sells dependency scanning). The agent attribution is the author's inference. |
| `unused-imports`, a squat on `eslint-plugin-unused-imports` that models suggest, is described as malicious and "still pulling 233 downloads a week" in early February 2026, under an npm security hold. | [Aikido, Dania Durnas, February 20, 2026](https://www.aikido.dev/blog/slopsquatting-ai-package-hallucination-attacks). Opened. | Vendor blog; no package analysis shown in the post. The CSA note repeats it. |
| An empty PyPI package registered under the invented name `huggingface-cli` got "more than 30k authentic downloads" in three months, and its install command appeared in an Alibaba research repo README. | [Bar Lanyado, Lasso Security, March 28, 2024](https://lasso.security/blog/ai-package-hallucinations). Opened. | Researcher test with no payload. Shows that invented names get installed, not that attackers did it. |
| pnpm's `minimumReleaseAge` sets the minutes that must pass after a version is published before pnpm installs it; the documented default is 1440. | [pnpm settings: dependency resolution](https://pnpm.io/settings/dependency-resolution). Opened. | Default depends on pnpm version; the page does not say which. It checks version age, not first-publish age of a name. |

**Public incident.** One package described as malicious (`unused-imports`) and two researcher placeholders (`huggingface-cli`, `react-codeshift`) in the sources I opened. I found no public report of a claimed invented name that compromised a named company.

## 5. The fix
**The principle:** A new dependency is trusted because of who published it, when, and an explicit approval, never because its name resolves.

**Do this**
1. **"Found on the registry" is never reported as "verified."** The gate shows existence, first-publish date, publisher and repository link as separate results.
2. **Hold young packages.** A package whose first release is under 30 days old (proposed starting point, inside the 30-90 day window the CSA note suggests) is held for a named human reviewer before it enters a lockfile.
3. **Allowlist for agents and CI.** Agents and CI install only packages already in the lockfile or on an allowlist. Anything else is held, not installed and reported later.
4. **Install from the lockfile with hashes in CI.** CI never resolves a fresh name; it installs exactly what the reviewed lockfile records.
5. **Flag "named before it existed."** If the first file in your repo that references a package is older than the package's first publish date, the gate says so in the hold message.
6. **Check conflations, not only typos.** The gate compares a new name against allowlisted names and flags a name built from parts of two of them (as `react-codeshift` was from `jscodeshift` and `react-codemod`).
7. **Scan your own install commands.** Docs, READMEs, agent skill files and scripts are scanned for `pip install`, `npm install`, `npx`, `pnpm dlx`, `yarn dlx` and `bunx` commands; every name that does not resolve, or resolves to a held package, opens a fix ticket the same week.
8. **Every hold says what failed and what to do next**, names the allowlisted alternatives if any, and routes to a reviewer.

**Reference design: gate decision for each new dependency**
| Name state | Example signal | Gate does |
|---|---|---|
| In lockfile or on allowlist | Lockfile entry with hash | Install |
| Resolves, first release 30+ days ago, known publisher, repo link | Registry metadata | Hold for one-click review; show metadata |
| Resolves, first release under 30 days, or publisher has no history, or no repo link | Registry metadata | Hold; security review required |
| Resolves, and our repo named it before its first publish | Git history vs. publish date | Hold; label "possible claimed invented name" |
| Does not resolve | Registry 404 | Block; open a ticket to fix the file that named it |

```
Never report a dependency as verified because its name exists on the registry.
Show first-publish date, publisher, and repository link as separate checks.
Hold any package not in the lockfile or allowlist; agents and CI do not install it.
If the package was first published within 30 days, or after our repo first named it, label the hold and require security review.
In every hold, say which check failed, list allowlisted alternatives, and give the review path.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | A held package: say which checks failed and link the registry page and git history. Not for a lockfile package. |
| Offer choices: 2-4 options plus "Something else", free text open | After a hold where allowlisted alternatives exist: switch, request review, or "Something else". Do not offer them when the name does not resolve at all; then there is only one path, fix the reference. |
| Hand off to a person | A young, unknown-publisher or named-before-it-existed package: route to security review. Do not hand off for allowlisted packages. |

**Don't over-correct.** Do not block every new package; a team that cannot add anything will route around the gate. Do not hold a well-known package because one version is new; the age rule is about the name's first release (version age is what `minimumReleaseAge` covers). Do not label a hold "malicious"; say what was checked. Do not register invented names yourself as a defense without reading the registry's policy; the researchers in section 4 did it as disclosed research.

**Hand-off rule.** Any hold labeled "possible claimed invented name" goes to the security team, who also check every repo and skill file that references the name.

**Framework used:** none yet.

## 6. How to test it (short version)
No test file exists yet. Results: **not yet run.** These are designed scenarios.

| # | Scenario | Pass if |
|---|---|---|
| 1 | PR adds a package first published 5 days ago | Held; message shows publish date and review path (rules 1, 2, 8) |
| 2 | Agent in CI tries `npx` with a name not on the allowlist | Not executed; hold logged (rule 3) |
| 3 | Skill file committed in March names a package first published in June | Hold labeled "named before it existed" (rule 5) |
| 4 | New name joins parts of two allowlisted names | Flagged as a possible conflation (rule 6) |
| 5 | README contains an install command for a name that 404s | Ticket opened to fix the README (rule 7) |
| 6 | PR bumps an allowlisted package to a new version | Not held by the first-publish rule (Don't over-correct) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unreviewed young-or-unlisted dependency rate** (primary) | 0 | Lockfile diffs joined to registry first-publish date, allowlist and review log | Any |
| Gate messages that say "verified" from existence alone | 0 | Sampled review of gate output | Any |
| Install commands in docs and skill files that do not resolve | 0 open older than 7 days | Weekly scan of repo text for install commands, resolved against the registry | Any older than 7 days |
| Agent or CI installs outside lockfile and allowlist | 0 | Package proxy or install log | Any |
| Holds overturned as false alarms (counter-metric) | Track; set from baseline | Reviewer outcome on each hold | Rising two weeks in a row |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Package first published after the commit that first named it | Git history joined to registry metadata | The team named a package it planned to publish itself |
| New dependency with a young first release and a publisher with no other packages | Registry metadata at gate time | A new, legitimate project from a known org's new account |
| Same unresolvable name appears in several repos or skill files | Org-wide text scan | A private package name missing from the public registry |
| Install attempts for a name from agent user agents or `npx` in CI | Proxy logs | A planned trial of a new tool |
| New name built from two allowlisted names | String comparison at gate | A real plugin named after its host tool |

**Starter rule:** never report a dependency as verified because its name exists; hold any package not in the lockfile or allowlist until a person reviews it.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: code-slopsquatting
runs: pre_send
reads: [lockfile_diff.new_packages, registry.first_publish_date, registry.publisher_history, registry.repo_link, allowlist, git.first_reference_date]
trigger: a new dependency is not in the lockfile or allowlist, or was first published within 30 days or after the repo first named it
moves: [admit_uncertainty, offer_choices, hand_off]
choices: ["Switch to an allowlisted package", "Request security review", "Fix the file that named it", "Something else"]
on_miss: handoff
metric: unreviewed young-or-unlisted dependency rate
counter_metric: holds overturned as false alarms
status: proposed
```

## 8. Related patterns
- [Invented packages and APIs](../../coding-agents/failures/invented-packages-and-apis.md): the closest page. It covers the assistant in chat suggesting a made-up name; this page covers the name after someone registers it, where an existence check passes, and the gate, allowlist and repo scan that catch it.
- [AI code calls functions that don't exist](./code-nonexistent-apis.md): invented names in your own diff, caught pre-merge. It notes that "exists" is not "safe"; this page is the defense for that case.
- [Malicious tool injection](../../../../../cross-cutting/security/goals/runtime-security/failures/malicious-tool-injection.md): lists typosquatting of tool packages; slopsquatting differs because the target name comes from model output, not from a misspelling of a real name.
- [Supply chain attacks](../../../../../cross-cutting/security/goals/safety-security/failures/supply-chain.md): a real dependency is compromised; here the name was never real until someone claimed it.
- A planned sibling page (queue row SL-55) covers coding agents that install hallucinated packages on their own; this page is the registry and gate side.

## 9. Common questions
### What is slopsquatting?
Registering a package name that AI tools tend to invent, so anyone who installs the suggested name gets your code. It works because invented names repeat: in one study, 43% of them came back in all 10 re-runs of the same prompt ([section 4](#4-why-it-matters)).

### Has slopsquatting actually happened?
Aikido describes `unused-imports` as a malicious squat on a name models suggest. Two other well-known names, `huggingface-cli` and `react-codeshift`, were claimed by researchers with empty packages, and both still got installs. I found no public report of a named company being compromised this way.

### Why doesn't our dependency scanner catch it?
Most checks ask whether the name exists and has known vulnerabilities. A freshly claimed package exists and has no reports yet. Add first-publish date, publisher history and an allowlist ([section 5](#5-the-fix)).

### Don't npm and PyPI block look-alike names?
PyPI rejects names that normalize to an existing one, such as `py-fo0` for `py-foo`. That catches typo variants. Most invented names in the study were fabrications or conflations of two real names, which such a filter does not target.

### Does a minimum release age setting stop it?
It helps. pnpm's `minimumReleaseAge` waits a set number of minutes after a version is published. It does not tell you whether the name is the one you meant, so keep the allowlist and review.

### What should I do if our docs contain an invented package name?
Replace the command with the real package, search every repo and skill file for the same name, and check whether the name has been registered since. If it has, treat past installs as a security incident.

---
## Technical section

### T1. Solution architecture
```
lockfile diff / install request / npx call
  -> allowlist + lockfile check -> registry metadata (first publish, publisher, repo link)
  -> git history (first reference date) -> conflation check vs. allowlist
  -> install | hold for review | block + ticket -> log (name, checks, outcome, reviewer)
weekly: scan docs, READMEs, skill files for install commands -> resolve -> tickets
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No install outside lockfile or allowlist for agents and CI | Package proxy | Install log; test 2 |
| Young or named-before-it-existed packages held | PR check | Tests 1 and 3 |
| No "verified" from existence alone | Gate message template | Sampled review |

### T3. Evals
- **Dataset:** start with 50 cases: allowlisted packages, version bumps, young packages, conflations of allowlisted names, unresolvable names in docs, and the public names in section 4.
- **Release gate:** block a gate change if any young or unlisted package installs without a hold.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Agent or CI install outside allowlist | Any | Any with a young package | Find the install path that skipped the proxy |

### T5. Trade-offs
- Registry metadata lookups add latency; cache them briefly.
- Holds slow adoption of genuinely new tools; track the false-alarm counter-metric.
- First-publish date can be gamed by registering early and waiting; the allowlist and publisher checks cover that.

---
### Deep dive
- **Not used.** Search summaries mentioned a 2026 replication of the package study on newer models and a later CSA note; I did not open them, so nothing here depends on them.
- **Open question.** I found no measured effect of a release-age or allowlist gate on slopsquatting specifically.
