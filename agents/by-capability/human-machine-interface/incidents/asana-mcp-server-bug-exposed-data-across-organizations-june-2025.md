---
title: "Asana MCP server: a bug could show one organization's Asana data to other organizations' AI assistant users, May-June 2025"
date: 2025-06-04
source: "https://status.asana.com/incidents/5b9hhtgs3mxs"
description: "How a bug in Asana's MCP server, its connector for AI assistants, could show one organization's data to users in other organizations in mid-2025."
summary: "Asana launched an experimental MCP server on May 1, 2025, so AI apps could read and act on Asana data. On June 4 it found a bug that could expose information from one customer's Asana domain to MCP users at other organizations, within those users' own access scope. Asana's status page shows MCP disabled from June 5 through June 17, all connections reset, and customers told to reconnect by hand. An Asana spokesperson told BleepingComputer roughly 1,000 customers were affected. Asana said it was not a hack. No opened source explains the coding error."
categories:
  - Security
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - outage-updates-generic-or-late
  - no-user-facing-record-of-what-the-bot-said
---

**This page is a dated teardown of public reporting and Asana's own status page on a bug in Asana's MCP server, for teams that let AI assistants read customer data through a shared tool connection that serves many organizations.** The product was Asana's Model Context Protocol (MCP) server, an opt-in connector that let outside AI apps query and change a user's Asana data in plain language. The users were people at Asana customer organizations who connected an AI assistant to Asana. The moment was June 4, 2025, when Asana found that the server could return one organization's information to users at other organizations. Every fact below comes from a source we opened (listed at the end). No opened source has Asana's code, logs or full incident report.

**Status: Needs review.** Asana's status-page incident "MCP Maintenance" (read through the status page's public JSON feed), BleepingComputer, The Register, UpGuard and CSO Online were downloaded as raw HTML, JSON or Markdown on 2026-10-28 and read as plain text. Each quote below was checked word for word against that text. Asana's emails to customers were not opened; where we cite them, we cite them as quoted by The Register or UpGuard. Dark Reading, SecurityWeek, TechRadar, Nudge Security, Security Boulevard and others were not opened.

> **Read this first.** This is a summary of public reporting and a company status page, not a finding of fact, and not legal, privacy or security advice. It does not say whether Asana or any customer broke any law or contract, or whether any notice duty applied. It states no rule of law. The customer count is a figure an Asana spokesperson gave one outlet; no opened source checked it. We name no affected customer. We give no steps to reproduce the bug, and no opened source describes it in that detail.

**Channel note.** Assistant tool connection, used through text chat. Per CSO Online, an employee could ask an AI assistant to "Find all my incomplete tasks due this week," and the assistant would fetch the answer from Asana through the MCP server. The bug sat in that connection, not in a chat window Asana ran. This phase of the knowledge base is chat-first: the text-chat signals and checks below are proposed; voice is planned and not covered here.

## What happened (as reported)

- **The launch.** Asana rolled out its MCP server on May 1, 2025 (The Register, Jessica Lyons, June 18, 2025; BleepingComputer, Bill Toulas, June 18, 2025). The Register quotes Asana's enable screen calling it "an experimental beta tool" and warning: "You may encounter bugs, errors, or unexpected results." CSO Online (Howard Solomon, June 18, 2025) says it lets customers access Asana data from compatible AI apps and generate reports and summaries.
- **The bug.** Asana found it on June 4 (UpGuard; The Register; BleepingComputer). Per Asana's customer notice as quoted by The Register, the bug could have "exposed certain information from your Asana domain to other Asana MCP users." BleepingComputer says the exposure was limited, "the data type being limited to each user's access scope," and that other companies' MCP users might have seen another domain's data, "including chatbot-generated queries."
- **What it was not.** UpGuard (Greg Pollock) quotes Asana: "This was not a result of a hack or malicious activity on our systems." BleepingComputer calls it "a logic flaw in the MCP system." UpGuard says "There is no indication that attackers exploited the bug," or that other users actually viewed the data.
- **How long.** BleepingComputer: "these cross-organization data leaks occurred for over a month," counting from the May 1 launch to the June 4 discovery. UpGuard says the bug "appears to have been part of this initial release." Neither cites a log or Asana statement for the start date.
- **The shutdown.** Asana's status page posted on June 5, 2025 at 17:51 UTC: "Asana's MCP server is undergoing maintenance." The next update came on June 16 at 20:45 UTC: "We identified a bug affecting our Model Context Protocol (MCP) server." The server was marked operational on June 17 at 16:51 UTC.
- **The notice to customers.** UpGuard says Asana notified potentially affected customers on June 16, meaning anyone with a user who had used the MCP server. BleepingComputer says Asana sent notices with links to contact forms to each affected organization.
- **How many.** BleepingComputer: "a spokesperson has told us the incident impacts roughly 1,000 customers." The Register says Asana's spokesperson "did not answer our questions about the bug, including how many customers were affected."

## What the company said

- **On its status page, June 17, 2025 (postmortem).** Asana said it disabled MCP from June 5 through June 17 "for maintenance to address a vulnerability." It said affected organizations had been contacted directly, the bug was fixed, and "we reset all connections to the MCP server," so customers must reconnect by hand.
- **To customers, as quoted by UpGuard.** Asana asked organizations to review what they got through the MCP server in recent weeks and "immediately delete any data that does not belong to your organization." UpGuard says customers could ask for logs and metadata on their MCP users to check for cross-account exposure, and that a post-mortem would be available on request.
- **To The Register.** A spokesperson said "we're working on a full incident report as we speak," with the main focus so far on helping affected customers.
- **What we did not find.** No opened source has Asana's explanation of the coding error, its full incident report, or what changed in the server so the same kind of bug is caught before release.

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| When the server went offline | UpGuard quotes Asana saying it took the server down after the June 4 discovery. Asana's status page and The Register say June 5 through June 17. The first status post is timed June 5, 17:51 UTC. |
| Whether Asana spoke publicly | BleepingComputer says Asana "has not issued a public statement about the incident." Asana's status page did post updates and a postmortem, but they say "vulnerability" and "bug," not that data could cross organizations. |
| How many customers | BleepingComputer: roughly 1,000, per a spokesperson. The Register: the spokesperson did not answer. No Asana document we opened gives a count. |
| How the bug worked | The Register says Asana's incident report "doesn't provide details about the coding error." BleepingComputer calls it a logic flaw. No opened source says more. |
| UpGuard's date | The page's metadata says published June 16, 2025; the visible page says "July 2, 2026," likely an update date. The Register cites UpGuard on June 18, 2025. |

## Where in the conversation flow it broke

Based on the reporting, and only as far as it goes:

1. **The ask.** A user at one company asked an AI assistant about their Asana work, such as tasks due this week (CSO Online's example).
2. **The tool call.** The assistant asked Asana's MCP server for the data. This is where the bug sat. Per the reporting, the server could return information from another organization's Asana domain.
3. **The answer.** The assistant would have shown whatever came back, in the same voice as a correct answer. No opened source says the user saw any cue that some items came from a different company.
4. **The status page.** For 11 days the public status said only "undergoing maintenance." The word "bug" appeared on June 16, and "vulnerability" on June 17.
5. **The cleanup.** Asana asked customers to find and delete data that was not theirs, and offered logs on request. That depends on the customer being able to tell which items in past AI answers were foreign.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). No opened source shows a full conversation with foreign data in it, so no fit is core.

- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Partial fit.** An answer built from another organization's tasks would read like a normal answer. BleepingComputer's advice to review AI summaries for data "pulled from another organization" assumes users can spot it; no source says the answer marked where items came from.
- [Outage updates generic or late](../goals/travel-and-utility-agents/failures/outage-updates-generic-or-late.md) (`outage-updates-generic-or-late`). **Partial fit.** The status page said "undergoing maintenance" from June 5 to June 16, with no cause or next-update time. That page's family is travel and utilities, so this is a fit by analogy, not by domain.
- [No user-facing record of what the bot said](../goals/privacy-and-governance/failures/no-user-facing-record-of-what-the-bot-said.md) (`no-user-facing-record-of-what-the-bot-said`). **Weak fit.** Cleanup depended on logs of what the MCP server returned, which customers had to request. That entry is about bot promises, not tool output, so the fit is loose.
- **Considered, not a fit.** [Third-party data shared by users](../goals/privacy-and-governance/failures/third-party-data-shared-by-users.md) (`third-party-data-shared-by-users`): there a user pastes someone else's data; here the system served it. `conflicting-inputs-resolved-silently` and `ambient-assistants-act-on-overheard-conversation`: used for the prompt-injection MCP cases; no opened source reports injected instructions here. `over-confirmation`: no source reports a confirmation step. `sensitive-data-collected-in-chat`: the data was not collected from the user in chat. `humans-can-t-see-what-the-bot-said-or`: no handoff to a person is reported.
- **Possible gap for a person to judge.** No taxonomy entry covers an assistant's answer that includes data from another customer or account because the tool connection returned it. This is a proposal, not a decision.

## How it differs from close cases

The key difference is the cause. Here, per every opened source, a bug in Asana's own server crossed the line between organizations, with no attacker. In the prompt-injection cases, the server worked as designed and an attacker's text steered the agent.

- [GitHub MCP server (May 2025)](github-mcp-server-prompt-injection-private-repo-leak-invariant-labs-may-2025.md): a planted public issue told the user's agent to copy private repo data into a public pull request. That needed an attacker and a broad token. Asana's exposure needed neither, per the sources.
- [Supabase MCP (June 2025)](supabase-mcp-support-ticket-prompt-injection-sql-data-leak-june-2025.md): instructions hidden in a support ticket steered a coding agent with an admin key. The fix there is about what the agent trusts. Here it is about what the server returns to whom.
- [ChatGPT chat titles bug (March 2023)](openai-chatgpt-bug-exposes-other-users-chat-titles-march-2023.md): the closest match. A bug, not an attack, showed some users other users' data, and the service was taken offline. There it was a chat history list; here it was data an AI assistant fetched through a tool connection, across companies, not just across users.

## What to measure

Proposed signals, not results. Status: Not yet run. Text-chat signals are proposed; voice signals are planned only. Each is computable from tool-call logs and status-page history.

- Share of MCP tool responses that contain any object whose owning organization differs from the organization of the token that made the call. The target is zero.
- Count of distinct organizations represented in a single tool response. The target is one.
- Share of tool calls logged with both the caller's organization and each returned object's organization, so the first signal can be computed at all.
- Time from a security-related takedown to the first status update that names the cause in plain words.
- Time from discovery to notice for affected customers, logged per incident.

## What a team can change

Our proposals, not Asana's. Each is a pass/fail check on a transcript, a test run or a log query. Status: Not yet run. Windows and thresholds are for the team to set.

1. **Check the organization on every response.** Pass: a log query over a set window finds no tool response that returned an object from an organization other than the caller's.
2. **Test with two organizations before release.** Pass: a pre-release test with two seeded test organizations, A and B, runs every tool as a user of A, and no response includes any object seeded in B.
3. **Keep those tests running.** Pass: the two-organization test runs on every deploy of the connector, and a failing run blocks the deploy.
4. **Log what the assistant was given.** Pass: for any tool call in the window, a support person can pull which objects were returned and to which organization, without a code change.
5. **Say what kind of incident it is.** Pass: when a connector is taken down for a data-exposure bug, the first status update within a set time names a security issue, the affected feature and the next update time, not only "maintenance."
6. **Don't over-correct.** Pass: after the fix, a test user in organization A who asks "show my tasks due this week" still gets their own tasks, with no extra refusal or re-login beyond the one-time reconnect.

## What we could not verify

- How the bug worked. No opened source describes the coding error, and Asana's full incident report was not found.
- The count of affected customers. Only BleepingComputer's spokesperson figure; not checked by any opened source.
- Whether anyone actually saw another organization's data. UpGuard says there is no indication of it; no log data is public.
- When the exposure began. "Over a month" is BleepingComputer's reading from the May 1 launch; not confirmed by Asana in any opened source.
- Asana's customer emails and the form it sent. Seen only as quoted by The Register and UpGuard.
- A reported cost to fix of about $7.5 million. Seen only in a search summary of an index page; not opened, not used.
- An exposure window of June 5 to June 17 attributed to Pomerium, and details in Nudge Security, Security Boulevard, TechRadar, Yahoo/AOL, SANS NewsBites, SOCRadar, PointGuard AI and Adversa. Seen only in search summaries; not opened, not used.
- Asana's developer page for the MCP server was downloaded, but its text did not load as plain text, so it is not used. A November 18, 2025 status entry for MCP downtime is unrelated and not used.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://status.asana.com/incidents/5b9hhtgs3mxs | Asana status page, "MCP Maintenance" | 2025-06-05 to 2025-06-17 | Yes, 2026-10-28, via the status page's public JSON feed (status.asana.com/api/v2/incidents.json); quotes checked word for word |
| https://www.bleepingcomputer.com/news/security/asana-warns-mcp-ai-feature-exposed-customer-data-to-other-orgs/ | BleepingComputer (Bill Toulas) | 2025-06-18 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.theregister.com/2025/06/18/asana_mcp_server_bug/ | The Register (Jessica Lyons) | 2025-06-18 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.upguard.com/blog/asana-discloses-data-exposure-bug-in-mcp-server | UpGuard (Greg Pollock, per the page bio and The Register) | 2025-06-16 (metadata); page shows 2026-07-02 | Yes, 2026-10-28, Markdown version read as text; quotes checked word for word |
| https://www.csoonline.com/article/4009373/asanas-mcp-ai-connector-could-have-exposed-corporate-data-csos-warned.html | CSO Online (Howard Solomon) | 2025-06-18 | Yes, 2026-10-28, raw HTML read as text; quote checked word for word |

## Corrections

If you have Asana's full incident report, a primary-source count of affected customers, or a technical account of the bug, tell us and we will fix this page.
