# AI Agent Memory Safety Failures: Poisoning, Wrong Recall, and Failure to Forget

**Memory safety failures happen when an agent remembers, recalls, or forgets the wrong thing: poisoned memories get trusted, private memory is used in the wrong context, a deletion request is ignored, or a soft preference is treated as a hard rule.** Ten patterns cover safe memory operations.

## Key Takeaways

- Wrong recall and missing recall are separate failures: using the wrong fact versus not using a relevant one.
- Memory can be an attack surface: malicious or wrong content gets stored and later trusted.
- Users need to be able to make the agent forget, and the agent needs to honor it.
- Preferences and instructions are different things and should not be mixed up.

## Patterns

| Pattern | What goes wrong |
|---|---|
| [Context Window Overflow with Silent Truncation](failures/context-window-overflow-silent-truncation.md) | Agent Silently Drops Input Context When Message Exceeds Context Window |
| [Incorrect Memory Recall](failures/incorrect-memory-recall.md) | Agent recalls wrong past preference or fact |
| [Memory Conflict](failures/memory-conflict.md) | Two memories contradict; agent fails to resolve |
| [Memory Deletion Failure](failures/memory-deletion-failure.md) | Agent fails to forget information when requested |
| [Memory Poisoning](failures/memory-poisoning.md) | Malicious or wrong content gets stored and later trusted |
| [Memory Privilege Leak](failures/memory-privilege-leak.md) | Agent uses private memory in inappropriate context |
| [Missing Memory Recall](failures/missing-memory-recall.md) | Agent fails to use relevant durable information |
| [Outdated Memory](failures/outdated-memory.md) | Agent uses information that changed |
| [Over-Applied Memory](failures/over-applied-memory.md) | Agent applies a past preference where it does not belong |
| [Preference Vs Instruction Confusion](failures/preference-vs-instruction-confusion.md) | Agent treats a soft preference as a hard rule |

**Total: 10 patterns**

## How These Patterns Group

- **Recall:** [Incorrect Memory Recall](failures/incorrect-memory-recall.md), [Missing Memory Recall](failures/missing-memory-recall.md), [Outdated Memory](failures/outdated-memory.md), [Over-Applied Memory](failures/over-applied-memory.md), [Preference Vs Instruction Confusion](failures/preference-vs-instruction-confusion.md)
- **Integrity:** [Memory Conflict](failures/memory-conflict.md), [Memory Poisoning](failures/memory-poisoning.md)
- **Privacy and deletion:** [Memory Privilege Leak](failures/memory-privilege-leak.md), [Memory Deletion Failure](failures/memory-deletion-failure.md)
- **Context limits:** [Context Window Overflow with Silent Truncation](failures/context-window-overflow-silent-truncation.md)

## When This Matters

- The agent keeps durable memory about users
- Users can ask to delete their data
- Memory is written from untrusted content

## Frequently Asked Questions

### What happens if an agent's memory is poisoned?

See [memory poisoning](failures/memory-poisoning.md).

### Why does my agent still remember something I asked it to forget?

See [memory deletion failure](failures/memory-deletion-failure.md).

### Why does my agent apply an old preference where it does not belong?

See [over-applied memory](failures/over-applied-memory.md) and [preference vs instruction confusion](failures/preference-vs-instruction-confusion.md).

### What is the difference between memory safety and memory management?

[Memory management](../memory-management/) covers storage and retrieval quality. This goal covers what is safe to remember, recall, and delete.

## Related

- [All operations goals](../)
- [Operations overview](../../)
