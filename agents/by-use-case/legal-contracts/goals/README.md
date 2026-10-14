# Legal Contracts AI Agent Failures by Goal: 30 Patterns, Causes, and Fixes

**Legal Contracts AI agents fail in 8 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 30 documented patterns across 8 goals; the most documented is [Risk Detection](risk-detection/) with 5.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## Legal Contracts Goals

| Goal | When it fails | Patterns |
|---|---|---|
| [Compliance](compliance/) | When a compliance agent reasons from a stale or mismatched snapshot of the law or the contract instead of its current, jurisdiction-correct state | 4 |
| [Contract Drafting](contract-drafting/) | Contract drafting failures concentrate at three integration points: assembling boilerplate clauses without reconciling negotiated specifics | 4 |
| [Due Diligence](due-diligence/) | When an agent reasoning over disclosed financial facts or contract terms constructs a causal or correlational narrative that drifts from the supporting evidence | 4 |
| [Ip Rights](ip-rights/) | When an agent confirms the presence of IP-assignment language without verifying that the mechanism actually transfers title under the specific work category and jurisdiction at issue | 4 |
| [Jurisdiction Handling](jurisdiction-handling/) | When a contract-drafting or compliance agent applies a rule from the wrong jurisdiction without detecting the mismatch | 3 |
| [Litigation Support](litigation-support/) | When vocabulary shifts (code names, abbreviations, terminology drift over time) cause the classifier to miss genuinely responsive documents | 3 |
| [Precedent Currency](precedent-currency/) | When a legal research agent cites a case as controlling law without checking whether it has been overruled | 3 |
| [Risk Detection](risk-detection/) | When an agent confirms the presence of a risk-mitigating clause (limitation-of-liability, indemnification, termination terms) without evaluating its actual scope, cap, or enforceability | 5 |

**Total: 30 patterns**

## Frequently Asked Questions

### How do you evaluate indemnification risk beyond clause presence?

Build a structured indemnification analyzer: (1) locate indemnification clause and extract scope/direction, (2) locate limitation-of-liability clause, (3) extract all carve-outs from limitation, (4) for each carve-out, determine whether indemnification is carved out (uncapped) or capped, (5) quantify effective exposure. See [Risk Detection](risk-detection/).

### What causes a compliance agent to apply an outdated regulatory requirement?

A training-data cutoff combined with no retrieval step against a current, authoritative regulatory text source. See [Compliance](compliance/).

### How do you distinguish a clause version retrieved correctly from one that's just lexically similar?

Apply a deterministic lookup keyed to the clause's canonical version ID and context (jurisdiction, deal size) before attempting similarity ranking. See [Contract Drafting](contract-drafting/).

## Related

- [Legal Contracts overview](../)
- [All agent failure patterns](../../../)
