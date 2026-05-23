# Silent Data Errors

## Issue: Correct-Looking Wrong Data

**Frequency**: Very Common

**Symptoms**
- Pipeline completes successfully
- No errors logged or alerts triggered
- Data appears valid but is incorrect
- Discovered only through audits or customer complaints

**Root Cause**
The worst OCR failures are not the ones that throw errors - they are silent failures where the output looks correct, no errors are flagged, and the extraction completes successfully, but the data relationships are wrong.

**Example**
```
Input: Invoice with two tables - "Items Ordered" and "Items Backordered"

Pipeline output:
- Item: Widget A, Qty: 10, Status: Ordered
- Item: Widget B, Qty: 5, Status: Ordered

Actual:
- Widget A: 10 ordered
- Widget B: 5 backordered (from wrong table)

Result: Inventory system expects shipment that's actually backordered
```

**Key Statistic**
88% of businesses still report errors in their data pipelines, with teams spending six or more hours per week fixing "automated" data.

**Mitigation Strategies**
1. **Dual extraction paths**: Compare independent extraction methods
2. **Business rule validation**: Apply domain-specific sanity checks
3. **Statistical monitoring**: Track distribution shifts in extracted values
4. **Sample auditing**: Regularly verify random samples against source
5. **Customer feedback loops**: Make it easy to report extraction errors
