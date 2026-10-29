# Why Does ChatGPT Always End With a Summary or a Moral? Stated-Moral Endings in AI Writing

<!-- SEO
title: Why ChatGPT Always Ends With a Summary or a Moral, and the Fix
description: AI-drafted posts, emails and stories close with "Ultimately, it's about trust" or "The lesson here is". An ending rule plus a last-paragraph check catches it before publishing.
search phrases:
- why does chatgpt always end with a summary
- chatgpt ends every story with a moral
- stop chatgpt from adding a conclusion at the end
- ai writing ultimately at the end
- in the end it's about ai writing tell
- how to tell if ai wrote a story ending
- chatgpt last paragraph repeats everything
- ai generated linkedin post ends with lesson
-->

**Frequency**: Very Common

## Issue: An AI-drafted post, email, story or essay closes with a tidy stated lesson or wrap-up ("Ultimately, it's about community", "The lesson here is", "At the end of the day") that repeats what the piece already said, and readers and editors flag it as an AI tell.

> **One line:** The last paragraph of an AI draft restates the thesis as a moral or summary, and readers who know the habit "go to the end" to spot the AI; the fix is an ending rule (end on the last concrete fact, action or next step, and cut a final paragraph that only summarizes) plus a check on the last paragraph before the piece is sent or published.

| | |
|---|---|
| **Channel** | Written for **published text** in prose: blog and LinkedIn posts, newsletters, emails, short stories, personal essays and op-eds drafted with ChatGPT, Claude, Gemini or Copilot. Headed "Conclusion" blocks are covered by the uniform-structure page (section 8). |
| **Stakes** | Low to medium. A moral on a blog post costs some credit. It costs more on a story for a contest or a class, a eulogy, or a cover letter, where the reader concludes nobody wrote it for them. |
| **Who is affected** | Readers, editors and teachers who read to the end, and the writer whose name is on the piece |
| **Frequency** | Very common, by our reading. Expert readers in one study cited conclusions in 13.1% of their explanations (section 4). I found no count of how often AI drafts end this way. |
| **Pattern ID** | text-stated-moral-endings |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Clean-ending rate: AI-drafted prose pieces whose final paragraph passes the ending check (no unwaived wrap-up phrase and no restated thesis), divided by all checked pieces. Proposed starting point: 95% (tune). |
| **Maturity** | Researched (see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | Partly. Wikipedia editors now describe the habit mainly in "older LLMs", but the study in section 4 caught it in GPT-4o and Claude 3.5 Sonnet output, and only the writer knows where a given piece should stop. (Our judgment, not tested.) |
| **Also searched as** | chatgpt always adds a conclusion · ai story ends with a lesson · "at the end of the day" ai · ai essay summary ending · remove moral from ai story · "in conclusion" ai giveaway |

## 1. In plain words
People end a piece where the content ends: the last fact, the last scene, the ask. An AI draft adds one more paragraph that tells the reader what it all meant: "Ultimately, it's about the people we meet along the way." That paragraph says nothing new, sounds like a greeting card, and is exactly where practiced readers look first. The writer can catch it by checking one paragraph before the piece goes out.

## 2. What it looks like
**Without the fix**
```
Owner:   Write a 150-word LinkedIn post about our Tucson bakery's first year. We sold 41,000 loaves and
         hired our first two bakers in June. Next month we start selling at the Rillito farmers market.
AI tool: [Three paragraphs covering the loaves, the hires and the market.]
         At the end of the day, this journey has never really been about bread. It's about community,
         resilience and the power of showing up every single morning. Here's to year two!
Owner:   Nice. Posting it.
         (A comment under the post: "Did ChatGPT write the last paragraph?")
```
**With the fix**
```
Owner:   Write a 150-word LinkedIn post about our Tucson bakery's first year. We sold 41,000 loaves and
         hired our first two bakers in June. Next month we start selling at the Rillito farmers market.
AI tool: [Three paragraphs covering the loaves, the hires and the market.]
         Starting Sunday, November 1, find us at the Rillito farmers market, 8 a.m. to noon. Bring cash or a card.
Ending check: last paragraph names a date, a place and an action. 0 wrap-up phrases. Restates the thesis: no. Pass.
```
The fixed draft stops on the next step the reader can take. The "it was never about bread" paragraph is gone, and nothing the reader needed went with it.

## 3. Why it happens
- **The model learned that endings summarize.** Wikipedia's editors describe LLMs that end "paragraphs or sections by summarizing and restating its core idea", the school-essay shape. With no instruction about the ending, the draft uses it for every genre, including stories and short posts.
- **The model leans positive at the close.** The guidelines the Russell et al. experts wrote say AI tends "to emotionally uplift the reader, especially towards the conclusion", which is why the wrap-up becomes a moral ("resilience", "community") instead of a plain recap.
- **Nobody re-reads the last paragraph alone.** The writer checks that the facts in the body are right; the closing paragraph is not wrong, so it passes. No check asks whether deleting it would lose anything. (Our reading.)

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Five expert annotators (people who often use LLMs for writing) labeled 300 nonfiction articles; their majority vote misclassified only 1 of 300. Conclusions appeared in 13.1% of their explanations: "AI-generated conclusions tend to be repetitive and overly optimistic summaries, while human-written conclusions end more abruptly and less tidily." | [Russell, Karpinska and Iyyer, *People who frequently use ChatGPT for writing tasks are accurate and robust detectors of AI-generated text*, ACL 2025, arXiv 2501.15654](https://arxiv.org/html/2501.15654). HTML full text opened. | Nonfiction articles, not emails or fiction. 13.1% is the share of explanations that mention the cue, not accuracy from endings alone. Single study. |
| The same paper ends with one expert's comment on a GPT-4o conclusion: "This time I went to the end of the piece and said: 'Hello, AI.'" The experts' own guidelines say "AI-generated text always ends with a neat conclusion, instead of just ending the article naturally" and conclusions "summarize everything that has already been written". | Same paper, conclusion section and appendix guidelines. Opened. | Annotator opinion recorded in the paper, not a measured rate; "always" is the annotators' word. Cheerful summary conclusions still showed up after paraphrasing, per the paper. |
| Wikipedia's guide, under "Section summaries", lists "In summary", "In conclusion" and "Overall" as words to watch, and says older LLMs "often ended paragraphs or sections by summarizing and restating its core idea." A separate section says AI "Challenges" paragraphs end "with either a vaguely positive assessment" or speculation about the future. | [Wikipedia, *Signs of AI writing*](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). Raw wikitext opened, Oct. 2026 version. | Volunteer editors' guide for encyclopedia text; it says it is less useful for fiction and "Not all text featuring these indicators is AI-generated." It cites Ju et al. (ACL Findings 2025), which I did not open. |
| A storytelling paper reports that writers' concerns about LLM co-writing included "overly moralistic and predictable endings", citing Chakrabarty et al. (2024b). | [Mirowski et al., *Fabula: Building a Narrative Storytelling Sidekick with the Writers' Community*, arXiv 2606.14411](https://arxiv.org/html/2606.14411). HTML opened. | Secondhand: I did not open the Chakrabarty et al. paper it cites. Writers' critique, not a count. |
| GPTZero's writing guide says "ChatGPT tends to put a summary sentence at the end of any response, even if it's just writing a few simple sentences," and calls "In conclusion" "a strong tell". | [Faizan Mehdi, GPTZero, April 4, 2024](https://gptzero.me/news/untitled/). Opened. | Vendor of an AI detector, with an interest in the claim. No data given. |

**Read only in search summaries.** A search summary pointed to an OpenAI community forum thread where users ask ChatGPT to stop ending replies with a conclusion; I did not open it and do not rely on it. I found no study that counts moral endings in AI versus human fiction, and no test of whether cutting the wrap-up changes reader trust. **Public incident:** none found; this is a style default, not a dated event.

## 5. The fix
**The principle:** A piece ends on its last piece of content, a concrete fact, scene, action or next step, never on a sentence that tells the reader what the piece meant.

**Do this**
1. **The last paragraph adds something.** Check: it contains at least one fact, name, date, number, scene detail or action that does not appear earlier in the piece. If not, cut it and re-check the new last paragraph.
2. **No wrap-up opener in the last two sentences.** Check: no unwaived match for the phrase list below in the final two sentences.
3. **No restated thesis.** Check: the final sentence does not repeat the title or the opening claim in other words. A judge or a reviewer answers "Does this sentence say what the opening already said?"; yes fails.
4. **Stories end in the scene.** Check: the last paragraph of fiction is action, dialogue or image; no sentence states what a character "learned" or what the story is "about".
5. **Emails and posts end on the ask or the next step.** Check: the last sentence is the request, the date, the link or the action, followed only by a sign-off.
6. **Re-check after every edit.** A human edit or a second AI pass re-runs the ending check, because a rewrite often adds the moral back.

**Reference design: ending phrase list** (case-insensitive; in the last two sentences only; starting list, our judgment plus the sources in section 4)
| Group | What to match | Default action |
|---|---|---|
| Stated moral | "The lesson here is", "The real lesson", "What I learned is that", "It was never really about", "it's about" + abstract noun | Block |
| Wrap-up openers | "Ultimately,", "At the end of the day", "In the end,", "In conclusion", "In summary", "To sum up", "Overall," | Block |
| Uplift closers | "remember that", "anything is possible", "a testament to", "here's to", "the journey" | Flag; rewrite unless waived |

**Prompt block for the drafting tool**
```
End where the content ends. The last paragraph must give the reader something new: the next step,
a date, a link, a final fact, or in fiction the last action or line of dialogue.
Do not state the lesson, the theme or what the piece "is really about". Do not summarize earlier paragraphs.
Before you finish, read your last paragraph alone. If deleting it loses no fact, delete it.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the conversation is the writer prompting the drafting tool, or the checker reporting to the writer)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | The request gives no next step or final fact to end on: "What should readers do or know last: the market date, a link, something else?" |
| Offer choices | The checker flags the ending: "Cut the last paragraph", "End on the next step", "Keep it: the moral is the point", "Something else". |
| Admit uncertainty and show how to check | The checker cannot tell a restated thesis from a real final point: it shows the last paragraph next to the opening and asks the writer. |

**Don't over-correct.** A summary is not always wrong. A report over about 800 words (tune) may open with one; a children's fable or a sermon is expected to state its moral; a speech may repeat its main point on purpose. Do not end every piece on an abrupt fact to "sound human", and do not cut the one sentence of thanks or regret that belongs in a personal email. The rule targets a closing paragraph nobody chose and that adds nothing.

**Hand-off rule.** When the piece is a eulogy, an apology, a legal or HR notice, or graded or contest writing, the checker does not rewrite the ending; it flags the paragraph and routes it to the named author or owner. When the checker is used to judge whether someone else (a student, an applicant) used AI, it hands the decision to a person and reports the ending only as weak evidence.

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md). The phrase list draws on Wikipedia's guide and the Russell et al. annotator guidelines (section 4) plus our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Bakery post whose last paragraph only restates "community" | Check fails; cutting it leaves the market date last | 1, 5 |
| 2 | Newsletter ending "Ultimately, it's about trust." | Blocked; phrase named | 2 |
| 3 | Op-ed whose final sentence rewords its headline | Restated-thesis check fails | 3 |
| 4 | 1,000-word short story ending "She finally learned that home is where the heart is." | Flagged; ending moves into the scene | 4 |
| 5 | Email to a landlord in Columbus about a broken heater | Last sentence is the ask (repair date) plus sign-off | 5 |
| 6 | Clean draft; an editor adds "At the end of the day, we're a family." | Re-check blocks | 6 |
| 7 | Children's fable that states its moral on purpose, waived | Pass; waiver recorded (over-correction check) | 2 |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Clean-ending rate** (primary, proposed) | 95% | Ending-check log: pieces with no unwaived phrase hit and no restated-thesis flag in the last paragraph / all checked pieces | Below 90% in a week |
| Final paragraphs with no new fact | Under 5% | Rule plus judge on the last paragraph versus the rest of the piece | Over 10% |
| Wrap-up phrases in the last two sentences, at draft | Track; set from baseline | Phrase scan of AI drafts before editing | Rising two weeks in a row |
| Pieces published with no ending-check record | 0 | Publish log without a matching check record | Any |
| Reader comments asking "Did AI write this?" | Track; set from baseline | Phrase match in comments and replies | Any rise after a template change |
| Intended endings flagged in error (counter-metric) | Under 10% | Monthly review of 50 flags, labeled real tell or chosen ending | Over 20% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| "Ultimately", "At the end of the day" or "The lesson" in the last two sentences | Ending scan of the draft | A quote, or a piece about AI writing habits |
| The last paragraph has no number, name or date absent from the earlier text | Token overlap between the last paragraph and the body | A short poem or a closing line that echoes the opening on purpose |
| The final sentence closely rewords the title or the first sentence | Similarity score, last sentence versus title and opening | A speech or sermon that repeats its point by design |
| An abstract noun stack in the close ("community, resilience and growth") | Last-paragraph text | A mission statement where those words are the actual content |

**Starter rule:** before an AI-drafted prose piece is sent or published, flag a final paragraph that adds no new fact or that opens with a listed wrap-up phrase, and require a cut or a recorded waiver.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: text-stated-moral-endings
runs: pre_send
reads: [request.genre, draft.title, draft.first_paragraph, draft.last_paragraph, draft.body, phrase_list.version, waiver_list]
trigger: an AI-drafted prose piece is about to be sent or published, or the drafting tool is about to report it as done
moves: [ask_clarifying_question, offer_choices, admit_uncertainty]
choices: ["Cut the last paragraph", "End on the next step", "Keep it: the moral is the point", "Something else"]
on_miss: rewrite
metric: clean-ending rate
counter_metric: intended endings flagged in error
status: proposed
```

## 8. Related patterns
- [Headings, bold and bullets on everything](./text-uniform-structure.md): the closest existing pattern. Its rule 4 removes headed "Key takeaways", "Conclusion" and "In summary" blocks from short genres. This page covers only the ending, in prose with no heading at all: the final paragraph or sentence that states a moral or restates the thesis, including in stories and essays, which that page does not cover.
- [Chatbot filler and closing recaps](../../response-structure/failures/filler-and-padding.md): the same recap habit in a live chat reply. This page is about pieces a person sends or publishes, where readers read the ending as an AI tell.
- ["It depends" answers that never pick](./text-balanced-non-answers.md): closes with "Ultimately, the choice is yours" instead of a verdict. That page is about the missing decision; this one is about an ending that repeats what was said.
- [Stock phrases in AI-written text](./text-stock-phrases.md) and [rhythm tells](./text-rhythm-tells.md): word-level and sentence-shape tells anywhere in the piece; this page checks one position, the end.

## 9. Common questions
### Why does ChatGPT always end with a summary?
Chatbots learned the school-essay habit of restating the main idea at the end, and Wikipedia's editors describe LLMs doing it at the end of paragraphs and sections. With no instruction about the ending, the draft adds one. Tell the tool where to stop (the prompt block in section 5).

### How do I stop ChatGPT from adding a moral to every story?
Ask for an ending inside the scene, an action, a line of dialogue or an image, and forbid stating what a character learned. Then read the last paragraph alone; if it explains the story, cut it.

### Is ending with "Ultimately" a sign that AI wrote it?
It is a sign, not proof. Experts in the Russell et al. study used tidy, upbeat conclusions as one clue, and Wikipedia warns that people write this way too. Never accuse someone on the ending alone.

### Should an essay never have a conclusion?
A conclusion that adds a new point, a consequence or a next step is fine. The tell is a final paragraph that only repeats the piece in softer words. Use the check in rule 1: if deleting it loses no fact, delete it.

### Will "make it sound human" fix the ending?
Usually not, by our reading: the tool swaps "Ultimately" for "When all is said and done" and keeps the moral. Name the ending you want and run the ending check.
