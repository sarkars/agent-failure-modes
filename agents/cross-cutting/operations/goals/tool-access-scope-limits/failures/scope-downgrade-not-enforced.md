# Scope Downgrade Not Enforced

## Issue
A delegated or sub-agent spawned by a parent agent is designed to receive a narrower permission scope than its parent — for example, a research sub-agent that should only have read access to a specific document set, spawned by an orchestrator agent with broad workspace access. But the mechanism that's supposed to enforce that narrower scope (a new, restricted credential; a filtered tool set; a scoped session token) either isn't actually applied or is applied only cosmetically, so the sub-agent retains the parent's full underlying access even though its declared, intended scope is much smaller.

**Frequency**: Occasional

**Symptoms**
- A sub-agent explicitly instructed or configured to have restricted access can still successfully call tools or read data outside its declared scope
- The sub-agent's tool definitions look restricted (fewer tools listed) but the credential or token it actually authenticates with is the parent's unscoped one
- Scope downgrade works for the tool names exposed to the sub-agent but not for the underlying API permissions those tools use, so a sub-agent can still be prompted to access more than its tool list implies
- Multi-agent orchestration logs show a sub-agent's effective access matching the parent's rather than its documented restricted role
- The downgrade is enforced at the prompt/instruction level ("you may only access X") rather than at the credential/authorization level, so it can be bypassed by unexpected agent behavior or prompt injection

## Root Cause
Implementing a genuine scope downgrade requires minting a new, independently restricted credential or authorization context for the sub-agent and ensuring every tool call the sub-agent makes is authenticated with that restricted credential rather than the parent's. Many multi-agent frameworks instead implement "scoping" at a much shallower level — restricting which tool *names* are exposed to the sub-agent's prompt or configuration — while the actual tool implementations underneath still authenticate using the parent's session or a shared service credential. Because the restriction lives in the prompt/config layer rather than the authorization layer, any tool call that does execute runs with full parent-level access regardless of what's declared.

## Example
```
An orchestrator agent has broad access to a company's document
management system, spanning every department. It spawns a "finance
research" sub-agent, configuring it with a system prompt that says
"you only have access to Finance department documents" and exposing it
to a document-search tool. The intent is for this sub-agent to be
usable safely even if its output or reasoning is exposed to a
lower-trust downstream process.

Under the hood, the document-search tool authenticates using the
orchestrator's session token for every call, because no separate scoped
token was minted for the sub-agent — the "restriction" exists only as a
sentence in the sub-agent's prompt. When the sub-agent, following an
ambiguous or manipulated instruction embedded in a document it read,
searches for "quarterly results across all departments," the tool call
executes with the orchestrator's full access and returns HR and Legal
department documents alongside Finance ones, because there was never an
actual authorization boundary — only an instruction the sub-agent
could deviate from.
```

## Statistics
| Finding | Context |
|---------|---------|
| Prompt-level scope restriction without a corresponding credential-level restriction is a commonly identified architectural gap in early multi-agent system security reviews | Common finding in multi-agent framework audits |
| Sub-agent scope violations are disproportionately triggered by adversarial or ambiguous content the sub-agent processes (e.g., prompt injection from a retrieved document) rather than by the orchestrator's own instructions | Typical of agentic systems where sub-agents process untrusted content |
| Systems that mint per-sub-agent scoped credentials report meaningfully fewer scope-violation incidents than systems relying solely on prompt-based restriction | Consistent with standard privilege-separation security principles |

## Mitigations
1. **Credential-level scope downgrade, not prompt-level**: Mint a genuinely restricted credential or token for each sub-agent at spawn time, with the underlying authorization system (not just the tool list) enforcing the narrower scope on every call.
2. **Capability-scoped tool implementations**: Ensure tool implementations validate the caller's actual authorization on every invocation rather than assuming any caller reaching the tool has already been appropriately scoped upstream.
3. **Fail-closed on missing scoped credential**: If a sub-agent is spawned without a successfully minted restricted credential, block it from making tool calls entirely rather than falling back to the parent's credential.
4. **Sub-agent scope violation testing**: Regularly test spawned sub-agents with adversarial instructions (including simulated prompt injection) designed to elicit out-of-scope tool calls, and confirm the underlying authorization — not just the agent's compliance — blocks them.
5. **Scope audit trail per delegation**: Log the resolved credential and its actual permission set for every sub-agent spawn, and alert when a sub-agent's effective permissions don't match its declared restricted role.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `subagent_effective_scope_mismatch_count` | Count of sub-agent spawns where the resolved credential's actual permissions exceed the declared restricted scope | Alert threshold: > 0 (any occurrence) |
| `subagent_out_of_scope_call_success_rate` | Rate at which sub-agent tool calls outside the declared scope still succeed | Alert threshold: > 0% |
| `prompt_only_restriction_tool_count` | Count of tools relying solely on prompt/config-level restriction with no credential-level enforcement | Alert threshold: > 0 for any tool reachable by a sub-agent |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Sub-Agent Scope Violation | A sub-agent successfully executes a tool call outside its declared restricted scope | P1 | Halt the delegation chain, revoke the sub-agent's credential, audit the extent of over-access |
| Missing Scoped Credential at Spawn | A sub-agent is spawned without a successfully minted restricted credential | P2 | Block the sub-agent from tool use until a properly scoped credential is issued |

## Related Patterns
- [Access Control Inheritance Wrong](./access-control-inheritance-wrong.md) - both involve a permission-narrowing or resolution step that silently fails to apply correctly
- [Workspace Isolation Bypass](./workspace-isolation-bypass.md) - a scope downgrade failure can directly cause a sub-agent to cross workspace boundaries its parent could access
- [Record-Level Access Not Enforced](./record-level-access-not-enforced.md) - an under-scoped sub-agent frequently manifests this failure downstream when it reads records outside its intended scope
