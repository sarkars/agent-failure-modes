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

---

## Test Scenario & Reproduction

### Scenario Setup
- Agent must produce a plan for a multi-step, high-risk task (e.g., deployment) with no domain-specific decomposition template to check against
- No mandatory dependency mapping or completeness checklist gate before execution
- No plan-vs-template diff step

### Trigger Mechanism
1. Ask the agent to plan a task with well-known required sub-steps beyond the obvious ones (e.g., a deployment requiring migration, LB drain, health checks, rollback, monitoring)
2. Capture the agent's generated plan before any execution occurs
3. Compare the plan against the known-complete set of required steps

**Example Reproduction Steps:**
```
1. Ask the agent: "Deploy the new API version" in an environment with an actual DB migration, load balancer, and monitoring stack
2. Capture the full step-by-step plan the agent produces
3. Compare against the known-required steps: DB migration, LB drain, health checks, rollback prep, monitoring setup
4. Measure: how many of the 5 required-but-non-obvious steps are missing from the agent's plan
5. If executed in a sandbox, observe what breaks due to the missing steps (e.g., migration not run before restart)
```

### Expected Failure State
- Agent's plan contains only the surface-level steps ("update code," "restart service") and omits migration, rollback, and monitoring
- No checklist or template comparison flagged the gap before execution began
- Executing the incomplete plan in a sandbox produces a failure traceable directly to a missing step

---

## Mitigation Strategies

### Prevention
1. **Domain-specific decomposition templates**: For recurring task classes like deployments, maintain a vetted template enumerating required steps (code update, DB migration, LB drain, health checks, rollback prep, monitoring) so the agent's plan is checked against a known-complete pattern rather than generated from scratch. Trade-off: templates lag behind evolving infrastructure and need active maintenance.
2. **Mandatory dependency mapping before execution**: Require the agent to explicitly enumerate dependencies between subtasks (e.g., "DB migration must precede service restart") before any step executes, surfacing missing prerequisite steps like the ones omitted in the example. Trade-off: adds planning overhead for genuinely simple tasks where dependency mapping is overkill.
3. **Expert/checklist review gate for complex tasks**: Route plans for high-risk task classes (deployments, migrations, financial operations) through a checklist comparison against standard requirements before execution begins. Trade-off: introduces a review bottleneck that slows down time-sensitive operations.

### Detection & Response
1. **Missing-step discovery rate tracking**: Log every case where a step is added mid-execution that wasn't in the original plan (as would have happened when migration/rollback needs surfaced after deployment started) — a rising rate signals systematic decomposition gaps for that task type.
2. **Post-mortem gap classification**: For every task failure, classify whether the root cause was a missing subtask, wrong ordering, or unidentified dependency, and feed this back into template updates.
3. **Plan-vs-template diff at generation time**: Automatically diff the agent's generated plan against the closest matching domain template and flag deviations (extra or missing steps) for review before execution, rather than waiting for post-mortem.

### Architecture Patterns
1. **Structured decomposition with completeness checklist**: Pair plan generation with an explicit checklist validation step — e.g., a deployment plan must check off migration/LB/health-check/rollback/monitoring before being marked ready. Deployment consideration: checklist must be domain-specific and versioned alongside the systems it governs.
2. **Plan-then-execute with checkpoint review**: Generate the full plan first, pause for either automated dependency-analysis validation or human review, and only then execute — preventing the "Update code, Restart, Done!" pattern from reaching production. Deployment consideration: for low-risk tasks this checkpoint should be skippable to avoid unnecessary friction.
3. **Failure-mode-analysis pre-step**: Before finalizing a plan, require an explicit "what could go wrong" pass that specifically probes for the categories of omission seen in the example (data integrity, rollback, monitoring). Deployment consideration: this step is only as good as the failure-mode taxonomy it's checked against; needs periodic updates from real incidents.

### Metrics
1. **plan_completeness_score**: Target: > 95% of required template steps present in generated plans for known task classes; Alert if < 85% over rolling 50 plans.
2. **mid_execution_step_addition_rate**: Target: < 10% of executions require adding an unplanned step; Alert if > 25% over rolling 50 executions.
3. **deployment_failure_rate_from_planning_gaps**: Target: < 2% of deployments fail due to a decomposition gap (missing migration/rollback/health-check step); Alert on any single incident causing data corruption.
4. **rollback_availability_rate**: Target: 100% of production-affecting plans include a rollback step; Alert on any plan lacking rollback that reaches execution.

### Alerts
1. **Production Plan Missing Rollback** (P1): Condition - a plan affecting production systems is approved for execution without a rollback/contingency step. Action: block execution, return the plan for revision, and require explicit sign-off if genuinely rollback-is-not-possible.
2. **Repeated Missing-Step Pattern** (P2): Condition - the same category of step (e.g., health checks, monitoring setup) is missing across more than 3 plans for the same task type within 30 days. Action: update the domain template for that task type and re-run affected agents' plans through the revised checklist.

## References
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Task decomposition failures
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Planning failures
