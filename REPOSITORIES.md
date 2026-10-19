# Which Repository Holds What

**Two repositories make up this project. This one holds the words. The other one holds the website that publishes them.** If a change is about what the library says, it goes here. If it is about how the site looks, routes, or builds, it goes there.

| | **Content repo** (this repo) | **Site repo** |
|---|---|---|
| Name | `sarkars/agent-failure-modes` | `sarkars/agent-kb-autopublish` |
| Job | The library: failure patterns, solution pages, plans, checks | The Astro website and the code that publishes the library |
| Format | Markdown only (plus a few Python check scripts) | Astro, Python import scripts, Vercel config |
| Live at | GitHub (readers can browse it) | agent-kb-autopublish.vercel.app |
| Who writes to it | You, and the scheduled hourly run | You; the scheduled run only reads it |

## Content repo: put these here
- Failure patterns and the goal and category folders (`agents/by-use-case`, `by-capability`, `cross-cutting`), including the human-machine-interface (HMI) library under `agents/by-capability/human-machine-interface/`.
- Solution pages in `agents/solutions/` (for example `chat-use-cases.md`) and agent pages in `agents/by-agent/`.
- The HMI roadmap, catalog, execution plan, content program, tests, incident drafts, glossary, symptom pages, and the SEO log (`agents/by-capability/human-machine-interface/roadmap/seo/`).
- Page titles, summaries, SEO comment blocks, and internal links inside those Markdown files.
- The guard scripts in `roadmap/tools/` and the frozen list of public URLs (`public-urls.tsv`).

## Site repo: put these here
- Page templates, layouts, styles, navigation, and search.
- The importers (`scripts/import_patterns.py`, `scripts/import_taxonomy_readmes.py`) that read this repo and build site pages.
- Sitemap, structured data, robots rules, redirects (`vercel.json`), analytics, and the newsletter and compare pages.
- Published incident pages (`website-astro/src/content/incidents/`). Drafts live here in `incidents/`; a person copies an approved one to the site.
- Anything that makes `agents/solutions/` or `agents/by-agent/` appear on the site. Today the importer reads only files under a `failures/` path.

## Where a change goes: quick test
| If you want to... | Repo |
|---|---|
| Write or fix a pattern, solution page, or plan | Content |
| Change a page title or summary shown in search | Content (the pattern file), unless the template builds it |
| Change how pages look, link to each other, or are numbered | Site |
| Publish a new kind of page (solutions, agents) | Both: the pages here, the importer change there |
| Add or change a redirect | Site (`vercel.json`) |
| Keep a public URL stable | Both: do not rename files here; the importer decides the URL there |
| Record search data and SEO decisions | Content (`roadmap/seo/log.md`) |

## Rules for the scheduled run
1. It writes only under `agents/by-capability/human-machine-interface/` and `agents/solutions/` in the content repo.
2. It never edits the site repo. It reads that repo to check which incidents exist and how the importer works.
3. A change that needs the site repo goes into `roadmap/merge-proposals.md` in this repo, as a proposal with the file and the reason. A person makes the change there.
4. Existing public URLs never change (`check_public_urls.py` enforces this).
5. It opens no pull requests.

## Order for a change that touches both
1. Write the pages here and make the checks pass.
2. Describe the site change as a proposal here.
3. Make the site change in the site repo, then build and compare the page list before merging.
4. Merge the content change first, then the site change, so the site never links to a page that doesn't exist.
