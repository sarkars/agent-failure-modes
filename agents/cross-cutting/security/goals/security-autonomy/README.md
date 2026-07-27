# What Are the Most Common Security and Autonomy Failures in AI Agents?

**Security-autonomy fails when agents with broad tool access, file handling, and code-execution capabilities are compromised via prompt injection, tool-output injection, or supply-chain attack—executing unauthorized commands, exfiltrating data, or escalating privileges before detection.** An agent designed to autonomously complete tasks gets a prompt-injected request embedded in retrieved document and executes a data-exfiltration command, an agent chaining tool outputs together does not validate intermediate outputs and an attacker injects malicious commands via tool output that agent blindly executes, and an agent updates dependencies without verification and a supply-chain-poisoned package introduces backdoors into agent reasoning. Security-autonomy failures matter precisely because autonomy amplifies the impact of compromises: a compromised agent that can execute code, invoke tools, handle files, and escalate privileges is far more dangerous than one with limited autonomous capabilities.

## Key Takeaways

- 19 patterns cover security-autonomy failures, grouped into five mechanisms: prompt injection (direct and indirect), tool-output validation gaps, unsafe code/command execution, supply-chain compromise, and credential/permission overschoping.
- Prompt-injection attacks (direct via user input, indirect via retrieved context) are rated Common: attackers inject malicious instructions via user messages or documents that agents execute with full autonomy and tool access.
- Tool-output-injection and unsafe-code-execution are rated Common: agents chain tool outputs without validation or execute code without sandboxing, enabling attackers to inject malicious commands via tool output or code parameters.
- Effective defense requires validating every external input before execution (user input, retrieved context, tool output, file content), restricting agent autonomous execution to pre-approved actions, and sandboxing code/command execution.

## Scope

- **Direct Prompt Injection** — Attackers inject malicious instructions via user input that agents execute with full autonomy and tool access.
- **Indirect Prompt Injection** — Attackers inject malicious instructions via retrieved documents, file content, or tool output that agents execute.
- **Tool-Output Validation Gaps** — Agents chain tool outputs without validating that output contains legitimate data (not injected commands) or malicious patterns.
- **Unsafe Code/Command Execution** — Agents execute code or commands without proper sandboxing or validation, enabling command injection via input parameters.
- **Credential and Permission Overschoping** — Agents operate with overly broad permissions (file access, credential access, tool invocation) enabling attackers to escalate damage when compromise occurs.

## When Security-Autonomy Matters

- Agents have autonomous tool access (file I/O, code execution, external API invocation) and process untrusted input (user queries, retrieved documents, tool output) without full validation.
- Agents handle file uploads or external file access without validating file content or detecting malicious payloads embedded in files.
- Agents chain multiple tool invocations together (tool A's output feeds into tool B) without validating output at chain boundaries.

## Cross-Pattern Insight

Effective security-autonomy requires treating autonomous capability as privilege requiring defense in depth: every autonomous action (file access, code execution, tool invocation, command execution) must be preceded by validation, authorization, and sandboxing. The shared lesson is that autonomy without verification is dangerous: an agent that can invoke any tool without authorization, execute any code without sandboxing, or handle any file without validation is fundamentally exploitable. The fix is restricting autonomous actions to a pre-approved, minimal set, validating every input (user, file, tool-output) before autonomous action, and sandboxing code/command execution so compromised agents cannot escalate impact beyond their sandbox.

## Frequently Asked Questions

### How do you prevent prompt injection in agents that must process user input?
Input validation and sandboxing are required: (1) mark user input as untrusted, (2) separate user-input from trusted system prompts using structural markers, (3) validate user input against patterns (reject input containing suspicious tokens like "ignore above instructions"), (4) limit autonomous action based on user input alone (require additional human approval or automated verification before executing user-suggested actions), (5) test adversarial inputs to verify injection attempts are caught.

### Can tool sandboxing prevent command injection if tool-output contains malicious commands?
Tool sandboxing limits what a tool can do, but does not prevent tool-output injection: if an agent receives tool output and executes commands embedded in that output, sandboxing does not help. Defense requires: (1) tool-output validation (parse tool output for expected schema, reject malicious patterns), (2) separating data from commands (tool output is data, not executable code), (3) restricting what commands an agent can execute (allowlist of pre-approved commands only, reject novel commands).

### How do you handle file uploads securely if agents must process files?
File handling requires defense in depth: (1) validate file type and size before processing, (2) scan files for malicious patterns (malware, suspicious embeddings), (3) parse files safely without executing embedded code or instructions, (4) isolate file content from agent reasoning (file data is input, not executable instructions), (5) restrict agent file-system access (read-only access to quarantined directory, no write access to system files).

### What's the fastest way to detect credential overschoping in an agent system?
Audit agent credential usage: what credentials does agent currently use, what resources does agent access with those credentials, what resources could agent access (permissions) that it actually doesn't use. Down-scope credentials to minimal set actually needed. Implement just-in-time credential provisioning: agent requests temporary access to resource, receives scoped credential for specific action only, credential expires after action completes. This limits blast radius if credentials are compromised.

## Patterns

| Pattern | Mechanism | Frequency |
|---|---|---|
| [Command Injection](failures/command-injection.md) | Attacker injects malicious commands via input parameters | Common |
| [Credential Leakage In Logs](failures/credential-leakage-in-logs.md) | Credentials leak via logs or error messages | Common |
| [Cross Tenant Data Leak](failures/cross-tenant-data-leak.md) | One agent's actions leak sensitive data from another tenant | Occasional |
| [Data Exfiltration](failures/data-exfiltration.md) | Compromised agent exfiltrates data via autonomous tool invocation | Common |
| [Direct Prompt Injection](failures/direct-prompt-injection.md) | Attackers inject malicious instructions via user input | Common |
| [Fine-Tuning Data Poisoning](failures/fine-tuning-data-poisoning.md) | Training data is poisoned to introduce unsafe behavior | Occasional |
| [Indirect Prompt Injection](failures/indirect-prompt-injection.md) | Attackers inject malicious instructions via retrieved context or files | Common |
| [Insecure Output Handling](failures/insecure-output-handling.md) | Agent output containing sensitive data exposed to unauthorized parties | Occasional |
| [Malicious File Handling](failures/malicious-file-handling.md) | Agent processes malicious files and executes embedded attacks | Occasional |
| [Model Denial Of Service](failures/model-denial-of-service.md) | Attacker sends input crafted to exhaust model compute | Occasional |
| [Over Scoped Credentials](failures/over-scoped-credentials.md) | Agent has overly broad permissions enabling damage when compromised | Common |
| [Privilege Escalation](failures/privilege-escalation.md) | Compromised agent escalates permissions to perform unauthorized operations | Occasional |
| [Prompt Injection Via User Context](failures/prompt-injection-via-user-context.md) | User context or history contains injected malicious instructions | Common |
| [Secret Exposure](failures/secret-exposure.md) | Secrets (API keys, passwords) exposed via agent output or logs | Common |
| [Supply Chain Vulnerability](failures/supply-chain-vulnerability.md) | Compromised dependencies or malicious packages introduce unsafe behavior | Occasional |
| [Tool Output Injection](failures/tool-output-injection.md) | Attacker injects malicious commands via tool output that agent executes | Common |
| [Uncontrolled Destructive Actions](failures/uncontrolled-destructive-actions.md) | Agent takes destructive actions without approval or validation | Occasional |
| [Uncontrolled Tool Chaining Attack](failures/uncontrolled-tool-chaining-attack.md) | Agent chains tools without validating intermediate outputs | Occasional |
| [Unsafe Code Execution](failures/unsafe-code-execution.md) | Agent executes code without sandboxing or input validation | Common |

**Total: 19 patterns**

## Related Goals

- [Tool Authorization Limits](../tool-authorization-limits/) — restricts which tools agents can invoke; security-autonomy adds runtime validation and detection.
- [Runtime Security](../runtime-security/) — detects attacks at runtime; security-autonomy focuses on autonomous execution of compromised actions.
- [Safety & Security](../safety-security/) — core security constraints; security-autonomy emphasizes attack surface expansion from autonomous capabilities.
