# Multi-Agent Handoff Drops Confirmed Accommodation Before Equipment Provisioning

## Issue: A Recruiting-Coordinator Agent's Conversation With a New Hire Establishes a Confirmed Workplace Accommodation (e.g., an Ergonomic Setup or Assistive Equipment Tied to a Documented Need) During the Pre-Start Conversation, but the Structured Handoff Record Passed to the Downstream Onboarding/IT-Provisioning Agent Omits the Accommodation Field, So the Provisioning Agent Ships Standard-Issue Equipment and the New Hire Arrives on Day One Without What Was Already Agreed

**Frequency**: Occasional

**Symptoms**
- New hire's day-one equipment shipment matches the standard role-based provisioning template, not the accommodation discussed and confirmed during pre-boarding
- The recruiting-coordinator agent's chat transcript contains an explicit confirmation ("Yes, we'll have the sit-stand desk and the ergonomic keyboard ready for you") that never appears as a field in the structured onboarding-task record the provisioning agent acted on
- IT/Facilities ticket created by the provisioning agent shows only default SKU codes for the new hire's role and location, with no accommodation flag set
- New hire has to re-raise the same accommodation request after start date, which HR has to treat as a new, time-sensitive accessibility request rather than something already settled
- Re-reading the original pre-boarding conversation confirms the accommodation was discussed, agreed, and not marked tentative or pending

**Example**
```
Recruiting-coordinator agent's pre-boarding chat with new hire: hire mentions a documented
need for a sit-stand desk and ergonomic keyboard; agent confirms "Noted, we'll have this
ready for your first day"
Coordinator agent hands off to the onboarding/provisioning agent via a structured task
schema containing: start_date, role, location, manager, standard_equipment_bundle
The accommodation discussion exists only in the coordinator agent's free-text chat log,
which is not a field the structured handoff schema captures
Provisioning agent reads only the structured fields, generates a standard equipment
ticket for the role/location, and never sees the accommodation commitment
New hire arrives day one to a standard desk setup; has to file a new accessibility
request through HR, delaying resolution by over a week
Post-incident review finds the commitment was real and timely in the source
conversation -- it simply never crossed the agent-to-agent handoff boundary
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent system failures are frequently attributable to information loss at inter-agent handoff boundaries, where one agent's conversational context is not faithfully carried into the structured state the next agent consumes | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Execution-provenance research argues that without traceable links between an agent's claims and the upstream evidence that produced them, downstream agents and human reviewers cannot detect when a commitment made earlier was silently dropped | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |
| Tool-use error detection research finds agents rarely flag when an upstream input they consumed was incomplete relative to the full available context, instead proceeding as if the structured fields they received were the complete picture | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |

**Contributing Factors**
- The structured handoff schema between coordinator and provisioning agents has no field for accommodations, exceptions, or any commitment made in free-text conversation
- The coordinator agent treats confirming the accommodation in chat as equivalent to recording it, with no step that writes the commitment into a field the next agent will actually read
- The provisioning agent has no instruction to check for an unstructured "exceptions" note before defaulting to the standard equipment bundle
- No reconciliation step compares what was promised in the pre-boarding conversation against what the provisioning ticket actually requests before it ships

---

## Mitigation Strategies

1. **Structured Exception Field**: Add a mandatory accommodation/exception field to the coordinator-to-provisioning handoff schema; the coordinator agent cannot close out a pre-boarding conversation without explicitly setting it to "none" or describing the exception
2. **Commitment-to-Field Reconciliation**: Before provisioning, run an automated check that scans the coordinator agent's full chat transcript for accommodation-related commitments and flags any that do not appear in the structured record
3. **Human Confirmation for Accommodations**: Route any detected accommodation commitment to an HR reviewer for confirmation before the provisioning agent generates equipment tickets, rather than letting it flow through fully autonomously
4. **Day-Minus-Five Equipment Audit**: Require a manual or automated cross-check of the provisioning ticket against the original pre-boarding conversation a fixed number of days before start date, while there is still time to correct it

### Metrics
- Rate of new-hire equipment tickets that omit an accommodation or exception mentioned in the pre-boarding conversation
- Number of post-start-date accessibility requests that duplicate a commitment already made pre-boarding
- Time between original accommodation commitment and actual fulfillment

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Accommodation field empty with chat evidence present | Coordinator transcript contains accommodation language but handoff record's exception field is unset | P1 | Hold provisioning ticket; route to HR for manual confirmation |
| Standard bundle shipped against flagged profile | Equipment ticket uses default SKU set for a new hire whose pre-boarding record has any exception note | P2 | Cancel/amend ticket before fulfillment |
| Repeat post-start accommodation request | New hire files an accessibility request within 14 days of start date | P3 | Audit whether the request duplicates a pre-boarding commitment |

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
