# Cascading External Failures

## Issue
An agent's tool chain includes multiple tools that, unknown to the agent's error-handling logic, share a common downstream external dependency. When that shared dependency has an outage, every tool built on top of it fails simultaneously, and the agent — which was designed to handle each tool's failure independently, perhaps with per-tool fallbacks — finds that its fallback options are also unavailable because they depend on the same failed upstream service, leaving it with no working path forward.

**Frequency**: Occasional

**Symptoms**
- Multiple, seemingly unrelated tools fail within the same short time window
- Fallback or backup tools that were expected to provide redundancy fail for the same underlying reason as the primary tool
- Error messages from different tools trace back to the same root-cause outage (e.g., a shared cloud region, a shared identity provider, a shared upstream data API) once investigated
- Agent's retry logic retries each failing tool independently, multiplying load on an already-degraded shared dependency

## Root Cause
Agents are typically built with per-tool error handling — if tool A fails, try tool B — under the implicit assumption that A and B fail independently. In practice, many tools that appear independent at the interface level share infrastructure underneath: two different "weather API" tools might both resell data from the same underlying provider, two different "identity verification" tools might both call the same KYC vendor, or an agent's primary and fallback search tools might both route through the same CDN or DNS provider. The agent has no visibility into this shared dependency graph — it only sees tool-level interfaces — so it cannot anticipate that a single upstream outage will take down what it believed were independent, redundant options.

## Example
```
A travel-booking agent uses "FlightAPI-Primary" for flight search and,
on failure, falls back to "FlightAPI-Backup" -- two seemingly distinct
vendors the platform team contracted with specifically for redundancy.

Both vendors, unknown to the platform team, resell data from the same
underlying GDS (Global Distribution System) aggregator. The aggregator
suffers a 40-minute outage due to a database migration gone wrong.

The agent's flight search fails via FlightAPI-Primary, triggers its
fallback logic, calls FlightAPI-Backup, which also fails (same root
cause), and then falls back further to a cached-results tool, which
returns week-old pricing data. The agent presents these stale prices
to 340 customers as live quotes over the 40-minute window, and when
the underlying outage resolves, the platform has to process refunds
and price-adjustment complaints from customers who booked at prices
that were no longer honored.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 15-25% of "redundant" tool pairs in production agent systems share at least one upstream infrastructure dependency when traced fully | Typical range observed in dependency-mapping audits of agent tool stacks |
| Outages affecting a shared upstream dependency take noticeably longer to diagnose than single-tool outages, because symptoms initially appear as unrelated multi-tool failures | Reported range across incident response teams |
| Agents with circuit breakers scoped only per-tool (not per-shared-dependency) show elevated retry volume during cascading outages compared to dependency-aware circuit breakers | Estimated from telemetry comparing circuit breaker designs during upstream outages |

## Mitigations
1. **Dependency graph mapping**: Maintain an explicit map of which tools share which upstream infrastructure or vendors, and use it to determine true redundancy rather than assuming interface-level distinctness implies independence.
2. **Dependency-aware circuit breakers**: Scope circuit breakers at the level of the shared upstream dependency where known, so one confirmed outage trips the breaker for all tools built on it at once, rather than each tool discovering the outage independently through repeated failed calls.
3. **Genuine multi-vendor redundancy verification**: Periodically audit "backup" tools to confirm they don't silently resell or proxy the same underlying data/service as the primary, and prefer vendors with verifiably independent infrastructure for true redundancy.
4. **Explicit staleness flagging on cache fallback**: When falling back to cached data during an outage, always tag the output as stale with a timestamp, rather than presenting it with the same confidence as a live result.
5. **Outage correlation alerting**: Monitor for simultaneous failures across multiple tools and automatically flag them as a potential shared-dependency incident rather than treating each as an isolated tool failure requiring separate investigation.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| correlated_tool_failure_count | Count of distinct tools failing within the same short time window | Alert if >= 2 tools fail within 5 minutes |
| fallback_chain_exhaustion_rate | Rate at which an agent exhausts its entire fallback chain (all options failed) for a given task type | Alert if > 1% |
| stale_data_served_count | Count of responses served from a stale-data fallback path during a suspected outage | Alert if > 0 without an explicit staleness flag |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Correlated multi-tool outage | Two or more tools believed to be independently redundant fail within the same short window | High | Investigate for shared upstream dependency, trip dependency-scoped circuit breaker, notify affected teams |
| Full fallback chain exhausted | An agent exhausts every configured fallback option for a task without a successful result | High | Halt task execution rather than serving degraded output silently, escalate to on-call |

## Related Patterns
- [Transitive Tool Dependency Failure](./transitive-tool-dependency-failure.md) - the underlying structural cause: tools depending on other tools/services in ways the agent doesn't model, of which cascading failure across "redundant" tools is one visible consequence
- [Required Field Added To API](./required-field-added-to-api.md) - both involve an agent's tool-integration assumptions silently breaking due to changes in infrastructure it doesn't directly control
