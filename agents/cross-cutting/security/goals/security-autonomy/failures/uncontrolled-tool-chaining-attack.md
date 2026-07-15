# Uncontrolled Tool Chaining Attack

## Issue: Attacker Chains Legitimate Tools in Unintended Sequences to Bypass Controls

**Frequency**: Occasional

**Symptoms**
- Agent chains tools in ways system designer didn't anticipate
- Sequence of legitimate operations achieves unauthorized result
- Individual operations were individually safe; the combination is not
- Hard to detect because no single tool was misused
- Attacker maps out tool capabilities and finds exploitable sequences

**Root Cause**
When an agent has access to multiple tools with broad capabilities, attackers can chain them together in unanticipated ways to bypass application-level controls. Each individual tool call looks legitimate (reads data, modifies file A, calls API B) but together they accomplish something prohibited (exfiltrate data, escalate privilege, cause denial of service).

**Example**
```
Available Tools:
- read_file(path): Read any file in /home/user/
- write_file(path, content): Write to /home/user/
- execute_sql(query): Query user data in database

Exploit Sequence:
1. read_file("/etc/database_config.json") → get DB credentials
2. write_file("/tmp/credentials.txt", contents) → stage credentials
3. execute_sql("SELECT * FROM users WHERE ...") with escalated creds → exfiltrate

Result: Attacker gained unauthorized data access through tool chaining
Individual controls didn't prevent this because each tool was used "correctly"
```

**Key Statistics**
- 35-40% of real agent compromises involved chaining legitimate tools
- Average cost of undetected tool-chain attack: $50K-500K (data breach, cleanup)
- 90% of tool-chain exploits could be prevented with capability composition rules
- Time to discover: weeks to months (silent exfiltration)

**Contributing Factors**
- Tools designed with too-broad permissions
- No whitelist of approved tool combinations
- No audit of tool sequencing
- Insufficient isolation between tools
- No dependency/capability analysis

---

## Test Scenario & Reproduction

### Scenario Setup
- Agent has access to N tools (file read/write, APIs, DB queries, system calls)
- Each tool individually safe (proper permissions, input validation)
- Attacker can request arbitrary sequences
- Tools can access shared state/files

### Trigger Mechanism
1. Attacker enumerates tool capabilities
2. Finds sequences that together accomplish unauthorized goal
3. Requests legitimate-looking task that hides the chain
4. Sequence executes without raising suspicion

**Example Reproduction Steps:**
```
1. List all available tools and their capabilities
2. Draw dependency graph: which tool outputs become inputs to others?
3. Identify paths from tool A → tool B → tool C that bypass controls
4. Test each path: does chaining work?
5. Measure: can you accomplish unauthorized goal with sequence?
```

### Expected Failure State
- Tool sequence executes successfully
- Each individual operation appears legitimate
- Combined result is unauthorized/harmful
- No alerts trigger because individual operations were safe
- Attacker achieves goal silently

### Mitigation Validation Protocol

**Test Checklist:**
- [ ] Attempt 5-10 known harmful tool chains → blocked
- [ ] Attempt legitimate sequences → work normally
- [ ] Attempt "innocent-sounding" request hiding chain → blocked
- [ ] Verify approval/audit for any cross-tool dependencies
- [ ] Test with adversarial tool combinations (fuzzing)

**Success Criteria:**
- 0% success rate on harmful chains
- <5% false positive blocking legitimate sequences
- All suspicious chains logged and reviewed
- Capability composition rules in place
- No silent failures

---

## Mitigation Strategies

### Prevention

1. **Explicit Tool Composition Allowlist**: Define exactly which tool sequences are permitted. Don't assume tools can be freely chained; require explicit approval for any multi-step operations. Implement as a policy: "tool A can call tool B, but not tool C" or "read operations only, no write chains".

2. **Capability-Based Security Model**: Instead of "user has read access", use "user can read file X for purpose Y". Attach purpose/context to each tool invocation so chaining operations requires re-establishing the same purpose, preventing aliasing attacks.

3. **Dependency Injection with Immutable Bindings**: Bind tools to specific narrowly-scoped capabilities at initialization time. A tool requesting escalated permissions gets a "sandboxed" version with restricted output/side-effects. Prevent dynamic permission elevation through chaining.

### Detection & Response

1. **Multi-Tool Sequence Monitoring**: Track sequences of tool calls within a session. Flag sequences matching known attack patterns (read-privilege-escalation, read-write-exfiltrate). Log unusual sequences for manual review.

2. **Capability Flow Analysis**: Trace how data/permissions flow between tools. Alert if the output of a sensitive tool (read) becomes the input to a privileged tool (write).

3. **Anomaly Detection on Tool Chains**: Build a baseline of normal tool sequences. Flag outlier sequences (unusual combinations, lengths, timing).

### Architecture Patterns

1. **Sandboxed Tool Execution with Capability Revocation**: Wrap tools in a capability framework. Each tool runs with only the permissions it needs for its specific task. Chaining a write tool after a read tool automatically drops permissions gained from the read.

2. **Explicit User Approval for Cross-Tool Dependencies**: Require explicit user approval for any operation that chains multiple tools or requires the output of one tool as input to another.

3. **Tool Isolation with Clear Boundaries**: Separate tools by trust domain. Tools in different domains cannot directly chain; data must pass through a sanitization/validation layer.

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `unusual_tool_chain_sequences_per_day` | Anomalous tool call sequences | >5 per day |
| `capability_escalation_attempts` | Tool chains attempting to elevate privilege | >1 per day |
| `cross_domain_tool_chains` | Sequences crossing security domains | Any occurrence |
| `tool_chain_audit_coverage` | % of tool chains reviewed by audit | >95% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unusual Tool Sequence | Tool chain doesn't match known patterns | P2 | Log and monitor for patterns |
| Capability Escalation via Chain | Sequence attempts to gain unauthorized privilege | P1 | Block immediately; investigate |
| Cross-Domain Chain | Tools from different trust domains chained | P1 | Block; require explicit approval |
| Exfiltration Pattern Detected | Read→Write→Transfer chain detected | P1 | Block and audit recent operations |

---

## References

- [Adversarial Attacks on LLMs](https://arxiv.org/abs/2310.02949) — Tool abuse and chaining attacks
- [OWASP LLM Top 10: Excessive Agency](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — LLM04: Excessive Agency
- [Security Patterns for Multi-Tool Agents](https://arxiv.org/abs/2404.13861) — Formal framework for tool access control
