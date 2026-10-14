<!--
HMI PATTERN TEMPLATE
Rules:
1. A reader must understand the failure and the fix in 60 seconds, from the top of the file.
2. Sections 1-5 are the "quick read". Everything after the divider is optional depth.
3. The Fix (section 5) is REQUIRED and must contain a reference design a team can copy.
4. Cite only sources you could verify. Say when a number is vendor-reported, secondhand, or from a different
   setting (e.g. human-to-human research). Never invent statistics.
5. Keep example transcripts short (6-10 lines). Show the failure and the fixed version side by side.
-->

# [Pattern name in plain words]

> **One line:** [What goes wrong, in one sentence a non-engineer would understand.]

| | |
|---|---|
| **Channel** | Chat / Voice / Visual / All (say which are written, which are planned) |
| **Stakes** | Low / Medium / High / Any |
| **Who is affected** | [All users / a specific group / a specific situation] |
| **Frequency** | Very common / Common / Occasional / Rare, plus how you know |
| **Family** | [e.g. conversation-leadership] |

## 1. In plain words
[2-3 sentences. No jargon.]

## 2. What it looks like
**Without the fix**
```
User: ...
Bot:  ...
```
**With the fix**
```
User: ...
Bot:  ...
```
[One sentence on what changed.]

## 3. Why it happens
- [Cause 1]
- [Cause 2]
- [Cause 3 at most]

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| [Verified finding] | [link] | [e.g. human-to-human study; vendor survey] |

## 5. The fix
**The principle:** [one sentence]

**Do this**
1. [Concrete, testable rule]
2. [...]

**Reference design** [prompt block, state schema, flow, decision table, or improved transcript]

**Don't over-correct** [the opposite failure this fix can cause, and the guardrail]

**Hand-off rule** [when to move to a human or another channel]

**Framework used:** [link to solutions-library page]

## 6. How to test it
| # | Scenario | Pass if |
|---|---|---|
| 1 | | |

## 7. How to spot it in production
| Signal | What it means |
|---|---|
| | |

## 8. Related patterns
- [link] - [how it differs]

---
### Deep dive (optional)
- Root-cause detail
- Edge cases
- Modality notes (voice / visual: what changes; mark as PLANNED if not yet written)
- References
