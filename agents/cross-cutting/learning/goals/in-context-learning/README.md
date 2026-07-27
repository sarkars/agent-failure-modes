# What Are the Most Common In-Context Learning Failures in AI Agents?

**In-context learning fails when an agent receives examples or few-shot instruction within a request but interprets examples incorrectly, forgets examples mid-conversation, or applies learned patterns too rigidly to new scenarios.** An agent given five worked examples of how to format output mode-switches to the formatting of only the first example and ignores the others, a system learns from examples in the first message but produces behavior inconsistent with the learned pattern by the tenth message, and a few-shot learner shown two successful approaches to a problem locks onto the first approach and refuses to use the second even when the first fails in a new context. In-context learning failures matter precisely because they occur within a single conversation or session, making such failures harder to detect through offline evaluation: the agent's training-time knowledge is stable, but its within-conversation learning is broken.

## Key Takeaways

- In-context learning operates within a single request or conversation, using examples and instructions to guide behavior without persistent model updates or retraining, making it fundamentally different from persistent safe-learning in behavior, observability, and failure modes.
- Example interpretation is the highest-frequency failure category: agents misalign on example intent (rule vs. preference vs. anti-pattern), selectively attend to examples (noticing first or last examples but ignoring middle ones), and fail to generalize learned patterns to out-of-distribution scenarios not covered by the examples.
- Context window degradation (forgetting early examples or instructions as the conversation extends) and example-count sensitivity (behavior changes dramatically based on 1 vs. 3 vs. 5 examples) are documented patterns across language models, not edge cases, and should be designed-for rather than designed-around.
- Effective in-context learning requires instrumentation beyond what works for training-time learning: measuring example coverage (do all provided examples get equal attention), measuring within-conversation consistency (does learned behavior persist across turns), and detecting example-forgetting (does behavior drift from taught patterns as context window fills).

## Scope

In-context learning covers learning-within-a-conversation behaviors including:
- **Example interpretation and alignment** — does the agent correctly interpret example intent (working example vs. anti-pattern vs. user preference), attend to all examples equally, and distinguish worked examples from negative examples.
- **Few-shot pattern learning** — can the agent extract generalizable patterns from examples and apply learned patterns to out-of-sample scenarios the examples did not cover.
- **Instruction-following consistency** — when inline instructions and examples conflict, how does the agent prioritize, and does the agent maintain consistency between early-instruction-learned behavior and late-instruction-learned behavior.
- **Context-window-aware learning** — does the agent forget or de-emphasize early examples/instructions as the conversation extends and context window fills, and can the agent re-emphasize important learned patterns when asked to recall earlier context.

## When In-Context Learning Matters

- The agent needs to adapt to user-specific output format preferences, domain conventions, or problem-solving approaches without requiring a full training cycle or user-specific model deployment.
- Conversations are long (hundreds of tokens or dozens of turns), and early examples or instructions must remain salient throughout, not fade as context accumulates.
- The agent receives ambiguous or multi-interpretation examples and must learn from user correction (e.g., user says "that's close but I need X instead") to disambiguate intent and adjust within-conversation behavior.

## Cross-Pattern Insight

Effective in-context learning systems treat examples and inline instructions as first-class inputs with the same rigor applied to training data: every example is logged with context (user-provided vs. system-generated, format expectations, error anti-patterns), every learned pattern is tracked (what rule was learned, from which examples, at what point in conversation), and every within-conversation behavior change is audited (did behavior actually change after examples, did change persist, did change cause regressions in other scenarios). The shared lesson across successful in-context systems is that example quality and example coverage matter more than example quantity: one well-designed, well-explained worked example often outweighs ten poorly-formatted examples the agent must interpret, and the agent's ability to distinguish rule-examples from preference-examples from anti-pattern-examples is more important than the total example count. The resolution is treating in-context learning instrumentation as non-negotiable: if the system cannot measure which examples were attended to and how learned patterns changed behavior, the system cannot optimize for in-context learning quality or detect degradation mid-conversation.

## Frequently Asked Questions

### How do language models sometimes lose examples and mode-switch back to training-time behavior mid-conversation?
Context-window degradation and example-forgetting are well-documented: as conversation length increases and context window fills, models often de-emphasize or lose access to early examples and learned patterns, reverting to training-time defaults or the most recent input. Mitigations include: re-emphasizing key examples or rules periodically throughout the conversation (e.g., "Remember, all outputs should follow the format from the examples earlier"), using structured formatting for examples (code blocks, XML tags) that models attend to more consistently, and explicitly prompting the agent to recall or re-commit to learned patterns ("Based on the examples I showed you, what format should I use?").

### How do you handle examples that conflict with the agent's training-time behavior or safety guidelines?
In-context examples that push agents toward unsafe or undesired behavior (e.g., format-examples showing prompt-injection, coding-examples showing insecure patterns) should be explicitly rejected or reinterpreted. Effective systems distinguish training-aligned examples from training-conflicting examples and handle conflicts through: safe-mode filtering (reject examples that violate guardrails), re-interpretation (interpret the example as showing a non-obvious pattern rather than prescribing unsafe behavior), or escalation (flag conflicts to a human reviewer). The key is preventing the agent from learning unsafe patterns mid-conversation just because an example demonstrated that pattern.

### Can in-context learning replace persistent fine-tuning or training-time learning?
In-context learning handles within-conversation personalization and adaptation, but does not replace persistent learning for behavior that should generalize across conversations. If the same correction or preference appears across 1000 conversations from different users, in-context learning cannot scale (the agent must be taught the same pattern 1000 times), and the pattern should be promoted to a persistent update. The distinction is: in-context learning handles instance-specific or user-specific patterns; persistent updates handle systemic patterns that benefit many users across many conversations.

### How do you measure whether examples are being interpreted correctly?
In-context learning quality should be measured through: (1) example-attendance metrics—for each provided example, does the agent's behavior align with the example's content or does it diverge; (2) pattern-extraction metrics—does the agent correctly generalize learned patterns to out-of-sample scenarios (did it learn the rule or just memorize the examples); (3) consistency metrics—does learned behavior persist across conversation turns or degrade as context window fills; (4) conflict-resolution metrics—when examples conflict (format-example shows X, safety-guideline prohibits X), does the agent navigate the conflict correctly. These metrics should be measured continuously to detect in-context learning failures early.

### What's the difference between in-context learning and prompt injection?
In-context learning treats user-provided examples and instructions as authoritative guidance that should shape behavior, with adequate safeguards to prevent examples from subverting guardrails or agent intent. Prompt injection is the adversarial version: an attacker provides examples or instructions designed to override or bypass the agent's actual objectives or safety constraints. Effective defense against prompt injection while preserving in-context learning requires: instruction-hierarchy clarity (training-time guidelines override in-context examples if conflict), example-validation (reject examples that violate safety constraints), and behavior-monitoring (detect when learned behavior violates guidelines).

## Failure Patterns

The in-context-learning goal currently has no documented failure patterns. Patterns in in-context-learning will focus on example interpretation errors, context-window-aware degradation, example-forgetting, example-generalization failures, and instruction-consistency issues within conversations.

## Related Goals

- [Safe Learning](../safe-learning/) — focuses on persistent behavior updates driven by feedback; where in-context-learning focuses on within-conversation adaptation, safe-learning focuses on updates that persist across conversations and require validation gates.
- [Feedback and Adaptation](../feedback-and-adaptation/) — covers iterative refinement through user feedback loops; both feedback-and-adaptation and in-context-learning are learning mechanisms within conversation, but feedback-and-adaptation emphasizes corrective feedback loops while in-context-learning emphasizes example-based pattern learning.
