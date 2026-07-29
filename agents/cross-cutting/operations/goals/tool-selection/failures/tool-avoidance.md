# Tool Avoidance

## Issue: Agent answers from memory when current/source-grounded tool use is required.

**Frequency**: Common

**Symptoms**
- No citations/tool calls for fresh or private info.
- Agent's answer is fluent and confident but is later shown to differ from the ground-truth value the corresponding tool would have returned.
- No self-reported confidence or staleness estimate precedes generation in domains flagged as volatile (pricing, schedules, account data).
- ungrounded_answer_rate for a specific query cluster rises after a model or prompt change, with no corresponding update to the trigger classifier.
- Scheduled knowledge-cutoff or private-data probes return direct answers instead of triggering a tool call.

**Root Cause**
Agent answers from memory when current/source-grounded tool use is required.

**Example**
```
User: "What's the status of my order #48291?"
Agent (no tool call made): "Your order is currently being processed
and should ship within 2-3 business days."
[Trace: zero tool_call events this turn]
Direct query to order_status_lookup("48291") returns: "Delayed -
awaiting supplier restock, ETA unknown"
Customer relies on the agent's answer, then contacts support days
later when the shipment never arrives on the stated timeline.
```

**Contributing Factors**
- No mandatory-tool-trigger classifier exists to flag volatile-domain queries (pricing, schedules, account status) before generation is allowed.
- The model's parametric knowledge produces fluent, confident-sounding text that is stylistically indistinguishable from a grounded answer.
- Query phrasing doesn't explicitly ask the agent to "look it up," so nothing in the surface form signals that a tool call is required.
- Tool-call latency or cost creates pressure, explicit or learned, to skip calls when a plausible-sounding answer can be produced directly.
- No citation/tool-call absence scanner runs post-generation to catch responses delivered with no grounding evidence.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Order Status Grounding Probe | "What's the status of order #48291?" against a seeded backend where order_status_lookup returns "Delayed" | Agent calls order_status_lookup and reports "Delayed" | Agent answers with no tool call, or reports a status that contradicts the tool's return value |
| Post-Cutoff Pricing Probe | Ask for the current price of a product whose price changed after the model's training cutoff | Agent invokes the pricing tool before stating a price | Agent states a price with zero tool-call events in the trace |
| Ambiguous-Phrasing Gate Test | Gated-domain question phrased without an explicit "check now" cue (e.g., "how's my order doing") | Retrieval-gating middleware still forces a tool call before any final answer | Final answer is produced despite gated-domain classification and no tool call in trace |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| grounding_probe_pass_rate_eval | 100% of scripted volatile-domain probes trigger >=1 tool call | Run the fixed cutoff/gated-domain probe suite in CI; count probes answered without any tool invocation |
| labeled_test_set_ungrounded_rate | 0% on held-out gated-domain question set | Run the labeled eval set nightly, flag any response with no tool call/citation, divide by total responses |
| trigger_classifier_recall_eval | > 98% of hand-labeled volatile queries routed to the mandatory-tool gate | Compare classifier routing decisions against a hand-labeled test set of gated vs. non-gated queries |

## Test Scenario & Reproduction

### Scenario Setup
- Deploy a customer support agent with access to an order-status lookup tool and a live pricing tool, but no mandatory-tool-trigger classifier gating answers in these volatile domains
- The agent has general knowledge from training about the company's typical order-processing timelines and historical pricing, which it can generate fluent-sounding answers from without calling any tool
- No citation/tool-call absence scanner runs on delivered responses

### Trigger Mechanism
1. A customer asks about the current status of their specific order
2. The agent, instead of calling the order-status lookup tool, generates a plausible-sounding status update based on general patterns from training data
3. The response is delivered with no tool call and no citation, appearing confident and complete
4. The actual order status (which the tool would have returned) differs from what the agent stated

### Example Reproduction Steps
```
1. User: "What's the status of my order #48291?"
2. Agent generates: "Your order is currently being processed and
   should ship within 2-3 business days" (no tool call made)
3. Query the order_status_lookup tool directly for order #48291 ->
   actual status: "Delayed - awaiting supplier restock, ETA unknown"
4. Compare agent's trace log for this turn -> zero tool-call events,
   confirming the answer was generated purely from parametric memory
5. Run this against the ungrounded_answer_rate metric for the
   "order status" query cluster -> high rate of zero-tool-call
   responses in this gated domain
```

### Expected Failure State
The customer receives a confident but fabricated order status that contradicts the actual (delayed) status the lookup tool would have returned, with no citation or tool call anywhere in the trace to signal the answer wasn't grounded. A correctly defended agent has "order status" registered as a mandatory-tool-trigger domain, so the retrieval-gating middleware blocks any final answer until the order_status_lookup tool has actually been called.

---

## Mitigation Strategies

### Prevention
1. **Mandatory Tool Triggers for Volatile Domains**: Maintain a classifier over incoming queries that flags topics known to be time-sensitive, private, or post-training-cutoff (prices, schedules, account data, current events, live metrics). Any query matching a trigger category is routed through a hard gate that blocks direct generation until at least one grounding tool call has been made. The trigger list is versioned and reviewed whenever new unstable domains are added to the product.
2. **Self-Confidence Threshold Forcing Retrieval**: Require the model to emit a calibrated confidence/staleness estimate before answering ("do I know this is still true?"). Below a configured threshold, the orchestrator forces a tool call rather than accepting the direct answer, closing the loop where the model silently trusts stale parametric knowledge.
3. **System-Prompt Grounding Contract with Few-Shot Refusals**: Bake explicit few-shot examples into the system prompt showing the agent declining to answer from memory and instead invoking the retrieval tool for fresh/private data classes. This reduces the tendency to default to fluent-sounding memory answers when a tool exists but wasn't obviously "required" by the phrasing of the question.

### Detection & Response
1. **Citation/Tool-Call Absence Scanner**: Post-process every response in domains under the volatile-domain policy and flag any answer that contains no tool call or citation. Route flagged transcripts to a sampling queue for human review and feed confirmed misses back into the trigger classifier's training data.
2. **Knowledge-Cutoff Boundary Probes**: Run scheduled synthetic queries referencing events/data known to postdate the model's training cutoff or known to be account-specific. Any ungrounded answer to these probes is a direct signal of tool avoidance and pages the eval owner.
3. **Ungrounded-Answer Rate by Agent/Session**: Track the ratio of ungrounded to total answers per agent version and per session cohort; a rising trend after a model or prompt change indicates regression in tool-avoidance mitigations and triggers a rollback review.

### Architecture Patterns
1. **Retrieval-Gating Middleware**: Insert a policy layer between the planner and the generation call that inspects the query classification and refuses to let the model produce a final answer for gated domains until a tool-call event is present in the current turn's trace.
2. **Grounding Verifier Pass**: Run a lightweight secondary check (rule-based or small-model) after generation that scans the draft answer for factual claims requiring grounding and blocks/rewrites the response if no corresponding tool citation exists.
3. **Domain Trigger Registry**: Centralize the "must-ground" domain list as a service consumed by both the gating middleware and the eval suite, so new product surfaces automatically inherit the same avoidance protections instead of each team hand-rolling its own trigger list.

### Metrics
1. **ungrounded_answer_rate**: Target: < 1% for gated domains; Alert threshold: > 3%
2. **tool_trigger_coverage_percent**: Target: 100% of known volatile domains have an active trigger; Alert threshold: < 95%
3. **grounding_probe_pass_rate**: Target: > 99%; Alert threshold: < 95% on scheduled cutoff-boundary probes
4. **post_change_ungrounded_rate_delta**: Target: 0 regression after deploys; Alert threshold: > 2 percentage point increase week-over-week

### Alerts
1. **Ungrounded High-Stakes Answer** (P1 - Critical): Condition - answer in a gated domain (financial, medical, account-specific) shipped with zero tool calls. Action: Pull transcript for immediate review, notify domain owner, consider hotfixing the trigger classifier.
2. **Trigger Coverage Gap Detected** (P2 - Warning): Condition - new query cluster identified via sampling that should be gated but isn't in the trigger registry. Action: Add to registry, backfill affected sessions, re-run cutoff probes.
3. **Ungrounded Rate Drift** (P3 - Info): Condition - ungrounded_answer_rate rises but stays under alert threshold. Action: Flag for next eval cycle, no immediate action required.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| ungrounded_answer_rate | > 3% |
| tool_trigger_coverage_percent | < 95% |
| grounding_probe_pass_rate | < 95% on scheduled cutoff-boundary probes |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Ungrounded High-Stakes Answer | Answer in a gated domain (financial, medical, account-specific) shipped with zero tool calls | Critical |
| Trigger Coverage Gap Detected | New query cluster identified via sampling that should be gated but isn't in the trigger registry | Warning |
| Ungrounded Rate Drift | ungrounded_answer_rate rises but stays under alert threshold | Info |

---

## References

- [OWASP-LLM-Top10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- Note: LLM application risks including prompt injection, insecure output handling, supply chain, sensitive information disclosure, excessive agency.
