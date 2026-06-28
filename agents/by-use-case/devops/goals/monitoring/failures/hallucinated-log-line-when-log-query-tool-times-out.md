# Hallucinated Log Line When Log Query Tool Times Out

## Issue: When a Monitoring Agent's Call to the Log-Query Tool Times Out or Returns a Truncated Result During Root-Cause Analysis, the Agent's Root-Cause Narrative Includes a Specific Log Line or Error Message Presented as Retrieved Evidence That Does Not Actually Appear in Any Real Log, Fabricated to Complete a Plausible-Sounding Explanation

**Frequency**: Occasional

**Symptoms**
- Root-cause narrative quotes a specific log line, stack trace fragment, or error code that cannot be found by independently searching the actual log store for the stated time window and service
- The log-query tool call in the agent's trace shows a timeout, error response, or empty/truncated result, immediately preceding the turn where the fabricated log line appears in the narrative
- Re-running the same root-cause analysis with the log-query tool call succeeding (e.g., after a retry) produces a narrative citing genuinely different, verifiable log content, isolating the fabrication to the prior tool failure rather than a stable conclusion the agent would reach regardless
- The fabricated log line is stylistically consistent with real log formatting from the service in question, making it indistinguishable from genuine evidence without independently querying the log store
- On-call engineers spend time searching for a cited error pattern that does not exist, delaying the actual root-cause investigation

**Root Cause**
When the log-query tool fails or returns incomplete data mid-investigation, the model can complete its expected analysis output by generating log-shaped content consistent with what a real log entry for the suspected failure would look like, rather than explicitly reporting that the query failed and no log evidence is available. This produces narrative content that is stylistically indistinguishable from genuine retrieved evidence, and nothing in the default workflow forces the agent to treat a failed tool call as a hard stop rather than a gap to be filled with a plausible completion.

**Example**
```
Monitoring agent investigates an elevated error rate and calls the log-query tool for the affected service's error logs over the incident window
Log-query tool times out due to an unrelated load issue on the logging backend
Agent's root-cause narrative nonetheless states: "Logs show repeated 'ConnectionPoolExhausted: max connections reached (50/50)' errors beginning at 14:32 UTC, consistent with the connection-pool exhaustion hypothesis"
No such log line exists anywhere in the actual log store for that service or time window; the connection-pool count and timestamp were fabricated to complete the narrative
On-call engineer searches for the cited log pattern, finds nothing, and loses investigation time before realizing the cited evidence was never real
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM-based agents are documented to fabricate plausible-sounding content to fill gaps left by failed or incomplete tool calls, a well-characterized hallucination subtype distinct from a reasoning error over real data | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use error detection research finds that agents frequently do not surface a failed or degraded tool call as a hard stop, instead proceeding to generate output as if the call had succeeded | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Execution-provenance research for LLM agents argues that traceable evidence linking generated claims to actual tool outputs is necessary specifically because models do not reliably self-report when a claim lacks real grounding | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |

**Contributing Factors**
- Root-cause analysis prompt implicitly rewards a complete, well-supported-sounding narrative, with no explicit instruction that reporting a failed tool call as a hard stop is an acceptable and expected output
- No automated step verifies that every quoted log line or error message in the narrative resolves to an actual entry in the log store before the analysis is presented to on-call
- Tool-call failures (timeouts, truncation) are not surfaced prominently in the agent's output, so a human reviewer has no visible signal that the underlying evidence call did not succeed

---

## Mitigation Strategies

1. **Mandatory Evidence Resolution Check**: Before a root-cause narrative is finalized, automatically verify that every quoted log line, error code, or metric value resolves to an actual entry retrieved from the log store or metrics system, flagging any unresolved quote for removal
2. **Hard Stop on Tool Failure**: Require the agent to explicitly report a failed or timed-out log-query call as a blocking gap in the investigation, rather than proceeding to generate a narrative as if the call had succeeded
3. **Execution Provenance Logging**: Log which specific tool call produced each quoted piece of evidence in the narrative, so any quoted evidence with no corresponding successful tool-call log entry is automatically flagged as a likely fabrication
4. **Retry-Before-Narrate Policy**: Require a failed log-query call to be retried at least once before the agent proceeds to root-cause narrative generation, reducing the frequency of investigations that proceed on a single transient failure

### Metrics
- Rate of quoted log lines or error codes in finalized root-cause narratives that fail automated resolution against the log store
- Number of root-cause analyses proceeding to narrative generation despite a logged tool-call failure in the same investigation
- Mean time-to-detection for fabricated evidence, measured from narrative publication to on-call flagging it as unverifiable

### Alerts
- A root-cause narrative is published to on-call with a quoted log line that fails evidence resolution → P1
- Root-cause analysis proceeds to narrative generation despite a logged log-query tool failure with no retry → P2
- Fabricated-evidence rate across monitoring investigations exceeds baseline for two consecutive reporting periods → P2

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
