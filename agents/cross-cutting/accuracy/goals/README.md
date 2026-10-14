# Accuracy AI Agent Failures by Goal: 66 Patterns, Causes, and Fixes

**Accuracy failures in AI agents are grouped here into 8 goals, each with a catalog of named failure patterns, the symptoms you will see, the root cause, and mitigations you can copy.** Start from the symptom you are debugging, pick the matching goal below, and open its failure list.

## Key Takeaways

- This cross-cutting concern covers 8 goals and 66 documented failure patterns.
- The largest goal is [Output Accuracy](output-accuracy/) with 16 patterns.
- Each goal page explains the failure class, how to tell it apart from its neighbors, and which mitigations apply across its patterns.
- Each failure page covers the symptoms, an example, the root cause, and how to fix it.

## Accuracy Goals

| Goal | What goes wrong | Patterns |
|---|---|---|
| [Context Management](context-management/) | Agents lose or misapply context over long conversations because system instructions become proportionally smaller as conversation history grows, conflicting instructions from multiple sources lack a declared resolution order | 8 |
| [Evaluation Reliability](evaluation-reliability/) | Agents pass evaluation on golden datasets but fail systematically in production because the test dataset doesn't represent production's actual distribution, contains stale or mislabeled data, or measures the wrong metrics | 8 |
| [Knowledge Staleness](knowledge-staleness/) | Agents with access to live lookup tools default to stale training-era knowledge instead of querying the tools | 1 |
| [Output Accuracy](output-accuracy/) | Agents generate plausible but false content when parametric knowledge lacks evidence, input is ambiguous, or the model defaults to learned patterns over retrieval | 16 |
| [Output Optimization](output-optimization/) | Agents have access to known techniques that improve accuracy (confidence calibration, abstention on low-confidence answers, deterministic verification, self-reflection before high-stakes output) but these techniques aren't applied | 5 |
| [Output Verification](output-verification/) | Agents perform "verification" by re-querying the same upstream data source that provided the initial answer, so when the upstream source is stale, corrupted, or incorrect, re-querying returns the same wrong value | 1 |
| [Reasoning Quality](reasoning-quality/) | Agents break down complex tasks incorrectly, deviate from goals, violate domain rules, or fail to correct themselves because the reasoning process isn't grounded in verifiable prerequisites, domain constraints, or external feedback | 12 |
| [Verification](verification/) | Agents skip or perform inadequate verification of their own outputs, leaving errors undetected | 15 |

**Total: 66 patterns**

## Frequently Asked Questions

### Where do I start if my accuracy agent is failing?

Match the symptom to a goal in the table above, then open that goal's page for how to tell its failures apart and where to look first. Each failure page ends in mitigations you can apply directly.

### How are these accuracy failure patterns organized?

By goal: the outcome the agent is supposed to achieve. Under each goal, a `failures` folder holds one page per pattern. For the full picture see the [Accuracy overview](../).

## Related

- [Accuracy overview](../)
- [All agent failure patterns](../../../)
