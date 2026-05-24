# Step Repetition

## Issue: Agent Repeats Same Steps Without Progress

**Frequency**: Common (15.7% of MAS failures)

**Symptoms**
- Same tool calls executed multiple times
- Identical reasoning patterns repeated
- No progress despite continued activity
- Output loops without variation

**Root Cause**
Agent repeats the same steps without making progress toward task completion. Unlike infinite loops which may involve retry logic, step repetition involves the agent genuinely re-executing identical steps as if it hasn't done them before.

**Example**
```
Task: "Find and summarize the Q3 sales report"

Agent trace:
Turn 1: search_files("Q3 sales report") → Found: report.pdf
Turn 2: read_file("report.pdf") → [contents]
Turn 3: search_files("Q3 sales report") → Found: report.pdf  [REPEAT]
Turn 4: read_file("report.pdf") → [contents]                 [REPEAT]
Turn 5: search_files("Q3 sales report") → Found: report.pdf  [REPEAT]
Turn 6: read_file("report.pdf") → [contents]                 [REPEAT]
...

Result: Agent never proceeds to summarization
        Burns tokens repeating discovery steps
```

**Key Statistics**
From MAST study of 1642 MAS traces:
- Step repetition accounts for 15.7% of failures
- One of the most common failure modes
- Part of "System Design Issues" category
- Major contributor to resource exhaustion

**Repetition Patterns**
- **Discovery loops**: Repeatedly finding same information
- **Verification loops**: Re-checking already confirmed facts
- **Setup loops**: Re-initializing already configured state
- **Query loops**: Re-asking same questions

**Contributing Factors**
- Agent loses track of completed steps
- No memory of previous actions
- Context window doesn't include recent actions
- Lack of progress tracking mechanism
- Missing state management

**Mitigation Strategies**
1. **Action history**: Maintain visible log of completed steps
2. **Progress markers**: Track task completion state
3. **Repetition detection**: Flag repeated tool calls
4. **State summaries**: Periodically summarize progress
5. **Step limits**: Cap repetitions of same action

**Detection**
- Identical tool calls in short sequence
- Same outputs appearing multiple times
- No task progress despite activity
- Token usage without corresponding progress

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Failure mode 1.3: Step Repetition (15.7% of failures)
- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Loop detection
- [DEV.to: $47,000 Agent Loop](https://dev.to/waxell/the-47000-agent-loop-why-token-budget-alerts-arent-budget-enforcement-389i) - Cost impact of repetition
