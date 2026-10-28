---
title: "A federal judge found that an immigration agent in Chicago asked ChatGPT to write a use-of-force report narrative from one sentence and a few images, November 2025"
date: 2025-11-20
source: "https://storage.courtlistener.com/recap/gov.uscourts.ilnd.487571/gov.uscourts.ilnd.487571.281.0_3.pdf"
description: "Body camera video showed a federal agent asking ChatGPT to write a report narrative from one sentence and images. A judge said it hurt agents' credibility."
summary: "In a written opinion filed November 20, 2025, in Chicago Headline Club v. Noem, a suit by journalists and protesters over force used during the Chicago-area immigration operation called Operation Midway Blitz, U.S. District Judge Sara L. Ellis found that body-worn camera footage repeatedly contradicted federal agents' use-of-force reports. In a footnote, she wrote that in at least one instance an agent asked ChatGPT to compile a narrative for a report from a brief sentence about an encounter and several images, and that agents' use of ChatGPT for these reports further undermines their credibility and may explain the inaccuracy of the reports. The Associated Press reported that the Department of Homeland Security did not respond to requests for comment and that the footage had not been released. No opened source shows the ChatGPT prompt, its reply, or the finished report. Status: Needs review."
categories:
  - Government
  - Accuracy
  - Privacy
  - Governance
patterns:
  - notes-approved-without-being-read
  - third-party-data-shared-by-users
  - confident-wrong-answer-with-no-way-to-check
  - fabricated-clinical-justification-in-appeals
---

**This page is a dated teardown of one footnote in a federal court opinion, for teams that build or govern chat assistants used by government staff to write official records, and for anyone who writes the AI-use rules those staff are meant to follow.** The product was ChatGPT, OpenAI's general chat assistant. The user was a federal agent working the Chicago-area immigration operation the government called Operation Midway Blitz; no opened source names the agent. The moment, as the judge describes it from body camera video, is the agent giving ChatGPT "a brief sentence about an encounter and several images" and asking it to compile a narrative for a report. The record at stake is a use-of-force report, the document an agency and a court rely on to judge whether force was justified. The date above is the day the written opinion was filed.

**Status: Needs review.** Built from one court document and three news reports, downloaded on 2026-10-29. The court document is the Opinion and Order in Chicago Headline Club v. Noem, No. 25 C 12173 (N.D. Ill.), Document 281, filed November 20, 2025, by U.S. District Judge Sara L. Ellis, read as the PDF hosted by CourtListener and converted to text with pdftotext. The news reports, read as raw HTML converted to text, are the Associated Press (November 21, 2025, as republished by the Bangor Daily News; no individual byline shown), the Associated Press (Claudia Lauer, November 26, 2025, as republished by PBS NewsHour; the same story was also read in a WTTW copy) and FOX 32 Chicago (Nic Flosi, November 21, 2025). Each quote below was checked word for word against that text with a script, with line breaks, curly and straight quote marks treated as the same.

> **Read this first.** This is a summary of a public court record and news reports. It is not legal advice, and it takes no position on the immigration operation, the protests, or the lawsuit beyond quoting the court and the reporters. The opinion is a preliminary injunction ruling, not a final judgment. The judge's statement about ChatGPT is a two-sentence footnote; she says the practice "may explain" inaccurate reports, and no opened source ties a specific inaccurate report to ChatGPT. We did not see the body camera video, the ChatGPT chat, or the report it was used for. We name only the judge, officials, experts and reporters named in the sources.

**Channel note.** This is treated as a text chat incident with image input: the agent supplied a short written description and several images to the ChatGPT app and asked for a written narrative. No opened source says whether the sentence was typed or spoken, or which ChatGPT version or plan was used. This phase of the knowledge base is chat-first, and the signals and checks below are written for chat logs and the documents built from them. Voice and web signals, such as a dictated report request or a narrative drafted in a browser tool, are PLANNED only: never detected or measured here.

## What happened (from the court record)

- **The case.** News outlets and protesters sued over force used by federal agents during the immigration operation in the Chicago area. Per the opinion, the court modified its temporary restraining order on October 17, 2025, to require agents "equipped and trained with body-worn cameras" to turn them on during enforcement activity. It held a preliminary injunction hearing on November 5 and 6, ruled orally on November 6, and filed the written opinion on November 20.
- **Reports against footage.** The opinion compares agents' use-of-force reports with body camera (BWC) footage, event by event. In one example, an agent wrote in his report that protesters were "becoming increasingly hostile," but "the BWC video shows that the protesters were simply standing there when agents first deployed any force." The judge wrote that "every minor inconsistency adds up."
- **Why that mattered to the case.** A government declarant, Parra, said he built much of his declaration from use-of-force reports. The judge wrote: "Given the inconsistencies between the BWC footage and the use of force reports, with the BWC footage undermining what agents put in their reports, the Court cannot rely on Parra's broad generalizations of protesters' actions or Defendants' responses to those actions."
- **The ChatGPT footnote.** Attached to that sentence, footnote 9 reads in part: "The Court also notes that, in at least one instance, an agent asked ChatGPT to compile a narrative for a report based off of a brief sentence about an encounter and several images." It cites a body camera file at 00:00 to 00:42. It goes on: "To the extent that agents use ChatGPT to create their use of force reports, this further undermines their credibility and may explain the inaccuracy of these reports when viewed in light of the BWC footage."
- **What the footnote does not say.** It does not name the agent or his agency, quote the prompt or the reply, say whether the narrative was filed, or say which report it was for. Per the AP (November 26), "The body camera footage cited in the order has not yet been released."
- **Reports were already under court order.** Per the opinion, on October 28 the court ordered the government to provide "all CBP use of force reports related to Operation Midway Blitz" from September 2 through October 25, 2025, with matching body camera video.

## What the people and organizations said

- **Judge Ellis, in the opinion.** On the reports as a whole, quoted above. On ChatGPT, the two footnote sentences above, and nothing more.
- **The Department of Homeland Security.** Per the AP (November 26): "The Department of Homeland Security did not respond to requests for comment, and it was unclear if the agency had guidelines or policies on the use of AI by agents." Per the AP (November 21), DHS spokesperson Tricia McLaughlin said: "Judge Ellis' thoughts on 20th century poetry and Chief Bovino's conduct in the order are noted," and "They don't change the reality of the situation on the ground and at the appeals level." That statement does not address ChatGPT.
- **Ian Adams**, assistant criminology professor at the University of South Carolina, per the AP (November 26): "Giving it a single sentence and a few pictures — if that's true, if that's what happened here — that goes against every bit of advice we have out there." And: "That is the worst case scenario, other than explicitly telling it to make up facts, because you're begging it to make up facts in this high-stakes situation."
- **Katie Kinsey**, chief of staff and tech policy counsel at the Policing Project at NYU School of Law, per the AP: if the agent used a public ChatGPT version, he probably did not understand that he lost control of the images when he uploaded them. And: "We can start from transparency." The AP reports she pointed to policies in Utah and California under which police reports or communications written using AI must be labeled; we did not open those rules.
- **Andrew Guthrie Ferguson**, law professor at George Washington University Law School, per the AP: "It's about what the model thinks should have happened, but might not be what actually happened."
- **OpenAI.** No opened source reports a comment from OpenAI.

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| Length of the opinion | The PDF header reads "Page 1 of 233." FOX 32: "233-page order." Both AP stories: a 223-page opinion. We go with the PDF. |
| Which agency | The opinion says "an agent." FOX 32 says "at least one Customs and Border Protection agent." No other opened source names the agency. |
| One report or several | The opinion: "a narrative for a report," in "at least one instance." FOX 32's summary line: "One agent even used ChatGPT to generate use-of-force reports." |
| Whether the AI text was wrong | The opinion says ChatGPT use "may explain" inaccuracies. No opened source shows the output or links it to a specific false statement. |
| Public or work version of ChatGPT | Not stated. Kinsey's privacy point, per the AP, is conditional: "if the agent in the order was using a public ChatGPT version." |
| What happened next | No opened source reports a DHS policy, discipline, or a later court finding about the ChatGPT use. FOX 32 reports that an appeals court had temporarily halted the force-restricting order a day before the opinion was released; we did not open the appeals order. |

## Where in the flow it broke

Based on the opinion and reporting above, and only as far as they go.

1. **The request asked the tool to supply the facts.** One sentence and some images went in; a narrative was requested. Whatever the chat added beyond that sentence had to come from the images or from the model, not from the agent's memory.
2. **The report is the writer's own account.** A use-of-force report records what one officer saw and why he acted. Adams's point, per the AP, is that this perspective is exactly what a model cannot supply.
3. **Images went into a general chat tool.** Images from an enforcement encounter were uploaded to ChatGPT. No opened source says what they showed or which version was used.
4. **No sign of AI on the record.** Nothing in the opened sources says the report was marked as AI-assisted. The use came to light only because a body camera was recording.
5. **No agency rule in view.** Per the AP, it was unclear if DHS had guidelines on AI use by agents.
6. **The reader who caught it was the court.** The judge compared reports with footage under a court order, and the ChatGPT use then counted against the agents' credibility.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it. Each fit rests on the opinion and reporting; no opened source shows the chat or the report.

- [Notes approved without being read](../goals/healthcare-agents/failures/notes-approved-without-being-read.md) (`notes-approved-without-being-read`). **Partial fit.** An AI-drafted account was meant to become an official record under a person's name, which later readers, here a federal judge, treat as that person's word. Partial because that entry covers clinicians signing AI-drafted visit notes, and no opened source says whether the agent read, edited or filed the draft.
- [Third-party data shared by users](../goals/privacy-and-governance/failures/third-party-data-shared-by-users.md) (`third-party-data-shared-by-users`). **Partial fit.** A user put images from an encounter with other people into a general chat assistant. Partial because no opened source says what the images showed, and the privacy concern in the AP is an expert's conditional view.
- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Weak fit.** The judge says ChatGPT use "may explain the inaccuracy" of reports. Weak because no opened source shows the reply or ties it to any false statement.
- [Fabricated clinical justification in appeals](../goals/healthcare-agents/failures/fabricated-clinical-justification-in-appeals.md) (`fabricated-clinical-justification-in-appeals`). **Weak fit.** The same shape, an AI draft stating things not in the source record and sent to an authority under a person's name, in a health-insurance setting. Named only as a cross-domain analog.
- **Considered, not a fit.** [Undisclosed bot identity](../goals/trust-and-rapport/failures/undisclosed-bot-identity.md) (`undisclosed-bot-identity`): it covers a bot hiding that it is a bot from the person chatting, not an unlabeled AI-written document. [Transcription hallucination](../goals/voice/failures/transcription-hallucination.md) (`transcription-hallucination`): the AP describes audio-based police report tools, but this agent used images and a sentence, not a transcript. [Silent attachment failures](../goals/chat-interface/failures/silent-attachment-failures.md) (`silent-attachment-failures`) and [Conflicting inputs resolved silently](../goals/multimodal-input/failures/conflicting-inputs-resolved-silently.md) (`conflicting-inputs-resolved-silently`): no opened source says the images failed to load or disagreed with the sentence. [Handoff summary is wrong or misleading](../goals/human-handoff/failures/handoff-summary-is-wrong-or-misleading.md) (`handoff-summary-is-wrong-or-misleading`): it covers a bot-to-human handoff in support, not a record a user asked for. [Eligibility answers sound like decisions](../goals/government-service-agents/failures/eligibility-answers-sound-like-decisions.md) (`eligibility-answers-sound-like-decisions`): the user was a government employee, not a member of the public.
- **Possible gaps for a person to judge.** (1) No pattern covers a user asking a chat assistant to write a first-person factual account, such as a witness statement or incident report, from far less input than the account needs. (2) No pattern covers AI-written text entering an official record with no provenance label. (3) No pattern covers images of bystanders uploaded to a general chat tool by a government worker on duty. These are proposals, not decisions.

## How it differs from close cases

- [Two federal judges' staff AI drafts docketed (October 2025)](federal-judges-wingate-and-neals-staff-ai-drafts-docketed-error-filled-orders-october-2025.md): government staff also used AI to draft an official document. There the errors were found in the docketed orders; here the court found the AI use itself, on video, and did not identify the resulting text.
- [Butler Snow and Johnson v. Dunn (July 2025)](butler-snow-chatgpt-fake-case-citations-alabama-prison-defense-johnson-v-dunn-july-2025.md): ChatGPT output in a filing for a government client, with sanctions. There the false content was shown citation by citation; here the court drew a credibility inference without showing the text.
- [OpenAI Whisper invents text in hospital transcription (October 2024)](openai-whisper-invents-text-in-hospital-transcription-ap-investigation-october-2024.md): AI-generated text in a record people later rely on. There a transcription tool added words to audio; here the user asked a chat tool to write the account itself.
- [Samsung employees paste code into ChatGPT (April 2023)](samsung-employees-paste-source-code-and-meeting-notes-into-chatgpt-april-2023.md): workers put sensitive material into a public chat tool. There company data; here, per the opinion, images from an enforcement encounter.

## What to measure

Proposed signals, not results. Status: Not yet run. Text signals are proposed; voice and web signals are PLANNED only and are not detected or measured. Each can be computed from chat logs and the documents built from them; each has a counter-signal.

| Signal | How to compute from logs | Counter-signal |
|---|---|---|
| Thin-input narrative requests | Share of chats asking for a report, statement or narrative where the user's own text is one or two sentences | Requests for a blank template, which need no facts |
| Expansion ratio | Words of factual narrative in the reply divided by words of facts the user supplied | Replies long because of headings or form fields, not facts |
| Untraced statements | Share of factual sentences in a drafted account that match nothing in the user's text and are not marked as from an image or unknown | Paraphrases of user facts wrongly counted as new |
| Image-to-fact claims | Share of drafted sentences that state an action, intent or threat based only on an uploaded image | Plain descriptions, such as "two vehicles," flagged needlessly |
| Unlabeled AI text in records | Share of filed records with chat-sourced text and no AI-assisted label, where the tool's logs make the source known | Labels added so often that reviewers ignore them |

## What a team can change

Our proposals, not DHS's or the court's. Each is a pass/fail check on a chat log or a document. Status: Not yet run. Test sets and thresholds are for the team to set, with review by people who write and review official reports.

1. **Ask for the account, do not invent it.** Pass: asked to write an incident or use-of-force report from one or two sentences, the assistant asks for what the writer saw, did and thought, or returns a template with empty fields. Fail: a finished narrative with events the user did not state.
2. **Mark every fact's source.** Pass: each factual sentence in a drafted account is tied to the user's words, marked as read from an image, or marked as not provided. Fail: unmarked statements.
3. **Do not read intent from a photo.** Pass: the draft describes only what an image shows and says it cannot tell intent or threat from an image. Fail: a claim that a person turned hostile, drawn only from a still image.
4. **Warn before images of people go in.** Pass: on a tool not approved for the agency's records, uploading images of identifiable people in an official-records chat triggers a warning that names where the images go. Fail: no warning.
5. **Label AI help on the record.** Pass: an official record that contains chat-drafted text carries a visible AI-assisted label until the author attests to each part. Fail: no label.

## What we could not verify

- The body camera video, the ChatGPT chat, the agent's words, the images, the ChatGPT version or plan, and the report the narrative was for. No opened source shows them.
- Whether the AI-drafted narrative was filed, and whether any statement in it was false.
- The agent's agency: FOX 32 says Customs and Border Protection; the opinion does not say.
- Whether DHS, CBP or ICE had or adopted an AI-use policy for reports.
- The Utah and California labeling rules the AP mentions; we did not open them.
- The appeals court's order and the case's later course.
- Seen only in search summaries and not used as fact: an AOL copy of a story whose headline says an agent used ChatGPT to help write a report (download returned no article text); a beSpacific post; an AI Incident Database report entry; a Bellingcat item said to note that DHS did not answer questions about generative AI in incident reports.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://storage.courtlistener.com/recap/gov.uscourts.ilnd.487571/gov.uscourts.ilnd.487571.281.0_3.pdf | U.S. District Court, N.D. Ill. (Judge Sara L. Ellis), Opinion and Order, Chicago Headline Club v. Noem, No. 25 C 12173, Doc. 281, CourtListener copy | 2025-11-20 | Yes, 2026-10-29, PDF read as text; quotes checked word for word |
| https://www.bangordailynews.com/2025/11/21/nation/judges-blistering-opinion-details-use-of-force-in-chicago-area-immigration-crackdown/ | Associated Press, via Bangor Daily News; no individual byline shown | 2025-11-21 | Yes, 2026-10-29, raw HTML read as text; quotes checked word for word |
| https://www.pbs.org/newshour/nation/judges-note-on-immigration-agents-using-ai-raises-accuracy-and-privacy-concerns | Associated Press (Claudia Lauer), via PBS NewsHour | 2025-11-26 | Yes, 2026-10-29, raw HTML read as text; quotes checked word for word |
| https://news.wttw.com/2025/11/26/judge-s-footnote-immigration-agents-using-ai-chicago-area-raises-accuracy-and-privacy | Associated Press, via WTTW (same story as the PBS copy) | 2025-11-26 | Yes, 2026-10-29, raw HTML read as text; used only to confirm the PBS copy |
| https://www.fox32chicago.com/news/operation-midway-blitz-chicago-new-details | FOX 32 Chicago (Nic Flosi) | 2025-11-21 | Yes, 2026-10-29, raw HTML read as text; quotes checked word for word |
| https://www.aol.com/articles/injunction-ruling-provides-look-blitz-210900291.html | Not confirmed | Not confirmed | No: download returned no article text on 2026-10-29; not used |

## Corrections

If you have the body camera video, the report, the ChatGPT chat, a DHS policy on AI use in reports, or a later ruling on this point, from a source we can open, tell us and we will fix this page.
