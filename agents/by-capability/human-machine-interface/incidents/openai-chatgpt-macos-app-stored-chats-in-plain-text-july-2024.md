---
title: "OpenAI's ChatGPT Mac App Stored Conversations in Plain Text Outside the macOS Sandbox (July 2024)"
date: 2024-07-03
source: "https://www.theverge.com/2024/7/3/24191636/openai-chatgpt-mac-app-conversations-plain-text"
description: "A developer showed the ChatGPT Mac app kept chats in plain text that any other app could read. After press questions, OpenAI shipped an encrypting update."
summary: "In early July 2024, developer Pedro José Pereira Vieito posted that OpenAI's ChatGPT app for macOS was not sandboxed and stored all conversations in plain text in an unprotected folder, so any other app, process or malware could read them without a permission prompt. He built a demo app that did this. He says OpenAI's bug bounty program first marked his report Not Applicable. On July 3, 2024, The Verge reported that after it contacted OpenAI, the company shipped a version that encrypts the chats. Pereira Vieito says the fixed version, 1.2024.171, keeps the key in the macOS Keychain, but the app is still not sandboxed. Status: Needs review."
categories:
  - Search and Chat Assistants
  - Security
patterns:
  - sensitive-data-collected-in-chat
  - always-listening-surprises
  - third-party-data-shared-by-users
---

# OpenAI's ChatGPT Mac app stored conversations in plain text outside the macOS sandbox (July 2024)

**This page is a dated teardown of one public finding, a chat app that saved users' conversations to disk where any other app could read them, for teams that ship a desktop or mobile chatbot that keeps chat history on the device.** The product was OpenAI's ChatGPT app for macOS, then recently launched. The user was Pedro José Pereira Vieito, a developer who wondered why the app had opted out of Apple's app sandbox. The moment was a look at the app's data folder: by his account, every conversation sat there as plain text, readable by any running app with no permission prompt.

**Status: Needs review.** Built from Pereira Vieito's own recap post on pvieito.com (July 2024), The Verge's story by Jay Peters (July 3, 2024), Computing's story by Dev Kundaliya (July 8, 2024), Bitdefender's blog post by Graham Cluley (July 8, 2024) and Moonlock's story by Ray Fernandez (July 12, 2024). All were downloaded on 2026-10-27 and read as text. Quotes and numbers were string-matched against those files. His Threads post loaded only as a script shell with no post text, so we did not read it directly. We did not test the ChatGPT app. Last updated 2026-10-27.

> **Read this first.** This page is a summary of public reporting, not a security audit of ChatGPT or its Mac app today. The finding is Pereira Vieito's, confirmed by The Verge's reporter on his own machine. We did not reproduce it and do not know how the app stores data now. This page makes no legal claim about OpenAI or Apple.

**Channel note.** Text chat only. The stored files were typed ChatGPT conversations in the desktop app. No source discusses voice chats. The checks below are written for text chats; voice checks are planned, not done.

**Why the slug says July 2024.** Pereira Vieito's posts and The Verge's story both came out in early July 2024. We date the page by The Verge's story, July 3, 2024, the first dated report we opened.

## How this differs from the closest pages

- [ChatGPT bug exposes other users' chat titles (March 2023)](openai-chatgpt-bug-exposes-other-users-chat-titles-march-2023.md) is a server bug that showed one user's data to another. Here nothing left OpenAI's servers by mistake. The weak point was the user's own Mac.
- [DeepSeek exposed database (January 2025)](deepseek-exposed-database-leaks-chat-history-and-api-keys-january-2025.md) is chat history left open on the internet. Here the history was open only to software already running on the same computer.
- [ChatGPT shared links indexed by search engines (July 2025)](chatgpt-shared-links-indexed-by-search-engines-july-2025.md) is about a share button. Here the user shared nothing; the app saved the chats on its own.

## What happened (as reported)

- **The finding.** Pereira Vieito writes that the app "is not sandboxed and stored all conversations in" plain text at `~/Library/Application Support/com.openai.chat/conversations-{uuid}`. Moonlock shows the same path in his embedded post.
- **Why it mattered on a Mac.** He writes that Apple began blocking access to private user data with macOS 10.14 Mojave, and that files in a sandboxed app's container are protected in macOS 14 Sonoma. By opting out of the sandbox, he says, the app was outside those defenses, so "any running app, process, or malware could read all your ChatGPT conversations without any permission prompt."
- **The demo.** He built a demo app, ChatGPTStealer, and posted its source code on GitHub. The Verge's reporter used it and says it read his own ChatGPT conversations "with the click of a button." The reporter says he could also find the files and see the text of conversations "just by changing the file name."
- **How he found it.** He told The Verge: "I was curious about why [OpenAI] opted out of using the app sandbox protections and ended up checking where they stored the app data."
- **Why the sandbox did not apply.** The Verge says OpenAI offered the Mac app only through its own website, so it did not have to follow the sandboxing rules for the Mac App Store.
- **The bug report.** Pereira Vieito says he first reported the issue through OpenAI's program on BugCrowd. He says it was marked "Not Applicable" because an attacker "would need physical access to the victim's device." He disagreed, so he posted the issue on Threads and Mastodon.
- **Press coverage.** He says The Verge, Ars Technica and 9to5Mac covered his posts. We opened only The Verge of those three.

## What OpenAI said and did

- **The statement.** OpenAI spokesperson Taya Christianson told The Verge: "We are aware of this issue and have shipped a new version of the application which encrypts these conversations." The Verge says the update came after it contacted OpenAI.
- **The fix, as tested by the press.** The Verge's reporter says that after the update, the demo app no longer worked for him and he could not see his conversations in plain text.
- **The fix, as described by the finder.** Pereira Vieito names the version as ChatGPT 1.2024.171 for Mac. He says chats move to a new folder, `conversations-v2-{uuid}`, are encrypted with a key named `com.openai.chat.conversations_v2_cache` stored in the macOS Keychain, and the old plain-text files are removed on upgrade.
- **What did not change.** He writes: "However, the app is still not sandboxed." Computing and Moonlock say the same.
- **The bug report.** No opened source has OpenAI's own comment on why the report was marked Not Applicable.

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| When the post went up | Moonlock says "On July 1"; the post it embeds is dated July 2, 2024. Pereira Vieito's recap says only that the posts came "during the past week." |
| When it was fixed | The Verge (July 3) says "Until Friday" the app had the issue, without a date. No opened source dates version 1.2024.171. |
| How serious | OpenAI's bug program, per Pereira Vieito, said an attacker needs physical access. He, Computing, Bitdefender and Moonlock say any running app or malware could read the files. |
| Who saw it | No opened source reports that anyone's chats were actually taken. |
| What users were told | No opened source quotes an in-app notice or release note about the change. Computing tells users to update. |

## Where in the conversation flow it broke (as reported)

1. **The user typed into the chat.** Conversations can hold personal, work or third-party details.
2. **The app saved the chat locally.** That is normal for a desktop app.
3. **The save skipped the operating system's protections.** No sandbox, no encryption, an unprotected folder.
4. **Any other app could read it.** No permission prompt, per Pereira Vieito's demo.
5. **The user was not told.** No opened source says the app showed where or how chats were stored.
6. **The first report was closed.** By his account, the bug program judged it Not Applicable. The fix came after press questions.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it.

- [Sensitive data collected in chat](../goals/channel-selection/failures/sensitive-data-collected-in-chat.md) (`sensitive-data-collected-in-chat`). **Partial fit.** That page is about a bot that asks for card numbers, SSNs or passwords, which then land in transcripts and logs that are not built to protect them. Here the stored transcript itself was readable by any app. Partial, because the app did not ask for the data; users typed it in.
- [Always-listening surprises](../goals/in-car-and-home-assistants/failures/always-listening-surprises.md) (`always-listening-surprises`). **Weak fit.** The assistant kept a history the user did not know was exposed. Weak, because that page is about voice devices in a home and what they heard.
- [Third-party data shared by users](../goals/privacy-and-governance/failures/third-party-data-shared-by-users.md) (`third-party-data-shared-by-users`). **Weak fit.** Chats can hold other people's details, and those were readable too. Weak, because no source shows such data in the files.
- **Considered and rejected.** [Privacy-rights requests not recognised](../goals/privacy-and-governance/failures/privacy-rights-requests-not-recognised.md): no user made a request in chat. [Copy, share, and export lose content](../goals/chat-interface/failures/copy-share-and-export-lose-content.md): no share or export was involved. `sensitive-category-inference`: the app guessed nothing about the user.
- **Possible gaps for a person to judge.** (1) No pattern covers chat history stored on a device without encryption or outside the system's app protections. (2) No pattern covers a vendor closing a privacy report as out of scope, then fixing it after press coverage. (3) No pattern covers a fix that leaves the root cause, here the sandbox opt-out, in place. (4) No pattern covers telling users where their chat history is kept. These are proposals, not decisions.

## What to measure

Proposed measures on a desktop build and its data folder. Status: Not yet run.

1. **Readable chat files.** After a test chat, count files in the app's data folders that contain the chat text in plain form.
2. **Cross-app access.** From a second, unprivileged test app, count chat files it can read without a permission prompt.
3. **Leftovers after upgrade.** After an upgrade, count old-format chat files that remain on disk.
4. **Report triage.** Count privacy reports closed as out of scope that are later fixed. The window is for the team to set.

## What a team could check

Proposed checks, each pass/fail on a product build or a text transcript. Status: Not yet run. Test accounts, prompts and the number of runs are for the team to set.

1. **No plain-text chat on disk.** Type a unique test phrase into a chat. Search the device for it. Pass: no file holds the phrase in plain text. Fail: any file does.
2. **Other apps are blocked.** Run a second test app with no special access and try to open the chat folder. Pass: access is denied or the system shows a permission prompt. Fail: it reads chat content silently.
3. **Key kept in the system store.** Pass: the decryption key is in the platform's secure key store, not in a file next to the chats. Fail: the key sits in the app's folder.
4. **Old files removed on upgrade.** Install the old build, chat, then upgrade. Pass: no plain-text chat files remain. Fail: any remain.
5. **Users can learn where chats live.** Input in chat: "Where are my conversations stored on this computer?" Pass: the reply or a help link says where history is stored and how to delete it. Fail: no answer or a wrong one.
6. **Delete removes the file.** Delete a test chat in the app. Pass: its content no longer appears in any file on disk. Fail: it does.

A voice version (spoken chats and any stored audio or transcripts) is planned, not run.

## What a team can change

Proposed changes. Status: proposed, not tested.

- **Use the platform's protections.** Store chat history inside the app's sandbox or a protected container, encrypted at rest.
- **Keep keys in the system key store.** Not in a file the same app writes.
- **Clean up on upgrade.** Remove old plain-text files when moving to encrypted storage.
- **Do not close local-access reports by default.** Malware on the same machine is a real reader, not only a person at the keyboard.
- **Tell users.** Say in plain words where history is kept and how to delete it.

## What is unverified

- **The Threads post.** We could not load its text. We rely on his recap post and on quotes in Computing, Bitdefender and Moonlock.
- **The BugCrowd ruling.** We have only Pereira Vieito's account of it.
- **The fix date and version.** Only Pereira Vieito names version 1.2024.171. No opened source dates it.
- **Today's app.** No opened source reports a test after July 2024.
- **Seen only in search summaries, not used:** Ars Technica, 9to5Mac, Tom's Guide, heise, iMore, Macworld, gHacks, ForkLog, Lowyat, ProPakistani, mezha.media, mysmartprice, Cybersecurity News, AI Weekly, OECD.AI's incident entry and the AI Incident Database (downloaded, not read). Engadget and AppleInsider links we guessed returned 404.

## Related incidents

- [ChatGPT bug exposes other users' chat titles (March 2023)](openai-chatgpt-bug-exposes-other-users-chat-titles-march-2023.md): another OpenAI flaw that exposed chat history.
- [DeepSeek exposed database (January 2025)](deepseek-exposed-database-leaks-chat-history-and-api-keys-january-2025.md): chat history left unprotected, on a server.
- [ChatGPT shared links indexed by search engines (July 2025)](chatgpt-shared-links-indexed-by-search-engines-july-2025.md): private-feeling chats made readable by others.
- [Samsung employees paste source code into ChatGPT (April 2023)](samsung-employees-paste-source-code-and-meeting-notes-into-chatgpt-april-2023.md): why stored chats can hold sensitive work data.

## Sources

| Source | Author | Date | URL | Opened? date, how |
|---|---|---|---|---|
| PVIEITO, "ChatGPT for Mac Was Storing All Conversations in an Unprotected Location" | Pedro José Pereira Vieito | July 2024 (no day shown) | https://pvieito.com/2024/07/chatgpt-unprotected-conversations | Yes, 2026-10-27, HTML read as text; quotes, paths and version checked |
| The Verge, "OpenAI's ChatGPT Mac app was storing conversations in plain text" | Jay Peters | 2024-07-03 | https://www.theverge.com/2024/7/3/24191636/openai-chatgpt-mac-app-conversations-plain-text | Yes, 2026-10-27, HTML read as text; quotes checked |
| Computing, "ChatGPT's Mac app exposed user conversations" | Dev Kundaliya | 2024-07-08 | https://www.computing.co.uk/news/4332673/chatgpts-mac-app-exposed-user-conversations | Yes, 2026-10-27, HTML read as text; used to confirm quotes |
| Bitdefender, "ChatGPT for Mac app flaw left users' chat history exposed" | Graham Cluley | 2024-07-08 | https://www.bitdefender.com/en-us/blog/hotforsecurity/chatgpt-mac-app-flaw-left-users-history-exposed | Yes, 2026-10-27, HTML read as text; used to confirm quotes |
| Moonlock, "ChatGPT for macOS let malware potentially access your chats" | Ray Fernandez | 2024-07-12 | https://moonlock.com/chatgpt-macos-chats | Yes, 2026-10-27, HTML read as text; dates of the post checked |
| Pereira Vieito on Threads | Pedro José Pereira Vieito | July 2024 | https://www.threads.net/@pvieito/post/C85NVV6hvF6 | No, page loaded without post text |

## Corrections

This page needs review. If you have the original Threads or Mastodon posts, OpenAI's release notes for version 1.2024.171, or a later test of how the app stores chats, tell us and we will update this page.
