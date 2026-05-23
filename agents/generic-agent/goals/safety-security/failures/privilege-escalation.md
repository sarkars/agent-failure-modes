# Privilege Escalation

## Issue: Agent Gains More Access Than Intended

**Frequency**: Occasional

**Symptoms**
- Agent accesses resources beyond its scope
- User-level agent performs admin actions
- Agent chain grants elevated permissions
- Tool combinations enable unauthorized access

**Root Cause**
- Permission checks at wrong layer
- Tool combinations bypass controls
- Multi-agent handoffs lose restrictions
- Dynamic permissions not validated

**Example**
```
User (viewer): "Read the sales report"
Agent: (Has read access) ✓

User: "Now update the Q3 projections"
Agent: Uses write_file tool (no user permission check)

Result: Viewer modified data they should only read
```

**Mitigation Strategies**
1. **Permission enforcement at tool level**: Every tool checks permissions
2. **Context propagation**: Pass user permissions through agent chain
3. **Capability-based security**: Explicit capability tokens
4. **Regular audits**: Verify permission boundaries
5. **Deny by default**: Require explicit grants
6. **Tool composition analysis**: Test tool combinations

**Detection**
- Monitor permission check failures
- Track cross-role action attempts
- Alert on unusual permission patterns
- Audit privileged operations
