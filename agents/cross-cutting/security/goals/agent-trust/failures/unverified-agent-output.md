# Unverified Agent Output

## Issue: Agents Accept Other Agents' Outputs Without Verification

**Frequency**: Very Common

**Symptoms**
- Errors from one agent propagate through entire system
- Hallucinations amplified across agent chain
- No detection of incorrect intermediate results
- Final output contains compounded errors
- System confidently returns wrong answers

**Root Cause**
In multi-agent systems, downstream agents typically accept upstream agent outputs as ground truth. When Agent A passes results to Agent B, Agent B processes them without independent verification. If Agent A hallucinates, makes errors, or is compromised, these errors propagate unchallenged through the entire agent chain, often amplifying at each step.

**Example**
```
Research Agent System:

Agent A (Researcher):
  Task: "Find the market cap of TechCorp"
  Output: "$450 billion" (HALLUCINATED - actual is $45 billion)

Agent B (Analyst):
  Receives: "$450 billion market cap"
  Task: "Compare to competitors"
  Output: "TechCorp is 10x larger than its nearest competitor"
  (Compounds the error with confident analysis)

Agent C (Writer):
  Receives: "10x larger than competitors"
  Task: "Write investment summary"
  Output: "TechCorp dominates the market with unprecedented scale,
           making it a must-buy for any tech portfolio..."
  (Error now buried in persuasive narrative)

Final output: Completely wrong investment advice
Error source: Invisible to end user
Each agent trusted the previous agent's output implicitly
```

**Key Statistics**
From Multi-Agent Research (2026):
- 21.30% of multi-agent failures from verification gaps (MAST)
- Independent judge agents improve accuracy 7x (PwC)
- STRATUS multi-agent SRE improved mitigation 1.5x with validation agents
- Error amplification increases with agent chain length
- Most systems have zero inter-agent verification

**Trust Patterns**
| Pattern | Risk | Prevalence |
|---------|------|------------|
| Direct passthrough | High | Very Common |
| Format validation only | Medium | Common |
| Semantic validation | Low | Rare |
| Independent verification | Very Low | Very Rare |
| Cross-agent consensus | Very Low | Rare |

**Contributing Factors**
- Agents designed to "be helpful" and accept input
- Verification adds latency and cost
- No standard inter-agent verification protocols
- Downstream agents lack context to verify
- System assumes all agents are correct

## Test Scenario & Reproduction

### Scenario Setup
- Deploy a three-agent research pipeline (Researcher -> Analyst -> Writer) producing investment summaries, with each agent accepting the prior agent's output as ground truth and no independent verifier agent inserted at any boundary
- No cross-reference validation checks factual claims (e.g., market cap figures) against an authoritative financial data source
- No confidence-decay mechanism propagates uncertainty across the chain
- Researcher is known to occasionally hallucinate numeric figures under ambiguous prompts

### Trigger Mechanism
1. Researcher is asked for TechCorp's market cap and hallucinates "$450 billion" (actual: $45 billion), stating it with full confidence and no verification
2. Analyst receives the figure as ground truth and derives a comparative claim ("10x larger than its nearest competitor") without independently checking the underlying number
3. Writer drafts an investment summary asserting TechCorp "dominates the market," burying the original numeric error inside persuasive narrative
4. The final summary is delivered to an end user with no indication any figure was unverified

### Example Reproduction Steps
```
1. Task: "Find the market cap of TechCorp" -> Researcher output:
   "$450 billion" (actual: $45 billion)
2. Task: "Compare to competitors" -> Analyst output, using the
   unverified $450B figure: "TechCorp is 10x larger than its nearest
   competitor"
3. Task: "Write investment summary" -> Writer output: "TechCorp
   dominates the market with unprecedented scale, making it a
   must-buy for any tech portfolio..."
4. Cross-check the $450 billion figure against an authoritative
   financial data source (e.g., a market-data API) -> confirms actual
   value is $45 billion, a 10x discrepancy
5. Check whether any pipeline stage flagged the figure for
   verification -> none did
```

### Expected Failure State
An end user receives confident, persuasive investment advice built on a market-cap figure that is off by 10x, with no verification step anywhere in the chain having caught or flagged the discrepancy. A correctly defended pipeline either cross-references the market-cap claim against an authoritative source before Analyst uses it, or inserts an independent verifier agent between Researcher and Analyst that catches the hallucinated figure before it can compound through the rest of the chain.

## Mitigation Strategies

### Prevention
1. **Dedicated independent verifier agents at key chain boundaries**: Insert a separate verifier agent (with no stake in producing a "successful-looking" answer) between hallucination-prone stages, specifically tasked with checking outputs against authoritative sources rather than assuming upstream correctness — research shown to improve accuracy roughly 7x in some studies. Trade-off: adds a verification stage to every chain, increasing latency and cost, and the verifier agent itself can still miss errors or be fooled by confidently-stated wrong information.
2. **Cross-reference validation against authoritative external sources**: For factual claims that matter downstream (market cap, financial figures, dates), require verification against an authoritative source (financial data API, database of record) rather than accepting an upstream agent's claim as ground truth, since this is the specific class of error (hallucinated figures) shown to compound catastrophically through agent chains. Trade-off: requires access to and integration with authoritative sources for every fact type that needs checking, which isn't available for all claim types.
3. **Confidence propagation with decay across the chain**: Require each agent to pass along not just its output but a confidence/certainty signal, and decay that confidence at each hop (reflecting compounding uncertainty), so by the time a claim reaches the final output stage, low cumulative confidence triggers review rather than the claim being stated with the same unwarranted certainty as the original hallucination. Trade-off: requires every agent in the chain to participate in confidence reporting and decay logic consistently, and confidence scores from LLMs are themselves often miscalibrated (see [[confidence-miscalibration]]).

### Detection & Response
1. **Per-boundary error rate tracking**: Instrument each agent-to-agent hand-off with error-rate tracking (using periodic ground-truth spot checks), since this reveals which specific stage in the chain introduces or amplifies errors, rather than only measuring end-to-end output quality where the source is invisible.
2. **Known-bad-input propagation testing**: Regularly inject known-incorrect information at an early stage of the chain (in a test/staging environment) and verify whether downstream agents catch, question, or blindly propagate/amplify it, directly measuring the system's actual verification behavior rather than assuming verification steps work as designed.
3. **Confidence-without-verification flagging**: Flag any final output presenting high confidence/certainty on a claim that never passed through an independent verification or cross-reference check, since this combination (confident + unverified) is exactly the pattern that produces convincing wrong answers like the TechCorp market-cap example.

### Architecture Patterns
1. **Verify-then-propagate chain architecture**: Architect multi-agent chains so no agent's output is considered final/trustworthy for downstream consumption until it has passed through an independent verification stage, making verification a required chain segment rather than an optional add-on.
2. **Consensus-required facts for high-stakes chains**: For chains producing high-stakes output (investment advice, medical information, compliance determinations), require multiple independent agents to agree on key facts before they're used in the final synthesis, rather than a single linear pipeline where one agent's error becomes unquestioned input to the next.
3. **Human checkpoint insertion at critical junctures**: Insert mandatory human review points before high-consequence chain outputs are finalized/acted upon, positioned specifically at the junctures where compounding error risk is highest (e.g., before financial figures flow from research into persuasive narrative).

### Metrics
1. **per_boundary_error_introduction_rate**: Target: < 2% per agent-to-agent hand-off (via spot-check); Alert if any boundary exceeds 8%
2. **verification_coverage_rate**: Target: 100% of high-stakes claims pass through independent verification before final output; Alert on any bypass
3. **confidence_without_verification_rate**: Target: 0% of final outputs present unverified claims with high confidence; Alert on any occurrence
4. **known_bad_input_catch_rate**: Target: > 95% of injected known-bad test inputs are caught/flagged before reaching final output; Alert if < 80%

### Alerts
1. **Verification Bypass on High-Stakes Output** (P1): Condition - a high-stakes final output (financial, medical, compliance) reaches production without passing through the required independent verification stage. Action: Hold the output, route for verification/human review before release, investigate how the required stage was bypassed.
2. **Boundary Error Rate Spike** (P2): Condition - error-introduction rate at a specific agent-to-agent boundary exceeds 8%. Action: Investigate that specific agent for a regression (model change, prompt change) and add a targeted verification check at that boundary.
3. **Known-Bad-Input Test Failure** (P1): Condition - a scheduled known-bad-input propagation test shows the chain failed to catch/flag the injected error. Action: Treat as a confirmed verification-gap regression; block deployment of the current chain configuration until the gap is fixed.

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - 21.30% verification gap failures
- [AugmentCode: Multi-Agent Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - Independent validation patterns
- [Redis: Why Multi-Agent Systems Fail](https://redis.io/blog/why-multi-agent-llm-systems-fail/) - Error propagation analysis
- [STRATUS Multi-Agent SRE](https://arxiv.org/abs/) - Validation agent improvements
