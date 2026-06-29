# Self-Verification Illusion in Coverage-Determination Recheck

## Issue: When a Claims-Adjuster Agent Is Asked to "Double-Check" Its Own Coverage Determination Before Issuing Payment, the Recheck Re-Runs the Same Model Against the Same Already-Cached Policy Snapshot Rather Than Re-Pulling the Current Policy Record, So a Mid-Term Endorsement or Exclusion Added After the Snapshot Was Cached Is Never Surfaced

**Frequency**: Occasional

**Symptoms**
- A claim is approved for payment under a coverage determination that the policy's current, live record would have excluded or modified, even though a "coverage recheck" step ran before payment and reported no issues
- The recheck step's tool-call trace shows it reused the same cached policy snapshot retrieved earlier in the claim-handling session rather than issuing a fresh policy-record query, even when significant time has elapsed since the snapshot was cached
- Confidence language in the recheck output ("coverage confirmed," "no exclusions apply") appears consistent between the first pass and the recheck even on claims where the policy record was modified by a mid-term endorsement between the snapshot being cached and the recheck running
- Claims rechecked with a freshly re-pulled policy record (rather than the cached snapshot) show a materially different coverage-determination rate than claims rechecked against the same cached snapshot used for the original determination
- The recheck rarely reverses the original coverage determination even on claims where an independent post-payment audit finds the policy had been modified mid-term, indicating the recheck is not functioning as a genuine error-catching step

**Root Cause**
Asking an LLM agent to verify its own prior coverage determination by re-prompting it against the same cached policy snapshot does not introduce an independent or more current source of evidence; the model has no privileged access to whether the policy record has changed since the snapshot was cached, so its "recheck" is largely a restatement of the same token-level reasoning applied to the same stale data, rather than a genuine re-verification against the policy's current, authoritative state. This differs from genuine verification, which requires a fresh query against the policy system of record at the time of the recheck, not a re-read of data already held in the agent's working context.

**Example**
```
Claims-adjuster agent caches the policy record at the start of claim handling and determines a water-damage claim is covered under the policy's current endorsement set
Three days later, before issuing payment, the workflow runs a "coverage recheck" step that re-prompts the same agent: "Double-check this coverage determination before payment"
Recheck reuses the cached policy snapshot from three days earlier rather than re-querying the policy system, and restates "coverage confirmed, no exclusions apply"
Policyholder's broker had submitted a water-damage exclusion endorsement two days after the snapshot was cached, which is now reflected in the policy system of record but was never re-pulled by the recheck step
Claim is paid despite the now-current policy excluding the loss, discovered only when a post-payment audit compares the payment against the policy system's current endorsement history
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Calibration in autonomous, tool-using agents remains notably underexplored relative to single-turn LLM calibration, and self-confirmation by the same model operating on the same cached data is not equivalent to independent verification | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |
| Self-reflection enables agents to critique their own outputs, but reflective self-checks that operate on the same evidence and same underlying model risk self-reinforcing the original conclusion rather than catching genuine errors | [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1) |
| Agentic AI applications in insurance decision-making are documented to require explicit re-grounding against live policy and claims systems of record, rather than relying on previously cached state, to maintain decision accuracy over multi-step workflows | [LLMs and Agentic AI in Insurance Decision-Making: Opportunities and Challenges For Africa](https://arxiv.org/html/2508.15110) |

**Contributing Factors**
- Recheck step reuses the cached policy snapshot from earlier in the claim-handling session rather than issuing a fresh query to the policy system of record
- Prompt framing for the recheck ("double-check this determination") biases the model toward confirming its own prior reasoning rather than re-deriving the determination from current data
- No tracking distinguishes "rechecked against a freshly pulled policy record" from "rechecked against the same cached snapshot," so the two are reported identically as a completed coverage recheck

---

## Mitigation Strategies

1. **Mandatory Fresh Policy-Record Pull on Recheck**: Require the coverage-recheck step to issue a fresh query against the policy system of record rather than reusing any cached snapshot from earlier in the claim-handling session, regardless of how recently the snapshot was cached
2. **Snapshot-Age Threshold Forcing Re-Pull**: Define a maximum age for any cached policy snapshot used in a coverage determination; any recheck running after that threshold must re-pull the policy record before proceeding
3. **Mid-Term Endorsement Change Flag**: Have the policy system of record emit a change event on any mid-term endorsement or exclusion addition, and require any in-flight claim referencing that policy to be automatically re-flagged for a fresh coverage recheck when such an event occurs
4. **Track Recheck-Type Outcome Divergence**: Continuously measure and report the coverage-reversal rate separately for rechecks using a freshly pulled policy record versus rechecks reusing a cached snapshot; a large divergence is itself evidence that the cached-snapshot recheck is not functioning as verification

### Metrics
- Rate of coverage rechecks that reuse a cached policy snapshot versus those that issue a fresh policy-record query
- Coverage-determination reversal rate, segmented by fresh-pull recheck vs. cached-snapshot recheck
- Time lag between a mid-term endorsement change and the corresponding in-flight claim being re-flagged for recheck

### Alerts
- A claim is paid following a coverage recheck that reused a cached policy snapshot older than the defined maximum age → P1
- A mid-term endorsement or exclusion change is recorded for a policy with an in-flight claim and no automatic recheck re-flag fires within the defined SLA → P1
- Post-payment audit finds a paid claim whose coverage determination would differ under the policy's current endorsement set → P1

---

## References

- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
- [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1)
- [LLMs and Agentic AI in Insurance Decision-Making: Opportunities and Challenges For Africa](https://arxiv.org/html/2508.15110)
