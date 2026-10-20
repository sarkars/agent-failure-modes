# ISO 24495-1 Plain Language for Chatbots: Relevant, Findable, Understandable, Usable

> **Use it when:** you need a standard to point to, for example in a public-sector or regulated deployment where "write clearly" is too vague for a contract or an audit.

> Status: **framework.** The reading-level threshold is from WCAG 3.1.5; ISO 24495-1 sets no number.

## The idea in one paragraph
ISO 24495-1:2023, *Plain language — Part 1: Governing principles and guidelines*, is the first international plain language standard, developed with the International Plain Language Federation. It defines a text as plain language when its intended readers can easily find what they need, understand what they find, and use that information. It sets four governing principles: the text is relevant, findable, understandable and usable. The standard deliberately does not rely on readability formulas; it judges a text by whether its readers can use it.

## The four principles
| Principle | The question it asks | Chat example |
|---|---|---|
| **Relevant** | Do readers get what they need, and only that? | Answer the question asked, not the whole policy |
| **Findable** | Can they find it quickly? | The answer in the first sentence; steps numbered |
| **Understandable** | Can they understand it? | Common words, short sentences, terms explained |
| **Usable** | Can they act on it? | A next step, a link, or a question that moves the task forward |

## How to use it in a bot
1. Identify the reader for each bot (residents, patients, staff) and what they are trying to do.
2. Check each reply against the four questions above in reviews.
3. Test with real readers, as the standard expects, rather than only with a formula.
4. Use the reading-level check as a cheap early warning, not as proof of compliance.

## Worked example
```
User: how do i renew my parking permit
Bot (not usable): Permit renewals are governed by Municipal Code 12.4 and are processed by the Department.
Bot (usable):     Renew online at the city permits page; it takes about 5 minutes. You'll need your plate
                  number and permit ID. Do you have your permit ID handy?
```

## What the checker flags
Choosing this framework turns on [reading level too high](../goals/accessibility/failures/language-that-is-hard-for-people-with-cognitive-disabilities.md) (Flesch-Kincaid grade above 9 on replies of 40+ words). Whether a reply is relevant, findable and usable needs an AI judge or a reader test.

## Limits
- The standard is paid; only summaries were read for this page.
- A formula can pass text that fails the standard, and the reverse.

## Source
- International Plain Language Federation, [The ISO plain language standard](https://www.iplfederation.org/iso-standard/) (summary by the body that helped develop it; the standard itself was not opened).

## Related
- [Federal plain language guidelines](plain-language-guidelines.md)
- [WCAG reading level](wcag-reading-level.md)
- [All frameworks](README.md)
