# Output Provenance Loss

## Issue: Cannot Trace Which Agent Produced Which Part of Output

**Frequency**: Common

**Symptoms**
- Unable to determine which agent caused an error
- Mixed outputs with unclear attribution
- Debugging requires examining entire agent chain
- Accountability impossible to establish
- Quality issues cannot be traced to source

**Root Cause**
Multi-agent systems combine outputs from multiple agents into final results. When provenance information—which agent contributed what—is not preserved, it becomes impossible to trace errors to their source, verify the trustworthiness of specific claims, or hold any particular agent accountable for failures. This "black box" effect undermines the reliability of the entire system.

**Example**
```
Research Report Multi-Agent System:

Agents involved:
  - DataCollector: Gathers raw statistics
  - Analyst: Interprets data
  - Writer: Drafts prose
  - Editor: Refines language

Final output:
  "Market growth exceeded 15% in Q3, driven primarily by 
   the APAC region which saw unprecedented demand..."

Problem discovered:
  - "15% growth" is wrong (actual: 5%)
  - "APAC" attribution is wrong (actual: Europe)

Debugging attempt:
  Q: "Where did the 15% figure come from?"
  A: Unknown - could be DataCollector, Analyst, or Writer
  
  Q: "Who said APAC?"
  A: Unknown - no provenance tracking
  
  Q: "Which agent should we fix?"
  A: Must examine all four agents and their full traces

Cost: 8 hours of debugging for error that would take
      5 minutes with provenance tracking
```

**Key Statistics**
From Multi-Agent Research (2026):
- "Which agent caused failure?" - hardest debugging question
- Average debug time 5-10x higher without provenance
- 36.94% of failures from coordination issues (MAST)
- Provenance rarely preserved across agent boundaries
- Audit requirements often mandate attribution

**Provenance Gaps**
| Gap | Impact | Frequency |
|-----|--------|-----------|
| No source tags on outputs | Cannot trace errors | Very Common |
| Mixed outputs | Unclear boundaries | Common |
| Transformed data | Original source lost | Common |
| Aggregated results | Individual contributions unclear | Common |
| Edited content | Changes not tracked | Occasional |

**Contributing Factors**
- Agents output plain text without metadata
- Frameworks don't enforce provenance
- Performance overhead of tracking
- Complex transformations lose attribution
- No standard provenance format

## Mitigation Strategies

### Prevention
1. **Mandatory output tagging with agent ID and timestamp**: Require every agent's output — including intermediate results passed to other agents — to carry metadata identifying which agent produced it and when, enforced at the framework/infrastructure level rather than left to individual agent implementations to remember. Trade-off: adds metadata overhead to every inter-agent message and requires disciplined enforcement across all agents in the system, including third-party or externally-developed ones.
2. **Structured, attribution-preserving output formats**: Use structured output formats (e.g., a claim/fact object with a `source_agent` field per claim) rather than free-form prose that gets concatenated across agents, so that even after aggregation and editing, each factual claim retains a traceable link to its originating agent. Trade-off: constrains agents to produce structured output rather than free-flowing natural language, which can reduce output quality/fluency for narrative-heavy tasks.
3. **Segment-level tracking through transformation stages**: When one agent transforms another's output (e.g., Writer rephrasing Analyst's conclusions), require the transformation to preserve a mapping back to the original segment/claim rather than producing an opaque rewrite that loses the link to its source, so provenance survives editing and stylistic transformation, not just direct pass-through. Trade-off: significantly increases the complexity of any agent that summarizes, synthesizes, or rewrites multiple inputs.

### Detection & Response
1. **Provenance-completeness auditing on final outputs**: Regularly audit final outputs for claims/values lacking a traceable source agent, treating gaps as a data-quality defect in the pipeline that needs fixing, not an acceptable cost of aggregation.
2. **Error-tracing time tracking as a monitored metric**: Measure and track mean time to identify the source agent for a given error across sample failures; a high or rising figure indicates the provenance system isn't functioning even if it's nominally in place.
3. **Attribution audit at every agent boundary**: Specifically check for provenance preservation at each inter-agent hand-off point (not just the final output), since provenance is often lost at a specific transformation stage (e.g., the Writer agent) rather than uniformly across the whole chain.

### Architecture Patterns
1. **Provenance-chain-as-first-class-data architecture**: Architect the multi-agent pipeline so provenance metadata is a required field of the data model passed between agents (not an optional annotation), making it a framework-level guarantee rather than dependent on each agent's implementation choosing to preserve it.
2. **Audit log with per-agent contribution recording**: Maintain a separate, queryable audit log recording each agent's individual contribution (not just the final merged output), enabling reconstruction of "what did each agent actually produce" independent of how the final output was assembled.
3. **Version-controlled multi-stage pipeline**: Track the output at each agent step as a distinct, versioned artifact (not just the final result), so any downstream error can be traced back through the exact sequence of transformations to identify precisely where a value diverged from its origin.

### Metrics
1. **provenance_completeness_rate**: Target: > 98% of final-output claims have traceable source-agent attribution; Alert if < 90%
2. **mean_time_to_error_source_identification**: Target: < 15 minutes; Alert if > 2 hours (signals provenance system isn't functioning)
3. **boundary_attribution_gap_rate**: Target: 0% of inter-agent hand-offs lose attribution; Alert on any detected gap
4. **audit_trail_completeness**: Target: 100% of agent contributions individually recorded; Alert on any missing contribution record

### Alerts
1. **Provenance Completeness Drop** (P2): Condition - provenance-completeness rate on final outputs falls below 90%. Action: Investigate which agent stage in the pipeline is dropping attribution; treat as a data-quality defect requiring a fix, not an acceptable tradeoff.
2. **Error Source Identification Delay** (P2): Condition - mean time to identify an error's source agent exceeds 2 hours on a sample failure. Action: Audit the provenance-tracking implementation at each pipeline stage for gaps.
3. **Audit Trail Gap Detected** (P1): Condition - an agent's individual contribution is missing from the audit log for a production output. Action: Treat as a monitoring/compliance defect; investigate the responsible agent's integration with the audit-logging framework immediately.

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Coordination failures
- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Monitoring requirements
- [LinkedIn: Silent Failures of Production AI](https://www.linkedin.com/pulse/silent-failures-production-ai-why-most-llm-monitoring-praveen-juyal-iqgyc) - Attribution gaps
- [AugmentCode: Multi-Agent Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - Debugging challenges
