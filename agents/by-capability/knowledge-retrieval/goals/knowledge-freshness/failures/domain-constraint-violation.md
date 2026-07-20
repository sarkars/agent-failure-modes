# Domain Constraint Violation

## Issue
An agent produces output or takes an action that violates a hard, non-negotiable constraint of the domain it's operating in — a regulatory requirement, a safety interlock, a licensing restriction — because the constraint was never surfaced by its retrieval layer. Unlike a best-practice miss, this isn't a matter of degree: the agent crosses a bright line (e.g. recommending a drug dosage that exceeds a labeled maximum, or drafting a contract clause that's unenforceable in a given jurisdiction) because its knowledge base treated the constraint as optional context rather than a gating rule.

**Frequency**: Occasional

**Symptoms**
- Agent output later found to violate a specific named regulation, statute, or safety limit
- No refusal or caveat produced even though the violated constraint is well-documented and unambiguous
- Constraint exists in the knowledge base but was retrieved as low-relevance background rather than as a blocking rule
- Downstream human reviewers catch violations that a constraint-aware system should have blocked upstream

## Root Cause
Retrieval systems typically rank content by semantic relevance to the query, not by whether the content encodes a hard constraint versus optional guidance. A regulatory maximum buried in a compliance document competes for retrieval "slots" against dozens of more topically-relevant but non-binding passages, and unless the system explicitly tags and always-includes constraint-type content, it can lose that competition and never reach the agent's context window at all. Even when retrieved, the agent has no architectural distinction between "this passage is advisory" and "this passage is a gate that must be checked before acting" — both are just text in context, weighted the same as everything else.

## Example
```
A healthcare-adjacent agent is asked to draft patient-facing guidance on
a medication's typical dosing schedule for a specific patient population
(pediatric, low body weight).

The agent's retrieval pulls general dosing information from a medical
reference doc but does not surface a separate, specifically-tagged
"contraindications and hard maximums" section of the same source that
caps the pediatric dose at a lower threshold than the adult-derived
recommendation the agent generalizes from.

The drafted guidance recommends a dose 40% above the pediatric hard
maximum. A pharmacist reviewing the output before it reaches any patient
catches the constraint violation, but in a lower-oversight deployment
this would have reached a caregiver directly.
```

## Statistics
| Finding | Context |
|---------|---------|
| Hard-constraint content is retrieved into context in an estimated 55-70% of queries where it is topically relevant but not the top semantic match | Estimated from retrieval-recall audits in regulated-domain agent deployments |
| Constraint-violation incidents are 3-5x more likely when the constraint is documented in a separate section/document from the general guidance the agent is generalizing from | Typical pattern observed in regulated-domain agent audits |
| Explicit constraint-gating layers (checked independent of retrieval ranking) reduce hard-constraint violations by a large majority in tested deployments | Reported range across teams that added dedicated constraint checks |

## Mitigations
1. **Constraint tagging and forced inclusion**: Tag hard-constraint content (regulatory limits, safety maximums, licensing restrictions) at ingestion time and always include it in context for any query touching its domain, independent of semantic relevance ranking.
2. **Post-generation constraint gate**: Run a dedicated, deterministic check (rules engine, not the generating model) against known hard constraints before any output reaches the user, separate from and in addition to retrieval-informed generation.
3. **Constraint registry decoupled from general knowledge base**: Maintain regulatory/safety constraints in a structured, queryable registry rather than as prose buried in general reference documents, so they can't lose a relevance-ranking competition.
4. **Jurisdiction/population scoping on constraints**: Require every hard constraint entry to carry explicit applicability metadata (population, jurisdiction, product line) so the gate can correctly match constraints to the situation rather than applying or missing them by accident.
5. **Human sign-off for constraint-adjacent domains**: For domains with severe violation consequences, require human review before output release regardless of automated gate results, and treat the gate as a triage aid rather than sole enforcement.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| constraint_retrieval_recall | Share of queries where a relevant hard constraint was actually present in context | Alert if < 98% for tagged constraint domains |
| constraint_violation_rate | Rate of outputs found (via review or gate) to violate a known hard constraint | Alert if > 0 for safety-critical domains |
| unscoped_constraint_matches | Count of constraint checks that misfired due to missing applicability metadata | Alert if trending upward |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Hard constraint violated in output | Post-generation gate or human review flags a domain hard-constraint violation | High | Block output immediately, halt agent for the session, escalate for incident review |
| Constraint retrieval miss detected | Audit finds a relevant hard constraint absent from context for a matching query | Medium | Add forced-inclusion rule for the constraint, backfill audit of recent similar queries |

## Related Patterns
- [Domain Exception Not Handled](./domain-exception-not-handled.md) - both involve missing a documented rule, but this one is a hard block rather than an exception to a general rule
- [Domain Rule Misunderstanding](./domain-rule-misunderstanding.md) - shares the mechanism of misapplied domain rules, differing in severity (hard constraint vs. general rule)
- [Domain Risk Blindness](./domain-risk-blindness.md) - related in that both stem from knowledge lacking domain-relevance weighting, one for risk factors and one for hard limits
