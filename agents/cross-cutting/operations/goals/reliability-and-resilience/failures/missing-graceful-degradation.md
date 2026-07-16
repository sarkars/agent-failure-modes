# Missing Graceful Degradation

## Issue: Agent Fails Completely When Dependency Unavailable Instead of Degrading Gracefully

**Frequency**: Common

**Symptoms**
- Agent returns errors to users when external service is down
- Service is fully unavailable instead of reduced-capability mode
- Users unable to use agent at all even for reduced-feature access
- No fallback path when primary capability fails
- Binary fail: works 100% or doesn't work at all

**Root Cause**
Agents are designed assuming all dependencies (APIs, tools, databases) are always available. When a dependency fails, the entire agent fails instead of operating in reduced mode. No fallback paths, no partial responses, no degraded-mode messaging to users.

**Example**
```
Agent capabilities:
1. Document retrieval (from external search API)
2. Data extraction (local NLP model)
3. Summarization (local model)

Dependency failure:
- External search API goes down
- Agent returns error: "Service unavailable"

Users:
- Cannot get document retrieval
- Cannot get extraction (depends on retrieved docs)
- Cannot get summarization

Better behavior:
- Search API down? Use local search (slower, lower quality) or skip retrieval
- Allow extraction on user-provided documents
- Allow summarization on provided text
- Return partial response: "Search unavailable, proceeding with provided documents"

Actual implementation:
- No fallback to local search
- No document upload option
- No partial response mode
- Users: "Agent is broken"
```

**Key Statistics**
- 50-70% of agents lack meaningful graceful degradation
- Availability impact: 2-5 hours per outage (when dependency fails)
- Cost of unavailability: $5K-500K per hour (depends on users)
- User frustration: "Why can't I at least use the parts that work?"

**Contributing Factors**
- No fallback paths designed
- Dependencies treated as always-available
- No partial response capability
- No feature-flag or reduced-capability mode
- Error handling is binary: works or fails

---

## Mitigation Strategies

### Prevention

1. **Dependency Isolation with Fallback Paths**: Design each capability with a primary and fallback implementation. If primary fails, use fallback automatically. Example: Primary search (external API) → Fallback (local keyword search) → Fallback (ask user for documents).

2. **Feature-Gated Degradation Levels**: Implement degradation tiers. When dependency X fails, agent operates at degradation level Y (reduced features, slower speed, manual intervention). Communicate level to users.

3. **Synthetic Failure Testing**: Regularly test what happens when each dependency fails. Don't assume they're always up; actively test degradation paths.

### Detection & Response

1. **Dependency Health Monitoring**: Monitor availability of all dependencies in real-time. When dependency fails, automatically switch to degradation mode.

2. **Graceful Degradation Testing**: In weekly testing, inject failures into each dependency and verify agent still works in degraded mode.

3. **User Communication on Degradation**: When operating in degraded mode, inform users: "Search service unavailable; using local search (results may be limited)."

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `graceful_degradation_test_pass_rate` | % of dependencies handled gracefully when down | <95% |
| `service_availability_with_degradation` | Uptime including degraded modes | <99.5% |
| `dependency_failure_recovery_time` | Time to switch to degradation mode | >30 seconds |
| `degraded_mode_feature_coverage` | % of features available in degraded mode | <50% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Dependency Failure, No Degradation | Dependency down but no fallback active | P1 | Activate degradation mode; investigate fallback |
| Graceful Degradation Failed | Fallback also failed | P1 | Incident response; may need manual intervention |
| Slow Recovery to Degradation | >30 seconds to switch modes | P2 | Optimize fallback detection and activation |
| Feature Loss in Degradation | Core feature unavailable in degraded mode | P1 | Implement missing fallback path |

### Dashboard Panels
- Panel 1: Dependency health (availability of each external service)
- Panel 2: Agent availability (100% mode vs. degraded mode)
- Panel 3: Degradation mode activation events
- Panel 4: Features available by degradation level
- Panel 5: User impact when operating degraded (latency, feature loss)

---

## References

- [Site Reliability Engineering: How Google Runs Production Systems](https://sre.google/sre-book/) — Resilience and graceful degradation patterns
- [Bulkhead Pattern: Resilience Pattern](https://docs.microsoft.com/en-us/azure/architecture/patterns/bulkhead) — Isolation and degradation
- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html) — Handling dependency failures gracefully
