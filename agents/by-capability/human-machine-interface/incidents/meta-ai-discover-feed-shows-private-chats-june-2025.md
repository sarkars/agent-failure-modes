---
title: "Meta AI App's Discover Feed Shows Users' Chatbot Conversations Publicly"
date: 2025-06-13
source: "https://www.laptopmag.com/ai/meta-ai-app-public-prompts-disaster"
summary: "In June 2025, outlets and the Mozilla Foundation reported that the Meta AI app's Discover feed showed users' prompts publicly, some of them personal, after a Share button flow users did not seem to understand. Meta said nothing is shared unless the user chooses to post, and added a warning. Read from Laptop Mag, Engadget and Slashdot."
categories:
  - Governance
patterns:
  - copy-share-and-export-lose-content
---

**This page is a dated teardown of one public chatbot incident, for teams that let users publish or share chats from an assistant.** It describes what the sources report and what Meta said. It makes no claim about anyone's intent. Every fact below comes from a page we opened (listed at the end).

**Read this first.** This is design analysis, not legal or privacy advice. Whether a sharing feature meets privacy law is a question for your own legal team.

## What happened (as reported)

- **Late April 2025.** Slashdot (June 8, 2025) says Meta introduced its Meta AI app in late April 2025. The app has a "Discover" feed of prompts that users post.
- **June 8, 2025.** Slashdot, relaying a Mozilla Foundation campaign, reports Mozilla warning that "Meta is quietly turning private AI chats into public content" and that many people do not realize it is happening. Mozilla asked Meta to shut the feed down until privacy protections exist, among other demands (listed below).
- **June 13, 2025.** Laptop Mag (Nick Lucchesi) reported that a "Share" button in the top-right of a Meta AI chat turns a question into a "public prompt" posted to the Discover feed. It reported private-looking questions sitting among AI-generated images, and said the prompts could also appear as suggestions on Facebook and Instagram.
- **June 16, 2025, updated June 17.** Engadget reported that Meta added a warning on the "post to feed" step. The update added a Meta spokesperson's comment.

## What the interface did (as reported)

- **Not public by default.** Slashdot says chats are not public unless a user taps a share button for that chat.
- **Share, then post.** Laptop Mag describes tapping Share, which leads to a public post. Engadget quotes a Meta spokesperson calling posting to Discover a "multi-step process" with some intended friction.
- **The added warning.** Engadget gives the text: "Prompts you post are public and visible to everyone. Your prompts may be suggested by Meta on other Meta apps. Avoid sharing personal or sensitive information." Engadget and Laptop Mag both say it appears only the first time.
- **Before the warning.** Laptop Mag calls the instructions vague. It does not quote the earlier screen text, and we did not see the earlier screen ourselves.
- **How to take posts down.** Engadget lists a path: profile (top right), Data & Privacy, Manage your information, "Make all public prompts visible only to you," then "apply to all."

## What was shown in the feed (as reported)

Laptop Mag reports that the feed showed prompts that looked personal, and that some people appeared to be sharing without realizing it. We do not repeat the users' prompts here, because we cannot check who wrote them or whether they meant to post. Slashdot, citing Business Insider, says some people appeared unaware they were sharing personal information publicly. We did not open the Business Insider article.

## What Meta said

All of this is Meta's statement as relayed by the outlets. We cannot check it.

- Meta described the feed as a place to "see the best prompts people are sharing, or remix them to make them your own" (Slashdot).
- "you're in control: nothing is shared to your feed unless you choose to post it" (Slashdot).
- A spokesperson called posting a "multi-step process" with intended friction and did not answer questions about the new disclaimer (Engadget).

## What Mozilla asked for (as relayed by Slashdot)

Shut down the feed until real privacy protections exist; make all AI interactions private by default with public sharing only after explicit, informed consent; disclose how many users unknowingly shared private information; offer a universal opt-out from AI training across Meta platforms; notify people whose conversations may have been made public and let them delete that content permanently. We could not open Mozilla's own page (see Sources).

## Where in the flow it broke

The user wanted to send or save a chat. The sources report that Share could put the chat in a public feed, and that people may not have known. The break is at the Share tap and the "post to feed" step: the label "Share" did not tell some users who would see the result, and the one warning shown (after the fix) appears only once. The sources do not say how many users meant to post publicly, and none explains why the original screen was built as it was. Laptop Mag's view that the instructions were vague is the outlet's opinion.

## Pattern match

Pattern IDs below were checked against the library files.

- [`copy-share-and-export-lose-content`](../goals/chat-interface/failures/copy-share-and-export-lose-content.md) is the closest page, as with the [ChatGPT shared-links teardown](chatgpt-shared-links-indexed-by-search-engines-july-2025.md). **The match is partial.** That page is about content lost or unclear when a reply is shared; this case is about a share control whose audience was unclear. Breaks at: the Share button and "post to feed" step.
- [`sensitive-data-collected-in-chat`](../goals/channel-selection/failures/sensitive-data-collected-in-chat.md) is adjacent only. It covers collecting card numbers or SSNs in chat; here, users typed personal topics in a normal chat and the exposure came later, at sharing. Not a direct match.
- [`dark-patterns`](../goals/visual/failures/dark-patterns.md) is not claimed. No source we opened says the design was meant to push users, and we make no such claim.

## What to measure

Proposed checks for a team with a publish-to-feed or share button. None come from Meta. Status: Not yet run.

| Metric | How to compute |
|---|---|
| Share controls that name the audience | Share of share/post buttons whose label or next screen says, in plain words, who can see the chat ("anyone, in a public feed") |
| Warning shown on every public post | Share of public posts preceded by an audience notice, not only the first |
| Comprehension of "Share" | In a user test on your own users, share who can say correctly who sees a chat after tapping Share |
| Unshare time | Time from a user hiding a post to it being gone from every surface that showed it |

## What a team can change

Proposed rules, each a pass/fail check on a screen. Status: Not yet run.

1. **Name the audience on the control.** Check: the button or next screen says "public" and where it will appear.
2. **Separate "send to a person" from "publish to everyone."** Check: they are two controls, and public is not the default.
3. **Show the exact content before it posts.** Check: a preview shows the prompt, and any reply, as others will see it.
4. **Warn every time, not once.** Check: the audience notice appears on each public post.
5. **Give a one-step way to undo.** Check: after posting, the confirmation links to hide or delete the post.

## What stays unknown

- How many chats were posted or how many users posted by mistake. No page we opened gives a count.
- What the Share screens looked like before and after the change; we did not see them.
- Whether the warning, feed or settings changed after mid-2025. We did not check.
- Why the flow was built as it was. No source we opened says.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://www.laptopmag.com/ai/meta-ai-app-public-prompts-disaster | Laptop Mag | 2025-06-13 | Yes, 2026-10-21, via fetch summary |
| https://engadget.com/social-media/meta-warns-users-to-avoid-sharing-personal-or-sensitive-information-in-its-ai-app-233900625.html | Engadget | 2025-06-16, updated 2025-06-17 | Yes, 2026-10-21, via fetch summary |
| https://tech.slashdot.org/story/25/06/08/1929242 | Slashdot (relaying Mozilla Foundation) | 2025-06-08 | Yes, 2026-10-21, via fetch summary |

All were read through the fetch tool, which returns a summary, not the raw page. Short quoted phrases are as that tool returned them.

Not opened: Mozilla Foundation campaign pages (HTTP 403), Business Insider (redirected), Neowin (HTTP 403), TechCrunch (not reached). Seen only in search summaries and kept out of the text above: Mozilla's July 3, 2025 note that Meta reached out and briefly used a mandatory warning screen, and a count of over 10,000 petition signatures; Business Insider's wording of the pop-up and a disabled "Post to feed" button; an Appfigures download figure; a report that the feed later showed mostly images and video.

## Caveats

- Single-source facts: the description of the personal-looking prompts (Laptop Mag only) and the take-down path (Engadget only).
- The page `date` is Laptop Mag's date, June 13, 2025.

## Corrections

If you have a screenshot of the original Share screens, Meta's own statement or a better date, tell us and we will fix this page.
