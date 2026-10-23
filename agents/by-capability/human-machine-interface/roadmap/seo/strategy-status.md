# SEO strategy status (Part G)

Tracks the items in the site repo's SEO-STRATEGY.md. One item per run; Done only after build and live check.

| Item | Status |
|---|---|
| G1 Waitlist page /waitlist/ | **Done** (live 200 on 2026-10-23, run 98). Built 2026-10-22 (run 80). |
| G2 Pillar guide: detect AI agent failures in production | **Done** (live 200 on 2026-10-23, run 98). Built 2026-10-22 (run 81, site commit ac4640127): /guides/ and /guides/detect-ai-agent-failures-in-production/. Spoke links from patterns back to the guide not added yet |
| G3 /security/ hub | **Done** (live 200 on 2026-10-23, run 98). Built 2026-10-22 (run 82, site commit 0db04e683): /security/ with grouped pattern links, 4 incident links and a 7-line checklist; |
| G4 Pillar guide: AI agent security failures | **Done** (live 200 on 2026-10-23, run 98). Built 2026-10-22 (run 83, site commit 1b0483a6b): /guides/ai-agent-security-failures/, sources OWASP LLM01 and LLM06 opened; |
| G5 Pillar guide: chatbot QA checklist | **Done** (live 200 on 2026-10-23, run 98). Built 2026-10-22 (run 84): /guides/chatbot-qa-checklist/, 12 checks each linked to a pattern, pass conditions labeled proposed; |
| G6 Pillar guide: evals vs production monitoring | **Done** (live 200 on 2026-10-23, run 98). Built 2026-10-22 (run 85, site commit 27bcd9e81): /guides/evals-vs-production-monitoring/, LangSmith, Langfuse and Braintrust docs opened via fetch summaries 2026-10-22; |
| G7 Original data post (counts from this library) | **Done** (live 200 on 2026-10-23, run 98). Built 2026-10-22 (run 86, site commit 2aa9e9d44): /guides/ai-agent-failure-patterns-by-the-numbers/, counts from the site's own pattern files (1,572 patterns; category and frequency-label tables), no outside statistics; |
| G8 Compare pages (Langfuse, LangSmith, Braintrust, Promptfoo/Garak, Lakera/Guardrails AI) | **Done** (live 200 on 2026-10-23, run 98). Built (all five vendors covered): Langfuse vs LangSmith built 2026-10-22 (run 87, site commit 0ba93d191), vendor docs opened via fetch summaries; Braintrust vs Langfuse built 2026-10-22 (run 88, site commit 0490040d6), Braintrust docs opened via fetch summaries; Promptfoo vs Garak built 2026-10-22 (run 89, site commit c91dff057), Promptfoo red-team page and Garak GitHub README opened via fetch summaries; Lakera Guard vs Guardrails AI built 2026-10-22 (run 90, site commit 5f4af6403), Lakera quickstart, Guardrails AI docs home, GitHub README and on_fail guide opened via fetch summaries; |

**Live check, 2026-10-22 17:50 UTC (run 91):** all twelve G1-G8 URLs return 404 on https://agent-kb-autopublish.vercel.app/. The live home page was last modified 07:49 UTC, and the site commits pushed after it (from ac4640127 on) show no Vercel status on GitHub. None is marked Done. Waiting for the owner to check why Vercel is not building pushes to main.

**Live check, 2026-10-23 (run 98):** all twelve G1-G8 URLs return 200 on https://agent-kb-autopublish.vercel.app/ (/, /waitlist/, /guides/, the five guide pages, /security/ and the four compare pages). G1-G8 marked Done. Weekly repeat (one new guide or compare page) is next due once 7 days pass with none done, so not before 2026-10-29.
