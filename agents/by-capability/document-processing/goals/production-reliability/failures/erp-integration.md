# ERP Integration Errors

## Issue: ERP Field Mapping Errors

**Frequency**: Common

**Symptoms**
- Extracted data in wrong ERP fields
- GL codes misassigned
- Dimension values incorrect

**Root Cause**
Mapping between extracted fields and ERP schema requires configuration. Changes to either side break the mapping without obvious errors.

**Example**
```
Extraction output: {"department": "Sales", "cost_center": "CC-100"}
ERP mapping (outdated): department -> DEPT_CODE, cost_center -> GL_ACCT

Result: "Sales" written to DEPT_CODE, "CC-100" written to GL_ACCT (wrong field)
```

## Mitigation Strategies

### Prevention
1. **Explicit, versioned field-mapping configuration with validation tests**: Maintain the extraction-output-to-ERP-schema mapping as an explicit, version-controlled artifact with its own test suite (given a known extraction output, assert the expected ERP write), rather than an implicit or ad-hoc mapping embedded in integration code, so mapping changes are reviewable and testable independent of either side's schema changes. Trade-off: adds process overhead for what might otherwise be treated as a quick config change.
2. **Dry-run validation before committing to ERP**: Run every extraction-to-ERP write through a dry-run/simulation mode that reports what would be written without committing, and require the dry-run output to pass validation (correct field types, no unexpected empty/overwritten fields) before allowing the real write. Trade-off: adds a validation step and requires the ERP integration to support a genuine simulate-without-commit mode, which not all ERP APIs provide.
3. **Coordinated schema-change notification between extraction and ERP teams**: Establish a process where changes to either the extraction output schema or the ERP input schema trigger a notification and joint review before deployment, since this failure mode specifically arises from the two sides changing independently without the other side knowing. Trade-off: requires organizational coordination across teams that may not otherwise need to interact frequently.

### Detection & Response
1. **Reverse validation query after write**: After every ERP write, query the ERP system back and verify the values that landed match what was intended to be written (not just that the write API call succeeded), since a field-mapping bug can cause a "successful" write of the wrong value into the wrong field. Trade-off: adds a read-after-write step and additional ERP API calls, increasing integration latency and load.
2. **Field-type mismatch detection**: Flag any write where the value's type/format doesn't match what the target ERP field expects (e.g., a cost-center code landing in a GL account field, detectable because the formats differ) even if the ERP API accepted the write without error.
3. **Systematic-shift monitoring on ERP-side aggregates**: Monitor ERP-side aggregate metrics (department spend totals, GL account activity) for shifts correlated with a mapping deployment, since a swapped mapping often produces a detectable pattern (e.g., a department's spend consistently appearing under the wrong dimension) before anyone notices the individual field-level error.

### Architecture Patterns
1. **Schema-versioned mapping layer as a first-class artifact**: Architect the extraction-to-ERP integration around an explicit mapping layer that references specific versions of both the extraction schema and the ERP schema, failing loudly (rather than silently misapplying an outdated mapping) when either side's schema version doesn't match what the mapping was built for.
2. **Dry-run-then-commit two-phase write pattern**: Require every ERP write to go through a simulate phase producing a diff/preview, with the actual commit as a separate, explicit second phase — this creates a natural point to insert validation and, for high-value writes, human confirmation.
3. **Reverse-validation as a standing pipeline stage**: Build reverse validation (query-back-and-compare) into the pipeline as a standard stage for every write, not an occasional manual audit, so mapping errors are caught within the same processing run rather than discovered later through business impact.

### Metrics
1. **mapping_test_suite_pass_rate**: Target: 100% required before mapping deployment; Alert/block on any failure
2. **reverse_validation_mismatch_rate**: Target: < 0.5% of writes show a mismatch between intended and landed value; Alert if > 3%
3. **field_type_mismatch_rate**: Target: < 1% of ERP writes; Alert if > 5%
4. **schema_change_coordination_lead_time**: Target: > 5 business days notice before either side's schema change is deployed; Alert if a schema change ships with < 1 day notice to the other team

### Alerts
1. **Reverse Validation Mismatch Spike** (P1): Condition - reverse-validation mismatch rate exceeds 3% following a mapping or schema deployment. Action: Roll back the mapping change immediately, audit affected ERP records for corrected re-write, investigate the specific field(s) involved.
2. **Field Type Mismatch Spike** (P2): Condition - field-type mismatch rate on ERP writes exceeds 5%. Action: Freeze the affected mapping, review recent extraction or ERP schema changes for the mismatch source.
3. **Uncoordinated Schema Change** (P2): Condition - either extraction schema or ERP schema changes deploy without the required cross-team notice window. Action: Treat the deployment as high-risk; run full reverse-validation sweep on writes immediately following the change.

## References

- [Production-Ready AI Agent for Document Extraction](https://www.stackai.com/insights/how-to-build-a-production-ready-ai-agent-for-document-data-extraction) - ERP integration patterns
- [IDP Accuracy Reckoning 2026](https://idp-software.com/news/idp-accuracy-reckoning-2026/) - GL miscoding rates
- [AlterSquare: Document AI Fails](https://altersquare.io/enterprise-document-ai-fails-extraction-layer-not-model-layer/) - Field mapping challenges
