# AI Content Check in CI That Never Blocks: Slop Detection Run Once, Not as a Release Gate

<!-- SEO
title: AI Content Check in CI That Never Blocks a Release
description: A team audits for AI slop once or runs the check as a warning, then ships it on later releases; make the check a blocking gate with recorded overrides.
search phrases:
- vale linter not failing ci
- make lint check required before merge
- block deploy if lorem ipsum found
- ai content check in ci pipeline
- pre-publish checklist for ai generated content
- fail build on llm eval threshold
- who bypassed branch protection
- warnings ignored in ci pipeline
-->

**Frequency**: Common

## Issue: A team audits for AI slop once or runs the check as a warning, then ships it on later releases; make the check a blocking gate with recorded overrides.

> **One line:** A team runs an AI slop check once (a launch audit, a cleanup sprint after a complaint) or wires it into CI as a warning nobody reads, so placeholder text, chatbot leftovers, invented citations and stock phrases return on the next release; the fix is to run the same check on every path to production, fail the release on error-level findings, and record every override with a name, a reason and an expiry date.

| | |
|---|---|
| **Channel** | Written for **pre-merge, pre-deploy and pre-publish checks** on AI-assisted web pages, docs, blog posts, emails and code: Vale or regex phrase rules, placeholder scans, citation resolvers and LLM eval suites run in GitHub Actions, GitLab CI or a CMS publish step. |
| **Stakes** | Medium. One escape is usually embarrassing, not harmful, but the check that was supposed to catch it gives the team false confidence. High when the escape is an invented citation or a fake proof block (see related patterns). |
| **Who is affected** | Editors, developers and release owners who believe "we checked for that"; readers and customers who see the slop |
| **Frequency** | Common, in our judgment. The official Vale GitHub Action does not block by default, and one public repo shows a docs linter left non-blocking with 308 findings unacted on. I found no count across teams. |
| **Pattern ID** | detect-no-release-gate |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Gated release rate: production releases and publishes that passed the full slop gate, or carry a recorded override, divided by all production releases and publishes. Proposed starting point: 100%. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A better model leaves fewer tells per draft, but whether a check runs and blocks is a pipeline setting, not a model property. (Our judgment, not tested.) |
| **Also searched as** | lint warnings ignored · allow_failure true vale · required status check · release gate for content · override log for CI · CMS publish skips checks |

## 1. In plain words
A slop check that runs once only describes one day. The next AI draft brings back the Lorem ipsum, the "Certainly! Here is" opener and the made-up source. A check that only warns is almost the same: the warnings pile up and people stop reading them. The fix is boring: run the check on every release, let error-level findings stop the release, and when someone ships anyway, write down who, why and until when.

## 2. What it looks like
**Without the fix** (illustrative: a Denver home-services company whose marketing site and blog are drafted with an AI tool)
```
March:   Launch audit. Agency scans 120 pages, finds 41 slop items, all fixed. Report filed.
June:    Blog moves to a CMS with its own Publish button. The scan lives only in the site repo.
August:  Writer:  Publish "5 Signs Your Furnace Needs Repair".
         CMS:     Published.
         (Post opens "Certainly! Here's a blog post about furnaces" and cites a
          2023 Department of Energy study nobody can find.)
         Customer email: "Did a robot write your website?"
         Marketing lead: "We checked all of this in March."
```
**With the fix**
```
Writer:  Publish "5 Signs Your Furnace Needs Repair".
Gate:    Blocked. slop-suite v9 found 2 errors:
         1. AI leftover in paragraph 1: "Certainly! Here's a blog post about furnaces"
         2. Citation "DOE furnace study, 2023" did not resolve to a source.
         Choose: "Fix and re-run", "Request an override", "Save as draft", "Something else".
Writer:  Fix and re-run.
Gate:    0 errors, 3 warnings (stock phrases, shown in the draft). Published. Run ID 8812 logged.
```
The fixed version runs the same suite on the CMS path as on the site repo, blocks on errors, and logs the run.

## 3. Why it happens
- **The check is set up as an event, not a step.** A launch audit or cleanup sprint produces a report, not a pipeline step, so nothing runs it on the next release. New publish paths (a CMS, a newsletter tool, an agent with deploy rights) are added later and never inherit it.
- **The tool's default does not block.** The official Vale GitHub Action "succeeds whatever Vale reports" unless `fail_on_error` is set, and GitLab jobs can run with `allow_failure: true` (section 4). Teams adopt the default, warnings pile up, and nobody acts on them.
- **Overrides leave no trace.** When a finding is inconvenient, someone with admin rights merges anyway or turns the job off "for this release". GitHub branch protection does not apply to admins by default (section 4), so the bypass is easy and the reason is not written down.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The official Vale action's `fail_on_error` defaults to `false`: "By default, the action succeeds whatever Vale reports." With it on, it fails only on `error`-level alerts, "so a warning or a suggestion still passes." | [vale-action README, GitHub](https://github.com/errata-ai/vale-action). Opened. | Tool docs, not a study. Shows the default, not how many teams keep it. |
| A pull request merged Oct. 9, 2024 made the action handle Vale's exit code 2 (runtime failure); before it, the action "doesn't fail" when Vale itself fails, so misconfigured workflows "will fail silently." | [vale-action PR #133, GitHub](https://github.com/errata-ai/vale-action/issues/133). Opened. | One tool, now fixed. Shows that a gate can pass because the check never ran. |
| A public GitLab repo's merge request (Aug. 4, 2026) says Vale ran in CI with `allow_failure: true`, so its 308 findings were never acted on, calling it "a linter whose output is permanently ignored." The MR disabled rules that did not fit the repo, fixed about 252 findings, and left 17 itemized; it notes Vale cannot become a real gate until those reach zero. | [gitlab-com/public-sector/reference MR !54](https://gitlab.com/gitlab-com/public-sector/reference/-/merge_requests/54). Opened. | A style linter on docs, not an AI-slop rule set. One repo; the gate was still non-blocking when I read it. |
| promptfoo's CI/CD docs list "Quality gates - Enforce minimum performance thresholds" and show `eval --fail-on-error` and a custom script that runs `exit 1` when the pass rate is below 95%. Their red-team example runs on a daily schedule. | [promptfoo, CI/CD integration docs](https://promptfoo.dev/docs/integrations/ci-cd/). Opened. | Vendor docs. The 95% is their example, not a recommendation for slop checks. |
| GitHub docs: "By default, the restrictions of a branch protection rule do not apply to people with admin permissions to the repository"; a separate setting applies them to admins. | [GitHub Docs, About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches). Opened. | Platform docs; other CI systems differ. |
| Datadog ships a default rule that watches GitHub audit logs for branch protection "overridden by a repository administrator", whose first triage step asks whether the change was authorized | [Datadog, GitHub branch protection override rule](https://docs.datadoghq.com/security/default_rules/github-branch-protection-override/). Opened. | Security vendor docs. Shows the bypass is logged; the reason for it is not. |

**Seen only in search summaries, kept out of the fix:** a mailing-list repost of a January 2024 Ars Technica story on Amazon listings named with OpenAI refusal text ("I'm sorry but I cannot fulfill this request"). Ars Technica could not be fetched. **No public incident found** of a team that ran a one-time slop audit and then shipped slop; searches run: "Vale prose linter GitHub Action fail_on_error CI documentation", "promptfoo CI/CD integration fail build on eval threshold", "GitHub required status checks branch protection bypass audit log", and an Amazon refusal-text listings search.

## 5. The fix
**The principle:** Nothing reaches production without passing the current slop suite, and every exception is written down.

**Do this**
1. **One suite, every path.** Keep one versioned slop suite (placeholder scan, AI-leftover strings, citation resolver, stock-phrase and UI-tell rules) and list every path to production: site deploy, CMS publish, email send, docs build, agent with deploy rights. Each path calls the same suite.
2. **Errors block.** Error-level findings fail the merge, deploy or publish. The gate is a required check, not an optional job (`fail_on_error: true`, no `allow_failure`).
3. **A check that did not run is a failure.** A runtime error, a missing rule file or a skipped rule fails the gate. The run record lists each rule and version that ran.
4. **Split by precision.** Only high-precision findings are errors: placeholders, chatbot leftovers, unresolved citations, unbacked proof blocks. Stylistic tells (em dashes, stock phrases) are warnings shown in the draft until they earn error level on your own data.
5. **Baseline first, then block new.** Before turning on blocking, fix or itemize existing findings, with an owner per item. New findings block from day one; itemized old ones carry an expiry date.
6. **Overrides are recorded.** An override needs a named person, the finding ID, a reason and an expiry date. High-stakes findings (citations, proof blocks) need a second approver. Admins go through the same gate.
7. **Re-scan what is live.** Crawl production weekly with the same suite to catch paths you missed and content edited after publish.

**Reference design: gate record** (one per release or publish, kept in the pipeline log)
```yaml
run_id: 8812
path: cms_publish            # site_deploy | cms_publish | email_send | docs_build | agent_deploy
suite: slop-suite
suite_version: 9
rules_run: [placeholders@4, ai_leftovers@3, citations@2, stock_phrases@14]
rules_skipped: []            # any entry here fails the gate
errors: 0
warnings: 3
result: pass                 # pass | fail | override
override:                    # filled only when result is override
  finding_ids: []
  approved_by: null
  second_approver: null      # required for citation and proof findings
  reason: null
  expires: null
```

**Decision table for the gate**
| Situation | Result |
|---|---|
| All rules ran, 0 errors | Pass; warnings shown in the draft |
| Any error-level finding | Fail; choices shown |
| A rule errored, was skipped or its file is missing | Fail: "Gate did not complete", with the rule named |
| Override requested on a citation or proof finding | Held until a second approver signs |
| Itemized baseline finding past its expiry | Fail, as a new error |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the conversation is the gate reporting to the writer or developer)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | The gate blocks: "Fix and re-run", "Request an override", "Save as draft", "Something else". Don't offer "Request an override" for a gate that did not complete; fix the run first. |
| Admit uncertainty and show how to check | The suite failed to run: say "Gate did not complete", name the rule, never show "pass". |
| Hand off to a person | An override request goes to the named approver, and to a second approver for citation and proof findings. |

**Don't over-correct.** Do not make every stylistic tell a blocking error: a gate that fails on one em dash teaches people to turn it off, and single tells are weak evidence (see [folk tells are not evidence](./text-folk-tells-unreliable.md)). Do not block on a vendor AI-detector score; a score is not a slop finding. Do not make overrides so slow that people publish around the gate; a quick recorded override beats an unrecorded bypass.

**Hand-off rule.** Overrides go to the named release owner for the path; citation and proof-block findings also need a second approver. If no owner is named for a path, that path is blocked until one is.

**Framework used:** none yet. Built from the blocking options in the Vale action and promptfoo docs, GitHub's admin-bypass setting and the baseline-then-gate approach in GitLab MR !54 (section 4), plus our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Post published from the CMS with "Certainly! Here's" in paragraph 1 | Publish blocked, same as on the site repo | 1, 2 |
| 2 | Vale exits with a runtime error on a deploy | Gate fails with "did not complete", not pass | 3 |
| 3 | Draft with two em dashes and no other finding | Publishes with warnings, not blocked | 4 |
| 4 | Gate turned on in a repo with 60 existing findings | Old findings itemized with owners and expiry; a new finding blocks | 5 |
| 5 | Admin merges past a failing gate | Merge refused, or override record with name, reason and expiry required | 6 |
| 6 | Override requested on an unresolved citation | Held until a second approver signs | 6, hand-off |
| 7 | Page edited live after publish adds "Lorem ipsum" | Weekly crawl flags it to the path owner | 7 |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Gated release rate** (primary) | 100% | Release and publish logs joined to gate records: releases with a pass or recorded override / all releases | Below 100% in any week |
| Paths to production calling the suite | 100% | Path inventory vs. gate records by `path` | Any path with no gate record in 30 days |
| Incomplete gate runs shown as pass | 0 | Gate records with `rules_skipped` non-empty and `result: pass` | Any |
| Override rate | Track; set from baseline | Gate records with `result: override` / all gate runs | Doubling month over month |
| Expired overrides still live | 0 | Override `expires` date vs. today, finding still present on the weekly crawl | Any |
| Live escapes found by crawl or readers | Falling to 0 | Weekly crawl hits plus reader reports, per 1,000 published pages | Any rise two weeks running |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A publish or deploy with no matching gate record | Release log vs. gate records | A hotfix with a recorded emergency override filed after the fact |
| The slop job is marked optional, `allow_failure: true` or `fail_on_error: false` | CI config in version control | A new rule in a trial period with an end date |
| Warning count rising for weeks with no fixes | Gate records over time | Content volume rose by the same share |
| Admin bypass events on branches where the gate failed | Platform audit log | Bypass for an unrelated required check |
| Weekly crawl finds slop on pages that passed the gate | Crawl report joined to gate records | Content edited after publish outside any gated path |

**Starter rule:** fail any production release or publish whose gate record is missing, shows a skipped rule, or has an error-level finding without a recorded override.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: detect-no-release-gate
runs: pre_send
reads: [release.path, gate.suite_version, gate.rules_run, gate.rules_skipped, gate.errors, gate.override]
trigger: a release or publish starts on any path to production
moves: [offer_choices, admit_uncertainty, hand_off]
choices: ["Fix and re-run", "Request an override", "Save as draft", "Something else"]
on_miss: block
metric: gated release rate
counter_metric: override rate
status: proposed
```

## 8. Related patterns
- [AI detection rules stop working after a model update](./detect-rules-decay.md) - the closest pattern. That page asks whether a rule still catches anything; this page asks whether the rules run on every release and are allowed to stop it. A gate of decayed rules passes everything; a fresh rule that only warns stops nothing.
- [Placeholder data left in](./ui-placeholder-data-left-in.md) - one check (placeholders) with its own deploy block; this page makes that block one rule in a suite that runs on every path, including CMS and email.
- [AI made-up citations and fake quotes](./text-invented-citations.md) - the citation gate whose findings need a second approver to override here.
- [Tone changes shipped with no regression test](../../measurement-and-feedback/failures/tone-changes-shipped-with-no-regression-test.md) - the same missing gate, applied to the bot's own prompt instead of published content.

## 9. Common questions
### Why does my Vale check pass in CI even with errors?
The official Vale GitHub Action succeeds by default whatever Vale reports. Set `fail_on_error: true` and make the job a required check. Before October 2024 the action also passed when Vale itself crashed, so update it and treat a crash as a failure (rule 3).

### Should AI slop checks block a release or just warn?
Block on high-precision findings: placeholders, chatbot leftovers, unresolved citations, unbacked proof. Warn on stylistic tells like stock phrases until your own data shows they are reliable (rule 4).

### We already did an AI content audit. Why run it again?
Every new AI draft can bring the same problems back, and new publish paths may skip the old check. An audit is one day's snapshot; a gate covers every release (rule 1).

### How do I let someone ship past a failing check without losing control?
Allow overrides, but record the person, the finding, the reason and an expiry date, and require a second approver for citation and proof findings (rule 6). Make admins go through the same gate.

### What if our existing content has hundreds of findings?
Fix or itemize them first, each with an owner and expiry, then block only new findings. One public GitLab repo cut 308 findings to 17 itemized ones this way before planning to make its linter a real gate.
