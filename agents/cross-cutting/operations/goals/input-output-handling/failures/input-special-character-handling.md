# Input Special Character Handling

## Issue
An agent's input parsing or downstream rendering logic breaks when the input contains characters with structural meaning in some layer of the pipeline — quotes, backslashes, delimiters (commas, pipes, tabs), markup characters (`<`, `>`, `&`), or control characters — and that layer wasn't written to treat them as literal data. A customer name containing an apostrophe, a product description containing a comma inside a CSV field, or free text containing an unescaped `<` breaks parsing, corrupts a field boundary, or renders incorrectly, independent of any encoding issue.

**Frequency**: Very Common

**Symptoms**
- CSV/TSV exports with misaligned columns whenever a field's own content contains the delimiter character
- Names like "O'Brien" or "D'Angelo" breaking string-interpolated queries or shell commands
- Free text containing `<`, `>`, or `&` rendering as broken HTML or being interpreted as markup instead of literal text
- Fields silently truncated or split at the first occurrence of a character that happens to match a parser's delimiter or terminator
- Intermittent failures that correlate with specific customer/product names rather than with input volume or system load

## Root Cause
Parsers and formatters for structured or semi-structured text (CSV, shell arguments, SQL string literals, HTML/XML, key-value formats) rely on specific characters to signal structure — a comma separates CSV fields, a quote closes a string literal, `<` opens a tag. When the literal data being placed into that format happens to contain one of those structural characters, the parser or renderer cannot distinguish "this is data that happens to look like a delimiter" from "this is an actual delimiter" unless the data was properly escaped or quoted when it was written. Many code paths write these formats via naive string concatenation or `str()`-style interpolation rather than a format-aware serializer that knows how to escape special characters for that specific format, so the failure surfaces only when a specific piece of data happens to contain the trigger character — which most test data doesn't.

## Example
```
An agent generates a CSV export of customer orders for a downstream
billing system, building each row by joining fields with commas:

    row = ",".join([customer_name, product, str(amount)])

A customer's name is "Smith, Jr., Robert" (as entered during signup,
including the comma). The generated row becomes:

    Smith, Jr., Robert,Premium Widget,49.99

The billing system's CSV parser, which splits naively on commas, reads
this as five fields instead of three: "Smith", " Jr.", " Robert",
"Premium Widget", "49.99". The extra fields shift every subsequent
column, and the billing system interprets "Premium Widget" as the
amount field, fails to parse it as a number, and either rejects the row
or -- worse, in a less strict downstream parser -- silently records a
malformed charge. The issue only surfaces for customers whose names or
addresses happen to contain a comma, making it appear intermittent and
customer-specific rather than a systemic serialization bug.
```

## Statistics
| Finding | Context |
|---------|---------|
| A nontrivial share of real-world names and addresses contain characters (apostrophes, commas, hyphens) that are structurally significant in common data formats | Estimated from typical name/address field character-frequency studies |
| CSV field-delimiter collisions are among the most common causes of "misaligned columns" support tickets in data-export pipelines | Typical range observed in data-pipeline incident logs |
| Using a format-aware serialization library instead of manual string joining eliminates the large majority of these incidents | Estimated from the reliability difference between naive concatenation and standard library serializers |

## Mitigations
1. **Always use format-aware serializers**: Generate CSV, JSON, HTML, SQL, and shell arguments through their respective standard-library or well-tested serialization functions (which handle quoting/escaping automatically) rather than manual string concatenation or interpolation.
2. **Escape at the point of formatting, not at the point of storage**: Store data in its raw, unescaped form, and apply format-specific escaping only when serializing into a specific target format — escaping too early risks double-escaping or escaping for the wrong target format.
3. **Test with adversarial-but-realistic data**: Include names/text containing commas, quotes, apostrophes, and markup characters in test fixtures, since these characters are common enough in real data that "clean" test data systematically hides this class of bug.
4. **Round-trip validation for exports**: For generated exports (CSV, XML, etc.), parse the generated output back and verify field counts/values match the source records, catching delimiter-collision bugs before they reach a downstream consumer.
5. **Prefer structured formats with unambiguous escaping over ad hoc ones**: Where the receiving system can accept it, prefer JSON or a similarly well-specified format over CSV or pipe-delimited text, since CSV's escaping rules are less consistently implemented across parsers.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| export_field_count_mismatch_rate | Share of generated export rows whose field count, on round-trip parse, doesn't match the expected schema | Alert if > 0.1% |
| special_character_input_rate | Share of ingested text fields containing delimiter/markup-significant characters | Informational; track for correlation with downstream errors |
| downstream_parse_rejection_rate | Rate of downstream systems rejecting or misparsing agent-generated exports | Alert if > 1% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Export round-trip mismatch | A generated export's re-parsed field count doesn't match the source record schema | High | Halt export delivery, identify offending field/character, patch serialization |
| Downstream parse rejection spike | A downstream consumer's rejection rate for agent-generated exports rises sharply | Medium | Correlate against recent input containing special characters, review serialization path |

## Related Patterns
- [Output Quote Escaping Failure](./output-quote-escaping-failure.md) - the same underlying issue, specifically scoped to quote characters breaking output parsing
- [Output Injection Vulnerability](./output-injection-vulnerability.md) - unescaped special characters are the mechanism that enables injection into SQL, shell, or HTML
- [Input Null Bytes Injection](./input-null-bytes-injection.md) - a more severe, security-relevant instance of a structurally-significant character breaking input handling
