# State Encoding Mismatch

## Issue
State that an agent writes with one encoding — a character set, a serialization scheme (JSON vs. protobuf field ordering), a number format (float vs. decimal string), or a timezone convention — is later read by a different component that assumes a different encoding. The read succeeds without error but produces subtly wrong values: mojibake in text, truncated precision in numbers, or a timestamp shifted by hours. Because the read doesn't throw, the corruption propagates silently into downstream decisions.

**Frequency**: Occasional

**Symptoms**
- Text fields containing garbled characters (mojibake) for names, addresses, or free-text notes from certain locales
- Numeric values that are off by a rounding amount consistent with float-to-decimal or vice versa conversion
- Timestamps that are consistently off by a fixed number of hours matching a timezone offset
- The corruption only appears for a subset of records (e.g. non-ASCII names, values above a precision threshold) not all of them
- Re-reading the same stored state with a different client/library produces a different, "correct" value

## Root Cause
Agent pipelines frequently pass state through multiple components — the agent's own memory store, a cache layer, a downstream microservice, a database — each of which may have been built with a different default encoding assumption (UTF-8 vs. Latin-1, naive vs. timezone-aware datetimes, IEEE-754 float vs. arbitrary-precision decimal) and none of which negotiate or declare that assumption explicitly at the boundary. Because most encoding mismatches don't raise exceptions — a UTF-8 byte sequence is still valid Latin-1 bytes, a float is still a valid number — the mismatch degrades data rather than breaking the pipeline, so it passes every functional test that doesn't specifically compare byte-for-byte or value-for-value across the boundary.

## Example
```
A CRM-sync agent writes a customer's name to a shared state store as a
UTF-8 encoded string: "Nguyễn Thị Hà" (Vietnamese, contains combining
diacritics).

The state store's write client correctly encodes it as UTF-8 bytes.

A downstream billing-agent, reading the same record through an older
client library that defaults to Latin-1 decoding when no charset
header is present, decodes the UTF-8 bytes as Latin-1:

  Stored bytes (UTF-8):  4E 67 75 79 E1 BB 85 6E ...
  Decoded as Latin-1:    "Nguyá»…n Thá»‹ HÃ "

The billing agent uses this garbled name to auto-generate an invoice
PDF and a payment-reminder email. The customer receives an invoice
with their name rendered as unreadable symbols, and the billing team
only discovers the root cause after the customer complains and support
compares the raw stored bytes to what was displayed.
```

## Statistics
| Finding | Context |
|---------|---------|
| Encoding-mismatch defects disproportionately affect non-ASCII locales, with 3-8x higher incidence in non-English-name datasets | Typical range observed in internationalized production systems |
| An estimated 60-80% of encoding mismatches are caught only by manual complaint or visual inspection, not automated tests | Estimated from teams without byte-level round-trip testing |
| Adding explicit charset/schema declarations at service boundaries reduces mismatch incidents by roughly 90% | Reported range across teams that added boundary contracts |

## Mitigations
1. **Explicit encoding contracts at every boundary**: Require every state read/write boundary (API, queue message, file, cache entry) to declare its encoding/schema explicitly (e.g. `Content-Type: application/json; charset=utf-8`) rather than relying on client-library defaults.
2. **Canonical internal representation**: Standardize on one encoding, numeric type, and timezone convention (e.g. UTF-8, decimal strings for currency, UTC ISO-8601) for all internally-passed state, with conversion only at true external boundaries.
3. **Round-trip validation tests**: Include automated tests that write representative non-ASCII, high-precision, and cross-timezone values through the full pipeline and assert byte-for-byte or value-for-value equality on read-back.
4. **Schema/type enforcement with strict decoding**: Use decoders that raise on invalid or ambiguous byte sequences rather than silently falling back to a lossy default charset, converting silent corruption into a loud, catchable error.
5. **Checksum or canary fields**: Include a checksum of critical state (or a known-value canary field) that downstream readers can verify, catching encoding corruption even when the specific field being read looks superficially valid.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| non_ascii_decode_error_rate | Rate of decode failures or replacement-character occurrences in text fields | Alert if > 0.1% |
| cross_service_checksum_mismatch_rate | Fraction of records where a state checksum computed on write doesn't match the checksum computed on read | Alert if > 0 |
| timezone_offset_anomaly_count | Count of timestamp fields differing from an independent reference by a fixed hour offset | Alert if sustained pattern detected |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Checksum mismatch on read | A stored state checksum fails to verify against the value read by a downstream consumer | High | Page owning team, quarantine affected records, audit encoding assumptions at the boundary |
| Replacement character spike | Text fields show a spike in Unicode replacement characters (U+FFFD) or mojibake patterns | Medium | Review recent client-library or encoding-config changes on the write path |

## Related Patterns
- [State Serialization Failure](./state-serialization-failure.md) - a broader category of read/write boundary failure where encoding mismatch is one specific mechanism
- [State Version Incompatibility](./state-version-incompatibility.md) - a related boundary mismatch, but driven by schema evolution rather than encoding assumptions
- [State Replication Lag](./state-replication-lag.md) - both are silent data-quality issues that pass functional checks while returning wrong values
