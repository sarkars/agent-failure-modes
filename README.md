# AI Agent Reliability Playbook

> Failure patterns, eval recipes, mitigation strategies, and production signals for real-world AI agents.

⭐ Star this repo if you are building production AI agents.
🤝 PRs welcome: contribute failures from your domain.
📚 Use this as a checklist before shipping an AI agent.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

<p align="center">
  <strong>An open-source project by <a href="https://saralabs.ai">SaraLabs.ai</a></strong><br>
  We help teams build AI agents that work reliably in production.<br><br>
  <a href="https://saralabs.ai">Website</a> · <a href="mailto:team@saralabs.ai">Contact Us</a> · <a href="#about-saralabsai">About</a>
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
| [Research Sources](#research-sources--references) | Academic papers, incident databases, industry reports |
| [Recent Sources](#recent-sources-feb-may-2026) | Latest 2026 incidents and research |
| [Contributing](#contributing) | How to add failure patterns |
| [About SaraLabs.ai](#about-saralabsai) | Who we are and how to work with us |

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
└── <agent-type>/
    ├── README.md                    # Agent overview
    └── goals/
        └── <business-or-technical-goal>/
            ├── README.md            # Goal description
            └── failures/
                └── <failure-pattern>.md  # Individual failure pattern
```

### Example: Structure

```
agents/
├── base-agent/                    # Cross-cutting (apply to all agents)
│   ├── security-agent/
│   │   └── goals/
│   │       ├── safety-security/
│   │       ├── runtime-security/
│   │       ├── agent-trust/
│   │       ├── data-loss-prevention/
│   │       └── security-autonomy/
│   ├── accuracy-agent/
│   ├── operations-agent/
│   ├── governance-agent/
│   └── learning-agent/
│
└── domain-agents/                 # Domain-specific agents
    ├── workflow-agent/
    ├── rag-agent/
    ├── ocr-agent/
    │   └── goals/
    │       ├── accurate-text-extraction/
    │       ├── layout-preservation/
    │       └── ...
    ├── voice-agent/
    └── ...
```

## Agent Types

### Base Agent (Cross-Cutting Patterns - Apply to ALL Agent Types)

| Agent | Description | Goals | Patterns |
|-------|-------------|-------|----------|
| [Base Agent](agents/base-agent/) | **All cross-cutting patterns** | 24 | 246 |
| ├─ [Security Agent](agents/base-agent/security-agent/) | Security, trust, runtime protection, DLP | 5 | 57 |
| ├─ [Accuracy Agent](agents/base-agent/accuracy-agent/) | Output correctness, evaluation, verification | 5 | 53 |
| ├─ [Operations Agent](agents/base-agent/operations-agent/) | Tools, cost, coordination, memory, state | 12 | 112 |
| ├─ [Governance Agent](agents/base-agent/governance-agent/) | Compliance, audit, accountability | 1 | 12 |
| └─ [Learning Agent](agents/base-agent/learning-agent/) | Self-improvement, feedback loops | 1 | 12 |

### Domain-Specific Agents

| Agent | Description | Goals | Patterns |
|-------|-------------|-------|----------|
| [Workflow Agent](agents/domain-agents/workflow-agent/) | Goal understanding, task planning | 2 | 20 |
| [Action Agent](agents/domain-agents/action-agent/) | Action execution in external systems | 1 | 11 |
| [Customer Service Agent](agents/domain-agents/customer-service-agent/) | Customer conversation resolution | 1 | 11 |
| [Domain Expert Agent](agents/domain-agents/domain-agent/) | Domain-specific judgment | 1 | 10 |
| [Multi-Agent System](agents/domain-agents/multi-agent/) | Agent coordination and orchestration | 1 | 15 |
| [RAG Agent](agents/domain-agents/rag-agent/) | Retrieval-augmented generation | 5 | 52 |
| [OCR Agent](agents/domain-agents/ocr-agent/) | Document text extraction | 6 | 48 |
| [Voice Agent](agents/domain-agents/voice-agent/) | Speech recognition and synthesis | 4 | 26 |
| [Code Agent](agents/domain-agents/code-agent/) | Code generation and review | - | Planned |
| [Data Extraction Agent](agents/domain-agents/data-extraction-agent/) | Structured data extraction | - | Planned |

**Total: 439 patterns across 45 goals**

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

## Quick Reference: Cross-Cutting Failure Patterns

These failures appear across multiple agent types. See [Base Agent](agents/base-agent/) for full documentation.

| Pattern | Agent | Goal | Description |
|---------|-------|------|-------------|
| [Prompt Injection](agents/base-agent/security-agent/goals/safety-security/failures/prompt-injection.md) | Security | Safety & Security | Malicious input hijacks agent behavior |
| [Memory Poisoning](agents/base-agent/security-agent/goals/safety-security/failures/memory-poisoning.md) | Security | Safety & Security | Malicious instructions injected into agent memory |
| [MCP Protocol Exploitation](agents/base-agent/security-agent/goals/runtime-security/failures/mcp-protocol-exploitation.md) | Security | Runtime Security | MCP vulnerabilities enable RCE on 200K+ servers |
| [Unverified Agent Output](agents/base-agent/security-agent/goals/agent-trust/failures/unverified-agent-output.md) | Security | Agent Trust | Agents accept other agents' outputs without verification |
| [Confident Fabrication](agents/base-agent/accuracy-agent/goals/output-accuracy/failures/confident-fabrication.md) | Accuracy | Output Accuracy | Agent states false information with high confidence |
| [Goal Drift](agents/base-agent/accuracy-agent/goals/reasoning-quality/failures/goal-drift.md) | Accuracy | Reasoning Quality | Agent loses focus on original objective |
| [Context Overflow](agents/base-agent/accuracy-agent/goals/context-management/failures/context-overflow.md) | Accuracy | Context Management | Agent loses information when context exceeds limits |
| [Infinite Loops](agents/base-agent/operations-agent/goals/cost-efficiency/failures/infinite-loops.md) | Operations | Cost Efficiency | Agent gets stuck in retry loops, burns tokens |
| [Parameter Mismatches](agents/base-agent/operations-agent/goals/tool-reliability/failures/parameter-mismatches.md) | Operations | Tool Reliability | 37% of tool calls have silent parameter errors |
| [Agent Misalignment](agents/base-agent/operations-agent/goals/multi-agent-coordination/failures/agent-misalignment.md) | Operations | Multi-Agent | Agents pursue conflicting objectives |
| [PII Exposure](agents/base-agent/security-agent/goals/data-loss-prevention/failures/pii-exposure.md) | Security | Data Loss Prevention | Agent outputs contain personal data |
| [Cross-Session Bleed](agents/base-agent/security-agent/goals/data-loss-prevention/failures/cross-session-bleed.md) | Security | Data Loss Prevention | User A's data appears in User B's session |

## Research Sources & References

### Incident Databases

| Source | Description |
|--------|-------------|
| [AI Incident Database (AIID)](https://incidentdatabase.ai/) | 3,000+ documented real-world AI failures, open-source |
| [MIT AI Incident Tracker](https://airisk.mit.edu/ai-incident-tracker) | 1,400+ incidents classified by risk, cause, harm, severity |
| [Museum of Failure - AI Exhibits](https://museumoffailure.com/exhibition/air-canada-ai-chat) | Curated AI failure case studies |

### Academic Research

| Paper | Key Contribution |
|-------|------------------|
| [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) | 1600+ annotated traces, 14 failure modes across 7 MAS frameworks |
| [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) | Red team analysis of memory poisoning, bias, action isolation |
| [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) | 142 traces, 6 failure modes, system-for-agent design paradigm |
| [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) | 15 hidden failure modes from system-engineering perspective |
| [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) | Legal AI tools hallucinate 17-33% despite RAG |
| [Why AI Agents Fail (AREP Framework)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6572478) | 40+ sources, 7 practitioner recommendations |

### Industry Analysis

| Source | Coverage |
|--------|----------|
| [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) | Field analysis of production failures |
| [Adversa AI 2025 Security Report](https://adversa.ai/blog/adversa-ai-unveils-explosive-2025-ai-security-incidents-report-revealing-how-generative-and-agentic-ai-are-already-under-attack/) | AI security incidents and attack patterns |
| [Responsible AI Labs: AI Safety 2024](https://responsibleailabs.ai/knowledge-hub/articles/ai-safety-incidents-2024) | Lessons from real-world failures |
| [Digital Defynd: Top 40 AI Disasters](https://digitaldefynd.com/IQ/top-ai-disasters/) | Detailed analysis of major AI failures |

### Notable Incident Case Studies

#### Infrastructure Failures
- [PocketOS Database Wipe](https://dev.to/alessandro_pignati/the-9-second-disaster-how-an-ai-agent-wiped-a-production-database-p56) - Claude agent deleted production DB in 9 seconds
- [Replit Rogue Agent](https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident/) - Agent ran DROP TABLE, created fake users to cover tracks

#### Customer Service Failures
- [Air Canada Chatbot Lawsuit](https://www.cbc.ca/news/canada/british-columbia/air-canada-chatbot-lawsuit-1.7116416) - Invented bereavement fare policy, company held liable
- [DPD Chatbot](https://www.theregister.com/2024/01/23/dpd_chatbot_goes_rogue/) - Swore, wrote poem calling itself "worst delivery company"
- [NYC MyCity Chatbot](https://www.cxtoday.com/contact-center/3-times-customer-chatbots-went-rogue-and-the-lessons-we-need-to-learn/) - Advised businesses to break laws
- [McDonald's AI Drive-Thru](https://www.cnbc.com/2024/06/17/mcdonalds-to-end-ibm-ai-drive-thru-test.html) - Ordered 260 chicken nuggets, added bacon to ice cream
- [Chevy Tahoe $1 Deal](https://medium.com/cut-the-saas/chatbot-case-study-purchasing-a-chevrolet-tahoe-for-1-fc3a51ab2561) - Chatbot agreed to legally binding $1 price

#### Legal Domain Failures
- [Avianca Lawyers](https://www.cnn.com/2023/05/27/business/chat-gpt-avianca-mata-lawyers/index.html) - Submitted brief with 6 fake ChatGPT-generated cases, fined $5K

### Agent-Type Specific Resources

#### RAG Agents
- [Mindee: RAG Hallucinations Explained](https://www.mindee.com/blog/rag-hallucinations-explained) - Causes, risks, and fixes
- [RAGAS Fails 83% of Time](https://medium.com/data-science-collective/air-canada-lost-a-lawsuit-because-their-rag-hallucinated-yours-will-too-b92b6b9a4d39) - Benchmark results
- [Self-Healing RAG Layer](https://towardsdatascience.com/rag-hallucinates-i-built-a-self-healing-layer-that-fixes-it-in-real-time/) - Real-time hallucination fixes
- [RAGAS Documentation](https://docs.ragas.io/) - RAG evaluation framework and metrics
- [RAGAS Context Precision](https://docs.ragas.io/en/latest/concepts/metrics/context_precision.html) - Retrieval ranking quality metric
- [RAGAS Noise Sensitivity](https://docs.ragas.io/en/latest/concepts/metrics/noise_sensitivity.html) - Irrelevant context impact measurement
- [RAGAS Answer Relevancy](https://docs.ragas.io/en/latest/concepts/metrics/answer_relevance.html) - Query-answer alignment metric
- [RAGAS Faithfulness](https://docs.ragas.io/en/latest/concepts/metrics/faithfulness.html) - Grounding verification metric
- [Lost in the Middle](https://arxiv.org/abs/2307.03172) - Position attention bias in long context
- [HyDE Paper](https://arxiv.org/abs/2212.10496) - Hypothetical document embedding risks
- [LongLLMLingua](https://arxiv.org/abs/2310.06839) - Query-aware context compression

#### Voice Agents
- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Common issues and fixes
- [AppInventiv: 8 Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Why AI voice agents fail
- [Bluejay: 7 Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Voice agents in production
- [AssistYou: Mishearing Callers](https://www.assistyou.ai/blog/why-your-ai-voice-agent-mishears-callers) - ASR accuracy issues
- [Stanford: Racial Disparities in ASR](https://www.pnas.org/doi/10.1073/pnas.1915768117) - Accent bias in speech recognition
- [W3C SSML Specification](https://www.w3.org/TR/speech-synthesis11/) - Speech synthesis markup standard
- [Google Cloud Speech: Custom Vocabulary](https://cloud.google.com/speech-to-text/docs/speech-adaptation) - ASR customization
- [AWS Transcribe: Custom Vocabulary](https://docs.aws.amazon.com/transcribe/latest/dg/custom-vocabulary.html) - Domain term handling

#### Code Agents
- [Cursor vs Claude Code vs Copilot](https://levelup.gitconnected.com/cursor-vs-claude-code-vs-copilot-i-spent-500-testing-all-three-on-real-production-code-c57f97607d36) - Production testing comparison
- [15 AI Coding Agents Ranked](https://www.morphllm.com/ai-coding-agent) - Only 3 changed how teams ship

#### OCR/Document Agents
- [AlterSquare: Document AI Fails](https://altersquare.io/enterprise-document-ai-fails-extraction-layer-not-model-layer/) - Extraction layer failures
- [OCR vs IDP](https://forage.ai/blog/ocr-vs-idp/) - Why traditional OCR fails
- [Why AI OCR Fails](https://parseur.com/blog/why-ai-ocr-fail) - Common OCR failure patterns
- [Why OCR Alone Fails in Real-World Documents](https://dev.to/jakemiller/why-ocr-alone-fails-in-real-world-documents-5f86) - Production failure patterns
- [Why OCR Is the Weakest Part of Document AI](https://medium.com/@manalisomani099/why-ocr-is-the-weakest-part-of-most-document-ai-systems-c9188381d1b9) - System-level analysis
- [IDP Accuracy Reckoning 2026](https://idp-software.com/news/idp-accuracy-reckoning-2026/) - Practitioner perspectives on OCR, agents, tables
- [IDP Challenges 2026](https://idp-software.com/guides/idp-challenges-2026/) - Table extraction as hardest unsolved problem

#### Multimodal/VLM Document Processing
- [Hallucination of Multimodal LLMs Survey](https://arxiv.org/html/2404.18930v2) - Object, attribute, relational hallucination types
- [Mitigating OCR Hallucinations in MLLMs](https://arxiv.org/html/2506.20168v2) - NeurIPS 2025 research on visual degradation
- [Why LLMs Hallucinate More on Enterprise Documents](https://www.adlibsoftware.com/news/why-llms-hallucinate-more-on-enterprise-documents) - Input quality gap analysis
- [Evaluating Multimodal LLMs for Production](https://galileo.ai/blog/multimodal-llm-guide-evaluation) - Production reliability metrics
- [VLMs for Spreadsheet Understanding](https://arxiv.org/html/2405.16234v1) - Cell omission and spatial perception issues
- [Table Extraction Using LLMs](https://nanonets.com/blog/table-extraction-using-llms-unlocking-structured-data-from-documents/) - Merged cells, complex layouts

#### Agentic Document Processing
- [Why Frontier Agents Can't Read Documents](https://www.databricks.com/blog/why-frontier-agents-cant-read-documents-and-how-were-fixing-it) - OfficeQA benchmark, <50% accuracy
- [AI Agents and Document Processing 2026](https://parsio.io/blog/ai-agents-document-processing-2026) - What's actually changing
- [Agentic Document Processing](https://www.llamaindex.ai/blog/agentic-document-processing) - How AI agents automate workflows
- [Document AI: Next Evolution of IDP](https://www.llamaindex.ai/blog/document-ai-the-next-evolution-of-intelligent-document-processing) - Agentic OCR and workflows
- [Production-Ready AI Agent for Document Extraction](https://www.stackai.com/insights/how-to-build-a-production-ready-ai-agent-for-document-data-extraction) - Error handling, validation gates

#### Tool/Workflow Agents
- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Context overflow, timeouts, loops
- [MCP Tool Design](https://dev.to/aws-heroes/mcp-tool-design-why-your-ai-agent-is-failing-and-how-to-fix-it-40fc) - Why agents fail with MCP
- [Silent Tool-Call Errors](https://www.roborhythms.com/fix-ai-agent-tool-call-errors/) - 37% of calls have parameter mismatches
- [5 MCP Server Mistakes](https://dev.to/thedailyagent/5-mcp-server-mistakes-that-waste-your-ai-agents-time-and-how-to-fix-them-18m5) - Common MCP mistakes
- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html) - Fault tolerance for tool calls
- [MCP Protocol](https://modelcontextprotocol.io/) - Tool protocol standardization

#### Multi-Agent Orchestration
- [MAST Taxonomy](https://arxiv.org/abs/2503.13657) - Multi-agent failure modes (36.94% coordination failures)
- [Redis: Multi-Agent Systems Fail](https://redis.io/blog/why-multi-agent-llm-systems-fail/) - Coordination patterns
- [Augment Code: Multi-Agent Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - 41-86.7% failure rates

#### Agent Runtime Security
- [OX Security: Mother of All AI Supply Chains](https://www.ox.security/blog/the-mother-of-all-ai-supply-chains-critical-systemic-vulnerability-at-the-core-of-the-mcp/) - Critical MCP vulnerability affecting 150M+ downloads
- [SecurityWeek: Claude OAuth Token Theft via MCP Hijacking](https://www.securityweek.com/claude-code-oauth-tokens-can-be-stolen-through-stealthy-mcp-hijacking/) - Silent OAuth token interception (April 2026)
- [Check Point: Claude Code RCE & Token Exfiltration](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/) - CVE-2025-59536, CVE-2026-21852
- [Microsoft: Prompts Become Shells](https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/) - RCE in AI frameworks (CVE-2026-25592)
- [VentureBeat: Comment and Control Attack](https://venturebeat.com/security/ai-agent-runtime-security-system-card-audit-comment-and-control-2026) - Three AI coding agents leaked secrets via single injection
- [IBM: OpenClaw Agentic AI Vulnerabilities](https://www.ibm.com/think/x-force/agentic-ai-growing-fast-vulnerabilities) - ClawJacked indirect prompt injection
- [Foresiet: AI Security Incidents April 2026](https://foresiet.com/blog/ai-security-incidents-attack-paths-april-2026/) - 6 incidents with full attack paths
- [NSA: Careful Adoption of Agentic AI](https://media.defense.gov/2026/Apr/30/2003922823/-1/-1/0/CAREFUL%20ADOPTION%20OF%20AGENTIC%20AI%20SERVICES_FINAL.PDF) - Government guidance on agent control

### Key Statistics

| Finding | Source |
|---------|--------|
| AI safety incidents: 149 (2023) → 233 (2024), 56.4% increase | Stanford AI Index 2025 |
| GenAI involved in 70% of incidents | Stanford AI Index 2025 |
| Legal RAG tools hallucinate 17-33% | Stanford Study |
| RAGAS fails on 83% of production cases | Benchmark Study |
| 37% of tool calls have silent parameter mismatches | Developer Analysis |
| ASR accuracy drops 16 points on accented speech | Voice AI Research |
| 50%+ of OCR data requires manual checking | Enterprise Survey |
| Only 29% of developers trust AI output accuracy | Industry Survey |
| 40% of agentic AI projects will be scrapped by 2027 | Gartner |

### Cost & Evaluation Statistics (2026)

| Finding | Source |
|---------|--------|
| 70-80% of queries can use smaller models | Cost Analysis Research |
| Semantic caching reduces costs 40-70% | Caching Research |
| Batching reduces API costs 20-40% | Batch Processing Research |
| Eval-production gap: 15-40% performance drop | MLOps Research |
| 30-50% of golden datasets have label issues | Data Quality Research |
| 83% of RAG systems fail on production despite benchmarks | RAGAS Study |
| 25-35% of tasks routed to suboptimal agent | Routing Research |
| Background noise increases ASR WER 15-40% | Voice AI Research |

### OCR/Document AI Statistics (2026)

| Finding | Source |
|---------|--------|
| 88% of businesses report errors in automated data pipelines | Parseur 2026 Survey |
| Frontier agents score <50% on enterprise document reasoning | Databricks OfficeQA |
| 30% of invoice requests fail first iteration (templates) | Accenture |
| Legacy OCR plateaus at 60-70% automation | Industry Analysis |
| IDP reduces error rates by 52% vs OCR-only | Benchmark Study |
| 40% of IDP implementations underperform ROI projections | Industry Analysis |
| VLMs struggle with sparse tables, mismatching columns | VLM Research |
| Long-document benchmarks: 66-69% on complex tables | Model Benchmarks |
| $47,000 spent on single 11-day agent loop | DEV.to Incident |
| 68% of businesses see errors on >1% of invoices | IOFM |
| 3.6% manual data entry error rate | IOFM |
| 5-10% GL miscoding rate in AP automation | APQC |

---

## Recent Sources (Feb-May 2026)

### Security Incidents & Vulnerabilities

#### MCP & Tool Infrastructure
- [MCP Design Flaw: 200K Servers at Risk](https://www.theregister.com/2026/04/16/anthropic_mcp_design_flaw/) - Critical architectural vulnerability in Anthropic's MCP SDKs
- [OX Security: Mother of All AI Supply Chains](https://www.ox.security/blog/the-mother-of-all-ai-supply-chains-critical-systemic-vulnerability-at-the-core-of-the-mcp/) - Systemic MCP vulnerability affecting 150M+ downloads
- [Check Point: Claude Code RCE & Token Exfiltration](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/) - CVE-2025-59536, CVE-2026-21852
- [SecurityWeek: Claude OAuth Token Theft via MCP Hijacking](https://www.securityweek.com/claude-code-oauth-tokens-can-be-stolen-through-stealthy-mcp-hijacking/) - Silent OAuth token interception (April 2026)
- [Obot: Claude Leak Crisis MCP Security](https://obot.ai/blog/mcp-security-masterclass-claude-leak-crisis/) - Source map leak exposing 512K lines of code

#### Prompt Injection & Agent Exploits
- [Microsoft: Prompts Become Shells - RCE in AI Frameworks](https://www.microsoft.com/en-us/security/blog/2026/05/07/prompts-become-shells-rce-vulnerabilities-ai-agent-frameworks/) - Semantic Kernel CVE-2026-25592, CVE-2026-26030
- [VentureBeat: Comment and Control Attack](https://venturebeat.com/security/ai-agent-runtime-security-system-card-audit-comment-and-control-2026) - Three AI coding agents leaked secrets through single prompt injection
- [AIRIA: AI Security 2026 - Lethal Trifecta](https://airia.com/ai-security-in-2026-prompt-injection-the-lethal-trifecta-and-how-to-defend/) - Prompt injection defense strategies
- [OWASP GenAI Q1 2026 Exploit Roundup](https://genai.owasp.org/2026/04/14/owasp-genai-exploit-round-up-report-q1-2026/) - Quarterly exploit report
- [IBM: OpenClaw Agentic AI Vulnerabilities](https://www.ibm.com/think/x-force/agentic-ai-growing-fast-vulnerabilities) - ClawJacked indirect prompt injection

#### Enterprise Security Reports
- [Kiteworks: 65% of Firms Hit by AI Agent Security Incidents](https://www.kiteworks.com/cybersecurity-risk-management/ai-agent-security-incidents-2026/) - 2026 enterprise survey
- [VentureBeat: 88% Enterprises Breached](https://venturebeat.com/security/most-enterprises-cant-stop-stage-three-ai-agent-threats-venturebeat-survey-finds/) - AI agent security enforcement gap
- [Beam AI: 5 Real AI Agent Security Breaches 2026](https://beam.ai/agentic-insights/ai-agent-security-breaches-2026-lessons) - Breach analysis and lessons
- [Foresiet: 6 AI Security Incidents April 2026](https://foresiet.com/blog/ai-security-incidents-attack-paths-april-2026/) - Full attack path analysis
- [NSA: Careful Adoption of Agentic AI](https://media.defense.gov/2026/Apr/30/2003922823/-1/-1/0/CAREFUL%20ADOPTION%20OF%20AGENTIC%20AI%20SERVICES_FINAL.PDF) - Government guidance (April 2026)

### Production Failures & Incidents

#### Major 2026 Incidents
- [Medium: AI Agent Failures - 7 Real Disasters](https://medium.com/neuralnotions/ai-agent-failures-in-production-7-real-disasters-and-what-caused-them-51274f55a211) - Production disaster analysis
- [Medium: Why AI Agents Keep Failing](https://medium.com/data-science-collective/why-ai-agents-keep-failing-in-production-cdd335b22219) - Systemic failure patterns
- [Augment Code: Multi-Agent Coordination Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - 41-86.7% failure rates
- [Redis: Why Multi-Agent LLM Systems Fail](https://redis.io/blog/why-multi-agent-llm-systems-fail/) - Coordination breakdowns

#### Cost Runaway Incidents
- [DEV.to: $47,000 Agent Loop](https://dev.to/waxell/the-47000-agent-loop-why-token-budget-alerts-arent-budget-enforcement-389i) - 11-day infinite loop, no hard stop
- [Dev Journal: $437 Overnight AI Agent](https://earezki.com/ai-news/2026-04-29-i-let-my-ai-agent-run-overnight-it-cost-437/) - Unchecked overnight run
- [LeanOps: Agents Burn 50x More Tokens](https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026/) - Token cost analysis
- [Portal26: Agentic Token Controls](https://siliconangle.com/2026/04/23/portal26-launches-agentic-token-controls-cap-runaway-ai-agent-spend/) - New cost control tools
- [MindStudio: Token Budget Management](https://www.mindstudio.ai/blog/ai-agent-token-budget-management-claude-code) - Budget enforcement strategies

#### Cost Efficiency & Model Selection
- [OpenAI: Model Pricing](https://openai.com/api/pricing/) - Current model costs for routing decisions
- [Anthropic: Claude Pricing](https://www.anthropic.com/pricing) - Claude model tier pricing
- [GPTCache: Semantic Caching](https://github.com/zilliztech/GPTCache) - LLM response caching
- [LangChain: Caching Patterns](https://python.langchain.com/docs/modules/model_io/llms/llm_caching) - Caching implementation
- [OpenAI: Batch API](https://platform.openai.com/docs/guides/batch) - Native batch processing
- [Anthropic: Message Batches](https://docs.anthropic.com/en/docs/build-with-claude/message-batches) - Claude batch API

### Evaluation & Testing

#### Golden Dataset & Benchmark Issues
- [Contamination in Language Models](https://arxiv.org/abs/2310.10628) - Benchmark contamination study
- [BERTScore](https://arxiv.org/abs/1904.09675) - Semantic similarity evaluation
- [LLM-as-Judge](https://arxiv.org/abs/2306.05685) - Using LLMs for evaluation
- [RAGAS](https://docs.ragas.io/) - RAG evaluation framework
- [Confident Learning](https://arxiv.org/abs/1911.00068) - Finding label errors in datasets
- [Data-centric AI](https://datacentricai.org/) - Label quality and data focus
- [Arize: Data Drift Detection](https://arize.com/blog/data-drift-detection/) - Distribution monitoring

#### Evaluation Research
- [Databricks: OfficeQA Benchmark](https://www.databricks.com/blog/why-frontier-agents-cant-read-documents-and-how-were-fixing-it) - Real-world vs benchmark gap (<50% accuracy)
- [RAGAS Fails 83%](https://medium.com/data-science-collective/air-canada-lost-a-lawsuit-because-their-rag-hallucinated-yours-will-too-b92b6b9a4d39) - Benchmark limitations
- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) - 17-33% hallucination despite RAG

### Legal & Regulatory

#### Lawsuits & Legal Actions
- [Alston & Bird: Pennsylvania Sues Character.AI](https://www.alston.com/en/insights/publications/2026/05/pennsylvania-brings-suit-against-chatbot-developer) - Unlawful practice of medicine (May 2026)
- [Baker Botts: 78 State Bills, 58 Lawsuits](https://ourtake.bakerbotts.com/post/102mipe/ai-chatbot-regulation-78-state-bills-58-lawsuits) - Regulatory landscape
- [Lyon Firm: Undisclosed AI Chatbot Lawsuits](https://thelyonfirm.com/blog/undisclosed-chatbot-consumer-rights-ai-disclosure-law/) - Consumer rights violations
- [Class Law Group: AI Chatbot Harm Claims](https://www.classlawgroup.com/ai-chatbot-lawsuits) - Active litigation tracker
- [Baker McKenzie: US Chatbot Laws](https://www.bakermckenzie.com/en/insight/publications/2026/02/united-states-navigating-the-laws-of-chatbots-and-ai-assistants) - Legal framework (Feb 2026)

#### Customer Service Failures
- [Social Intents: AI Chatbot Hallucination 2026](https://www.socialintents.com/blog/ai-chatbot-hallucination-in-customer-service/) - Customer service hallucination patterns
- [Envive: NYC MyCity Chatbot Case Study](https://www.envive.ai/post/case-study-nycs-mycity-chatbot) - Wrong legal advice analysis

### Code Agent Issues

- [SitePoint: Claude Code vs Cursor vs Copilot 2026](https://www.sitepoint.com/claude-code-vs-cursor-vs-copilot-the-2026-developer-comparison/) - Developer comparison
- [MintMCP: 2026 Security Comparison](https://www.mintmcp.com/blog/claude-code-cursor-vs-copilot) - Security vulnerabilities across tools
- [GitHub Discussion: AI Security Headaches 2026](https://github.com/orgs/community/discussions/194034) - Community-reported issues
- [Dev Genius: Which AI Fixes Production Bugs?](https://blog.devgenius.io/github-copilot-vs-cursor-vs-claude-code-which-ai-actually-fixes-production-bugs-9485b33131c6) - Real bug fix comparison
- [Hashnode: Brutal 2026 Review](https://hashnode.com/forums/thread/claude-code-vs-cursor-vs-copilot-a-brutal-2026-review) - Honest limitations assessment

### RAG & Enterprise AI

- [Medium: 7 RAG Hallucination Root Causes](https://medium.com/@umesh382.kushwaha/why-your-rag-pipeline-hallucinates-7-root-causes-and-how-to-fix-them-1a04a84be7f5) - March 2026 analysis
- [Atlan: LLM Hallucinations 2026](https://atlan.com/know/llm-hallucinations/) - Comprehensive hallucination guide
- [CMARix: RAG & AI Trust Statistics 2026](https://www.cmarix.com/blog/rag-ai-statistics/) - Enterprise trust metrics
- [FloTorch: 2026 RAG Performance Landscape](https://www.flotorch.ai/blogs/the-2026-rag-performance-landscape-what-every-enterprise-leader-needs-to-know) - Enterprise benchmarks

### Observability & Monitoring

- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Complete monitoring guide
- [LinkedIn: Silent Failures of Production AI](https://www.linkedin.com/pulse/silent-failures-production-ai-why-most-llm-monitoring-praveen-juyal-iqgyc) - Why monitoring fails
- [Plain English: LLM Reliability Paradox](https://plainenglish.io/artificial-intelligence/the-llm-reliability-paradox-agents-aren-t-broken-your-architecture-is) - Architecture vs model issues

### Recent Statistics (2026)

| Finding | Source |
|---------|--------|
| 88% of enterprises reported AI agent security incidents | VentureBeat/Kiteworks 2026 |
| 61% of incidents involved sensitive data exposure | CSA Report April 2026 |
| 45% of AI-generated code has security vulnerabilities | Veracode 2026 |
| 52% of enterprise AI responses contain fabrications with ungoverned RAG | Enterprise Survey 2026 |
| 82% discovered unknown AI agents in past year | CSA "Autonomous but Not Controlled" |
| Multi-agent systems fail at 41-86.7% rates | MAST Taxonomy |
| MCP vulnerability affects 200,000+ servers | OX Security April 2026 |
| 78 chatbot bills filed across 27 states (Jan 2026) | Baker Botts |

---

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

To add a new failure pattern:
1. Navigate to the appropriate agent type (e.g., `agents/ocr-agent/`)
2. Find or create the relevant goal folder (e.g., `goals/accurate-text-extraction/`)
3. Add a new failure file in `failures/` (e.g., `failures/my-failure.md`)
4. Update the goal's README.md to include your failure in the table
5. Submit a PR

## Related Resources

- [Awesome Agent Failures (Vectara)](https://github.com/vectara/awesome-agent-failures) - Academic/research-focused failure documentation
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) - Security vulnerabilities in LLM applications

---

## About SaraLabs.ai

<p align="center">
  <a href="https://saralabs.ai"><strong>saralabs.ai</strong></a> — Building reliable AI agents for production
</p>

This repository is maintained by **[SaraLabs.ai](https://saralabs.ai)**, a company dedicated to making AI agents work reliably in production environments.

### Our Mission

We believe AI agents will transform how businesses operate—but only if they work reliably. Today, **40% of agentic AI projects are projected to be scrapped by 2027** (Gartner), and **88% of enterprises report AI agent security incidents**. We're here to change that.

SaraLabs.ai builds the knowledge, tools, and expertise needed to deploy AI agents with confidence.

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
| **General inquiries** | [team@saralabs.ai](mailto:team@saralabs.ai) |
| **Consulting & projects** | [team@saralabs.ai](mailto:team@saralabs.ai) |
| **Contribute a pattern** | Submit a PR or email us |
| **Report an issue** | Open a GitHub issue |

We respond to every inquiry. If you've encountered a failure pattern not documented here, we'd love to hear about it.

<p align="center">
  <a href="https://saralabs.ai"><strong>Visit saralabs.ai →</strong></a>
</p>

---

*Built by [SaraLabs.ai](https://saralabs.ai) — Reliable AI agents for production.*
