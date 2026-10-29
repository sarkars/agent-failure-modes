# Why AI Writing Sounds Like a Report: "-ing" Clauses, Nominalizations and "Including" Lists

<!-- SEO
title: Why AI Writing Sounds Like a Report, and How to Check It
description: AI drafts stack "-ing" clauses, abstract nouns and "including" lists even when told to match a style. Count them against your own writing before publishing.
search phrases:
- why does ai writing sound like a report
- ai writing too formal
- chatgpt writes in noun phrases
- ai writing ending sentences with ing phrases
- highlighting the importance ai writing
- make chatgpt match my writing style
- grammatical differences between ai and human writing
- ai text nominalization participle clauses
-->

**Frequency**: Common

## Issue: AI drafts stack "-ing" clauses, abstract nouns and "including" lists even when told to match a style. Count them against your own writing before publishing.

> **One line:** An AI-drafted newsletter, post or update comes out in a dense report voice ("reflecting our commitment", "a wide range of services, including...", "Overall, this represents an important step"), even when the prompt said "match our style"; the fix is a prompt rule that asks for verbs, people and one concrete example, plus a pre-publish check that compares the draft's grammar rates with your own human-written pieces.

| | |
|---|---|
| **Channel** | Written for **published text**: newsletters, blog posts, member and customer updates, product pages, internal announcements drafted with ChatGPT, Claude, Gemini or Copilot. Chat replies are planned. |
| **Stakes** | Low to medium. The piece reads as boilerplate and gets skimmed. Using these rates to accuse a person of using AI is a separate, higher-stakes harm (see "Don't over-correct"). |
| **Who is affected** | Readers of the published text, and the writer or brand whose voice turns into a generic report voice |
| **Frequency** | Common, by our reading: instruction-tuned models used present participial clauses at 2 to 5 times the human rate when asked to continue a text in its own style (section 4). I found no count for marketing or member mail. |
| **Pattern ID** | text-hedged-list-register |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Register-match rate: published AI-drafted pieces whose register check shows no feature above its flag line, or whose flags were reviewed by a person, divided by all published AI-drafted pieces. Proposed starting target: 95%. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Larger models did not close the gap in the study below, and instruction-tuned models drifted further than base models, so a style prompt alone is not enough; a baseline check stays with the builder. (Our judgment from one study, not tested.) |
| **Also searched as** | AI writing sounds corporate · ChatGPT formal tone · "ensuring" and "highlighting" AI · AI writing too wordy · AI won't match my voice · academic tone in AI drafts |

## 1. In plain words
Chatbots don't only pick favorite words; they pick a favorite grammar. They tack "-ing" clauses onto sentences ("..., ensuring members stay informed"), turn actions into abstract nouns ("the implementation of the expansion"), and build lists with "including" and "such as" where a person would name one thing. The result sounds like a grant report, even in a note about branch hours. You can count these features and compare them with your own past writing.

## 2. What it looks like
**Without the fix**
```
Editor: Write a short member update: our Columbus branch opens at 8 a.m. instead of 9 starting June 2. Match our usual friendly newsletter style.
AI tool: Starting June 2, our Columbus branch will open at 8 a.m., reflecting our ongoing commitment to member convenience
         and ensuring access to a wide range of services, including deposits, loan consultations, and account management.
         This adjustment represents an important enhancement to the accessibility of our in-person offerings.
         Overall, the change underscores our dedication to meeting the evolving needs of our community.
Editor: Fine. Scheduling it for 31,000 members.
```
**With the fix**
```
Editor: Write a short member update: our Columbus branch opens at 8 a.m. instead of 9 starting June 2. Match our usual friendly newsletter style.
AI tool: Starting June 2, our Columbus branch on High Street opens at 8 a.m., an hour earlier.
         I don't know why the hours changed. Give me one reason in your words, or I'll leave it out.
Editor: Lots of members asked to stop in before work.
AI tool: Lots of you asked to stop in before work, so we will open at 8. See you then.
Register check: participial clauses 0, nominalizations near our baseline, no "including" list, no "Overall" opener. Ready.
```
The fixed draft uses verbs and people instead of abstract nouns, names one real reason instead of a service list, and the check compares it with the credit union's own writing before it goes out.

## 3. Why it happens
- **Instruction tuning pushes text toward a dense, informational register.** Reinhart et al. found instruction-tuned GPT-4o and Llama 3 models departed from human grammar rates more than base Llama 3 models, and Milička et al. report base models "often performed stylistically better than instruction-tuned ones" (section 4). Why tuning does this is not settled in the sources I read; Juzek and Ward's tests are consistent with human-feedback tuning playing a role for word choice.
- **"Match our style" is too weak an instruction.** In Reinhart et al., the models were given 500 words of the human text and told to continue "in the same style, tone, and diction", and still shifted. A style request without examples of verbs, people and concrete detail doesn't hold.
- **The prompt has few facts, so the grammar fills the space.** With one fact (new hours), a participial clause, a service list and an "Overall" line make the text look complete. (Our reading.)

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Compared with human continuations of the same texts, instruction-tuned models used present participial clauses at 224% to 527% of the human rate (human rate 1.7 per 1,000 words) and nominalizations at 145% to 214% (human 14.6 per 1,000). Phrasal coordination ran 144% to 194% (human 6.1). Base Llama 3 stayed close to human rates (participial clauses 94% and 102%). | [Reinhart et al., *Do LLMs write like humans? Variation in grammatical and rhetorical styles*, arXiv 2410.16107 v1](https://arxiv.org/html/2410.16107v1), published in PNAS Feb. 2025 per a search summary. HTML full text opened. | Models tested: GPT-4o, GPT-4o Mini, Llama 3 8B and 70B. English, two corpora of about 39 and 34 million words. Single study; newer models not tested. I did not open the PNAS page. |
| The same paper reports example output: "Bryan, leaning on his agility, dances around the ring, evading Show's heavy blows." Some features went the other way: GPT-4o used agentless passives at 53% and contractions at 60% of the human rate. | Same paper. Opened. | Shows the drift is not "more formal on every count"; the check must use your own baseline, not a fixed list. |
| A classifier on these features told human from GPT-4o text with about 98% accuracy within the corpora, but trained on one corpus and tested on arXiv text it reached 70.63% for GPT-4o and about 51% (near chance) for base Llama models. | Same paper, Tables 8 and 10. Opened. | Why this page uses the features as a pre-publish style check on your own drafts, not as an authorship detector. |
| CMU's news release on the study says LLMs used present participle clauses at "two to five times" the human rate and nominalizations at 1.5 to 2 times. | [Carnegie Mellon University News, *Is It Human, or Is It AI?*, Feb. 24, 2025](https://www.cmu.edu/news/stories/archives/2025/february/is-it-human-or-is-it-ai). Opened. | University press release about its own study; secondary to the paper. |
| A benchmark of 16 models using Biber's multidimensional analysis found most models shifted English text "from involved to informational production", with consistent shifts toward explicit reference across all models, and that "Base models often performed stylistically better than instruction-tuned ones". | [Milička, Marklová, Cvrček, *Benchmark of stylistic variation in LLM-generated texts*, arXiv 2509.10179, Sept. 2025](https://arxiv.org/html/2509.10179). Abstract and HTML opened. | Reports dimension scores, not single words; results for Czech differ. Venue (International Journal of Corpus Linguistics, 2026) taken from the arXiv record. |
| Wikipedia's editor guide lists "superficial analyses", "often done by attaching a present participle ('-ing') phrase at the end of sentences", with words to watch such as "highlighting", "underscoring", "ensuring", "reflecting" and "contributing to". | [Wikipedia, *Signs of AI writing*](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). Opened (about 200,000 of 250,000 characters). | Volunteer guide, not a study. It does **not** list "overall", "including" or "important" as signs; it says not all text with these signs is AI-generated. |
| In 14 million PubMed abstracts, "Out of all 319 excess style words in 2024, 66% were verbs and 16% were adjectives"; excess words included "additionally", "crucial", "enhancing", "notably" and "within". | [Kobak et al., arXiv 2406.07016 v4](https://arxiv.org/html/2406.07016v4). Opened. | Scientific abstracts. The paper does not name "important", "overall" or "including" as excess words. |

**What I could not support.** The words in this page's working title, "important", "overall" and "including", are common in AI drafts by our reading, but no source I opened measures them as AI markers. This page treats them as parts of measured features (an "including" list is a kind of phrasal coordination; "Overall," is a summary opener) and never as proof on their own.

**Public incident.** Not required for this tier; none searched.

## 5. The fix
**The principle:** Before an AI draft ships, its grammar is compared with your own human-written pieces, and any feature far above your baseline is rewritten into verbs, people and one concrete example.

**Do this**
1. **Build a baseline from your own writing.** Measure the features below in 20 or more pieces your team wrote without AI (tune). Store the rate per 1,000 words for each feature.
2. **Flag features at 2x your baseline.** A draft whose rate for any feature is twice your baseline or more is flagged (starting point; Reinhart et al. found 1.5x to 5x gaps for models).
3. **Rewrite sentence-final "-ing" clauses.** A clause like ", ensuring..." or ", reflecting..." becomes its own sentence with a subject who does something, or is cut.
4. **Name one, not a list.** An "including" or "such as" list of three or more items is replaced with the one item the reader needs, unless the list is the content (a menu, a schedule).
5. **Turn abstract nouns back into verbs.** "The implementation of the expansion" becomes "we added". Keep a noun when it is the real term (a "loan consultation" you book).
6. **No "Overall," wrap-up line.** If the last sentence restates the piece, cut it.
7. **Give the prompt facts and a sample.** The prompt includes one human-written past piece and the facts; when a fact is missing, the AI tool asks once instead of filling the space.
8. **Re-check after edits.** A human edit or second AI pass re-runs the check.

**Reference design: register check** (counts per 1,000 words; patterns are rough approximations, our judgment)
| Feature | What to count | Default action |
|---|---|---|
| Sentence-final participial clause | Comma followed by a word ending in "-ing" ("..., ensuring", "..., highlighting") | Flag at 2x baseline; show each line |
| Nominalizations | Words ending in -tion, -ment, -ness, -ity, -ance, -ence (minus a stop list of your product terms) | Flag at 2x baseline |
| "Including" / "such as" lists | "including" or "such as" followed by 3 or more comma-separated items | Show every one; ask "is this list the content?" |
| Summary openers | Sentence starting "Overall,", "In summary,", "Ultimately," | Show; cut unless it adds a fact |
| Importance adjectives | "important", "crucial", "key", "essential", "significant" | Count only; never blocks |

**Prompt block for the AI tool**
```
Write like the sample below. Use people as subjects and active verbs ("we open at 8").
Do not end a sentence with a comma and an -ing clause. Do not list services with "including" or "such as";
name the one thing that matters to this reader. Do not end with an "Overall" summary.
If you lack a fact, name it and ask; do not fill the gap with a general sentence.
Sample: [paste one past piece your team wrote]
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the conversation is the editor prompting the AI tool, or the checker reporting to the editor)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The draft's first sentence states the change (new hours, date), not a commitment line. |
| Ask one clarifying question | The draft has one fact; the tool asks for the reason instead of adding a participial clause or a service list. |
| Offer choices: 2-4 options plus "Something else", free text open | The checker flags a line: "Rewrite with a verb", "Cut it", "Keep it (this list is the content)", "Something else". |
| Admit uncertainty and show how to check | The checker shows rates against the baseline and says rates show style, not who wrote the text. |

**Don't over-correct.** Do not strip every "-ing" word or every noun; technical, legal and financial text needs nominalizations, and the gap is about rate, not presence. Do not flatten text into choppy short sentences; that is a different template (see [rhythm tells](./text-rhythm-tells.md)). Do not use these rates to decide that a student, applicant or contributor used AI: the features drop to near-chance accuracy outside the training corpus (section 4), and people who learned formal English write this way too.

**Hand-off rule.** When a flag sits in legal, medical, rate or fee text, route it to the named owner for a human rewrite instead of auto-fixing. When anyone asks the checker whether a person used AI, it declines to score authorship and points to [folk tells are not evidence](./text-folk-tells-unreliable.md).

**Framework used:** none yet. The features come from Biber's register features as used by Reinhart et al. and Milička et al. (section 4).

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Team has 20 past newsletters | Baseline rates stored per feature | 1 |
| 2 | Draft with participial clauses at 3x baseline | Flagged, each line shown | 2, 3 |
| 3 | Branch-hours update with "a wide range of services, including..." | List replaced by one reason or one service | 4 |
| 4 | Holiday schedule listing five closed dates with "including" | Kept as content, no rewrite forced | 4 |
| 5 | "Implementation of the new hours" | Rewritten with "we" and a verb | 5 |
| 6 | Draft ends "Overall, this change..." | Line cut or given a fact | 6 |
| 7 | Prompt has no reason for the change | Tool asks once; no padding clause | 7 |
| 8 | Clean draft, then editor adds ", ensuring..." | Re-check flags it | 8 |
| 9 | User asks "did my intern use AI?" | Checker declines and shows the "not evidence" note | Hand-off |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Register-match rate** (primary) | 95% | Pre-publish check log: pieces with no unreviewed flag / all published AI-drafted pieces | Below 90% in a week |
| Participial-clause rate at publish, vs. baseline | Under 1.5x | Same check, per 1,000 words | Above 2x for two weeks |
| Nominalization rate at publish, vs. baseline | Under 1.5x | Same check | Above 2x for two weeks |
| "Including" lists per 1,000 words | Track | Same check | Rising after a model change |
| Baseline age | Under 12 months | Date of the baseline set | Older than 12 months |
| Flag false-positive rate (counter-metric) | Under 15% | Monthly review of 50 flags, labeled "needed a rewrite" or "fine as is" | Over 25% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Two or more sentences end in a comma plus an "-ing" clause in one short piece | Pre-publish check on the draft body | A sports or action story where the writer chose this on purpose |
| Nominalization rate at 2x the team baseline or more | Register check output | A policy, legal or technical piece, which is dense by genre |
| An "including" or "such as" list of 3+ items in a piece with one stated fact | Check output plus fact count from the prompt | A schedule, menu or eligibility list that is the content |
| Last sentence starts "Overall," and adds no number, date or name | Check on the final sentence | A long report where a summary is expected |
| Rates jump across all features after a model or tool change | Weekly rate trend | A new writer or a new content type joined the mix |

**Starter rule:** flag for human rewrite any AI-drafted piece whose sentence-final participial-clause or nominalization rate is twice the team's own human-written baseline or more.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: text-hedged-list-register
runs: pre_send
reads: [draft.body, draft.word_count, team_baseline.rates, team_baseline.date, term_stop_list]
trigger: an AI-drafted piece is about to be sent or published, or the AI tool is about to report a draft as done
moves: [lead_with_answer, ask_clarifying_question, offer_choices, admit_uncertainty]
choices: ["Rewrite with a verb", "Cut it", "Keep it (this list is the content)", "Something else"]
on_miss: rewrite
metric: register-match rate
counter_metric: flag false-positive rate
status: proposed
```

## 8. Related patterns
- [Stock phrases in AI-written text](./text-stock-phrases.md) - the closest existing pattern. It blocks named words and phrases ("delve", "It's important to note") with a fixed list; this page measures grammar rates (participial clauses, nominalizations, list-building) against your own baseline, which a word list cannot catch.
- [Em dashes, lists of three and "not X, it's Y"](./text-rhythm-tells.md) - sentence shape and punctuation; this page is the noun-heavy register underneath, not the cadence.
- ["It depends" answers that never pick](./text-balanced-non-answers.md) - hedging that withholds a verdict; here the problem is dense wording around a fact that is present.
- [Why AI always ends with a summary or a moral](./text-stated-moral-endings.md) - covers endings in depth; this page only counts the "Overall," opener as one feature.
- [Does using em dashes mean AI wrote it?](./text-folk-tells-unreliable.md) - why none of these features proves authorship.
- [AI detection rules stop working after a model update](./detect-rules-decay.md) - re-measure baselines and flag lines after a model change.

## 9. Common questions
### Why does ChatGPT write like a report even when I ask for casual?
In one study, models told to continue a text "in the same style, tone, and diction" still used "-ing" clauses and abstract nouns far more than the humans did. Give the model a sample of your writing and facts, and check the result (section 5).

### What is a present participial clause, in plain words?
An "-ing" phrase hanging off a sentence: "We updated the app, ensuring a smoother experience." Rewrite it as its own sentence with a subject: "The app now loads faster."

### Are "overall", "including" and "important" proof that AI wrote something?
No. No source I opened measures these words as AI markers, and people use them all the time. Treat them as parts of a pattern you count, not as tells on their own.

### Can I use these features as an AI detector?
Not for judging people. A classifier on these features dropped to near chance on some models when tested outside its training texts (section 4). Use them to edit your own drafts.

### How many of my own pieces do I need for a baseline?
Start with 20 or more pieces of the same kind written without AI. That number is our starting point, not a sourced figure.
