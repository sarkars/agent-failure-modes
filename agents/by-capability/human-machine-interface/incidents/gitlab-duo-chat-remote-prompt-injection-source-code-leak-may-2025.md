---
title: "GitLab Duo Chat remote prompt injection: hidden text in projects could make Duo leak private code through streamed HTML, May 2025"
date: 2025-05-20
source: "https://www.legitsecurity.com/blog/remote-prompt-injection-in-gitlab-duo"
description: "How hidden text in a public GitLab project could steer another user's Duo Chat into reading their private code and sending it out via a rendered image tag."
summary: "On May 20, 2025, Legit Security researcher Omer Mayraz disclosed a remote prompt injection in GitLab Duo Chat. Instructions hidden in merge requests, comments, commit messages, issues or source code were followed when another user asked Duo about that content. Duo runs with that user's permissions, so it could read their private merge requests, and because Duo rendered streamed Markdown as HTML too early, the reply could carry an image tag that sent the data to an outside server. Legit says it reported the flaw on February 12, 2025 and that GitLab fixed it in duo-ui!52, which blocks unsafe tags pointing outside gitlab.com. Dark Reading, Techzine and The Hacker News reported it on May 22-23, 2025. No opened source reports use against real users."
categories:
  - Security
patterns:
  - conflicting-inputs-resolved-silently
  - confident-wrong-answer-with-no-way-to-check
  - invented-packages-and-apis
  - ambient-assistants-act-on-overheard-conversation
---

**This page is a dated teardown of one public security finding about a coding assistant, for teams that ship an assistant that reads merge requests, issues, or code written by people outside the user's control and renders its replies as HTML.** Every fact below comes from a source we opened (listed at the end). The attack is Legit Security's proof of concept in projects it set up; no opened source reports use against real users.

**Status: Needs review.** Legit Security's post, Dark Reading, The Hacker News, Techzine, Simon Willison's post and GitLab's merge request duo-ui!52 were downloaded as raw HTML on 2026-10-28 and read as plain text. Each quote below was checked word for word against that text. TechRepublic returned HTTP 403 (not bypassed) and was not used.

> **Read this first.** This is a summary of public research and reporting, not a finding of fact and not security or legal advice. We describe the attack at a high level only. Legit and others published the injection text; we do not repeat it. Have a qualified security engineer review your own assistant.

**Channel note.** Text chat in a web app. The victim typed a question into the Duo Chat panel on GitLab's site and the answer streamed back as rendered Markdown. This phase of the knowledge base is chat-first: the text-chat signals and checks below are proposed; voice is planned and does not apply to this incident.

## What happened (as reported)

- **Who and when.** Legit Security posted "Remote Prompt Injection in GitLab Duo Leads to Source Code Theft," written by Omer Mayraz and dated May 20, 2025. Dark Reading (Nate Nelson) and Techzine (Erik van Klinken) reported it on May 22, 2025; The Hacker News (Ravie Lakshmanan) and Simon Willison on May 23, 2025.
- **The product.** Per Legit, GitLab Duo is the AI assistant built into GitLab and is powered by Anthropic's Claude. The attack ran through Duo Chat.
- **The headline claim.** Legit's summary: "A hidden comment was enough to make GitLab Duo leak private source code." It adds that the same flaw let Duo inject untrusted HTML into its replies. No opened source names a CVE or a severity score.
- **Where the text went in.** Legit planted hidden prompts in merge request descriptions and comments, commit messages, issue descriptions and comments, and source code. It writes: "Every single one of these worked." Its reason: Duo reads the whole page context to answer.
- **How it was hidden.** Per Legit, the prompts were disguised with Unicode smuggling, Base16 encoding, and KaTeX math set in white text, so people viewing the page would not see them. Duo still read them.
- **What the injection could do to answers.** Legit says it made Duo add a malicious JavaScript package to suggested code, present a malicious link as safe (leading to a fake login page), and present a malicious merge request as safe to reviewers.
- **The rendering flaw.** Duo streamed its answer and turned Markdown into HTML line by line. Legit says an HTML tag that arrived before the structure of the reply was known could be treated as active HTML. Answers did pass through the DOMPurify sanitizer, but per Legit it does not remove tags such as images, forms and links by default.
- **The data access.** Per Legit, Duo runs with the victim's permissions: "Duo can see everything the user can." Duo can also be asked about a specific merge request the user is not viewing.
- **The demo.** Legit hid instructions in the source code of a merge request in a public project. A victim asked Duo an ordinary question about a file there. Duo read a merge request from the victim's private iOS project, encoded the code changes, and put them into an image address. The victim's browser tried to load the "image" and sent the data to Legit's server.
- **Confidential issues.** Legit says the same method could pull a confidential issue the victim can read, such as a private report of an unfixed vulnerability. This is Legit's described scenario, not a demo result.

## What GitLab did

- **The timeline, per Legit.** Legit says it disclosed the issue on February 12, 2025. The Hacker News gives the same date. Dark Reading says Feb. 23 (see "Where the sources disagree").
- **The fix, per Legit.** GitLab confirmed the HTML injection, acknowledged the prompt injection as a security issue, and said both had been remediated. The patch, duo-ui!52, stops Duo from rendering unsafe tags such as images or forms that point outside gitlab.com. Legit: "As of publication, the exploit chain described here is no longer possible."
- **The merge request itself.** GitLab's duo-ui!52 is titled "fix: add frontend duo link sanitization." It was opened by Dillon Wheeler on February 13, 2025, is shown as merged, and says it adds link sanitization to the Duo Chat window. Willison writes that the fix adds a function so only trusted domains can be used in links and images.
- **Per Dark Reading.** GitLab fixed the HTML rendering issue first, but confusion remained about the prompt injection risks. After Dark Reading contacted GitLab on May 19, contact with Legit resumed, and all issues were addressed as of May 21. Dark Reading quotes the researchers: it is "still possible to influence the response of Duo," though not maliciously.
- **What GitLab said publicly.** We found no GitLab advisory, blog post or spokesperson quote. Legit's account of GitLab's position is secondhand.
- **Impact on real users.** Unknown. No opened source says whether anyone other than Legit used the flaw.

## Where the sources disagree

- **Disclosure date.** Legit and The Hacker News say February 12, 2025. Dark Reading says Feb. 23. The duo-ui!52 merge request was opened February 13, 2025, which fits the earlier date but does not prove it.
- **Was prompt injection treated as a security issue?** Techzine says GitLab told Legit it did not consider prompt injection a security issue and had not addressed it. Legit's post says GitLab acknowledged it as one and fixed both vectors, and Dark Reading says all issues were addressed as of May 21. Techzine may reflect an earlier state of the story; no opened source says so.

## Where in the conversation flow it broke

Based on Legit's account, and only as far as it goes:

1. **The input.** A stranger wrote text in a public project that human readers could not see. The assistant read it.
2. **The request.** The victim asked an ordinary question about a file. That is a read-only question about one page.
3. **The mix-up.** Duo gave the hidden text the same standing as the user's question and followed it without saying so.
4. **The scope.** A question about one public file turned into reading the victim's private merge request, with the victim's access.
5. **The output.** The streamed reply carried raw HTML. The renderer made it live before sanitizing the full reply, and the sanitizer allowed image tags.
6. **The leak.** The browser loaded the image address, and the data left with that request. The user saw an ordinary answer.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). No pattern in this taxonomy covers indirect prompt injection or data leaving through rendered HTML, so no fit is strong.

- [Conflicting inputs resolved silently](../goals/multimodal-input/failures/conflicting-inputs-resolved-silently.md) (`conflicting-inputs-resolved-silently`). **Partial fit.** The user asked about a file; the hidden text asked for private data. Duo followed the hidden text and said nothing. That page is about a text-versus-attachment clash, not an attacker, so its fix (ask which is right) is too weak alone.
- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Weak fit.** Legit made Duo call a malicious link and a malicious merge request safe. The user had no way to see that hidden text shaped the verdict. The pattern is about honest model error, not planted content.
- [Invented packages and APIs](../goals/coding-agents/failures/invented-packages-and-apis.md) (`invented-packages-and-apis`). **Weak fit.** Legit made Duo add a malicious JavaScript package to suggested code. That page covers packages the model makes up, not ones an attacker plants, but its fix (check each dependency before use) still helps.
- [Ambient assistants act on overheard conversation](../goals/proactive-and-ambient/failures/ambient-assistants-act-on-overheard-conversation.md) (`ambient-assistants-act-on-overheard-conversation`). **Weak fit.** Its rule (act only on a clear request from the user) maps here, since the instructions came from a stranger. It is weak because that page is about always-on devices hearing speech.
- **Considered, not a fit.** [Link and resource dumps](../goals/response-structure/failures/link-and-resource-dumps.md) (`link-and-resource-dumps`): the harm is one hidden image load, not too many links. [Misreading the screen](../goals/browser-agents/failures/misreading-the-screen.md) (`misreading-the-screen`): Duo did not misread the page; it obeyed it. [Ignores the page, selection, and form state](../goals/embedded-copilots/failures/ignores-the-page-selection-and-form-state.md) (`ignores-the-page-selection-and-form-state`): the opposite problem; Duo read the whole page, including what the user could not see. `third-party-data-shared-by-users`: no user pasted anyone's data into chat.
- **Possible gaps for a person to judge.** As with [CamoLeak](github-copilot-chat-camoleak-pull-request-prompt-injection-private-code-leak-october-2025.md), [EchoLeak](microsoft-365-copilot-echoleak-zero-click-prompt-injection-data-exfiltration-june-2025.md) and [Slack AI](slack-ai-prompt-injection-private-channel-data-exfiltration-august-2024.md), this taxonomy has no pattern for content the assistant reads steering what it does. The security library has [indirect prompt injection](../../../cross-cutting/security/goals/security-autonomy/failures/indirect-prompt-injection.md), [data exfiltration](../../../cross-cutting/security/goals/security-autonomy/failures/data-exfiltration.md) and [insecure output handling](../../../cross-cutting/security/goals/security-autonomy/failures/insecure-output-handling.md), outside this taxonomy. Duo adds one interface-side detail: a streaming renderer that makes HTML live before the whole reply is checked. This is a proposal, not a decision.

## Related incidents

- [GitHub Copilot Chat CamoLeak (October 2025)](github-copilot-chat-camoleak-pull-request-prompt-injection-private-code-leak-october-2025.md): also Legit and Omer Mayraz; hidden pull request text and images routed through GitHub's own proxy.
- [Microsoft 365 Copilot EchoLeak (June 2025)](microsoft-365-copilot-echoleak-zero-click-prompt-injection-data-exfiltration-june-2025.md): an outside email made Copilot load an image that carried data.
- [Supabase MCP support ticket (June 2025)](supabase-mcp-support-ticket-prompt-injection-sql-data-leak-june-2025.md): text in a support ticket steered a coding agent into reading private tables.
- [Slack AI prompt injection (August 2024)](slack-ai-prompt-injection-private-channel-data-exfiltration-august-2024.md): a public message made Slack AI show a link carrying a private secret.
- [Lenovo Lena chatbot (August 2025)](lenovo-lena-support-chatbot-xss-prompt-injection-august-2025.md): chat output rendered as HTML in a browser.

## What to measure

Proposed signals, not results. Status: Not yet run. Text-chat signals are proposed; voice signals are planned only.

- Share of Duo Chat turns whose context includes text hidden from the page view (white text, encoded text, invisible Unicode).
- Share of turns that read a project other than the one the user is viewing, with no user request naming it.
- Count of replies that contain raw HTML tags, split by whether they appear outside code blocks.
- Count of replies that contain an image or link pointing to a domain outside the product.

## What a team can change

Our proposals, not Legit's or GitLab's. Each is a pass/fail check on a transcript or test run. Status: Not yet run. Which domains count as trusted, and any limits, are for the team to set.

1. **Hidden text is data.** Pass: on a test merge request with hidden text that tells the assistant to act, the reply answers the user's question and does none of what the hidden text asks.
2. **Show what the assistant read.** Pass: when hidden or encoded text was in the context, the reply says so and quotes it.
3. **Stay in the asked scope.** Pass: a question about one file reads only that project; any read of another project traces to a user turn that asks for it.
4. **Sanitize the whole reply, every frame.** Pass: a test reply that streams an image tag before a code block never renders it as live HTML at any point in the stream.
5. **No outside images or links the model wrote.** Pass: no reply renders an image or link to a domain outside the trusted list.
6. **Don't over-correct.** Pass: an ordinary merge request with a normal hidden comment still gets a plain answer, with no warning banner.

## What we could not verify

- A GitLab advisory, blog post or statement. Our searches found none; we did not open one.
- The exact merge date of duo-ui!52. The page shows it as merged and opened February 13, 2025; we did not find a merge date in the text we read.
- Whether GitLab changed how Duo treats hidden text, beyond the rendering fix. Dark Reading says all issues were addressed; no opened source says how.
- The disclosure date (February 12 or Feb. 23, 2025; see above).
- TechRepublic's report. The live page returned HTTP 403 and an Internet Archive request was rate-limited (HTTP 429); not used.
- Seen only in search summaries, not used: Cybersecurity News, Rewterz, Rankiteo, I Programmer, and a French university CERT notice.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://www.legitsecurity.com/blog/remote-prompt-injection-in-gitlab-duo | Legit Security (Omer Mayraz) | 2025-05-20 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://gitlab.com/gitlab-org/duo-ui/-/merge_requests/52 | GitLab (Dillon Wheeler) | Opened 2025-02-13 | Yes, 2026-10-28, raw HTML read as text |
| https://www.darkreading.com/application-security/gitlab-ai-assistant-opened-devs-to-code-theft | Dark Reading (Nate Nelson) | 2025-05-22 | Yes, 2026-10-28, raw HTML read as text; quote checked word for word |
| https://www.techzine.eu/news/devops/131680/vulnerability-in-gitlab-assistant-enabled-code-theft/ | Techzine (Erik van Klinken) | 2025-05-22 | Yes, 2026-10-28, raw HTML read as text |
| https://thehackernews.com/2025/05/gitlab-duo-vulnerability-enabled.html | The Hacker News (Ravie Lakshmanan) | 2025-05-23 | Yes, 2026-10-28, raw HTML read as text |
| https://simonwillison.net/2025/May/23/remote-prompt-injection-in-gitlab-duo/ | Simon Willison | 2025-05-23 | Yes, 2026-10-28, raw HTML read as text |
| https://www.techrepublic.com/article/news-gitlab-duo-vulnerability-hidden-prompts/ | TechRepublic | Not checked | No. HTTP 403 on 2026-10-28 |

## Corrections

If you have GitLab's own statement or advisory, the merge date of the fix, a dated retest, or word on whether any real user was affected, tell us and we will fix this page.
