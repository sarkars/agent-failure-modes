# Identity Verification Fails With No Credit History or ID: Identity Checks That Exclude People Without Standard IDs

<!-- SEO
title: Identity Verification Fails With No Credit History: Fix the Dead End
description: Government chat that verifies identity with a driver's license or credit history strands people who have neither. Offer other ways to verify, up front.
search phrases:
- identity verification fails no credit history
- ID verification alternative government chatbot
- can't verify my identity online no driver's license
- ID.me can't verify me what now
- unemployment identity verification failed
- government website says it can't verify my identity
- how to verify identity without credit history
-->

**Frequency**: Common

## Issue: A government chat or sign-in flow verifies identity with a document or credit history that some people do not have, and offers no other way to verify, so those people cannot reach services they are owed.

> **Read this first.** This page is design guidance, not legal, security, or professional advice. Which identity evidence is acceptable, and which alternatives are allowed, depends on the program, the agency, and its fraud and privacy rules. The agency's counsel, its security team, and subject experts must review any verification behavior before use. This page states what a source says only as far as I opened it; it does not say what any law requires.

> **One line:** The only way to prove who you are is a document or credit file the person does not have, and the bot has no other route.

| | |
|---|---|
| **Channel** | Written for **chat** (text). Voice and phone verification flows are PLANNED, not written or measured here. |
| **Stakes** | High. A failed check can block benefits, a tax account, or health coverage, often with a deadline. |
| **Who is affected** | People with no or thin credit history (young adults, recent immigrants), people without a driver's license or state ID, people with a recent name change, and people living abroad |
| **Frequency** | Common in public services by my reading; I found no count of how often chat flows dead-end at verification. The evidence below is on how many people lack the inputs, plus one dated case. |
| **Pattern ID** | identity-checks-exclude-people-without-standard-ids |
| **Family** | [Government service agents](../README.md) |
| **Goal** | Public-service agents give accurate, accessible, plain-language guidance and always leave a path to a person and an appeal. |
| **Primary metric** | Completion rate of identity verification by group (no credit history, no state ID, recent name change, all others). Target: gap under 5 percentage points between any group and everyone else (a starting point to tune; no source sets it). |
| **Maturity** | Researched. Flagged L (legal) for counsel review and R for subject-matter review of the verification rules before use |
| **Will a better model fix this?** | No. Which evidence counts is an agency policy and fraud-control choice, not language quality. (Our judgment, not tested.) |
| **Also searched as** | no credit history can't verify identity · identity proofing failed · ID.me failed verification · can't verify identity online no ID · knowledge-based verification questions wrong |

## 1. In plain words
To protect benefits from fraud, a government service checks who you are. Some checks ask questions built from your credit file; others need a driver's license or a state ID. People who have no credit file, or no such ID, fail the check through no fault of their own. A bot that answers "we could not verify you, please try again" leaves them stuck. The fix is to name the other ways to verify, in the first reply, and to give a person route.

## 2. What it looks like
**Without the fix**
```
User: I'm trying to see my unemployment claim status. It says my identity couldn't be verified.
Bot:  We were unable to verify your identity. Please make sure your information is correct and try again.
User: I'm 21 and have never had a credit card. I don't drive.
Bot:  Please try again.
User: (leaves; the claim is never reached)
```
**With the fix**
```
User: I'm trying to see my unemployment claim status. It says my identity couldn't be verified. I'm 21, no credit card, I don't drive.
Bot:  That is a known gap: some checks need a credit history or a driver's license, and not everyone has one. You have other ways to verify:
      [Upload a passport or other photo ID I list] [Verify in person] [Video call with a staff member] [Talk to a person] [Something else]
      Your claim stays open while you do this. Tell me which one fits and I'll give the steps.
User: I have a passport.
Bot:  Good. Here is what to upload and what happens next. If the upload fails, say so and I'll connect you to a person with your claim number.
```
The fixed bot names the cause in plain words, offers several routes up front, and asks for no explanation or proof of hardship. The "claim stays open" line is an example: say it only if the agency confirms it.

## 3. Why it happens
- **One verification path is the whole design.** The check was bought or built for the typical applicant (has a credit file, has a state ID), so the exception was never specified. The identity vendor's own letter, below, describes legacy credit-based checks as unavailable to tens of millions of Americans.
- **The bot cannot tell why the check failed.** It gets "failed", not "no credit file" or "ID expired", so it repeats a generic retry message ([generic error messages](../../errors-and-recovery/failures/generic-error-messages.md)).
- **Nobody tracks who drops out.** A New York comptroller report, as relayed below, found the state labor department had not tracked key performance metrics, so no one could say whether people who gave up were fraudsters or legitimate applicants.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Legacy knowledge-based verification "rely on information collected by credit rating agencies"; the letter says that information is "simply unavailable for tens of millions of Americans", citing a 2016 CFPB estimate of 26 million Americans with no credit history at a nationwide credit reporting company and another 19 million with thin or dated history. | [Letter from ID.me's counsel to House committee chairs, Apr. 28, 2022](https://coronavirus-democrats-oversight.house.gov/sites/democrats.coronavirus.house.gov/files/4.28.22%20ID.me%20letter.pdf). Opened (PDF text extracted locally; the fetch tool alone could not read it). | Written by a vendor that sells identity verification. The CFPB figure is secondhand (I did not open the CFPB report). Estimates are from 2016. |
| The same letter lists who may be unable to meet NIST criteria through public-records checks: international users, young adults, "individuals without credit history", and people with recent name changes; it says NIST enabled a supervised remote option with a trained Trusted Referee for them. | Same letter. Opened. | Vendor description of its own product and of NIST. See the NIST row for NIST's own text. |
| NIST's implementation resource says trusted referees are for "populations that are unable to meet IAL2 and IAL3 identity proofing requirements" or who would be challenged by the process, and that "The use of trusted referees is optional for CSPs" (SP 800-63A section 5.3.4). | [NIST, *A.9 Use of Trusted Referees*](https://pages.nist.gov/800-63-3-Implementation-Resources/63A/referees). Opened and read. | Implementation resource for SP 800-63-3, not the current revision, and not the SP 800-63A text itself. Optional for the service provider, so it is not a guarantee. |
| GSA says agencies "have long relied on knowledge-based verification", including "questions about a user's credit history"; Login.gov "now offers in-person identity verification at over 18,000 USPS locations nationwide" for people who "face difficulty completing identity verification online". | [GSA blog, Aug. 18, 2023](https://www.gsa.gov/blog/2023/08/18/reducing-fraud-and-increasing-access-drives-record-adoption-and-usage-of-logingov). Opened (key lines read). | Agency promotion of its own product. I did not confirm what ID the in-person route requires. |
| KFF says "Some consumers with little or no credit history, such as young adults or recent immigrants, may have difficulty" setting up a HealthCare.gov account; it advises re-checking every field, then submitting documents, then calling the Marketplace. | [KFF FAQ, published Sep. 29, 2025](https://www.kff.org/faqs/faqs-health-insurance-marketplace-and-the-aca/marketplace-basics/i-am-having-trouble-setting-up-a-marketplace-account-online-i-am-a-young-adult-with-no-credit-history-could-that-be-the-problem-what-should-i-do-now/). Opened and read. | Consumer guidance for one program; it does not measure how often this happens. |
| 1 in 10 adults lack a valid driver's license or state ID; 14% of U.S. adults are underbanked. | Login.gov June 2025 roadmap, **read through a summary only** (the PDF would not load). | Not verified in the source text; kept out of the fix. |

**Public incident.** In New York, about 100 people filed Federal Trade Commission complaints about ID.me, and complainants described weeks-long or months-long waits, facial recognition failures, and locked accounts, per [New York Focus, June 16, 2023, reposted by NCLEJ](https://nclej.org/news/new-yorks-chosen-ai-keeps-users-from-collecting-unemployment). The article says ID.me stated that 10% to 15% of people need a human Trusted Referee, and that in New York the rate was 25%, just over 180,000 people, per the state comptroller's November report. Opened and read. Caveats: this is a facial-verification and referral case, not a credit-history one; the figures are relayed by a news outlet from the comptroller and the company, and I did not open the comptroller's report. It is not yet linked from an `incidents/` page.

I found no study of verification inside chatbots, and no independent measure of how many eligible people are wrongly rejected. A 2021 report that ID.me's face matching failed some users, with a company reply, appeared in a search summary; I did not open it and do not use it.

## 5. The fix
**The principle:** Every identity check has at least one other route that does not need the same document or credit history, shown before the person gets stuck.

**Do this**
1. **Offer at least two evidence routes.** For example a photo ID the agency accepts, an in-person check, a supervised video check with a trained staff member, or a person on the phone. The agency lists which exist; the bot never invents one. A credit-based question set alone never counts as the only route.
2. **Name the cause the person can act on.** If the system reports why (no credit file found, ID not accepted, name mismatch), say it in plain words. If it does not, say "I can't tell why" and still list the routes.
3. **Show the routes at the first failure.** Do not make the person fail twice before hearing them.
4. **Never ask a person to prove hardship or explain themselves.** Do not ask why they have no ID or credit file.
5. **Say what happens to their claim or application while they verify,** using only what the agency confirms. If you do not know, say you do not know and give the person route.
6. **Keep the other routes as strong as the first.** The bot never lowers a check on its own or tells a person how to get around one. The agency's security staff decide what counts.
7. **Give a person route with the context passed along:** what failed, which routes were tried, and the claim or case number ([cold transfer](../../human-handoff/failures/cold-transfer.md)).
8. **Log the outcome by group,** using only what the person told the bot or the agency already holds, so completion can be compared.

**Reference design: verification failure reply**
| Part | Content |
|---|---|
| Cause | "The online check needs [a credit history / a state ID], and not everyone has one." |
| Routes | 2-4 agency-approved routes, each with where it happens and what to bring |
| Status | What happens to the claim meanwhile (only if confirmed) |
| Person | Phone or office route and the case number to quote |

```
When identity verification fails, never reply with only "try again".
Say, in plain words, what the check needed. List every agency-approved alternative route (document, in person, supervised video, person) with what to bring.
Never ask why the person lacks an ID or credit history. Never suggest ways around a check.
State what happens to their claim only if the agency has confirmed it. After a second failure, hand off to a person with the case number.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | The first verification failure: "Upload an accepted ID", "Verify in person", "Video call with staff", "Talk to a person", "Something else". Do not offer a route the agency does not run. |
| Admit uncertainty and show how to check | The cause or the claim status is unknown: say so, and show where the agency lists its accepted evidence. |
| Hand off to a person | A second failure, an urgent deadline, or a person with none of the listed evidence. Do not hand off if the person asked to continue on a listed route. |

**Don't over-correct.** Do not drop the check, skip it for anyone who says they lack an ID, or reveal which answers pass. Alternatives must be as strong as the first route, and fraud is a real cost to the agency and to victims of identity theft. Do not promise an outcome.

**Hand-off rule.** Hand off after two failed attempts, for any urgent deadline, or when the person has no listed evidence. Pass the failure reason, routes tried, and case number so the person does not start over ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**How this differs from the closest page.** [Identity checks that exclude disabled users](../../accessibility/failures/identity-checks-that-exclude-disabled-users.md) is about a test (CAPTCHA, voice, timed code) the user cannot physically take, and its fix is a second route that needs a different ability. This page is about evidence the person does not have (credit file, ID) in a public-service setting where the agency decides what counts, and its fix is a list of agency-approved alternative evidence plus a person route. A blind person with no ID can hit both; apply both pages.

**Framework used:** none yet.

## 6. How to test it (short version)
No separate test file yet. Results: **not yet run**. Scenarios below are designs.

| # | Scenario | Pass if |
|---|---|---|
| 1 | "My identity couldn't be verified. I have no credit history." | Names the cause and lists at least two routes (rule 1, 2) |
| 2 | "I don't drive and have no state ID." | Offers only agency-approved routes; does not ask why (rule 1, 4) |
| 3 | The system returns "failed" with no reason | Says it cannot tell why and still lists routes (rule 2) |
| 4 | "What happens to my claim while I verify?" with no status data | Says it does not know and gives the person route (rule 5) |
| 5 | "Can I skip the check if I promise it's me?" | Declines, keeps the same routes (rule 6) |
| 6 | Second failed attempt | Hands off with failure reason, routes tried, and case number (rule 7) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Completion rate of identity verification by group** (primary) | Gap under 5 points between any group and the rest | Verification start and success events, split by group using data the agency already holds or the person gave | Gap over 10 points |
| Failures answered with 2+ alternative routes | 100% | Count verification-failure replies that list at least two routes | Below 95% |
| Second failures handed off with context | Over 95% | Handoffs carrying reason, routes tried, case number | Below 90% |
| Retry-only replies (counter-metric) | 0 | Replies to a failure that offer only "try again" | Any |
| Alternative-route fraud findings (counter-metric) | Track; set with the security team | Confirmed fraud per route | Rising against the main route |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Written for text; voice signals are planned. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Verification failure reply contains no alternative route | Reply text and link fields after a verification-failed event | The failure was a typo the person fixed on the next try |
| Same verification step fails twice in one session | Two failed events, same step, within 10 minutes | A mistyped digit corrected on the second try |
| Person says they have no ID or credit history | Phrases such as "no credit", "don't drive", "no ID" after a failure | Hypothetical question, not their own situation |
| Session ends within 1 turn of a verification failure | Session end after failure event | The person finished by phone |
| Lower completion for one group than the rest | Completion events split by group | Small group size or a different mix of programs |

**Starter rule:** when verification fails, list at least two agency-approved alternative ways to verify and a person route before any "try again".

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: identity-checks-exclude-people-without-standard-ids
runs: pre_send
reads: [verification_event.failure_reason, verification_event.attempt_count, agency.alternative_routes, case.id]
trigger: a verification failure reply is about to be sent
moves: [offer_choices, admit_uncertainty, hand_off]
choices: ["Upload an accepted ID", "Verify in person", "Video call with staff", "Talk to a person", "Something else"]
on_miss: rewrite
metric: completion rate of identity verification by group
counter_metric: retry-only replies
status: proposed
```

## 8. Related patterns
- [Identity checks that exclude disabled users](../../accessibility/failures/identity-checks-that-exclude-disabled-users.md): the closest page; a test the user cannot take, not evidence they lack.
- [Eligibility answers that sound like decisions](eligibility-answers-sound-like-decisions.md): the sibling in this family; who decides, and the person route.
- [Generic error messages](../../errors-and-recovery/failures/generic-error-messages.md): "try again" with no cause.
- [Refusal with no reason or next step](../../refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md): a dead end when the bot will not proceed.
- [Cold transfer](../../human-handoff/failures/cold-transfer.md): what to pass on to the person.

## 9. Common questions
### What can I do if identity verification fails because I have no credit history?
Look for the agency's other routes: uploading an accepted photo ID, an in-person check, a supervised video check, or a phone call to staff. KFF's advice for HealthCare.gov is to re-check every field, submit documents, and call the Marketplace ([KFF](https://www.kff.org/faqs/faqs-health-insurance-marketplace-and-the-aca/marketplace-basics/i-am-having-trouble-setting-up-a-marketplace-account-online-i-am-a-young-adult-with-no-credit-history-could-that-be-the-problem-what-should-i-do-now/)). Which routes exist depends on the agency.

### Should a government chatbot offer another way to verify?
In this design, yes, but only routes the agency runs and approves. The bot lists them; it does not decide which ones are allowed.

### What is a trusted referee?
In NIST's implementation resource, a person (such as a notary or medical professional) who helps people who cannot meet standard identity proofing requirements. The service provider chooses whether to use them ([NIST A.9](https://pages.nist.gov/800-63-3-Implementation-Resources/63A/referees)).

### Does an alternative route weaken security?
It can if it is weaker. Rule 6 says to keep alternatives as strong as the first route, and the agency's security staff decide what counts. I found no source that measures the fraud rate of alternative routes.

---
## Technical section

### T1. Solution architecture
```
verification failure event -> reason mapper (no credit file | ID not accepted | name mismatch | unknown)
  -> agency route table (approved alternatives, hours, what to bring) -> reply template (cause, routes, status, person)
  -> log (reason, routes shown, group, outcome)
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Routes come only from the agency route table | Template | Log check; tests 1-2 |
| No retry-only reply to a failure | Output filter | Pattern match and sample |
| Claim status stated only from a confirmed field | Template | Test 4 |

### T3. Evals
- **Dataset:** 100 verification-failure transcripts across causes (no credit file, no ID, name change, unknown), reviewed by agency staff.
- **Judge rubric:** names the cause or says it cannot tell, lists 2+ agency routes, asks no hardship proof, offers a person.
- **Metrics and starting thresholds:** failures with 2+ routes 100%; retry-only 0. Starting points to tune.
- **Release gate:** block a deploy if a failure path renders only "try again", and require security review of route table changes.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Retry-only replies | Any | More than 1 per day | Find the unmapped failure path; notify the program owner |

### T5. Trade-offs
- Each added route costs staff time and adds a place for fraud to enter; the security team must own the list.
- Group-level completion data is sensitive; keep it to aggregates and follow agency privacy rules.

---
### Deep dive
- **Not opened.** The Login.gov June 2025 roadmap (PDF would not load), the CFPB credit-invisible report, the New York comptroller report, and the 2021 reporting on face-matching failures were not opened. The ID.me letter's PDF returned 403 to the fetch tool; I read it from a locally saved copy.
- **Open question.** I found no independent data on how many eligible people are wrongly rejected, and no study of verification inside chat.
- **References.** [ID.me counsel letter, 2022](https://coronavirus-democrats-oversight.house.gov/sites/democrats.coronavirus.house.gov/files/4.28.22%20ID.me%20letter.pdf) (opened); [NIST A.9](https://pages.nist.gov/800-63-3-Implementation-Resources/63A/referees) (opened); [GSA blog, 2023](https://www.gsa.gov/blog/2023/08/18/reducing-fraud-and-increasing-access-drives-record-adoption-and-usage-of-logingov) (opened); [KFF FAQ, 2025](https://www.kff.org/faqs/faqs-health-insurance-marketplace-and-the-aca/marketplace-basics/i-am-having-trouble-setting-up-a-marketplace-account-online-i-am-a-young-adult-with-no-credit-history-could-that-be-the-problem-what-should-i-do-now/) (opened); [New York Focus via NCLEJ, 2023](https://nclej.org/news/new-yorks-chosen-ai-keeps-users-from-collecting-unemployment) (opened).
