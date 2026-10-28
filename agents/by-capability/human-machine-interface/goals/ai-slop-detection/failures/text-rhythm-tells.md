# Em Dashes, Lists of Three and "It's Not X, It's Y": AI Writing Rhythm Tells

<!-- SEO
title: Em Dashes and "Not X, It's Y": Catch AI Writing Rhythm
description: AI drafts often stack em dashes, lists of three and "not X, it's Y" lines. A style rule and a pre-publish check catch them without blaming writers.
search phrases:
- em dash AI writing
- does using em dashes mean AI wrote it
- how to stop chatgpt using em dashes
- "it's not x it's y" AI writing
- rule of three AI writing tell
- signs of AI writing sentence structure
- AI writing uniform sentence length burstiness
- check blog post for AI writing patterns before publishing
-->

**Frequency**: Common

## Issue: AI drafts often stack em dashes, lists of three and "not X, it's Y" lines. A style rule and a pre-publish check catch them without blaming writers.

> **One line:** An AI-drafted email or post goes out with an em dash in every other sentence, every claim in a set of three, and "This isn't just X, it's Y" in each paragraph, so readers hear a template; the fix is a style rule in the prompt plus a pre-publish check that counts these marks and sends flagged lines to a person, who rewrites them with real specifics.

| | |
|---|---|
| **Channel** | Written for **text** a builder publishes: marketing emails, blog posts, product pages, release notes, support macros. Chat replies get the same check before send (planned). |
| **Stakes** | Low to medium. One email reads as careless. A brand that ships the same cadence every week teaches readers to skim it. Using these marks to accuse a person of using AI is a separate, higher-stakes harm (see "Don't over-correct"). |
| **Who is affected** | Readers of the published text, and the writer or brand whose text sounds machine-made |
| **Frequency** | Common, by our reading: Wikipedia's editor guide lists all three marks as signs of AI writing (section 4). I found no count of how often published AI-drafted text carries them. |
| **Pattern ID** | text-rhythm-tells |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Rhythm-check clearance rate: published AI-drafted pieces whose pre-publish rhythm check shows zero unreviewed flags, divided by all published AI-drafted pieces. Proposed starting target: 100%. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Vendors have already cut em dashes in newer models, but the guide notes the habit moves to other marks, and triplets and stock contrasts remain. (Our judgment, not tested.) |
| **Also searched as** | AI em dash overuse · "not just X but Y" ChatGPT · ChatGPT writes in threes · how to make AI writing sound human · AI writing tells checklist · burstiness AI detection |

## 1. In plain words
Read an AI draft aloud and you can often hear it before you see it. A dash sets up a reveal, a "not X, it's Y" turns a plain fact into a correction nobody asked for, and claims come in threes ("faster, smarter, and simpler"). Sentences also run to about the same length. Any one of these is normal human writing; the tell is the stack, sentence after sentence. The fix is not to ban a punctuation mark but to replace the template with facts only the writer knows.

## 2. What it looks like
**Without the fix**
```
Writer:  Draft the email for our free gait check this Saturday at Stride Running Co. in Columbus.
AI tool: This isn't just a fitting — it's a chance to rethink how you run.
         Our experts will film your stride, find your perfect shoe, and help you run
         farther, faster, and pain-free. It's not about selling shoes — it's about you.
         Spots are limited — book today!
Writer:  Perfect. Sending to 4,200 subscribers.
(Reply from a regular customer: "Did a robot write this?")
```
**With the fix**
```
Writer:  Draft the email for our free gait check this Saturday. Style rules attached.
AI tool: Free gait check this Saturday, 9 a.m. to 1 p.m., at our High Street store.
         A fitter films you on the treadmill for two minutes and plays the clip back.
         Then you try a couple of pairs that suit how you land.
         Bring the shoes you run in now. We have 24 slots.
Check:   0 em dashes, 0 "not X, it's Y", 0 three-item runs. Sentence length 4 to 15 words.
         No flags. Writer still reads it before sending.
```
The fixed draft swaps the reveal, the contrast and the triplets for a time, a place, a step and a number.

## 3. Why it happens
- **Training data and tuning reward the "punched up" register.** Wikipedia's guide says models regress toward the most likely, most broadly palatable prose, and that their em dashes often mimic sales-like writing. Marketing copy is exactly where builders use AI most.
- **The template fills the space where facts should be.** When the prompt gives no time, place or number, a triplet or a "not X, it's Y" makes a thin claim sound complete. (Our reading; it matches the guide's note that triplets make shallow analysis look thorough.)
- **A "no em dashes" rule alone does not stick, and it does not touch the rest.** One preprint found that some models kept using em dashes even when told not to, and none of these rules changes the contrasts or triplets (section 4).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| LLM output is "much more disposed" to em dashes than nonprofessional human text of the same genre, often in a formulaic way, and the sign "is most useful when taken in combination with other indicators, not by itself." | [Wikipedia, *Signs of AI writing*, "Overuse of em dashes"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). Opened (page source, Oct. 2026 version). | Community editor guide, written for Wikipedia text; it says some signs may not apply elsewhere. It now files em dashes under "historical indicators." |
| The same guide says LLMs overuse the rule of three ("adjective, adjective, adjective") and that "not just X, but Y" contrasts are common among human writers but "stereotypically an 'AI sign.'" | [Wikipedia, *Signs of AI writing*, "Rule of three" and "Negative parallelisms"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). Opened. | Observations, not counts. The guide calls its list descriptive and says "Not all text featuring these indicators is AI-generated." |
| Wikipedia reports that a July 30, 2026 *Economist* study found only Claude, among current models, used em dashes more than professional writers, and ChatGPT used them less. | [Wikipedia, *Signs of AI writing*](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), citing *The Economist*. | **Read through Wikipedia only.** I did not open the *Economist* article. Shows the em dash signal changes by model and date. |
| In 8 published human essays (57,232 words) em dashes ran 3.23 per 1,000 words on average, with a range of 0.33 to 17.12. GPT-4.1 produced 10.62 per 1,000 unprompted and 3.86 when told directly not to use them; DeepSeek V3 kept 1.57 under the same instruction. | [Freeburg, *The Last Fingerprint: How Markdown Training Shapes LLM Prose*, arXiv 2603.27006, March 2026](https://arxiv.org/abs/2603.27006). Abstract and full HTML opened. | Single-author preprint, not peer reviewed, small human sample. The 50-fold human range is the useful part: heavy dash use is normal for some writers. |
| On Nov. 14, 2025, Sam Altman posted that if you tell ChatGPT not to use em dashes in custom instructions, "it finally does what it's supposed to do." TechCrunch notes this does not remove em dashes by default. | [TechCrunch, *OpenAI says it's fixed ChatGPT's em dash problem*, Nov. 14, 2025](https://www.techcrunch.com/2025/11/14/openai-says-its-fixed-chatgpts-em-dash-problem/). Opened. | News report of a vendor claim; not tested by us. |
| On 5,935 matched human and machine document pairs, a test scored em dashes at AUROC 0.595, the rule of three at 0.515 and sentence-length burstiness at 0.521, where 0.500 is chance. Median machine long-form text had 3.50 em dashes per 1,000 words; median human long-form text had none. | [Opace, *AI writing myths measured*, Aug. 30, 2026](https://opace.agency/tools/ai/content-verification-integrity/research/ai-writing-myths-measured/). Opened. | **Vendor, single source**, methods not peer reviewed. If right, each mark alone barely beats a coin flip at telling authors apart. |
| A detector-review site defines burstiness as variation in sentence length and structure, says AI text "tends to be less 'bursty'," and says detectors "should not be relied upon to provide absolute proof." | [Scribbr, *How do AI detectors work?*](https://www.scribbr.com/ai-tools/how-do-ai-detectors-work/). Opened (page source). | Vendor that sells writing tools; explains the idea, does not measure it. |
| Several GPT detectors consistently misclassified non-native English writing samples as AI-generated, while native samples were classified correctly. | [Liang et al., *GPT detectors are biased against non-native English writers*, arXiv 2304.02819 (published in *Patterns*)](https://arxiv.org/abs/2304.02819). Abstract opened. | About detector tools in general, not these marks. I read the abstract only, so no rates are given here. Shows the cost of false blame. |

**Public incident.** I found no dated, sourced case of a brand publicly called out for rhythm tells alone, so I describe none.

## 5. The fix
**The principle:** Count the marks before publishing, have a person rewrite the flagged lines with specifics, and never treat a count as proof of who wrote the text.

**Do this**
1. **Give the tool a rhythm rule in the prompt.** Every AI drafting prompt for public copy includes the style block below.
2. **Em dash budget.** AI-drafted copy has at most one em dash per 200 words (proposed); each extra one is flagged.
3. **Contrasts only for a real misconception.** "Not X, it's Y", "not just X, but Y" and "isn't X, it's Y" appear at most once per piece, and only when a reader actually believes X.
4. **Lists have as many items as the facts.** No stacked three-adjective or three-phrase runs ("faster, smarter, and simpler"); at most one three-item list per paragraph.
5. **Vary sentence length.** Flag any paragraph of four or more sentences where every sentence is within 5 words of the others (proposed).
6. **Fix with facts, not punctuation.** A flagged line is rewritten with a time, place, number, name or step. Swapping a dash for a comma or semicolon while keeping the same contrast counts as unfixed.
7. **A person decides.** The check reports counts and lines; it never auto-rewrites or blocks, and a human reads every flagged piece before it ships.
8. **Never use the count to accuse.** Reviews of someone else's text (a student, a contractor, a job applicant) report the marks only; they do not conclude "AI-written."

**Reference design: prompt block**
```
Write in plain sentences. Do not use em dashes; use a period, comma or colon.
Do not use "not X, it's Y" or "not just X, but Y" unless I name a belief readers hold.
Do not group adjectives or phrases in threes. List exactly the items I give you.
Mix short and long sentences. Use the facts I give (times, places, prices, names);
if a sentence has no fact in it, ask me for one instead of filling it with style.
```

**Reference design: pre-publish rhythm check**
| Mark | What to count | Flag when (proposed) | Action |
|---|---|---|---|
| Em dash | "—" and spaced " -- " or " - " used as a dash | More than 1 per 200 words | Show each line to the writer |
| Negative parallel | "not ... it's", "isn't ... it's", "not just ... but", "not only ... but", "rather than" in a contrast | More than 1 per piece | Ask: who believes X? |
| Three-run | Three adjectives or three short phrases joined by commas and "and" | More than 1 per paragraph | Ask for the real list |
| Flat length | Sentence word counts in a paragraph | 4+ sentences all within 5 words | Suggest a split or a merge |
| Stack | Two or more marks above flagged in the same piece | Always | Human rewrite before publish |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the conversation is the AI tool drafting for the writer, or the checker reporting to the writer)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | A sentence has style and no fact ("help you run farther, faster, and pain-free"): the tool asks for the one fact it should carry. |
| Offer choices: 2-4 options plus "Something else", free text open | The checker flags a line: "Rewrite with a fact", "Keep it (house style)", "Cut the sentence", "Something else". |
| Admit uncertainty and show how to check | Every report says the marks are style signals, not proof of AI use, and shows the counted lines. |
| Hand off to a person | Any stack flag, and any review of text written by someone else. |

**Don't over-correct.** Em dashes, lists of three and contrasts are ordinary English; human writers in one preprint ranged from 0.33 to 17.12 em dashes per 1,000 words. Do not strip a writer's own dashes because a tool flagged them, and do not ban the mark from a style guide that uses it. A blanket swap breeds the next tell: Wikipedia's guide notes that newer models told to avoid em dashes now lean on periods and commas, a claim the guide itself marks as needing a citation. Never present these counts as evidence that a person used AI; detectors already misjudge non-native writers.

**Hand-off rule.** Send to a human editor when a piece has two or more mark types flagged, when it goes to more than one audience at once (an email list, a press release), or when anyone asks "was this AI-written?" about someone else's text. The editor rewrites or signs off; the tool does not answer the authorship question.

**Framework used:** none yet. The marks come from Wikipedia's *Signs of AI writing* guide; the thresholds are our proposal.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Drafting prompt for a launch email with no style block | Prompt linter flags the missing block | 1 |
| 2 | 300-word post with 6 em dashes | Check flags 5 lines and names them | 2 |
| 3 | Post with "It's not a sale, it's a celebration" and "not just shoes, but a lifestyle" | Second contrast is flagged; the writer is asked who believes X | 3 |
| 4 | Paragraph with "faster, smarter, and simpler" and "bold, fresh, and fun" | One three-run is flagged | 4 |
| 5 | Five sentences of 14, 15, 16, 14, 15 words | Flat-length flag | 5 |
| 6 | Writer fixes "isn't X — it's Y" as "isn't X; it's Y" | Check still flags it | 6 |
| 7 | Human-written essay with 12 em dashes per 1,000 words, author's house style | Report shows counts with a "not proof" note; nothing is auto-changed; waiver is logged | 7, 8 |
| 8 | Manager asks the tool "Did my contractor use AI?" | Tool lists marks, states they are not proof, and hands off | 8 |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Rhythm-check clearance rate** (primary) | 100% | Publish log: AI-drafted pieces with zero unreviewed flags / all AI-drafted pieces published | Any piece published with an unreviewed flag |
| Em dashes per 1,000 words in AI-drafted copy | At or below your human-written baseline | Count in the publish log; compare with a sample of the team's own human-written copy | Above 2x baseline for a month |
| Stacked-tell rate | Under 5% of pieces | Pieces with two or more mark types flagged / all pieces checked | Over 10% |
| Fix-by-punctuation rate | 0 | Sampled review of 30 edited flags a month: dash swapped, contrast kept | Any |
| Human-text flag rate (counter-metric) | Track; set from baseline | Run the check on a labeled set of the team's human-written posts | Rising two months in a row |
| Authorship claims made by the tool (counter-metric) | 0 | Search tool replies for "AI-written", "generated by AI" when reviewing others' text | Any |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Em dash density above the team's human baseline | Draft text in the publish log | A writer whose own style uses many dashes, or a genre (fiction, essays) that does |
| Two or more "not X, it's Y" contrasts in one piece | Regex count on the draft | A myth-busting post where readers really hold X |
| Repeated three-item adjective or phrase runs | Draft text, comma-and-"and" pattern | A real list of three products, steps or locations |
| Flat sentence length across a paragraph | Word counts per sentence | Short legal or safety text written to a fixed template |
| Three or more mark types in the same piece | Combined check output | A human imitating "punchy" ad copy; still worth a rewrite, never an accusation |

**Starter rule:** before publishing AI-drafted copy, count em dashes, negative-parallel contrasts and three-runs, and send any piece with a flag to a person for a fact-based rewrite.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: text-rhythm-tells
runs: pre_send
reads: [draft.text, draft.word_count, draft.source (ai_drafted | human), style_waivers]
trigger: an AI-drafted piece is about to publish, or a user asks whether a text was AI-written
moves: [ask_clarifying_question, offer_choices, admit_uncertainty, hand_off]
choices: ["Rewrite with a fact", "Keep it (house style)", "Cut the sentence", "Something else"]
on_miss: ask
metric: rhythm-check clearance rate
counter_metric: human-text flag rate
status: proposed
```

## 8. Related patterns
- [Stock phrases](../../persona-and-tone/failures/stock-phrases.md) - the closest existing pattern. It covers canned words ("I'd be happy to help", "As an AI") at the start of chat replies; this page covers the shape of sentences (dashes, contrasts, triplets, even length) anywhere in published text, whatever the words.
- [Filler and padding](../../response-structure/failures/filler-and-padding.md) - sentences that add nothing. A triplet or contrast often carries a real fact in a template shape, so cutting it is not enough; it needs a rewrite.
- [Bullet and heading overuse](../../response-structure/failures/bullet-and-heading-overuse.md) - structure applied to text that did not need it; the Freeburg preprint links em dashes to markdown habits.
- [Stock hero copy and template section order](./ui-generic-hero-layout.md) - the same "any company could say this" problem in page headlines.

## 9. Common questions
### Does using em dashes mean AI wrote it?
No. Human writers use them heavily too; one preprint found a 50-fold range across eight published essays. Wikipedia's guide says the sign is useful only with other indicators, and newer models use fewer of them. Treat a count as a reason to reread, not a verdict.

### How do I stop ChatGPT from using em dashes?
Put the rule in custom instructions or in the prompt block in section 5. OpenAI's CEO said in November 2025 that ChatGPT now follows that instruction, and a 2026 preprint found some other models still leak dashes. Run the count before publishing either way.

### Why does AI keep writing "It's not X, it's Y"?
The contrast makes a plain statement sound like an insight, and the guide notes it is a common human device too. Keep it only when readers really believe X; otherwise state Y with a fact.

### Can an AI detector measure sentence-length variation reliably?
Not on its own. One vendor test put burstiness near chance on matched documents, and a detector-review site says detectors cannot give absolute proof. Use length checks as an editing aid.

### Should I just replace my em dashes with commas?
Only if the sentence reads better. Swapping the mark while keeping the same reveal or contrast leaves the rhythm in place, so rewrite with a concrete detail instead (rule 6).
