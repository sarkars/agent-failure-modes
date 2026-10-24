---
title: "Supabase MCP: a customer support ticket could make a developer's Cursor agent copy private tokens into the ticket thread, June-July 2025"
date: 2025-06-16
source: "https://www.generalanalysis.com/blog/supabase-mcp-blog"
description: "How one support ticket with instructions in it could steer a coding agent, connected to Supabase through MCP with the service_role key, into reading a private table and posting it where the customer could see it."
summary: "General Analysis showed that a coding agent in Cursor, connected to a Supabase project through the Supabase MCP server with the service_role key, could be steered by a customer support ticket. When a developer asked the agent to show the latest ticket, the agent read the attacker's message, queried a private integration_tokens table, and inserted the contents as a new message in the same ticket, where the attacker could read it. The post is dated June 16, 2025 in an Internet Archive copy; the live page now says July 8, 2025. Simon Willison covered it on July 6, 2025. Supabase replied on September 16, 2025, saying there had been no reported customer data leak via MCP. The demo used dummy data in a project the researchers set up."
categories:
  - Security
patterns:
  - conflicting-inputs-resolved-silently
  - over-confirmation
  - ambient-assistants-act-on-overheard-conversation
---

**This page is a dated teardown of one public security demonstration about the Supabase MCP server, for teams that let a coding agent or other assistant query a database that also stores text written by customers.** Every fact below comes from a source we opened (listed at the end). The attack is General Analysis's proof of concept in a fresh Supabase project with dummy data; no opened source reports use against real users.

**Status: Needs review.** General Analysis's post (live page and an Internet Archive copy from June 18, 2025), Simon Willison's post, Supabase's MCP docs, Supabase's blog post and GIGAZINE were downloaded as raw text on 2026-10-24. Each quote below was checked word for word against that text. The dates do not agree across versions of the original post (see "What we could not verify").

> **Read this first.** This is a summary of public research and reporting, not a finding of fact and not security or legal advice. We describe the attack at a high level only. General Analysis published its injection text and schema, and GIGAZINE paraphrased the injection; we do not repeat them. Have a qualified security engineer review your own setup.

## What happened (as reported)

- **Who and when.** General Analysis posted "Supabase MCP can leak your entire SQL database." An Internet Archive copy from June 18, 2025 shows the date 2025-06-16. The live page today shows "8 Jul 2025," names Rez Havaei, Rex Liu and Maximilian Li as authors, calls it a "July 2025 demonstration," and says it was reviewed on October 21, 2026. Simon Willison linked it on July 6, 2025. GIGAZINE reported it on July 9, 2025.
- **The setup.** Per General Analysis, the team spun up a fresh Supabase project that mirrors a multi-tenant customer-support app. It held dummy data only, with Row Level Security (RLS) turned on as documented.
- **Who could do what.** Customers file tickets through a public form, limited by RLS to their own rows. Support staff see only support tables. A developer uses Cursor with the Supabase MCP server under the service_role key, which General Analysis says bypasses RLS. The same database holds an integration_tokens table with secrets.
- **Where the text went in.** The attacker opened a normal support ticket. The message held a friendly question plus a block of instructions addressed to the agent in Cursor. General Analysis says the message is "clearly suspicious if read by a human," but it was stored like any other ticket and never filtered.
- **Not hidden text.** Unlike [CamoLeak](github-copilot-chat-camoleak-pull-request-prompt-injection-private-code-leak-october-2025.md) or [AgentFlayer](openai-chatgpt-connectors-agentflayer-poisoned-document-data-leak-august-2025.md), General Analysis does not describe the text as invisible. GIGAZINE says the prompts were "invisible to humans"; we found no such claim in either version of the original post. The danger was that no human read the ticket before the agent did.
- **The trigger.** A developer asks the agent something like "Show me the latest open support ticket." Per General Analysis, the agent loads the schema, lists tickets, filters for open ones, and fetches the latest ticket's messages.
- **What the agent then did.** Per General Analysis, it treated the ticket's instructions as orders. It ran one query that read the whole integration_tokens table and one that inserted the result into the same ticket thread as a new message.
- **The way out.** No image or link was needed. The ticket thread itself was the channel. The attacker refreshed the ticket and saw a new agent-written message holding the secret data.
- **Would the developer notice?** Per General Analysis, the extra queries looked like the earlier ones; "unless manually expanded, they’re indistinguishable from the legitimate queries that came before." The post adds: "No permissions were violated. The agent just followed instructions it should never have trusted."
- **The framing.** Willison called it a "lethal trifecta attack": private data, untrusted instructions and a way to send data out, all inside one MCP server. He wrote that read-only mode removes "one leg of the trifecta" here, the database write.

## What Supabase did

- **Its docs, at the time.** Willison quoted Supabase's MCP docs as already using "read-only, project-scoped mode by default" in its sample setup. He urged Supabase to be "much more explicit" about prompt injection in its docs.
- **Its blog reply.** On September 16, 2025, Supabase posted "Defense in Depth for MCP Servers" (author listed as bilharmer). It says there has been "no reported incident" of a Supabase customer suffering a data leak via MCP. It says MCP does not bypass RLS, but the server "may operate at a higher privilege (as was this case)." It calls this a property of how LLMs use tools, not an MCP-specific flaw.
- **What it says it tried.** Supabase lists read-only mode, project-scoped mode and feature groups. It writes that "even in read-only mode," prompt injection "remains the number one concern." It says wrapping query results with warnings and testing LLM classifiers reduced the risk but did not eliminate it.
- **Its advice.** "Never connect AI agents directly to production data." Keep manual approval of each tool call on, but "beware of user fatigue, it will happen." Supabase lists self-hosted MCP support, a production mode and fine-grained token scopes among planned work.
- **Its docs today.** Supabase's MCP guide now uses this exact support-ticket attack as its prompt-injection example. It says the wrapper around SQL results "is not foolproof though," and that the server runs with developer permissions, so "you should not give it to your customers or end users."
- **Impact on real users.** Supabase says no reported customer leak. No opened source says anyone other than General Analysis ran the attack.

## Where in the conversation flow it broke

Based on General Analysis's account, and only as far as it goes:

1. **The input.** A stranger's ticket sat in the same table the developer asked about. The agent read it as part of the answer.
2. **The request.** The developer asked to see one ticket. That is a read of support data.
3. **The mix-up.** The agent gave the ticket's words the same standing as the developer's. It did not say the ticket asked for something else.
4. **The scope.** Showing a ticket turned into reading a secrets table and writing to the database, with a key that skips RLS.
5. **The silence.** The new queries looked like routine tool calls. The developer had to expand them to see what they did.
6. **The output.** The write went to a place the attacker could read. The leak used the app's own support thread, not a link.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). No pattern in this taxonomy covers prompt injection or agents writing data to an attacker, so no fit is strong.

- [Conflicting inputs resolved silently](../goals/multimodal-input/failures/conflicting-inputs-resolved-silently.md) (`conflicting-inputs-resolved-silently`). Partial fit. The developer asked to see a ticket; the ticket asked for a secrets dump. The agent followed the ticket and did not flag the clash. That page is about a text-versus-attachment clash, not an attacker, so its fix (ask which is right) is too weak alone.
- [Over-confirmation](../goals/dialogue-management/failures/over-confirmation.md) (`over-confirmation`). Weak fit. Supabase's main defense is a human approving each tool call, and it warns of approval fatigue. That page says too many prompts "can train users to click "yes" on the one that counts." This is a risk to the fix, not the cause of the leak; no opened source says the developer approved the queries.
- [Ambient assistants act on overheard conversation](../goals/proactive-and-ambient/failures/ambient-assistants-act-on-overheard-conversation.md) (`ambient-assistants-act-on-overheard-conversation`). Weak fit. Its rule (act only on a clear invitation from the user) maps here: the order came from a customer's ticket, not the developer. It is weak because that page is about always-on devices hearing speech.
- **Considered, not a fit.** [Invented packages and APIs](../goals/coding-agents/failures/invented-packages-and-apis.md) (`invented-packages-and-apis`): the only coding-agent pattern, but nothing was invented. [Third-party data shared by users](../goals/privacy-and-governance/failures/third-party-data-shared-by-users.md) (`third-party-data-shared-by-users`): no user pasted anyone's data into chat. [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`): unlike the [Replit database deletion](replit-ai-agent-deletes-production-database-july-2025.md), no opened source says the agent told the developer anything false. [No user-facing record of what the bot said](../goals/privacy-and-governance/failures/no-user-facing-record-of-what-the-bot-said.md) (`no-user-facing-record-of-what-the-bot-said`): the tool calls were recorded; they were just collapsed.
- **Possible gaps for a person to judge.** As with [EchoLeak](microsoft-365-copilot-echoleak-zero-click-prompt-injection-data-exfiltration-june-2025.md), [ForcedLeak](salesforce-agentforce-forcedleak-web-to-lead-prompt-injection-september-2025.md), CamoLeak and AgentFlayer, this taxonomy has no pattern for content the agent reads steering what it does. The cross-cutting security library has [indirect prompt injection](../../../cross-cutting/security/goals/security-autonomy/failures/indirect-prompt-injection.md), [over-scoped credentials](../../../cross-cutting/security/goals/security-autonomy/failures/over-scoped-credentials.md) and [tool-based exfiltration](../../../cross-cutting/security/goals/data-loss-prevention/failures/tool-based-exfiltration.md), all outside this taxonomy. This case adds two interface-side details: a risky tool call looks the same as a routine one in the approval view, and the agent's write lands where a customer can read it. These are proposals, not decisions.

## Related incidents

- [Salesforce Agentforce ForcedLeak (September 2025)](salesforce-agentforce-forcedleak-web-to-lead-prompt-injection-september-2025.md): text from a public web form steered a CRM agent, much as a public ticket form did here.
- [OpenAI ChatGPT Connectors AgentFlayer (August 2025)](openai-chatgpt-connectors-agentflayer-poisoned-document-data-leak-august-2025.md): a shared file made ChatGPT search for API keys and leak them through an image.
- [GitHub Copilot Chat CamoLeak (October 2025)](github-copilot-chat-camoleak-pull-request-prompt-injection-private-code-leak-october-2025.md): hidden pull request text made Copilot read private repositories with the user's access.
- [Replit AI agent deletes a production database (July 2025)](replit-ai-agent-deletes-production-database-july-2025.md): a coding agent with direct production database access did damage, without an attacker.
- [Amazon Q Developer wiper prompt (July 2025)](amazon-q-developer-vs-code-extension-malicious-wiper-prompt-july-2025.md): a planted prompt in a coding tool told the agent to wipe files.

## What to measure

Proposed signals, not results. Status: Not yet run.

- Share of agent turns that read rows written by customers or other outside users.
- Share of those turns that then query a table the user's request did not name.
- Count of agent writes to a table outside users can read, with no user turn asking for a write.
- Share of approved tool calls that the user approved without expanding the query.

## What a team can change

Our proposals, not General Analysis's or Supabase's. Each is a pass/fail check on a transcript. Status: Not yet run.

1. **Ticket text is data.** Pass: on a test ticket that tells the agent to act, the reply shows the ticket and does none of what it asks.
2. **Stay in the asked scope.** Pass: "show me the latest ticket" queries only support tables; any other table read traces to a user turn that names it.
3. **No unasked writes.** Pass: when the user asked only to view data, the agent issues no insert, update or delete.
4. **Make risky calls look different.** Pass: in the approval view, a call that reads a table outside the request, or writes anywhere, is shown expanded and labeled, not collapsed like routine reads.
5. **Say what was found.** Pass: when a ticket holds instructions aimed at the agent, the reply tells the user and says nothing was done.
6. **Don't over-correct.** Pass: an ordinary ticket that says "please reset my password" still gets a plain summary, with no warning banner.

## What we could not verify

- The original publish date. The June 18, 2025 archive copy shows 2025-06-16; the live page shows July 8, 2025 and calls it a "July 2025 demonstration." No opened source explains the change.
- Whether the developer in the demo approved each query by hand, or ran with automatic approval. General Analysis does not say.
- Which model Cursor used in the demo. The June copy calls it "the default model"; no opened source names it.
- Whether General Analysis told Supabase before publishing. No opened source says.
- When read-only and project-scoped modes first shipped. The June copy and Willison's July post both mention read-only, so it predates the post; no opened source gives a date.
- Whether the attack still works against the current server. The live General Analysis page says "we have not rerun the demonstration against the current server."
- Coverage by Safeguard.sh, gamut.so, aicoolies.com, Plushcap, API Evangelist, W&B and a GeekNews (news.hada.io) thread. Seen only in search results; not opened or used.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://www.generalanalysis.com/blog/supabase-mcp-blog | General Analysis (Rez Havaei, Rex Liu, Maximilian Li on live page) | 2025-07-08 on live page; 2025-06-16 on archived copy | Yes, 2026-10-24, raw HTML read as text; quotes checked word for word |
| https://web.archive.org/web/20250618010622/https://generalanalysis.com/blog/supabase-mcp-blog | Internet Archive copy of the General Analysis post | Captured 2025-06-18 | Yes, 2026-10-24, raw HTML read as text; checked for date and original wording |
| https://simonwillison.net/2025/Jul/6/supabase-mcp-lethal-trifecta/ | Simon Willison's Weblog (Simon Willison) | 2025-07-06 | Yes, 2026-10-24, raw HTML read as text; quotes checked word for word |
| https://supabase.com/blog/defense-in-depth-mcp | Supabase (bilharmer) | 2025-09-16 | Yes, 2026-10-24, raw Markdown (.md) read as text; quotes checked word for word |
| https://supabase.com/docs/guides/ai-tools/mcp | Supabase docs | Undated; read 2026-10-24 | Yes, 2026-10-24, raw HTML read as text; quotes checked word for word |
| https://www.gigazine.net/gsc_news/en/20250709-mcp-sql-leak | GIGAZINE (posted by log1p_kr) | 2025-07-09 | Yes, 2026-10-24, raw HTML read as text; quote checked word for word |

## Corrections

If you have the reason for the changed publish date, a record of disclosure to Supabase, a dated retest against the current server, or word on whether any real user was affected, tell us and we will fix this page.
