# Auto-Translated Duplicate Pages and Machine-Translated Web Data: Mass Machine-Translated Duplicates

<!-- SEO
title: Auto-Translated Duplicate Pages and Machine-Translated Data
description: AI agents mass-translate pages into many languages with no review. Publish only reviewed translations and filter multi-way copies from training data.
search phrases:
- is auto translating my website bad for seo
- ai translate whole site into 20 languages
- google scaled content abuse translated pages
- machine translated content low resource languages training data
- multi-way parallel machine translation web filter
- wikipedia machine translated articles errors
- how to detect machine translated text in a web crawl
-->

**Frequency**: Common

## Issue: AI agents mass-translate pages into many languages with no review. Publish only reviewed translations and filter multi-way copies from training data.

> **One line:** A content agent is told "translate the whole site," and it pushes thousands of unreviewed machine-translated copies of the same pages into 20 languages; readers in those languages get garbled text, the site risks a spam penalty, and the copies end up in other teams' training data. The fix is to translate only pages people in that language need, have a fluent reviewer pass a sample before any language goes live, keep unreviewed copies out of search, and drop text that appears in many machine-translated languages at once when you build a dataset.

| | |
|---|---|
| **Channel** | Written for **agent-run publishing and data pipelines**: a localization or content agent that generates and publishes pages, and a crawl pipeline that ingests multilingual web text. Chat is the control surface; voice is not covered. |
| **Stakes** | Medium for a single site (lost trust, a possible search penalty). High for speakers of smaller languages, where these copies can become most of what exists online in their language (section 4). |
| **Who is affected** | Readers who search in a language other than English; site owners and SEO teams; ML teams that train multilingual models on web text; volunteer editors of small-language wikis |
| **Frequency** | Common, in our judgment. One study found 57.1% of sentences in a 6.4B-sentence web corpus sat in groups translated into three or more languages (section 4). I found no count of sites that mass-publish unreviewed translations. |
| **Pattern ID** | data-machine-translated-duplicates |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Reviewed-before-index rate: machine-translated pages that are open to search only after a fluent reviewer passed a sample of that language, divided by all indexable machine-translated pages. Proposed starting target: 100%. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Better translation lowers the error count, but the harm also comes from volume and from translating pages nobody in that language asked for, which no model fixes. (Our judgment, not tested.) |
| **Also searched as** | auto-translated spam pages · machine translation seo penalty · translationese in training data · ai translated wikipedia · hreflang auto translate · multilingual content farm |

## 1. In plain words
Translating a page with AI costs almost nothing, so it is easy to copy a whole site into every language at once. Nobody who reads those languages checks the result, and the copies say the same thin thing 20 times. Researchers now find that much of the web in smaller languages is this kind of copy. The fix is to translate less, check what you publish, and treat many-language copies as a warning sign when you collect data.

## 2. What it looks like
**Without the fix** (illustrative: a home-improvement blog in Columbus, Ohio, using a content agent)
```
Owner: Translate all 4,000 posts into every language you support and publish.
Agent: Done. 4,000 posts x 22 languages = 88,000 new pages, all live
       with hreflang tags and added to the sitemap.
Owner: Great.
(A month later: a Swahili reader reports that "drywall anchor" was rendered
 as a word for a ship's anchor in every post. Search traffic drops after a
 spam review. A dataset vendor's crawl ingests all 22 copies.)
```
**With the fix**
```
Owner: Translate all 4,000 posts into every language you support and publish.
Agent: Readers came in Spanish (11%) and French (3%); the other 20 languages
       had under 50 visits last year. Before I publish, pick one:
       1. Spanish and French, reviewed sample first (recommended)
       2. Spanish only, as a pilot
       3. All 22 languages, but unreviewed ones kept out of search (noindex)
       4. Something else (tell me what you have in mind)
Owner: 1. My cousin reads Spanish; I'll find a French reviewer.
Agent: Each reviewer gets 25 posts; a language goes live once they pass.
```
The fixed agent checks real demand, offers choices with "Something else", and holds each language until a fluent person signs off.

## 3. Why it happens
- **Translation is nearly free, so volume is the default.** An agent asked to "translate everything" has no cost signal to stop it, and the per-language page count multiplies the site by the number of languages.
- **Nobody on the team can read the output.** A team ships 22 languages but reads one, so errors in smaller languages, where machine translation is weakest, go unseen until a reader complains.
- **Crawlers cannot tell a careful translation from a mass copy.** A data pipeline sees each language copy as fresh native text unless it checks how many other languages hold the same sentences.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a corpus of "6.4B unique sentences in 90 languages," 57.1% of sentences came from groups translated into three or more languages. Lower-resource languages were more multi-way parallel. | [Thompson et al., *A Shocking Amount of the Web is Machine Translated*, Findings of ACL 2024, arXiv 2401.05749v2](https://arxiv.org/html/2401.05749v2). Opened (HTML version). | One corpus built by the authors; "multi-way parallel" is a proxy for machine translation, not proof for each sentence. |
| Highly multi-way parallel translations scored lower in quality: 8+ way groups were 6.2 CometQE points below 2-way pairs. The authors call multi-way parallelism "a promising way to detect low quality, machine translated data." | Same paper. Opened. | Quality is a model-based estimate, not human rating. Basis for rule 5. |
| Content translated into many languages leaned toward low-value topics: "Conversation & Opinion" rose from 22.5% of 2-way data to 40.1% of 8+ way data, consistent with low-quality English content translated "en masse." | Same paper (abstract and body). Opened. | The authors infer ad-revenue motives; they do not prove them. |
| Google's spam policy lists "automated transformations like synonymizing, translating, or other obfuscation techniques" under scaled content abuse, which it defines as many pages generated "for the primary purpose of manipulating search rankings." | [Google Search Central, Spam policies](https://developers.google.com/search/docs/essentials/spam-policies). Opened. | A platform policy, not law. Purpose and value decide it, not the use of translation alone. |
| In June 2025 Google removed advice to block auto-translated pages with robots.txt, calling it "a docs-only change, no change in behavior." | [Search Engine Journal, Matt G. Southern, June 11, 2025](https://www.searchenginejournal.com/google-removes-robots-txt-guidance-for-blocking-auto-translated-pages/548870). Opened. | Trade press. Means value, not a blanket block, is the test. |
| Google told an SEO consultant that "our policies do not strictly define content that has been translated by AI as spam." He reports Reddit had about 2.3M AI-translated URLs ranking in France and 2.4M in Spain, and that site owners hit by manual actions tied to translation at scale contacted him. | [Glenn Gabe, G-Squared Interactive, May 5, 2025, updated June 11, 2025](https://www.gsqi.com/marketing-blog/auto-translating-content-google-scaled-content-abuse/). Opened. | One consultant; the penalized sites are unnamed and unverified. Shows that translation can rank when it adds value. |
| The Greenlandic Wikipedia had about 1,500 articles, mostly by people who did not speak Greenlandic; one machine-translated entry said Canada had 41 inhabitants. Its new admin deleted nearly all of it. Volunteers on four African-language editions estimated 40% to 60% of their articles were uncorrected machine translations. | [Jacob Judah, MIT Technology Review, Sept. 25, 2025](https://www.technologyreview.com/2025/09/25/1124005/ai-wikipedia-vulnerable-languages-doom-spiral/). Opened. | Journalism with volunteer estimates, not a measured audit. |
| The same article cites a 2022 study that found Wikipedia was "the sole easily accessible source of online linguistic data for 27 under-resourced languages," so bad copies there feed later models. | Same article. Opened. | The 2022 study itself was not opened. |
| A historical Wikimedia page states: "an unedited machine translation, left as a Wikipedia article, is worse than nothing." | [Meta-Wiki, Machine translation](https://meta.wikimedia.org/wiki/Machine_translation). Opened. | The page is "kept for historical interest"; policy may be obsolete. |

**Could not open:** the Search Engine Land article on Reddit's AI translations returned 403. Its content is kept out of this page.

## 5. The fix
**The principle:** Translate where readers exist, publish only what a fluent person has checked, and treat sentences that show up in many machine-translated languages as low-trust data.

**Do this**
1. **Check demand before translating.** Before a bulk translation job, the agent reports traffic or customer counts per target language and recommends only languages above a threshold the owner sets. It never runs a "translate everything" job without showing these counts.
2. **No language goes live unreviewed.** Each new language stays `noindex` and out of the sitemap until a fluent reviewer passes a random sample (proposed starting point: 25 random pages per language). The reviewer's name and date are logged.
3. **Lock key terms.** Product names, part names, prices, units and safety words come from a reviewed glossary per language. A page that contains a glossary term translated outside the glossary is held.
4. **Label machine translation to readers.** Every unreviewed or sample-reviewed translated page says it was machine-translated and links to the original-language page.
5. **Filter multi-way copies in data pipelines.** When building a multilingual dataset, group near-identical sentences across languages. Groups found in many languages (proposed starting flag: 8 or more) are tagged `likely_mt` and capped or excluded, and the share removed is reported per language.
6. **Do not translate thin pages.** Pages that are short, auto-generated, or have under a set traffic floor in the source language are not queued for translation.

**Reference design: translation publish gate**
| Check | Looks at | Action on hit |
|---|---|---|
| No demand data | Bulk job with no per-language audience counts | Ask owner; do not start |
| Unreviewed language | Language with no passed reviewer sample | Keep `noindex`, out of sitemap |
| Glossary miss | Locked term translated off-glossary | Hold page |
| Missing MT label | Translated page without label and source link | Block publish |
| Thin source page | Source below length or traffic floor | Skip page |
| Multi-way group (data side) | Sentence group in 8+ languages | Tag `likely_mt`, cap or drop |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md))
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | The owner asks for a bulk translation into many languages: offer the reviewed-subset, pilot and noindex options. Do not offer choices when the owner already named reviewed languages. |
| Ask one clarifying question | No audience data exists: ask once which languages their customers read. |
| Admit uncertainty and show how to check | The agent reports translation quality: it says no one has reviewed the language and names what the sample check covers. |
| Hand off to a person | A reviewer fails a sample, or a reader reports a mistranslated safety or price term: a fluent person fixes the glossary before any more pages ship. |

**Don't over-correct.** Do not refuse translation or strip every non-English page: translated pages can serve readers well and can rank (section 4). Do not delete small-language data from a corpus outright; for some languages it is most of what exists. Cap and tag it, and keep a slice of verified native text.

**Hand-off rule.** A language fails its reviewer sample twice, or a reader reports a wrong safety, price or legal term: pull that language to `noindex` and send it to a fluent person before republishing.

**Framework used:** none yet. Rule 5 draws on the multi-way parallelism finding (Thompson et al.); the rest is our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Owner asks "translate everything into all languages" | Agent shows per-language demand and offers choices before starting | 1 |
| 2 | Spanish pages generated, no reviewer yet | All Spanish pages `noindex`, not in sitemap | 2 |
| 3 | "Drywall anchor" translated off-glossary | Page held | 3 |
| 4 | Translated page published without label | Publish blocked | 4 |
| 5 | Crawl contains a sentence group in 12 languages | Group tagged `likely_mt`, share removed reported | 5 |
| 6 | 80-word auto-generated tag page queued | Page skipped | 6 |
| 7 | Owner names two reviewed languages up front | No choice menu; job runs for those two | 1 |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Reviewed-before-index rate** (primary) | 100% | Indexable MT pages in languages with a passed sample / all indexable MT pages | Below 100% |
| Reviewer sample pass rate | 90% or more | Pages passed / pages sampled, per language | Below 80% |
| Pages per reader by language | Tracked | New pages per language / visits in that language | 1,000+ pages in a language with under 50 visits a year |
| `likely_mt` share by language (data side) | Reported each build | Tagged sentences / all sentences, per language | Rise of 10+ points between builds |
| Over-filtering rate (counter-metric) | Under 20% | Monthly review of 30 removed sentences by a fluent reader, labeled human or MT | Over 40% human |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Page count in a language jumps by thousands in one day | CMS publish log | A planned launch with reviewers in place |
| New language pages have near-zero visits after 60 days | Analytics by language | New market still being promoted |
| The same sentence group appears in 8+ languages in a crawl | Cross-language near-duplicate join | Official multilingual text, such as UN or EU documents |
| Readers report wrong words in one language | Feedback tagged by locale | A regional term dispute between fluent speakers |
| Indexable pages in a language with no reviewer record | CMS index flags joined with review log | Reviewer log not yet synced |

**Starter rule:** keep every machine-translated language out of search until a fluent reviewer has passed a sample of its pages.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: data-machine-translated-duplicates
runs: pre_send
reads: [job.target_languages, analytics.visits_by_language, review_log.language_status, page.indexable, page.mt_label, glossary.hits, corpus.multiway_group_size]
trigger: a bulk translation job is requested, a translated page is about to be indexed, or a multilingual dataset is built
moves: [offer_choices, ask_clarifying_question, admit_uncertainty, hand_off]
choices: ["Reviewed languages only", "One language as a pilot", "All languages, unreviewed kept noindex", "Something else"]
on_miss: ask
metric: reviewed-before-index rate
counter_metric: over-filtering rate
status: proposed
```

## 8. Related patterns
- [Model collapse from AI-generated training data](./data-model-collapse-contamination.md) - the closest page. It covers AI-written text of any kind entering a training set and fixes it with provenance tags and a frozen human set. This page covers one specific source, mass machine-translated copies, which can be found by counting how many languages hold the same text, and also covers the publishing side that creates them.
- [Unchecked translation in high-stakes text](../../language-and-locale/failures/unchecked-translation-in-high-stakes-text.md) - one bot translating a bill or a dose for one user. This page is about volume: thousands of unreviewed pages published at once.
- [Templated reviews](./data-templated-reviews.md) - another kind of mass, near-duplicate AI text that pollutes scrapes.
- [AI detector false positives](./detect-detector-false-positives.md) - why the data filter caps and tags instead of judging single sentences.

## 9. Common questions
### Will Google penalize my site for AI-translated pages?
Not for translation alone. Google says AI-translated content is not strictly spam, but its policy lists translating as one way to mass-produce low-value pages for rankings (section 4). Translate pages readers want, review them, and keep unreviewed copies out of search.

### Should I translate my whole website into every language?
Usually not. Start with the languages your customers read, check a sample with a fluent person, and add more as demand shows up (section 5, rules 1 and 2).

### How much of the web is machine translated?
No one has an exact number. One 2024 study found 57.1% of sentences in a large web corpus were part of groups translated into three or more languages, and those groups looked like low-quality machine translation. The share is higher in smaller languages.

### How do I find machine-translated text in a training corpus?
Group sentences that are translations of each other across languages. Text that appears in many languages at once is a strong sign of mass machine translation, per the same study. Tag and cap it rather than trusting a detector on single sentences.

### Why does this matter for small languages?
For some languages, a few websites and a small Wikipedia are almost all the text online. If those are filled with bad machine translations, models trained on them learn the errors and translate the language worse.
