# Memory Poisoning

## Issue: Malicious or wrong content gets stored and later trusted.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Stored memory contains instructions or unverified claims.
- [Add more specific symptoms]

**Root Cause**
Malicious or wrong content gets stored and later trusted.

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
1. **Write-Time Provenance and Sanitization Gate**: Every candidate memory write is tagged with its source (user_direct_statement, tool_output, third_party_document, inferred) and passed through a sanitizer that strips imperative/instruction-like language ("ignore previous instructions", "always respond with...") before storage. Content originating from untrusted external sources (fetched web pages, documents, tool results) is never stored as a trusted fact without explicit user confirmation.
2. **Instruction-vs-Fact Classification**: A classifier screens content proposed for memory storage and rejects or quarantines anything that reads as an instruction/directive rather than a factual statement about the user or world, since legitimate memories are facts to recall, not commands to execute later.
3. **Trust-Tiered Storage with Write Authorization**: Memory writes from low-trust sources (content embedded in tool outputs, documents processed on the user's behalf, other agents in a multi-agent system) require either explicit user confirmation or elevated approval before being promoted from a quarantine buffer into the trusted memory store that influences future behavior.

### Detection & Response
1. **Stored-Content Instruction Scan**: Periodically scan the memory store for content matching instruction/injection patterns (imperative verbs directed at "the assistant", role-play framing, system-prompt-like phrasing) that may have slipped past write-time sanitization. Quarantine matches immediately pending review.
2. **Unverified-Claim Flagging**: Flag stored memories whose source is a low-trust channel (scraped content, third-party document, another agent) and that have not been corroborated by a direct user statement; surface these with a lower trust weight rather than treating them as confirmed fact.
3. **Behavioral Drift Correlation**: Monitor for agent behavior changes (new refusal patterns, new "preferences" appearing, unexpected tone/policy shifts) and correlate against recent memory writes to catch poisoning that influenced behavior before it was caught by content scanning.

### Architecture Patterns
1. **Quarantine Buffer for Untrusted Writes**: All memory candidates from non-direct-user sources land in a quarantine store first, separate from the trusted memory used in retrieval; promotion to trusted storage requires passing the sanitizer/classifier and, for high-impact content, human or user confirmation.
2. **Immutable Provenance Ledger**: Store source, timestamp, sanitizer verdict, and promotion decision for every memory record, enabling forensic tracing of exactly how a poisoned entry entered trusted memory and what it affected downstream.
3. **Read-Time Instruction Filtering**: As defense-in-depth, the retrieval/prompt-assembly layer strips or neutralizes any instruction-like phrasing found in memory content before injecting it into the model context, even if it slipped past write-time checks.

### Metrics
1. **poisoned_memory_detection_count**: Target: 0 reaching trusted store; Alert threshold: > 0
2. **untrusted_source_write_quarantine_rate_percent**: Target: 100% of low-trust writes quarantined before promotion; Alert threshold: < 100%
3. **instruction_pattern_scan_hit_rate_percent**: Target: < 0.1% of stored records; Alert threshold: > 0.5% (sanitizer likely under-blocking)
4. **behavioral_drift_incidents_correlated_to_memory**: Target: 0 per month; Alert threshold: > 0

### Alerts
1. **Poisoned Memory Reached Trusted Store** (P1 - Critical): Condition - instruction-pattern scan or behavioral drift correlation confirms poisoned content influenced agent behavior. Action: Immediate quarantine of the record and any derived memories, roll back affected agent behavior, audit blast radius across users/sessions, patch the sanitizer gap.
2. **Quarantine Bypass Detected** (P1 - Critical): Condition - a low-trust-source write was found in the trusted store without having passed through quarantine/promotion approval. Action: Freeze write pipeline, root-cause the bypass, re-audit recent trusted writes from that source channel.
3. **Rising Instruction-Pattern Hit Rate** (P2 - Warning): Condition - instruction_pattern_scan_hit_rate_percent exceeds 0.5% over a rolling week. Action: Investigate source of injected content (specific tool, document type, or agent), tighten sanitizer rules, consider disabling the offending ingestion path temporarily.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Critical |

---

## References

- [MS-Agentic-Failure-Taxonomy](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf)
- Note: Agentic AI failure modes; safety/security; memory poisoning; tool use; multi-agent risks.
