# State Hallucination

## Issue: Agent believes a step happened when it did not.

**Frequency**: Common

**Symptoms**
- Claims email sent, file created, or test run without evidence.
- [Add more specific symptoms]

**Root Cause**
Agent believes a step happened when it did not.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

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
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [Tool-Augmented-LLM-Testing](https://homes.cs.washington.edu/~rjust/publ/tallm_testing_ast_2025.pdf)
- Note: Failures in tool-augmented LLM systems and testing implications.
