# Output Encoding Issues

## Issue
An agent generates output text and serializes it in one encoding while the downstream consumer (an API client, a file writer, a terminal, an email client) expects or declares a different one, corrupting non-ASCII characters — accented letters, currency symbols, emoji, non-Latin scripts — before the text reaches its destination. Unlike an input encoding mismatch, the corruption is introduced by the agent's own serialization step rather than inherited from a source, and it typically affects every non-ASCII character the agent itself generates or passes through, not just specific fields.

**Frequency**: Common

**Symptoms**
- Generated documents/emails/API responses showing mojibake (garbled character sequences) specifically for non-ASCII content
- A downstream system's declared encoding (an HTTP `Content-Type` header, a file's expected charset) not matching the actual bytes the agent wrote
- Content that renders correctly in the agent's own logs/testing environment but garbles when opened in the actual target application
- Currency symbols (€, £, ¥), accented names, or emoji specifically affected while plain ASCII content is unaffected
- Issue appears only in production, where the downstream consumer's locale/charset settings differ from the agent's development environment

## Root Cause
Serialization boundaries — writing a file, sending an HTTP response, generating an email — require an explicit encoding decision, and when that decision is left to a library default or platform default rather than being set explicitly and matched to what the consumer expects, the two ends of the pipeline can silently disagree. A common variant is generating text internally as one encoding (say, the runtime's native Unicode representation) and writing it out with a library defaulting to a legacy platform encoding (e.g. Windows' default codepage) unless UTF-8 is explicitly requested; another is declaring one encoding in metadata (an HTTP header or XML declaration) while actually writing bytes in a different one. Because the agent's own encoding of the bytes always "succeeds" from its point of view, there's no error at generation time — the mismatch only becomes visible when a consumer trusts the declared or assumed encoding and decodes incorrectly.

## Example
```
An agent generates order-confirmation emails and writes them via a
mail-sending library on a Windows-hosted worker. The library's default
text encoding on that platform is Windows-1252 unless UTF-8 is
explicitly specified, but the email's Content-Type header is generated
by a separate templating step that always declares "charset=utf-8"
regardless of what encoding the mail library actually used.

An order confirmation for a customer named "François Müller" ordering
a product listed at "€49.99" is generated. The mail library encodes the
body as Windows-1252 (since UTF-8 wasn't explicitly configured), but the
header still claims UTF-8.

The customer's email client trusts the declared UTF-8 charset and decodes
the Windows-1252 bytes as UTF-8, rendering the name as "FranÃ§ois MÃ¼ller"
and the price as "â‚¬49.99". The order details are otherwise correct, but
the visibly broken text triggers a wave of "is this email legitimate?"
support tickets, since the garbling resembles phishing-email artifacts
customers have been trained to distrust.
```

## Statistics
| Finding | Context |
|---------|---------|
| A meaningful share of generated-document/email mojibake incidents trace to a mismatch between declared and actual output encoding, not to input corruption | Typical range observed in outbound-communication incident logs |
| Platform-default (non-UTF-8) text encodings remain a common source of silent output corruption in cross-platform pipelines | Well-established pattern in internationalization engineering |
| Explicitly setting UTF-8 at every serialization boundary and verifying declared-vs-actual encoding eliminates the large majority of these incidents | Estimated from the directness of the fix relative to the failure mechanism |

## Mitigations
1. **Explicitly set UTF-8 at every serialization boundary**: Never rely on a library's or platform's default text encoding; explicitly specify UTF-8 (or the consumer's required encoding) at every point text is written to a file, HTTP response, or message body.
2. **Match declared metadata to actual bytes**: Ensure any encoding declared in headers, XML prologues, or metadata is generated from the same configuration that actually encodes the bytes, not set independently by a separate templating step.
3. **Encoding round-trip tests with non-ASCII fixtures**: Include names, currency symbols, and non-Latin script content in output-generation test fixtures, and assert the round-tripped (written-then-read-back) content matches exactly.
4. **Platform-aware default audits**: When deploying the same code across different OS/runtime environments, explicitly audit and pin text-encoding defaults, since platform defaults (especially on Windows) frequently differ from Unix/Linux defaults.
5. **Consumer-encoding contract verification**: For integrations with external consumers, confirm their expected encoding explicitly rather than assuming UTF-8 is universally safe, and log/alert on any consumer-reported decode failures.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| non_ascii_output_mojibake_rate | Share of generated outputs containing known mojibake character sequences | Alert if > 0.1% |
| declared_vs_actual_encoding_mismatch_count | Count of outputs where declared charset metadata doesn't match the actual byte encoding used | Alert on any occurrence |
| downstream_decode_failure_reports | Count of consumer-reported rendering/decode failures for agent-generated output | Alert on sustained upward trend |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Mojibake detected in outbound content | Generated output contains known mojibake patterns before delivery | High | Block delivery, trace serialization step, verify encoding configuration |
| Encoding metadata mismatch | Declared charset in output metadata doesn't match the encoding actually used to write the bytes | High | Halt affected pipeline, audit templating/serialization separation |

## Related Patterns
- [Input Encoding Mismatch](./input-encoding-mismatch.md) - the mirror-image failure occurring at ingestion rather than at output generation
- [Output Quote Escaping Failure](./output-quote-escaping-failure.md) - a related output-serialization failure, focused on structural characters rather than character-set encoding
- [Output Truncation Silent](./output-truncation-silent.md) - multi-byte encoding mismatches can compound with truncation when byte-length limits are applied without encoding awareness
