# Wrong Tool Selection

## Issue: Agent Selects Inappropriate Tool for Task

**Frequency**: Common

**Symptoms**
- Agent uses read tool when write is needed
- Similar tools confused (search vs. lookup)
- Agent uses complex tool when simple one suffices
- Tool selection doesn't match user intent

**Root Cause**
- Too many similar tools available
- Poor tool naming or descriptions
- Agent doesn't understand tool capabilities
- Tools with overlapping functionality

**Example**
```
User: "Delete the file"

Available tools: 
- file_read: Read file contents
- file_write: Write to file (overwrites)
- file_delete: Delete file

Agent selects: file_write with empty content

Result: File emptied but not deleted, takes up space
```

## Mitigation Strategies

### Prevention
1. **Require explicit confirmation before executing a destructive action reached via an ambiguous path**: The example's core danger isn't just picking `file_write` over `file_delete` — it's that the wrong choice (emptying the file) executes silently without the agent or user noticing the mismatch until later; for any tool whose effect is irreversible or resource-consuming (delete, overwrite, empty), require an explicit confirmation step naming the specific action ("This will delete example.txt — confirm?") so a wrong-tool selection is caught before it executes, not after. Trade-off: confirmation prompts add friction and latency to legitimate, correctly-routed destructive actions too.
2. **Eliminate functional overlap between near-synonym tools where possible**: `file_write` with empty content achieving a file-emptying effect that overlaps with `file_delete`'s domain is exactly the kind of "tools with overlapping functionality" the root cause names — where two tools can produce a similar-looking but semantically different outcome (empty vs. gone), either merge them or add hard guardrails (e.g., `file_write` explicitly rejecting an empty-content overwrite with a warning to use `file_delete` instead) so the ambiguous middle ground doesn't exist. Trade-off: merging or restricting tools can remove legitimate use cases (a user genuinely wanting to empty a file's contents while keeping the file).
3. **Intent-classification pre-step before tool selection for tasks with obvious verb-to-tool mapping**: For a clear command like "Delete the file," classify the user's verb intent (delete/read/write) before the agent chooses among `file_read`/`file_write`/`file_delete`, so the routing decision is anchored to the stated intent rather than left to the model's independent judgment among three superficially similar file tools. Trade-off: an intent classifier adds an extra reasoning step and can itself misclassify ambiguous or compound requests.

### Detection & Response
1. **Wrong-tool-then-correct-tool sequence logging**: Track sessions where the agent calls one tool, then shortly after calls a different tool addressing what appears to be the same user request — in the example this would show as `file_write` followed eventually by a user complaint or a corrective `file_delete`, a directly loggable pattern distinguishing wrong-tool-selection from a normal multi-step task.
2. **Destructive-action-outcome mismatch audits**: Specifically for tools with resource/state side effects (delete, write, overwrite), periodically verify that the actual post-call state matches user intent (e.g., did "delete the file" actually result in the file being gone, not just emptied) — this directly catches the example's failure where the file "takes up space" despite the user's stated intent to remove it.
3. **User-correction clustering by tool-pair**: When users push back on an agent's action ("no, I wanted it deleted, not emptied"), tag the correction with the specific wrong-tool/right-tool pair involved and track recurrence — repeated corrections on the same pair (file_write vs. file_delete) indicate a systemic selection ambiguity, not an isolated model error.

### Architecture Patterns
1. **Guardrails on tools that can produce delete-like side effects via a non-delete tool**: Add a runtime check in `file_write` that flags or blocks an empty-content overwrite of an existing file with a message directing the agent to `file_delete` if removal was the actual intent, closing the specific loophole the example exploits; deployment consideration — needs careful scoping so it doesn't block legitimate empty-file-write use cases (e.g., truncating a log file).
2. **Tool selection confirmation gate for destructive/irreversible actions**: Route any call to a tool tagged "destructive" (delete, overwrite, bulk-modify) through a confirmation or dry-run step before execution, independent of which specific tool was chosen, so a wrong-but-still-destructive selection (like emptying instead of deleting) gets caught by the same gate as a correct-but-risky one; deployment consideration — requires tagging tools by destructiveness consistently across the tool catalog, which needs to be maintained as tools are added.
3. **Intent-based pre-router mapping common verbs to tool categories**: For a fixed set of file/CRUD-style tools, maintain an explicit verb-to-tool mapping (delete→file_delete, read→file_read, overwrite/replace→file_write) that's checked before falling back to open-ended model reasoning, reducing reliance on the model correctly disambiguating three similarly-named, similarly-described tools every time; deployment consideration — the mapping only covers anticipated verb patterns and needs a sensible fallback for requests that don't match cleanly.

### Metrics
1. **wrong_tool_selection_rate**: Target < 3% of tool calls later identified (via correction or outcome audit) as the wrong tool for the stated intent; Alert if > 10% for a specific tool pair over a week.
2. **destructive_action_confirmation_coverage**: Target: 100% of tools tagged destructive routed through a confirmation/dry-run gate; Alert on any destructive tool call executing without passing through the gate.
3. **outcome_intent_mismatch_rate**: Target < 2% of destructive/state-changing actions where post-call state doesn't match stated user intent (e.g., emptied vs. deleted); Alert if > 8% for a given tool.
4. **user_correction_rate_by_tool_pair**: Target < 3% of tool-pair invocations followed by a user correction; Alert if a specific pair (e.g., file_write/file_delete) exceeds 15% correction rate over a month.

### Alerts
1. **Destructive Action Without Confirmation Gate** (P1): Condition - a tool tagged destructive executes without passing through the confirmation/dry-run gate (destructive_action_confirmation_coverage gap). Action: page immediately, this is a guardrail failure; audit the specific call for unintended data loss and patch the routing to enforce the gate.
2. **Outcome/Intent Mismatch Confirmed** (P2): Condition - outcome_intent_mismatch_rate exceeds 8% for a tool (e.g., file_write producing delete-like user expectations unmet). Action: add the specific guardrail (e.g., block empty-content overwrite) and update the tool's description with clearer negative guidance.
3. **Recurring Wrong-Tool Pair** (P3): Condition - user_correction_rate_by_tool_pair exceeds 15% for a specific pair over a month. Action: review whether the two tools should be merged, add explicit negative examples to each tool's description, or add an intent pre-router mapping for the ambiguous verb.

## References

- [MCP Tool Design](https://dev.to/aws-heroes/mcp-tool-design-why-your-ai-agent-is-failing-and-how-to-fix-it-40fc) - How poor tool design leads to wrong tool selection
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Research on tool selection failures in multi-agent systems
