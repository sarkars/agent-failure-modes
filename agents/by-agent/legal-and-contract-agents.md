# Legal and Contract Agents: Business Goals, Failure Patterns, and Fixes

**Legal and Contract Agents fail along 8 goals: Risk Detection, Compliance, Contract Drafting carry the most documented failures.** This page maps each goal to the failures that threaten it, so you can decide what to protect first and where the fixes are.

## Key Takeaways

- 30 documented failure patterns across 8 goals. What it does: review, draft, and check contracts and support due diligence.
- The most documented goal is [Risk Detection](../by-use-case/legal-contracts/goals/risk-detection/) with 5 patterns.
- Frequencies below are as recorded on each pattern page. They are not measured rates.
- Business-goal definitions (metric, baseline, owner, what counts as a failure) are not written yet for this agent. Define them before choosing which patterns to prioritize.

## Goals this agent must protect

| Goal | When it fails | Patterns |
|---|---|---|
| [Risk Detection](../by-use-case/legal-contracts/goals/risk-detection/) | When an agent confirms the presence of a risk-mitigating clause | 5 |
| [Compliance](../by-use-case/legal-contracts/goals/compliance/) | When a compliance agent reasons from a stale or mismatched snapshot of the law or the contract instead of its current | 4 |
| [Contract Drafting](../by-use-case/legal-contracts/goals/contract-drafting/) | Contract drafting failures concentrate at three integration points | 4 |
| [Due Diligence](../by-use-case/legal-contracts/goals/due-diligence/) | When an agent reasoning over disclosed financial facts or contract terms constructs a causal or correlational narrative that drifts from the supporting evidence | 4 |
| [Ip Rights](../by-use-case/legal-contracts/goals/ip-rights/) | When an agent confirms the presence of IP-assignment language without verifying that the mechanism actually transfers title under the specific work category and | 4 |
| [Jurisdiction Handling](../by-use-case/legal-contracts/goals/jurisdiction-handling/) | When a contract-drafting or compliance agent applies a rule from the wrong jurisdiction without detecting the mismatch | 3 |
| [Litigation Support](../by-use-case/legal-contracts/goals/litigation-support/) | When vocabulary shifts (code names, abbreviations, terminology drift over time) cause the classifier to miss genuinely responsive documents | 3 |
| [Precedent Currency](../by-use-case/legal-contracts/goals/precedent-currency/) | When a legal research agent cites a case as controlling law without checking whether it has been overruled | 3 |

## Failures most often recorded

| Failure | What goes wrong | Recorded frequency |
|---|---|---|
| [Boilerplate Clause Misapplication](../by-use-case/legal-contracts/goals/contract-drafting/failures/boilerplate-clause-misapplication.md) | Agent Drafts a New Contract by Inserting a Standard Boilerplate Clause Library Entry That Is Inconsistent With Deal-Specific Terms Negotiated… | Very Common |
| [Contract Amendment Tracking Failure](../by-use-case/legal-contracts/goals/compliance/failures/amendment-tracking-failure.md) | Contract Modified Multiple Times; Model Analyzes Original, Ignoring Amendments; Outdated Analysis Given | Common |
| [Change-of-Control Clause Omission in M&A Due Diligence](../by-use-case/legal-contracts/goals/due-diligence/failures/change-of-control-clause-omission.md) | Agent Reviewing a Target Company's Contract Portfolio for M&A Due Diligence Fails to Flag Change-of-Control Provisions That Trigger on the… | Common |
| [Choice-of-Law & Jurisdiction Mishandling](../by-use-case/legal-contracts/goals/jurisdiction-handling/failures/choice-of-law-mishandling.md) | Model Fails to Properly Interpret Choice-of-Law Clauses; Applies Wrong Jurisdiction's Laws to Obligations | Common |
| [Circuit Split Blindness in Citation Selection](../by-use-case/legal-contracts/goals/precedent-currency/failures/circuit-split-blindness-in-citation-selection.md) | Legal Research Agent Cites a Precedent as Settled Law Without Flagging That a Circuit Split (or Equivalent Jurisdictional Disagreement) Exists,… | Common |
| [Contract Ambiguity Detection Failure](../by-use-case/legal-contracts/goals/risk-detection/failures/contract-ambiguity-misses.md) | Model Misses Ambiguous or Conflicting Clauses in Contracts; Leads to Dispute When Parties Interpret Differently | Common |

## Before you build: define each goal

For every goal in the table, write down: the metric and how you measure its baseline today; the person who owns it; what counts as a failure and how severe it is; who is told when it happens; and when a person takes over. Then use the failures above as your test list.

## Security and governance

Every agent also needs the cross-cutting checks in [security](../cross-cutting/security/), [accuracy](../cross-cutting/accuracy/), [governance](../cross-cutting/governance/), and [operations](../cross-cutting/operations/).

## Frequently Asked Questions

### What fails most often in legal and contract agents?

The most documented goal is Risk Detection (5 patterns). The failures table above lists the ones recorded as most frequent. These are the library's records, not measured rates.

### Where should I start when building legal and contract agents?

Define your business goals and what counts as failure, then test against the failure patterns for each goal. The section above lists what to write down.

## Related

- [All agents by business goal](./)
