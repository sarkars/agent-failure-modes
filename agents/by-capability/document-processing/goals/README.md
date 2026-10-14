# Document Processing AI Agent Failures by Goal: 46 Patterns, Causes, and Fixes

**Document Processing failures in AI agents are grouped here into 6 goals, each with a catalog of named failure patterns, the symptoms you will see, the root cause, and mitigations you can copy.** Start from the symptom you are debugging, pick the matching goal below, and open its failure list.

## Key Takeaways

- This capability covers 6 goals and 46 documented failure patterns.
- The largest goal is [Multimodal Reliability](multimodal-reliability/) with 10 patterns.
- Each goal page explains the failure class, how to tell it apart from its neighbors, and which mitigations apply across its patterns.
- Each failure page covers the symptoms, an example, the root cause, and how to fix it.

## Document Processing Goals

| Goal | What goes wrong | Patterns |
|---|---|---|
| [Accurate Text Extraction](accurate-text-extraction/) | Accurate text extraction fails when OCR or vision-language models misread characters, numbers, or punctuation in a document image | 8 |
| [Agentic Orchestration](agentic-orchestration/) | Agentic orchestration fails when an agent's document reasoning is sound but the surrounding machinery — context management, tool calls, and self-correction — corrupts or loses the information the reasoning depends on | 6 |
| [Document Classification](document-classification/) | Document classification fails when a pipeline cannot correctly determine what a document is, where it starts and ends, or which schema applies, before extraction ever begins | 6 |
| [Layout Preservation](layout-preservation/) | Layout preservation fails when an agent reads every character correctly but flattens the document's two-dimensional structure into the wrong one-dimensional text stream | 6 |
| [Multimodal Reliability](multimodal-reliability/) | Multimodal reliability fails when a vision-language model produces a fluent, confident-sounding extraction that isn't actually grounded in what the document shows | 10 |
| [Production Reliability](production-reliability/) | Production reliability fails when a document-processing pipeline that worked in testing degrades, silently or operationally, once it runs continuously at real-world scale | 10 |

**Total: 46 patterns**

## Frequently Asked Questions

### Where do I start if my document processing agent is failing?

Match the symptom to a goal in the table above, then open that goal's page for how to tell its failures apart and where to look first. Each failure page ends in mitigations you can apply directly.

### How are these document processing failure patterns organized?

By goal: the outcome the agent is supposed to achieve. Under each goal, a `failures` folder holds one page per pattern. For the full picture see the [Document Processing overview](../).

## Related

- [Document Processing overview](../)
- [All agent failure patterns](../../../)
