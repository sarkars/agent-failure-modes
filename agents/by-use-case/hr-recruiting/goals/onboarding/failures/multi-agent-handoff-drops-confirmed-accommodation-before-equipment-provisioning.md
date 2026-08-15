# Multi-Agent Handoff Drops Confirmed Accommodation Before Equipment Provisioning

## Issue: A Recruiting-Coordinator Agent's Conversation With a New Hire Establishes a Confirmed Workplace Accommodation (e.g., an Ergonomic Setup or Assistive Equipment Tied to a Documented Need) During the Pre-Start Conversation, but the Structured Handoff Record Passed to the Downstream Onboarding/IT-Provisioning Agent Omits the Accommodation Field, So the Provisioning Agent Ships Standard-Issue Equipment and the New Hire Arrives on Day One Without What Was Already Agreed

**Frequency**: Occasional

**Symptoms**
- The new hire's day-one shipment matches the standard role-based bundle rather than the accommodation that was explicitly discussed and confirmed before their start date
- The coordinator agent's chat log shows an unambiguous confirmation of the accommodation, and that confirmation is nowhere among the fields of the structured onboarding-task record the provisioning agent acted on
- The IT/Facilities ticket the provisioning agent generates shows only default SKUs for the role and location, with no accommodation flag set anywhere
- The new hire has to re-raise the same request after starting, and HR ends up processing it as a new, time-sensitive accessibility case instead of recognizing it as already settled
- Rereading the original pre-boarding conversation shows the accommodation was discussed and agreed without qualification — it wasn't tentative, it simply never reached the provisioning step

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
- The onboarding task schema was built around role, location, and a standard equipment bundle; it has no field representing an exception negotiated during the pre-boarding conversation
- The coordinator agent treats verbally confirming the accommodation in chat as the end of the task, with no subsequent step that writes the commitment into a field the provisioning agent will actually consult
- Provisioning defaults to the standard bundle for the hire's role and location unless told otherwise, and nothing in its instructions has it check for an unstructured exceptions note before doing so
- No step compares what was promised during pre-boarding against what the provisioning ticket actually requests, so a dropped commitment looks identical to a hire who never asked for anything

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
