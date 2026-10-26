---
title: "OpenAI's ChatGPT Atlas Browser: Address-Bar Text Run as a Command, and a Disputed Memory Attack, October 2025"
date: 2025-10-24
source: "https://neuraltrust.ai/blog/openai-atlas-omnibox-prompt-injection"
description: "Days after OpenAI launched Atlas, NeuralTrust showed URL-like text in its address bar run as a command; LayerX claimed a memory attack that OpenAI disputed."
summary: "OpenAI launched its ChatGPT Atlas browser on October 21, 2025, and its launch post warned that agents are open to hidden instructions. On October 24, NeuralTrust (Martí Jordà) said text built to look like a web address, but malformed, was treated by Atlas's address bar as a trusted command to the agent. Around October 27-28, LayerX said a forged request could write hidden instructions into a user's ChatGPT memory; OpenAI told CSO Online the issue does not affect Atlas and it could not reproduce it. No opened source reports use against real users. Status: Needs review."
categories:
  - Security
patterns:
  - conflicting-inputs-resolved-silently
  - missing-the-obvious-intent
  - misreading-the-screen
---

# OpenAI's ChatGPT Atlas Browser: Address-Bar Text Run as a Command, and a Disputed Memory Attack, October 2025

**This page is a dated teardown of two public security findings about one AI browser, for teams that ship a single text box that can either go somewhere or tell an agent to do something.** The product was OpenAI's ChatGPT Atlas, a browser for macOS with ChatGPT built in. The user was anyone who pasted a link into its address bar, or who stayed signed in to ChatGPT while browsing. The moment was the paste: by NeuralTrust's account, text that looked like a link was read as the user's own command. Every fact below comes from a source we opened (listed at the end).

**Status: Needs review.** Eight pages (OpenAI's launch post, NeuralTrust, Simon Willison's weblog, The Hacker News, CSO Online, SC Media, teiss and TechSpot) were downloaded as raw HTML on 2026-10-26 and read as text. Quotes were string-matched against those files. LayerX's own blog returned 403 and was not read, so every LayerX claim here is as relayed by news outlets.

> **Read this first.** This is a summary of public reporting, most of it by security companies that sell AI security products. It is not security or legal advice. We did not test Atlas, then or now. We reproduce no attack text, prompt or method; we only say what the researchers say happened. We make no finding about anyone's intent. **Last updated: 2026-10-26.**

**Why the slug says October 2025.** OpenAI launched Atlas on October 21, 2025. NeuralTrust's post is dated October 24, and the LayerX coverage we opened is dated October 27 to 29. We date the page by when the failures became public, as the sibling teardowns do.

## What happened (as reported)

- **The launch and its warning.** OpenAI's post (October 21, 2025) says Atlas launched "worldwide on macOS", with ChatGPT memory built in, optional "browser memories," and agent mode in preview for Plus, Pro and Business users. It says agents "are susceptible to hidden malicious instructions" and that "our safeguards will not stop every attack that emerges as AI agents grow in popularity." It lists limits: the agent cannot run code in the browser or reach other apps, it pauses on some sensitive sites, such as financial institutions, to make sure the user is watching, and a logged-out mode limits its access.
- **OpenAI's security chief.** Simon Willison (October 22, 2025) quotes a post on X by Dane Stuckey, OpenAI's Chief Information Security Officer, saying "prompt injection remains a frontier, unsolved security problem". Stuckey describes a "Watch Mode" that pauses the agent if the user leaves a sensitive tab. Willison writes that on GitHub and a banking site, "Atlas continued to navigate even when I had switched to another application." That is one tester's report; we did not open Stuckey's post on X.
- **The address-bar finding.** NeuralTrust (Martí Jordà, October 24, 2025) says Atlas's address bar, which it calls the omnibox, reads input either as a web address or as a command to the agent. It says a string made to look like a link, but malformed so it fails as one, is treated as a prompt, and "The embedded instructions are now interpreted as trusted user intent with fewer safety checks." NeuralTrust's examples are hypothetical: a "Copy link" button that hands the user such a string, leading to a fake Google page, or one telling the agent to delete files in Google Drive. Its timeline lists the finding and the public post on the same day, October 24. It does not say whether OpenAI was told first or replied.
- **News coverage.** The Hacker News (Ravie Lakshmanan, October 27, 2025) and TechSpot (Alfonso Maruccia, October 29, 2025) repeat NeuralTrust's account. Neither carries an OpenAI comment on it.
- **The memory claim.** CSO Online (Nidhi Singal, October 28, 2025) says LayerX researchers found a way for a web page to send a forged request (cross-site request forgery, or CSRF) that rides on the user's ChatGPT sign-in and writes hidden instructions into ChatGPT's memory, which later chats then use. SC Media (October 28, 2025) calls it "Tainted Memories" and quotes LayerX's Michelle Levy on "a standard CSRF chained to a memory write". teiss (October 28, 2025) says such memories can last until the user deletes them in settings. CSO says LayerX reported it to OpenAI without sharing more technical detail.
- **OpenAI's answer.** CSO quotes an OpenAI spokesperson: "To our knowledge, this issue doesn’t impact ChatGPT Atlas, which isn’t vulnerable to this kind of cross-site request forgery (CSRF) attack." The spokesperson said OpenAI could not reproduce the report from what it was given, and: "We have not seen any real-world attempts to exploit this to date."
- **A phishing test.** CSO says that in LayerX's tests, 97 of 103 in-the-wild attacks got through Atlas, a failure rate over 94%, and that Chrome and Edge stopped about 50%. SC Media gives 5.8% blocked for Atlas and 47% for Chrome. These are LayerX's numbers; no opened source repeats the test.

## What the user saw

The user copies what looks like a link, maybe from a page's "Copy link" button, and pastes it into the address bar. They expect a web page to load. By NeuralTrust's account, the browser instead hands the text to the agent as if the user had typed a request, and the agent goes where the text says. Nothing in the opened sources says the screen told the user that their paste was being run as a command. For the memory claim, the user does nothing unusual after one visit to a bad page; LayerX, via CSO, says later chats draw on the planted memory. OpenAI disputes that this works in Atlas.

## Where in the flow it broke

Based on the researchers' accounts, and only as far as they go:

1. **One box, two meanings.** The address bar decides on its own whether input is a place to go or a task to do (NeuralTrust).
2. **The silent fallback.** When the input fails as a web address, it becomes a prompt with no question to the user (NeuralTrust).
3. **Borrowed trust.** Text the user pasted, but did not write, is treated as the user's own words, with fewer checks than page content gets (NeuralTrust).
4. **The reach.** The agent can act in sites where the user is signed in (OpenAI's own launch post names this risk).
5. **The memory step (disputed).** A forged request writes to memory that the user did not ask to change, and later chats trust it (LayerX via CSO; OpenAI says Atlas is not affected).
6. **The report.** No opened source says Atlas told the user that their input, or their memory, carried someone else's instructions.

**Contrast with Perplexity Comet.** In [Brave's Comet finding (August 2025)](perplexity-comet-browser-indirect-prompt-injection-august-2025.md), the hidden instructions sat in a web page the user asked to summarize; the agent mixed page text with the user's request. In NeuralTrust's Atlas finding, the instructions arrive through the box reserved for the user, so they skip the line entirely and look first-party. Both rest on the same missing boundary between what the user said and what someone else wrote.

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| Did the memory attack work in Atlas? | LayerX, via CSO, SC Media and teiss: yes. OpenAI, via CSO: not to its knowledge, and not reproduced. No opened source settles it. |
| Phishing numbers | CSO: over 94% failure, 97 of 103; Chrome and Edge about 50%. SC Media: 5.8% blocked; Chrome 47%. Both from LayerX. |
| Was the address-bar issue fixed? | No opened source says. |
| Did OpenAI hear from NeuralTrust before the post? | NeuralTrust's timeline lists only October 24. No opened source says. |
| Real-world use | OpenAI, via CSO: none seen for the memory claim. No source reports use of the address-bar trick. |

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). No pattern in this taxonomy covers prompt injection, so every fit is partial.

- **[Conflicting inputs resolved silently](../goals/multimodal-input/failures/conflicting-inputs-resolved-silently.md)** (`conflicting-inputs-resolved-silently`). Partial fit. The input looked like one thing (a link) and contained another (a command), and the browser picked one reading without saying so. That pattern is about text clashing with an attachment, not an attacker.
- **[Missing the obvious intent](../goals/embedded-copilots/failures/missing-the-obvious-intent.md)** (`missing-the-obvious-intent`). Partial fit. The likeliest meaning of pasting a link is to open that site. Atlas, per NeuralTrust, read it as a task. That pattern is about everyday misreads in an in-product assistant, not hostile text.
- **[Misreading the screen](../goals/browser-agents/failures/misreading-the-screen.md)** (`misreading-the-screen`). Weak fit. A browser agent treated content as a command. That pattern is about wrong clicks and false "done" reports.
- **Considered, not a fit.** [Over-confirmation](../goals/dialogue-management/failures/over-confirmation.md) (`over-confirmation`): the problem here is a missing question, not too many. [Memory contaminates conversation experiments](../goals/model-and-prompt-changes/failures/memory-contaminates-conversation-experiments.md) (`memory-contaminates-conversation-experiments`): about A/B tests, not an outside write to memory.
- **Gap for a person to judge.** As the Comet page notes, the [emerging surfaces roadmap](../roadmap/emerging-surfaces.md) names hidden instructions hijacking a browsing agent, but no pattern page exists in this taxonomy. The cross-cutting security library has [indirect prompt injection](../../../cross-cutting/security/goals/security-autonomy/failures/indirect-prompt-injection.md) and [prompt injection via user context](../../../cross-cutting/security/goals/security-autonomy/failures/prompt-injection-via-user-context.md), outside this taxonomy. Two interface-side patterns may be warranted: a dual-purpose input box that silently switches modes, and saved memory changed without the user seeing it. These are proposals, not decisions.

## Related incidents

- [Perplexity Comet indirect prompt injection (August 2025)](perplexity-comet-browser-indirect-prompt-injection-august-2025.md): the same class of attack, there through page text.
- [ChatGPT Connectors "AgentFlayer" poisoned document (August 2025)](openai-chatgpt-connectors-agentflayer-poisoned-document-data-leak-august-2025.md): another OpenAI surface where outside content steered the model.
- [OpenAI Operator buys eggs without confirmation (February 2025)](openai-operator-buys-eggs-without-confirmation-february-2025.md): OpenAI's earlier browser agent acting without asking.
- [ChatGPT memory: missing memories (November 2025)](chatgpt-memory-missing-memories-november-2025.md): users unable to see or trust what ChatGPT's memory holds.

## What to measure

Proposed signals, not results. Status: Not yet run.

| Signal | How to compute |
|---|---|
| Silent mode switch rate | Address-bar inputs that start like a web address but are sent to the agent as a prompt with no on-screen choice, divided by all such inputs |
| Off-task action rate | Agent runs started from pasted text where the agent opens a site or takes a step not named in visible text the user typed, divided by those runs |
| Memory writes without notice | Memory entries created with no visible "memory updated" notice in the same chat, divided by all memory writes |
| Memory writes from outside | Memory entries whose origin is not a user turn in a chat, from server logs, divided by all memory writes |
| Watch-mode hold rate | Runs on sensitive sites where the user switched away and the agent kept acting, divided by runs where the user switched away |

## What a team can change

Our proposals, not OpenAI's. Each is a pass/fail check on a transcript, a screen or a log. Status: Not yet run.

1. **Ask which one.** Pass: when input in a shared box fails as a web address, the screen asks "Go to a site or ask the assistant?" before anything runs. Fail: it runs as a prompt with no choice, as NeuralTrust recommends avoiding.
2. **Pasted is not typed.** Pass: pasted text that tells the agent to act gets a confirmation that quotes the action. Fail: the agent acts on pasted text with no prompt.
3. **Say what changed in memory.** Pass: every memory write shows a notice in the chat that names the new entry. Fail: an entry appears in settings with no notice.
4. **Only the user writes memory.** Pass: a memory write that does not come from a user turn is refused and logged. Fail: it is stored.
5. **Keep the promise on sensitive sites.** Pass: when the user leaves a sensitive tab, the agent stops within one step. Fail: it keeps going.
6. **Don't over-correct.** Pass: ordinary links still open on one paste, and ordinary questions still go to the assistant, with no extra prompt.

## What we could not verify

- LayerX's own write-up and its date. Its blog returned 403; we relied on CSO Online, SC Media and teiss.
- Dane Stuckey's post on X. Seen only as quoted by Willison and The Hacker News.
- Whether OpenAI fixed the address-bar issue, or answered NeuralTrust. No opened source says.
- That LayerX found Atlas users were up to 90% more exposed than Chrome or Edge users. Seen only in search summaries.
- When OpenAI deprecated Atlas. Its launch post now says "Atlas has since been deprecated", with no date, and we do not tie that to these findings.
- Seen only in search summaries, not used: a Nopal Cyber advisory (October 31, 2025), reports in Decrypt, eSecurity Planet and the AI Incident Database, and claims of clipboard and Google Docs attacks on launch day.

## Sources

| URL | Publisher (author) | Date | Opened |
|---|---|---|---|
| https://openai.com/index/introducing-chatgpt-atlas/ | OpenAI | 2025-10-21 | Yes, 2026-10-26, raw HTML read as text; quotes checked |
| https://simonwillison.net/2025/Oct/22/openai-ciso-on-atlas/ | Simon Willison's Weblog (Simon Willison), quoting Dane Stuckey | 2025-10-22 | Yes, 2026-10-26, raw HTML read as text; quotes checked |
| https://neuraltrust.ai/blog/openai-atlas-omnibox-prompt-injection | NeuralTrust (Martí Jordà) | 2025-10-24 | Yes, 2026-10-26, raw HTML read as text; quotes checked |
| https://thehackernews.com/2025/10/chatgpt-atlas-browser-can-be-tricked-by.html | The Hacker News (Ravie Lakshmanan) | 2025-10-27 | Yes, 2026-10-26, raw HTML read as text |
| https://www.csoonline.com/article/4080144/atlas-browser-exploit-lets-attackers-hijack-chatgpt-memory.html | CSO Online (Nidhi Singal) | 2025-10-28 | Yes, 2026-10-26, raw HTML read as text; quotes checked |
| https://www.scworld.com/brief/chatgpt-atlas-hit-by-tainted-memories-exploit | SC Media (SC Staff) | 2025-10-28 | Yes, 2026-10-26, raw HTML read as text; quote checked |
| https://www.teiss.co.uk/news/new-chatgpt-atlas-browser-exploit-can-hide-persistent-malicious-instructions-that-execute-code-16618 | teiss (no byline found) | 2025-10-28 | Yes, 2026-10-26, raw HTML read as text |
| https://www.techspot.com/news/110049-openai-chatgpt-atlas-vulnerable-prompt-injection-attacks-within.html | TechSpot (Alfonso Maruccia) | 2025-10-29 | Yes, 2026-10-26, raw HTML read as text |
| https://layerxsecurity.com/?p=3590 | LayerX Security | Unknown | No, blocked (403) |

## Corrections

If you have LayerX's original post, an OpenAI reply to NeuralTrust, or a record of a fix for either issue, tell us and we will fix this page.
