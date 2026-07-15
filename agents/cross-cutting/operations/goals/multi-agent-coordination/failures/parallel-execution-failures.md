# Parallel Execution Failures

## Issue: Agents Operating in Parallel Cause Conflicts or Inconsistencies

**Frequency**: Common

**Symptoms**
- Race conditions when agents modify shared state
- Duplicate work from uncoordinated parallel execution
- Inconsistent outputs from parallel agents
- Resource contention between concurrent agents
- Results merged incorrectly from parallel branches

**Root Cause**
Multi-agent systems often run agents in parallel for efficiency. Without proper coordination, parallel agents may read stale state, overwrite each other's work, duplicate effort, or produce inconsistent results that can't be merged. The non-deterministic nature of parallel execution makes these issues intermittent and hard to reproduce.

**Example**
```
Scenario: Code editing multi-agent system

Task: "Refactor the authentication module"

Parallel agent execution:
  Agent A: Refactors auth.py (renames functions)
  Agent B: Updates tests for auth.py
  Agent C: Updates documentation for auth.py

Timeline:
  T0: All agents read current auth.py
  T1: Agent A renames login() → authenticate()
  T2: Agent B writes tests calling login() (stale name)
  T3: Agent A commits changed auth.py
  T4: Agent B commits tests (now broken - login doesn't exist)
  T5: Agent C commits docs referencing login() (also stale)

Result:
  - Tests fail (function renamed)
  - Documentation incorrect
  - 2 of 3 parallel branches produce invalid output
  
Required coordination:
  - Lock on files being modified
  - Sequential execution for dependent changes
  - State refresh before each agent writes
  - Merge conflict detection
```

**Key Statistics**
From Parallel Execution Research (2026):
- 35% of parallel multi-agent tasks have coordination issues
- Race conditions cause 12% of agent output errors
- Duplicate work rate in uncoordinated systems: 20-40%
- Merge conflict rate: 15-25% for overlapping work
- Parallel efficiency (actual vs. theoretical): 60-75%

**Parallel Failure Types**
| Type | Cause | Impact |
|------|-------|--------|
| Race condition | Concurrent state access | Corruption |
| Duplicate work | No work claiming | Waste |
| Merge conflicts | Overlapping edits | Manual fix needed |
| Stale reads | No cache invalidation | Wrong output |
| Resource contention | Shared resource limits | Deadlock/delays |

**Contributing Factors**
- No locking mechanism for shared resources
- Optimistic concurrency without validation
- No work distribution coordination
- Missing merge conflict handling
- Stale state used for decisions
- No parallel execution visibility

## Mitigation Strategies

### Prevention
1. **File-level locking for dependent artifacts**: The refactor example fails because Agent A renames `login()` to `authenticate()` in `auth.py` while Agent B and C are simultaneously writing tests and docs that reference the old name — all three read the same stale state at T0. Require an agent about to rename/change a public interface to acquire a lock on that symbol across all files that reference it before any agent proceeds with dependent work. Trade-off: locking serializes work that could otherwise run in parallel, partially undoing the point of parallel execution.
2. **Dependency-aware work partitioning instead of blind topic partitioning**: The task was split by artifact type (code / tests / docs) without recognizing that tests and docs both structurally depend on the code agent's function names — a partitioning that looks clean (3 agents, 3 files) but has a hidden dependency edge. Partition work by analyzing which agents' outputs are inputs to others (tests and docs depend on the renamed API) and sequence those specific dependent pairs rather than the whole task. Trade-off: dependency analysis adds planning overhead and may serialize work that turns out not to actually conflict.
3. **State refresh immediately before commit, not just at task start**: All three agents read `auth.py` "at T0" and never refreshed before their own T3-T5 commits, so Agent B commits tests against a name that had already changed at T3. Require each agent to re-read the current state of any shared file immediately before writing/committing, not just once at task start. Trade-off: re-reading before every write adds latency and I/O, especially costly for agents that write frequently.

### Detection & Response
1. **Stale-reference detector on commit**: Since the failure is precisely that Agent B's tests and Agent C's docs reference `login()` after it no longer exists, run a symbol-existence check (e.g., a lightweight static check or test run) immediately after each agent's commit and flag references to renamed/removed symbols before merging.
2. **Interleaved-timeline reconstruction**: Log each agent's read-timestamp and write-timestamp per shared file; the root failure pattern here (read at T0, write at T2-T5 without refresh) is detectable by comparing an agent's write-time against the shared file's last-modified time — if the file changed between an agent's read and its write, flag a stale-write risk before allowing the commit.
3. **Post-merge test-pass verification**: The observable outcome is "tests fail (function renamed)" — so gate merges of parallel branches on the merged test suite actually passing, not just on the absence of textual merge conflicts, since this failure produces a clean textual merge with broken semantics.

### Architecture Patterns
1. **Coordinator agent for the specific rename-fanout case**: A dedicated coordinator that owns "public API surface changes" would see Agent A's plan to rename `login()` and proactively notify/block Agent B and C until the rename lands, rather than letting three agents work from an assumed-stable snapshot. Deployment consideration: the coordinator needs visibility into planned (not just completed) changes, which requires agents to declare intent before executing.
2. **Saga pattern with compensating steps for cross-file renames**: Treat "rename a function" as a saga spanning code + tests + docs — if the docs/tests steps fail because they were based on stale state, the saga triggers a compensating re-generation step against the now-current code rather than leaving broken tests/docs merged in. Deployment consideration: requires defining compensating actions per artifact type, which is extra design work beyond simple locking.
3. **Optimistic concurrency with commit-time conflict detection**: Let all three agents work in parallel from the T0 snapshot (as they did), but require each commit to include the snapshot version it was based on, and reject/re-run Agent B and C's commits if `auth.py`'s version changed underneath them (Agent A's rename) instead of silently accepting stale-based work. Deployment consideration: rejected agents must be re-triggered automatically, or their work silently disappears, recreating the "dropped work" failure from task-handoff-errors.

### Metrics
1. **stale_write_rate**: Target < 3% of parallel commits based on state that changed since the agent's last read; Alert if > 10% over a rolling window.
2. **post_merge_test_pass_rate**: Target > 98% of parallel-branch merges pass the full test suite immediately after merge; Alert if < 90%, matching the example's "2 of 3 branches invalid."
3. **duplicate_work_rate**: Target < 5% of parallel tasks producing overlapping/redundant output (per the 20-40% uncoordinated baseline this should meaningfully beat); Alert if > 15%.
4. **parallel_efficiency**: Target actual/theoretical speedup > 75% (upper end of the 60-75% baseline range cited); Alert if < 50%.

### Alerts
1. **Cross-Artifact Stale Reference** (P1): Condition - a committed artifact (test, doc) references a symbol/name that no longer exists in its dependency (code file) after a parallel merge. Action: block the merge, notify the owning agents, and trigger regeneration of the stale artifact against current state.
2. **Concurrent Write Without Refresh** (P2): Condition - two or more agents write to overlapping files where at least one agent's read timestamp predates another agent's completed write to the same file. Action: reject the stale write, force a state refresh, and re-queue that agent's task.
3. **Post-Merge Test Failure** (P1): Condition - the test suite fails immediately after a parallel-branch merge that had no textual conflicts. Action: revert the merge, isolate which branch introduced the semantic break, and route to the coordinator agent for resequencing.

## References

- [MAST Taxonomy](https://arxiv.org/abs/2503.13657) - Multi-agent failure modes (36.94% coordination failures)
- [Redis: Multi-Agent Systems Fail](https://redis.io/blog/why-multi-agent-llm-systems-fail/) - Coordination patterns
- [Augment Code: Multi-Agent Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - Parallel execution
- [Microsoft: Failure Modes in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Agent coordination
- [Replit Rogue Agent](https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incident/) - Uncoordinated agent actions
