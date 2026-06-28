# Stale Training Knowledge of Revoked Certification Scheme

## Issue: A Supplier-Onboarding Agent Verifying a Prospective Supplier's Compliance Certification Answers Whether the Certification Is Currently Valid From Facts Memorized During Pretraining Rather Than Calling a Live Certification-Registry Tool It Has Available, Approving a Credential Issued Under a Scheme That Has Since Been Revoked, Superseded, or Had Its Issuing Body Decertified

**Frequency**: Occasional

**Symptoms**
- Agent approves a supplier's certification document as valid based on the certification scheme's name and issuing body being recognized as legitimate from general training knowledge, without calling the live certification-registry tool available in its toolset
- The certification scheme, in fact, was decertified, merged into a successor standard, or had its issuing body's accreditation revoked after the model's training cutoff, a fact the live registry tool would have surfaced
- Re-running the same verification with an explicit instruction to call the certification-registry tool before approving produces the correct, current answer, isolating the failure to the agent defaulting to memorized knowledge rather than the tool being unavailable
- The error concentrates on certification schemes with a recent revocation, merger, or accreditation change, where the gap between the model's training cutoff and the current registry state is largest
- A supplier is onboarded on the strength of a credential that would not pass current procurement compliance standards, discovered only during a later audit or a downstream customer's supply-chain compliance review

**Root Cause**
The model's pretraining corpus encodes the certification landscape as it existed up to its training cutoff, and absent an explicit instruction or workflow step forcing a live registry lookup, the model defaults to answering from this memorized snapshot because the certification scheme's name and issuing body are immediately recognizable and the verification question's surface form does not itself signal that the underlying registry state is time-sensitive. The agent has a live certification-registry tool available specifically to avoid this, but nothing in the default workflow requires the agent to prefer the tool's output over its own memorized recognition when the two would conflict.

**Example**
```
Onboarding request: "Verify that [Certification Scheme X] presented by the prospective supplier is a currently valid, accredited certification"
Agent recognizes the certification scheme name and issuing body from training knowledge and responds: "Yes, this is a recognized, accredited certification," consistent with the scheme's status as of the model's training cutoff
The scheme's issuing body, in fact, had its accreditation revoked after the model's training cutoff, following a standards-body audit, which a live certification-registry lookup available to the agent would have surfaced
Supplier is approved and onboarded on the strength of the now-invalid certification
A downstream customer's supply-chain compliance audit later flags the certification as unaccredited, exposing the buyer to compliance risk in their own customer relationships
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Surveys of LLM agents in business and operational contexts identify reliance on static, pretraining-encoded knowledge -- rather than live registry or database sources -- as a specific, named failure category for time-sensitive verification tasks | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use calibration research notes that agents with retrieval tools available do not reliably prefer tool-grounded answers over parametric knowledge unless workflow design explicitly forces the preference | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |
| Retrieval reliability research finds that ungrounded reliance on memorized knowledge for time-sensitive facts is a recurring failure mode distinct from retrieval returning a wrong document | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |

**Contributing Factors**
- Workflow does not require the agent to call the certification-registry tool before approving a certification as currently valid, leaving the choice to the model's own judgment about whether a lookup is needed
- The verification question's surface form (recognizing a certification scheme's name and issuing body) does not signal to the model that the underlying registry status is time-sensitive
- No automated check compares the agent's stated validity conclusion against the most recent registry status for the cited certification scheme before the supplier is approved

---

## Mitigation Strategies

1. **Mandatory Registry Lookup for Every Certification Verification**: Require any certification-validity determination to be preceded by a logged call to the live certification-registry tool, and block the determination from being used in onboarding if no such call occurred
2. **Recency Flag on All Certification Conclusions**: Require the agent to explicitly state the as-of date of the registry source it relied on, making it visible when a conclusion is based on memorized knowledge with no stated current source
3. **Automated Cross-Check Against Current Registry Status**: Before a supplier is approved, automatically diff the agent's stated certification-validity rationale against the current registry record retrieved from the certification database, flagging any conflict
4. **Maintain a Recently-Revoked Schemes Watchlist**: Maintain and surface to the agent a running list of certification schemes with recent revocations, mergers, or accreditation changes, forcing a mandatory lookup specifically for any scheme on the watchlist

### Metrics
- Rate of certification-validity determinations made without a logged registry-lookup tool call
- Number of onboarded suppliers later found to hold a certification that conflicted with a registry change predating the onboarding date
- Percentage of certification conclusions that include an explicit as-of date for their cited registry source

### Alerts
- A supplier is approved with a certification on the recently-revoked schemes watchlist and no logged registry-lookup call → P1
- Automated cross-check finds the agent's stated certification-validity rationale conflicts with the current registry record and the supplier proceeds to approval → P1
- A certification-validity conclusion is generated with no as-of date for its source → P2

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
