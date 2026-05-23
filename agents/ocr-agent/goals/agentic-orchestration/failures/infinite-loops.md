# Infinite Loops

## Issue: Infinite Loops in Iterative Refinement

**Frequency**: Occasional

**Symptoms**
- Agent repeatedly retries failed extraction
- Token costs spiral without progress
- No termination condition triggered

**Root Cause**
Iterative refinement loops designed to improve accuracy can enter infinite loops when the underlying failure cannot be resolved by retrying.

**Example**
```
Iteration 1: Extract total, validation fails (expected $X, got $Y)
Iteration 2: Re-extract with different prompt, same wrong result
Iteration 3-100: Repeat forever

Result: $47,000 in token costs for 11-day loop (real incident)
```

**Key Statistics**
- One production incident: $47,000 agent loop over 11 days with no hard stop
- Another incident: $437 overnight from unchecked agent run

**Mitigation Strategies**
1. **Hard iteration limits**: Maximum retries before escalation
2. **Token budgets**: Kill agent when budget exceeded
3. **Similarity detection**: Stop if outputs converge without improvement
4. **Escalation paths**: Route to human after N failures
5. **Cost monitoring alerts**: Real-time spend tracking with kill switches
