# Chatbot Assumes Gender or Uses Exclusionary Terms? Google's Inclusive Language Guide

## The problem
A user asks about returns and the bot replies "It's 30 days, sir." Or it says "crazy fast" or "whitelist". Small word choices like these can make someone feel the product wasn't made for them.

**This page is for you if** you need a practical, maintained word list for product and support text, including the bot's replies.

> Status: **framework.** The rule check below is proposed, not calibrated.

## The framework that fixes it
Google's developer documentation style guide has a section, "Write inclusive documentation", that sets rules for its technical writing. It asks writers to avoid ableist language (such as "crazy", "dumb", "cripple"), to avoid unnecessarily gendered language and default to gender-neutral wording, to avoid violent language where it isn't needed, and to replace terms like "whitelist/blacklist" and "master/slave" with precise alternatives ("allowlist/blocklist", "primary/replica"). The guidance is practical: each term comes with a replacement, which makes it easy to turn into a bot rule.

## The rules
| Rule | Instead of | Use |
|---|---|---|
| No ableist terms | "crazy fast", "dumb mistake", "lame" | "very fast", "simple mistake", a precise word |
| Gender-neutral by default | "guys", "he" for an unknown user, "sir" | "everyone", "they", the user's name |
| Precise technical terms | "whitelist", "blacklist", "master/slave" | "allowlist", "blocklist", "primary/replica" |
| No needless violence | "kill the process", "hit the button" | "stop the process", "select the button" |
| No assumptions | "Your wife can also sign" | "Another account holder can also sign" |

## How to use it in a bot
1. Add the replacement list to the system prompt and to post-processing.
2. Don't assume gender from a name; ask or use neutral wording.
3. Keep exact technical terms when the user's system uses them (an API field called `whitelist`), but don't introduce them.

## Worked example
```
User: whats the return window
Bot (assumes): It's 30 days, sir.
Bot (neutral): It's 30 days from delivery.
```

## What the checker flags
Choosing this framework turns on the non-inclusive language check (shared with [APA bias-free language](apa-bias-free-language.md)): listed terms with replacements, and "sir" or "ma'am" when the user gave no gender cue. The cue check looks for the user's own words, such as "this is Mr. Lee".

## Limits
- Written for documentation; conversation is more personal, so mirror the user's own terms for themselves.

## Source
- Google developer documentation style guide, [Write inclusive documentation](https://developers.google.com/style/inclusive-documentation). Opened.

## Related
- [APA bias-free language](apa-bias-free-language.md)
- [All frameworks](README.md)
