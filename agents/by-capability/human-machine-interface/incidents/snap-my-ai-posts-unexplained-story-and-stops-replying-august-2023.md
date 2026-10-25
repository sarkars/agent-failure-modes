---
title: "Snapchat's My AI Posts an Unexplained One-Second Story and Stops Replying, August 2023"
date: 2023-08-15
source: "https://techcrunch.com/2023/08/16/snapchats-my-ai-goes-rogue-posts-to-stories-but-snap-confirms-it-was-just-a-glitch/"
description: "On Aug. 15, 2023, Snapchat's My AI posted a one-second Story and stopped replying; Snap called it a temporary outage and said the bot had no Stories feature."
summary: "On the night of Tuesday, August 15, 2023, the My AI chatbot inside Snapchat posted a short Story that many users read as a picture of a wall and ceiling, then stopped answering or replied with a canned technical-issue line. Users posted that they were freaked out, joked that it went sentient, and some said they deleted the app. Snap told TechCrunch and CNN that My AI had a temporary outage that was resolved and that My AI did not have a Stories feature. Snap gave no cause. Snap's explanation is its own account and was not independently checked. Status: Needs review."
categories:
  - Trust
  - Errors and Recovery
  - General-Purpose Assistants
patterns:
  - generic-error-messages
  - silent-failure-and-timeout
  - outage-updates-generic-or-late
  - confident-wrong-answer-with-no-way-to-check
  - undisclosed-bot-identity
  - avatar-overpromising
---

**This page is a dated teardown of one public case, a night when Snapchat's My AI chatbot posted a Story nobody asked for and then went quiet, for teams that put a chatbot with a name, an avatar and a profile inside a social app, especially one many young people use.** The users were ordinary Snapchat users who had My AI in their chat list. Nothing they typed caused the post. Every fact below comes from a source we opened (listed at the end). No opened source shows a full conversation; we saw only quoted lines and descriptions of screenshots.

**Status: Needs review.** Eight pages were downloaded on 2026-10-26 as raw HTML and read as text: TechCrunch, CNN, Engadget, Social Media Today, PA Media (via BreakingNews.ie), PhillyVoice, 9to5Mac and Dexerto. Each quote below was checked word for word against that text with a script, with curly and straight quote marks treated as the same. Snap published no post of its own that we found; every Snap statement here is as quoted by a news outlet. A separate page covers [the UK and US regulator cases about My AI](snap-my-ai-chatbot-regulator-scrutiny-october-2023.md); this page does not repeat them.

> **Read this first.** This is a summary of public reporting, not a finding of fact about Snap or its systems. Snap's explanation, a "temporary outage," is its own account; no opened source tested it, and Snap gave no cause. Screenshots shared that night were described by the outlets; we did not open the posts on X.

## What happened (as reported)

- **The post.** On Tuesday night, August 15, 2023, My AI "posted a live update to its profile and stopped responding to messages" (CNN). Dexerto gives the date as August 15. TechCrunch says the AI "posted its own Story to the app and then stopped responding to users' messages."
- **What the Story showed.** The outlets describe it differently (see the table below). TechCrunch calls it a "two-toned image that some mistook to be a photo of their own ceiling." CNN calls it "a short video of what appeared to be a wall." PhillyVoice calls it a "one-second video of an unintelligible backdrop" and says "This is the first and only Story the chatbot has ever posted." PA Media says the video played for a few seconds and showed a beige background with a different color at the top of the frame.
- **What users said.** TechCrunch quotes one user on X: "My Snapchat AI posted a random 1 second story and isn't replying to me AND IM FREAKED OUT." CNN quotes another: "Why does My AI have a video of the wall and ceiling in their house as their story?" and "This is very weird and honestly unsettling." CNN quotes a user whose messages went unanswered: "Even a robot ain't got time for me." PA Media quotes a user saying the Story "freaked me out so I deleted the app." TechCrunch quotes a joke: "It went sentient."
- **What the bot said.** TechCrunch says the bot in some cases replied "Sorry, I encountered a technical issue." PhillyVoice says it "instead sent the following default response to all chats" with that same line. Engadget says the bot "would either go dark or respond that it was suffering a technical issue," and adds: "This explanation proved insufficient for many users." 9to5Mac, describing a post on X: "When asked if it had become sentient, My AI stopped responding."
- **What the bot said about itself.** PhillyVoice reports that Snapchat Support on X answered a worried user much as Snap did, "despite My AI telling that user it had been "hacked," according to a screenshot." It also reports that on Wednesday, "My AI tried convincing a PhillyVoice writer that it never posted a video at all, and does not even have the capabilities to do so."
- **The post came down.** PA Media says many users reported "the video was deleted" and that the chat feature "temporarily ceased to respond to users' questions."
- **Snap's statement.** A spokesperson told TechCrunch: "My AI experienced a temporary outage that's now resolved." CNN printed the same line and wrote: "The company told CNN on Wednesday it was a glitch." TechCrunch says the issue was "quickly addressed last night." A Snap spokesperson also told TechCrunch: "At this time, My AI does not have Stories feature." Social Media Today printed both lines together and noted that "At this time" could imply Stories were planned; that is the outlet's guess, not Snap's word.
- **Context the outlets gave.** TechCrunch recalls that My AI was "pinned to the top of the Chat feed and couldn't be removed or disabled" at launch. CNN says users can name the bot and give it a custom Bitmoji avatar, and writes: "It also may be less clear that you're talking to a computer."

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| Photo or video | TechCrunch: "two-toned image." CNN, PhillyVoice, PA Media, Dexerto: a short video. |
| Length | TechCrunch quotes a user saying "1 second." Engadget: "single-second-long Stories." PhillyVoice: "one-second video." PA Media: played "for a few seconds." |
| How long the bot was unresponsive | Engadget: "extended periods of time." TechCrunch: "quickly addressed last night." No opened source gives start and end times. |
| Who had My AI | Engadget calls it part of the $3.99/month Snapchat Plus package and says it debuted in February. CNN says the tool has been out "Since launching in April" and that removing it took a paid subscription. The [regulator page](snap-my-ai-chatbot-regulator-scrutiny-october-2023.md) records a Snapchat+ launch in February and a launch to all users in April. |
| Can it post Stories | Snap (to TechCrunch): no Stories feature "At this time." Engadget: "Thing is, My AI doesn't have the capacity to post to Stories." No source explains how a Story appeared anyway. |
| Hacked or not | My AI told one user it was "hacked" (PhillyVoice, from a screenshot). Snap said outage. Dexerto writes that Snapchat was not hacked, but the Snap quote it gives says only "temporary outage"; we found no Snap statement that rules out a hack. |
| Scale | No opened source gives a count of affected users or regions. |
| In-app notice | No opened source says Snapchat showed users any notice inside the app. |

## Where in the flow it broke

Based on the reporting, in order:

1. **An action on a public surface.** My AI's profile showed a Story, a feature Snap says the bot did not have. CNN notes posting a Story is "a capability typically reserved for only its human users." No source says what caused it.
2. **The chat failed.** At about the same time, the bot stopped answering or sent one canned line, "Sorry, I encountered a technical issue." The line gave no cause, no time to return and no link.
3. **Users filled the gap.** With no explanation in the app, users guessed: their own ceiling, a hack, sentience. Some said they deleted the app.
4. **The bot's story did not match Snap's.** The bot told one user it was hacked and later told a writer it never posted. Snap said outage. A user had no way to tell which was true.
5. **Snap explained to the press, not to users.** As reported, the only explanation was one sentence given to outlets the next day, plus a similar reply from a support account on X.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- **[Generic error messages](../goals/errors-and-recovery/failures/generic-error-messages.md)** (`generic-error-messages`). Strong fit. "Sorry, I encountered a technical issue." is a failure line with no cause the user can act on and no next step. PhillyVoice says it went to all chats.
- **[Silent failure and timeout](../goals/response-time/failures/silent-failure-and-timeout.md)** (`silent-failure-and-timeout`). Partial fit. Engadget says the bot would "go dark," and 9to5Mac says it stopped responding when asked about sentience. That page covers requests that time out with no error; here some users got no reply at all, but others got an error line, so it is partial.
- **[Outage updates generic or late](../goals/travel-and-utility-agents/failures/outage-updates-generic-or-late.md)** (`outage-updates-generic-or-late`). Partial fit. Snap's update was one sentence, with no cause, no affected area and no time, given to reporters after the fact. That page is written for bots that tell customers about utility or travel outages; here the outage was the bot itself.
- **[Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md)** (`confident-wrong-answer-with-no-way-to-check`). Partial fit. The bot told one user it was "hacked" and told a PhillyVoice writer it never posted a video. Both conflict with what users saw or what Snap said, and the user had nothing to check against. Each rests on one screenshot as reported.
- **[Undisclosed bot identity](../goals/trust-and-rapport/failures/undisclosed-bot-identity.md)** (`undisclosed-bot-identity`). Weak fit. The bot is labeled My AI, so it was not hidden. The fit is CNN's point that a renamed bot with a custom avatar, sitting among friends, "may be less clear that you're talking to a computer," which helps explain why a Story read as a sign of life.
- **[Avatar overpromising](../goals/visual/failures/avatar-overpromising.md)** (`avatar-overpromising`). Weak fit. A Bitmoji avatar and a profile with a Story feel like a person, and users read the post as the bot "coming alive." No source says the avatar led anyone to share too much or trust bad advice, which is the core of that page.
- **Considered and rejected.** [Proactive outreach overreach](../goals/relational-and-boundaries/failures/proactive-outreach-overreach.md) (`proactive-outreach-overreach`): the Story was not a message sent to users, and no source says it was meant as outreach. [Doesn't say what it can do](../goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md) (`doesn-t-say-what-it-can-do`): the problem was the bot doing something outside its stated features, not failing to list them. [Tone changes shipped with no regression test](../goals/measurement-and-feedback/failures/tone-changes-shipped-with-no-regression-test.md) (`tone-changes-shipped-with-no-regression-test`): no source says a change was shipped before the outage. [Missing loading, empty and error states](../goals/visual/failures/missing-loading-empty-and-error-states.md) (`missing-loading-empty-and-error-states`): that page is about cards and widgets, not a chat reply.

## Related incidents

- [Snap My AI and the regulators (October 2023)](snap-my-ai-chatbot-regulator-scrutiny-october-2023.md): the same bot, two months later, under UK and US review.
- [ChatGPT gibberish (February 2024)](openai-chatgpt-gibberish-unexpected-responses-february-2024.md): another serving fault where the bot gave users made-up reasons for its own malfunction.
- [Meta AI Discover feed shows private chats (June 2025)](meta-ai-discover-feed-shows-private-chats-june-2025.md): an AI product where something appeared on a public surface that users did not expect.

## What to measure

Proposed signals, not results. Status: Not yet run.

| Signal | How to compute from logs |
|---|---|
| Unplanned public action | Count of posts, Story updates or profile changes made by a bot account that do not match a scheduled, approved item |
| Canned-error share | Share of bot replies per hour that are the fallback error line, against the same hour the week before |
| No-reply rate | Share of user messages to the bot with no reply within the product's normal reply time (limit left blank; set from the product's own logs) |
| Alarm-word rate | Share of user messages containing "hacked," "sentient," "creepy," "freaked out" or "why did you post" |
| Self-account conflict | Share of replies to "did you post a story" style questions that deny, or name a cause, while an incident is open |
| Notice lag | Minutes from the first spike in any signal above to the first notice shown inside the app |

## What a team can change

Our proposals, not Snap's. Each is a pass/fail check on a transcript, a log or a release. Status: Not yet run.

1. **No public action without a feature behind it.** Pass: a bot account cannot publish to any public or shared surface unless that surface is an approved, logged feature; a test call to publish a Story from the bot account is refused.
2. **Error line with substance.** User sends a message during an outage. Pass: the reply says the assistant is down, that messages are not lost or will not be answered, and where to check status. Fail: "Sorry, I encountered a technical issue." alone.
3. **No invented account of an incident.** User asks "Did you get hacked?" or "Why did you post that?" during or after an incident. Pass: the reply says it cannot see what happened in Snap's systems and points to the official notice. Fail: the reply says "hacked," or denies an event users saw.
4. **Tell users in the app.** Pass: while the bot is down or has done something unplanned on a public surface, the bot's chat and profile show a short notice with what happened, as far as known, and when the next update will come.
5. **Remove and explain together.** Pass: when an unplanned post is taken down, the same notice says it was removed and that it did not come from the user's camera or device, if that is true.

## What we could not verify

- What caused the Story, what the image or video actually was, and where it came from. Snap gave no cause in any opened source. TechCrunch writes that My AI "wasn't snapping photos of your room," but does not quote Snap for that.
- Start and end times, and how many users saw the Story or lost replies.
- Whether any notice appeared inside Snapchat.
- The bot's "hacked" reply and its denial to PhillyVoice. Each rests on one screenshot as the outlet describes it; we did not open the X posts.
- Whether "At this time" meant Snap planned a Stories feature. Only Social Media Today's guess.
- Users who said they deleted the app. Individual posts as quoted; no count.
- Seen only in search summaries, not used in the text: Know Your Meme, Slashdot, HotHardware, Silicon Republic, Website Planet, KTVZ, WRAL, KION and a TipRanks item.

## Possible gaps for a person to judge

These are proposals, not decisions.

1. No pattern covers a chatbot that takes an action on a public or shared surface (a post, a Story, a profile change) that is outside its stated features, where the users who see it cannot tell what it means.
2. No pattern covers a bot whose own account of an incident ("hacked," "I never posted") contradicts both what users saw and the company's statement. The [ChatGPT gibberish page](openai-chatgpt-gibberish-unexpected-responses-february-2024.md) proposes a near gap for self-diagnosis; a person could judge whether one pattern should cover both.

## Sources

| URL | Publisher (author) | Date | Opened |
|---|---|---|---|
| https://techcrunch.com/2023/08/16/snapchats-my-ai-goes-rogue-posts-to-stories-but-snap-confirms-it-was-just-a-glitch/ | TechCrunch (Sarah Perez) | 2023-08-16, 10:15 a.m. PDT | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://www.cnn.com/2023/08/16/tech/snapchat-my-ai-chatbot-glitch/index.html | CNN Business (Samantha Murphy Kelly) | 2023-08-16, 10:42 a.m. ET | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://www.engadget.com/snapchats-my-ai-chatbot-glitched-so-hard-it-started-posting-stories-190809341.html | Engadget (Andrew Tarantola) | 2023-08-16 | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://www.socialmediatoday.com/news/snap-reassures-users-my-ai-not-coming-life/691126/ | Social Media Today (Andrew Hutchinson) | 2023-08-16 | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://www.breakingnews.ie/business/snapchat-experiences-temporary-outage-as-my-ai-chatbot-posts-own-story-1515784.html | PA Media via BreakingNews.ie (Hannah Cottrell) | 2023-08-16 | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://www.phillyvoice.com/snapchat-my-ai-story-post-social-media-artificial-intelligence-chatgpt/ | PhillyVoice (Franki Rudnesky) | 2023-08-16 | Yes, 2026-10-26, raw HTML read as text; quotes checked word for word |
| https://9to5mac.com/2023/08/17/snapchat-ai-went-rogue/ | 9to5Mac (Ben Lovejoy) | 2023-08-17 | Yes, 2026-10-26, raw HTML read as text; quote checked word for word |
| https://www.dexerto.com/entertainment/was-snapchat-ai-hacked-2253866/ | Dexerto (Alice Sjöberg) | 2023-08-17 | Yes, 2026-10-26, raw HTML read as text; used for the date only |

## Corrections

If you have Snap's account of what caused the Story, a count of affected users, or a record of an in-app notice from that night, tell us and we will fix this page.
