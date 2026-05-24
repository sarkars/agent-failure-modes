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

**Mitigation Strategies**
1. **Sandbox enforcement**: Run agent actions in isolated containers
2. **Network segmentation**: Restrict agent network access
3. **Filesystem restrictions**: Limit paths agent can access
4. **Credential scoping**: Bind credentials to specific actions
5. **Output sanitization**: Filter agent outputs before use
6. **Environment hardening**: Remove unnecessary capabilities from agent environment

**Detection**
- Network connections to unexpected destinations
- Filesystem access outside allowed paths
- Process spawning or system calls outside normal patterns
- Data access patterns inconsistent with agent task

## References

- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Insufficient isolation as existing security failure mode
- [Replit Rogue Agent](https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident/) - Code agent escaping isolation
- [Context is Key for Agent Security](https://arxiv.org/abs/2501.17070) - Isolation requirements for agents
