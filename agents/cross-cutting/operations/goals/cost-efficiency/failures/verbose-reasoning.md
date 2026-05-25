# Verbose Reasoning

## Issue: Excessive Chain-of-Thought Output

**Frequency**: Very Common

**Symptoms**
- Agent produces lengthy reasoning for simple tasks
- Output tokens far exceed necessary length
- Repetitive explanations across turns
- "Thinking out loud" when action is clear

**Root Cause**
- Chain-of-thought prompting without length constraints
- Agent trained to be thorough rather than efficient
- No feedback on verbosity in production
- Prompts encouraging detailed explanations

**Example**
```
User: What's 2+2?

Agent: Let me think through this step by step. First, I need to 
understand what addition means. Addition is a mathematical operation 
that combines two numbers... [500 more tokens of explanation]
The answer is 4.

Result: 600 tokens for a 1-token answer
```

**Mitigation Strategies**
1. **Conciseness instructions**: Explicitly prompt for brevity
2. **Output token limits**: Cap maximum response length
3. **Structured outputs**: Use JSON/schemas to reduce verbosity
4. **Separate reasoning**: Move thinking to cheaper model or cache
5. **Task-appropriate detail**: Scale explanation to complexity
6. **Post-processing**: Summarize verbose outputs before returning

**Detection**
- Track output token distribution by task type
- Compare reasoning length to task complexity
- Monitor user engagement with lengthy responses
- A/B test concise vs. verbose responses

---

## References

- [LeanOps: Agents Burn 50x More Tokens](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026/) - Analysis of excessive token usage from verbose reasoning
- [MindStudio: Token Budget Management](https://www.mindstudio.ai/blog/ai-agent-token-budget-management-claude-code) - Strategies for managing token budgets in AI agents
