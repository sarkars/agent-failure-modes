# Input Locale Mismatch

## Issue
An agent interprets a date, number, or currency value using the wrong locale convention — reading "03/04/2026" as March 4th when the source used day-month-year, or parsing "1.234,56" as one-point-two-three-four instead of one thousand two hundred thirty-four point five six. The value parses without error under the wrong locale's rules, so the agent proceeds confidently with a value that is silently different from what the source intended.

**Frequency**: Common

**Symptoms**
- Dates that are transposed month/day for the first twelve days of any month (ambiguous range) and silently correct thereafter, making the bug intermittent and hard to reproduce
- Numeric values off by a factor tied to decimal/thousands-separator confusion (e.g. 1.234,56 read as 1.234 instead of 1234.56)
- Downstream reports showing implausible clustering of dates in the 1st-12th of each month
- Currency or quantity fields that are off by roughly 1000x or a decimal-point shift
- Errors only surface when a value happens to fall outside the ambiguous range (e.g. day 25, which cannot be a month) and throws a hard parse error

## Root Cause
Date and number formatting conventions vary by locale (MM/DD/YYYY vs DD/MM/YYYY vs YYYY-MM-DD; "." vs "," as decimal separator) and, critically, most format strings within the ambiguous range are structurally valid under more than one convention — there is no syntactic signal in "03/04/2026" alone that reveals which convention produced it. An agent's parser that hardcodes or defaults to one locale (usually the one used during development/testing) will silently misinterpret any input from a system using a different convention, and because the misparse produces a syntactically valid date or number rather than an error, no validation layer catches it unless it explicitly checks for locale provenance or plausibility.

## Example
```
A logistics agent ingests shipment manifests from a European freight
partner whose system exports dates as DD/MM/YYYY. The agent's parser was
built and tested against a US-based manifest source and calls:

    datetime.strptime(date_str, "%m/%d/%Y")

A manifest lists a container's customs clearance deadline as "05/11/2026"
(intended: 5 November 2026). The agent parses it as May 11, 2026 -- six
months earlier than intended.

The agent's scheduling logic flags the shipment as already overdue by two
months relative to "today" (which the agent computes as being after May
11), triggers an automated overdue-customs escalation email to the client,
and deprioritizes what is actually an on-time shipment in favor of others
it now believes are more urgent. The error is caught only when the client
calls to ask why they received an overdue notice for a shipment that
hasn't left the port yet.
```

## Statistics
| Finding | Context |
|---------|---------|
| Roughly 12/31 (about 39%) of calendar dates are structurally ambiguous between MM/DD and DD/MM parsing and will misparse silently under the wrong convention | Derived from the fact that day values 1-12 are valid as either a month or a day |
| A meaningful share of cross-border data-integration incidents trace back to date or decimal-separator locale mismatches | Typical range observed in integration postmortems |
| Requiring ISO 8601 (YYYY-MM-DD) at system boundaries eliminates the majority of date-locale incidents in practice | Reported range across teams that standardized on ISO 8601 |

## Mitigations
1. **Mandate unambiguous formats at ingestion**: Require ISO 8601 (`YYYY-MM-DD`) for dates and a fixed decimal convention at every system boundary, converting from locale-specific formats immediately at the edge rather than deep in the pipeline.
2. **Explicit locale tagging**: Require every input source to declare its locale/format convention as metadata, and parse using that declared locale rather than a hardcoded or inferred default.
3. **Plausibility checks post-parse**: After parsing, sanity-check the result against context (e.g. a "customs deadline" shouldn't be in the past relative to the shipment's known origin date) and flag implausible results for review instead of acting on them silently.
4. **Fail loud on ambiguity, not just on invalidity**: Treat any date/number string matching more than one supported locale convention as requiring explicit disambiguation, rather than silently applying a default when the string happens to also be valid under it.
5. **Source-system format audit**: Maintain a registry of each upstream source's known format convention, verified against sample data, rather than assuming a single global convention across all integrations.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| ambiguous_date_parse_rate | Share of parsed dates whose day component is <= 12 (structurally ambiguous) | Informational; track alongside error rate |
| post_parse_plausibility_failure_rate | Share of parsed values failing a downstream plausibility check | Alert if > 2% |
| locale_mismatch_correction_count | Count of records manually corrected due to identified locale misparsing | Alert on any sustained upward trend |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Implausible parsed date | A parsed date fails a context-based plausibility check (e.g. precedes the record's own creation date) | High | Quarantine record, re-parse with alternate locale, verify against source |
| New source with undeclared locale | An ingestion source begins sending data without a locale/format declaration | Medium | Block ingestion until format is confirmed with source owner |

## Related Patterns
- [Input Timezone Ambiguity](./input-timezone-ambiguity.md) - a related temporal-interpretation failure, often co-occurring with date locale mismatches in the same payload
- [Input Encoding Mismatch](./input-encoding-mismatch.md) - both are silent misinterpretation failures where a value "successfully" parses under the wrong assumption
- [Output Precision Loss](./output-precision-loss.md) - a related numeric-fidelity failure that can compound with decimal-separator misparsing
