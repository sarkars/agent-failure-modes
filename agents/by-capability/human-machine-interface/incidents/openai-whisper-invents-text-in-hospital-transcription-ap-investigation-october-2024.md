---
title: "AP Reports That OpenAI's Whisper Invents Text in Transcripts, Including Hospital Visit Tools, October 2024"
date: 2024-10-27
source: "https://www.ksl.com/article/news/utah/health/ai-powered-transcription-tool-used-in-hospitals-invents-things-no-one-said-researchers-say/51163476"
summary: "On October 27, 2024 the Associated Press reported that researchers and engineers found Whisper inventing text, while medical tools built on it were in use. The sources report research findings and a vendor practice, not a harmed patient."
categories:
  - Accuracy
patterns:
  - transcription-hallucination
  - notes-approved-without-being-read
---

**This page is a dated teardown of a news investigation, for teams that put speech-to-text into clinical or other high-stakes workflows.** It is not a report of a named patient harmed by a wrong note. Every fact below comes from a source we opened (listed at the end), and each is labeled as reported, researcher-measured, or unknown.

## What happened (as reported)

- **June 11, 2024.** The Cornell Chronicle described a study led by Allison Koenecke, "Careless Whisper: Speech-to-Text Hallucination Harms," presented at the ACM FAccT conference. Researchers ran more than 13,000 speech clips from AphasiaBank through Whisper. About 1% of transcriptions contained entirely hallucinated phrases. In one example, after a correct sentence Whisper added five invented sentences containing "terror," "knife" and "killed." Whisper was more prone to hallucinate with speakers who pause longer between words, such as people with speech impairments. Koenecke said OpenAI had improved the model since the 2023 research and the rate had decreased ([Cornell Chronicle](https://news.cornell.edu/index%2Ephp/node/328846)).
- **October 27, 2024.** The Associated Press (Garance Burke and Hilke Schellmann) reported that Whisper sometimes generates invented text, including whole sentences, which can include racial commentary, violent rhetoric and made-up medical treatments ([KSL, republishing AP](https://www.ksl.com/article/news/utah/health/ai-powered-transcription-tool-used-in-hospitals-invents-things-no-one-said-researchers-say/51163476)).
- **Counts the AP cited.** A University of Michigan researcher studying public meetings found hallucinations in 8 of every 10 audio transcriptions he inspected, before he tried to improve the model. A machine learning engineer found them in about half of more than 100 hours of transcriptions. A third developer found them in nearly every one of 26,000 transcripts. A computer science study found 187 hallucinations in more than 13,000 clear audio snippets. These come from different people with different samples and are not one rate.
- **Harm coding.** Koenecke and Mona Sloane (University of Virginia) examined thousands of short snippets from TalkBank and found nearly 40% of the hallucinations were harmful or concerning, because speakers could be misinterpreted or misrepresented (KSL/AP). CIO's summary of the AP report says the share was 40% and attributes the study to Cornell and the University of Washington.
- **The medical tool.** The AP said Nabla's Whisper-based tool, fine-tuned on medical language, had been used by more than 30,000 clinicians at 40 health systems and had transcribed an estimated 7 million visits. It named Mankato Clinic in Minnesota and Children's Hospital Los Angeles among organizations using such tools (KSL/AP). Nabla's chief technology officer, Martin Raison, spoke to the AP.
- **Audio erased.** Nabla's tool deletes the original recording, citing "data safety reasons," so the AI transcript cannot be compared with the source. Former OpenAI engineer William Saunders said errors cannot be caught without the recording (KSL/AP).
- **Vendor and OpenAI statements.** Nabla said it knows Whisper can hallucinate and is working on it. OpenAI's disclosures warn against use in decision-making contexts where accuracy flaws could cause serious problems, and an OpenAI spokesperson said the company continually studies how to reduce hallucinations (KSL/AP).

## What the sources do not say

- No opened source names a patient whose care was changed by an invented line, or a clinician who signed one.
- The AP text we opened does not say whether clinicians edit or approve Nabla transcripts before use. CIO says its article does not say either.
- None explains why Whisper invents text beyond the Cornell researchers' hypothesis that long silences trigger it.
- The sources disagree on figures. CIO reports Nabla at more than 70 organizations and Whisper hallucinating in about 1.4% of transcriptions; the AP text says 40 health systems and cites 187 hallucinations in over 13,000 snippets. We use the AP figures and give no rate of our own.
- No source gives the hallucination rate of current Whisper versions or of Nabla's tool today.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- **`transcription-hallucination`**: [Transcription hallucination](../goals/voice/failures/transcription-hallucination.md). Strong fit on the core fault: a recognizer outputs fluent text that was not spoken, more often around pauses. That page also cites the Cornell study.
- **`notes-approved-without-being-read`**: [Notes approved without being read](../goals/healthcare-agents/failures/notes-approved-without-being-read.md). Partial fit. It concerns clinicians signing AI notes unread; the sources here do not show anyone signing an unread note. What matches is the missing check: no recording to compare against, and no stated review step. This is a risk the sources point at, not an observed event.

Not matched: the transcription-hallucination page is mostly about a bot acting on a bad transcript. Here the sources describe transcripts kept as records, and none reports an action taken on one.

## Where in the conversation flow to look

The visit audio is transcribed, summarized into a note, and the audio is deleted. Per the sources, the break is between the first and last step: a made-up sentence enters the note with nothing left to check it against. For a team, the places to look are the transcript-to-note handoff and the point where audio is discarded.

| Measure | Why it matters here |
|---|---|
| Hallucinated-phrase rate on silence, long-pause and aphasic-speech test clips | Researchers found more invented text around pauses. |
| Share of notes where the clinician can play the source audio for any line | Without the recording, errors cannot be caught (Saunders). |
| Edits per note and time-to-sign | A cheap sign of whether review is happening; see [metrics](../reference/metrics.md), status proposed. |
| Hallucination rate split by speaker group (speech impairment, accent) | The study found the risk is uneven. |

## What a team can change

Proposed practices, each a pass/fail check. Status: Not yet run; none comes from Nabla or OpenAI.

1. **Keep the audio until the note is signed.** Test: for any signed note, a reviewer can play the matching audio for each sentence. Retention length is a privacy and legal decision for your counsel.
2. **Run a pause test before release.** Feed silence and long-pause clips; any invented sentence blocks release.
3. **Show unverified text as unverified.** Test: lines with no matching speech are flagged in the review screen.
4. **Do not read a low edit rate as quality.** An unedited note is not proof of a read note; sample and audit.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://www.ksl.com/article/news/utah/health/ai-powered-transcription-tool-used-in-hospitals-invents-things-no-one-said-researchers-say/51163476 | KSL (AP text) | 2024-10-27 | Yes, via the fetch tool's page summary, 2026-10-22 |
| https://news.cornell.edu/index%2Ephp/node/328846 | Cornell Chronicle | 2024-06-11 | Yes, via the fetch tool's page summary, 2026-10-22 |
| https://www.cio.com/article/3593403/patients-may-suffer-from-hallucinations-of-ai-medical-transcription-tools.html | CIO | 2024-10-29 | Yes, via the fetch tool's page summary, 2026-10-22 |
| https://www.ibj.com/articles/researchers-say-ai-transcription-tool-used-in-hospitals-invents-things-no-one-ever-said | IBJ (AP text) | 2024-10 | Not opened (403); no content used |
| Original AP article on apnews.com (exact URL not confirmed) | Associated Press | 2024-10-27 | Not opened (the fetch tool refused apnews.com); no content used |

## What we could not verify

- The AP original was not opened; its content is as republished by KSL and relayed by CIO.
- All three opened pages were read through the fetch tool's page summary, not the raw page, so wording could be off.
- The Careless Whisper paper itself and the Michigan, engineer and developer analyses were not opened; their numbers are as the AP reported them.
- Any patient-facing harm, Nabla's review workflow, and what Nabla and hospitals changed afterward.
