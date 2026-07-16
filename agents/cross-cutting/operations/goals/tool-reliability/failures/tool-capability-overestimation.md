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

---

## Test Scenario & Reproduction

### Scenario Setup
- Search/utility tool has a vague description with no explicit negative-capability statements
- No structured capability manifest or completeness field in tool responses
- No cross-verification against a second, differently-scoped tool for high-stakes completeness claims

### Trigger Mechanism
1. Give the agent a task that requires capabilities the tool doesn't actually have (date filtering, academic-source scope) but that a vague description doesn't rule out
2. Observe whether the agent's constructed query assumes unsupported functionality
3. Check whether the tool's response is treated as complete despite being capped/partial

**Example Reproduction Steps:**
```
1. Provide a web-search tool described only as "Search the web for information" with a real cap of 10 results and no date filter
2. Ask the agent: "Find all scientific papers on X published between 2020-2024"
3. Capture the actual query the agent constructs (check for assumed date-filter syntax)
4. Capture the tool's raw response (result count, any completeness field)
5. Capture the agent's final summary — does it claim the search is complete?
```

### Expected Failure State
- Agent's query embeds unsupported functionality (date range, site-restricted boolean query) the tool silently ignores
- Tool returns exactly its capped result count (10) with no completeness/truncation flag
- Agent's final answer is presented as complete despite being a small, non-representative sample

---

## Mitigation Strategies

### Prevention
1. **Document explicit negative capabilities, not just positive ones**: The web search tool in the example only says "Search the web for information," leaving the agent to assume date filtering, academic-database access, and boolean queries all work — instead, the description must state "Does NOT support date range filtering, does NOT search academic databases, returns only top 10 general web results, does NOT support boolean operators" so the agent can't infer capabilities that don't exist. Trade-off: exhaustively listing every non-capability makes tool descriptions longer and requires updating them whenever new limitations are discovered.
2. **Attach a result-completeness field to every response, not just data**: Since the tool silently returned "10 general web results" and the agent interpreted that as "search complete," have the tool return `{"results": [...], "result_count": 10, "total_available": "unknown", "coverage": "general_web_only"}` so incompleteness is visible in the response structure rather than inferred from a plausible-looking but partial result set. Trade-off: requires the underlying API to actually expose completeness/total-count information, which many search APIs don't provide.
3. **Structured capability schema separate from the free-text description**: Provide a machine-readable capability manifest (`{"supports_date_filter": false, "supports_boolean_query": false, "max_results": 10, "sources": ["general_web"]}`) alongside the natural-language description, since relying on the LLM to correctly infer every limitation from prose is exactly the failure mode described — a structured schema lets the calling layer enforce or warn on unsupported parameter usage before the call even executes. Trade-off: maintaining a structured schema in parallel with the description is extra authoring and sync overhead per tool.

### Detection & Response
1. **Unsupported-parameter usage tracking**: Log every case where the agent's query includes patterns implying unsupported functionality (e.g., `site:scholar.google.com` or explicit date ranges sent to a tool with no date-filtering support) — the example's query construction is itself evidence the agent believed the tool supported filtering it doesn't, and this pattern is detectable directly from call logs.
2. **Result-count-at-limit flagging**: When a tool consistently returns exactly its maximum result count (e.g., always exactly 10 for the web search tool), flag this as a likely truncation signal requiring the agent to be told results are partial — the example's "10 general web results" returned as if complete is a case where hitting the cap silently should have triggered a completeness warning.
3. **Downstream completeness complaints tied to specific tools**: When users report "you only found some of the papers" or similar, tag the correction to the specific tool and capability gap involved (date filtering, source scope) so recurring gaps for the same tool are visible in aggregate rather than treated as one-off agent mistakes.

### Architecture Patterns
1. **Capability manifest / allowlist per tool**: Maintain a structured, versioned capability declaration for each tool (supported filters, max results, source coverage) that the tool-calling layer validates requests against before dispatch, rejecting or warning on requests for unsupported functionality (like a date-range filter on a tool that doesn't support one) rather than silently ignoring it; deployment consideration — requires discipline to keep the manifest current as the underlying tool's real capabilities change.
2. **Multi-tool cross-verification for high-stakes completeness claims**: For tasks like "find all papers 2020-2024" where completeness matters, require the agent to cross-check results from a second, differently-scoped tool (e.g., an actual academic database API) rather than trusting a single general-purpose tool's output as exhaustive; deployment consideration — adds cost and complexity by requiring multiple tool integrations for tasks that need genuine completeness guarantees.
3. **Confidence/completeness bounds surfaced in every response**: Standardize a `completeness: "partial" | "exhaustive" | "unknown"` field across all search/list-type tools so agents (and downstream logic) treat "partial" results as requiring further exploration by default rather than assuming exhaustiveness, directly countering the optimistic-interpretation bias named as a contributing factor; deployment consideration — for tools whose backing APIs genuinely can't report a total count, "unknown" must be an honest default, not a passthrough for "exhaustive."

### Metrics
1. **unsupported_capability_request_rate**: Target < 5% of calls to a given tool requesting functionality outside its documented capability manifest; Alert if > 20% for any tool over a week (signals the description/manifest isn't communicating limits clearly).
2. **capped_result_without_warning_rate**: Target: 0% of responses hitting a tool's max-result cap without an accompanying completeness/truncation flag; Alert on any occurrence once the completeness field is implemented.
3. **user_reported_incompleteness_rate**: Target < 3% of tool-derived answers corrected by users for being incomplete; Alert if > 10% for a specific tool over a month.
4. **capability_manifest_staleness**: Target: manifest reviewed/updated within 30 days of any underlying API change; Alert if a manifest is older than 90 days with no review.

### Alerts
1. **Confident Incomplete Answer Delivered** (P1): Condition - user_reported_incompleteness_rate spikes for a specific tool/task combination, or a capped_result_without_warning event is confirmed to have produced a materially wrong "complete" claim to a user. Action: page the owning team, add explicit completeness warnings to that tool's responses immediately, notify affected users if identifiable and material (e.g., a research or compliance task).
2. **Unsupported Capability Request Spike** (P2): Condition - unsupported_capability_request_rate exceeds 20% for a tool. Action: rewrite the tool description with explicit negative capabilities and add a structured capability manifest the calling layer can validate against.
3. **Stale Capability Manifest** (P3): Condition - capability_manifest_staleness exceeds 90 days for a tool with a known upstream API change. Action: schedule a manifest review, re-verify documented limitations against current API behavior.

## References

- [MCP Tool Design](https://dev.to/aws-heroes/mcp-tool-design-why-your-ai-agent-is-failing-and-how-to-fix-it-40fc) - Tool description best practices
- [5 MCP Server Mistakes](https://dev.to/thedailyagent/5-mcp-server-mistakes-that-waste-your-ai-agents-time-and-how-to-fix-them-18m5) - Common tool design errors
- [MAST Taxonomy](https://arxiv.org/abs/2503.13657) - Tool-related failure modes
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Tool reliability issues
- [Braintrust: Agent Observability](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Tool monitoring
