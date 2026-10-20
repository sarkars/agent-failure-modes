# Finance Agents: Goal, Metrics, and Patterns

> **Goal:** Finance agents post to the right place, reconcile only what exists, and can't be steered into unauthorised payments.

> **Read this first.** This family is design guidance, not accounting, audit, or legal advice. Rules depend on the company, its auditors, and its jurisdiction. Every pattern here needs review by a qualified accountant or controller before use.

## Why this family exists
A chat assistant that drafts entries, matches bank lines, or prepares payments writes to books and bank accounts that other people rely on. A wrong period, an invented reconciling item, or a payment split under an approval limit looks fine in the chat and only shows up later in a report, an audit, or a loss. This family covers those failures in a chat setting.

## How we measure it
Shared metrics the patterns below report against. Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | Defined in |
|---|---|---|
| Posting errors per 1,000 entries | Under 5 (starting point) | [posting to the wrong period or account](failures/posting-to-the-wrong-period-or-account.md) |
| Unsupported reconciling items | 0 | [inventing reconciling items](failures/inventing-reconciling-items.md) |
| Split payments under thresholds flagged | 100% of test and sampled cases | [splitting payments under approval limits](failures/splitting-payments-under-approval-limits.md) |

## Patterns
| Pattern | One line |
|---|---|
| [Posting to the wrong period or account](failures/posting-to-the-wrong-period-or-account.md) | Books a September service into October, or a repair into the wrong ledger account |
| [Inventing reconciling items](failures/inventing-reconciling-items.md) | Gets the difference to zero by adding a "timing difference" nobody can find in the records |
| [Splitting payments under approval limits](failures/splitting-payments-under-approval-limits.md) | Each payment is under the limit, the total is over it, and no approver saw the real amount |

## Related
- [Payment approved by a deepfake or spoofed email](../../../../by-use-case/mortgage-documents/goals/fraud-detection/failures/deepfake-impersonation.md): a chat example on the deepfake impersonation page covers this finance case.
- [Stakes calibration](../stakes-calibration/README.md)
- [Human handoff](../human-handoff/README.md)
- [Area overview](../../README.md) · [Pattern template](../../_templates/hmi-pattern.md)
