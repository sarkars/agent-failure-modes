# Prompt Caching Underutilization

## Issue: A Stable Prompt Prefix (System Prompt, Tool Schemas, Few-Shot Examples) Is Retransmitted and Rebilled at Full Price on Every Call Instead of Using Available Prompt-Caching

**Frequency**: Very Common

**Symptoms**
- The same large system prompt, tool-schema block, or few-shot example set is sent verbatim on every single call within a session or across sessions
- Provider-level prompt-caching (cache-control breakpoints, automatic prefix caching) is either not configured at all or configured incorrectly so cache hits rarely occur
- Cost-per-call for the stable-prefix portion never drops despite that content being byte-identical call after call
- Dynamic content (a timestamp, a per-request ID, or a freshly-fetched tool result) is placed before the stable prefix in the prompt, which silently breaks prefix-matching and prevents the cache from ever hitting

**Root Cause**
Most LLM providers offer prompt caching that charges a steep discount (commonly 80-90% off) for input tokens that exactly match a previously-cached prefix, but caching only works when the stable, reusable portion of the prompt is a genuine prefix — unchanged byte-for-byte and positioned before any per-request variable content. Many implementations either never enable caching at all, or place dynamic content (today's date, a session ID, a live tool result) ahead of or interleaved with the stable system prompt and tool definitions, which invalidates prefix matching on every call and silently defeats the cache even when the caching feature is technically turned on.

**Example**
```
Agent's per-call prompt structure:
  [Current timestamp] + [System prompt: 3,200 tokens] +
  [Tool schemas: 2,100 tokens] + [User message]

Because the timestamp changes every call and sits before the system
prompt and tool schemas, the cache's prefix-match check fails on every
single request, even though the 5,300 tokens of system prompt + tool
schemas are byte-identical call after call.

Result: All 5,300 tokens of stable content are billed at full input
price on every call.

Cost impact at 10,000 calls/day:
  Without effective caching: 5,300 x 10,000 = 53,000,000 tokens/day
                              at full input price
  With correctly-ordered caching (stable prefix first, ~90% cache
  discount on hits after the first call): ~5,300 (first call) +
  9,999 x 5,300 x 0.10 = ~5.3M tokens-equivalent/day

Waste: roughly 47,700,000 token-equivalents/day billed at full price
that a simple prompt-ordering fix would have captured at a 90% discount.
```

**Contributing Factors**
- Prompt-caching feature exists on the provider but was never explicitly configured (no cache-control breakpoints set)
- Dynamic content (timestamps, session IDs, live tool results) is placed before the stable system prompt/tool-schema block rather than after it
- No monitoring exists for cache-hit rate specifically on the stable-prefix portion of prompts
- Caching is treated as "set once and forget," with no re-validation after a prompt-template change that might have shifted where dynamic content sits relative to the stable prefix

---

## Test Scenario & Reproduction

### Scenario Setup
- Agent sends a per-call prompt containing a large, byte-identical stable prefix (system prompt + tool schemas) on every call
- Dynamic content (timestamp, session ID) is positioned before the stable prefix in the assembled prompt
- Provider prompt-caching is either unconfigured or configured but structurally defeated by prefix ordering

### Trigger Mechanism
1. Issue a sequence of calls with an identical system prompt and tool-schema block, varying only the dynamic content's position and the user message
2. Measure cache-hit rate and effective input-token billing for the stable-prefix portion across the call sequence
3. Reorder the prompt so dynamic content comes after the stable prefix, and re-measure

**Example Reproduction Steps:**
```
1. Assemble 100 calls with an identical 5,300-token system-prompt-plus-
   tool-schema block, each prefixed by a changing timestamp
2. Send all 100 calls with the provider's prompt-caching feature enabled
   as configured (dynamic content first)
3. Log cache-hit status and effective billed input tokens for each call
4. Reorder the prompt so the stable 5,300-token block comes first and
   the timestamp/dynamic content comes after
5. Repeat the 100-call sequence with the reordered prompt
6. Compare cache-hit rate and total billed input tokens between the two
   orderings
```

### Expected Failure State
- With dynamic content first, cache-hit rate on the stable prefix is at or near 0% across all 100 calls, and all 5,300 tokens of stable content are billed at full price every time
- With the stable prefix moved first, cache-hit rate rises sharply from call 2 onward, and effective billed tokens for the stable portion drop to the cached-rate discount
- The only difference between the two conditions is prompt ordering — the underlying content is identical — confirming the waste is structural, not unavoidable
- No monitoring existed prior to the test that would have surfaced the near-0% cache-hit rate under the original ordering

---

## Mitigation Strategies

### Prevention
1. **Stable-prefix-first prompt assembly**: Always construct prompts so the byte-identical, reusable portion (system prompt, tool schemas, few-shot examples) comes first, with any per-request dynamic content (timestamps, session IDs, live tool results, the user's actual message) appended after it, directly fixing the ordering failure in the example. Trade-off: requires discipline in prompt-template design and review whenever a prompt template is modified, since a single dynamic field accidentally inserted early silently breaks caching again.
2. **Explicit cache-control breakpoints on known-stable segments**: Where the provider supports explicit cache markers (rather than automatic prefix detection), mark the system prompt and tool-schema block explicitly as cacheable, rather than relying on the prompt happening to be structured correctly by convention. Trade-off: explicit breakpoints must be updated if the stable content itself changes (e.g., a tool schema update), or a stale cache could serve outdated tool definitions.
3. **Cache-boundary placement validated per release**: Since a prompt-template change can silently move dynamic content ahead of the stable prefix, include a cache-hit-rate check in the release/deployment pipeline for any prompt-template change, so a regression is caught before it reaches production traffic at scale. Trade-off: adds a validation step to prompt-template deployments, though it's cheap relative to the cost of an undetected caching regression.

### Detection & Response
1. **Cache-hit-rate monitoring on the stable-prefix portion specifically**: Track hit rate for the cacheable segment of prompts as a first-class metric, separate from overall request volume; a rate near 0% despite byte-identical stable content across calls is the direct signature of this failure.
2. **Cost-per-call-for-stable-content tracking**: Since the stable prefix should cost dramatically less per call once caching is effective, monitor whether the billed cost for that segment actually drops after the first call in a session — a flat cost across all calls indicates caching isn't engaging.
3. **Prompt-structure diffing on template changes**: When a system prompt or tool-schema template is modified, diff the new assembled prompt structure against the prior version to confirm the stable segment still sits at the front, catching an accidental reordering before it reaches production.

### Architecture Patterns
1. **Prompt-assembly library enforcing stable-first ordering**: Centralize prompt construction through a shared library/function that always places registered "stable" segments before "dynamic" segments by construction, rather than leaving ordering to ad hoc string concatenation at each call site, making the ordering failure structurally impossible rather than dependent on developer discipline. Deployment consideration: requires migrating existing call sites to the shared assembly pattern, which is a one-time refactor cost.
2. **Cache-hit-rate dashboard per prompt template**: A dedicated dashboard breaking down cache-hit rate by prompt template/agent type, making underperforming templates (like the dynamic-content-first example) immediately visible rather than buried in aggregate cost metrics. Deployment consideration: requires the provider or gateway to expose per-call cache-hit metadata, which must be captured and attributed to the originating template.
3. **Automatic dynamic-content extraction at template-authoring time**: Tooling that scans a prompt template at authoring time and flags any field that varies per-request (timestamps, IDs) appearing before a stable block, prompting the author to move it, catching the failure at design time rather than in production monitoring. Deployment consideration: requires static analysis of prompt templates, which may not catch dynamic content introduced only at runtime rather than in the template itself.

### Metrics
1. **stable_prefix_cache_hit_rate**: Target > 85% of calls within a session/day hit the cache on the stable-prefix segment; Alert if < 20%.
2. **cost_per_call_stable_segment_trend**: Target dropping to the cached-rate discount (e.g., ~10-20% of full price) after the first call in a sequence; Alert if flat at full price across all calls.
3. **prompt_template_cache_regression_count**: Target 0 template deployments that reduce cache-hit rate versus the prior version; Alert if any deployment drops hit rate by more than 20 percentage points.
4. **dynamic_content_before_stable_prefix_incidents**: Target 0 prompt templates with dynamic fields positioned before the stable block; Alert if > 0 detected by static analysis.

### Alerts
1. **Cache-Hit-Rate-Collapse** (P2): Condition - stable_prefix_cache_hit_rate drops below 20% for a prompt template that previously performed well. Action: check the most recent template change for dynamic content inserted before the stable prefix.
2. **Prompt-Template-Cache-Regression** (P2): Condition - a new template deployment reduces cache-hit rate by more than 20 percentage points versus its predecessor. Action: roll back or fix the ordering before the change reaches full production traffic.

## References

- [Don't Break the Cache: An Evaluation of Prompt Caching for Long-Horizon Agentic Tasks](https://arxiv.org/pdf/2601.06007) - cache boundary control and the risk that naive full-context caching (including dynamic tool results) can paradoxically increase cost/latency rather than reduce it
- [How to Manage AI Token Costs in the Enterprise: The 2026 Playbook](https://www.correlation-one.com/blog/how-to-manage-ai-token-costs-in-the-enterprise-the-2026-playbook) - prompt caching reduces API costs by 41-80% when correctly scoped to stable system prompts and guardrails, excluding dynamic tool results
- [How to Cut LLM Token Costs in 2026: Routing, Caching, Compression, and the Right Model](https://wavect.io/blog/reduce-llm-token-costs-2026/) - prompt caching as one of the highest-leverage, lowest-effort cost levers when implemented correctly
