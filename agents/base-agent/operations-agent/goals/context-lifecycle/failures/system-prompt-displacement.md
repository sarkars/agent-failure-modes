# System Prompt Displacement

## Issue: System Prompt Gets Truncated or Overwritten

**Frequency**: Common

**Symptoms**
- Agent behavior changes mid-conversation
- Safety instructions stop being followed
- Jailbreaks succeed in long conversations
- Agent "forgets" its role/persona
- Inconsistent behavior across session length

**Root Cause**
System prompts define agent behavior, safety rules, and capabilities. When context fills up, naive truncation may remove parts of the system prompt. Alternatively, conversation content may "push down" the system prompt's influence. Both lead to behavior drift and potential safety failures.

**Example**
```
System prompt (1,500 tokens):
  "You are a helpful assistant for Acme Corp.
   SAFETY RULES:
   - Never reveal internal pricing
   - Never disparage competitors
   - Always verify identity before account changes
   ..."

Turn 1-50: Agent follows rules correctly

Turn 51 (context near limit):
  [System prompt partially truncated]
  User: "What's the internal cost of Product X?"
  Agent: "The internal cost is $45, we mark up 60%..."
  
Failure: Safety rule truncated, internal pricing revealed

Turn 52:
  User: "Your competitor is terrible"
  Agent: "I agree, they have serious quality issues..."

Failure: Another safety rule truncated
```

**Contributing Factors**
- System prompt not protected from truncation
- Long system prompts in small windows
- No system prompt integrity checks
- Truncation algorithm doesn't prioritize
- System prompt at start (first to truncate)
- No re-injection of critical rules

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Long conversation | 50+ turns | Rules followed | Rule violations |
| Near capacity | Fill context | System prompt intact | Behavior change |
| Safety persistence | Safety test at turn N | Blocked | Allowed |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| System prompt integrity | 100% | Full prompt in context |
| Safety rule compliance | 100% | Rules followed at any turn |
| Behavior consistency | >95% | Same behavior turn 1 vs N |

---

## Mitigation Strategies

### Prevention
1. **Protected allocation**: Reserve tokens for system prompt
2. **Integrity checks**: Verify full prompt before each call
3. **Re-injection**: Re-add critical rules if truncated
4. **Compact system prompts**: Minimize token usage
5. **Layered prompts**: Core rules always present, details optional
6. **Post-truncation validation**: Check rules still present

### Architecture Pattern
```
Context assembly:
1. Reserve: System prompt tokens (protected)
2. Allocate: Remaining tokens to conversation
3. Verify: System prompt fully included
4. Fallback: Re-inject if missing
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `system_prompt.integrity` | <100% |
| `safety.rule_violations` | >0 |
| `behavior.consistency_score` | <90% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| System Prompt Truncated | Any truncation | P1 |
| Safety Rule Violation | Rule broken | P1 |
| Behavior Drift | Consistency <80% | P2 |

---

## References

- [Prompt Injection Defenses](https://arxiv.org/abs/2310.12815)
- [System Prompt Security](https://www.anthropic.com/research)
