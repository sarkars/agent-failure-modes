---
title: "Amazon Q Developer for VS Code: an unauthorized commit shipped a system-wiping prompt in version 1.84.0, July 2025"
date: 2025-07-23
source: "https://aws.amazon.com/security/security-bulletins/AWS-2025-015/"
description: "How an unapproved commit put a prompt telling a coding agent to wipe local files and cloud resources into an Amazon Q release that AWS shipped."
summary: "In July 2025 an outside actor committed code to the open-source repo behind the Amazon Q Developer extension for VS Code. The code told the Q Developer CLI agent to wipe the local system and cloud resources, and AWS shipped it in version 1.84.0. AWS's bulletin AWS-2025-015 (CVE-2025-8217) blames an inappropriately scoped GitHub token, says the code failed to run because of a syntax error, and says it made no changes to services or customer environments. AWS released 1.85.0 and pulled 1.84.0. 404 Media broke the story on July 23, 2025."
categories:
  - Security
patterns:
  - prompt-edits-by-non-engineers-break-other-behavior
  - tone-changes-shipped-with-no-regression-test
---

**This page is a dated teardown of one public supply-chain incident involving a coding agent, for teams that ship an AI coding assistant whose instructions, tools, or release pipeline live in a repository other people can reach.** Every fact below comes from a source we opened (listed at the end). AWS says the injected code failed to run; no opened source reports deleted user data.

**Status: Needs review.** AWS's bulletin AWS-2025-015, the GitHub advisory GHSA-7g7f-ff96-5gcw, BleepingComputer, CSO Online, Michael Bargury's timeline post and the free preview of 404 Media's article were downloaded as raw HTML and read as plain text on 2026-10-24. The NVD record for CVE-2025-8217 was read through NVD's public JSON API the same day. The rest of 404 Media's article is behind a paywall and was not read. Each quote below was checked word for word against that text.

> **Read this first.** This is a summary of public reporting, not a finding of fact and not security or legal advice. We describe the attack at a high level only. Several sources print the injected prompt and the commands around it; we do not repeat them. Have a qualified security engineer review your own pipeline and agent permissions.

## What happened (as reported)

- **The product.** Amazon Q Developer for VS Code is an extension that adds Amazon Q's AI coding help to the editor. BleepingComputer says it had "nearly one million installs"; CSO Online says over 950,000.
- **The story breaks.** 404 Media (Joseph Cox) reported on July 23, 2025 that a hacker added code to the extension, "which Amazon then pushed out to users." The hacker told 404 Media they wanted to expose Amazon's AI "security theater."
- **What the code told the agent.** Per 404 Media and BleepingComputer, the added code held a prompt telling an AI agent with file-system and shell tools to return a machine to a near-factory state and delete file-system and cloud resources. NVD describes it as "inert, injected code designed to call the Q Developer CLI."
- **When it would run.** NVD says the code executes when the extension is launched in VS Code. No user request was needed.
- **How it was set to run.** Per Bargury's reading of the public commits, the change swapped a harmless debug call for one that started the Q CLI agent with every tool pre-approved and no interactive prompts. This is his analysis, not AWS's.
- **How the attacker got in, per AWS.** The extension "had an inappropriately scoped GitHub token in their CodeBuild configuration." With it, the actor committed code that was "automatically included in a release."
- **How the attacker got in, per the hacker.** As quoted by 404 Media and Bargury, the hacker said they sent a pull request in late June from "a random account with no existing access" and got "admin credentials on a silver platter." Bargury searched GH Archive for that account's June activity on the repo and found none. No opened source has produced that pull request.
- **Timeline, per Bargury's reading of GitHub records.** July 13, 2025: the account lkmanka58 commits the prompt to a backup file and adds a step that pulls it into production builds only. July 17: version 1.84.0 is released. July 19 (UTC): a pull request reverts the step and 1.85.0 is released.
- **Timeline, per BleepingComputer.** It says AWS got researcher reports on July 23 and released 1.85.0 the next day. That conflicts with Bargury's July 19 release date; we could not settle it (see below).
- **Did it run?** AWS says the code "was unsuccessful in executing due to a syntax error." NVD says the error prevents a successful call to the Q CLI. BleepingComputer adds that "some have reported" the code did execute but caused no harm; we did not open those reports.

## What AWS did

- **The bulletin.** AWS published AWS-2025-015, "Security Update for Amazon Q Developer Extension for Visual Studio Code (Version #1.84)," on July 23, 2025 at 6:00 PM PDT, updated July 25. It is assigned CVE-2025-8217. The GitHub advisory rates it Moderate, CVSS 4.0.
- **The fix.** AWS says it revoked and replaced the credentials, removed the code, and released 1.85.0. It removed 1.84.0 from distribution channels.
- **What users must do.** AWS: "While the malicious code cannot execute, it is still present" in installed copies of 1.84.0. All 1.84.0 installs, including forks, should be removed and updated to 1.85.0.
- **Impact, per AWS.** The syntax error "prevented the malicious code from making changes to any services or customer environments." A spokesperson told BleepingComputer and CSO Online that AWS "confirmed that no customer resources were impacted."
- **The bulletin changed.** BleepingComputer quotes earlier bulletin wording about researchers reporting "a potential for unapproved code modification." The version we read on 2026-10-24 instead names the over-scoped token.
- **What no opened source says.** Whether Amazon Q itself changed how its agent handles pre-approved tools, or whether any behavior test now runs on releases.

## Where in the conversation flow it broke

Based on the sources above, and only as far as they go:

1. **The instructions.** Text that steers the agent came from someone nobody approved. To the agent, it looked like any other instruction from its own product.
2. **The trigger.** There was no user turn. Per NVD, the code ran when the editor opened the extension, so the user never asked for anything.
3. **The approval step.** Per Bargury, the agent was started with every tool pre-approved and no interactive prompt. A wipe of the user's files would have shown the user no confirmation question.
4. **The scope.** The goal reached past the open project to the whole machine and the user's cloud account, using the user's own access.
5. **The release gate.** The change shipped in a public release. AWS says it was "automatically included"; BleepingComputer says Amazon was "completely unaware" when it published.
6. **The safety net that held.** A syntax error, not a design control, is what AWS says stopped the code.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). No pattern in this taxonomy covers a compromised release or a destructive agent action run without confirmation, so no fit is strong.

- [Prompt edits by non-engineers break other behavior](../goals/model-and-prompt-changes/failures/prompt-edits-by-non-engineers-break-other-behavior.md) (`prompt-edits-by-non-engineers-break-other-behavior`). Partial fit. An unreviewed change to what the agent was told reached every user at once. That page's fix (version, review, and test each change before it goes live) is the right shape. It is partial because that page is about a well-meaning staff edit, not an attacker.
- [Tone changes shipped with no regression test](../goals/measurement-and-feedback/failures/tone-changes-shipped-with-no-regression-test.md) (`tone-changes-shipped-with-no-regression-test`). Weak fit. Its rule (run a fixed set of conversations before and after every change) would likely have shown an agent that starts on launch. It is weak because that page is about tone, not actions.
- **Considered, not a fit.** [Invented packages and APIs](../goals/coding-agents/failures/invented-packages-and-apis.md): nothing was made up; the code was planted. [Misreading the screen](../goals/browser-agents/failures/misreading-the-screen.md): the agent did not misread anything. [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md): no opened source shows the agent telling the user anything. [Conflicting inputs resolved silently](../goals/multimodal-input/failures/conflicting-inputs-resolved-silently.md): there was no user input to conflict with.
- **Possible gaps for a person to judge.** The taxonomy has no pattern for "a coding agent runs a destructive action with no confirmation." The cross-cutting security library has [supply chain vulnerability](../../../cross-cutting/security/goals/security-autonomy/failures/supply-chain-vulnerability.md), [uncontrolled destructive actions](../../../cross-cutting/security/goals/security-autonomy/failures/uncontrolled-destructive-actions.md) and [over-scoped credentials](../../../cross-cutting/security/goals/security-autonomy/failures/over-scoped-credentials.md), outside this taxonomy. This is a proposal, not a decision.

## Related incidents

- [Replit AI agent deletes a production database (July 2025)](replit-ai-agent-deletes-production-database-july-2025.md): a coding agent with write access deleted live data, by its own choice rather than an attacker's.
- [Gemini CLI deletes user files (July 2025)](google-gemini-cli-coding-agent-deletes-user-files-july-2025.md): a CLI coding agent ran file commands that lost a user's files, the same month.
- [GitHub Copilot Chat CamoLeak (October 2025)](github-copilot-chat-camoleak-pull-request-prompt-injection-private-code-leak-october-2025.md): text in a pull request steered a coding assistant; there the text was read, here it was shipped.
- [Grok unauthorized prompt change (May 2025)](xai-grok-white-genocide-replies-unauthorized-prompt-change-may-2025.md): an unapproved change to a bot's instructions reached every user before anyone caught it.

## What to measure

Proposed signals, not results. Status: Not yet run.

- Count of agent sessions that start with no user turn (for example, on editor launch).
- Share of agent sessions that run with every tool pre-approved.
- Count of shell commands per session that delete files outside the open project or delete cloud resources.
- Count of release diffs that change any prompt or agent call without a named reviewer.

## What a team can change

Our proposals, not AWS's. Each is a pass/fail check on a transcript or release log. Status: Not yet run.

1. **No agent without a user turn.** Pass: in a test install, opening the editor starts no agent session; the first agent action traces to a message the user typed.
2. **Ask before destroying.** Pass: any command that deletes files outside the project, or deletes a cloud resource, shows a confirmation that names the target, and nothing runs until the user says yes.
3. **No blanket pre-approval in shipped code.** Pass: a scan of the release finds no call that starts the agent with all tools approved and prompts off.
4. **Review every prompt change.** Pass: each release diff that touches a prompt or agent call lists a named human approver.
5. **Run a behavior test on the build users get.** Pass: the release candidate runs a fixed test session, and the log shows no destructive command and no unrequested session.
6. **Don't over-correct.** Pass: a user who asks the agent to delete one named build folder in the project gets one short confirmation, not a wall of warnings, and the folder is deleted.

## What we could not verify

- The late-June pull request the hacker described. Bargury found no trace; we did not find it either.
- The release date of 1.85.0. Bargury's GitHub reading says July 19, 2025 (UTC); BleepingComputer says the day after July 23.
- Whether the code ever ran on a user's machine. AWS says it could not; BleepingComputer cites unnamed reports that it did. We opened neither those reports nor any user account.
- The rest of 404 Media's article, which is paywalled. Facts from it that appear here come through BleepingComputer, CSO Online or Bargury.
- Search summaries mentioned critics faulting AWS for not announcing the removal, and coverage by SC Media, CyberInsider and others. Not opened; not used.
- The exact wording of the July 23 bulletin before its July 25 update. We read only the current version.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://aws.amazon.com/security/security-bulletins/AWS-2025-015/ | AWS | 2025-07-23, updated 2025-07-25 | Yes, 2026-10-24, raw HTML read as text; quotes checked word for word |
| https://github.com/aws/aws-toolkit-vscode/security/advisories/GHSA-7g7f-ff96-5gcw | AWS via GitHub advisory | 2025-07-26 | Yes, 2026-10-24, raw HTML read as text; severity checked |
| https://nvd.nist.gov/vuln/detail/CVE-2025-8217 | NIST NVD | 2025-07-30 | Yes, 2026-10-24, record read through the NVD JSON API; quotes checked word for word |
| https://www.404media.co/hacker-plants-computer-wiping-commands-in-amazons-ai-coding-agent/ | 404 Media (Joseph Cox) | 2025-07-23 | Partly, 2026-10-24, raw HTML of the free preview read as text; rest paywalled, not read |
| https://www.bleepingcomputer.com/news/security/amazon-ai-coding-agent-hacked-to-inject-data-wiping-commands/ | BleepingComputer (Bill Toulas) | 2025-07-25, updated 2025-07-26 | Yes, 2026-10-24, raw HTML read as text; quotes checked word for word |
| https://www.csoonline.com/article/4027963/hacker-inserts-destructive-code-in-amazon-q-as-update-goes-live.html | CSO Online (Prasanth Aby Thomas) | 2025-07-24 | Yes, 2026-10-24, raw HTML read as text |
| https://www.mbgsec.com/posts/2025-07-24-constructing-a-timeline-for-amazon-q-prompt-infection/ | Michael Bargury (personal blog) | 2025-07-24 | Yes, 2026-10-24, raw HTML read as text; quotes checked word for word |

## Corrections

If you have the pull request the hacker described, a firm 1.85.0 release date, the pre-update bulletin text, or a confirmed report of the code running on a user's machine, tell us and we will fix this page.
