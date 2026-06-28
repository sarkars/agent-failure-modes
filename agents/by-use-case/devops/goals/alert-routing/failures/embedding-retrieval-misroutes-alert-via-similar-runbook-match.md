# Embedding Retrieval Misroutes Alert via Similar Runbook Match

## Issue: An Alert-Routing Agent That Decides Which Team to Page by Retrieving the Most Semantically Similar Past Incident Runbook for the Incoming Alert Text Pulls a Lexically Similar but Substantively Different Runbook -- Written for a Different Service With Overlapping Error-Message Vocabulary -- and Pages the Wrong Team

**Frequency**: Occasional

**Symptoms**
- An alert containing a generic error signature ("connection timeout," "5xx spike," "queue depth exceeded") is routed based on the runbook whose past incident description is most lexically similar, regardless of whether that runbook's service actually matches the alerting service
- The paged team reports the alert is "not ours" and re-routes manually, after which the correct team resolves it using a different runbook than the one the agent retrieved
- Re-running the same alert text through retrieval with the service name added explicitly as a filter (rather than relying on free-text similarity alone) returns the correct runbook, isolating the failure to retrieval scope rather than the correct runbook being absent
- Misroutes cluster on alert types with generic, widely reused error vocabulary (timeouts, connection resets, generic 5xx errors) shared across many services' runbooks, where lexical similarity is highest and service-specificity is least encoded in the text
- On-call fatigue increases for teams that are frequently paged via this misroute pattern for alerts that are never actually theirs

**Root Cause**
The routing agent selects a runbook by embedding similarity over free-text incident descriptions rather than first filtering by structured service ownership metadata, so two runbooks describing similar-sounding symptoms (a generic connection timeout) for two entirely different services can sit close together in embedding space. The agent has no signal distinguishing "describes a similar-sounding problem" from "is the runbook for the service that's actually alerting," because the retrieval step never constrains the candidate set to runbooks tagged with the alerting service before ranking by similarity.

**Example**
```
Incoming alert: "connection timeout spike on checkout-service, p99 latency 8s"
Retrieval over the runbook library by semantic similarity returns the highest-scoring match: a runbook titled "Connection Timeout Spike Investigation" written for a different service, inventory-service, with similar generic symptom language
Routing agent pages the inventory-service on-call team based on this match
Inventory-service team confirms their systems are healthy and the alert is unrelated; checkout-service's actual on-call team is paged only after manual re-routing, adding several minutes to time-to-engagement
Postmortem finds the correct checkout-service runbook existed in the library but scored lower on semantic similarity due to differences in how its symptom description was originally written
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM orchestration for incident response is evaluated specifically against deterministic routing accuracy, underscoring that similarity-based matching without structured constraints is a known gap relative to ownership-grounded routing | [Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response](https://arxiv.org/pdf/2511.15755) |
| Retrieval reliability research finds that semantically similar but substantively different documents are frequently confused by similarity-only retrieval when structured filtering is unavailable | [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1) |
| Tool-use calibration research notes that retrieval-grounded agent actions require independent verification against structured ground truth (e.g., service ownership), not similarity scores alone | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |

**Contributing Factors**
- Runbook retrieval ranks candidates by free-text semantic similarity without first filtering to runbooks tagged with the alerting service's structured ownership metadata
- Generic error vocabulary (timeouts, 5xx spikes) is shared across many services' runbooks, maximizing embedding-space proximity between substantively unrelated incidents
- No automated check compares the retrieved runbook's tagged service against the alert's actual originating service before the page is sent

---

## Mitigation Strategies

1. **Structured Service Filter Before Semantic Ranking**: Require the retrieval step to filter candidate runbooks to those tagged with the alert's actual originating service (from monitoring metadata, not free text) before ranking by semantic similarity
2. **Service-Match Verification Gate**: Before paging, automatically verify the retrieved runbook's tagged service matches the alerting service, and block the page (routing to a default escalation path instead) if they do not match
3. **Symptom-Vocabulary Disambiguation for Generic Alerts**: For alert types known to share generic vocabulary across many services (timeouts, 5xx spikes), require an additional structured signal (affected endpoint, dependency graph) beyond free-text similarity before selecting a runbook
4. **Misroute Tracking by Alert-Type**: Track the rate of manual re-routes following an automated page, segmented by alert type, to identify which generic-vocabulary alert types are most prone to this failure and prioritize fixes there

### Metrics
- Rate of automated pages followed by a manual re-route within a defined window, segmented by alert type
- Percentage of runbook retrievals where the top semantic match's tagged service does not match the alerting service
- Mean time-to-correct-engagement for alerts that are initially misrouted versus correctly routed

### Alerts
- Automated page is sent to a team whose runbook's tagged service does not match the alerting service → P2
- Manual re-route rate for a given alert type exceeds baseline for two consecutive reporting periods → P2
- A new alert-routing workflow is deployed using free-text similarity retrieval with no structured service filter → P3

---

## References

- [Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response](https://arxiv.org/pdf/2511.15755)
- [Towards Reliable Retrieval in RAG Systems for Large Legal Datasets](https://arxiv.org/html/2510.06999v1)
- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
