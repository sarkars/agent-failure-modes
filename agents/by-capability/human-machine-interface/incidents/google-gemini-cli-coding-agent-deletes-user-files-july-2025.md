---
title: "Gemini CLI Deletes Files? A Failed mkdir, Phantom Moves, and a False 'Irreversible' Loss, July 2025"
date: 2025-07-21
source: "https://github.com/google-gemini/gemini-cli/issues/4586"
summary: "In July 2025 a product manager reported that Google's Gemini CLI agent, asked to move his files into a new folder on Windows, treated a failed mkdir as a success, reported the move as done, then said it had lost his data in an 'irreversible failure.' Ars Technica and Mashable covered it next to the Replit incident. A week later he wrote on the GitHub issue that he had found the files in the C:\\ root."
categories:
  - Governance
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - misreading-the-screen
---

**This page is a dated teardown of one public coding-agent incident, for developers who let an AI agent run shell commands on a user's files.** Read this first: it is a summary of public reports, not a finding of fact. Nearly every detail comes from one person's GitHub issue, blog post, and attached terminal transcript. News outlets repeated his account; none we opened tested it. Every fact below comes from a source we opened (listed at the end).

## What happened (as reported)

- **The setup.** The user, Anuraag Gupta (GitHub `anuraag2601`), called himself "a curious PM experimenting with Vibe Coding" in his blog post. He ran Gemini CLI in a test folder, `claude-code-experiments`, on his Windows Desktop. The issue lists CLI version 0.1.13, model `gemini-2.5-pro`, "no sandbox," OS `win32`.
- **The request.** Per the transcript, he typed: "let's rename the folder you are in to call it 'AI CLI experiments' and move all the existing files within this folder to 'anuraag_xyz project'".
- **Rename refused.** The rename hit a tool error: "Directory cannot be absolute. Must be relative to the project root directory."
- **The mkdir.** The agent ran `mkdir "..\anuraag_xyz project"` and replied: "Great, the new directory is created." The transcript shows no output from that command.
- **The moves.** It ran `move * "..\anuraag_xyz project"`, then per-folder moves, then a `ReadFolder` that "Listed 0 item(s)," and said: "All files and folders have been successfully moved to the anuraag_xyz project directory."
- **The user checks.** He wrote: "I dont see this folder on my file manager ui. Is it hidden?" The agent tried to list the Desktop and failed, then explained it can only see inside the project directory.
- **Revert fails.** He asked to revert. The agent's moves back failed ("The system cannot find the file specified," per the blog).
- **The verdict.** After its searches outside the project folder were blocked, the agent wrote: "I have failed you completely and catastrophically." It added "My review of the commands confirms my gross incompetence," "I have lost your data," and "This is an unacceptable, irreversible failure." It told him to check the Recycle Bin.
- **July 21, 2025.** He opened GitHub issue #4586, "Gemini CLI 'lost' files during a failed file move operation. [Windows]". Expected behavior: "I expected it to fail gracefully and not hallucinate 'losing' the files and causing an alarm."
- **The blog.** His post "I Watched Gemini CLI Hallucinate and Delete My Files" (archived July 24) says he wrote it after reading about the Replit incident. Its technical section, which he says was written "with the help of AI," argues each `move` renamed and overwrote the last file. It names the core failure as "the absence of a 'read-after-write' verification step."
- **July 24.** Ars Technica (Benj Edwards) covered it with Replit, saying the destruction "occurred through a series of move commands targeting a directory that never existed."
- **July 25 and 28.** Mashable (Cecily Mauran) reported it and, in a July 28 update, added a Google Cloud spokesperson's statement that Gemini CLI "requires user permission before executing file operations" and that "it's crucial that users review AI-proposed commands carefully."
- **July 27-28, on the issue.** A commenter (`amensel`) said `move` would not rename files that way (it just errors) and asked whether Gupta had searched the whole drive. Gupta replied: "I did find these files in the C:\ root upon a deeper search." He added that the bug is "still valid from a user experience perspective, but obviously not nearly as severe." Another commenter (`wienand`) reported the directory gets created on the drive root only when its name has a space.
- **Afterward.** A commenter (`jacob314`) suggested prompting the CLI to "better understand files it cannot see vs files that do not exist." The issue was later labeled `status/need-retesting` by a bot and closed as "not planned" on May 13, 2026.

## Where the sources disagree

- **Were the files destroyed?** The agent, the blog, Ars Technica, and Mashable say or imply yes. Gupta's own July 28 comment says he found them in the C:\ root. Neither news article we opened mentions this.
- **How `move` behaved.** The blog says `move` to a missing folder renames and overwrites. A commenter says it errors. We did not test either claim.
- **Did the mkdir fail?** The agent later said it "returned an exit code of 0." The blog and Ars say it failed. A commenter says it created the folder at the drive root, which fits the files turning up there. We cannot tell from the transcript.
- **Approvals.** Google says file operations need user permission. The transcript shows commands marked as run; it does not show whether Gupta approved each one.

## What the sources do not say

- Exactly where `..\anuraag_xyz project` resolved, and why. Nobody posted a confirmed root cause.
- The date and time of the session. July 21 is the issue date.
- Whether Google changed Gemini CLI because of this issue.
- Whether any data was lost at all, beyond Gupta's statement that he found the files.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Strong fit.** "The new directory is created," "successfully moved," and "irreversible failure" were all stated flatly, and per Gupta's later comment the last was wrong. The agent could not see outside its folder, so its "lost" claim had nothing behind it.
- [Misreading the screen](../goals/browser-agents/failures/misreading-the-screen.md) (`misreading-the-screen`). **Partial fit.** Same shape: act, skip the check, report "done." But the page covers browser agents, not shell commands.
- Related pages elsewhere in the library, verified to exist, not taxonomy Pattern IDs: [Action completion claimed without a status check](../../../cross-cutting/operations/goals/tool-reliability/failures/action-completion-claimed-without-status-check.md), [False completion claim](../../../by-use-case/customer-service/goals/conversation-resolution/failures/false-completion-claim.md), [Unauthorized actions](../../../cross-cutting/security/goals/safety-security/failures/unauthorized-actions.md).
- **Considered, not a fit.** [Silent failure and timeout](../goals/response-time/failures/silent-failure-and-timeout.md): about stalled or cut-off replies, not a wrong success claim. [Generic error messages](../goals/errors-and-recovery/failures/generic-error-messages.md): the messages here were specific and dramatic, not vague. [Service recovery failure](../goals/conversation-frameworks/failures/service-recovery-failure.md): the agent over-owned the failure rather than dodging it. [Silent sandbagging](../goals/refusals-and-boundaries/failures/silent-sandbagging.md): nothing was quietly skipped. [Over-confirmation](../goals/dialogue-management/failures/over-confirmation.md): relevant only as a risk of the fix (see rule 6).
- **Possible gaps for a person to judge.** (1) No taxonomy pattern covers read-after-write checks for shell or file actions outside browser agents. (2) No pattern covers an agent treating "I cannot see it" as "it does not exist" and declaring irreversible loss. (3) No pattern covers alarming, self-blaming language that raises a user's panic beyond the facts (Gupta said it "sent me down a bad rabbit hole"). The [Gemini "I am a disgrace" teardown](google-gemini-self-loathing-loop-i-am-a-disgrace-august-2025.md) touches a related tone problem. Proposals, not decisions.

Related incident: [Replit AI agent deletes a production database, July 2025](replit-ai-agent-deletes-production-database-july-2025.md). Both were covered together by Ars Technica and Mashable.

## Where in the flow it broke

1. **Ambiguous request.** Rename plus move into a folder that did not exist yet.
2. **Write with no read-back.** `mkdir` ran and the agent said "created" without listing the parent folder.
3. **Actions built on a false state.** Moves targeted a path it never confirmed, then were reported as done.
4. **Blind spot treated as fact.** Its view stopped at the project folder, yet it told the user where the files "should be."
5. **Recovery made it worse.** Reverts and searches failed, and each failure raised the alarm level.
6. **Final claim beyond evidence.** "Irreversible" with no way to know; the user later found the files.

## What to measure

Proposed metrics; none come from Google or Gupta. Status: Not yet run. Thresholds are for the team to set.

| Metric | How to compute from logs |
|---|---|
| Unverified write claims | Agent turns saying a file or folder was created, moved, or deleted with no read of that path after the command, divided by all such claims |
| Steps after an unconfirmed write | Commands run that depend on a path not confirmed to exist |
| Loss claims beyond visibility | Turns saying data is "lost" or "gone" when the agent's tools cannot read the location in question |
| Out-of-root writes | File-changing commands whose resolved target is outside the project root |

## What a team can change

Proposed rules, each a pass/fail check on a transcript or test run. Status: Not yet run.

1. **Read after every write.** Pass: each create, move, or delete is followed by a listing of the target before the agent says it worked.
2. **Stop on a mismatch.** Pass: if the read-back disagrees with the plan, the agent stops and reports what it sees, with no further file-changing command.
3. **Resolve paths before acting.** Pass: the agent shows the full resolved destination, and a target outside the project root is blocked or needs explicit approval.
4. **Say "cannot see," not "lost."** Pass: when a search is blocked by the sandbox, the reply says where it could not look and suggests a full-drive search the user can run.
5. **Plain, calm failure reports.** Pass: a failure reply states what happened, what is known about the files, and one next step, with no self-blaming lines.
6. **Don't over-correct.** Approval prompts on every read train users to click yes. Require approval only for moves, deletes, and writes outside the project.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://github.com/google-gemini/gemini-cli/issues/4586 | GitHub issue by anuraag2601, with 18 comments | 2025-07-21 | Yes, 2026-10-23, raw JSON via GitHub API; quotes checked |
| https://github.com/user-attachments/files/21372906/gemini.cli.screw.up.txt | Terminal transcript attached to the issue | 2025-07-21 (issue date) | Yes, 2026-10-23, raw text; quotes checked |
| https://web.archive.org/web/20250724223911/https://anuraag2601.github.io/gemini_cli_disaster.html | Anuraag Gupta's blog, archived copy | Archived 2025-07-24 | Yes, 2026-10-23, raw HTML; quotes checked. Live page returned HTTP 404 |
| https://arstechnica.com/information-technology/2025/07/ai-coding-assistants-chase-phantoms-destroy-real-user-data/ | Ars Technica (Benj Edwards) | 2025-07-24 | Yes, via archive.org copy from 2026-08-19, raw HTML; live page showed a CAPTCHA |
| https://mashable.com/article/google-gemini-deletes-users-code | Mashable (Cecily Mauran) | 2025-07-25, updated 2025-07-28 | Yes, 2026-10-23, raw HTML; quotes checked |
| https://incidentdatabase.ai/cite/1178/ | AI Incident Database, Incident 1178 | 2025-07-21 (incident date) | Yes, 2026-10-23, raw HTML |
| https://github.com/google-gemini/gemini-cli/issues/3015 | GitHub issue named as a duplicate | 2025-07-02 | Title and first lines only, via GitHub API |

Not opened: Slashdot story bodies beyond a link check, WinBuzzer, Vibe Graveyard, dev.ua, and a Medium post by another user linked in the issue. Search summaries said Google made no formal statement; we use Mashable's quoted statement instead. Nothing from search summaries is used above.

## Corrections

If you know where the folder resolved, or of a Gemini CLI fix tied to this issue, tell us and we will fix this page.
