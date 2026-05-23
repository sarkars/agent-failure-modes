# Punctuation Errors

## Issue: Punctuation and Special Character Errors

**Frequency**: Common

**Symptoms**
- Decimal points become commas (or vice versa) breaking numeric parsing
- Currency symbols misread or dropped
- Hyphens, dashes, and minus signs interchanged

**Root Cause**
Small punctuation marks are often damaged in scans or rendered differently across fonts. Regional formatting differences (`.` vs `,` for decimals) add ambiguity.

**Example**
```
Input Image: Total: $1,234.56
Expected: 1234.56
Actual: 1.23456 (comma interpreted as decimal)

Result: Invoice processed for wrong amount
```

**Mitigation Strategies**
1. **Locale-aware parsing**: Detect document locale and apply appropriate numeric formatting rules
2. **Sanity bounds**: Reject values outside expected ranges (e.g., invoice line item > $1M)
3. **Multiple extraction passes**: Extract raw string AND parsed numeric, compare
4. **Currency symbol detection**: Identify currency before parsing to infer format

**Detection**
- Unusual value distributions (many values < $1 when expecting larger amounts)
- Parsing exceptions in downstream systems
- Currency mismatch alerts
