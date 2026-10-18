# Test Files: How to Check Whether Your Assistant Has a Pattern

**Each flagship pattern has a test file here: 10 to 20 short conversations and a pass/fail rubric you can run against any assistant.** The tests tell you whether your bot shows the failure. They are not a score for any product, and a pattern is only labeled *Tested* after someone runs them and records the result.

## Format
Each test file is named after its pattern (`<pattern-file-name>.md`) and has:

1. **Pattern link and goal.** The pattern page and its primary metric.
2. **Rubric.** One line per rule in the fix. Each line says what counts as pass and what counts as fail. Every test below maps to a rubric line.
3. **Conversations.** Numbered scenarios. Each has the setup (what the assistant knows), the user turns, and the expected behavior. Use US examples. No real people's data.
4. **Results.** A table of model name, version, date, who ran it, and pass counts per rubric line. It says **"Not yet run"** until a real run is recorded. Never write results you did not obtain.

## Rules
- A conversation tests one thing. If it can fail for two reasons, split it.
- Include at least two conversations where the right behavior is to do **nothing special** (to catch over-correcting).
- Keep user turns realistic: typos, short replies, and incomplete information.

## Related
- [Execution plan](../roadmap/execution-plan.md)
- [Content program](../roadmap/content-program.md)
