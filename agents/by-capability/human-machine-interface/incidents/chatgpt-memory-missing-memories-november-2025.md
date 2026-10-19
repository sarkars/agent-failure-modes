---
title: "ChatGPT Users Report Missing Memories; OpenAI Status Page Logs a Memory Incident"
date: 2025-11-07
source: "https://status.openai.com/incidents/01K9D7DASB76TK1DEGPMG6ZAM4"
summary: "OpenAI's status page shows an incident titled Issues with ChatGPT Memory from Nov. 6 to Nov. 7, 2025, with partial recovery of memories for a subset of users and possible gaps for memories created during the incident window."
categories:
  - Accuracy
patterns:
  - no-warning-of-context-loss
---

OpenAI's status page lists an incident, "Issues with ChatGPT Memory", that began on November 6, 2025 at 6:38 PM with "an issue related to missing ChatGPT memories". Updates on November 7 say there was "partial recovery of ChatGPT Memories for a subset of impacted users", that users who created new memories during the incident window "may still see gaps", and that the root cause was identified and a fix was rolling out. The incident was marked resolved on November 7, 2025 at 4:47 PM. The page does not say how many users were affected or what caused it.

**Pattern match:** [No warning of context loss](/no-warning-of-context-loss/) is about an assistant that loses what the user told it without saying so. This case is a service incident that removed stored memories, reported on a status page. The page I opened does not say whether users were told inside the product, so it is an adjacent case, not a direct match.

**The fix:** tell the user in the product what was lost, what was kept, and how to restore it, not only on a status page.
