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

**Mitigation Strategies**
1. **Write for AI routing**: Docstrings are prompts, not docs
2. **Include "when to call"**: Specify scenarios explicitly
3. **Describe parameters**: Use Field(description=...) for every param
4. **Specify return structure**: Tell AI what to expect
5. **Add negative guidance**: "Do NOT use for X"
6. **Test with AI**: Ask "would AI know when to call this?"

**Detection**
- Agent using wrong tools for tasks
- Agent asking user for info tools could provide
- Low tool utilization despite availability
- Frequent tool selection errors in logs

## References

- [5 MCP Server Mistakes](https://dev.to/thedailyagent/5-mcp-server-mistakes-that-waste-your-ai-agents-time-and-how-to-fix-them-18m5) - Mistake #2: Vague descriptions
- [Roborhythms: Fix AI Agent Tool-Call Errors](https://www.roborhythms.com/fix-ai-agent-tool-call-errors/) - Tool design for AI
- [MCP Tool Design](https://dev.to/aws-heroes/mcp-tool-design-why-your-ai-agent-is-failing-and-how-to-fix-it-40fc) - AI-oriented tool documentation
