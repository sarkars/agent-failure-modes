# Agent Infers Product Line from Recently-Mentioned Topic Instead of Entitlement Record

## Issue: Ticket-Routing Agent Determines Which Product Line a Ticket Belongs to Based on Whatever Product Name Was Most Recently Mentioned in the Conversation, Rather Than Querying the Customer's Actual Purchase/Entitlement Record

**Frequency**: Common

**Symptoms**
- A customer who mentions a competitor's product, a product they evaluated but did not buy, or a product they used at a previous employer gets routed to that product line's queue instead of the one they actually hold an entitlement for
- Routing accuracy is measurably lower for tickets where the customer's message references more than one product name, compared to tickets referencing only the product they actually own
- The entitlement/purchase-record lookup tool is available to the routing agent but is not called before the routing decision when the conversational text already contains a plausible product name
- Customers migrating between the vendor's own product tiers (e.g., asking "how is this different from your Enterprise plan") are frequently misrouted to the tier they asked about rather than the tier their account is actually on
- Manually re-routing tickets that were misrouted this way, and comparing the conversational product mention against the entitlement record, shows the two disagree in essentially all of the misrouted cases

**Root Cause**
The agent is prompted or trained to extract a product-line label from the ticket text as a convenient, low-latency signal, and a recently-mentioned product name is a strong, easily-extractable feature relative to the extra step of calling an entitlement-lookup tool. Because the model completes "which product is this about" by pattern-matching on salient text rather than treating product identity as a fact that must be retrieved from the account record, any product name mentioned for a comparison, migration, or competitor reference is treated identically to a mention of the customer's actually-owned product — the model has no structural signal distinguishing "this is what I own" from "this is what I'm asking about."

**Example**
```
Customer message: "We're currently on your Standard plan but I'm
  wondering if switching to Enterprise would fix our API rate-limit
  issue -- can someone look into this?"
Entitlement record (not queried before routing): Standard plan, API
  rate limits apply per Standard-tier terms
Agent routing decision: Routes to Enterprise product-line queue,
  because "Enterprise" is the most recently and prominently mentioned
  product term in the message
Actual need: Standard-tier support agent should handle the rate-limit
  question and can also loop in sales for the potential upgrade --
  instead the ticket sits in an Enterprise queue whose agents don't
  have context on Standard-tier rate-limit behavior and reroute it
  back, adding a full routing cycle of delay
```

**Additional Example (structured field already in context, no retrieval gap involved)**
```
Resident messages a home-services chatbot: "need someone for a
  jhaadu-pochha today, quick"
Matched provider record, already included in the prompt context from
  the directory search the chatbot just ran: { categoryName:
  "home-cleaning", subcategoryName: "sweeping-mopping" }
Chatbot's reply: "Got it, connecting you with a jhaadu-pochha
  specialist near you" -- the model lifts the resident's own
  colloquial phrase back into the reply instead of naming the service
  using the matched provider's subcategory field, even though that
  field was already sitting in the same context window
Downstream analytics and the provider's own listing expect the
  standardized subcategory label; the colloquial phrase now appears
  in a customer-facing confirmation and in logged analytics as if it
  were the taxonomy term, which the provider never used and does not
  recognize on cross-reference
```
This variant shows the mechanism is not limited to skipping a retrieval call: even when the authoritative field is already present in the prompt, the model still defaults to echoing the user's own salient wording unless explicitly instructed to prefer the structured field over it.

**Key Statistics**
| Finding | Context |
|---|---|
| Work on resolving conflicts between an LLM's in-context textual signal and externally retrieved ground truth finds that models frequently default to the more salient in-context signal unless explicitly required to prioritize retrieved data, even when the retrieved data is authoritative | Seeing through the Conflict: Transparent Knowledge Conflict Handling in Retrieval-Augmented Generation (arXiv:2601.06842) |
| Domain-grounded retrieval research finds that routing or classification decisions made from parametric/in-context text pattern-matching alone are measurably less accurate than decisions gated on a retrieval step against an authoritative source, particularly when the in-context text contains a plausible-but-incorrect candidate value | Mitigating LLM Hallucinations through Domain-Grounded Tiered Retrieval (arXiv:2603.17872) |
| In production ticket-routing audits, misrouting driven by a mentioned-but-not-owned product name typically requires a full additional routing cycle to correct, adding to time-to-first-response for the affected tickets | Illustrative range from support-operations audit practice |

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|---|---|---|---|
| Single product mentioned, matches entitlement | Customer mentions only the product they own | Routes correctly to that product line | Misroute (unlikely but included as baseline) |
| Comparison mention | Customer asks about switching from their current plan to a different one | Routes based on entitlement record's current plan, not the plan asked about | Routes to the plan mentioned in the comparison |
| Competitor product mentioned | Customer references a competitor's product by name while describing their issue | Routes based on entitlement record, ignoring the competitor mention | Routes based on the competitor product name matching internal taxonomy noise |
| No entitlement record available | New or trial account with no finalized entitlement record yet | Agent falls back to an explicit "unconfirmed product" queue or asks a clarifying question, not a guess from text | Agent guesses a specific product line from conversational text alone |

### Evaluation Dataset
- **Source**: Historical tickets where the routing decision was later corrected by a human, paired with the original conversational text and the actual entitlement record at ticket time
- **Size**: 200+ misrouted tickets plus a matched sample of correctly-routed tickets
- **Key variations**: comparison/upgrade mentions; competitor mentions; multi-product accounts; no-entitlement-yet accounts

### Metrics
| Metric | Target | How to Measure |
|---|---|---|
| Entitlement-grounded routing rate | 100% of routing decisions preceded by an entitlement-record lookup | % of routed tickets with a logged entitlement-lookup tool call before the routing decision |
| Multi-product-mention routing accuracy | Within a few points of single-product-mention routing accuracy | Routing accuracy on tickets with 2+ product mentions vs. tickets with 1 product mention |
| Cross-queue reroute rate | < 3% | % of tickets rerouted to a different product-line queue after initial routing |

### Automated Checks
```python
def check_ungrounded_product_routing(trace: list[dict], routed_product: str,
                                       entitlement_product: str | None) -> dict:
    """Flag a routing decision made without an entitlement lookup, or one that
    disagrees with the entitlement record when a lookup was available."""
    entitlement_calls = [c for c in trace if c["tool"] == "get_entitlement_record"]
    return {
        "has_entitlement_lookup": len(entitlement_calls) > 0,
        "ungrounded_routing_risk": len(entitlement_calls) == 0,
        "entitlement_mismatch": (
            entitlement_product is not None and routed_product != entitlement_product
        ),
    }
```

---

## Mitigation Strategies

### Prevention
1. **Mandatory Entitlement-Lookup Gate**: Require a successful entitlement-record lookup before the product-line routing decision is reachable, so routing can never be based purely on conversational text extraction
2. **Owned-vs-Mentioned Disambiguation Prompt**: When multiple product names appear in the ticket text, explicitly require the agent to identify which one matches the entitlement record before using any product name as the routing label
3. **Fallback Queue for Missing Entitlement**: When no entitlement record is available (new/trial accounts), route to an explicit unconfirmed-product queue rather than guessing from text

### Detection & Response
1. **Entitlement-Mismatch Scan**: Automatically flag routed tickets where the routing label does not match the entitlement record's product field, for rapid re-routing
2. **Comparison-Language Audit**: Sample tickets containing comparison or upgrade language ("switching to," "how does this compare to," "instead of") and check whether they were routed to the mentioned product or the owned product

### Architecture Patterns
- **Retrieve-Then-Route Pipeline**: Structurally separate entitlement lookup from routing-label generation, so the routing step only has the retrieved entitlement field available, not free-text product-name extraction
- **Structured Entitlement-Field Routing**: Route using the entitlement record's product field directly as the primary signal, reserving conversational text analysis for sub-categorization within the correct product line rather than for product-line selection itself

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| `routing.ungrounded_product.count` | Routing decisions made with no preceding entitlement lookup | > 0 per day |
| `routing.entitlement_mismatch.rate` | % of routed tickets where routing label disagrees with entitlement record | > 2% |
| `routing.cross_queue_reroute.rate` | % of tickets rerouted to a different product-line queue after initial routing | > 3% |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Ungrounded Product Routing | Ticket routed with no entitlement lookup in trace | P2 | Re-route based on entitlement record; audit routing pipeline for the affected window |
| Entitlement Mismatch Spike | Entitlement-mismatch rate exceeds threshold for a rolling day | P1 | Investigate routing logic regression; consider temporary human review gate |

---

## References
- [Seeing through the Conflict: Transparent Knowledge Conflict Handling in Retrieval-Augmented Generation](https://arxiv.org/pdf/2601.06842)
- [Mitigating LLM Hallucinations through Domain-Grounded Tiered Retrieval](https://arxiv.org/html/2603.17872v1)
