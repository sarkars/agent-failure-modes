# Test File: Mixed-Language Experience

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs keeps every part of one reply (text, buttons, scripted lines, retrieved articles) in one language, falls back for the whole message when a string is missing, and leaves alone a user who mixes languages on purpose.

> **Read this first.** These are test conversations only. They are not legal or professional advice. All businesses, strings, and people are invented (fake). Missing-string setups need a test build where you can delete or blank a translation; the setup says what is missing. Bills, deadlines, fees, and consent lines are high stakes, so have a native speaker confirm the hand-off path before you rely on it.

**Pattern:** [Chatbot Replies in Two Languages at Once: Mixed-Language Experience](../goals/language-and-locale/failures/mixed-language-experience.md)
**Pattern ID:** mixed-language-experience
**Goal:** A supported language is fully supported. (Pattern-specific goal, from the pattern page; the family goal is that users are answered in the language that works for them.)
**Primary metric:** Localization coverage of strings. Starting targets on the pattern page: 100% coverage and a mixed-language reply rate under 1% (starting points to tune on your own data). Single conversations below cannot measure either; see "Cannot be judged from a transcript alone".
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. Text chat only; voice is PLANNED, not written. Run each conversation in at least two non-default languages (the page suggests Spanish and Vietnamese). The scripts below are in Spanish and English; swap in the second language yourself. Every conversation carries the Pattern ID above; the R-lines say which rule it checks.

**Invented product used in every setup unless stated.** Desert Valley Power (fake), a Phoenix electric utility with a chat that lists English and Spanish. Its buttons are "Pay now", "View bill", "Talk to a person" and "Something else".

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. No language ships as "supported" below 100% string coverage | Every language the bot lists answers a normal question with no English left over; a language that cannot is not offered | A listed language with visible gaps |
| R2 | 2. One reply language per message | Text, buttons, and scripted lines in one message are all in the reply language (names, addresses, codes, and quoted user text excepted) | Any button, line, or paragraph in another language |
| R3 | 3. A missing string never fills in silently | If a string is missing, the whole message is in the fallback language with a one-line notice written in the user's language | One English button inside a Spanish message, or an English message with no notice |
| R4 | 4. Label anything from outside | An excerpt or error in another language follows a notice, in the user's language, naming that language | An English paragraph or error pasted in with no notice |
| R5 | 5. Mark a translation stale when its source changes | Not judged here (needs the string catalog and release check) | Not judged here |
| R6 | 6. Empty is missing | A key with an empty value is treated as missing: whole-message fallback with the notice, no blank button | A blank or empty label shown, or a half-and-half message |
| R7 | 7. Scripted and fallback paths are in the test set | The "I didn't understand", timeout, error, and hand-off messages are in the user's language | Any of these in the default language |
| R8 | Hand-off rule | After two asks for a language the bot cannot serve, or when the missing text carries money, deadline, legal, or health meaning, a person is offered in the user's language | Another English retry, or an offer in English only |
| R9 | Don't over-correct | The user's own terms, brand names, addresses, codes, and loanwords are kept and not flagged; the bot does not refuse because the only source is in another language | A "please use one language" remark, or a refusal over an English source |

**Moves caveat.** Rules 3 and 4 name a notice and a set of choices ("Read it in English", "Switch to English", "Talk to a person", "Something else"). Those parts rest on the pattern page's Moves table and reference design rather than a numbered rule. Rules 5 and 6 are checks on the string catalog; R6 has a transcript form below, R5 does not.

## Conversations
1. **Language list matches reality (R1).**
   Setup: Desert Valley Power chat. The language menu lists English and Spanish.
   User: "que idiomas hablan?"
   Expect: The reply is in Spanish, and every language it offers can answer a normal question with no English left over. A listed language that then answers in English fails.

2. **Normal question in Spanish, buttons checked (R2).**
   Setup: Desert Valley Power. Spanish is complete.
   User: "hola, necesito pagar mi factura de luz antes del viernes"
   Expect: Reply and every button label are Spanish ("Pagar ahora", "Ver factura", "Hablar con una persona"). One English label fails.

3. **Same, second language (R2).**
   Setup: Same, in Vietnamese (fake translations written by a native speaker).
   User: "chào, tôi cần trả tiền điện trước thứ Sáu"
   Expect: Reply and every button in Vietnamese. English on any button fails.

4. **Missing button string, whole message falls back (R3).**
   Setup: Test build. The Spanish string for "Talk to a person" is deleted.
   User: "necesito pagar mi factura"
   Expect: The whole message is in the fallback language (English) with a one-line notice in Spanish saying why. A Spanish message with one English button fails. An English message with no notice fails.

5. **The fallback notice itself is in the user's language (R3).**
   Setup: Same as 4.
   User: "necesito pagar mi factura"
   Expect: The notice is written in Spanish. A notice in English only fails.

6. **Empty value counts as missing (R6).**
   Setup: Test build. The Spanish "View bill" key exists but its value is an empty string.
   User: "quiero ver mi factura"
   Expect: Same behavior as conversation 4: whole-message fallback and a notice. A blank button fails.

7. **Help article exists only in English (R4).**
   Setup: Desert Valley Power. The only article on late fees is in English.
   User: "que pasa si pago tarde mi factura?"
   Expect: The reply says in Spanish that the source is in English and offers choices such as "Read it in English", "Talk to a person", "Something else". An English paragraph pasted in unlabeled fails.

8. **Backend error text in English (R4).**
   Setup: Desert Valley Power. The payment system returns an English error string.
   User: "pagar ahora" (after tapping a payment button)
   Expect: The user sees a Spanish message for the error (mapped to a prepared message, or labeled as coming from an English source). The raw English error with no notice fails.

9. **"I didn't understand" path (R7).**
   Setup: Desert Valley Power, Spanish.
   User: "asdfgh jkl"
   Expect: The fallback line is in Spanish. "Sorry, I didn't understand that" fails.

10. **Timeout path (R7).**
    Setup: Desert Valley Power, Spanish. The user goes quiet; the session reaches its timeout message.
    User: (no reply for the timeout period)
    Expect: The timeout message is in Spanish. An English timeout line fails.

11. **Hand-off path (R7).**
    Setup: Desert Valley Power, Spanish. A person is available.
    User: "quiero hablar con una persona"
    Expect: The transfer line and the wait message are in Spanish. "Transferring you to an agent. Please hold." fails.

12. **Asked twice for a language the bot cannot serve (R8).**
    Setup: Desert Valley Power. The only help article is English, and the bot has already offered it.
    User: "no leo ingles" then, next turn, "no leo ingles, ayuda por favor"
    Expect: By the second ask a person is offered in Spanish. A third English article fails.

13. **Missing text carries a deadline (R8).**
    Setup: Test build. The Spanish string for the shut-off date notice is missing; the English one exists. The user's account has a shut-off date.
    User: "cuando es la fecha limite para pagar?"
    Expect: The bot does not show the date line as untranslated text alone. It uses the notice, offers a person in Spanish, and does not guess the date. An unlabeled English date line with no hand-off offer fails.

14. **Do nothing special: user mixes languages (R9).**
    Setup: Desert Valley Power, Spanish. The tool can find a refund policy.
    User: "Quiero un refund de mi last bill"
    Expect: The reply answers the request and keeps the user's terms without a remark on mixing or a flag. A "please write in one language" remark fails.

15. **Do nothing special: names, address, and codes in a Spanish reply (R9).**
    Setup: Desert Valley Power, Spanish. The account address is "2210 N Central Ave, Phoenix" and the plan is called "Time-of-Use Plus" (an invented plan name).
    User: "cual es mi plan y mi direccion?"
    Expect: A Spanish reply that shows the English plan name and the street address as they are. Treating them as mixing, or translating the address, fails.

16. **Do nothing special: an English user (R9).**
    Setup: Desert Valley Power, English session.
    User: "when is my bill due?"
    Expect: A normal English answer, with no language notice, no language choice, and no mention of other languages. A language notice fails.

## Cannot be judged from a transcript alone
- **Primary metric.** Coverage is a count over the string catalog per language each build, and the mixed-reply rate needs language ID on a sample of sent replies reviewed by a native speaker. These are single cases.
- **R1, full coverage.** Conversation 1 checks only what a user can see. Coverage of 100% needs the catalog export with empty and stale values marked.
- **R5, stale keys.** Needs the source hash and translation hash for each key and a failing release check. There is no transcript form of it.
- **Logging.** That a `string_fallback` event was logged in conversations 4 and 6 needs the reply-assembly log.
- **Translation quality.** The page covers missing translations, not wrong ones; see [unchecked translation in high-stakes text](../goals/language-and-locale/failures/unchecked-translation-in-high-stakes-text.md).
- **Real wording.** I wrote the Spanish lines myself as test inputs; have a native speaker check them, and check the Vietnamese ones too, before use.
- **Voice.** PLANNED, not covered.

## Notes (rests on my reading, not the page's text)
- The page's section 6 gives eight scenarios. Conversations 1 (test 1, partly), 2 and 3 (test 2), 4 (test 3), 7 (test 4), 9 (test 6), 12 (test 8), and 14 (test 7) follow them. Test 5 (stale key) has no conversation; see R5.
- Conversations 5, 6, 8, 10, 11, 13, 15, and 16 are my additions from the rules: 5 (notice language), 6 (rule 6), 8 (rule 4, error text), 10 and 11 (rule 7), 13 (hand-off rule, money/deadline), and 15 and 16 (Don't over-correct).
- Desert Valley Power, the plan name, and the address are invented. The utility scenario and button names come from the page's example.
- In conversation 4, the page does not say which language is the fallback; the test assumes English as the default and checks only that the whole message is in one language with a notice.
- In conversation 8, the page's rule 4 covers backend errors in another language by labeling; the Canva source also says to map error codes to prepared messages. Either passes.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
