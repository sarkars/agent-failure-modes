# Output Hallucination in Structured Format

## Issue
When an agent is required to produce output matching a fixed schema, it will sometimes fabricate a plausible-looking value for a field it has no actual basis for — inventing a tracking number, a confidence score, a source citation, or an ID — rather than leaving the field empty, marking it as unknown, or declining to complete the schema. The output is structurally valid and passes any format/type check, which makes the fabrication far more dangerous than a free-text hallucination: it looks exactly like a correctly-populated field to any downstream system or reviewer that trusts schema conformance as a proxy for correctness.

**Frequency**: Common

**Symptoms**
- Fields containing values that are well-formed (correct format, plausible range) but don't correspond to any real underlying fact or lookup
- Fabricated IDs, reference numbers, or citations that don't resolve to any real record when checked
- Confidence/score fields populated with a plausible-looking number even when the agent had no mechanism for computing an actual confidence value
- Downstream systems accepting and acting on fabricated fields because schema validation (which only checks type/format) passes
- Discrepancies discovered only when someone attempts to actually use the fabricated value (look up the ID, follow the citation) and it doesn't exist

## Root Cause
A structured-output schema with a required field creates strong pressure for the model to produce *something* in that slot, because leaving it null or writing "unknown" often scores worse against the schema's apparent completeness expectation than confidently filling it with a plausible value — especially when the schema doesn't explicitly provide a "not available"/null option as a first-class, expected outcome. The model's underlying tendency to produce fluent, plausible-sounding completions (the same mechanism behind free-text hallucination) applies just as much to a structured field as to a sentence; the schema constrains the *shape* of the fabrication (a nine-digit tracking number instead of a nonsense string) without constraining its *truthfulness*. Because the fabricated value satisfies every mechanical check a type/format validator can run, there's no structural signal distinguishing it from a genuinely sourced value.

## Example
```
A research-summarization agent extracts structured findings from a set
of source documents into a schema requiring, for each finding, a
"source_citation" field (expected format: document name + page number).

For a finding that is actually a reasonable inference drawn by combining
information from two documents, rather than a fact stated verbatim on
one page, the agent doesn't have a single clean citation to point to.
Rather than using a "derived_from_multiple_sources" flag (which the
schema doesn't offer) or leaving the field null, it fills the field with:

    "source_citation": "Annual_Report_2025.pdf, page 34"

Page 34 of that document exists and discusses a related but different
topic; the specific figure cited does not appear anywhere in it. The
citation is well-formed and passes schema validation. A junior analyst
building a board presentation from the summarized findings cites page 34
directly in the deck; a board member who happens to check the source
finds no such figure, and the credibility of the entire analysis --
including the parts that were accurately sourced -- is called into
question.
```

## Statistics
| Finding | Context |
|---------|---------|
| Fabrication rates for optional-seeming-but-schema-required fields (citations, IDs, confidence scores) tend to run higher than free-text hallucination rates for the same underlying claim | Typical range observed across structured-extraction evaluation studies |
| Providing an explicit "unknown"/null option in the schema measurably reduces fabrication rates for fields the model lacks grounding for | Reported range across teams that added explicit null/uncertain states to extraction schemas |
| Fabricated structured fields are disproportionately likely to go undetected relative to free-text hallucinations, since format validity is often mistaken for correctness | Estimated from the lower scrutiny structured fields typically receive relative to prose |

## Mitigations
1. **Make "unknown"/null a first-class schema option**: Explicitly include a null, "not available", or "insufficient evidence" value as a valid, expected outcome for any field the model might lack grounding for, removing the pressure to fabricate a plausible-looking substitute.
2. **Require grounding evidence alongside the value**: For fields like citations or IDs, require the agent to also output the verbatim source text it's drawing from, and separately verify that text actually appears in the cited source before accepting the field.
3. **Post-hoc verification for high-stakes fields**: For fields that feed into decisions with real consequences (citations, reference numbers, dollar amounts), run an automated verification pass — does this ID exist in the system of record, does this citation's text match the source — before the output is used downstream.
4. **Explicit confidence calibration, not free-form confidence**: Where a confidence score is required, derive it from an actual measurable signal (retrieval score, model log-probability, agreement across multiple extraction passes) rather than asking the model to self-report a number, which is itself prone to fabrication.
5. **Audit sampling weighted toward structured fields**: Include structured fields, not just free-text output, in human review sampling, since format validity creates a false sense of security that leads reviewers to scrutinize prose more than schema-conformant fields.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| unverifiable_citation_rate | Share of citation/reference fields that fail an automated existence/text-match check against the source | Alert if > 2% |
| null_field_usage_rate | Share of eligible fields using the explicit null/unknown option versus always being populated | Alert if near 0% (suggests fabrication pressure, not genuine full coverage) |
| post_hoc_verification_failure_rate | Rate of structured fields failing downstream verification against a system of record | Alert if > 1% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Citation fails source match | An extracted citation's referenced text doesn't appear in the cited source document/page | High | Flag finding for human review, do not forward to downstream report without correction |
| Structured field never uses null option | A required-but-often-ungrounded field is populated 100% of the time across a large sample, despite an available null option | Medium | Audit sample of populated values for fabrication, consider prompt or schema adjustment |

## Related Patterns
- [Output Format Not Validated](./output-format-not-validated.md) - format validation alone will not catch this failure, since fabricated values are typically well-formed
- [Output Inconsistency](./output-inconsistency.md) - fabricated values are often a source of inconsistency, since a hallucinated field may vary between repeated calls on identical input
- [Input Default Value Assumption](./input-default-value-assumption.md) - a related failure where a plausible-but-unfounded value is substituted for a genuinely missing one, on the input side rather than the output side
