# Why AI Writing Has Headings, Bold and Bullets on Everything: Uniform Structure

<!-- SEO
title: AI Writing With Headings and Bullets on Everything: Fix
description: Why AI-drafted emails, posts and PR descriptions all get headings, bold lead-ins and a Key takeaways block, and a genre rule plus pre-publish check.
search phrases:
- why does ai writing use so many headings and bullet points
- how to tell if something was written by chatgpt formatting
- chatgpt key takeaways conclusion every time
- ai generated email bullet points bold headings
- stop chatgpt adding conclusion section
- ai written pr description too many headers
- linkedin post ai formatting bold bullets
- make ai write emails without bullet points
-->

**Frequency**: Common

## Issue: An AI-drafted email, post, PR description or README gets the same shape regardless of genre or length: a heading per section, bold lead-ins, bullets, and a Key takeaways or Conclusion block.

> **One line:** Every document the AI drafts looks like a slide deck, so readers spot it as AI output before they read a word; the fix is a prompt rule that picks format by genre and length, plus a pre-publish check that flags structure the genre does not use.

| | |
|---|---|
| **Channel** | Written for **published text**: emails, chat posts, social posts, PR descriptions, READMEs, memos and reports drafted with AI and sent under a person's name. Voice is out of scope. |
| **Stakes** | Low for an internal note. Medium to high when the reader is a customer, a hiring manager, a reviewer or a grieving colleague, and the shape tells them nobody wrote it for them. |
| **Who is affected** | Readers who receive the document, and the sender whose message reads as unedited AI output |
| **Frequency** | Common, by our reading. Expert readers in one study cited formatting in 15.0% of their explanations (section 4). I found no count of how often AI drafts ship with this shape. |
| **Pattern ID** | text-uniform-structure |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Genre-fit structure rate: AI-drafted documents that leave the pre-publish check with zero unwaived structure flags, divided by all checked documents. Proposed starting target: 95%. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Vendors now tell their models to format less, but preference training rewards lists and bold (section 4), and a model cannot know your genre or house style unless told. (Our judgment, not tested.) |
| **Also searched as** | chatgpt formatting giveaway · ai email with headings · "Key takeaways" at the end of every post · bold text every line ai · ai readme too many sections · inline bold bullet lists |

## 1. In plain words
People write a thank-you note, a bug fix description and a quarterly report in three different shapes. An AI drafting tool left to its defaults gives all three the same shape: title-case headings, bullets with a bold label and a colon, and a summary block at the end. Readers who use AI themselves now recognize that shape at a glance, and the message loses credit before its content is read.

## 2. What it looks like
**Without the fix**
```
Builder: Draft an email to Dana at Riverside Plumbing. We need to move Thursday's install in Columbus to Monday; the countertop is late.
AI tool: Subject: Installation Schedule Update
         ## Overview
         - **Reason for Change:** The countertop delivery has been delayed.
         - **New Date:** Monday, at the same time.
         ## Key Takeaways
         - **Flexibility:** We appreciate your flexibility.
         ## Conclusion
         Thank you for your understanding and continued partnership!
```
**With the fix**
```
Builder: Draft an email to Dana at Riverside Plumbing. We need to move Thursday's install in Columbus to Monday; the countertop is late.
AI tool: Subject: Moving Thursday's install to Monday
         Hi Dana, the countertop won't arrive until Friday, so we need to move Thursday's install to Monday.
         Does 9 a.m. Monday still work for your crew? If not, Tuesday morning is open too.
         Thanks, Sam
Pre-publish check: genre email, 52 words. 0 headings, 0 bullets, 0 summary blocks. Pass.
```
The fixed draft takes its shape from the genre (a short email is plain sentences), leads with the change, and drops the Overview, bold labels, Key takeaways and Conclusion that carried nothing new.

## 3. Why it happens
- **Preference training rewards the look.** Zhang et al. found human raters, GPT-4 and top reward models favor lists, bold text, links and emojis, and that models can exploit this (section 4). A model tuned on those preferences learns that structure scores well, whatever the genre.
- **The prompt names no genre, reader or length.** "Write an update about the delay" gives the tool nothing to choose a shape from, so it uses its default document shape, which looks like a README or a slide deck.
- **Nobody checks the shape before sending.** Reviewers read for facts and tone. A heading on a 60-word email or a Conclusion that repeats the opening passes because it is not wrong, only wrong for the genre.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Preference models, "including human evaluators, GPT-4, and top-ranking models on the RewardBench benchmark," show strong biases toward "lists, links, bold text, and emojis"; LLMs can exploit these biases to rank higher on AlpacaEval and LMSYS Chatbot Arena, and less than 1% biased data can inject significant bias into a reward model. | [Zhang et al., *From Lists to Emojis: How Format Bias Affects Model Alignment*, arXiv 2409.11704, Sept. 2024, revised May 2025](https://arxiv.org/abs/2409.11704). Opened (abstract and arXiv record). | Explains a cause; it measures rater and reward-model preference, not how readers react to published documents. I read the abstract, not the full tables. |
| In a study of 300 nonfiction articles, the majority vote of five annotators who often use LLMs for writing misclassified only 1 of 300. In their explanations, formatting appeared in 15.0% ("AI-generated formatting is overly consistent (e.g., fully capitalized headings, bolded lists, paragraphs of similar length)") and conclusions in 13.1% (AI conclusions are "repetitive and overly optimistic summaries"). | [Russell, Karpinska and Iyyer, *People who frequently use ChatGPT for writing tasks are accurate and robust detectors of AI-generated text*, ACL 2025, arXiv 2501.15654](https://arxiv.org/abs/2501.15654). Opened (abstract and HTML full text, Table 3). | Five expert annotators reading news-style articles, not emails or PR descriptions. The percentages are shares of explanations that mention the cue, not detection accuracy from formatting alone. |
| Wikipedia's field guide lists title-case headings, "Overuse of boldface," "Inline-header vertical lists" (a bullet followed by a bold header and a colon) and heading errors as signs of AI writing. It says chatbots bold phrases "often in a 'key takeaways' fashion," and that "Markdown presence" is among the most common current signs. | [Wikipedia, *Signs of AI writing*](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). Opened (page and raw wikitext), October 2026 version. | Volunteer editors' observations about Wikipedia content. The page says the list is "descriptive, not prescriptive" and "Not all text featuring these indicators is AI-generated." |
| Anthropic advises telling the model what to do instead of what not to do (for example, "smoothly flowing prose paragraphs" instead of "Do not use markdown"), and says the formatting style of the prompt might influence the style of the response. | [Anthropic, *Prompting best practices*](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices). Opened. | Vendor guidance for its own models; no measured effect is reported. It is the basis for writing the prompt block below as positive instructions. |

A search summary mentioned reports that a large share of long LinkedIn posts are AI-generated (Pangram Labs, Originality.ai). I did not open those sources, they rely on contested automatic detectors, and they are not used here.

**Public incident.** No dated incident found. The searches behind this page returned research and guides, not a named case where document shape alone caused harm.

## 5. The fix
**The principle:** The genre and length of the document decide its shape; structure the genre does not use is removed or waived with a reason before the document is sent.

**Do this**
1. **Every drafting prompt names the genre, the reader and a target length.** Check: the request log has a genre value from the table below; if it is missing, the tool asks once.
2. **Format comes from the genre table, not from habit.** Check: the draft's heading, bullet and summary-block counts are within the limits for its genre.
3. **No headings in any document of 300 words or fewer.** Check: heading count is 0. (300 is a starting point to tune.)
4. **No "Key takeaways", "Conclusion", "In summary" or "Final thoughts" block outside reports over 800 words, and never both a summary and a conclusion.** Check: phrase match on headings and closing paragraphs.
5. **No inline-header bullets (bold label, colon, text) in emails, letters, posts or PR descriptions.** Check: zero lines matching `- **Label:**` in those genres.
6. **Bullets only for 3 or more parallel items the reader will scan or act on.** Check: each item still makes sense if the list is reordered.
7. **A house template wins.** If the repo has a PR template or the company has a memo format, the draft fills that template and adds no sections of its own. Check: section names match the template.
8. **Run the structure check before publish and record waivers.** Check: every sent AI draft has a check result; each waived flag has a reason.

**Reference design: format by genre and length**
| Genre | Headings | Bullets | Bold | Summary or conclusion block |
|---|---|---|---|---|
| Email or letter under 300 words | None | Only 3+ items the reader must act on (dates, documents) | None | None |
| Condolence, apology, thank-you, cover letter | None | None | None | None |
| Chat or social post (Slack, LinkedIn) | None | One short list at most | None | None; no "Key takeaways" |
| PR description | The repo template's sections only; else none | Changed files or test steps | None | None; one summary sentence opens it |
| README or how-to guide | Yes, per task (install, usage) | Steps, options | Sparing, for UI labels | None |
| Memo or report over 800 words | Sentence-case headings, one per topic | Only for parallel items | At most one phrase per section | One summary at the top, not a conclusion that repeats it |

**Prompt block for the drafting tool**
```
Before drafting, confirm the genre, the reader and the length. If I have not said, ask me once.
Shape the draft the way a careful person writes that genre: an email or post is plain sentences,
a PR description follows the repository template, and only long reports and how-to guides use headings.
Write headings in sentence case. Use a bullet list only for three or more parallel items.
End where the content ends, with the next step or the ask, not with a summary of what you said.
```

**Pre-publish structure check**
| Flag | Rule | Default action |
|---|---|---|
| Heading in a document of 300 words or fewer | 3 | Remove |
| "Key takeaways", "Conclusion", "In summary", "Final thoughts", "TL;DR" heading in a short genre | 4 | Remove |
| Summary block and conclusion block in the same document | 4 | Keep one |
| `- **Label:** text` bullets in email, letter, post or PR description | 5 | Rewrite as sentences |
| Bullet list of fewer than 3 items, or items that depend on each other | 6 | Rewrite as sentences |
| Every section has the same paragraph count and a heading | 2 | Ask the author |
| Title-case headings, or a heading that repeats the document title | 2 | Fix case or remove |
| Section names that differ from the house template | 7 | Use the template |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the conversation is the author prompting the drafting tool, or the checker reporting to the author)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | The request names no genre or reader: "Is this an email to Dana or a note for the team channel?" |
| Lead with the answer | Every short draft opens with the point (the change, the ask, the decision), in a sentence, not under an Overview heading. |
| Offer choices | The checker flags structure: "Rewrite as plain sentences", "Keep it: this is a reference doc", "Use our template", "Something else". |

**Don't over-correct.** Do not strip structure from documents that need it: a README, a runbook, a long report or a step-by-step guide reads better with headings and lists. Do not turn real parallel items (documents to bring, three plan options) into a dense paragraph. Do not add typos or casual filler to "sound human"; the goal is a shape that fits the genre, not disguise.

**Hand-off rule.** When the genre is regulated or has an owner (legal notices, HR letters, investor updates, press releases), the checker does not rewrite; it flags and routes the draft to that owner or the house style guide.

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md). The flag list draws on the Wikipedia guide and the Russell et al. cue table (section 4) plus our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | "Draft something about the install delay" with no genre | The tool asks one question about genre or reader before drafting | 1 |
| 2 | 60-word email to a contractor | 0 headings, 0 bullets, 0 summary block | 2, 3 |
| 3 | LinkedIn post about a product launch | No "Key takeaways" heading and no closing summary | 4 |
| 4 | Email listing 4 documents a renter must bring to a Denver leasing office | One plain bullet list of the 4 items, no bold labels | 5, 6 |
| 5 | PR description in a repo with a template (Summary, Testing) | Only the template's sections appear | 7 |
| 6 | 1,500-word quarterly report | Sentence-case headings per topic; one summary at top; no repeated conclusion | 2, 4 |
| 7 | Condolence note to a coworker | Plain sentences only, no formatting | 2 |
| 8 | Draft sent without a check result in the log | Flagged in the weekly audit | 8 |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Genre-fit structure rate** (primary) | 95% | Check log: AI-drafted documents with zero unwaived structure flags / all checked documents | Below 85% |
| Headings in documents of 300 words or fewer | Under 2% | Count heading markup per draft by word count, from the check log | Over 5% |
| Summary or conclusion blocks in short genres | Under 2% | Phrase match on headings and last paragraph, by genre tag | Over 5% |
| Inline-header bullets in email, post or PR genres | Under 2% | Regex count of `- **Label:**` lines by genre tag | Over 5% |
| Drafts sent with no check result | 0 | Sent drafts in the send log without a matching check record | Any |
| Needed structure removed (counter-metric) | Under 5% | Monthly sampled review of 50 READMEs, guides and long reports after the check, labeled "structure missing" or not | Over 10% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Heading markup in an email or post under 300 words | Draft text plus genre tag | A newsletter or digest that the team formats with sections on purpose |
| A "Key takeaways" or "Conclusion" heading in a short genre | Heading text match | A training handout where a recap is the house format |
| Most bullets start with a bold label and a colon | Line-pattern ratio in the draft | A glossary or spec sheet where labeled items are the content |
| Every section has a heading and the same number of paragraphs | Section and paragraph counts | A form-based report generated from a fixed template |
| The reader replies "Did AI write this?" or "Is this ChatGPT?" | Phrase match in replies to sent drafts | A reader asking out of curiosity about a tool the team uses openly |

**Starter rule:** before an AI-drafted document is sent, flag any heading, summary block or bold-label bullet that its genre's row in the format table does not allow.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: text-uniform-structure
runs: pre_send
reads: [request.genre, request.reader, draft.word_count, draft.headings, draft.bullet_lines, draft.closing_block, house_template.sections, waiver_list]
trigger: an AI-drafted document is about to be sent or published, or the request names no genre
moves: [ask_clarifying_question, lead_with_answer, offer_choices]
choices: ["Rewrite as plain sentences", "Keep it: this is a reference doc", "Use our template", "Something else"]
on_miss: rewrite
metric: genre-fit structure rate
counter_metric: needed structure removed
status: proposed
```

## 8. Related patterns
- [Bullet and heading overuse](../../response-structure/failures/bullet-and-heading-overuse.md) - the closest existing pattern. It covers a chatbot's live reply that breaks reasoning into fragments; this page covers documents a person sends or publishes, where readers read the shape as an AI tell and the builder needs a genre rule and a pre-publish check.
- [Answer buried](../../response-structure/failures/answer-buried.md) - order, not shape. An Overview heading in front of the point buries it too.
- [Filler and padding](../../response-structure/failures/filler-and-padding.md) - a Conclusion that repeats the opening is padding as well as a structure tell.
- [Stock phrases](../../persona-and-tone/failures/stock-phrases.md) - canned wording in chat replies; this page is about canned shape.
- [Placeholder data left in](./ui-placeholder-data-left-in.md) and [emoji as icons](./ui-emoji-as-icons.md) - the same family's pre-ship checks for visual output.

## 9. Common questions
### How can you tell if ChatGPT wrote something from the formatting?
Look for title-case headings on a short text, bullets that start with a bold label and a colon, and a Key takeaways or Conclusion block that repeats the opening. These are signs, not proof; Wikipedia's guide warns that people write this way too.

### Why does AI put headings and bullet points in everything?
Preference training rewards lists and bold text (Zhang et al., section 4), and most prompts do not say what kind of document is wanted. With no genre given, the tool falls back on its default document shape.

### How do I get AI to write an email without bullet points?
Name the genre, reader and length, and say what you want instead of what you don't: "a plain email of three or four sentences that ends with the ask." Anthropic's guide recommends that positive phrasing. Use the prompt block in section 5.

### Should I delete every "Key takeaways" and "Conclusion" section?
In emails, posts, letters and PR descriptions, yes. In a long report, keep one summary at the top and drop the conclusion that repeats it.

### Is it OK to use headings in a README or a long report?
Yes. Reference documents and long reports need headings to be scanned. The failure is using that shape for genres that never had it.

### Will removing the formatting make AI text undetectable?
No, and that is not the goal. Russell et al.'s expert readers relied mostly on vocabulary and sentence patterns, not formatting alone. The goal is a document that fits its reader; disguise is out of scope.
