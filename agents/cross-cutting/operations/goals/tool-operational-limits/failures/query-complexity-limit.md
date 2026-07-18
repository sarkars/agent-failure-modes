# Query Complexity Limit

## Issue
Query tools that support flexible field selection — most notably GraphQL APIs — often score each incoming query for computational cost (a function of field count, list multipliers, and nesting) and reject any query above a threshold, independent of raw depth or byte size. An agent auto-generating a query to fulfill a broad request ("get me everything about this customer") can easily construct a query that is shallow and small in text but scores extremely high in complexity, because a handful of fields that each return large lists multiply together into a cost the agent has no way to estimate from the query text alone.

**Frequency**: Occasional

**Symptoms**
- Queries rejected with a complexity-score error (e.g., "query cost 4,200 exceeds maximum 1,000") on queries that look modest in size or depth
- Complexity failures that are hard to predict from query structure alone, since the cost model weighs list-returning fields more heavily than scalar fields
- Agents that dynamically select fields based on a task description, including expensive fields (e.g., a field returning a paginated list of all historical orders) without realizing the cost multiplier
- Retried queries that fail identically because the agent's retry logic doesn't reduce field selection or add pagination limits between attempts
- Complexity limits that vary by endpoint or by authenticated client tier, so a query that succeeds against one environment fails against another with a stricter limit

## Root Cause
Complexity/cost-analysis limits exist because query depth and payload size alone don't capture true execution cost in a schema where a single field can trigger an expensive database aggregation or fan out into thousands of nested results (a customer's `orders` field returning 10,000 rows, each with a nested `line_items` field). Agents constructing queries from a natural-language goal typically select fields based on relevance to the task, not based on the schema's declared cost weights for each field — information that, even when published, is not something the agent's query-generation logic consults before assembling the query. As a result the agent has no way to estimate the complexity score of a query it has not yet sent, and discovers the limit only via rejection, often without a clear signal of which specific field selection drove the cost over threshold.

## Example
```
An agent building a customer 360 dashboard issues a single GraphQL query
requesting a customer's profile, all orders (each with all line items and
associated shipment tracking events), and all support tickets (each with
full comment threads). Textually the query is only 4 levels deep and
under 2KB, well within depth and payload-size limits. The GraphQL server's
cost analyzer, which weights list fields by an estimated multiplier
(orders: x50, line_items per order: x20, tracking_events: x10, tickets:
x30, comments per ticket: x15), computes a total query cost of 6,800
against a maximum of 1,000, and rejects the query with
{"errors": [{"message": "Query cost 6800 exceeds maximum cost 1000",
"extensions": {"cost": 6800, "maxCost": 1000}}]}.
The agent has no logic to interpret the cost/maxCost fields, retries the
identical query twice, then falls back to fetching each section (orders,
tickets) as separate unpaginated queries — each of which independently
also exceeds the cost limit, since the underlying list sizes didn't change.
```

## Statistics
| Finding | Context |
|---------|---------|
| GraphQL cost-analysis maximums commonly sit in the low thousands (e.g., 1,000-5,000 cost units) with list-returning fields weighted 10-50x a scalar field | Common configuration pattern for cost-based GraphQL rate limiting |
| Complexity-limit rejections are harder for agents to self-diagnose than depth or size limits, since the cost model is rarely fully exposed to clients ahead of query submission | Structural property of cost-based vs. structural limits |
| Adding pagination arguments (`first: N`) to list fields is typically sufficient to bring an otherwise-rejected query under the complexity threshold, since cost models scale with expected result-set size | Based on typical GraphQL cost-analysis implementations |

## Mitigations
1. **Always paginate list-returning fields explicitly**: Include a `first`/`limit` argument on every field that can return a list, since unbounded list fields are the primary driver of complexity-score blowups; never rely on server-side defaults.
2. **Parse and act on cost/maxCost extensions in error responses**: When a complexity error includes the actual and maximum cost, use that ratio to decide how aggressively to reduce field selection or pagination on retry, rather than retrying unchanged.
3. **Decompose expensive queries into multiple cheaper ones**: Split a single high-cost query into sequential smaller queries (e.g., fetch orders paginated, then fetch line items per order in a follow-up batch) that each stay under the complexity ceiling.
4. **Maintain a field-cost awareness list for frequently-used schemas**: Track which fields are known to carry high complexity weight (from documentation or observed rejections) and bias query construction away from including several such fields in one request.
5. **Request the schema's published cost directives when available**: Some GraphQL schemas expose `@cost` directives via introspection; use these to estimate a query's cost before submission rather than discovering it via rejection.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `query.estimated_complexity_score` | Agent-side estimate (or server-reported actual) complexity cost of constructed queries | Alert when estimate exceeds 80% of known max |
| `query.complexity_rejection_count` | Count of queries rejected specifically for exceeding cost/complexity threshold | Alert if > 0 |
| `query.unpaginated_list_field_count` | Number of list-returning fields included without an explicit pagination argument | Alert if > 0 on any constructed query |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Query complexity limit exceeded | Response includes a cost/maxCost complexity rejection | Medium | Add pagination to list fields, decompose into smaller queries, resubmit |
| Repeated retry without complexity reduction | Same high-cost query resubmitted unchanged after a complexity rejection | High | Disable naive retry, route through complexity-aware query decomposition |

## Related Patterns
- [Join Depth Limit](./join-depth-limit.md) - a structural depth cap that complements but is independent of cost-based complexity scoring
- [Query Planning Timeout](./query-planning-timeout.md) - a query that passes complexity scoring can still time out during planning if the cost model underestimates true execution cost
- [Nesting Depth Limit](./nesting-depth-limit.md) - a payload-structure limit distinct from query-cost limits, though both stem from bounding server-side processing cost
