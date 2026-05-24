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

**Mitigation Strategies**
1. **Rate limiting**: Limit approval requests per time period
2. **Clear explanations**: Require plain-language action descriptions
3. **Cooling off periods**: Delay high-impact actions
4. **Anomaly detection**: Flag unusual approval patterns
5. **Action categorization**: Different approval flows by risk level
6. **Batch inspection**: Require individual review of batch items

**Detection**
- High volume of approval requests in short time
- Pattern of quick approvals following denials
- Approvals during unusual hours
- Actions that don't match user's typical behavior

## References

- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - HitL bypass as existing security failure mode
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) - User trust exploitation
- [MFA Fatigue Attacks](https://community.microsoft.com/t5/microsoft-entra-blog/defend-your-users-from-mfa-fatigue-attacks/ba-p/2365677) - Similar fatigue-based attack pattern
