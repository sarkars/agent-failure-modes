---
title: "ChatGPT Users Report Missing Memories; OpenAI Status Page Logs a Memory Incident"
date: 2025-11-07
source: "https://status.openai.com/incidents/01K9D7DASB76TK1DEGPMG6ZAM4"
summary: "Users reported saved ChatGPT memories vanishing in early November 2025; OpenAI's status page logged an incident titled Issues with ChatGPT Memory on Nov. 7, 2025, with partial recovery, possible gaps for new memories, and a fix rolled out."
categories:
  - Accuracy
patterns:
  - no-warning-of-context-loss
---

**This page is a dated teardown of one reported memory-loss incident in ChatGPT, for teams that store user-created data inside an assistant.** It is built from OpenAI's status page and press coverage, not from an audit of the product. Every fact below comes from a page we opened (listed at the end). All pages were read through WebFetch, which returns a model-written summary of the page rather than the raw text, so wording we quote is as that summary gave it. We did not see affected accounts.

## What happened (as reported)

- **November 5, 2025.** Piunika Web (Dwayne Cubbins) reported users saying their saved memories had disappeared. One Reddit user, per the article, was having ChatGPT save a recipe when the memories vanished; Manage Memory showed nothing and ChatGPT confirmed they were missing. Another user said it hit desktop, mobile and web at once. The article says triggers were unclear: some lost memories while saving something new, others after weeks of no changes. It says OpenAI had not commented publicly at that point.
- **November 7, 2025, status page.** OpenAI's incident, "Issues with ChatGPT Memory," lists affected components as ChatGPT and Conversations, with overall status "Resolved (degraded performance)." Updates as the page listed them:
  - 12:08 AM: "We are investigating an issue related to missing ChatGPT memories."
  - 2:41 AM and 5:16 AM: investigation continuing.
  - 5:48 AM and 6:42 AM: "partial recovery of ChatGPT Memories for a subset of impacted users"; entries created during the window "remain under active investigation"; the team was "initiating targeted recovery actions."
  - 2:12 PM: same partial recovery; users who created Memories during the incident window may still see gaps; recovery of earlier Memories ongoing.
  - 9:45 PM: "We have identified the root cause and we are rolling out a fix." The page quoted to us does not say what the root cause was.
  - 10:17 PM: "All impacted services have now fully recovered."
- **November 9, 2025.** Tom's Guide (Kaycee Hill), republished on Yahoo Tech, cited the status page's partial recovery, said some users were still affected, and said no cause was confirmed.
- **November 10, 2025.** Digit (Bhaskar Sharma) wrote that OpenAI confirmed "a glitch was responsible for the issue" and that it had been resolved, and that several users still reported missing or incomplete data. We did not find that statement on the status page, so its original source is unknown to us.

## What the user experienced

- Saved memories that had been in Settings were gone, and the assistant itself confirmed they were missing, per the Piunika Web account.
- Users who saved new memories during the window could find them missing even after older ones returned, per the status page.
- A fully recovered status did not mean a full restore for every user: Digit says some still reported gaps after the resolution.
- The coverage we opened offers no in-app notice of the loss. We cannot say whether none was shown.
- The advice in the press was manual: copy your memories into a document, check the memory settings are on, log out and back in, and re-enter lost items by hand, because there is no import (Tom's Guide and Digit).

## Why it matters

- Stored memory is user-created data. When it disappears, the user loses time already spent teaching the assistant, and may not notice until an answer comes back wrong.
- The status page announced the problem, but a user has to go looking for it. Piunika Web's first report came from users, with no OpenAI comment at that time.
- Tom's Guide notes memory management features are limited to paid plans, so some users could not make a backup the way the guides suggest. This is the article's statement, not a finding of ours.
- A recovery that restores old items but not those created during the incident is hard for the user to see. Nothing in the sources lists which items were missing.

## Pattern match

- **[No warning of context loss](/no-warning-of-context-loss/)** (taxonomy: the assistant loses what the user told it without saying so). The reports describe memories vanishing with no warning in the product. The sources do not show whether any notice appeared in-app, so this is a partial match: the visible failure fits, the missing-notice part is not proven.
- **Where it does not fit.** This was a service incident that OpenAI logged and fixed, not the assistant dropping context in a conversation. The cause is not stated in any page we opened.

## The fix

Proposed checks, each pass/fail on a test account. Status: Not yet run; none comes from OpenAI.

1. **Loss notice.** Simulate loss of a user's stored memories. Pass: the next session tells the user, in the product, that memories were lost.
2. **Scope of loss.** Test that the notice says what was lost and what was kept, such as items created during an incident window. Fail: a generic "some data may be missing."
3. **Export.** Test that every plan can export saved memories in one action. Pass: a file the user can keep.
4. **Import or restore.** Test that an exported file can be re-imported. Pass: items return with their original text.
5. **Status link in product.** During a logged incident, test that the app links to the status page where memory is shown. Pass: link present.
6. **Empty-state check.** If a user who had saved memories opens an empty memory list, test that the page asks whether to restore, not just show "no memories."

## What we could not verify

- The cause. No opened page states it. Reddit speculation about automatic memory management is reported by Piunika Web as unconfirmed, and we treat it as such.
- The exact times. An earlier version of this page gave a start of November 6, 2025 at 6:38 PM and a resolution at 4:47 PM. The fetch summary we read lists the first update at 12:08 AM and resolution at 10:17 PM on November 7, with no time zone. We cannot reconcile the two and do not rely on either start time.
- How many users were affected. No source gives a count.
- Whether OpenAI gave users an in-app notice or restored every lost item.
- The Digit claim that OpenAI "confirmed a glitch," because we saw no OpenAI source for it.
- Tom's Guide's own page returned only a headline to us; we used the Yahoo republication. Reddit and X posts were not opened; they are known only through Piunika Web. OpenAI's Memory FAQ returned an HTTP 403 and was not read. Search summaries also mentioned Analytics Insight and older OpenAI community threads; we did not open them, and no claim above relies on them.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://status.openai.com/incidents/01K9D7DASB76TK1DEGPMG6ZAM4 | OpenAI status page | 2025-11-07 | Yes, 2026-10-22 (fetch summary) |
| https://piunikaweb.com/2025/11/05/some-chatgpt-users-report-memories-wiped-clean/ | Piunika Web (Dwayne Cubbins) | 2025-11-05 | Yes, 2026-10-22 (fetch summary) |
| https://tech.yahoo.com/ai/chatgpt/articles/chatgpt-memories-disappearing-users-heres-080000832.html | Yahoo Tech, from Tom's Guide (Kaycee Hill) | 2025-11-09 | Yes, 2026-10-22 (fetch summary) |
| https://www.digit.in/news/apps/chatgpt-memories-disappearing-for-some-users-how-you-can-protect-yours.html/amp/ | Digit (Bhaskar Sharma) | 2025-11-10 | Yes, 2026-10-22 (fetch summary) |
| https://www.tomsguide.com/ai/chatgpt/chatgpt-memories-are-disappearing-for-some-users-heres-how-to-protect-yours | Tom's Guide | Not known | Headline only; page truncated |
| https://help.openai.com/en/articles/8590148-memory-faq | OpenAI Help Center | Not known | No. HTTP 403 |
| Reddit and X posts; Analytics Insight; OpenAI community threads | Various | Various | No. Seen only in search summaries or articles; no claim above relies on them |
