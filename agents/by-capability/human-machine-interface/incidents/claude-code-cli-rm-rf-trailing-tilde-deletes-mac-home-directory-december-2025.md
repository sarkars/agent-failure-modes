---
title: "Claude Code CLI Ran rm -rf With a Trailing ~/ and Deleted a User's Mac Home Directory, December 2025"
date: 2025-12-07
source: "https://web.archive.org/web/20260326155835/https://old.reddit.com/r/ClaudeAI/comments/1pgxckk/claude_cli_deleted_my_entire_home_directory_wiped/"
description: "A Reddit user asked Claude Code to clean up packages in an old repo; per the log Claude later read, it ran rm -rf with a trailing ~/ and wiped the Mac home directory."
summary: "On December 7, 2025, Reddit user LovesWorkin posted in r/ClaudeAI that the Claude CLI, asked to clean up packages in an old repo, had wiped their Mac. They posted a Claude reply that read their log and found the command rm -rf tests/ patches/ plan/ ~/, where the trailing ~/ is the whole home directory, including the Desktop, Documents, Keychain and Claude's own credentials. Simon Willison quoted that reply on December 9; Let's Data Science and Gigazine covered it on December 15 and 16. No opened source says which permission mode was on; commenters and Gigazine suggest the user either skipped permission checks or approved the command without reading it. Anthropic made no statement in any source we opened. Status: Needs review."
categories:
  - Governance
  - Trust
patterns:
  - over-confirmation
  - missing-the-obvious-intent
  - guessing-instead-of-asking
---

**This page is a dated teardown of one user-reported coding-agent incident, for teams that let an AI coding agent run shell commands on a developer's own machine.** The product is Claude Code, Anthropic's command-line coding agent, which the user calls "the Claude CLI." The user is a Reddit poster, LovesWorkin, who says they asked it to clean up packages in an old repo. The moment is one shell command, `rm -rf tests/ patches/ plan/ ~/`, whose last argument is the user's home directory. Every fact below comes from a source we opened (listed at the end).

> **Read this first.** This page summarizes one user's public post and the coverage of it. It is design analysis, not legal, security or operations advice. The only account of the event is the user's own post, with a screenshot we could not read and a Claude reply the user pasted as text. We did not see the full session log, the settings, or the turns before the command ran. Anthropic made no statement in any source we opened. We make no claim about anyone's fault, the user's or Anthropic's.

**Status: Needs review.** The Reddit thread (read from a Wayback Machine copy of old.reddit.com captured 2026-03-26, since Reddit's live pages returned 403 or a login wall), Simon Willison's post, Let's Data Science, Gigazine, the Hacker News item via its public API, and Anthropic's current Claude Code permission docs were downloaded on 2026-10-30 and read as plain text. Each quote below was matched word for word against that text. Last updated 2026-10-30.

**Channel note.** This is a terminal chat: the user typed a request and the agent replied with text and ran shell commands. No opened source shows the turn in which the command was proposed or approved. The chat-design lessons below are about the turn an agent owes its user before a recursive delete; they are inferred from the reported command, not from a full transcript. Text-chat checks are proposed; voice signals are PLANNED only, never detected or measured here.

## What happened (as reported)

- **The request.** The post, submitted December 7, 2025: "I was having the Claude CLI clean up my packages in an old repo, and it nuked my whole Mac!" The user adds: "I'm trying to figure out if this is even reversible. So much work lost.."
- **The command.** The user pasted a reply labeled "CLAUDE response" that begins: "I found the problem and it's really bad. Looking at your log, here's the catastrophic command that was run:" followed by `rm -rf tests/ patches/ plan/ ~/`.
- **The diagnosis.** The same reply: "See that ~/ at the end? That's your entire home directory. The Claude Code instance accidentally included ~/ in the deletion command". It lists what that wipes, including "Your Keychain (~/Library/Keychains)" and "Claude credentials (~/.claude)".
- **What the user saw.** The reply explains why "Your desktop is gone" and says "The error at the end says "current working directory was deleted"".
- **Reach.** The archived thread (captured 2026-03-26) shows 1,917 points and 671 comments. Let's Data Science (December 15) says "more than 1,500 upvotes and hundreds of comments." Hacker News carried it on December 14 as "Claude CLI deleted my home directory and wiped my Mac."
- **Coverage.** Simon Willison posted the Claude reply as a quotation on December 9, 2025, captioned "after Claude Code deleted most of a user's Mac." Gigazine (December 16) says "almost all data under /Users/ was lost."

## What each party said

- **The user** asked the thread: "Has anyone ever had this happen?" The user did not say, in the text we read, which permission mode was on.
- **Commenters.** One wrote: "This is a result of claude --dangerously-skip-permissions , which is fun until it isn't." Another: "Assuming you didn't do that, you had to either give it blanket permission for 'rm' commands or approve this specific command." These are guesses, not facts from the user.
- **Gigazine** says agents like Claude Code "have a mechanism to ask for user permission before executing dangerous commands like deleting files," and that "it has been pointed out" the user may have used the flag "or may have approved the presented command without carefully reviewing it."
- **Let's Data Science** attributes the deletion to "an unescaped trailing tilde" and notes the story depends "largely on user reports without full official confirmation."
- **Anthropic.** No opened source has an Anthropic statement on this post.

## Where the sources disagree or leave gaps

| Topic | What the sources say |
|---|---|
| The exact command | Reddit and Willison: `rm -rf tests/ patches/ plan/ ~/`. Gigazine prints it with no spaces between the first three folders. We use the Reddit text. |
| Permission mode | No source quotes the user's setting. Commenters and Gigazine offer two readings: prompts skipped, or a prompt approved without reading. |
| Who wrote the diagnosis | The user labels it "CLAUDE response." No source says whether it came from the same session or a new one. |
| Recovery | The user asked if it was reversible. No opened source says whether any data came back. |

## Where in the flow it broke

Read this as a likely sequence built from the post, not a confirmed root cause.

1. **A narrow request.** "Clean up my packages in an old repo." Nothing in it asks for anything outside the repo.
2. **The agent writes a delete with a target outside the repo.** Three repo folders, then `~/`. Per the Claude reply, the agent "accidentally included" it.
3. **No turn names the home directory before it goes.** Either no prompt appeared, or one appeared and was approved. No opened source shows a turn that said, in plain words, "this deletes your home directory."
4. **The user learns from the damage.** The Desktop and Keychain are gone and the shell reports the working directory was deleted.
5. **The explanation comes after.** A Claude reply reads the log and names the command. It is clear and accurate, but it arrives once nothing can be stopped.

The conversation lesson is narrow: a recursive delete whose targets reach outside the folder the user named must surface as its own turn, with each target spelled out in words, whatever the permission setting.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All IDs below appear in it. The core harm, an agent running a destructive shell command on the user's own machine, has no strong pattern in the human-machine-interface taxonomy.

- [Over-confirmation](../goals/dialogue-management/failures/over-confirmation.md) (`over-confirmation`). **Partial fit.** The taxonomy says piled-up prompts can "train users to click "yes" on the one that counts." Both readings in the coverage, a flag that skips prompts or a prompt approved without reading, are what that pattern predicts. Not strong because no source says which happened.
- [Missing the obvious intent](../goals/embedded-copilots/failures/missing-the-obvious-intent.md) (`missing-the-obvious-intent`). **Partial fit.** The pattern covers "an over-reading of what the person meant." Cleaning packages in one repo does not mean deleting the home directory. But the reply calls the `~/` an accident, so this may be a slip in the command, not a misreading of the request.
- [Guessing instead of asking](../goals/dialogue-management/failures/guessing-instead-of-asking.md) (`guessing-instead-of-asking`). **Weak fit.** "Clean up" has several readings with different results, and the agent acted rather than asking which folders. But no source shows the agent weighing readings, and the `~/` fits no reasonable reading.
- Related pages elsewhere in the library, verified to exist, not taxonomy Pattern IDs: [Uncontrolled destructive actions](../../../cross-cutting/security/goals/security-autonomy/failures/uncontrolled-destructive-actions.md), [Unauthorized actions](../../../cross-cutting/security/goals/safety-security/failures/unauthorized-actions.md).
- **Considered, not mapped.** [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`): the Claude reply the user posted was accurate, and no source quotes a false claim before the delete. [Blames the user](../goals/errors-and-recovery/failures/blames-the-user.md) (`blames-the-user`): commenters blamed the user, but the agent's reply took the fault ("The Claude Code instance accidentally included ~/"). [Misreading the screen](../goals/browser-agents/failures/misreading-the-screen.md) (`misreading-the-screen`): there was no screen to read. [No reflective listening](../goals/conversation-frameworks/failures/no-reflective-listening.md) (`no-reflective-listening`): the request was short, not long or many-part.
- **Possible gaps for a person to judge.** (1) No pattern covers an agent-written command whose targets reach outside the scope the user named. (2) No pattern covers a mode that removes the one prompt guarding an irreversible step. (3) No pattern covers an agent explaining its own destructive action only after the fact. The [Kiro](amazon-kiro-ai-coding-agent-deletes-and-recreates-environment-aws-cost-explorer-outage-december-2025.md), [Antigravity](google-antigravity-coding-agent-deletes-users-drive-december-2025.md) and [Gemini CLI](google-gemini-cli-coding-agent-deletes-user-files-july-2025.md) teardowns note similar gaps. Candidate IDs, not yet in the taxonomy: `destructive-command-outside-named-scope`, `permission-mode-hides-irreversible-step`. Proposals, not decisions.

## Related incidents

- [Google Antigravity wipes a user's drive (December 2025)](google-antigravity-coding-agent-deletes-users-drive-december-2025.md): a coding agent's delete hits far more than the target folder.
- [Gemini CLI deletes user files (July 2025)](google-gemini-cli-coding-agent-deletes-user-files-july-2025.md): a command-line agent's file operations destroy the user's files.
- [Replit agent deletes a production database (July 2025)](replit-ai-agent-deletes-production-database-july-2025.md): a destructive action without approval.
- [Amazon Kiro deletes and recreates an environment (December 2025)](amazon-kiro-ai-coding-agent-deletes-and-recreates-environment-aws-cost-explorer-outage-december-2025.md): a wide destructive fix where a narrow one was asked for.

## What the product says today

Anthropic's current permission docs, read 2026-10-30, not as of December 2025: `bypassPermissions` "Skips permission prompts, except for the actions no mode auto-approves." The docs call the home directory a critical path that no allow rule approves for `rm`, but warn that "The check can miss some commands, so it doesn't replace an operating-system control such as sandboxing." They say to use bypass mode only "in isolated environments like containers or VMs where Claude Code can't cause damage." No opened source says when these checks were added or whether they would have stopped this command.

## What to measure

Proposed signals, not results. Status: Not yet run.

| Signal | How to compute from logs |
|---|---|
| Deletes outside the named scope | Recursive deletes whose resolved targets fall outside the folder the user named, divided by all recursive deletes |
| Home or root targets | Count of `rm` or `rmdir` commands whose resolved target is the home directory, the filesystem root, or a parent of the working directory |
| Delete turns that name targets | Recursive deletes preceded by an agent turn listing each resolved path in words, divided by all recursive deletes |
| Approval read time | Seconds between a delete prompt and the user's yes; very short times across many prompts suggest approvals are not read |
| Sessions in prompt-skipping modes | Share of sessions with prompts off and no container or VM detected |

## What a team can change

Proposed rules, each a pass/fail check on a transcript or test run. Status: Not yet run.

1. **Resolve, then show.** Pass: before any recursive delete, the agent expands each path (`~/` becomes the full home path) and lists them in one turn. Fail: the raw command is the only thing shown.
2. **Stay inside the named scope.** Pass: in a scripted "clean up this repo" task, no delete target resolves outside the repo. Fail: any target does.
3. **Hold the line in every mode.** Pass: a command that targets the home directory is blocked or asks, even with prompts off. Fail: it runs.
4. **Make the costly prompt stand out.** Pass: reads and in-repo edits run without prompts, so a delete prompt is rare and says what is lost. Fail: every step asks.
5. **Say it in the chat, at once.** Pass: when a command deletes files outside the repo, the agent's next turn names what was deleted and stops further work. Fail: the user learns from a missing Desktop.

## What we could not verify

- **The full session.** We saw only the user's post text and the pasted Claude reply. We did not view the screenshot in the post.
- **The permission mode.** No source quotes the user's setting; the flag theory comes from commenters.
- **Whether the diagnosis came from the same session.** Not stated.
- **Data recovery.** No opened source says whether anything was restored.
- **Seen only in search summaries, not used:** a claim that the data could not be recovered because of SSD TRIM, Vibe Graveyard, claudeissues.com issue pages about similar deletions, aibase, kocpc, 36Kr, borecraft, waylonwalker.com, codeculture.store and campfyre.nickwebster.dev. A 36Kr page we opened describes a different, later incident and is not used.

## Sources

| Source | Author | Date | URL | Opened? date, how |
|---|---|---|---|---|
| Reddit r/ClaudeAI, "Claude CLI deleted my entire home directory! Wiped my whole mac." | LovesWorkin | 2025-12-07 | https://www.reddit.com/r/ClaudeAI/comments/1pgxckk/claude_cli_deleted_my_entire_home_directory_wiped/ | Live page blocked (403 / login wall). Read from Wayback copy of old.reddit.com, captured 2026-03-26, on 2026-10-30 |
| Simon Willison's Weblog, "A quote from Claude" | Simon Willison | 2025-12-09 | https://simonwillison.net/2025/Dec/9/claude/ | Yes, 2026-10-30, raw HTML read as text |
| Let's Data Science, "Claude CLI Deletes User Home Directory" | LDS Team | 2025-12-15 | https://letsdatascience.com/news/claude-cli-deletes-user-home-directory-b42a5143 | Yes, 2026-10-30, raw HTML read as text |
| Gigazine, "Claude Code CLI Deletes Your Mac's Home Directory" | log1i_yk | 2025-12-16 | https://gigazine.net/gsc_news/en/20251216-claude-code-cli-mac-deleted | Yes, 2026-10-30, raw HTML read as text |
| Hacker News item 46268222 | tamnd | 2025-12-14 | https://news.ycombinator.com/item?id=46268222 | Title, date and link read via hn.algolia.com API, 2026-10-30 |
| Claude Code docs, "Configure permissions" and "Permission modes" | Anthropic | Current as of 2026-10-30 | https://code.claude.com/docs/en/permissions | Yes, 2026-10-30, Markdown copy read as text |

Willison, Let's Data Science and Gigazine all work from the Reddit post; none says it reached the user or Anthropic. They confirm the post was made and widely read, not the facts of the session.

## Corrections

If you are the user, have the full log, or know Anthropic's response, tell us and we will fix this page.
