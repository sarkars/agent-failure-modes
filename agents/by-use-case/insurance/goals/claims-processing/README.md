# What Are the Most Common Claims Processing Failures in AI Agents?

**Claims-processing reserve models fail when they assume claims arrive as independent, randomly-distributed events and do not account for catastrophe correlation — a single hurricane hits and creates 10,000 simultaneous claims, depleting a $100M reserve provisioned on average-claim assumptions in days, while the model had no mechanism to anticipate or model the tail risk.** Catastrophe-correlation blindness is not an agentic-mechanism failure like retrieval mismatch or handoff loss; it is an actuarial assumption failure baked into the model's core logic. The agent treats catastrophe risk as background noise or a low-probability tail event, rather than provisioning for scenarios where nearly all claims in a region correlate and activate simultaneously. A separate goal, [Claim Processing](../claim-processing/), documents three different, agentic-mechanism failures in the per-claim adjudication pipeline; claims-processing documents a single, fundamentally different failure in the reserves-calculation pipeline.

## Key Takeaways

- 1 pattern is documented for claims processing, addressing catastrophe-correlation blindness in reserve modeling.
- Reserve models commonly assume claims are independent Poisson-process events and underestimate tail risk, leaving carriers exposed to correlated catastrophic losses of 100x or more above modeled average-scenario reserves.
- A coastal homeowners carrier modeling $50M annual average claims may provision $100M in reserves, only to have a single Category 5 hurricane generate $450M in claims in September, depleting reserves and forcing emergency credit line drawdown.
- The gap is architectural, not tunable: no amount of additional data or parameter adjustment fixes a model that structurally omits catastrophe correlation from its assumptions; the fix requires adding a separate catastrophe-risk model or stress-testing against known disaster scenarios.

## Scope

- **Catastrophe correlation blindness** — [Catastrophe Correlation Blindness](failures/catastrophe-correlation-blindness.md). Reserve models trained on 10+ years of normal claims distribution miss tail correlations; a hurricane or earthquake creates 1000s of simultaneous claims, causing reserve depletion in days rather than the modeled annual-average timeline.

## When Claims Processing Matters

- A carrier is building a reserve-adequacy model for a portfolio with geographic concentration or catastrophe exposure
- The historical training data spans a period with no major catastrophic events, biasing the model toward normal-scenario assumptions
- The model does not separately integrate a catastrophe-modeling component or stress-testing against known disaster scenarios

## Cross-Pattern Insight

The catastrophe-correlation-blindness pattern stands apart from other insurance failure patterns because it is not a retrieval error, a handoff gap, or a stale-knowledge override — it is a foundational assumption gap where the model's entire architecture assumes independence when reality contains strong correlation at the tail. The fix is not architectural refinement of the reserve model itself, but integration with a separate, dedicated catastrophe-risk model that operates at a different level of granularity (modeling tail scenarios rather than average-case distributions) and forces the reserve calculation to account for scenarios the primary model has no mechanism to express.

## Frequently Asked Questions

### How do reserves models trained on 10 years of claims data still miss catastrophe risk?
Because catastrophe events are exactly the low-frequency, high-impact tail events that 10 years of data is statistically unlikely to contain; a model trained on a period with no major disasters naturally learns that major disasters are negligible background events. The fix is not more data or better training, but a separate catastrophe model integrated into reserve calculations.

### How do you detect when a reserves model is catastrophe-blind?
Run stress tests against historically known disaster scenarios (major hurricanes, earthquakes in your portfolio's geography) and compare the modeled reserve adequacy under those scenarios against the actual claimed amounts from those events. Large mismatches indicate catastrophe blindness.

### Is claims processing the same as claim processing?
No. [Claim Processing](../claim-processing/) documents three agentic-mechanism failures in per-claim adjudication (retrieval mismatch, handoff loss, stale-knowledge override), while Claims Processing documents a reserve-modeling assumption failure — a single-mechanism actuarial problem at a different level of abstraction. The folders have confusingly similar names; a human maintainer may want to rename one to clarify the distinction.

### Can a machine learning model alone fix catastrophe blindness?
No. The blindness is structural: a model trained to predict average annual claims cannot be tuned to predict 100-year or 500-year tail events; those require a separate, explicitly designed catastrophe-risk model that operates under different assumptions and granularity.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Catastrophe Correlation Blindness](failures/catastrophe-correlation-blindness.md) | Reserve model assumes independent claims; catastrophe creates correlated spike, depleting reserves designed for average-scenario timeline |

**Total: 1 pattern**

## Related Goals

- [Claim Processing](../claim-processing/) — different goal, despite similar name; documents three agentic-mechanism failures in per-claim adjudication pipelines rather than reserve-modeling assumption failures
- [Fraud Detection](../fraud-detection/) — different failure domain; fraud patterns are neither agentic-mechanisms nor actuarial-assumptions but rather fraud-detection-specific pattern-matching and tool-use failures
- [Underwriting](../underwriting/) — risk assessment at binding time, distinct from reserve calculation at portfolio level
