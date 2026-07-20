# Data Pipeline Schema Drift

## Issue
An upstream system or team changes the shape of the data it emits — renaming a field, changing a type, adding a required field, deprecating an enum value — without coordinating with every downstream consumer. Because the pipeline has no contract enforcement between producer and consumer, the change ships silently, and the agent's parsing logic either throws on the first unexpected value, silently coerces it to null/default, or misinterprets a renamed field as absent, breaking downstream behavior with no upstream-visible signal that anything happened.

**Frequency**: Very Common

**Symptoms**
- Parsing errors or exceptions appear in a downstream consumer immediately after an unrelated team's deploy, with no communication between the teams
- A field the agent depends on silently becomes null or its default value after an upstream release, without any error being thrown
- An enum or categorical field starts containing a new value the agent's logic doesn't have a branch for, and it falls through to an unhandled or default case
- Downstream dashboards or agent outputs show a step-change in a metric that lines up with an upstream deploy timestamp
- The upstream team is unaware any downstream consumer existed until the breakage is reported

## Root Cause
In most organizations, data producers and data consumers are decoupled by design — that's the point of a pipeline — but this decoupling also means producers frequently have no visibility into who consumes their output or how, so a change that looks purely internal to them (renaming a field for clarity, adding a new required attribute, tightening a type) is in fact a breaking change for every downstream parser that pattern-matches on the old shape. Without an explicit, versioned schema contract that both sides validate against — and a registry or notification mechanism that tells the producer who depends on which fields — schema evolution happens unilaterally, and the burden of detecting the break falls entirely on downstream consumers discovering it after the fact.

## Example
```
A user-profile service emits a "user.updated" event with fields including
"phone_number" (string, e.g. "+1-555-0142"). A recommendation agent's
pipeline parses this event to determine the user's region from the phone
number's country code prefix.

The user-profile team migrates to a structured phone number library and
changes the field to an object: "phone" (object: {country_code, number,
extension}), removing "phone_number" entirely, as part of an internally
scoped "clean up contact fields" release. They test against their own
service's consumers but have no registry of external pipeline consumers, so
the recommendation pipeline is not on their release checklist.

After the deploy, the recommendation pipeline's parser looks for
"phone_number", finds it absent, and its schema library treats missing
optional fields as null rather than raising an error. The region-detection
logic silently defaults every user to "unknown region" for three days before
someone notices recommendation quality has degraded and traces it back to
the phone field change, well after the user-profile team has moved on to
other work and forgotten the release.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 45-60% of downstream pipeline breakages are attributable to an uncoordinated upstream schema change rather than a bug in the consuming code itself | Typical range observed in cross-team incident classification |
| Silent schema drift (no error thrown, wrong/default value produced) is detected an estimated 3-7 days later on average than drift that causes an outright parsing error | Estimated from time-to-detection comparisons across drift incident types |
| Teams using an enforced, versioned schema registry with consumer-breaking-change checks report 70-85% fewer schema-drift incidents | Reported range across teams adopting schema registries |

## Mitigations
1. **Versioned schema registry with compatibility checks**: Require all producer schema changes to go through a registry that enforces backward-compatibility rules (no field removal/rename/type-narrowing without a major version bump) before a change can ship.
2. **Consumer registration and change notification**: Maintain a registry of which pipelines/teams consume which event schemas, and require producers to notify or get sign-off from registered consumers before a breaking change ships.
3. **Strict schema validation at ingestion**: Validate incoming events against the expected schema at the pipeline's entry point and fail loudly (reject/quarantine the event) rather than silently coercing missing or mistyped fields to null/default.
4. **Contract tests across team boundaries**: Maintain automated contract tests that run in the producer's CI pipeline, asserting the schema still satisfies every known downstream consumer's declared expectations.
5. **Deprecation windows with dual-write**: When a field must change, require the producer to emit both old and new forms for a defined deprecation window, giving consumers time to migrate before the old field is removed.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| schema_validation_failure_rate | Rate of ingested events failing schema validation against the expected contract | Alert if > 0.5% |
| unexpected_null_default_rate | Rate at which a normally-populated field is null/default, correlated against recent upstream deploys | Alert if a step-change coincides with an upstream release |
| unhandled_enum_value_count | Count of categorical field values encountered that don't match any known branch in downstream logic | Alert if > 0 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Breaking schema change detected pre-deploy | A producer's proposed schema change fails a registered consumer's contract test | High | Block producer deploy until consumer coordination or compatible change |
| Post-deploy field anomaly | Downstream null/default rate or validation failure rate spikes within a window after an upstream deploy | High | Roll back or hotfix upstream change, notify consumer teams |

## Related Patterns
- [Data Pipeline Lossy Transformation](./data-pipeline-lossy-transformation.md) - schema drift is the unplanned, upstream-driven counterpart to a transform intentionally narrowing its output schema
- [Integration API Contract Violation](./integration-api-contract-violation.md) - schema drift is the pipeline-internal version of an integrated service breaking its documented contract
- [Dependency Breaking Change](./dependency-breaking-change.md) - both describe an upstream change shipping without downstream coordination, one in code dependencies and one in data schemas
