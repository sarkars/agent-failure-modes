# What Are the Most Common Agent Trust Failures in AI Agents?

**Inter-agent trust fails when a system designed for multi-agent collaboration accepts outputs, delegates tasks, or chains decisions without verifying that upstream agents are actually trustworthy, have the capabilities they claim, or executed tasks correctly.** An orchestrator delegates security-review work to an agent that claims expertise but lacks smart-contract knowledge and ships code with a $2M vulnerability, a knowledge-base-poisoning attack injects malicious instructions that bypass tool-sandboxing and circuit-breakers because the corrupted beliefs look like normal context, and one agent's corrupted state propagates through a chain of five downstream agents before anyone detects the problem. Agent-trust failures matter precisely because they hide in multi-agent architectures that assume "if Agent A says Agent B did it correctly, then B did it correctly"—a trust-by-default model that scales attack surface with agent count.

## Key Takeaways

- 11 patterns cover agent-trust failures, grouped into four mechanisms: unverified-capability delegation, corrupted-agent-state propagation, identity-verification gaps, and knowledge-base-poisoning that bypasses existing defenses.
- Memory-poisoning attacks are rated Common in production (95%+ success rate) and Critical gap in all major frameworks: attackers inject malicious instructions into agent memory/knowledge-base that look like normal context, bypassing tool-contracts, circuit-breakers, and I/O moderation because those defenses monitor tool calls, not belief systems.
- Blind-delegation (deploying to wrong agent, trusting agent output without verification) and unverified-agent-output are both rated Very Common to Common, and the defining trait is that the failure is only discovered post-deployment when incorrect output has already propagated downstream.
- Zero-trust inter-agent architecture (requiring cryptographic identity verification, capability proof, and output validation on every agent interaction regardless of "trusted" network position) is the consistent fix across all 11 patterns, treating agent-chains with the security rigor applied to service-mesh architectures.

## Scope

- **Unverified Capability Delegation** — [blind-delegation](failures/blind-delegation.md), [capability-misrepresentation](failures/capability-misrepresentation.md). Both describe orchestrators delegating tasks to agents without verifying that agents actually possess claimed capabilities, possess required permissions, or can execute correctly. Failures manifest as tasks delegated to incapable agents and outputs accepted without verification.
- **Corrupted-Agent State and Propagation** — [corrupted-agent-state](failures/corrupted-agent-state.md), [output-provenance-loss](failures/output-provenance-loss.md). Both describe scenarios where an agent's internal state or behavior is compromised (via injection, memory poisoning, or unauthorized modification), and the corruption propagates through all downstream agents that trust agent-provided output.
- **Identity Verification and Impersonation** — [agent-impersonation](failures/agent-impersonation.md), [sybil-agent-attack](failures/sybil-agent-attack.md), [trust-transitivity-abuse](failures/trust-transitivity-abuse.md). All three describe scenarios where attackers manipulate trust relationships: impersonating trusted agents, creating multiple fake agents to manipulate consensus, or extending trust incorrectly through agent chains.
- **Knowledge-Base Poisoning** — [memory-poison-defense-gap-existing-tools-insufficient.md](failures/memory-poison-defense-gap-existing-tools-insufficient.md), [memory-poisoning-attack-95-percent-success-rate.md](failures/memory-poisoning-attack-95-percent-success-rate.md), [temporally-decoupled-poison-execution.md](failures/temporally-decoupled-poison-execution.md). All three describe attackers injecting malicious instructions into agent memory/knowledge-base that bypass existing defenses (tool-contracts, circuit-breakers) because corrupted beliefs appear as normal context, not suspicious tool calls.

## When Agent Trust Matters

- Multiple agents collaborate in orchestration chains, and outputs from upstream agents are consumed by downstream agents without re-verification or sandboxing.
- Agents delegate tasks to other agents based on declared capabilities, with no mechanism to verify that claimed capabilities match actual capabilities or permissions.
- Agents access shared knowledge-bases, memory systems, or retrieval-augmented generation (RAG) sources that may be subject to poisoning attacks, and the system has no defense that distinguishes legitimate context from injected malicious instructions.

## Cross-Pattern Insight

The dominant fix across all 11 patterns is zero-trust inter-agent architecture: every agent interaction (delegation, output consumption, capability invocation) requires independent verification regardless of network position or apparent trust level. This reverses the default from "trust unless proven malicious" to "verify unless proof of trustworthiness exists." A second recurring theme is distinguishing defenses that work on tool-call surfaces versus defenses that work on belief systems: tool-contracts, circuit-breakers, and I/O moderation all detect suspicious tool calls, but memory poisoning bypasses such tool-layer defenses because corrupted beliefs are indistinguishable from legitimate context. Effective defense requires both layers: (1) tool-layer verification (detect suspicious tool calls), and (2) belief-layer verification (detect when retrieved context contradicts known facts or safety guidelines). The shared lesson is that multi-agent systems scale attack surface with agent count: a 10-agent orchestration is not 10x as trustworthy as a single agent, it is 10x as exploitable if trust is assumed between agents rather than verified on every interaction.

## Frequently Asked Questions

### How do you prevent blind-delegation when an agent genuinely lacks expertise to verify a delegate's capabilities?
The orchestrator cannot always verify whether Agent A truly has the expertise Agent B claims. The fix is not to trust Agent A's claim but to require proof: capability certificates (Agent B is certified by trusted authority for "smart-contract security review"), capability-scoped authorization (Agent B can only invoke tools that align with claimed capabilities), or post-execution verification (after Agent B returns output, run a sanity check: "Does Agent B's output pass basic fact-checking, does it align with known constraints"). If post-execution verification catches errors, the delegation pathway is flagged for investigation and Agent B's capability claim is downgraded.

### Can tool-contracts and circuit-breakers prevent memory-poisoning attacks?
No. Tool-contracts control which tools an agent can invoke and with what parameters. Circuit-breakers cut off tool access if too many failures occur. But memory poisoning injects instructions into agent memory/knowledge-base that manipulate agent reasoning before tool-invocation occurs. A memory-poisoned agent executes the attack through "normal" reasoning, not through suspicious tool calls, so tool-layer defenses never trigger. Defense against memory poisoning requires belief-layer verification: detecting when retrieved context contradicts known facts, safety guidelines, or baseline agent behavior.

### What's the difference between a trust-transitivity-abuse and unverified-agent-output?
Trust-transitivity-abuse describes a trust relationship that is incorrectly extended through a chain: Agent A trusts Agent B, Agent B trusts Agent C, and Agent A incorrectly infers that it should therefore trust Agent C (transitivity). Unverified-agent-output describes Agent A accepting Agent B's output without independent verification of whether that specific output is correct. Both occur in multi-agent systems, but transitivity is about mis-inherited trust relationships while unverified-output is about missing verification on a single output. The fix for transitivity is explicit trust-scope boundaries (Agent A trusts B only for X, not for all of B's outputs); the fix for unverified-output is post-output validation gates.

### How do you detect corrupted-agent-state before it propagates to five downstream agents?
Corrupted-agent-state propagation requires early detection: continuous behavioral-baseline monitoring (does Agent A's output still match its known behavior pattern, or has it shifted suddenly in a way that indicates compromise), output-consistency checking (do Agent A's outputs contradict previously established facts or safe behaviors), and isolation of suspect output (quarantine Agent A's output until investigation, prevent downstream consumption). Without such mitigations, corrupted state propagates invisibly until a downstream agent detects a contradiction and escalates.

### Can temporal decoupling in poison execution prevent detection of the attack?
Temporally-decoupled-poison-execution injects malicious instructions that remain dormant (unexecuted) for days or weeks, then activates via a trigger condition (e.g., "when user ID = X, exfiltrate data"). The attack remains dormant so the attacker connection cannot be traced to the trigger event. Defense requires logging and analyzing agent behavior changes even after latency: if Agent A behaved normally for 10 days then suddenly changed behavior dramatically, investigate what changed in Agent A's knowledge-base or reasoning patterns between then and now. Without post-hoc analysis, the delayed attack goes undetected.

## Patterns

| Pattern | Mechanism | Frequency |
|---|---|---|
| [Agent Impersonation](failures/agent-impersonation.md) | Attacker poses as trusted agent in communication channel | Occasional |
| [Blind Delegation](failures/blind-delegation.md) | Orchestrator delegates to agents without verifying capabilities | Common |
| [Capability Misrepresentation](failures/capability-misrepresentation.md) | Agents claim capabilities they don't actually possess | Common |
| [Corrupted Agent State](failures/corrupted-agent-state.md) | Agent state compromised, affecting all downstream interactions | Occasional |
| [Memory Poison Defense Gap](failures/memory-poison-defense-gap-existing-tools-insufficient.md) | Standard defenses miss memory poisoning attacks on belief systems | Critical Gap |
| [Memory Poisoning Attack](failures/memory-poisoning-attack-95-percent-success-rate.md) | Attackers inject malicious instructions into agent memory | Common in Production |
| [Output Provenance Loss](failures/output-provenance-loss.md) | Cannot trace which agent produced which part of output | Common |
| [Sybil Agent Attack](failures/sybil-agent-attack.md) | Attacker creates multiple fake agents to manipulate consensus | Rare |
| [Temporally Decoupled Poison](failures/temporally-decoupled-poison-execution.md) | Malicious instructions remain dormant, activate after delay | Uncommon but High-Impact |
| [Trust Transitivity Abuse](failures/trust-transitivity-abuse.md) | Trust relationship incorrectly extended through agent chains | Occasional |
| [Unverified Agent Output](failures/unverified-agent-output.md) | Agents accept other agents' outputs without verification | Very Common |

**Total: 11 patterns**

## Related Goals

- [Data Loss Prevention](../data-loss-prevention/) — focuses on preventing unauthorized data exfiltration; agent-trust failures can enable data-loss-prevention violations when corrupted or malicious agents are trusted to handle sensitive data.
- [Runtime Security](../runtime-security/) — focuses on detecting and responding to attacks at runtime; agent-trust failures are often discovered via runtime anomaly detection when upstream agents behave unexpectedly.
- [Tool Authorization Limits](../tool-authorization-limits/) — focuses on limiting agent access to external tools; agent-trust complements tool-authorization by adding agent-to-agent verification in addition to tool-invocation gating.
