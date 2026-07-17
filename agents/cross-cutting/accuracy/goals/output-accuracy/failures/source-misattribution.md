# Source Misattribution

## Issue: Agent Attributes Information to Wrong Source

**Frequency**: Common

**Symptoms**
- Citations point to documents that don't contain the claim
- Quote attributed to wrong person
- Statistics linked to wrong study
- Source exists but doesn't support the claim made

**Root Cause**
Agent knows information should be cited but doesn't maintain accurate links between claims and sources. May confuse which source contained which information.

**Example**
```
Agent: "According to the Q3 2024 report, revenue increased 15% [1]"

Source [1] content: Q2 2024 report showing 12% growth

Reality: Q3 report showed 15%, but citation points to Q2 report

Result: User follows citation, finds different data, loses trust
```

---

## Test Scenario & Reproduction

### Scenario Setup
- A retrieval-augmented generation pipeline with multiple similar source documents available (e.g., Q2 2024 and Q3 2024 reports covering the same company)
- No extractive-citation or claim-source binding requirement enforced at generation time
- A specific, checkable numeric claim that differs between the similar source documents (12% vs. 15% growth)

### Trigger Mechanism
1. Ensure both the Q2 and Q3 reports are present in the retrieval corpus, with different growth figures in each
2. Prompt the agent to answer a question about Q3 revenue growth with a citation
3. Check whether the cited source [1] actually contains the claimed figure, or whether the claim and citation were drawn from different documents

**Example Reproduction Steps:**
```
1. Load both the Q2 2024 report (12% growth) and Q3 2024 report (15% growth) into the retrieval index
2. Ask: "What was the revenue growth in the Q3 2024 report?"
3. Record the agent's stated figure and its citation marker (e.g., "15% [1]")
4. Open the document referenced by citation [1] and check whether it actually states 15% growth or a different figure (12%, from Q2)
5. Repeat across multiple near-duplicate document pairs (adjacent quarters, similar-named entities) to measure how often the citation resolves to the wrong-but-related document
6. Compute the claim-source mismatch rate across the test batch
```

### Expected Failure State
- The stated numeric claim (15%) is correct, but the citation marker points to a document (Q2 report, 12%) that does not contain that figure
- Manually following the citation surfaces contradictory data rather than confirming the claim
- The mismatch is specifically a wrong-but-adjacent source (same company, neighboring time period) rather than a completely unrelated document, matching the documented failure pattern
- No automated check catches the mismatch before the response is delivered to the user

---

## Mitigation Strategies

### Prevention
1. **Extractive-only citation generation**: Require the agent to quote or closely paraphrase the exact retrieved span it's citing rather than freely generating a citation number and separately generating the claim — this prevents the example's failure where a 15% growth claim was generated correctly but linked to source [1], which actually contained the 12% Q2 figure. Trade-off: extractive citation is more restrictive and can produce less fluent prose than freely-generated summaries.
2. **Claim-source binding at generation time**: Bind each generated claim to the specific retrieved chunk it was derived from as part of the generation process (not a post-hoc citation lookup), so the citation mechanism can't drift from the claim it's attached to. Trade-off: requires a generation architecture that tracks provenance per-span, which is more complex than plain retrieval-augmented generation.
3. **Page/line-level reference granularity**: Cite to the specific location within a source (page, paragraph, line) rather than the document as a whole, making it possible to verify the claim actually appears at the cited location rather than just somewhere in a large source. Trade-off: requires source documents to be chunked/indexed at fine granularity, adding preprocessing overhead.

### Detection & Response
1. **Automated claim-in-source verification**: For every citation, programmatically check whether the cited claim's key facts (numbers, names, dates) actually appear in the cited source span — this would directly catch the 15%-vs-12% mismatch in the example before it reaches the user.
2. **User-reported broken-citation tracking**: Log and categorize user reports of citations that don't support the claim (as in the example's "user follows citation, finds different data") to identify systemic patterns versus one-off errors.
3. **Sample-based human citation audits**: Periodically sample published citations and have a human verify the cited source actually supports the claim, since automated matching can miss paraphrased or contextually-wrong citations that pass a naive keyword check.

### Architecture Patterns
1. **Retrieval-then-generate with hard provenance links**: Generate claims only from retrieved content, maintaining an explicit mapping from each generated sentence to its source chunk throughout the generation process, so misattribution requires an active linking bug rather than being the default failure mode of free generation. Deployment consideration: constrains the generation model to retrieved content, which can reduce fluency or force awkward phrasing when retrieved content doesn't read naturally.
2. **Citation verification as a blocking post-generation step**: Run a dedicated verification pass after generation that checks every citation against its claimed source and blocks or flags responses where citations fail verification, rather than trusting citations added during generation. Deployment consideration: adds a verification model/step to the pipeline, increasing latency and cost per response.
3. **Versioned source-claim mapping store**: Maintain an explicit, queryable mapping between claims and sources (not just inline citation markers) so citation accuracy can be audited and corrected independently of the generation pipeline. Deployment consideration: requires infrastructure to store and query claim-source mappings at scale, beyond what inline citations alone provide.

### Metrics
1. **citation_accuracy_rate**: % of citations where the cited source actually contains the claimed fact; target > 98%; alert if < 90%.
2. **claim_source_mismatch_rate**: % of citations pointing to a source discussing a related but different fact/period (like Q2 vs Q3 in the example); target < 2%; alert if > 8%.
3. **user_broken_citation_reports**: Reports per 10,000 citations served; target < 5; alert if > 20.
4. **sample_audit_pass_rate**: % of human-audited citation samples confirmed accurate; target > 97%; alert if < 90%.

### Alerts
1. **Citation Accuracy Below Threshold** (P1): Condition — citation_accuracy_rate drops below 90% for a content category. Action: pause citation-bearing responses for that category pending root-cause review of the retrieval/generation binding.
2. **Claim-Source Mismatch Spike** (P2): Condition — claim_source_mismatch_rate exceeds 8% over a rolling week. Action: audit recent responses for the specific mismatch pattern (e.g., adjacent time-period confusion) and patch the claim-source binding logic.
3. **User Broken-Citation Reports Spike** (P2): Condition — user_broken_citation_reports exceeds 20 per 10,000 citations. Action: sample the reported cases, confirm the pattern, and escalate to the retrieval/generation pipeline owners.

---

## References

- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Research on citation accuracy in legal RAG systems
- [Mindee: RAG Hallucinations Explained](https://www.mindee.com/blog/rag-hallucinations-explained) - Analysis of source attribution failures in RAG pipelines
