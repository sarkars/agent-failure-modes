# Parameter Type Mismatches

> **⚠️ DEPRECATED — Largely Mitigated**: Strict JSON-schema / structured-output
> tool-calling modes (now standard in major model tool-use APIs) constrain the
> model to emit schema-conformant types at generation time, closing most of
> the failure path described below. Still relevant for legacy integrations
> without strict-mode enforcement. For tool-side leniency (the tool itself
> silently coercing bad input after a valid call), see `silent-type-coercion.md`,
> which is not mitigated by this and remains current.

## Issue: Agent Passes Wrong Parameter Types to Tools

**Frequency**: Very Common

**Symptoms**
- Tools receive string instead of integer (or vice versa)
- Arrays passed as single values
- Dates in wrong format
- Nested objects flattened incorrectly

**Root Cause**
LLMs generate text and must format tool parameters correctly. Type mismatches occur when:
- Schema not clearly communicated to model
- Model infers types incorrectly
- Implicit type coercion fails
- Complex nested types confuse the model

**Example**
```
Tool schema: { "user_id": integer, "active": boolean }

Agent call: { "user_id": "12345", "active": "true" }

Result: Tool fails or silently processes wrong types
```

**Key Statistic**
37% of tool calls have silent parameter mismatches according to developer analysis.

**Mitigation Strategies**
1. **Strict schema validation**: Validate all parameters before execution
2. **Type coercion layer**: Safely convert common mistakes (string "123" to int)
3. **Clear type descriptions**: Include examples in tool schemas
4. **Structured output modes**: Use JSON mode with schema enforcement
5. **Runtime type checking**: Fail fast with clear error messages
6. **Few-shot examples**: Show correct parameter formatting

**Detection**
- Log all parameter validation failures
- Track type coercion frequency
- Monitor tool success rate by parameter type
- Compare expected vs. actual parameter types

---

## References

- [Silent Tool-Call Errors](https://www.roborhythms.com/fix-ai-agent-tool-call-errors/) - Analysis finding 37% of tool calls have parameter mismatches
- [MCP Tool Design](https://dev.to/aws-heroes/mcp-tool-design-why-your-ai-agent-is-failing-and-how-to-fix-it-40fc) - Best practices for designing agent-friendly tool schemas
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Research paper on multi-agent system failure modes
