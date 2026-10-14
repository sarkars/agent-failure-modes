# Knowledge Retrieval AI Agent Failures by Goal: 74 Patterns, Causes, and Fixes

**Knowledge Retrieval failures in AI agents are grouped here into 7 goals, each with a catalog of named failure patterns, the symptoms you will see, the root cause, and mitigations you can copy.** Start from the symptom you are debugging, pick the matching goal below, and open its failure list.

## Key Takeaways

- This capability covers 7 goals and 74 documented failure patterns.
- The largest goal is [Knowledge Freshness](knowledge-freshness/) with 22 patterns.
- Each goal page explains the failure class, how to tell it apart from its neighbors, and which mitigations apply across its patterns.
- Each failure page covers the symptoms, an example, the root cause, and how to fix it.

## Knowledge Retrieval Goals

| Goal | What goes wrong | Patterns |
|---|---|---|
| [Answer Synthesis](answer-synthesis/) | Answer synthesis fails when a model has the right retrieved context in front of it and still produces a wrong or misleading answer | 11 |
| [Citation Accuracy](citation-accuracy/) | Citation accuracy fails when a citation exists and looks legitimate but doesn't actually do the job a citation is supposed to do | 7 |
| [Knowledge Freshness](knowledge-freshness/) | Knowledge freshness fails when an agent applies information that is true in isolation but wrong for the moment, scope, or domain-context it's actually needed in | 22 |
| [Query Understanding](query-understanding/) | Query understanding fails when an agent resolves what a user actually wants silently and incorrectly | 8 |
| [Retrieval](retrieval/) | Retrieval fails when the pipeline searches the wrong corpus, returns too few or too many documents, misses content trapped in tables or scanned images | 12 |
| [Retrieval Quality](retrieval-quality/) | Retrieval quality fails when the pipeline finds documents that are topically plausible but wrong along a dimension similarity search doesn't measure | 13 |
| [Retrieval Relevance](retrieval-relevance/) | Retrieval relevance fails when an agent selects a comparable or reference item using text-embedding similarity alone, and the selected item matches on language but not on the structured attributes | 1 |

**Total: 74 patterns**

## Frequently Asked Questions

### Where do I start if my knowledge retrieval agent is failing?

Match the symptom to a goal in the table above, then open that goal's page for how to tell its failures apart and where to look first. Each failure page ends in mitigations you can apply directly.

### How are these knowledge retrieval failure patterns organized?

By goal: the outcome the agent is supposed to achieve. Under each goal, a `failures` folder holds one page per pattern. For the full picture see the [Knowledge Retrieval overview](../).

## Related

- [Knowledge Retrieval overview](../)
- [All agent failure patterns](../../../)
