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
**Search Console: Blocked for our site.** Chrome tools worked, and the signed-in Search Console showed one property, `https://campfyrr.vercel.app/` (Overview: 0 clicks, "Processing data, please check again in a day or so"). That is not `agent-kb-autopublish.vercel.app`, so nothing from it was recorded as our data. `inbox/` is empty. No search data recorded, no changes made.

**Public checks, 2026-10-20 (curl):**
| Check | Result |
|---|---|
| `/`, `/goals/conversation-leadership/`, `/answer-and-go-conversation/` | All return 200 |
| H1 count | Home: 2. Goal page: 1. `/answer-and-go-conversation/`: 1 (it was 2 on 2026-10-19) |
| `sitemap-0.xml` | 1,592 `<loc>` entries (1,553 on 2026-10-19) |

**Action:** none. Not checked: titles, meta descriptions, and whether the home page's second H1 is intended.
