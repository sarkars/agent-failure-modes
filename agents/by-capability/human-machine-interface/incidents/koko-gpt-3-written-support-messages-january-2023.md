---
title: "Koko Peer-Support App Sends GPT-3-Assisted Replies to About 4,000 People"
date: 2023-01-06
source: "https://www.nbcnews.com/tech/internet/chatgpt-ai-experiment-mental-health-tech-app-koko-rcna65110"
summary: "In January 2023 Koko co-founder Rob Morris said about 4,000 people on the peer-support service got replies written with help from GPT-3; critics said users had not given informed consent, and Morris said replies were labeled as co-written. All sources were read through fetch summaries."
categories:
  - Companion and Wellbeing Agents
  - Governance
patterns:
  - undisclosed-bot-identity
---

**This page is a dated teardown of one public incident, for teams that let staff or volunteers send AI-drafted messages to people seeking emotional support.** It is built from press reports of Rob Morris's posts and interviews, not from a test of Koko. Every fact below comes from a source we opened (listed at the end).

**Status: Needs review.** Every source was read through a fetch-tool summary, not as a full page. The sources disagree on what users were told and whether they could opt out. Details seen only in search-result summaries are kept out of the claims and listed under "What we could not verify."

## What happened (as reported)

- **October (2022, inferred).** NBC News (Jan 14) says the experiment ran "In October"; the year is inferred from the article date. It gives no end date.
- **How it worked.** GPT-3 wrote replies "either in whole or in part," per NBC News. Human supporters could edit them and still pressed send. Popular Science (Jan 11) says supporters reviewed AI-suggested replies and chose whether to use them.
- **January 6, 2023.** Morris disclosed the experiment on Twitter, per NBC News. Vice (Jan 10) quotes him: "We provided mental health support to about 4,000 people — using GPT-3."
- **Scale and results.** Vice reports AI was used in more than 30,000 messages. It quotes Morris that "Response times went down 50%, to well under a minute." Morris said co-written replies were rated higher, but NBC News says he had no official data to share.
- **Why it stopped.** Morris said that once people learned a machine helped, "it didn't work," per Popular Science. Vice quotes him: "Simulated empathy feels weird, empty."
- **The label.** NBC News says recipients saw "Someone replied to your post! (written in collaboration with Koko Bot)," with no further detail on the bot's role.
- **The dispute.** Morris said critics misread his thread, which said users were told "from the start" (Vice). He wrote, "We were not pairing people up to chat with GPT-3, without their knowledge," and said the feature was opt-in (Popular Science). NBC News reports, in contrast, that "No option was provided to opt out of the experiment aside from not reading the response at all."
- **Consent and review.** Morris told Vice the experiment was exempt from informed consent. Vice reports no sign of IRB review. NBC News says Koko has no federal funding, so it generally had no legal duty to follow IRB rules. Morris later said Koko was exploring a third-party IRB process.

## What the user experienced

- A person posted about a struggle and got a notice that someone replied, "written in collaboration with Koko Bot." Nothing said what the bot wrote or what the human changed.
- Per NBC News, the only way to avoid an AI-assisted reply was not to read it.
- Koko's Discord promised it "connects you with real people who truly get you," per Vice.
- Per Morris, replies rated well until people learned a machine was involved; then they felt "weird, empty."

## Pattern match

- **[Undisclosed bot identity](../goals/trust-and-rapport/failures/undisclosed-bot-identity.md)** (taxonomy: the bot hides that it's an AI or hides what it can't do). A partial fit. The label did name a bot, so this is not a bot posing as a human. The fit is weaker disclosure: a short tag on a notice, no advance notice per Popular Science (citing New Scientist), a disputed opt-in, and a service promising "real people."
- **Where it does not fit.** Humans picked, edited and sent each draft, per NBC News and Popular Science. No user was chatting with GPT-3 alone. We did not use `missed-crisis-signals`: Morris said higher-risk users are always sent to crisis lines (NBC News), and no opened source reports a missed crisis.

## What to measure and what to change

Proposed checks, each pass/fail on a test transcript or message log. Status: Not yet run. None come from Koko.

1. **Disclosure before first use.** Pass: the user sees, before posting, that replies may be drafted by AI and edited by a person.
2. **Per-message label.** Pass: every AI-assisted reply carries a label that says the AI drafted it and a human reviewed it. Fail: a label on the notice only, or none.
3. **Real opt-out.** Pass: a user who opts out gets only human-written replies, and the log shows zero AI drafts sent to them.
4. **Honest marketing.** Pass: no in-app or onboarding text says "real people" without naming AI help.
5. **Ethics review before testing on users.** Pass: a written review exists, dated before launch, for any test in a support setting.
6. **Log and review.** Count AI-assisted replies per user and opt-out requests per week. Any AI reply to an opted-out user blocks the feature until reviewed.

## What we could not verify

- Whether advance notice existed. Vice reports Morris's "from the start" claim; Popular Science cites New Scientist saying users apparently had none. We did not open New Scientist.
- Whether the feature was opt-in. Morris says yes (Popular Science); NBC News reports no opt-out.
- The exact end date and length of the experiment.
- Search summaries say supporters accepted GPT-3 drafts about half the time and that Morris told Insider the work imposed "no further risk." Not in any source we opened.
- Morris's original Twitter thread. We did not open it; it is known only through the articles below.
- Any data behind the higher ratings or the 50% response-time drop. NBC News says Morris shared no official data.
- Gizmodo's report. The link redirected to the Gizmodo home page.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://www.nbcnews.com/tech/internet/chatgpt-ai-experiment-mental-health-tech-app-koko-rcna65110 | NBC News (David Ingram) | 2023-01-14 | Yes, 2026-10-22, fetch-tool summary |
| https://www.vice.com/en/article/4ax9yw/startup-uses-ai-chatbot-to-provide-mental-health-counseling-and-then-realizes-it-feels-weird | Vice (Chloe Xiang) | 2023-01-10 | Yes, 2026-10-22, fetch-tool summary |
| https://www.popsci.com/technology/koko-ai-chatbot-mental-health/ | Popular Science (Andrew Paul) | 2023-01-11 | Yes, 2026-10-22, fetch-tool summary |
| https://gizmodo.com.au/?p=1849133 | Gizmodo | Not known | No. Redirected to the Gizmodo home page |
| New Scientist report on Koko | New Scientist | Not known | No. Known only through Popular Science |
| Insider interview with Rob Morris | Insider | Not known | No. Seen only in search summaries |
| Rob Morris's Twitter thread | Twitter (X) | 2023-01-06 | No. Known only through the articles above |
