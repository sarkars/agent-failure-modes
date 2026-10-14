# Accuracy AI Agent Failures by Goal: 66 Patterns, Causes, and Fixes

**Accuracy AI agents fail in 8 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 66 documented patterns across 8 goals; the most documented is [Output Accuracy](output-accuracy/) with 16.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## Accuracy Goals

| Goal | When it fails | Patterns |
|---|---|---|
| [Context Management](context-management/) | Agents lose or misapply context over long conversations because system instructions become proportionally smaller as conversation history grows | 8 |
| [Evaluation Reliability](evaluation-reliability/) | Agents pass evaluation on golden datasets but fail systematically in production because the test dataset doesn't represent production's actual distribution, contains stale or mislabeled data | 8 |
| [Knowledge Staleness](knowledge-staleness/) | When policies, rules, thresholds, or regulatory requirements change after the model's training cutoff, the agent applies outdated values and makes incorrect decisions. | 1 |
| [Output Accuracy](output-accuracy/) | When parametric knowledge lacks evidence, input is ambiguous, or the model defaults to learned patterns over retrieval | 16 |
| [Output Optimization](output-optimization/) | Agents have access to known techniques that improve accuracy | 5 |
| [Output Verification](output-verification/) | When the upstream source is stale, corrupted, or incorrect, re-querying returns the same wrong value — the agent reports "verified correct" with false confidence | 1 |
| [Reasoning Quality](reasoning-quality/) | When execution reveals the gap. | 12 |
| [Verification](verification/) | When a second opinion would catch them). | 15 |

**Total: 66 patterns**

## Frequently Asked Questions

### How does output accuracy differ from hallucination?

Hallucination is one class of output accuracy failures — false content generated from patterns. See [Output Accuracy](output-accuracy/).

### How does verification differ from output accuracy?

Output accuracy covers generation of false outputs (hallucination, bias). See [Verification](verification/).

### How does reasoning quality differ from output accuracy failures?

Output accuracy failures cover hallucination and fabrication (generation of false facts). See [Reasoning Quality](reasoning-quality/).

## Related

- [Accuracy overview](../)
- [All agent failure patterns](../../../)
