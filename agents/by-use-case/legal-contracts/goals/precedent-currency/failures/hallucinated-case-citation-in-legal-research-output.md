# Hallucinated Case Citation in Legal Research Output

## Issue: A Legal-Research Agent Asked to Support a Legal Proposition Generates a Citation to a Case That Does Not Exist -- a Plausible-Sounding Case Name, Reporter Citation, and Holding That the Model Fabricates Rather Than Retrieves From an Actual Case-Law Database -- and Presents It With the Same Confidence and Formatting as Genuine Citations

**Frequency**: Occasional

**Symptoms**
- A cited case (name, reporter citation, court, and year) does not exist in any case-law database when independently searched, despite being formatted exactly like genuine citations elsewhere in the same research output
- The fabricated case's stated holding is a plausible, on-point summary of the legal proposition being argued, which is precisely why it reads as credible without independent verification
- Re-asking the agent to produce the case's exact holding language or a pin-cite to the specific page produces either a different fabricated detail or an admission that it cannot locate the case, rather than a consistent, verifiable citation
- Fabricated citations occur even when the agent has a real case-law database tool available, specifically on propositions where the actual case law is thin, mixed, or does not cleanly support the desired argument
- A brief or memo is filed or relied upon with the fabricated citation, surfacing only when opposing counsel, a clerk, or the court itself cannot locate the cited case

**Root Cause**
When asked to support a legal proposition and the available case-law retrieval does not return a clean, directly on-point case, the model can complete the expected citation pattern by generating a citation-shaped continuation -- a name, reporter number, and holding statistically consistent with how real citations look -- rather than either returning the closest real case with a caveat or stating that no directly on-point authority was found. This is a generation failure distinct from a retrieval miss: even when a case-law database tool is available, the model is not guaranteed to prefer "no clean match" as an output over a fabricated one that better completes the expected response shape.

**Example**
```
Research request: "Find a case supporting the proposition that a force majeure clause covers a pandemic-driven supply disruption under [State] law"
Agent's available case-law database returns no case squarely on point for this specific fact pattern under this state's law
Agent's output nonetheless includes: "See Henley Logistics v. Carrow Freight, 412 F.3d 188 (7th Cir. 2021), holding that pandemic-related supply disruptions fall within standard force majeure language"
No such case exists in any reporter; the citation, court, and holding are fabricated to complete a confident-sounding answer
Citation is included in a draft memo; an associate cite-checking the memo cannot locate the case, and the research is found to rest on a fabricated authority
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM-based agents are documented to fabricate citation-shaped content -- including non-existent case names, reporters, and holdings -- as a well-characterized hallucination subtype distinct from retrieval failure | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Surveys of LLMs in legal applications explicitly identify fabricated case citation as a named, recurring failure category requiring dedicated cite-checking tooling distinct from general legal-accuracy review | [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267) |
| Retrieval reliability research in legal RAG systems notes that ungrounded citation generation occurs specifically when retrieval does not return a clean supporting match for the exact proposition requested | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |

**Contributing Factors**
- Research prompt implicitly rewards a confident, well-supported-sounding answer, with no instruction that "no directly on-point authority found" is an acceptable and expected output
- No automated step verifies that every cited case resolves to a real entry in a case-law database with a matching name, reporter citation, and court before the research output is finalized
- Human reviewers tend to evaluate the research output's narrative coherence rather than independently re-verifying every individual citation against a case-law database

---

## Mitigation Strategies

1. **Mandatory Citation Resolution Against Case-Law Database**: Before any research output is finalized, automatically verify that every cited case resolves to a real entry with a matching name, reporter citation, and court in an authoritative case-law database, flagging unresolved citations for removal
2. **Explicit "No On-Point Authority Found" Output Path**: Instruct the research agent explicitly that stating no directly on-point authority was found is a valid and expected output, rather than implicitly pressuring it toward always producing a supporting case
3. **Pin-Cite Verification for Every Cited Holding**: Require every cited holding to include a pin-cite to a specific page, and automatically verify the pin-cite resolves to text in the actual case that supports the stated holding, not merely that the case exists
4. **Cite-Check Gate Before Filing or Distribution**: Require a citation-resolution pass to complete with zero unresolved citations as a hard gate before any research output is included in a filed brief or distributed memo

### Metrics
- Rate of citations in research outputs that fail automated resolution against a case-law database
- Number of unresolved or fabricated citations caught at the cite-check gate versus discovered after filing or distribution
- Percentage of research outputs that include an explicit "no on-point authority found" statement when retrieval returns no clean match

### Alerts
- A brief or memo is filed or distributed with one or more citations that fail the resolution check → P1
- Cite-check gate finds an unresolved citation and the document proceeds without correction → P1
- Citation fabrication rate across research outputs exceeds baseline for two consecutive reporting periods → P2

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
