# Multi-Agent Handoff Drops Feature-Flag Precondition Between Deploy Agent and Config Agent

## Issue: A Deployment Agent That Determines, in Its Own Planning Reasoning, That a Specific Feature Flag Must Be Flipped to a Particular State Before a Given Deploy Is Safe Hands the Deploy Off to a Configuration Agent Through a Structured Deploy Manifest That Has No Field for Cross-System Preconditions, So the Configuration Agent Applies the Deploy Without the Flag Change Ever Happening

**Frequency**: Occasional

**Symptoms**
- The deployment agent's planning output explicitly states that a feature flag must be set to a specific value before the deploy can proceed safely, but the structured deploy manifest it hands to the configuration agent has no precondition field reflecting that
- The configuration agent, which acts solely on the structured manifest, applies the deploy without checking or setting the feature flag, since the manifest's schema has no field representing that dependency
- Re-reading the deployment agent's planning transcript clearly shows the precondition was identified and reasoned through; it simply never reached the structured field the configuration agent reads
- The resulting incident (the new code path executing against the old flag state) is diagnosed only after investigation traces back to the missing flag flip, since the deploy itself completes without any error
- Deploys whose only precondition is deploy-target state (a prior migration, a config value on the same host) rarely trigger this, since the manifest already models that; the failure needs a precondition that lives in a system the manifest was never built to describe, like a flag service's current value

**Root Cause**
The deploy manifest schema was built to describe the deploy target itself -- artifact, environment, target configuration -- because that is what the configuration agent's job has always been to apply. A precondition that lives in a separate system, like whether "new-schema-reads" is already true in the flag service, falls outside that schema's design entirely, so the deployment agent's reasoning about it can only surface as narrative in its planning output. The configuration agent's execution step was written to apply manifests, not to interpret planning prose, so it proceeds against whatever the manifest's fixed fields say and has no occasion to notice the flag was never checked.

**Example**
```
Deployment agent plans a release that ships new code reading from a redesigned data schema, reasoning: "This deploy is only safe if the 'new-schema-reads' feature flag is already set to true in the flag service; if it's still false, the new code will read from the old schema location and fail"
Deployment agent generates a structured deploy manifest specifying the new build artifact and target environment; the manifest schema has no field for external feature-flag preconditions
Configuration agent executes the deploy from the manifest exactly as specified, with no check of the feature-flag service's current state
Feature flag is still set to false at deploy time; new code attempts to read from the old schema location and throws errors across the affected service
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM systems exhibit a documented failure category where a precondition or constraint established by one agent is lost or never reaches a downstream agent's effective input, distinct from either agent reasoning incorrectly on its own | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Generalist multi-agent system designs are shown to require explicit, structured task and precondition specification between agents, since narrative planning output alone does not reliably propagate to a downstream agent acting on a fixed schema | [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468) |
| Studies of failure lifecycles in platform-orchestrated agentic workflows identify cross-system precondition loss between sequential agent steps as a recurring driver of downstream execution failures | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |

**Contributing Factors**
- The deploy manifest schema covers only deploy-target configuration fields, with no general-purpose field for cross-system preconditions in external services like a feature-flag platform
- The configuration agent's execution logic consults only the structured manifest, never the deployment agent's planning transcript
- No reconciliation step compares precondition language in the deployment agent's planning output against what the structured manifest actually encodes before the deploy executes

---

## Mitigation Strategies

1. **Structured Cross-System Precondition Field in Deploy Manifest**: Extend the deploy manifest schema to carry an explicit, structured list of external-system preconditions (feature flags, config values, dependent service states), and require the deployment agent to populate it directly from its own planning determination
2. **Pre-Deploy Precondition Verification Gate**: Before the configuration agent executes a deploy, automatically verify every structured precondition in the manifest against the live state of the relevant external system, blocking the deploy on any unmet precondition
3. **Pre-Execution Precondition Reconciliation Scan**: Before a deploy manifest is finalized, automatically scan the deployment agent's planning transcript for precondition language and flag any mismatch against the manifest's structured precondition field
4. **Cross-System State Snapshot in Deploy Audit Log**: Capture and log the state of all referenced external systems (feature flags, config services) at deploy time, enabling rapid root-cause identification when a precondition mismatch causes an incident

### Metrics
- Rate of deploys where the deployment agent's planning transcript contains precondition language not reflected in the structured deploy manifest
- Rate of deploys executed with an unmet, structurally-declared precondition
- Time between deploy execution and detection of a precondition-related incident

### Alerts
- A deploy executes despite a structured precondition in the manifest being unmet at deploy time → P1
- The deployment agent's planning transcript contains precondition language not reflected in the structured manifest before deploy → P2
- Precondition-reconciliation mismatch rate exceeds the defined threshold for a rolling window → P3

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
