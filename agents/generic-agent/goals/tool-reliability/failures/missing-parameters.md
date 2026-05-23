# Missing Required Parameters

## Issue: Agent Omits Required Tool Parameters

**Frequency**: Common

**Symptoms**
- Tool calls fail with "missing required field" errors
- Agent assumes defaults that don't exist
- Partial tool calls that can't execute
- Agent "forgets" parameters mentioned in conversation

**Root Cause**
- Tool schema not clearly marking required vs. optional
- Long context causing agent to lose track of requirements
- Ambiguous parameter names
- Agent conflating similar tools with different requirements

**Example**
```
Tool: send_email(to: required, subject: required, body: required, cc: optional)

Agent call: send_email(to: "user@example.com", body: "Hello!")

Missing: subject (required)

Result: Email not sent, user thinks message was delivered
```

**Mitigation Strategies**
1. **Required field validation**: Reject calls missing required params
2. **Clear schema annotations**: Mark required fields prominently
3. **Pre-flight checks**: Verify all required params before execution
4. **Helpful error messages**: Tell agent exactly what's missing
5. **Parameter confirmation**: Have agent list params before calling
6. **Sensible defaults**: Where safe, provide defaults for required fields

**Detection**
- Track missing parameter errors by tool
- Monitor which parameters are most often omitted
- Alert on repeated missing parameter errors
- Log parameter completeness rate
