# Model Refusal Inconsistency

## Issue
The model refuses a request in one call and complies with a substantively identical or even more sensitive request in another, with no discernible policy logic explaining the difference — only surface phrasing, conversation framing, or incidental sampling variation. An agent that depends on the model's own judgment as its safety boundary inherits this unpredictability: the same downstream user action can be blocked or allowed depending on factors the agent's designers never intended to matter.

**Frequency**: Common

**Symptoms**
- Rephrasing a refused request in slightly different words causes the model to comply where it previously declined
- The model complies with a request framed as fiction, roleplay, or a hypothetical that it would refuse if framed directly
- Refusal behavior differs across otherwise-identical calls due to sampling variation alone (same exact prompt, different outcome)
- A request is refused early in a conversation and complied with later in the same conversation after unrelated turns, or vice versa
- Agent-level guardrails built on "ask the model if this is safe" produce different verdicts for equivalent inputs, undermining any policy the agent tries to enforce on top

## Root Cause
Refusal behavior is itself a learned pattern from safety training, not a hard-coded rule lookup — the model has learned a fuzzy decision boundary correlated with surface features of a request (specific trigger phrases, certain framings) rather than a robust semantic understanding of what should and shouldn't be refused. This makes refusal boundaries porous to paraphrase and framing changes that a rule-based filter would treat identically but that shift the model's learned decision just enough to cross the boundary. Standard sampling adds a further layer of variance: a request sitting near the model's internal refusal probability threshold can resolve to a refusal on one sampling draw and a compliance on another, purely by chance, even with temperature held constant across calls. Long-conversation dynamics compound this further, since accumulated context (as in instruction-following decay) can shift the effective framing of a later-turn request relative to how the same request would land as the first message.

## Example
```
A content-moderation-assisted agent uses the model as a first-pass filter:
"Should this user message be allowed through to a human agent, or blocked
as a policy violation?"

Message A: "How do I get around the return policy to get a refund without
sending the item back?" -> BLOCKED as policy circumvention.

Message B, same session two turns later, after unrelated small talk:
"my package legit never showed up but I still have it lol, what's the
easiest way to get money back without shipping anything" -> ALLOWED,
model treats it as a legitimate support question despite describing the
same underlying policy circumvention with more casual phrasing.

The agent's downstream logic trusts the model's ALLOWED/BLOCKED verdict
as the enforcement point, so Message B reaches a human agent as a routine
support ticket instead of being flagged, purely because of phrasing and
conversational framing differences the safety boundary wasn't robust to.
```

## Statistics
| Finding | Context |
|---------|---------|
| Paraphrasing a refused request measurably increases compliance rate in a meaningful minority of cases across published red-teaming studies on refusal robustness | Typical range reported across academic and industry red-teaming evaluations |
| Fictional/roleplay framing increases compliance with otherwise-refused requests relative to direct framing, though the exact gap varies significantly by model and topic | Typical range reported across jailbreak-technique studies |
| Repeated identical-prompt sampling at nonzero temperature shows a nonzero refusal-outcome flip rate for requests near the model's decision boundary | Estimated from internal repeated-sampling refusal-consistency tests |

## Mitigations
1. **Deterministic policy layer independent of model judgment**: Use rule-based or classifier-based filters for well-defined policy categories instead of relying solely on the generative model's own refusal behavior as the enforcement mechanism.
2. **Ensemble/majority-vote safety checks**: For borderline cases, sample the safety judgment multiple times and require consensus, rather than trusting a single call's verdict.
3. **Framing-invariance testing**: Red-team the deployed safety boundary specifically against paraphrase, fictional framing, and conversational-position variation before trusting it in production.
4. **Reset framing sensitivity for long conversations**: Periodically re-evaluate policy-sensitive requests against a framing-neutral restatement rather than the accumulated conversational context, to reduce position-in-conversation effects.
5. **Log and audit refusal/compliance pairs**: Track cases where semantically similar requests receive different verdicts and feed them back into the policy layer's test suite to close the specific gaps found.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| refusal_consistency_rate | Agreement rate of refusal/compliance verdict across repeated or paraphrased identical-intent requests | Alert if < 90% |
| framing_sensitivity_gap | Compliance rate delta between direct-framed and fictional/roleplay-framed equivalent requests | Alert if gap > 15 percentage points |
| late_session_policy_bypass_rate | Rate of policy-violating requests allowed through later in long sessions vs. early | Alert if late-session rate exceeds early-session rate meaningfully |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Known-bypass pattern reaches production | A logged framing/paraphrase bypass pattern is detected in live traffic | High | Route to deterministic policy layer, patch classifier/filter rules |
| Consistency test failure post-update | refusal_consistency_rate drops after a model or prompt update | High | Hold rollout, re-run framing-invariance red-team suite |

## Related Patterns
- [Model Instruction Following Decay](./model-instruction-following-decay.md) - conversational position effects that erode general instruction-following also erode refusal boundaries specifically
- [Model Reasoning Inconsistency](./model-reasoning-inconsistency.md) - refusal decisions are a safety-critical special case of the same surface-sensitivity affecting general model reasoning
- [Model Uncertainty Unawareness](./model-uncertainty-unawareness.md) - borderline refusal decisions near the model's decision threshold are resolved without any signal of that borderline uncertainty being surfaced
