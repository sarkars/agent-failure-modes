# What Failures Are Built Into My Industry or Domain?

**Use-case failures originate from *where the agent operates* — the regulatory, business, and user-expectation context of a specific domain.** An agent that handles customer support has different failure modes than one that processes insurance claims, even if both use identical technology. This taxonomy routes you to the domain-specific patterns that matter for your industry.

Use this section when planning for a specific domain:
- **Building a healthcare agent?** → Start with [Healthcare](healthcare/) to understand diagnosis, treatment, and safety-specific failures
- **Shipping a financial-services agent?** → Start with [Financial Services](financial-services/) to handle regulatory compliance, trading bias, and market data failures
- **Processing legal documents?** → Start with [Legal Contracts](legal-contracts/) for jurisdiction, amendment, and compliance patterns
- **Automating support tickets?** → Start with [Support Services](support-services/) for routing, knowledge-base decay, and escalation patterns

## By-Use-Case Categories

| Industry / Domain | Description | Key Risks | Patterns |
|---|---|---|---|
| [Healthcare](healthcare/) | Diagnosis, treatment planning, drug interactions, clinical safety | Patient safety, liability, regulatory compliance, treatment contraindications | 48 |
| [Mortgage Documents](mortgage-documents/) | Document OCR, fraud detection, income verification, compliance validation | Loan qualification errors, fraud, TRID timing, income miscalculation | 62 |
| [Financial Services](financial-services/) | Portfolio analysis, trading, market data, regulatory compliance | Market bias, regulatory breaches, position mismatches, trading errors | 44 |
| [Support Services](support-services/) | Ticket routing, KB freshness, escalation, SLA management | Routing misses, KB staleness, escalation miscalibration, over-automation | 32 |
| [Supply Chain](supply-chain/) | Demand forecasting, supplier risk, inventory optimization | Bullwhip effect, forecast drift, supplier bias, planning cascades | 31 |
| [Legal Contracts](legal-contracts/) | Risk detection, jurisdiction handling, amendment compliance | Missed clauses, jurisdiction traps, regulatory misses, liability exposure | 39 |
| [Content Marketing](content-marketing/) | Engagement prediction, trending topics, SEO, content decay | Trending drift, engagement hallucination, SEO miscalibration, staleness | 23 |
| [HR Recruiting](hr-recruiting/) | Resume screening, candidate assessment, bias detection, culture fit | Screening bias, skill miscalibration, discrimination, undervaluation | 24 |
| [Sales CRM](sales-crm/) | Lead qualification, pipeline forecasting, discount pressure | Qualification gaming, forecast inflation, discount authorization drift | 21 |
| [Insurance](insurance/) | Claims processing, underwriting, fraud detection, reserves | Claims fraud, underwriting conservatism drift, false positives in fraud | 19 |
| [Customer Service](customer-service/) | Conversation resolution, canned-response selection, escalation | Wrong response template, lost context in handoff, escalation misfires | 19 |
| [Agent Interaction](agent-interaction/) | Conversation quality, clarification, tone, multi-turn understanding | Clarification loops, tone miscalibration, context loss, topic drift | 25 |
| [DevOps](devops/) | Monitoring alerts, capacity planning, deployment safety, anomaly detection | Alert fatigue, false positives, unsafe deployments, cascading failures | 39 |

**Total: 427 patterns**

## How to Use This Section

### Scenario: "I'm Building an AI Agent for Healthcare — Where Do I Start?"

1. **Start with your domain** — [Healthcare](healthcare/) has 48 patterns covering diagnosis, treatment planning, drug interactions, and safety-specific failures.
2. **Match your specific function** — Is your agent diagnosing, recommending treatment, or checking drug interactions? Each has distinct failure patterns.
3. **Layer in capability patterns** — Your healthcare agent likely uses [Knowledge Retrieval](../by-capability/knowledge-retrieval/) (medical literature), [Reasoning & Thought](../by-capability/reasoning-and-thought/) (differential diagnosis), or [External Actions](../by-capability/external-actions/) (EHR queries). Check those sections too.
4. **Add cross-cutting foundation** — Layer in [Accuracy](../cross-cutting/accuracy/) (hallucination, knowledge staleness), [Security](../cross-cutting/security/) (patient data protection), and [Operations](../cross-cutting/operations/) (cost, monitoring).

**Result**: You build a compliance-aware, diagnosis-safe, observable healthcare agent.

### Scenario: "We're Building a Mortgage-Processing Agent. What Can Go Wrong?"

1. **Start with domain** — [Mortgage Documents](mortgage-documents/) has 62 patterns covering document OCR, income verification, fraud detection, and compliance.
2. **Identify the sub-domain** — Are you focusing on document OCR (extraction failures), fraud detection (model gaming), income verification (data accuracy), or compliance (TRID timing)?
3. **Layer in capability patterns** — Mortgage processing is heavily [Document Processing](../by-capability/document-processing/) (OCR, layout preservation, multimodal reliability).
4. **Consider regulatory risk** — [Governance](../cross-cutting/governance/) covers compliance auditing and liability.

**Result**: You avoid $10K+ loan-qualification errors and regulatory violations.

### Scenario: "Our Support Agent Keeps Routing Tickets Wrong. What's Happening?"

1. **Start with domain** — [Support Services](support-services/) covers routing misses, KB staleness, and escalation patterns.
2. **Check the pattern** — [Routing mismatch](support-services/) typically involves [Knowledge Retrieval](../by-capability/knowledge-retrieval/) (KB ranking) or [Reasoning & Thought](../by-capability/reasoning-and-thought/) (ticket complexity estimation).
3. **Cross-reference** — [Customer Service](customer-service/) has specific patterns for canned-response selection that may apply to your routing problem.

**Result**: You diagnose whether the issue is KB staleness, ranking algorithm failure, or skill-based routing miscalibration.

## Domain-Specific Routing Guide

**Choose your entry point based on your primary risk:**

| Primary Risk | Entry Point |
|---|---|
| Patient or customer safety | [Healthcare](healthcare/), [Financial Services](financial-services/), [Legal Contracts](legal-contracts/) |
| Regulatory compliance or audit | [Financial Services](financial-services/), [Mortgage Documents](mortgage-documents/), [Legal Contracts](legal-contracts/) |
| Financial loss (fraud, miscalibration) | [Financial Services](financial-services/), [Insurance](insurance/), [Mortgage Documents](mortgage-documents/) |
| Operational efficiency (routing, automation) | [Support Services](support-services/), [HR Recruiting](hr-recruiting/), [Sales CRM](sales-crm/) |
| Content quality or engagement | [Content Marketing](content-marketing/), [Customer Service](customer-service/), [Agent Interaction](agent-interaction/) |
| Supply chain or infrastructure | [Supply Chain](supply-chain/), [DevOps](devops/) |

## Frequently Asked Questions

### How does a use-case failure differ from a capability failure?

A use-case failure is shaped by *domain context, regulations, or business logic*, not just technology.

- **Capability** (Multi-Agent Systems): "Agent handoff drops state between triage and specialist"
- **Use Case** (Support Services): "Handoff between triage and billing agent forgets customer's prior credit, agent re-issues the credit"

The first is a technical problem (handoff schema). The second adds domain context (refund policies, account history) that changes severity and mitigation strategy.

### Should I start with By-Capability or By-Use-Case?

- **Use-Case first** if you're new to the domain and want to understand domain-specific risks before diving into technical architecture.
- **Capability first** if you already know the domain and want to understand technical implementation risks.
- **Cross-Cutting first** if you want to build a foundation that applies everywhere (security, accuracy, operations).

Most teams check all three, but entry order depends on your context.

### Can I use the same mitigation across different domains?

Partially. The technical mitigation might be the same (e.g., "add confidence gating"), but the *threshold* and *context* are domain-specific:

- **Healthcare** — Confidence threshold for diagnosis recommendations is 95%+; false negatives are more costly than false positives.
- **Financial Services** — Confidence threshold for trade execution is 99%+; regulatory penalties justify high thresholds.
- **Customer Service** — Confidence threshold for canned response is 80%; escalation is cheaper than wrong answers.

The pattern applies everywhere; the configuration is domain-specific.

### Do all domains have equal numbers of patterns?

No. Complexity varies by regulatory burden, financial stakes, and multi-step orchestration:

- [Mortgage Documents](mortgage-documents/) (62 patterns) — High regulatory burden, financial stakes, document complexity
- [Healthcare](healthcare/) (48 patterns) — High safety stakes, complex clinical reasoning
- [Financial Services](financial-services/) (44 patterns) — Regulatory compliance, market dynamics, portfolio complexity

Simpler domains may have fewer documented patterns not because they're safer, but because the failure modes are more obvious or less extensively studied.

## Related Categories

- [By Capability](../by-capability/) — Technical/architectural failure patterns that apply across domains
- [Cross-Cutting Patterns](../cross-cutting/) — Security, accuracy, operations patterns that apply everywhere
- [Top-Level Navigation](../) — How to choose between By-Capability, By-Use-Case, and Cross-Cutting taxonomies
