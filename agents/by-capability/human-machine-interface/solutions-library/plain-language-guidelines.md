# Plain Language for Chatbots: The US Federal Plain Language Guidelines

> **Use it when:** the bot serves the general public, explains rules, money or health, or its users read in a second language.

> Status: **framework.** The reading-level threshold comes from WCAG 3.1.5, not from these guidelines, which give no number.

## The idea in one paragraph
The Federal Plain Language Guidelines were written by PLAIN, a group of US federal employees, to support the Plain Writing Act of 2010. Their core advice is to write for your audience and the task they are trying to do: organize around the reader's questions, use "you" and active voice, prefer short sentences and common words, put the main point first, and test the text with real readers. A chatbot is a plain-language writer that never gets edited, so it needs these rules built in.

## The main rules
| Rule | What it means | Chat example |
|---|---|---|
| Write for the reader | Answer the question they asked, in their words | "You can apply online" not "Applications may be submitted electronically" |
| Use "you" and active voice | Say who does what | "We'll email you" not "Notification will be sent" |
| Short sentences | One idea per sentence | |
| Common words | "use" not "utilize", "before" not "prior to" | |
| Main point first | See [answer first](answer-first-bluf-pyramid.md) | |
| Lists for steps | Number steps the user must follow in order | |
| Test it | Check real users understand | See [teach-back](teach-back.md) |

## How to use it in a bot
1. Put a plain-language rule set in the system prompt, with a short list of words to avoid and their plain swaps.
2. Keep reply sentences short; split any sentence with two "and"s.
3. After instructions, check understanding with [teach-back](teach-back.md), not "Does that make sense?"
4. Measure reading level on a sample of replies (see below).

## Worked example
```
User: am i eligible for help with rent
Bot (dense): Eligibility determinations necessitate comprehensive documentation substantiating applicants'
      circumstances, including verification of household composition, remuneration and residency.
Bot (plain): You may be. We need to see who lives with you, what you earn, and where you live.
      Can you send a pay slip and a bill with your address?
```

## What the checker flags
Choosing this framework turns on [reading level too high](../goals/accessibility/failures/language-that-is-hard-for-people-with-cognitive-disabilities.md): a reply of 40 or more words with a Flesch-Kincaid grade above 9. Grade 9 comes from [WCAG 3.1.5](wcag-reading-level.md) (lower secondary education). Code blocks and links are skipped.

## Limits
- Readability formulas count syllables and sentence length; they cannot see jargon that is short ("lien", "APR") or text that is simple but wrong.
- The syllable count is an estimate, so a grade near the threshold is a prompt to look, not a verdict.

## Source
- PLAIN, [Federal Plain Language Guidelines](https://webarchive.library.unt.edu/web/20121006190813mp_/http:/www.plainlanguage.gov/howto/guidelines/FederalPLGuidelines/TOC.cfm) (archived copy; the live plainlanguage.gov site blocked automated access).

## Related
- [ISO 24495-1 plain language](iso-24495-plain-language.md)
- [WCAG reading level](wcag-reading-level.md)
- [All frameworks](README.md)
