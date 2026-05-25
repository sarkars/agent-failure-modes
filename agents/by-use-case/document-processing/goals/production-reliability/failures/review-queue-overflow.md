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

## References

- [IDP Accuracy Reckoning 2026](https://idp-software.com/news/idp-accuracy-reckoning-2026/) - Automation rate targets
- [AI Agents and Document Processing 2026](https://parsio.io/blog/ai-agents-document-processing-2026) - Human-in-the-loop optimization
- [Production-Ready AI Agent for Document Extraction](https://www.stackai.com/insights/how-to-build-a-production-ready-ai-agent-for-document-data-extraction) - Review queue management
