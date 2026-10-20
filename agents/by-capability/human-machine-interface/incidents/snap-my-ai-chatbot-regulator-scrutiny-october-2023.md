---
title: "Snapchat's My AI Chatbot Draws a UK Regulator's Notice (October 2023) and an FTC Referral (January 2025)"
date: 2023-10-06
source: "https://cy.ico.org.uk/about-the-ico/media-centre/news-and-blogs/2024/05/ico-warns-organisations-must-not-ignore-data-protection-risks-as-it-concludes-snap-my-ai-chatbot-investigation"
summary: "Snap launched the My AI chatbot in February 2023 to Snapchat+ subscribers and to all users in April. TechCrunch, citing a Washington Post report, said the bot gave unsafe replies soon after launch. The UK ICO issued a preliminary enforcement notice on Oct 6, 2023 and closed the case in May 2024. In January 2025 the FTC said it referred a complaint to the Justice Department."
categories:
  - Governance
patterns:
  - child-user-treated-as-adult
  - no-way-to-report-bad-behaviour
---

**This page is a dated teardown of one public chatbot launch that regulators questioned, for teams that put a general-purpose chatbot in an app that teens use.** Read this first: the two regulator documents we opened say little about what the bot actually said. The FTC statement is one page and describes the complaint only in general terms. Neither regulator's findings on the facts are public in what we read.

## What happened (as reported)

- **Feb 27, 2023.** Per the ICO's May 2024 announcement, Snap launched My AI for Snapchat+ subscribers. Snap's April 2023 post says it was built with OpenAI's GPT technology.
- **Before Apr 5, 2023.** TechCrunch (Ivan Mehta, April 5) says a Washington Post report, days after the Snapchat+ launch, said the bot responded in an unsafe and inappropriate manner. We did not open the Post article, so we do not repeat its examples.
- **Apr 4, 2023.** Snap published "Early learnings from My AI and new safety enhancements." It said some users tried to trick the bot into answers that break Snap's guidelines. It said 0.01% of My AI responses were non-conforming, a category it defines (violence, sexually explicit terms, drug use, bullying, hate speech and similar). Its most common example was the bot repeating inappropriate words users had asked about. It announced OpenAI moderation tooling, temporary access limits for misuse, an age signal drawn from a user's birthdate, and a Family Center view for parents (both parent and teen must opt in).
- **Apr 19, 2023.** Per the ICO, My AI became available to all Snapchat users.
- **June 2023.** The ICO opened an investigation after concerns that Snap had not adequately assessed data protection risks.
- **Oct 6, 2023.** The ICO issued Snap a preliminary enforcement notice (ICO announcement; LBC report). LBC says the ICO called its findings provisional and said no conclusions should be drawn. LBC also says Snap could have been required to stop offering My AI to UK users until it completed an adequate risk assessment. LBC quotes Snap as saying it was closely reviewing the provisional decision.
- **May 21, 2024.** The ICO said it had closed the investigation. It said Snap did a more thorough review, showed it had put mitigations in place, and now had a compliant risk assessment. Its Executive Director of Regulatory Risk called the case a "warning shot for industry."
- **June 19, 2024.** The ICO's decisions page lists a decision: Snap's revised assessment complies with Article 35 UK GDPR, and Snap did not infringe Article 36 by not consulting the ICO before launch.
- **Jan 16, 2025.** The FTC published a statement saying it referred a complaint against Snap to the Justice Department. It says the complaint concerns deploying My AI in Snapchat and the allegedly resulting risks and harms to young users. It says the review began from compliance checks on a 2014 settlement and that the Commission also looked at other possible violations.

## What the failure was

The sources describe a risk-assessment and young-user safety concern, not one logged bad reply:

- **ICO:** the issue was whether Snap assessed the data protection risks of the chatbot before launch. The ICO later said the revised assessment was compliant.
- **FTC:** the complaint concerns allegedly resulting risks and harms to young users. The statement gives no specifics, and the complaint itself was not in what we opened.
- **Snap:** it attributes the early problems to users probing the bot and to the bot repeating their words, and it published its own rate. We found no independent check of the 0.01% figure or its method.

## Where the sources disagree or are silent

| Topic | What the sources say |
|---|---|
| Who the risk was for | LBC says the ICO's concern centered on children; the ICO's May 2024 page we opened does not mention children. The ICO's October announcement, which would settle this, did not load. |
| Outcome | The ICO closed its case in Snap's favor on the assessment. The FTC referral came later and covers different law. They are not in conflict. |
| Current status of the FTC matter | We did not find whether the Justice Department filed a complaint. |
| Cause of the bad replies | Snap's explanation is user tricks and repetition. The sources do not give an independent cause. |

## What the sources do not say

- What My AI said in any specific test, or how many young users got an unsafe reply. Snap gives one rate for all users, not by age.
- How the age signal works when a user gives a false birthdate.
- What the revised risk assessment contained. The ICO did not publish detail in what we read.
- Whether any child was harmed. No opened source reports a case.
- What the FTC complaint alleges beyond the one-paragraph statement.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [Chatbots and kids: when the user might be a child or teen](../goals/age-adaptation/failures/child-user-treated-as-adult.md) (`child-user-treated-as-adult`). Partial fit. The regulators' concern is about risk to young users from a general chatbot, and Snap added an age signal after launch. No opened source shows the bot answering a specific child badly. The fit is on the pre-launch question: did the team plan for a 13-to-17-year-old user.
- [No way to report bad behavior](../goals/measurement-and-feedback/failures/no-way-to-report-bad-behaviour.md) (`no-way-to-report-bad-behaviour`). Weak, partial fit, on the fix side only. Snap's post says users can report concerning replies in the app. Nothing we read says the path was missing or broken.

## Where in the flow it broke

Based on the sources, and only as far as they go:

1. **Pre-launch assessment.** The ICO's issue, later resolved by a revised assessment.
2. **Age handling at launch.** Snap's age signal was announced about five weeks after the Snapchat+ launch (Feb 27 to Apr 4).
3. **Abuse of the bot.** Snap says users probed it. Its post lists moderation and temporary access limits as new.
4. **Oversight.** Two regulators acted: one closed its case, one referred a complaint.

## What to measure

Our analysis, not Snap's or a regulator's. Status: Not yet run.

| Metric | How to compute from logs |
|---|---|
| Unsafe-reply rate by age band | Reviewer-rated unsafe replies divided by replies, split by under-13 / 13-17 / 18+ account age |
| Echo rate | Bot replies that repeat a user-supplied sensitive word, divided by replies |
| Age-claim mismatch | Sessions where the user states an age that differs from the account birthdate |
| Report-to-fix time | Days from a "this reply was a problem" tap to a logged decision |

## What a team can change

Our analysis, not the companies' or regulators'. Status: Not yet run.

1. **Write the child risk assessment before launch.** Check: a dated assessment names under-18 users, sample prompts and mitigations, and exists before the release date.
2. **Test with a teen persona set.** A fixed set of prompts from a stated 13-year-old account covering alcohol, sex and self-harm. Check: every reply refuses, redirects or gives safe help; 0 give how-to detail.
3. **Use the account age even when the user never states it.** Check: the same prompt gets a different, safer reply on a 13-year-old account than on a 30-year-old one.
4. **Do not echo.** A scripted "repeat this word" request with a blocked word returns no blocked word. Check: 0 blocked words in a scripted set.
5. **Give a one-tap report on every reply that logs the reply and the account age band.** Check: the tap writes a record.
6. **Do not over-correct.** If rule 2 blocks ordinary health or school questions, teens lose real help. Run rule 2 alongside a set of ordinary teen questions and require normal answers.

## Sources

| URL | Publisher | Date | Status |
|---|---|---|---|
| https://cy.ico.org.uk/about-the-ico/media-centre/news-and-blogs/2024/05/ico-warns-organisations-must-not-ignore-data-protection-risks-as-it-concludes-snap-my-ai-chatbot-investigation | UK ICO | 2024-05-21 | Opened 2026-10-20 |
| https://ico.org.uk/action-weve-taken/other-decisions/ | UK ICO | 2024-06-19 (decision entry) | Opened 2026-10-20 |
| https://www.ftc.gov/system/files/ftc_gov/pdf/commission-statement-snap.pdf | FTC | 2025-01-16 | Opened 2026-10-20 |
| https://newsroom.snap.com/early-learnings-from-my-ai-and-new-safety-enhancements | Snap | 2023-04-04 | Opened 2026-10-20 |
| https://techcrunch.com/?p=2524297 | TechCrunch (Ivan Mehta) | 2023-04-05 | Opened 2026-10-20 |
| https://www.lbc.co.uk/article/91d28745e68148c38ef2927ad2b73ce7-DWzgzt_2/ | LBC | Oct 2023, updated 2026-02-10 | Opened 2026-10-20 |
| https://www.freevacy.com/news/ico/ico-satisfied-with-snaps-my-ai-data-protection-risk-assessment/5289 | Freevacy | 2024 | Opened; used only to cross-check the Oct 6, 2023 and May 21, 2024 dates |

Summary only, not used above: the ICO's October 2023 announcement (our fetch returned 404; its dates and terms appear only in a search summary and in LBC), the Washington Post test (not opened; its exact ages and examples differ across the second-hand accounts in search summaries), a Center for Humane Technology test described in news summaries, and a claim in a search summary that Commissioner Ferguson dissented from the FTC referral. The FTC page we opened says only that he was recorded absent and issued a separate statement, so we use neither claim. Law-firm and trade summaries of the ICO case (DAC Beachcroft, Michalsons, Burges Salmon, IAPP) loaded without their body text or were not opened.

## Corrections

If you have the ICO's October 2023 notice, the full ICO decision, or the FTC complaint if it is filed, tell us and we will fix this page.
