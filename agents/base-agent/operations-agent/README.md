# Operations Agent

Tools, cost, coordination, memory, context, state

## Goals

| Goal | Description | Patterns |
|------|-------------|----------|
| [Context Lifecycle](goals/context-lifecycle/) | Context assembly and truncation | 6 |
| [Cost Efficiency](goals/cost-efficiency/) | Token and API cost management | 12 |
| [Cost Tracking](goals/cost-tracking/) | Budget enforcement and attribution | 6 |
| [Human Oversight](goals/human-oversight-reliability/) | Human-in-the-loop reliability | 8 |
| [Memory Management](goals/memory-management/) | Memory summarization and retrieval | 6 |
| [Memory Safety](goals/memory-safety/) | Safe memory operations | 9 |
| [Multi-Agent Coordination](goals/multi-agent-coordination/) | Agent coordination | 9 |
| [State Tracking](goals/state-tracking/) | State management across steps | 9 |
| [Tool Invocation](goals/tool-invocation/) | Safe tool invocation | 12 |
| [Tool Reliability](goals/tool-reliability/) | Reliable tool invocation | 17 |
| [Tool Selection](goals/tool-selection/) | Correct tool selection | 10 |
| [Traceability](goals/traceability/) | Auditing and debugging | 8 |

**Total: 112 patterns across 12 goals**

## How to Use

1. **Review each goal** - Understand what "reliable" looks like
2. **Check failure patterns** - See if your agent exhibits these issues
3. **Apply mitigations** - Implement prevention and detection
4. **Monitor in production** - Track metrics and alerts

## Cross-References

See [Base Agent](../) for other cross-cutting patterns.
