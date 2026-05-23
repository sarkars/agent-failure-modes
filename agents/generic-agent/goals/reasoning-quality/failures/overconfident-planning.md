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

**Mitigation Strategies**
1. **Historical calibration**: Compare to similar past tasks
2. **Buffer factors**: Add contingency to estimates
3. **Scope expansion prompts**: Actively look for hidden complexity
4. **Progressive estimation**: Refine as task progresses
5. **Expert input**: Consult domain experts for complex tasks
6. **Worst case planning**: Consider what could make task harder

**Detection**
- Track estimate vs. actual completion
- Monitor scope creep frequency
- Alert on tasks exceeding estimates
- Compare planning accuracy by task type
