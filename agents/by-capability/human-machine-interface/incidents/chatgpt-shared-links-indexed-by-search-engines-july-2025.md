---
title: "ChatGPT Shared Chats Appear in Search Results; OpenAI Removes the Discoverable Option"
date: 2025-07-31
source: "https://techcrunch.com/2025/07/31/your-public-chatgpt-queries-are-getting-indexed-by-google-and-other-search-engines/"
summary: "In July 2025 shared ChatGPT conversations whose owners had ticked a discoverable option showed up in search engine results. On July 31 OpenAI said it was removing the option and working to remove indexed content. Read from TechCrunch, Search Engine Journal, The Register, Simon Willison and an OECD.AI record."
categories:
  - Governance
patterns:
  - copy-share-and-export-lose-content
---

**This page is a dated teardown of one public chatbot incident, for teams that let users share chats by link.** It describes what the sources report and what OpenAI said. It makes no claim about anyone's intent. Every fact below comes from a page we opened (listed at the end).

**Read this first.** This is design analysis, not legal or privacy advice. Whether a sharing feature meets privacy law is a question for your own legal team.

## What happened (as reported)

- **Since at least May 2023.** ChatGPT offered shared links, per The Register (August 1, 2025). The Register says documentation from May 2023 said shared links "are not indexed by search engines," and that a later version said users could make them "available to be indexed by search engines." The Register says OpenAI did not respond to its question about when the wording changed.
- **July 31, 2025.** TechCrunch (published 12:23 PM PDT) reported that shared chats could be found in search engines. It describes the steps: the user clicks share, then "create link," then can toggle whether the chat is discoverable. Chats were not public by default. Search Engine Journal, also dated July 31, says the option let search engines such as Google index the chat.
- **July 31, 2025, hours later.** TechCrunch's update (4:10 PM PT) says OpenAI removed the feature. OpenAI's chief information security officer, Dane Stuckey, called it "a short-lived experiment," per Search Engine Journal and The Register. Search Engine Journal says the change was rolling out to all users "through tomorrow morning."
- **August 1, 2025.** The Register reported that a `site:chatgpt.com/share` search no longer returned a list on Google, while Bing returned "thousands of results" and DuckDuckGo and Brave also returned many.

## What the interface did (as reported)

- **Two steps to make a chat searchable.** The user had to create a share link and then turn on the discoverable setting (TechCrunch).
- **The label.** The Register says the option was titled "Make this chat discoverable" in a "Share public link to chat" popup. Simon Willison (August 3) adds that it carried the subtitle "Allows it to be shown in web searches" and was unchecked by default. TechCrunch did not quote the label text.
- **What stayed private.** TechCrunch reports OpenAI said names, custom instructions and later messages stayed private.
- **What users found.** The Register says the reporter saw personal information in some results. TechCrunch lists example topics such as a bathroom renovation, a recipe and a résumé.

## What OpenAI said

All of this is OpenAI's statement as relayed by the outlets. We cannot check it.

- Chats are private unless the user chooses to share them (TechCrunch).
- The feature "introduced too many opportunities for folks to accidentally share things they didn't intend to" (Stuckey, as quoted by Search Engine Journal and The Register). That is the reason OpenAI gave for removing it.
- OpenAI is working to remove indexed content from the relevant search engines (Search Engine Journal, The Register).
- Google's reported position, per TechCrunch: neither Google nor any other search engine controls what pages are made public on the web, and publishers control whether their pages are indexed.

## Where in the flow it broke

The user wanted to send a chat to someone. One extra setting on the share screen also let strangers find it through a search. The sources do not say how many users meant that. OpenAI's own stated reason is that the feature made accidental sharing too likely. Simon Willison's view is that "discoverable" is insider jargon; that is his opinion, not a finding.

## Pattern match

- [Copy, share and export lose content](../goals/chat-interface/failures/copy-share-and-export-lose-content.md) (pattern ID `copy-share-and-export-lose-content`) is the closest page. Its stakes line already names a shared link that shows more than the sender meant. **The match is partial.** That page is mainly about formatting and links lost on copy, share and export. This case is about a share option that exposed more than users may have intended, which is a privacy problem. We found no better page in the failure taxonomy for this case. Treat it as an adjacent case, not a direct match.

## What to measure

Proposed checks for a team with a share-by-link feature. None come from OpenAI. Status: Not yet run.

| Metric | How to compute |
|---|---|
| Share dialogs that state who can see the chat | Share of share dialogs that say, in plain words, who can open the link and whether search engines can find it |
| Public-by-search options off by default | Count of options on the share screen that widen the audience beyond people holding the link, and how many are off by default |
| Comprehension of the option | In a user test, share of participants who can say correctly who can see a chat after they tick the option. Run it on your own users |
| Time to take down | Hours from a share link being deleted or unshared to it no longer being reachable from the open web |

## What a team can change

Proposed rules, each a pass/fail check on a screen or transcript. Status: Not yet run.

1. **Say who can see it, in plain words, next to the control.** Check: the label names the audience ("Anyone on the internet, including search engines") and does not use words like "discoverable" alone.
2. **Make the wider audience a separate, second choice, off by default.** Check: sharing by link and being found by search are two different controls.
3. **Show what is shared before the link is made.** Check: the dialog shows or names the content the link will expose.
4. **Tell the user how to undo it.** Check: the confirmation after sharing shows where to find and delete the link.

## What stays unknown

- How many chats were indexed or exposed. No page we opened gives a count.
- When indexing began and how long the option was live. The sources say "earlier this year" or give only 2023 documentation.
- How completely the content was removed from search engines. The Register reported Bing, DuckDuckGo and Brave still showing results on August 1.
- How many users ticked the option on purpose.
- What the share screen looks like today. We did not test it.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://techcrunch.com/2025/07/31/your-public-chatgpt-queries-are-getting-indexed-by-google-and-other-search-engines/ | TechCrunch | 2025-07-31 | Yes, 2026-10-21, via fetch summary |
| https://www.searchenginejournal.com/openai-is-pulling-shared-chatgpt-chats-from-google-search/552671/ | Search Engine Journal | 2025-07-31 | Yes, 2026-10-21, via fetch summary |
| https://www.theregister.com/2025/08/01/openai_removes_chatgpt_selfdoxing_option/ | The Register | 2025-08-01 | Yes, 2026-10-21, via fetch summary |
| https://simonwillison.net/2025/Aug/3/privacy-design/ | Simon Willison's Weblog | 2025-08-03 | Yes, 2026-10-21, via fetch summary |
| https://oecd.ai/en/incidents/2025-07-30-1ef6 | OECD.AI incidents | 2025-07-30 | Yes, 2026-10-21, via fetch summary (headline list, not full articles) |

All were read through the fetch tool, which returns a summary rather than the raw page. Short quoted phrases are as that tool returned them.

Not opened: eWeek (HTTP 403), The Verge (fetch blocked), Fast Company's original report, and the other outlets named in the OECD.AI page.

Not verified (seen only in search summaries or in the OECD.AI headline list, kept out of the text above): the count "over 4,500" links found by Fast Company and "nearly 4,500" from PC Gamer; the claim that a researcher scraped almost 100,000 conversations; reports of over 100,000 chats still online; the 2025-07-30 start date of Fast Company's coverage; a statement that Google largely cleared its results; and a quote from Google beyond the one in TechCrunch.

## Where sources disagree

- **Google's statement.** TechCrunch (as fetched) includes a Google position; Search Engine Journal and The Register (as fetched) do not.
- **Checkbox wording.** The Register and Simon Willison give the label; TechCrunch's page as fetched quotes none. Simon Willison also gives a subtitle that The Register does not mention.

## Caveats

- Everything is through fetch summaries, not raw pages.
- The date field is TechCrunch's date, July 31, 2025. The OECD.AI page dates its record July 30.
- Simon Willison's post is commentary; we used it only for the label text and marked his views as his own.

## Corrections

If you have a screenshot of the share dialog, OpenAI's original post or a better date, tell us and we will fix this page.
