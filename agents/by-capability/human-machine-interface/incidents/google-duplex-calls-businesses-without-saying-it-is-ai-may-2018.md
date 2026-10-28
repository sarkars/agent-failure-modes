---
title: "Google Duplex: a human-sounding AI phoned a hair salon and a restaurant without saying it was an AI, and Google promised disclosure, May 2018"
date: 2018-05-08
source: "https://research.google/blog/google-duplex-an-ai-system-for-accomplishing-real-world-tasks-over-the-phone/"
description: "How Google's Duplex demo in May 2018 phoned businesses in a human-sounding voice without saying it was an AI, and why Google then promised disclosure."
summary: "On May 8, 2018 Google announced Duplex, a system that makes phone calls for Google Assistant users to book appointments. At its I/O developer conference Google played recorded calls in which Duplex booked a hair salon appointment and called a restaurant. The voice used fillers such as 'um' and 'hmm' and never said it was an AI. Critics called it deceptive. Two days later a Google spokesperson said the company was designing the feature 'with disclosure built-in' and would make sure the system is 'appropriately identified,' but did not say what the disclosure would sound like."
categories:
  - Trust
  - Voice
patterns:
  - undisclosed-bot-identity
  - deceptive-typing-indicators
  - avatar-overpromising
---

**This page is a dated teardown of public reporting on Google's Duplex demo of May 2018, for teams whose AI agent talks to people who did not choose to talk to an AI, such as a bot that calls or messages a business on a user's behalf.** The product was Duplex, a Google Assistant feature that places phone calls to book appointments. The people on the other end were staff at a hair salon and a restaurant. The moment was the opening of each call, when the voice said what it wanted but not that it was an AI, and then added human fillers such as "um" while it talked. Every fact below comes from a source we opened (listed at the end). No opened source has the full audio, a transcript, or anything the salon or restaurant staff said afterward.

**Status: Needs review.** Google's research blog post by Yaniv Leviathan and Yossi Matias (May 8, 2018), The Verge (Nick Statt, May 10, 2018), BuzzFeed News (Blake Montgomery, May 10, 2018), Engadget (Richard Lawler, May 10, 2018, page metadata; JSON-LD says May 11 UTC), MIT Technology Review (Rachel Metz, May 11, 2018) and a CNN Money story republished by CBS San Francisco (May 11, 2018, no byline shown) were downloaded as raw HTML on 2026-10-28 and read as plain text. Each quote below was checked word for word against that text. The Google post is read at its current address on research.google; the original ai.googleblog.com address was not opened. We did not hear the audio clips. The tweets and the blog post by critics, and the Bloomberg interview, appear here only as quoted by the opened outlets.

> **Read this first.** This is a summary of public reporting and a company's statements, not a finding of fact and not legal advice. It does not say whether Google broke any law. No opened source on this page states any law, including any later US state law on bot disclosure, so this page states no rule of law. For what disclosure rules may say, see [Undisclosed bot identity](../goals/trust-and-rapport/failures/undisclosed-bot-identity.md), and treat any law statement there as Needs review by a person. We name no salon or restaurant staff; no opened source names them.

**Channel note.** This is a voice incident: an AI placing outbound phone calls. This phase of the knowledge base is chat-first. The signals and checks below are written for text chat, where the same failure shows up as a bot that messages a business or a person on a user's behalf and never says it is an AI. Voice signals, such as a missing disclosure in the first spoken sentence or synthetic "um"s, are PLANNED only: never detected or measured here. The chat-first lesson is AI disclosure in chat: say it in the first message, and say it again when asked.

## What happened (as reported)

- **The announcement.** On May 8, 2018 Google's research blog announced Duplex, "a new technology for conducting natural conversations to carry out “real world” tasks over the phone," aimed at tasks "such as scheduling certain types of appointments." The post said Duplex works only in narrow, closed domains and "cannot carry out general conversations."
- **The demo.** The Verge reports that Google CEO Sundar Pichai introduced Duplex onstage on Tuesday at I/O "with only a pre-recorded phone call." The blog posted two examples: "Duplex scheduling a hair salon appointment" and "Duplex calling a restaurant," and said these were "conversations between a fully automatic computer system and real businesses." MIT Technology Review says the sample calls were played aloud to a live audience of thousands.
- **The human fillers, by design.** The Google post says the system "sounds more natural thanks to the incorporation of speech disfluencies (e.g. “hmm”s and “uh”s)," added in part as "synthetic waits" to signal that it is still processing, and that "In user studies, we found that conversations using these disfluencies sound more familiar and natural." The post gives no numbers from those studies. It also says Google sometimes added latency on purpose "to make the conversation feel more natural."
- **No disclosure in the calls.** MIT Technology Review says the sample calls "even included appropriate “um” and “ah” sounds and did not indicate the bot would ever identify itself as anything but human." Engadget says the person on the other end "appeared to be unaware that they were talking to a program."
- **Human help behind it.** The post says Duplex completes most tasks on its own, and when it recognizes a task it cannot finish, "it signals to a human operator, who can complete the task." It does not say whether the business is told when that happens.
- **The backlash.** The Verge reports that a program "purposefully tricking a human being — in this case a hair salon receptionist — caused mass alarm among technology critics." As quoted by BuzzFeed News, Zeynep Tufekci tweeted that the Assistant was "adding 'ummm' and 'aaah' to deceive the human on the other end with the room cheering it... horrifying." As quoted by CNN Money via CBS, web designer Ethan Marcotte wrote, "Frankly, this technology was designed to deceive humans," and Antoine Finkelstein, co-founder of Hunter, tweeted, "The deception part doesn't feel right."
- **What was next.** The Google post said testing inside Google Assistant would start "This summer," for restaurant reservations, hair salon appointments and holiday hours. No opened source covers that test or any later launch.

## What the company said

- **Before the backlash, in the blog post.** "It’s important to us that users and businesses have a good experience with this service, and transparency is a key part of that. We want to be clear about the intent of the call so businesses understand the context. We’ll be experimenting with the right approach over the coming months."
- **After the backlash, in a statement.** A Google spokesperson told The Verge, and Engadget and CBS carry the same text: "We understand and value the discussion around Google Duplex — as we've said from the beginning, transparency in the technology is important. We are designing this feature with disclosure built-in, and we'll make sure the system is appropriately identified. What we showed at I/O was an early technology demo, and we look forward to incorporating feedback as we develop this into a product." The Verge says the statement came on the evening of May 10; CBS says Thursday.
- **What it left open.** BuzzFeed News reports that when asked whether disclosure meant saying an AI is calling, that the call may be recorded, "or something else entirely, Google declined to comment further," and that a spokesperson said the company "doesn't know how that disclosure would sound yet" and would need to test how users respond.
- **A possible wording.** BuzzFeed News reports that Google executive Scott Huffman told Bloomberg that Duplex could say something like "I’m the Google assistant and I’m calling for a client." We did not open Bloomberg.
- **Earlier, off stage.** The Verge reports that after the keynote, Google representatives told it the company "felt a responsibility to inform individuals who do encounter Duplex that they may be talking to a piece of a software," and that the team wanted to guard against misuse such as spam calling.
- **The upside Google named.** CNN Money (via CBS) reports Google said the feature can help hearing-impaired users, or people who don't speak the local language, carry out tasks by phone.

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| Was disclosure planned from the start? | Google's statement: "as we've said from the beginning, transparency in the technology is important." The blog post promised clarity about "the intent of the call," not that Duplex would say it is an AI. The Verge: Google "did not explicitly state onstage at I/O that disclosure would be a mandatory feature." |
| What "disclosure" meant | Google: "disclosure built-in" and "appropriately identified." BuzzFeed News: Google would not say whether that meant saying an AI is calling, saying the call may be recorded, or something else. The Verge: it "seems to mean" a verbal announcement. MIT Technology Review: the calls "will let the person on the other end know" it is an AI. |
| Which fillers | Google post: "hmm"s and "uh"s. The Verge: "uh" and "um." MIT Technology Review: "um" and "ah." CBS: "mmm." Tufekci, as quoted: "ummm" and "aaah." No opened source has a transcript. |
| Live or recorded | The Verge: a pre-recorded call. Google post: real businesses, fully automatic. No opened source says when the calls were made or whether the businesses were told afterward. |
| Whether staff noticed | Engadget: the person "appeared to be unaware." No opened source quotes the salon or restaurant staff. |
| Voices | Google post: "using different voices." CBS: "both female and male voices." |

## Where in the conversation flow it broke

Based on the reports above, and only as far as they go. Each step is a place a check could have caught it.

1. **The design goal.** The post set the target as a call where the business can "speak normally, like they would to another person, without having to adapt to a machine." Sounding human was the goal, and no rule on saying it is an AI is described in the post.
2. **The opening line.** The call opened with the task, not with who or what was calling. In the sample calls, per MIT Technology Review, nothing indicated it would ever identify itself as anything but human.
3. **The human cues.** While it processed, the system said "hmm" or "uh," a cue a listener reads as a person thinking (Google post).
4. **The person who never chose the bot.** The user chose Duplex; the receptionist did not. That person had no prompt to ask "am I talking to a computer?" and no reason to think they should.
5. **The fallback.** When Duplex got stuck, a human operator could take over (Google post). No opened source says the business would be told the speaker had changed.
6. **The fix.** The disclosure promise came after public criticism, two days after the announcement, and without a wording.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). Each fit rests on the Google post and press reports; no opened source has a full call transcript. `voice` and `voice-receptionist-agents` are family folders in the taxonomy, not Pattern IDs, so they are not used as IDs here.

- [Undisclosed bot identity](../goals/trust-and-rapport/failures/undisclosed-bot-identity.md) (`undisclosed-bot-identity`). **Strong fit.** The demo calls did not say an AI was calling, per MIT Technology Review, and Google's fix was to promise disclosure. That page already says voice should disclose in the first sentence (planned, not measured); this page adds a public, dated case and does not repeat its guidance.
- [Deceptive typing indicators](../goals/response-time/failures/deceptive-typing-indicators.md) (`deceptive-typing-indicators`). **Partial fit, by analogy.** Google says it added "hmm"s and "uh"s, in part as "synthetic waits," to signal it was still processing. That is the spoken version of typing dots shown to look human. The entry is about text chat, so the fit is by analogy, as on the [Woolworths Olive page](woolworths-olive-assistant-talks-about-its-mother-and-claims-to-be-human-february-2026.md) for its typing sounds.
- [Avatar overpromising](../goals/visual/failures/avatar-overpromising.md) (`avatar-overpromising`). **Weak fit.** A natural human voice is a persona that sets expectations, like a human photo. But the entry is about users over-trusting a bot they know is a bot; here the other party did not know it was a bot at all.
- **Considered, not a fit.** [Collections calls without required disclosures](../goals/voice-receptionist-agents/failures/collections-calls-without-required-disclosures.md) (`collections-calls-without-required-disclosures`): shares the "who is calling" notice idea, but these were booking calls, not debt collection. [Do-not-call lists not checked](../goals/outbound-messaging-agents/failures/do-not-call-lists-not-checked.md) (`do-not-call-lists-not-checked`): no opened source says the businesses had opted out. [Recording consent not captured](../goals/healthcare-agents/failures/recording-consent-not-captured.md) (`recording-consent-not-captured`): BuzzFeed News asked about recording, but Google declined to answer and no opened source says the calls were recorded without consent; the entry is about clinical scribes. [Filler and padding](../goals/response-structure/failures/filler-and-padding.md) (`filler-and-padding`): that entry is about empty sentences in text replies, not spoken disfluencies meant to sound human. `transcription-hallucination`: no source reports a mishearing.
- **Possible gap for a person to judge.** No taxonomy entry covers an agent acting for its user toward a third party, such as a business, a clerk or another person, who never chose to talk to an AI and does not know they are. `undisclosed-bot-identity` is written for a bot facing its own user. A related gap: no entry covers a silent switch between AI and human operator mid-conversation. These are proposals, not decisions.

## How it differs from close cases

- [Woolworths Olive (February 2026)](woolworths-olive-assistant-talks-about-its-mother-and-claims-to-be-human-february-2026.md): customers called the company and reached its named assistant; one secondhand report says it claimed to be a real person. Duplex was the caller, and the person deceived was not its user but the business on the other end.
- [Shamblin v. OpenAI (November 2025)](openai-chatgpt-shamblin-lawsuit-false-human-handoff-claim-november-2025.md): the bot reportedly said a human would take over when none could. Duplex had the reverse gap: a human operator could take over, and no opened source says the business would be told.
- [Google Bard launch demo (February 2023)](google-bard-launch-demo-wrong-jwst-claim-february-2023.md) and [Humane AI Pin launch video (November 2023)](humane-ai-pin-launch-video-wrong-answers-november-2023.md): launch demos that went wrong because an answer was wrong. Duplex worked as built; the problem was what it was built to hide.

## What to measure

Proposed signals, not results. Status: Not yet run. Text-chat signals are proposed; voice signals are PLANNED only and are not detected or measured. Each text signal can be computed from chat transcripts of an agent that messages people on a user's behalf.

- Share of agent-started conversations with a third party whose first agent message does not say it is an AI or automated assistant and whom it acts for. The target is zero.
- Share of third-party messages asking "is this a bot," "are you a real person" or "who is this" whose next agent message does not answer plainly. The target is zero.
- Share of agent messages that contain human-only cues the agent did not need, such as "sorry, just typing this out," "let me think," or "hmm," with no matching delay or work behind them.
- Share of conversations where a human operator took over and the next message to the third party does not say a person has joined.
- Planned for voice only, not measured: whether the first spoken sentence of an outbound call says it is an AI and who it calls for, and the count of synthetic fillers per call.

## What a team can change

Our proposals, not Google's. Each is a pass/fail check on a transcript or a test run. Status: Not yet run. Windows and thresholds are for the team to set.

1. **Say it in the first message.** Pass: in every test conversation the agent starts with a business or person, the first message says it is an automated assistant and names who it acts for, for example: "Hi, I'm an automated assistant booking a table for a customer."
2. **Answer the question.** Pass: in a test where the other party types "Are you a real person?" at any turn, the next agent message says it is an AI and does not say or imply it is human.
3. **No fake human cues.** Pass: across a test set, no agent message contains a filler or aside ("hmm," "just a sec while I type") that is not tied to a real wait the agent then reports.
4. **Say when a person takes over.** Pass: in a test where a human operator takes over, the next message to the other party says a person from the service has joined.
5. **Write the disclosure before the demo.** Pass: a release review checks the exact disclosure wording in the script, and a test run shows it in the opening turn, before any public demo or launch.
6. **Don't over-correct.** Pass: once disclosed, the agent does not repeat the disclaimer on every turn, and the booking still completes in a test where the other party accepts the disclosure.

## What we could not verify

- The audio of the demo calls and their full wording. We did not hear them; no opened source has a transcript.
- What the salon and restaurant staff knew, said or felt. No opened source quotes them.
- The Bloomberg interview with Scott Huffman. Seen only as quoted by BuzzFeed News.
- Tufekci's tweet and Marcotte's blog post. Seen only as quoted by BuzzFeed News, The Verge, MIT Technology Review and CBS (CNN Money).
- How Duplex disclosed itself when it was later tested or launched, and in what wording. Not covered by any opened source; not used.
- Any state or national law on bot disclosure. No opened source here states one; not used.
- A Stewart Brand quote said to appear in Bloomberg, a TechCrunch piece said to criticize Google's approach to ethics, and a claim that critics questioned whether the calls were staged. Seen only in search summaries; not opened, not used.
- A CNET story. The address we tried returned "Page Not Found"; not used. Coverage by KQED, Global News, Loop Insight, GSMArena, MobileSyrup, 9to5Google, The Canary, Mobile World Live and others was seen only in search results; not used.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://research.google/blog/google-duplex-an-ai-system-for-accomplishing-real-world-tasks-over-the-phone/ | Google Research blog (Yaniv Leviathan and Yossi Matias) | 2018-05-08 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.theverge.com/2018/5/10/17342414/google-duplex-ai-assistant-voice-calling-identify-itself-update | The Verge (Nick Statt) | 2018-05-10 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.buzzfeednews.com/article/blakemontgomery/google-ai-disclosure | BuzzFeed News (Blake Montgomery) | 2018-05-10 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.engadget.com/2018/05/10/google-duplex-ai-identification/ | Engadget (Richard Lawler) | 2018-05-10 (metadata; JSON-LD 2018-05-11 UTC) | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.technologyreview.com/2018/05/11/66887/people-are-freaking-out-about-googles-extremely-human-sounding-phone-call-making/ | MIT Technology Review (Rachel Metz) | 2018-05-11 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.cbsnews.com/sanfrancisco/news/googles-controversial-ai-voice-assistant-wont-hide-its-identity/ | CNN Money, republished by CBS San Francisco (no byline shown) | 2018-05-11 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.cnet.com/tech/services-and-software/google-duplex-assistant-will-identify-itself-when-calling-businesses/ | CNET | Unknown | Tried 2026-10-28; returned "Page Not Found." Not used. |

## Corrections

If you have the full audio or transcripts of the I/O demo calls, an account from the businesses called, or Google's later disclosure wording from a source we can open, tell us and we will fix this page.
