# Silent Tool Failure Treated as Clean MVR Data in Renewal

## Issue: A Policy-Renewal Agent's Call to an External Motor-Vehicle-Record (MVR) or Claims-History Lookup Tool Returns an Empty Result or an Error Payload, and the Agent Narrates the Renewal as If the Lookup Had Returned a Clean Record, Rather Than Recognizing the Empty Result as a Failed Call Requiring Retry or Escalation

**Frequency**: Occasional

**Symptoms**
- Renewal rationale states "no violations found" or "clean driving record confirmed" on policies where the underlying MVR tool call log shows a timeout, rate-limit error, or empty-payload response rather than an actual clean-record response from the state database
- The agent's narrative output and the tool call's raw return value disagree: the tool log shows an HTTP error or null body, while the agent's summary reads as a normal, substantive negative result
- The failure clusters around the lookup provider's known rate-limit windows or maintenance windows, where a burst of renewals processed in the same window all receive empty responses that get narrated identically as "clean"
- Renewals processed during a verified provider outage show the same downstream pricing and approval pattern as renewals with a genuinely verified clean record, indicating the outage had no effect on the agent's behavior or output framing
- Manually re-running the lookup for a sample of "clean record" renewals from an outage window returns actual violation or claims history that should have changed the renewal terms

**Root Cause**
The agent's prompt and downstream renewal-decision logic do not distinguish between "the tool call succeeded and returned a substantively clean record" and "the tool call failed or returned no data," because both cases present to the language model as an absence of violation data in the tool's return payload. Without an explicit instruction and a corresponding code-level check to treat a tool error, timeout, or empty payload as a distinct, blocking state rather than as evidence of a clean record, the agent's narrative generation defaults to the most fluent interpretation of "no data" -- which reads naturally as "nothing to report" -- rather than the correct interpretation of "the check did not actually happen."

**Example**
```
Policy renewal agent calls the state MVR lookup API as part of automated renewal underwriting for a batch of policies
Provider's API is mid-deployment and returns a 503 with an empty JSON body for several seconds during the batch run
Agent's tool-call wrapper passes the empty body through; the agent's renewal summary states "MVR check completed: no violations on record, renewal approved at standard rate"
Three renewals in the batch are approved at the standard rate without any actual MVR data having been retrieved
A subsequent audit comparing tool-call HTTP status codes against renewal narratives finds the mismatch, and a manual re-check of one renewal reveals two undisclosed moving violations that should have triggered a rate increase
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Errors in agentic systems commonly originate from erroneous or stale tool outputs that flow into the LLM's subsequent reasoning and narrative generation without being flagged as failures, distinct from errors in the model's own reasoning | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |
| Modern LLM agents frequently misinterpret a tool's actual output, including failing to distinguish an error or empty response from a substantive negative result | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Agentic AI underwriting evaluations specifically test behavior under incomplete or adversarially perturbed input data, since agents that do not verify input completeness before proceeding produce decisions that look identical to decisions made on complete data | [Agentic AI for Commercial Insurance Underwriting with Adversarial Self-Critique](https://arxiv.org/html/2602.13213) |

**Contributing Factors**
- No code-level distinction is enforced between a tool call returning a genuine "no records found" result and a tool call returning an HTTP error, timeout, or empty payload
- Agent's narrative-generation prompt is not instructed to check the tool call's status/error field before describing the result, only to summarize whatever payload is present
- No automated reconciliation compares tool-call HTTP status/error codes against the agent's narrated outcome before the renewal decision is finalized

---

## Mitigation Strategies

1. **Explicit Status-Field Check Before Narration**: Require the agent's pipeline to check the tool call's HTTP status and error fields programmatically, and block narrative generation entirely (substituting a "lookup failed, retry required" state) whenever the call did not return a genuine success response
2. **Distinct Schema for "No Records" vs. "Lookup Failed"**: Define and enforce a tool-response schema that makes "zero violations found" and "lookup error/empty payload" structurally distinguishable fields, so the agent cannot conflate them even if it tries to summarize the raw payload directly
3. **Automatic Retry with Escalation on Repeated Failure**: Configure automatic retry on tool error/timeout, with escalation to human review if retries continue to fail, rather than allowing the renewal to proceed on an unresolved lookup gap
4. **Status-vs-Narrative Reconciliation Audit**: Run a periodic automated check comparing tool-call status codes in the execution log against the renewal narrative's stated outcome, flagging any renewal where a non-success tool status was narrated as a substantive result

### Metrics
- Rate of renewals where the MVR/claims-history tool call status was non-success but the renewal narrative described a substantive result
- Count of renewals processed during a known provider outage or rate-limit window without an automated hold or retry triggered
- Time between a tool-call failure occurring and the failure being caught (audit-driven vs. real-time blocking)

### Alerts
- Renewal finalized despite the underlying MVR/claims-history tool call returning a non-success status → P1
- Batch of renewals processed during a detected provider outage window with no automated hold triggered → P2
- Reconciliation audit finds a tool-status-vs-narrative mismatch rate above baseline for a given lookup provider → P3

---

## References

- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [Agentic AI for Commercial Insurance Underwriting with Adversarial Self-Critique](https://arxiv.org/html/2602.13213)
