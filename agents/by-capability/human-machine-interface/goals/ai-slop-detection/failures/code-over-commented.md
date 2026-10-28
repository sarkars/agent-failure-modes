# AI Code Has Too Many Comments: Over-Commented Code and Tutorial-Style Comments

<!-- SEO
title: AI Code Has Too Many Comments: How to Stop Over-Commenting
description: AI coding tools comment every line, number tutorial steps and leave chat text in comments. Set a why-not-what rule and check each diff before merge.
search phrases:
- ai code too many comments
- how to stop copilot adding comments
- claude code adds too many comments
- cursor comments every line
- chatgpt code redundant comments
- how to tell if code is ai generated comments
- step 1 import libraries comment ai
-->

**Frequency**: Common

## Issue: AI coding tools comment every line, number tutorial steps and leave chat text in comments; set a why-not-what rule and check each diff before merge.

> **One line:** The assistant writes "# Increment the counter" above `count += 1`, "# Step 1: Import libraries" above the imports, and "# Here's the updated function" at the top, and reviewers read the whole file as unreviewed AI code.

| | |
|---|---|
| **Channel** | Written for **generated code**: files and diffs from Copilot, Cursor, Claude Code, ChatGPT and similar tools. Docstrings and API docs are out of scope except where they leak chat text. |
| **Stakes** | Low to medium. Noise slows review and hides the few comments that matter; chat text in a shipped file tells customers and auditors nobody read it. |
| **Who is affected** | Code reviewers, maintainers who inherit the file, and developers whose work is judged by the diff |
| **Frequency** | Common. A 2026 study names redundant comments as a readability issue pattern in LLM code, and a Claude Code issue reports the habit across languages and models (section 4). I found no rate across tools. |
| **Pattern ID** | code-over-commented |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Comment-clean diff rate: share of AI-assisted pull requests whose added lines hold no comment that restates the next line, numbers tutorial steps, or speaks to the chat. Target 95% before merge (proposed starting point; no catalog row yet). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. The issue reporter saw it on current Opus and Sonnet models with a mandatory CLAUDE.md rule in place, so a rule plus a diff check is what makes it hold. (Our judgment, not tested.) |
| **Also searched as** | AI comments every line · remove obvious comments from AI code · Copilot verbose comments · tutorial comments in production code · signs code was written by ChatGPT · comments say why not what |

## 1. In plain words
You ask an AI tool for a small function. It comes back with a comment on almost every line that says what the next line plainly does, numbered "Step 1, Step 2" comments like a coding tutorial, and sometimes a line that talks to you ("Here's the updated function with the fix you asked for"). The code may be fine, but the reviewer stops trusting it. The fix: tell the tool to match the repo's comment density and write comments only for why, then check every diff for restating, step and chat comments before merge.

## 2. What it looks like
A property manager in Denver asks Cursor to add a late fee to overdue rent invoices.

**Without the fix**
```python
# Here's the updated function with the late fee logic you asked for!
# Step 1: Import the necessary libraries
from datetime import date

# Step 2: Define the function
def apply_late_fee(invoice, today: date):
    # Check if the invoice is overdue
    if today > invoice.due_date:
        # Add the late fee to the invoice total
        invoice.total += 25
    # Return the invoice
    return invoice
```
```
Reviewer: Six comments, none tells me anything. Was this read before you opened the PR?
```
**With the fix**
```python
from datetime import date, timedelta

GRACE_PERIOD = timedelta(days=5)  # Lease section 4.2; change it only with legal sign-off.
LATE_FEE_USD = 25

def apply_late_fee(invoice, today: date):
    if today > invoice.due_date + GRACE_PERIOD and not invoice.late_fee_applied:
        invoice.total += LATE_FEE_USD
        # The nightly job re-runs on failure; without this flag a tenant could be charged twice.
        invoice.late_fee_applied = True
    return invoice
```
```
Developer: Add a $25 late fee to overdue rent invoices. Follow the comment rules in .cursor/rules.
Assistant: Done in billing/fees.py. Two comments, both say why: the grace period source and the
           double-charge guard. Comment check: 0 restating, 0 step, 0 chat lines in the diff.
           One question: does the 5-day grace period come from your lease, or should I take it out?
```
The fixed version deletes every comment that repeats the code, keeps two that say why, carries no chat text, and the assistant asks instead of guessing about the grace period.

## 3. Why it happens
Our reading, with the issue report and study in section 4 as support.
- **Training data is full of teaching code.** Tutorials, answers and notebooks explain each line to a learner, so "comment each step" looks like good code to the model.
- **The model writes for the chat, not the repo.** It explains its work to the person asking, and that explanation lands in the file as comments, including references to the chat itself.
- **The rule is an instruction, not a check.** Claude Code's own docs say CLAUDE.md is read as context, not enforced configuration, and the issue below reports a mandatory rule not holding. Nothing scans the diff.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A study of 2,735 scenarios from World of Code and LeetCode names "redundant comments" among the readability issue patterns in LLM-generated code, and finds the role of prompt design "remains bounded." | [Ye, Ran, Xu and Zhou, *Characterizing Readability Issue Patterns and the Role of Prompt Design in LLM-Generated Code*, arXiv, May 2026](https://arxiv.org/abs/2605.13280). Abstract opened and read. | Preprint. I read the abstract only, not the full paper, so I have no per-pattern rate. A search summary gave a different scenario count; the 2,735 figure is from the abstract. |
| A user reports Claude Code over-comments by default; the comments are "mostly redundant, restating what the adjacent code already makes obvious" or refer to the chat; a "mandatory rule in `CLAUDE.md` does not reliably suppress it." Other commenters report the same. | [anthropics/claude-code issue #65961, opened June 7, 2026](https://github.com/anthropics/claude-code/issues/65961). Opened and read. | User reports on one tool. Open, flagged by a bot as a possible duplicate, when I read it. |
| Google's code review guide: comments should "explain why some code exists, and should not be explaining what some code is doing"; if code is unclear, "the code should be made simpler." Regular expressions and complex algorithms are exceptions. | [Google Engineering Practices, *What to look for in a code review*](https://google.github.io/eng-practices/review/reviewer/looking-for.html). Opened and read. | A style rule from one company, not a measurement. It treats docstrings as separate from comments. |
| Google's Python style guide says of block and inline comments: "never describe the code." | [Google Python Style Guide, section 3.8.5](https://google.github.io/styleguide/pyguide.html). Opened and read. | Style guide, Python only. |
| An exploratory study of repositories from 2021 to 2025 found comments detected as likely LLM-generated have "a relatively low proportion of grammatically correct sentences." | [Ji, Wang, Zhou, Chen and Yang, *An Exploratory Study on LLM-Generated Code and Comments in Code Repositories*, arXiv, July 2026](https://arxiv.org/abs/2607.01867). Abstract opened and read. | Uses a detector as a proxy for AI authorship. The abstract gives no comment rates. A summary said these comments cluster in explanatory and meta categories; I read that only in a summary, so it is not used here. |
| Claude Code docs (vendor): CLAUDE.md files are loaded into every session, and Claude "treats them as context, not enforced configuration"; to block an action, use a hook. | [Claude Code docs, *How Claude remembers your project*](https://code.claude.com/docs/en/memory). Opened and read. | Vendor docs. Supports the "rule plus check" design, not a rate. |
| GitHub Copilot (vendor) reads repository-wide rules from `.github/copilot-instructions.md`, which "apply to all requests made in the context of a repository." | [GitHub Docs, *Adding repository custom instructions*](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions). Opened and read. | Vendor docs. Says where the rule goes, not whether it is followed. |

I found no study that measures how often reviewers reject or flag a pull request because of AI-style comments. The "Step 1" and "Here's the updated function" examples are our illustrations of the habit, not quotes from a dataset.

## 5. The fix
**The principle:** A comment says why the code is this way, never what the next line does, and a check of every diff proves it before merge.

**Do this**
1. **No comment that restates the next line.** Check: a comment whose words mostly repeat the identifiers on the line below it ("# Return the invoice" over `return invoice`) fails.
2. **No tutorial step comments.** No "Step 1:", "First, we", "Now we", "Finally" comments in source files. Notebooks and teaching material the user asked for are allow-listed.
3. **No chat text in files.** No comment that addresses the user or the session: "Here's", "as you asked", "updated version", "I added", "fixed the bug you mentioned", "Phase 2 of the plan".
4. **Match the repo's comment density.** Before writing, the assistant reads two or three nearby files; the added lines' comment-to-code ratio stays near that file's ratio.
5. **Keep the why.** Business rules, workarounds, magic numbers, odd orderings and non-obvious regular expressions get one short comment with the reason or source.
6. **Report in the reply, not the file.** What changed and why goes in the chat reply or the PR description, never in a code comment.
7. **Enforce with a check.** A pre-merge script or reviewer checklist runs rules 1-3 on added lines and posts the result on the PR.

**Reference design: project rule plus pre-merge check**
```
Comment rules (put in CLAUDE.md, AGENTS.md, .cursor/rules or .github/copilot-instructions.md):
- Match the comment density of the file you are editing. If it has few comments, add few.
- Comments say why: a business rule, a source, a workaround, a trap. Never what the next line does.
- No "Step 1" or "First, we" comments. This is production code, not a tutorial.
- Never write to me in a comment. Explain your change in the chat reply or the PR description.
- Do not delete existing comments unless they are now wrong; say so in the reply if you do.
```
| Check | Where | Fails when |
|---|---|---|
| Chat-text scan on added comment lines (regex for "here's", "as you asked", "updated", "I added", "you mentioned") | Pre-commit and CI | Any match outside allow-listed files |
| Step-comment scan (`Step \d+:`, "First, we", "Now we") | Pre-commit and CI | Any match outside notebooks and docs the user asked for |
| Restatement check: share of comment words found on the next code line | CI script on added lines | Overlap above a threshold you set from your own labeled sample |
| Comment density of added lines vs. the file's existing lines | CI script | Added ratio far above the file's ratio (set the gap from your baseline) |
| Human review question: "Does every new comment say something the code cannot?" | PR template checkbox | Reviewer unchecks it |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md)). Adapted: the "conversation" is the developer prompting the assistant, or the checker reporting on the PR.
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The assistant's reply and the checker report open with what changed and the count of flagged comments, with file:line. |
| Offer choices: 2-4 options plus "Something else", free text open | For each flagged comment: "Delete it", "Rewrite it as a why", "Keep it (explains a regex or algorithm)", "Something else". |
| Ask one clarifying question | A number or rule has no known source (the 5-day grace period): ask once where it comes from instead of inventing a reason in a comment. |
| Hand off to a person | A comment records a legal, safety or compliance reason: the code owner confirms the wording. |

**Don't over-correct.** Do not strip every comment. Comments that explain a regex, an algorithm, a workaround or a business rule stay, and the Google guide names regexes and complex algorithms as exceptions. Do not delete existing human comments when editing a file; one Claude Code report (#49743, read only through a search summary) describes that opposite failure. Do not apply these rules to docstrings, public API docs, or a tutorial the user asked for, where explaining each step is the point.

**Hand-off rule.** When a flagged comment carries a legal, security or compliance reason, or the assistant cannot tell why a rule exists, it leaves the code unchanged, asks the code owner, and notes the open question in the PR description.

**Framework used:** none yet.

## 6. How to test it (short version)
No test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Ask for a 10-line function in a repo with sparse comments | No comment repeats the next line | 1, 4 |
| 2 | Ask "write a script to load a CSV and plot it" in a `src/` file | No "Step 1:" or "First, we" comments | 2 |
| 3 | Ask for a fix, then a second fix in the same session | No comment mentions the chat, the fix request or "updated" | 3 |
| 4 | Ask for a function with a magic number from a lease or contract | One comment gives the source or the assistant asks for it | 5 |
| 5 | Ask for a change, then read the reply | The explanation is in the reply or PR description, not the file | 6 |
| 6 | Open a PR with a planted "# Here's the updated code" line | The pre-merge check fails and names the line | 7 |
| 7 | Edit a file with existing why-comments | Existing comments are kept | Don't over-correct |
| 8 | Ask for a regex that validates US ZIP+4 codes | A short comment explaining the regex is kept | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; none comes from a source.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Comment-clean diff rate** (primary) | 95% (proposed) | Pre-merge check on AI-assisted PRs; PRs with no flagged comment / PRs checked | Below 90% |
| Chat-text comments merged | 0 (proposed) | Chat-text scan on merged commits | Any |
| Comment density gap | Track; set from baseline | Added-line comment ratio minus the file's prior ratio, per PR | Rising for 2 weeks |
| Reviewer flags for AI-style comments | Track; set from baseline | PR review comments matching "remove comment", "obvious comment", "AI comment", sampled monthly | Rising month over month |
| Useful comments removed (counter-metric) | 0 (proposed) | Sampled review of 20 diffs a month for deleted why-comments, regex or algorithm notes | Any in a sample |

### Detection signals (proposed, not yet calibrated)
Signals in a diff that suggest this failure. Proposed until checked against human-labeled reviews.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Comment whose words mostly match the identifiers on the next line | Added lines, comment plus next code line | A team rule that every public method gets a one-line summary |
| "Step N:" or "First, we / Now we" comments in a source file | Added comment lines | A tutorial, sample or notebook the user asked for |
| Comment addressing the user or session ("here's", "as you asked", "updated version") | Added comment lines | A changelog file or a test that quotes such text as data |
| Comment-to-code ratio of added lines far above the file's ratio | Diff stats per file | A new module where the team wants heavy docs |

**Starter rule:** comments in AI-written code say why, never what the next line does, and no step or chat comment passes the pre-merge check.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: code-over-commented
runs: pre_send
reads: [diff.added_lines, diff.comment_lines, diff.file_type, file.prior_comment_ratio, allowlist.files, pr.description]
trigger: the AI tool writes a file or opens a PR, and the check finds a restating, step-numbered or chat-text comment outside an allow-listed file
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]
choices: ["Delete it", "Rewrite it as a why", "Keep it (explains a regex or algorithm)", "Something else"]
on_miss: rewrite
metric: comment-clean diff rate
counter_metric: useful comments removed
status: proposed
```

## 8. Related patterns
- [Chatbot filler phrases](../../response-structure/failures/filler-and-padding.md): the closest existing page. It covers restated questions and recaps in **chat replies**; this page covers the same habit written into **code files** as comments, and the diff check that catches it.
- [Placeholder data left in](./ui-placeholder-data-left-in.md): leftover filler in built pages; chat text left in a comment is the code version of the same "nobody read it" tell.
- [Emoji as icons](./ui-emoji-as-icons.md): emoji in code comments and commit messages, another tell in the same diffs.
- [Invented packages and APIs](../../coding-agents/failures/invented-packages-and-apis.md): a riskier code failure; over-commented code can still call a function that does not exist.
- Family overview: [AI slop detection](../README.md).

## 9. Common questions
### Why does AI add so many comments to code?
Our reading: much of the code models learn from is teaching code that explains every line, and the model explains its work to you as it writes. Both end up in the file. A study of LLM code names redundant comments as a readability issue pattern (section 4).

### How do I stop Copilot, Cursor or Claude Code from commenting every line?
Put the comment rules from section 5 in `.github/copilot-instructions.md`, `.cursor/rules`, CLAUDE.md or AGENTS.md. Users report the rule alone does not always hold, so add a pre-merge check on added comment lines.

### Can you tell code is AI-generated from its comments?
Comments that restate each line, "Step 1" headers and lines like "Here's the updated function" are common tells. None proves AI wrote the code, and a junior developer can write the same way; treat them as a sign the diff was not reviewed.

### Should code have no comments at all?
No. Google's review guide says comments should explain why code exists, and that regexes and complex algorithms often need comments on what they do. Delete the restating ones and keep the reasons.

### Should I delete AI comments before committing?
Delete the ones that restate code, number steps or talk to you. Keep any that give a reason, a source or a warning, and move the change explanation to the PR description.
