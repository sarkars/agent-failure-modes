# [Failure Pattern Name]

## Issue: [One-line description]

**Frequency**: [Very Common | Common | Occasional | Rare]

**Symptoms**
- Symptom 1
- Symptom 2
- Symptom 3

**Root Cause**
[Explanation of why this failure occurs at a technical level]

**Example**
```
[Concrete scenario showing the failure in action]
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Statistic 1 | Source 1 |
| Statistic 2 | Source 2 |

**Contributing Factors**
- Factor 1
- Factor 2
- Factor 3

---

## Eval Recipes

How to test for this failure before it reaches production.

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Test 1 | [input] | [expected output] | [what indicates failure] |
| Test 2 | [input] | [expected output] | [what indicates failure] |

### Evaluation Dataset
- **Source**: [Where to get test data]
- **Size**: [Recommended dataset size]
- **Key variations**: [What variations to include]

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Metric 1 | [threshold] | [measurement method] |
| Metric 2 | [threshold] | [measurement method] |

### Automated Checks
```python
# Example evaluation code or pseudocode
def check_for_failure(output):
    # Detection logic
    pass
```

---

## Mitigation Strategies

How to prevent or reduce the impact of this failure.

### Prevention
1. **Strategy 1**: Description
2. **Strategy 2**: Description

### Detection & Response
1. **Strategy 1**: Description
2. **Strategy 2**: Description

### Architecture Patterns
- Pattern 1: Description
- Pattern 2: Description

---

## Production Signals

What to monitor in production to detect this failure.

### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Metric 1 | What it measures | When to alert |
| Metric 2 | What it measures | When to alert |

### Logs & Traces
- Log pattern 1 to watch for
- Trace attribute to monitor

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Alert 1 | [trigger condition] | [P1/P2/P3] | [response action] |

### Dashboard Panels
- Panel 1: [What to visualize]
- Panel 2: [What to visualize]

### Health Checks
```
# Example health check query or command
```

---

## References

- [Reference 1](url) - Description
- [Reference 2](url) - Description
