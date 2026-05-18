# Contributing to AI Agent Failure Taxonomy

Thank you for helping document real-world AI agent failures! Your contributions help the community build more reliable systems.

## How to Contribute

### Adding a New Issue

1. Navigate to the appropriate agent type folder under `agents/`
2. Find or create the relevant goal file
3. Add your issue using the template below

### Issue Template

```markdown
### Issue: [Short descriptive name]

**Frequency**: Common | Occasional | Rare

**Symptoms**
- What the user/system observes when this fails

**Root Cause**
Why this happens at a technical level

**Example**
```
Input: [example input]
Expected: [what should happen]
Actual: [what actually happens]
```

**Mitigation Strategies**
1. [First mitigation approach]
2. [Second mitigation approach]

**Detection**
How to identify this issue in production (logs, metrics, alerts)

**Related Issues**
- Links to related issues in this repo or external resources
```

### Adding a New Agent Type

1. Create a new folder under `agents/` with the pattern `[agent-type]-agent/`
2. Add a `README.md` describing the agent type
3. Create goal files for each major goal category
4. Add at least 3 documented issues per goal

### Adding a New Goal Category

1. Create a new `.md` file in the agent folder
2. Use kebab-case naming: `goal-name.md`
3. Start with an overview of the goal
4. Document at least 2 issues

## Quality Guidelines

- **Be specific**: Include concrete examples, not abstract descriptions
- **Share real data**: Sanitize but include actual inputs/outputs when possible
- **Document mitigations that work**: Focus on practical solutions you've tested
- **Include detection methods**: Help others find these issues in their systems

## What We're Looking For

- Issues you've encountered in production deployments
- Edge cases that documentation doesn't cover
- Failures that took significant time to debug
- Patterns that repeat across different implementations

## What We're NOT Looking For

- Theoretical or hypothetical failures
- Well-documented issues already covered elsewhere
- Security vulnerabilities (report these privately)
- Vendor-specific bugs (report to vendors)

## Code of Conduct

- Be constructive - we're all learning from failures
- Respect confidentiality - sanitize proprietary information
- Give credit where due - cite sources and collaborators

## Questions?

Open an issue with the `question` label or start a discussion.
