# Policy Consistency Violation

## Issue
Two policies that are supposed to be consistent with each other — for example, a global organization-wide policy and a team-level override, or two policies covering overlapping domains — actually conflict in their requirements. Rather than applying a defined precedence rule, the agent's policy engine applies whichever policy it happens to evaluate first (often just an artifact of lookup order or cache layout), producing inconsistent enforcement depending on incidental factors rather than deliberate governance design.

**Frequency**: Common

**Symptoms**
- Identical actions receiving different approval requirements depending on which team or system evaluated them
- Two policy documents whose thresholds, scopes, or requirements directly contradict each other with no stated precedence
- Policy engine output that changes when the internal evaluation order of policy rules changes, even though no policy content changed
- Compliance findings citing "policy X requires approval but policy Y does not" for the same action class
- No documented precedence hierarchy (e.g., "team policy can only tighten, never loosen, the global policy") anywhere in the governance documentation

## Root Cause
Policies are frequently authored by different teams (central compliance, individual business units, security) at different times, without a shared review process that checks new or updated policies against existing ones for conflicts. Policy engines that evaluate rules in an unspecified or incidental order (e.g., alphabetical, insertion order, or whichever policy source loads first) will produce different outcomes for the same action depending entirely on implementation details rather than a deliberate precedence design.

## Example
```
1. The central compliance team publishes a global policy: "Any customer
   data export requires compliance approval."
2. A regional sales team, wanting faster turnaround for small CRM exports,
   publishes a team-level policy: "CRM exports under 500 rows do not
   require approval," intending it as a narrow operational carve-out but
   without going through central compliance review.
3. The agent's policy engine evaluates team-level policies before global
   policies in its rule list, because team policies were added to the
   engine's configuration more recently and the engine has no explicit
   precedence field.
4. A 400-row customer data export proceeds without compliance approval,
   satisfying the team policy, even though it plainly falls under the
   global policy's data-export requirement.
5. Compliance discovers the gap only during a periodic audit, and neither
   team had visibility into how the other's policy interacted with theirs.
```

## Statistics
| Finding | Context |
|---------|---------|
| Organizations with more than one tier of policy authorship (global plus team/regional) commonly report a nontrivial share of policy pairs with undetected conflicts, often in the range of 5-15% of overlapping policy pairs in large audits | Typical finding in multi-tier governance reviews |
| Policy engines without an explicit precedence model are disproportionately represented in consistency-violation findings compared to engines with a documented precedence hierarchy | Consistent with the role of implementation-order artifacts in producing inconsistent outcomes |
| Conflicts between global and team-level policies are found more often to unintentionally loosen, rather than tighten, the effective control | Reflects the common motivation for team-level overrides being speed/friction reduction |

## Mitigations
1. **Explicit, documented precedence hierarchy**: Define and enforce a clear rule (e.g., "team policies may only add restrictions, never remove ones imposed by a global policy") and implement it as an explicit precedence check in the policy engine, not implicit evaluation order.
2. **Conflict detection at policy publish time**: When a new or updated policy is published, automatically check it against existing policies covering overlapping scope and flag direct conflicts before the policy goes live.
3. **Deterministic, most-restrictive-wins evaluation for conflicts**: Where no explicit precedence is defined and a genuine conflict is detected, default to the more restrictive requirement rather than an arbitrary evaluation order, and flag the conflict for resolution.
4. **Cross-team policy review board**: Require any team-level policy that touches a domain already covered by a global policy to go through a joint review with the global policy's owning team before publication.
5. **Periodic cross-policy consistency audit**: Run automated checks on a regular cadence that compare all active policies pairwise for overlapping scope and contradictory requirements, independent of any single incident triggering the review.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `policy_conflict_pair_count` | Number of active policy pairs with detected contradictory requirements over overlapping scope | > 0 (target: zero unresolved conflicts) |
| `evaluation_order_dependent_outcome_rate` | Share of actions whose approval outcome would change under a different policy evaluation order | > 0.5% of evaluated actions |
| `unreviewed_team_policy_count` | Number of team-level policies published without cross-review against overlapping global policies | > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Contradictory policies detected on overlapping scope | Two active policies impose different requirements on the same action class with no defined precedence | Critical | Apply most-restrictive-wins as interim default, escalate to governance for precedence resolution |
| Team policy published without global review | A team-level policy touching a globally-governed domain goes live without cross-team sign-off | Warning | Flag for retroactive review, hold enforcement pending confirmation of consistency |

## Related Patterns
- [Policy Ambiguity Exploitation](./policy-ambiguity-exploitation.md) - both involve gaps in policy design that produce unintended enforcement outcomes
- [Policy Version Mismatch](./policy-version-mismatch.md) - both result in an agent applying the wrong policy content due to a gap between authoritative and evaluated policy state
- [Policy Scope Misunderstanding](./policy-scope-misunderstanding.md) - both involve incorrect determination of which policy actually governs a given action
