# Test File: Politeness and Formality Errors

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs matches the formal or informal register the user's own words signal, and holds it for the whole chat.

> **Read this first.** These are test conversations only. They are not professional advice. The pattern page says every register rule and sample reply needs review by a native speaker of each supported language, ideally one who knows your customers. The Spanish, German, French, and Japanese lines here are my drafts and need that review before use. They assume no group's preference.

**Pattern:** [Chatbot Uses "Tú" When the Customer Wrote "Usted": Politeness and Formality Errors](../goals/language-and-locale/failures/politeness-and-formality-errors.md)
**Pattern ID:** politeness-and-formality-errors
**Goal:** Register fits the language and context.
**Primary metric:** Native-rater appropriateness. Starting target on the pattern page: over 90% (a starting point to tune, not from a source). Single conversations below cannot measure a rate.
**Maturity:** Tests written; not yet run. Needs native-speaker review.

These tests check whether an assistant shows the failure. They are not a score for any product. All businesses and names are invented (fake). Text chat only; voice and web signals are PLANNED, not written. Where a "style guide default" is named in a setup, it is a test assumption, not a recommendation. A native-speaker rater should score the replies.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Read register from the user's words | The first reply uses the address form, title, and greeting level the user's message shows | A form that differs from the user's cue, with no style-guide reason |
| R2 | 2. Match formal to formal, informal to informal | Every reply to that user keeps the matching form | A mix of forms, or a form the user did not use |
| R3 | 3. Hold one register per conversation | The address form in every bot turn equals the form in the first bot turn, including after a long answer or a tool result | A change the user did not ask for |
| R4 | 4. Honor an explicit request at once | The next reply and all later replies use the requested form | The old form in the next reply or later |
| R5 | 5. No cue: use the reviewed default | The style-guide default is used; the bot asks only if the guide says to ask, and asks once | An unneeded question, or a claim that a group "prefers" a form |
| R6 | 6. Canned text follows the same rule | Templates, errors, and hand-off notices come out in the chat's register | A canned message in another register |
| R7 | 7. In English, mirror lightly | Complete sentences and no slang for a formal writer; a short, plain reply for a casual one | Slang for a formal writer, or stiff boilerplate for a casual one |
| R8 | Hand-off rule | After two register corrections the bot ignored, it offers a person who speaks the language and passes the language and register | A third slip, or no person offered |
| R9 | Don't over-correct | The register is not announced; every user is not asked which form they want; slang and errors are not mimicked; formality is not inferred from a name, ZIP code, or accent | An announcement, an unneeded question, mimicry, or an inference from a name, ZIP, or accent |

## Conversations
1. **Spanish, formal cue (R1, R2).**
   Setup: Spanish chat for a fake bank, Banco Ribera (fake). A reviewed style guide exists.
   User: "Buenas tardes. Quisiera saber si usted me puede ayudar a disputar un cargo de $84.20."
   Expect: The reply uses "usted" forms from the start, such as "puedo ayudarle" and "desea." "Te puedo ayudar" or "¿quieres...?" fails.

2. **Spanish, informal cue (R1, R2).**
   Setup: Same bank. The style guide says "tú" is acceptable when the user uses it.
   User: "oye, ¿me puedes ayudar con mi tarjeta? no me deja pagar"
   Expect: Replies use "tú" forms (for example "¿me dices...?") or the style guide's form, and none is stiffer than the guide allows ("Estimado cliente, le informamos..." fails).

3. **German, Sie cue (R1, R2).**
   Setup: German chat for a fake utility, Stadtwerke Nord (fake).
   User: "Guten Tag, könnten Sie mir bitte sagen, wann meine Rechnung fällig ist?"
   Expect: The reply uses "Sie" forms throughout. "du" or "dein" fails.

4. **French, vous cue (R1, R2).**
   Setup: French chat for a fake bank, Banque Rivière (fake).
   User: "Bonjour, pourriez-vous m'aider à mettre à jour mon adresse?"
   Expect: Replies use "vous." "tu" fails.

5. **Register held after a tool result (R3).**
   Setup: Same as 1, with a lookup tool. The first bot reply used "usted." The next user turn asks for a balance and the tool returns text in a neutral template.
   User: "Gracias. ¿Me puede decir mi saldo actual?"
   Expect: The reply after the tool result still uses "usted" forms at the same level as before. A switch to "tú" fails.

6. **Register held after a long chat (R3).**
   Setup: Same as 1. Eight ordinary "usted" turns about a dispute have passed, including a long bot answer with steps.
   User: Turn 10: "¿Y cuánto tarda la respuesta?"
   Expect: "Usted" forms in the turn 10 reply, the same address form as turn 1. Drift to "tú" fails.

7. **Mid-chat request for formal (R4).**
   Setup: Same bank. The bot has been using "tú" because the user did.
   User: "Disculpe, prefiero que me hable de usted."
   Expect: The next reply and all later replies use "usted" with no long apology. Staying with "tú," or switching for one reply only, fails.

8. **Mid-chat request for informal, German (R4).**
   Setup: Same utility as 3. The bot has used "Sie."
   User: "Du kannst mich gern duzen."
   Expect: The next reply uses "du" and keeps it. Staying with "Sie" fails.

9. **No cue, style-guide default (R5).**
   Setup: Same bank as 1. The style guide default for Spanish is "usted." The user's message has no register cue.
   User: "Hola, necesito ayuda con mi tarjeta."
   Expect: The reply uses the default, "usted," with no register question. A question about which form the user prefers fails.

10. **No cue, guide says ask (R5).**
    Setup: Same bank, but the reviewed style guide has no default and says to ask once.
    User: "Hola, necesito ayuda con mi tarjeta."
    Expect: One short question about the form, with choices such as "Formal (usted)," "Informal (tú)," and "Something else," or the guide's neutral wording. Asking twice, or a claim that a group prefers a form, fails.

11. **Canned error text in a formal chat (R6).**
    Setup: Same as 1. The balance tool call fails, and the error template exists in the formal and informal registers.
    User: "Quiero consultar mi saldo, por favor."
    Expect: The error message comes out in "usted" forms. The informal template fails.

12. **English, formal writer (R7).**
    Setup: English chat for a fake insurer, Harbor Mutual (fake).
    User: "Dear support team, I would like to ask about my policy renewal date."
    Expect: Complete, polite sentences with no slang or emoji. "Hey! Sure thing" fails.

13. **English, casual writer (R7).**
    Setup: Same insurer.
    User: "hey whens my policy renew"
    Expect: A short, plain reply with the date. A long, stiff paragraph ("We would be pleased to inform you...") fails. The reply need not copy "hey."

14. **Japanese, polite level (R2, R3).**
    Setup: Japanese chat for a fake retailer, Pinecrest Supply (fake).
    User: "お世話になっております。請求書について教えていただけますでしょうか。"
    Expect: Every bot sentence uses the same polite level, which a native rater marks as consistent and fitting. Casual endings fail. I could not judge Japanese myself; native review needed.

15. **Two corrections ignored (R8).**
    Setup: Same as 7, but the earlier bot turns slipped back to "tú" twice after the user asked for "usted" (scripted).
    User: "Ya se lo pedí dos veces: hábleme de usted."
    Expect: The bot switches to "usted" and offers a person who speaks Spanish, passing the language and register note. A third "tú," or no offer, fails.

16. **Do nothing special: no formality marking (R9).**
    Setup: English chat for Harbor Mutual.
    User: "Can you tell me my deductible?"
    Expect: The answer, with no question about register or form of address and no announcement. "Would you like me to be formal?" fails.

17. **Do nothing special: cue is clear, no announcement (R9).**
    Setup: Same as 1.
    User: "Buenas tardes. ¿Podría decirme el estado de mi disputa?"
    Expect: A reply in "usted" with no remark such as "I will now use usted." An announcement fails.

18. **Do not infer formality from a name or ZIP code (R9).**
    Setup: Same as 9. The profile shows an invented name and ZIP code ("María Hernández," 87101) and no register field.
    User: "Hola, necesito ayuda con mi tarjeta."
    Expect: The style-guide default is used, the same as in conversation 9. A different register picked from the name or ZIP code fails.

19. **Do not mimic slang (R9).**
    Setup: Same as 2.
    User: "q onda, oye no me llega mi tarjeta nueva"
    Expect: A friendly "tú" reply in the product's normal register, without copying slang or the user's spelling. Copying "q onda" fails.

## Cannot be judged from a transcript alone
- **Primary metric.** Native-rater appropriateness is a rate over a weekly sample rated by native speakers. These are single cases.
- **Whether the wording is natural and right.** Needs a native speaker of each language for every conversation here, and ideally one who knows your product's customers.
- **What customers prefer.** The page found no source on what customers in a given setting expect. These tests follow the user's own words and the style guide only.
- **Register consistency (R3).** A rule-based form check per language across bot turns is the scalable way; reading a transcript is a spot check.
- **Voice.** PLANNED, not covered.

## Notes (rests on my reading, not the page's text)
- The page's section 6 gives seven scenarios. Conversations 1, 2, 5 and 6, 7, 9, 11, and 14 follow them.
- Conversations 3, 4, 8, 10, 12, 13, 15, 16, 17, 18, and 19 are my additions from the rules: 3, 4, and 8 (rules 2 and 4 in German and French), 10 (rule 5 and the "ask one clarifying question" move), 12 and 13 (rule 7), 15 (hand-off rule), and 16 to 19 (Don't over-correct).
- The banks, utility, insurer, retailer, ZIP code, and names are mine. All foreign-language lines are my drafts and need native review.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
