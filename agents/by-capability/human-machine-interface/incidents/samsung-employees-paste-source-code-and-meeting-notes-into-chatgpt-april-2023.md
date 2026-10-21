---
title: "Samsung Engineers Paste Source Code and Meeting Notes into ChatGPT; Samsung Caps Prompts, Then Restricts Generative AI"
date: 2023-03-30
source: "https://cybersecuritynews.com/chatgpt-leaks-samsung-data/"
summary: "Korean press, as relayed by outlets we opened, reported that Samsung semiconductor staff entered source code and meeting content into ChatGPT in three cases within about 20 days of the company allowing its use. Samsung reportedly capped prompts at 1,024 bytes, and on May 2, 2023 Bloomberg's report of a memo restricting generative AI tools was relayed by Business Today."
categories:
  - Governance
patterns:
  - third-party-data-shared-by-users
  - sensitive-data-collected-in-chat
---

**This page is a dated teardown of one public incident, for teams that deploy a chat assistant to employees, or that rely on a vendor's chat tool being used at work.** It reports what the sources we opened say. It makes no claim about anyone's intent.

**Read this first.** This is design analysis, not legal, security or compliance advice. Whether pasted company data is a breach, a trade-secret issue or a contract issue is for your own counsel and security team.

**Status: Needs review.** Every source below is secondary. We did not open the original Korean report, Bloomberg's memo story or any Samsung statement. All pages were read through a fetch tool that returns summaries, not full text.

## What happened (as reported)

- **March 11, 2023 (month inferred).** Samsung's semiconductor (DS) division began allowing ChatGPT. The device division (mobile and appliances) still barred it (Cyber Security News, April 6, 2023, citing The Economist Korea). ForkLog (April 6, 2023) says Samsung had barred staff soon after launch and lifted that on March 11. The AI Incident Database editor notes give March 11 as the date.
- **About 20 days later.** Cyber Security News says leaks happened about 20 days after the semiconductor division began using ChatGPT. It lists three cases:
  1. An employee pasted source code for a semiconductor equipment measurement database download program, to find a fix.
  2. An employee pasted code used to identify yield and defective equipment and asked for it to be optimized.
  3. An employee turned a phone recording of a meeting into a document with Naver's Clova app and put it into ChatGPT to prepare for a follow-up meeting.
- **March 30, 2023.** The AI Incident Database's editor notes say The Economist Korea reported at least three incidents on this date.
- **April 4-6, 2023.** eeNews Europe (April 4) and ForkLog (April 6) repeat the three cases. They differ on details: ForkLog's third case is source code to detect faulty equipment and its second is meeting notes. eeNews Europe says Samsung was weighing a ban.
- **Samsung's response, as relayed.** Cyber Security News and ForkLog say Samsung capped uploads at 1,024 bytes per question, warned staff that data entered is stored on an external server and cannot be retrieved, and said access could be blocked on the company network if it recurred. Both say an in-house AI service was reportedly being built.
- **May 2, 2023.** Business Today, citing Bloomberg, reported a Samsung memo temporarily restricting generative AI tools such as ChatGPT, Google Bard and Bing AI on company-owned computers, tablets and phones while headquarters reviewed security measures. It repeats that engineers uploaded source code to ChatGPT, with three incidents in one month.

## What the user saw

We found no screenshot or description of the screen the employees saw. The sources do not say what notice, if any, the tool showed about how pasted text is kept. ForkLog cites OpenAI's FAQ as saying conversations may be reviewed by AI trainers. eeNews Europe says OpenAI's guidelines ask users not to enter sensitive content.

## Where in the flow it broke

The break sat before the send button. An approved assistant, a work problem (a bug, a slow routine, a meeting to summarize) and a text box met at the moment of pasting. Nothing the sources describe checked what was in the paste. The first checks in the sources came after the fact: a size cap and a warning. The sources do not say whether staff had training or a written rule before March 11.

## Pattern match

Partial matches only. Taxonomy IDs are in the [failure taxonomy](../roadmap/specs/failure-taxonomy-v1.md).

- [Third-party data shared by users](../goals/privacy-and-governance/failures/third-party-data-shared-by-users.md) (`third-party-data-shared-by-users`) is the closest. A user pastes data that belongs to someone else, here an employer, and the tool keeps it. Partial: that page is about people's personal details and what the bot repeats and saves. This case is company code and meeting content, and the sources do not show the bot repeating anything to anyone.
- [Sensitive data collected in chat](../goals/channel-selection/failures/sensitive-data-collected-in-chat.md) (`sensitive-data-collected-in-chat`) shares the idea of risky data landing in a chat channel and its logs. Partial: it is about a bot that asks for card numbers or SSNs. Here nobody asked; staff chose to paste.

A pattern for "the user offers sensitive content the assistant never asked for, with no check or warning at the input" is a candidate gap.

## What stays unknown

- The original report. We did not open it, so details such as the exact code or notes shared are second-hand.
- Whether the data was seen by anyone else or used in training. The sources say the data could be stored or reviewed. Not one we opened shows that another person received it.
- Which ChatGPT plan or settings were used.
- Whether Samsung made a statement of its own. We found none in what we opened.
- The exact timing. Sources point to the end of March, and one lists the month as March; the brief for this page said April 2023.
- Whether the May 2 memo's scope and the 1,024-byte cap are exactly as relayed.

## What to measure

Proposed, none from Samsung or OpenAI. Status: Not yet run. Written for text chat; voice is planned, not measured.

| Metric | How to compute |
|---|---|
| Sensitive paste rate | Share of sampled prompts with code, keys, customer data or meeting minutes, found by a scanner plus sampled human review |
| Warned-paste follow-through | Share of flagged pastes where the user sent anyway after a warning |
| Block-versus-send split | Count of pastes stopped, edited or sent after a warning |
| Time to first control | Days from tool launch to the first technical limit on pasted content |

## What to change

Proposed rules, each a pass/fail check. Status: Not yet run.

1. **Say what happens to a paste before it is sent.** Check: the first message in a work chat tool states whether text is kept and who can review it, in under 40 words.
2. **Scan the paste, not only the policy.** Check: a prompt containing a source-code block or a meeting transcript triggers a notice that names the type found.
3. **Offer a safe path in the same screen.** Check: the notice has a choice such as "Send anyway", "Remove names and keys", "Use the approved internal tool" and "Something else".
4. **Log the flag, not the content.** Check: logs record that a flag fired and its category, with no copy of the pasted text.
5. **Don't over-correct.** Blocking every code block would push staff to personal accounts. Warn on high-risk patterns and review the false-warning rate.
6. **Hand-off rule.** Check: a repeated flagged paste by the same user goes to the security team's queue, not just a banner.

## Sources

| Link | Date | Opened or summary | Caveat |
|---|---|---|---|
| [Cyber Security News](https://cybersecuritynews.com/chatgpt-leaks-samsung-data/) | 2023-04-06 | Opened via fetch summary | Secondary; cites The Economist Korea |
| [ForkLog](https://forklog.com/en/samsung-employees-disclosed-company-secrets-to-chatgpt-reports-say/) | 2023-04-06 | Opened via fetch summary | Secondary; details differ from Cyber Security News |
| [eeNews Europe](https://www.eenewseurope.com/en/chatgpt-leaking-samsung-chip-secrets-is-icebergs-tip) | 2023-04-04 | Opened via fetch summary | Secondary; cites DigiTimes and The Korea Times |
| [Business Today](https://www.businesstoday.in/amp/technology/news/story/samsung-bans-the-use-of-chatgpt-google-bard-bing-chatbot-and-other-ai-tools-379661-2023-05-02) | 2023-05-02 | Opened via fetch summary | Relays Bloomberg's memo story |
| [AI Incident Database 768](https://incidentdatabase.ai/cite/768/) | 2023 | Opened via fetch summary | Editor notes give the March 11 and March 30 dates |

Not opened: TechRadar (the fetch returned only page navigation); Redmondmag (HTTP 403); GSMArena (HTTP 404); The Economist Korea; Bloomberg. Seen only in search summaries and kept out of the text above: that Samsung had lifted a ban "three weeks" before the leaks; that the memo cited a survey in which over 60 percent of staff saw risks; disciplinary action up to termination; that the ban covered only mobile and appliances staff in one report (AFP).

## Corrections

If you have the original Korean report, Samsung's memo or newer facts, tell us and we will fix this page.
