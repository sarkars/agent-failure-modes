---
title: "Meta AI Says an Activist Was at the January 6 Riot; Starbuck Sues Meta for Defamation, April 2025"
date: 2025-04-29
source: "https://ppc.land/content/files/2025/10/Starbuck-v-Meta.pdf"
description: "Robby Starbuck sued Meta in April 2025, alleging Meta AI falsely tied him to the January 6 riot and kept doing so for months after he complained."
summary: "On April 29, 2025, activist Robby Starbuck sued Meta Platforms for defamation in Delaware Superior Court. His complaint alleges Meta AI said he was at the January 6, 2021 Capitol riot and was charged with a misdemeanor, and kept repeating such claims for about nine months after he gave notice on August 5, 2024. Meta's Joel Kaplan apologized on X. CNN reported a settlement in August 2025 under which Starbuck advises Meta on bias. The claims were never decided by a court. Status: Needs review."
categories:
  - Governance
  - General-Purpose Assistants
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - corrections-not-applied
  - no-way-to-report-bad-behaviour
  - refusal-with-no-reason-or-next-step
---

**This page is a dated teardown of one US lawsuit over a chatbot that, the plaintiff alleges, kept stating false crimes about a named public figure after the company was told they were false, for teams whose assistant answers "who is this person?" and who own the route for fixing a wrong answer.** Every fact below comes from a source we opened (listed at the end).

**Read this first.** This page summarizes public reporting and one court filing, the complaint. Everything the complaint says is an allegation. No court ruled on whether Meta AI's statements were defamatory; the case settled. This is design analysis, not legal advice. Quotes of Meta AI output come from the complaint's text, not from screenshots we checked. **Status: Needs review.**

## What happened (as reported)

From the complaint (filed April 29, 2025, Delaware Superior Court, Case No. N25C-04-283 SKR CCLD), unless another source is named:

- **August 5, 2024: first sighting.** A Harley-Davidson dealership's X account posted a screenshot of Meta AI (using Llama 3.1, per the complaint) saying Starbuck was "present at" the riot and "accused of participating in or promoting the event." AP (Sarah Parvini, April 30, 2025) says Starbuck was then campaigning against Harley-Davidson's DEI policies.
- **Same day: his own check.** Starbuck says it was his first time using Meta AI. He alleges it told him he was arrested for a misdemeanor tied to January 6, was a "white nationalist," had been sued for defamation, and backed Nick Fuentes. The complaint says all of this is false and that he was home in Tennessee on January 6.
- **Same day: notice.** He tagged Meta executives on X, and his lawyer sent a cease-and-desist letter to Meta's chief legal officer.
- **August 8-23, 2024: investigation.** Meta's outside counsel said an investigation was under way. On August 9, a @support.facebook.com address replied to the letter that "we do not understand how we may be responsible for this content." Meanwhile, the complaint says, Meta AI told others he entered and filmed inside the Capitol. On August 23 counsel said Meta had made "enhancements" and that "Meta had taken appropriate action and considered the matter closed."
- **December 4, 2024: repeats.** The complaint says Meta AI again told a relative and a colleague he was at the riot and charged with a misdemeanor. It says Llama 3.2 had shipped in late September.
- **By April 2025: name blocked, claims still there.** The complaint says Meta AI's website now answered questions about him with "Sorry, I can't help you with this request right now." Yet asked who changed DEI at IBM, Walmart and Tractor Supply, it named him, and on the next prompt said "Robby Starbuck's past includes involvement in the January 6th Capitol riot."
- **April 21, 2025: voice.** A colleague heard Meta AI's voice feature say he pleaded guilty to disorderly conduct and promoted Holocaust denial. Starbuck recorded his own voice session; the complaint quotes it advising businesses to avoid him and saying "Authorities should consider removing parental rights to protect them."
- **The suit.** One count, defamation per se. It seeks an injunction against republishing statements found defamatory, damages "estimated to exceed $5,000,000," and punitive damages. Dhillon Law Group's release is dated April 28, 2025; the court stamp reads April 29.
- **April 29-30, 2025: Meta's reply.** AP, Fox Business (David Spector) and AOL (Daily Caller, Robert McGreevy) report that Joel Kaplan, Meta's chief global affairs officer, wrote on X: "This is clearly not how our AI should operate." He said he was sorry that "the fix we put in place didn't address the underlying problem." A Meta spokesperson told AP "we have already released updates and will continue to do so."
- **May 7, 2025.** NewsGuard (Sofia Rubinson, May 9) asked Meta AI whether he took part in the riot. It answered: "Robby Starbuck was not at the January 6, 2021, Capitol riot."
- **August 2025: settlement.** CNN (Clare Duffy, August 14, 2025) reports Meta announced a settlement "on Friday." A joint statement says they "resolved this matter to our mutual satisfaction" and will work to "minimize the risk that the model returns hallucinations in response to user queries." CNN says Starbuck will advise Meta on "bias." Meta declined to discuss financial terms.
- **A separate case.** Reuters (via Al Jazeera, October 22, 2025) reports Starbuck sued Google in Delaware state court, alleging Bard and Gemma produced "outrageously false" claims about him. A Google spokesperson called most claims Bard "hallucinations" it addressed in 2023. We did not open that complaint.

## What the user saw

Two groups of users saw different things. People who asked about Starbuck got fluent, specific statements of crimes: an arrest, a charge, a guilty plea, filming inside the Capitol, with no source they could open. Later, a question that named him got a flat "Sorry, I can't help you with this request right now," with no reason. The complaint argues that refusal itself made people wonder what he did. Starbuck, the subject, was not the user at first. A stranger's screenshot told him. His complaint got a form reply that pointed him to "the party responsible for posting the content."

## Where in the flow it broke

1. **Answer about a named person.** The model stated crimes as fact, with no checkable source (alleged).
2. **Report intake.** The legal letter reached a support queue that treated Meta AI's output like user-posted content (per the August 9 email quoted in the complaint).
3. **Fix.** The fix the complaint describes was a block on his name, not a correction.
4. **Coverage of the fix.** Questions that described him without his name got around the block (alleged). Kaplan's post concedes the fix missed the underlying problem.
5. **New surface.** The voice feature repeated and extended the claims, and turned them into advice about hiring him and about his children (alleged).
6. **Verification.** No source shows a test, before or after the fix, of reworded prompts or the voice channel.

## How this differs from Walters and noyb

- [Walters v. OpenAI](chatgpt-false-embezzlement-claim-walters-v-openai-defamation-ruling-may-2025.md): one journalist, one chat, caught within hours, no notice to OpenAI, and a court ruling for OpenAI. Here the complaint alleges many third-party readers, months of repeats *after* notice, and a failed fix. It settled, so no court weighed the claims.
- [noyb's complaint over ChatGPT](chatgpt-false-claims-about-a-person-noyb-complaint-march-2025.md): a GDPR accuracy complaint by a private person, filed with a regulator. Starbuck is a public figure suing for damages under US law. Both sources say the visible output was fixed while the claim may persist below it.
- What is new here: the fix-then-repeat cycle, the jump to a voice channel, and a name-block that refuses instead of correcting.

## Which patterns it illustrates

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Strong fit.** Specific crimes stated in a sure tone, in text and in a voice the complaint calls "confident," with no source.
- [Corrections not applied](../goals/dialogue-management/failures/corrections-not-applied.md) (`corrections-not-applied`). **Partial fit.** The old false claim came back after the company said it was fixed. Partial, because that pattern covers a correction inside one chat; here it was made through lawyers and applied across all users.
- [No way to report bad behaviour](../goals/measurement-and-feedback/failures/no-way-to-report-bad-behaviour.md) (`no-way-to-report-bad-behaviour`). **Partial fit.** The subject was not a user, and his report met a form reply. The complaint asks for "a user-friendly report mechanism" for false claims about a person.
- [Refusal with no reason or next step](../goals/refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md) (`refusal-with-no-reason-or-next-step`). **Partial fit.** The name block gave no reason and no correct answer.
- **Considered, not mapped.** [False premises accepted](../goals/dialogue-management/failures/false-premises-accepted.md): the prompts asking for advice based on the earlier answers built on the bot's own claims, not a user's false premise. [Over-refusal of ordinary requests](../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md): close to the name block, but that pattern is about a word that looks risky. [Over-correcting for identity](../goals/fairness-and-identity/failures/over-correcting-for-identity.md): the settlement mentions bias, but no source shows tailoring by identity. [Privacy-rights requests not recognised](../goals/privacy-and-governance/failures/privacy-rights-requests-not-recognised.md): this was a defamation demand, not a data-rights request.
- **Possible gaps for a person to judge.** (1) As the Walters and noyb pages note, no pattern covers false accusations about a named third party. (2) No pattern covers a fix that blocks a name instead of correcting the claim, or a fix that fails on reworded prompts. (3) No pattern covers a fix applied to one surface (web text) but not another (voice). Proposals, not decisions.

## What to measure

Our proposals, not Meta's. Status: Not yet run. Thresholds are for the team to set.

| Signal | How to compute |
|---|---|
| Reported-claim recurrence | Per reported false claim, share of a fixed set of prompts (name, description without name, other language, voice) that still produce it, run daily |
| Unsourced crime claims | Replies that say a named person was arrested, charged or convicted, divided by those that cite a retrievable source |
| Time to correct | Hours from a report about a named person to a passing recurrence check |
| Block-instead-of-fix | Reported people whose name now gets a refusal, divided by all reported people |
| Report routing | Reports about model output sent to the user-content queue, divided by all reports about model output |

## What a team can change

Our proposals, each a pass/fail check on a transcript. Status: Not yet run.

1. **No crime without a source.** Pass: a "who is [name]?" test returns no arrest, charge or plea unless a source is shown; otherwise the bot says it has no reliable record.
2. **Test a fix like an attacker.** Pass: after a fix, the reported claim does not appear for the name, a description without the name, a follow-up turn, or the voice channel.
3. **Correct, don't erase.** Pass: a question about a reported public figure gets a sourced answer, not a bare refusal, unless a stated reason is given.
4. **Route output reports to the model team.** Pass: a report that quotes the bot's own answer is not answered by telling the reporter to contact whoever posted it.
5. **One fix list for every surface.** Pass: each logged correction has a check for text, voice and any app that uses the same model.
6. **Don't over-correct.** Pass: ordinary questions about public figures still get answered after a fix.

## What is unverified

- **Screenshots and the voice recording.** We read the complaint's text only; we did not check its images or the linked video.
- **Anti-vaccine claim.** Fox Business says the suit alleges this; we did not find it in the complaint text.
- **Settlement date and terms.** CNN says "on Friday" in an August 14 story; we did not confirm the date. Whether the suit was formally dismissed, and any payment, are not in what we opened. A search summary said he dropped the suit in August; not used.
- **Meta's side.** No Meta filing or answer to the complaint was opened. Meta's August 2024 claim that other AI tools gave "similar" answers is reported only through the complaint.
- **The Wall Street Journal.** AOL says the WSJ first reported the suit. We did not open it.
- **Google case details** beyond the Reuters text, including the $15 million figure as filed. CourtListener was not searched successfully; no docket was opened.

## Sources

| URL | Publisher (author) | Date | Opened |
|---|---|---|---|
| https://ppc.land/content/files/2025/10/Starbuck-v-Meta.pdf | Starbuck v. Meta Platforms complaint, Del. Super. Ct. (Dhillon Law Group; Shaw Keller LLP) | 2025-04-29 | Yes, 2026-10-24, PDF converted to text; quotes checked word for word |
| https://www.dhillonlaw.com/lawsuits/starbuck-v-meta/ | Dhillon Law Group press release | 2025-04-28 | Yes, 2026-10-24, raw HTML read as text |
| https://www.ksat.com/business/2025/04/30/conservative-activist-robby-starbuck-sues-meta-over-ai-responses-about-him/ | AP via KSAT (Sarah Parvini) | 2025-04-30 | Yes, 2026-10-24, raw HTML read as text; quotes checked |
| https://www-ak-ms.foxbusiness.com/media/robby-starbuck-sues-meta-claiming-ai-chatbot-defamed-him | Fox Business (David Spector) | 2025-04-30 | Yes, 2026-10-24, raw HTML read as text |
| https://www-ak-ms.foxbusiness.com/media/robby-starbuck-says-its-too-late-meta-apologize-after-ai-chatbot-allegedly-defamed-him | Fox Business (David Spector) | 2025-05-01 | Yes, 2026-10-24, raw HTML read as text |
| https://www.aol.com/news/meta-exec-apologizes-conservative-influencer-213223722.html | Daily Caller via AOL (Robert McGreevy) | 2025-04-30 | Yes, 2026-10-24, raw HTML read as text |
| https://www.newsguardrealitycheck.com/p/conservative-activist-sues-meta-ai | NewsGuard Reality Check (Sofia Rubinson) | 2025-05-09 | Yes, 2026-10-24, raw HTML read as text; quote checked |
| https://abc17news.com/news/2025/08/14/right-wing-activist-robby-starbuck-joins-meta-as-an-ai-advisor-focused-on-bias/ | CNN via ABC17 (Clare Duffy) | 2025-08-14 | Yes, 2026-10-24, raw HTML read as text; quotes checked |
| https://www.aljazeera.com/economy/2025/10/22/conservative-activist-sues-google-over-ai-generated-statements | Reuters via Al Jazeera | 2025-10-22 | Yes, 2026-10-24, raw HTML read as text; quotes checked |

Not opened: the AP original on washingtontimes.com (HTTP 403) and the Reuters copy on StreetInsider (HTTP 403). Seen only in search results: Bloomberg Law and Fox News on the Google suit, PinkNews, GCN and CO/AI on the settlement, and AI Incident Database report 6296.

## Corrections

If you have a Meta filing, the dismissal order, or the settlement date, tell us and we will fix this page.
