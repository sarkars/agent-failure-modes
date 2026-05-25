# Domain Expert Agent

Agents that make **domain-specific judgments** requiring specialized knowledge (legal, medical, financial, regulatory).

## Goals

| Goal | Description | Patterns |
|------|-------------|----------|
| [Domain Decisions](goals/domain-decisions/) | Domain-correct decisions | 10 |

**Total: 10 patterns across 1 goal**

## Key Failure Modes

- **Regulatory threshold miss** - Missing compliance boundaries
- **Risk severity misclassification** - Wrong risk assessment
- **Domain rule miss** - Violating domain-specific rules
- **Source of truth confusion** - Using wrong authoritative source

## How to Use

1. **Identify domain expertise required** - Legal? Medical? Financial?
2. **Check failure patterns** - See if your agent exhibits these issues
3. **Apply mitigations** - Domain-specific validation and review
4. **Add human oversight** - Critical decisions need expert review

## Cross-References

- [Base Agent](../../base-agent/) - Cross-cutting patterns
- [Capability Agents](../) - Other capability-based patterns
