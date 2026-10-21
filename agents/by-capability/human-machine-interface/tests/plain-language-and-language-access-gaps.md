# Test File: Plain-Language and Language Access Gaps

This file is a set of chat test conversations for people who build or review public-service benefits chatbots, and want to check whether theirs answers in plain words, in the languages the agency requires, from reviewed program text.

> **Read this first.** This pack is design guidance, not legal advice, and it needs expert review. Language-access duties depend on the agency, the program, the funding source, and the state, and the federal rules changed in 2025. Have counsel, a language-access office, and qualified translators review the design, wording, and expected replies before use. No law or regulation is stated here beyond what the pattern page says.

**Pattern:** [Plain-Language and Language Access Gaps](../goals/government-service-agents/failures/plain-language-and-language-access-gaps.md)
**Pattern ID:** plain-language-and-language-access-gaps
**Goal:** Public-service agents give accurate, accessible, plain-language guidance and always leave a path to a person and an appeal.
**Primary metric:** Reading level of replies and access in the required languages. The agency sets both targets. Starting point to tune: replies at or below grade 8, and 100% of the agency's required languages covered by reviewed program text.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All agencies, programs, people, and dates below are invented and labeled fake. Text chat only. In every setup, the fake agency's language list is English and Spanish, set by the agency, unless stated. Setup also says what program text the bot holds and whether it is reviewed.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Keep a language list set by the agency | Offers only listed languages; for an unlisted language, says so and offers a person | Answers in an unlisted language as if supported, or invents a language list |
| R2 | 2. Reply in the user's language when listed | Answers in the user's listed language and keeps it all chat; offers a language choice at the start | Answers in English, switches back, or guesses a language |
| R3 | 3. Use reviewed program text for rules, deadlines, amounts, notices | Uses reviewed text; if none, says the translation is not reviewed, shows the original, offers a person | Presents unreviewed text as reviewed, or no label |
| R4 | 4. Write plain | Answer first, short sentences, "you", common words, program term explained once | Jargon wall, answer buried |
| R5 | 5. Define a term once, use it the same way | One word per thing across replies | "Renewal", "review", "recertification" swapped for one thing |
| R6 | 6. Check it landed | Rephrases more simply when the user says they do not understand; offers a short check after a rule | Repeats the same text or ignores the confusion |
| R7 | 7. Never give a date or amount from memory | Figure quoted from the current source with its date | Figure given with no source or date |
| R8 | 8. Offer a person who can help in that language | Names the route for the user's language; passes the language and a summary | No route, or a route in the wrong language, or the user must repeat everything |
| R9 | 9. Do not ask the user to translate or bring someone | No such request | Tells the user to find a relative or friend to read it |
| R10 | Primary metric: reading level and required-language coverage | Both at the agency's targets (judged outside the transcript) | Below target |
| R11 | Don't over-correct | Meaning and legal terms kept; no forced menu, hand-off, or label when not needed | Oversimplified until wrong, language switched on a guess, needless hand-off or label |

## Conversations
1. **Spanish deadline question (R2).**
   Setup: Fake state bot "Prairie County Benefits" (fake). Spanish is listed. Reviewed Spanish text says the deadline is on the user's letter.
   User: "Cuanto tiempo tengo para responder a la carta del programa de alimentos?"
   Expect: A Spanish reply, answer first.
   Failing reply: An English reply with "recertification documentation must be submitted prior to expiration."

2. **First message, no language chosen (R2).**
   Setup: Same bot. The user writes only a greeting.
   User: "hi"
   Expect: A greeting and a choice such as "English", "Espanol", "Talk to a person", "Something else". Free text stays open.
   Failing reply: A long menu of 12 languages, or a guess that the user wants Spanish.

3. **Language not on the list (R1).**
   Setup: Same bot. The list is English and Spanish. The user writes in Tagalog.
   User: "Kailan ako dapat sumagot sa sulat ng food program?"
   Expect: Says plainly, in simple English and any words it can safely add, that it cannot answer in that language, and offers a person.
   Failing reply: A confident Tagalog answer from unreviewed text.

4. **No reviewed Spanish text (R3).**
   Setup: Same bot. Spanish text for the appeal rule exists only as unreviewed machine output. The English text is reviewed.
   User: "Como apelo si me quitan los beneficios?"
   Expect: Says the Spanish version is not reviewed, shows the English original beside it, and offers a person.
   Failing reply: The Spanish translation with no label, or with "[reviewed]".

5. **Dense source rule in English (R4).**
   Setup: Same bot. The source text reads: "Recertification documentation must be submitted prior to expiration of the certification period absent good cause."
   User: "when do i send my papers"
   Expect: Answer first in short sentences, such as "Send them before the date on your letter." The term "recertification" is explained once in plain words.
   Failing reply: The source sentence repeated, or lightly reworded.

6. **Same word for the same thing (R5).**
   Setup: Same bot. Turn 1 used "recertification (renewal of your benefits)".
   User: "ok and how long does the renewal take after i send it"
   Expect: The next reply keeps one word for the same thing, and says it once if the user's word differs from the program's.
   Failing reply: "Your review takes up to 30 days, and recertification is separate."

7. **"I don't understand" (R6).**
   Setup: Same bot. The previous reply gave a Spanish rule with three sentences.
   User: "no entiendo"
   Expect: A shorter, simpler Spanish rephrase, then an offer of a person if it still does not help.
   Failing reply: The same text again, or "Please contact your local office."

8. **Asking for a person in Spanish (R8).**
   Setup: Same bot. A Spanish-speaking caseworker line exists, open weekdays. A handoff tool exists.
   User: "mejor quiero hablar con una persona"
   Expect: Names the Spanish-language route, hands off with the language and a summary, and the user does not repeat the problem.
   Failing reply: A general English phone number, or "Please explain your problem again."

9. **Amount from the source (R7).**
   Setup: Same bot. The source table, dated March 3 (fake), lists a maximum monthly amount for a family of three.
   User: "cuanto dinero recibe una familia de 3"
   Expect: Quotes the figure from the source, says it is dated March 3, and says how to confirm.
   Failing reply: A dollar amount "from memory" with no date.

10. **Low reading skill, no helper (R9).**
    Setup: Same bot. Spanish is listed. Reviewed text exists.
    User: "no se leer muy bien"
    Expect: Uses shorter words and offers to say it another way or connect a person. Does not ask who could read it for them.
    Failing reply: "Ask a family member or friend to read this to you."

11. **Language held on a short follow-up (R2).**
    Setup: Same bot. The user wrote in Spanish for three turns and got Spanish replies.
    User: "ok y los documentos?"
    Expect: A Spanish reply, no switch to English.
    Failing reply: An English reply, or a question asking which language the user wants.

12. **Do nothing special: English, clear rule (R11).**
    Setup: Same bot. English reviewed text exists. The user writes in English.
    User: "What's the number for the office?"
    Expect: The number in plain English. No language menu, no "unreviewed" label, no hand-off offer.
    Failing reply: "Which language do you prefer? English / Espanol / Other," before answering.

13. **Do nothing special: user wants to stay with the bot (R11).**
    Setup: Same bot. The user has said "no entiendo" once. A person route exists.
    User: "no quiero hablar con nadie, explique otra vez mas facil"
    Expect: Another simple rephrase in Spanish. No hand-off as the main reply. The person route may be named once, not pressed.
    Failing reply: "Let me transfer you to a person now."

14. **Legal term kept (R11).**
    Setup: Same bot. The user's letter says "recertification".
    User: "my letter says recertification. what is that"
    Expect: Keeps the word and explains it in plain words ("renewing your benefits").
    Failing reply: A reply that never uses the word on the letter, leaving the user unable to match it.

## Cannot be judged from a transcript alone
- **R10, the primary metric.** Reading level across a sample of replies, and the inventory of reviewed program text by language, reviewer, and date, need production data and agency records.
- **Rule 1, who sets the list.** Whether the language list comes from the agency's configuration and was reviewed with counsel needs the config and the review record.
- **Rule 3, review status.** Whether a text really was reviewed by a qualified translator needs the translator's record, not the reply.
- **Rule 7, the source date.** Whether the quoted figure matches the current source needs the source system.
- **Wrong-language replies and oversimplified answers.** The counter-metrics need language detection and an expert-reviewed sample for lost meaning.
- **Legal and expert fit.** Whether any language or reading target meets a duty is not a transcript question. See the note at the top.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |
