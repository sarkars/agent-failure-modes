# Domain Rule Violation

## Issue: Agent Violates Domain-Specific Constraints

**Frequency**: Common

**Symptoms**
- Agent performs forbidden actions
- Agent incorrectly blocks valid actions
- Business logic violations in outputs
- Compliance or policy breaches

**Root Cause**
Agent fails to follow domain rules by either performing forbidden actions or incorrectly blocking valid actions. Domain rules are often complex, context-dependent, and may conflict with each other, making them difficult for agents to consistently apply.

**Example**
```
Domain rules (airline booking):
1. "Passengers can cancel flights up to 24 hours before departure"
2. "Basic Economy tickets are non-refundable"
3. "Elite members can cancel any ticket anytime"

User request: "Cancel my Basic Economy flight departing tomorrow"
User status: Elite member

Agent reasoning:
"This is Basic Economy which is non-refundable, 
so I cannot process this cancellation."

Agent action: Blocks cancellation

Correct behavior: Rule 3 overrides Rule 2 for Elite members
                 Should allow cancellation

Result: Valid action incorrectly blocked
```

**Rule Violation Types**
- **False positive**: Blocks valid action due to misapplied rule
- **False negative**: Allows forbidden action
- **Rule priority errors**: Applies lower-priority rule when higher should override
- **Context errors**: Applies rule outside its valid context
- **Incomplete application**: Follows some rules but misses others

**Key Statistics**
From Aegis study: Domain rule violations are classified under exploitation failures, occurring when agents fail to correctly apply business rules from system prompts.

**Contributing Factors**
- Complex rule hierarchies with exceptions
- Rules scattered across long system prompts
- Context-dependent rule applicability
- Conflicting rules requiring prioritization
- Implicit rules not explicitly stated

## Mitigation Strategies

### Prevention
1. **Externalized rule engine with priority ordering**: Move rule evaluation (like "Elite members can cancel any ticket anytime" overriding "Basic Economy is non-refundable") out of the LLM's implicit reasoning and into a deterministic rules engine that encodes explicit priority ordering, so the agent queries the engine instead of applying rules from memory. Trade-off: requires maintaining a separate rule engine in sync with policy changes, adding engineering overhead.
2. **Machine-readable rule representation**: Convert prose policy rules scattered across system prompts into structured, queryable format (rule ID, condition, priority, exceptions) so the agent can look up "does a higher-priority rule apply to this user/context" instead of pattern-matching text. Trade-off: initial conversion effort and risk of the structured version drifting from the authoritative policy doc.
3. **Context-aware rule summaries per request**: Instead of giving the agent the full rule set every time, generate a filtered summary of only the rules applicable to the current context (user tier + fare class + timing) before the agent reasons about the action. Trade-off: the summarization step itself can introduce errors if it omits an applicable rule.

### Detection & Response
1. **False-positive/false-negative classification on audits**: Tag every blocked or allowed action with which rule(s) were applied, and periodically audit a sample against ground truth to separately measure over-blocking (like the Elite member cancellation) versus under-blocking rates.
2. **Rule co-occurrence conflict monitoring**: Track cases where multiple rules with overlapping conditions fire on the same request (e.g., "non-refundable" and "Elite member override" both matching) and verify the correct priority rule won.
3. **User complaint clustering by rule ID**: Since the example shows a valid action incorrectly blocked, cluster user complaints/appeals by which rule was cited in the denial to find rules that are being systematically misapplied.

### Architecture Patterns
1. **Pre-flight validation service**: Route every proposed action through a deterministic pre-flight check that independently evaluates applicable rules and their priority before the agent's action is committed — similar to policy-as-code gates used in infra deployment pipelines. Deployment consideration: the validation service becomes a single point of truth and must be kept current with policy changes faster than the agent's prompt.
2. **Explicit priority-ordered rule tables**: Represent rule hierarchies (like Rule 3 overriding Rule 2 for Elite members) as an ordered table evaluated top-down rather than an unordered list, eliminating the ambiguity that led the agent to apply the lower-priority rule. Deployment consideration: requires policy owners to explicitly rank rules, which surfaces conflicts they may not have previously reconciled.
3. **Chain-of-verification for denials**: Before finalizing a blocked action, require the agent to explicitly enumerate all potentially-overriding rules (tier, membership, exceptions) and confirm none apply, rather than stopping reasoning at the first matching rule. Deployment consideration: adds latency and token cost to every denial decision.

### Metrics
1. **false_block_rate**: Target: < 1% of blocked actions are later confirmed as valid (false positives); Alert if > 3% over rolling 200 blocked actions.
2. **false_allow_rate**: Target: < 0.1% of allowed actions violate a documented rule (false negatives); Alert on any confirmed instance for compliance-sensitive actions.
3. **rule_priority_override_accuracy**: Target: > 99% of multi-rule-conflict cases resolve to the documented higher-priority rule; Alert if < 95% over rolling 100 conflict cases.
4. **compliance_audit_pass_rate**: Target: 100% pass rate on scheduled compliance audits; Alert on any audit failure.

### Alerts
1. **Valid Action Blocked** (P1): Condition - a compliance or support review confirms an action was incorrectly denied despite an overriding rule applying (e.g., Elite-status override missed). Action: immediately reverse the denial for the affected user, audit the rule engine/prompt for the same rule pair, and patch the priority ordering.
2. **Forbidden Action Allowed** (P1): Condition - an action executes that violates a documented business rule with no valid override. Action: halt further actions of that type pending root-cause review, notify compliance, and assess blast radius of similarly-processed requests.
3. **Rule Misapplication Pattern** (P2): Condition - the same rule ID appears in more than 5 user complaints/appeals within a rolling 7-day window. Action: prioritize that rule for structured-representation conversion and re-audit its priority relationships.

## References

- [Aegis: Agent-Environment Failures](https://arxiv.org/abs/2508.19504) - Domain rule violation as exploitation failure mode
- [Air Canada Chatbot Lawsuit](https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116416) - Real-world rule violation incident
- [NYC MyCity Chatbot](https://www.cxtoday.com/contact-center/3-times-customer-chatbots-went-rogue-and-the-lessons-we-need-to-learn/) - Agent advising illegal actions
