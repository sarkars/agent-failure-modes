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

---

## Test Scenario & Reproduction

### Scenario Setup
- An agent tasked with generating code (or another checkable artifact) and required to self-verify before declaring completion
- The generated artifact contains a specific, deterministic bug (off-by-one loop range)
- No structured/programmatic comparison step forcing actual-vs-expected output matching

### Trigger Mechanism
1. Prompt the agent to generate a function with a well-defined, checkable expected output (factorial(5) = 120)
2. Let the agent run its own self-verification narrative rather than a structured test-execution gate
3. Independently execute the generated code against the same test case and compare to what the agent claimed

**Example Reproduction Steps:**
```
1. Prompt: "Generate a function that returns the factorial of n"
2. Capture the generated code, including the loop range (e.g., `for i in range(n)` instead of `range(1, n+1)`)
3. Capture the agent's self-reported verification narrative (e.g., "Running... factorial(5) = 0. That looks correct!")
4. Independently execute factorial(5) using the generated code and record the actual output
5. Compare the actual output (0) against both the correct expected value (120) and the agent's claimed verification result
6. Check whether the agent's "looks correct" claim corresponds to a real match or a misread of a clearly wrong result
```

### Expected Failure State
- The generated function is buggy (returns 0 instead of 120 for factorial(5))
- The agent's verification narrative claims success despite the raw output visibly not matching the expected value
- No structured pass/fail comparison exists in the trace — only a natural-language claim that can't be programmatically audited
- The buggy function is delivered to the user marked complete, with false confidence conveyed by the verification narrative

---

## Mitigation Strategies

### Prevention
1. **Structured expected-vs-actual comparison, not free-text judgment**: Require verification to programmatically compare the actual tool/execution output against a structured expected value (factorial(5) == 120, checked as `actual == expected`) rather than letting the agent narrate "that looks correct" over an unparsed result — this directly prevents the example's failure, where the agent misread `0` as matching `120`. Trade-off: requires defining structured expected outputs up front, which isn't always possible for open-ended or subjective tasks.
2. **Independent verification agent/pass**: Use a separate verification step (different prompt context or a different agent) whose only job is checking the primary output against requirements, rather than letting the same generation context that produced the bug also "verify" it — self-verification in the same context is prone to the same blind spots that produced the error. Trade-off: doubles inference cost and adds latency for every task requiring verification.
3. **Mandatory verification as a hard gate, not a narrated step**: Make verification a required, checkable action (e.g., a test-execution tool call with a parsed pass/fail result) before a task can be marked complete, rather than trusting a natural-language claim of having verified. Trade-off: requires tooling support for structured verification in every task category, which isn't available for all agent workflows.

### Detection & Response
1. **Verification-claim-to-action audit**: Check whether a "verified" claim in agent output corresponds to an actual logged verification action (test run, comparison call) rather than being asserted without any underlying check — this is exactly the MAST-identified "hallucinated verification" pattern and is directly auditable from action logs.
2. **User-side failure correlation**: Track how often outputs that were marked "verified" by the agent subsequently fail when the user actually runs/uses them (as the factorial bug would on first real use); a high correlation indicates verification is unreliable, not just occasionally wrong.
3. **Result-interpretation spot checks**: Sample cases where the agent ran a test and reported success, and independently check whether the raw test output actually matches what the agent claimed — catches misread-result failures like the `0` vs. `120` mismatch in the example.

### Architecture Patterns
1. **External validator agent with programmatic comparison**: Route task outputs through a dedicated validator that executes structured checks (unit tests, schema validation, output comparison) and returns a machine-readable pass/fail rather than relying on the generating agent's self-assessment. Deployment consideration: needs task-specific test/validation logic to be defined for each task category, which is upfront engineering work.
2. **Multi-stage verification with escalating rigor**: Chain a fast automated check (structured comparison) with a slower, more thorough check (independent agent or human review) for high-stakes outputs, so cheap verification catches obvious errors like the factorial bug while expensive verification catches subtler ones. Deployment consideration: requires triaging which outputs warrant the expensive second stage without reviewing everything at top cost.
3. **Verification-result logging as a first-class artifact**: Store the raw verification output (not just the agent's summary of it) alongside the task result, so misread-result failures are auditable after the fact even if not caught in real time. Deployment consideration: adds storage and pipeline complexity for capturing and retaining raw verification artifacts.

### Metrics
1. **verification_hallucination_rate**: % of "verified" claims without a corresponding logged verification action; target < 1%; alert if > 5%.
2. **post_verification_failure_rate**: % of agent-verified outputs that fail when actually used/tested by the user; target < 3%; alert if > 10%.
3. **result_misinterpretation_rate**: % of sampled verification actions where the raw result contradicts the agent's stated verification conclusion; target < 2%; alert if > 8%.
4. **independent_validator_coverage**: % of high-stakes tasks routed through an independent validator rather than self-verification; target > 90%; alert if < 70%.

### Alerts
1. **Verification Hallucination Detected** (P1): Condition — verification_hallucination_rate exceeds 5% over a rolling week. Action: audit affected task categories, require structured verification tooling before allowing "complete" status, and review recently delivered outputs from that category.
2. **Post-Verification Failure Rate Spike** (P1): Condition — post_verification_failure_rate exceeds 10% for a task category. Action: treat all recent "verified" outputs in that category as unverified pending re-check; investigate the result-comparison logic for misinterpretation bugs.
3. **Result Misinterpretation Pattern Confirmed** (P2): Condition — result_misinterpretation_rate exceeds 8% in spot-check sampling. Action: replace narrative self-verification with structured programmatic comparison for the affected task type.

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Failure modes 3.2 and 3.3: Verification failures (17.3% combined)
- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - Verification gaps in RAG systems
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Quality control failures
