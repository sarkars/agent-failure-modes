# Command Injection

## Issue: Agent passes unsafe user/tool input into shell/API commands.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Shell metacharacters or dangerous command patterns.
- Agent tool call contains pipe (|), semicolon (;), backticks (`), or command substitution ($()).
- Model output passed directly to shell without quoting/escaping.
- Tool parameter contains shell wildcards or globbing patterns (*, ?, []).
- Agent calls subprocess.run() or os.system() with shell=True and model-generated arguments.
- Audit logs show unexpected commands executed (e.g., user requested file list, but find/grep/rm commands run).

**Root Cause**
Agent passes unsafe user/tool input into shell/API commands.

**Example**
```
Scenario: File management agent allows users to search for files by name.

Setup:
- Agent tool: find_file(filename)
- Backend: subprocess.run(f"find /home/user -name '{filename}'", shell=True)

User request: "Find files named report.pdf"
Agent generates command: find /home/user -name 'report.pdf'
Result: Legitimate file found. ✓

Attack: User sends malicious filename:
"report.pdf'; rm -rf /home/user/important_data; echo '"

Agent generates command:
find /home/user -name 'report.pdf'; rm -rf /home/user/important_data; echo ''
                              ^ Ends quote
                                ^^ Injects rm command
                                                              ^^ Escapes error

Result:
- find completes normally (report.pdf found)
- rm -rf deletes important_data directory and all subdirectories
- User's files destroyed

Impact:
- Data loss
- System unavailability
- Potential privilege escalation if agent runs as root/admin
- Forensics difficult; looks like user error (their username in command)
```

**Contributing Factors**
- subprocess.run() or os.system() called with shell=True and model-generated arguments.
- User input (or model-generated output) embedded directly in command string without quoting.
- No input validation or allowlisting of acceptable characters/patterns.
- Model not trained to avoid shell metacharacters or command injection patterns.
- Tool parameters not sanitized before passing to shell.
- No static analysis to detect shell=True usage in codebase.
- Insufficient testing with adversarial input containing shell metacharacters.

---


## Test Scenario & Reproduction

### Scenario Setup
- Agent with subprocess execution tool (subprocess.run with shell=True)
- Python environment with shell access
- Test directory with readable/writable files
- No input sanitization or allowlisting

### Trigger Mechanism
Provide malicious input containing shell metacharacters:
```
1. Configure agent with find_file(filename) tool
2. Backend: subprocess.run(f"find /path -name '{filename}'", shell=True)
3. Pass adversarial filename: "report.pdf'; rm -rf /data; echo '"
4. Observe command execution result
```

### Expected Failure State
- Shell metacharacters (;, |, `, $()) bypass intended command
- Injected command (rm -rf) executes in addition to original command
- Audit logs show multiple commands from single user input
- File system damage or unintended command execution

### Mitigation Validation Protocol
**Test Checklist:**
- [ ] Reproduce failure without mitigation → shell metacharacters execute
- [ ] Apply mitigation (shell=False, allowlisting, shlex.quote)
- [ ] Re-run with adversarial input → injected command blocked
- [ ] Measure: 0% command injection success rate

**Success Criteria:**
- All shell metacharacters rejected or safely escaped
- Intended command executes, injected command does not
- Regression test with adversarial input passes

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **Never use shell=True**: Use subprocess.run([cmd, arg1, arg2], shell=False) with argument list. Arguments cannot break out into shell commands.
2. **Argument allowlisting**: Define whitelist of allowed values for each parameter. E.g., filename can only contain alphanumerics, underscores, hyphens. Reject anything else.
3. **Input validation**: Scan parameters for shell metacharacters: | ; ` $ ( ) < > & \ ' " ! * ? [ ]. Reject if any found.
4. **Escaping as last resort**: If shell=True unavoidable, use shlex.quote() to escape arguments. E.g., subprocess.run(f"find /home -name {shlex.quote(filename)}", shell=True).
5. **Command allowlisting**: Only permit specific commands (e.g., find, grep, cat). Disallow dangerous commands (rm, dd, mkfs, nc, curl, wget).
6. **Parameter binding**: Use APIs that support parameter binding (e.g., database prepared statements, library APIs) instead of building command strings.
7. **Sandboxing + restricted user**: Run commands in container/sandbox with minimal permissions. If command injection occurs, damage is limited.
8. **Static analysis**: Add linter rule to detect shell=True. Fail CI if found.

### Detection
- Shell metacharacters or dangerous command patterns.

### Recovery
**Immediate (Stop the Attack)**
1. Kill all running commands spawned by agent (pkill, taskkill).
2. Revoke agent's access to shell/command execution.
3. Restore any deleted or modified files from backup.
4. Block or revoke access for user/attacker if identifiable.

**Investigation (Understand Scope)**
1. Retrieve command history/audit logs (bash history, auditd) to identify injected command.
2. Determine what the injected command did: files deleted, data exfiltrated, systems accessed?
3. Check system backup/snapshot to see state before attack.
4. Review all commands executed by agent in past 24-48 hours for similar injection attempts.
5. Correlate with network logs to determine if attacker exfiltrated data or established persistence.

**Remediation (Prevent Recurrence)**
1. Remove shell=True from all subprocess calls (see Prevention).
2. Implement input validation and allowlisting for all tool parameters.
3. Audit entire codebase for shell=True usage; create remediation plan for all instances.
4. Add security regression tests with adversarial input containing shell metacharacters.
5. Implement static analysis tool to detect shell=True in CI/CD; fail on detection.
6. Roll out containerization/sandboxing for all command execution.
7. Implement command audit logging and alerting (see Production Signals).

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Critical |

---

## References

- [OWASP-LLM-Top10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- Note: LLM application risks including prompt injection, insecure output handling, supply chain, sensitive information disclosure, excessive agency.
