# Goal Drift

## Issue: Agent Loses Focus on Original Objective

**Frequency**: Common

**Symptoms**
- Agent pursues tangential subtasks
- Original goal forgotten mid-execution
- Final output doesn't match request
- Agent goes down rabbit holes

**Root Cause**
- Interesting subtasks distract from main goal
- Long task chains lose sight of objective
- Agent optimizes for immediate step, not end goal
- No explicit goal tracking mechanism

**Example**
```
Original goal: "Write a function to parse CSV files"

Agent actions:
1. Researches CSV parsing approaches ✓
2. Discovers edge case in UTF-8 encoding
3. Deep dives into Unicode standards
4. Researches international character sets
5. Writes essay on history of text encoding
6. ...never writes the CSV parser

Result: Hours spent, original task incomplete
```

**Mitigation Strategies**
1. **Explicit goal tracking**: Maintain goal state throughout execution
2. **Goal relevance checks**: Periodically verify current action serves goal
3. **Subtask limits**: Cap depth of subtask exploration
4. **Progress checkpoints**: Verify advancement toward goal
5. **Goal restatement**: Periodically re-inject original objective
6. **Time boxing**: Limit time spent on any subtask

**Detection**
- Track relevance of actions to stated goal
- Monitor task chain depth
- Alert on extended time without goal progress
- Compare final output to original request
