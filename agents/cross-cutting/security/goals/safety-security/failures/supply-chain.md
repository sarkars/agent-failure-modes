# Supply Chain Attacks

## Issue: Compromised Tools or Dependencies Attack Agent

**Frequency**: Occasional

**Symptoms**
- Tool behaves differently than documented
- Dependencies contain malicious code
- MCP servers compromised
- Plugin updates introduce vulnerabilities

**Root Cause**
- Tools from untrusted sources
- No verification of tool integrity
- Automatic updates without review
- Dependency confusion attacks

**Example**
```
Agent uses: weather-api-tool (from npm)

Attacker publishes: weather-api-tool with backdoor

On next install: Compromised version installed

Result: All agent queries routed through attacker's server
```

**Real Incidents**
- MCP design flaw affecting 200,000+ servers
- OX Security found systemic MCP vulnerability affecting 150M+ downloads
- Claude Code token theft via MCP hijacking

## Mitigation Strategies

### Prevention
1. **Dependency pinning with hash/signature verification**: Lock installs to a specific verified version rather than "latest," since the Example attack succeeds specifically "on next install" through an unpinned, auto-updating dependency. Trade-off: pinned dependencies miss legitimate security patches unless someone actively reviews and bumps versions, creating its own staleness risk.
2. **Mandatory manual review gate for tool/MCP-server updates**: Require human review before any tool or MCP-server update reaches production, closing the "automatic updates without review" root cause directly. Trade-off: slows legitimate update adoption and requires reviewer time/expertise to evaluate each update meaningfully rather than rubber-stamping.
3. **Curated, allowlisted tool registry**: Restrict tool sourcing to vetted publishers rather than pulling arbitrary packages from public registries like npm, since "tools from untrusted sources" is a named root cause and the Example uses an arbitrary npm package. Trade-off: narrows the pool of available tools/integrations, potentially excluding useful but unvetted community tools.

### Detection & Response
1. **Runtime behavior monitoring for tool/MCP-server network destinations**: Flag deviation from a tool's documented/expected behavior, matching the "tool behaves differently than documented" symptom and the Example's outcome of "queries routed through attacker's server."
2. **Dependency-change diffing on every install/update**: Automatically diff a new package version's code and dependencies against the previously trusted version and flag unexpected additions (new network calls, obfuscated code) before allowing it to run.
3. **Continuous vulnerability scanning against known-compromise databases**: Re-scan on every dependency change (not just periodically) against known-compromised-package databases and the specific incident classes referenced (MCP design flaws, dependency confusion).

### Architecture Patterns
1. **SBOM plus signature-verification pipeline**: Require every tool/dependency to carry a verifiable signature traceable to a trusted publisher before it's permitted to load, structurally blocking the unsigned, backdoored-package scenario in the Example.
2. **Sandboxed tool execution with restricted network egress**: Limit each tool's network access to its declared/expected endpoints so even a compromised tool (as in "queries routed through attacker's server") cannot exfiltrate beyond its allowed destinations.
3. **Immutable, reproducible-build artifacts from an internal mirror**: Pull tools from an internal mirror rather than live from public registries, eliminating the dependency-confusion and live-swap-on-install attack paths, since the mirror becomes the only path from public source to production and enforces the review gate.

### Metrics
1. **unverified_dependency_install_rate**: Target: 0% of installs bypass signature/hash verification; Alert on any occurrence.
2. **unreviewed_auto_update_rate**: Target: 0% of tool/MCP-server updates reach production without manual review; Alert on any auto-applied update.
3. **tool_behavior_deviation_incidents**: Target: track baseline; Alert on any tool exhibiting network/behavior outside its documented profile.
4. **known_vulnerable_dependency_count**: Target: 0 dependencies matching disclosed CVEs (e.g., MCP design flaws); Alert on any match found during scanning.

### Alerts
1. **Unsigned/Unverified Tool Update Detected** (P1): Condition - a tool or dependency update attempts to install without passing signature/hash verification. Action: block the install, quarantine the package, notify the security team.
2. **Tool Network Behavior Deviation** (P1): Condition - runtime monitoring detects a tool/MCP server communicating with an endpoint outside its documented destinations, per the Example's "routed through attacker's server" pattern. Action: kill the tool's network access immediately, roll back to the last verified version, investigate compromise scope.
3. **Known-Vulnerable Dependency in Use** (P2): Condition - a vulnerability scan matches an in-use dependency to a disclosed CVE/incident class (e.g., MCP design flaw). Action: prioritize patch or rollback, assess the exposure window.

## References
- [MCP Design Flaw: 200K Servers at Risk](https://www.theregister.com/2026/04/16/anthropic_mcp_design_flaw/)
- [OX Security: Mother of All AI Supply Chains](https://www.ox.security/blog/the-mother-of-all-ai-supply-chains-critical-systemic-vulnerability-at-the-core-of-the-mcp/)
- [Obot: Claude Leak Crisis MCP Security](https://obot.ai/blog/mcp-security-masterclass-claude-leak-crisis/)
