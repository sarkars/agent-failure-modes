# Knowledge Scope Assumption Wrong

## Issue
An agent applies a fact using an incorrectly assumed scope — the wrong jurisdiction, the wrong product version, the wrong organizational unit — because it never explicitly confirmed the scope the fact actually applies to versus the scope the user's situation is actually in. The fact is retrieved correctly and stated correctly for its true scope; the error is the silent assumption that the true scope matches the user's, when it may not.

**Frequency**: Very Common

**Symptoms**
- Agent answers with information correct for one jurisdiction/version/unit but the user is asking about a different one
- No clarifying question is asked about jurisdiction, version, or applicable unit before answering a scope-sensitive query
- The knowledge base contains scope-specific variants of the same fact, but only one was retrieved and its scope wasn't checked against the user's actual context
- Users in non-default scopes (non-US jurisdictions, older product versions, non-headquarters offices) experience a disproportionate share of these errors

## Root Cause
Retrieval and generation systems typically default to whichever scope is most represented in the knowledge base or most recently indexed — often the jurisdiction, version, or unit the organization treats as its primary reference case — and nothing forces an explicit check of whether that default matches the actual scope implied by the user's query. When a query doesn't explicitly state its scope (which is common, since users often don't think to specify jurisdiction or version unless prompted), the system silently assumes the default rather than treating scope as an unresolved variable that needs confirmation, so a scope mismatch produces a confident, correctly-sourced, wrong-for-the-user answer rather than an error or a clarifying question.

## Example
```
A company operates in the US, UK, and Germany, each with different data
retention policies. Its internal knowledge base contains distinct
retention-period documents for each jurisdiction, but the US document
is the oldest, most-referenced, and most topically prominent entry.

An employee in the Germany office asks an internal policy agent: "How
long do we need to retain customer records?" The agent retrieves and
answers using the US retention period (7 years) without checking or
asking which jurisdiction the employee is in, defaulting to the most
prominent document in the knowledge base.

Germany's retention requirement is materially different (governed by
GDPR-aligned rules with its own specific period). The employee, acting
on the US figure, either retains records too long (compliance exposure)
or deletes them too early, and the mismatch is only caught during a
compliance audit months later.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 15-25% of scope-sensitive queries (jurisdiction, version, unit) that don't explicitly state their scope result in a default-scope answer without any clarifying check | Estimated from scope-sensitivity audits of multi-jurisdiction/multi-version knowledge bases |
| Users in non-default scopes experience scope-mismatch errors at a markedly higher rate than users whose situation matches the knowledge base's dominant/default scope | Typical pattern observed in multi-region enterprise agent deployments |
| Adding an explicit scope-confirmation step for queries touching known scope-sensitive topics (retention, tax, licensing, product version) substantially reduces mismatch errors, at the cost of an extra clarifying turn | Reported range across teams that added scope-gating prompts |

## Mitigations
1. **Scope-sensitive topic tagging**: Identify and tag topics known to vary by jurisdiction/version/unit (retention policy, tax rules, feature availability), and require explicit scope confirmation before answering queries on tagged topics rather than defaulting silently.
2. **User-context-derived scope inference**: Where available, use known user context (account region, product version on file, org unit) to infer scope automatically rather than defaulting to the knowledge base's most prominent variant, and confirm the inference explicitly when confidence is low.
3. **Multi-scope retrieval with explicit disambiguation**: When a scope-sensitive topic has multiple scope-specific variants in the knowledge base, retrieve all relevant variants and either ask the user to select or clearly present the applicable one(s) rather than silently picking the single top-ranked match.
4. **Default-scope bias detection**: Periodically audit which scope variant of a fact is retrieved by default for ambiguous queries, and check whether that default reflects an actual majority-user scope or merely an accident of indexing order/prominence.
5. **Explicit "does this apply to you" framing**: When answering with a scope-specific fact by necessity (no scope information available), explicitly state the assumed scope and invite correction, rather than presenting it as universally applicable.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| scope_confirmation_rate | Share of scope-sensitive-topic queries that receive explicit scope confirmation before an answer is given | Alert if < 90% |
| non_default_scope_error_rate | Error rate for users in non-default jurisdictions/versions/units relative to default-scope users | Alert if markedly higher than default-scope error rate |
| scope_mismatch_correction_rate | Rate of expert/user corrections identifying a wrong-scope answer | Track trend; alert on sustained increase |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Wrong-scope answer in compliance-relevant response | Review confirms a jurisdiction/version mismatch in a compliance, tax, or legal response | High | Correct the response, add topic to scope-sensitive tagging list if not already tagged |
| Non-default scope error rate elevated | non_default_scope_error_rate significantly exceeds default-scope error rate | Medium | Audit retrieval defaulting behavior for the affected topic/scope combination |

## Related Patterns
- [Fact Source Confusion](./fact-source-confusion.md) - both stem from insufficient disambiguation before answering, one for entity identity and one for applicable scope
- [Knowledge Version Mismatch](./knowledge-version-mismatch.md) - the specific case of this pattern where the mismatched scope is product/policy version
- [Fact Generalization Error](./fact-generalization-error.md) - shares the mechanism of a narrowly-scoped fact being applied outside its true scope, framed at the population/condition level rather than jurisdiction/version
