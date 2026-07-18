# Untraceable Data Flow

## Issue: Cannot Track How Data Moved Through Agent Pipeline

**Frequency**: Common

**Symptoms**
- Output contains data of unknown origin
- Cannot verify data transformations
- PII exposure source unidentifiable
- Data lineage requirements unmet
- Cannot trace errors to data source

**Root Cause**
Agents consume data from multiple sources, transform it through various steps, and produce outputs that combine information in complex ways. Without explicit data lineage tracking, it's impossible to know where specific pieces of information came from, how they were transformed, or whether they should be in the output at all.

**Example**
```
Agent output includes customer SSN in summary email

Investigation: "Where did the SSN come from?"

Data sources queried:
  - Customer database (has SSN, masked in output)
  - Support ticket system (SSN in free text?)
  - Previous emails (customer sent SSN?)
  - Knowledge base (example with real SSN?)

Data flow (not tracked):
  1. Retrieved customer record → masked SSN
  2. Retrieved support ticket → contained full SSN in notes
  3. Summarized ticket → SSN included in summary
  4. Generated email → SSN propagated to email
  
Without lineage:
  - Can't identify which source leaked SSN
  - Can't determine if masking failed or was bypassed
  - Can't fix the specific leak path
  - Can't audit other potentially affected records
  
With lineage would show:
  ticket.notes → summary.context → email.body
  (SSN should have been filtered at step 2)
```

**Key Statistics**
From Data Governance Research (2026):
- Data lineage required by GDPR, CCPA for PII
- Average agent touches 5-10 data sources per task
- Cross-source data combination common
- PII leakage often from unexpected sources
- "Where did this come from?" - frequent compliance question

**Lineage Gap Types**
| Gap | Risk | Frequency |
|-----|------|-----------|
| Source attribution | Can't verify origin | Very Common |
| Transformation tracking | Can't verify processing | Common |
| Aggregation lineage | Can't trace components | Common |
| Cross-agent flow | Lost at boundaries | Very Common |
| Temporal lineage | Don't know when from | Occasional |

**Contributing Factors**
- Data combined in LLM context window
- No automatic lineage in text processing
- Cross-source joins lose attribution
- Summarization obscures sources
- RAG retrieval doesn't tag sources

## Test Scenario & Reproduction

### Scenario Setup
- Deploy a customer-support agent that retrieves data from multiple sources (customer database with masked SSN, support ticket system with unmasked free-text notes, prior emails, knowledge base) and summarizes it into a response email
- No source-tagging is applied to retrieved fragments before they enter the agent's context, and no PII-aware filtering runs at each transformation step (only at the original database query)
- The support ticket system contains a ticket with a customer's full SSN typed into the free-text notes field
- No lineage graph or output-attribution requirement blocks unattributed sensitive content

### Trigger Mechanism
1. The agent retrieves the customer record (SSN properly masked) and the related support ticket (SSN present, unmasked, in free-text notes)
2. Both sources are pulled into the same summarization context with no distinguishing source tags
3. The summarization step includes the ticket's SSN in its output, since PII filtering was only applied at the database-query step and not at this transformation
4. The generated email propagates the SSN from the summary into the final customer-facing message

### Example Reproduction Steps
```
1. Retrieve customer record -> SSN masked: "XXX-XX-4921"
2. Retrieve support ticket notes -> contains: "Customer confirmed
   SSN 287-65-4921 for verification"
3. Summarization step combines both sources with no source tagging;
   output includes: "...verified customer identity using SSN
   287-65-4921..."
4. Email generation step propagates the summary text unchanged into
   the outbound email body
5. Investigator: "Where did the SSN come from?" -> queries customer
   database (masked, ruled out), support ticket system (checks notes
   field, finds unmasked SSN) -> confirms leak path only after manual
   cross-source investigation, since no lineage graph existed
```

### Expected Failure State
The customer's unmasked SSN reaches the outbound email because it entered through the support-ticket source (not the properly-masked database source) and no lineage tracking or transformation-stage PII filtering caught it before the email was sent, requiring a reactive manual investigation across every possible source to find the leak path afterward. A correctly instrumented system tags the ticket-notes content by source and sensitivity at retrieval time, applies PII filtering at the summarization transformation step (not just the original query), and blocks the SSN from reaching the summary in the first place.

## Mitigation Strategies

### Prevention
1. **Source-tagging at retrieval time for every data source touched**: Tag every piece of retrieved data (customer record, support ticket, prior email, knowledge-base entry) with its origin the moment it enters the agent's context, so a summarization step can filter based on source sensitivity — the example's SSN leak specifically happened because the support-ticket source (which had unmasked SSN in free text) wasn't distinguished from the customer-database source (which was properly masked) once both were pulled into the same summarization step. Trade-off: tagging every retrieved fragment adds overhead to the retrieval pipeline and requires every data source integration to participate consistently.
2. **PII-aware filtering enforced at each transformation step, not just at the final source**: Apply PII detection/masking at every transformation boundary (ticket → summary → email), not only at the original customer-database query, since the example shows masking was correctly applied at step 1 but the unmasked SSN entered through step 2 (the support ticket) and propagated unfiltered through summarization and email generation. Trade-off: requires PII-scanning at multiple pipeline stages rather than once, increasing latency and false-positive risk (over-redacting legitimate content).
3. **Explicit output-attribution requirement before including sensitive-category content**: Require that any output segment containing a sensitive data pattern (SSN-like strings, financial data) carry a resolvable source attribution before it's allowed into the final output; if attribution can't be established, block or redact rather than pass through — this would have flagged the SSN in the summary as unattributed/unexpected before the email was ever generated. Trade-off: adds a hard gate that can block legitimate content if the attribution mechanism has gaps, trading some availability for security.

### Detection & Response
1. **Automated output-content auditing for unattributed sensitive data**: Continuously scan agent outputs for PII-pattern content (SSNs, financial identifiers) and check whether each instance can be traced to an attributed, expected source; content without traceable attribution is the exact leak pattern the example describes and should be caught before or immediately after the email sends, not during a reactive investigation.
2. **PII-source-tracing test suite**: Regularly test whether the pipeline can correctly trace a known-injected PII value back through retrieval, transformation, and output stages, verifying the lineage mechanism actually works rather than assuming it does until an incident like the SSN leak forces a manual investigation.
3. **Lineage-coverage measurement across all data sources**: Measure what fraction of an agent's touched data sources (the example notes agents typically touch 5-10 per task) actually have lineage tracking versus being "black box" inputs — the support-ticket source in the example was evidently one of the untracked ones, which is exactly the coverage gap this metric surfaces.

### Architecture Patterns
1. **Lineage graph (DAG) as a first-class pipeline artifact**: Maintain an explicit directed graph of data flow — source → transformation → output — for every task execution, so a question like "where did the SSN come from" resolves to a graph traversal (`ticket.notes → summary.context → email.body`) instead of a reactive, manual, cross-source investigation. Deployment consideration: requires every pipeline stage (retrieval, summarization, generation) to emit lineage edges, which is a structural requirement on the agent architecture, not an add-on.
2. **PII-tagged special-handling lineage for sensitive data categories**: Build a dedicated, higher-scrutiny lineage path specifically for data classified as PII, so sensitive content is tracked with extra rigor (mandatory masking checkpoints, mandatory attribution) distinct from the lineage tracking applied to non-sensitive data. Deployment consideration: requires reliable PII classification at ingestion, which itself can have false negatives (unstructured free-text SSNs, as in the support ticket, are harder to classify than structured database fields).
3. **Cross-agent lineage preservation at every handoff boundary**: When data or derived summaries pass between agents or pipeline stages, explicitly carry forward the lineage metadata rather than letting it reset at each boundary — "cross-agent flow lost at boundaries" is named as a very common gap type, and preserving lineage across boundaries is what makes end-to-end tracing (not just within-agent tracing) possible. Deployment consideration: requires a shared lineage schema/protocol that every agent and tool in a multi-agent pipeline honors consistently.

### Metrics
1. **lineage_coverage_rate**: % of data sources touched by agent tasks that have functioning lineage tracking; target > 95%; alert if < 70% (targeting the "5-10 sources per task, many untracked" gap in the example).
2. **unattributed_sensitive_content_rate**: % of outputs containing PII-pattern content without a resolvable source attribution; target 0%; alert on any nonzero occurrence in production.
3. **pii_source_tracing_test_pass_rate**: % of PII-tracing test cases (known-injected sensitive values) correctly traced end-to-end; target 100%; alert if < 95%.
4. **cross_agent_lineage_preservation_rate**: % of multi-agent handoffs that preserve lineage metadata across the boundary; target > 90%; alert if < 60%.

### Alerts
1. **Unattributed Sensitive Content in Output** (P1): Condition — unattributed_sensitive_content_rate registers any nonzero event in production (PII-pattern content without traceable source, matching the SSN-in-email example). Action: immediately quarantine/recall the affected output if possible, treat as a data-protection incident, and trace the leak path using whatever lineage data exists before it's lost.
2. **Lineage Coverage Gap** (P2): Condition — lineage_coverage_rate falls below 70% for a task category. Action: prioritize adding source-tagging and transformation logging for the highest-risk untracked sources first (free-text fields like support tickets, which are more likely to contain unmasked PII than structured database fields).
3. **PII Tracing Test Failure** (P1): Condition — pii_source_tracing_test_pass_rate falls below 95%. Action: block reliance on lineage claims for compliance purposes until the tracing mechanism is fixed and re-validated; treat any compliance attestations made using the broken tracing as suspect.

## References

- [GDPR Article 30](https://gdpr.eu/article-30-records-of-processing-activities/) - Processing records requirements
- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Data provenance
- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Citation tracking
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Cross-agent data flow
