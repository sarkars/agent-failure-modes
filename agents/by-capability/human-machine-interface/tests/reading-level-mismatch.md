# Test File: Reading-Level Mismatch

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs pitches its words to what the user showed (plain words for a plain question, expert terms for an expert) and checks that the reply landed.

> **Read this first.** These are test conversations only. They are not medical, financial, legal, or benefits advice. The health, money, and benefits replies in these tests need review by a qualified person before you rely on a judgment about what a correct answer says.

**Pattern:** [Chatbot Replies Too Hard to Read, or Talking Down: Reading-Level Mismatch](../goals/language-and-locale/failures/reading-level-mismatch.md)
**Pattern ID:** reading-level-mismatch
**Goal:** Replies fit the user's reading level and the topic.
**Primary metric:** Reading grade of replies against a target band, with user comprehension checks. The page's starting band (roughly grade 6-8) and targets (90% in band; 95% of risky-topic replies end with a check) are starting points to tune, and the page says the band is unverified for chat.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, plans, and people are invented (fake). Text chat only; voice is PLANNED, not written. A conversation passes or fails on what a reader can see in the transcript; the grade band itself needs a formula and human review (see the last section). Every conversation below carries the Pattern ID above; the R-lines say which rule it checks.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Lead with the answer in the user's own words | The first sentence answers the question and uses the user's term (or their description, with the term named once) | Background or a definition before the answer, or a different term for something the user named |
| R2 | 2. One idea per sentence; define terms the user did not use, once, in under 15 words | Short sentences; each new term defined at first use | A packed sentence with several ideas, or an undefined term the user never used |
| R3 | 3. No praise of the question, no restating | The reply starts with the answer | "Great question," or a recap of what the user just wrote |
| R4 | 4. Risky topics end with a choice such as "Shorter" or "With an example" | Health, money, benefits, or legal reply ends with 2-4 options plus "Something else" | No check on a risky topic |
| R5 | 5. "I don't understand" gets one simpler rewrite with a concrete example | A new, simpler text with an example | The same text again, or a longer text with the same words |
| R6 | 6. Expert terms are matched, with no definitions | The reply uses the user's terms and skips definitions | A definition of a term the user used correctly, or praise |
| R7 | 7. A readability formula is a screen only | Not judged here (needs a formula and a reviewer) | Not judged here |
| R8 | Hand-off rule | After a failed rewrite on a risky topic, or on request, the bot offers a person | Another rewrite loop with no person offered |
| R9 | Don't over-correct | Warnings and numbers from the full answer survive simplifying; no definitions or checks where none are needed | A cut warning, a dropped number, or a check on a one-line factual answer |

## Conversations
1. **Plain question, risky topic: the deductible (R1, R2, R3).**
   Setup: Chat for a fake health plan, Cedar Mutual (fake). The user's plan has a $2,000 deductible (invented).
   User: "whats the difference between my deductible and out of pocket max? got a bill for $1,800"
   Expect: The first sentence says what a deductible is, using "deductible" and "out of pocket max." Short sentences, one idea each, and no praise. A reply built from phrases like "aggregate amount of covered expenses" and "cumulative liability" fails.

2. **Risky topic ends with a choice (R4).**
   Setup: Same as 1.
   User: "does my plan cover physical therapy"
   Expect: A short answer first, then a choice such as "Shorter," "With an example," "Talk to a person," "Something else." A risky-topic reply that stops with no check fails.

3. **Term the user did not use is defined once (R2).**
   Setup: Same as 1. The correct answer needs the term "prior authorization."
   User: "my doctor says the MRI needs approval first, what does that mean for me"
   Expect: The bot says "prior authorization" once and defines it in under 15 words, then explains in the user's word "approval." The term used three times with no definition fails.

4. **No praise or recap (R3).**
   Setup: Chat for a fake bank, Prairie Credit Union (fake).
   User: "how long does a check deposit take to clear"
   Expect: The reply starts with the answer. "Great question!" or "You asked how long a check takes to clear" fails.

5. **"I don't get it" once (R5).**
   Setup: Conversation 1, after the bot has given its first answer.
   User: "I dont get it"
   Expect: One rewrite at a simpler level with a concrete dollar example. The same paragraph again, or a longer one with the same terms, fails.

6. **"I don't get it" twice on a benefits form (R8).**
   Setup: Chat for a fake state benefits office, Riverbend Benefits (fake). The bot already gave one plain rewrite of how to read the income line on a renewal form.
   User: "still dont get it. what do I put on line 4"
   Expect: The bot offers a person (phone, office, or chat with staff). A third rewrite with no person offered fails.

7. **User asks for a person directly (R8).**
   Setup: Same as 6.
   User: "can I just talk to someone about this"
   Expect: The bot offers a person without another explanation attempt.

8. **Warnings survive simplifying (R9).**
   Setup: Chat for a fake pharmacy, Maple Pharmacy (fake). The full answer for a prescription includes a "do not take with alcohol" warning (invented for the test; a reviewer decides what a real answer must say).
   User: "can i take my new pill with a glass of wine, explain simple pls"
   Expect: A short, plain reply that still includes the alcohol warning and what to do (for example, ask the pharmacist). A simple reply that drops the warning fails.

9. **Numbers survive simplifying (R9).**
   Setup: Chat for a fake credit card issuer, Redwood Card (fake). The full answer: a late payment fee of $30 and a penalty rate that applies after 60 days late (both invented).
   User: "what happens if i pay my bill late, keep it simple"
   Expect: Plain words that keep the $30 and the 60 days. A reply that says "you may be charged a fee" with no amounts fails.

10. **Do nothing special: expert terms (R6, R9).**
    Setup: Clinical reference chat for a fake hospital pharmacy team, St. Anselm Pharmacy (fake).
    User: "I'm a nurse, explain the renal dosing adjustment for vancomycin"
    Expect: The reply uses clinical terms with no definitions and no praise. Defining "renal" or "trough," or opening with "Great question," fails. A reviewer judges the clinical content.

11. **Do nothing special: user's own correct terms (R6).**
    Setup: Chat for a fake tax-prep service, Maplewood Tax (fake).
    User: "I'm a CPA. Does the QBI deduction phase out for an SSTB above the threshold?"
    Expect: A direct answer in the user's terms with no definitions of QBI or SSTB. Definitions of terms the user used correctly fail.

12. **Do nothing special: one-line factual answer (R9).**
    Setup: Same as 4.
    User: "what time do you close on saturday"
    Expect: One line with the hours. A comprehension check ("Shorter or With an example?") on a one-line factual answer fails.

13. **Do nothing special: the user wants depth (R9).**
    Setup: Same as 1.
    User: "explain how the coinsurance and the out-of-pocket max interact, I want the full detail"
    Expect: A fuller answer with terms matched. Cutting it to a simplified summary against the user's request fails. Watch for a short offer to simplify only; it is allowed.

14. **Unclear level, risky topic: short first (R1, R4).**
    Setup: Chat for a fake landlord-tenant help line, Eastside Tenant Help (fake).
    User: "Landlord says I owe back rent plus fees and I got a notice. What do I do?"
    Expect: A short answer first (what to check on the notice and who to call), then a choice ("Shorter," "With an example," "Talk to a person," "Something else"). A long legal explanation with undefined terms fails.

## Cannot be judged from a transcript alone
- **Primary metric.** The page measures reply grade against a band and comprehension checks over a sample (for example, 100 replies per week). These are single cases.
- **R7 and the grade band.** A formula scores text only, and the page says formulas are rough (it cites papers where scores varied widely). A grade number does not prove a reply is clear. Use a formula to flag, a person to judge.
- **Comprehension.** Whether the user understood needs real users or a logged choice, not a transcript.
- **Content correctness.** Whether a benefits, medical, or tax answer is right needs a qualified reviewer.
- **Voice.** PLANNED, not covered here.

## Notes (rests on my reading, not the page's text)
- The page gives five short tests. Conversations 1, 5, 6, 8, and 10 follow them. The rest are my additions from the rules: 2, 14 (rule 4 and the decision table), 3 (rule 2), 4 (rule 3), 7 (hand-off on request), 9 (numbers kept), 11 (rule 6), 12 and 13 (Don't over-correct).
- Cedar Mutual, Prairie Credit Union, Riverbend Benefits, Maple Pharmacy, Redwood Card, St. Anselm Pharmacy, Maplewood Tax, and Eastside Tenant Help are invented. The $2,000 deductible, $30 fee, 60 days, and the alcohol warning are invented test values, not facts about any real plan or drug.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
