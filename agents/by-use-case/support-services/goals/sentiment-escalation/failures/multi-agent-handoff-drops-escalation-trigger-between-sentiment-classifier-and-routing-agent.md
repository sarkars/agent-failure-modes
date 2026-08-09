# Multi-Agent Handoff Drops Escalation Trigger Between Sentiment-Classifier and Routing Agent

## Issue: A Sentiment-Classification Agent That Concludes, in Its Own Analysis, That a Ticket's Tone Indicates a High Risk of Customer Churn or Public Complaint Hands the Ticket Off to a Routing Agent Through a Structured Sentiment-Score Field That Falls Within the Routing Agent's Normal Range, So the Specific Escalation Reasoning the Classifier Reached Never Translates Into Priority Routing

**Frequency**: Occasional

**Symptoms**
- The classifier's write-up quotes the customer's exact words announcing an intended action -- posting publicly, canceling -- but the ticket's numeric score reflects the message's overall tone, which reads as only moderately negative once that one sentence is averaged against the rest
- A routing agent reading only the numeric field cannot distinguish this ticket from any other moderately negative ticket, since both land in the same score band and produce the same standard-queue outcome
- Tickets that go on to escalate publicly are found, on retrospective review, to have contained a named intent statement whose score fell just short of the routing threshold at a materially higher rate than tickets that don't escalate
- Lowering the general escalation threshold to catch these cases would also route large volumes of ordinary moderately negative tickets to expedited handling, so the fix isn't a threshold tweak -- it's a missing category of signal entirely
- Nobody notices the miss until the customer's stated action actually happens and a retrospective review pulls the original transcript

**Root Cause**
The numeric sentiment score is trained to summarize a message's tone as a whole, so a single sentence stating a concrete future action competes for weight against the rest of the message's more neutral phrasing and rarely moves the aggregate score past a fixed threshold on its own. The classifier's narrative reasoning can name that sentence specifically because reasoning operates over discrete statements, but the score is a single averaged number with no mechanism for one clause to override the rest of the message -- so a threshold tuned against typical negative-tone distributions systematically underweights exactly the tickets where the risk is concentrated in one explicit line rather than spread evenly across the whole tone.

**Example**
```
Sentiment-classification agent analyzes a ticket and reasons: "Customer's tone is moderately negative overall, but the specific statement 'if this isn't fixed by Friday I'm posting about it on social media and switching providers' is a distinct high-risk signal independent of general tone"
Classifier outputs a structured sentiment score of -0.4, which reflects the moderately negative overall tone but does not reach the routing agent's -0.7 escalation threshold
Routing agent routes the ticket to the standard queue based solely on the -0.4 score, with no visibility into the specific public-complaint-risk statement the classifier's analysis identified
Customer's stated deadline passes without resolution; they follow through on the stated intent, posting a public complaint that draws wider attention
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM systems exhibit a documented failure category where a determination established by one agent is lost or never reaches a downstream agent's effective input, distinct from either agent reasoning incorrectly on its own | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Business-scenario evaluations of LLM agents in CRM-adjacent tasks identify structured state propagation between conversational and routing agents as a distinct reliability requirement from either agent's individual task accuracy | [CRMArena-Pro: Holistic Assessment of LLM Agents Across Diverse Business Scenarios and Interactions](https://arxiv.org/abs/2505.18878) |
| CRM task-capability benchmarks for LLM agents identify routing and escalation decisions based on compressed, single-dimension signals as a distinct failure category from misclassification of sentiment itself | [CRMArena: Understanding the Capacity of LLM Agents to Perform Professional CRM Tasks in Realistic Environments](https://arxiv.org/html/2411.02305v2) |

**Contributing Factors**
- The handoff between the sentiment-classification agent and the routing agent compresses the classifier's full analysis into a single numeric score, with no separate structured field for specific, named risk signals
- The routing agent's escalation logic acts solely on the numeric score threshold, never on the classifier's underlying analysis text
- No reconciliation step compares specific risk-signal language in the classifier's analysis against the structured score before routing occurs

---

## Mitigation Strategies

1. **Structured Named-Risk-Signal Field Separate From Sentiment Score**: Extend the handoff schema to carry an explicit, structured flag for named high-risk signals (stated churn intent, stated public-complaint intent) independent of the general numeric sentiment score, and require the classification agent to populate it directly
2. **Hard Escalation Rule for Named Risk Signals**: Require any ticket flagged with a named high-risk signal to route to expedited or specialist handling regardless of its general numeric sentiment score
3. **Pre-Routing Risk-Signal Reconciliation Scan**: Before a routing decision is finalized, automatically scan the classification agent's analysis for named risk-signal language and flag any mismatch against the structured routing outcome
4. **Periodic Threshold Recalibration Against Named-Signal Outcomes**: Regularly review tickets containing named risk signals that did not cross the numeric escalation threshold, and use those cases to recalibrate either the threshold or the structured-field design

### Metrics
- Rate of tickets where the classification agent's analysis contains named high-risk-signal language not reflected in an escalation-triggering structured field
- Rate of churn or public-complaint outcomes traced back to a ticket whose named risk signal did not trigger escalation
- Time between a named risk-signal statement and the customer's actual follow-through (churn, public post), when it occurs

### Alerts
- A ticket containing a named high-risk signal in the classification analysis routes to a non-expedited queue → P1
- A customer follows through on a previously identified named risk signal that did not trigger escalation → P1
- Risk-signal reconciliation mismatch rate exceeds the defined threshold for a rolling window → P2

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [CRMArena-Pro: Holistic Assessment of LLM Agents Across Diverse Business Scenarios and Interactions](https://arxiv.org/abs/2505.18878)
- [CRMArena: Understanding the Capacity of LLM Agents to Perform Professional CRM Tasks in Realistic Environments](https://arxiv.org/html/2411.02305v2)
