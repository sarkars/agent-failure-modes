# Domain Rule Misunderstanding

## Issue
An agent retrieves a correctly-stated domain rule but misapplies it because it misreads the precise conditions under which the rule holds — extending it to cases just outside its actual scope, or narrowing it to exclude cases it actually covers. The rule text itself is never altered or hallucinated; the failure is in the agent's interpretation of qualifying language like "only if," "except when," or "applies to X but not Y" that defines the rule's true boundary.

**Frequency**: Common

**Symptoms**
- Agent quotes or paraphrases the rule accurately but applies it to a case outside its documented scope
- Errors cluster around rules with compound conditions (multiple ANDs/ORs) or negated qualifiers
- Domain experts describe the error as "it got the rule right but applied it wrong"
- The same rule is applied correctly in simple cases and incorrectly in cases with boundary conditions

## Root Cause
Domain rules are frequently expressed in dense, conditional prose — "this applies when A and B, unless C, in jurisdictions where D" — and correctly parsing compound and negated conditions requires precise logical reading that language generation can get subtly wrong even while reproducing the rule's wording faithfully. The failure is a scope-boundary error, not a factual error: the agent isn't wrong about what the rule says, it's wrong about which cases the rule's conditions actually pick out. This is especially likely when a case sits near a boundary condition (e.g. just inside or just outside a "unless" clause), because the semantic distance between "matches the rule" and "matches the exception to the rule" can be small in the case description while being decisive in the actual outcome.

## Example
```
An HR-policy agent is asked whether a contractor who has worked for the
company for 11 months, on a renewing 3-month contract, qualifies for a
benefit that the retrieved policy states applies to "employees who have
completed 12 consecutive months of service, excluding contractors
engaged on a project basis but including contractors on standing
renewable agreements of 6+ months."

The agent correctly retrieves the policy text but misapplies the
"excluding contractors" clause as a blanket exclusion, missing that the
subsequent "including contractors on standing renewable agreements of
6+ months" clause carves this specific contractor back in. It tells the
user they don't qualify.

The contractor, relying on this answer, doesn't file for the benefit
before a deadline, and later learns from HR directly that the standing-
agreement carve-back applied to their exact situation.
```

## Statistics
| Finding | Context |
|---------|---------|
| Rules with 2+ compound conditions (AND/OR/exception chains) show a markedly higher misapplication rate than single-condition rules in domain-QA evaluation | Typical pattern observed in policy-QA benchmark evaluations |
| Cases within a narrow margin of a rule's boundary condition are misclassified at several times the rate of cases clearly inside or outside the rule | Estimated from boundary-case testing in rule-heavy domains |
| Decomposing compound rules into explicit conditional logic (rather than leaving them as prose) reduces misapplication substantially in tested systems | Reported range across teams that added rule decomposition |

## Mitigations
1. **Rule decomposition into structured conditions**: At ingestion, parse compound domain rules into explicit structured conditions (each AND/OR/exception as a separate checkable clause) rather than leaving them as prose for the agent to interpret at generation time.
2. **Boundary-case test suites**: Build evaluation sets specifically targeting cases near each rule's boundary conditions, since these are where misapplication concentrates and general-case testing won't catch them.
3. **Explicit clause-by-clause application in reasoning**: Require the agent to walk through each condition of a compound rule against the case facts individually and show which clause determined the outcome, making misapplied clauses visible and auditable rather than hidden in a single-shot answer.
4. **Confidence-scaled hedging near boundaries**: When a case's facts are close to a rule's boundary condition, have the agent flag the proximity and recommend human/expert confirmation rather than issuing a confident answer.
5. **Domain-expert rule review**: Have domain experts review the structured decomposition of high-stakes rules (not just the original prose) to confirm the parsed conditions match actual practice, since misparsing can happen at ingestion as well as at generation.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| compound_rule_accuracy | Accuracy on cases involving rules with 2+ compound conditions, tracked separately from simple-rule accuracy | Alert if > 10 percentage points below simple-rule accuracy |
| boundary_case_error_rate | Error rate specifically on cases within a defined margin of a rule's boundary condition | Alert if > 15% |
| rule_misapplication_correction_rate | Rate of expert corrections describing errors as rule misapplication rather than factual error | Track trend; alert on sustained increase |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Boundary-case misapplication confirmed | Expert review confirms a rule was misapplied on a boundary-condition case | High | Decompose the rule into structured conditions, add case to boundary test suite |
| Compound-rule accuracy regression | compound_rule_accuracy drops below simple-rule accuracy by more than threshold | Medium | Audit recently modified or added compound rules for decomposition gaps |

## Related Patterns
- [Domain Exception Not Handled](./domain-exception-not-handled.md) - a specific case of rule misunderstanding where the missed element is a documented exception rather than a general scope-boundary misread
- [Domain Constraint Violation](./domain-constraint-violation.md) - misunderstanding a rule's scope can directly cause a hard-constraint violation when the rule is safety- or compliance-critical
- [Fact Negation Confusion](./fact-negation-confusion.md) - shares the mechanism of mishandled negation/conditional language, at the level of a single fact rather than a compound rule
