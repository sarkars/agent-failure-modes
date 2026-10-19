# Guardrail Tools Compared: What Each Checks, Where It Runs, and What It Does on a Miss

This page compares five guardrail tools, from their vendor docs, against the proposed Guide spec fields, for developers choosing a tool to sit beside conversation guidance in a chatbot.

> **Status: Needs review, 2026-10-20.** The owner reviews tool comparisons before this is treated as final. Every tool statement below comes from a vendor page opened with WebFetch on 2026-10-20; docs change, so check the version you run. **Nothing was run hands-on:** no tool was installed, configured or called, and no results or benchmarks are reported. The "Could it express the Guide spec?" column is our reading of the docs (our judgment, untested). Read the sibling page first: [Output guardrails vs. conversation guidance](output-guardrails-vs-conversation-guidance.md) explains the two layers and the Guide spec. This page does not repeat it.

## 1. What each can check
| Tool | Input | Output | Dialog flow | Other checks named on the opened page |
|---|---|---|---|---|
| NeMo Guardrails | Yes (input rails) | Yes (output rails) | Yes (dialog rails) | Retrieval and execution rails |
| Amazon Bedrock Guardrails | Yes | Yes | Not listed | Content filters, denied topics, word filters, sensitive information (PII, custom regex), contextual grounding, Automated Reasoning |
| Guardrails AI | Yes (input guards) | Yes (output guards) | Not listed | Validators from the Guardrails Hub (list not on the page opened) |
| Azure AI Content Safety | Yes (for example Prompt Shields) | Yes (for example protected material, groundedness preview) | Not listed | Text and image harm categories with severity levels; task adherence for agent tool use |
| Llama Guard 3 | Yes (prompt classification) | Yes (response classification) | Not listed | 14 hazard categories (S1-S14) plus Code Interpreter Abuse |

## 2. Where it runs
| Tool | Where | Source says |
|---|---|---|
| NeMo Guardrails | Your Python environment as a library; or a server started with `nemoguardrails server` that exposes OpenAI-style chat completions endpoints | Opened page also mentions a Kubernetes microservice but not its internals |
| Amazon Bedrock Guardrails | AWS-managed. Attach to a model call by guardrail ID and version, or call the `ApplyGuardrail` API without invoking a model | Evaluation of only part of a prompt (tagging) is SDK-only, not console |
| Guardrails AI | "In your application" as a Python library | The page opened on server mode did not say either way; not confirmed |
| Azure AI Content Safety | Azure service (needs a subscription and a resource in a supported region); text and image APIs, plus a Studio for testing | Pricing tiers and rate limits exist; see the page |
| Llama Guard 3 | A model you host yourself (weights required; a quantized version is offered) | No hosted API described on the model card opened |

## 3. What it does on a miss
| Tool | Documented action when a check fails |
|---|---|
| NeMo Guardrails | Rails "block, alter, or validate" inputs and outputs. For PII: detect and block, or mask. The page did not list fixed outcomes and did not use the word "rewrite", so rewrite is unconfirmed here |
| Amazon Bedrock Guardrails | Block or mask (sensitive information); block or flag (grounding); you configure the message returned to the user when a filter is triggered |
| Guardrails AI | Per-validator `on_fail`: REASK (regenerate with an auto-generated prompt describing the failure), FIX, FILTER (drop a failing field, structured data only), REFRAIN (return `None`), NOOP (log only), EXCEPTION, FIX_REASK, CUSTOM (your function) |
| Azure AI Content Safety | The opened overview describes detection, severity levels and blocklists. It did not describe the service itself rewriting or blocking; the calling app acts on the result (our reading) |
| Llama Guard 3 | Outputs "safe" or "unsafe" plus violated categories; probability of the first token can be thresholded. It does not enforce anything; your system does. The card notes it may increase refusals of benign prompts |

Only Guardrails AI documents reask as a built-in action on the pages opened.

## 4. Could it express the proposed Guide spec?
The reference spec is from [generic error messages](../goals/errors-and-recovery/failures/generic-error-messages.md): `runs: pre_send`, `reads` (error event and session fields), `trigger`, `moves`, `choices`, `on_miss: rewrite`, `metric`, `counter_metric`, `status`. Judgment from the docs only; no tool was tried.

| Spec field | NeMo | Bedrock | Guardrails AI | Azure CS | Llama Guard 3 |
|---|---|---|---|---|---|
| `runs: pre_send` (check a draft before it is sent) | Likely: output rails run after the LLM, before the user | Likely: output evaluation of model completions | Likely: output guards | Possible: you call the API on the draft | Possible: you call the model on the draft |
| `reads` (session or error-event fields) | Unknown: the page did not say what dialog rails receive | No: filters evaluate prompt and completion text | Unknown: custom validators may take your inputs; not confirmed | No: text or image in | No: prompt and response text in |
| `trigger` (a named moment, such as "an error is about to be shown") | Possible via dialog rails; not confirmed | No: category and policy triggers only | Possible via a custom validator; not confirmed | No | No |
| `moves` and `choices` (what the reply should do) | Not documented as a concept | Fixed message only | CUSTOM handler could hold the logic | No | No |
| `on_miss: rewrite` | "Alter" is documented; rewrite to a chosen move is unconfirmed | No: block, mask or flag, plus a fixed message | FIX, REASK or CUSTOM are closest | No | No |
| `metric`, `counter_metric`, `status` | Not a tool feature | Not a tool feature | Not a tool feature | Studio shows block rate and latency, which are not these metrics | Not a tool feature |

**Reading the table:** none of the five documents anything like a `moves` field or a pattern-level metric. The closest fits are NeMo dialog rails and Guardrails AI `CUSTOM` and `REASK`, and both would need your own logic; whether they can carry a full spec is unknown without a trial. Bedrock, Azure and Llama Guard fit the content-rule layer and would sit beside the Guide check, not implement it (our judgment).

## 5. How to choose (decision aid, not a ranking)
- **You need content rules only** (safety, PII, topic): any of the five checks content. Differences are where it runs and what you must build around it (sections 2 and 3).
- **You need the reply to be re-asked or repaired in code:** Guardrails AI documents REASK and FIX; NeMo documents altering outputs.
- **You want a classifier you control:** Llama Guard 3 is a model you host; you write the enforcement.
- **You want the proposed moves enforced:** no opened doc claims this. Plan to write the Guide check yourself, with a guardrail beside it. The reference module is not shipped.

## 6. Not tested
- No hands-on run of any tool. No latency, accuracy, false-positive rate or cost was measured, and none is reported.
- No custom rail, validator or handler was built to test whether a Guide spec field maps onto it.
- No tool was checked for how it behaves on multi-turn history.

## 7. Not opened or not confirmed
- **Guardrails AI:** the docs home page (`guardrailsai.com/docs`) did not list failure actions or checks; the validator on-fail page did, and is the source for section 3. Server mode and the Hub validator list were not confirmed.
- **NeMo:** the overview and rail-types pages were opened; what dialog rails receive was not stated, and Colang flow syntax was not opened.
- **Bedrock:** only the user guide landing page was opened; the sub-pages ("How Guardrails works", tiers, tagging, languages) were not.
- **Azure:** only the overview was opened; the harm-categories, Prompt Shields and task-adherence concept pages were not.
- **Llama Guard:** only the Llama Guard 3 8B model card on GitHub was opened.
- OpenAI and Anthropic moderation docs were not opened; nothing about them is claimed.

## 8. Sources (all opened 2026-10-20)
| Tool | Page |
|---|---|
| NeMo Guardrails | [Overview](https://docs.nvidia.com/nemo/guardrails/latest/about/overview.html); [rail types](https://docs.nvidia.com/nemo/guardrails/about-nemo-guardrails-library/rail-types.md) |
| Amazon Bedrock Guardrails | [User guide](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) |
| Guardrails AI | [Docs home](https://www.guardrailsai.com/docs); [validator on-fail actions](https://guardrailsai.com/docs/concepts/validator_on_fail_actions) |
| Azure AI Content Safety | [Overview](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/overview) |
| Llama Guard 3 | [Model card](https://github.com/meta-llama/PurpleLlama/blob/main/Llama-Guard3/8B/MODEL_CARD.md) |

## Related
- [Output guardrails vs. conversation guidance](output-guardrails-vs-conversation-guidance.md): the two layers and the Guide spec fields.
- [Generic error messages](../goals/errors-and-recovery/failures/generic-error-messages.md): the reference Guide spec used above.
- [Glossary](glossary.md): Guide spec, counter-metric.
