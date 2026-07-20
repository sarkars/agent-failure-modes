# Input Encoding Mismatch

## Issue
An agent reads input bytes assuming one character encoding (typically UTF-8) while the actual source encoded the text differently (Latin-1/ISO-8859-1, Windows-1252, UTF-16, or a legacy code page), producing mojibake — visually garbled or silently wrong characters — in names, addresses, and free text. Because most bytes in Latin-1 and Windows-1252 are also valid (but differently-meaning) UTF-8 continuation sequences for a wide range of inputs, the decode frequently "succeeds" without throwing an error, so the corruption passes silently into storage and downstream processing.

**Frequency**: Common

**Symptoms**
- Names/addresses containing sequences like "café" rendering as "café" or "Müller" as "MÃ¼ller"
- Smart quotes, em-dashes, or accented characters from Word/Windows-authored documents turning into control-character-looking garbage
- Search and exact-match lookups failing on records that look correct visually but differ at the byte level
- Downstream systems (email, PDF generation, CSV exports) either erroring on unexpected byte sequences or silently substituting replacement characters (`�`)
- Issue is invisible in the agent's own logs if the logging pipeline itself re-encodes leniently

## Root Cause
Character encoding is metadata that travels separately from the bytes themselves, and many ingestion paths (file uploads, legacy database exports, third-party API responses, copy-pasted content, CSVs from spreadsheet tools) either omit that metadata or declare it incorrectly. An agent's input pipeline that hardcodes a `decode('utf-8')` (or relies on a library's default) instead of detecting or validating the declared encoding will happily decode Latin-1 or Windows-1252 bytes as UTF-8 whenever the byte sequence happens to form valid UTF-8 code points — which for many two-byte Latin-1 sequences it does, just with the wrong resulting character. Because UTF-8 decoding of non-UTF-8 bytes doesn't reliably raise `UnicodeDecodeError`, there is no natural failure signal forcing the mismatch to surface.

## Example
```
A customer-support agent ingests a CSV export from a legacy on-prem CRM
that was saved as Windows-1252 (the CRM's default on a German Windows
deployment). The ingestion pipeline calls:

    df = pd.read_csv(upload, encoding="utf-8")

For most ASCII rows this works fine. But a customer record with the name
"Jürgen Müller" is stored in Windows-1252 as bytes that UTF-8 misdecodes
as garbage rather than raising an error (some byte sequences do error;
others silently decode to unrelated multi-byte characters).

The agent ingests the row without error, stores "JÃ¼rgen MÃ¼ller" in the
database, and later uses that name to generate a personalized renewal
email: "Dear JÃ¼rgen MÃ¼ller, your subscription is expiring." The email
is sent to 40 customers with German/French/Scandinavian names in the same
batch before a support ticket flags the garbled greeting.
```

## Statistics
| Finding | Context |
|---------|---------|
| Non-UTF-8 legacy sources (older CRMs, mainframe exports, Windows-authored CSVs) account for a meaningful share of encoding-mismatch tickets in support/data pipelines | Typical range observed in data-ingestion incident logs |
| A majority of encoding mismatches involving Latin-1/Windows-1252 bytes decode as UTF-8 without raising an exception | Estimated from characteristics of the encodings' byte-sequence overlap |
| Adding encoding auto-detection at ingestion reduces mojibake-related tickets substantially | Reported range across teams that added a detection library to their pipeline |

## Mitigations
1. **Encoding detection at ingestion**: Run a detection pass (e.g. byte-order-mark checks plus statistical detection) on any input whose encoding isn't explicitly and reliably declared, rather than assuming UTF-8 by default.
2. **Strict decode with fallback chain**: Attempt UTF-8 decoding in strict mode first; on failure, fall back to a declared or detected legacy encoding, and flag/log every fallback occurrence rather than silently succeeding.
3. **Round-trip validation**: After decoding, re-encode and compare against the original bytes (or check for known mojibake character patterns) to catch "successful" but incorrect UTF-8 decodes of non-UTF-8 input.
4. **Explicit encoding contracts on ingestion endpoints**: Require upstream systems and file-upload interfaces to declare their encoding explicitly (HTTP `charset`, CSV metadata) and reject uploads with no declared encoding rather than guessing.
5. **Normalization at the boundary**: Normalize all accepted input to a single internal encoding (UTF-8, NFC-normalized) immediately at ingestion so encoding assumptions don't need to be re-litigated at every downstream consumer.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| replacement_character_rate | Share of ingested text fields containing `�` or other decode-failure markers | Alert if > 0.1% |
| non_ascii_byte_anomaly_rate | Share of records where detected encoding disagrees with the encoding actually used to decode | Alert if > 1% |
| encoding_fallback_count | Count of ingestions that required fallback from the default (UTF-8) encoding | Alert on any sustained upward trend |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Mojibake pattern detected | Known mojibake byte patterns (e.g. "Ã¼", "â€™") found in newly ingested text | High | Quarantine batch, identify source encoding, re-ingest with correct decode |
| Decode failure spike | UnicodeDecodeError rate exceeds baseline for a given source system | Medium | Notify source-system owner, verify declared encoding hasn't changed |

## Related Patterns
- [Input Special Character Handling](./input-special-character-handling.md) - encoding mismatches often manifest specifically around accented and special characters
- [Output Encoding Issues](./output-encoding-issues.md) - the same class of problem occurring on the output side rather than at ingestion
- [Input Null Bytes Injection](./input-null-bytes-injection.md) - another byte-level input handling failure that surfaces during decoding/parsing
