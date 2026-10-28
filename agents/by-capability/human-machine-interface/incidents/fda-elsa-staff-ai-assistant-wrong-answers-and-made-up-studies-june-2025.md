---
title: "FDA staff say the agency's Elsa AI assistant gave outdated and wrong answers and made up studies, June and July 2025"
date: 2025-06-04
source: "https://www.cnn.com/2025/07/23/politics/fda-ai-elsa-drug-regulation-makary"
description: "FDA staff told reporters the agency's Elsa chat assistant gave outdated facts, miscounted approved drugs and cited studies that do not exist."
summary: "On June 2, 2025, the US Food and Drug Administration rolled out Elsa, a generative AI chat assistant for its own staff. Two days later, RAPS Regulatory Focus reported that officials said Elsa named Robert Califf as the current commissioner and gave other outdated answers, while one reviewer said it worked well on uploaded test reports. On July 23, 2025, CNN reported that three current FDA employees said Elsa made up nonexistent studies or misrepresented research, and that it gave wrong answers to questions such as how many drugs carry a certain label. The FDA's head of AI told CNN that Elsa could potentially hallucinate; the commissioner said its use is optional. No opened source reports a regulatory decision changed by an Elsa error. Status: Needs review."
categories:
  - Government
  - Health care
  - Accuracy
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - doesn-t-say-what-it-can-do
  - users-must-engineer-prompts-to-get-good-results
---

**This page is a dated teardown of reported failures in Elsa, the US Food and Drug Administration's internal AI chat assistant, in June and July 2025, for teams that build or run a chat assistant for government or health staff who use its answers in their work.** The product was Elsa, a chat tool the FDA rolled out to its staff on June 2, 2025. The users were FDA employees, including scientific reviewers. The moments that matter are ordinary questions typed into a box that says "Ask Elsa anything": who runs the agency, how many drugs carry a certain label, what studies support a point. Staff told reporters that some answers were out of date, some counts were wrong, and some cited studies did not exist. The date above is the first original report we opened (RAPS, June 4, 2025); the main reporting on made-up studies is CNN's, July 23, 2025.

**Status: Needs review.** Three sources were downloaded on 2026-10-28 as raw HTML and read as plain text: CNN (Sarah Owermohle, July 23, 2025), RAPS Regulatory Focus (Ferdous Al-Faruque, June 4, 2025) and BioSpace (Natalia Mesa, June 30, 2025). CNN and RAPS are original reporting: each spoke with FDA staff and officials. BioSpace is secondary on the launch errors (it cites NBC News and STAT News) and original only for its own expert interviews. Each quote below was checked word for word against the downloaded text with a script, with curly and straight quote marks treated as the same. The FDA's own June 2, 2025 press release could not be downloaded as raw text (the request was blocked); a summarizing fetch tool showed its headline and date, and we quote it only where CNN, RAPS or BioSpace quote it.

> **Read this first.** This is a summary of public reporting, not a finding of fact, and not legal, medical or regulatory advice. The employees who described errors spoke without their names; we did not see their chats, the "documents seen by CNN," or any Elsa answer ourselves. No opened source says an Elsa error changed a drug or device decision. We name only people who spoke on record: FDA Commissioner Marty Makary, FDA head of AI Jeremy Walsh, and outside experts quoted by name.

**Channel note.** This is a text incident: staff typed questions into a web chat inside the agency and read typed answers. This phase of the knowledge base is chat-first, and the signals and checks below are written for chat transcripts. Voice and web signals, such as an assistant that reads answers aloud or a public web page that repeats an assistant's output, are PLANNED only: never detected or measured here.

## What happened (as reported)

- **June 2, 2025: launch.** Per RAPS, Makary announced that day that the agency had launched Elsa almost a month ahead of schedule. In a video he said: "One scientific reviewer told me, what took him two to three days, now takes six minutes." CNN reports that Makary said the rollout came "ahead of schedule and under budget."
- **The screen.** Per CNN, which was given a demonstration, Elsa "welcomes the user with "How can I help you?" above an entry field that says "Ask Elsa anything," much like other popular publicly used AI."
- **Outdated answers, per RAPS.** One high-level official told RAPS: "It was trained on Anthropic's Claude so it only has public data through April 2024." Two high-level officials said that, asked who the current FDA commissioner and chief counsel are, Elsa answered Robert Califf and Stacy Amin; RAPS notes Amin left the agency in 2021.
- **A political question, per RAPS.** Asked who Robert F. Kennedy Jr. is, Elsa did not say he was the HHS secretary. It said it does not give personal opinions or engage in political discussions, then said: "However, I can provide some factual, FDA-relevant information related to Robert F. Kennedy Jr."
- **A good report, per RAPS.** A reviewer who uploaded test reports said: "I used it to query test reports and confirmed the accuracy," and "It only had two minor mistakes." The same reviewer said: "I'm kind of using it like the Google NotebookLM and not like the ChatGPT tool."
- **The on-screen warning, per RAPS.** "Elsa can make mistakes. Please verify responses," the AI states. "Elsa's knowledge is current through April 2024." RAPS says Elsa's disclaimers call it an assistive tool and not a "decision maker."
- **Launch-day errors, secondhand.** BioSpace, citing NBC News, says some responses were "incorrect or only partially accurate." We did not open the NBC News or STAT News reports.
- **Made-up studies, per CNN.** Elsa "has also made up nonexistent studies, known as AI "hallucinating," or misrepresented research, according to three current FDA employees and documents seen by CNN." One employee: "Anything that you don't have time to double-check is unreliable. It hallucinates confidently." A second: "AI is supposed to save our time, but I guarantee you that I waste a lot of extra time just due to the heightened vigilance that I have to have."
- **Wrong counts, per CNN.** Employees asked questions "like how many drugs of a certain class are authorized for children to use or how many drugs are approved with a certain label." In both cases, CNN reports, Elsa returned wrong answers. When one employee told it a count was wrong, it admitted the mistake. "But it still doesn't help you to answer the question," that employee said.
- **What it could not see, per CNN.** Two staffers said Elsa could not help with review work because it could not reach many relevant documents, such as industry submissions.
- **After a correction, per CNN.** Told that a cited study does not exist, Elsa is usually "apologetic," one employee said. In one shared case, it insisted a research area was not in the FDA's purview; CNN reports that it was.

## What the organization said

- **Jeremy Walsh, FDA head of AI, to CNN.** "Elsa is no different from lots of [large language models] and generative AI," and "They could potentially hallucinate." On the errors: "Some of those responses don't surprise me at all. But what's important is … how we address those gaps in the capability."
- **Walsh's fixes, as CNN reports them.** Training, personal document libraries "in the coming weeks," and a feature that lets users click a summary to see which parts of a document it cited. CNN notes that feature worked only for internal documents and could not link to journal articles. Walsh also said hallucinations can be reduced by asking more precise questions.
- **Marty Makary, FDA commissioner, to CNN.** "I have not heard those specific concerns, but it's optional," and "They don't have to use Elsa if they don't find it to have value." On double-checking: "You have to determine what is reliable information that [you] can make major decisions based on, and I think we do a great job of that." He said most scientists were using Elsa for its "organization abilities."
- **HHS to BioSpace.** BioSpace says HHS did not respond to its request for comment.

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| Does it work | RAPS: one reviewer found it accurate on uploaded test reports, with "two minor mistakes." CNN: three current employees describe made-up or misrepresented studies. CNN also reports Elsa is useful for meeting notes, summaries and templates. |
| Why it was wrong | The RAPS reviewer blamed the April 2024 knowledge date. CNN's employees describe made-up studies, which a date cutoff does not explain. Walsh said precise questions help. |
| How many use it | Makary and Walsh told CNN more than half of staff had logged time in Elsa. The staff CNN spoke with said use in their areas was weak or limited. |
| How it checks itself | Walsh pointed to clickable citations. CNN: that works only for internal documents. BioSpace quotes Adam Rodman of Harvard: "People have a tendency to trust AI systems." |
| Scale of errors | No opened source gives an error rate, a count of wrong answers, or any FDA test results. |

## Where in the conversation flow it broke

Based on the sources above, and only as far as they go.

1. **Open box, no scope.** The entry field says "Ask Elsa anything." No opened source says the screen told staff which documents Elsa could and could not reach.
2. **A question about live facts.** Asked who leads the agency, Elsa answered from data that ended in April 2024, per RAPS, in the voice of a current fact.
3. **A question it lacked data for.** Asked to count drugs with a certain label, it gave a number, per CNN, rather than saying it could not see the full list.
4. **A cited source that does not exist.** Per CNN, Elsa cited nonexistent studies. For journal articles, there was no link to click to check.
5. **The correction turn.** Told it was wrong, Elsa apologized but did not reach a right answer, per CNN.
6. **The burden lands on the reader.** A generic "Please verify responses" line sits on screen. Staff told CNN that checking every answer cost them time.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). Each fit rests on anonymous staff accounts relayed by reporters; no opened source shows a full Elsa transcript.

- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Strong fit.** Wrong counts and made-up studies were given as answers, an employee said it "hallucinates confidently," and for journal articles there was no source link to check.
- [Doesn't say what it can do](../goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md) (`doesn-t-say-what-it-can-do`). **Partial fit.** The box invites "Ask Elsa anything," yet it could not reach industry submissions and its public knowledge ended in April 2024. The on-screen date notice, per RAPS, is a partial scope statement, so the fit is not full.
- [Users must engineer prompts to get good results](../goals/onboarding-and-discoverability/failures/users-must-engineer-prompts-to-get-good-results.md) (`users-must-engineer-prompts-to-get-good-results`). **Partial fit.** Walsh's answer to hallucinations was to ask more precise questions, which puts the fix on the user. No opened source shows an example of a vague versus precise question.
- [Corrections not applied](../goals/dialogue-management/failures/corrections-not-applied.md) (`corrections-not-applied`). **Weak fit.** Elsa accepted corrections but still did not answer the question. That entry is about an old value coming back after a correction, which no source describes.
- [Over-refusal of ordinary requests](../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md) (`over-refusal-of-ordinary-requests`). **Weak fit.** Elsa insisted one research area was outside the FDA's purview, per CNN, and treated a question about the HHS secretary as political, per RAPS. Both are single reports.
- **Considered, not a fit.** [Deferring work to the user](../goals/effort-and-memory/failures/deferring-work-to-the-user.md) (`deferring-work-to-the-user`): that entry is about a bot that has the data and tells the user to look it up; here staff checked answers because they could not trust them. [Excess disclaimers and warnings](../goals/refusals-and-boundaries/failures/excess-disclaimers-and-warnings.md) (`excess-disclaimers-and-warnings`): only one short warning is reported. [Notes approved without being read](../goals/healthcare-agents/failures/notes-approved-without-being-read.md) (`notes-approved-without-being-read`): no one is reported acting on an unread Elsa output. [Clean-lab testing](../goals/measurement-and-feedback/failures/clean-lab-testing.md) (`clean-lab-testing`): no opened source describes how Elsa was tested before launch.
- **Possible gaps for a person to judge.** (1) No pattern covers an assistant answering questions about current facts (who holds an office now) from a fixed knowledge date, with the date shown only as a general notice. (2) No pattern covers an internal staff assistant whose errors shift a checking burden onto expert employees. These are proposals, not decisions.

## How it differs from close cases

- [Amazon Q preview: employees report hallucinations (December 2023)](amazon-q-business-chatbot-hallucinations-and-confidential-data-leaks-december-2023.md): also an assistant for staff, also reported through leaked or anonymous accounts. Amazon Q was a product sold to other companies; Elsa is a government agency's own tool for regulators.
- [Canada Revenue Agency Charlie chatbot audit (October 2025)](canada-revenue-agency-charlie-chatbot-wrong-tax-answers-october-2025.md): a government chatbot with wrong answers, but public-facing and measured by an auditor's test. Elsa's errors come from staff accounts, with no test results.
- [Pieces Technologies and the Texas attorney general (September 2024)](pieces-technologies-texas-attorney-general-clinical-ai-hallucination-rate-claims-september-2024.md): a dispute over an advertised accuracy figure for a health AI. For Elsa, no accuracy figure was published at all; leaders cited time saved instead.

## What to measure

Proposed signals, not results. Status: Not yet run. Text signals are proposed; voice and web signals are PLANNED only and are not detected or measured. Each signal can be computed from chat logs plus a labeled review set; each has a counter-signal so a team does not fix one thing by breaking another.

| Signal | How to compute from logs | Counter-signal |
|---|---|---|
| Unresolvable citation rate | Share of answers that cite a study, document or rule that a lookup in the source library or a citation index cannot find | Share of answers that give no source at all, so citations are not dropped to pass this check |
| Current-fact answers past the knowledge date | Share of questions about who holds a role or what is current that are answered from model memory rather than a dated lookup | Share of such questions refused outright when a dated lookup was available |
| Count-question accuracy | On a labeled set of "how many" questions with known answers, share answered with the right number | Share answered "I can't count that" when the data was in reach |
| Out-of-reach admission | Share of questions needing data the tool cannot reach (for example, industry submissions) where the reply says so | Share of in-reach questions wrongly called out of reach |
| Correction recovery | After a user says an answer is wrong, share of next replies that give a checked answer or say plainly it cannot | Share of right answers the bot drops just because the user pushed back |
| Re-ask after a wrong answer | Share of sessions where the user types the same question a second time after saying the first answer was wrong | Share of sessions ended right after the first answer with no sign the answer was used |

## What a team can change

Our proposals, not the FDA's. Each is a pass/fail check on a transcript or a test run. Status: Not yet run. Test sizes and thresholds are for the team to set.

1. **No citation without a match.** Pass: every study or document named in an answer resolves to a record in the source library or a citation index, and the link is shown. Fail: a citation with no match is shown as fact.
2. **Look up live facts, or say the date.** Pass: asked "Who is the FDA commissioner?", the reply comes from a dated internal source or says "My information ends in April 2024; check the current staff directory." Fail: a name from model memory stated as current.
3. **Say what you cannot see.** Pass: asked how many approved drugs carry a certain label, a tool without the full label list says it cannot see the full list, names where the answer lives, and gives no number. Fail: a number.
4. **Scope on the first screen.** Pass: the opening screen lists which document sets Elsa can read and which it cannot. Fail: only "Ask Elsa anything."
5. **Fix, don't just apologize.** Pass: after "That study does not exist," the next reply either gives a citation that resolves or says it has no source. Fail: an apology followed by another unverified claim.
6. **Ask, don't make the user craft the prompt.** Pass: when a question is too broad to answer from the library, the bot asks one clarifying question. Fail: a broad answer with made-up specifics.

## What we could not verify

- The NBC News and STAT News launch reports. Not opened; we use only BioSpace's short attribution to them.
- The FDA's June 2, 2025 press release in raw text. The download was blocked; we quote it only as CNN, RAPS and BioSpace quote it.
- The "documents seen by CNN" and any full Elsa transcript. Not public in the opened sources.
- Which model and vendor power Elsa. RAPS quotes an official on Anthropic's Claude; BioSpace, citing STAT, adds Deloitte. Neither is an FDA statement we opened.
- Search summaries said STAT News described staff finding hallucinated studies and regulatory citations, and that Pharmaceutical Executive and Medical Economics covered the CNN interview. Seen only in search summaries; not used.
- Whether the promised document libraries or other fixes shipped, and whether errors fell after them. No opened source reports it.
- Whether any regulatory decision used a wrong Elsa answer. No opened source reports it.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://www.raps.org/resource/fda-s-elsa-ai-tool-gets-mixed-response-from-some-s.html | RAPS Regulatory Focus (Ferdous Al-Faruque), original reporting | 2025-06-04 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.biospace.com/fda/fdas-ai-rollout-raises-questions-around-readiness-legality | BioSpace (Natalia Mesa); secondary on launch errors, original for expert interviews | 2025-06-30 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.cnn.com/2025/07/23/politics/fda-ai-elsa-drug-regulation-makary | CNN (Sarah Owermohle), original reporting | 2025-07-23 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.fda.gov/news-events/press-announcements/fda-launches-agency-wide-ai-tool-optimize-performance-american-people | US Food and Drug Administration (press release) | 2025-06-02 | Partly: raw download blocked on 2026-10-28; headline and date seen through a summarizing fetch only; not quoted directly |

## Corrections

If you have the FDA's own test results for Elsa, a full transcript of a reported error, the NBC News or STAT News launch reports, or a dated FDA statement on fixes, from a source we can open, tell us and we will fix this page.
