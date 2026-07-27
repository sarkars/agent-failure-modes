# What Failures Are Built Into My Agent's Design?

**Capability-based failures originate from *how the agent is architected* — the technical components and design decisions you make.** Whether you're building a retrieval-augmented agent, a multi-step planner, or a system that processes documents, your architectural choices introduce specific failure modes. This taxonomy routes you to those design-driven patterns.

Use this section when debugging production issues:
- **Text extraction is returning garbled characters?** → Check [Document Processing](document-processing/)
- **Agent forgets context after a few exchanges?** → Check [Knowledge Retrieval](knowledge-retrieval/) and [Reasoning & Thought](reasoning-and-thought/)
- **Two agents coordinate but keep issuing conflicting commands?** → Check [Multi-Agent Systems](multi-agent-systems/)
- **External API calls sometimes succeed and sometimes silently fail?** → Check [External Actions](external-actions/)
- **Speech-based agent misunderstands accented speech at scale?** → Check [Speech & Audio](speech-and-audio/)

## By-Capability Categories

| Capability | Description | Focus | Patterns |
|------------|-------------|-------|----------|
| [Document Processing](document-processing/) | OCR, text extraction, layout preservation, multimodal reliability | Character accuracy, field hallucination, structure loss, production drift | 53 |
| [Knowledge Retrieval](knowledge-retrieval/) | RAG, embedding-based retrieval, context management, relevance ranking | Context precision, false positives, semantic drift, knowledge staleness | 82 |
| [Speech & Audio](speech-and-audio/) | Speech recognition, synthesis, accent handling, interruption detection | ASR errors, audio quality degradation, accent bias, context in voice | 71 |
| [Vision & Images](vision-and-images/) | Image understanding, object detection, multimodal reasoning | Confidence miscalibration, adversarial robustness, hallucination in vision | 49 |
| [Reasoning & Thought](reasoning-and-thought/) | Step-by-step reasoning, chain-of-thought, thought verification | Circular reasoning, reasoning shortcuts, backtracking failures | 31 |
| [Task Planning](task-planning/) | Goal decomposition, subtask ordering, prerequisite handling | Bad decomposition, missing prerequisites, plan abandonment | 23 |
| [Multi-Agent Systems](multi-agent-systems/) | Agent coordination, handoff reliability, message passing, role clarity | Agent misalignment, context loss in handoff, conflicting objectives | 23 |
| [Domain Expertise](domain-expertise/) | Domain-specific judgment, regulation compliance, context-aware decision-making | Regulatory misses, domain hallucination, compliance gaps | 12 |
| [External Actions](external-actions/) | External system calls, API execution, state mutation, rollback handling | Wrong target selection, no rollback, transaction failures, race conditions | 13 |

**Total: 357 patterns**

## How to Use This Section

### Step 1: Match Your Symptom to a Capability

**Symptom: "Agent keeps asking for the same information the user already provided"**  
→ This is a [Knowledge Retrieval](knowledge-retrieval/) failure. The agent's context management or retrieval ranking is losing relevance. See [Context Overflow](knowledge-retrieval/goals/) patterns.

**Symptom: "Extracted document fields are correct individually but don't make sense together"**  
→ This is a [Document Processing](document-processing/) + [Reasoning & Thought](reasoning-and-thought/) failure. The extraction pipeline succeeds at individual fields, but reasoning over multiple fields fails. See [Agentic Orchestration](document-processing/goals/agentic-orchestration/).

**Symptom: "Agent sends a command to System A, then System B doesn't know what happened"**  
→ This is a [Multi-Agent Systems](multi-agent-systems/) failure. The handoff schema is losing state. See coordination and communication patterns.

### Step 2: Understand the Design Trade-offs

Each capability makes architectural choices that introduce risk:

- **RAG systems** trade memory for knowledge freshness but introduce retrieval failures (semantic drift, ranking inversions).
- **Speech agents** trade real-time responsiveness for accuracy (interruption handling, accent adaptation).
- **Multi-agent systems** trade modularity for coordination overhead (state loss, misalignment).
- **Document pipelines** trade speed for accuracy (confidence-gated review, validation checkpoints).

Understanding these trade-offs helps you decide which failure patterns matter most for your use case.

### Step 3: Layer with Cross-Cutting Patterns

Every capability-based failure also involves cross-cutting concerns:

- **Accuracy** — Can I verify the output is correct? (Document Processing needs [Output Verification](../cross-cutting/accuracy/))
- **Operations** — Can I detect and respond when this fails at scale? (Multi-Agent Systems needs [Cost Efficiency](../cross-cutting/operations/))
- **Security** — Can an attacker exploit this capability? (External Actions needs [Runtime Security](../cross-cutting/security/))

## Frequently Asked Questions

### How is a capability-based failure different from a use-case failure?

A capability-based failure is driven by the *technical component*, not the *domain*. 

- **Capability** (Document Processing): "Vision-language models hallucinate field values when table structure is ambiguous"
- **Use Case** (Mortgage Documents): "Hallucinated income field causes loan qualification to approve an unqualified applicant"

Both patterns exist. The first helps you design the extraction pipeline; the second helps you assess downstream risk in a specific domain.

### Which capability should a developer check first?

1. If the agent **retrieves external knowledge** (documents, databases, web) → Start with [Knowledge Retrieval](knowledge-retrieval/)
2. If the agent **processes unstructured input** (documents, speech, images) → Start with [Document Processing](document-processing/), [Speech & Audio](speech-and-audio/), or [Vision & Images](vision-and-images/)
3. If the agent **coordinates with other agents or systems** → Start with [Multi-Agent Systems](multi-agent-systems/) or [External Actions](external-actions/)
4. If the agent **reasons over multiple steps** → Start with [Reasoning & Thought](reasoning-and-thought/) and [Task Planning](task-planning/)

### Is a better model the answer for capability failures?

Rarely. Most capability failures are architectural, not model-capability problems:

- **Document Processing** — A stronger VLM reduces hallucination but doesn't add validation checkpoints or confidence-gating
- **Knowledge Retrieval** — A better embedding model reduces some ranking failures but doesn't solve context overflow
- **Multi-Agent Systems** — A smarter agent can't fix a handoff schema that loses state

Upgrade the model after you've solved the architectural failures, not before.

## Related Categories

- [Cross-Cutting Patterns](../cross-cutting/) — Security, accuracy, operations patterns that apply to all capabilities
- [By Use Case](../by-use-case/) — Domain-specific failures that layer on top of capability patterns
- [Top-Level Navigation](../) — How to choose between By-Capability, By-Use-Case, and Cross-Cutting taxonomies
