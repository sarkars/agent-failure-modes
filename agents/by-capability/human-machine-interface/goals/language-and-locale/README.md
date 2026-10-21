# Language and Locale: Goal, Metrics, and Patterns

> **Goal:** Users are understood and answered in the language, reading level, and format that work for them.

## Why this family exists
People write in the language, register, and format they live in. A reply in the wrong language, at the wrong reading level, or with a wrong name or pronoun costs trust, and in billing, legal, and medical text it can cost money or health. The guidance here is design guidance only. Have native speakers and, where laws apply, counsel review before launch. Written for chat; voice and web signals are planned.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Human-rated accuracy on critical strings | Start over 98%; unverified translations flagged | [unchecked translation in high-stakes text](failures/unchecked-translation-in-high-stakes-text.md) |
| Native-rater appropriateness of register | Start over 90% | [politeness and formality errors](failures/politeness-and-formality-errors.md) |
| Reading grade of replies against a target band | Set per audience; unverified start of roughly grade 6-8 for general consumer content | [reading-level mismatch](failures/reading-level-mismatch.md) |
| Pronoun-handling pass rate; unneeded gender inferences | Unneeded inferences: 0 | [gender and pronoun errors](failures/gender-and-pronoun-errors.md) |
| Intent accuracy on a noisy set vs. clean | Start: gap under 5 points | [typos, shorthand, and noisy input](failures/typos-shorthand-and-noisy-input.md) |
| Appropriate-handling rate; false profanity flags | Starting points on the page | [profanity and slang handling](failures/profanity-and-slang-handling.md) |
| Localization coverage of strings; mixed-language reply rate | Target: 100%; mixed-language replies under 1% | [mixed-language experience](failures/mixed-language-experience.md) |
| RTL render-test pass rate | Target: 100% | [right-to-left and mixed-script rendering](failures/right-to-left-and-mixed-script-rendering.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Unchecked translation in high-stakes text](failures/unchecked-translation-in-high-stakes-text.md) | Machine-translated billing, legal, or medical text goes out with no check and no label |
| [Politeness and formality errors](failures/politeness-and-formality-errors.md) | Wrong formal or informal register in languages that mark it |
| [Reading-level mismatch](failures/reading-level-mismatch.md) | Replies are too dense, or talk down |
| [Gender and pronoun errors](failures/gender-and-pronoun-errors.md) | The bot guesses gender or ignores stated pronouns |
| [Typos, shorthand, and noisy input](failures/typos-shorthand-and-noisy-input.md) | Misspellings and texting shorthand break understanding, or the bot asks for a retype |
| [Profanity and slang handling](failures/profanity-and-slang-handling.md) | The bot warns over mild swearing, or swears back |
| [Mixed-language experience](failures/mixed-language-experience.md) | Part of a reply is in the user's language and part is not |
| [Right-to-left and mixed-script rendering](failures/right-to-left-and-mixed-script-rendering.md) | Arabic and Hebrew replies show with the wrong direction and scrambled numbers |

## Covered in other pages
Emoji and punctuation tone ("k.", "..."): see the example in [sarcasm misread as satisfaction](../../../../by-use-case/support-services/goals/sentiment-escalation/failures/sarcasm-misread-as-satisfaction.md).

Short chat examples were added to existing pages: wrong-language reply and language switch ([language barrier failures](../../../speech-and-audio/goals/conversation-flow/failures/language-barrier-failures.md)), jargon ([response adaptation failure](../../../speech-and-audio/goals/conversation-flow/failures/response-adaptation-failure.md)), locale formats ([input locale mismatch](../../../../cross-cutting/operations/goals/input-output-handling/failures/input-locale-mismatch.md)), names ([name recognition failures](../../../speech-and-audio/goals/speech-recognition/failures/name-recognition-failures.md)), and dialect ([accent dialect bias](../../../speech-and-audio/goals/speech-recognition/failures/accent-dialect-bias.md)).

## Planned (not yet written)
See the [language and locale catalog](../../roadmap/language-and-locale.md) for the rest.

## Related
- [Cultural adaptation](../cultural-adaptation/README.md)
- [Fairness and identity](../fairness-and-identity/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
