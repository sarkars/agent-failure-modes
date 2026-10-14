# Security AI Agent Failures by Goal: 75 Patterns, Causes, and Fixes

**Security failures in AI agents are grouped here into 9 goals, each with a catalog of named failure patterns, the symptoms you will see, the root cause, and mitigations you can copy.** Start from the symptom you are debugging, pick the matching goal below, and open its failure list.

## Key Takeaways

- This cross-cutting concern covers 9 goals and 75 documented failure patterns.
- The largest goal is [Safety Security](safety-security/) with 19 patterns.
- Each goal page explains the failure class, how to tell it apart from its neighbors, and which mitigations apply across its patterns.
- Each failure page covers the symptoms, an example, the root cause, and how to fix it.

## Security Goals

| Goal | What goes wrong | Patterns |
|---|---|---|
| [Agent Trust](agent-trust/) | Inter-agent trust fails when a system designed for multi-agent collaboration accepts outputs, delegates tasks, or chains decisions without verifying that upstream agents are actually trustworthy, have the capabilities they claim | 11 |
| [Data Loss Prevention](data-loss-prevention/) | Data loss prevention fails when agents designed to protect sensitive data instead leak, exfiltrate, or expose information to unauthorized parties because safeguards are bypassed, incomplete | 8 |
| [Jailbreak Resistance](jailbreak-resistance/) | Jailbreak resistance fails when agents designed to maintain safety constraints and refuse harmful requests instead get persuaded, tricked, or engineered to ignore constraints and execute harmful operations (planned, no patterns written yet) | 0 |
| [Output Filtering Moderation](output-filtering-moderation/) | Output filtering fails when agents designed to prevent harmful, illegal, or policy-violating content in their outputs instead produce content that violates guardrails, bypasses moderation checks, or leaks unfiltered data (planned, no patterns written yet) | 0 |
| [Runtime Security](runtime-security/) | Runtime security fails when attacks targeting agent execution at inference time—injection, exploitation, credential theft, tool-level compromise—succeed because runtime defenses are incomplete or misconfigured | 8 |
| [Safety Security](safety-security/) | Safety and security fail when agents designed with guardrails, authorization checks, and safety mechanisms instead bypass those guardrails via prompt injection, excessive agency, memory manipulation | 19 |
| [Security Autonomy](security-autonomy/) | Security-autonomy fails when agents with broad tool access, file handling, and code-execution capabilities are compromised via prompt injection, tool-output injection, or supply-chain attack—executing unauthorized commands | 19 |
| [Tool Authorization Limits](tool-authorization-limits/) | Tool authorization fails when agents designed to access only a limited, pre-approved set of tools instead escalate to broader tool access, bypass authorization checks, or invoke tools without proper validation | 10 |
| [Value Alignment](value-alignment/) | Value alignment fails when agents designed to optimize for human values instead pursue proxy metrics, misinterpret stated objectives, or develop instrumental goals that conflict with human values (planned, no patterns written yet) | 0 |

**Total: 75 patterns**

## Frequently Asked Questions

### Where do I start if my security agent is failing?

Match the symptom to a goal in the table above, then open that goal's page for how to tell its failures apart and where to look first. Each failure page ends in mitigations you can apply directly.

### How are these security failure patterns organized?

By goal: the outcome the agent is supposed to achieve. Under each goal, a `failures` folder holds one page per pattern. For the full picture see the [Security overview](../).

## Related

- [Security overview](../)
- [All agent failure patterns](../../../)
