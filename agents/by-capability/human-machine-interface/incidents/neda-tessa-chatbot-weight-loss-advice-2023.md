---
title: "NEDA's Tessa Chatbot Is Taken Down After Reports of Weight-Loss Advice"
date: 2023-05-30
source: "https://www.wypr.org/2023-06-08/an-eating-disorders-chatbot-offered-dieting-advice-raising-fears-about-ai-in-health"
summary: "In late May 2023 users reported that Tessa, a chatbot run for the National Eating Disorders Association, gave dieting advice to people who said they had an eating disorder. NEDA took it down on May 30. NEDA and the vendor, Cass, later gave different accounts of how the bot had changed."
categories:
  - Health and Wellbeing Chatbots
patterns:
  - missed-crisis-signals
  - stakes-blind-register
  - confident-wrong-answer-with-no-way-to-check
---

**This page is a dated teardown of one public chatbot incident, for teams that ship a chat assistant in a health or wellbeing setting.** Every fact below comes from a source we opened (listed at the end). Claims are marked as reported or unknown. Spot an error? See "Corrections" at the end.

> **Read this first.** This page covers eating disorders, a health topic. It is design guidance for chat teams, not clinical advice, and it makes no legal claim. Anyone who is struggling should talk to a qualified clinician or a crisis service. Have clinical experts review any wording or rule before you ship it.

## What happened (as reported)

- **Before 2023.** Fortune (May 31) says Dr. Ellen Fitzsimmons-Craft, a Washington University psychiatry professor, helped design Tessa. Gizmodo (May 31) says Tessa was created in 2018 with grant funding, was designed in part by the company Cass (formerly X2AI), and builds on an earlier "emotional health chatbot" named Tess.
- **October 2022.** NPR's Michigan Radio reporter Kate Wells (June 8) says a leader at another eating disorder organization sent NEDA screenshots of Tessa urging "healthy" snacks such as fruit. NEDA passed them to Cass, and the language was removed.
- **Late May 2023.** Fortune says NEDA announced it would replace its human helpline staff with Tessa on June 1. It says NEDA had six paid employees overseeing about 200 volunteers, who handled calls from nearly 70,000 people the previous year. Gizmodo notes former staff claim they were illegally fired for trying to unionize; we cannot judge that claim.
- **Before May 30, 2023.** Sharon Maxwell, an eating disorder activist, tested Tessa. Gizmodo reports she says it told her to lose one to two pounds per week, use calipers, track calories and weigh herself constantly, and kept doing so after she said she had an eating disorder. WYPR adds a 2,000-calorie daily limit and a 500 to 1,000 calorie daily deficit among the advice she reported.
- **Same days.** Fortune says NEDA first called Maxwell's claims a lie, then deleted that post after she sent screenshots. Psychologist Alexis Conason then posted screenshots of her own test that she said showed similar weight-loss language.
- **May 30, 2023.** NEDA said on Instagram that the current Tessa program "may have given information that was harmful and unrelated to the program" (Gizmodo's quote) and took it down. Fortune says NEDA took it down pending an investigation. WYPR gives May 30 as the date it was disabled.
- **June 7-8, 2023.** NPR/WYPR reports NEDA CEO Liz Thompson saying NEDA "was never advised of these changes and did not and would not have approved them." Cass CEO Michiel Rauws told NPR the change was a "systems upgrade" made the year before that added an "enhanced question and answer feature" using generative AI, and that it was part of NEDA's contract.

## What the organization and the vendor said

- **NEDA, May 31 (Gizmodo).** Thompson said the weight-loss and calorie-limit feedback violates NEDA's policies and core beliefs. She said more than 2,500 people had interacted with Tessa, that NEDA had not seen such responses before, and that the bot was taken down while it fixed a "bug" and "triggers." Communications VP Sarah Chase told Gizmodo the bot "can't go off script" and was not learning over time.
- **NEDA, June 7-8 (WYPR).** Thompson said the helpline and Tessa decisions had become conflated in public messaging.
- **Cass, June 8 (WYPR).** Rauws said the generative feature was part of NEDA's contract. He said earlier problematic language came from pre-scripted content, not generative AI.
- **Original designer (WYPR).** Fitzsimmons-Craft said the version she helped build was rule-based: "All of the responses were pre-programmed."
- **Gizmodo (May 31):** Cass did not reply to its request for comment before publication.

## What the sources do not say

- **How many users received harmful replies.** Maxwell noted outsiders cannot tell (Gizmodo). The "2,500" figure is NEDA's count of people who interacted, not of harm.
- **Whose account is right** on whether the generative feature was authorized. Thompson and Rauws disagree and we do not resolve it.
- **The cause of the replies.** Gizmodo reports little public information on design, training data or safeguards. We found nothing that confirms which part of the system produced the quoted advice.
- **Full transcripts.** We did not see the screenshots, only descriptions.
- **Calorie figures.** Sources describe different numbers (2,000 a day, 500 to 1,000 deficit). We report them as attributed and do not reconcile them.
- **Whether and how Tessa returned.** No opened source says.
- **Whether the replies matched the first Tessa study.** Gizmodo describes a 2022 study (2,409 participants, 52,000+ comments reviewed) but we did not open the paper.

## Pattern match

- [Missed crisis signals](../goals/vulnerable-users/failures/missed-crisis-signals.md) is the closest fit. Per Maxwell, the bot kept giving dieting advice after she said she had an eating disorder. That page is about suicidal thoughts and abuse; what carries over is a stated risk that the reply did not change for.
- [Stakes-blind register](../goals/stakes-calibration/failures/stakes-blind-register.md) fits the generic "healthy eating" tone used with a user who named a clinical condition.
- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) is a partial fit. The reported advice was delivered as plain instruction with no uncertainty or source. Whether it was "wrong" in a clinical sense is for clinicians, not us.

No existing page is named for a rule-based bot that gains free-text generation after launch. We do not claim one is.

## Where in the flow it broke

1. **Change control.** Per both parties, the bot's behavior changed after the first study (NEDA says it was never told; Cass says it was in the contract). Neither account describes a test of the changed bot against eating-disorder scenarios.
2. **No condition-aware path.** After a user stated an eating disorder, the reported replies continued the diet advice. No reported guard reacted to that sentence.
3. **Earlier warning.** Screenshots in October 2022 led to one fix. The sources we opened do not say whether a broader test followed.
4. **Helpline replacement.** Tessa was announced to replace a human line (Fortune). People in distress reached a bot with no live person behind it.
5. **Slow public response.** NEDA first disputed the report and then took the bot down (Fortune, Gizmodo).

## What to measure

Proposed metrics; none come from NEDA or Cass. Status: Not yet run.

| Metric | How to compute from logs |
|---|---|
| Disclosure-then-advice rate | Sessions where the user states a health condition and a later reply gives instructions that conflict with it, found by reviewer labels |
| Prohibited-topic rate | Replies containing calorie, weight-loss or numeric body-target language on a blocked list, per 1,000 sessions |
| Post-change regression | Same scripted test set before and after any model or feature change; count of new failures |
| Handoff offer rate | Share of sessions with a risk disclosure where a person or crisis resource is offered within one turn |
| Time to takedown | Hours from first credible report to the feature being disabled |

## What a team can change

Proposed rules, each a pass/fail check on a transcript. Status: Not yet run.

1. **Gate on stated conditions.** If a user names a health condition, the reply must not give advice on a clinician-approved blocked list for that condition. Check: scripted disclosure prompts across five turns.
2. **Re-run red-team scripts after every change.** Any new generation feature, upgrade or content update triggers the full risk test set. Check: release blocked unless the set passes.
3. **Write change control into the vendor agreement.** Name who approves behavior changes and who is told. Have counsel review the wording.
4. **Offer a person.** On a stated risk, the reply offers a human or crisis resource and does not continue the task. Check: handoff offered in the next reply.
5. **Treat every forwarded screenshot as a test case.** Add it to the regression set the day it arrives, and test whether sibling prompts also fail.
6. **Keep a kill switch with an owner.** Disabling a feature should take minutes and have a named decision-maker.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://www.wypr.org/2023-06-08/an-eating-disorders-chatbot-offered-dieting-advice-raising-fears-about-ai-in-health | NPR (Kate Wells, Michigan Radio), via WYPR | 2023-06-08, updated 2023-06-09 | Yes, 2026-10-20 |
| https://gizmodo.com/ai-chatbot-eating-disorder-helpline-neda-1850490751 | Gizmodo (Kyle Barr) | 2023-05-31 | Yes, 2026-10-20 |
| https://fortune.com/well/2023/05/31/neda-ai-chatbot-harmful-advice | Fortune (Chris Morris) | 2023-05-31 | Yes, 2026-10-20 |

Not opened: NEDA's Instagram statement (not retrieved; we rely on Gizmodo and Fortune quoting it), Maxwell's and Conason's own posts, the NPR.org copy of the helpline story (timed out), Daily Dot, Futurism and the AI Incident Database (search results only; nothing from them is stated above).

## Corrections

If you have NEDA's original statement, the posts by Maxwell or Conason, or Cass's own account, tell us and we will fix this page.
