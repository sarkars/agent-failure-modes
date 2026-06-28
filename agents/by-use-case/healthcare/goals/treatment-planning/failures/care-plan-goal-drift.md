# Care Plan Goal Drift Across Encounters

## Issue: Agent Regenerates the Care Plan at Each Visit From the Current Problem List Alone, Losing Continuity With Previously Agreed Patient Goals

**Frequency**: Common

**Symptoms**
- Long-term, patient-specific goals set in an earlier visit (e.g., "avoid insulin if achievable through lifestyle changes for 6 months") are absent from the next visit's regenerated plan
- Each visit's care plan reads as if generated fresh from the diagnosis list, with generic goals rather than the negotiated, patient-specific ones
- Progress toward a previously set goal (e.g., weight loss target, A1c target) is not tracked or referenced in the new plan
- Care team members receive inconsistent goal framing across visits, leading to conflicting guidance given to the patient

**Root Cause**
Care plan generation is often implemented as a stateless per-visit task: given the current problem list and latest note, produce a plan. Without an explicit mechanism to retrieve and carry forward the previously negotiated goals and their progress status, each generation event is independent and has no memory of prior shared decision-making, so the plan silently reverts to generic, diagnosis-driven defaults rather than continuing the patient's actual care trajectory.

**Example**
```
Scenario: Visit 1 — patient and clinician agree to a 6-month trial of lifestyle modification before considering insulin
Visit 2 (3 months later): Agent regenerates care plan from current A1c and problem list
Generated plan: "Recommend initiating insulin therapy" (generic guideline-driven default)
Missed: Prior 6-month trial agreement, 3 months of progress already made
Impact: Erodes patient trust in care continuity; may override a deliberate, agreed-upon care strategy
```

**Key Statistics**
- Loss of care plan continuity across encounters is a recurring theme in studies of fragmented, episodic clinical documentation systems
- Shared decision-making goals that are not explicitly carried forward in structured form are disproportionately likely to be lost or contradicted in subsequent encounters
- Structured, longitudinal goal-tracking fields in care plans have been associated with improved goal-concordant care continuity compared to per-visit plan regeneration

---

## Mitigation Strategies

1. **Persistent Goal Object**: Store patient-specific care goals as a structured, persistent object (goal, agreed timeframe, progress checkpoints) separate from and carried into every visit's plan generation, not re-derived from the problem list each time
2. **Progress-Aware Regeneration**: Require the agent to explicitly state progress against each active goal before proposing any plan changes
3. **Guideline-Override Justification**: When a generated recommendation would override a previously agreed patient-specific goal, require explicit justification and patient re-discussion rather than silent replacement
4. **Goal Continuity Audit**: Periodically audit care plans for goals that disappeared between visits without documented resolution

### Metrics
- % of active patient-specific goals correctly carried forward into the next visit's plan
- Rate of generated plans that silently override a prior agreed goal without justification
- Goal-concordance rate measured via patient/clinician review

### Alerts
- Active patient-specific goal absent from new plan with no documented resolution → P2
- Generated plan contradicts a previously agreed goal without explicit override justification → P1

---

## References

- [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1)
- [Reinventing Clinical Dialogue: Agentic Paradigms for LLM Enabled Healthcare Communication](https://arxiv.org/pdf/2512.01453)
