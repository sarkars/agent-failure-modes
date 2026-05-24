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

**Mitigation Strategies**
1. **Rule validation offloading**: Environment checks rules before execution
2. **Rule summaries**: Provide applicable rules for current context
3. **Structured rule representation**: Use machine-readable rule format
4. **Pre-flight checks**: Validate action against rules before execution
5. **Rule conflict resolution**: Explicit priority ordering for rules

**Detection**
- Actions that violate documented business rules
- User complaints about incorrect denials
- Compliance audit failures
- Pattern of same rule being misapplied

## References

- [Aegis: Agent-Environment Failures](https://arxiv.org/abs/2508.19504) - Domain rule violation as exploitation failure mode
- [Air Canada Chatbot Lawsuit](https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116416) - Real-world rule violation incident
- [NYC MyCity Chatbot](https://www.cxtoday.com/contact-center/3-times-customer-chatbots-went-rogue-and-the-lessons-we-need-to-learn/) - Agent advising illegal actions
