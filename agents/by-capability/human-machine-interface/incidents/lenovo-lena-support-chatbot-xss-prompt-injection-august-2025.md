---
title: "Lenovo's 'Lena' Support Chatbot: One Prompt Turned Chat Output Into Script Aimed at Agents"
date: 2025-08-18
source: "https://www.csoonline.com/article/4043005/lenovo-chatbot-breach-highlights-ai-security-blind-spots-in-customer-facing-systems.html"
summary: "In August 2025, Cybernews researchers reported that a roughly 400-character prompt made Lenovo's GPT-4-based support chatbot Lena emit HTML that could send session cookies to an attacker's server, including from a human agent's browser after a handoff. Lenovo said it assessed the risk and took corrective action. The attack chain is the researchers' demonstration; no opened source reports real-world theft."
categories:
  - Security
patterns:
  - handoff-summary-is-wrong-or-misleading
---

**This page is a dated teardown of one public security finding about a customer-support chatbot, for teams that show chatbot output in a web page or pass chat transcripts to human agents.** Every fact below comes from a source we opened (listed at the end), and none is the researchers' own write-up, which we could not open. The attack is what researchers say they demonstrated; we found no report of misuse against real customers.

## Read this first

This page is design guidance, not security or legal advice. It does not say whether any company broke any law or standard. Have a qualified security engineer review your own chat rendering and handoff flow. We give no working attack text on purpose.

## What happened (as reported)

- **July 22, 2025.** Adversa AI (Aug 22) says Cybernews researchers found the flaw and told Lenovo the same day. This date comes from one secondary source; we found it nowhere else.
- **Aug 6, 2025.** Adversa says Lenovo acknowledged the flaw two weeks after notice. Also single-source.
- **Before Aug 18, 2025.** Adversa says Lenovo had put protective measures in place, gives no patch date, and says Lenovo did not publish specific deployment dates. No opened source gives the fix date.
- **Aug 18-20, 2025.** Public coverage appears. Security Boulevard (Aug 19, updated Aug 21), CSO (Aug 20) and Cyber Security News (Aug 20) report the finding. Adversa dates public disclosure to Aug 18-20.
- **Lenovo's statement.** CSO quotes Lenovo spokesman Stuart Gill saying a third-party researcher alerted the company, it assessed the risk, took corrective actions, and thanked the researchers. Security Boulevard says Lenovo was "recently made aware" of it.

## What the researchers reported they did

From the opened coverage (our paraphrase; the sources differ in small details):

- **The bot.** Lena is Lenovo's customer-support chatbot, described as built on OpenAI's GPT-4.
- **One prompt.** About 400 characters. It began as a normal product question, then asked for the reply in HTML and in other formats so the page would render it.
- **The payload.** The reply carried an image tag with an invalid source, so the browser's error handler ran and sent cookie data to a server the researchers controlled. A last instruction pressed the bot to show the image.
- **Stored in the chat.** The ATLAS case study and the AI Incident Database summary say the reply was saved in the chat history.
- **The handoff.** Those same two sources say that when the researchers asked for a human, the agent's normal step of opening the transcript ran the payload in the agent's browser and exposed the agent's session cookie. Security Boulevard and CSO describe the cookie capture without this step, so the sources differ on exactly when the code ran.
- **Why, per the researchers.** Weak input and output handling: the bot's text was treated as safe to render, and user text reached the model unchecked.

## Demonstrated versus potential

| Topic | What the sources say |
|---|---|
| Demonstrated | Session cookies could be captured, by the researchers. CSO and Security Boulevard both say they report no real-world theft. |
| Potential, not tested | Logging in as an agent, reading live and past chats, keylogging, phishing redirects, changing what agents see, lateral movement. Adversa and the AI Incident Database summary label these as risks the researchers named, not shown outcomes. |
| Fix | Lenovo says corrective action; no opened source says what changed. |
| Severity | Adversa says no formal severity score was published. "Critical" is the press and researchers' word. |

## What the sources do not say

- Whether anyone other than the researchers ever sent such a prompt, or whether any customer or agent session was taken over.
- The exact prompt, Lenovo's logs, or how long the flaw existed before July 22.
- What the fix was, or its date.
- Whether the sales or product-question flow had other holes. We opened no test.
- Cybernews's own account of dates and steps. Its page returned an error to our fetch tool (HTTP 403), so every detail here is second-hand.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [Handoff summary is wrong or misleading](../goals/human-handoff/failures/handoff-summary-is-wrong-or-misleading.md) (`handoff-summary-is-wrong-or-misleading`). Weak, partial fit. The only link is the handoff: what the bot produced reached a human unchecked. That pattern is about summaries that drop or invent facts, not about code in a transcript.

The core failure here, model output rendered as live page content, is not covered by any pattern in the taxonomy. We do not force a match. This page may be evidence for a future security-focused pattern; that is a proposal, not a decision.

## Where in the flow it broke

Based on the reports, and only as far as they go:

1. **User input.** Text with hidden instructions reached the model. The sources say nothing was filtered or length-limited.
2. **Model output.** The model produced markup on request.
3. **Storage.** The markup was reportedly saved in the transcript.
4. **Display.** A browser rendered it, in the customer's chat or, per two sources, the agent's console.
5. **Handoff.** The person receiving the transcript trusted it as ordinary text.
6. **Response.** A private report, an acknowledgement two weeks later per one source, a fix, and thin public detail.

The reported cost is press coverage. We found no figure for loss, and none for customers affected.

## What to measure

Our proposals, not Lenovo's or the researchers'. Status: Not yet run.

| Metric | How to compute from logs |
|---|---|
| Raw-markup rate | Bot replies containing HTML tags or script-like text, divided by replies |
| Render-sanitize rate | Scripted replies containing markup that display as plain text in the customer view and the agent view, divided by scripted replies |
| Handoff-view parity | Scripted transcripts that render with no active content in the agent console, divided by scripted transcripts |
| Over-block rate | Ordinary questions that mention code or HTML and still get a normal answer, divided by those questions |

## What a team can change

Our proposals, not Lenovo's. Status: Not yet run. These are chat-design checks, not a security audit.

1. **Treat bot output as untrusted text.** Show it as text or an allow-listed format, never as raw page markup. Check: a scripted reply containing a tag shows as characters in every view.
2. **Check the agent console separately.** Agents often view transcripts in a different tool. Check: the same scripted transcript is safe there.
3. **Limit what a reply may contain.** Strip or refuse links and images that point off-site unless a rule allows them. Check: a scripted reply with an off-site image shows no image.
4. **Say what the bot will not do.** If asked to reply in code or markup, answer in plain words and offer the product help instead. Check: the scripted request gets a plain answer.
5. **Keep a reporting path.** Publish a way to report a flaw, and log the date of notice, reply and fix. Check: the log has all three.
6. **Don't over-correct.** Blocking every message that contains code harms users who truly need a snippet. Run rule 4 with an ordinary-question set and require near-zero refusals.

## Sources

| URL | Publisher | Date | Status |
|---|---|---|---|
| https://www.csoonline.com/article/4043005/lenovo-chatbot-breach-highlights-ai-security-blind-spots-in-customer-facing-systems.html | CSO Online (Gyana Swain) | 2025-08-20 | Opened 2026-10-20 (fetch tool returned a summary) |
| https://securityboulevard.com/2025/08/flaw-in-too-trusting-lenovo-chatbot-could-have-let-hackers-in/ | Security Boulevard (Jeffrey Burt) | 2025-08-19 | Opened 2026-10-20 (summary) |
| https://cybersecuritynews.com/lenovo-ai-chatbot-vulnerability | Cyber Security News (Florence Nightingale) | 2025-08-20 | Opened 2026-10-20 (summary) |
| https://adversa.ai/blog/lenovo-ai-chatbot-incident-critical-xss-vulnerability-exposes-enterprise-ai-security-gaps | Adversa AI (vendor blog) | 2025-08-22 | Opened 2026-10-20 (summary); source of the July 22 and Aug 6 dates |
| https://www.startupdefense.io/mitre-atlas-case-studies/aml-cs0060-cross-site-scripting-via-prompt-manipulation-in-lenovo-ai-chatbot | Startup Defense, repeating MITRE ATLAS case AML.CS0060 | undated | Opened 2026-10-20 (summary) |
| https://incidentdatabase.ai/reports/6189 | AI Incident Database, hosting a Cybernews report | 2025 | Opened 2026-10-20 (summary of a mirror, not the original) |

Not opened, and not used as facts above: the Cybernews original (https://cybernews.com/security/lenovo-chatbot-lena-plagued-by-critical-vulnerabilities/, HTTP 403); BetaNews (HTTP 403; known only from search summaries); the ATLAS site itself; any Lenovo advisory; and other outlets seen only in search summaries. Our fetch tool summarizes pages, so quotes are limited to short phrases attributed to Lenovo. Two dates and the handoff detail rest on one or two secondary sources.

## Corrections

If you have the Cybernews write-up, a Lenovo advisory, or better dates, tell us and we will fix this page.
