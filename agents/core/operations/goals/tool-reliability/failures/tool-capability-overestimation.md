# Tool Capability Overestimation

## Issue: Agent Assumes Tool Can Do More Than It Actually Can

**Frequency**: Common

**Symptoms**
- Agent calls tool with unsupported parameters
- Tool returns partial results, agent assumes complete
- Agent expects tool to handle edge cases it can't
- Tool limitations not reflected in tool description
- Confident but incorrect results from tool misuse

**Root Cause**
Agents infer tool capabilities from descriptions and names, but these rarely capture full limitations. A "search" tool might not handle boolean queries. A "calculator" might not handle symbolic math. The agent's language understanding leads it to assume broader capabilities than exist, resulting in silent failures or incorrect results when pushing beyond actual tool limits.

**Example**
```
Scenario: Research agent with web search tool

Tool description: "Search the web for information"

Agent task: "Find all scientific papers on X published between 2020-2024"

Agent's assumption:
  - Tool supports date range filtering
  - Tool searches academic databases
  - Tool returns comprehensive results
  - Tool handles boolean queries

Actual tool capabilities:
  - General web search only
  - No date filtering
  - No academic database access
  - Returns top 10 results only
  - No boolean query support

Agent query: "X scientific papers 2020-2024 site:scholar.google.com"

Result:
  - Tool returns: 10 general web results
  - Agent interprets as: "Found 10 papers, search complete"
  - Missing: 500+ relevant papers
  - User receives: Confidently incomplete answer

Post-incident analysis:
  - Tool description didn't specify limitations
  - Agent didn't verify result completeness
  - No feedback loop for capability mismatch
```

**Key Statistics**
From Tool Usage Research (2026):
- 45% of tool calls exceed actual tool capabilities
- Tool descriptions capture only 30-50% of limitations
- 28% of "successful" tool calls return incomplete results
- Capability overestimation causes 15% of agent errors
- Users can't distinguish tool limits from agent limits

**Overestimation Types**
| Type | Example | Impact |
|------|---------|--------|
| Scope | "Search" = "search everything" | Missing data |
| Precision | "Calculate" = "any math" | Wrong answers |
| Completeness | "List" = "all items" | Partial results |
| Format | "Parse" = "any format" | Parse failures |
| Scale | "Process" = "any size" | Truncation |

**Contributing Factors**
- Vague tool descriptions
- No explicit capability boundaries
- Agent infers from natural language
- Missing "does not support" documentation
- No capability probing mechanism
- Optimistic interpretation bias

**Mitigation Strategies**
1. **Explicit limitations**: Document what tool does NOT do
2. **Capability schemas**: Structured capability declarations
3. **Probing queries**: Agent tests tool limits before use
4. **Failure feedback**: Tool reports capability mismatches
5. **Confidence bounds**: Tool indicates result completeness
6. **Multi-tool verification**: Cross-check with other tools

**Detection**
- Monitor tool calls with unsupported parameters
- Track partial result returns
- Compare expected vs. actual tool output scope
- Alert on capability mismatch errors
- Audit user complaints about incomplete results

## References

- [MCP Tool Design](https://dev.to/aws-heroes/mcp-tool-design-why-your-ai-agent-is-failing-and-how-to-fix-it-40fc) - Tool description best practices
- [5 MCP Server Mistakes](https://dev.to/thedailyagent/5-mcp-server-mistakes-that-waste-your-ai-agents-time-and-how-to-fix-them-18m5) - Common tool design errors
- [MAST Taxonomy](https://arxiv.org/abs/2503.13657) - Tool-related failure modes
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Tool reliability issues
- [Braintrust: Agent Observability](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Tool monitoring
