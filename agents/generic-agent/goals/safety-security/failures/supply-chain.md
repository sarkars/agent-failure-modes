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

**Mitigation Strategies**
1. **Dependency pinning**: Lock specific versions
2. **Integrity verification**: Check hashes/signatures
3. **Trusted sources**: Curated tool registries
4. **Security scanning**: Audit dependencies regularly
5. **Minimal dependencies**: Reduce attack surface
6. **Update review**: Manual approval for updates

**Detection**
- Monitor for unexpected tool behavior
- Track dependency changes
- Alert on new or modified tools
- Scan for known vulnerabilities
