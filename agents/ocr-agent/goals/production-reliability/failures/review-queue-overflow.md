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

**Mitigation Strategies**
1. **Confidence calibration**: Tune thresholds based on actual accuracy
2. **Prioritized review**: Process time-sensitive documents first
3. **Partial automation**: Auto-fill high-confidence fields, review only uncertain ones
4. **Feedback loops**: Learn from corrections to reduce future review
