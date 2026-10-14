# Roadmap: Language and Locale Failures

> **Family goal:** Users are understood and answered in the language, reading level, and format that work for them.

**Context (verified):** About 22% of Americans age 5 and older spoke a language other than English at home in the 2017-2021 ACS (released June 2025), so language handling is a core need for US products, not a niche. Source: [Census Bureau](https://www.census.gov/newsroom/press-releases/2025/2017-2021-acs-language-use-tables.html). Speaking another language at home does not mean limited English proficiency.

Flags: **V** verified source · **R** needs research · **L** legal review · **E** expert review. See the [roadmap README](README.md).

| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags |
|---|---|---|---|---|---|
| LG-01 | Wrong-language reply | A user writes in Spanish and the bot answers in English, or the reverse | Reply in the language the user is using, unless they ask otherwise | Language-match rate. Start: over 98% | |
| LG-02 | Code-switching breakage | A user mixes languages in one message and the bot misreads it | Mixed-language input is understood as well as single-language input | Intent accuracy on a code-switched set vs. monolingual. Start: gap under 5 points | E |
| LG-03 | Language switch ignored | The user asks to switch language mid-chat and the bot doesn't, or switches back | A requested switch holds for the rest of the conversation | Switch-persistence rate. Start: over 95% | |
| LG-04 | Unchecked translation in high-stakes text | Machine translation errors in billing, legal, or medical content | Critical content is accurate in every supported language | Human-rated accuracy on critical strings. Start: over 98%; unverified translations flagged | E |
| LG-05 | Politeness and formality errors | Wrong formal or informal address or register in languages that mark it | Register fits the language and context | Native-rater appropriateness. Start: over 90% | R, E |
| LG-06 | Reading-level mismatch | Replies are too complex, or condescending | Replies fit the user's reading level and the topic | Reading grade of replies against a target band, with user comprehension checks. Start: roughly grade 6-8 for general consumer content (unverified; check plain-language guidance) | R |
| LG-07 | Jargon, acronyms, and idioms | Undefined terms and figures of speech confuse users | Plain words by default; terms defined when needed | Undefined-acronym rate under 2%; idiom rate under 1% | |
| LG-08 | Locale format errors | Ambiguous dates (04/05), currency, units, time zones, or phone and address formats | Formats match the user's locale and are unambiguous | Locale-format correctness on a test set. Target: 100%; ambiguous dates: 0 | |
| LG-09 | Name and transliteration errors | Names are mangled, "corrected", or put in the wrong order; diacritics dropped | Names are preserved exactly as given | Name-preservation rate. Target: 100% | |
| LG-10 | Gender and pronoun errors | The bot assumes gender, or misuses a person's stated pronouns, in gendered languages or in English | The bot uses stated pronouns and infers none | Pronoun-handling pass rate; unneeded gender inferences: 0 | E |
| LG-11 | Dialect and slang misreading | Regional dialects, slang, or non-standard varieties are misunderstood or "corrected" | Dialects are accepted as valid input | Intent accuracy parity across dialect test sets. Start: within 3 points. Related to the [fairness pattern](../core/fairness-and-identity/failures/dialect-and-name-quality-gap.md) | |
| LG-12 | Typos, shorthand, and noisy input | Texting shorthand, typos, and voice-to-text errors break understanding | Noisy input is understood nearly as well as clean input | Intent accuracy on a noisy set vs. clean. Start: gap under 5 points | |
| LG-13 | Emoji and punctuation tone misreads | "k.", "...", ALL CAPS, or emoji are read as the wrong mood | Tone cues are read the way people mean them | Agreement with human raters on tone. Start: over 85% | R |
| LG-14 | Profanity and slang handling | The bot over-reacts to mild swearing, or echoes it | Proportionate response; no refusal over harmless language, no mimicry | Appropriate-handling rate; false profanity flags | |
| LG-15 | Mixed-language experience | Parts of the interface or bot are translated and parts aren't | A supported language is fully supported | Localisation coverage of strings. Target: 100%; mixed-language reply rate under 1% | |
| LG-16 | Right-to-left and mixed-script rendering | Arabic, Hebrew, or mixed-script text renders wrongly | Text displays correctly in every supported script | RTL render-test pass rate. Target: 100% | |
