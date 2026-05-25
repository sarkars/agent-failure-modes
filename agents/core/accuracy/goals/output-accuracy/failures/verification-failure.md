# Verification Failure

## Issue: Agent Fails to Verify or Incorrectly Verifies Work

**Frequency**: Common (17.3% of MAS failures combined)

**Symptoms**
- Agent delivers output without checking correctness
- Verification performed but with wrong criteria
- Errors pass through verification undetected
- Agent claims success when task actually failed

**Root Cause**
Agent fails in task verification - either by not verifying its work at all, performing incomplete verification, or verifying incorrectly. This final quality control step is crucial but frequently fails, allowing errors to propagate to users.

**Example**
```
Task: "Generate a function that returns the factorial of n"

Agent output:
def factorial(n):
    result = 1
    for i in range(n):  # Bug: should be range(1, n+1)
        result *= i
    return result

Agent verification:
"Let me verify: factorial(5) should be 120.
 Running... factorial(5) = 0
 That looks correct! Task complete."

Problem: 
- Agent tested but misread result (0 != 120)
- Incorrect verification led to buggy code delivery

Result: Broken function delivered with false confidence
```

**Key Statistics**
From MAST study of 1642 MAS traces:
- No/Incomplete Verification: 8.2% of failures
- Incorrect Verification: 9.1% of failures
- Combined verification failures: 17.3%
- Part of "Task Verification" category (23.5% total)

**Verification Failure Types**
- **Skipped verification**: No testing before delivery
- **Incomplete verification**: Only partial testing
- **Wrong criteria**: Testing against incorrect expectations
- **Misread results**: Incorrect interpretation of test output
- **Hallucinated verification**: Claiming to verify without doing so

**Contributing Factors**
- Pressure to complete quickly
- No explicit verification requirements
- Verification steps not in prompt
- Difficulty interpreting test outputs
- Overconfidence in initial output

**Mitigation Strategies**
1. **Mandatory verification**: Require verification before completion
2. **Structured test cases**: Define expected test scenarios
3. **External validation**: Use separate verification agent
4. **Result comparison**: Explicit expected vs actual comparison
5. **Multi-stage verification**: Multiple verification rounds

**Detection**
- Outputs failing when users test them
- Verification claims without corresponding actions
- Test results mismatched with verification conclusions
- Pattern of "verified" outputs having errors

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Failure modes 3.2 and 3.3: Verification failures (17.3% combined)
- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Verification gaps in RAG systems
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Quality control failures
