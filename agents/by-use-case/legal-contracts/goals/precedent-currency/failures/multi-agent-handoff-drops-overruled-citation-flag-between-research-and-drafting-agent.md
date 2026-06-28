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

1. **Point-Specific Validity-Status Field in Citation Schema**: Extend the structured citation-list schema to carry an explicit, point-specific validity status for each citation (e.g., which specific holding is and is not still good law), and require the research agent to populate it directly rather than leaving nuance in narrative analysis only
2. **Pre-Insertion Citation Validity Re-Check**: Before the drafting agent inserts a citation to support a specific proposition, automatically re-verify that citation's validity status on that exact point against a current case-law validity service, independent of the original research handoff
3. **Drafting Agent Access to Full Research Rationale**: Require the drafting agent's citation-insertion step to have access to the research agent's full analysis for any citation flagged with partial or point-specific validity limitations
4. **Mandatory Citator Check Before Filing**: Require every citation in a filed document to pass through an automated citator or validity-checking service immediately before filing, regardless of what validity information was captured during research

### Metrics
- Rate of inserted citations where the research agent's analysis contains validity-limitation language not reflected in the structured citation-list entry
- Rate of filed documents containing a citation later flagged as overruled or limited on the cited point
- Time between citation-validity determination during research and citation insertion during drafting

### Alerts
- A citation is inserted to support a proposition the research agent's analysis identified as the specific point on which the case was overruled → P1
- A filed document contains a citation that fails an automated citator check run before filing → P1
- Validity-reconciliation mismatch rate between research analysis and structured citation entries exceeds the defined threshold for a rolling window → P2

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
