# Chatbot Too Hard to Read? WCAG 3.1.5 Sets a Reading Level

## The problem
Some replies need college-level reading. That shuts out many readers with cognitive disabilities, people reading in a second language, and anyone tired or in a hurry. You need a number to aim for, and a way to measure it.

**This page is for you if** accessibility matters for the bot (public services, health, education), or you need a sourced number for "too hard to read".

> Status: **framework.** This is the one rule in the checker with a sourced threshold.

## The framework that fixes it
The Web Content Accessibility Guidelines (WCAG), from the W3C, include success criterion 3.1.5 Reading Level, at the strictest conformance level (AAA). It says that when text needs a reading ability more advanced than lower secondary education, after removing proper names and titles, supplemental content or a simpler version should be available. W3C's Understanding document defines lower secondary education as roughly 7 to 9 years of school, and lists readability formulas such as Flesch-Kincaid as one way to estimate the level. For a chatbot, the simplest "simpler version" is to write the reply simply in the first place.

## What the criterion asks
| Part | What it means | For a chatbot |
|---|---|---|
| Level | Lower secondary education (about 7-9 years of school) | Aim for replies a 9th grader can read |
| Exceptions | Proper names and titles don't count | Product names, laws and places can stay |
| Remedy | A summary, a simpler version, or illustrations | A plain first sentence, detail on request |
| Measuring | Readability formulas are one accepted estimate | Flesch-Kincaid grade on a sample of replies |

## How to use it in a bot
1. Ask for a plain first reply and offer detail: "Want the full rules?"
2. Run a readability check on sampled replies each week; investigate any grade above 9.
3. Keep proper names and required legal terms, but explain each in plain words the first time.

## Worked example
```
Bot (grade ~20): Supplementary documentation may additionally be requested where exceptional circumstances
                 warrant individualized consideration by the department.
Bot (grade ~5):  We may ask for more papers if your case is unusual. We'll tell you exactly what we need.
```

## What the checker flags
Choosing this framework turns on [reading level too high](../goals/accessibility/failures/language-that-is-hard-for-people-with-cognitive-disabilities.md): a reply of 40 or more words, after removing code blocks and links, with a Flesch-Kincaid grade above 9. Grade = 0.39 × (words per sentence) + 11.8 × (syllables per word) − 15.59. Syllables are estimated by counting vowel groups, so treat grades near 9 as "look at this", not as a verdict.

## Limits
- AAA is the strictest level; most laws require AA, which does not include 3.1.5. Treat this as best practice.
- Formulas don't understand meaning. Short jargon passes; long common words fail.
- Short replies (under 40 words) are skipped because formulas are unstable on them.

## Source
- W3C, [Understanding Success Criterion 3.1.5: Reading Level](https://www.w3.org/WAI/WCAG20/Understanding/reading-level). Opened 2026-10-20.

## Related
- [Federal plain language guidelines](plain-language-guidelines.md)
- [ISO 24495-1 plain language](iso-24495-plain-language.md)
- [Accessibility in chat](../goals/fairness-and-identity/failures/accessibility-in-chat.md)
- [All frameworks](README.md)
