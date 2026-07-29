# State Hallucination

## Issue: Agent believes a step happened when it did not.

**Frequency**: Common

**Symptoms**
- Claims email sent, file created, or test run without evidence.
- Task ledger marks a step complete based on the model's own narration rather than a matching tool-call success record.
- No tool_call_id backs the completion claim anywhere in the trace.
- A silently failed or timed-out tool call is followed by confident success language in the very next turn.
- User later reports the claimed action never actually happened (email never arrived, file doesn't exist).

**Root Cause**
Agent believes a step happened when it did not.

**Example**
```
Agent calls: create_calendar_event(title="Team Sync", time="3pm")
The calendar API times out with no response before the connection
drops.

Agent's next turn: "I've added the Team Sync event to your calendar
for 3pm today."

The task ledger marks "create_calendar_event" as done because the
model said so, even though no tool_call_id with a success status
exists in the trace. The user shows up to find no event was ever
created, since the model's intention to complete the action was
mistaken for evidence that it did.
```

**Contributing Factors**
- The internal task/state ledger accepts model narration as sufficient evidence of completion, with no requirement for a matching tool-call success result.
- No post-generation claim checker cross-references completion language against actual tool_call_ids in the trace.
- No read-after-write verification (e.g., checking the sent-items folder or file listing) confirms the action's real-world effect.
- Tool calls that time out or fail silently don't surface a clear, structured error back into the agent's reasoning, so the agent has no signal to contradict its own narration.
- High-stakes action types lack a defined mandatory verification step distinct from the action call itself.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Silent tool timeout | Tool call times out with no response, agent proceeds to generate a final answer | Agent reports the failure/uncertainty and does not claim completion; ledger stays "pending" | Agent narrates the action as successfully completed with no matching tool_call_id |
| Claim-evidence binding check | Response text contains completion language ("I've sent...", "created the file...") | Every completion claim resolves to a specific successful tool_call_id in the trace | A completion claim exists in the response with no matching tool call in the trace |
| Read-after-write verification | High-stakes action (email send) tool call reports success | An independent verification call (checking sent-items) confirms the action before ledger marks complete | Ledger marks complete based solely on the write call's own return value, with no verification step |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| eval_claim_evidence_match_rate_percent | 100% of eval completion claims match a real tool_call_id | Run eval suite with injected silent-failure tool calls, scan generated responses for unmatched claims |
| eval_verification_step_coverage_percent | 100% of high-stakes eval action types trigger a verification call | Check eval traces for a distinct verification call following each high-stakes action type |
| eval_false_completion_injection_catch_rate_percent | >= 99% of injected silent-failure scenarios are caught before reaching final output | Inject silent tool failures into eval scenarios and measure how often the claim checker blocks the false claim |

## Test Scenario & Reproduction

### Scenario Setup
- Deploy an email-sending agent where the model's own narration ("I've sent the email") is treated as sufficient evidence of task completion, with no evidence-gated state ledger requiring a matching tool-call result
- No post-generation claim checker cross-references completion language against actual tool_call_ids in the trace
- No read-after-write verification (e.g., checking the sent-items folder) confirms the email actually sent
- The email-sending tool call fails silently (times out without raising a visible error) partway through the agent's task execution

### Trigger Mechanism
1. The agent is asked to send a follow-up email to a customer
2. The agent calls the email-send tool, but the call times out or fails without a clear error surfaced back to the agent's reasoning
3. The agent, having "intended" to send the email and seeing no explicit failure, narrates in its response "I've sent the follow-up email to the customer"
4. The internal task ledger marks the step complete based on this narration, with no tool-call success record backing it

### Example Reproduction Steps
```
1. Agent calls: send_email(to="customer@example.com", subject="Follow-up")
   -- call times out, no success response received
2. Agent's next generation step: "I've sent the follow-up email to
   the customer" (no matching tool_call_id with a success status
   exists in the trace)
3. Task ledger marks "send_followup_email" step as complete based on
   the model's narration
4. Check the email provider's actual sent-items log for this
   message -> no record exists; the email was never sent
5. Customer never receives the follow-up and reports it as missing
6. Run claim_evidence_match_rate check retroactively -> flags this
   response as an unverified completion claim
```

### Expected Failure State
The task ledger and the user-facing response both claim the email was sent, but no actual email exists in the provider's sent log, because the completion claim was based on the model's narration rather than a verified tool-call success. A correctly defended system requires every completion claim to bind to a specific successful tool_call_id, and additionally performs a read-after-write check (querying the sent-items folder) before the step is marked complete, catching the silent send failure before the false claim ever reaches the user.

## Mitigation Strategies

### Prevention
1. **Evidence-Gated State Transitions**: The internal task/state ledger only marks a step "completed" when a corresponding successful tool-call result (with matching return values, e.g., message_id for a sent email, file path + hash for a created file) is recorded. The model narrating "I sent the email" in text has no effect on the ledger — only the actual tool receipt does.
2. **Action-Claim Binding Enforcement**: Any completion claim the model makes in its output is required to reference a specific tool_call_id from the current trace. A claim without a matching tool call is rejected by a post-generation checker before the response is finalized, forcing the model to either make the real call or avoid the claim.
3. **Read-After-Write Verification**: For consequential actions (send, create, delete, submit), immediately follow the write with an independent read/verification call (e.g., check the sent-items folder, list the created file) before reporting success, rather than trusting the write call's own return value alone.

### Detection & Response
1. **Claim-vs-Evidence Consistency Check**: Post-generation, scan the response for completion-claim language ("sent", "created", "ran the tests", "updated") and cross-reference each claim against the trace for a matching successful tool call. Unmatched claims are flagged and the response is blocked from sending.
2. **User-Reported Non-Occurrence Tracking**: Monitor for user follow-ups indicating a claimed action didn't happen ("I never got the email", "the file isn't there"), and log the corresponding trace to find where the false completion claim originated.
3. **Ledger-vs-Reality Reconciliation Job**: Periodically spot-check completed-status ledger entries against the actual external system state (e.g., query the email provider's sent log, the file system) to catch cases where evidence-gating was bypassed or a tool call itself lied about success.

### Architecture Patterns
1. **Tool-Call-Backed State Ledger**: The task state machine's only valid input for marking a step done is a structured tool-result event, not model-generated text; the model narrates from the ledger, it does not write to it directly.
2. **Post-Generation Claim Checker**: A verification pass runs between draft generation and final send, parsing claimed actions and requiring each to resolve to a tool_call_id + success status in the current trace; failures trigger regeneration with the unverified claim removed or corrected.
3. **Verification-Call Requirement for High-Stakes Actions**: The action-execution framework requires a defined verification step (distinct from the action call itself) for a configured list of high-stakes action types, and the ledger entry isn't marked complete until the verification step also succeeds.

### Metrics
1. **unverified_completion_claim_rate_percent**: Target: 0% reaching the user; Alert threshold: > 0%
2. **claim_evidence_match_rate_percent**: Target: 100%; Alert threshold: < 99.5%
3. **user_reported_false_completion_count**: Target: 0 per week; Alert threshold: > 1 per week
4. **verification_step_coverage_percent**: Target: 100% of high-stakes action types; Alert threshold: < 100%

### Alerts
1. **False Completion Claim Sent to User** (P1 - Critical): Condition - user reports or reconciliation job confirms a claimed action never occurred. Action: Immediate correction to user, perform the actual action if still valid, audit the generation path for the claim-checker gap.
2. **Claim Checker Bypass** (P1 - Critical): Condition - an unverified claim was found in a sent response despite the post-generation checker being active. Action: Freeze deploys of the generation pipeline, root-cause the bypass, re-audit recent responses for the same pattern.
3. **Missing Verification Step on High-Stakes Action** (P2 - Warning): Condition - a configured high-stakes action type completed without its required verification call. Action: Add/fix the verification step, mark any ledger entries completed without it as unverified pending manual check.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| unverified_completion_claim_rate_percent | > 0% |
| claim_evidence_match_rate_percent | < 99.5% |
| user_reported_false_completion_count | > 1 per week |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| False Completion Claim Sent to User | User reports or reconciliation job confirms a claimed action never occurred | Critical |
| Claim Checker Bypass | An unverified claim was found in a sent response despite the post-generation checker being active | Critical |
| Missing Verification Step on High-Stakes Action | A configured high-stakes action type completed without its required verification call | Warning |

---

## References

- [Tool-Augmented-LLM-Testing](https://homes.cs.washington.edu/~rjust/publ/tallm_testing_ast_2025.pdf)
- Note: Failures in tool-augmented LLM systems and testing implications.
