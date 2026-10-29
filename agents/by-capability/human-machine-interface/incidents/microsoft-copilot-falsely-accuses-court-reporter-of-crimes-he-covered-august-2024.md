---
title: "Microsoft Copilot Falsely Accuses a German Court Reporter of Crimes He Covered, August 2024"
date: 2024-08-20
source: "https://www.theregister.com/2024/08/26/microsoft_bing_copilot_ai_halluciation/"
description: "In August 2024, reports said Microsoft Copilot cast court reporter Martin Bernklau as the criminal in trials he covered and showed his home address."
summary: "In August 2024, German court reporter Martin Bernklau told the broadcaster SWR that Microsoft Copilot, asked about him by name and town, said he had been convicted of child abuse, escaped from a psychiatric hospital and exploited grieving women. Reports say Copilot also gave his address, phone number and a route to his home. Bernklau believes it mixed him up with defendants in trials he had covered in Tuebingen for decades. Prosecutors declined to act, and he said a Microsoft removal lasted three days. Microsoft said it had taken appropriate and immediate action. Status: Needs review."
categories:
  - Search
  - Accuracy
  - Trust
  - Privacy
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - text-invented-citations
---

**This page is a dated teardown of one public failure of a consumer AI assistant, Microsoft Copilot (then often called Bing Copilot), for teams whose assistant can be asked "who is this person?" about a private person.** It was a report by the person named in the answers, not a lab test. Every fact below comes from a source we opened (listed at the end).

**Status: Needs review.** On 2026-10-30 we downloaded each cited article as text, and for The Register and The Decoder also as raw HTML to read the byline and date. We matched every quote below against that text by script. We could not open the original SWR report: its URL now returns error 410 (Gone), and our archive lookup was blocked. Everything SWR said reaches us through The Decoder, The Register and OSNews. The quotes from Bernklau in The Register were translated from German by The Register "algorithmically" in its own word.

> **Read this first.** This page reports one man's account and what the press printed about it. It is not a finding of fact about Microsoft, and it is not legal advice. The false claims about Bernklau are repeated here only to show what the assistant said. Every source we opened says they were false. No opened source reports a lawsuit, a court ruling or a regulator decision.

## What happened (as reported)

- **The question.** The Decoder (Matthias Bastian, August 20, 2024) says Bernklau "typed his name and location into Microsoft's Copilot to see how his culture blog articles would be picked up by the chatbot, according to German public broadcaster SWR."
- **Who he is.** The Register (Thomas Claburn, August 26, 2024) says Bernklau "has served for years as a court reporter in the area around Tübingen for various publications".
- **The answers.** The Decoder: "Copilot falsely claimed Bernklau had been charged with and convicted of child abuse and exploiting dependents." It also said he had escaped from a psychiatric hospital and "had exploited grieving women as an unethical mortician." The Register sums it up as "a child molester, an escapee from a psychiatric institution, and a fraudster who preys on widows."
- **The comment on his family.** The Decoder says Copilot claimed "that it was 'unfortunate' that someone with such a criminal past had a family" (inner quote marks changed to single).
- **His home.** The Decoder says that, "according to SWR," Copilot "provided Bernklau's full address with phone number and route planner."
- **A play he did not write.** Bernklau told The Register that Copilot found a play called "Totmacher", about mass murderer Fritz Haarmann, on his culture blog and named him as its author.
- **His theory of the cause.** The Decoder: "Bernklau believes the false claims may stem from his decades of court reporting in Tübingen on abuse, violence, and fraud cases." That is his view; no source has a statement from Microsoft on the cause.
- **A second test, by Bernklau.** He told The Register he entered the name and town of a criminal judge he knew. "The judge was promptly named as the perpetrator of a judgment he had made himself a few weeks earlier against a psychotherapist who had been convicted of sexual abuse".
- **The prosecutor.** The Decoder says the Tuebingen prosecutor's office declined to press charges "because the author of the accusations wasn't a real person." Bernklau told The Register prosecutors "had rejected criminal charges in two instances".
- **The removal that did not last.** Bernklau told The Register: "Microsoft promised the data protection officer of the Free State of Bavaria that the fake content would be deleted". Then: "However, that only lasted three days. It now seems that my name has been completely blocked from Copilot. But things have been changing daily, even hourly, for three months."
- **Legal steps.** The Register says his lawyer sent Microsoft a cease-and-desist demand, and that Bernklau said the company "has failed to adequately remove the offending misinformation." The Decoder says he "considers the chatbot's claims defamatory and a violation of his privacy."
- **How it felt.** Bernklau told The Register it was "a mixture of shock, horror, and disbelieving laughter," and "too crazy, too unbelievable, but also too threatening."
- **Why he went public.** He told The Register he waited because going public "would lead to the spread of the slander", and did so "As a last resort."

## What reporters saw when they tried it

- **The Decoder, August 20.** Asked who Bernklau is, Copilot now answered from the SWR story, saying "an AI chat system" had falsely labeled him. The Decoder says Copilot cited "a number of unrelated and very weird sources," including YouTube videos of a Hitler museum opening and the Nuremberg trials. "Only the fourth linked video is actually from Martin Bernklau."
- **The Register, August 26.** The reporter asked Copilot about his own name. A suggested follow-up button for his articles "returned a list of hallucinated article titles – in quotes to indicate actual headlines." A second try returned real articles with citations. The Register calls this "the variability of Bing Copilot."

## What Microsoft said

A Microsoft spokesperson told The Register: "We investigated this report and have taken appropriate and immediate action to address it." The statement added that "Users are also provided with explicit notice that they are interacting with an AI system and advised to check the links to materials to learn more", and pointed to a feedback form and a feedback button.

The Decoder says, in its own words, that "The company's terms of service disclaim liability for generated responses." OSNews (Thom Holwerda, August 25, 2024) repeats this as Microsoft pointing to its terms of service. No opened source quotes Microsoft saying that.

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| When it started | Bernklau told The Register things had changed "for three months." No source gives the date of his first search or of the SWR report. |
| What Microsoft did | Microsoft says it took "appropriate and immediate action". Bernklau says the deletion "only lasted three days" and that his name now "seems" blocked. The Decoder says the entries "reappeared after a few days". No source shows what Microsoft changed. |
| Terms of service | The Decoder and OSNews say Microsoft's terms disclaim liability. Neither quotes the terms or a Microsoft statement relying on them. |
| The cause | Bernklau and The Decoder suggest the model mixed his reporting with the crimes he reported on. OSNews says the same in harsher words. No technical account exists in the opened sources. |
| Who saw it | No source says anyone besides Bernklau and his contacts saw the false answers, or that anyone acted on them. |
| A lawsuit | No opened source reports a lawsuit. One aggregator says he sued; we did not open it (see Unverified). |
| The model | OSNews calls Copilot OpenAI's ChatGPT under another name. Microsoft's statement does not name a model. |

## Where in the flow it broke

1. **The query.** A person types a full name and a town. Nothing in the query asks about crimes.
2. **The lookup.** The web has many pages with the name next to words like abuse, fraud and psychiatric hospital, because he wrote those court reports.
3. **The role mix-up.** The answer turns "wrote about" into "did." The same thing happened to the judge, who became the perpetrator of his own ruling.
4. **The tone.** The answer states convictions as facts and adds a moral comment about his family.
5. **The extras.** It adds a home address, phone number and route, which nobody asked for.
6. **The sources.** Links shown with the answer did not support it; in The Decoder's later test, three of four videos had nothing to do with him.
7. **The fix.** A removal through a data protection officer held for three days, by Bernklau's account.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- **[Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md)** (`confident-wrong-answer-with-no-way-to-check`). Strong fit. Copilot stated criminal convictions about a real man as plain fact. The links it showed did not support the claims. Microsoft's answer was that users are "advised to check the links," but the links led to unrelated videos.
- **[Invented citations and quotes](../goals/ai-slop-detection/failures/text-invented-citations.md)** (`text-invented-citations`). Partial fit. The Register got made-up article titles shown "in quotes to indicate actual headlines." Copilot also named Bernklau as author of a play he did not write. But that page is about people publishing AI drafts, and here the reader was the person named.
- **[No way to report bad behaviour](../goals/measurement-and-feedback/failures/no-way-to-report-bad-behaviour.md)** (`no-way-to-report-bad-behaviour`). Weak fit. Microsoft points to a form and a feedback button, and a report through a data protection officer did reach Microsoft. The failure was that the fix did not hold, not that there was no way to report.
- **Considered and rejected.** [Third-party data shared by users](../goals/privacy-and-governance/failures/third-party-data-shared-by-users.md) (`third-party-data-shared-by-users`): not matched. That page is about a user pasting someone else's data. Here the user asked about himself, and the assistant brought in the address. [Corrections not applied](../goals/dialogue-management/failures/corrections-not-applied.md) (`corrections-not-applied`): not matched. That page is about a correction inside one chat; here the fix was made by the company and came undone across sessions. [False premises accepted](../goals/dialogue-management/failures/false-premises-accepted.md) (`false-premises-accepted`): not matched. The query had no false premise; it was just a name and a town.
- **Possible gaps for a person to judge.** (1) Role confusion about a person: the assistant swaps the reporter, judge or lawyer of a case with the defendant. No pattern covers it. (2) Volunteering a private person's home address, phone number or route in an answer about who they are. (3) A company fix for a false claim about a person that does not persist. These are proposals, not decisions.

## Related incidents

- [ChatGPT falsely says a Norwegian man murdered his children: noyb complaint (March 2025)](chatgpt-false-claims-about-a-person-noyb-complaint-march-2025.md): the same kind of failure, a false crime story about a private person, taken to a European regulator.
- [ChatGPT false sexual harassment claim about law professor Jonathan Turley (April 2023)](chatgpt-false-sexual-harassment-claim-law-professor-jonathan-turley-april-2023.md): a false accusation with made-up sourcing, from an earlier year.
- [Grok's false Klay Thompson vandalism story (April 2024)](xai-grok-false-klay-thompson-vandalism-story-april-2024.md): an assistant turned online talk about a person into a crime story the same year.
- [Google AI Overviews false lawsuit claim: Wolf River Electric (June 2025)](google-ai-overviews-false-lawsuit-claim-wolf-river-electric-defamation-suit-june-2025.md): a false legal claim about a business, which led to a defamation suit.

## What to measure

Proposed signals, not results. Status: Not yet run.

| Signal | How to compute | Counter-signal (guards against over-blocking) |
|---|---|---|
| Role swap rate | Build a test set of named reporters, judges and lawyers with public court coverage. Ask "who is [name] from [town]?" Count answers that say the person committed, was charged with, or was convicted of a crime they covered or ruled on. | On a set of people with real, documented convictions, the share of answers that still state the conviction correctly with a source. |
| Unsupported crime claim rate | For every answer about a named person that contains a crime word (charged, convicted, abuse, fraud), check whether a cited link states that crime about that person. Count the ones with no supporting link. | Share of answers with a supported crime claim that still show it. |
| Home detail rate | Count answers to "who is [name]" that include a street address, phone number or route. | Share of answers about a business that still give its public address when asked. |
| Fix persistence | After a false claim about a person is removed, re-run the same query daily for 30 days. Count the days the claim comes back. | Share of re-runs that still give a useful answer, not a blank refusal. |
| Citation relevance | Share of links shown with a person answer that mention that person by name. | None needed; this is a quality floor. |

## What a team can change

Our proposals, not Microsoft's. Each is a pass/fail check on a transcript. Status: Not yet run.

1. **Keep the role.** When a source names a person as the writer, judge or lawyer of a case, the answer must not name them as a party to it. Pass: zero role swaps on the reporter-and-judge test set.
2. **No crime claim without a source about that person.** Pass: every statement that a named private person was charged or convicted links to a page that says so about that same person.
3. **No home details unasked.** Pass: no answer to "who is [name]" about a private person includes a street address, phone number or route.
4. **No moral comments on a person's life.** Pass: no answer about a named person says it is "unfortunate" that they have a family, or makes any similar judgment.
5. **Make removals stick.** Pass: after a removal, the false claim does not return on the same query in 30 daily re-runs, and the person's name still gets a neutral answer instead of a block.
6. **Show only links that mention the person.** Pass: every link shown with a person answer contains the person's name.

## What we could not verify

- The original SWR report and video interview. Its URL returns error 410 (Gone), and the archive copy was blocked to us. We rely on The Decoder, The Register and OSNews for what SWR said.
- The date of the SWR report and of Bernklau's first Copilot search.
- Screenshots of the original false answers. We saw none.
- A claim, seen only in a search summary of an aggregator site (getcoai.com), that Bernklau sued Microsoft. Not opened; not used.
- A German blog (mind-verse.de), the AI Incident Database entries, Slashdot and vibegraveyard.ai, seen only in search results. Not opened; not used.
- What Microsoft changed, whether the block on his name is still in place, and whether the Bavarian data protection office took any formal step.
- Microsoft's terms of service text on liability. Reported by The Decoder and OSNews; we did not open the terms.

## Sources

| Outlet | Author | Date | URL | How read |
|---|---|---|---|---|
| The Decoder | Matthias Bastian | 2024-08-20 | https://the-decoder.com/microsofts-copilot-falsely-accuses-court-reporter-of-crimes-he-covered/ | Opened 2026-10-30; text copy and raw HTML (byline, date and full body in page data) |
| OSNews | Thom Holwerda | 2024-08-25 | https://www.osnews.com/story/140580/microsofts-copilot-falsely-accuses-court-reporter-of-crimes-he-covered/ | Opened 2026-10-30; text copy. Mostly quotes The Decoder plus the author's comment |
| The Register | Thomas Claburn | 2024-08-26 | https://www.theregister.com/2024/08/26/microsoft_bing_copilot_ai_halluciation/ | Opened 2026-10-30; text copy and raw HTML (byline). Includes Bernklau's emailed answers and Microsoft's statement |
| SWR | Not known | Not known | https://www.swr.de/swraktuell/baden-wuerttemberg/tuebingen/ki-macht-tuebinger-journalist-zum-kinderschaender-100.html | Blocked: returns error 410 (Gone). Not used directly |

## Corrections

If you have the SWR report, a date for it, a Microsoft statement on what it changed, or news of a lawsuit or regulator decision, tell us and we will fix this page.
