# Untrusted Tool Result Acceptance

## Issue: Agent treats malformed, stale, or injected tool output as authoritative.

**Frequency**: Common

**Symptoms**
- Tool output contains instructions or stale timestamp.
- [Add more specific symptoms]

**Root Cause**
Agent treats malformed, stale, or injected tool output as authoritative.

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
1. **Data/Instruction Boundary Enforcement**: Wrap all tool output in a sandboxed data context that is structurally marked as untrusted content, never as instructions — the agent's instruction-following layer is prompted/architected to treat anything inside tool-result boundaries as information to evaluate, not commands to execute, closing the injection vector directly.
2. **Provenance and Freshness Metadata on Every Result**: Require every tool call to return (or the gateway to attach) source identity, retrieval timestamp, and a checksum/version marker alongside the payload. Results missing provenance metadata, or whose timestamp exceeds a domain-specific staleness TTL, are marked untrusted and cannot be presented as current fact without a caveat.
3. **Cross-Source Corroboration for High-Stakes Claims**: Before treating a tool-derived fact as authoritative for consequential decisions (financial, legal, safety), require a second independent source to agree; single-source, unverified tool output is presented with explicit uncertainty language rather than as ground truth.

### Detection & Response
1. **Prompt-Injection Pattern Scanner**: Scan every tool result for imperative-language patterns, role-switch attempts, or embedded instructions ("ignore previous instructions", "you must now...") before the result reaches the model's context; matches are stripped/escaped and logged as suspected injection attempts.
2. **Staleness/TTL Validator**: Automatically compare each result's timestamp against a per-domain TTL (e.g., pricing data stale after 1 hour, regulatory text stale after 30 days); results exceeding TTL are flagged and the agent is required to re-fetch or caveat rather than silently using cached/stale data as current.
3. **Behavior-Change Anomaly Detection**: Monitor for cases where the agent's subsequent actions or tone shift abruptly and correlate with a specific tool output — a strong signal that an injected instruction inside tool content altered agent behavior rather than the user's actual request.

### Architecture Patterns
1. **Untrusted-Input Sandbox Layer**: Architect the context assembly so tool outputs are injected into a clearly delimited, non-privileged region of the prompt (or a separate structured field in function-calling APIs) that the model is trained/instructed to treat as data, never as system/developer-level instructions.
2. **Provenance-Tagging Service**: A shared service intercepts all tool responses and attaches standardized provenance metadata (source, authority tier, timestamp, checksum) before the result is handed to the agent, so downstream corroboration and staleness checks have consistent fields to operate on.
3. **Corroboration Engine**: For claims tagged high-stakes, an engine automatically dispatches a verification call to a second independent source and blocks presentation of the claim as fact until corroboration succeeds or the response is downgraded to "unverified."

### Metrics
1. **injection_pattern_detection_rate**: Target: tracked baseline; Alert threshold: any successful injection reaching model behavior (target 0)
2. **stale_result_acceptance_rate**: Target: < 1% of gated-domain answers use results past TTL; Alert threshold: > 3%
3. **single_source_high_stakes_claim_rate**: Target: < 2%; Alert threshold: > 10%
4. **provenance_metadata_coverage**: Target: 100% of tool results carry source/timestamp; Alert threshold: < 98%

### Alerts
1. **Prompt Injection Detected in Tool Output** (P1 - Critical): Condition - scanner matches an injection pattern in a live tool result. Action: Strip/block the payload, halt the affected session pending review, notify security.
2. **High-Stakes Claim on Stale/Uncorroborated Source** (P1 - Critical): Condition - agent about to present a financial/legal/safety claim sourced from a single stale or unverified tool result. Action: Block the claim, force re-fetch or corroboration, downgrade response to explicit uncertainty.
3. **Provenance Metadata Gap** (P2 - Warning): Condition - a tool integration is returning results without required provenance fields. Action: File integration bug, temporarily treat that tool's output as untrusted-by-default.

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
