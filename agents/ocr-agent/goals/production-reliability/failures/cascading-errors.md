# Cascading Downstream Errors

## Issue: Cascading Downstream Errors

**Frequency**: Common

**Symptoms**
- Single extraction error corrupts multiple downstream systems
- Error propagates before detection
- Cleanup requires touching many systems

**Root Cause**
Automation moves data faster - meaning bad inputs create even bigger issues downstream. Errors in GL coding, invoice matching, or field mapping propagate across financial reports and compliance processes in real time.

**Example**
```
OCR extracts vendor: "ABC Corp" (actual: "ABG Corp")

Downstream impact:
- Payment routed to wrong vendor in AP system
- Spend analytics misattribute purchase
- Tax reporting shows incorrect vendor payments
- Audit flags unexplained vendor discrepancy
```

**Mitigation Strategies**
1. **Validation gates**: Verify before each integration point
2. **Soft deletes**: Keep original data recoverable
3. **Batch boundaries**: Limit blast radius of errors
4. **Rollback capabilities**: Enable reversal of bad data pushes
