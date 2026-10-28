---
title: "ChatGPT memory: text in a document or web page could write lasting memories, and the SpAIware demo made the Mac app leak every later chat, September 2024"
date: 2024-09-20
source: "https://embracethered.com/blog/posts/2024/chatgpt-macos-app-persistent-data-exfiltration/"
description: "How untrusted web or document text could plant lasting ChatGPT memories, and how one planted memory made the Mac app send every later chat to a stranger."
summary: "On May 22, 2024, security researcher Johann Rehberger (Embrace The Red) showed that a Google Doc, an uploaded image or a web page could make ChatGPT write false memories that carried into later chats. He says OpenAI closed his May report as a model safety issue, not a security one. In June 2024 he reported a second demo, which he named SpAIware: a planted memory told the ChatGPT macOS app to send what the user typed, and ChatGPT's replies, to his server in every new chat. He says OpenAI fixed that data path in ChatGPT version 1.2024.247 in September 2024, and he disclosed it on September 20, 2024. He also says untrusted content could still write memories. Ars Technica (Dan Goodin, September 24, 2024) called the fix partial. No opened source reports use against real users."
categories:
  - Security
patterns:
  - conflicting-inputs-resolved-silently
  - confident-wrong-answer-with-no-way-to-check
  - ambient-assistants-act-on-overheard-conversation
  - over-confirmation
---

**This page is a dated teardown of one public security finding about ChatGPT's long-term memory, for teams that ship an assistant that saves facts about the user across chats while it also reads documents, images or web pages written by strangers.** The product was OpenAI's ChatGPT, with the SpAIware demo run in its macOS app. The user was anyone with memory on who asked ChatGPT to look at a document or web page. The moment was that one request: by Rehberger's account, the outside text wrote a memory, and from then on every new chat carried it. Every fact below comes from a source we opened (listed at the end). The attacks are Rehberger's proofs of concept; no opened source reports use against real users.

**Status: Needs review.** Rehberger's two Embrace The Red posts, an archived copy of the Ars Technica article, The Hacker News and TechRadar were downloaded as raw HTML on 2026-10-28 and read as plain text. Each quote below was checked word for word against that text. The live Ars Technica page refused our download (HTTP 403 and 405), so we read the Wayback Machine copy captured on December 17, 2024. We found no OpenAI advisory or statement on this finding (see "What we could not verify").

> **Read this first.** This is a summary of public research and reporting, not a finding of fact and not security or legal advice. We describe the attack at a high level only. Rehberger published his injection text and the address of his collection server; we do not repeat either, and we give no steps to rebuild the attack. Have a qualified security engineer review your own assistant.

**Channel note.** Text chat. The user typed requests into ChatGPT (on the web in the May demos, in the macOS app for SpAIware), and the model called its own memory tool and drew images on its own. This phase of the knowledge base is chat-first: the text-chat signals and checks below are proposed; voice is planned and not covered here.

## What happened (as reported)

- **The feature.** Rehberger's May post says ChatGPT's memory lets it recall information across chats, and that "The memory feature is on by default in ChatGPT." He found a memory tool, named bio in the system prompt, that the model calls to save a fact. When it runs, the chat shows a "Memory updated" notice the user can click to see what was saved. Ars Technica says OpenAI began testing memory in February 2024 and made it more broadly available in September 2024.
- **Who and when.** Rehberger posted "ChatGPT: Hacking Memories with Prompt Injection" on May 22, 2024, after a post on X dated May 17, 2024. He posted "Spyware Injection Into Your ChatGPT's Long-Term Memory (SpAIware)" on September 20, 2024. His timeline lists a public talk at BSides Vancouver Island 2024 the same day.
- **Three ways in (May 2024).** Rehberger tried three routes for outside text to reach the chat. A Google Doc read through ChatGPT's Connected Apps feature wrote memories; he says every instruction in the document became a memory. An image the user asked ChatGPT to analyze also wrote memories. Browsing with Bing at first refused to call the memory tool, which he took as a quiet OpenAI defense. He says he got around it a few times, for example by chaining a memory write to an image request, and that it worked "at least 2-3 times."
- **What a planted memory does.** Per Rehberger, the planted memories showed up and were used in a new chat. He writes that a prompt injection could also delete all of a user's memories, and: "I was able to create dozens of new, fake memories in one shot." Ars Technica says his demo made ChatGPT believe the user was 102 years old, lived in the Matrix and thought Earth was flat, and that ChatGPT would use that in all future chats.
- **OpenAI's first answer.** Rehberger writes that the May report "was closed as “Model Safety Issue” and it is not considered a security vulnerability." He disagreed, saying it harms the integrity of stored memories and all future chats.
- **The SpAIware demo (reported June 2024).** Rehberger's September post says the user analyzes an untrusted document or visits an untrusted website. Its text makes ChatGPT save a memory with spyware instructions. From then on, each new chat tells ChatGPT to draw an image from his server, with the user's words and ChatGPT's reply placed in the image address. Drawing the image delivers that text to the server. He writes: "The image rendered in the video is invisible for stealth." In the video, per Ars, he says: "What is really interesting is this is memory-persistent now".
- **Why the Mac app.** Per Rehberger, OpenAI added a check named url_safe in December 2023 that tells the app whether an image address is safe to show. He says the check ran on the client, so the web app got it but the iOS app stayed open, and the newer macOS and Android apps shipped with the same gap in 2024. Ars and TechRadar say the attack did not work in the ChatGPT web interface because of that check.
- **The fix.** Rehberger's timeline says OpenAI fixed the issue in ChatGPT version 1.2024.247 in September 2024, and his post says OpenAI released the macOS fix the week before September 20. The Hacker News (Ravie Lakshmanan, September 25, 2024) says the fix closed the exfiltration vector.
- **What the fix did not cover.** Rehberger asks whether hacking memories through prompt injection is fixed and answers: "No. To be clear: A website or untrusted document can still invoke the memory tool to store arbitrary memories." He says only the image route for sending data out was closed. Ars Technica wrote that OpenAI "issued a partial fix earlier this month."
- **His advice to users.** Watch for the "Memory updated" notice and click through it, review stored memories often, delete suspicious ones, and use temporary chats or turn memory off. TechRadar (Ellen Jennings-Trace, September 26, 2024) repeats this advice.
- **His advice to builders (May post).** Do not call tools on their own once untrusted data is in the chat; if a tool does run, let the user see and decide; always ask before deleting all memories; and cap how many memories one turn can add.

## What OpenAI did

- **May 2024.** Per Rehberger, OpenAI closed his memory report as a model safety issue. He says it seemed to have added quiet defenses to the browsing tool, which he could still get past, and none to images or Connected Apps.
- **September 2024.** Per Rehberger and The Hacker News, OpenAI fixed the image-based data path in macOS app version 1.2024.247. Rehberger thanks OpenAI for the fix.
- **No public statement we found.** Ars Technica says: "Company representatives didn’t respond to an email asking about its efforts to prevent other hacks that plant false memories." No opened source quotes OpenAI.
- **Impact on real users.** Unknown. No opened source says anyone other than Rehberger used the technique.

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| How SpAIware started | Rehberger: the user analyzes an untrusted document or visits an untrusted website. Ars: the user told ChatGPT to view a web link that hosted a malicious image. |
| How complete the fix was | Rehberger: the data path is fixed; memory writes from untrusted content are not. Ars: a "partial fix." TechRadar's subhead: OpenAI introduced a partial fix to the exploit. THN: "now-patched." |
| When memory launched | Ars: testing in February 2024, broader in September 2024. THN: introduced in February, rolled out to Free, Plus, Team and Enterprise users at the start of September. We did not open OpenAI's own announcement. |
| The 102-year-old, Matrix and flat-Earth memories | Ars reports them. The text of Rehberger's May post does not name them; they may be in his screenshots or video, which we did not view. |
| Web interface | Ars and TechRadar: not possible there thanks to url_safe. Rehberger's September post says url_safe still lets some information leak and points to known bypasses. |

## Where in the conversation flow it broke

Based on Rehberger's account, and only as far as it goes:

1. **The input.** The user asked ChatGPT to read a document, an image or a web page written by someone else.
2. **The mix-up.** ChatGPT gave that outside text the same standing as the user's words and called its memory tool.
3. **The silent write.** The only sign was a small "Memory updated" notice. No step asked the user whether to save what the page said.
4. **The carry-over.** The memory loaded into every new chat. Closing the chat did not end the attack.
5. **The send.** In the Mac app, each later reply drew an invisible image whose address held the user's words, which sent them to Rehberger's server.
6. **The report.** Nothing in the opened sources says ChatGPT told the user that a memory came from a web page or document rather than from them.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). No pattern in this taxonomy covers prompt injection, outside text writing to saved memory, or data leaving through an image address, so no fit is strong.

- [Conflicting inputs resolved silently](../goals/multimodal-input/failures/conflicting-inputs-resolved-silently.md) (`conflicting-inputs-resolved-silently`). **Partial fit.** The user asked to read a page or file; the content asked for a memory write. ChatGPT followed the content and did not point out the clash. That page is about a text-versus-attachment clash, not an attacker, so its fix (ask which is right) is too weak alone.
- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Weak fit.** Per Ars, false memories (age 102, flat Earth) would steer all future answers, and nothing in the reply shows that an answer rests on a planted memory. It is weak because no opened source shows a specific wrong answer the user received.
- [Ambient assistants act on overheard conversation](../goals/proactive-and-ambient/failures/ambient-assistants-act-on-overheard-conversation.md) (`ambient-assistants-act-on-overheard-conversation`). **Weak fit.** Its rule (act only on a clear invitation from the user, and show what was heard) maps here: the order to remember came from a stranger's text. It is weak because that page is about always-on devices hearing speech.
- [Over-confirmation](../goals/dialogue-management/failures/over-confirmation.md) (`over-confirmation`). **Weak fit, for the fix, not the failure.** Rehberger asks for user confirmation before memory deletes and before tools run after untrusted data enters the chat. Memory writes happen often, so a prompt on each one could train users to click yes. A team adding approval should check how often it fires.
- **Considered, not a fit.** [No warning of context loss](../goals/effort-and-memory/failures/no-warning-of-context-loss.md) (`no-warning-of-context-loss`): about memory that is dropped, not memory that is added. [Fresh-session amnesia](../goals/effort-and-memory/failures/fresh-session-amnesia.md) (`fresh-session-amnesia`): the opposite problem; here a new chat remembered too much. [Memory contaminates conversation experiments](../goals/model-and-prompt-changes/failures/memory-contaminates-conversation-experiments.md) (`memory-contaminates-conversation-experiments`): about A/B test arms, not an outside write. [Silent attachment failures](../goals/chat-interface/failures/silent-attachment-failures.md) (`silent-attachment-failures`): the file was read; the harm came from obeying it. `no-user-facing-record-of-what-the-bot-said`: ChatGPT did show a "Memory updated" notice and a memory list; the problem was what got saved, not a missing record.
- **Possible gaps for a person to judge.** As the [Atlas page](openai-chatgpt-atlas-omnibox-and-memory-prompt-injection-october-2025.md) notes, this taxonomy has no pattern for saved memory changed by someone other than the user. The cross-cutting security library has [indirect prompt injection](../../../cross-cutting/security/goals/security-autonomy/failures/indirect-prompt-injection.md), [data exfiltration](../../../cross-cutting/security/goals/security-autonomy/failures/data-exfiltration.md) and [tool-based exfiltration](../../../cross-cutting/security/goals/data-loss-prevention/failures/tool-based-exfiltration.md), all outside this taxonomy. This case adds one interface-side detail: a memory write signaled only by a small notice turns one bad page into a lasting change in every later chat. This is a proposal, not a decision.

## How it differs from close cases

- [ChatGPT Atlas omnibox and memory (October 2025)](openai-chatgpt-atlas-omnibox-and-memory-prompt-injection-october-2025.md): LayerX's Atlas claim also ends with hidden instructions in ChatGPT memory, but its way in was a forged web request (CSRF) riding on the user's sign-in, not text the model read. OpenAI disputed that claim. Here, Rehberger's own posts show the write, and OpenAI fixed the data path while, per Rehberger, the memory write stayed possible.
- [ChatGPT missing memories (November 2025)](chatgpt-memory-missing-memories-november-2025.md): the same feature failing the other way. There saved memories vanished in a service incident; here unwanted ones were added by a stranger.
- [ChatGPT Mac app stored chats in plain text (July 2024)](openai-chatgpt-macos-app-stored-chats-in-plain-text-july-2024.md): the same Mac app two months earlier. There other software on the Mac could read chats on disk; here a planted memory sent chats over the network while the app worked as designed.
- [Google Gemini calendar invite (August 2025)](google-gemini-calendar-invite-prompt-injection-smart-home-hijack-august-2025.md): instructions in outside text waited for a later user turn before acting. Here the wait spans chats, because memory carries the instructions forward.
- [ChatGPT Connectors AgentFlayer (August 2025)](openai-chatgpt-connectors-agentflayer-poisoned-document-data-leak-august-2025.md): also a poisoned document and an image address carrying data out, and it got past url_safe on the web. AgentFlayer leaked once, in one chat; SpAIware kept leaking.
- [Slack AI prompt injection (August 2024)](slack-ai-prompt-injection-private-channel-data-exfiltration-august-2024.md): the same summer, a public message steered an assistant into showing a link that leaked a secret, but the user had to click it. Here no click was needed.

## What to measure

Proposed signals, not results. Status: Not yet run. Text-chat signals are proposed; voice signals are planned only.

- Share of memory writes made in a turn where the model read a web page, document, image or connector file the user did not write.
- Count of memories saved per turn; flag any turn that saves more than a set number.
- Share of saved memories that hold an instruction (for example, words telling the assistant what to do in future chats) rather than a fact about the user.
- Count of replies that draw an image or link from a domain the user never typed or approved, per 1,000 chats, split by app (web, macOS, iOS, Android).
- How often users open the "Memory updated" notice, and how often they then delete the new memory.

## What a team can change

Our proposals, not Rehberger's or OpenAI's. Each is a pass/fail check on a transcript or test run. Status: Not yet run. The limits and allowed domains are for the team to set.

1. **Outside text cannot write memory.** Pass: on a test page or file that tells the assistant to remember something, no memory is saved, and the reply summarizes the content.
2. **Say where a memory came from.** Pass: every saved memory shows whether the user said it in chat or it came from a named file or page, and the user can see that in the memory list.
3. **Ask before saving from content.** Pass: when a memory would be saved in a turn that read outside content, the user sees the exact text first and the save waits for a yes.
4. **Memories are facts, not orders.** Pass: a memory that tells the assistant to take an action in future chats (draw an image, add text to a link) is refused or flagged to the user.
5. **No user text in image addresses.** Pass: no rendered image or link address contains words from the user's message or the reply, in every client (web, desktop, mobile), with the check run on the server.
6. **Ask before wiping memory.** Pass: a request to delete all memories that did not come from a user turn does nothing and tells the user.
7. **Don't over-correct.** Pass: when the user types "remember that I'm vegetarian," it saves with the usual notice and no extra prompt.

## What we could not verify

- Any OpenAI statement, advisory or release note on this finding. Ars says OpenAI did not reply; our searches found none.
- The date version 1.2024.247 shipped. Rehberger says September 2024 and "last week" before September 20; no opened source gives a day.
- Whether the memory write from untrusted content still works today. No opened source gives a dated retest.
- The Ars detail that the SpAIware demo started from a web link hosting an image; Rehberger describes a document or website.
- The 102-year-old, Matrix and flat-Earth memories. Reported by Ars; not found in the text of Rehberger's post. We did not view his screenshots or videos.
- OpenAI's memory announcement and help pages, which Rehberger links. Not opened.
- Seen only in search summaries, not used: coverage by SC Media, ChannelE2E, Gigazine, Le Monde Informatique, Anvilogic and Adversa AI; a search summary saying a forum commenter claimed the issue did not apply to the web interface or API; and a Tenable advisory on a separate "Command Memories" injection via SearchGPT.
- Whether any real user was affected.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://embracethered.com/blog/posts/2024/chatgpt-hacking-memories/ | Embrace The Red (Johann Rehberger) | 2024-05-22 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://embracethered.com/blog/posts/2024/chatgpt-macos-app-persistent-data-exfiltration/ | Embrace The Red (Johann Rehberger) | 2024-09-20 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://web.archive.org/web/20241217211935/https://arstechnica.com/security/2024/09/false-memories-planted-in-chatgpt-give-hacker-persistent-exfiltration-channel/ | Ars Technica (Dan Goodin), Wayback Machine copy | 2024-09-24 | Yes, 2026-10-28, raw HTML of the archived copy read as text; quotes checked word for word. Live page refused download. |
| https://thehackernews.com/2024/09/chatgpt-macos-flaw-couldve-enabled-long.html | The Hacker News (Ravie Lakshmanan) | 2024-09-25 | Yes, 2026-10-28, raw HTML read as text |
| https://www.techradar.com/pro/hacker-creates-false-memories-in-chatgpt-to-steal-victim-data-but-it-might-not-be-as-bad-as-it-sounds | TechRadar Pro (Ellen Jennings-Trace) | 2024-09-26 | Yes, 2026-10-28, raw HTML read as text |

## Corrections

If you have OpenAI's own statement or release note, the ship date of version 1.2024.247, a dated retest of memory writes from untrusted content, or word on whether any real user was affected, tell us and we will fix this page.
