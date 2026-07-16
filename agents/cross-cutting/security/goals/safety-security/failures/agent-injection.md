# Agent Injection

## Issue: Malicious Agent Introduction

**Frequency**: Emerging (Multi-Agent Systems)

**Symptoms**
- Unexpected agents appearing in multi-agent workflows
- Legitimate workflows producing unexpected outputs
- Consensus-based systems producing biased results
- New agent behavior doesn't match expected patterns

**Root Cause**
A threat actor introduces new malicious agents into an existing multi-agent system with the intent of performing malicious actions or having a detrimental impact on the system. Unlike agent compromise (taking over existing agents), agent injection adds entirely new malicious components.

**Example**
```
Multi-agent system: 5 agents vote on content moderation decisions

Attack: Threat actor injects 10 new agents, each instructed to vote "approve"

Result: Consensus model now heavily weighted toward approval
        Harmful content passes moderation 15-5
```

**Attack Vectors**
- Gaining access to code defining the agentic system and adding new agent
- Exploiting agent registration mechanisms
- Manipulating agent discovery services
- Poisoning agent provisioning pipelines

**Potential Effects**
- Agent misalignment with intended purpose
- Data exfiltration via injected agent
- Manipulation of system decisions
- Denial of service through resource consumption

---

## Test Scenario & Reproduction

### Scenario Setup
- A multi-agent workflow with a fixed, expected roster (e.g., 5 voting agents for content moderation)
- No cryptographic identity check or registry enforcement on workflow participation
- Agent registration/discovery mechanism reachable by more principals than strictly necessary

### Trigger Mechanism
1. Register additional agent instances against the same discovery/registration mechanism the legitimate agents use, configured to always vote a fixed way
2. Have the injected agents join the next workflow execution alongside the legitimate roster
3. Observe whether the workflow validates participant count/identity before tallying the consensus result

**Example Reproduction Steps:**
```
1. Stand up a 5-agent consensus workflow (e.g., content moderation voting)
2. Register 10 additional agent instances via the same provisioning path, each hardcoded to vote "approve"
3. Submit a piece of content that the legitimate 5 agents would reject 5-0
4. Observe the tallied consensus result
5. Check: did the workflow detect that 15 agents voted instead of 5?
6. Measure: consensus outcome (expected reject, injected-agent scenario approves 10-5)
```

### Expected Failure State
- Workflow executes and tallies votes from all 15 agents with no roster-mismatch error
- Consensus outcome flips from the expected reject to approve
- No alert fires despite 3x the expected agent count participating
- Audit trail shows no distinction between legitimate and injected agents

---

## Mitigation Strategies

### Prevention
1. **Allowlisted agent registry with fixed expected membership**: Maintain an explicit, version-controlled registry of authorized agents for each multi-agent workflow (e.g., "exactly 5 voting agents for content moderation") and reject any workflow execution whose participant count or identity set deviates from the registry, since the root cause is a threat actor introducing entirely new components into a system with no such check. Trade-off: legitimate scaling of the agent pool (adding a 6th moderator) now requires an explicit registry-update step rather than dynamic self-registration.
2. **Cryptographically signed agent identity for workflow participation**: Require every agent to present a cryptographic identity (signed certificate/key) issued by a trusted authority before it can join a workflow or cast a vote, so an attacker who gains code-level access to add an agent still cannot make it a *recognized* participant without also compromising the signing authority. Trade-off: adds key-management overhead and a dependency on a secure certificate-issuance process, which itself becomes a target.
3. **Restricted access controls on agent provisioning pipelines**: Lock down who/what can register a new agent instance or modify agent discovery services to a small, audited set of principals, directly closing the "Exploiting agent registration mechanisms" and "Poisoning agent provisioning pipelines" attack vectors named in the file. Trade-off: slows down legitimate operational agility (e.g., quickly spinning up a new agent for an incident) since provisioning now requires going through the restricted, audited path.

### Detection & Response
1. **Real-time agent-count and identity reconciliation**: Continuously compare the live count and identity set of agents participating in a workflow against the registry baseline, triggering an immediate halt when a mismatch is found — directly catching the documented scenario where 10 unauthorized agents joined a 5-agent voting system.
2. **Consensus-outcome shift monitoring**: Track the statistical distribution of consensus outcomes over time (e.g., historical approve/deny ratios for content moderation) and flag sudden shifts like the 15-5 approval skew in the example, since a coordinated block of injected agents voting identically produces a detectable deviation from historical baselines.
3. **Unknown-agent-ID correlation with network/resource activity**: When an unrecognized agent ID appears in workflow logs, immediately correlate it against network connections and resource consumption from that agent instance to assess whether it's performing data exfiltration or denial-of-service, per the "Potential Effects" listed in the file.

### Architecture Patterns
1. **Consensus quorum bound to a cryptographically verified fixed roster**: Architect the voting/consensus mechanism to only count votes from agents whose identity is verified against the fixed roster at vote-tally time, not just at session start, so injected agents cannot participate even if they briefly join the process.
2. **Isolated agent-provisioning control plane**: Separate the control plane that provisions/registers agents from the runtime plane that executes workflows, with independent access controls on each, so compromising the runtime environment doesn't automatically grant the ability to inject new registered agents.
3. **Immutable, append-only agent-membership audit trail**: Record every agent addition, removal, and identity change to an append-only log independent of the agent system itself, ensuring that even a successful injection attack leaves an unerasable record for post-incident investigation.

### Metrics
1. **agent_roster_deviation_count**: Target: 0 discrepancies between live agent count/identity and the registry baseline; Alert on any deviation
2. **consensus_outcome_drift_score**: Target: outcomes stay within historical statistical bounds; Alert on any statistically significant shift (e.g., >2 standard deviations from baseline)
3. **unauthorized_registration_attempt_rate**: Target: 0 agent registrations from principals outside the restricted provisioning access list; Alert on any attempt
4. **unknown_agent_id_occurrence_rate**: Target: 0 unrecognized agent IDs appearing in workflow logs; Alert on any occurrence

### Alerts
1. **Agent Roster Mismatch Detected** (P1): Condition - live participating agent count/identity set diverges from the registered baseline for a workflow. Action: Halt the workflow immediately, quarantine unrecognized agents, investigate the provisioning pipeline for compromise.
2. **Consensus Outcome Anomaly** (P2): Condition - voting/consensus results shift significantly from historical baseline distribution. Action: Suspend automatic action on the consensus result, manually review recent votes and agent roster, re-run with verified-only agents.
3. **Unauthorized Agent Registration Attempt** (P1): Condition - an agent registration or discovery-service modification is attempted by a principal outside the approved provisioning access list. Action: Block the registration, alert security team, audit recent provisioning pipeline changes for tampering.

## References

## References

- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Agent injection defined as novel security failure mode
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Multi-agent system failure taxonomy
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) - Agent security vulnerabilities
