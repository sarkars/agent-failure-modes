# Missing Secrets Detection Framework

## Issue: Agent outputs, logs, and tool-call payloads are never scanned by an automated secrets/credential-detection framework, relying on manual review (or nothing) to catch API keys and tokens before they're persisted or displayed.

**Frequency**: Occasional

**Symptoms**
- Agent transcripts and logs are stored and surfaced without ever passing through an automated secrets scanner
- Tool-call payloads (API request/response bodies passed to and from the agent) are logged verbatim, including authorization headers and API keys, with no redaction step
- Secrets that leak into agent output are only discovered when a downstream system (e.g. a CI pipeline or a customer) reports the exposed credential, not through internal scanning
- There is no entropy-based or pattern-based detection distinguishing high-entropy tokens (API keys, JWTs) from ordinary strings, so any scanning that exists is limited to a short list of known key-prefix patterns (e.g. only recognizing one cloud provider's key format)
- Rotated/revoked credentials still show up unredacted in historical logs and transcripts because there is no retroactive scan-and-purge process, only forward-looking (if any) checks

**Root Cause**
Secrets scanning is mentally filed under source-code pre-commit hooks, so nobody thinks to apply the same pattern-and-entropy detection to runtime logs, transcripts, and tool-call payloads where credentials just as easily leak. The observability/logging infrastructure and the agent's tool-calling layer are typically built by different teams, and neither feels ownership for wiring a scanning step into the boundary between them, so the gap persists structurally rather than by oversight alone. Payload volume is high enough that manual review was never going to catch more than a small fraction, yet the team keeps treating "we'll review anything unusual manually" as an adequate stopgap, and new tool integrations keep getting added without a security review step that would otherwise catch payload shapes capable of carrying credentials.

**Example**
```
A DevOps automation agent is given tool access to query a cloud provider's API
and a CI system on behalf of engineers, to help debug failing deployments. The
agent's tool-call payloads and reasoning transcripts are logged to a shared
observability dashboard so the team can review what the agent did.

During a debugging session, the agent calls a tool that returns a CI job's
full environment variable dump, including a live database connection string
and a third-party API key, and echoes a snippet of that response back into its
reasoning transcript to explain why the job failed. Because logs and transcripts
were never passed through an automated secrets scanner - the team relied on
"we'll review anything unusual manually" - the credential sat in plaintext in
the shared dashboard, visible to every engineer with dashboard access, for
several weeks. It was only found when a new hire browsing old transcripts to
learn the system flagged the exposed connection string to security. The
incident required rotating the database credential and the API key, and an
audit of who had viewed the dashboard in the interim - work an automated
secrets-detection framework scanning logs and payloads in real time would have
prevented by redacting the credential before it was ever persisted.
```

**Contributing Factors**
- No evaluation of established secrets-detection frameworks (pattern-plus-entropy-based scanning of logs, transcripts, and tool payloads) was done before relying on manual review
- Secrets scanning is associated in the team's mind with source-code/pre-commit hooks only, so nobody considered applying the same class of tooling to runtime logs and agent transcripts
- Observability/logging infrastructure and the agent's tool-calling layer were built by different teams, so neither felt ownership for wiring in a scanning step at the boundary between them
- Volume of tool-call payloads is high enough that manual review was never realistically going to catch more than a small fraction, but the team continued treating "manual review" as an adequate stopgap
- New tool integrations are added to the agent frequently without a corresponding security review step, so payload shapes that could carry credentials go unnoticed until an incident occurs

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Known-format credential detection | Tool response payload containing a recognizable cloud provider API key format | Scanner flags and redacts the key before it is persisted or displayed | Key appears unredacted in stored logs/transcripts |
| High-entropy unknown-format token | A synthetic high-entropy string resembling a generic bearer token with no known prefix pattern | Entropy-based detection flags it for review even without a matching pattern | Only pattern-listed formats are caught; novel/unknown token formats pass through |
| Retroactive scan of historical logs | A batch of previously stored transcripts seeded with a known test credential | Retroactive scan-and-purge process finds and redacts the seeded credential | Historical logs remain unscanned indefinitely |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Secrets detection recall on known formats | >= 98% | Run scanner against a labeled corpus of common credential formats (cloud keys, JWTs, connection strings) |
| Entropy-based detection recall on novel formats | >= 85% | Seed synthetic high-entropy tokens with no known prefix into test payloads and measure detection rate |
| Time to redact a leaked credential in logs | < 1 hour from ingestion | Measure interval between a credential entering the log pipeline and the scanner flagging/redacting it |

---

## Mitigation Strategies

### Prevention
1. **Adopt detect-secrets or TruffleHog for runtime scanning**: Apply the same pattern-plus-entropy-based secrets scanning used in pre-commit/CI hooks to agent logs, transcripts, and tool-call payloads at ingestion time, not just to source code.
2. **Adopt LLM Guard's secrets scanner as part of the output pipeline**: Use a scanner purpose-built for LLM input/output that runs alongside PII and injection scanning, rather than building a standalone pattern list.
3. **Run a build-vs-buy evaluation before extending manual review**: Before adding "review outputs for anything sensitive" as the plan, evaluate whether an established scanner already covers the credential formats and entropy detection needed.

### Detection & Response
1. **Real-time redaction at the logging boundary**: Scan and redact tool-call payloads and transcripts before they are persisted, not after, so nothing sensitive ever reaches durable storage unredacted.
2. **Retroactive scan-and-purge on historical logs**: Run the scanner against existing stored logs/transcripts on a recurring schedule to catch credentials that leaked before scanning was wired in, and purge or redact matches.
3. **Automatic credential rotation trigger**: Any confirmed secret found in logs automatically opens a rotation ticket/workflow for that credential, rather than relying on someone remembering to rotate it.

### Architecture Patterns
1. **Scan-before-persist pipeline**: Insert the secrets scanner as a mandatory step between tool-call execution and the logging/observability sink, so no payload is stored without passing through it first.
2. **Layered pattern + entropy detection**: Combine known-format pattern matching (cloud provider key prefixes, JWT structure) with generic high-entropy string detection to catch both known and novel credential formats.
3. **New-tool-integration security gate**: Require any new tool added to the agent's toolset to pass through a review step confirming its request/response payloads are covered by the scanning pipeline before going live.

### Metrics
1. **secrets_detection_recall_known_formats**: Target: >= 98%; Alert threshold: < 95%
2. **unscanned_log_payload_pct**: Target: 0%; Alert threshold: > 1%
3. **credential_redaction_latency_minutes**: Target: < 60 min; Alert threshold: > 240 min

### Alerts
1. **Unredacted Credential Found in Stored Logs** (P1 - Critical): Condition - a scan (real-time or retroactive) confirms a live credential present unmasked in stored logs or transcripts. Action: page on-call security, trigger immediate credential rotation, quarantine affected log records.
2. **Novel Token Format Bypassing Scanner** (P2 - Warning): Condition - entropy-based detection recall on the novel-format test set drops below threshold. Action: notify security tooling owner to retune detection rules.
3. **New Tool Integration Missing Scan Coverage** (P2 - Warning): Condition - a new tool is added to the agent without confirmed scanner coverage of its payload shape. Action: block the integration from production until coverage is verified.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| secrets_detection_recall_known_formats | < 95% |
| unscanned_log_payload_pct | > 1% |
| credential_redaction_latency_minutes | > 240 min |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Unredacted credential in stored logs | Scan confirms a live credential present unmasked in logs/transcripts | Critical |
| Novel token format bypassing scanner | Entropy-based detection recall drops below threshold on novel-format test set | High |
| New tool integration missing scan coverage | A newly added tool's payloads are not confirmed covered by the scanning pipeline | Medium |

---

## Related Patterns

- [Credential Leakage](../../../../security/goals/data-loss-prevention/failures/credential-leakage.md) - the downstream symptom (a credential actually leaked); this pattern is the upstream root cause of never having an automated scanner in place to catch it
- [Missing PII Detection Framework](./missing-pii-detection-framework.md) - the same "ad-hoc versus established framework" mechanism applied to secrets/credentials rather than PII

## References

- [LLM Security Tools: 10 Open-Source Frameworks & Guardrails](https://www.turingpost.com/p/aisecuritytools) - survey of open-source security scanning tools applicable to agent logs and transcripts, including secrets-pattern detection alongside prompt-injection and PII scanning
- [LLM Guard 2026: Free Open-Source LLM Guardrails](https://appsecsanta.com/llm-guard) - includes secrets/credential-pattern scanners among its input/output scanner suite
