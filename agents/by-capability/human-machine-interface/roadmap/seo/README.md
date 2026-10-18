# SEO Log: Daily Search Console Review

> **What this is.** Once per UTC day, a scheduled run reviews the search terms people use to reach the site, and turns them into content decisions. This folder holds the log and the rules. It is Markdown only.

## Why
Rankings are the distribution plan. The site's search terms show which problems people search for, which pages get impressions without clicks, and which pages Google does not index. Each review feeds the pattern queue and the SEO fixes.

## The daily review (workstream 15)
1. **Get the data, in this order. Use the first that works.**
   1. **Chrome browser.** If Claude in Chrome tools are available in the session, open Google Search Console for the property `agent-kb-autopublish.vercel.app` in the user's signed-in Chrome. Open Performance, search results. Set the range to the last 28 days, then read: top queries, top pages, and the queries table filtered to pages under `/goals/`, `/categories/`, and the human-machine-interface patterns. Also open Pages (indexing) and note pages "Crawled, currently not indexed" and "Discovered, currently not indexed".
   2. **Export in the repo.** If Chrome is not available, look for a person's export in `seo/inbox/` (CSV or pasted Markdown from the Performance report). Read the newest file.
   3. **Neither.** Write "Blocked: no Search Console access today" in the log and do the public checks below. Do not estimate or invent search data.
2. **Record only what you read.** Copy the date range, the top 25 queries (clicks, impressions, CTR, average position), and the top 25 pages. Mark each number as read from the screen or export. Never fill in a missing number.
3. **Find the opportunities**, each with the numbers behind it:
   - **Near page one:** queries with average position 8 to 20 and real impressions. Action: strengthen that page's title, H1, summary, and internal links.
   - **Low click-through:** queries with high impressions and CTR well below the site's own median. Action: rewrite the title and meta description.
   - **Query with no matching page:** a query people use that no page answers. Action: add a catalog row or a pattern to the queue, with the query as evidence.
   - **Not indexed:** pages Google found but did not index. Action: check thin content, duplicates, and internal links.
4. **Act inside the allowed scope.** Edit HMI pages and `agents/solutions/` pages directly (titles, H1s, summaries, SEO comment blocks, internal links, new catalog rows). For pages outside those folders, write a proposal in `roadmap/merge-proposals.md`. Never change a public URL.
5. **Log it.** Append an entry to `seo/log.md`: UTC date, data source used, range, the opportunities found, what was changed, and what was left as a proposal. If a query was added to the queue, say which row.
6. **Check the guards,** then commit and push the SEO changes on their own commit.

## Public checks (when Search Console is not available)
- Fetch the live home page, a goal page, and two HMI pattern pages. Confirm each loads, has one H1, a title, and a meta description.
- Fetch `sitemap-index.xml` and confirm it lists the newly merged HMI pages.
- Record what you saw. These checks do not replace Search Console data.

## Rules
- Search data is a source, not a target. Do not stuff queries into pages. Write for the person with the problem.
- Do not put personal data from Search Console into the repo. Queries are aggregate; skip any that look like a person's name or contact details.
- A change made because of a query is recorded with the query and the number that justified it.
- If sign-in is needed, stop and ask. Never enter credentials.
