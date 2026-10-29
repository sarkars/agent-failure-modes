# SEO log

*(The daily review appends an entry here: UTC date, data source, range, opportunities, changes, proposals.)*

## 2026-10-18 (UTC): Blocked
No Search Console access today: no Chrome tools in the session and no export in `inbox/`. Public site checks could not run because the session cannot reach external hosts. No data was recorded and no changes were made.

## 2026-10-18 (UTC), run 2
Still blocked: no Search Console access (no Chrome tools, empty `inbox/`) and no external network. Nothing recorded.

## 2026-10-19 (UTC), manual run 10
**Search Console: Blocked.** No Chrome tools in the session and `inbox/` is empty. No search data recorded.

**Public checks (network now works), 2026-10-19:**
| Check | Result |
|---|---|
| Home, `/goals/conversation-leadership/`, `/answer-and-go-conversation/`, `/hollow-empathy/` | All return 200 and have a title and a meta description of 154 to 155 characters |
| H1 count | Goal page: 1. The two HMI pattern pages checked: **2 identical H1s**. A non-HMI pattern (`/sycophancy/`): 1 |
| Body text | The HMI pattern page shows the SEO comment text (`description:`, `search phrases:` and the list) as visible text |
| `sitemap-0.xml` | 1,553 URLs. Includes the 14 HMI patterns; includes none of the three new human-handoff patterns (not yet merged) and no solutions page |

**Cause (read in the site repo, not changed):** the site repo's committed copy of the HMI pattern pages is an older import (`frequency: "Occasional"`, `source:` path from before the move). It predates the current files, so the comment block leaks and the H1 repeats.

**Action:** none inside this folder can fix it. Written up as [proposal 1](../merge-proposals.md) for the site repo (re-run the importers and redeploy). Impact: the 14 live HMI pages show raw SEO text and a duplicate H1 until that is done, which affects how Google reads them.

## 2026-10-20 (UTC), scheduled run 22
**Correction, same day:** the property dropdown does list `https://agent-kb-autopublish.vercel.app/`; the first look only saw the property that was open. Last 28 days (Performance, read in Chrome): 16 clicks, 4.94K impressions, average CTR 0.3%, average position 9. Top pages by clicks: safety-filter-bypass 2 clicks / 43 impressions; canned-response-context-mismatch 2 / 6; patterns/ 1 / 1,800; conflicting-instructions 1 / 65; background-interference 1 / 50. 553 pages have data. Queries tab and HMI-only pages not read yet.

**Earlier note (wrong): Search Console: Blocked for our site.** Chrome tools worked, and the signed-in Search Console showed one property, `https://campfyrr.vercel.app/` (Overview: 0 clicks, "Processing data, please check again in a day or so"). That is not `agent-kb-autopublish.vercel.app`, so nothing from it was recorded as our data. `inbox/` is empty. No search data recorded, no changes made.

**Public checks, 2026-10-20 (curl):**
| Check | Result |
|---|---|
| `/`, `/goals/conversation-leadership/`, `/answer-and-go-conversation/` | All return 200 |
| H1 count | Home: 2. Goal page: 1. `/answer-and-go-conversation/`: 1 (it was 2 on 2026-10-19) |
| `sitemap-0.xml` | 1,592 `<loc>` entries (1,553 on 2026-10-19) |

**Action:** none. Not checked: titles, meta descriptions, and whether the home page's second H1 is intended.

## 2026-10-21 (UTC), scheduled run 45
**Source:** Search Console, read in Chrome (property `https://agent-kb-autopublish.vercel.app/`). Last 28 days (Sep 21 to Oct 18, 2026): 15 clicks, 4.98K impressions, average CTR 0.3%, average position 9.1. 131 queries and 567 pages with impressions. Top 10 only read (not the top 25).

**Top queries (all 0 clicks; impressions):** a long "context failure detection strategy ... same query twice" question 75 (and 14 for the same without "?"); "what are the signs that an ai agent is following your style guide correctly vs. just pattern-matching your prompts?" 48; "de-identified patient samples" 18; "automated litigation support" 17; "factor crowding risk" 16; "deterministic tool calling with sql" 16; "semantic mismatch" 15; "what steps do agents take when an ai underwriting platform assigns the wrong business class code?" 10; one quoted query about "vpc seller timing bad-state handoff" 9.

**Top pages (clicks / impressions):** canned-response-context-mismatch 2 / 6; patterns/ 1 / 1,792; conflicting-instructions 1 / 67; background-interference 1 / 52; safety-filter-bypass 1 / 39; memory-fragmentation-allocation-failure 1 / 20; perspective-distortion-misunderstanding 1 / 17; resource-exhaustion 1 / 8; apr-calculation-errors 1 / 8; ssml-markup-failures 1 / 8. No HMI chat pattern is in the top 10.

**Opportunities:** none acted on. The top queries point at older pages outside the HMI folder (agent context, style-guide and underwriting topics), so any title change is a proposal for a person. Indexing report not read this run. Not checked: positions per query.

**Action:** none. No changes made; no merge proposal added.

## 2026-10-22 (UTC), scheduled run 68
**Source:** Search Console, read in Chrome (property `https://agent-kb-autopublish.vercel.app/`). Last 28 days (Sep 22 to Oct 19, 2026): 16 clicks, 5.01K impressions, average CTR 0.3%, average position 9.3. 129 queries with impressions. Top 10 queries only read; the Pages tab was not opened this run.

**Top queries (all 0 clicks; impressions):** a long "context failure detection strategy ... same query twice" question 81 (15 more without "?"); "what are the signs that an ai agent is following your style guide correctly vs. just pattern-matching your prompts?" 48; "de-identified patient samples" 18; "semantic mismatch" 17; "automated litigation support" 17; "factor crowding risk" 16; "deterministic tool calling with sql" 16; an underwriting business-class-code question 9; an AI bot scraping runbook query 8.

**Opportunities:** none acted on. Every top query points at older pages outside the HMI folder, so any title change is a proposal for a person. No HMI chat pattern appears in the top 10. Not checked: positions per query, indexing report.

**Action:** none. No changes made; no merge proposal added.

## 2026-10-23 (UTC), scheduled run 94
**Source:** Search Console, read in Chrome (property `https://agent-kb-autopublish.vercel.app/`). Last 28 days (Sep 23 to Oct 20, 2026): 15 clicks, 5.07K impressions, average CTR 0.3%, average position 9.3. 131 queries with impressions. Top 10 queries read; the Pages tab was not opened. Page indexing report also read: 878 indexed, 13 not indexed, all for one reason, "Not found (404)", first detected 8/18/26.

**Top queries (all 0 clicks; impressions):** the long "context failure detection strategy ... same query twice" question 88 (17 more without "?"); "what are the signs that an ai agent is following your style guide correctly vs. just pattern-matching your prompts?" 48; "semantic mismatch" 18; "de-identified patient samples" 18; "automated litigation support" 17; "factor crowding risk" 16; "deterministic tool calling with sql" 15; an underwriting business-class-code question 9; an AI bot scraping runbook query 8.

**Opportunities:**
- **Not indexed (acted on):** the 10 example 404 URLs shown are all of the form `/<page>/<sibling>.md`, for example `/policy-consistency-violation/policy-version-mismatch.md` (last crawled Sep 27, 2026). Pattern sources link siblings as `./slug.md`, and the site served those links unchanged, so they resolved under the current page and 404ed. Every target checked (six) exists as a page at `/<slug>/`. Part F fix in the site repo: a remark plugin rewrites `./slug.md` links to `/slug/` (or `/incidents/slug/`) when the page exists. After the build, 6 such links remain because their targets have no page; those are left for a person. After deploy, a person can press "Validate fix" on the 404 report.
- Queries: none acted on. Every top query points at older pages outside the HMI folder, so any title change is a proposal for a person. No HMI chat pattern appears in the top 10.

**Action:** site repo commit a7938e13b (Part F). No content page changed; no merge proposal added.

## 2026-10-24 (UTC), scheduled run 118
**Source:** Search Console, read in Chrome (property `https://agent-kb-autopublish.vercel.app/`). Report default range, about three months (chart runs Jul 23 to Oct 21, 2026): 24 clicks, 9.42K impressions, average CTR 0.3%, average position 16.2. 309 queries with impressions. Top 10 queries and the top pages list read from the screen. Page indexing report read: 878 indexed, 13 not indexed, one reason, "Not found (404)", validation "Started" (a person pressed Validate fix after the run 94 link fix).

**Top queries (all 0 clicks; impressions):** the long "context failure detection strategy ... same query twice" question 101; "vpc seller timing bad-state handoff" in three spellings 71, 61 and 31; "de-identified patient samples" 55; the "style guide vs. pattern-matching your prompts" question 48; "voice agent conversation flow adherence" 29; "automatic approval review timed out while evaluating the requested approval" 28; "insecure output handling" 26; "de-identified clinical samples" 25.

**Top pages (CTR and position read; click and impression cells were not exposed to the reader, so not recorded):** /safety-filter-bypass/ (4.1%, 9.9), /canned-response-context-mismatch/ (28.6%, 11.0), /patterns/ (position 6.9), /conflicting-instructions/ (1.1%, 5.5), /factor-crowding-blindness/ (1.7%, 6.8), /background-interference/ (1.9%, 5.1). One HMI pattern is in the top 15: /difficult-customers/failures/mishandled-abuse.md (10%, 4.4); that old `.md` URL returns 308 and /mishandled-abuse/ returns 200, checked 2026-10-24.

**Opportunities:**
- Near page one: /safety-filter-bypass/ (9.9) and /canned-response-context-mismatch/ (11.0) are outside the HMI folder; no proposal written, since the impression counts behind them were not read.
- Query with no matching page: "voice agent conversation flow adherence" (29). Voice work waits for its own phase (Channel scope), so no queue row added.
- Not indexed: the 13 404s are already in validation; nothing more to do until Google finishes.

**Action:** none. No content page changed; no merge proposal added.

## 2026-10-24 (UTC), on request in a working session
**Source:** Search Console, read in Chrome (property `https://agent-kb-autopublish.vercel.app/`). Last 28 days (Sep 25 to Oct 22, 2026): 18 clicks, 5.61K impressions, average CTR 0.3%, average position 9.2. 200 queries and 677 pages with impressions. Top 26 queries and top 18 pages by impressions read from the table, with CTR and position. Page indexing: 878 indexed, 13 not indexed, "Not found (404)", validation still "Started".

**Top queries (all 0 clicks; impressions, position):** the "context failure detection strategy ... same query twice" question 99 (9.4), plus 16 without "?" (9.5); the "style guide vs. pattern-matching your prompts" question 48 (10.0); "semantic mismatch" 18 (7.8); "de-identified patient samples" 18 (64.9); "automated litigation support" 18 (74.4); "factor crowding risk" 16 (6.5); "deterministic tool calling with sql" 15 (43.5); the underwriting business-class-code question 10 (6.2); "ai documentation completeness" 10 (85.0); "automatic approval review timed out while evaluating the requested approval" 7 (6.7) and 7 with a period (7.9); "stale state" 4 (1.0).

**Top pages by impressions (clicks, impressions, CTR, position):** /patterns/ 1, 1,718, 0.1%, 6.9; /difficult-customers/failures/mishandled-abuse.md 1, 158, 0.6%, 5.0; /approval-timeout-mishandling/ 0, 97, 0%, 7.0; /mishandled-abuse/ 0, 95, 0%, 4.9; /stale-state-use/ 0, 77, 0%, 7.9; /chunk-boundary/ 0, 65, 0%, 6.9; /semantic-mismatch/ 0, 65, 0%, 9.6; /goals/voice-synthesis/ 0, 57, 0%, 9.6; /conflicting-instructions/ 1, 56, 1.8%, 5.3; /multi-agent-false-consensus-risk/ 0, 56, 0%, 6.9.

**Opportunities:**
- **Low click-through:** /patterns/ has 1,718 impressions at position 6.9 but CTR 0.1% (site 0.3%). Its title is "Agent Failure Patterns | Good Agent Lab" and its description is 84 characters. Site repo page, so proposal 5 in merge-proposals.md.
- **Near page one:** /semantic-mismatch/ (position 9.6; query "semantic mismatch" at 7.8) has a generic title. Older pattern outside the HMI folder, so proposal 6.
- **HMI page:** mishandled-abuse gets 253 impressions across its old `.md` URL (308 to the new one, checked today) and /mishandled-abuse/ at position about 5, with 1 click. Its title and description were already rewritten for search; no change. Google should merge the old URL over time.
- **Not indexed:** the 13 404s are still in validation. Nothing to do.
- **Query with no matching page:** none new that fits the chat-first scope.

**Action:** proposals 5 and 6 added to merge-proposals.md. No page changed.

## 2026-10-25 (UTC), scheduled run 139
**Source:** Search Console, read in Chrome (property `https://agent-kb-autopublish.vercel.app/`). Last 28 days (Sep 26 to Oct 23, 2026): 24 clicks, 6.08K impressions, average CTR 0.4%, average position 8.9. 255 queries with impressions. Top 10 queries read as text; top 6 pages read from the Pages tab on screen (clicks and impressions only). Page indexing report not opened this run.

**Top queries (all 0 clicks; impressions):** the "context failure detection strategy ... same query twice" question 107 (17 more without "?"); the "style guide vs. pattern-matching your prompts" question 48; "semantic mismatch" 18; "de-identified patient samples" 18; "automated litigation support" 18; "factor crowding risk" 16; "deterministic tool calling with sql" 15; "ai documentation completeness" 11; a German profanity query 10.

**Top pages by clicks (clicks, impressions):** /accusatory-or-harsh-refusals/ 2, 27; /canned-response-context-mismatch/ 2, 6; /patterns/ 1, 1,598; /difficult-customers/failures/mishandled-abuse.md 1, 339; /background-interference/ 1, 54; /conflicting-instructions/ 1, 52.

**Opportunities:**
- **HMI page earning clicks:** /accusatory-or-harsh-refusals/ (HMI, refusals-and-boundaries) got 2 clicks from 27 impressions. Its title and description were already rewritten for search; no change.
- **Low click-through:** /patterns/ 1,598 impressions, 1 click. Already covered by merge proposal 5 and Part G item G9 (built; the live page is still the old one, title "Agent Failure Patterns | Good Agent Lab", checked today).
- **Old URL:** /difficult-customers/failures/mishandled-abuse.md still collects impressions (339); it returns 308 to /mishandled-abuse/ (checked run 118). Nothing to do.
- **Query with no matching page:** none new that fits the chat-first scope. The profanity query is not a topic to target.

**Action:** none. No content page changed; no merge proposal added.

## 2026-10-26 (UTC), scheduled run 145
**Source:** Search Console, read in Chrome (property `https://agent-kb-autopublish.vercel.app/`). Default range shown, last 3 months (Jul 24 to Oct 23, 2026): 31 clicks, 10.8K impressions, average CTR 0.3%, average position 15. 430 queries with impressions. Top 10 queries read as text; top 6 pages read from the Pages tab on screen (clicks and impressions only). Page indexing report not opened this run. The range differs from run 139 (28 days), so the totals are not comparable.

**Top queries (all 0 clicks; impressions):** the "context failure detection strategy ... same query twice" question 119; three variants of "vpc seller timing bad-state handoff" 71, 61 and 31; "de-identified patient samples" 55; the "style guide vs. pattern-matching your prompts" question 48; "voice agent conversation flow adherence" 29; "automatic approval review timed out while evaluating the requested approval" 28; "insecure output handling" 26; "de-identified clinical samples" 25.

**Top pages by clicks (clicks, impressions):** /safety-filter-bypass/ 2, 50; /accusatory-or-harsh-refusals/ 2, 27; /canned-response-context-mismatch/ 2, 7; /patterns/ 1, 2,209; /difficult-customers/failures/mishandled-abuse.md 1, 339; /conflicting-instructions/ 1, 95.

**Opportunities:**
- **Low click-through:** /patterns/ 2,209 impressions, 1 click. Already covered by merge proposal 5 and Part G item G9 (built; the live page still has the old title "Agent Failure Patterns | Good Agent Lab", checked today).
- **New page with clicks:** /safety-filter-bypass/ is outside the HMI folder (vision-and-images); no edit here.
- **Odd query:** the "vpc seller timing bad-state handoff" variants look like automated or operator-prefixed queries; not a topic to target.
- **Query with no matching page:** "voice agent conversation flow adherence" is voice, out of the chat-first scope for now.

**Action:** none. No content page changed; no merge proposal added.

## 2026-10-27 (UTC), scheduled run 174
**Source:** Search Console, read in Chrome (property `https://agent-kb-autopublish.vercel.app/`). Last 28 days (Sep 27 to Oct 24, 2026): 28 clicks, 6.71K impressions, average CTR 0.4%, average position 8.8. 327 queries and 745 pages with impressions. Top 10 queries read as text; top 50 pages read from the Pages tab, sorted by impressions. Page indexing report not opened this run.

**Top queries (all 0 clicks; impressions):** the "context failure detection strategy ... same query twice" question 110 (18 more without "?"); the "style guide vs. pattern-matching your prompts" question 48; "semantic mismatch" 19; "automated litigation support" 19; "de-identified patient samples" 18; a German profanity query 17; "factor crowding risk" 14; "deterministic tool calling with sql" 13; "ai documentation completeness" 12.

**Top pages by impressions (clicks, impressions):** /patterns/ 1, 1,511; /difficult-customers/failures/mishandled-abuse.md 1, 400; /mirroring-hostility/ 0, 390; /mishandled-abuse/ 0, 335; /stale-state-use/ 0, 77; /approval-timeout-mishandling/ 0, 74; /semantic-mismatch/ 0, 71; /chunk-boundary/ 0, 66. Pages with clicks: /accusatory-or-harsh-refusals/ 2, 43; /character-confusion/ 2, 13; /canned-response-context-mismatch/ 2, 6.

**Opportunities:**
- **HMI pages with impressions and no clicks:** /mirroring-hostility/ (390) and /mishandled-abuse/ (335) already carry search-phrase titles; no change.
- **Generic titles on high-impression pages:** handled by Part G item G10, batch 1 (10 pages retitled in the site repo; see `strategy-status.md`). Merge proposal 6 (semantic-mismatch) done by G10.
- **/patterns/:** live page now has the G9 title; CTR 1 click from 1,511 impressions; re-check after a few weeks of data.
- **Question queries:** the two long questions are G12 work (short answers), next after G10.

**Action:** no HMI content page changed. Site repo: G10 batch 1 (10 non-HMI pattern pages retitled, built, committed).

## 2026-10-28 (UTC), scheduled run 198
**Source:** Search Console, read in Chrome (property `https://agent-kb-autopublish.vercel.app/`). Last 28 days (Sep 28 to Oct 25, 2026): 32 clicks, 7.37K impressions, average CTR 0.4%, average position 8.7. 393 queries and 775 pages with impressions. Top 10 queries read as text; top 100 pages read from the Pages tab, sorted by impressions (clicks and impressions only; position per page not read). Page indexing report not opened this run.

**Top queries (all 0 clicks; impressions):** the "context failure detection strategy ... same query twice" question 112 (17 more without "?"); the "style guide vs. pattern-matching your prompts" question 48; "semantic mismatch" 21; "automated litigation support" 21; "de-identified patient samples" 18; "factor crowding risk" 14; "deterministic tool calling with sql" 14; two profanity queries (German 21, Arabic 14).

**Top pages by impressions (clicks, impressions):** /patterns/ 1, 1,447; /mirroring-hostility/ 0, 607; /mishandled-abuse/ 1, 537; /difficult-customers/failures/mishandled-abuse.md 1, 400; /profanity-and-slang-handling/ 0, 86; /stale-state-use/ 0, 78; /approval-timeout-mishandling/ 0, 73; /semantic-mismatch/ 0, 71; /chunk-boundary/ 0, 68; /silent-failure-and-timeout/ 1, 64. Pages with 2 clicks: /accusatory-or-harsh-refusals/ (56 impressions), /character-confusion/ (14), /canned-response-context-mismatch/ (6).

**Opportunities:**
- **HMI pages with impressions and few clicks:** /mirroring-hostility/ (607, up from 390 on 2026-10-27's read) and /mishandled-abuse/ (537, 1 click). Both already carry search-phrase titles; their queries were not read per page, so no rewrite without the query data.
- **Generic titles in the top 30 by impressions:** none left. Every top-30 pattern page now has a search-phrase title in the site source (G10 batches 1 and 2 plus earlier pattern titles); the batch 1 and 2 titles are not live yet (Vercel has not built since c69c78cdd).
- **Question queries:** the two long questions stay G12 work (short answers).
- **Profanity queries:** they land on /profanity-and-slang-handling/ and /mirroring-hostility/, which match the topic; no action.

**Action:** none. No content page changed; no merge proposal added.

## 2026-10-29 (UTC), scheduled run 220
**Source:** Search Console, read in Chrome (property `https://agent-kb-autopublish.vercel.app/`). Last 28 days (chart Sep 29 to Oct 26, 2026): 38 clicks, 7.92K impressions, average CTR 0.5%, average position 8.6. 455 queries and 813 pages with impressions. Top 10 queries and top 10 pages read as text, in the report's default order (sorted by clicks); pages sorted by impressions were not read this run. Page indexing report not opened.

**Top queries (all 0 clicks; impressions):** the "context failure detection strategy ... same query twice" question 103 (17 more without "?"); the "style guide vs. pattern-matching your prompts" question 26; "semantic mismatch" 24; "automated litigation support" 21; "de-identified patient samples" 19; "factor crowding risk" 14; "deterministic tool calling with sql" 14; two profanity queries (German 21, Arabic 15).

**Top pages by clicks (clicks, impressions):** /character-confusion/ 3, 17; /mishandled-abuse/ 2, 737; /silent-failure-and-timeout/ 2, 78; /accusatory-or-harsh-refusals/ 2, 56; /canned-response-context-mismatch/ 2, 6; /difficult-customers/failures/mishandled-abuse.md 1, 400; /silent-sandbagging/ 1, 63; /background-interference/ 1, 51; /conflicting-instructions/ 1, 48; /safety-filter-bypass/ 1, 35.

**Opportunities:**
- **/mishandled-abuse/:** 737 impressions (537 on 2026-10-28's read) and 2 clicks; the .md copy of the same page adds 400. Its queries were not read per page, so no title rewrite without the query data.
- **Question queries:** the two long questions stay G12 work (short answers).
- **Profanity queries:** no action (they land on matching pages).

**Action:** none. No content page changed; no merge proposal added.
