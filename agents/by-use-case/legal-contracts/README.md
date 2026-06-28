# Legal & Contract Analysis

Agents reviewing contracts, flagging compliance issues, and extracting obligations face domain-specific failures around jurisdiction, precedent, and multi-party obligations.

## Goals

| Goal | Description | Patterns |
|------|-------------|----------|
| [Jurisdiction Compliance](goals/jurisdiction-compliance/) | Jurisdiction detection, applicable law, cross-border rules | In progress |
| [Precedent Currency](goals/precedent-currency/) | Outdated case law, overturned rulings, jurisdiction-specific precedent | In progress |
| [Obligation Tracking](goals/obligation-tracking/) | Multi-party obligations, conditional clauses, cross-document consistency | In progress |

**Status**: ~40 patterns planned

## Key Challenges

1. **Jurisdiction Complexity**: Same contract word means different things in different jurisdictions
2. **Knowledge Staleness**: Case law changes; reversals not captured
3. **Clause Structure**: Complex conditionals, severability, choice-of-law buried in text
4. **Multi-Party Semantics**: Obligation asymmetry hard to spot
5. **Regulatory Drift**: Laws change; versions not tracked
