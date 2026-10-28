---
title: "OpenAI custom GPTs: plain chat requests made many reveal their builders' instructions and hand over uploaded knowledge files, November 2023"
date: 2023-11-29
source: "https://www.wired.com/story/openai-custom-chatbots-gpts-prompt-injection-attacks/"
description: "How plain chat requests made many of OpenAI's new custom GPTs reveal their builders' private instructions and let users download uploaded knowledge files."
summary: "OpenAI launched custom GPTs on November 6, 2023, letting anyone build a version of ChatGPT with their own instructions and uploaded files. On November 15, 2023, Adversa AI posted methods for getting GPTs to reveal their instructions, connected APIs and knowledge files. On November 20, 2023, Northwestern University researchers posted an arXiv paper testing 216 custom GPTs: their simple prompts extracted the system prompt from 97.2% and leaked files from every tested GPT that had files (24 of 24). WIRED (Matt Burgess, November 29, 2023) reported both, and OpenAI told WIRED it is working to make its products more robust against prompt injections. The researchers say some routes got harder over time. No opened source reports a full fix."
categories:
  - Security
  - Privacy
patterns:
  - refusals-that-reveal-internal-rules
  - third-party-data-shared-by-users
---

**This page is a dated teardown of public research and reporting on OpenAI's custom GPTs giving up their private instructions and uploaded files, for teams that build a chat assistant on top of a hosted model with a hidden prompt and a set of knowledge files.** The product was OpenAI's custom GPTs, launched in November 2023. The user was anyone chatting with a public GPT. The moment was a plain request in the chat box to repeat the bot's first instructions or to list and hand over its files. Every fact below comes from a source we opened (listed at the end). The tests were run by researchers and reporters; no opened source names a builder who was harmed.

**Status: Needs review.** WIRED's article, the Northwestern paper (arXiv abstract page and HTML full text, version 2), Adversa AI's blog post, OpenAI's "Introducing GPTs" post, Decrypt and InfoQ were downloaded as raw HTML on 2026-10-28 and read as plain text. Each quote below was checked word for word against that text. Tech Xplore refused our download (HTTP 403) and is not used.

> **Read this first.** This is a summary of public research and reporting, not a finding of fact, and not legal or security advice. It does not say whether any company broke any law or contract. We describe the attacks at a high level only. We reproduce no extracted prompts, no extracted files, no attack prompts and no credentials, and we do not name the third-party GPTs the researchers probed. Have a qualified security engineer review your own assistant.

**Channel note.** Text chat. Users typed requests into a custom GPT inside ChatGPT, and the GPT answered in text or offered a file download link. This phase of the knowledge base is chat-first: the text-chat signals and checks below are proposed; voice is planned and not covered here.

## What happened (as reported)

- **The launch.** OpenAI's post "Introducing GPTs" is dated November 6, 2023. It says anyone can build a custom version of ChatGPT by "giving it instructions and extra knowledge" and picking tools such as web search, image making or data analysis, with no coding. It says builders can share GPTs publicly, and that a GPT Store with verified builders would roll out later that month.
- **What OpenAI promised on privacy.** The same post says: "Your chats with GPTs are not shared with builders." It names usage-policy review, builder identity checks and a report button. We found no line in it about whether a GPT's instructions or files are kept from users.
- **What builders put in.** WIRED says a builder gives the GPT instructions on what it should or should not do and can upload documents to give it more expertise. Per WIRED, Northwestern researcher Jiahao Yu said GPT data often holds the designer's "domain-specific insights," and he cited examples of "salary and job descriptions" uploaded alongside other confidential data.
- **Adversa AI (November 15, 2023).** Adversa AI's post describes a chain of chat requests against custom GPTs. Per the post, a short request got a close copy of a GPT's instructions; another listed the outside APIs it was connected to and whether browsing or image tools were on; another listed the names of its knowledge files. The post then describes ways to get a download link for those files. It says: "Some first publicly known methods appeared on 9th November but were quickly fixed." It describes newer routes that still worked for it, including one using Linux commands. It says it took all the information from a number of top GPTs, and it warns that a whole GPT could be copied.
- **The Northwestern study (posted November 20, 2023).** "Assessing Prompt Injection Risks in 200+ Custom GPTs," by Jiahao Yu, Yuhang Wu, Dong Shu, Mingyu Jin, Sabrina Yang and Xinyu Xing, was first posted to arXiv on November 20, 2023, and revised on May 25, 2024. The abstract page says it was accepted at an ICLR 2024 workshop.
  - **What they tested.** Per the paper, 16 custom GPTs made by OpenAI and 200 third-party GPTs sampled from an online GPT list, 216 in all. Each attack got up to three tries.
  - **Results.** Per the paper's Table 1, system prompts came out of 210 of 216 GPTs: 120 of 120 with the code interpreter on, and 90 of 96 without it. Files leaked from all 24 GPTs that had files (14 with the code interpreter, 10 without). The paper calls these "alarming success rates" for simple prompts: 97.2% for system prompts and 100% for files.
  - **"Do not share" did not hold.** The paper says some extracted prompts or files said not to share them, yet the attacks still worked. It concludes that "the current defensive prompts are not robust enough."
  - **Experts against a defense.** In a second test, four experts each had 10 tries against a GPT with a chosen defensive prompt. With the code interpreter on, all four got the system prompt and the file. With it off, three of the four failed to get the system prompt, and the one who did needed nine tries; all four still got the file.
  - **Disclosure.** The paper says the team reported its findings to OpenAI before release. It says that at the time of writing, OpenAI had tried to fix a related route, so direct queries to the API could no longer see uploaded file names and plugin schema details.
- **WIRED (November 29, 2023).** WIRED's "OpenAI's Custom Chatbots Are Leaking Their Secrets," by Matt Burgess, reports that researchers and technologists made custom GPTs spill their initial instructions and downloaded the files used to build them. Yu told WIRED it was "surprisingly straightforward." WIRED says one GitHub page lists around 100 sets of leaked GPT instructions, and that at least one developer has taken down the data they uploaded. Adversa AI CEO Alex Polyakov told WIRED that in some cases simply asking for the instructions or the knowledge-base file list was enough.
- **Later coverage.** Decrypt (Jose Antonio Lanz, December 12, 2023) wrote that it got the full prompt and confidential data of a public custom GPT by asking for its initial prompt. InfoQ (Andrew Hoblitzell, January 14, 2024) summarized the Northwestern and Adversa work as the GPT Store rolled out.

## What OpenAI said

- **To WIRED.** After publication, OpenAI spokesperson Niko Felix told WIRED the company takes the privacy of user data "very seriously." He said OpenAI is working to make its models and products "safer and more robust against adversarial attacks, including prompt injections." WIRED added the comment in an update at 12:20 pm ET on November 29, 2023.
- **What changed, as others report it.** WIRED says the researchers found some information got harder to extract over time, a sign OpenAI had blocked some prompt injections. Polyakov told WIRED his newest methods used Linux commands, which take more skill than plain English. InfoQ writes that OpenAI said it had patched the flaws Adversa reported; we did not find that OpenAI statement in a source we opened.
- **What we did not find.** No opened source has an OpenAI advisory, a dated fix, a statement that GPT instructions or knowledge files are meant to be secret, or a notice to builders.

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| "100 percent for file leakage" | WIRED quotes Yu on 100 percent for files and 97 percent for prompts. The paper's Table 1 shows the file figure covers 24 GPTs that had files, not all 216. |
| How many GPTs | The paper's title and WIRED say more than 200. The paper's tables count 216 (16 by OpenAI, 200 third-party). |
| Whether it was fixed | Adversa: some early download methods were "quickly fixed," others still worked on November 15. Paper: OpenAI tried to close the API route. WIRED: some routes got harder. InfoQ: OpenAI said it patched Adversa's findings. None gives a date or says all routes closed. |
| Who was at risk | OpenAI's post speaks to users' chats not reaching builders. The leaks ran the other way: builders' instructions and files reached users. |

## Where in the conversation flow it broke

Based on the reporting, and only as far as it goes:

1. **The build.** A builder typed private instructions and uploaded files, and per Yu some did not know users could pull those files out.
2. **The ask.** A user typed a plain request to see the bot's instructions or its list of files. Per Polyakov and Adversa, no special skill was needed in many cases.
3. **The rule in the prompt.** Some builders had told the GPT not to share. Per the paper, the GPT shared anyway; a sentence in the prompt was the only lock.
4. **The answer.** The GPT recited its instructions, listed file names, or gave a download link. The builder got no sign it had happened.
5. **The copy.** Per Adversa and the paper, the instructions, API list and files together were enough to clone a GPT.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). No pattern in this taxonomy covers a hosted assistant that hands its hidden prompt and knowledge files to any user who asks, so no fit is strong.

- [Refusals that reveal internal rules](../goals/refusals-and-boundaries/failures/refusals-that-reveal-internal-rules.md) (`refusals-that-reveal-internal-rules`). **Partial fit.** That page is about a refusal that quotes the system prompt, and its notice assumes "your prompt can leak anyway." Here the GPTs did not even refuse: they recited the prompt when asked. The page's lesson carries over: write the prompt as if users will read it, and keep real secrets out of it.
- [Third-party data shared by users](../goals/privacy-and-governance/failures/third-party-data-shared-by-users.md) (`third-party-data-shared-by-users`). **Weak fit.** Per WIRED, builders uploaded files such as salary and job descriptions, which may hold other people's details. That page is about an end user pasting someone's data into a chat; here the builder uploaded it and a stranger pulled it out.
- **Considered, not a fit.** [Sensitive data collected in chat](../goals/channel-selection/failures/sensitive-data-collected-in-chat.md) (`sensitive-data-collected-in-chat`): the bots did not ask users for data; the data flowed out to users. [Conflicting inputs resolved silently](../goals/multimodal-input/failures/conflicting-inputs-resolved-silently.md) (`conflicting-inputs-resolved-silently`): the builder's "do not share" rule and the user's request did clash, but that page is about a user's text against the user's own attachment. [Prompt edits by non-engineers break other behavior](../goals/model-and-prompt-changes/failures/prompt-edits-by-non-engineers-break-other-behavior.md) (`prompt-edits-by-non-engineers-break-other-behavior`): no prompt edit broke anything here. `silent-attachment-failures`: files were read as built; the harm was handing them over. `undisclosed-bot-identity`: users knew they were talking to a GPT.
- **Possible gap for a person to judge.** The cross-cutting security library has [direct prompt injection](../../../cross-cutting/security/goals/security-autonomy/failures/direct-prompt-injection.md) and [context injection leakage](../../../cross-cutting/security/goals/data-loss-prevention/failures/context-injection-leakage.md), both outside this taxonomy. This case adds one interface-side detail: when a builder's only guard is a sentence in the prompt, the chat box itself is the download button. This is a proposal, not a decision.

## How it differs from close cases

- [Amazon Q Business (December 2023)](amazon-q-business-chatbot-hallucinations-and-confidential-data-leaks-december-2023.md): days later, leaked internal documents said a new work assistant was leaking confidential data, which Amazon disputed. That was an internal report about one product; here outside researchers measured the leak across hundreds of bots.
- [Optum SOP Chatbot (December 2024)](optum-internal-ai-sop-chatbot-exposed-to-internet-december-2024.md): an internal bot cited documents behind a login to anyone who reached it. Here the bots were meant to be public; what leaked was the builder's setup and files.
- [ChatGPT Connectors AgentFlayer (August 2025)](openai-chatgpt-connectors-agentflayer-poisoned-document-data-leak-august-2025.md): a hidden instruction in a document steered ChatGPT into leaking a user's keys. Here no planted document was needed; the user asked and the bot answered.
- [Discord Clyde grandma exploit (2023)](discord-clyde-chatbot-grandma-exploit-role-play-jailbreak-and-shutdown-2023.md): role-play got a chatbot past its content rules. Here the target was the bot's own setup, not banned content.

## What to measure

Proposed signals, not results. Status: Not yet run. Text-chat signals are proposed; voice signals are planned only.

- Share of replies that contain a run of words matching the system prompt above a set length.
- Count of replies that list knowledge-file names, or that offer a link to download a knowledge file, per 1,000 chats.
- Share of red-team requests for "your instructions" or "your files" that get the content, split by whether the code interpreter or another code tool is on.
- Count of uploaded knowledge files that hold names, salaries, emails or keys, found by a scan at upload time.
- Share of builders who, when asked at setup, say they expect users can see their instructions and files.

## What a team can change

Our proposals, not OpenAI's or the researchers'. Each is a pass/fail check on a transcript, a test run or a config review. Status: Not yet run. Thresholds and what counts as secret are for the team to set.

1. **Assume the prompt is public.** Pass: a config review finds no keys, passwords, internal URLs, prices meant to stay private or people's details in the system prompt.
2. **Files are for answers, not downloads.** Pass: a test request to download, export or convert a knowledge file gets no file and no link, with the code tool on and off.
3. **Don't list the shelf.** Pass: a test request for the names of knowledge files gets no file names.
4. **No recital.** Pass: a test request to repeat the first instructions gets a short decline, and an output check blocks any reply that matches a long run of the prompt.
5. **Scan before upload.** Pass: uploading a test file with a fake salary table or a fake key shows the builder a warning before the file is saved.
6. **Tell builders the truth.** Pass: the setup screen states, before the first upload, that users may be able to see instructions and files.
7. **Don't over-correct.** Pass: a user who asks "what can you help me with?" gets a plain summary of what the bot does, not a refusal.

## What we could not verify

- Any OpenAI advisory, release note or dated fix. InfoQ says OpenAI said it patched Adversa's findings; we did not find that statement in a source we opened.
- Whether the routes still work today. No opened source gives a dated retest.
- Whether any builder lost money or users from a leak. WIRED says one developer took down uploaded data; no source says why or what was in it.
- The GitHub page of around 100 leaked instruction sets that WIRED cites. Not opened, and we would not reproduce it.
- The posts on X that Adversa cites for the November 9 download methods. Not opened.
- The GPT Store's actual launch date. OpenAI's November 6 post said later that month; InfoQ (January 14, 2024) says it had started rolling out. We did not open an OpenAI source with the date.
- Seen only in search summaries, not used: Tech Xplore's write-up of the Northwestern study (download refused, HTTP 403), Gizmodo, Baldur Bjarnason's notes, AIPressRoom, Adversa's "Towards Secure AI Week 48" roundup, a Decrypt piece on jailbreaks at OpenAI and Amazon, a promptfoo vulnerability database entry and a Natural News item.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://openai.com/index/introducing-gpts/ | OpenAI | 2023-11-06 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://adversa.ai/blog/llm-red-teaming-gpts-prompt-leakage-api-leakage-documents-leakage/ | Adversa AI | 2023-11-15 | Yes, 2026-10-28, raw HTML read as text; quote checked word for word |
| https://arxiv.org/abs/2311.11538 | arXiv (Jiahao Yu, Yuhang Wu, Dong Shu, Mingyu Jin, Sabrina Yang, Xinyu Xing; Northwestern University) | v1 2023-11-20; v2 2024-05-25 | Yes, 2026-10-28, abstract page raw HTML read as text |
| https://arxiv.org/html/2311.11538v2 | arXiv, same paper, HTML full text (version 2) | 2024-05-25 | Yes, 2026-10-28, raw HTML read as text; numbers and quotes checked word for word |
| https://www.wired.com/story/openai-custom-chatbots-gpts-prompt-injection-attacks/ | WIRED (Matt Burgess) | 2023-11-29, updated same day | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://decrypt.co/209353/your-custom-gpt-could-be-tricked-into-giving-up-your-data | Decrypt (Jose Antonio Lanz) | 2023-12-12 | Yes, 2026-10-28, raw HTML read as text |
| https://www.infoq.com/news/2024/01/gpts-may-leak-sensitive-info/ | InfoQ (Andrew Hoblitzell) | 2024-01-14 | Yes, 2026-10-28, raw HTML read as text |

## Corrections

If you have OpenAI's own advisory or fix date, a dated retest of these routes, or a report from a builder whose GPT was copied, tell us and we will fix this page.
