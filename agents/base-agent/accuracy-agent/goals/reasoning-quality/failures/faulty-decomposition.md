# Faulty Decomposition

## Issue: Agent Breaks Down Task Incorrectly

**Frequency**: Common

**Symptoms**
- Missing critical subtasks
- Wrong order of operations
- Unnecessary subtasks wasting resources
- Dependencies not identified

**Root Cause**
- Incomplete understanding of task requirements
- Missing domain knowledge
- Over-simplification of complex tasks
- Template-based planning not fitting task

**Example**
```
Task: "Deploy the new API version"

Agent's plan:
1. Update code on server
2. Restart service
3. Done!

Missing:
- Database migration
- Load balancer drain
- Health checks
- Rollback preparation
- Monitoring setup

Result: Deployment fails, data corrupted, no rollback
```

**Mitigation Strategies**
1. **Domain templates**: Use proven patterns for common tasks
2. **Dependency analysis**: Explicitly map task dependencies
3. **Expert review**: Verify plans for complex tasks
4. **Iterative refinement**: Refine plan as understanding improves
5. **Checklist validation**: Compare against standard requirements
6. **Failure mode analysis**: Consider what could go wrong

**Detection**
- Compare plans to expert templates
- Track missing step discovery rate
- Monitor task failures due to planning gaps
- Analyze post-mortems for planning issues

## References
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Task decomposition failures
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Planning failures
