# Sales Crm AI Agent Failures by Goal: 16 Patterns, Causes, and Fixes

**Sales Crm failures in AI agents are grouped here into 4 goals, each with a catalog of named failure patterns, the symptoms you will see, the root cause, and mitigations you can copy.** Start from the symptom you are debugging, pick the matching goal below, and open its failure list.

## Key Takeaways

- This use case covers 4 goals and 16 documented failure patterns.
- The largest goal is [Quota Achievement](quota-achievement/) with 5 patterns.
- Each goal page explains the failure class, how to tell it apart from its neighbors, and which mitigations apply across its patterns.
- Each failure page covers the symptoms, an example, the root cause, and how to fix it.

## Sales Crm Goals

| Goal | What goes wrong | Patterns |
|---|---|---|
| [Deal Management](deal-management/) | Deal management failures occur when agents assemble contract clauses, track negotiated terms, or approve deals using stale pricing data, wrong contract templates, or missing handoff fields that capture negotiated exceptions | 3 |
| [Lead Scoring](lead-scoring/) | Lead-scoring failures occur when agents compute a lead's likelihood-to-close using stale scoring rules, fabricated data when tool results are unavailable, superficially-similar deal precedents instead of structurally comparable ones | 4 |
| [Pipeline Forecasting](pipeline-forecasting/) | Pipeline-forecasting failures occur across multiple independent dimensions | 4 |
| [Quota Achievement](quota-achievement/) | Quota-achievement failures occur when agents calculate rep quota attainment using stale discount policies, fabricated approval records, mismatched coaching recommendations, or unverified credit adjustments | 5 |

**Total: 16 patterns**

## Frequently Asked Questions

### Where do I start if my sales crm agent is failing?

Match the symptom to a goal in the table above, then open that goal's page for how to tell its failures apart and where to look first. Each failure page ends in mitigations you can apply directly.

### How are these sales crm failure patterns organized?

By goal: the outcome the agent is supposed to achieve. Under each goal, a `failures` folder holds one page per pattern. For the full picture see the [Sales Crm overview](../).

## Related

- [Sales Crm overview](../)
- [All agent failure patterns](../../../)
