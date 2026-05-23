# Character Confusion

## Issue: Visually Similar Character Substitution

**Frequency**: Very Common

**Symptoms**
- Numbers appear in text fields, letters appear in numeric fields
- Validation fails on extracted data that "looks correct"
- Downstream calculations produce unexpected results

**Root Cause**
Many characters are visually similar, especially in certain fonts or at low resolutions. The model cannot distinguish between them without additional context.

**Commonly Confused Characters**

| Characters | Context Where Confusion Occurs |
|------------|-------------------------------|
| `0` / `O` / `o` | Alphanumeric codes, serial numbers |
| `1` / `l` / `I` / `|` | IDs, license plates, codes |
| `5` / `S` | Codes, amounts |
| `8` / `B` | Alphanumeric sequences |
| `2` / `Z` | Handwritten forms, fax copies |
| `6` / `G` | Low-resolution scans |
| `rn` / `m` | Narrow fonts, small text |
| `cl` / `d` | Serif fonts |
| `vv` / `w` | Stylized fonts |

**Example**
```
Input Image: Invoice #INV-2024-O1523
Expected: INV-2024-O1523 (letter O)
Actual: INV-2024-01523 (digit 0)

Result: Invoice lookup fails because ID doesn't exist
```

**Mitigation Strategies**
1. **Field-type validation**: If a field should be numeric-only, flag alphabetic characters
2. **Regex patterns**: Define expected formats (e.g., `INV-\d{4}-[A-Z]\d{4}`)
3. **Checksum validation**: Use check digits for critical IDs
4. **Confidence thresholding**: Flag characters with low confidence for review
5. **Context-aware post-processing**: Use domain dictionary to correct likely errors

**Detection**
- Monitor field validation failure rates by field type
- Track "manual correction" rates in human review queues
- A/B test extraction against ground truth samples
