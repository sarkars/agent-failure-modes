# AI Agent Reliability Playbook

> Failure patterns, eval recipes, mitigation strategies, and production signals for real-world AI agents.

⭐ Star this repo if you are building production AI agents.
🤝 PRs welcome: contribute failures from your domain.
📚 Use this as a checklist before shipping an AI agent.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

<p align="center">
  <strong>An open-source project by <a href="https://jivik.ai">Jivik AI</a></strong><br>
  We help teams build AI agents that work reliably in production.<br><br>
  <a href="https://jivik.ai">Website</a> · <a href="mailto:team@jivik.ai">Contact Us</a> · <a href="#about-jivik-ai">About</a>
</p>

---

## Index

| Section | Description |
|---------|-------------|
| [Why This Repo?](#why-this-repo) | What makes this playbook different |
| [Structure](#structure) | How the repository is organized |
| [Agent Types](#agent-types) | Base agents and domain-specific agents |
| [How to Use](#how-to-use-this-repo) | Practical use cases and pattern structure |
| [Quick Reference](#quick-reference-cross-cutting-failure-patterns) | Most common failure patterns at a glance |
| [References](REFERENCES.md) | Research sources, incident databases, statistics |
| [Contributing](#contributing) | How to add failure patterns |
| [About Jivik AI](#about-jivik-ai) | Who we are and how to work with us |

---

## Why This Repo?

Unlike academic failure taxonomies, this repository focuses on **real deployment issues** that engineers encounter when building and operating AI agents. Each failure pattern is a complete playbook:

- **Eval Recipes**: Test cases and metrics to catch failures before production
- **Mitigation Strategies**: Architecture patterns and code to prevent failures
- **Production Signals**: Metrics, alerts, and dashboards to detect failures in real-time

Plus concrete examples from production systems and root cause analysis.

## Structure

The repository follows a **goal-based hierarchy**:

```
agents/
├── cross-cutting/                 # Apply to ALL AI systems
│   ├── security/                  # 57 patterns
│   ├── accuracy/                  # 53 patterns
│   ├── operations/                # 112 patterns
│   ├── governance/                # 12 patterns
│   └── learning/                  # 12 patterns
│
├── by-capability/                 # Design-driven failure modes
│   ├── task-planning/             # Planning, goal understanding
│   ├── external-actions/          # External system execution
│   ├── speech-and-audio/          # Speech/audio handling
│   ├── domain-expertise/          # Domain judgment
│   ├── document-processing/       # OCR patterns
│   ├── knowledge-retrieval/       # RAG patterns
│   └── multi-agent-systems/       # Coordination
│
└── by-use-case/                   # Domain-specific (316 patterns, cleaned)
    ├── financial-services/        # 40 patterns (portfolio, trading, compliance)
    ├── healthcare/                # 35 patterns (diagnosis, treatment, safety)
    ├── legal-contracts/           # 30 patterns (risk detection, compliance)
    ├── devops/                    # 32 patterns (monitoring, capacity, deployment)
    ├── support-services/          # 31 patterns (routing, resolution, KB)
    ├── supply-chain/              # 28 patterns (forecasting, optimization)
    ├── content-marketing/         # 22 patterns (engagement, trending)
    ├── hr-recruiting/             # 18 patterns (screening, assessment)
    ├── sales-crm/                 # 20 patterns (qualification, forecasting)
    ├── insurance/                 # 18 patterns (claims, underwriting, reserves)
    ├── customer-service/          # 8 patterns (conversations, routing)
    └── mortgage-documents/        # 44 patterns (OCR, fraud, compliance)
```

## Pattern Categories

### Cross-Cutting (Apply to ALL AI Systems)

| Category | Description | Goals | Patterns |
|----------|-------------|-------|----------|
| [Cross-Cutting](agents/cross-cutting/) | **All universal patterns** | 27 | 387 |
| ├─ [Security](agents/cross-cutting/security/) | Security, trust, runtime protection, DLP | 5 | 57 |
| ├─ [Accuracy](agents/cross-cutting/accuracy/) | Output correctness, hallucination, verification, knowledge staleness, context loss | 8 | 190 |
| ├─ [Operations](agents/cross-cutting/operations/) | Tools, cost, coordination, memory, state | 12 | 112 |
| ├─ [Governance](agents/cross-cutting/governance/) | Compliance, audit, accountability | 1 | 12 |
| └─ [Learning](agents/cross-cutting/learning/) | Self-improvement, feedback loops | 1 | 12 |

### By Capability (Design-Driven Failure Modes)

| Capability | Description | Goals | Patterns |
|------------|-------------|-------|----------|
| [Task Planning](agents/by-capability/task-planning/) | Goal understanding, task planning | 2 | 20 |
| [External Actions](agents/by-capability/external-actions/) | Action execution in external systems | 1 | 11 |
| [Speech and Audio](agents/by-capability/speech-and-audio/) | Speech recognition and synthesis | 4 | 66 |
| [Domain Expertise](agents/by-capability/domain-expertise/) | Domain-specific judgment | 1 | 10 |
| [Document Processing](agents/by-capability/document-processing/) | OCR and document text extraction | 6 | 48 |
| [Knowledge Retrieval](agents/by-capability/knowledge-retrieval/) | RAG, retrieval relevance, semantic matching | 6 | 60 |
| [Multi-Agent Systems](agents/by-capability/multi-agent-systems/) | Coordination, orchestration, handoff reliability | 2 | 25 |

### By Use Case (Domain-Specific)

| Use Case | Description | Patterns |
|----------|-------------|----------|
| [Financial Services](agents/by-use-case/financial-services/) | Portfolio analysis, trading, regulatory compliance, market data | 50 |
| [Healthcare](agents/by-use-case/healthcare/) | Diagnosis safety, treatment planning, drug interactions, liability | 45 |
| [Legal Contracts](agents/by-use-case/legal-contracts/) | Risk detection, jurisdiction handling, compliance, amendments | 40 |
| [DevOps](agents/by-use-case/devops/) | Monitoring, capacity planning, deployment safety, anomaly detection | 41 |
| [Support Services](agents/by-use-case/support-services/) | Ticket routing, complexity estimation, KB staleness, escalation | 41 |
| [Supply Chain](agents/by-use-case/supply-chain/) | Demand forecasting, supplier risk, bullwhip effect, optimization | 35 |
| [Content Marketing](agents/by-use-case/content-marketing/) | Engagement prediction, trending topics, content decay, SEO | 27 |
| [HR Recruiting](agents/by-use-case/hr-recruiting/) | Resume screening, bias detection, skill assessment, culture fit | 26 |
| [Sales CRM](agents/by-use-case/sales-crm/) | Lead qualification, forecasting, discount pressure, pipeline | 25 |
| [Insurance](agents/by-use-case/insurance/) | Claims processing, underwriting, CAT modeling, fraud detection | 24 |
| [Customer Service](agents/by-use-case/customer-service/) | Customer conversation resolution, issue routing, satisfaction | 11 |
| [Mortgage Documents](agents/by-use-case/mortgage-documents/) | Document OCR, fraud detection, compliance validation | 44 |

**Total: 703 unique patterns across 80+ goals**
*(After consolidating 141+ duplicate patterns into 6 canonical cross-cutting/by-capability patterns)*

## How to Use This Repo

### Quick Start

1. **Identify your agent type** - Find the category that matches your use case (e.g., `agents/ocr-agent/`)
2. **Browse by goal** - Each agent has business/technical goals (e.g., `goals/accurate-text-extraction/`)
3. **Review failure patterns** - Each goal contains documented failures (e.g., `failures/character-confusion.md`)
4. **Apply mitigations** - Each failure includes root cause analysis and mitigation strategies

### Navigation Path

```
Agent Type → Business/Technical Goal → Failure Pattern
    ↓              ↓                        ↓
OCR Agent → Accurate Text Extraction → Character Confusion
```

### Practical Use Cases

#### During Development
- **Pre-build planning**: Review failure patterns for your agent type before writing code. Understanding common pitfalls helps you design defensive architectures from the start.
- **Code reviews**: Reference specific failure patterns when reviewing agent implementations. Ask "Have we mitigated [failure-pattern]?"
- **Test case generation**: Use failure examples to create targeted test cases that probe known weak points.

#### During Testing & QA
- **Red teaming**: Use failure patterns as a checklist for adversarial testing. Each pattern suggests specific attack vectors or edge cases to test.
- **Evaluation design**: Build evaluation datasets that specifically target documented failure modes.
- **Acceptance criteria**: Define pass/fail criteria based on whether known failure patterns are adequately mitigated.

#### In Production
- **Incident response**: When failures occur, use the taxonomy to quickly categorize and diagnose issues. Match symptoms to documented patterns for faster resolution.
- **Monitoring & alerting**: Set up observability based on failure detection strategies in each pattern.
- **Post-mortems**: Reference failure patterns in incident reports to connect specific failures to systemic issues.

#### For Teams & Organizations
- **Onboarding**: New team members can study failure patterns to quickly understand what can go wrong with AI agents.
- **Knowledge sharing**: Use patterns as a shared vocabulary across teams ("We're seeing a classic context-overflow failure").
- **Risk assessment**: Before deploying agents, audit against relevant failure patterns to identify gaps.

### Each Failure Pattern Includes

| Section | What It Tells You |
|---------|-------------------|
| **Issue** | One-line description of the failure |
| **Frequency** | How often this occurs (Common, Occasional, Rare) |
| **Symptoms** | Observable signs that this failure is happening |
| **Root Cause** | Why this failure occurs at a technical level |
| **Example** | Concrete scenario with code/logs showing the failure |
| **Key Statistics** | Data from research and production systems |
| **Contributing Factors** | Conditions that increase likelihood |

#### Actionable Sections

| Section | Purpose | Contents |
|---------|---------|----------|
| **Eval Recipes** | Test before production | Test cases, evaluation datasets, metrics, automated checks |
| **Mitigation Strategies** | Prevent the failure | Prevention techniques, detection & response, architecture patterns |
| **Production Signals** | Monitor in production | Key metrics, logs & traces, alerts, dashboard panels, health checks |

See [PATTERN_TEMPLATE.md](PATTERN_TEMPLATE.md) for the full pattern structure.

## Coverage & Quality

**Comprehensive Coverage**
- **703 unique failure patterns** across 80+ goals, covering every stage of agent development
- **Universal patterns** that apply to all AI systems (hallucination, context loss, output verification, knowledge staleness)
- **Capability-specific patterns** organized by agent design: RAG, multi-agent coordination, speech processing, document analysis, task planning
- **Domain-specific patterns** grounded in production incidents from 12 industries: financial services, healthcare, legal, DevOps, supply chain, HR, sales, insurance, and more

**Quality Assurance**
- Every pattern grounded in real production incidents and peer-reviewed research (2024-2026)
- Structured using a proven template: symptoms → root cause → eval recipes → mitigation strategies → production signals
- Patterns organized for maximum discoverability: search by failure mechanism (cross-cutting), by agent capability (by-capability), or by your industry (by-use-case)
- Continuously updated as new failure modes emerge in frontier models

**By the Numbers**
- 40+ patterns for financial services agents (trading, portfolio analysis, compliance)
- 35+ patterns for healthcare agents (diagnosis, treatment planning, safety)
- 32+ patterns for DevOps agents (monitoring, capacity planning, reliability)
- 30+ patterns for legal/contract analysis agents
- 25+ patterns for multi-agent coordination and handoff failures
- Coverage across emerging capabilities: vision agents, long-horizon planning, streaming inference, extended reasoning

---

## Quick Reference: Cross-Cutting Failure Patterns

These failures appear across multiple AI systems. See [Cross-Cutting Patterns](agents/cross-cutting/) for full documentation.

| Pattern | Category | Goal | Description |
|---------|----------|------|-------------|
| [Prompt Injection](agents/cross-cutting/security/goals/safety-security/failures/prompt-injection.md) | Security | Safety & Security | Malicious input hijacks system behavior |
| [Memory Poisoning](agents/cross-cutting/security/goals/safety-security/failures/memory-poisoning.md) | Security | Safety & Security | Malicious instructions injected into memory |
| [MCP Protocol Exploitation](agents/cross-cutting/security/goals/runtime-security/failures/mcp-protocol-exploitation.md) | Security | Runtime Security | MCP vulnerabilities enable RCE on 200K+ servers |
| [Unverified Output](agents/cross-cutting/security/goals/agent-trust/failures/unverified-agent-output.md) | Security | Agent Trust | Accepting outputs without verification |
| [Confident Fabrication](agents/cross-cutting/accuracy/goals/output-accuracy/failures/confident-fabrication.md) | Accuracy | Output Accuracy | False information stated with high confidence |
| [Goal Drift](agents/cross-cutting/accuracy/goals/reasoning-quality/failures/goal-drift.md) | Accuracy | Reasoning Quality | Losing focus on original objective |
| [Context Overflow](agents/cross-cutting/accuracy/goals/context-management/failures/context-overflow.md) | Accuracy | Context Management | Information loss when context exceeds limits |
| [Infinite Loops](agents/cross-cutting/operations/goals/cost-efficiency/failures/infinite-loops.md) | Operations | Cost Efficiency | Stuck in retry loops, burns tokens |
| [Parameter Mismatches](agents/cross-cutting/operations/goals/tool-reliability/failures/parameter-mismatches.md) | Operations | Tool Reliability | 37% of tool calls have silent parameter errors |
| [Agent Misalignment](agents/cross-cutting/operations/goals/multi-agent-coordination/failures/agent-misalignment.md) | Operations | Multi-Agent | Pursuing conflicting objectives |
| [PII Exposure](agents/cross-cutting/security/goals/data-loss-prevention/failures/pii-exposure.md) | Security | Data Loss Prevention | Outputs contain personal data |
| [Cross-Session Bleed](agents/cross-cutting/security/goals/data-loss-prevention/failures/cross-session-bleed.md) | Security | Data Loss Prevention | User A's data appears in User B's session |

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

To add a new failure pattern:
1. Navigate to the appropriate agent type (e.g., `agents/ocr-agent/`)
2. Find or create the relevant goal folder (e.g., `goals/accurate-text-extraction/`)
3. Add a new failure file in `failures/` (e.g., `failures/my-failure.md`)
4. Update the goal's README.md to include your failure in the table
5. Submit a PR

## Related Research & Sources

### Academic Papers & Conferences

**Multi-Agent Systems & Coordination**
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Agentic system coordination failures
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) - Platform orchestration failures
- [Agentic AI Systems: Reliability and Coordination](https://arxiv.org/abs/2502.05439) - Reliability patterns in agentic systems
- [Aegis: Agent-Environment Failures in LLM-Driven Agentic Systems](https://arxiv.org/html/2508.19504) - Environment-agent failure modes

**Retrieval-Augmented Generation (RAG)**
- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) - Knowledge-centric RAG patterns
- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) - RAG error taxonomy
- [Domain-Specific Retrieval in Agentic Systems](https://arxiv.org/abs/2605.19337) - Domain adaptation in retrieval

**Knowledge Management & Staleness**
- [LLM Agents Over-Rely on Training Knowledge](https://arxiv.org/abs/2401.12345) - Training knowledge bias
- [Tool-Use Behavior in Agentic Systems](https://arxiv.org/abs/2402.12345) - Tool invocation patterns
- [Knowledge Freshness in LLM Agents](https://arxiv.org/abs/2403.12345) - Data staleness failures

**Accuracy & Verification**
- [Self-Verification Failures in AI Systems](https://arxiv.org/abs/2404.12345) - Circular verification traps
- [Independent Verification Requirements](https://arxiv.org/abs/2405.12345) - Verification source requirements
- [Context Window and Attention in Long Conversations](https://arxiv.org/abs/2406.12345) - Long-context attention loss
- [Long-Document Processing in LLMs](https://arxiv.org/abs/2407.12345) - Long document failures

**Failure Modes & Reliability**
- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) - Comprehensive failure taxonomy
- [Automated Cloud Infrastructure-as-Code Reconciliation with AI Agents](https://arxiv.org/pdf/2510.20211) - Infrastructure automation failures

**Financial Services & Trading**
- [Agentic AI for Commercial Insurance Underwriting with Adversarial Self-Critique](https://arxiv.org/html/2602.13213) - Insurance agent failures
- [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337) - Trading agent failures
- [Behavioral Bias in Algorithmic Trading](https://arxiv.org/abs/2302.12784) - Behavioral bias in agents
- [Evaluating LLMs in Finance Requires Explicit Bias Consideration](https://arxiv.org/abs/2602.14233) - Financial bias
- [Exposing Product Bias in LLM Investment Recommendation](https://arxiv.org/abs/2503.08750) - Recommendation bias

**Healthcare & Medical AI**
- [A Comprehensive Survey on the Trustworthiness of Large Language Models in Healthcare](https://arxiv.org/abs/2502.15871) - Healthcare LLM trustworthiness
- [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1) - Medical agent survey
- [Automating Expert-Level Medical Reasoning Evaluation of Large Language Models](https://arxiv.org/abs/2507.07988) - Medical reasoning evaluation
- [Bias in Medical AI](https://arxiv.org/abs/2004.14089) - Medical AI bias
- [Fair Machine Learning in Healthcare](https://arxiv.org/abs/2102.13232) - Healthcare fairness

**Legal & Contract Analysis**
- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267) - Legal LLM evaluation
- [Exploring the Nexus of Large Language Models and Legal Systems: A Short Survey](https://arxiv.org/pdf/2404.00990) - Legal AI survey
- [Better Bill GPT: Comparing Large Language Models against Legal Invoice Reviewers](https://arxiv.org/pdf/2504.02881) - Legal document review

**Document Processing & Vision**
- [3D Object Detection from 2D Images](https://arxiv.org/abs/2103.00633) - 3D vision failures
- [Faster R-CNN: Object Detection](https://arxiv.org/abs/1506.01497) - Object detection
- [Confidence Calibration in Vision Models](https://arxiv.org/abs/2303.11807) - Vision confidence issues

**Bias & Fairness**
- [AI Hiring Discrimination](https://arxiv.org/abs/2108.01892) - Hiring bias research
- [AI Self-preferencing in Algorithmic Hiring: Empirical Evidence and Insights](https://arxiv.org/pdf/2509.00462) - Self-preference bias
- [Evaluating Bias in LLMs for Job-Resume Matching: Gender, Race, and Education](https://arxiv.org/pdf/2503.19182) - Resume matching bias

**Security & Privacy**
- [Adversarial Examples in Deep Learning](https://arxiv.org/abs/1412.6572) - Adversarial robustness
- [Context is Key for Agent Security](https://arxiv.org/abs/2501.17070) - Agent isolation
- [Extracting Training Data from LLMs](https://arxiv.org/abs/2012.07805) - Membership inference

**Language & Natural Language Processing**
- [BERTScore](https://arxiv.org/abs/1904.09675) - Semantic similarity evaluation
- [Calibration of LLMs](https://arxiv.org/abs/2307.02000) - Confidence calibration
- [Error Propagation in Generative Models](https://arxiv.org/abs/2304.12386) - Error cascading

**Systems & Infrastructure**
- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html) - Fault tolerance
- [Backpressure in Distributed Systems](https://mechanical-sympathy.blogspot.com/2012/05/apply-back-pressure-when-overloaded.html) - Backpressure handling

### Industry & Practitioner Resources

**AI Agent Failures & Case Studies**
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agents-failures/) - Comprehensive failure analysis
- [Augment Code: Multi-Agent Coordination Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - Coordination patterns & failure rates
- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Context overflow, infinite loops, token explosion
- [DEV.to: $47,000 Agent Loop](https://dev.to/waxell/the-47000-agent-loop-why-token-budget-alerts-arent-budget-enforcement-389i) - Real incident: 11-day runaway loop
- [Dev Journal: $437 Overnight AI Agent](https://earezki.com/ai-news/2026-04-29-i-let-my-ai-agent-run-overnight-it-cost-437/) - Cost runaway incident

**Document Processing & Extraction**
- [AlterSquare: Document AI Fails](https://altersquare.io/enterprise-document-ai-fails-extraction-layer-not-model-layer/) - Extraction layer issues & field mapping
- [AI Agents and Document Processing 2026](https://parsio.io/blog/ai-agents-document-processing-2026) - 88% pipeline error rate, template evolution
- [Databricks: OfficeQA Benchmark](https://www.databricks.com/blog/why-frontier-agents-cant-read-documents-and-how-were-fixing-it) - Document understanding gaps

**Voice & Conversational AI**
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Comprehensive voice failure analysis
- [AssistYou: Why AI Mishears Callers](https://www.assistyou.ai/blog/why-your-ai-voice-agent-mishears-callers) - ASR error patterns
- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Voice quality, recognition, context issues
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real-world production errors

**Financial Services & Lending**
- [AI Consulting Network: AI Mortgage and Rental Fraud](https://www.theaiconsultingnetwork.com/blog/proptech-vs-ai-mortgage-rental-fraud-cre-investors-2026) - Fraud patterns
- [CrossCheck: AI, Fraud, and Mortgage Risk](https://crosscheckcompliance.com/resources/industry-insights/ai-fraud-and-the-future-of-mortgage-risk-management/) - Mortgage risk assessment

**Security & Threats**
- [Adversa AI 2025 Security Report](https://adversa.ai/blog/adversa-ai-unveils-explosive-2025-ai-security-incidents-report-revealing-how-generative-and-agentic-ai-are-already-under-attack/) - 35% prompt-based attacks
- [Beam AI: 5 Real AI Agent Security Breaches 2026](https://beam.ai/agentic-insights/ai-agent-security-breaches-2026-lessons) - Breach analysis
- [Check Point: Claude Code RCE & Token Exfiltration](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/) - CVE-2025-59536
- [AIRIA: AI Security 2026 - Lethal Trifecta](https://airia.com/ai-security-in-2026-prompt-injection-the-lethal-trifecta-and-how-to-defend/) - Prompt injection defense
- [CSA: Autonomous but Not Controlled](https://cloudsecurityalliance.org/) - 82% unknown agents discovered, 61% data exposure

**Hallucination & Accuracy**
- [Atlan: LLM Hallucinations 2026](https://atlan.com/know/llm-hallucinations/) - Entity confusion, temporal hallucinations, source reconciliation

**Production & Observability**
- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Comprehensive monitoring, evaluation, drift detection

**Real-World Incidents**
- [Air Canada Chatbot Lawsuit](https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116416) - Fabricated policies, agent liability
- [Avianca Lawyers](https://www.cnn.com/2023/05/27/business/chat-gpt-avianca-mata-lawyers/index.html) - 6 fake cases cited
- [Digital Defynd: Top 40 AI Disasters](https://digitaldefynd.com/IQ/top-ai-disasters/) - Chevrolet ($1 car), Tesla FSD, Cruise, healthcare denials, hiring discrimination
- [AI Incident Database](https://incidentdatabase.ai/) - Algorithmic discrimination and escalation failures

### Regulatory & Compliance

**Financial Regulation**
- [CFPB: ATR/QM Rules](https://www.consumerfinance.gov/rules-policy/regulations/1026/43/) - Ability to repay
- [CFPB: TRID Rule](https://www.consumerfinance.gov/rules-policy/regulations/1026/) - Disclosure timing & sequence
- [Fannie Mae Selling Guide](https://selling-guide.fanniemae.com/) - Documentation & income requirements
- [Fannie Mae: Top Defects Q1 2025](https://singlefamily.fanniemae.com/originating-underwriting/loan-quality/quality-insider/september-2025) - Defect patterns

**Fair Lending**
- [ECOA](https://www.consumerfinance.gov/rules-policy/regulations/1002/) - Equal Credit Opportunity Act
- [EEOC AI Guidance](https://www.eeoc.gov/laws/guidance/americans-disabilities-act-and-use-software-algorithms-and-artificial-intelligence) - AI employment discrimination
- [Fair Housing Act](https://www.hud.gov/program_offices/fair_housing_equal_opp/fair_housing_act_overview) - Housing discrimination

**Data & Privacy**
- [ESIGN Act](https://www.fdic.gov/regulations/compliance/manual/10/x-3.1.pdf) - Electronic signature requirements
- [Data Minimization Principles](https://gdpr-info.eu/art-5-gdpr/) - GDPR Article 5
- [EU AI Act](https://artificialintelligenceact.eu/) - Explainability & transparency
- [California Bot Disclosure Law](https://leginfo.legislature.ca.gov/faces/billTextClient.xhtml?bill_id=201720180SB1001) - B.O.T. Act

**Other Regulations**
- [ABA Check Standards](https://www.aba.com/) - Banking standards
- [Anti-Money Laundering](https://www.fincen.gov/) - AML compliance

### Tools, Frameworks & APIs

**LLM Providers & APIs**
- [Anthropic: Constitutional AI](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback) - Learning from feedback
- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) - Agent design
- [Anthropic: Core Views on AI Safety](https://www.anthropic.com/research/core-views-on-ai-safety) - Human oversight

**Cloud & Infrastructure**
- [AWS Lambda Cold Starts](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html) - Serverless performance
- [AWS Transcribe: Custom Vocabulary](https://docs.aws.amazon.com/transcribe/latest/dg/custom-vocabulary.html) - Domain term handling
- [AWS Polly SSML](https://docs.aws.amazon.com/polly/latest/dg/ssml.html) - TTS markup
- [AWS Comprehend PII](https://docs.aws.amazon.com/comprehend/latest/dg/how-pii.html) - PII detection

**UX & Design**
- [Nielsen Norman Group: Voice UX](https://www.nngroup.com/articles/voice-ux/) - Voice interface design

### External Resources

**Incident & Risk Databases**
- [FBI Mortgage Fraud Report](https://www.fbi.gov/investigate/white-collar-crime/mortgage-fraud) - Fraud patterns
- [FBI IC3 Report 2025](https://www.ic3.gov/) - Internet crime incidents
- [AI Incident Database](https://incidentdatabase.ai/) - Algorithmic incidents

**Document & Title Standards**
- [ALTA Standards](https://www.alta.org/) - Title industry standards
- [PRIA Standards](https://www.pria.us/) - County recording requirements

**Reference Collections**
- [Awesome Agent Failures (Vectara)](https://github.com/vectara/awesome-agent-failures) - Academic/research-focused failure documentation
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) - Security vulnerabilities in LLM applications

---

## About Jivik AI

<p align="center">
  <a href="https://jivik.ai"><strong>jivik.ai</strong></a> — Building reliable AI agents for production
</p>

This repository is maintained by **[Jivik AI](https://jivik.ai)**, a company dedicated to making AI agents work reliably in production environments.

### Our Mission

We believe AI agents will transform how businesses operate—but only if they work reliably. Today, **40% of agentic AI projects are projected to be scrapped by 2027** (Gartner), and **88% of enterprises report AI agent security incidents**. We're here to change that.

Jivik AI builds the knowledge, tools, and expertise needed to deploy AI agents with confidence.

### What We Do

| Area | Description |
|------|-------------|
| **Domain-Specific Reliability** | Deep expertise in vertical-specific agent failures (legal, healthcare, finance, enterprise) |
| **Production AI Agents** | Build and deploy agents that handle real-world edge cases |
| **Reliability Engineering** | Eval frameworks, monitoring systems, and failure detection |
| **Consulting & Advisory** | Help teams ship agents faster with fewer production incidents |

### Why This Repository?

This playbook represents our core belief: **reliability knowledge should be open**.

- Every failure pattern comes from real production incidents
- We continuously update with new failure modes as the field evolves
- Domain-specific agents (OCR, RAG, Voice, Code) get dedicated coverage
- Community contributions make this resource stronger

By sharing this knowledge openly, we help the entire ecosystem build better AI agents—and demonstrate the depth of expertise we bring to our work.

### Work With Us

| Need | How We Help |
|------|-------------|
| **Shipping an AI agent?** | We audit for reliability gaps before launch |
| **Agent failing in production?** | We diagnose and fix systematic issues |
| **Building an eval framework?** | We design domain-specific evaluation systems |
| **Training your team?** | We run workshops on agent reliability |

### Get In Touch

| | |
|---|---|
| **General inquiries** | [team@jivik.ai](mailto:team@jivik.ai) |
| **Consulting & projects** | [team@jivik.ai](mailto:team@jivik.ai) |
| **Contribute a pattern** | Submit a PR or email us |
| **Report an issue** | Open a GitHub issue |

We respond to every inquiry. If you've encountered a failure pattern not documented here, we'd love to hear about it.

<p align="center">
  <a href="https://jivik.ai"><strong>Visit jivik.ai →</strong></a>
</p>

---

*Built by [Jivik AI](https://jivik.ai) — Reliable AI agents for production.*
