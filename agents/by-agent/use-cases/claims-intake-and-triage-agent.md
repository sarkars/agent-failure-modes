# Insurance Claims Intake and Triage Agent: Business Goals, Failure Definitions, and Test List

An agent that takes a first notice of loss, collects the facts, and routes the claim to the right queue at the right priority. It does not decide coverage.

> **Read this first.** These are design starting points to adapt with your own business owners, not benchmarks or advice. No target numbers are given because none can be set without your baseline. Parts of this agent touch law or regulated practice (flags: L, E); get legal or expert review before use.

## Scope (a starting point)

**The agent does:**
- Collect a complete, accurate account of the loss
- Check what is on the policy and flag obvious questions for the adjuster
- Route by type, severity, and catastrophe status

**The agent does not:**
- Decide or promise coverage, payment, or amounts
- Accuse a claimant of fraud
- Give legal advice

## Business goals

| # | Goal | Success means | Owner |
|---|---|---|---|
| G1 | Capture a complete, accurate first notice of loss | The adjuster gets the facts needed without calling the claimant back for basics. | Claims operations manager |
| G2 | Route and prioritize correctly | Each claim reaches the right queue with the right urgency, including claims that are part of a larger event. | Claims operations manager |
| G3 | Never present a coverage decision as final | Claimants hear what is collected and what happens next, and never receive a coverage promise or denial from the agent. | Claims legal and compliance |
| G4 | Flag possible fraud without accusing or discriminating | Suspicious patterns go to the investigation team with the evidence, and claimants are not treated as suspects by the agent. | Head of special investigations with compliance |
| G5 | Handle a person in distress with care | Claimants who have lost a home, a car, or a family member are met with the right tone and a person when needed. | Head of claims experience |

## Goal definitions

For every goal: how to measure it, how to find your baseline, what counts as a failure and how severe it is, and when the agent hands over to a person. Baseline method for all goals: Take a sample of conversations or cases the way a person handled them over a period you choose (one vendor's guidance uses 90 days as an example) and compute the same measure. A statement like "it takes too long" is not a baseline.

### G1. Capture a complete, accurate first notice of loss

| Field | Definition |
|---|---|
| How to measure | Share of claims that need a callback for missing basic facts; field-level accuracy against the final claim file. |
| A failure is | Missing or wrong dates, parties, or policy details; the wrong policy version or endorsement used. |
| Severity | High: a wrong loss date or wrong policy applied. Medium: missing contact details. |
| Hand over to a person when | The claimant is unable to complete the intake, or details conflict. |

**Failures to test for this goal (from the library):**
- [Embedding-Retrieval Wrong Endorsement Version Applied](../../by-use-case/insurance/goals/claim-processing/failures/embedding-retrieval-wrong-endorsement-version-applied.md): A Claims-Adjudication Agent's RAG Retrieval Step Pulls a Lexically Similar but Superseded or Wrong-State Policy Endorsement from the…
- [Stale Training-Corpus Prompt-Payment Deadline Overrides Current State Statute](../../by-use-case/insurance/goals/claim-processing/failures/stale-training-corpus-prompt-payment-deadline-overrides-current-state-statute.md): A Claims-Processing Agent Determining the Statutory Deadline by Which a Claim Must Be Acknowledged, Investigated, or Paid Under a Given…

### G2. Route and prioritize correctly

| Field | Definition |
|---|---|
| How to measure | Misroute rate and time-to-first-contact by priority class, from audited samples. |
| A failure is | Urgent claims are queued as routine, or claims from one event are treated as unrelated. |
| Severity | Critical: an injury or safety-related claim not escalated. High: a catastrophe-related surge handled as routine. Medium: a wrong queue. |
| Hand over to a person when | Injury, safety, or a possible total loss; any claim tagged to a catastrophe event. |

**Failures to test for this goal (from the library):**
- [Catastrophe Correlation Blindness](../../by-use-case/insurance/goals/claims-processing/failures/catastrophe-correlation-blindness.md): Catastrophe risk model assumes independent claims; hurricane hits coast, model hadn't provisioned for 10k simultaneous claims; reserve…

### G3. Never present a coverage decision as final

| Field | Definition |
|---|---|
| How to measure | Sampled review: replies that state or imply coverage, denial, or an amount. Target: zero. |
| A failure is | The agent says "you are covered", states an amount, or misses an exclusion noted earlier in the file. |
| Severity | Critical: a coverage promise or denial stated as final. High: a missed exclusion noted by an earlier step. |
| Hand over to a person when | Any question about coverage, amounts, or a denial. |

**Failures to test for this goal (from the library):**
- [Multi-Agent Handoff Drops Noted Exclusion Before Payment Step](../../by-use-case/insurance/goals/claim-processing/failures/multi-agent-handoff-drops-noted-exclusion-before-payment-step.md): A Coverage Exclusion Identified by an Earlier Stage of a Multi-Agent Claims Pipeline (Intake → Triage → Adjudication → Payment) Is Surfaced…

### G4. Flag possible fraud without accusing or discriminating

| Field | Definition |
|---|---|
| How to measure | Precision of fraud flags after investigation; false-flag rate by claimant group; claims delayed by a flag. |
| A failure is | Unrelated claimants matched as a fraud ring, dropped conflicting dates, or outdated red-flag lists applied. |
| Severity | High: an innocent claimant delayed or accused. Medium: a missed flag a human would have caught. |
| Hand over to a person when | Any flag goes to the investigation team; the agent says nothing to the claimant about it. |

**Failures to test for this goal (from the library):**
- [Embedding Retrieval Flags Unrelated Claimant as Fraud-Ring Match](../../by-use-case/insurance/goals/fraud-detection/failures/embedding-retrieval-flags-unrelated-claimant-as-fraud-ring-match.md): A Fraud-Detection Agent's Link-Analysis Retrieval Step, Which Searches for Claimants Embedding-Similar to Known Fraud-Ring Members Based on…
- [Multi-Agent Handoff Drops Pre-Inception Loss-Date Conflict Before SIU Triage](../../by-use-case/insurance/goals/fraud-detection/failures/multi-agent-handoff-drops-pre-inception-loss-date-conflict-before-siu-triage.md): An Initial-Review Agent's Free-Text Note Flagging That a Claimant's Reported Loss Date Appears to Predate the Policy's Effective Date Is…
- [Stale Training-Corpus Fraud Typology Overrides Current SIU Red-Flag List](../../by-use-case/insurance/goals/fraud-detection/failures/stale-training-corpus-fraud-typology-overrides-current-siu-red-flag-list.md): A Fraud-Detection Agent Screening Claims for SIU Referral Applies a Generic Fraud-Typology Pattern Absorbed During Pretraining (e.g., a…

### G5. Handle a person in distress with care

| Field | Definition |
|---|---|
| How to measure | Complaints about tone; share of sensitive-loss intakes handed to a trained person. |
| A failure is | A form-filling tone in a moment of loss, or missed signs of crisis. |
| Severity | Critical: a crisis signal missed. High: cold handling of a major loss. |
| Hand over to a person when | Any crisis signal, a death, or a total loss. |

**Failures to test:** none documented in the library yet for this goal; this is a gap to fill.

## Conversation-level failures to check

This agent talks to people. Also test these:
- [stakes-blind register](../../by-capability/human-machine-interface/goals/stakes-calibration/failures/stakes-blind-register.md)
- [missed crisis signals](../../by-capability/human-machine-interface/goals/vulnerable-users/failures/missed-crisis-signals.md)
- [no channel switch or context lost](../../by-capability/human-machine-interface/goals/channel-selection/failures/no-channel-switch-or-context-lost.md)

## Operations concerns for this agent

| Area | Why it matters here | Patterns |
|---|---|---|
| [Tool Reliability](../../cross-cutting/operations/goals/tool-reliability/) | Policy and claim systems must be queried live | 19 |
| [State Tracking](../../cross-cutting/operations/goals/state-tracking/) | Facts gathered over the conversation must not be lost or invented | 9 |
| [Agent Handoffs Delegation](../../cross-cutting/operations/goals/agent-handoffs-delegation/) | Intake hands to routing, investigation, and adjusters | 10 |
| [Memory Safety](../../cross-cutting/operations/goals/memory-safety/) | Claimant data must not leak between claims | 10 |
| [Traceability](../../cross-cutting/operations/goals/traceability/) | Claims decisions are audited | 8 |
| [Human Oversight Reliability](../../cross-cutting/operations/goals/human-oversight-reliability/) | High-priority claims must reach a person | 8 |

## Security and governance to check

- [Data Loss Prevention](../../cross-cutting/security/goals/data-loss-prevention/) (security)
- [Tool Authorization Limits](../../cross-cutting/security/goals/tool-authorization-limits/) (security)
- [Governance](../../cross-cutting/governance/goals/governance/) (governance)
- [Verification](../../cross-cutting/accuracy/goals/verification/) (accuracy)

## Decisions your business owner must make

- The exact words the agent may and may not use about coverage
- Which events count as injury or safety escalations
- What the investigation team needs in a flag
- Which jurisdictions' rules apply to the script and recordings

## Related

- [All agents by business goal](../)
