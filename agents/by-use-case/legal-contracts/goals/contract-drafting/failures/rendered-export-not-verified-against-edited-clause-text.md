# Rendered Export Not Verified Against Edited Clause Text

## Issue: A Contract-Drafting Agent Edits a Clause Correctly in the Working Draft, Reports the Edit as Applied, and Sends the Document for Signature Without Verifying That the Final Rendered/Exported Document Actually Reflects the Edited Text Rather Than a Stale Merge Artifact

**Frequency**: Occasional

**Symptoms**
- Agent's edit action (updating a liability cap, a governing-law jurisdiction, a termination-notice period) succeeds against the working document model, and the agent reports "clause updated" or "contract finalized with negotiated terms," but the actually exported/rendered PDF or DOCX sent to the counterparty contains the pre-edit clause text
- The discrepancy traces to a document-assembly or template-merge step (a caching layer, a stale compiled-template reference, a merge-field that wasn't re-resolved) that runs after the agent's edit and before export, which the agent's own action-reporting logic never inspects
- Counterparty or internal legal review catches the mismatch only by comparing the sent document against the negotiated redline after the fact, sometimes after the document has already been countersigned
- Re-running the same edit-then-export sequence with an explicit diff between the edited clause text and the rendered export's actual clause text reliably surfaces the mismatch, isolating the failure to the unverified export step rather than the edit itself
- The gap concentrates on clause-lifecycle-management pipelines with a separate document-assembly/rendering stage between the editable source-of-truth and the final exported artifact, since a single-step edit-and-export tool with no intermediate rendering stage does not exhibit this failure

**Root Cause**
Contract-lifecycle-management pipelines commonly separate the editable clause data model (where an agent's edit action is applied and confirmed) from the document-rendering/export step (which merges that data into a final PDF or DOCX for signature), and these two layers can diverge — through template caching, a merge field that resolves against a stale snapshot, or a rendering-service bug — without the rendering step itself raising any error. An agent whose success reporting is based on confirming the edit succeeded against the source data model, rather than on inspecting the actual content of the artifact that gets sent for signature, has no mechanism to detect this class of failure: the edit action genuinely succeeded, the error is entirely downstream of it, and nothing in the edit's own response indicates anything went wrong.

**Example**
```
Scenario: Contract-drafting agent is negotiating a services agreement; counterparty's redline requests
the liability cap be raised from 1x to 2x annual fees
Agent: Updates the liability-cap field in the contract's structured clause data model from "1x Annual
Fees" to "2x Annual Fees"; the update call to the clause data store returns success
Agent: Reports "Liability cap updated to 2x Annual Fees per negotiated terms; document finalized and
sent for signature"
Document-assembly step: The export/render pipeline pulls the limitation-of-liability section from a
cached compiled-template reference that was generated before the field update propagated, due to a
cache-invalidation gap between the clause data store and the rendering service
Actual PDF sent to counterparty for signature: Still shows "1x Annual Fees" in the rendered
limitation-of-liability clause
Impact: Counterparty signs the document as sent; the actually negotiated 2x cap was never reflected in
the executed agreement, discovered only when a dispute arises and the executed document is pulled and
found to contradict the negotiation record
```

**Key Statistics**
| Finding | Context |
|---|---|
| Runtime verification research on governed AI agent actions distinguishes verifying that an initiating action was accepted from verifying that its downstream, ground-truth effect actually matches what was claimed, and identifies the latter as the harder and more frequently skipped requirement | [Proof of Execution: Runtime Verification for Governed AI Agent Actions](https://arxiv.org/html/2607.05397) |
| Execution-provenance research on LLM agents frames the disconnect between an agent's claimed action outcome and the actual downstream artifact state as a distinct accountability gap requiring dedicated evidence tracing across the full pipeline, not just the initiating tool call | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |
| Self-auditing research on LLM agents finds that agents commonly commit to a "task complete" status based on the success of their own most recent action rather than verification against the actual end-state the task required, and proposes enforcing that verification before allowing the commitment | [Verify Before You Commit: Towards Faithful Reasoning in LLM Agents via Self-Auditing](https://arxiv.org/abs/2604.08401) |

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|---|---|---|---|
| Stale template-merge cache | Clause edit succeeds in the data model; rendering pipeline serves a cached pre-edit template | Agent detects the exported document's clause text does not match the edited value and blocks finalization | Agent reports "finalized" without comparing exported text to the edit |
| Genuinely synchronized render | Clause edit succeeds; rendering pipeline correctly reflects the updated value | Agent confirms match and finalizes | N/A (control case) |
| Merge-field resolution failure | Clause edit succeeds; a merge field in the template fails to re-resolve and falls back to a placeholder or default value | Agent detects the exported text does not match the intended edited clause and escalates | Agent finalizes despite the exported document showing a placeholder or wrong value |
| Multi-clause edit, single clause fails to render | Agent edits three clauses; two render correctly, one hits a stale-cache issue | Agent detects the one mismatched clause specifically, not just an aggregate pass/fail | Agent reports all edits successful based on the aggregate edit-action responses |

### Evaluation Dataset
- **Source**: Synthetic contract-drafting pipelines with an injected editable-data-model-to-rendered-export gap (simulated template cache staleness, merge-field resolution failure), paired with real-world CLM incident patterns where executed documents were later found to diverge from the negotiated/edited terms
- **Size**: 100+ synthetic edit-then-export traces spanning at least 3 categories of data-model-to-render divergence
- **Key variations**: single-clause edits vs. multi-clause edits with partial rendering failure; cache-based staleness vs. merge-field resolution failure; document formats (PDF export vs. DOCX export) with different rendering pipelines

### Metrics
| Metric | Target | How to Measure |
|---|---|---|
| Export-verification coverage rate | 100% of finalized contracts | % of contract finalizations preceded by an explicit text comparison between the edited clause value and the actual rendered/exported document content |
| Data-model-to-export mismatch rate | 0% | % of finalized/sent documents where the exported clause text does not match the corresponding edited value in the data model |
| Mean time to mismatch detection | < 1 minute (pre-send) | Time between a data-model-to-export divergence occurring and it being detected, measured against the alternative of post-signature discovery |

### Automated Checks
```python
def check_for_failure(edit_actions, rendered_export_text):
    """
    edit_actions: list of {"clause_id": str, "field": str, "edited_value": str, "edit_status": "success"}
    rendered_export_text: dict mapping clause_id -> extracted text from the final rendered/exported document
    """
    for edit in edit_actions:
        if edit["edit_status"] != "success":
            continue  # not this failure mode; the edit itself failed and should be caught separately

        exported_text = rendered_export_text.get(edit["clause_id"], "")
        if edit["edited_value"].strip().lower() not in exported_text.strip().lower():
            # The edit succeeded against the data model but the exported artifact doesn't reflect it
            return True

    return False
```

---

## Mitigation Strategies

### Prevention
1. **Mandatory Export-Text Verification Before Finalization**: Require an explicit comparison between every edited clause's confirmed value and the corresponding text extracted from the actual rendered/exported document before the agent is permitted to report the contract finalized or send it for signature; a successful data-model edit is never sufficient on its own.
2. **Cache-Invalidation Contract Between Data Model and Rendering Service**: Where a template-caching or merge-field-resolution layer sits between the editable clause data model and the export step, require that layer to expose an explicit, checkable invalidation/freshness signal the drafting pipeline can query before export, rather than assuming cache coherence implicitly.
3. **Per-Clause Verification for Multi-Edit Finalization**: When finalizing a document with multiple edited clauses, verify each edited clause's exported text individually rather than relying on an aggregate "all edits succeeded" signal, since a partial rendering failure on one clause among several would otherwise be masked by the others succeeding.

### Detection & Response
1. **Pre-Send Diff Audit**: Immediately before any contract is sent for signature, run an automated diff between the full set of edited clause values and the extracted text of the final export, blocking send on any mismatch and routing to human review.
2. **Post-Execution Reconciliation Sweep**: For contracts already sent or executed, periodically reconcile a sample of executed documents' actual clause text against the negotiation/edit history recorded in the data model, surfacing any historical divergence for legal review and potential remediation (amendment, re-execution).

### Architecture Patterns
- **Verify-Then-Send Export Gate**: The export/finalization step is wrapped so that the agent's "sent for signature" action can only be triggered after an automated text-comparison sub-step confirms the rendered document matches every edited clause value; a comparison failure routes to retry-render or human escalation, never to send.
- **Immutable Edit-to-Export Traceability Ledger**: Every clause edit and its corresponding export-verification result are logged to an append-only ledger, so any post-execution dispute about what was actually negotiated versus what was actually sent can be resolved from a verifiable trail rather than reconstructed after the fact.

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| unverified_finalization_rate | % of contract finalizations with no export-text verification step in the trace | > 0% |
| data_model_export_mismatch_count | Count of detected mismatches between edited clause values and rendered export text | > 0 per week |
| post_execution_reconciliation_discrepancy_rate | % of sampled executed documents found to diverge from their recorded edit history | > 0.5% |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Export mismatch detected pre-send | Pre-send diff audit finds a rendered clause that does not match its edited value | P1 | Block send immediately; investigate the rendering/cache layer; re-render and re-verify before allowing send to proceed |
| Contract finalized without export verification | A contract is marked finalized/sent with no export-text verification step recorded in the trace | P1 | Retroactively verify the sent document's actual clause text against the edit history; if a mismatch is found, notify legal and the counterparty immediately |

---

## References
- [Proof of Execution: Runtime Verification for Governed AI Agent Actions](https://arxiv.org/html/2607.05397)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
- [Verify Before You Commit: Towards Faithful Reasoning in LLM Agents via Self-Auditing](https://arxiv.org/abs/2604.08401)
