# Deploy: Merge to `main`, Then Publish to the Website

**Every run ends by publishing what it wrote.** First the content repo's branch is merged into `main`. Then the new and changed human-machine-interface pages are copied into the site repo, checked with a full build, and pushed so the website deploys. This page is the runbook. It was written on 2026-10-19 after the first manual deploy (site commit `99d2fa6`).

## Scope and limits
- **Content repo (`sarkars/agent-failure-modes`):** merge the run's branch into `main` with a pull request. Never force-push `main`.
- **Site repo (`sarkars/agent-kb-autopublish`):** only touch `website-astro/src/content/patterns/`, `goals/`, and `categories/`, and only for pages whose `source:` path contains `human-machine-interface`. Never change templates, config, redirects, other patterns, or the Hugo `website/` folder.
- **Never delete or rename** any page already on the live site. If a build or check below fails, stop and do not push.

## Steps
1. **Finish the run's commits** on the branch and make sure the five checks in the execution plan pass.
2. **Merge to `main`.** Open a pull request from the run's branch into `main` (base `main`), then merge it with a merge commit, with the expected head SHA set. Use the GitHub tools. If the merge is blocked, record why in the Run log and stop before step 3.
3. **Reset the branch.** `git fetch origin main` then `git checkout -B <branch> origin/main`, so the next run starts from the merged history.
4. **Make a scratch copy of the site repo.** Copy `/home/user/agent-kb-autopublish` to a scratch folder next to a link named `agent-failure-modes` that points at the content repo checkout (the importers expect that sibling layout). Run `python3 -I scripts/import_patterns.py` and `python3 -I scripts/import_taxonomy_readmes.py` there. They write Hugo-format files into `website/content/`.
5. **Select only the human-machine-interface pages.** From `website/content/*.md`, take files whose front matter has `source:` containing `human-machine-interface`. Copy them to `website-astro/src/content/patterns/`. For each goal they list (lowercased, spaces to hyphens), copy `website/content/goals/<goal>/_index.md` to `website-astro/src/content/goals/<goal>/_index.md`. Copy the `human-machine-interface` category term page the same way.
6. **Build.** In `website-astro`, run `npm install` then `npm run build`. The build must finish with no errors.
7. **Check no URL is lost.** Fetch the live `sitemap-0.xml` from `https://agent-kb-autopublish.vercel.app/`. Every URL in it must exist in the new build's `dist/` as `<path>/index.html`. Any missing URL means stop. Also confirm a sample HMI page has exactly one `<h1>` and no visible `search phrases:` text.
8. **Apply to the real site repo.** Copy the same files from the scratch copy into `/home/user/agent-kb-autopublish/website-astro/src/content/`, `git add website-astro/src/content`, commit with the attribution lines, and `git push origin HEAD:main`. Before pushing, run `git fetch origin main`; if `main` has moved, rebase or redo steps 4 to 8 on the new `main`.
8b. **Trigger the Vercel build if a hook is configured.** If the environment variable `VERCEL_DEPLOY_HOOK_URL` is set, send one `POST` to it with `curl -sS -X POST "$VERCEL_DEPLOY_HOOK_URL"` (never print the URL). If it is not set, rely on Vercel's own build on push.
9. **Confirm the deploy.** Vercel builds on push. After a few minutes, fetch one new page on the live site (for example `/<newest-pattern-slug>/`) and check it returns 200. If it does not after 15 minutes, record that in the Run log. Do not push again to "retry".
10. **Record it.** Add a Deploy line to the run's Run log entry: the content-repo merge commit, the site-repo commit, the build page count, the URLs added and removed (removed must be zero), and the live check result.

## Notes
- The Hugo importer stamps each page with a date. Existing pages keep their dates because the importer reuses them; new pages get the run date.
- The site's sitemap host in a local build shows `localhost`; compare paths only.
- **Known gap (2026-10-19).** The first publish, site commit `99d2fa6`, was pushed to the site repo's `main` and the live site had not changed 15 minutes later: GitHub shows no deployment or status for it, and the live site's last build is from 2026-10-16. Earlier site commits were authored from the owner's computer. Whether Vercel builds on push for commits authored by this session is unconfirmed. Until the owner confirms, step 9 may report "not deployed", and that is not a reason to push again.
- `agents/solutions/`, `agents/by-agent/`, and the incident drafts in `incidents/` are not published by this runbook. See proposals 3 and 4 in [merge-proposals.md](merge-proposals.md).
