# Superseded Case-Law Citation

## Issue: Agent Cites a Case as Controlling Precedent Without Detecting That It Has Been Overturned, Limited, or Superseded by Later Authority

**Frequency**: Common

**Symptoms**
- Agent's legal research output cites a case for a legal proposition without checking whether the case has since been reversed, vacated, or overruled on appeal or by a later decision
- A case that was "good law" at the time it was added to the agent's reference corpus is cited even after a subsequent statute or higher-court ruling has superseded it, because the corpus was not refreshed
- Citations are validated for correct Bluebook/citation-format accuracy but not for current legal status (i.e., the citation "looks right" syntactically while being substantively obsolete)
- A brief or memo using an agent-assisted citation is challenged by opposing counsel for relying on bad law, requiring late-stage correction
- Agent has no access to or does not consult a citator (Shepard's, KeyCite, or equivalent) signal indicating negative subsequent treatment of a cited case

**Root Cause**
Legal research agents, particularly those relying on a static training corpus or a periodically-refreshed document store, are exposed to the legal status of a case as of whatever point their underlying data was last updated. Without an explicit, live citator check (Shepard's/KeyCite-style negative-treatment lookup) performed at generation time, the agent has no mechanism to know that a case it has "seen" as valid precedent has since been overturned, limited to its facts, or abrogated by statute — the case's text in the corpus remains unchanged regardless of its current legal status.

**Example**
```
Agent's training/reference corpus: Includes Case X (2019), a frequently cited precedent on a procedural standard
Subsequent development: Case X was overruled by a 2024 appellate decision on the same issue
Agent task (2026): Draft a motion section citing relevant precedent on this procedural standard
Agent output: Cites Case X as controlling, without noting the 2024 overruling, because the corpus snapshot predates the overruling or the overruling case was not retrieved
Impact: Opposing counsel flags the citation as relying on overruled authority, undermining the motion's credibility and requiring rework under time pressure
```

**Key Statistics**
- Reliance on outdated or invalidated case law is one of the most consequential and reputationally damaging failure modes in legal AI literature, given direct court sanctions imposed in multiple documented instances of AI-assisted filings citing non-existent or invalidated cases
- Citator services (Shepard's, KeyCite) exist specifically because manual and automated legal research alike face this currency problem, and legal AI survey research identifies live citator integration as a key mitigation distinct from corpus freshness alone
- Static or infrequently-updated legal reference corpora used by LLM-based research tools are specifically flagged in legal AI evaluation literature as a structural source of currency risk independent of the model's general hallucination tendency

---

## Mitigation Strategies

### Prevention

1. **Mandatory real-time citator-check gate before output**: Implement citation-output validation: (a) after agent generates candidate citations, before returning to user, run each citation through live citator service (Shepard's/KeyCite/LexisNexis/legal-research-API), (b) citator check queries: case overruled? vacated? limited? negatively treated? (c) for each citation, capture citator_status = {status: (GOOD_LAW|OVERRULED|VACATED|LIMITED|QUESTIONED|NEGATIVE_HISTORY), negative_authority: [list of overruling cases], negative_history_summary: "text", check_date: timestamp, citator_service: name}. (d) If citator_status != GOOD_LAW, output citation with warning flag and negative_authority link: "[Citation] [WARNING: Overruled by X (2024)]", never output without flag. (e) Fail-safe: if citator service unavailable, output citation as UNVERIFIED and require attorney confirmation before use. Root cause: Prevents superseded cases from reaching users unvalidated.

2. **Corpus-freshness tracking and age-based verification gating**: For any reference corpus (case database, precedent library, statutory compilations): (a) track as-of_date (last update), (b) on every citation sourced from corpus older than 6 months, auto-flag as "sourced from potentially stale data; citator check mandatory", (c) for corpus older than 1 year, mandatory citator check + attorney approval before citation included in output, (d) output metadata: "This citation sourced from corpus dated [date]; citator check performed [date, result]". For live-feed services (PACER, ECLI), no age restriction applies. Root cause: Ensures user visibility into corpus freshness and prevents reliance on outdated-corpus citations.

3. **Citation-status disclosure in all outputs**: Require every citation in agent output to include status label: {case_name, citation_format, citator_status (GOOD_LAW|NEGATIVE_HISTORY|UNVERIFIED), citator_check_date, status_brief (e.g., "Good law as of 2026-07-11" or "Overruled on this point by X (2024)")}. For negative-history cases, include summary of negative authority and reasoning. Never output naked citation without status context. User can immediately see which citations carry risk and which are verified good law. Root cause: Makes citation status transparent rather than opaque.

### Detection & Response

1. **Citation-output audit logging with citator-check verification**: For each citation output, log: {citation_id, case_id, citator_check_performed (Y/N), citator_service_used, citator_status_at_output_time, status_flag_included_in_output (Y/N), corpus_source_date (if applicable), subsequent_citator_check_results (if discovered post-output)}. Weekly audit: sample 20% of output citations, re-run citator checks to verify status has not changed since output was generated. Alert if: >2% have changed status post-output, indicating either citator service lag or citations that became superseded between output and audit. For high-risk citations (opinions, motions filed in court), re-check immediately before filing.

2. **Post-Output Supersession Detection and Retroactive Remediation**: Monitor for new citations, overruling decisions, statute amendments that affect previously-output citations. When supersession detected: (a) identify all outputs containing affected citation, (b) notify users/attorneys of supersession, (c) provide corrected citation or retraction recommendation, (d) for filed documents: assess whether retroactive supplemental brief required. Log all retroactive supersessions for trend analysis: which case types, practice areas most frequently become superseded? Use for corpus-update planning.

### Architecture Patterns

1. **Real-Time Citator-Check Integration at Output Gate**: Before citation returned to user, query live citator service. Retrieve citator_status and negative_authority. Tag citation in output with status. If citator unavailable, mark UNVERIFIED and escalate. Build integration with multiple citator providers (Shepard's, KeyCite, FastCase) with fallback logic.

2. **Corpus-Freshness Registry with Age-Based Verification Gating**: Maintains metadata for every reference corpus in use: name, as-of_date, refresh_frequency, freshness_threshold (6 months | 1 year). On citation generation, check if source corpus age exceeds threshold. If yes, auto-flag for citator check. On corpus refresh, update registry and trigger re-check of recent citations from old corpus.

3. **Citation-Status Disclosure Engine**: Post-citator-check, structured citation output includes status_label for every citation. Never outputs citation without status context. Supports detailed disclosure for negative-history cases.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Citator-Check Coverage Rate | 100% | <99% | # of case citations checked against live citator before output / total case citations generated |
| Citator-Check Availability | >99.5% | <99% | # of citator checks completed successfully / total citations requiring checks (excluding service-unavailable scenarios) |
| Negative-History Detection Rate | 100% | <99% | # of citations with negative subsequent treatment flagged before output / total citations with negative history (validated via audit re-checks) |
| Status-Flag Inclusion Rate | 100% | <99% | # of output citations including citator_status flag / total citations in final output |
| Corpus-Age Threshold Compliance | 100% | <99% | # of citations sourced from corpus older than threshold that underwent citator check / total such citations |
| Post-Filing Supersession Incidents | 0% | >0% | # of filed documents later flagged by court or opposing counsel as citing superseded authority / total filed documents (audited via post-filing opposition/ruling review) |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Citation Output Without Citator Check | Citation included in output with no evidence of citator check performed | CRITICAL | Remove citation from output before delivery; require citator check; re-deliver only after GOOD_LAW or status-flagged status confirmed |
| Negative-History Citation Not Flagged | Citation with negative subsequent treatment (overruled, limited, questioned) included in output without warning flag | CRITICAL | Immediately escalate to attorney; remove or re-flag citation; if already delivered, notify recipient of correction; assess filing/delivery damage |
| Citator Service Unavailable at Output Time | Citator API down or unavailable when citation generated | HIGH | Mark citation UNVERIFIED in output; notify user; require attorney confirmation or secondary citator check before use; monitor citator availability |
| Stale-Corpus Citation Not Verified | Citation from corpus older than threshold included in output without citator check | MEDIUM | Escalate to attorney; recommend citator verification before use; may not block output but requires advisory flag |
| Post-Output Citation Supersession Detected | New authority or ruling discovered post-output that supersedes previously-output citation | HIGH | Identify all outputs affected; notify relevant attorneys; assess whether filed documents require supplemental brief; update corpus and future citations |
| Court/Opposing-Counsel Supersession Challenge | Court or opposing counsel flags citation in filed document as superseded or bad law | CRITICAL | Immediate escalation to litigation counsel; assess whether malpractice/sanctions risk; determine whether supplemental filing or retraction required; audit all recent citations from same corpus/agent for similar issues |

---

## References

- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
- [Large Language Models Meet Legal Artificial Intelligence: A Survey](https://arxiv.org/pdf/2509.09969)
