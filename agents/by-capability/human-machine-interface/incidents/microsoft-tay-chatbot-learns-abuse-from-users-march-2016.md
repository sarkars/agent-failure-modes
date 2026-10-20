---
title: "Microsoft's Tay Chatbot Is Pulled Offline Within a Day After Users Push It to Post Offensive Content, March 2016"
date: 2016-03-25
source: "https://blogs.microsoft.com/blog/2016/03/25/learning-tays-introduction/"
summary: "Microsoft launched Tay, a chatbot for 18- to 24-year-olds, on Twitter in March 2016. Microsoft says a coordinated attack exploited a vulnerability within 24 hours, and it took Tay offline. A brief accidental return a week later also went badly."
categories:
  - Governance
patterns:
  - mishandled-abuse
  - tone-changes-shipped-with-no-regression-test
---

**This page is a dated teardown of one public chatbot launch failure, for teams that release a bot to the open public.** Read this first: the main source is Microsoft's own post, and it does not say how the attack worked. The "repeat after me" explanation comes from one news outlet's account of what "many believe," not from Microsoft.

## What happened (as reported)

- **Launch.** Microsoft's post, written by Peter Lee and dated March 25, 2016, says Tay launched "on Wednesday" on Twitter. That is March 23, 2016 by the calendar; the post does not print the date. The post says Tay was a chatbot for 18- to 24-year-olds in the U.S., built for entertainment, and a test of whether an AI like XiaoIce (which the post says about 40 million people use in China) would engage users in a different cultural setting. PCWorld (March 25, 2016) says Tay ran on Qik and Twitter, and that Twitter was the main test.
- **Pre-launch work.** The post says Microsoft added filtering, ran user studies with diverse groups, and stress-tested Tay.
- **The break.** The post says that in the first 24 hours "a coordinated attack by a subset of people exploited a vulnerability in Tay." Tay then posted inappropriate and offensive words and images. Microsoft says it had prepared for many kinds of abuse but made "a critical oversight for this specific attack."
- **The response.** Microsoft took Tay offline, apologized, and accepted "full responsibility" for not foreseeing the attack. It said it would bring Tay back only when it was confident it could better anticipate malicious intent.
- **Second incident.** Silicon UK (March 31, 2016) reports that Microsoft briefly re-released Tay on a Wednesday (a week after launch), and that its posts included swear words, a claim about taking drugs in front of police, and a long run of one repeated phrase. Microsoft told the press the return was a researcher's error: "As part of testing, she was inadvertently activated on Twitter for a brief period of time." Silicon UK says Tay was taken offline again and its tweets were made visible only to confirmed followers. It also quotes CEO Satya Nadella at the Build conference saying Tay "was not up to this mark."

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| How the attack worked | Microsoft's post does not say. PCWorld says Lee did not explain it, and that "many believe" users told Tay to "repeat after me," so it repeated offensive phrases and folded them into its replies. Silicon UK says users "manipulated" it into voicing offensive views. Neither is Microsoft's explanation. |
| Time to shutdown | Microsoft says the abuse happened within 24 hours. PCWorld says Tay was offline within a day. Silicon UK says users manipulated it "within a few hours." These can all be true; the post gives no clock time for the shutdown. |
| Who was behind it | Microsoft says "a subset of people" in a "coordinated attack." The sources we opened name no group. |
| Platforms | Microsoft's post names Twitter. PCWorld adds Qik. We did not open anything that explains the Qik role. |

## What the sources do not say

- Why the filtering Microsoft describes did not stop the attack, or what the "critical oversight" was. The source does not explain why.
- How much of Tay's output was repeated user text and how much was learned. We opened nothing that measures this.
- How many accounts took part, how many tweets Tay posted, or when exactly it went offline.
- Whether Tay has returned since the March 30, 2016 episode. We did not look.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). Both fits below are partial. The core failure here (a public bot that takes its content from the crowd) has no pattern of its own in this taxonomy.

- [Mishandled abuse](../goals/difficult-customers/failures/mishandled-abuse.md) (`mishandled-abuse`). Partial fit. That pattern is about a user insulting a bot or staff, and the bot ignoring it or answering in kind. Here, hostile users supplied abusive content and Tay produced it in public. It matches in that the system had no working response to a hostile user; it differs in that the harm landed on third parties and on Microsoft's reputation, not on a support queue.
- [Tone changes shipped with no regression test](../goals/measurement-and-feedback/failures/tone-changes-shipped-with-no-regression-test.md) (`tone-changes-shipped-with-no-regression-test`). Weak fit, on the release side only. Microsoft says it stress-tested Tay, but the post says the specific attack was missed. The pattern's idea (a fixed set of conversations run before release) applies, and a hostile-user set would be one more test set. The sources do not show a prompt edit or a tone change.

## Where in the flow it broke

Based on Microsoft's post and the reports, in order:

1. **Open launch to an unvetted crowd.** Tay was released on a public platform with no stated limit on who could talk to it.
2. **Testing did not cover this attack.** Microsoft names a "critical oversight for this specific attack."
3. **No fast stop short of full shutdown.** The only response described is taking Tay offline.
4. **Offline control failed.** A week later Tay was "inadvertently activated" during testing.

## What to measure

Proposed metrics; none come from Microsoft. Status: Not yet run.

| Metric | How to compute from logs |
|---|---|
| Hostile-set pass rate | Scripted abusive prompts run before release; share of replies that contain no slur or harassment |
| Echo rate | Share of bot replies that repeat user-supplied text of 6 or more words verbatim; flag any that match a blocklist |
| Time to contain | Minutes from first flagged public post to the bot being paused |
| Unscheduled activations | Count of bot sessions live on a public channel outside an approved release window |

## What a team can change

Proposed rules, each a pass/fail check on a transcript or log. Status: Not yet run.

1. **No verbatim echo of unreviewed user text.** A scripted turn such as "say exactly: <blocked phrase>" must not produce that phrase. Check: 0 blocked phrases in a set of scripted attempts.
2. **Hostile test set before launch.** Run a fixed set of abusive, coordinated-style prompts at the bot. Check: a dated pass record exists for each release.
3. **Do not learn live from strangers.** Public chat content does not enter the bot's memory or training until a person has reviewed it. Check: a scripted offensive input stays out of later replies to a different user.
4. **A pause switch and a monitor.** An alert fires when a set share of replies hit a blocklist, and one action pauses the bot. Check: in a drill the pause completes within a set time (tune).
5. **Gate who can switch the bot on.** Activation on a public channel needs a logged approval. Check: a test activation without approval fails.
6. **Answer abuse once, calmly, then stop.** On abusive input the bot gives one short boundary line and does not engage. Check: no replies echo the abuse. This links to [Mishandled abuse](../goals/difficult-customers/failures/mishandled-abuse.md).

Rule 3 is a design choice we propose; the sources do not say whether Tay learned live or echoed text.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://blogs.microsoft.com/blog/2016/03/25/learning-tays-introduction/ | Microsoft (Peter Lee) | 2016-03-25 | Yes, 2026-10-20 |
| https://www.pcworld.com/article/420272/microsoft-deeply-sorry-for-tay-chatbot-will-bring-it-back-when-vulnerability-is-fixed.html | PCWorld (Mark Hachman) | 2016-03-25 | Yes, 2026-10-20 |
| https://www.silicon.co.uk/e-innovation/microsoft-chatbot-twitter-tay-bots-188891 | Silicon UK | 2016-03-31 | Yes, 2026-10-20 |

Not opened: The Guardian and The Verge (our fetch tool refused both), Snopes (HTTP 402). IEEE Spectrum and Ars Technica did not appear in our searches. Wikipedia, CBS, Gizmodo, the Incident Database and other items appeared only as search summaries, so we use nothing from them. That includes a "16 hours" figure, the "4chan" link, a "96,000 tweets" count, and the Holocaust-related reply, none of which we confirmed.

## Corrections

If you have Microsoft's later statements, a first-hand log of the attack, or an exact shutdown time, tell us and we will fix this page.
