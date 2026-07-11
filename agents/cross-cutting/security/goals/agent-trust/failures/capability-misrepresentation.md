# Capability Misrepresentation

## Issue: Agents Claim Capabilities They Don't Actually Have

**Frequency**: Common

**Symptoms**
- Agent accepts tasks it cannot complete
- Poor quality outputs from "specialist" agents
- Tasks silently fail or produce wrong results
- No way to verify agent claims before delegation
- System relies on self-reported capabilities

**Root Cause**
In multi-agent systems, agents declare their capabilities to orchestrators and peers. These declarations are typically self-reported with no verification mechanism. Agents may overstate capabilities due to training on optimistic descriptions, lack of self-awareness about limitations, or intentional deception. Orchestrators route tasks based on these false claims, leading to failures.

**Example**
```
Legal Document Review System:

Agent registry:
  LegalReviewAgent:
    capabilities: ["contract_review", "compliance_check", 
                   "regulatory_analysis", "litigation_support"]
    
Reality:
  - Trained primarily on US contract law
  - No GDPR expertise
  - No securities regulation knowledge
  - "Litigation support" = generic text analysis

Task routing:
  User request: "Review this EU data processing agreement for GDPR compliance"
  
  Orchestrator:
    - Checks capabilities: "compliance_check" ✓
    - Assigns to LegalReviewAgent

  LegalReviewAgent output:
    "This agreement appears compliant. Standard clauses present.
     Recommended: proceed with execution."
  
  Reality:
    - Agreement missing mandatory GDPR Article 28 clauses
    - Unlawful data transfer provisions
    - Agent lacked expertise to identify issues
    - Confident wrong answer

Outcome: Company signs non-compliant agreement
         €2M GDPR fine 6 months later
```

**Key Statistics**
From Multi-Agent Research (2026):
- 41.77% of failures from specification problems (MAST)
- Agents cannot accurately assess own capabilities
- Capability verification virtually non-existent
- LLMs consistently overestimate their abilities
- No standard for capability assessment

**Misrepresentation Types**
| Type | Cause | Risk |
|------|-------|------|
| Overstated expertise | Training data bias | High |
| Missing limitations | No self-awareness | High |
| Version mismatch | Outdated capability list | Medium |
| Context blindness | Works in training, fails in production | High |
| Intentional deception | Malicious agent | Critical |

**Contributing Factors**
- LLMs trained to be helpful, not accurate about limits
- No penalty for claiming false capabilities
- Capability verification expensive/difficult
- Self-reported capabilities standard practice
- No capability testing frameworks

## Mitigation Strategies

### Prevention
1. **Independent benchmark-based skill certification**: Certify each agent's claimed capability against a domain-specific benchmark task set with known-correct answers (e.g., a set of contracts with confirmed GDPR compliance gaps) before allowing it to be routed tasks in that category, rather than accepting the agent's self-declared capability list. Trade-off: building representative benchmarks for every specialized domain (GDPR, securities law, litigation) is a significant, ongoing investment, and a benchmark can go stale as regulations/domains evolve.
2. **Explicit negative-capability declaration requirement**: Require agents (or their configuration) to explicitly enumerate known limitations and out-of-scope domains, not just capabilities, and treat any task falling in an undeclared or negative-capability zone as requiring escalation rather than default routing to the closest-matching agent. Trade-off: negative capabilities are harder to enumerate exhaustively than positive ones, especially for domains the agent's developers didn't anticipate.
3. **Progressive trust with staged task exposure**: Start newly-registered or newly-claimed capabilities with low-stakes tasks and expand the agent's task scope only after a track record of verified successful outcomes in that category, rather than granting full task-routing eligibility immediately based on a capability declaration. Trade-off: slows onboarding of genuinely capable new agents/capabilities and requires infrastructure to track staged trust levels.

### Detection & Response
1. **Capability-claim-vs-outcome tracking with confidence calibration monitoring**: Continuously compare an agent's claimed capability and reported confidence against actual task outcome correctness, flagging agents that are both wrong and confident (the most dangerous combination, since confident-wrong outputs are least likely to trigger review).
2. **Periodic re-testing against evolving benchmarks**: Regularly re-run capability certification tests, especially after any model/version change, since a capability that was previously verified can silently regress or a domain's requirements (e.g., a regulatory change) can shift out from under a previously-valid certification.
3. **User-reported performance surveys segmented by claimed capability**: Collect structured feedback specifically tied to which capability an agent was exercising, since aggregate satisfaction metrics can mask a systematic failure pattern concentrated in one specific claimed-but-unverified capability.

### Architecture Patterns
1. **Capability certification as a gating service**: Architect task routing so the orchestrator must query a capability-certification service (tracking verified, benchmark-tested capabilities per agent) before routing, rather than reading capability claims directly from agent self-description metadata.
2. **Confidence-gated routing with escalation on uncertainty**: Require agents to report calibrated confidence alongside their output, and route low-confidence outputs (or outputs from agents without high-confidence certification in that domain) to a secondary specialist or human reviewer rather than accepting the first response as final.
3. **Staged trust-level infrastructure**: Build task routing around explicit trust tiers per agent-capability pair (untested, provisionally-trusted, fully-trusted) with automated promotion/demotion based on tracked outcome accuracy, rather than a binary trusted/untrusted model.

### Metrics
1. **certified_capability_coverage**: Target: 100% of routed task categories have benchmark-certified agents; Alert if any task category is routed to an uncertified agent
2. **confidence_calibration_error**: Target: < 0.1 Expected Calibration Error per agent per capability; Alert if > 0.25 (signals overconfident misrepresentation)
3. **claimed_vs_actual_success_rate_gap**: Target: < 10 percentage points; Alert if gap exceeds 25 points for any agent-capability pair
4. **recertification_cadence_compliance**: Target: 100% of active capabilities re-certified within the defined interval (e.g., quarterly or after any model update); Alert on any lapsed certification

### Alerts
1. **Uncertified Capability Routing** (P1): Condition - a task is routed to an agent for a capability lacking valid benchmark certification. Action: Block the routing, escalate to a certified agent or human reviewer, investigate how the routing bypassed the certification gate.
2. **Confidence-Accuracy Divergence** (P1): Condition - an agent reports high confidence while its actual accuracy for that capability falls below threshold. Action: Suspend the agent from that capability's delegate pool, treat outputs from the affected period as suspect and route for re-review.
3. **Certification Lapse** (P2): Condition - a capability certification exceeds its revalidation interval without re-testing. Action: Suspend routing to that capability until re-certification completes.

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Specification failures
- [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) - Capability mismatch patterns
- [AugmentCode: Multi-Agent Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - Role specification
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Production failure analysis
