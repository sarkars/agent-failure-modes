# Prioritized Source List for New Agent Failure Patterns

**Compiled**: July 2026  
**Total High-Priority Sources**: 95+  
**Estimated New Patterns**: 180-220  
**Research Period**: 2024-2026  

---

## PHASE 1: CRITICAL NEW PATTERNS (START HERE - Week 1-2)

### 1. VISION-LANGUAGE MODEL FAILURES
**Priority**: CRITICAL | **Estimated Patterns**: 25-30 | **Domain**: by-capability/vision-and-multimodal

#### High-Impact Sources:
1. **arXiv:2509.15435 - ORCA: Agentic Reasoning Framework for VLM Hallucination**
   - Failure: State-of-the-art models fail at grid cell counting (specific cell sizes)
   - Failure: Patch tokenization hides visual edges
   - Patterns to author: vision-hallucination-counting, patch-tokenization-boundaries, cell-size-sensitivity

2. **arXiv:2510.10991 - Survey on Agentic Multimodal LLMs**
   - Failure: Multimodal hallucinations in reasoning chains
   - Failure: Image-text misalignment in decision-making
   - Patterns: multimodal-hallucination-cascade, image-text-grounding-failure

3. **arXiv:2602.15382 - Vision Wormhole: Latent-Space Communication**
   - Failure: Communication failures in heterogeneous multi-agent vision systems
   - Failure: Latent space representation drift across agents
   - Pattern: vision-agent-communication-failure

4. **arXiv:2607.00174 - Steal the Patch Size: Adversarial VLM Attacks**
   - Failure: Adversarial patch attacks on vision-language models
   - Failure: Adversarial robustness failures
   - Pattern: adversarial-patch-manipulation-vlm

5. **arXiv:2603.05465 - HALP: Detecting Hallucinations in VLMs**
   - Failure: Confidence-accuracy mismatch in VLM hallucinations
   - Pattern: vision-hallucination-confidence-miscalibration

6. **arXiv:2506.15065 - HEAL: Hallucinations in Embodied Agents**
   - Failure: Action hallucinations in robotics/embodied agents
   - Failure: Environmental misperception in embodied context
   - Pattern: embodied-agent-action-hallucination

#### Additional Supporting Sources:
- arXiv:2505.17061 - Mixture of Decoding (VLM decoding failures)
- arXiv:2505.12343 - Inter-Layer Consistency (VLM consistency)
- arXiv:2604.12115 - HTDC: Hesitation-Triggered Calibration
- arXiv:2410.11242 - Automated Hallucination Test Case Generation
- arXiv:2603.25740 - Vision-Language-Action Model Failures (Autonomous Driving)

---

### 2. MULTI-AGENT COORDINATION FAILURES
**Priority**: CRITICAL | **Estimated Patterns**: 30-40 | **Domain**: by-capability/multi-agent-systems + cross-cutting/accuracy

#### High-Impact Sources:
1. **arXiv:2503.13657 - Why Do Multi-Agent LLM Systems Fail? (MAST)**
   - Finding: Documented 14 unique multi-agent failure modes
   - Failure: Error propagation & cascading (17x error amplification)
   - Failure: Collective reasoning failure as agent count increases
   - Failure: False consensus in critical domains
   - Patterns: multi-agent-error-propagation, collective-reasoning-collapse, false-consensus-risk, agent-count-scaling-failure

2. **arXiv:2503.06789 - Towards Reliable Multi-Agent LLM Systems (80%+ Failure)**
   - Finding: 80%+ documented failure rates in production
   - Failure: Monolithic entanglement (agents tightly coupled)
   - Pattern: monolithic-agent-entanglement

3. **arXiv:2510.10581 - GraphTracer: Failure Tracing in Multi-Agent Deep Search**
   - Failure: Failure attribution in complex multi-turn multi-agent workflows
   - Failure: Cascading errors across agent chains
   - Pattern: multi-agent-failure-attribution, cascading-failure-chains

4. **arXiv:2606.03467 - StepFinder: Temporal Semantic Framework for Failure Attribution**
   - Failure: Temporal misalignment in multi-agent systems
   - Pattern: temporal-semantic-misalignment-agents

5. **arXiv:2509.03312 - AgenTracer: Who Is Inducing Failure in Agentic Systems**
   - Failure: Root cause attribution in agent failures
   - Pattern: agent-failure-root-cause-blindness

6. **arXiv:2505.11556 - Systematic Failures in Collective Reasoning**
   - Failure: Distributed information handling failures
   - Failure: Consensus breakdown in decentralized agent systems
   - Pattern: collective-reasoning-under-partial-information-failure

7. **arXiv:2603.21522 - EAGER: Efficient Failure Management for Multi-Agent Systems**
   - Failure: Recovery mechanisms insufficient in agent systems
   - Pattern: agent-recovery-mechanism-failure

8. **arXiv:2601.22290 - Six Sigma Agent: Enterprise-Grade Reliability**
   - Failure: Consensus-driven decomposition failures
   - Pattern: consensus-driven-decomposition-failure

#### Supporting GitHub Issues:
- github.com/langchain-ai/langchain/issues - Agent chaining failures (tag: agents)
- github.com/bytedance/deer-flow/issues/1055 - Repetitive tool call loops

---

### 3. MEMORY POISONING & CORRUPTION (EMERGING SECURITY THREAT)
**Priority**: CRITICAL | **Estimated Patterns**: 20-25 | **Domain**: cross-cutting/security/agent-trust

#### High-Impact Sources:
1. **arXiv:2601.05504 - Memory Poisoning Attack and Defense on Memory-Based LLM Agents**
   - Finding: 95%+ attack success rate (MINJA 2025)
   - Finding: 80% success with <0.1% poison rate (AgentPoison 2024)
   - Finding: 91,000+ attack sessions captured (Oct 2025-Jan 2026)
   - Failure: Temporally decoupled attacks (execute weeks later)
   - Failure: Existing defenses fail (tool contracts, circuit breakers, I/O moderation)
   - Patterns: memory-poisoning-attack-success, temporally-decoupled-poison-execution, memory-poison-defense-gap

2. **arXiv:2605.03482 - MEMSAD: Gradient-Coupled Anomaly Detection**
   - Failure: Gradient-based detection evasion
   - Pattern: gradient-anomaly-detection-evasion

3. **arXiv:2602.16901 - AgentLAB: Benchmarking LLM Agents Against Long-Horizon Attacks**
   - Failure: Long-horizon attack resilience
   - Pattern: long-horizon-attack-vulnerability

4. **arXiv:2605.28201 - Plant, Persist, Trigger: Sleeper Attack on LLM Agents**
   - Failure: Sleeper agent attacks (plant early, trigger later)
   - Pattern: sleeper-agent-attack-vector

5. **arXiv:2605.23723 - MemAudit: Post-hoc Auditing of Poisoned Agent Memory**
   - Failure: Post-compromise detection challenges
   - Pattern: memory-poison-post-hoc-detection-failure

#### Supporting Sources:
- arXiv:2603.01564 - From Secure Agentic AI to Secure Agentic Web
- arXiv:2603.09002 - Security Considerations for Multi-Agent Systems
- CSA Report (April 2026): 61% sensitive data exposure; 82% unknown agents discovered

---

### 4. EXTENDED REASONING FAILURES (o1/o3-style Models)
**Priority**: HIGH | **Estimated Patterns**: 25-35 | **Domain**: by-capability/reasoning-and-chain-of-thought

#### High-Impact Sources:
1. **arXiv:2601.19928 - Mechanistic Understanding of Large Reasoning Models**
   - Focus: Training, inference, and failure modes in extended reasoning
   - Failure: Reasoning overconfidence
   - Failure: Intermediate-step token overflow
   - Patterns: reasoning-overconfidence, intermediate-step-token-explosion, reasoning-path-divergence

2. **arXiv:2601.10101 - Matrix as Plan: Structured Logical Reasoning with Feedback**
   - Failure: Replanning failures in reasoning chains
   - Pattern: reasoning-replanning-failure

3. **arXiv:2510.09312 - Verifying Chain-of-Thought via Computational Graph**
   - Failure: Computational graph inconsistencies
   - Pattern: cot-computational-graph-inconsistency

4. **arXiv:2510.04040 - FaithCoT-Bench: Instance-Level Faithfulness**
   - Failure: Unfaithful reasoning steps (correct answer, wrong reasoning)
   - Pattern: unfaithful-chain-of-thought-path

5. **arXiv:2606.23404 - ReasoningLens: Hierarchical Visualization & Diagnostic Auditing**
   - Failure: Reasoning opacity in extended reasoning models
   - Pattern: reasoning-opacity-in-extended-models

6. **arXiv:2606.13603 - Beyond the Commitment Boundary: Epiphenomenal Chain-of-Thought**
   - Failure: Chain-of-thought as epiphenomena (output doesn't affect reasoning)
   - Pattern: epiphenomenal-chain-of-thought

7. **arXiv:2506.12301 - Unveiling Confirmation Bias in Chain-of-Thought**
   - Failure: Confirmation bias in reasoning chains
   - Pattern: confirmation-bias-in-extended-reasoning

8. **arXiv:2602.06176 - Large Language Model Reasoning Failures**
   - Comprehensive taxonomy of reasoning failures
   - Pattern: reasoning-failure-taxonomy (consolidation opportunity)

---

### 5. CONTEXT WINDOW OVERFLOW & MEMORY ARCHITECTURE
**Priority**: HIGH | **Estimated Patterns**: 15-20 | **Domain**: cross-cutting/accuracy/context-management

#### High-Impact Sources:
1. **arXiv:2602.07962 - LOCA-bench: Benchmarking Under Controllable Extreme Context Growth**
   - Finding: Performance degrades after 32K tokens
   - Failure: Lost-in-middle effect (ignores 100K of 150K context)
   - Failure: Token creep (2K→25K over conversation)
   - Patterns: context-window-performance-degradation, lost-in-middle-effect, token-creep-accumulation

2. **arXiv:2511.22729 - Solving Context Window Overflow in AI Agents**
   - Failure: Context overflow cascades
   - Pattern: context-overflow-cascade-failure

3. **arXiv:2507.05257 - Evaluating Memory in LLM Agents via Incremental Multi-Turn**
   - Failure: Memory quality degradation over turns
   - Pattern: memory-degradation-over-turns

4. **arXiv:2509.08912 - Characterizing User-Reported Risks in LLMs "In the Wild"**
   - Failure: Real-world context management risks
   - Pattern: context-management-production-failure

#### Industry Findings:
- Databricks research (August 2025): Million-token windows insufficient for large codebases
- Factory.ai research: Enterprise context windows are bottleneck for code agents
- Pattern: code-agent-context-window-overflow

---

## PHASE 2: HIGH-VALUE PATTERNS (Week 3-4)

### 6. CODE GENERATION & VERIFICATION FAILURES
**Priority**: HIGH | **Estimated Patterns**: 30-40 | **Domain**: by-use-case/code-generation

#### High-Impact Sources:
1. **arXiv:2605.29442 - How Coding Agents Fail Their Users (20,574 Real Sessions)**
   - Finding: 10x increase in security findings (Dec 2024-June 2025)
   - Finding: Behavioral drivers beyond simple resolution rates
   - Failure: Environment synthesis failures (dependency resolution)
   - Failure: Logic bugs (difficult to catch)
   - Failure: Verification bottleneck (time saved re-spent auditing)
   - Failure: Lack of proactivity (not just autonomy)
   - Patterns: code-generation-security-regression, environment-synthesis-failure, code-logic-bug-evasion, code-verification-bottleneck, agent-proactivity-deficiency

2. **arXiv:2602.02138 - CAM: Causality-based Analysis for Multi-Agent Code Generation**
   - Failure: Causal reasoning failures in code generation
   - Pattern: code-generation-causal-reasoning-failure

3. **arXiv:2604.04226 - SW-A²-Bench: Autonomous Software Agent Generation**
   - Failure: End-to-end CLI tool generation failures
   - Pattern: cli-tool-generation-failure

4. **arXiv:2604.02547 - Beyond Resolution Rates: Behavioral Drivers of Coding Agent Success**
   - Failure: Behavioral patterns driving code agent failure
   - Pattern: code-agent-behavioral-failure-drivers

5. **arXiv:2508.00083 - Survey on Code Generation with LLM-based Agents**
   - Comprehensive taxonomy of code generation failures

6. **arXiv:2604.06742 - Evaluating LLM-Based 0-to-1 Software Generation**
   - Failure: Greenfield code generation failures

7. **arXiv:2605.06717 - Agentic Coding Needs Proactivity, Not Just Autonomy**
   - Failure: Passive autonomy (waits for human direction)
   - Pattern: code-agent-passivity-failure

8. **arXiv:2602.06593 - AgentStepper: Interactive Debugging**
   - Failure: Debugging in agent workflows
   - Pattern: code-agent-debugging-failure

---

### 7. TOOL CALLING & HALLUCINATIONS
**Priority**: HIGH | **Estimated Patterns**: 20-25 | **Domain**: cross-cutting/operations/tool-reliability

#### High-Impact Sources:
1. **arXiv:2601.05214 - Internal Representations as Indicators of Hallucinations in Agent Tool Selection**
   - Failure: Tool selection hallucinations (non-existent tools, semantically wrong tools)
   - Failure: Parameter errors (e.g., guests=15 despite max 10)
   - Patterns: tool-selection-hallucination, tool-parameter-error, tool-nonexistence-hallucination

2. **arXiv:2601.06818 - AgentHallu: Benchmarking Automated Hallucination Attribution**
   - Failure: Hallucination attribution challenges
   - Pattern: tool-hallucination-attribution-failure

3. **arXiv:2605.25310 - Tool-Call Dependency Structure is Linearly Decodable**
   - Failure: Tool call dependency failures
   - Pattern: tool-call-dependency-failure

4. **arXiv:2510.23853 - Your LLM Agents are Temporally Blind**
   - Failure: Temporal misalignment in tool use decisions
   - Pattern: tool-use-temporal-blindness

5. **arXiv:2606.06976 - Exploring Agentic Tool-Calling Decisions via Uncertainty**
   - Failure: Confidence calibration in tool selection
   - Pattern: tool-selection-confidence-miscalibration

6. **arXiv:2509.05755 - Red-Teaming Coding Agents from Tool-Invocation Perspective**
   - Failure: Tool invocation security vulnerabilities
   - Pattern: tool-invocation-security-failure

#### GitHub/Standards:
- SEP-1303 (MCP Standard): Input validation errors returned as Protocol Errors
  - Failure: Prevents LLM self-correction; model repeats mistakes
  - Pattern: mcp-protocol-error-feedback-loop
  - Impact: 315 MCP vulnerabilities (2025); 270% increase Q2→Q3 2025

---

### 8. LONG-HORIZON PLANNING & AUTONOMOUS TASKS
**Priority**: HIGH | **Estimated Patterns**: 20-30 | **Domain**: by-capability/long-horizon-planning

#### High-Impact Sources:
1. **arXiv:2508.13143 - Exploring Autonomous Agents: Why They Fail Completing Tasks**
   - Failure: Long-horizon task completion failures
   - Failure: Goal degradation over time
   - Patterns: long-horizon-goal-drift, autonomous-task-failure-cascade

2. **arXiv:2503.09572 - Plan-and-Act: Improving Planning for Long-Horizon Tasks**
   - Failure: Planning-action mismatch in long horizons
   - Pattern: planning-action-mismatch-long-horizon

3. **arXiv:2605.29927 - Does The Way You Plan Matter? Planning Representations for Web Agents**
   - Failure: Representation-dependent planning failures
   - Pattern: planning-representation-failure

4. **arXiv:2604.17220 - Dynamics of Cognitive Heterogeneity in Supply Chains**
   - Failure: Behavioral bias in multi-stage long-horizon systems
   - Pattern: behavioral-bias-long-horizon-systems

#### Industry/Real-World:
- DEV.to: $47,000 Agent Loop - 11-day infinite loop incident
- Dev Journal: $437 Overnight AI Agent - Cost runaway
- Pattern: unchecked-long-horizon-execution-cost-explosion

---

## PHASE 3: DOMAIN-SPECIFIC PATTERNS (Week 5-6)

### 9. HEALTHCARE & MEDICAL AGENTS
**Priority**: MEDIUM | **Estimated Patterns**: 35-45 | **Domain**: by-use-case/healthcare

#### High-Impact Sources:
1. **arXiv:2602.09653 - ClinAlign: Scaling Healthcare Alignment**
   - Failure: Clinician preference misalignment
   - Pattern: healthcare-alignment-failure

2. **arXiv:2510.10185 - Auditing Medical Multi-Agent AI (False Consensus Risk)**
   - Failure: False consensus in multi-agent medical systems
   - Failure: Collective hallucination in diagnosis
   - Patterns: medical-false-consensus-risk, multi-agent-diagnostic-hallucination, medical-team-hallucination-amplification

3. **arXiv:2604.11978 - Long-Horizon Task Mirage in Agentic Systems**
   - Failure: Healthcare long-horizon task failures
   - Pattern: healthcare-long-horizon-failure

4. **arXiv:2506.12482 - Tiered Agentic Oversight: Hierarchical Systems for Healthcare**
   - Failure: Oversight failures in healthcare agents
   - Pattern: healthcare-oversight-failure

5. **arXiv:2512.01453 - Reinventing Clinical Dialogue: Agentic Paradigms**
   - Failure: Dialogue failures in clinical agents
   - Pattern: clinical-dialogue-failure

6. **arXiv:2602.15871 - Trustworthiness of LLMs in Healthcare (Survey)**
   - Comprehensive taxonomy of healthcare trust failures

---

### 10. LEGAL AI & HALLUCINATIONS
**Priority**: MEDIUM | **Estimated Patterns**: 30-40 | **Domain**: by-use-case/legal-contract-analysis

#### High-Impact Sources (Stanford Study):
1. **Stanford HAI Legal Hallucination Study (2024)**
   - Finding: 800,000+ legal queries tested
   - Finding: GPT-4 (58%), GPT-3.5 (69%), Llama 2 (88%) hallucination rates
   - Finding: ~1,000 documented hallucination cases in court filings
   - Finding: As of April 2026: "Problem far from solved"
   - Patterns: legal-hallucination-artifact-citation, legal-case-precedent-fabrication, legal-statute-misquotation

2. **arXiv:2601.15267 - Evaluation of LLMs in Legal Applications**
   - Comprehensive evaluation framework
   - Pattern: legal-evaluation-framework (reference)

3. **arXiv:2604.00945 - A Visionary Look at Vibe Researching (Legal Research)**
   - Failure: Intuition-based legal research failures
   - Pattern: vague-legal-research-guidance-hallucination

4. **arXiv:2606.23716 - Legal Reasoning Is Not Lawyering**
   - Failure: Legal reasoning-execution gap
   - Pattern: legal-reasoning-lawyering-gap

---

### 11. MORTGAGE & LENDING DOMAIN
**Priority**: MEDIUM | **Estimated Patterns**: 40-50 | **Domain**: by-use-case/mortgage-and-lending (NEW)

#### High-Impact Sources:
1. **Industry Finding: 80% of AI Tools Fail in Production (Mortgage)**
   - Failure: FHA limits, dates, deadlines misstatement
   - Failure: Voice cloning + deepfakes for borrower impersonation
   - Failure: Compliance failure from hallucinations
   - Patterns: mortgage-fha-limit-hallucination, mortgage-deadline-misstatement, mortgage-fraud-voice-cloning, mortgage-compliance-hallucination

2. **Fannie Mae Quality Insider Q1 2025**
   - Failure: Document requirement misunderstandings
   - Failure: Income verification failures
   - Pattern: mortgage-document-requirement-confusion

3. **CrossCheck Compliance: AI, Fraud, and Mortgage Risk**
   - Failure: Fraud detection failures
   - Pattern: mortgage-fraud-detection-gap

4. **DocVu.AI: 7 Mortgage Document Challenges**
   - Failure: Document processing edge cases
   - Pattern: mortgage-document-processing-failure

---

### 12. SUPPLY CHAIN & E-COMMERCE
**Priority**: MEDIUM | **Estimated Patterns**: 35-45 | **Domain**: by-use-case/supply-chain, by-use-case/ecommerce (NEW)

#### High-Impact Sources:
1. **arXiv:2411.10184 - Agentic LLMs in Supply Chain (Consensus-Seeking)**
   - Failure: Consensus breakdown in distributed supply chain agents
   - Pattern: supply-chain-consensus-failure

2. **arXiv:2604.17220 - Cognitive Heterogeneity in Supply Chains**
   - Failure: Behavioral bias in multi-stage systems
   - Pattern: supply-chain-behavioral-bias

3. **arXiv:2407.11384 - InvAgent: LLM Multi-Agent Inventory Management**
   - Failure: Inventory optimization failures
   - Pattern: inventory-optimization-failure

4. **Industry Finding: 6,969 E-Commerce Complaints (+56.3% YoY in 2024)**
   - Failure: Chatbot irrelevance
   - Failure: Customer service agent misalignment
   - Pattern: ecommerce-chatbot-irrelevance, customer-service-agent-misalignment

---

## PHASE 4: INFRASTRUCTURE & SECURITY (Week 7)

### 13. INFERENCE ENGINE & INFRASTRUCTURE FAILURES
**Priority**: MEDIUM | **Estimated Patterns**: 20-25 | **Domain**: cross-cutting/operations

#### High-Impact Sources:
1. **Microsoft Study: 156 High-Severity Incidents**
   - Finding: ~60% failures occur at inference engine level
   - Failure: KV cache errors, memory leaks, multi-GPU crashes
   - Failure: Asynchronous vs sync: 47% vs 11% success rates
   - Patterns: kv-cache-error-in-inference, inference-memory-leak, multi-gpu-crash, async-inference-timing-failure

2. **OWASP Top 10 for Agentic Applications (Dec 2025)**
   - Failure: Infrastructure-level security issues
   - Pattern: agentic-infrastructure-security-gap

---

### 14. RAG & RETRIEVAL FAILURES
**Priority**: MEDIUM | **Estimated Patterns**: 25-35 | **Domain**: by-capability/knowledge-retrieval (expansion)

#### High-Impact Sources:
1. **arXiv:2510.09106 - When Retrieval Succeeds and Fails**
   - Failure: Retrieval failure modes
   - Pattern: retrieval-failure-taxonomy

2. **arXiv:2509.04820 - Fishing for Answers: One-shot vs Iterative Retrieval**
   - Failure: Retrieval strategy failures
   - Pattern: retrieval-strategy-failure

3. **arXiv:2505.20625 - Long Context Scaling: Multi-Agent Question-Driven Collaboration**
   - Failure: Multi-agent long-context retrieval failures
   - Pattern: multi-agent-long-context-retrieval-failure

4. **arXiv:2506.10408 - Reasoning RAG via System 1 or System 2**
   - Failure: Reasoning type misalignment in RAG
   - Pattern: rag-system1-system2-mismatch

5. **arXiv:2605.27123 - Rethinking Agentic RAG**
   - Failure: Logic retrieval beyond embeddings
   - Pattern: rag-embedding-limitation

---

## CONSOLIDATED SOURCE MATRIX

| **Category** | **Priority** | **Est. Patterns** | **Lead Sources** | **Domain** | **Status** |
|---|---|---|---|---|---|
| Vision-Language Models | CRITICAL | 25-30 | arXiv:2509.15435, 2510.10991 | by-capability/vision | START WEEK 1 |
| Multi-Agent Coordination | CRITICAL | 30-40 | arXiv:2503.13657, 2503.06789 | by-capability/multi-agent + cross-cutting | START WEEK 1 |
| Memory Poisoning | CRITICAL | 20-25 | arXiv:2601.05504, 2605.03482 | cross-cutting/security | START WEEK 1 |
| Extended Reasoning | HIGH | 25-35 | arXiv:2601.19928, 2510.09312 | by-capability/reasoning | WEEK 2 |
| Context Window Overflow | HIGH | 15-20 | arXiv:2602.07962, 2511.22729 | cross-cutting/accuracy | WEEK 2 |
| Code Generation | HIGH | 30-40 | arXiv:2605.29442, 2602.02138 | by-use-case/code | WEEK 3-4 |
| Tool Calling | HIGH | 20-25 | arXiv:2601.05214, 2601.06818 | cross-cutting/operations | WEEK 3 |
| Long-Horizon Planning | HIGH | 20-30 | arXiv:2508.13143, 2503.09572 | by-capability/long-horizon | WEEK 4 |
| Healthcare | MEDIUM | 35-45 | arXiv:2510.10185, 2602.09653 | by-use-case/healthcare | WEEK 5 |
| Legal AI | MEDIUM | 30-40 | Stanford Study, arXiv:2601.15267 | by-use-case/legal | WEEK 5 |
| Mortgage/Lending | MEDIUM | 40-50 | Industry reports, Fannie Mae | by-use-case/mortgage | WEEK 5 |
| Supply Chain/E-Commerce | MEDIUM | 35-45 | arXiv:2411.10184, Industry data | by-use-case/supply-chain, ecommerce | WEEK 6 |
| Infrastructure/Security | MEDIUM | 20-25 | Microsoft Study, OWASP | cross-cutting/operations, security | WEEK 7 |
| RAG & Retrieval | MEDIUM | 25-35 | arXiv:2510.09106, 2505.20625 | by-capability/knowledge-retrieval | WEEK 7 |

**TOTAL ESTIMATED NEW PATTERNS**: 375-475 unique patterns

---

## IMPLEMENTATION ROADMAP

### Week 1 (CRITICAL PATH - 3 sources, ~80-95 patterns)
- [ ] Vision-Language Model failures (25-30 patterns)
- [ ] Multi-Agent Coordination failures (30-40 patterns)
- [ ] Memory Poisoning attacks (20-25 patterns)

### Week 2 (HIGH VALUE - ~40-55 patterns)
- [ ] Extended Reasoning failures (25-35 patterns)
- [ ] Context Window Overflow (15-20 patterns)

### Week 3-4 (CODE FOCUS - ~50-65 patterns)
- [ ] Code Generation failures (30-40 patterns)
- [ ] Tool Calling failures (20-25 patterns)

### Week 5 (DOMAIN FOCUS - ~105-135 patterns)
- [ ] Healthcare domain (35-45 patterns)
- [ ] Legal domain (30-40 patterns)
- [ ] Mortgage/Lending domain (40-50 patterns)

### Week 6 (OPERATIONAL FOCUS - ~35-45 patterns)
- [ ] Supply Chain (20-25 patterns)
- [ ] E-Commerce (15-20 patterns)

### Week 7 (INFRASTRUCTURE & RAG - ~45-60 patterns)
- [ ] Infrastructure & Security (20-25 patterns)
- [ ] RAG & Retrieval expansion (25-35 patterns)

### Week 8 (LONG-HORIZON - ~20-30 patterns)
- [ ] Long-Horizon Planning (20-30 patterns)

---

## QUALITY ASSURANCE CHECKLIST

For each pattern authored from these sources:
- [ ] Source paper/blog cited with arXiv ID or URL
- [ ] Failure mechanism grounded in academic research or production incident
- [ ] Concrete example provided (realistic scenario from source)
- [ ] Evaluation recipe included (test cases, metrics)
- [ ] Production signals documented (alerts, dashboards, logs)
- [ ] Mitigation strategies practical and implementable
- [ ] Cross-references to related patterns added
- [ ] No placeholder text ([Add ...])

---

## NOTES FOR AUTHORSHIP

### Hallucination Patterns (HIGH VOLUME)
- Legal domain has 1,000+ documented court cases
- Healthcare has measurable diagnostic error rates (5%)
- Mortgage has compliance-driven impact
- Vision models have specific failure patterns (counting, patches)
- **Recommendation**: Prioritize domain-specific hallucination variants

### Memory & Context Issues (FOUNDATIONAL)
- Multiple sources converge on context window as bottleneck
- Memory poisoning represents emerging threat class
- **Recommendation**: Create cross-cutting patterns covering architecture-level issues

### Multi-Agent Failures (EXPLOSIVE GROWTH AREA)
- MAST taxonomy identifies 14 distinct failure modes
- Error propagation is multiplicative (17x)
- **Recommendation**: Structure as consolidated patterns (not per-domain)

### Security Patterns (URGENT)
- Memory poisoning: 95%+ success rate
- MCP vulnerabilities: 270% increase Q2→Q3 2025
- **Recommendation**: Prioritize attack surface documentation

---

## RELATED RESEARCH TO MONITOR

1. **Anthropic Responsible Scaling Policy** (ongoing)
2. **Anthropic "Detecting and Countering Misuse" (Aug 2025)**
3. **LangChain State of Agent Engineering Reports** (quarterly)
4. **Stanford HAI Legal AI Benchmark Updates**
5. **Gartner AI Agents Research** (40% projects projected scrapped by 2027)
6. **OWASP Updates to Top 10 for Agentic Applications**

---

## APPROVED BY
- Research Agent: aa8654739fb3089cb
- Compiled: July 2026
- Ready for authorship: ✅ YES

