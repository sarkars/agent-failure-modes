# Output Quote Escaping Failure

## Issue
An agent generates text that must be embedded inside a structured format — a JSON string value, a CSV field, a shell argument, a string literal in generated code — and the content itself contains quote characters, apostrophes, or backslashes that need to be escaped for the target grammar. Because the model produces the escaped output as free-form text generation rather than by running a deterministic escaping function, it frequently gets the transform wrong: under-escaping (leaving a raw quote that terminates the string early), over-escaping (doubling an already-correct escape sequence), or escaping for the wrong target grammar entirely (JSON-escaping content destined for a shell command, or vice versa). The result is a downstream parse failure or a corrupted field, distinct from output injection in that no malicious input is required — the model breaks its own well-intentioned output on ordinary content like a customer's name containing an apostrophe.

**Frequency**: Very Common

**Symptoms**
- JSON parsing fails on agent-generated output with an "unexpected token" or "unterminated string" error, traceable to an unescaped double-quote or backslash inside a string value the model generated
- A downstream consumer receives a field with visibly wrong escaping — literal `\"` characters appearing in rendered text, or a string that was truncated at an internal quote character
- The same underlying content (e.g. a book title containing an apostrophe, like "Wendy's Story") escapes correctly in some outputs and incorrectly in others from the same model and prompt, because the model is generating the escape sequence probabilistically rather than applying a fixed rule
- Nested-quoting scenarios (a shell command inside a JSON field, a SQL string inside a generated script) fail more often than single-layer quoting, because the model must track and correctly apply two different escaping grammars simultaneously
- Asking the model to "make sure to escape quotes properly" in the prompt reduces but does not eliminate the failure rate, since the underlying mechanism (text generation, not a parser/serializer) hasn't changed

## Root Cause
Escaping is a deterministic, mechanical transformation defined by a target format's grammar — a JSON serializer, a shell-quoting library, and a CSV writer each apply an exact, well-specified rule with no room for interpretation. When an LLM is asked to produce already-escaped output as part of its free-form text generation (rather than the surrounding harness applying a proper serializer to the model's raw string output), the escaping becomes a probabilistic prediction of "what escaped text usually looks like" rather than an exact application of the grammar's rule. This breaks down specifically on inputs that are less common in the model's training distribution for that context (unusual quote nesting, multiple special characters in one field, multi-layer embedding), and the failure mode compounds when the model must simultaneously satisfy two different grammars' escaping rules for the same underlying character.

## Example
```
An agent is asked to generate a JSON array of customer testimonials to
populate a marketing page, with each testimonial as a JSON object
containing a "quote" field. One customer's actual submitted testimonial
reads:

  He said, "This tool saved us 10 hours a week," and he wasn't kidding.

The model, generating the full JSON document as text, needs to escape
both the double quotes around "This tool saved us 10 hours a week" and
correctly leave the apostrophe in "wasn't" unescaped. In one run it
produces:

  {"quote": "He said, "This tool saved us 10 hours a week," and he
  wasn't kidding."}

The inner double quotes are left unescaped, terminating the JSON string
value early at `"He said, "` - everything after that point becomes
invalid JSON syntax rather than part of the string value. The
downstream page-rendering job's JSON parser throws a syntax error on
this one testimonial, and because the generation pipeline builds one
JSON document containing all testimonials rather than one per
testimonial, the parse failure takes down rendering for every
testimonial in the batch, not just the one with the problematic quote.
```

## Statistics
| Finding | Context |
|---|---|
| Free-form model generation of already-escaped structured output shows a measurably higher malformed-output rate on fields containing embedded quote characters than on fields without them | Typical range observed in structured-generation pipelines handling user-submitted free text |
| Nested/multi-layer escaping scenarios (e.g. shell-inside-JSON) show substantially higher failure rates than single-layer escaping in the same pipeline | Estimated from comparisons of single- vs. multi-grammar escaping tasks |
| Routing string values through a proper serializer after generation (rather than having the model produce pre-escaped text) eliminates nearly all quote-escaping-specific parse failures in practice | Reported range across teams that moved from model-escaped to harness-escaped output construction |

## Mitigations
1. **Never have the model produce pre-escaped structured output directly**: Have the model generate raw, unescaped field values and pass them to a proper serializer (a JSON library's stringify function, a shell-quoting utility, a CSV writer) in the calling code, so escaping is applied deterministically by code rather than predicted by the model.
2. **Use structured output / function-calling modes where available**: When the model supports a constrained JSON-mode or tool-call output format, use it instead of asking the model to hand-write escaped JSON as free text, since constrained decoding modes typically guarantee well-formed output at the format level.
3. **Validate and re-serialize before use, never trust model-escaped output directly**: Parse the model's raw output defensively and re-serialize it through the harness's own serializer before it reaches any downstream consumer, catching and correcting escaping errors rather than propagating them.
4. **Isolate multi-layer embedding into separate generation and composition steps**: When output must satisfy two different grammars (e.g. a shell command embedded in JSON), generate the innermost content first, apply that layer's escaping deterministically in code, then compose the outer structure — never ask the model to reason about both grammars' escaping rules in a single generation pass.
5. **Fail the batch item, not the whole batch, on a parse error**: Structure batch-generation pipelines so a malformed individual record is isolated and skipped/retried rather than corrupting the parse of an entire batch document, limiting the blast radius of any single escaping failure.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| structured_output_parse_failure_rate | Rate of agent-generated structured output that fails to parse against its target format | Alert if rate increases, especially correlated with content containing quote characters |
| escaping_error_field_correlation | Correlation between parse failures and the presence of embedded quotes/special characters in specific fields | Track to confirm root cause when failure rate rises |
| batch_generation_full_failure_rate | Rate at which a single malformed record causes an entire batch document to fail to parse | Alert if nonzero, indicating missing per-record isolation |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Structured output parse failure spike | structured_output_parse_failure_rate exceeds baseline | High | Switch affected generation path to harness-side serialization instead of model-escaped output |
| Batch-wide failure from one malformed record | A single record's escaping error causes full-batch parse failure | Medium | Add per-record isolation/validation so one bad record doesn't block the whole batch |

## Related Patterns
- [Output Injection Vulnerability](./output-injection-vulnerability.md) - injection is the security-framed version of unescaped interpolation with adversarial intent; this pattern is the reliability-framed version where ordinary, non-malicious content breaks the model's own attempted escaping
- [Output Encoding Issues](./output-encoding-issues.md) - both are about the model's own serialization step corrupting output, one from character-encoding mismatch and one from escaping-grammar mismatch
- [Output Format Not Validated](./output-format-not-validated.md) - a missing validation gate is what allows a quote-escaping failure to reach a downstream consumer undetected rather than being caught at the source
