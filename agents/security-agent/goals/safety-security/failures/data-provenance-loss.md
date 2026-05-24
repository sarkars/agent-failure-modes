# Loss of Data Provenance

## Issue: Data Origin and Classification Lost During Processing

**Frequency**: Common

**Symptoms**
- Agent outputs contain data from unknown sources
- Classification labels stripped during processing
- Sensitive data exposed without appropriate controls
- Audit trails incomplete or missing
- Cannot determine which data informed decisions

**Root Cause**
An agentic AI system has access to data sources to inform and ground its actions. This data is passed between multiple agents or components before being output, potentially leading to loss of provenance for that data and subsequent data integrity or confidentiality issues.

**Example**
```
Multi-agent system:
- Research Agent: Accesses classified internal documents
- Synthesis Agent: Combines research with public data
- Output Agent: Generates report for external stakeholders

Data flow:
1. Research Agent retrieves TOP SECRET document
2. Passes relevant excerpt to Synthesis Agent
3. Classification metadata stripped during transfer
4. Synthesis Agent treats data as unclassified
5. Output Agent includes in external report

Result: Classified data leaked in "public" report
```

**Provenance Loss Points**
- Agent-to-agent communication boundaries
- Context window truncation
- Data format transformations
- Memory storage and retrieval
- Output aggregation

**Potential Effects**
- Confidential data exposure
- Compliance violations (GDPR, HIPAA, etc.)
- Inability to audit decision sources
- Misattribution of information
- Legal liability from data handling failures

**Mitigation Strategies**
1. **Metadata preservation**: Carry provenance through all transformations
2. **Data tagging**: Apply persistent classification labels
3. **Output controls**: Check data provenance before external output
4. **Audit logging**: Track data flow through system
5. **Trust boundaries**: Explicit handling at agent boundaries
6. **Source attribution**: Maintain links between outputs and inputs

**Detection**
- Outputs containing data without source attribution
- Classification mismatches between input and output
- Audit gaps in data processing chain
- User reports of unexpected data in outputs

## References

- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Loss of data provenance as security failure mode
- [NSA: Careful Adoption of Agentic AI](https://media.defense.gov/2026/Apr/30/2003922823/-1/-1/0/CAREFUL%20ADOPTION%20OF%20AGENTIC%20AI%20SERVICES_FINAL.PDF) - Government guidance on data handling
- [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) - Data integrity in agent systems
