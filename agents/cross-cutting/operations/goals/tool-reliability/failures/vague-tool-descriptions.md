# Vague Tool Descriptions

## Issue: AI Cannot Determine When to Use Tools Due to Poor Documentation

**Frequency**: Very Common

**Symptoms**
- Agent uses wrong tool for task
- Agent fails to use available tool that would help
- Agent asks user for information tools could provide
- Multiple tools seem equally applicable
- Agent guesses at tool parameters

**Root Cause**
Tool docstrings and descriptions are written for human developers, not for AI tool routing. Vague descriptions like "Get data" or "Process request" don't tell the AI when to call the tool, what parameters to pass, or what to expect in return. The AI must guess, leading to wrong tool selection or missed opportunities.

**Example**
```python
# BAD: Vague description
@tool
def get_data(query: str) -> dict:
    """Get data from the system."""
    ...

# AI's perspective:
# - What kind of data? Customer? Order? Product?
# - When should I call this vs. other tools?
# - What does 'query' mean - SQL? search term? ID?
# - What structure does the response have?

# Result: AI guesses wrong, uses incorrect tool, or asks user

---

# GOOD: Clear, AI-oriented description
@tool  
def get_customer_orders(
    customer_id: str = Field(description="The customer's UUID from the CRM"),
    status: str = Field(description="Filter by status: 'pending', 'shipped', 'delivered'")
) -> dict:
    """
    Retrieve a customer's order history from the order management system.
    
    Call this when the user asks about their orders, order status, 
    or purchase history. Returns list of orders with dates, items, 
    and current status.
    
    Do NOT use for: inventory queries, product info, or other customers.
    """
    ...

# AI knows: when to call, what to pass, what comes back
```

**Key Statistics**
From MCP Server Mistakes Analysis (2026):
- Vague descriptions are #2 most common MCP server mistake
- Tool selection accuracy drops 40%+ with poor descriptions
- AI defaults to asking user when tool descriptions are ambiguous
- Well-described tools get used 3x more often than vague ones

**Description Failures**
- **Missing "when to call"**: No guidance on appropriate scenarios
- **Missing "what it returns"**: AI can't plan next steps
- **Missing "what NOT to use for"**: AI can't distinguish similar tools
- **Generic parameter names**: "query", "data", "input" mean nothing
- **No examples**: AI can't infer usage patterns

**Contributing Factors**
- Descriptions written for human IDE tooltips
- Copy-pasted docstrings from internal documentation
- Developers assume AI understands context
- No testing from "AI's perspective"
- Parameter descriptions omitted or minimal

---

## Test Scenario & Reproduction

### Scenario Setup
- Two or more tools with overlapping functionality, at least one with a vague description (generic name, no when-to-call guidance, generic parameter names)
- No negative guidance ("do NOT use for...") distinguishing similar tools
- No intent-classification pre-step before tool selection

### Trigger Mechanism
1. Register a vaguely-described tool (`get_data(query: str)`) alongside a more specific, correctly-scoped tool for the same underlying task
2. Issue a request that should map clearly to the specific tool
3. Observe which tool the agent selects and whether it asks the user for clarification instead

**Example Reproduction Steps:**
```
1. Register get_data(query: str) with docstring "Get data from the system" alongside get_customer_orders(customer_id, status) with a clear, well-scoped description
2. Ask the agent: "What's the status of my recent orders?"
3. Capture which tool the agent selects and what parameters it passes
4. Repeat across multiple trials/phrasings
5. Measure: % of trials where the agent picks the vague tool, guesses wrong parameters, or asks the user for info the specific tool could supply directly
```

### Expected Failure State
- Agent selects the vaguely-described tool and guesses at the `query` parameter's meaning, or asks the user a clarifying question the specific tool's parameters could have resolved
- No negative guidance or when-to-call text disambiguated the two overlapping tools
- Tool selection accuracy is measurably below the well-described baseline

---

## Mitigation Strategies

### Prevention
1. **Rewrite docstrings as AI-routing prompts, not human IDE tooltips**: The root cause names this precisely — descriptions like "Get data from the system" are written for a human developer skimming an IDE, not for a model deciding whether to call the tool; every tool description should state, at minimum, when to call it, what parameters mean semantically (not just their type), and what shape the response takes, following the `get_customer_orders` example's explicit "Call this when the user asks about their orders..." pattern. Trade-off: AI-oriented descriptions are longer and more repetitive than terse human docstrings, increasing the token cost of every tool-definition load.
2. **Add explicit negative guidance ("Do NOT use for X") to every tool with a similar sibling**: Since the failure mode explicitly includes "Multiple tools seem equally applicable," any tool with functional overlap needs a stated boundary — the `get_customer_orders` example's "Do NOT use for: inventory queries, product info, or other customers" is exactly the disambiguation that prevents the agent from guessing between look-alike tools. Trade-off: negative guidance must be kept current as new tools are added, or an old tool's "do not use for X" can become stale/wrong once X gets its own dedicated tool.
3. **Use Field(description=...) with concrete meaning and format for every parameter, not just a type**: The bad example's `query: str` gives no hint whether it means "SQL," "search term," or "ID" — replace generic parameter names and bare types with descriptions like the good example's `customer_id: str = Field(description="The customer's UUID from the CRM")`, so the agent doesn't have to guess parameter semantics. Trade-off: writing precise per-parameter descriptions for every tool is meaningfully more authoring effort than a one-line docstring, and requires domain knowledge from whoever writes the tool.

### Detection & Response
1. **Wrong-tool-selection rate tracking, tied to specific tool pairs**: Log every case where the agent calls one tool, gets an unhelpful/empty result, then calls a different tool for what appears to be the same underlying intent — recurring pairs (e.g., agent tries `get_data` then falls back to a more specific tool) point directly at which vague descriptions are causing routing confusion.
2. **"Agent asked user for info a tool could have provided" tracking**: Since the root cause states vague descriptions cause the AI to default to asking the user rather than confidently selecting a tool, specifically tag conversation turns where the agent asks a clarifying question that a well-described tool's parameters could have resolved directly — this is a distinct, measurable failure signature named in the symptoms.
3. **Low-utilization audit against available tool set**: Compare how often each registered tool is actually invoked against how often its described functionality is plausibly relevant to incoming tasks; a tool that's rarely called despite obvious relevance (per the "well-described tools get used 3x more often than vague ones" stat) is a strong candidate for a description rewrite.

### Architecture Patterns
1. **Tool-description linting/review as a required step before shipping a new tool**: Enforce a checklist (when-to-call present, negative guidance present if overlapping tools exist, every parameter has a Field description, return structure documented) as a gate in code review for any new or modified tool, operationalizing "Test with AI: would AI know when to call this?" as a concrete, repeatable check rather than an informal reminder; deployment consideration — requires someone to actually own and enforce the checklist, or it decays into an ignored guideline.
2. **Few-shot usage examples embedded per tool**: Attach one or two concrete example invocations (input → expected reasoning → output) directly in the tool description for tools with a history of misuse, giving the model a pattern to match against rather than inferring purely from prose; deployment consideration — examples can become stale or misleading if the tool's behavior changes and the example isn't updated in lockstep.
3. **Semantic tool-selection pre-router for large tool sets**: For agents with many overlapping tools, insert an intent-classification step that narrows the candidate tool set before the model makes its final selection, reducing the chance of confusing two vaguely-described but functionally different tools; deployment consideration — the pre-router itself needs accurate training/prompting and can introduce a new source of misrouting if it's also poorly specified.

### Metrics
1. **tool_selection_accuracy_rate**: Target > 90% (recovering toward the baseline the cited 40%+ accuracy drop implies is achievable with clear descriptions); Alert if a specific tool's selection accuracy falls below 70%.
2. **clarifying_question_deflection_rate**: Target < 5% of turns where the agent asks the user for info a described tool's parameters could supply; Alert if > 15% for a given task category.
3. **tool_utilization_rate** (relative to plausible relevance): Target: every registered tool used in > 50% of sessions where it's plausibly applicable; Alert if a tool's utilization is < 15% of plausible-relevance sessions for 2+ weeks (signals a description problem, not a demand problem).
4. **description_checklist_compliance_rate**: Target: 100% of newly shipped tools pass the when-to-call/negative-guidance/parameter-description checklist at review time; Alert on any tool merged without full compliance.

### Alerts
1. **Tool Selection Accuracy Drop** (P2): Condition - tool_selection_accuracy_rate for a specific tool falls below 70%. Action: rewrite the tool's description following the when-to-call/negative-guidance/Field-description pattern, add negative guidance against its most commonly confused sibling tool.
2. **High Clarifying-Question Deflection** (P2): Condition - clarifying_question_deflection_rate exceeds 15% for a task category. Action: identify which tool's parameters could have answered the question directly, rewrite its description and parameter Field descriptions.
3. **Underutilized Tool Despite Relevance** (P3): Condition - tool_utilization_rate stays below 15% of plausible-relevance sessions for 2+ weeks. Action: review the tool's description for vagueness, run the "would AI know when to call this?" test with a fresh reviewer, add few-shot examples if the issue persists.

## References

- [5 MCP Server Mistakes](https://dev.to/thedailyagent/5-mcp-server-mistakes-that-waste-your-ai-agents-time-and-how-to-fix-them-18m5) - Mistake #2: Vague descriptions
- [Roborhythms: Fix AI Agent Tool-Call Errors](https://www.roborhythms.com/fix-ai-agent-tool-call-errors/) - Tool design for AI
- [MCP Tool Design](https://dev.to/aws-heroes/mcp-tool-design-why-your-ai-agent-is-failing-and-how-to-fix-it-40fc) - AI-oriented tool documentation
