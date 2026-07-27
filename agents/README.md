# How Should I Navigate AI Agent Failure Patterns?

**This repository organizes failure patterns across three taxonomies, each answering a different question about where failures originate.** Whether you're designing an agent, debugging production incidents, or building organizational resilience, start by understanding which taxonomy maps to your problem.

- **By Capability** — Failures driven by *what the system does* (document processing, multi-agent coordination, knowledge retrieval). Use this when the failure arises from a specific technical capability or architectural component.
- **By Use Case** — Failures driven by *where the system operates* (healthcare, financial services, legal contracts). Use this when the failure is domain-specific or shaped by regulatory/business context.
- **Cross-Cutting** — Failures that apply to *all AI systems* (security, accuracy, operations). Use this first as a foundation; every other pattern builds on these.

## Three Taxonomies

| Taxonomy | Answer This Question | Use When | Patterns |
|----------|---------------------|----------|----------|
| [By Capability](by-capability/) | What design or architectural component is failing? | Debugging tech-stack choices: "Why do OCR agents fail?" "How do multi-agent systems misalign?" | 358 |
| [By Use Case](by-use-case/) | What business or regulatory domain creates this failure? | Building for a specific industry: "I'm shipping a healthcare agent—what can go wrong?" "What do support agents miss?" | 521 |
| [Cross-Cutting](cross-cutting/) | What could break in any AI system? | Foundation work: security, accuracy, operations apply to everything. Start here. | 628 |

**Total: ~1,507 patterns across 50+ goals**

## How to Use These Taxonomies

### Scenario: "My Customer-Service Agent Keeps Picking the Wrong Response Template"

1. **By Capability** — This is a *retrieval* failure. Check [Knowledge Retrieval](by-capability/knowledge-retrieval/) for embedding-based matching failures.
2. **By Use Case** — This is a *support-domain* failure. Check [Customer Service](by-use-case/customer-service/) for canned-response selection patterns specific to account state matching.
3. **Cross-Cutting** — Layer in [Accuracy](cross-cutting/accuracy/) for verification strategies and [Operations](cross-cutting/operations/) for monitoring.

**Result**: You find [Embedding Retrieval Selects Similar-but-Wrong Canned Response](by-use-case/customer-service/goals/conversation-resolution/failures/embedding-retrieval-selects-similar-but-wrong-canned-response.md), which ties together retrieval mechanics (capability), support context (use case), and verification architecture (cross-cutting).

### Scenario: "We're Building an OCR Pipeline and Want to Avoid Known Pitfalls"

1. **By Capability** — Start here. [Document Processing](by-capability/document-processing/) covers 6 goals across the OCR pipeline: classification, text extraction, layout preservation, multimodal reliability, orchestration, and production monitoring.
2. **Cross-Cutting** — Layer in [Accuracy](cross-cutting/accuracy/) for evaluation and [Operations](cross-cutting/operations/) for cost and reliability at scale.
3. **By Use Case** — If your OCR serves a specific domain (mortgage documents, legal contracts, healthcare records), check the domain-specific section to find industry-specific failure patterns not captured in generic OCR.

### Scenario: "Security Audit—What Can Go Wrong?"

1. **Cross-Cutting** — Start with [Security](cross-cutting/security/). All AI systems need to cover safety, runtime protection, data loss prevention, and trust.
2. **By Capability** — If your agent runs externals actions (database writes, API calls), check [External Actions](by-capability/external-actions/).
3. **By Use Case** — If you handle regulated data (financial, healthcare, legal), review the domain section for compliance-specific threats.

## Pattern Structure

Every failure pattern across all three taxonomies follows the same template:

| Section | What It Tells You |
|---------|-------------------|
| **Issue** | One-line description of the failure |
| **Symptoms** | Observable signs that this failure is happening |
| **Root Cause** | Why this failure occurs at a technical level |
| **Example** | Concrete scenario showing the failure in action |
| **Eval Recipes** | Test cases and metrics to catch the failure before production |
| **Mitigation Strategies** | Prevention, detection, and response approaches |
| **Production Signals** | Metrics, alerts, and dashboards to catch the failure in real-time |

## Related Resources

- [Contributing](../CONTRIBUTING.md) — Add new failure patterns to this repository
- [REFERENCES.md](../REFERENCES.md) — Academic research, incident databases, regulatory guidance
- [Published Knowledge Base](https://agent-kb-autopublish.vercel.app/) — Browse all patterns online
