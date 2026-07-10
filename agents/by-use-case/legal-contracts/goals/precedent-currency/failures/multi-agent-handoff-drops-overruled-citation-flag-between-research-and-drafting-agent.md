# Multi-Agent Handoff Drops Overruled-Citation Flag Between Research and Drafting Agent

## Issue: A Legal-Research Agent That Identifies, in Its Own Analysis, That a Specific Case It Surfaced Has Been Overruled on the Exact Point It Was Going to Be Cited For Hands Off a Structured List of Candidate Citations to a Drafting Agent That Strips That Overruled-Status Context, So the Drafting Agent Cites the Case as If It Were Still Good Law

**Frequency**: Occasional

**Symptoms**
- The research agent's analysis explicitly notes that a candidate case was overruled or its holding limited on the relevant point, but the structured citation list it hands to the drafting agent contains only case name, citation, and a one-line summary of the original holding
- The drafting agent cites the case in the brief or memo as supporting authority, with no mention of its overruled status, because that status existed only in the research agent's narrative analysis, not the structured list
- Re-reading the research agent's full research transcript clearly shows the overruled status was identified and reasoned through; it simply never reached the structured citation-list field the drafting agent reads
- The gap concentrates on cases that remain good law for some holdings but were specifically overruled or limited on the narrower point being cited, since the structured list's brief summary field does not capture that nuance
- The error surfaces only when opposing counsel or a clerk flags the citation as overruled, since the drafted document otherwise reads as a well-supported, confidently cited argument

**Root Cause**
The research agent and the drafting agent communicate through a structured citation-list schema with fields for case name, citation, and a brief holding summary, but no dedicated field for current-validity status on the specific point cited. When the research agent's overruled-status determination is more specific than "still good law: yes/no" -- for example, overruled on one holding but not another -- that nuance exists only in the research agent's narrative analysis and is never mapped into a structured field the drafting agent's citation-insertion process actually reads.

**Example**
```
Research agent surfaces a case as a candidate citation for a proposition about contractual indemnification scope, and notes in its analysis: "This case's indemnification holding was overruled by a later appellate decision on the specific question of consequential damages, though its holding on attorney's fees remains good law"
Research agent's structured handoff to the drafting agent lists the case with citation and a brief summary: "Holds that indemnification clauses are construed narrowly" -- no validity-status field exists
Drafting agent inserts the citation into the brief to support an argument specifically about consequential damages exclusion, the exact point on which the case was overruled
Opposing counsel's response brief flags the citation as overruled on the cited point, undermining the argument's credibility before the court
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM systems exhibit a documented failure category where a determination established by one agent is lost or never reaches a downstream agent's effective input, distinct from either agent reasoning incorrectly on its own | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Evaluations of large language models in legal applications identify citation-validity propagation between research and drafting stages as a distinct reliability gap from citation-retrieval accuracy itself | [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267) |
| Retrieval-augmented legal research systems are shown to require structured, point-specific validity flags rather than a single binary good-law indicator to reliably support downstream drafting | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |

**Contributing Factors**
- The structured citation-list schema used for handoff has a single brief-summary field with no dedicated, point-specific validity-status field
- The drafting agent's citation-insertion process consults only the structured citation list, never the research agent's full analysis transcript
- No reconciliation step compares validity-status language in the research agent's analysis against what the structured citation list actually encodes before a citation is inserted

---

## Mitigation Strategies

### Prevention

1. **Point-specific validity-status field in citation-handoff schema with required population**: Extend citation-list schema to include: {case_id, citation, original_holding_summary, validity_status: {overall_status (GOOD_LAW|OVERRULED|LIMITED), point_specificity [{proposition: "string", validity_on_point: (GOOD_LAW|OVERRULED|LIMITED|NARROWED), overruling_authority: "cite", reasoning: "string"}], full_analysis_doc_id}}. Validation gate: if research_agent's_analysis contains validity-limitation language (e.g., "overruled on", "limited to", "narrowed by"), mandatory population of validity_status.point_specificity with all points identified. Fail-safe: citation-list rejected if overall_status != analysis_finding or if analysis mentions point-specific limitations not captured in point_specificity array. Root cause: Prevents point-specific validity nuance from being dropped at handoff.

2. **Pre-insertion citation-validity verification with point-matching**: Before drafting agent inserts citation to support specific proposition: (a) extract proposition being supported from draft text, (b) query citation-validity status against current Shepardizing/KeyCiting service, (c) check if cited case is overruled/limited on ANY point related to the proposition, (d) if validity_status from handoff shows GOOD_LAW but current citator shows OVERRULED or LIMITED, alert: "Research handoff may be stale; re-verify validity status", (e) if overruled/limited on cited point, block insertion and escalate to research agent for re-evaluation. Root cause: Ensures validity check happens at insertion time, not just at research time.

3. **Full-analysis linkage for point-specific-validity citations**: In structured citation-list, include full_analysis_doc_id (link to research agent's complete reasoning for that citation). Drafting agent's citation-insertion process: if validity_status.overall_status != GOOD_LAW, auto-fetch full_analysis_doc_id and display summary of reasoning to drafter: "Research found this case overruled on: [points]. See research memo section X for details." Drafter must explicitly confirm understanding and intentionality before citation is inserted. Root cause: Gives drafting agent visibility into limitations that structured fields alone cannot capture.

### Detection & Response

1. **Validity-status handoff audit logging with analysis-to-structure reconciliation**: For each citation research→drafting handoff, log: {citation_id, research_analysis_contains_validity_language (Y/N), validity_language_captured_in_schema (Y/N), validity_status_overall, validity_status_point_specificity_count, analysis_to_schema_reconciliation_status (MATCH|MISMATCH), timestamp}. Daily audit: sample 10% of handoffs, verify: (a) if analysis contains validity limitations, schema captures them, (b) if schema shows GOOD_LAW but analysis indicates limitations, flag as MISMATCH. Alert if: >5% have MISMATCH status, indicating systematic gap between analysis and structured fields.

2. **Citation-insertion validity verification and post-insertion citator check**: At insertion time, check validity_status from handoff. If not GOOD_LAW, require confirmation. After insertion, log for later verification. Before filing, run automated citator check: pass all citations through current Shepardizer/KeyCite/LexisNexis, verify each citation still valid on the specific point cited. Flag any citations now showing OVERRULED or LIMITED, block filing, and escalate to attorney for revision.

### Architecture Patterns

1. **Point-Specific Citation Validity Schema with Handoff Validation Engine**: Research agent generates citation list with detailed validity_status including per-point evaluations. Validation gate: NLP scan of research_analysis for validity keywords; if found, require point_specificity population. Handoff schema enforces completeness: missing point_specificity entries for findings in analysis trigger rejection. Drafting agent consumes schema and can access linked full_analysis for additional context.

2. **Pre-Insertion Validity Verification with Citator Integration**: Drafting agent, before inserting citation: checks validity_status from handoff, queries current citator service, compares results. If citator shows overruled/limited on cited point, blocks insertion. If handoff validity stale, alerts to research agent. Ensures citation validity verified at insertion time, not just at research time.

3. **Analysis-to-Schema Reconciliation Audit**: Post-research, before handoff to drafting, automated scan of research_analysis for validity-limiting language. For each limitation found, verify corresponding point_specificity entry in citation schema. Mismatches escalated to research agent for correction before handoff transmitted.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Validity-Status Population Completeness | 100% | <99% | # of citations with point_specificity array populated for all points identified in research analysis / total citations with point-specific limitations |
| Analysis-to-Schema Reconciliation Pass Rate | 100% | <99% | # of handoffs where validity-limiting language in analysis is captured in schema / total handoffs with validity-relevant research |
| Pre-Insertion Validity Verification Rate | 100% | <99% | # of citations verified for current validity status before insertion into draft / total citations inserted (those with non-GOOD_LAW status) |
| Pre-Filing Citator-Check Pass Rate | 100% | <99% | # of filed documents with all citations passing automated citator check at filing time / total filed documents |
| Overruled-Citation Insertion Rate | 0% | >0.5% | # of filed documents containing citations later flagged as overruled/limited on the cited point / total filed documents (audited via post-filing opposing counsel citations or internal review) |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Validity-Status Mismatch Between Analysis and Schema | Research analysis identifies point-specific validity limitation but structured schema does not capture it | CRITICAL | Block handoff to drafting agent; escalate to research agent; require schema population with point_specificity details before re-transmission |
| Citation Validity Stale Post-Handoff | Pre-insertion verification shows citation's validity_status in handoff (GOOD_LAW) contradicts current citator result (OVERRULED/LIMITED) | HIGH | Block insertion; escalate to research agent for validity re-check; may require memo supplement if research timing is recent |
| Point-Specific Overruled Citation Inserted | Drafting agent inserts citation for exact proposition on which case was overruled, per research analysis | CRITICAL | Flag citation immediately before filing; require revision or removal; may require supplemental briefing if filed before detection |
| Pre-Filing Citator Check Fails | Automated citator check before filing reveals citation is overruled/limited on cited point | CRITICAL | Block filing; escalate to attorney; revise brief to remove/correct citation; may require supplemental memo explaining citation withdrawal/change |
| Recurring Validity-Handoff Mismatches | >3 validity-status mismatches in one week, suggesting systematic schema/process gap | HIGH | Audit citation-handoff workflow; investigate whether point_specificity validation is functional; may require training/process revision |

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
