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

---

## Test Scenario & Reproduction

### Scenario Setup
- A multi-agent pipeline (research agent → synthesis agent → output agent) where classification metadata is carried as a separable field rather than bound to the data
- No re-derivation or verification of classification at format-transformation boundaries
- No pre-output provenance gate on the externally-facing agent

### Trigger Mechanism
1. Feed the research agent a classified (or sensitivity-tagged) source document
2. Have it pass an excerpt to the synthesis agent, observing whether the classification tag survives the handoff
3. Have the output agent generate an external-facing artifact and check whether the classified content is included without the original tag

**Example Reproduction Steps:**
```
1. Tag a test document as TOP SECRET / restricted in the source system
2. Have the research agent extract and forward a relevant excerpt to the synthesis agent
3. Inspect the excerpt's metadata as received by the synthesis agent
4. Have the synthesis agent combine it with public data and pass to the output agent
5. Check the final external-facing report for the restricted content and its classification status
6. Measure: does the classification tag survive each of the 3 handoffs?
```

### Expected Failure State
- Classification metadata is missing or defaulted to "unclassified" by the second handoff
- The output agent includes the originally-restricted content in an external-facing report with no flag
- Audit trail cannot show which source informed the final output's restricted content

---

## Mitigation Strategies

### Prevention
1. **Provenance metadata bound to data as an immutable, non-strippable attribute**: Attach classification and source metadata to data as a cryptographically-bound attribute (not a separable header/field) that survives every transformation and agent-to-agent handoff, since the root cause is explicitly that classification metadata gets "stripped during transfer" between agents like the Research and Synthesis agents in the example. Trade-off: requires every component in the pipeline (including third-party tools and format converters) to understand and propagate the binding, which is difficult to guarantee across a heterogeneous multi-agent system.
2. **Format-transformation-safe provenance carriers**: When data changes format (e.g., extracted excerpt from a full document, summarized text from raw text), require the transformation step to explicitly re-derive and re-attach the classification of the source rather than defaulting to "unclassified," directly targeting the example's failure point where "Synthesis Agent treats data as unclassified" after receiving an excerpt of a TOP SECRET document. Trade-off: conservative re-derivation (inheriting the highest classification of any contributing source) can over-classify combined outputs, requiring a declassification review process to avoid permanently over-restricting benign synthesized content.
3. **Pre-output provenance gate at every external-facing boundary**: Require an explicit provenance check before any agent (like the Output Agent in the example) can include content in an external-facing report, blocking inclusion of any data whose classification cannot be verified or exceeds the intended audience's clearance. Trade-off: a strict "block if provenance unknown" policy can halt legitimate outputs when metadata is incidentally lost for benign reasons (e.g., a formatting bug), requiring a manual override/review path that itself needs careful access control.

### Detection & Response
1. **Classification-mismatch scanning between input and output boundaries**: Compare the classification metadata present at each pipeline stage's input against its output, flagging any case where classification appears to silently downgrade (e.g., TOP SECRET input, unclassified output) as happened in the documented example when metadata was "stripped during transfer."
2. **Source-attribution completeness auditing on all agent outputs**: Audit generated outputs (reports, summaries) for content that lacks a traceable link back to a specific source input, since "cannot determine which data informed decisions" is a named symptom — outputs without attribution are a leading indicator that provenance was lost somewhere in the pipeline.
3. **Data-flow audit-trail gap detection across agent boundaries**: Monitor the audit trail specifically at agent-to-agent handoff points (the documented "provenance loss point") for missing or incomplete entries, since these boundaries are named as the primary loss point, distinct from general logging gaps elsewhere in the pipeline.

### Architecture Patterns
1. **Provenance-as-first-class-data architecture (data classes carry, not just describe, their trust level)**: Architect the multi-agent data model so classification/provenance is structurally part of the data object itself (not a sidecar field agents can drop), so a Synthesis Agent physically cannot construct an "unclassified" output object from a TOP SECRET input without an explicit, logged declassification action.
2. **Explicit trust-boundary gateways between agents**: Insert dedicated gateway components at every agent-to-agent handoff that validate, log, and enforce provenance propagation rules, rather than relying on each agent implementation to individually preserve metadata correctly — centralizing the "explicit handling at agent boundaries" the file calls for.
3. **Output-agent classification-aware rendering pipeline**: Architect the final output-generation stage (like the Output Agent in the example) to require a resolved, verified classification for every included data fragment before rendering, with unresolved-provenance content automatically excluded rather than defaulting to inclusion.

### Metrics
1. **provenance_metadata_survival_rate**: Target: 100% of data retains classification metadata through all transformations; Alert on any detected stripping event
2. **classification_downgrade_incidents**: Target: 0 instances of output classification lower than the highest-classified contributing input; Alert on any downgrade
3. **output_source_attribution_coverage_pct**: Target: 100% of external-facing output content has traceable source attribution; Alert on any unattributed content in an external report
4. **agent_boundary_audit_gap_rate**: Target: 0 gaps in the audit trail at agent-to-agent handoff points; Alert on any detected gap

### Alerts
1. **Classification Downgrade Detected** (P1): Condition - data flowing between pipeline stages shows a lower classification at output than at input. Action: Block the affected output from proceeding further (especially to external-facing stages), investigate the transformation step that dropped the metadata.
2. **Unattributed Content in External Output** (P1): Condition - an external-facing report contains content with no traceable source/provenance link. Action: Hold the report from release, trace the content back through the pipeline manually, fix the attribution gap before allowing future releases.
3. **Agent Handoff Audit Gap** (P2): Condition - the audit trail is missing an expected entry at an agent-to-agent data handoff. Action: Flag the handoff for review, reconstruct the data flow from available logs if possible, treat as a compliance risk pending resolution.

## References

## References

- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Loss of data provenance as security failure mode
- [NSA: Careful Adoption of Agentic AI](https://media.defense.gov/2026/Apr/30/2003922823/-1/-1/0/CAREFUL%20ADOPTION%20OF%20AGENTIC%20AI%20SERVICES_FINAL.PDF) - Government guidance on data handling
- [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) - Data integrity in agent systems
