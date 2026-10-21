# Test File: Language That Is Hard for People With Cognitive Disabilities

This file is a set of chat test conversations for people who build or review chatbots, and want to check whether theirs answers in idioms, long sentences, and shifting names that people with cognitive disabilities cannot follow.

> **Read this first.** This is design guidance for testing your own product. It is not legal, clinical, or professional advice, and it is not a conformance claim. The pattern page found no study that compares plain and standard chatbot replies with people who have cognitive disabilities, so the rubric below is a design hypothesis, not a measured standard. The 20-word sentence limit and the 4-step limit are starting points to tune, not sourced numbers. Whether a text is understandable to a person needs expert review and testing with people from the group. These tests check one reply at a time.

**Pattern:** [Language That Is Hard for People With Cognitive Disabilities](../goals/accessibility/failures/language-that-is-hard-for-people-with-cognitive-disabilities.md)
**Pattern ID:** language-that-is-hard-for-people-with-cognitive-disabilities
**Goal:** People who use screen readers, keyboards, captions, relay services, or plain-language support can use every part of the agent.
**Primary metric:** Replies passing the plain-language checklist. Start: 95% (a starting point to tune, from the pattern page).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and amounts below are invented. Text chat only. The setup holds the persona prompt and what the harness shows.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. No idioms or figures of speech | Literal words; any figure of speech is explained in plain words right after | An idiom such as "put through the wringer" or "get the ball rolling" with no explanation |
| R2 | 2. Keep sentences short, key fact first | Each sentence has 20 words or fewer and one idea; the key fact comes first | A sentence over 20 words, or the key fact buried at the end |
| R3 | 3. One instruction per step | Numbered list, one action per step, 4 or fewer shown, rest offered | A step with two actions, or more than 4 steps shown at once |
| R4 | 4. One name per thing | The glossary word every time; no new words invented | A second name ("claim", "case") for the glossary term |
| R5 | 5. Common words; explain the rest | "Pay stub"; a needed technical word said once with its meaning | "Supporting documentation" with no plain version, or a technical word with no meaning |
| R6 | 6. Say what to do now | Ends with the one next action, or "You do not need to do anything now." | A vague close such as "You may be contacted later" |
| R7 | 7. Simpler on request | "Say it simpler", "in easy words" or "one step at a time" is kept for the rest of the chat, without comment | Style slides back after one reply, or the bot comments on the request |
| R8 | Hand-off rule | After two failed "simpler" attempts, or a high-stakes step the user does not follow, a person is offered with the topic and what was tried | A third rewrite with no person offered |
| R9 | Don't over-correct | Dates, amounts and deadlines kept; no talking down; no guess about the user's ability | A needed fact dropped, baby talk, or a remark on the user's ability |

## Conversations
1. **Idiom in a status answer (R1).**
   Setup: Fake agency "Lakeview County Benefits" (fake). The food-help application was received Oct 8 (fake date) and a caseworker reviews it next. Persona prompt: "Be friendly and casual."
   User: "I applied for food help last week. What happens now?"
   Expect: Literal words: "A caseworker is checking your application." No idiom.
   Failing reply: "Your case will be put through the wringer, so hang tight!"

2. **Long sentence, key fact last (R2).**
   Setup: Fake "Maple Ridge Library" (fake). A card renewal needs a photo ID and takes 5 minutes at the desk.
   User: "How do I renew my library card?"
   Expect: Short sentences, key fact first: "Bring a photo ID to the front desk." Each sentence 20 words or fewer.
   Failing reply: "Once you have gathered the appropriate identification, which should include a photo, you may proceed to the front desk, where a staff member will assist you with the renewal, which takes about five minutes."

3. **Six steps at once, two actions in one step (R3).**
   Setup: Fake "Harbor Credit Union" (fake). Resetting the online banking password takes 6 steps.
   User: "How do I reset my online banking password?"
   Expect: A numbered list with one action per step and 4 or fewer shown. The rest is offered: "Want the next steps?"
   Failing reply: All six steps in one list, including "3. Open the app and tap Settings."

4. **Second name for the same thing (R4).**
   Setup: Product glossary: "application". The user has an open application. Earlier bot replies used "application".
   User: "What about my claim?"
   Expect: Keeps the glossary word: "Your application is still being checked." It does not adopt the user's word as a second name.
   Failing reply: "Your claim is still open, and your case number is 4417 (fake)."

5. **Technical word with no plain version (R5).**
   Setup: Same agency as case 1. The user needs to send a pay stub or a utility bill.
   User: "What do I send you?"
   Expect: "Send a pay stub or a power bill." Any technical word is said once with its meaning.
   Failing reply: "Please submit supporting documentation to verify your income and residency."

6. **No clear next action (R6).**
   Setup: Same agency. Nothing is needed from the user now.
   User: "So do I need to do something?"
   Expect: "You do not need to do anything now." The next event is named.
   Failing reply: "You may be contacted to provide supporting documentation at a later date."

7. **Simpler style does not last (R7).**
   Setup: Same agency. Turn 1: the user wrote "in easy words please" and the bot simplified. Persona prompt: "Be thorough and professional."
   User: "And when do I get the card?"
   Expect: Still short and plain, with no comment on the style: "You get a letter first. The letter says yes or no."
   Failing reply: A long, formal paragraph, or "Of course, I will keep using simple words for you."

8. **Two failed simpler attempts (R8).**
   Setup: Fake "Redwood Health Plan" (fake). The bot has explained a copay twice in simpler words. The user still does not follow.
   User: "I still don't get it."
   Expect: Offers a person and passes the topic (copay) and what was tried (two simpler explanations), so the user does not start over.
   Failing reply: A third rewrite with no person offered.

9. **High-stakes step the user does not follow (R8).**
   Setup: Same health plan. Fake deadline: Oct 30 (fake date) to send a form. The user says they do not understand the form step.
   User: "I don't know what to put on the form."
   Expect: Offers a person with a summary: the form, the Oct 30 deadline, what the bot already said. Design guidance only; a medical or legal topic needs expert review.
   Failing reply: "Just fill it out carefully and send it in."

10. **Simple language that drops the facts (R9).**
    Setup: Fake utility "Brightline Power" (fake). The bill is $85 (fake amount), due Nov 3 (fake date).
    User: "When do I pay my bill?"
    Expect: Short and plain, with both facts: "Your bill is $85. Pay it by Nov 3."
    Failing reply: "You have to pay soon." Or: "Don't worry, this is easy! I will use tiny words for you."

## Cannot be judged from a transcript alone
- **Reading grade of replies.** Rule 8 of the fix needs a readability formula on sampled replies. The pattern page gives grade 8 as an assumption, not a standard.
- **Whether a person with a cognitive disability can follow the steps.** It needs moderated sessions with people from the group and an expert.
- **Term consistency across a long chat.** Ten conversations give a glimpse. A glossary check on production logs is needed.
- **Required facts missing from simplified replies, at scale.** It needs sampled human review against a fact list per topic.
- **Voice and read-aloud delivery.** This file is text only.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
