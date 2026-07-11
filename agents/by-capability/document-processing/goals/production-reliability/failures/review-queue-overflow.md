# Review Queue Overflow

## Issue: Human Review Queue Overflow

**Frequency**: Common

**Symptoms**
- Review queue grows faster than reviewers process
- SLAs missed on time-sensitive documents
- Reviewers rubber-stamp to clear backlog

**Root Cause**
When automation confidence is poorly calibrated or too conservative, too many documents route to human review, overwhelming capacity.

**Example**
```
Daily volume: 10,000 invoices
Automation rate: 85% (target: 95%)
Review queue: 1,500/day (target: 500/day)
Reviewer capacity: 600/day

Result: Queue grows by 900/day, 5-day backlog after one week
```

## Mitigation Strategies

### Prevention
1. **Empirically-calibrated confidence thresholds**: Set the auto-accept confidence threshold based on measured accuracy-per-confidence-bucket from ground-truth audits, not an arbitrary conservative default, since an overly conservative threshold routes far more documents to review than the actual accuracy risk justifies, directly causing queue overflow. Trade-off: requires ongoing calibration work and ground-truth data collection, and a threshold set too aggressively increases downstream error risk.
2. **Field-level partial automation instead of document-level**: Auto-accept individual high-confidence fields within a document while routing only the specific low-confidence fields to review, rather than sending an entire document to manual review because one field is uncertain — this can dramatically reduce reviewer workload per document since most fields in most documents are high-confidence. Trade-off: requires a review UI that supports partial/field-level correction rather than whole-document re-entry, which is more complex to build.
3. **Correction-feedback-driven threshold and model improvement loop**: Feed human corrections back into recalibrating confidence thresholds and, where applicable, retraining/fine-tuning extraction, so fields/document types that reviewers consistently don't need to correct get promoted to higher automation over time, shrinking the review queue's structural size. Trade-off: requires infrastructure to capture, aggregate, and act on correction data systematically rather than treating corrections as throwaway.

### Detection & Response
1. **Queue growth-rate monitoring against reviewer capacity**: Continuously track queue inflow rate versus reviewer processing capacity (not just current queue depth), since a queue that's growing net-positive will overflow regardless of its current size — this is a leading indicator that should trigger action before the backlog becomes unmanageable.
2. **Rubber-stamping detection**: Monitor reviewer decision patterns (time spent per document, correction rate, approval rate) for signatures of rubber-stamping under backlog pressure (e.g., near-instant approvals, unusually low correction rate compared to historical baseline), since a backlogged queue creates strong incentive for reviewers to approve without genuine verification, defeating the purpose of the review gate.
3. **SLA-risk prioritization within the queue**: Dynamically reprioritize the queue based on document time-sensitivity/SLA risk rather than pure FIFO, ensuring time-critical documents are processed first even when the aggregate queue is backlogged, so overflow degrades non-urgent processing before it causes SLA violations on urgent items.

### Architecture Patterns
1. **Field-level review UI with confidence-highlighted fields**: Build the review interface around individual low-confidence fields needing attention (with surrounding document context for reference) rather than a whole-document re-entry form, structurally enabling the field-level partial-automation strategy above.
2. **Dynamic threshold auto-tuning based on queue pressure and accuracy budget**: Architect threshold-setting as a continuously-tuned function of both measured accuracy-per-bucket and current queue pressure (within an acceptable accuracy-risk budget), rather than a static, manually-set value, so the system can absorb temporary volume spikes without either overflowing or accepting too much accuracy risk.
3. **Priority-queue architecture with SLA-aware scheduling**: Replace simple FIFO queue processing with an SLA-aware priority scheduler that considers document urgency, value, and age, so reviewer capacity is allocated to minimize business-impact-weighted backlog rather than simple document count.

### Metrics
1. **queue_net_growth_rate**: Target: <= 0 (queue shrinking or stable) on a rolling 7-day basis; Alert if net growth positive for > 3 consecutive days
2. **automation_rate_vs_target**: Target: within 3 percentage points of the target automation rate; Alert if actual rate falls > 8 points below target
3. **reviewer_rubber_stamp_signature_rate**: Target: < 5% of reviews show rubber-stamp signatures (near-instant approval, near-zero correction rate); Alert if > 15%
4. **sla_violation_rate_during_backlog**: Target: 0% of SLA-tagged documents miss SLA even during backlog periods; Alert on any occurrence

### Alerts
1. **Queue Growth Trend** (P2): Condition - review queue shows net positive growth for more than 3 consecutive days. Action: Recalibrate confidence thresholds upward (within accuracy-risk budget) or add reviewer capacity before backlog reaches SLA-risk levels.
2. **Rubber-Stamping Signature Detected** (P1): Condition - reviewer behavior metrics show a spike in rubber-stamp signatures correlated with queue backlog. Action: Treat review-queue output as unreliable for the affected period; audit a sample of "approved" documents from that window for actual accuracy.
3. **SLA Violation During Backlog** (P1): Condition - any SLA-tagged document misses its SLA due to queue backlog. Action: Immediately reprioritize the queue to protect remaining SLA-tagged documents; escalate for additional reviewer capacity or emergency threshold adjustment.

## References

- [IDP Accuracy Reckoning 2026](https://idp-software.com/news/idp-accuracy-reckoning-2026/) - Automation rate targets
- [AI Agents and Document Processing 2026](https://parsio.io/blog/ai-agents-document-processing-2026) - Human-in-the-loop optimization
- [Production-Ready AI Agent for Document Extraction](https://www.stackai.com/insights/how-to-build-a-production-ready-ai-agent-for-document-data-extraction) - Review queue management
