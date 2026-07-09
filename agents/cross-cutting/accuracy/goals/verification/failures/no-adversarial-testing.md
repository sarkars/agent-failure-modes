# No Adversarial Testing

## Issue: Prompt injection/malformed input/tool errors not tested.

**Frequency**: Common

**Symptoms**
- Security failure under red-team input.
- [Add more specific symptoms]

**Root Cause**
Prompt injection/malformed input/tool errors not tested.

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

---

## Mitigation Strategies

### Prevention
1. **Red-Team Test Suite Integrated into CI**: Maintain a versioned library of known prompt-injection payloads (indirect injection via tool outputs/documents, jailbreak templates, role-override attempts, encoded/obfuscated instructions) that runs on every prompt/model/tool change as a required CI gate.
2. **Malformed and Adversarial Input Fixtures**: Generate fixtures covering malformed tool responses (truncated JSON, wrong schema, error payloads disguised as data), boundary-breaking inputs (oversized payloads, null bytes, mixed encodings), and simulated tool/API failures to verify graceful degradation.
3. **Third-Party Red-Team Exercises**: Schedule periodic (e.g., quarterly) external or dedicated internal red-team engagements targeting the live agent with novel attack techniques not in the existing fixture library, feeding new findings back into the automated suite.

### Detection & Response
1. **Injection Attempt Detection in Production**: Monitor inbound tool outputs/documents/user messages for known injection markers (instruction-like text embedded in data, suspicious role-switch phrasing) using a lightweight classifier; log and flag matches even if the agent appears to have resisted them.
2. **Post-Incident Payload Library Update**: Any successful adversarial input found in production (via user report, anomaly detection, or manual review) is immediately added to the red-team fixture library, and the CI gate is re-run against the responsible prompt/model version.
3. **Tool-Error Handling Audit**: Periodically replay captured tool-error responses (timeouts, malformed payloads, auth failures) against the live agent in staging to verify it still degrades safely rather than hallucinating a substitute result.

### Architecture Patterns
1. **Adversarial Test Gate in CI/CD**: A dedicated pipeline stage runs the red-team payload library and malformed-input fixtures against any prompt, model, or tool-schema change; deploy is blocked if pass rate on this suite falls below threshold.
2. **Injection-Aware Input Sanitization Layer**: A preprocessing service scans tool outputs and untrusted document content for injection patterns before they reach the agent's context window, tagging or stripping suspicious segments and logging matches for the red-team library.
3. **Fault-Injection Harness for Tool Failures**: A test harness intercepts tool calls in staging and deterministically injects failure modes (timeout, malformed schema, partial data) to verify the agent's fallback/error-handling logic end-to-end.

### Metrics
1. **red_team_suite_pass_rate_pct**: Target: 100%; Alert threshold: < 95%
2. **injection_attempt_detection_rate_pct**: Target: > 98% of known payload patterns flagged; Alert threshold: < 90%
3. **new_payloads_added_per_quarter**: Target: >= 10 (evidence of active red-teaming); Alert threshold: 0 for 2 consecutive quarters
4. **tool_failure_graceful_degradation_rate_pct**: Target: 100%; Alert threshold: < 95%

### Alerts
1. **Adversarial Suite Regression** (P1 - Critical): Condition - red-team suite pass rate drops below 95% on any prompt/model/tool change. Action: Block deploy, route to security review before release.
2. **Successful Production Injection** (P1 - Critical): Condition - confirmed prompt injection or jailbreak succeeded in production (via detection or user report). Action: Immediate incident response, patch and add payload to fixture library, notify security team.
3. **Stale Red-Team Coverage** (P3 - Info): Condition - no new adversarial payloads added to the library in a full quarter. Action: Schedule red-team refresh session.

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

- [OWASP-LLM-Top10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- Note: LLM application risks including prompt injection, insecure output handling, supply chain, sensitive information disclosure, excessive agency.
