---
title: "OpenAI ChatGPT plugins: one link could install a plugin without the user's approval, and plugin sign-in flaws risked account takeover, March 2024"
date: 2024-03-13
source: "https://salt.security/blog/security-flaws-within-chatgpt-extensions-allowed-access-to-accounts-on-third-party-websites-and-sensitive-data"
description: "How Salt Labs found one link could install a ChatGPT plugin with no confirmation, and plugin sign-in flaws could hand over users' GitHub and other accounts."
summary: "On March 13, 2024, Salt Security's Salt Labs published research by Aviad Carmel on three flaw types in the ChatGPT plugin system. In ChatGPT itself, a crafted link could install an attacker's plugin on a signed-in victim's account without a confirmation, so later chat messages could reach that plugin. In PluginLab, a plugin framework, a flaw allowed account takeover with no click, shown on the AskTheCode plugin for GitHub. In several plugins, including Charts by Kesem AI, unchecked sign-in redirects could leak a user's code through a link. Salt says it told OpenAI on July 10, 2023, and the plugin makers in September 2023, that all were fixed, and that there was no evidence of use in the wild. No opened source has an OpenAI statement."
categories:
  - Security
  - Privacy
patterns:
  - manipulated-consent-ui
  - over-confirmation
  - forces-a-fresh-login
---

**This page is a dated teardown of public security research on ChatGPT plugins and their sign-in flow, for teams that let users connect a chat assistant to an outside account (GitHub, Google Drive, a CRM) through a link, a sign-in page or an "approve" step.** The product was ChatGPT plugins, which in 2023 let ChatGPT send data to third-party services and act on a user's accounts there. The user was a signed-in ChatGPT user. The moment was a click on a link, or an approval on a plugin's sign-in page, that connected an account with no clear "yes, connect this" step the user could see and refuse. Every fact below comes from a source we opened (listed at the end). The attacks were Salt Labs' research demonstrations; no opened source reports use against real users.

**Status: Needs review.** Salt Security's blog post and press release, Dark Reading, SC Media, Infosecurity Magazine, BetaNews, TechRadar and Security Affairs were downloaded as raw HTML on 2026-10-28 and read as plain text. Each quote below was checked word for word against that text. BankInfoSecurity refused our download (HTTP 403) and is not used. We found no OpenAI statement, advisory or fix date (see "What we could not verify").

> **Read this first.** This is a summary of public research and reporting, not a finding of fact, and not legal or security advice. It does not say whether any company broke any law or contract. We describe the attacks at a high level only. We reproduce no links, codes, IDs, request formats or steps from the research. Have a qualified security engineer review your own sign-in and connection flows.

**Channel note.** Text chat. Users installed plugins from inside ChatGPT, signed in on the plugin's site, and then chatted in text while ChatGPT passed messages to the plugin. This phase of the knowledge base is chat-first: the text-chat signals and checks below are proposed; voice is planned and not covered here.

## What happened (as reported)

- **The research.** Salt Labs' blog post, by security researcher Aviad Carmel, is dated March 13, 2024. Salt says the research took place in July 2023, when plugins were ChatGPT's main way to reach outside services. It says that using a plugin gives ChatGPT permission to send sensitive data to a third-party site, and, for some plugins, access to private accounts on Google Drive, GitHub and more. It notes that a plugin is built by outside developers while "the user interface is still ChatGPT," which gives users a more consistent feeling.
- **Flaw 1: install by link, no confirmation (in ChatGPT).** Per Salt, installing a plugin that needs sign-in sent the user to the plugin's site to approve, and the plugin then sent the user back to ChatGPT with a code. When ChatGPT got the code, it installed the plugin automatically. Salt writes: "ChatGPT doesn’t validate that the user indeed started the plugin installation." So an attacker could send a victim a link on ChatGPT's own domain, and "By clicking on this link, the victim installs a malicious plugin, without a confirmation." Per Salt, the victim's new messages could then reach the attacker's plugin, and the attacker could see private chat data that "may include credentials, passwords or other sensitive data." Salt says ChatGPT did use a check value meant to tie the return trip to the user who started it, but the value was not random and could be guessed.
- **Flaw 2: account takeover with no click (in PluginLab).** Per Salt, PluginLab is a framework developers use to build ChatGPT plugins. Salt shows the flaw on AskTheCode, a PluginLab plugin that answers questions about a user's GitHub repositories. Per Salt, a PluginLab sign-in step did not check who was asking, and a user's ID could be worked out from an email address. With that, an attacker could get a victim's code and read the victim's private repositories through the attacker's own ChatGPT. Salt writes: "This is a zero-click attack." It says the flaw "affected dozens of other plugins" built on PluginLab.
- **Flaw 3: unchecked sign-in redirects (in several plugins).** Per Salt, several plugins did not check where their sign-in page sent the user's code afterward. Salt uses Charts by Kesem AI as its example. If a victim clicked a link the attacker had altered, the plugin sent the victim's code to the attacker, who could take over the victim's plugin account. Salt says some other plugins checked the domain but not the path, which was also open to abuse.
- **What Salt says about GPTs.** Salt says GPTs, launched in November 2023, are a similar concept, and that OpenAI's security work on them is "a major improvement over Plugins." It says OpenAI now warns the user each time data is sent from ChatGPT to a third party. It also says users "need to remain vigilant" and teases a follow-up post.
- **Disclosure timeline, per Salt.** Found the ChatGPT flaw June 25, 2023. Told ChatGPT July 10, 2023. Found and told PluginLab.AI and KesemAI in September 2023. Sent all three the blog after all had fixed their flaws, February 27, 2024. Published March 13, 2024.
- **Press coverage.** Dark Reading (Nathan Eddy, March 13, 2024), SC Media (Laura French, March 13, 2024), Infosecurity Magazine (Alessandro Mascellino, March 13, 2024), BetaNews (Ian Barker, March 13, 2024), TechRadar (Lewis Maddison, March 14, 2024) and Security Affairs (Pierluigi Paganini, March 14, 2024) all reported the three flaw types. SC Media wrote that, if the victim was signed in, clicking the link "would automatically install the attacker’s plugin to their account without any confirmation."

## What OpenAI and the plugin makers said

- **OpenAI.** No opened source quotes OpenAI or links an OpenAI advisory. Salt's press release says Salt followed coordinated disclosure with OpenAI and third-party vendors, "and all issues were remediated quickly, with no evidence that these flaws had been exploited in the wild." That is Salt's claim, not OpenAI's.
- **PluginLab.** Salt quotes PluginLab's reply, which says that "no user data has been compromised as a result of the identified vulnerability" and that the issue was "promptly addressed and resolved." Salt says PluginLab also sent a notice to its users saying no users had been impacted.
- **Kesem AI.** Salt thanks Kesem.ai for acting to resolve the flaw. No opened source quotes Kesem AI.
- **Salt's asks.** Salt calls on OpenAI to put more weight on security in its developer documentation, including a line on checking redirect addresses. Per Dark Reading, Salt's Yaniv Balmas said security leaders "should review what plug-ins and GPTs their company is using and what third-party accounts are exposed through those plug-ins and GPTs."

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| How many flaws were zero-click | Dark Reading's opening says the three flaws open the door to "zero-click access." Salt says only the PluginLab flaw was zero-click; the ChatGPT install flaw and the redirect flaw needed the victim to click a link. |
| How many plugins | Salt says the PluginLab flaw affected "dozens" of plugins and the redirect flaw "several." No opened source gives a count. |
| Plugins versus GPTs | Salt's press release subhead calls plugin functionality "now known as GPTs" and says GPTs pose similar risks. The blog says GPTs are a separate feature that fixed most of the plugin issues. |
| What users should do | Dark Reading says users "should update their apps as soon as possible." Salt's opened texts describe fixes made by OpenAI and the vendors and ask users for nothing. |
| A quoted line | Salt's press release and BetaNews quote Balmas on attackers who "execute account takeovers." SC Media prints the same quote as "executive account takeovers." |
| Fix dates | Salt says all vendors had fixed their flaws by February 27, 2024. No source gives the date of any single fix. |

## Where in the conversation flow it broke

Based on the reporting, and only as far as it goes:

1. **The link.** A signed-in ChatGPT user got a link on ChatGPT's own domain. Nothing about the address marked it as unsafe.
2. **The connect step.** Per Salt and SC Media, one click installed a plugin with no screen that named the plugin and asked the user to approve it. The step that should have been the user's "yes" was skipped.
3. **The chat after.** The user kept chatting. Per Salt, messages could now reach a plugin the user never chose, and no opened source describes any notice in the chat that a new plugin was on.
4. **The sign-in page.** For the redirect flaw, the user signed in on a real plugin page, and the page sent the result to the wrong place. The user could not see where it went.
5. **No user at all.** For the PluginLab flaw, the victim did nothing. No consent step could have helped; the fix had to be on the server.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). No pattern in this taxonomy covers a chat product that connects an outside account or tool to a user's chat without the user's own confirmation, so no fit is core.

- [Manipulated consent UI](../goals/visual/failures/manipulated-consent-ui.md) (`manipulated-consent-ui`). **Partial fit.** That page is about a consent prompt where Accept is easy and Reject is buried, so consent is not a real choice. Here the ChatGPT flaw removed the choice entirely: a link stood in for the approval. The page's lesson, that the user must see and be able to refuse the choice, carries over.
- [Over-confirmation](../goals/dialogue-management/failures/over-confirmation.md) (`over-confirmation`). **Weak fit.** That page warns that too many "are you sure?" prompts bury the few that guard a costly step. This case is the costly step with no prompt at all. It supports the page's point that the confirmation budget belongs on steps like connecting an account.
- [Forces a fresh login](../goals/embedded-copilots/failures/forces-a-fresh-login.md) (`forces-a-fresh-login`). **Weak fit.** That page is about asking a signed-in user to sign in again for low-risk requests, and it says skipping the check on risky actions is the opposite and worse failure. Installing a plugin that can read chats is that risky action; here the user's existing sign-in was enough to carry it out.
- **Considered, not a fit.** [Accepts consent pop-ups for the user](../goals/browser-agents/failures/accepts-consent-pop-ups-for-the-user.md) (`accepts-consent-pop-ups-for-the-user`): no agent clicked anything for the user; the platform skipped the step. [Third-party data shared by users](../goals/privacy-and-governance/failures/third-party-data-shared-by-users.md) (`third-party-data-shared-by-users`): the risk was to the user's own chats and accounts, not to someone they pasted in. [Sensitive data collected in chat](../goals/channel-selection/failures/sensitive-data-collected-in-chat.md) (`sensitive-data-collected-in-chat`): Salt says chats may hold passwords, but the bot did not ask for them; the harm was where messages went. `undisclosed-bot-identity`: users knew they were using ChatGPT.
- **Possible gap for a person to judge.** The cross-cutting security library has [OAuth token theft](../../../cross-cutting/security/goals/runtime-security/failures/oauth-token-theft.md), [human-in-the-loop bypass](../../../cross-cutting/security/goals/safety-security/failures/human-loop-bypass.md) and [malicious tool injection](../../../cross-cutting/security/goals/runtime-security/failures/malicious-tool-injection.md), all outside this taxonomy. This case adds one interface-side pattern the taxonomy lacks: a tool or account is connected to the chat without a confirmation the user sees, and the chat never says it is on. A possible ID would be "tool connected without the user's confirmation." This is a proposal, not a decision.

## How it differs from close cases

- [ChatGPT Connectors AgentFlayer (August 2025)](openai-chatgpt-connectors-agentflayer-poisoned-document-data-leak-august-2025.md): the user had connected Google Drive on purpose, and a hidden instruction in a shared document steered ChatGPT into leaking keys. Here no planted instruction was needed; the flaw was in the connect step itself, which let an attacker attach a plugin the user never chose.
- [Custom GPTs leak instructions and files (November 2023)](openai-custom-gpts-leak-instructions-and-uploaded-files-november-2023.md): users pulled a builder's setup out of a GPT by asking. Here the user was the victim, and the leak ran from the user's chats and accounts to an attacker.
- [GitHub MCP server (May 2025)](github-mcp-server-prompt-injection-private-repo-leak-invariant-labs-may-2025.md): a planted issue steered an agent with GitHub access. Here the PluginLab flaw reached private repositories with no model in the loop and no click.

## What to measure

Proposed signals, not results. Status: Not yet run. Text-chat signals are proposed; voice signals are planned only.

- Share of plugin, tool or connector installs that finish without a logged user approval event in the same session.
- Share of sign-in return trips that arrive with no matching start event for that user and session.
- Count of installs per 1,000 sessions that start from an outside link rather than from the product's own install screen.
- Share of sessions where a new tool is turned on and the chat shows no message naming that tool before the next user turn.
- Count of sign-in requests whose return address does not match the exact registered address, per 1,000 requests.

## What a team can change

Our proposals, not OpenAI's, Salt's or the plugin makers'. Each is a pass/fail check on a transcript, a test run or a config review. Status: Not yet run. Thresholds and what counts as a risky connection are for the team to set.

1. **No connect without a yes.** Pass: opening an install or connect link that the user did not start shows a screen naming the tool and what it can read, and nothing installs until the user taps approve.
2. **Tie the return to the start.** Pass: a test return trip with no matching start in the same session is refused, and the refusal is logged.
3. **Exact return addresses.** Pass: a test sign-in request with any return address other than the exact registered one is refused.
4. **Say it in the chat.** Pass: after a tool is connected, the next assistant turn names the tool and what it will receive, before any message is sent to it.
5. **Easy to see, easy to remove.** Pass: a user who types "what is connected?" gets a list of every connected tool and a way to remove each one in the same chat.
6. **Ask where it counts.** Pass: a review of confirmation prompts finds one on every new connection and on no routine read-only step.
7. **Don't over-correct.** Pass: a user who connects a tool from the product's own install screen sees one approval screen, not a second sign-in for the same request.

## What we could not verify

- Any OpenAI statement, advisory, changelog entry or fix date. Salt says the flaws were fixed; no opened source quotes OpenAI.
- How many plugins were affected by the PluginLab and redirect flaws. Salt says "dozens" and "several" without a list.
- Whether any real user was harmed. Salt says there was no evidence of use in the wild, and PluginLab told Salt no user data was compromised; no independent source checks either claim.
- Salt's promised follow-up post on GPTs. Not opened.
- PluginLab's notice to its users. Described by Salt; not opened.
- Seen only in search summaries, not used: BankInfoSecurity (download refused, HTTP 403), GovInfoSecurity, SDxCentral, Hackread, TechTarget, OODA Loop, Calcalist, SecurityInfoWatch, VKTR and CIO Influence.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://salt.security/blog/security-flaws-within-chatgpt-extensions-allowed-access-to-accounts-on-third-party-websites-and-sensitive-data | Salt Security, Salt Labs (Aviad Carmel) | 2024-03-13 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://salt.security/press-releases/salt-security-uncovers-security-flaws-within-chatgpt-extensions-that-allowed-access-to-third-party-websites-and-sensitive-data---issues-have-been-remediated | Salt Security (press release) | 2024-03-13 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.darkreading.com/vulnerabilities-threats/critical-chatgpt-plugin-vulnerabilities-expose-sensitive-data | Dark Reading (Nathan Eddy) | 2024-03-13 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.scworld.com/news/chatgpt-0-click-plugin-exploit-risked-leak-of-private-github-repos | SC Media (Laura French) | 2024-03-13 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.infosecurity-magazine.com/news/security-risks-chatgpt-plugins/ | Infosecurity Magazine (Alessandro Mascellino) | 2024-03-13 | Yes, 2026-10-28, raw HTML read as text |
| https://betanews.com/2024/03/13/flaws-in-chatgpt-extensions-allowed-access-to-sensitive-data/ | BetaNews (Ian Barker) | 2024-03-13 | Yes, 2026-10-28, raw HTML read as text; quote checked word for word |
| https://www.techradar.com/pro/security/chatgpt-plugin-flaws-could-have-allowed-hackers-to-take-over-other-accounts | TechRadar (Lewis Maddison) | 2024-03-14 | Yes, 2026-10-28, raw HTML read as text |
| https://securityaffairs.com/?p=160447 | Security Affairs (Pierluigi Paganini) | 2024-03-14 | Yes, 2026-10-28, raw HTML read as text |

## Corrections

If you have OpenAI's own statement or fix date, a list of affected plugins, or a report from a user whose account was reached through these flaws, tell us and we will fix this page.
