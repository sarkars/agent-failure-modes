# Hallucinated Carrier Transit-Time When Rate API Returns Partial Quote Set

## Issue: A Routing Agent Requesting Shipping Quotes From Multiple Carriers Via a Rate API That Returns a Response Where Some Carriers' Quotes Include Pricing but No Confirmed Transit-Time Field -- Because That Carrier's Sub-System Timed Out Mid-Response -- Fills In a Plausible Transit-Time Estimate for the Missing Field Rather Than Treating It as Incomplete, and Commits to a Customer ETA Based on the Fabricated Value

**Frequency**: Occasional

**Symptoms**
- The customer-facing ETA commitment is based on a specific carrier transit time that does not match what that carrier's own tracking system or service-level documentation states for the selected service tier
- The rate API's logged response for the selected carrier shows a null or missing transit-time field, while the routing agent's output presents a specific number of days with full confidence
- Re-querying the same carrier and service tier through the rate API, when its transit-time sub-system is functioning, returns a different transit time than what was committed to the customer
- The gap concentrates on carriers or service tiers whose transit-time data depends on a separate, less reliable sub-system than the one providing pricing, so partial responses recur for the same carrier-tier combinations
- The discrepancy surfaces only when the shipment misses the committed ETA and a customer escalation traces the commitment back to its origin

**Root Cause**
When a carrier's rate-API response returns pricing but an empty or missing transit-time field, the routing agent's task -- selecting a carrier and committing to a customer ETA -- still requires a transit-time value to complete, and the agent has no instruction distinguishing "transit-time sub-system unavailable" from "transit-time data confirms a short transit." Lacking that distinction, the model fills the gap with a plausible estimate based on typical transit times for similar routes and service tiers, rather than treating the missing field as a blocking signal requiring exclusion of that carrier or quote or a fallback to a secondary transit-time source.

**Example**
```
Routing agent requests quotes for a cross-country shipment from three carriers via the rate API
Carrier B's response includes a price quote but the transit-time field returns null due to a timeout in that carrier's separate transit-estimation sub-system
Routing agent, evaluating Carrier B as the lowest-cost option, fills in "3 business days" as a plausible transit time consistent with similar routes from other carriers
Customer-facing system commits to a 3-business-day delivery ETA based on this fabricated value
Carrier B's actual transit time for this route and service tier is 5 business days; shipment arrives two days after the committed ETA, triggering a customer service escalation
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM-based agents are documented to complete plausible-sounding values when an expected tool response field is missing or incomplete, rather than treating the gap as a blocking error | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Frameworks for detecting and correcting tool-use errors in agentic systems identify failure to recognize partial or field-level-incomplete tool responses as a distinct, recurring tool-use error category | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Multi-agent consensus-seeking research in supply-chain contexts identifies reliable handling of partial or degraded carrier-system responses as a distinct requirement for autonomous logistics decision-making | [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184) |

**Contributing Factors**
- The rate API's response schema allows pricing and transit-time fields to be populated independently, with no flag distinguishing a fully complete quote from a partially complete one
- The routing agent's carrier-selection and ETA-commitment logic treats a quote with a missing transit-time field as usable, rather than requiring transit-time confirmation as a precondition for including that quote
- No automated check compares the transit time committed to a customer against a confirmed, non-null value from the rate API before the commitment is finalized

---

## Mitigation Strategies

1. **Hard Stop on Unconfirmed Transit Times**: Prohibit the routing agent from selecting a carrier quote or committing a customer ETA based on a transit-time value unless that exact value was returned as a confirmed, non-null field in the rate API response
2. **Explicit Partial-Quote Flag in Rate API Schema**: Require the rate API to return an explicit flag distinguishing a fully complete quote from one with missing fields, and exclude partial quotes from carrier selection by default
3. **Secondary Transit-Time Source on Primary Field Gap**: When a carrier's primary transit-time field is missing, require a fallback query to a secondary transit-time source (historical shipment data for that carrier-route-tier combination) before using that carrier's quote, rather than estimating from general route similarity
4. **Post-Commitment Transit-Time Provenance Audit**: Automatically verify, for every committed customer ETA, that the underlying transit time matches a confirmed, non-null rate API field, flagging any commitment where it does not

### Metrics
- Rate of customer ETA commitments based on a transit-time value with no matching confirmed, non-null rate API field
- Rate of rate API responses returning partial quotes (pricing present, transit time missing) by carrier and service tier
- Rate of missed-ETA incidents attributable to a fabricated transit-time value

### Alerts
- A customer ETA commitment is finalized with no corresponding confirmed transit-time field in the rate API response → P1
- A carrier-tier combination's partial-quote rate exceeds the defined threshold for a rolling window → P2
- A missed-ETA incident is traced to a transit-time value not confirmed by the rate API → P1

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [Agentic LLMs in the Supply Chain: Towards Autonomous Multi-Agent Consensus-Seeking](https://arxiv.org/pdf/2411.10184)
