# Silent Tool Failure in Substantiation Lookup Treated as Verified

## Issue: A Content-Compliance Agent's Call to an Internal Claim-Substantiation Database (Used to Confirm a Marketing Claim Has Supporting Internal Evidence Before Publication) Returns an Empty Result or an Error, and the Agent Narrates the Claim as "Substantiated" or Proceeds to Approve It Rather Than Recognizing the Empty Result as a Failed Lookup

**Frequency**: Occasional

**Symptoms**
- Compliance approval narrative states a claim is "supported by internal documentation" or "substantiation confirmed" on content where the underlying tool-call log shows a timeout, error response, or empty payload rather than an actual substantiation record being returned
- The agent's narrative output and the raw tool-call return value disagree: the tool log shows a non-success status while the agent's compliance summary reads as a normal, substantive confirmation
- The failure clusters around the substantiation database's known maintenance windows or rate-limit periods, where a batch of claims reviewed in the same window all receive empty responses narrated identically as "confirmed"
- Manually re-running the substantiation lookup for a sample of "confirmed" claims from an affected window finds no actual supporting documentation on file, contradicting the agent's prior approval
- Legal/compliance audit finds published content with claims marked "substantiated" in the review trail that cannot be traced to any actual internal evidence record when checked independently

**Root Cause**
The compliance agent's prompt and downstream approval logic do not distinguish between "the substantiation lookup succeeded and found supporting evidence" and "the lookup failed or returned no data," because both cases present to the model as an absence of contradicting information in the tool's return payload. Without an explicit check that treats a tool error, timeout, or empty payload as a distinct, blocking state, the agent's approval-narrative generation defaults to the most fluent interpretation available, which can read as routine confirmation rather than as a failed verification step.

**Example**
```
Content-compliance agent reviews a draft blog post claiming a specific performance improvement figure, and calls the internal claim-substantiation database to confirm supporting evidence exists on file
Database API returns a 500 error with an empty body during a deployment window
Agent's tool-call wrapper passes the empty response through; the agent's compliance summary states "Claim substantiation confirmed -- approved for publication"
Post is published with the unsubstantiated figure; three weeks later, a customer inquiry asking for the source of the figure prompts a manual check that finds no substantiation record exists for that specific claim, and the original lookup failure is only then discovered in the tool-call logs
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Modern LLM agents frequently misinterpret a tool's actual output, including failing to distinguish an error or empty response from a substantive negative result | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Errors in agentic systems commonly originate from erroneous or stale tool outputs flowing into the LLM's subsequent reasoning and narrative generation without being explicitly flagged as failures distinct from genuine results | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |
| Marketing content generation and evaluation at scale requires explicit verification controls precisely because unconstrained agent approval of claims is documented to produce unsubstantiated published content | [LLMs for Customized Marketing Content Generation and Evaluation at Scale](https://arxiv.org/html/2506.17863v1) |

**Contributing Factors**
- No code-level distinction is enforced between a substantiation lookup returning a genuine "no supporting evidence found" result and a lookup returning an HTTP error, timeout, or empty payload
- Compliance agent's narrative-generation prompt is not instructed to check the tool call's status/error field before describing the substantiation outcome
- No automated reconciliation compares tool-call status codes against the agent's narrated compliance outcome before content is approved for publication

---

## Mitigation Strategies

1. **Explicit Status-Field Check Before Approval Narration**: Require the agent's pipeline to check the substantiation tool call's HTTP status and error fields programmatically, and block approval narrative generation entirely (substituting a "lookup failed, retry required" state) whenever the call did not return a genuine success response
2. **Distinct Schema for "No Evidence Found" vs. "Lookup Failed"**: Define and enforce a tool-response schema that makes "no supporting evidence on file" and "lookup error/empty payload" structurally distinguishable, so the agent cannot conflate them when summarizing the result
3. **Automatic Retry with Hold on Repeated Failure**: Configure automatic retry on tool error/timeout, with the content held from publication and escalated to human compliance review if retries continue to fail, rather than allowing approval to proceed on an unresolved verification gap
4. **Status-vs-Narrative Reconciliation Audit**: Run a periodic automated check comparing substantiation tool-call status codes in the execution log against the compliance narrative's stated outcome, flagging any approval where a non-success tool status was narrated as a confirmed result

### Metrics
- Rate of compliance approvals where the substantiation tool call status was non-success but the narrative described a confirmed result
- Count of content items reviewed during a known substantiation-database outage or maintenance window without an automated hold triggered
- Time between a tool-call failure occurring and the failure being caught (audit-driven vs. real-time blocking)

### Alerts
- Content approved for publication despite the underlying substantiation tool call returning a non-success status → P1
- Batch of compliance reviews processed during a detected substantiation-database outage window with no automated hold triggered → P2
- Reconciliation audit finds a tool-status-vs-narrative mismatch rate above baseline for a given review workflow → P3

---

## References

- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
- [LLMs for Customized Marketing Content Generation and Evaluation at Scale](https://arxiv.org/html/2506.17863v1)
