# Overconfident Planning

## Issue: Agent Underestimates Task Complexity

**Frequency**: Common

**Symptoms**
- Plans too few steps for complex tasks
- Time/resource estimates wildly optimistic
- Edge cases not anticipated
- Contingencies not planned

**Root Cause**
- Lack of execution experience
- Pattern matching to simpler similar tasks
- Optimism bias in planning
- Hidden complexity not visible from description

**Example**
```
Task: "Add dark mode to the app"

Agent's estimate: "This will take about 3 steps:
1. Add CSS variables for colors
2. Add toggle button
3. Done!"

Reality: Requires changes to:
- 47 components with hardcoded colors
- Image assets (need dark variants)
- Third-party components
- Persistence layer
- User preferences sync
- Accessibility testing

Result: "Quick task" becomes multi-week project
```

---

## Test Scenario & Reproduction

### Scenario Setup
- Agent must estimate/plan a task type with significant hidden complexity (cross-cutting UI change) with no historical-calibration data or scope-expansion probe
- No buffer factor or worst-case pre-mortem step applied to the initial estimate

### Trigger Mechanism
1. Ask the agent to plan and estimate a task with known-but-non-obvious broad impact (e.g., a UI-wide styling change in a large codebase)
2. Capture the agent's initial step count/estimate before any deeper investigation
3. Run a static analysis or manual audit of the actual affected surface area and compare

**Example Reproduction Steps:**
```
1. Ask the agent: "Add dark mode to the app" against a codebase with 47 components using hardcoded colors, third-party components, and a persistence layer
2. Capture the agent's initial plan and step/time estimate
3. Run a static search for hardcoded color usage across the codebase to get the true affected-component count
4. Compare the agent's estimate against the actual scope
5. Measure: ratio of actual required steps/components to the agent's initial estimate
```

### Expected Failure State
- Agent's initial plan covers only 2-3 surface-level steps
- No scope-expansion probe surfaced the 47 affected components, image assets, or persistence/sync needs
- Actual required work is many times larger than the stated estimate

---

## Mitigation Strategies

### Prevention
1. **Historical calibration against similar past tasks**: Before finalizing an estimate/plan, compare against actual completion data for similar tagged tasks rather than pattern-matching to a superficially similar but simpler task, which is exactly how "dark mode = 3 steps" was under-scoped. Trade-off: requires a maintained history of past task actuals, which may not exist for novel task types.
2. **Mandatory scope-expansion probe**: Before accepting an initial estimate, run an explicit search for hidden complexity sources specific to the task type — for a UI-wide change like dark mode, explicitly probe for how many components have hardcoded values, third-party dependencies, and persistence/sync needs, rather than stopping at the surface-level "add CSS variables + toggle" framing. Trade-off: this probing step itself takes time and may be skipped under schedule pressure, defeating its purpose.
3. **Buffer factors calibrated by task category**: Apply a category-specific contingency multiplier to initial estimates (UI-wide changes, migrations, and integrations warranting larger buffers than isolated bug fixes) instead of a flat buffer, since the example shows a 3-step estimate ballooning to a multi-week project. Trade-off: buffers can become self-fulfilling if teams treat them as targets rather than contingency.

### Detection & Response
1. **Estimate-vs-actual variance tracking**: Continuously log the ratio of actual effort to estimated effort per task category; a task type (like broad UI changes) showing consistent multi-fold overruns should trigger recalibration of that category's baseline estimate.
2. **Scope-creep frequency by discovery phase**: Track when hidden requirements are discovered — during planning (good) vs. mid-execution (bad, as in the example where the 47 components were presumably found after coding started) — and flag categories with a high mid-execution discovery rate.
3. **Component/dependency count as a leading indicator**: For tasks involving codebase-wide changes, surface the actual affected-component count (the 47 components) as early as possible via static analysis, and compare against what the initial plan assumed, to catch underestimation before execution begins.

### Architecture Patterns
1. **Progressive/rolling-wave estimation**: Instead of committing to a fixed 3-step plan upfront, re-estimate after each discovery phase (e.g., after the first pass reveals hardcoded colors in components, re-scope before continuing) — a standard rolling-wave planning technique. Deployment consideration: requires stakeholders to accept estimates as provisional rather than fixed commitments, which can be a process/communication challenge.
2. **Expert/domain-consult gate for cross-cutting changes**: Route tasks that touch many parts of a system (styling, third-party integration, persistence, accessibility — all named in the example) through a mandatory domain-expert review before the estimate is finalized. Deployment consideration: adds a dependency on expert availability that can bottleneck fast-moving teams.
3. **Worst-case pre-mortem**: Before finalizing a plan, require an explicit "what would make this take 10x longer" exercise, directly targeting the optimism bias root cause rather than just padding the number. Deployment consideration: only effective if taken seriously rather than treated as a pro forma checkbox.

### Metrics
1. **estimate_accuracy_ratio**: Target: actual/estimated effort within 1.5x for > 80% of tasks; Alert if median ratio exceeds 3x for a task category over rolling 20 tasks.
2. **mid_execution_scope_discovery_rate**: Target: < 15% of tasks have major scope discovered after execution begins (vs. during planning); Alert if > 40% over rolling 30 tasks.
3. **planning_accuracy_by_task_type**: Target: track and publish per-category accuracy; Alert when any category's accuracy degrades more than 20 percentage points quarter-over-quarter.
4. **buffer_utilization_rate**: Target: contingency buffer consumed in 40-70% of buffered tasks (indicates buffer sized correctly); Alert if < 10% (buffer too large, wasted estimate) or > 95% (buffer too small).

### Alerts
1. **Estimate Blowout In Progress** (P2): Condition - actual effort on an in-flight task exceeds 3x the original estimate with no completion in sight. Action: pause and re-scope the task, run the scope-expansion probe retroactively, and re-estimate remaining work with domain-expert input.
2. **Systematic Category Underestimation** (P2): Condition - a task category's estimate_accuracy_ratio median exceeds 2.5x over 20+ tasks. Action: recalibrate the baseline estimate and buffer factor for that category and require expert-consult gate for future instances.

## References
- [Augment Code: Multi-Agent Coordination Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - Planning accuracy issues
- [Gartner: 40% of agentic AI projects scrapped](https://www.gartner.com/) - Overconfident project estimates
