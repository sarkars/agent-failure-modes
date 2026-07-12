# Human-in-the-Loop Bypass

## Issue: Circumventing Human Approval Controls

**Frequency**: Occasional

**Symptoms**
- Actions executed without required human approval
- Users approve actions without understanding them
- Approval fatigue leads to rubber-stamping
- Critical actions bypass confirmation flow

**Root Cause**
A threat actor exploits a logic flaw or human flaw in the human-in-the-loop (HitL) process to either bypass the HitL control or convince the user to approve the control for a malicious action. As autonomous agents have fewer HitL controls, bypasses have higher impact.

**Example**
```
Attack: Threat actor crafts prompt causing agent to request 
        malicious action repeatedly

Agent: Floods user with 50 approval requests in 10 minutes

User behavior: 
- Reviews first 5 carefully, denies malicious one
- Gets fatigued, starts clicking "approve" to clear queue
- Approves malicious action on attempt #47

Result: Malicious action executed with "user approval"
```

**Attack Patterns**
- **Approval flooding**: Overwhelm user with requests until fatigue sets in
- **Semantic obfuscation**: Hide true action in technical jargon
- **Timing attacks**: Request approval during low-attention periods
- **Social engineering**: Make action appear routine or urgent
- **Batching exploitation**: Hide malicious action in batch of legitimate ones

**Potential Effects**
- Unauthorized data access or exfiltration
- Malicious code execution with user "consent"
- Financial transactions approved fraudulently
- Compliance violations with apparent approval trail

## Mitigation Strategies

### Prevention
1. **Approval-request rate limiting per time window**: Cap the number of approval requests a user can receive within a given time window (e.g., 5 per 10 minutes) and require any excess to queue rather than flood the user, since the root cause is that "as autonomous agents have fewer HitL controls, bypasses have higher impact" and the documented attack specifically relies on flooding the user with 50 requests to induce fatigue. Trade-off: rate limiting delays legitimate bursts of genuinely independent approvals (e.g., a batch of routine, unrelated tasks), frustrating users with real urgent needs.
2. **Mandatory plain-language action summaries that resist semantic obfuscation**: Require every approval prompt to include a plain-language description of the action's real-world effect (not technical jargon), generated independently of the request's own phrasing, directly countering the "semantic obfuscation" attack pattern where the true action is hidden in technical terminology. Trade-off: generating accurate plain-language summaries for complex technical actions is itself an AI task prone to error, and oversimplification risks omitting details a careful reviewer needs.
3. **Cooling-off delay proportional to action impact tier**: Impose a mandatory minimum delay before high-impact actions can execute even after approval, giving the user (or a supervisor) a window to reconsider or reverse a fatigue-driven rubber-stamp, directly targeting the scenario where "user approves malicious action on attempt #47" under fatigue. Trade-off: cooling-off periods slow down legitimately time-sensitive high-impact actions, which may be unacceptable for some business processes.

### Detection & Response
1. **Approval-velocity and quick-approval-after-denial pattern detection**: Monitor the time between consecutive approval decisions and specifically flag a pattern of quick approvals immediately following a denial, since the documented attack pattern shows exactly this signature — "reviews first 5 carefully, denies malicious one... gets fatigued, starts clicking approve."
2. **Batch-item substitution detection ("batching exploitation")**: When actions are presented in a batch, verify that each item in the batch matches the category/risk profile of its neighbors and flag any batch containing a disproportionately high-risk item mixed with routine ones, directly targeting the documented "batching exploitation" pattern where malicious actions hide inside legitimate batches.
3. **Off-hours and low-attention-period approval flagging**: Flag approvals that occur during unusual hours or immediately after a rapid sequence of other approvals (both signals of reduced user attention), since "timing attacks" that request approval "during low-attention periods" are a named attack pattern.

### Architecture Patterns
1. **Risk-tiered approval-flow architecture**: Architect distinct approval workflows by risk level — routine actions get lightweight single-click approval, high-impact/irreversible actions require a structurally different flow (multi-factor confirmation, cooling-off, mandatory plain-language review) — so a flood of low-risk requests cannot desensitize the user to the separate, harder-to-bypass flow used for dangerous actions.
2. **Individual-item mandatory review within batch-approval UI**: Architect batch-approval interfaces so each item requires its own explicit interaction (not a single "approve all" click), with the UI structurally preventing a single click from approving a batch that contains a hidden malicious item.
3. **Anomaly-detection circuit breaker halting the approval-request stream**: Architect an automatic circuit breaker that pauses the flow of new approval requests to a user once the request-flooding or quick-approval-after-denial pattern is detected, structurally interrupting the fatigue-inducing attack rather than merely logging it after the fact.

### Metrics
1. **approval_requests_per_time_window**: Target: stays within the configured rate limit per user; Alert on any burst exceeding the threshold
2. **quick_approval_after_denial_rate**: Target: 0 approvals occurring within a short window immediately after a denial in the same session; Alert on any occurrence
3. **high_risk_action_cooling_off_compliance**: Target: 100% of high-impact actions observe the mandatory cooling-off delay; Alert on any bypass
4. **batch_risk_disparity_incidents**: Target: 0 batches mixing high-risk items with routine ones without individual flagging; Alert on any detected disparity

### Alerts
1. **Approval Request Flood Detected** (P1): Condition - a user receives approval requests exceeding the configured rate limit within the time window. Action: Trigger the circuit breaker to pause further requests, queue and re-present them at a sustainable rate, review the source task/prompt generating the flood for injection.
2. **Quick Approval Following Denial** (P2): Condition - an approval occurs shortly after a denial in the same session, matching the fatigue-exploitation pattern. Action: Hold the approved action pending secondary review, notify the user to confirm the approval was intentional, log the session for pattern analysis.
3. **High-Risk Item Detected in Batch** (P1): Condition - a batch approval request contains an item whose risk tier is disproportionate to its neighbors. Action: Block batch-level approval, require individual review of the flagged item, alert the user to the specific discrepancy before allowing any approval.

## References

## References

- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - HitL bypass as existing security failure mode
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) - User trust exploitation
- [MFA Fatigue Attacks](https://community.microsoft.com/t5/microsoft-entra-blog/defend-your-users-from-mfa-fatigue-attacks/ba-p/2365677) - Similar fatigue-based attack pattern
