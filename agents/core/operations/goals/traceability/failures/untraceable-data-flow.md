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

**Mitigation Strategies**
1. **Source tagging**: Mark all data with origin metadata
2. **Transformation logging**: Record each data modification
3. **Lineage graph**: Maintain data flow DAG
4. **Output attribution**: Tag output segments with sources
5. **PII tracking**: Special lineage for sensitive data
6. **Cross-agent lineage**: Preserve lineage across boundaries

**Detection**
- Audit output for unattributed data
- Test PII source tracing
- Measure lineage coverage
- Run lineage queries on samples
- Compliance audit dry runs

## References

- [GDPR Article 30](https://gdpr.eu/article-30-records-of-processing-activities/) - Processing records requirements
- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Data provenance
- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Citation tracking
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Cross-agent data flow
