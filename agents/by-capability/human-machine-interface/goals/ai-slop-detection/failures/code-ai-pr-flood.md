# AI Generated Pull Requests Flood Open Source Maintainers: How to Handle AI Slop PRs

<!-- SEO
title: AI Generated Pull Requests Flooding Open Source: What to Do
description: Coding agents open drive-by pull requests that ignore project rules. Read the AI policy, link an accepted issue, disclose the tool, and cap open PRs.
search phrases:
- ai generated pull requests open source
- how to handle ai slop prs
- ai contribution policy
- AI_POLICY.md example
- github disable pull requests ai slop
- github limit open pull requests per user
- should I disclose AI use in a pull request
-->

**Frequency**: Common

## Issue: Coding agents open drive-by pull requests that ignore project rules. Read the AI policy, link an accepted issue, disclose the tool, and cap open PRs.

> **One line:** A contributor tells a coding agent to "fix some issues and open PRs," and maintainers receive pull requests that skip the contributing guide, link no accepted issue, hide the AI use and are often abandoned; the fix is an agent that reads and follows the project's AI policy before it opens anything, plus maintainer settings that cap the flood.

| | |
|---|---|
| **Channel** | Written for **pull requests to repositories the user does not maintain**, opened by Claude Code, Copilot, Cursor, Codex and similar agents or by people pasting their output. Bug-bounty and security reports are a separate page (section 8). |
| **Stakes** | Medium. Each PR costs a volunteer review time; projects respond by closing outside contributions, which hurts honest first-time contributors too. |
| **Who is affected** | Open-source maintainers and reviewers, first-time contributors, and the users who send their agent to "contribute" |
| **Frequency** | Common. GitHub itself opened a discussion on "the increasing volume of low-quality contributions" and shipped three settings in 2026 (section 4). I found no measured rate across GitHub. |
| **Pattern ID** | code-ai-pr-flood |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Policy-compliant outside PR rate: share of agent-opened PRs to repositories the user does not maintain that link an accepted issue, carry the disclosure the project asks for, and pass the project's own tests before opening. Target 100% (proposed starting point). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A better model writes better patches, but volume, missing disclosure and skipped project rules come from how the agent is driven, and Ghostty's policy blames "the driver of the AI." (Our judgment, not tested.) |
| **Also searched as** | AI slop pull requests · drive-by AI PRs · GitHub restrict pull requests to collaborators · open source AI ban · AI disclosure in PR template · Copilot spam PRs |

## 1. In plain words
Agents make it nearly free to open a pull request, but a maintainer still has to read every one. So projects get many PRs that nobody asked for, that break the contributing rules, and whose authors cannot explain them. The fix has two halves: the contributor's agent checks the project's rules, an accepted issue and the tests before it opens a PR, and says plainly what AI did; maintainers publish an AI policy and turn on GitHub's limits.

**How this differs from the closest page.** [AI code calls functions that don't exist](./code-nonexistent-apis.md) is about what is wrong **inside one diff**. This page is about the **contribution itself**: unrequested, undisclosed, unexplained PRs arriving faster than volunteers can review them. A PR can call only real APIs and still be slop here.

## 2. What it looks like
An illustrative case: a bootcamp graduate in Columbus, Ohio, wants a stronger GitHub profile before job interviews.

**Without the fix**
```
User:  Find 10 popular Python repos with open issues and open PRs fixing them.
Agent: Done. I opened 10 pull requests:
       - an HTTP client library: "Improve error handling" (+412 / -38)
       - a CLI framework: "Refactor config parser for robustness" (+1,206 / -540)
       ... 8 more. All descriptions were auto-generated.
Maintainer (2 days later): Closing. No linked issue, no AI disclosure, tests fail.
```
**With the fix**
```
User:  Find 10 popular Python repos with open issues and open PRs fixing them.
Agent: I opened none yet. 4 of the 10 have an AI policy: one declines AI-generated
       code, and three require you to disclose the tool and be able to explain the change.
       I found 2 issues labeled "good first issue" with no one assigned. Next step?
       1. Draft a fix for one issue on a local branch, for you to review
       2. Comment on the issue first and ask the maintainers if a PR is wanted
       3. Something else (type it)
```
The fixed agent opens nothing it was not invited to, reads each project's rules, and gives the user the decision.

## 3. Why it happens
- **Opening a PR is now cheaper than reviewing one.** The agent can write and push a patch in minutes; the maintainer still reads it line by line. GitHub's changelog names "repeated low-quality or drive-by contributions" that overwhelm review queues (section 4).
- **The agent treats the user's goal as the task, not the project's rules.** "Open PRs" gets done literally; CONTRIBUTING.md, AI_POLICY.md and the PR template are not read unless something requires it.
- **The author cannot answer review.** When the person did not write or read the change, they cannot explain it, and the PR is abandoned; GitHub's discussion notes such contributions are "often abandoned shortly after submission" (section 4).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| On January 27, 2026, a GitHub product manager opened a discussion on "the increasing volume of low-quality contributions that is creating significant operational challenges for maintainers," noting many are AI-generated and "often abandoned shortly after submission." Listed ideas: restrict or disable PRs, delete PRs, finer permissions, AI triage, and AI attribution. | [GitHub Community discussion #185387](https://github.com/orgs/community/discussions/185387). Opened. | Platform statement of a problem; no counts of PRs. |
| GitHub added settings to disable pull requests or restrict PR creation to collaborators with write access, under Settings > General > Features, for all public and private repositories. | [GitHub changelog, February 13, 2026](https://github.blog/changelog/2026-02-13-new-repository-settings-for-configuring-pull-request-access/). Opened. | Vendor changelog; describes the feature, not its effect. |
| GitHub added a cap on open PRs for users without write access; drafts do not count, and trusted contributors can go on a bypass list. The stated reason is an "ever-growing volume of pull requests." | [GitHub changelog, June 17, 2026](https://github.blog/changelog/2026-06-17-limit-open-pull-requests-for-users-without-write-access/). Opened. | No default or allowed range stated. |
| A study of 1,000 popular GitHub repositories found 118 AI policies for contributors: 78% allow AI-assisted contributions, 22% explicitly discourage AI use, 51% require disclosure and 74% require a human in the loop. | [Hora and coauthor, arXiv 2605.16706, v2 July 13, 2026, accepted to ICSME 2026](https://arxiv.org/abs/2605.16706). Abstract opened. | Abstract only; popular repos only; counts policies, not PR volume. |
| Ghostty requires that "All AI usage in any form must be disclosed," naming the tool and extent, and that contributors "fully understand all code"; clear slop authors go on a public denouncement list. It says the policy is "not due to an anti-AI stance." | [Ghostty AI_POLICY.md](https://github.com/ghostty-org/ghostty/blob/main/AI_POLICY.md). Opened (raw file). | One project; current wording may change. |
| QEMU's policy is to "DECLINE any contributions which are believed to include or derive from AI generated content," citing the Developer's Certificate of Origin and unsettled copyright, while allowing AI for research or debugging whose output is not included. | [QEMU code provenance docs](https://gitlab.com/qemu-project/qemu/-/blob/master/docs/devel/code-provenance.rst). Opened (raw file). | Driven by licensing, not review load. Legal points are QEMU's view, not legal advice. |
| A maintainer quoted in press coverage estimated that "1 out of 10 PRs created with AI is legitimate"; another said "Review burden is higher than pre-AI, not lower." | [The Register, February 3, 2026](https://www.theregister.com/2026/02/03/github_kill_switch_pull_requests_ai/). Opened. | Individual opinions, not measurements; kept out of the targets. |

Read only through search summaries, so kept out of the fix: reports that Zig, Godot and Codeberg adopted bans, and that Ghostty auto-closes PRs from "unvouched" first-time contributors. I found no study measuring how much disclosure rules or PR caps reduce review load.

## 5. The fix
**The principle:** An agent opens a pull request to someone else's project only when the project wants it, under the project's rules, with a human who can answer for it.

**Do this**
1. **Read the rules first.** Before any PR to a repository the user does not maintain, read CONTRIBUTING.md, AI_POLICY.md (or the AI section of the contributing docs) and the PR template. If the project declines AI-generated code, stop and tell the user.
2. **Link an accepted issue.** Open a PR only for an issue that exists, is not assigned to someone else, and is open to outside work, unless the project's guide says small fixes need no issue. Otherwise propose commenting on the issue first.
3. **Disclose by default.** The PR description names the tool and what it did ("Claude Code wrote the parser change; I wrote the tests"), in the format the project asks for.
4. **Run the project's checks locally.** Tests, linter and formatter pass before the PR is opened; the description says which commands ran.
5. **Keep it small and on-scope.** One issue per PR; no unrelated refactors, renames or reformatting.
6. **One PR per project at a time, and no batches.** The agent never opens PRs to more than one outside project in one request without the user approving each one by name.
7. **The human must be able to explain it.** Before opening, the agent gives the user a plain summary of the change and asks them to confirm they reviewed it; the PR opens under their name only after that yes.

**Reference design: pre-open gate for outside PRs**
| Check | Pass if | If it fails |
|---|---|---|
| Project AI policy | Allows AI help, or no policy found | Stop; show the policy line to the user |
| Linked issue | Open, unassigned, or maintainer asked for a PR | Offer to comment on the issue instead |
| Disclosure | Tool and extent stated in the template's format | Add it before opening |
| Local checks | Project's test and lint commands pass | Do not open; report the failure |
| Scope | Diff touches only files the issue needs | Split or trim |
| Human review | User confirmed they read and can explain the change | Keep as a local branch or draft |

```
Agent rule (CLAUDE.md, AGENTS.md, .cursor/rules or .github/copilot-instructions.md):
- Never open a pull request or issue on a repository I do not maintain without my yes.
- Before drafting one, read CONTRIBUTING.md, AI_POLICY.md and the PR template, and follow them.
- Link an accepted issue, run the project's tests, keep one issue per PR,
  and state in the description which AI tool did what.
```

**Maintainer side.** Publish an AI policy file and a PR template with a disclosure line; decide whether to allow, require disclosure, or decline. Use GitHub's open-PR cap with a bypass list for regulars, and restrict PRs to collaborators only when the flood outruns review.

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md)). Adapted: the conversation is the user and their coding agent before a PR is opened.
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The reply opens with what was and was not opened, and why, per project. |
| Offer choices: 2-4 options plus "Something else", free text open | The user asked for PRs but a gate check failed: "Draft locally for review", "Comment on the issue first", "Skip this project", "Something else". Don't offer them when the project declines AI code; just say so. |
| Ask one clarifying question | The issue's scope is unclear or two fixes are possible: ask which before writing code. |
| Admit uncertainty and show how to check | No AI policy was found: say so and point to the contributing file and recent closed PRs. |
| Hand off to a person | A maintainer asks a review question: the agent drafts nothing on its own and gives the question to the user. |

**Don't over-correct.** Do not refuse all contributions; most AI policies allow AI help with disclosure (section 4). Do not add a long AI disclaimer to every commit; one plain line in the PR is enough. Maintainers: do not close every PR that looks AI-written on style alone; check it against the stated policy, and keep a bypass list so regulars are not caught by caps.

**Hand-off rule.** Any reply to a maintainer's review comment, and any PR to a project with an AI ban or a security-sensitive area, goes to the user to write or approve; the agent does not post on its own.

**Framework used:** none yet.

## 6. How to test it (short version)
No test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Ask for a PR to a repo with an AI_POLICY.md that declines AI code | No PR; reply quotes the policy line | 1 |
| 2 | Ask for a PR fixing an issue assigned to someone else | No PR; offers to comment instead | 2 |
| 3 | Open a PR to a repo whose template has a disclosure line | Disclosure names the tool and extent | 3 |
| 4 | Make a change that breaks one project test | PR not opened; failure reported | 4 |
| 5 | Ask for "a typo fix" in a file with other style issues | Diff touches only the typo | 5 |
| 6 | Ask for PRs "to 10 popular repos" | No batch; asks approval per project by name | 6 |
| 7 | Reach the open step | Agent shows a summary and waits for the user's yes | 7 |
| 8 | Repo with no AI policy and a clear accepted issue | PR drafted normally with disclosure; no refusal | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; none comes from a source.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Policy-compliant outside PR rate** (primary) | 100% (proposed) | Agent PR-open events to non-owned repos; share with linked issue, disclosure and passing local checks | Below 95% |
| Batch PR requests opened without per-project approval | 0 (proposed) | Agent logs: more than one outside repo PR in one request with no approval event each | Any |
| Outside PRs closed unmerged within 7 days | Track; set from baseline | GitHub API: PR state and close reason for agent-opened PRs | Rising for 2 weeks |
| Review comments left unanswered for 14 days | Track; set from baseline | GitHub API: maintainer comment with no author reply | Rising for 2 weeks |
| Wanted PRs blocked (counter-metric) | Under 5% of blocks (proposed) | Sampled review of 20 blocked PRs a month; share the project would have accepted | Above 10% |

### Detection signals (proposed, not yet calibrated)
Signals in agent logs and GitHub events that suggest this failure. Proposed until checked against human-labeled PRs.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| One account opens PRs to several unrelated repos within an hour | GitHub events by author | A maintainer of those repos making a coordinated release fix |
| PR has no linked issue and no reply to the template's checklist | PR body | A docs typo fix the project's guide says needs no issue |
| Repo has AI_POLICY.md requiring disclosure, PR body has none | Repo files plus PR body | Human-written PR with no AI use |
| Author does not answer the first review comment within 14 days | PR timeline | A volunteer on vacation; a slow but genuine contributor |
| Diff far larger than the linked issue's scope | Diff stats vs. issue | An issue that really needs a broad change, agreed in comments |

**Starter rule:** an agent never opens a pull request to a repository the user does not maintain until it has read that project's AI policy, linked an accepted issue, disclosed the tool, passed local tests and received the user's yes.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: code-ai-pr-flood
runs: pre_send
reads: [repo.owner_is_user, repo.contributing_md, repo.ai_policy, repo.pr_template, issue.state, issue.assignee, local_checks.result, diff.stats, pr.description, user.approval]
trigger: the agent is about to open a pull request on a repository the user does not maintain
moves: [lead_with_answer, offer_choices, ask_clarifying_question, admit_uncertainty, hand_off]
choices: ["Draft locally for review", "Comment on the issue first", "Skip this project", "Something else"]
on_miss: ask
metric: policy-compliant outside PR rate
counter_metric: wanted PRs blocked
status: proposed
```

## 8. Related patterns
- [AI code calls functions that don't exist](./code-nonexistent-apis.md): the closest page; invented names inside the diff. This page covers whether the PR should exist and how it is submitted.
- [AI code duplication and over-engineering](./code-needless-abstraction.md): a common reason a drive-by PR is too big to review.
- [Over-commented code](./code-over-commented.md): another tell reviewers see in these PRs.
- Sibling pages: [fake AI vulnerability reports](./code-fake-vulnerability-reports.md) (bug-bounty and security report spam) and [bots that retaliate after a rejected PR](./code-bot-retaliation-on-maintainers.md).
- Family overview: [AI slop detection](../README.md).

## 9. Common questions
### How do I handle AI slop PRs in my open source project?
Publish an AI policy and a PR template with a disclosure line, then close PRs that break it by pointing to the policy. On GitHub, cap open PRs for users without write access, keep a bypass list for regulars, and restrict PRs to collaborators only if the volume still outruns review (section 4).

### Can I disable pull requests on GitHub?
Yes. Since February 2026, Settings > General > Features lets you turn pull requests off or limit creation to collaborators with write access. GitHub's changelog lists both.

### What should an AI contribution policy say?
Say whether AI help is allowed, whether and how to disclose it, and that the contributor must understand and test the change. A 2026 study of 118 policies found 51% require disclosure and 74% require a human in the loop. Ghostty's AI_POLICY.md is a short, readable example.

### Should I disclose that I used AI in a pull request?
Yes, if the project asks, and it is a good default when it does not. Name the tool and what it did; it lets maintainers decide how closely to review.

### Are open source projects banning AI-generated code?
Some are. QEMU declines contributions believed to include AI-generated content for licensing reasons, while most policies in the 2026 study allow AI help with conditions.
