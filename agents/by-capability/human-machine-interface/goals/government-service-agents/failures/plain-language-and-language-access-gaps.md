# Government Chatbot Only in English or Too Dense to Read: Plain-Language and Language Access Gaps

<!-- SEO
title: Government Chatbot Plain Language and Language Access Gaps
description: A public-service chatbot that gives program rules in dense text, or only in English, shuts people out. Offer plain language and the languages the agency requires.
search phrases:
- government chatbot plain language
- language access chatbot LEP
- limited English proficiency chatbot government
- benefits chatbot Spanish
- government ai chatbot only in english
- plain language benefits rules chatbot
- multilingual government chatbot design
-->

**Frequency**: Common

## Issue: A public-service chatbot gives program rules in dense text, or only in English, so people who read slowly or in another language cannot use the answer; offer plain language and the languages the agency is required to serve.

> **Read this first.** This page is design guidance, not legal advice. Language-access duties depend on the agency, the program, the funding source, and the state, and the federal rules changed in 2025 (see section 4). It has not had review by counsel, a language-access office, or qualified translators; get that review before use. Where this page states what a law or order says, that is only as far as the sources linked in section 4, which I opened.

> **One line:** The bot answers a program question in a wall of jargon, or only in English, and the person who needed it most cannot read it.

| | |
|---|---|
| **Channel** | Written for **chat** (text). Signals and rules for voice, such as interpreter lines and spoken language choice, are PLANNED, not written or measured. |
| **Stakes** | High. The text is about benefits, deadlines, and notices. |
| **Who is affected** | People with limited English proficiency (LEP), people with low literacy or cognitive disabilities, and anyone reading under stress or in a second language |
| **Frequency** | Common by our judgment. I found no count of how often public-service chatbots fail this way. |
| **Pattern ID** | plain-language-and-language-access-gaps |
| **Family** | [Government service agents](../README.md) |
| **Goal** | Public-service agents give accurate, accessible, plain-language guidance and always leave a path to a person and an appeal. |
| **Primary metric** | Reading level of replies and access in the required languages. Both targets are set by the agency. Starting point to tune (labeled, not sourced for chat): replies at or below grade 8 on a readability formula, and 100% of the agency's required languages covered by reviewed program text. |
| **Maturity** | Researched. Flagged **L** (legal): counsel review needed. Flagged **R**: translators and language-access staff must review. Tests not yet written. |
| **Will a better model fix this?** | Partly. A stronger model writes plainer text and translates better, but which languages are required, and whether program text was reviewed, are agency decisions. (Our judgment, not tested.) |
| **Also searched as** | government chatbot plain language · language access chatbot · LEP chatbot · benefits chatbot in Spanish · chatbot English only · plain writing government AI |

## 1. In plain words
A person asks a government chat how a program works. The bot answers in the words of the rule book, or only in English. The fix has two parts: write the answer in plain language, and offer it in the languages the agency is required to serve, using program text that people have checked. When it cannot do that, it says so and gives a route to a person who can.

## 2. What it looks like
Illustrative scenario (not a real incident): a state benefits chat.

**Without the fix**
```
User: (in Spanish) Cuanto tiempo tengo para responder a la carta del programa de alimentos?
Bot:  Per program regulations, recertification documentation must be submitted prior to the
      expiration of the certification period, absent good cause for an extension.
User: no entiendo
Bot:  Please contact your local office for further assistance.
```

**With the fix**
```
User: (in Spanish) Cuanto tiempo tengo para responder a la carta del programa de alimentos?
Bot:  Mire la fecha en su carta: esa es su fecha limite. Si no puede cumplirla, llame a la oficina antes de esa fecha.
      [Texto revisado por el programa, 3 de marzo. Si algo no esta claro, puedo conectarlo con una persona que habla espanol.]
      Quiere que le explique que documentos enviar, o prefiere hablar con una persona?
      [Documentos] [Hablar con una persona] [Otra cosa]
```
The fixed reply answers in the user's language, uses short plain sentences, shows that the program text was reviewed and when, and offers a person.

## 3. Why it happens
These are our reading of the pattern.
- **The source text is dense.** The bot repeats or lightly paraphrases program rules and notices written for lawyers and caseworkers, and nobody tells it to rewrite them.
- **Language support stops at the model.** The model can answer in many languages, so the product ships with English-only program text and no list of the languages the agency must serve. That makes the Spanish or Vietnamese answer an on-the-fly translation of unreviewed text.
- **Nobody owns the target.** No one sets a reading level or a language list for the bot, so nothing is tested against one.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The Plain Writing Act of 2010 says its purpose is to improve federal agencies' effectiveness and accountability "by promoting clear Government communication that the public can understand and use." It defines a covered document as one that is needed to get a federal benefit or service, or explains one, in paper or electronic form; regulations are excluded. | [Plain Writing Act of 2010, Public Law 111-274 (govinfo)](https://www.govinfo.gov/content/pkg/PLAW-111publ274/html/PLAW-111publ274.htm). Opened and read. | Applies to federal executive agencies. I did not find a source that says whether a chatbot reply is a "covered document," so I make no claim either way. State and local agencies are not covered by this law. |
| Digital.gov's plain-language guide says the Act "established the requirement that content for the public is written for its specific audience." | [Digital.gov, Plain language guide](https://digital.gov/guides/plain-language) (the old plainlanguage.gov/law address redirects there). Opened and read. | A short summary page; it does not list the covered documents. |
| Title VI of the Civil Rights Act of 1964 "prohibits discrimination on the basis of national origin (language) by entities that receive federal funds," and Executive Order 13166 (2000) required federal agencies to plan for "meaningful access" for LEP persons. | [Justice Department, Fifteen Questions for the Fifteenth Anniversary of EO 13166, 2015](https://www.justice.gov/crt/fcs/newsletters/summer-2015/FIFTEEN%20QUESTIONS%20FOR%20THE%20FIFTEENTH%20ANNIVERSARY%20OF%20EXECUTIVE%20ORDER%2013166). Opened and read. | A 2015 federal explainer, now dated. It is not a legal opinion on chatbots. |
| **Federal status changed in 2025.** Executive Order 14224 says Executive Order 13166 is "hereby revoked," says "nothing in this order, however, requires or directs any change in the services provided by any agency," and tells the Attorney General to rescind guidance issued under 13166 and issue updated guidance consistent with applicable law. The Justice Department's LEP page says it "temporarily suspended the operations of lep.gov" pending internal review (page last updated July 17, 2025). | [EO 14224, American Presidency Project copy](https://www.presidency.ucsb.edu/node/376525); [Justice Department LEP page](https://www.justice.gov/crt/limited-english-proficiency). Both opened and read. | I did not open the Federal Register text or any court or agency reading of what duties remain under Title VI or state law. Check current guidance with counsel. State laws may impose their own language-access duties; I opened none. |
| A Rutgers Bloustein School report looked at a bilingual (English and Spanish) retrieval-grounded chatbot for New Jersey SNAP information. The page says chatbots on other states' SNAP sites perform inconsistently in Spanish. The audit covered 56 state and territory SNAP websites. | [Rutgers Bloustein School, report page](https://bloustein.rutgers.edu/?p=76216). Opened the page; **did not open the full report**, so I give the page's own summary only. | Page summary of a report I did not read. It reports no accuracy figures, and I cite no results beyond the 56-site count. |

I found no controlled study of how LEP residents or low-literacy users do with government chatbots. A Digital Government Hub paper that I saw only in search results (it reports that LEP workers are less likely to receive unemployment benefits) was **read through a summary only**, so it is kept out of the fix.

**Public incident.** No public incident found for plain-language or language-access failures in a government chatbot. I ran four searches (government chatbot plain language and LEP; Plain Writing Act; EO 13166 and Title VI; EO 14224) and they returned legal framework pages and a report, not a dated incident. For an adjacent case of confident wrong guidance from a government bot, see the NYC MyCity case in [eligibility answers sound like decisions](eligibility-answers-sound-like-decisions.md).

## 5. The fix

**The principle:** Answer in plain words, in the language the person uses, from program text a qualified person has reviewed in that language; if there is none, say so and offer a person.

**Do this**
1. **Keep a language list set by the agency.** The bot offers the languages on the agency's required list. Which languages those are is the agency's decision with counsel; the bot does not choose.
2. **Reply in the user's language when it is on the list.** If the user writes in a listed language, answer in it, and keep it for the whole conversation. Offer a switch at the start ("English / Espanol / Other").
3. **Use reviewed program text for rules, deadlines, amounts, and notices.** For those strings, use text a qualified translator approved. If none exists in the user's language, say the translation is not reviewed, show the original beside it, and offer a person ([unchecked translation in high-stakes text](../../language-and-locale/failures/unchecked-translation-in-high-stakes-text.md)).
4. **Write plain.** Put the answer first; one idea per sentence; "you" and active voice; common words, with the program term in parentheses the first time. Check each reply against the agency's reading-level target ([plain language guidelines](../../../solutions-library/plain-language-guidelines.md)).
5. **Define a term once, then use it the same way.** Do not swap "recertification," "renewal," and "review" for one thing.
6. **Check it landed.** After a rule or deadline, offer a short check ("Want me to say it another way?") and rephrase more simply when the user says they do not understand ([teach-back](../../../solutions-library/teach-back.md)).
7. **Never give the date or amount in words only from memory.** Quote the figure from the current source with its date.
8. **Offer a person who can help in that language.** If the agency has an interpreter or a multilingual line, name it in the reply. If it does not, say what the person can do next.
9. **Do not ask the user to translate or to bring someone.** Do not tell a person to find a family member to read the reply.

**Reference design: language and reading-level plan**
| Part | Content |
|---|---|
| Languages | The agency's required list, set by the agency, with the date it was last reviewed |
| Program text | Per language: reviewed or unreviewed, reviewer, review date |
| Reading target | Set by the agency; starting point grade 8 or below (labeled, to tune) |
| Unreviewed text | Label as unreviewed, show the original, offer a person |
| Route | Interpreter line, bilingual caseworker, or office, per language |

```
Answer in the language the user writes in, if it is on the agency's list. Offer a language choice at the start.
For rules, deadlines, amounts, and notices, use the reviewed text for that language. If there is none, say the translation is not reviewed, show the original, and offer a person.
Write short sentences with the answer first. Use "you". Explain each program term once in plain words.
After a deadline or rule, offer to say it another way. Always name a person route for the user's language.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every rule or deadline: the answer comes first, in plain words and the user's language. Do not use it when the bot does not yet know which language the user wants. |
| Admit uncertainty and show how to check | The program text in the user's language is not reviewed: say so, show the original, and say how to confirm. |
| Offer choices: 2-4 options plus "Something else", free text open | At the start, or after "I don't understand": "English", "Espanol", "Talk to a person", "Something else". Do not offer them when the user has already written in one language. |
| Hand off to a person | The user's language is not on the list, the user says twice they do not understand, or the question is about a deadline or notice. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Do not oversimplify until the answer is wrong, and do not drop a legal term that the notice itself uses; explain it. Do not switch the user's language because the bot guessed. Do not claim a translation is reviewed unless it is. Do not offer a long language menu that hides the answer.

**Hand-off rule.** Hand off to a person who can help in the user's language, or to the agency's interpreter route, when the language is not on the list, when two rephrasings did not work, or when the question concerns a deadline or notice. Pass the language and a summary ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** [plain language guidelines](../../../solutions-library/plain-language-guidelines.md), [ISO 24495-1 plain language](../../../solutions-library/iso-24495-plain-language.md), [WCAG reading level](../../../solutions-library/wcag-reading-level.md).

## 6. How to test it (short version)
The full test file is **not yet written**. These scenarios are designs; results: **Not yet run**.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | A user writes in a listed language and asks about a deadline | The reply is in that language, uses reviewed text, and names a person route (rules 2, 3, 8) |
| 2 | A user writes in a language not on the list | The bot says so plainly and offers a person (rule 1, hand-off) |
| 3 | No reviewed text exists in the user's language | The reply says the translation is not reviewed and shows the original (rule 3) |
| 4 | A dense rule from the source text | The reply puts the answer first and meets the agency's reading target (rule 4) |
| 5 | The user says "I don't understand" | The bot rephrases more simply once, then offers a person (rule 6) |
| 6 | The same term appears in two replies | The same word is used for the same thing (rule 5) |
| 7 | A date or amount is asked for | It comes from the source with its date (rule 7) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given. The agency sets the final targets.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Replies meeting the reading-level target** (primary, part 1) | Agency sets; starting point 95% at grade 8 or below (unverified for chat) | Readability formula on replies, plus sampled review | Below 90% |
| **Required languages with reviewed program text** (primary, part 2) | 100% of the agency's list | Inventory of program text by language, reviewer, and date | Any listed language below 100% |
| Replies in the user's language when it is listed | Over 98% | Language detection on user and reply turns | Below 95% |
| Unreviewed translations labeled | 100% | Replies that use unreviewed text and carry the label | Any unlabeled |
| "I don't understand" followed by a person offer | Over 95% | Events after a repeated confusion signal | Below 90% |
| Wrong-language or mixed-language replies (counter-metric) | Under 1% | Language detection plus sample | Over 3% |
| Oversimplified answers (counter-metric) | Under 5% | Expert-reviewed sample for lost meaning | Over 10% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. They are written for text; voice signals (interpreter use, spoken language switches) are PLANNED.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| User writes in a listed language, reply is in English | Language detection on user and reply turns | The user asked for English or pasted English text |
| Reply to a rule question is above the reading-level target | Readability score on the reply | The reply quotes a notice or form field the user asked about |
| User replies "no entiendo", "I don't understand", or repeats the question | Same intent in the next turn | A deliberate rephrase to be precise |
| Program text used in the reply has no reviewed flag for that language | Retrieval event with language and review status | A greeting or menu with no program rules |
| User's language is not on the list and there is no person offer | Language detection plus handoff event | The user switched to a listed language |

**Starter rule:** reply in the user's language when it is on the agency's list, using reviewed program text written in plain words, and name a person route for that language.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: plain-language-and-language-access-gaps
runs: pre_send
reads: [draft_reply, user_language, agency.language_list, retrieved_text.language, retrieved_text.review_status, draft_reply.reading_grade]
trigger: a reply about a program rule, deadline, or notice is about to be sent
moves: [lead_with_answer, admit_uncertainty, offer_choices, hand_off]
choices: ["English", "Espanol", "Talk to a person", "Something else"]
on_miss: rewrite
metric: replies meeting the reading-level target and required languages with reviewed text
counter_metric: wrong-language or mixed-language replies
status: proposed
```

## 8. Related patterns
- [Eligibility answers sound like decisions](eligibility-answers-sound-like-decisions.md): the sibling page; it covers who decides, this page covers whether the person can read the answer.
- [Unchecked translation in high-stakes text](../../language-and-locale/failures/unchecked-translation-in-high-stakes-text.md): the closest pattern. It covers machine translation with no check in billing, legal, and medical text in any product; this page covers the public-agency setting, with language-access duties and a list of languages set by the agency.
- [Reading-level mismatch](../../language-and-locale/failures/reading-level-mismatch.md): matches reply level to any reader; this page adds an agency-set target for program rules.
- [Mixed-language experience](../../language-and-locale/failures/mixed-language-experience.md): replies that switch languages without cause.
- [Cold transfer](../../human-handoff/failures/cold-transfer.md): what to pass to the person who helps.

## 9. Common questions
### Does a government chatbot have to answer in languages other than English?
It depends on the agency, the program, its funding, and state law, and the federal position changed in 2025 (section 4). This page is not legal advice; ask counsel. The sources I opened say Title VI bars national-origin discrimination by recipients of federal funds, and that EO 13166 was revoked by EO 14224 without a direct order to change services.

### What reading level should a government chatbot use?
The Plain Writing Act asks federal writing to be clear for its audience; it sets no grade. The grade 8 starting point here is a labeled guess to tune, not a legal number.

### Can a chatbot just machine-translate the program rules?
For rules, deadlines, and amounts, use text a qualified translator has reviewed. Otherwise say the translation is not reviewed and offer a person.

### Is a language-access chatbot the same as an interpreter?
No. The bot gives written guidance; a person still helps with cases, disputes, and notices.

---
## Technical section

### T1. Solution architecture
```
user turn -> language detect -> agency language list check -> retrieve program text (language, review status, date)
          -> draft -> readability check -> label if unreviewed -> send, or route to a person
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Rules, deadlines, and amounts come from reviewed text or carry the unreviewed label | Retrieval and template | Log check |
| Language list comes from agency configuration, not the model | Config | Config review |
| Draft above the reading target is rewritten once | Pre-send check | Readability log |

### T3. Evals
- **Dataset:** starting set of 60 program questions per listed language, with the reviewed answer and the source text; built with the agency's translators.
- **Judge rubric:** correct language, answer first, reading target met, unreviewed label present, person route named.
- **Metrics and starting thresholds:** the table in section 7; starting points to tune.
- **Release gate:** block a deploy when a listed language has no reviewed text for a core rule.

### T5. Trade-offs
- Reviewed text in each language costs money and upkeep when rules change; stale reviewed text is worse than a labeled one.
- A strict reading target can strip needed legal terms; test for lost meaning.

---
### Deep dive
- **Open questions.** I did not find whether a chatbot reply counts as a "covered document" under the Plain Writing Act, or what duties remain under Title VI or state law after EO 14224. Counsel must answer both.
- **Sources blocked or not opened.** The Federal Register copy of EO 14224 redirected to a block page, so I used the American Presidency Project copy. The Rutgers full report was not opened. The Digital Government Hub paper was read through a summary only.
- **Voice.** PLANNED: spoken language choice, interpreter handoff, and text-to-speech reading level. Not written or measured here.
- **References.** [Plain Writing Act (govinfo)](https://www.govinfo.gov/content/pkg/PLAW-111publ274/html/PLAW-111publ274.htm); [Digital.gov](https://digital.gov/guides/plain-language); [DOJ, 2015](https://www.justice.gov/crt/fcs/newsletters/summer-2015/FIFTEEN%20QUESTIONS%20FOR%20THE%20FIFTEENTH%20ANNIVERSARY%20OF%20EXECUTIVE%20ORDER%2013166); [EO 14224](https://www.presidency.ucsb.edu/node/376525); [DOJ LEP page](https://www.justice.gov/crt/limited-english-proficiency); [Rutgers](https://bloustein.rutgers.edu/?p=76216).
