# Vision and Images AI Agent Failures by Goal: 43 Patterns, Causes, and Fixes

**Vision and Images failures in AI agents are grouped here into 5 goals, each with a catalog of named failure patterns, the symptoms you will see, the root cause, and mitigations you can copy.** Start from the symptom you are debugging, pick the matching goal below, and open its failure list.

## Key Takeaways

- This capability covers 5 goals and 43 documented failure patterns.
- The largest goal is [Spatial Reasoning](spatial-reasoning/) with 14 patterns.
- Each goal page explains the failure class, how to tell it apart from its neighbors, and which mitigations apply across its patterns.
- Each failure page covers the symptoms, an example, the root cause, and how to fix it.

## Vision and Images Goals

| Goal | What goes wrong | Patterns |
|---|---|---|
| [Adversarial Robustness](adversarial-robustness/) | Vision models lose accuracy when input images deviate from the conditions they were trained on | 6 |
| [Generation Artifacts](generation-artifacts/) | Generated-image quality degrades over repeated generation or regeneration because generative models sample stochastically with no built-in mechanism to preserve quality, identity, or semantic intent across iterations | 7 |
| [Multi Image Understanding](multi-image-understanding/) | Vision models process images independently by default, so when a task requires reasoning across several images — the same object from different angles, consecutive video frames, or several imaging modalities | 6 |
| [Spatial Reasoning](spatial-reasoning/) | Vision models get spatial relationships wrong because 2D image projection is fundamentally lossy for 3D properties | 14 |
| [Visual Hallucination](visual-hallucination/) | Vision-language models hallucinate objects, attributes, and entire scenes because they optimize for confident, contextually-plausible output rather than for grounding every claim in visible pixels | 10 |

**Total: 43 patterns**

## Frequently Asked Questions

### Where do I start if my vision and images agent is failing?

Match the symptom to a goal in the table above, then open that goal's page for how to tell its failures apart and where to look first. Each failure page ends in mitigations you can apply directly.

### How are these vision and images failure patterns organized?

By goal: the outcome the agent is supposed to achieve. Under each goal, a `failures` folder holds one page per pattern. For the full picture see the [Vision and Images overview](../).

## Related

- [Vision and Images overview](../)
- [All agent failure patterns](../../../)
