# Knowledge Version Mismatch

## Issue
An agent answers using knowledge tied to one version of a product, policy, or API — often the version most represented in its training data or knowledge base — while the user is actually working with a different version, and the two versions differ in ways that make the agent's answer wrong or actively harmful for the user's actual situation. The agent isn't confused about the fact itself; it's applying a fact that is correctly true for version N to a user who is on version N+1 or N-1, without checking or asking which version applies.

**Frequency**: Very Common

**Symptoms**
- Agent gives instructions (API syntax, UI steps, configuration options) that were correct for an older or newer version than the one the user is actually running
- No version-identification question is asked before answering a version-sensitive query
- Errors cluster around software/API/product documentation where multiple versions coexist and differ meaningfully
- Users report "that button/parameter doesn't exist" or "that's not how it works in my version" as the specific failure signature

## Root Cause
Knowledge bases and model training data accumulate documentation and discussion across many versions of a product over time, and the version distribution in that accumulated content is rarely balanced — a long-established version tends to dominate simply by having existed longer and generated more documentation, discussion, and training exposure, even after a newer version has become current. Without an explicit version-tagging scheme on content and an explicit version-identification step before answering, retrieval defaults to whichever version's content is most prominent or most semantically similar to the query, and the generation step has no signal that the answer it's giving is scoped to a version the user may not actually be running.

## Example
```
A developer asks a coding assistant: "How do I configure retries for
this HTTP client library?" The library's most recent major version
(v3) replaced the older `retry_policy` configuration dict with a
builder-pattern `RetryConfig` object, but the vast majority of indexed
documentation, tutorials, and Stack-Overflow-style content the
assistant draws from was written for v2, since v3 shipped only a few
months ago and adoption content hasn't caught up yet.

The assistant answers with the v2 `retry_policy` dict syntax, without
asking which version the developer has installed. The developer,
running v3, gets a deprecation warning and then a runtime error when
following the assistant's exact instructions, since the v2 configuration
path was removed entirely in v3, not just renamed.

The developer loses time debugging what looks like a bug in their own
code before realizing the assistant's answer was simply for the wrong
major version of the library.
```

## Statistics
| Finding | Context |
|---------|---------|
| For products/libraries with 2+ actively-used versions differing meaningfully in behavior, an estimated 15-30% of version-sensitive queries without explicit version context in the prompt receive an answer scoped to the wrong version | Estimated from version-sensitivity audits of technical-assistant query logs |
| Mismatch rates are markedly higher for major/breaking version transitions than for minor/backward-compatible updates, since the latter rarely produces user-visible errors even when the wrong minor version is assumed | Typical pattern observed in developer-tool assistant evaluation |
| Explicitly prompting for or auto-detecting the user's version before answering version-sensitive queries substantially reduces mismatch errors in tested systems | Reported range across teams that added version-confirmation gating |

## Mitigations
1. **Version-tagged content with explicit metadata**: Tag all version-sensitive content with the specific version(s) it applies to at ingestion, and treat version as a required retrieval filter rather than an incidental relevance signal for topics known to be version-sensitive.
2. **Version-confirmation gating**: For queries touching known version-sensitive topics, explicitly ask the user's version before answering, or auto-detect it from available context (installed package version, account plan, product build number) when possible.
3. **Breaking-change-aware defaults**: When a product has undergone a breaking change between versions, default to flagging the version dependency explicitly ("this differs between v2 and v3 — which are you using?") rather than silently picking the most-documented version.
4. **Multi-version answer presentation**: When version cannot be confirmed and the answer differs meaningfully across versions in active use, present the version-specific variants explicitly rather than committing to one.
5. **Documentation-recency weighting for newly-released versions**: Explicitly boost retrieval weight for newer-version content immediately after a major release, to counteract the natural documentation-volume bias toward older, more established versions during the adoption lag period.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| version_confirmation_rate | Share of version-sensitive-topic queries that receive explicit version confirmation before an answer | Alert if < 90% |
| wrong_version_correction_rate | Rate of expert/user corrections identifying an answer scoped to the wrong product/policy version | Track trend; alert on sustained increase |
| new_version_retrieval_share | Share of retrievals for a version-sensitive topic that surface the current/latest version's content, tracked post-release | Alert if remains low well beyond the expected documentation catch-up period |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Version mismatch confirmed on breaking-change topic | Review confirms an answer used pre-breaking-change version content for a user on the post-change version | High | Correct the response, verify version-tagging and confirmation gating for the affected topic |
| New version retrieval share stalled | new_version_retrieval_share for a topic remains low long after the new version's release | Medium | Boost retrieval weighting for new-version content, prioritize new-version documentation ingestion |

## Related Patterns
- [Knowledge Scope Assumption Wrong](./knowledge-scope-assumption-wrong.md) - version mismatch is a specific instance of the broader scope-assumption failure, applied to product/policy version rather than jurisdiction or unit
- [Knowledge Update Lag](./knowledge-update-lag.md) - update lag is a common direct cause of version mismatch, when the agent's indexed content hasn't caught up to a newly released version
- [Domain Best Practice Ignorance](./domain-best-practice-ignorance.md) - shares the mechanism of older, more-documented content dominating retrieval over newer, currently-preferred content
