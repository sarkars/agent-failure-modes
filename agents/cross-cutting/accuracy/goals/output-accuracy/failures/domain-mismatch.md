# Domain Mismatch

## Issue: Agent Fails on Out-of-Distribution or Specialized Inputs

**Frequency**: Common

**Symptoms**
- Responses remain coherent but align to wrong domain
- Shallow or irrelevant content for specialized queries
- Agent applies general knowledge to domain-specific questions
- Accuracy collapse on real-world inputs vs. benchmarks

**Root Cause**
Agent encounters inputs from unfamiliar or highly specialized domains that differ from its training distribution. While broad pre-training enables general competence, it "presents distinct challenges" when facing novel domains. The agent produces internally coherent responses that are aligned to the wrong domain rather than being obviously incorrect.

**Example**
```
Domain: Industrial chemical processing

User: "What's the optimal residence time for a CSTR 
       with A → B reaction, k=0.05/min, target 95% conversion?"

Agent response:
"For optimal conversion, you should allow sufficient time
for the reaction to complete. Consider monitoring temperature
and pressure to ensure safety. Chemical reactions typically
require careful attention to stoichiometry..."

Problem: 
- Response is coherent but doesn't apply chemical engineering math
- Agent avoided τ = X/(k(1-X)) calculation it doesn't know
- Provided general chemistry advice instead of process engineering

Result: User gets unhelpful generic response, may not realize
        the agent lacks domain expertise
```

**Key Statistics**
From Failure Modes in LLM Systems (arxiv:2511.19933):
- Domain mismatch identified as distinct from hallucination
- Pre-training on broad corpora creates challenges for specialized domains
- Accuracy collapse occurs when real-world inputs differ from benchmark prompts
- Errors manifest as shallow content rather than obvious fabrication

**Mismatch Patterns**
- **Domain confusion**: Agent applies wrong field's knowledge
- **Depth limitation**: Surface-level response to deep technical query
- **Terminology mismatch**: Uses general terms instead of domain-specific ones
- **Method avoidance**: Skips domain-specific calculations or procedures

**Contributing Factors**
- Training data weighted toward general knowledge
- Limited exposure to specialized professional domains
- No mechanism to recognize domain boundaries
- Benchmark tests don't capture domain-specific depth
- Confidence masks lack of expertise

## Mitigation Strategies

### Prevention
1. **Domain-signature detection before generation**: Classify incoming queries for domain-specific markers (technical notation, formula requests, professional terminology like "CSTR," "k=0.05/min") and route flagged queries through a domain-check gate before the agent attempts a general-purpose answer — this catches the chemical-engineering query in the example before the agent substitutes generic chemistry advice for the actual calculation. Trade-off: a domain classifier itself needs training/maintenance and can misclassify borderline queries as general when they're specialized.
2. **Explicit method-completeness check**: Before responding to a query that implies a specific calculation or procedure (like the τ = X/(k(1-X)) residence-time formula), require the agent to either produce the specific method or explicitly declare it cannot, rather than silently substituting general advice — this directly targets "method avoidance" named as a mismatch pattern. Trade-off: adds a self-check step that increases latency and can produce more "I don't know" responses than users expect from a capable-sounding agent.
3. **Domain-specific retrieval requirement**: For queries classified as specialized, require grounding in domain-specific retrieved content (engineering handbooks, process design references) rather than allowing the model to answer from parametric knowledge alone. Trade-off: requires building and maintaining a domain corpus for every specialized field the agent might encounter, which isn't feasible for long-tail domains.

### Detection & Response
1. **Terminology-depth scoring**: Score responses for domain-specific terminology and method usage versus generic language on queries classified as specialized; a coherent-but-generic response to a technical query (as in the example) is directly measurable as a terminology-depth gap.
2. **Method-presence audit**: For query types known to require a specific calculation or procedure, automatically check whether the response contains the expected method markers (formula, named procedure, specific parameters); absence flags a likely domain mismatch even when the response reads fluently.
3. **Expert-sampled domain benchmark review**: Periodically sample agent responses to known specialized-domain queries and have a domain expert score depth and correctness against a benchmark, since fluency masks the failure and generic monitoring won't catch it.

### Architecture Patterns
1. **Domain router to specialized backends**: Route queries classified as domain-specific to a fine-tuned model, domain RAG pipeline, or specialist agent rather than the general-purpose model, so depth-limited responses aren't generated in the first place. Deployment consideration: requires maintaining routing accuracy and specialist backends for each domain the system claims to support.
2. **Confidence-gated hedging on out-of-distribution inputs**: When the router or model signals low domain-fit confidence, force explicit uncertainty language into the response rather than allowing a confidently-coherent-but-wrong answer. Deployment consideration: confidence signals for domain-fit need calibration against real out-of-distribution examples, not just in-distribution validation data.
3. **Domain-specific RAG with method retrieval**: Retrieve not just background text but structured method/formula references for domains where correctness depends on applying a specific technique, so the agent has the τ = X/(k(1-X))-equivalent formula available rather than reasoning from general knowledge. Deployment consideration: structured method retrieval is more expensive to build than plain document RAG and needs domain-expert curation.

### Metrics
1. **domain_mismatch_rate**: % of specialized-domain queries where expert review finds shallow or wrong domain application; target < 5%; alert if > 15%.
2. **method_presence_rate**: % of queries requiring a specific method/formula where the response contains the expected method markers; target > 90%; alert if < 70%.
3. **domain_routing_accuracy**: % of specialized queries correctly routed to a domain-specific backend; target > 95%; alert if < 85%.
4. **user_relevance_complaint_rate**: "Not relevant"/"too general" feedback per 1,000 specialized-domain sessions; target < 10; alert if > 40.

### Alerts
1. **Method Absence on Known-Specialized Query** (P2): Condition — method_presence_rate drops below 70% for a domain category over a rolling week. Action: review the domain router's classification accuracy and the specialist backend's coverage for that category.
2. **Domain Routing Accuracy Drop** (P2): Condition — domain_routing_accuracy falls below 85%. Action: audit recent misrouted queries, retrain or patch the domain classifier, and manually reroute affected sessions if still active.
3. **User Relevance Complaint Spike** (P3): Condition — user_relevance_complaint_rate exceeds 40 per 1,000 sessions for a domain. Action: sample flagged sessions for expert review and prioritize domain-specific RAG or specialist routing for that category.

## References

- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) - Domain mismatch/out-of-distribution failure mode
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Pre-training bias overriding context
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Specialized domain challenges
