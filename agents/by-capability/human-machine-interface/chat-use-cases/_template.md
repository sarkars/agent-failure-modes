<!-- Template for one narrow chat use case. Copy to <use-case-name>.md. Do not add link syntax with placeholder targets: the link checker will flag it. -->
# [Use case]: Guardrails, Instructions, and Evals Backed by Metrics

**[One sentence: who talks to the assistant, what it is for, and the one thing it must never get wrong.]**

| Field | Answer |
|---|---|
| **Use case ID** | CU-nn |
| **Industry and user** | |
| **Business goal** | One sentence, with the primary metric in section 2 |
| **Stakes** | Low / Medium / High / Critical, and why |
| **Tier** | A (public evidence, lower stakes) / B (regulated) / C (high-stakes relational; needs expert review before instructions are published) |
| **Maturity** | Untested draft / Evals written / Tested / Verified |
| **Reviews required** | Legal, clinical, child-safety, or accessibility review, as flagged |
| **Last reviewed** | Date |

> **Read this first.** Design guidance, not legal, clinical, or other professional advice. Every threshold is a starting point set from your own baseline unless a source is cited. Instructions and guardrails below are **untested drafts** until a recorded test run says otherwise.

## 1. The use case
Who the user is, where the chat lives, what the assistant can see and do, what it cannot do, and when a person takes over.

## 2. Goals and metrics
| Goal | Primary metric | Counter-metric (what it must not harm) | Baseline method | Owner |
|---|---|---|---|---|

## 3. Instructions (system prompt blocks)
Each block is short and does one job. Each points to a failure pattern and a ledger row.
| Block | Text | Prevents | Ledger |
|---|---|---|---|

## 4. Guardrails
Input checks, output checks, action limits, and hand-over rules.
| Guardrail | Type (input, output, action, hand-over) | Rule | Prevents | Ledger |
|---|---|---|---|---|

## 5. Evals
| Eval | What it tests | Test set (how built, how many) | Pass rule | Ledger |
|---|---|---|---|---|

Judge-based evals say how the judge is checked against human labels before its scores are trusted.

## 6. Metric ledger
The spine of the guide. Every instruction, guardrail, and eval above appears here with its metric.
| Ledger | Item | Failure pattern | Metric | How measured | Counter-metric | Threshold basis |
|---|---|---|---|---|---|---|
| L-01 | | | | Logs, eval, or sampled review | | Set from baseline / cited source |

## 7. Production dashboard and alerts
| Metric | Definition | Source | Alert method |
|---|---|---|---|

## 8. Failure patterns this guide uses
Links to written patterns, and candidates still to be written.

## 9. Legal and expert flags
What a lawyer, clinician, child-safety expert, or accessibility reviewer must check, and what is still unreviewed.

## 10. Open decisions for the business owner
