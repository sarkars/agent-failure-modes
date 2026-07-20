# Domain Exception Not Handled

## Issue
An agent correctly retrieves and applies a general domain rule, but fails to recognize that the specific case at hand falls under a documented exception that overrides or modifies the general rule. The exception exists in the knowledge base — often in a separate section, footnote, or appendix — but the agent's retrieval or reasoning never connects the specific case to it, so the general rule is applied as if it were universal.

**Frequency**: Common

**Symptoms**
- Agent output matches the general rule exactly but is wrong for the specific case
- A documented exception for the exact scenario exists in the same knowledge source, unretrieved or unweighted
- Domain experts respond with "that's the general rule, but this case is an exception because..."
- Errors cluster around edge cases, minority populations, or non-standard configurations that are precisely where exceptions tend to live

## Root Cause
General rules are usually the dominant pattern in a knowledge base — stated prominently, repeated across many documents, and semantically central to the topic — while exceptions are comparatively rare, often confined to a single caveat sentence, a footnote, or a separate "special cases" document. Standard retrieval, which favors high-frequency and high-relevance content, systematically under-retrieves exceptions relative to the general rule they modify. Even when an exception is retrieved alongside the general rule, the agent has no built-in precedence logic telling it that a specific, narrowly-scoped exception should override a general rule when both apply — so it can default to the more prominent, more frequently-reinforced general statement.

## Example
```
A tax-guidance agent is asked whether contributions to a specific
retirement account type are tax-deductible for a user who mentions,
in passing, that they are also covered by an employer-sponsored plan.

The agent retrieves the general rule: "Contributions to this account
type are tax-deductible up to the annual limit." It answers yes,
citing the general limit.

The knowledge base separately documents an exception: taxpayers covered
by an employer-sponsored plan are subject to income-based phase-out
rules that can reduce or eliminate the deduction entirely. This
exception lives in a separate subsection titled "Coverage by
Employer Plans" that was not retrieved because the user's question
was phrased around the account type, not employer coverage.

The user follows the agent's guidance, claims a deduction they were
not eligible for, and discovers the error only when reconciling with
a tax preparer months later.
```

## Statistics
| Finding | Context |
|---------|---------|
| Documented exceptions are retrieved alongside their governing general rule in an estimated 40-60% of queries where both are relevant | Estimated from retrieval-recall audits in policy/compliance-heavy domains |
| Cases matching a documented exception show a markedly higher error rate than cases matching only the general rule | Typical pattern observed in domain-QA evaluations of rule-heavy knowledge bases |
| Explicit exception-linking (structurally attaching exceptions to the rules they modify) cuts missed-exception errors substantially in tested systems | Reported range across teams that added rule-exception linking |

## Mitigations
1. **Structural rule-exception linking**: At ingestion time, explicitly link each documented exception to the general rule(s) it modifies, so retrieving the general rule always surfaces its known exceptions rather than relying on independent semantic match.
2. **Exception-triggering condition extraction**: Extract the specific conditions that trigger each exception (e.g. "employer plan coverage," "population under 18") into structured metadata, and check user-provided facts against these conditions explicitly rather than relying on free-text retrieval to catch them.
3. **General-rule hedging by default**: When answering with a general rule in a domain known to have exceptions, default to a caveat ("this is the general rule; certain circumstances such as X or Y can change the answer — do any apply to you?") rather than presenting the general case as unconditionally correct.
4. **Precedence logic for rule conflicts**: Where both a general rule and a specific exception are retrieved, apply explicit precedence logic favoring the more specific, narrowly-scoped rule rather than defaulting to whichever is more prominent in context.
5. **Exception coverage audit**: Periodically sample knowledge-base rules with known exceptions and verify retrieval surfaces the exception when the triggering condition is present in the query.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| exception_co_retrieval_rate | Share of queries matching a known exception's trigger condition where the exception is actually retrieved alongside the general rule | Alert if < 90% |
| exception_miss_correction_rate | Rate of user/expert corrections citing a missed documented exception | Alert if > 3% of rule-based responses |
| general_rule_only_response_rate | Share of responses in exception-heavy domains that cite only the general rule with no hedge | Track trend; alert on sustained increase |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Exception miss confirmed | Review or user correction confirms a documented exception was applicable but not surfaced | High | Add structural link between rule and exception, audit similar recent queries |
| Low exception co-retrieval | Audit finds exception co-retrieval rate below threshold for a rule with known exceptions | Medium | Prioritize structural linking for the affected rule set |

## Related Patterns
- [Domain Rule Misunderstanding](./domain-rule-misunderstanding.md) - both involve misapplying a domain rule's scope, one via ignoring an exception and one via misreading the rule itself
- [Domain Constraint Violation](./domain-constraint-violation.md) - exceptions can themselves function as hard constraints when missed, producing this more severe failure mode
- [Knowledge Contradiction Unresolved](./knowledge-contradiction-unresolved.md) - a general rule and its exception can look like a contradiction if the linking metadata connecting them is absent
