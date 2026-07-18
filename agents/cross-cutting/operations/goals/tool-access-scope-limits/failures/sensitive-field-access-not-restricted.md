# Sensitive Field Access Not Restricted

## Issue
Fields that are explicitly flagged in policy as sensitive — salary, health status, disability accommodations, immigration status, background check results — are technically accessible through a tool with no additional authorization check beyond the baseline permission to use the tool at all. The sensitivity flag exists as a governance label describing how the field *should* be handled, but no runtime gate (step-up authentication, role-specific approval, purpose limitation) actually stands between an agent and the field once it has ordinary access to the record it lives on.

**Frequency**: Common

**Symptoms**
- An agent with routine HR-lookup access can retrieve salary or health-related fields with no additional check, even though only a small subset of roles are policy-authorized to see them
- Sensitive fields are returned identically whether the request comes from a narrowly-scoped assistant or a broadly-privileged one, because no differentiation exists below the "can access this tool" level
- Compliance documentation lists these fields as requiring "need to know" access, but the technical implementation grants them to anyone who can call the underlying API
- Sensitive-field access events aren't logged any differently from ordinary field access, making after-the-fact review of who saw what effectively impossible
- The sensitivity label was added to the data dictionary after the tool was already built, and the tool was never revisited to add an enforcement check

## Root Cause
Marking a field "sensitive" is a governance and documentation exercise that frequently happens independently of, and later than, the engineering work of building the tool that serves it. Unless there's a mandatory process tying every sensitivity label to a corresponding runtime check — a step-up authorization requirement, a purpose-limitation gate, a dedicated approval workflow — the label has no technical teeth. The tool's access-control logic only knows about coarse-grained permissions (can call this endpoint, can access this record), and has no mechanism to consult a separate sensitivity classification before deciding what to return.

## Example
```
An internal HR-assistant agent is built to help managers answer routine
questions like "how many people report to me" and "when does this
person's PTO expire." It's granted access to the employee-records API,
which also includes `salary`, `health_accommodation_notes`, and
`disciplinary_history` fields on the same record — all flagged
"sensitive: restricted to HR-BP role" in the company's data
classification spreadsheet, a document maintained by the People
Analytics team and never wired into the API's authorization logic.

A manager asks the assistant, "can you pull up everything on file for
this employee so I can prep for their review," intending to get
performance notes. The agent calls the employee-records tool, which
returns the entire record because the manager's role passes the tool's
only check (can access employee records for direct reports), and the
assistant includes salary and disciplinary history in its summary,
exposing fields that were supposed to require HR-BP-specific
authorization the technical system never actually checked for.
```

## Statistics
| Finding | Context |
|---------|---------|
| Sensitive-field labels maintained outside the engineering system of record (spreadsheets, wikis, governance tools) are disproportionately represented in incidents where the label had no enforcement effect | Common finding in data-governance maturity assessments |
| HR, health, and compensation data are among the most frequently cited categories in insider-access and over-permissioning incidents | Consistent with typical enterprise access-review findings |
| Adding a runtime enforcement check retroactively to a tool already in production is a common and costly remediation step following sensitive-field exposure incidents, more so than the initial classification work itself | Typical of governance-to-enforcement gap remediations |

## Mitigations
1. **Enforcement-linked classification**: Require every field marked sensitive in the data dictionary to have a corresponding, tested runtime check before the classification is considered "complete" — a label with no enforcement hook should fail a governance audit, not just an engineering one.
2. **Step-up authorization for sensitive fields**: Require an additional authorization step (role check, purpose-of-access justification, or explicit approval) specifically for sensitive fields, separate from and more stringent than the baseline check for accessing the record.
3. **Sensitive-field response stripping by default**: Exclude sensitive fields from a tool's default response schema entirely, requiring an explicit, separately-authorized request parameter to include them, rather than returning them as part of the standard object.
4. **Dedicated access logging for sensitive fields**: Log every access to a sensitive field separately and more granularly than ordinary field access, including the requester's role and stated purpose, to support after-the-fact review and anomaly detection.
5. **Periodic reconciliation between classification and enforcement**: Regularly diff the data-governance sensitivity classification list against the set of fields with an actual runtime enforcement check, and treat any field on the former but not the latter as a compliance gap requiring remediation.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `sensitive_field_unrestricted_access_count` | Count of sensitive-field accesses that didn't pass through the required step-up authorization check | Alert threshold: > 0 (any occurrence) |
| `classification_enforcement_gap_count` | Count of fields marked sensitive in the governance system with no corresponding runtime enforcement check | Alert threshold: > 0 |
| `sensitive_field_access_without_purpose_log` | Rate of sensitive-field accesses missing a logged purpose/justification | Alert threshold: > 1% of sensitive-field accesses |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unauthorized Sensitive Field Access | A sensitive field is returned to a requester who didn't pass the step-up authorization check | P1 | Halt the tool path, notify HR/legal/compliance as appropriate, review the extent of exposure |
| Classification-Enforcement Gap Detected | Reconciliation job finds a governance-classified sensitive field with no runtime check | P2 | Prioritize adding enforcement before the field remains reachable by general-purpose tools |

## Related Patterns
- [Data Classification Access Not Enforced](./data-classification-access-not-enforced.md) - the general case of this pattern applied at the record/document level rather than specifically to known-sensitive fields
- [Field-Level Access Not Restricted](./field-level-access-not-restricted.md) - the underlying architectural gap (record-level-only enforcement) that allows sensitive fields to leak through
- [PII Field Exposure](./pii-field-exposure.md) - overlaps when the unrestricted sensitive field is also personally identifiable information
