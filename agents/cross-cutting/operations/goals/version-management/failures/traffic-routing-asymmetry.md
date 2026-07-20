# Traffic Routing Asymmetry

## Issue
A traffic-routing configuration meant to apply uniformly during a version rollout — a canary weight, a header-based version pin, a geographic or tier-based split — instead applies inconsistently across different request paths, entry points, or protocols. A user hitting the agent through the REST API gets routed according to the intended canary percentage, while the same logical traffic arriving through a WebSocket streaming endpoint, an internal service-to-service call, or a retry path bypasses the routing rule entirely and always lands on one version regardless of the configured split. The result is that "5% canary" is only true for some fraction of actual traffic, while another slice is either entirely exposed to the new version or entirely shielded from it, undermining both the safety intent and the statistical validity of the rollout.

**Frequency**: Occasional

**Symptoms**
- Observed version distribution differs meaningfully between different entry points (REST vs. streaming, external vs. internal) for what should be the same canary configuration
- A subset of traffic (e.g., retries, a specific client SDK version, a particular geographic edge node) consistently shows 0% or 100% exposure to the new version regardless of the configured weight
- Canary analysis metrics look clean because they're only measuring the correctly-routed slice, while an unmeasured slice is silently getting different treatment
- An incident traced to the new version affects users disproportionately from one entry point, revealing that entry point wasn't actually subject to the canary percentage
- Routing configuration is defined and enforced in multiple separate places (e.g., one rule in the API gateway, a different one in the internal service mesh) that have drifted out of sync

## Root Cause
Modern agent platforms typically have more than one path by which traffic reaches a given service — a public API gateway, an internal service mesh for service-to-service calls, a WebSocket or gRPC streaming layer that may use a different load-balancing mechanism than plain HTTP, and retry/fallback paths that may be hardcoded to a specific target for reliability reasons. When routing/canary rules are configured at only one of these layers (commonly the API gateway, since that's the most visible entry point), traffic that enters or is re-routed through a different layer never encounters the rule at all and falls back to whatever default target that layer uses — often the stable/old version, or sometimes a pinned target set up for a different, unrelated reason (like sticky session affinity from before the canary started). Nobody notices the asymmetry unless they specifically instrument version-distribution by entry point, because each individual layer looks like it's behaving correctly according to its own local configuration.

## Example
```
"ChatOrchestrator" runs a 20% canary for v12, configured as a
weighted routing rule in the public API gateway (Envoy-based),
splitting REST /chat requests 80/20 between v11 and v12.

The service also has a WebSocket streaming endpoint for real-time
token-by-token responses, used by the primary web client for about
60% of total traffic. The WebSocket layer uses a separate
connection-pool-based load balancer (older infrastructure, added
before the canary tooling existed) that was never wired into the
same weighted-routing configuration - it round-robins across
whatever instances are in the "stable" target group only, which
still points at v11 exclusively.

Canary dashboard, built from REST /chat telemetry only, shows a
clean 80/20 split with v12 metrics looking healthy at low volume.
Team promotes v12 to 100% based on this data.

Post-promotion, the WebSocket layer's separate config is manually
updated to point at v12 as a follow-up task, days later, and this
is when the actual first exposure of v12 to the 60% of traffic that
uses streaming happens - well after the canary was declared
successful, with none of the analysis that supposedly validated the
release having covered that traffic at all.
```

## Statistics
| Finding | Context |
|---------|---------|
| Multi-entry-point services frequently have canary/routing rules configured at only one layer, leaving other entry points outside the intended traffic split | Typical finding across teams auditing routing configuration coverage |
| A significant share of "successful" canary promotions in multi-protocol services are based on telemetry from a subset of total traffic rather than the full mix | Estimated from teams that later discovered entry-point routing gaps |
| Centralizing routing decisions at a single layer (e.g., service mesh sidecar applied uniformly regardless of entry protocol) removes most instances of this asymmetry in teams that have consolidated | Reported range across teams that unified routing configuration |

## Mitigations
1. **Single source of truth for routing rules**: Configure canary/version-routing weights in one place that all entry points (REST, streaming, internal mesh, retries) actually consult, rather than duplicating or partially applying rules across independently-configured layers.
2. **Version-distribution telemetry broken down by entry point**: Track observed version split separately for each protocol/entry point, and require them to match the intended configuration within tolerance before treating a canary as validly measured.
3. **Routing configuration audit at rollout start**: Before starting any canary or weighted rollout, explicitly enumerate every path traffic can take to reach the service and confirm each one is covered by the routing rule, rather than assuming the primary/visible path represents all traffic.
4. **Fail loud on unmanaged traffic paths**: Instrument entry points that bypass the central routing configuration to emit an explicit warning or metric flagging "traffic through this path is not subject to active canary/version routing," so gaps are visible rather than silent.
5. **Retry-path routing consistency**: Ensure retry and fallback logic explicitly re-applies the same routing decision (or explicitly and intentionally always targets the stable version) rather than defaulting to whatever the retry mechanism's original hardcoded target happens to be.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| version_distribution_variance_by_entrypoint | Difference between the intended canary weight and observed version split, broken down per entry point | Alert if any entry point deviates > 10 percentage points from configured weight |
| unmanaged_traffic_path_share | Percentage of total traffic flowing through a path not covered by the active routing configuration | Alert if > 1% during an active canary |
| canary_coverage_ratio | Share of total production traffic actually included in canary analysis telemetry | Alert if < 95% of total request volume |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Routing asymmetry detected | version_distribution_variance_by_entrypoint exceeds threshold for any entry point during an active rollout | High | Halt promotion decision, audit routing configuration across all entry points, recompute canary validity |
| Uncovered traffic path found | unmanaged_traffic_path_share is nonzero during an active canary | Medium | Extend routing rule coverage to the missed path before continuing the rollout |

## Related Patterns
- [Weighted Routing Algorithm Error](./weighted-routing-algorithm-error.md) - a related but distinct failure where the routing math itself is wrong, rather than the rule being inconsistently applied across paths
- [Canary Deployment Incomplete](./canary-deployment-incomplete.md) - routing asymmetry can produce a canary that looks complete and successful while actually only having validated a subset of real traffic
- [Sticky Session Loss](./sticky-session-loss.md) - stale sticky-session pins are one specific mechanism by which a subset of traffic ends up permanently exempt from an updated routing rule
