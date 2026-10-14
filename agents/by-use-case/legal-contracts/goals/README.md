# Legal Contracts AI Agent Failures by Goal: 30 Patterns, Causes, and Fixes

**Legal Contracts failures in AI agents are grouped here into 8 goals, each with a catalog of named failure patterns, the symptoms you will see, the root cause, and mitigations you can copy.** Start from the symptom you are debugging, pick the matching goal below, and open its failure list.

## Key Takeaways

- This use case covers 8 goals and 30 documented failure patterns.
- The largest goal is [Risk Detection](risk-detection/) with 5 patterns.
- Each goal page explains the failure class, how to tell it apart from its neighbors, and which mitigations apply across its patterns.
- Each failure page covers the symptoms, an example, the root cause, and how to fix it.

## Legal Contracts Goals

| Goal | What goes wrong | Patterns |
|---|---|---|
| [Compliance](compliance/) | Compliance failures happen when a compliance agent reasons from a stale or mismatched snapshot of the law or the contract instead of its current, jurisdiction-correct state | 4 |
| [Contract Drafting](contract-drafting/) | Contract drafting failures concentrate at three integration points | 4 |
| [Due Diligence](due-diligence/) | Due-diligence failures happen when an agent reasoning over disclosed financial facts or contract terms constructs a causal or correlational narrative that drifts from the supporting evidence | 4 |
| [Ip Rights](ip-rights/) | IP-rights failures happen when an agent confirms the presence of IP-assignment language without verifying that the mechanism actually transfers title under the specific work category and jurisdiction at issue | 4 |
| [Jurisdiction Handling](jurisdiction-handling/) | Jurisdiction-handling failures happen when a contract-drafting or compliance agent applies a rule from the wrong jurisdiction without detecting the mismatch | 3 |
| [Litigation Support](litigation-support/) | Litigation-support failures concentrate on three points in the evidence-handling pipeline | 3 |
| [Precedent Currency](precedent-currency/) | Precedent-currency failures happen when a legal research agent cites a case as controlling law without checking whether it has been overruled | 3 |
| [Risk Detection](risk-detection/) | Risk-detection failures happen when an agent confirms the presence of a risk-mitigating clause (limitation-of-liability, indemnification, termination terms) without evaluating its actual scope, cap, or enforceability | 5 |

**Total: 30 patterns**

## Frequently Asked Questions

### Where do I start if my legal contracts agent is failing?

Match the symptom to a goal in the table above, then open that goal's page for how to tell its failures apart and where to look first. Each failure page ends in mitigations you can apply directly.

### How are these legal contracts failure patterns organized?

By goal: the outcome the agent is supposed to achieve. Under each goal, a `failures` folder holds one page per pattern. For the full picture see the [Legal Contracts overview](../).

## Related

- [Legal Contracts overview](../)
- [All agent failure patterns](../../../)
