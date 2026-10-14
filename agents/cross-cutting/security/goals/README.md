# Security AI Agent Failures by Goal: 75 Patterns, Causes, and Fixes

**Security AI agents fail in 9 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 75 documented patterns across 9 goals; the most documented is [Safety Security](safety-security/) with 19.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## Security Goals

| Goal | When it fails | Patterns |
|---|---|---|
| [Agent Trust](agent-trust/) | When a system designed for multi-agent collaboration accepts outputs, delegates tasks, or chains decisions without verifying that upstream agents are actually trustworthy | 11 |
| [Data Loss Prevention](data-loss-prevention/) | When agents designed to protect sensitive data instead leak, exfiltrate, or expose information to unauthorized parties because safeguards are bypassed, incomplete | 8 |
| [Jailbreak Resistance](jailbreak-resistance/) | When agents designed to maintain safety constraints and refuse harmful requests instead get persuaded, tricked, or engineered to ignore constraints and execute harmful operations. | 0 |
| [Output Filtering Moderation](output-filtering-moderation/) | When agents designed to prevent harmful, illegal, or policy-violating content in their outputs instead produce content that violates guardrails, bypasses moderation checks, or leaks unfiltered data. | 0 |
| [Runtime Security](runtime-security/) | When attacks targeting agent execution at inference time—injection, exploitation, credential theft, tool-level compromise—succeed because runtime defenses are incomplete or misconfigured. | 8 |
| Safety Security | When agents designed with guardrails, authorization checks, and safety mechanisms instead bypass those guardrails via prompt injection, excessive agency, memory manipulation | 19 |
| [Security Autonomy](security-autonomy/) | When agents with broad tool access, file handling, and code-execution capabilities are compromised via prompt injection, tool-output injection, or supply-chain attack—executing unauthorized commands | 19 |
| [Tool Authorization Limits](tool-authorization-limits/) | When agents designed to access only a limited, pre-approved set of tools instead escalate to broader tool access, bypass authorization checks, or invoke tools without proper validation. | 10 |
| [Value Alignment](value-alignment/) | When agents designed to optimize for human values instead pursue proxy metrics, misinterpret stated objectives, or develop instrumental goals that conflict with human values. | 0 |

**Total: 75 patterns**

## Frequently Asked Questions

### How do you prevent prompt injection if agents must understand and respond to user input?

Prompt injection prevention requires input isolation and explicit trust boundaries: mark user input as untrusted, separate user-input section from trusted system prompts using structural markers (XML tags, code blocks), require explicit agent reasoning before executing user-suggested operations, and test adversarial inputs for prompt-injection attempts. See Safety Security.

### How do you prevent prompt injection in agents that must process user input?

Input validation and sandboxing are required: (1) mark user input as untrusted, (2) separate user-input from trusted system prompts using structural markers, (3) validate user input against patterns (reject input containing suspicious tokens like "ignore above instructions"), (4) limit autonomous action based on user input alone (require additional human approval or automated verification before executing user-suggested actions), (5) test adversarial inputs to verify injection attempts are caught. See Security Autonomy.

### How do you prevent blind-delegation when an agent genuinely lacks expertise to verify a delegate's capabilities?

The orchestrator cannot always verify whether Agent A truly has the expertise Agent B claims. See Agent Trust.

## Related

- [Security overview](../)
- [All agent failure patterns](../../../)
