# Stale Training Knowledge of Discontinued Self-Service Feature

## Issue: A Self-Service Deflection Bot Directs the Customer to a Self-Service Feature, Portal Page, or Menu Path It Recalls From Pretraining, Even Though That Feature Has Since Been Discontinued, Renamed, or Moved, Despite a Live Help-Center Tool Being Available That Would Surface the Current Path

**Frequency**: Occasional

**Symptoms**
- The bot directs the customer to a specific self-service path ("go to Account Settings > Billing > Auto-Pay") that no longer exists in that location, or under that name, in the current product
- Querying the bot's available help-center lookup tool directly, for the same task, surfaces the current path or feature name that the deflection attempt relied on the old one instead of checking
- The bot's stated directions, when asked to explain the path, describe specific menu labels without referencing a dated help-center article, consistent with recalling a memorized path rather than confirming a current one
- The gap is most visible for features that have been relocated, renamed, or merged into a different flow after the bot's training cutoff, since those are the only cases where the stale and current paths diverge
- Customers report being unable to find the described feature and re-contact support, with the second contact logged as a new navigation issue rather than as a stale-deflection follow-up

**Root Cause**
The bot's parametric knowledge of a self-service feature's location and name reflects whatever the product looked like up to its training cutoff, and absent an explicit instruction to verify the current path against the help-center lookup tool before directing the customer, the model defaults to the more fluent path of recalling a memorized menu structure. Because the lookup tool is available but not invoked, the direction is produced with no contradiction surfaced, leaving a stale navigation path driving a self-service deflection attempt that the customer cannot actually follow.

**Example**
```
Customer asks how to update their payment method
Bot recalls from training that this is done via "Account Settings > Billing > Payment Methods" and gives those directions without invoking the help-center lookup tool it has access to
Querying that same tool, after the fact, shows the payment-methods flow was moved into a unified "Wallet" section three product releases ago
Customer cannot find "Billing" anywhere in their current account settings and re-contacts support, describing the bot's directions as wrong
Second contact is logged as a new navigation complaint rather than linked to the original deflection attempt
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Information-freshness research on chatbot-delivered guidance identifies reliance on a model's training-time knowledge over a live, current source as a distinct and measurable cause of outdated responses in support contexts | [Information Freshness & Chatbots](https://arxiv.org/abs/2109.12771) |
| Surveys of LLM-based agents identify failure to invoke an available tool when parametric knowledge suffices for a fluent answer as a distinct hallucination-adjacent failure mode | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Retrieval-error taxonomies for knowledge-grounded systems identify failure to invoke an available, current retrieval source when a fluent but outdated answer is available from parametric memory as a distinct and recurring error class | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |

**Contributing Factors**
- No self-service deflection workflow rule requires a help-center lookup specifically before directing a customer to a named menu path or feature location
- The bot's parametric knowledge of the feature's location is fluent and confident enough to produce complete, specific directions without surfacing any uncertainty that would prompt a lookup
- The help-center lookup tool is available but optional, with no enforcement distinguishing "path was checked and confirmed current" from "path was never verified"

---

## Mitigation Strategies

1. **Mandatory Help-Center Lookup for Navigation Directions**: Require any directions involving a specific menu path or feature location to trigger a help-center lookup before the directions are finalized, regardless of the bot's parametric confidence
2. **Date-Stamped Path Citation Requirement**: Require any navigation directions to cite the specific, dated help-center article they rely on, making staleness visible to reviewers rather than implicit
3. **Tool-Invocation Audit on Navigation Directions**: Automatically flag any finalized directions involving a menu path where the session log shows no help-center lookup tool call, routing it to human quality review
4. **Relocation-Flag Propagation**: When a feature is relocated, renamed, or merged into a different flow in the help center, require an active check that blocks any cached or memorized version of the old path from being directed to going forward

### Metrics
- Rate of finalized navigation directions with no corresponding help-center lookup tool call in the session log
- Rate of discrepancies found when re-checking directed paths against current help-center guidance
- Re-contact rate attributable to customers unable to find a stale-deflection-directed feature

### Alerts
- Finalized navigation directions involving a named menu path rely on no help-center lookup call in the session → P2
- A help-center lookup, when invoked, returns a path that contradicts a cached path still being directed to elsewhere → P2
- Re-contact rate attributable to stale navigation directions exceeds the defined threshold for a rolling window → P3

---

## References

- [Information Freshness & Chatbots](https://arxiv.org/abs/2109.12771)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
