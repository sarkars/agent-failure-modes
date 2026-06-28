# Multi-Jurisdiction Regulatory Conflict

## Issue: Portfolio or Strategy Compliant in One Jurisdiction but Violates Rules in Another; Model Doesn't Handle Jurisdiction-Specific Rules

**Frequency**: Common

**Symptoms**
- Strategy approved by SEC (US), violates BaFin rules (Germany)
- Model applies US rules globally (or picks wrong jurisdiction)
- Regulatory arbitrage backfires (client sanctioned, not just fined)
- No jurisdiction-specific rule branching in code

**Root Cause**
Global financial institutions operate across jurisdictions with different rules. Model trained on single jurisdiction's rules doesn't know about others. Client location, asset domicile, and regulatory oversight all matter. Hard to encode all rules globally.

**Example**
```
Scenario: Global asset manager with US and EU clients
Leverage strategy: 50% margin allowed in US, 20% max in EU
Model deployed globally: Applies 50% margin to both
US clients: Fine (rule compliant)
EU clients: Violate MiFID II leverage limits
Impact: Sanctions, fines, client compensation
```

**Key Statistics**
- Regulatory jurisdictions: 50+ major (US, EU, UK, HK, SG, etc.)
- Rule overlap: 30-50% consistency across jurisdictions
- Conflict rate: 20-40% of complex strategies

---

## Mitigation Strategies

1. **Jurisdiction Tagging**: All clients/assets tagged with primary jurisdiction
2. **Rule Branching**: Model logic includes if/else for jurisdiction-specific rules
3. **Conflict Detection**: Automated check for violations across all relevant jurisdictions
4. **Legal Review**: Complex strategies reviewed by legal in each jurisdiction

### Metrics
- Compliance rate by jurisdiction (should be >99%)
- Multi-jurisdiction conflicts detected (should trend to zero)

### Alerts
- Strategy violation in any jurisdiction → P1

---

## References

- [Cross-Border Regulatory Compliance](https://arxiv.org/abs/2112.05503)
- [Regulatory Arbitrage Detection](https://arxiv.org/abs/2206.00851)
