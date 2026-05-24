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

**Mitigation Strategies**
1. **Output tagging**: Every agent output includes agent ID and timestamp
2. **Provenance chains**: Track full history of data transformations
3. **Structured outputs**: Use formats that preserve attribution
4. **Segment tracking**: Tag which agent produced each output segment
5. **Audit logs**: Record all agent contributions separately
6. **Version control**: Track changes at each agent step

**Detection**
- Audit final outputs for missing attribution
- Test error tracing on sample failures
- Measure mean time to identify error source
- Check for provenance at agent boundaries
- Verify audit trail completeness

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Coordination failures
- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Monitoring requirements
- [LinkedIn: Silent Failures of Production AI](https://www.linkedin.com/pulse/silent-failures-production-ai-why-most-llm-monitoring-praveen-juyal-iqgyc) - Attribution gaps
- [AugmentCode: Multi-Agent Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - Debugging challenges
