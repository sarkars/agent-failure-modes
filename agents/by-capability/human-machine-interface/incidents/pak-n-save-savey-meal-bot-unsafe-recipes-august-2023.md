---
title: "Pak'nSave's Savey Meal-bot Turns Household Chemicals Into 'Recipes'"
date: 2023-08-04
source: "https://interestingengineering.com/innovation/rogue-ai-bot-recipes-for-human-flesh-and-chlorine-gas"
summary: "In August 2023, users of New Zealand supermarket chain Pak'nSave's AI recipe tool entered non-food items and got back named recipes, including one that would produce chlorine gas. A spokesperson said a small minority had misused the tool and that controls would be fine-tuned, per Interesting Engineering, Futurism and ESM Magazine."
categories:
  - Customer Service
patterns:
  - false-premises-accepted
  - stakes-blind-register
---

**This page is a dated teardown of one public incident with a store's AI recipe tool, for teams that let shoppers type free text into a generator.** Every fact below comes from a source we opened (listed at the end). We give no harmful recipe or ingredient list on purpose.

## What happened

- **June 8, 2023.** Pak'nSave, a New Zealand supermarket chain, introduced the Savey Meal-bot, per the company's own page. Shoppers typed at least three ingredients they had at home, and the tool used AI to write a simple recipe that they could save and share. The stated aim was to cut food waste and save money.
- **August 4, 2023.** New Zealand political commentator Liam Hehir posted on X a recipe the bot had called an "aromatic water mix." Interesting Engineering (August 10) and Futurism (August 11) report that it would have produced chlorine gas. Interesting Engineering reports that another X user posted, the same day, a "Mysterious Meat Stew" that listed human flesh.
- **Other outputs.** Futurism names more recipes built from household chemicals. ESM Magazine (August 15) adds "poison bread sandwiches" and "mosquito-repellent roast potatoes," from media reports.
- **The model.** Interesting Engineering says the bot ran on OpenAI's GPT-3.5; ESM says ChatGPT-3. The sources differ, and Pak'nSave's page names no model.

The sources do not explain why the bot accepted these inputs, and none shows Pak'nSave's own logs.

## What the company said and did

A Pak'nSave spokesperson told The Guardian, as relayed by Interesting Engineering, Futurism and ESM, that the company was disappointed that a small minority had "tried to use the tool inappropriately and not for its intended purpose." Interesting Engineering reports that the company said it would "keep fine-tuning our controls" so the bot was safe and useful; ESM gives the same point in paraphrase. ESM notes the terms say users should be over 18.

The sources differ on the warning. Interesting Engineering says the site warned, before ingredients were entered, that an AI writes the recipes and no human reviews them. Futurism says the bot "now warns" this. ESM says Pak'nSave added warnings and tighter limits after the coverage. Interesting Engineering reports that when it retried the first user's inputs, the bot answered "Invalid ingredients found, or ingredients too vague."

Pak'nSave's page, updated March 28, 2025, says the tool is retiring after about 88,300 unique recipes. It does not mention the August 2023 coverage.

## What the sources do not say

- How many unsafe recipes were made, or whether anyone tried to make one. We found no report of harm.
- What the "controls" were before or after August 2023, or the date of any change.
- Whether ingredient checks existed at launch. Interesting Engineering's later test suggests a check existed by August 10.
- The Guardian's own wording. Its page refused our fetch tool, so every Guardian detail here is second-hand.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [False premises accepted](../goals/dialogue-management/failures/false-premises-accepted.md) (`false-premises-accepted`). Partial fit. The input "here are my ingredients" carried an untrue premise, that every item was food, and the bot answered as if it were true. That pattern is written for questions about orders and records, not for a generator's input list.
- [Stakes-blind register](../goals/stakes-calibration/failures/stakes-blind-register.md) (`stakes-blind-register`). Partial fit. The bot gave a toxic mix a cheerful dish name, as if it were any other meal. That pattern covers tone across stakes; here the failure was the content, and tone made it worse.

Adjacent, and different:

- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) shares the sure tone, but these outputs were unsafe, not merely wrong.
- [Over-refusal of ordinary requests](../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md) is the risk on the other side of any fix: an ingredient check that rejects real foods.

The core failure, no check on what a user may feed a generator, is not covered by any pattern in the taxonomy. We do not force a match.

## What the design failure was

In this library's terms: a free-text box fed a recipe writer, and nothing between them asked "is this food?" A disclaimer that no human reviews recipes moves the risk to the reader; it does not stop a named, shareable recipe for a toxic gas.

## What to measure

Our proposals, not Pak'nSave's. Status: Not yet run.

| Metric | How to compute from logs |
|---|---|
| Non-food acceptance rate | Scripted ingredient lists with a non-food item that still produce a recipe, divided by those lists |
| False-reject rate | Scripted lists of real grocery items that get "invalid ingredient," divided by those lists |
| Hazard-name rate | Generated recipes whose title or steps name a cleaning product, fuel or poison, divided by recipes |
| Share-before-check rate | Recipes saved or shared before any output check ran, divided by shared recipes |

## What a team can change

Our proposals, not Pak'nSave's. Status: Not yet run. The example is a US grocery chain's "use your leftovers" tool.

1. **Check the input against the catalog.** Accept only items that match the store's food catalog or a food list. Check: a scripted list with drain cleaner gets no recipe in 100% of runs.
2. **Check the output too.** Run every recipe past a second check for non-food items before display. Check: a scripted recipe naming a cleaning product is blocked.
3. **Say what it can do.** When an item is rejected, name it and offer a food swap: "Drain cleaner isn't food. Add chicken, rice or eggs?" Check: the reply names the item and a next step.
4. **Don't over-correct.** A shopper who types "ground beef, $4.99 tortillas, salsa" should get tacos. Check: the false-reject rate on a real-grocery set stays near zero.
5. **Gate sharing.** A recipe that failed any check cannot be saved or shared. Check: no shared link exists for a blocked recipe.
6. **Test before launch.** Run rules 1, 2 and 4 before the tool goes live and after each model change. Check: a dated pass record exists per release.

## Sources

| URL | Publisher | Date | Status |
|---|---|---|---|
| https://interestingengineering.com/innovation/rogue-ai-bot-recipes-for-human-flesh-and-chlorine-gas | Interesting Engineering (Sejal Sharma) | 2023-08-10 | Opened 2026-10-20 (read through the fetch tool's page summary) |
| https://futurism.com/the-byte/supermarket-ai-poison | Futurism (Maggie Harrison Dupré) | 2023-08-11 | Opened 2026-10-20 (read through the fetch tool's page summary) |
| https://www.esmmagazine.com/technology/new-zealand-supermarket-rolls-out-ai-based-bot-to-reduce-food-waste-247294 | ESM Magazine (Branislav Pekic) | 2023-08-15 | Opened 2026-10-20 (read through the fetch tool's page summary) |
| https://www.paknsave.co.nz/news/2023/savey-meal-bot | Pak'nSave (company page) | 2023-06-08, updated 2025-03-28 | Opened 2026-10-20 (read through the fetch tool's page summary) |

Not opened, and not used as facts above: The Guardian's report (our fetch tool cannot reach theguardian.com), the source of the spokesperson's statement; Decrypt (HTTP 403); Newshub's report, which now redirects to a Stuff page that returned only its headline; and other outlets seen only in search summaries. The spokesperson's words are as relayed by three outlets, not read in the original.

## Corrections

If you have The Guardian's report, Pak'nSave's statement, or the date the ingredient check was added, tell us and we will fix this page.
