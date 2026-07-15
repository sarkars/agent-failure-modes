# Communication Breakdown

## Issue: Information Lost or Corrupted Between Agents

**Frequency**: Common

**Symptoms**
- Downstream agent missing context from upstream
- Agent outputs based on incomplete information
- Repeated requests for already-provided information
- Inconsistent understanding across agents

**Root Cause**
When agents communicate through natural language or structured messages, information can be lost due to summarization, misinterpretation, or context window limitations. Each agent-to-agent handoff is an opportunity for information degradation.

**Example**
```
Research Agent: Finds 10 relevant papers, summarizes key findings
               Includes important caveat: "Results only valid for datasets > 1M rows"

Summary Agent: Condenses research into bullet points
              Caveat omitted for brevity

Decision Agent: Recommends approach based on summary
               Applied to 10K row dataset

Result: Invalid recommendation due to lost caveat
```

**Information Loss Points**
- **Summarization**: Details lost when condensing information
- **Context truncation**: Earlier context dropped for new input
- **Format conversion**: Structure lost in text serialization
- **Semantic drift**: Meaning shifts through paraphrasing
- **Priority filtering**: Agent drops "unimportant" details

**Potential Effects**
- Decisions made on incomplete information
- Important caveats or warnings lost
- Duplicated work due to lost state
- Cascading errors through agent chain

## Mitigation Strategies

### Prevention
1. **Structured message schemas with required constraint fields**: The caveat "Results only valid for datasets > 1M rows" was dropped because it traveled as free-text prose that the Summary Agent judged prunable. Replace natural-language handoffs with a schema that has a dedicated, non-optional `constraints`/`caveats` field the summarizer cannot omit without explicitly setting it to null. Trade-off: schema design requires anticipating which fields matter, and rigid schemas can force awkward representation of genuinely unstructured findings.
2. **Critical-information flags that survive summarization**: Mark specific facts (like the dataset-size caveat) as "must-preserve" at the point of origin (Research Agent), and have downstream summarization steps treat flagged content as a lossless pass-through rather than candidate-for-condensation text. Trade-off: overuse of "critical" flags on too much content defeats the purpose of summarization and bloats every downstream message.
3. **Compression verification step after each summarization hop**: Before the Summary Agent's output replaces the Research Agent's full findings, run an automated check (e.g., "does the summary retain all flagged facts?") and reject/re-summarize if a flagged fact is missing — this would have caught the dropped caveat before it reached the Decision Agent. Trade-off: adds a verification LLM call at every hop, increasing latency and cost proportional to chain length.

### Detection & Response
1. **Flagged-fact presence check at final output**: Since the failure here is a specific caveat present at the source but absent at the end, diff the set of flagged critical facts at origin against what's present in the final Decision Agent output, and treat any drop as a hard failure, not a quality nit.
2. **Decision-precondition mismatch monitor**: The Decision Agent recommended an approach that implicitly assumed the >1M row precondition without knowing it. Track cases where a downstream agent's recommendation depends on a numeric/categorical precondition and verify that precondition was explicitly present in the input it received, not just in the original source content.
3. **Repeated-request signal**: If a downstream agent (e.g., Decision Agent) asks a question already answered upstream (e.g., "what's the data scale?"), that is a direct signal information was lost in the Summary Agent hop — log and count these re-asks per pipeline stage.

### Architecture Patterns
1. **Provenance-chain metadata attached to every message**: Carry an immutable pointer from each summarized fact back to its full-fidelity source (Research Agent's original finding) so the Decision Agent can pull the un-summarized caveat on demand rather than trusting the lossy intermediate. Deployment consideration: requires a retrievable store (not just in-context text) for source artifacts, adding storage/retrieval infrastructure.
2. **Dedicated shared memory for constraints, separate from the narrative message flow**: Instead of relying on the caveat surviving inside prose that gets condensed, write applicability constraints (dataset size, valid ranges, etc.) to a separate structured store that every downstream agent queries independently of the summarized narrative. Deployment consideration: introduces a second source of truth that must be kept in sync with the narrative pipeline.
3. **Bidirectional confirmation handshake between adjacent agents**: Before Decision Agent acts on the Summary Agent's output, require it to restate the constraints it believes apply and have the Summary Agent (or a validator) confirm/correct that restatement — catching the missing caveat at the handoff boundary. Deployment consideration: adds a round-trip per hop; only worth it for chains where downstream errors are costly (e.g., a real recommendation vs. exploratory research).

### Metrics
1. **critical_fact_retention_rate**: Target > 99% of flagged must-preserve facts present verbatim in final output; Alert if < 95% over a rolling 100-task window.
2. **summarization_hop_fidelity**: Target > 95% semantic overlap (via fact-extraction diff) between pre- and post-summarization content for flagged sections; Alert if any single hop drops below 85%.
3. **downstream_re-ask_rate**: Target < 2% of tasks where a downstream agent requests information already provided upstream; Alert if > 8%.
4. **chain_length_vs_quality_correlation**: Target no statistically significant negative correlation between agent-chain length and output quality score; Alert if correlation coefficient exceeds -0.3.

### Alerts
1. **Flagged Caveat Dropped** (P1): Condition - a must-preserve constraint present in an upstream agent's output is absent from a downstream agent's input or final output. Action: block the downstream decision, re-inject the constraint from the provenance chain, and re-run the affected step.
2. **Precondition-Free Recommendation** (P1): Condition - a decision-making agent issues a recommendation whose validity depends on a numeric/categorical constraint not traceable in its received input. Action: halt output delivery and require explicit constraint verification before the recommendation is surfaced to the user.
3. **Repeated Information Request** (P3): Condition - a downstream agent asks for data already supplied by an upstream agent within the same task. Action: log the handoff stage as lossy, surface for pipeline review, and consider it a candidate for a critical-information flag going forward.

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Communication as failure category
- [Redis: Why Multi-Agent LLM Systems Fail](https://redis.io/blog/why-multi-agent-llm-systems-fail/) - Coordination breakdowns
- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Context overflow patterns
