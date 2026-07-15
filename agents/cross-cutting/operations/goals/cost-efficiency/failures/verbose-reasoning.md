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

## Mitigation Strategies

### Prevention
1. **Task-appropriate detail scaling**: The example shows a trivial "What's 2+2?" query producing 600 tokens including an unnecessary explanation of "what addition means" — classify task complexity and explicitly scale allowed explanation depth to it, so simple factual/arithmetic queries get direct answers while genuinely complex reasoning tasks retain full chain-of-thought. Trade-off: complexity classification can misjudge edge cases where a seemingly simple question actually needs explanation for the specific user.
2. **Explicit conciseness constraints in the prompt**: Since the root cause names "prompts encouraging detailed explanations" and "no feedback on verbosity in production" as drivers, add explicit brevity instructions (e.g., "answer directly; only show reasoning if the user asks or the task requires multi-step logic") rather than leaving verbosity unconstrained by default. Trade-off: overly aggressive conciseness instructions can suppress genuinely useful reasoning transparency that users or auditors want for complex decisions.
3. **Structured output schemas for deterministic-answer tasks**: For tasks with a clear expected answer shape (like arithmetic, classification, or lookups), require a JSON/schema-constrained output that has no room for free-form "thinking out loud," which structurally prevents the 500-token preamble seen in the example. Trade-off: schema constraints don't fit open-ended tasks (summarization, advice) where some prose is the actual desired output.

### Detection & Response
1. **Output-token-to-task-complexity ratio**: Track output tokens generated against an independent complexity score for the task; the example's 600-tokens-for-a-1-token-answer represents a ratio flag that should be visible and comparable across task types.
2. **Reasoning-length distribution by task type**: Monitor the distribution of output length for supposedly simple task categories (arithmetic, yes/no, lookups); a fat tail of long responses in a category expected to be short indicates verbosity constraints aren't being applied or are being ignored.
3. **Repetitive-explanation detection across turns**: Since "repetitive explanations across turns" is a named symptom, flag conversations where near-identical explanatory boilerplate (e.g., re-explaining what addition means) recurs across multiple turns of the same session.

### Architecture Patterns
1. **Output token cap by task category**: Enforce a hard max-token limit on generation calls classified as simple/factual (e.g., cap at 50 tokens for arithmetic/lookup-style queries), preventing the 500-token preamble in the example regardless of what the model would otherwise generate. Deployment consideration: caps must be set per task category, not globally, or complex tasks needing more room will be truncated mid-explanation.
2. **Separate reasoning/answer pipeline**: Route chain-of-thought reasoning to a cheaper model or a non-user-facing scratchpad, returning only the final answer to the user-facing channel, addressing "Move thinking to cheaper model or cache" from a cost-allocation angle — verbose reasoning still happens where needed but doesn't inflate the cost of the primary (often more expensive) model call. Deployment consideration: requires an architecture that can pass intermediate state between a cheap reasoning pass and the final-answer model call.
3. **Post-generation summarization/trim pass**: For cases where verbose output is already generated (e.g., a model that can't be reliably prompted into brevity), apply an automated post-processing step that extracts just the final answer/conclusion before returning it to the user, providing a safety net even when prevention-layer prompting fails. Deployment consideration: adds a second model call or heuristic pass, partially offsetting token savings unless done cheaply (e.g., simple final-sentence extraction).

### Metrics
1. **output_tokens_per_task_complexity_tier**: Target < 30 tokens for tier "trivial" (arithmetic, yes/no); Alert if median > 150 tokens for that tier (approaching the 600-token example).
2. **verbosity_ratio** (output tokens ÷ minimum-necessary tokens, sampled): Target < 3x; Alert if > 20x (matching the ~600x ratio in the example as the failure ceiling to catch well before).
3. **repetitive_explanation_rate**: Target < 5% of multi-turn sessions show near-duplicate explanatory boilerplate across turns; Alert if > 20%.
4. **pct_responses_within_token_cap**: Target > 95% of simple-tier responses within their category's token cap; Alert if < 80%.

### Alerts
1. **Verbosity-Ratio-Breach** (P3): Condition - verbosity_ratio for a sampled response exceeds 20x for a task classified as trivial/simple. Action: review the prompt/system-instruction for that task category for missing conciseness constraints; consider adding a hard output cap.
2. **Simple-Tier-Token-Cap-Violations** (P3): Condition - pct_responses_within_token_cap for the trivial tier drops below 80% over a rolling day. Action: audit whether a recent prompt or model change removed brevity instructions, and re-verify structured-output schema enforcement is active where applicable.

## References

- [LeanOps: Agents Burn 50x More Tokens](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026/) - Analysis of excessive token usage from verbose reasoning
- [MindStudio: Token Budget Management](https://www.mindstudio.ai/blog/ai-agent-token-budget-management-claude-code) - Strategies for managing token budgets in AI agents
