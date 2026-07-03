# Multi-Agent Error Propagation Cascade

## Issue: Single agent error compounds exponentially through multi-agent pipeline; downstream agents treat upstream errors as ground truth, amplifying impact 17x-20x by final output

**Frequency**: Common

**Symptoms**
- First agent makes 5% error in data processing
- Second agent's error rate jumps to 15% (error inherited + compounded)
- Third agent's error rate reaches 50%+ (cascading failures)
- Each agent reports high confidence despite using bad upstream data
- Errors appear to originate from different agents when traced back
- System works perfectly in isolation but fails in sequence
- Disabling one agent improves overall system reliability

**Root Cause**
Agents are chained sequentially; each agent's output becomes next agent's input. When agent A produces output with error E, agent B treats this output as ground truth. If agent B's own processing adds error E, total error is E + E = 2E. By agent D, error has amplified to ~2^N * E. Monolithic pipeline architecture creates tight coupling where upstream errors are invisible to downstream agents; no ability to detect or correct upstream problems.

**Examples**

### Example 1: Data Extraction Pipeline Failure
```
Pipeline:
  Agent A: Extract raw data from PDF → 95% accuracy
  Agent B: Normalize extracted data → 90% accuracy given good input
  Agent C: Deduplicate records → 95% accuracy given good input
  Agent D: Validate against database → 98% accuracy given good input

Cascade:
  Agent A: 1,000 records, 50 errors (5%)
  Agent B: Receives 50 bad records, makes 5 additional errors
           Total: 55 errors (5.5%) → Pass to Agent C
  Agent C: Receives 55 errors, makes 3 additional errors (from 55 bad records)
           Total: 58 errors (5.8%) → Pass to Agent D
  Agent D: Receives 58 errors, makes 1 additional error
           Total: 59 errors (5.9%) → Final output

Expected (if independent): 50 + 50 + 25 + 20 = 145 errors (would be caught)
Actual: Only 59 errors (cascaded but seemed to improve) - FALSE CONFIDENCE

BUT: When Agent A input is corrupted by 50% initially:
  Agent A: 500 errors (50%) instead of 50
  Agent B: 500 bad → Agent B can't normalize; generates another 450 errors
  Agent C: 950 bad → Can't deduplicate; amplifies to 1,400 errors
  Agent D: 1,400 bad → Validation fails on all 1,400

Final output: COMPLETELY CORRUPTED (140% error rate impossible)
Impact: Entire dataset unusable; downstream business logic receives garbage
```

### Example 2: Legal Document Processing Chain
```
Agent A: Extract contract provisions → 92% accuracy
Agent B: Classify provisions by type → 85% accuracy (on good extractions)
Agent C: Extract key terms → 90% accuracy (on correctly classified provisions)
Agent D: Generate summary → 80% accuracy (on correctly extracted terms)

Scenario: Agent A misidentifies "Non-Compete" clause as "Confidentiality"
  Agent A: Passes misclassified clause to Agent B
  Agent B: Applies confidentiality classification rules
           Extracts wrong terms (confidentiality-relevant, not non-compete)
  Agent C: Receives confidentiality terms instead of non-compete terms
           Creates false summary
  Agent D: Generates legal summary based on wrong understanding
           
Final: Document summary is completely wrong; lawyer relies on it
Impact: Legal obligations missed; $2M deal misunderstood
```

### Example 3: Customer Service Escalation Pipeline
```
Agent A: Analyze customer complaint → Classify urgency
Agent B: Route to appropriate team based on Agent A classification
Agent C: Generate response template based on Agent B's routing
Agent D: Personalize response based on Agent C's template

Agent A misclassifies urgent issue as low-priority (5% error)
  Agent B routes to general queue instead of urgent queue
  Agent C uses generic template (appropriate for low-priority)
  Agent D personalizes generic template
  Agent E (human): Never sees urgent issue; customer escalates on social media

Result: High-priority issue becomes P1 incident
Impact: Customer churn, negative publicity
Root cause: Single misclassification cascaded through entire pipeline
```

### Example 4: Supply Chain Optimization with Multi-Agent Failures
```
Agent A: Forecast demand from sales data → 90% accuracy
Agent B: Calculate safety stock based on forecast → Assume forecast is correct
Agent C: Optimize supplier selection based on safety stock → Assume stock correct
Agent D: Schedule shipments based on supplier selection → Assume selection correct

Agent A forecast error: 20% underestimate (actual demand 20% higher)
  Agent B calculates insufficient safety stock (based on underestimate)
  Agent C selects suppliers with smaller batch sizes (assuming demand is lower)
  Agent D schedules more frequent, smaller shipments
  
Actual demand arrives: 20% higher than forecast
  Safety stock depleted faster than expected
  Supplier batches too small; frequent reorders exceed supplier capacity
  Stockout occurs; production halts

Impact: 3-day production shutdown; $5M in lost sales
Root cause: 20% error in Agent A cascaded to 60%+ system dysfunction
```

**Key Statistics**
| Finding | Source |
|---|---|
| Error amplification factor: 17x in 3-agent systems; 20x+ in 4+ agent systems | arXiv:2503.13657 (MAST) |
| Monolithic entanglement: Tightly coupled agents show 80%+ failure rate | arXiv:2503.06789 |
| Error propagation: Each agent stage adds 5-20% additional errors | arXiv:2510.10581 |
| System degrades non-linearly: Adding agents decreases reliability (counterintuitive) | arXiv:2503.13657 |

---


## Test Scenario & Reproduction

### Scenario Setup
- 3+ agent pipeline (Agent A -> B -> C)
- Agent A makes inference error (15% error rate)
- Agent B uses Agent A's output as input
- Error amplifies through pipeline
- No error detection or correction

### Trigger Mechanism
```
1. Agent A processes input, introduces error (15% chance)
2. Agent B receives Agent A's output
3. Agent B's inference compounds error
4. Agent C receives Agent B's output
5. Error cascades: 15% -> 18% -> 22% final error
```

### Expected Failure State
- Errors amplify through pipeline (17x amplification)
- Final error rate dramatically exceeds component error rates
- No detection that components are misaligned
- Compound errors cascade to failure

### Mitigation Validation Protocol
**Test Checklist:**
- [ ] Reproduce: Error cascade through 3 agents
- [ ] Measure: Final error 15%+ of individual errors
- [ ] Apply mitigation (intermediate verification, consensus)
- [ ] Re-run → cascade limited to <2x amplification

**Success Criteria:**
- Error amplification <2x through pipeline
- Intermediate verification catches errors
- Final accuracy acceptable despite component errors

## Mitigation Strategies

1. **Agent-Level Error Detection**
   - Each agent validates its own output before passing to next agent
   - Validation checks: output format, value ranges, schema compliance
   - If validation fails: retry, escalate, or return error (don't pass bad data)
   - Prevents propagation of obviously malformed outputs

2. **Confidence Tracking Through Pipeline**
   - Each agent tags output with confidence score
   - Downstream agent checks confidence before using as premise
   - Low-confidence outputs trigger verification before downstream use
   - Confidence decays with each step (not amplifies)

3. **Error Isolation & Circuit Breaker**
   - Monitor error rate at each agent stage
   - If error rate exceeds threshold (e.g., 25%), halt pipeline
   - Don't pass degraded data downstream; flag for human review
   - Prevent cascade before it amplifies

4. **Upstream Verification Checkpoints**
   - Downstream agents can query upstream agents: "Are you confident in this output?"
   - Upstream agent re-checks its own work
   - Enables feedback loop where downstream questions trigger upstream re-validation
   - Catches upstream errors before they propagate far

5. **Redundancy & Consensus**
   - Run Agent A twice (independent instances), compare outputs
   - Only pass to Agent B if outputs match
   - For mission-critical steps, run 3 times; use majority vote
   - Trade-off: 2-3x compute cost, but prevents single-point failures

6. **Decomposition & Parallelization**
   - Don't chain agents sequentially; run independent paths where possible
   - Only merge results when necessary
   - Reduces error coupling; easier to isolate problems
   - Requires redesigning workflow, but significantly improves robustness

7. **Human Checkpoints at High-Impact Stages**
   - Identify 2-3 critical handoffs in pipeline (highest business impact)
   - Require human review/approval at these stages
   - Human can catch cascading errors before they propagate further
   - Trade-off: Adds latency, reduces automation benefit

### Metrics
- Error amplification factor per stage: error_rate_N / error_rate_N-1
- Cumulative error rate: % of end-to-end incorrect outputs
- Detection rate: % of bad data caught and prevented from propagating
- System reliability: Probability of correct end-to-end output
- Cascade depth: How many stages before error becomes unrecoverable

### Alerts
- Error rate increases >20% in any agent stage → P2 (degradation detected)
- Confidence scores decrease with pipeline depth → P2 (cascade starting)
- Circuit breaker triggers (error rate >threshold) → P1 (halt pipeline)
- Human checkpoint detects upstream error → P1 (downstream impact prevented)

---

## Related Patterns
- [Multi-Agent Collective Reasoning Collapse](./multi-agent-false-consensus-risk.md) — Consensus amplifies errors (related mechanism)
- [Monolithic Agent Entanglement](./multi-agent-monolithic-entanglement.md) — Tight coupling enables error propagation
- [Hallucinated Completion When Upstream Dependency Fails](../../../../../cross-cutting/accuracy/goals/output-accuracy/failures/hallucinated-completion-when-upstream-dependency-fails.md) — Agents hallucinate when upstream data is bad
- [Long-Horizon Goal Drift](../../../../../by-capability/long-horizon-execution/goals/goal-maintenance/failures/long-horizon-goal-drift.md) — Similar cascading mechanism over time

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Core reference; documents 17x error amplification
- [Towards Reliable Multi-Agent LLM Systems: Failure Rates Over 80%](https://arxiv.org/abs/2503.06789) - Production failure rates in multi-agent pipelines
- [GraphTracer: Graph-Guided Failure Tracing in LLM Agents for Robust Multi-Turn Deep Search](https://arxiv.org/abs/2510.10581) - Tracing error propagation through agent graphs
- [AgenTracer: Who Is Inducing Failure in the LLM Agentic Systems?](https://arxiv.org/abs/2509.03312) - Root cause attribution in cascading failures
