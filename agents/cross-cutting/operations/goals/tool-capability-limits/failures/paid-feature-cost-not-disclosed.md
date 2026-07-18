# Paid Feature Cost Not Disclosed

## Issue
An agent calls a tool capability that appears functionally identical to other calls in the same API, but is actually billed as a paid add-on with per-call or tiered pricing that isn't surfaced anywhere in the API response, error messages, or the agent's own logic. The agent has no cost-awareness built in, so it calls the feature as often as its workflow logic dictates, and the financial impact is only discovered when the bill arrives — often after the feature has been in heavy use for a full billing cycle.

**Frequency**: Occasional

**Symptoms**
- A tool's monthly invoice includes a large, unexpected line item for a specific API capability that was assumed to be included in the base plan
- No warning, confirmation prompt, or cost estimate was shown at call time for the paid feature
- The paid feature is functionally similar to a free/included feature, making it easy for the agent (or the developer who wrote its call) to reach for it without realizing the pricing difference
- Cost per call for the feature is only documented on a separate pricing page, not in the API reference the developer used to integrate it
- Usage of the paid feature scales with agent call volume, so cost grows silently in proportion to agent activity, not in proportion to any deliberate business decision

## Root Cause
Vendors often price granular capabilities (e.g., a "premium" OCR mode, an "enhanced" enrichment lookup, a real-time versus batch processing tier) differently within the same API surface, but API references typically document request/response shape and authentication, not real-time cost per call. Developers integrating a tool usually reference the API docs, not the separate pricing page, when writing the code that decides which capability to invoke — and once written, an agent has no mechanism to reconsider a "does this cost extra" question before each call, since neither its own logic nor the API response surfaces that signal. This is compounded when agents make autonomous decisions about which tool variant to call (e.g., choosing "high-accuracy mode" for a customer classified as high-value), since a cost-blind autonomous decision can silently outrun a budget far faster than a human clicking through a UI would.

## Example
```
1. An agent uses an identity-verification tool's API to check submitted IDs during
   customer onboarding. The API has two modes: "standard" (included in the base plan)
   and "enhanced" (invokes a third-party biometric cross-check, billed at $1.50/call).
2. A developer, following the API reference (which documents both modes identically
   with no pricing annotation), configures the agent to always request "enhanced" mode
   believing it simply produces better accuracy at no extra cost.
3. The agent processes roughly 8,000 onboarding verifications over the following month
   as part of normal operations, all in "enhanced" mode.
4. The monthly invoice arrives with a $12,000 line item for "enhanced verification calls,"
   dwarfing the base plan's $500/month cost.
5. Finance escalates to engineering, which discovers the pricing difference only by
   reading the vendor's separate pricing page, not the API docs used during integration.
6. Switching to "standard" mode for the 95% of verifications that don't need enhanced
   accuracy immediately cuts the recurring cost by roughly 90%.
```

## Statistics
| Finding | Context |
|---------|---------|
| Unexpected paid-feature usage is a recurring driver of SaaS/API budget overruns in agentic systems, with cost-surprise incidents commonly cited as a top-3 source of vendor bill disputes | Consistent with pricing and API documentation frequently living in separate, unlinked sources |
| Agents given autonomous choice between a free and paid variant of a capability default to the higher-cost option in a substantial share of unreviewed integrations, often estimated around 20-40% | Because "enhanced"/"premium" naming reads as strictly better with no cost signal to weigh against it |
| Adding a pre-call cost-tier check or hard per-feature budget cap has been observed to prevent the large majority of paid-feature cost overruns before they reach a full billing cycle | By surfacing the cost signal at decision time instead of at invoice time |

## Mitigations
1. **Cross-reference pricing pages during integration, not just API docs**: Before wiring up any tool capability, explicitly check the vendor's pricing page for per-call or tiered costs, and document the finding alongside the integration code.
2. **Cost-tier annotations in code**: Tag each tool call site in the codebase with its known cost tier (free/included, paid-per-call, paid-tiered) so cost implications are visible to anyone reviewing or modifying the agent's logic later.
3. **Per-feature spend caps and alerts**: Configure a budget ceiling specifically for known paid-add-on features, independent of overall API spend, so a cost spike from one capability is caught before it compounds across a billing cycle.
4. **Default to the free/included tier, opt into paid deliberately**: Where a tool offers both a free and paid variant of similar functionality, default agent logic to the free tier, and require an explicit, reviewed decision to route specific high-value cases to the paid tier.
5. **Reconcile usage against invoices on a short cycle**: Review vendor billing detail weekly or bi-weekly rather than waiting for the monthly invoice, so a cost anomaly from a paid feature is caught within days rather than a full billing cycle.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tool.paid_feature_call_count` | Count of calls to capabilities tagged as paid-add-on | Alert when daily count exceeds 2x the trailing 7-day average |
| `tool.estimated_daily_spend_by_feature` | Estimated cost accrued per tracked paid feature, computed from call volume times known unit price | Alert when projected monthly spend exceeds the configured budget cap |
| `tool.paid_vs_free_tier_call_ratio` | Ratio of calls routed to paid tier versus free/included tier for capabilities offering both | Alert on an upward trend with no corresponding business justification |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Paid feature spend cap approaching | `estimated_daily_spend_by_feature` projects to exceed budget cap within the billing cycle | High | Review call routing logic, consider reverting to free tier for non-critical cases |
| Unexpected paid-feature call volume spike | `paid_feature_call_count` doubles day-over-day with no corresponding workload change | Medium | Audit recent code changes for unintended routing to the paid variant |

## Related Patterns
- [Feature Flag Disabled](./feature-flag-disabled.md) - both involve capability-tier gaps between what the agent assumes and what the account actually has enabled/billed
- [Regional Feature Not Available](./regional-feature-not-available.md) - a related capability-assumption gap, availability instead of cost
- [Api Key Quota Per Account](../../tool-allocation-limits/failures/api-key-quota-per-account.md) - both are cases where the agent lacks visibility into a resource constraint tied to its account
