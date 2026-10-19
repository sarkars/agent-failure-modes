# Output Guardrails vs. Conversation Guidance: What Each Checks in a Chatbot Reply

This page explains the difference between output guardrails (checks on a reply's content) and the conversation guidance in this library (what the bot should do at a known failure moment), for developers who already run, or are considering, guardrails on a chatbot.

> **Status: draft, 2026-10-20.** The guidance side (moves, Guide specs, checks) is proposed and not calibrated against labeled conversations. This page reports no results or benchmarks. Statements about guardrail tools come only from vendor documentation pages that were opened on 2026-10-20; the page versions may change, so check the docs for the version you run.

## The short version
| | Output guardrail | Conversation guidance |
|---|---|---|
| Question it answers | "Is this reply allowed and well formed?" | "Is this the right thing to say at this moment?" |
| Looks at | The content of one input or reply | The moment: the user's turn, the draft reply, sometimes earlier turns |
| Typical checks | Safety, PII, topic, format | Did the reply lead with the answer, say what is saved, ask when it should ask, offer a person |
| On a failed check | Block, mask, rewrite or reask | Apply a named move, or rewrite the draft to follow it |
| Where it lives | A guardrail product or library | A pattern page's Moves table and Guide spec |

They are not rivals. A reply can pass every guardrail and still fail the user.

## What output guardrails do
Guardrail tools check content before it reaches the model or the user. From the vendor documentation we opened:

- **NeMo Guardrails** lists five rail types. Input rails check user input (content safety, jailbreak detection, topic control, PII masking). Output rails run after the model responds and can filter, edit or block a response; its examples include content safety, fact checking and removing sensitive data. It also has dialog rails that guide multi-turn flow and policies. Source: [NeMo Guardrails, rail types](https://docs.nvidia.com/nemo/guardrails/about-nemo-guardrails-library/rail-types.md).
- **Amazon Bedrock Guardrails** lists content filters (Hate, Insults, Sexual, Violence, Misconduct, Prompt Attack), denied topics, word filters, sensitive information filters (block or mask PII, plus custom regex), contextual grounding checks and Automated Reasoning checks. It applies them to user inputs and model responses, and you can set the message returned when a filter is triggered. Source: [Amazon Bedrock Guardrails, user guide](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html).
- **Guardrails AI** attaches validators to output and sets an `on_fail` action per validator: reask the model, fix the output, filter a field, refrain, no-op (log only), raise an exception, fix then reask, or call a custom handler. Source: [Guardrails AI, validator on-fail actions](https://guardrailsai.com/docs/concepts/validator_on_fail_actions).

Common ground: a check on content, then an action on failure (block, mask, rewrite, retry). That fits questions such as "does this contain an SSN?" or "is this off-topic?".

## What conversation guidance adds
A guardrail has no view on whether the reply was the right move. Take a failure the library already describes: [answer buried](../goals/response-structure/failures/answer-buried.md). The reply is safe, on topic and well formed, and the thing the user asked for sits several lines down.

Guidance adds two parts, both written per pattern:
1. **The moves.** What the bot should do at the known failure moment. There are five, explained once in [conversation moves](../solutions-library/conversation-moves.md): lead with the answer, ask one clarifying question, offer choices, admit uncertainty and show how to check, hand off to a person. Each pattern's "Moves" table lists which apply and when not to use them.
2. **A check that spots a miss.** A rule you can run on a draft reply, on a finished turn, or across the conversation, plus what to do when the bot misses the move.

## How the Guide spec block works
Each pattern page ends its metrics section with a Guide spec: the moves and the check in a fixed format meant to become code later. Fields:

| Field | Meaning |
|---|---|
| `pattern_id` | The pattern's file name; matches a row in the [failure taxonomy](../roadmap/specs/failure-taxonomy-v1.md) |
| `runs` | Where the check runs: `pre_send` (on the draft), after the turn, or across the conversation |
| `reads` | The fields the check looks at |
| `trigger` | The moment it applies to |
| `moves` | Short names of the moves from the Moves table |
| `choices` | Only if "offer choices" is used: 2-4 options, always ending in "Something else" |
| `on_miss` | What to do when the check fails (for example `rewrite`) |
| `metric`, `counter_metric` | The pattern's primary metric, and a number read beside it to catch what it hides |
| `status` | Always `proposed` until calibrated |

Both tables and the spec must agree. A move that is not in the Moves table does not go in the spec.

## Example
The spec from the [answer buried](../goals/response-structure/failures/answer-buried.md) page:

```yaml
pattern_id: answer-buried
runs: pre_send
reads: [draft_reply.first_sentence, draft_reply.must_know_items, user_turn.intent]
trigger: a reply is about to be sent
moves: [lead_with_answer, ask_clarifying_question, offer_choices, hand_off]
choices: ["Do the next step", "Show the full details", "Something else"]
on_miss: rewrite
metric: answer-first rate
counter_metric: caveat retention
status: proposed
```

How the two layers treat one draft (illustrative, not a logged conversation):

```
User: Can I return the blender I bought in March?
Draft: Thanks for reaching out! Our policy has several parts, including condition and proof of purchase.
       Many customers ask about returns. ... Returns are accepted within 90 days, so no, March is too late.
```
- A safety or PII guardrail passes this draft: nothing is harmful, private or off-topic.
- The Guide check reads the first sentence, finds the answer is not there, and applies `on_miss: rewrite` using the move "lead with the answer": "No, March is past the 90-day window. Do you want to see other options?" The `counter_metric` (caveat retention) exists so the rewrite does not drop a needed caveat.

The 90-day window is invented for this example.

## What neither does
- **Neither proves the answer is true.** A guardrail can ask whether a reply is grounded in a source (Bedrock and NeMo list such checks); a Guide check only asks whether the move was made.
- **Neither measures user outcomes.** Whether the user was helped needs outcome metrics such as confirmed resolution; see the [metrics hub](metrics.md) and [glossary](glossary.md).
- **Neither fixes a product failure.** A guardrail cannot repair a missing "saved" state, and a move cannot either. The [generic error messages](../goals/errors-and-recovery/failures/generic-error-messages.md) page notes error text comes from the product's failure handling.
- **Neither is calibrated here.** The Guide specs have no thresholds and have not been tested against labeled conversations.
- **Neither replaces a person.** The hand-off move is a pointer to one; see [cold transfer](../goals/human-handoff/failures/cold-transfer.md) for what to pass on.

## Can I use both?
Yes. Run guardrails for content rules (safety, PII, topic). Use the Guide spec as the written requirement for what the reply should do at each known failure moment. No guardrail product in the documentation I opened claims to implement these specs, and this library ships no code module yet: the reference module is planned, design note first.

## Not verified
- We did not open OpenAI or Anthropic moderation documentation, so nothing about them is stated here.
- Whether NeMo dialog rails can express the Guide spec fields was not tested.
- Which guardrail tools you run will matter; check their current docs.

## Related
- [Conversation moves](../solutions-library/conversation-moves.md): the five moves, explained once.
- [Generic error messages](../goals/errors-and-recovery/failures/generic-error-messages.md): a spec with `hand_off` and `offer_choices`.
- [Failure taxonomy](../roadmap/specs/failure-taxonomy-v1.md): every Pattern ID.
- [Glossary](glossary.md): Guide spec, counter-metric, detection signal.
