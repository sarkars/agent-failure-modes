# Tool Parameter Errors

## Issue: Tool Parameter Errors

**Frequency**: Common

**Symptoms**
- Tools called with wrong parameters
- Page ranges incorrect
- Region coordinates misspecified
- Output format mismatches downstream needs

**Root Cause**
Agent must translate document understanding into specific tool parameters. Errors in this translation cause extraction failures.

**Example**
```
Agent intent: Extract table from page 5
Tool call: extract_table(page=4)  # Off-by-one error

Result: Wrong table extracted, agent proceeds with incorrect data
```

**Key Statistic**
37% of tool calls have silent parameter mismatches according to developer analysis.

**Mitigation Strategies**
1. **Parameter validation**: Tools validate inputs before execution
2. **Visual confirmation**: Agent verifies extraction region matches intent
3. **Schema enforcement**: Strict parameter typing catches errors early
4. **Error recovery**: Failed tool calls trigger retry with corrected parameters
