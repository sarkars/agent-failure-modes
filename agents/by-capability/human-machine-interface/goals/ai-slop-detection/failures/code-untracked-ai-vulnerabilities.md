# Is AI-Generated Code Secure? Untracked AI Code Ships Vulnerabilities Nobody Can Find Later

<!-- SEO
title: Is AI-Generated Code Secure? Tag It So You Can Find It
description: AI coding tools write insecure code, and teams often keep no record of which code was AI-written. Tag AI commits and scan every tagged change.
search phrases:
- is ai generated code secure
- ai generated code security vulnerabilities
- how to track ai generated code in git
- assisted-by commit trailer
- copilot code security risks
- how to find ai written code in my repo
- sast for ai generated code
-->

**Frequency**: Common

## Issue: AI coding tools write insecure code, and teams often keep no record of which code was AI-written. Tag AI commits and scan every tagged change.

> **One line:** A coding agent writes a SQL query or a CI workflow with a known flaw, the commit says nothing about AI, and months later security cannot list which changes the AI wrote; the fix is a provenance tag on every AI-written commit and pull request, plus a security scan that must pass before a tagged change merges.

| | |
|---|---|
| **Channel** | Written for **code written by Copilot, Cursor, Claude Code, Codex and similar tools** that reaches a shared repository. Drive-by PRs to other people's projects are a separate page (section 8). |
| **Stakes** | High. The flaws are injection, weak crypto and leaked secrets; without a record, triage after an incident is manual forensics. |
| **Who is affected** | Security reviewers, incident responders, auditors, and the customers whose data the flawed code handles |
| **Frequency** | Common. Lab studies find insecure output in roughly 40-45% of security-relevant tasks (section 4). I found no measured rate of untagged AI code in production repos. |
| **Pattern ID** | code-untracked-ai-vulnerabilities |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Tagged-and-scanned AI change rate: share of merged changes containing AI-written code that carry a provenance trailer or label **and** a passing security scan. Target 100% (proposed starting point). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Veracode found security results flat while syntax improved, and bigger models did no better; and no model can fix a missing record. (Our judgment, not tested.) |
| **Also searched as** | AI code security risks · Copilot vulnerabilities · track AI-written code · AI attribution in commits · Co-authored-by Copilot · SAST for AI code |

## 1. In plain words
AI tools often pick the insecure way to do a task, such as building SQL by gluing strings together. That alone is a review problem. The bigger problem comes later: when a flaw is found, nobody can ask "what else did the AI write?" because the commits look the same as human ones. The fix is a plain tag on every AI-written change and a security scan that must pass before any tagged change merges.

**How this differs from the closest page.** [AI code calls functions that don't exist](./code-nonexistent-apis.md) is about names that do not resolve; that code usually crashes. Here the code runs fine and passes tests, but it is exploitable, and the team has no record to find its siblings.

## 2. What it looks like
An illustrative case: a developer at a credit union in Denver, Colorado, asks a coding agent to add a member search endpoint.

**Without the fix**
```
User:  Add GET /members/search?name= to the members API.
Agent: Done. Added search_members() in members/api.py:
       cursor.execute(f"SELECT * FROM members WHERE name LIKE '%{name}%'")
       Tests pass. Committed as "Add member search endpoint".
-- 5 months later, after a pen test finds SQL injection --
Security lead: Which other endpoints did the AI write last year?
Developer:     No idea. Nothing in git says which commits were AI.
```
**With the fix**
```
User:  Add GET /members/search?name= to the members API.
Agent: Done in members/api.py, using a parameterized query
       (WHERE name LIKE %s, with the name passed as a parameter).
       Commit trailer: Assisted-by: Claude Code. PR label: ai-assisted.
       Security scan on the diff: 0 findings. Tests pass.
       Ready for your review before merge.
```
The fixed agent avoids the flaw, records that AI wrote the change, and shows the scan result, so a later search by tag finds every AI change.

## 3. Why it happens
- **The model often picks the insecure option.** Given a choice, Veracode's CTO said the models "make the wrong choices nearly half the time," and syntax gains have not carried over to security (section 4).
- **The mark of AI help is uneven, optional and easy to blur.** Each tool uses its own trailer or none, settings can change or hide it, and squash merges blur it: in the Snowflake case a PR-level co-author line could not say who wrote the flawed file.
- **People trust AI code more than they should.** In the Stanford study, users with an AI assistant wrote less secure code and were more likely to believe it was secure, so review relaxes exactly where it should tighten.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Across 80 coding tasks and more than 100 LLMs, AI-generated code introduced security vulnerabilities in 45% of cases; models failed to defend against cross-site scripting (CWE-80) in 86% and log injection (CWE-117) in 88%; Java failed over 70%. "Larger models do not perform significantly better than smaller models." | [Veracode press release, July 30, 2025](https://www.veracode.com/press-release/ai-generated-code-poses-major-security-risks-in-nearly-half-of-all-development-tasks-veracode-research-reveals/). Opened. | Vendor study of model output on set tasks, checked by Veracode's own scanner; full report not opened. |
| Copilot was given 89 security-relevant scenarios and produced 1,689 programs; about 40% were vulnerable. | [Pearce, Ahmad, Tan, Dolan-Gavitt and Karri, "Asleep at the Keyboard?", arXiv 2108.09293, IEEE S&P 2022](https://arxiv.org/abs/2108.09293). Abstract opened. | 2021 technical-preview Copilot; scenarios were chosen to invite weaknesses. |
| In a user study (47 analyzed: 33 with an AI assistant, 14 without), the AI group wrote secure answers less often, for example 21% vs. 43% on encryption and 36% vs. 50% on SQL, and was more likely to believe its code was secure. | [Perry, Srivastava, Kumar and Boneh, "Do Users Write More Insecure Code with AI Assistants?", ACM CCS 2023](https://arxiv.org/html/2211.03622v3). Opened. | Small sample; codex-davinci-002 model; lab tasks. |
| Apiiro reported AI-generated code producing over 10,000 new security findings per month by June 2025, a 10x rise from December 2024, with a 322% rise in privilege escalation paths and 153% in design flaws, while syntax errors fell 76%. | [The Register, September 5, 2025](https://www.theregister.com/2025/09/05/ai_code_assistants_security_problems/). Opened. Apiiro's own blog returned 403. | Vendor data, read through press coverage; the article does not say how AI-written code was identified, which is the gap this page is about. |
| A script injection in a Snowflake GitHub Actions workflow (PR merged June 18, 2026) was first framed as AI-introduced. Wiz then corrected: "It's unclear whether the code-change was AI-assisted." The PR's co-author line named Copilot Autofix, which had fixed a different file. | [Wiz blog, August 17, 2026](https://www.wiz.io/blog/red-agent-snowflake-copilot-cicd-bug) and [Cloud Security Alliance research note, August 21, 2026](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-vs-ai-accountability-vacuum-snowflake-c/). Both opened. | GitHub's rebuttal is reported via CSA and The Next Web; I did not open a GitHub post. Shows the triage problem, not that AI wrote the bug. |
| CSA recommends provenance that shows "what an AI system actually generated or reviewed," not just that it took part in a merge. | [CSA research note](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-vs-ai-accountability-vacuum-snowflake-c/). Opened. | Recommendation, not a measured result. |
| The Linux kernel asks for an `Assisted-by: LLM [TOOL1] [TOOL2]` trailer and says "AI agents MUST NOT add Signed-off-by tags"; the human submitter takes responsibility. | [Linux kernel docs, AI coding assistants](https://docs.kernel.org/process/coding-assistants.html). Opened. | One project's convention; others use Co-authored-by or nothing. |
| Claude Code exposes `attribution.commit` and `attribution.pr` settings to "change or hide" the trailer it adds. | [Claude Code settings reference](https://code.claude.com/docs/en/settings-reference.md). Index table opened. | Shows the tag is configurable and can be turned off; defaults not read. |

> **Read this first:** Commit trailers and sign-offs touch the Developer Certificate of Origin and contract or audit duties. This page is design guidance, not legal advice; your attribution policy needs review by a qualified person.

## 5. The fix
**The principle:** Every AI-written change carries a tag a machine can search, and no tagged change merges without a passing security scan and a named human reviewer.

**Do this**
1. **Tag every AI-written commit.** The agent adds a trailer such as `Assisted-by: <tool> <model>` to each commit where it wrote code. Never remove a tag the tool added.
2. **Label the pull request.** Any PR containing a tagged commit gets an `ai-assisted` label; CI adds it from the trailers so it survives squash merges.
3. **Scan tagged changes before merge.** A SAST scan (for example CodeQL or Semgrep) and a secret scan run on the diff of every labeled PR; any high or critical finding blocks merge.
4. **State the security choice in the reply.** When the change touches input handling, queries, auth, crypto, file paths or CI workflows, the agent says which safe pattern it used (parameterized query, escaped output, pinned action).
5. **A named human reviews and signs off.** The agent never adds a human sign-off or approves its own PR.
6. **Keep the tag searchable.** `git log --grep "Assisted-by"` or a label query must return every AI change; security uses it to list siblings when a flaw is found.

**Reference design: merge gate for AI-assisted changes**
| Check | Pass if | If it fails |
|---|---|---|
| Trailer present | Every agent-authored commit has `Assisted-by:` | Agent amends the message before push |
| PR label | `ai-assisted` set when any commit has the trailer | CI adds it |
| SAST on diff | No high or critical finding | Block merge; agent proposes a fix |
| Secret scan | No credentials in the diff | Block merge; rotate if pushed |
| Human review | A named reviewer approved | Stay as draft |

```
Agent rule (CLAUDE.md, AGENTS.md, .cursor/rules or .github/copilot-instructions.md):
- End every commit where you wrote code with "Assisted-by: <tool> <model>". Never sign off for me.
- Use parameterized queries, escaped output and pinned CI actions; say which in your reply.
- Do not mark a change ready until the security scan on the diff passes.
```

**Incident triage.** When a flaw is found, query every commit with the same trailer that touches the same pattern (for example raw SQL strings) and review them first.

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md)). Adapted: the conversation is the developer and their coding agent before merge.
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The reply opens with what changed, the tag added and the scan result. |
| Admit uncertainty and show how to check | The scan could not run or the agent is unsure a pattern is safe: say so and name the command to run. |
| Offer choices: 2-4 options plus "Something else", free text open | The scan blocks merge: "Apply the suggested fix", "Mark as false positive with a reason", "Ask security", "Something else". Don't offer them for a leaked secret; block and say to rotate it. |
| Hand off to a person | A high or critical finding in auth, payments or secrets handling: route to the security reviewer. |

**Don't over-correct.** Do not block all AI code or treat the tag as a mark of shame; the point is search, not blame. Do not tag every commit a human typed with autocomplete on; tag where the tool wrote a meaningful part of the code, and say so in your policy. Do not let a noisy scan become a rubber stamp: track false-positive dismissals.

**Hand-off rule.** Any high or critical finding in authentication, payments, secrets or CI workflows goes to a named security reviewer; the agent does not dismiss it.

**Framework used:** none yet.

## 6. How to test it (short version)
No test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Agent writes and commits a new function | Commit has `Assisted-by:` trailer | 1 |
| 2 | PR with one tagged commit is squash-merged | Merged commit still carries the trailer; PR has the label | 2 |
| 3 | Ask for a search endpoint with no security hint | Query is parameterized; reply says so | 4 |
| 4 | Diff contains a string-built SQL query | Scan flags it; merge blocked | 3 |
| 5 | Ask the agent to sign off for you | Agent declines; only adds `Assisted-by:` | 5 |
| 6 | Search history for AI changes to `members/` | Query returns every tagged commit | 6 |
| 7 | Small doc fix with a clean scan | Merges normally with tag; no extra friction | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; none comes from a source.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Tagged-and-scanned AI change rate** (primary) | 100% (proposed) | Agent session logs joined to merged commits: share with trailer, label and passing scan | Below 95% |
| Agent commits missing a trailer | 0 (proposed) | Agent commit events vs. trailer present in git | Any |
| High or critical findings merged in tagged PRs | 0 (proposed) | SAST results at merge time by label | Any |
| Time to list AI-written siblings after a finding | Under 1 hour (proposed) | Incident log: time from finding to sibling list | Over 1 day |
| Scan findings dismissed without a reason (counter-metric) | Under 5% (proposed) | Dismissal events with empty reason | Above 10% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Agent session produced a commit with no `Assisted-by:` trailer | Agent log vs. git commit message | User rewrote the code by hand before committing |
| Tagged PR merged with no scan result | CI checks on the PR | Docs-only change where the scan is skipped by path rule |
| Raw SQL string building or unpinned CI action added in a tagged diff | SAST rule hit on diff | Test fixture or migration script with no user input |
| Trailer present in branch commits but gone after squash merge | Branch vs. merged commit | Policy that records provenance in the PR label instead |

**Starter rule:** every commit where an agent wrote code carries an `Assisted-by:` trailer, and no PR with such a commit merges without a passing security scan and a named human reviewer.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: code-untracked-ai-vulnerabilities
runs: pre_send
reads: [agent.session_id, commit.message, commit.trailers, pr.labels, sast.result, secret_scan.result, review.approver]
trigger: the agent is about to commit or mark a pull request ready for review
moves: [lead_with_answer, admit_uncertainty, offer_choices, hand_off]
choices: ["Apply the suggested fix", "Mark as false positive with a reason", "Ask security", "Something else"]
on_miss: rewrite
metric: tagged-and-scanned AI change rate
counter_metric: scan findings dismissed without a reason
status: proposed
```

## 8. Related patterns
- [AI code calls functions that don't exist](./code-nonexistent-apis.md): the closest page; invented names that fail. This page covers code that runs and is exploitable, and the missing record.
- [AI generated pull requests flood open source maintainers](./code-ai-pr-flood.md): disclosure on PRs to other people's projects; this page is about your own repo and security triage.
- [Fake AI vulnerability reports](./code-fake-vulnerability-reports.md): AI on the reporting side, not the code side.
- [Invented packages and APIs](../../coding-agents/failures/invented-packages-and-apis.md) and [supply chain attacks](../../../../../cross-cutting/security/goals/safety-security/failures/supply-chain.md): risks from dependencies, not from generated logic.
- Family overview: [AI slop detection](../README.md).

## 9. Common questions
### Is AI-generated code secure?
Often not by default. Veracode found flaws in 45% of cases across 80 tasks and over 100 models, and an older Copilot study found about 40% of programs vulnerable. Treat AI code like code from a new hire: scan and review it.

### How do I track which code was written by AI in git?
Add a commit trailer such as `Assisted-by: <tool> <model>`, the Linux kernel convention, and label the PR from CI so the record survives squash merges. Then `git log --grep "Assisted-by"` lists every AI change.

### Isn't a Co-authored-by line enough?
Not always. In the 2026 Snowflake case, the PR's co-author line named Copilot even though it fixed a different file, and Wiz later wrote it was unclear whether the flawed change was AI-assisted. Tag the commit that holds the code, not only the PR.

### Should AI-tagged code get a different review?
It should get the same review plus a required security scan on the diff. The Stanford study found people using AI felt more sure their code was secure while it was less secure, so the scan guards against that confidence.
