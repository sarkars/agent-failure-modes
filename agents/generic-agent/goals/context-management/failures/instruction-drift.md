# Instruction Drift

## Issue: Agent Gradually Deviates from Original Instructions

**Frequency**: Common

**Symptoms**
- Agent behavior changes over long conversations
- Style or approach shifts from initial instructions
- Constraints mentioned early are violated later
- Agent "forgets" persona or role

**Root Cause**
As conversations grow, system instructions become proportionally smaller in context. Recent turns may implicitly override or contradict earlier instructions. Agent attention shifts toward recent content.

**Example**
```
System: "Always respond formally. Never use contractions."

Turn 1-10: Formal responses, no contractions
Turn 20: "Here's what you'll need to do..."
Turn 30: "Yeah, that's totally doable!"

Result: Agent has drifted from formal style to casual
```

**Mitigation Strategies**
1. **Instruction repetition**: Periodically re-inject key instructions
2. **Instruction anchoring**: Place instructions where attention is highest
3. **Behavior monitoring**: Detect drift and course-correct
4. **Shorter sessions**: Reset context for fresh instruction adherence
5. **Instruction summarization**: Compress but preserve constraints
6. **Explicit reminders**: User or system reminds of constraints

**Detection**
- Track instruction adherence metrics over conversation length
- Monitor for constraint violations
- Compare early vs. late behavior patterns
- Alert on style/behavior drift

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Instruction following degradation
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Behavioral drift patterns
