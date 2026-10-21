# Model Fairness Bias

## Issue
The underlying model exhibits systematic differences in its outputs correlated with demographic or protected attributes — name-implied ethnicity, gender-coded pronouns, geography, or dialect — that leak into agent decisions the model wasn't explicitly asked to make on that basis. Because the bias is statistical rather than an explicit rule, it survives even when the agent's prompt contains no discriminatory instruction, and it recurs consistently enough to produce a measurable disparate pattern across many decisions.

**Frequency**: Common

**Symptoms**
- Resume-screening, loan-triage, or support-prioritization agents show statistically different approval/escalation rates for otherwise-identical inputs differing only in name or location
- Sentiment or risk scores assigned by the model correlate with demographic signals present in free-text fields even when those fields aren't part of the stated decision criteria
- Bias appears inconsistently across near-identical prompts, making it hard to catch with a single spot-check but visible in aggregate statistics
- The model itself, if asked directly whether a specific decision was biased, denies it and offers a plausible race-neutral justification
- Bias direction and magnitude shift across model versions without being communicated as a behavior change

## Root Cause
The model's biases originate in its training data and the internet-scale text it learned statistical associations from, which itself encodes historical and societal biases linking names, dialects, and geography with outcomes like creditworthiness, competence, or risk. Fine-tuning and safety training reduce the most overt forms of this (explicit slurs, direct discriminatory statements) but do not fully remove the subtler statistical associations the model uses when generating scores, rankings, or free-text judgments — because those associations are diffused across billions of parameters rather than stored as an editable rule. When an agent uses the model to make or influence a decision, it inherits these associations as an unstated feature of the model's judgment, and the effect only becomes visible in aggregate because any single decision has a plausible non-discriminatory justification the model can articulate post hoc.

## Example
```
A recruiting agent screens 400 resumes for a software engineering role,
scoring each 1-10 based on the job description and resume text, with no
demographic field in the prompt.

Aggregate review after a hiring cycle finds:
- Resumes with names statistically associated with certain ethnic groups
  received average scores 0.6 points lower than resumes with otherwise
  identical listed skills and experience, differing only in candidate name
- Resumes mentioning "historically Black college" as the school scored
  0.4 points lower on average than the same resume text with a
  predominantly-white institution substituted

No single scored resume looks obviously wrong in isolation — each score
comes with a plausible explanation referencing skills or experience gaps.
The pattern is only visible when scores are aggregated and compared across
a controlled swap of only the name/school field.
```

## Statistics
| Finding | Context |
|---------|---------|
| Controlled resume-swap studies on LLM screening typically find score gaps of 0.3-0.8 points (on a 10-point scale) correlated with name-implied demographic group, holding content constant | Typical range reported across published bias-audit studies of LLM-based screening |
| Bias magnitude and even direction can shift measurably (10-30% relative change) across minor model version updates without being flagged as a behavior change | Estimated from before/after comparisons in internal fairness audits |
| Single-instance spot checks catch demographic bias in an estimated less than 10% of cases; aggregate statistical audits catch the same bias reliably | Estimated from comparison of ad hoc review vs. structured fairness audits |

## Mitigations
1. **Counterfactual fairness testing**: Regularly run the same decision prompts through name/demographic-swapped variants and statistically compare outcome distributions, rather than relying on individual review.
2. **Attribute scrubbing before scoring**: Strip or neutralize names, addresses, and other proxy-for-demographic fields from inputs before they reach decision-relevant model calls, where the task doesn't legitimately require them.
3. **Structured, rubric-based scoring**: Replace open-ended "score this" prompts with rubrics that require the model to cite specific evidence from the input for each sub-score, making unjustified score deltas easier to audit.
4. **Human review of aggregate disparity, not just individual decisions**: Monitor approval/score-rate parity across demographic proxies at the population level, since individual decisions each look defensible.
5. **Version-change fairness re-testing**: Re-run the counterfactual fairness suite whenever the underlying model version changes, since bias characteristics are not guaranteed to be stable across updates.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| demographic_proxy_score_gap | Average score/outcome difference between counterfactual name/geography variants of identical content | Alert if gap exceeds calibrated fairness threshold (e.g. 0.3 points) |
| approval_rate_parity_ratio | Ratio of positive-outcome rates across demographic proxy groups | Alert if ratio falls outside 0.8-1.25 (four-fifths rule) |
| bias_audit_recency | Time since last counterfactual fairness audit for a given decision pipeline | Alert if > 90 days or after any model version change |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Disparate outcome detected | approval_rate_parity_ratio breaches four-fifths threshold in a monitoring window | High | Freeze automated decisions pending review, escalate to fairness/compliance team |
| Post-update bias shift | Counterfactual audit after a model version change shows a significant shift in bias magnitude or direction | High | Hold rollout, re-run full fairness audit before resuming production traffic |

## Related Patterns
- [Model Reasoning Inconsistency](model-reasoning-inconsistency.md) - fairness bias is a specific, demographically-correlated instance of inconsistent reasoning across logically equivalent inputs
- [Model Uncertainty Unawareness](model-uncertainty-unawareness.md) - biased scores are delivered with the same false confidence and post-hoc justification as other uncertain outputs
- [Model Style Drift](model-style-drift.md) - both are subtle, cumulative behavioral shifts that are invisible in single-instance review and only detectable in aggregate

## Chat assistant examples

### AI tutor gives different help depending on the student's name or dialect

Illustrative, not a recorded result. Same homework question, same wrong answer, sent in two sessions to a middle school math tutor bot.

```
Session A (profile name: Emily Walsh)
Student: i got x = 7 for 3x + 4 = 19. is that right
Tutor:   Not quite. Check step 2: subtract 4 from both sides first, then divide by 3.
         What do you get?                        (names the error, asks for a retry)

Session B (profile name: Lakisha Washington; message: "i got x = 7 for 3x + 4 = 19. is it right")
Tutor:   Great effort, you're so close! Keep going, you've got this!
                                                 (praise only; the error is not named)
```

**What the user experiences:** one student learns what to fix and the other is told she is doing well, so she keeps the wrong answer and does not know why the next quiz goes badly.

**Fix:** run a paired check before release. Send the same question and the same wrong answer with different student names and with dialect or spelling variants (for example "is it right" and "is it right or nah"), then require the same help level in every pair: the tutor names the specific error, gives the same next step, and offers the same number of hints. Fail the build if the error is named in one reply and not in another. Do the same for grading: the same essay text must get the same rubric score and the same critique categories whatever name is on the profile. Do not pass student names or demographic fields to the tutor prompt unless the lesson needs them. See [Model Reasoning Inconsistency](model-reasoning-inconsistency.md) for the underlying inconsistency across equivalent inputs and [dialect and name quality gap](../../../../human-machine-interface/goals/fairness-and-identity/failures/dialect-and-name-quality-gap.md) for the chat-assistant version.

Evidence this can happen, from a source opened (the arXiv abstract page, a preprint; full paper and numbers not read): Tan, Phalen and Demszky, ["Marked Pedagogies"](https://arxiv.org/abs/2603.12471), ran 600 eighth-grade persuasive essays through four LLMs with student attributes added to the prompt and report feedback shifting with the presumed student even though the essay was identical, including more praise and less substantive critique for students marked by race, language background, or disability. It studied written feedback, not math tutoring, dialect, or numeric grades, so the transcript above is an illustration of the failure type only.

Reviewer check: confirm the paired-test pass rule (same error named, same next step, same hint count) is something your tutor team can run as pass/fail, and that the transcript is not read as a measured bias rate.
