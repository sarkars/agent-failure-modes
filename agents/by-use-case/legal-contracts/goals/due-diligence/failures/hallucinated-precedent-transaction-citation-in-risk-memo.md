# Hallucinated Precedent Transaction Citation in Risk Memo

## Issue: A Due-Diligence Agent Drafting a Risk Memo Supports Its Assessment of a Flagged Contract Provision by Citing a "Similar Precedent Transaction" or a Specific Clause Reference Number That Does Not Actually Exist in Any Document the Agent Was Given, Fabricating a Plausible-Sounding Supporting Citation to Complete the Memo's Reasoning

**Frequency**: Occasional

**Symptoms**
- Risk memo states that a flagged provision is "consistent with the treatment seen in [specific prior deal name or document reference]," but no document matching that name or reference exists anywhere in the diligence data room
- A clause reference cited in the memo (e.g., "Section 8.3(b) of the Master Services Agreement") does not match the actual section numbering of the document being discussed, when the underlying document is checked directly
- Re-asking the agent to quote the exact text of the cited precedent or section produces either a different fabricated passage or an admission that no such passage exists, rather than a verbatim quote from a real source
- The fabricated citation is stylistically indistinguishable from genuine citations elsewhere in the same memo, making it undetectable without independently checking the underlying source document
- Deal team proceeds on the strength of the cited precedent without independently verifying it exists, since the memo's overall tone and structure read as well-sourced

**Root Cause**
When a due-diligence agent is asked to justify a risk assessment and the actual data room does not contain a clean, directly supporting precedent or exact section reference, the model can complete the expected citation pattern by generating a plausible-sounding name or section number rather than either omitting the citation or stating that no supporting precedent was found. This is a fabrication failure distinct from a wrong risk assessment -- the underlying risk flag may be correct, but the cited evidence supporting it does not exist, and a deal team that verifies the citation rather than the underlying analysis will be unable to find what was cited.

**Example**
```
Risk memo section on an indemnification cap: "This cap structure is unusually favorable to the seller and is consistent with the treatment in the Northgate-Veridian transaction reviewed during last year's diligence, Section 9.2"
Deal team member searches the diligence repository and the firm's prior-transaction archive for "Northgate-Veridian" -- no such transaction or document exists
Re-prompting the agent to "quote Section 9.2 of the Northgate-Veridian agreement verbatim" produces a fabricated passage rather than a retrieval result, confirming the citation was invented to support the memo's narrative
The underlying concern about the indemnification cap may still be valid, but the memo's stated evidentiary basis for it is fictitious, undermining the deal team's ability to verify or rely on the citation
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM-based agents are documented to fabricate plausible but non-existent supporting references when asked to justify a conclusion, a well-characterized hallucination subtype distinct from factual errors in the underlying analysis | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Surveys of LLMs in legal applications identify citation fabrication as a specific, recurring failure category requiring dedicated verification tooling rather than general accuracy review | [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267) |
| Retrieval reliability research in legal RAG systems notes that ungrounded generation of citation-like content occurs specifically when the retrieval step does not return a clean supporting match, and the model fills the gap rather than reporting the absence | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |

**Contributing Factors**
- Memo-drafting prompt implicitly rewards a well-supported-sounding narrative, with no instruction to explicitly state when no supporting precedent or exact citation was found
- No automated step verifies that every named precedent, document, or section reference in the drafted memo actually resolves to a real document in the diligence repository
- Deal teams typically review the memo's narrative and conclusions rather than independently re-verifying every individual citation against source documents

---

## Mitigation Strategies

1. **Mandatory Citation Resolution Check**: Before a risk memo is finalized, automatically verify that every named precedent, transaction, or section reference resolves to an actual document and section in the diligence repository, flagging any citation that does not resolve for removal or correction
2. **Explicit "No Supporting Precedent Found" Option**: Instruct the drafting agent explicitly that stating no supporting precedent was found is an acceptable and expected output, rather than implicitly pressuring it to always produce a citation
3. **Quote-on-Demand Verification for High-Stakes Citations**: For any citation supporting a material risk flag, require the agent to produce a verbatim quote with a resolvable source locator, and treat an unresolvable quote request as evidence the citation should be removed
4. **Citation Provenance Logging**: Log the retrieval step (if any) that produced each citation in the memo, so any citation with no corresponding retrieval event is automatically flagged as a likely fabrication before human review

### Metrics
- Rate of citations in finalized risk memos that fail an automated resolution check against the diligence repository
- Number of citations per memo with no corresponding retrieval-event log entry
- Rate of "quote-on-demand" verification requests that fail to produce a resolvable source

### Alerts
- A risk memo is finalized and sent to the deal team with one or more citations that fail the resolution check → P1
- A material risk flag's sole supporting citation cannot produce a verbatim, source-resolvable quote on demand → P1
- Citation fabrication rate across a diligence engagement's memos exceeds baseline for two consecutive engagements → P2

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
