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

1. **Mandatory Citator Check at Generation Time**: Require every case citation produced by the agent to be checked against a live citator service for negative subsequent treatment (overruled, vacated, limited, questioned) before inclusion in any output
2. **Currency Flag on All Citations**: Surface the citator-checked status explicitly alongside every citation in the agent's output (e.g., "good law as of [date]" or "flagged: superseded by [citation]"), rather than presenting citations without status context
3. **Corpus Freshness Tracking**: Track and disclose the as-of date of any static reference corpus used, and treat citations sourced from a corpus older than a defined threshold as requiring mandatory live verification
4. **Human Attorney Sign-Off on Citations**: Require attorney verification of all case citations before filing or client delivery, treating the agent's output as a draft requiring citation validation rather than a final authority

### Metrics
- Percentage of agent-generated citations checked against a live citator before output
- Number of citations flagged with negative subsequent treatment caught before filing/delivery vs. caught after (by opposing counsel or court)
- Corpus freshness (time since last update) for any static legal reference data in use

### Alerts
- An agent-generated citation is included in a final output without a citator check → P1
- A citator check returns negative subsequent treatment for a citation already included in a draft → P1

---

## References

- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
- [Large Language Models Meet Legal Artificial Intelligence: A Survey](https://arxiv.org/pdf/2509.09969)
