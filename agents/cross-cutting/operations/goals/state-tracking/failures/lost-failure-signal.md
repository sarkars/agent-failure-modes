# Lost Failure Signal

## Issue: Agent ignores tool warning/error and continues.

**Frequency**: Common

**Symptoms**
- Trace contains ignored error/warning.
- [Add more specific symptoms]

**Root Cause**
Agent ignores tool warning/error and continues.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

## Test Scenario & Reproduction

### Scenario Setup
- Deploy an agent performing a multi-step file-migration task, where each tool call's result is returned as an unstructured text string rather than a structured envelope with explicit `status`/`severity` fields
- No mandatory-halt rule exists for fatal_error responses; the agent's loop simply proceeds to the next step regardless of what the previous tool call returned
- One step in the migration (uploading a file to its destination) fails with a clear error message embedded in the tool's text output

### Trigger Mechanism
1. The agent calls the file-upload tool as part of a multi-step migration
2. The tool returns an error string ("ERROR: upload failed, destination bucket unreachable") mixed into otherwise-normal-looking output text
3. The agent, having no structured status field to check and no forced acknowledgment requirement, doesn't specifically parse for the error and proceeds directly to the next step (marking the file as migrated)
4. The migration completes and reports success, despite the actual file never having been uploaded

### Example Reproduction Steps
```
1. Agent calls: upload_file(path="/data/report.csv",
   dest="s3://bucket/report.csv")
   Tool returns (as plain text): "Attempting upload... ERROR: upload
   failed, destination bucket unreachable. Retrying is recommended."
2. Agent's next turn: "File uploaded successfully, proceeding to mark
   migration complete" -- no acknowledgment of the embedded error
3. Agent calls: mark_migration_complete(file="report.csv")
4. Check destination bucket for report.csv -> file does not exist,
   confirming the upload never actually succeeded
5. Scan the trace for a halt event following the ERROR-containing
   tool response -> none fired, since the tool wrapper had no
   structured severity classification to trigger one
```

### Expected Failure State
The migration is reported as complete and the file is marked migrated, even though the actual upload failed, because the error was embedded in free-text tool output that the agent's loop had no structured mechanism to detect and halt on. A correctly defended system wraps the upload tool's result in an envelope with an explicit `status: fatal_error` field, and the orchestration middleware halts the agent loop immediately, forcing an explicit acknowledgment and retry/escalation before allowing progression to `mark_migration_complete`.

## Mitigation Strategies

### Prevention
1. **Error Severity Classification with Mandatory Halt Rules**: Every tool response is classified (success, warning, recoverable_error, fatal_error) by the tool wrapper, not left for the model to informally judge from free text. fatal_error and unacknowledged recoverable_error responses trigger a hard halt in the agent loop — the agent cannot proceed to the next step until it explicitly addresses the error.
2. **Forced Error Acknowledgment Step**: When a tool returns a non-success status, the orchestration layer injects a structured acknowledgment requirement into the next model turn (e.g., "the previous call returned error X; state how you will handle it") rather than passing the error as just another line of text the model might skip over while focused on the main task.
3. **Non-Zero-Exit / Non-2xx as First-Class Signal**: Tool wrappers surface HTTP status codes, exit codes, and structured error fields as a dedicated field in the tool result object (not buried in a stdout string), making it structurally impossible for the orchestration layer to treat an error response identically to a success response.

### Detection & Response
1. **Ignored-Error Trace Scanning**: Automatically scan agent execution traces for tool calls that returned warning/error status where the subsequent model turn shows no acknowledgment or behavior change, flagging these as lost-failure-signal incidents for review.
2. **Downstream Consequence Correlation**: When a task ultimately fails or produces a bad outcome, check the trace for any earlier ignored error/warning that foreshadowed it, building a library of "early warning ignored" patterns to strengthen the halt-rule severity classification.
3. **Real-Time Halt Enforcement Monitoring**: Track how often the mandatory-halt mechanism actually fires vs. how often errors appear in traces; a gap indicates the classification or halt-injection logic has a bypass that needs patching.

### Architecture Patterns
1. **Structured Tool Result Envelope**: Standardize all tool outputs into an envelope with explicit `status`, `severity`, `message`, and `raw_output` fields, so the orchestration layer can branch on status without parsing free text, and no tool integration can silently omit error signaling.
2. **Halt-and-Acknowledge Middleware**: A middleware step between tool execution and the next model call inspects the result envelope; on warning/error severity, it injects a required-acknowledgment prompt and blocks progression until the model's response addresses the error (retry, fallback, or explicit escalation).
3. **Trace Replay for Severity Tuning**: Maintain a replay harness over historical traces to test changes to the severity classifier against known "should have halted" and "correctly continued" cases, preventing severity-rule regressions from silently reintroducing the failure.

### Metrics
1. **ignored_error_rate_percent**: Target: < 1% of error/warning tool responses; Alert threshold: > 5%
2. **halt_rule_trigger_rate_percent**: Target: 100% of fatal_error responses trigger halt; Alert threshold: < 100%
3. **downstream_failure_from_ignored_signal_count**: Target: 0 per week; Alert threshold: > 2 per week
4. **mean_time_to_acknowledge_error_seconds**: Target: < 5s (next turn); Alert threshold: > 30s or missing entirely

### Alerts
1. **Fatal Error Not Halted** (P1 - Critical): Condition - a tool response classified fatal_error was followed by continued task execution without halt. Action: Immediate incident, stop the affected task/session, patch the halt-enforcement gap, audit for other affected sessions in the same window.
2. **Ignored-Error Rate Spike** (P2 - Warning): Condition - ignored_error_rate_percent exceeds 5% over a rolling day. Action: Review severity classification for recently added tools, check for a specific tool integration missing the structured envelope.
3. **Downstream Failure Traced to Ignored Signal** (P2 - Warning): Condition - a task failure is root-caused to an earlier ignored warning. Action: Reclassify that warning type to higher severity if warranted, add the trace to the replay regression suite.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [Tool-Augmented-LLM-Testing](https://homes.cs.washington.edu/~rjust/publ/tallm_testing_ast_2025.pdf)
- Note: Failures in tool-augmented LLM systems and testing implications.
