---
title: "ChatGPT Stops Mid-Reply When Asked to Write \"David Mayer\" and Other Names"
date: 2024-12-02
source: "https://techcrunch.com/2024/12/03/why-does-the-name-david-mayer-crash-chatgpt-digital-privacy-requests-may-be-at-fault"
summary: "In early December 2024 ChatGPT broke off with an error when asked to write the name David Mayer and at least five other names; OpenAI said an internal privacy tool had flagged the name, and David Mayer worked again within about a day. All sources were read through fetch summaries."
categories:
  - General-Purpose Assistants
  - Governance
patterns:
  - generic-error-messages
  - over-refusal-of-ordinary-requests
---

**This page is a dated teardown of one public incident, for teams that run name or privacy filters on a chat assistant's output.** It is built from press reports, a blog post and a user forum thread, not from a test of ChatGPT. Every fact below comes from a source we opened (listed at the end).

**Status: Needs review.** Every source was read through a fetch-tool summary, not as a full page. We could not open The Guardian or Ars Technica. Details seen only in search-result summaries are kept out of the claims and listed under "What we could not verify."

**Read this first:** this is not legal advice; legal reading needs review. Sources mention privacy requests, a GDPR "right to be forgotten" request and false claims about real people. We report what they say and draw no legal conclusions.

## What happened (as reported)

- **December 2, 2024.** A user on the OpenAI Developer Community forum posted that sending or receiving the name "David Mayer" was "often resulting in an error." This is the earliest dated report we opened.
- **The behavior.** TechCrunch (Devin Coldewey, Dec. 3) says ChatGPT would "fail or even break off mid-name" and reply "I'm unable to produce a response," if it said anything at all. Simon Willison (Dec. 3) says ChatGPT "stops output with an error" instead of writing the names.
- **Other names.** TechCrunch, Willison and ZME Science (Mihai Andrei, Dec. 4) all list Brian Hood, Jonathan Turley, Jonathan Zittrain, David Faber and Guido Scorza. TechCrunch says the list was not exhaustive.
- **Images too.** ZME Science says ChatGPT also refused to generate images using these names. No other source we opened reports this.
- **Scope.** Willison writes that "The OpenAI API is entirely unaffected," so the failure was in the consumer ChatGPT apps.
- **OpenAI's statements.** ZME Science quotes OpenAI's statement to The Guardian: "One of our tools mistakenly flagged this name and prevented it from appearing in responses, which it shouldn't have. We're working on a fix." TechCrunch's update says OpenAI confirmed "David Mayer" was flagged by internal privacy tools and said: "There may be instances where ChatGPT does not provide certain information about people to protect their privacy." OpenAI gave no further detail on the tools or process, per TechCrunch.
- **The fix.** ZME Science says "David Mayer" worked again less than a day after the reports. TechCrunch says the other names still crashed while it was writing.
- **Reported explanations (not confirmed).** TechCrunch calls its own theory "just our own speculation": a list of people needing "special handling," possibly corrupted. TechCrunch and ZME Science note Brian Hood, an Australian mayor, objected after ChatGPT falsely described him as the perpetrator of a crime. ZME Science says Turley wrote about being falsely accused of sexual harassment by ChatGPT, and that Scorza said on Twitter he had filed a GDPR right-to-be-forgotten request. ZME Science adds that this theory does not explain every name.

## What the user experienced

- A user asks ChatGPT to write an ordinary name. The reply stops partway, sometimes mid-name, and shows an error such as "I'm unable to produce a response" (TechCrunch).
- The forum page links a separate thread on David Faber whose excerpt shows "Something went wrong while generating the response." That text does not say the name was the cause.
- Our reading: the error looked like a system fault, not a policy decision. Users found the trigger themselves; the forum poster tied it to the name, and TechCrunch says more names surfaced as people tried others.
- No message said a privacy rule applied or offered another way to get the answer. The privacy reason came later, from OpenAI's statement to the press.

## Pattern match

- **[Generic error messages](../goals/errors-and-recovery/failures/generic-error-messages.md)** (taxonomy: on failure the assistant shows a catch-all message with no cause the user can act on and no next step). A strong fit. A deliberate filter was shown to users as a crash. The message gave no cause, and retrying could never help.
- **[Over-refusal of ordinary requests](../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md)** (taxonomy: the assistant declines a safe, common request because a word in it resembles a risky one). A partial fit. Writing a common name like "David Mayer" is ordinary, and OpenAI said the tool flagged it "mistakenly." But it was not a visible refusal, and for some names the block may have been intended. We do not judge whether it was.
- **Where it does not fit.** We found no report of harm beyond blocked replies, and no lost conversations.

## What to measure and what to change

Proposed checks, each pass/fail on a test transcript or output log. Status: Not yet run. None come from ChatGPT.

1. **Filter hits are not errors.** Pass: when an output filter blocks text, the user sees a message that says content was withheld. Fail: a generic error or a reply cut off mid-word.
2. **No cut-off mid-reply.** Pass: a blocked reply is either withheld whole or rewritten. Fail: a reply that stops partway through a name.
3. **Next step.** Pass: a blocked reply says what the assistant can still do (for example, answer without that name).
4. **Shared-name test set.** Pass: a test set of common names that match blocked entries returns normal replies for the common uses. Any block on a name that only shares spelling counts as a fail.
5. **Same rule across surfaces.** Pass: a name rule gives the same documented behavior in chat, image generation and the API, or the difference is written down.
6. **Log and review.** Count filter-triggered stops per name per day. A spike on one name gets a human review within one business day.

## What we could not verify

- The Guardian's report. Search summaries say it quoted the error "I'm unable to produce a response" and said OpenAI declined to comment on a right-to-be-forgotten link. The site blocked our fetch.
- Ars Technica's report (Benj Edwards, Dec. 3, 2024), linked from Willison's post. The site blocked our fetch.
- When the problem began. Search summaries mention reports "over the weekend" before Dec. 2; no opened source dates the start.
- Which David Mayer was meant. TechCrunch describes a late academic whose name was used as an alias by a wanted man; search summaries say another outlet "understood" the glitch was unrelated to him. ZME Science says a David Mayer told The Guardian he never contacted ChatGPT; we could not confirm which person that was.
- Whether the other five names were later fixed. No opened source says.
- Search summaries say Hood "settled with OpenAI out of court." TechCrunch says his lawyers contacted OpenAI but no lawsuit was filed. We do not claim a settlement.
- The cause of any block. OpenAI named a privacy tool for "David Mayer" only; reasons for the other names are reporters' inferences.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://techcrunch.com/2024/12/03/why-does-the-name-david-mayer-crash-chatgpt-digital-privacy-requests-may-be-at-fault | TechCrunch (Devin Coldewey) | 2024-12-03 | Yes, 2026-10-22, fetch-tool summary |
| https://zmescience.com/science/news-science/chatgpt-david-mayer-other-names-crashing | ZME Science (Mihai Andrei) | 2024-12-04 | Yes, 2026-10-22, fetch-tool summary |
| https://simonwillison.net/2024/Dec/3/names-make-chatgpt-grind-to-a-halt/ | Simon Willison's blog | 2024-12-03 | Yes, 2026-10-22, fetch-tool summary |
| https://community.openai.com/t/david-mayer-bug-triggers-error-sending-his-name-or-when-reciving-it/1039406 | OpenAI Developer Community | 2024-12-02 | Yes, 2026-10-22, fetch-tool summary |
| The Guardian report on the David Mayer glitch | The Guardian | 2024-12-03 (per search summaries) | No. Fetch blocked by the site |
| Ars Technica, "Certain names make ChatGPT grind to a halt, and we know why" | Ars Technica (Benj Edwards) | 2024-12-03 | No. Fetch blocked by the site |
| Deccan Herald explainer | Deccan Herald | Not known | No. HTTP 403 |
| Diplo Digital Watch update | Digital Watch Observatory | Not known | No. HTTP 403 |
