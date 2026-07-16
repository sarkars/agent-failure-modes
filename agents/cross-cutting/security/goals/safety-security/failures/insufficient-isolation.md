# Insufficient Isolation

## Issue: Agent Actions Escape Intended Boundaries

**Frequency**: Common

**Symptoms**
- Agent accesses systems outside its scope
- Code execution affects unintended environments
- Data from one context leaks to another
- Agent interactions cross trust boundaries

**Root Cause**
An agent that can perform unstructured actions does so in a way that allows it to interact with systems, users, or components outside of the intended scope of the agent. Increased autonomy and usage of complex tools like code execution makes insufficient isolation more impactful.

**Example**
```
Agent task: "Generate and execute code to solve this data analysis problem"

Expected: Code runs in isolated sandbox
Actual: Code execution environment not properly isolated

Attack prompt: Crafted to generate code that:
1. Queries backend database
2. Extracts sensitive data
3. Returns data to threat actor

Result: Database breach through code generation agent
```

**Isolation Failures**
- **Network isolation**: Agent can reach unintended endpoints
- **Filesystem isolation**: Agent can read/write outside sandbox
- **Process isolation**: Agent code affects host system
- **Data isolation**: Agent accesses data from other users/contexts
- **Credential isolation**: Agent uses credentials beyond its scope

**Potential Effects**
- Cross-tenant data access
- Lateral movement through systems
- Privilege escalation via adjacent systems
- Data exfiltration through side channels

---

## Test Scenario & Reproduction

### Scenario Setup
- Agent has a code-execution tool without a hardened sandbox (no network/filesystem allow-list, shared execution context across tasks)
- No credential scoping bound to the sandbox lifetime
- No egress or filesystem-access monitoring on the execution environment

### Trigger Mechanism
1. Give the agent a data-analysis task that requires generating and executing code
2. Craft the task/prompt so the generated code attempts to reach a backend resource outside the intended scope (e.g., a database connection string reachable from the execution host)
3. Observe whether the code executes successfully and whether the access attempt is blocked or logged

**Example Reproduction Steps:**
```
1. Deploy the code-execution agent in a test environment with a reachable-but-unintended backend database
2. Submit a task: "Generate and execute code to solve this data analysis problem" with a prompt crafted to have the code query the backend database
3. Observe whether the generated code successfully connects to and extracts data from the database
4. Check network/filesystem logs for the unauthorized access attempt
5. Measure: was the attempt blocked by an allow-list, or did it succeed?
```

### Expected Failure State
- Generated code successfully reaches and extracts data from a system outside its intended scope
- No network egress control blocked the connection
- No alert fired despite the sandbox boundary being crossed

---

## Mitigation Strategies

### Prevention
1. **Sandboxed execution with default-deny network/filesystem access**: Run agent code execution in containers or microVMs with no network or filesystem access by default, only explicit allow-listed endpoints and paths, since the root cause is unstructured actions escaping the intended scope specifically through unisolated code execution environments. Trade-off: allow-list maintenance adds ongoing operational overhead as legitimate task needs evolve.
2. **Per-task ephemeral sandboxes**: Spin up a fresh, isolated environment for each task and destroy it on completion rather than reusing a persistent execution context, preventing data or state from one context leaking into another as described in the Symptoms. Trade-off: cold-start latency on every task and no caching/reuse benefits across tasks.
3. **Credential scoping bound to sandbox lifetime**: Issue credentials that are valid only within a specific sandbox instance and expire when it's destroyed, so a compromised code-execution environment cannot use credentials beyond that single task's scope, directly closing the "credential isolation" failure mode listed. Trade-off: requires a credential-issuance service integrated into the sandbox lifecycle rather than static long-lived secrets.

### Detection & Response
1. **Network egress monitoring**: Flag and block any sandbox connection attempt to a destination outside its declared allow-list, since "network isolation" failures let agents reach unintended endpoints; respond by terminating the sandbox instance immediately.
2. **Filesystem access auditing**: Monitor for read/write attempts outside the sandbox's designated paths, matching the "filesystem isolation" failure mode, and kill the execution on any out-of-bounds access.
3. **Cross-tenant/cross-context data correlation**: Correlate the data actually accessed during a task against the tenant or context that initiated it, flagging any mismatch as evidence of a data-isolation breach like the database extraction described in the Example.

### Architecture Patterns
1. **MicroVM/container-per-task isolation**: Use hardware-backed isolation (e.g., Firecracker-style microVMs or gVisor-sandboxed containers) per task so agent code execution structurally cannot affect the host system or other tenants, addressing "process isolation" at the infrastructure layer rather than relying on application-level checks.
2. **Zero-trust credential broker**: Route all credential and network access through a broker that issues narrowly scoped, task-bound grants rather than letting the sandbox hold standing credentials, so a compromised sandbox has nothing broad to exfiltrate.
3. **Output sanitization gateway**: Place a dedicated filtering layer between the sandbox and any downstream system that inspects and constrains results before they leave isolation, containing data-exfiltration attempts like the "extract sensitive data, return to threat actor" path in the Example even if the sandbox itself is compromised.

### Metrics
1. **sandbox_escape_attempt_rate**: Target: 0 confirmed escapes; Alert on any detected boundary violation.
2. **unscoped_network_egress_count**: Target: 0 connections outside declared allow-list per task; Alert on any occurrence.
3. **cross_tenant_data_access_rate**: Target: 0%; Alert on any task accessing data outside its originating tenant/context.
4. **credential_scope_violation_rate**: Target: 0% of credential usage occurs outside its issuing sandbox's lifetime/scope; Alert on any violation.

### Alerts
1. **Sandbox Boundary Breach** (P1): Condition - network or filesystem access occurs outside the declared sandbox scope. Action: terminate the sandbox instance immediately, quarantine the task, investigate the escape vector.
2. **Cross-Tenant Data Access Detected** (P1): Condition - a task accesses data belonging to a different tenant/context than the one that initiated it. Action: halt the task, notify affected tenants per incident policy, audit the isolation boundary that failed.
3. **Credential Used Outside Task Scope** (P2): Condition - a credential issued for one sandbox/task is used from a different context or after its intended lifetime. Action: revoke the credential, investigate whether it was exfiltrated from the sandbox.

## References

- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Insufficient isolation as existing security failure mode
- [Replit Rogue Agent](https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident/) - Code agent escaping isolation
- [Context is Key for Agent Security](https://arxiv.org/abs/2501.17070) - Isolation requirements for agents
