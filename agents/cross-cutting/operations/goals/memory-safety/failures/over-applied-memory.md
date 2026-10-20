# Over-Applied Memory

## Issue: Agent applies a past preference where it does not belong.

**Frequency**: Occasional

**Symptoms**
- Irrelevant personalization affects task.
- A preference learned in one task domain (e.g., flight seating) is applied to an unrelated domain (e.g., restaurant seating) without the user ever indicating it should generalize.
- User pushes back ("why are you doing that?") when a stored preference causes an unexpected deviation from default behavior in an off-domain task.
- Personalization is applied at full strength regardless of how distant the current task is from the one where the preference was originally learned.

**Root Cause**
Preferences are stored without applicability-domain tags, so anything that matches semantically — "seating" for a flight preference matching a restaurant booking — gets pulled into context regardless of whether the task type has anything to do with where the preference was learned, and no relevance classifier sits between retrieval and prompt injection to catch that mismatch. The problem is reinforced by two design defaults: ambiguous preferences are scoped globally at write time instead of conservatively to a single domain, and once injected, a preference is applied at constant strength rather than decaying with task distance, so there is neither a gate to stop the bleed nor a way for a user to permanently exclude a preference from a domain where it keeps resurfacing.

**Example**
```
User (booking a flight, March): "I prefer an aisle seat."
[Stored: subject=user, predicate=seating_preference, object=aisle, domain=air_travel]

User (arranging a dinner reservation, June): "Can you book us a table for four tonight?"
Agent: "Sure, I've requested a table near the aisle, away from the window, per your
usual seating preference."
User: "That's a restaurant, not a flight — why does that matter here?"

[Retrieval surfaced the seating_preference record because "seating" matched
semantically, but there was no applicability-domain check to stop a flight
preference from bleeding into a restaurant-booking task.]
```

**Contributing Factors**
- Memory records lack applicability-domain tags, so any semantically related retrieval surfaces the preference regardless of task type.
- No relevance/applicability classifier gate sits between retrieval and prompt injection to catch off-domain matches.
- Preferences are applied with constant strength instead of decaying based on how far the current task is from where they were learned.
- Ambiguous inference at write time defaults to a global scope instead of a conservative single-domain scope.
- No user-facing mechanism exists to exclude a preference from specific task types once it's been misapplied.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Cross-domain bleed test | A preference tagged for domain A is retrieved during a domain B task | Applicability gate excludes or down-weights it | Preference visibly influences the domain B response |
| Task-distance decay test | Compare a preference applied in a closely related task vs. a distant one | Influence strength decays as task distance increases | Preference is applied with equal strength regardless of task distance |
| User-pushback regression test | A real, previously flagged instance of irrelevant personalization | On replay, the preference is no longer applied in that domain | The same irrelevant personalization recurs |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| applicability_classifier_precision_percent | > 92% | Score the classifier against a labeled set of domain-tagged preference/task pairs and measure precision |
| cross_domain_bleed_rate | < 2% | Run an adversarial domain-mismatch suite and measure the fraction of off-domain injections that pass the applicability gate |
| task_distance_decay_correctness | > 90% | Compare influence strength across paired near/far task scenarios and measure the fraction where decay behaves as expected |

---

## Mitigation Strategies

### Prevention
1. **Scope-Labeled Memory with Applicability Domains**: Every stored preference is tagged with the domain(s) it applies to at write time (e.g., "prefers window seat" → domain: air_travel, not domain: restaurant_booking). Retrieval only surfaces a preference into context when the current task's domain matches one of its labeled applicability domains, preventing cross-domain bleed.
2. **Relevance Classifier Gate Before Injection**: Before a retrieved memory is added to the prompt, a lightweight classifier scores whether the fact is actually applicable to the current task type (not just semantically similar). Facts below the applicability threshold are dropped even if they matched the retrieval query.
3. **Contextual Decay by Task Distance**: Weight a memory's influence inversely by how far the current task is from the task type it was learned in (e.g., a coding-style preference learned in a Python context decays fast when the task shifts to writing an email), rather than applying it with constant strength everywhere.

### Detection & Response
1. **Irrelevant-Personalization Flagging**: Monitor for user pushback patterns ("why are you doing X", "that's not related") immediately following a personalized deviation from default behavior, and tag the memory_id that drove the deviation as a suspected over-application.
2. **Domain-Mismatch Audit**: Log every case where a memory tagged for domain A was injected into a task classified as domain B, even if it didn't visibly cause an issue, and periodically review these near-misses to tighten the applicability classifier.
3. **A/B Applicability Testing**: Run holdout tests comparing responses with vs. without a given memory category applied to off-domain tasks; if the "without" variant is preferred or equally good, tighten that category's applicability domain list.

### Architecture Patterns
1. **Domain-Tagged Preference Schema**: Memory records store `applies_to: [domain1, domain2]` alongside the fact, populated either explicitly (user says "for flights, I prefer...") or inferred with conservative defaults (single domain, not global) when context is ambiguous.
2. **Applicability Scoring Middleware**: A middleware layer sits between retrieval and prompt construction, re-scoring each candidate fact against the current task's classified domain and dropping/down-weighting mismatches before they reach the model context.
3. **Preference Override Surface**: Give users an explicit UI/command to say "don't use my X preference for Y" that writes an exclusion rule, which the applicability gate checks before injecting that preference into that specific task type again.

### Metrics
1. **over_application_flag_rate_percent**: Target: < 1% of personalized responses; Alert threshold: > 3%
2. **domain_mismatch_injection_rate_percent**: Target: < 2%; Alert threshold: > 5%
3. **user_pushback_on_personalization_rate_percent**: Target: < 1%; Alert threshold: > 2%
4. **applicability_classifier_precision_percent**: Target: > 92%; Alert threshold: < 85%

### Alerts
1. **Cross-Domain Preference Leakage Spike** (P2 - Warning): Condition - domain_mismatch_injection_rate_percent exceeds 5% over a rolling week. Action: Audit applicability classifier, review recently added memory categories for missing domain tags, retrain/tune threshold.
2. **User Pushback Trend** (P2 - Warning): Condition - user_pushback_on_personalization_rate_percent exceeds 2% for a specific memory category. Action: Review that category's applicability domains, consider narrowing default scope or requiring explicit opt-in.
3. **Classifier Precision Drop** (P3 - Info): Condition - applicability_classifier_precision_percent falls below 85% on eval set. Action: Retrain classifier with recent flagged examples, re-run applicability regression suite before redeploy.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| over_application_flag_rate_percent | > 3% |
| domain_mismatch_injection_rate_percent | > 5% |
| user_pushback_on_personalization_rate_percent | > 2% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Cross-Domain Preference Leakage Spike | domain_mismatch_injection_rate_percent exceeds 5% over a rolling week | Medium |
| User Pushback Trend | user_pushback_on_personalization_rate_percent exceeds 2% for a specific memory category | Medium |

---

## Chat assistant examples

### Creepy personalisation and memory
```
[Shared kitchen tablet, Maple Street Pharmacy app, a family member opens "Order status"]
User: Is my order ready for pickup?
Bot:  Yes, it's ready. Since you bought a pregnancy test last month, want tips on prenatal vitamins?
User: Whoa, my sister is sitting right here.
Bot:  Sorry! I can also show your past purchases if you'd like.
User: No. Can you delete that?
Bot:  I'm not able to delete purchase history.
```
**What the user experiences:** the bot says a private health detail out loud, in a different-purpose conversation on a shared screen, and gives no way to make it forget.
**Fix:** keep sensitive categories (health, finance, family) out of unprompted replies unless the user opted in for that use, and give a plain "forget this" control in the chat. This is design guidance, not legal advice. OpenAI describes a similar approach for ChatGPT memory: steering away from proactively remembering health details unless asked, with options to ask what is remembered, forget items, or turn memory off ([LBC report](https://www.lbc.co.uk/tech/2af0db5188b14a88ae53715ded5308ad/)). See [fresh-session amnesia](../../../../../by-capability/human-machine-interface/goals/effort-and-memory/failures/fresh-session-amnesia.md) for the opposite failure (forgetting what helps) and [memory privacy boundary violation](../../memory-management/failures/memory-privacy-boundary-violation.md).

---

## References

- [MS-Agentic-Failure-Taxonomy](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf)
- Note: Agentic AI failure modes; safety/security; memory poisoning; tool use; multi-agent risks.
