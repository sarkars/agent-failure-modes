# What Are the Most Common Security Failures in AI Agents?

**Agent security fails when systems designed to protect against attacks, enforce authorization, and maintain safety instead get compromised, bypassed, or exploited to enable unauthorized access, data leakage, or policy violation.** An orchestrator agent trusts downstream agents without verifying their identity or output, and a compromised agent exfiltrates sensitive data that downstream agents blindly trust and propagate, a prompt-injection attack makes an agent ignore safety constraints and execute harmful operations, and memory poisoning injects instructions into knowledge-base that agent retrieves and executes without distinguishing malicious context from legitimate information. Security failures in agents matter precisely because agents are software systems that interact with humans, other agents, and external systems—every interaction point is a potential attack surface, and most agents were built for capability, not security.

## Key Takeaways

- 75 documented patterns (across 6 goals with failures + 3 scaffold goals) cover agent security, grouped into nine mechanisms: inter-agent trust and verification, data protection and exfiltration prevention, runtime attacks (injection, tool-based), authentication and credential management, authorization and permission enforcement, safety constraint enforcement, audit and detection, supply-chain security, and value alignment.
- Multi-agent architectures exponentially increase attack surface: a 10-agent orchestration is not 10x as exploitable as a single agent, it is often 100x+ as exploitable because trust relationships compound and compromised agents propagate compromise through downstream chains.
- Prompt injection and memory poisoning are rated Common in production: attackers inject malicious instructions via user input or knowledge-base manipulation that agents execute despite safety training and guardrails designed to prevent such execution.
- Effective agent security requires defense-in-depth: no single security mechanism (authentication, authorization, runtime checks, audit logging) is sufficient. Attackers typically chain vulnerabilities to compromise systems that each individual security mechanism is supposed to prevent.

## Scope

Agent security covers six goals with documented failures and three scaffold goals:

- **[Agent Trust](goals/agent-trust/)** (11 patterns) — Inter-agent trust verification, capability proof, output validation, identity verification. When upstream agents are not verified before being trusted, compromised agents propagate compromise through agent chains.
- **[Data Loss Prevention](goals/data-loss-prevention/)** (8 patterns) — Protecting sensitive data (PII, credentials, trade secrets) from unintentional exposure (via logs, error messages) and intentional exfiltration (via compromised agents, prompt injection). Fine-grained data-tracking and output validation prevent data exposure.
- **[Runtime Security](goals/runtime-security/)** (8 patterns) — Defending against runtime attacks targeting agent execution during inference: context poisoning, malicious tool injection, protocol exploitation, credential theft. Layered defenses (input isolation, tool verification, credential rotation) prevent runtime compromise.
- **[Safety & Security](goals/safety-security/)** (19 patterns) — Core safety mechanisms: prompt injection resistance, excessive-agency prevention, memory poisoning defense, audit evasion detection, human-loop enforcement, supply-chain security. No single defense is sufficient; defense-in-depth requires guardrails, anomaly detection, audit logging, and supply-chain verification.
- **[Security & Autonomy](goals/security-autonomy/)** (19 patterns) — Securing autonomous agent actions: preventing injection attacks, validating tool outputs, restricting permission scope, preventing credential exposure. Autonomy amplifies attack impact; defense requires minimal-privilege tool access and comprehensive input validation.
- **[Tool Authorization Limits](goals/tool-authorization-limits/)** (10 patterns) — Restricting agent access to only approved tools and operations on approved resources. Fine-grained authorization (tool-level, parameter-level, resource-level) prevents agents from accessing tools beyond authorized scope.
- **[Jailbreak Resistance](goals/jailbreak-resistance/)** (scaffold) — Preventing attackers from persuading agents to ignore safety constraints via social engineering, constraint relaxation, or adversarial prompting. Training-time safety requires runtime constraint enforcement and continuous adversarial testing.
- **[Output Filtering & Moderation](goals/output-filtering-moderation/)** (scaffold) — Detecting and preventing harmful, illegal, or policy-violating content in agent output, and redacting sensitive data before output. Layered defenses (pattern matching, semantic checking, format validation) are required because single defenses are bypassed.
- **[Value Alignment](goals/value-alignment/)** (scaffold) — Ensuring agent behavior optimizes for human values, not just metrics. Proxy-metric divergence and literal-objective misinterpretation cause agents to optimize in ways that violate human intent.

## When Security Failures Matter

- Agents interact with humans, other agents, and external systems, with trust-by-default architectures that assume internal agents are trustworthy—a false assumption when agents can be compromised.
- Agents process untrusted input (user queries, retrieved documents, tool output) without full validation or isolation, enabling injection and prompt-manipulation attacks.
- Agents access external tools, files, databases, and credentials with overly broad permissions, enabling attackers to escalate impact when compromise occurs.

## Cross-Pattern Insight

The dominant pattern across all 75 documented security failures is that single-layer defenses fail against chained attacks: if authentication is the only defense, attackers bypass authentication. If authorization is the only defense, attackers escalate permissions. If audit logging is the only defense, attackers manipulate logs. Effective agent security requires defense in depth: (1) prevent compromise (authentication, secure configuration), (2) detect compromise (anomaly detection, audit logging), (3) limit damage (authorization, isolation, constraints), (4) respond to compromise (automatic isolation, rollback, incident response). The second dominant pattern is that agent architectures compound risk: each additional agent in an orchestration adds trust relationships that can be compromised, tool integrations that can be exploited, and data-flow paths that can leak information. Security requires not just hardening individual agents but also reducing agent count, isolating agent chains, and verifying trust at every agent boundary. The shared lesson is that agent security is not a feature added post-deployment—it requires security-first architecture: minimal-privilege default, defense-in-depth by design, continuous adversarial testing, and treating agents as high-risk systems requiring the same security rigor applied to critical infrastructure.

## Frequently Asked Questions

### How do you prevent a compromised agent from propagating compromise through a multi-agent chain?
By eliminating transitive trust: do not assume downstream agents can trust upstream agents without re-verification. Defenses include: (1) verify every inter-agent message (cryptographic signature, capability proof), (2) validate inter-agent output (re-verify output from upstream agent before accepting), (3) isolate agents (separate failure domains so one agent's compromise does not affect others), (4) monitor agent behavior (detect when agents suddenly behave differently after receiving message from upstream agent). Without output validation, one compromised agent compromises entire chain.

### Can prompt-injection resistance training prevent all prompt-injection attacks?
No. Training improves baseline resistance but does not prevent novel attack vectors. Defense requires: (1) robust safety training (model understands why constraints exist), (2) input isolation (separate user input from trusted context), (3) runtime constraint enforcement (technical checks that prevent harmful output regardless of reasoning), (4) continuous adversarial testing (red-team agents against novel attacks). Training alone is insufficient; defense-in-depth is required.

### How do you prevent over-scoped credentials from enabling attackers to escalate impact?
Implement just-in-time authorization: agents request access to specific resource for specific action, receive scoped credential (temporary access, specific parameters), credential expires after action completes. Pair with continuous monitoring: audit credential usage to detect unusual access patterns (agent suddenly accessing resources it previously never accessed). Implement credential rotation: periodically invalidate long-lived credentials and require re-authorization. Over-scoped credentials that never expire are security disasters waiting for exploitation.

### What's the fastest way to tell if an agent system is vulnerable to supply-chain attack?
Audit the supply chain: identify all external dependencies (model weights, packages, knowledge-base sources, prompts), verify integrity of each dependency (checksums, signatures), identify which dependencies are updated automatically vs. manually. Conduct adversarial testing: inject malicious content into dependency sources and verify agent detects/rejects malicious content. Many supply-chain compromises go undetected because dependency verification is incomplete or absent.

## Goals

| Goal | Patterns | Mechanism |
|---|---|---|
| [Agent Trust](goals/agent-trust/) | 11 | Inter-agent identity, capability proof, output validation |
| [Data Loss Prevention](goals/data-loss-prevention/) | 8 | Data classification, exfiltration prevention, redaction |
| [Runtime Security](goals/runtime-security/) | 8 | Input isolation, tool verification, credential management |
| [Safety & Security](goals/safety-security/) | 19 | Prompt injection, excessive agency, audit evasion defense |
| [Security & Autonomy](goals/security-autonomy/) | 19 | Autonomous action security, injection prevention, permission scoping |
| [Tool Authorization Limits](goals/tool-authorization-limits/) | 10 | Tool access control, parameter authorization, least-privilege |
| [Jailbreak Resistance](goals/jailbreak-resistance/) | — | Safety constraint resistance to persuasion and adversarial attack |
| [Output Filtering & Moderation](goals/output-filtering-moderation/) | — | Harmful content detection, data redaction, format validation |
| [Value Alignment](goals/value-alignment/) | — | Objective specification, metric divergence, constraint satisfaction |

**Total: 75 documented patterns**

## Related Categories

- [Accuracy](../) — accuracy failures combine with security failures to create compound risk: a system that is accurate but compromised is worse than a system that is both inaccurate and secure.
- [Governance](../) — governance and oversight mechanisms form part of security defense-in-depth: audit logging, human approval, and oversight enable detection and response to security failures.
- [Operations](../) — operational concerns (monitoring, alerting, incident response) are critical to security: a compromise detected and remediated quickly is less damaging than one that propagates undetected for weeks.
- [Learning](../) — learning mechanisms can introduce security risks: feedback-based updates can be poisoned, self-improvement can be exploited. Learning-system security is part of overall agent security.
