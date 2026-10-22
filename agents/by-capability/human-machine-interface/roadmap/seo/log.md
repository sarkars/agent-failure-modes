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
