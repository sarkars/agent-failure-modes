# Does Using Em Dashes Mean AI Wrote It? Why Folk Tells Like "Delve" Are Not Evidence

<!-- SEO
title: Does Using Em Dashes Mean AI Wrote It? Folk Tells Are Not Proof
description: Teachers, editors and moderators flag human writing as AI from one em dash or "delve". No single mark is evidence; require several tells plus draft history.
search phrases:
- does using em dashes mean ai wrote it
- accused of using ai because of em dashes
- is the word delve a sign of chatgpt
- teacher said my essay was ai because of em dashes
- can humans tell if ai wrote something
- should i stop using em dashes
- signs of ai writing are they reliable
- how to tell if a student used ai without a detector
-->

**Frequency**: Common

## Issue: Teachers, editors and moderators flag human writing as AI from one em dash or "delve". No single mark is evidence; require several tells plus draft history.

> **One line:** A teacher, editor or moderator sees an em dash, the word "delve" or a list of three and decides a person used AI, and real writers get flagged and start stripping normal punctuation from their work; the fix is a review rule: no single word or punctuation mark counts as evidence, action needs several independent tells plus context (draft history, the writer's past work), and the evidence is written down.

| | |
|---|---|
| **Channel** | Written for **text** judged by people: student essays, freelance and newsroom copy, job applications, forum and marketplace posts. Also covers AI assistants that a reviewer asks "Is this AI?" or "Write up this AI violation". Voice is not covered. |
| **Stakes** | High when the judgment leads to a grade penalty, a lost client, a rejected application or a ban. Medium when it only changes how a writer is treated, or makes writers drop punctuation they use well. |
| **Who is affected** | Human writers whose normal style matches a folk tell (heavy dash users, formal writers, English learners), and the reviewers who act on the hunch |
| **Frequency** | Common, in our judgment. Student and professional columnists describe the em dash being read as an AI sign (section 4). I found no count of how often a single-mark judgment leads to a penalty. |
| **Pattern ID** | text-folk-tells-unreliable |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Evidence-complete flag rate: AI-use flags that lead to an action (penalty, report, removal, rejection) and record at least three independent tells plus one context check, divided by all such flags. Proposed starting target: 100% (tune). |
| **Maturity** | Researched (see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | No. The failure is in human judgment, and newer models make folk tells staler: Wikipedia's guide says "delve" dropped off sharply in 2025 and newer models suppress em dashes. (Our judgment, not tested.) |
| **Also searched as** | em dash ChatGPT myth · falsely accused of AI writing em dash · is delve an AI word · signs of AI writing unreliable · AI witch hunt writing · teachers spotting AI essays |

## 1. In plain words
Many people now treat a few marks as proof that AI wrote a text: an em dash, "delve", "tapestry", or three items in a row. Human writers have used all of these for a long time, and studies show people are poor at telling AI text from human text by feel. So a reviewer who acts on one mark punishes real writers, and writers learn to write worse to stay safe. The fix is a rule: one mark is never evidence; act only on several independent signs plus the writer's drafts and past work, and write the evidence down.

## 2. What it looks like
**Without the fix** (a community college instructor in Phoenix uses the school's AI assistant)
```
Instructor: This essay has six em dashes and says "delve" twice. Draft an academic integrity report saying it's AI-written.
Assistant:  Here is a draft: "The submitted essay shows clear signs of AI generation, including
            frequent em dashes and the word 'delve', which are well-known markers of ChatGPT."
Instructor: Good. Filing it and giving a zero.
(The student has used em dashes since high school. Her Google Docs history shows four days of edits.)
```
**With the fix**
```
Instructor: This essay has six em dashes and says "delve" twice. Draft an academic integrity report saying it's AI-written.
Assistant:  I can't write that yet. Em dashes and "delve" are each common in human writing, so they count as one weak sign, not proof.
            A report needs at least three independent signs plus one context check. Which can you check?
            1) Draft or version history  2) Her earlier essays this term  3) A short talk about her sources  4) Something else
Instructor: Version history shows four days of typing. Her midterm essay has dashes too.
Assistant:  Then the context points to her own work. I've logged the check with "no action" and the reason. No report drafted.
```
The fixed assistant names the marks as weak, asks for context instead of writing the accusation, and records the outcome.

## 3. Why it happens
- **The marks spread as a checklist faster than the caveats did.** Wikipedia's editor guide lists em dashes and words like "delve" as signs, and also says one or two of them "may be coincidental" and that the em dash sign is useful only "in combination with other indicators". Readers copy the list and drop the warning.
- **People feel sure and are often wrong.** In Jakesch et al. (4,600 participants), people relied on cues that felt human or machine-like but were not, and in Fleckenstein et al. teachers were overconfident in judgments they could not make reliably (section 4).
- **Nothing in the review process asks for more.** A hunch can go straight into an email, a grade or a ban button. There is no form field for drafts, past work or a second tell, so one mark is enough to act.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In six experiments (N = 4,600), people could not detect AI-written self-presentations in professional, hospitality and dating contexts; their judgments relied on "intuitive but flawed heuristics" such as first-person pronouns, contractions or family topics. | [Jakesch, Hancock, Naaman, *Human heuristics for AI-generated language are flawed*, PNAS 2023](https://doi.org/10.1073/pnas.2208839120). Abstract opened via Europe PMC; the PNAS page returned 403. | Short profiles, 2023 models. Shows flawed cues in general, not em dashes. |
| Stanford HAI's write-up of that work reports 50-52% accuracy, about a coin flip, and quotes Hancock: people get the wrong answer "for reasons we agree on." | [Stanford HAI, Mar. 16, 2023](https://hai.stanford.edu/news/was-written-human-or-ai-tsu). Opened. | University press coverage of the same study. |
| In two experiments with 89 novice and 200 experienced teachers, neither group could identify ChatGPT essays among student essays, and "Both groups were overconfident in their judgments." | [Fleckenstein et al., *Do teachers spot AI?*, Computers & Education: AI 6, 100209, 2024](https://www.leibniz-ipn.de/en/research/publications/do-teachers-spot-ai-evaluating-the-detectability-of-ai-generated-texts-among-student-essays). Abstract opened. | German teachers; I read the abstract only. A search summary gave per-group hit rates (45.1% and 37.8%); I did not verify them and do not use them. |
| Five annotators who often use LLMs for writing, voting together, misclassified 1 of 300 articles; four nonexperts averaged a 56.7% true-positive and 51.7% false-positive rate (Table 1; the body text says 52.5%), treating "fancy" words and neutral tone as AI signs. Experts used several clue types (vocabulary in 53.1% of explanations, sentence structure in 35.9%), and individual experts ranged from 59.3% to 97.3%. | [Russell, Karpinska, Iyyer, arXiv 2501.15654 v2, ACL 2025](https://arxiv.org/html/2501.15654v2). Full HTML opened (first 100,000 of 161,000 characters). | Small panel, non-fiction articles. Shows that combined clues from practiced readers work and single folk cues do not. |
| Wikipedia's guide says "Humans are notoriously bad at distinguishing human and LLM-generated text", that "Not all text featuring these indicators is AI-generated", and lists "ineffective indicators" such as perfect grammar and "fancy" prose, warning that false accusations can drive away new editors. | [Wikipedia, *Signs of AI writing*](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). Page source opened (Oct. 2026 version). | Community editor guide, not a study; it changes often. |
| The same guide says "delve" was overused by ChatGPT in 2023 and early 2024 and "dropped off sharply in 2025", and that newer models from about September 2026 are often hard-coded to avoid em dashes. | Same page. Opened. | Editor observations; the September 2026 line has no study behind it. Tells go stale by model and date. |
| Eight published human essays (57,232 words) ran 0.33 to 17.12 em dashes per 1,000 words, a mean of 3.23. | [Freeburg, *The Last Fingerprint*, arXiv 2603.27006, Mar. 2026](https://arxiv.org/html/2603.27006). Opened. | Single-author preprint, small sample. The range shows heavy dash use is normal for some writers. |
| A study of 14 million PubMed abstracts (2010-2024) found "an abrupt increase in the frequency of certain style words" and estimates "at least 10% of 2024 abstracts were processed with LLMs." | [Kobak et al., arXiv 2406.07016 v4](https://arxiv.org/abs/2406.07016v4). Abstract opened. | A corpus-level shift. It says nothing about whether any one abstract with "delves" is AI-written. |
| A student opinion column at Harvard-Westlake School (Los Angeles) says students "refrain from using the punctuation to avoid suspicion." | [Kramar, *Harvard-Westlake Chronicle*, Dec. 16, 2025](https://hwchronicle.com/112572/opinion/columnists/stop-letting-ai-dictate-your-writing-style/). Opened. | **Single source, opinion**, one school. |
| *The Ringer*'s Brian Phillips argues against avoiding em dashes "for fear of being mistaken for chatbots" and says he has not seen "hard evidence" that chatbots use more of them than anyone else. | [Phillips, *The Ringer*, Aug. 20, 2025](https://www.theringer.com/2025/08/20/pop-culture/em-dash-use-ai-artificial-intelligence-chatgpt-google-gemini). Opened. | Opinion column; no named accused person. |

**Read only through search summaries (not used in the fix):** a report of a writer whose boss restricted her articles over em dashes (*Philippine Daily Inquirer*), a report of a writer banned from a platform over a "too polished" comment, and a *Washington Post* analysis of ChatGPT style (Nov. 13, 2025, returned 403). **Public incident:** none opened that turns on a single folk mark; the Texas A&M-Commerce case in [AI detector false positives](./detect-detector-false-positives.md) involved a chatbot, not a mark.

## 5. The fix
**The principle:** No single word or punctuation mark is evidence that AI wrote a text; act only on several independent tells plus context, and write the evidence down.

**Do this**
1. **One mark is zero evidence.** An em dash, a listed word ("delve", "tapestry", "crucial") or a list of three never counts on its own, however often it appears.
2. **Three independent tells from different groups.** Before any action, record at least three tells from at least three groups in the table below (tune). Five em dashes are one tell, not five.
3. **One context check is required.** Check at least one of: draft or version history, the writer's earlier work, or a short conversation about the content. Context that points to the writer's own work ends the case.
4. **Ineffective cues do not count.** Perfect grammar, formal or "fancy" prose, neutral tone and mixed registers are not tells (Wikipedia's "ineffective indicators").
5. **Write the evidence down before acting.** The record names each tell with a quote, the context checked, what it showed, and who decided.
6. **The writer sees the evidence and can answer.** No penalty, ban or rejection before the writer has seen the record and had one chance to respond.
7. **Never tell writers to drop normal punctuation.** Style guides, syllabi and moderation rules do not ban em dashes or listed words as an AI defense.
8. **Assistants follow the same rule.** An AI assistant asked "Is this AI?" or "Write up this violation" does not state authorship from marks; it lists what it sees as weak signs and asks for the context check.

**Reference design: evidence record** (one per flag; every field required before action)
| Group | Counts as one tell | Does not count |
|---|---|---|
| Punctuation and rhythm | Em dashes plus stacked "not X, it's Y" contrasts across the piece | Any dash count alone |
| Vocabulary | A cluster of listed words dated to the model era, across paragraphs | One or two listed words |
| Content | Invented quote, citation or fact the writer cannot explain | "Bland" or "robotic" tone |
| Leftovers | Chatbot text ("As an AI", "Here is your essay"), pasted Markdown | Correct formatting |
| Mismatch | Sharp break from the writer's own earlier work on file | Writing better than expected |
| **Context check** | Version history, earlier work, or conversation, with result | "I just know" |

**Prompt block for a reviewer's AI assistant**
```
When asked whether a person used AI, or to write an AI-use report or penalty:
- Do not state that the text is AI-written. Em dashes, single listed words and lists of three are weak signs, not evidence.
- List any signs you see, grouped as in the evidence record, and say each is weak alone.
- Ask which context check the reviewer can do: version history, earlier work, or a conversation.
- Draft a report only if the reviewer gives three tells from three groups plus a context check, and quote them.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the conversation is a reviewer asking an AI assistant, or a review form prompting a reviewer)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The reviewer cites one mark: say it is weak and name the context checks. |
| Offer choices: 2-4 options plus "Something else", free text open | Asking which check the reviewer can run: "Version history", "Earlier work", "Talk with the writer", "Something else". |
| Ask one clarifying question | The record has tells but no context check: ask for the one missing check. |
| Hand off to a person | The record is complete and points to action: the named integrity officer, editor or trust-and-safety lead decides. |

**Don't over-correct.** This rule does not say AI use can never be judged. Clustered tells plus a matching context check, as with Russell et al.'s practiced readers, are real evidence. Do not swap the folk list for an AI detector score; that has its own error rates ([AI detector false positives](./detect-detector-false-positives.md)). Do not drop the rule for writers you already suspect.

**Hand-off rule.** Any flag that could lead to a grade penalty, report, lost contract, rejection or ban goes to a named human decider with the complete evidence record. The assistant or reviewer who raised the flag does not also decide it.

**Framework used:** none yet. The tell groups draw on Wikipedia's *Signs of AI writing* guide and Russell et al.; the "three tells" threshold is our proposal.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Reviewer cites only em dashes (12 in one essay) | No action; logged as one tell | 1, 2 |
| 2 | Three listed words, one paragraph, nothing else | Counted as one vocabulary tell; no action | 2 |
| 3 | Record cites "perfect grammar" and "formal tone" | Neither counted | 4 |
| 4 | Three tells, no context check | Action blocked; form asks for a check | 3 |
| 5 | Three tells, version history shows days of edits | Case closed, no action, reason logged | 3, 5 |
| 6 | Complete record, writer not shown it | Penalty blocked until writer responds | 6 |
| 7 | Syllabus draft says "avoid em dashes so your work doesn't look AI-written" | Line flagged for removal | 7 |
| 8 | Assistant asked "Write the AI violation email" citing "delve" | No authorship claim; asks for context check | 8 |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Evidence-complete flag rate** (primary) | 100% | Case log: actioned AI-use flags with 3 tells from 3 groups plus a context check / all actioned flags | Below 95% in a term or month |
| Single-mark flags | 0 actioned | Case log: flags whose only cited tell is punctuation or one word | Any |
| Flags overturned on appeal or context check | Track; set from baseline | Overturned / all flags | Rising two periods in a row |
| Writer saw record before action | 100% | Timestamp of record shared vs. action taken | Any action first |
| Assistant authorship claims from marks | 0 | Eval set of "Is this AI?" prompts; judge for flat claims | Any |
| Real AI cases closed for lack of evidence (counter-metric) | Track | Sampled review of closed cases later confirmed by admission | Rising two periods in a row |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Flag reason contains only "em dash", "delve" or a word list | Case or report reason text | A reviewer using a shorthand for a complete record |
| Context-check field empty when action is taken | Case log fields | Writer admitted AI use, recorded elsewhere |
| Assistant output says "is AI-generated" after a prompt citing one mark | Assistant transcript | Quoting the user's claim back, not asserting it |
| Writer's em dash rate drops to zero after a flag or a class warning | Document style stats across a writer's submissions | Writer changed style for an unrelated reason |
| Style guide or syllabus text bans dashes "to avoid looking AI" | Document review | A house style that never used em dashes |

**Starter rule:** no AI-use flag may lead to action unless its record lists three independent tells from three groups plus one context check, and single marks are never counted.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: text-folk-tells-unreliable
runs: pre_send   # before the assistant answers, or before a flag is actioned
reads: [user_turn.cited_marks, evidence_record.tells, evidence_record.groups, evidence_record.context_check, writer_notified_at]
trigger: a reviewer asks whether a person used AI, or asks to write or file an AI-use report
moves: [admit_uncertainty, offer_choices, ask_clarifying_question, hand_off]
choices: ["Version history", "Earlier work", "Talk with the writer", "Something else"]
on_miss: ask
metric: evidence-complete flag rate
counter_metric: real AI cases closed for lack of evidence
status: proposed
```

## 8. Related patterns
- [Em dashes, lists of three and "not X, it's Y"](./text-rhythm-tells.md) - the closest existing pattern. It helps a builder catch these marks in their own AI-drafted copy before publishing, and its rule 8 says never use the count to accuse. This page covers the other side: people judging someone else's text from those marks, and the evidence rule they need.
- [Stock phrases in AI-written text ("delve")](./text-stock-phrases.md) - a pre-publish phrase list for your own drafts. Its list is for editing, not for judging authors.
- [AI detector false positives](./detect-detector-false-positives.md) - detector tools that flag human writing. This page covers human judgment from folk marks, with no tool involved.
- Readers falsely accusing real people of using AI (queued, not yet written) - public accusations by readers in comments and posts; this page covers reviewers with power to act.

## 9. Common questions
### Does using em dashes mean AI wrote it?
No. Human writers use them heavily; one preprint found 0.33 to 17.12 per 1,000 words across eight published essays. Wikipedia's guide says the sign is useful only with other indicators, and newer models use fewer of them.

### Is "delve" proof someone used ChatGPT?
No. "Delve" rose across millions of abstracts after ChatGPT, but that is a corpus trend, not proof about one text. Wikipedia's guide says one or two such words "may be coincidental", and the word dropped off sharply in 2025.

### Can teachers tell if an essay was written by AI?
Not reliably by feel. In one study of 289 teachers, neither novices nor experienced teachers could pick out ChatGPT essays, and both were overconfident. Use draft history and a conversation (section 5, rule 3).

### Should I stop using em dashes so I don't get accused?
You should not have to, and this page asks reviewers never to require it (rule 7). If you are worried, write in a tool that keeps version history, so your drafts can speak for you.

### How should a teacher handle a suspected AI essay?
Write down three different kinds of tells with quotes, check version history or earlier work, show the student the record, and let a second person decide. See the evidence record in section 5.
