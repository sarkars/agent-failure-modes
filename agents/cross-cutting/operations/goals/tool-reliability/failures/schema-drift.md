# Tool Schema Drift

## Issue: Tool Schema Changes Break Agent

**Frequency**: Occasional

**Symptoms**
- Previously working tool calls start failing
- New required parameters not provided
- Deprecated parameters still being sent
- Output format changes cause parsing failures

**Root Cause**
- Tools updated without updating agent configuration
- Schema changes not communicated to LLM
- Backward-incompatible API changes
- Version mismatches between agent and tools

**Example**
```
Original schema: create_task(title, description)
Updated schema: create_task(title, description, project_id: required)

Agent calls: create_task("My Task", "Details")

Result: Fails with "project_id required" - agent doesn't know about new param
```

**Mitigation Strategies**
1. **Schema versioning**: Track and validate schema versions
2. **Backward compatibility**: Add new required params with defaults
3. **Schema sync checks**: Verify agent has current schemas on startup
4. **Deprecation warnings**: Warn before removing parameters
5. **Schema change alerts**: Notify when tools update
6. **Graceful degradation**: Handle unknown parameters gracefully

**Detection**
- Monitor schema validation errors over time
- Track unknown parameter warnings
- Alert on sudden increase in tool failures
- Compare tool schemas across deployments

---

## References

- [5 MCP Server Mistakes](https://dev.to/thedailyagent/5-mcp-server-mistakes-that-waste-your-ai-agents-time-and-how-to-fix-them-18m5) - How schema changes break MCP server integrations
- [MCP Tool Design](https://dev.to/aws-heroes/mcp-tool-design-why-your-ai-agent-is-failing-and-how-to-fix-it-40fc) - Designing stable, versioned tool schemas
