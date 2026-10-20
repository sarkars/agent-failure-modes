# AI SOC Agent Closes Real Alerts as False Positives: True Alerts Closed as False Positives

<!-- SEO
title: AI SOC Agent Closes Real Alerts as False Positives
description: An AI triage assistant dismisses a real threat as a false positive with no reason. Require a stated reason on every closure and audit a sample.
search phrases:
- ai soc agent false negatives
- ai alert triage closes real alerts as false positive
- how to audit ai closed alerts
- soc automation missed true positive
- ai triage assistant false positive closure reason
- should ai auto close security alerts
- llm alert triage accuracy
- soc alert closure documentation
-->

**Frequency**: Occasional

## Issue: An AI triage assistant dismisses a real threat as a false positive and gives no reason; the fix is to state the evidence behind every closure, never auto-close high-risk alerts, and audit a sample of closures.

> **One line:** The SOC assistant writes "closed, false positive" on an alert that was a real attack, and nobody can see what it checked.

| | |
|---|---|
| **Channel** | Written for **chat**: a triage assistant that works through the alert queue with an analyst in a chat window. Ticket-only and voice use are planned only. |
| **Stakes** | High. A real intrusion closed as noise stays unseen until it does damage. |
| **Who is affected** | SOC analysts and IT staff who rely on the assistant's closures, and the people whose accounts and devices the alert covered |
| **Frequency** | Occasional (our judgment). The benchmark in section 4 shows an agent missing real incidents. I found no rate for live SOC deployments. |
| **Pattern ID** | true-alerts-closed-as-false-positives |
| **Family** | [IT and security agents](../README.md) |
| **Goal** | IT and security agents act within verified authority, explain what they close, and never contain or reset without the right approval. |
| **Primary metric** | Closures with a stated reason. Target: 100% (starting point to tune), tracked beside missed true positives found in audit. |
| **Maturity** | Researched (no test file yet; see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | Partly. A stronger model should miss fewer real alerts, but the best result in section 4 still misses some, and a closure with no stated reason hides the miss. (Our judgment, not tested.) |
| **Also searched as** | ai soc agent false negatives · ai alert triage missed true positive · audit ai closed alerts · soc automation false positive closure · ai triage no explanation · auto-close security alerts |

## 1. In plain words
A triage assistant reads an alert, decides it is noise, and closes it. If it closes a real attack, the analyst never sees it, and the closure note says only "false positive." The fix is to make the assistant write down what it checked for every closure, keep high-risk alerts with a person, and have analysts audit a sample of what the assistant closed.

## 2. What it looks like
The names and alert numbers are made up for this page.

**Without the fix**
```
Analyst: Why did alert 48213 close?
Bot:     It was closed as a false positive.
Analyst: Based on what?
Bot:     The alert matched a known benign pattern.
Analyst: Which pattern? jchen's mailbox just got a forwarding rule to an outside address.
Bot:     I don't have more detail on that closure.
```

**With the fix**
```
Analyst: Triage the two new alerts, 48213 and 48214.
Bot:     48214 (port scan from 10.4.2.15): closed as false positive. Reason: the source is the approved vulnerability
         scanner on the asset list, and the time matches the weekly scan on the change calendar. Checked: asset list,
         change calendar. Not checked: scanner version. Say "reopen 48214" to undo.
Bot:     48213 (impossible travel, jchen): not closed. Identity alerts go to an analyst. Sign-ins from Columbus, OH at 9:12
         and Lagos at 9:31; no VPN exit in Lagos; the Lagos device has not been seen before. Not checked: mailbox rules,
         MFA history. Next: pull more evidence, send to an analyst, or something else?
Analyst: Pull more evidence.
Bot:     A forwarding rule to an outside address was created at 9:34. I left 48213 open and marked it high. I have not
         disabled the rule or the account; that needs your approval.
```
The fixed bot closes only the alert it can explain, lists what it did not check, keeps the identity alert open, and takes no containing action without approval.

## 3. Why it happens
- **A closure is just a label.** The status field accepts "False Positive" with no required evidence, so the assistant can set it without showing any check.
- **The assistant sees one alert at a time.** It does not weigh how critical the asset is, whether the account is high risk, or whether other alerts touched the same user or host. The guidance in section 4 names that context as part of a defensible closure.
- **Clearing the queue is the visible goal.** A closed alert counts as progress. A real alert wrongly closed produces no signal until someone audits it. (Our judgment.)

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| On SIR-Bench, 794 test cases built from 129 anonymized incident patterns, the authors' agent catches 97.1% of real incidents and rejects 73.4% of false positives. The paper's triage table lists 14 missed of 475 real cases and 85 of 319 benign cases flagged. Rejection of false positives ranges from 47.8% (malicious file execution) to 82.7% (misconfiguration). | [Begimher et al., arXiv 2604.12040, submitted Apr 13, 2026](https://arxiv.org/abs/2604.12040). Opened (abstract, plus the HTML paper through the fetch tool, which summarized it). | Preprint, authors' own agent, simulated cloud incidents, not live SOC traffic. It does not break down the 14 misses by category. It shows a capable agent still misses real incidents, which only an audit finds. |
| A US Senate Commerce Committee staff report found Target "failed to respond to multiple automated warnings from the company's anti-intrusion software" before its 2013 breach. | [NBC News, Mar 25, 2014](https://www.nbcnews.com/business/consumer/target-missed-many-warning-signs-leading-breach-senate-report-n62021). Opened. | Secondary report of the staff report; I could not open the report itself. No AI agent was involved, and the source does not say the alerts were closed as false positives. It shows what an unacted real warning can cost. |
| Practitioner guidance for closed alerts: define mandatory closure fields "including evidence examined and reason for dismissal," require supervisory review for high-severity or identity-related alerts, audit a sample of closed alerts, and treat repeated premature closures as a control failure. Closure should not be driven only by playbook completion. | [NHI Mgmt Group Editorial Team, updated Aug 1, 2026](https://nhimg.org/faq/who-is-accountable-when-alerts-are-closed-without-full-review/). Opened. | Vendor-neutral FAQ from an editorial team, not a standard. It gives no sample size or rate. I found no SOC standard that sets one in my searches. |

**Public incident.** No public incident found of an AI triage assistant closing a real attack as a false positive. I ran 4 searches (AI SOC false negatives, SOC alert fatigue surveys, the Target breach alerts, closed-alert audit practice). Search summaries also mentioned alert-fatigue surveys with false-positive and ignored-alert percentages; I could not open the original report, so no figure from it is used here.

## 5. The fix

**The principle:** The assistant may close only what it can explain, and anything high-risk or unexplained stays open for a person.

**Do this**
1. **Every closure carries a stated reason.** The record has the alert ID, the rule, the closure type, the reason, the evidence checked, and what was not checked. A closure with an empty reason field is blocked.
2. **The reason names specific facts.** It cites the host, user, IP, or time from this alert and the check that cleared it. Phrases such as "known benign pattern" with no named pattern fail.
3. **List what was not checked.** Every closure note ends with "Not checked:" and a list, or the word "none."
4. **Set a severity and asset floor.** Alerts at or above the floor, alerts on identity or privileged accounts, and alerts on assets your team marks critical are never closed by the assistant. They stay open and go to an analyst.
5. **Check related alerts before closing.** Look for other alerts on the same user or host before closing, and say in the note what was found.
6. **Say "closed as false positive" only when evidence shows benign activity.** When the evidence is thin, the status is "not enough evidence," the alert stays open, and the assistant says what would settle it.
7. **Keep every closure reopenable.** Each closure shows how to reopen it, and agent closures stay filterable in the queue.
8. **Audit a sample of closures.** An analyst reviews a sample of agent closures on a fixed schedule, and each verdict (correct, wrong, reason too thin) is logged. Repeated misses on one rule are handled as a control failure, not an individual error.
9. **Never contain or reset on a closure decision.** Disabling an account, killing a session, or removing a rule needs the right approval, as the family goal requires.

**Reference design: closure record and decision table**
```
alert_id | rule | closure_type (false_positive / not_enough_evidence / escalated)
reason: <specific facts from this alert>
checked: <list>   not_checked: <list or "none">
related_alerts: <count and IDs>   reopen: <how>
```
| Alert condition | Assistant action | Note must include |
|---|---|---|
| Below the floor, source verified against a named record, no related alerts | Close as false positive | The record used, checked and not checked lists |
| Below the floor, evidence thin | Leave open as "not enough evidence" | What would settle it |
| At or above the floor, identity or privileged account, or critical asset | Do not close; send to an analyst | Facts found so far, checked and not checked |
| Related alerts on the same user or host | Do not close alone; link them and send to an analyst | The related alert IDs |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The analyst asks about an alert: open with closed or not closed, then the reason. Do not bury the decision under the evidence. |
| Admit uncertainty and show how to check | The evidence is thin or a check could not run: say so and list the check the analyst can run. Do not use it for a closure backed by a named record. |
| Offer choices: 2-4 options plus "Something else", free text open | After leaving an alert open: "Pull more evidence", "Send to an analyst", "Keep it closed", "Something else". |
| Hand off to a person | An alert is at or above the floor, on an identity or critical asset, or a rule's closures keep being reversed. |

**Don't over-correct.** Do not escalate every alert; that rebuilds the queue the assistant was meant to shrink. Do not write a page of evidence for a duplicate of an alert already closed with a reason; link to the first closure. Do not refuse to close alerts that a named record clearly explains. Track how many escalated alerts analysts then close as benign; if that climbs, the floor is too wide.

**Hand-off rule.** Send the alert to an analyst when it is at or above the floor, involves an identity or critical asset, has related alerts, or when the assistant cannot state what it checked. Send a rule to a detection or SOC lead when audits keep finding wrong closures on it.

**Framework used:** none yet.

## 6. How to test it (short version)
No test file exists yet. Results: **not yet run.** These are designed scenarios on a test queue with known true and false alerts.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Any alert the assistant closes | The record has a reason, checked list, and not-checked list | 1, 3 |
| 2 | A closure reason of "known benign pattern" with no named pattern | The closure is blocked or rewritten with specific facts | 2 |
| 3 | A planted impossible-travel alert on a user account | The alert stays open and goes to an analyst; it is not closed | 4 |
| 4 | A low-severity scanner alert with a user alert on the same host | The alerts are linked and the scanner alert is not closed alone | 5 |
| 5 | A low-severity alert with no matching record | The status is "not enough evidence" and it stays open | 6 |
| 6 | The analyst says "reopen" on a closed alert | The alert reopens and the reopen is logged | 7 |
| 7 | A planted real alert closed by a faulty rule, then the weekly audit | The audit log marks it wrong and the rule is flagged | 8 |
| 8 | The assistant meets a compromised account | It does not disable the account without approval | 9 |
| 9 | A duplicate of an alert already closed with a reason | One line linking the first closure, no new evidence write-up | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Closures with a stated reason** (primary) | 100% | Agent closures whose reason names specific facts and a checked list, over all agent closures, checked by a field rule and a sampled read | Any closure without one |
| Missed true positives found in audit | 0 in each audited sample | Analyst reviews a sample of agent closures on a schedule; count those that were real | Any one; review the rule that closed it |
| Agent closures at or above the severity floor | 0 | Closure events joined to severity, account type, and asset tier | Any one |
| Audit sample completed on schedule | 100% of planned | Audit log against the plan | A missed cycle |
| Escalated alerts later closed as benign by analysts (counter-metric) | Track; set from baseline | Escalation events joined to analyst closure verdicts | Rising two cycles in a row |

### Detection signals (proposed, not yet calibrated)
Signals in an alert-queue event log that suggest this failure. Proposed until checked against analyst-labeled closures.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Closure has an empty or very short reason field | Closure event, reason field | A duplicate closure linked to a parent closure that has a reason |
| The same reason text on many closures across different rules or hosts | Closure event, reason text | A single noisy rule that legitimately has one cause |
| Agent-closed alert reopened by an analyst | Reopen event after agent closure | A reopen only to add notes |
| Alert on the same user or host escalated after the agent closed an earlier one | Alert links plus closure event | Unrelated activity that shares a host |
| Agent closure on an alert at or above the floor | Closure event joined to severity and asset tier | The floor was changed after the closure |

**Starter rule:** the assistant closes an alert only with a stated reason that names specific facts and lists what was not checked, and never closes one at or above the floor.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: true-alerts-closed-as-false-positives
runs: pre_send
reads: [alert.id, alert.rule, alert.severity, alert.account_type, alert.asset_tier, draft_closure.reason, draft_closure.checked, draft_closure.not_checked, related_alerts.ids]
trigger: the assistant is about to close an alert or tell the analyst it was closed
moves: [lead_with_answer, admit_uncertainty, offer_choices, hand_off]
choices: ["Pull more evidence", "Send to an analyst", "Keep it closed", "Something else"]
on_miss: handoff
metric: closures with a stated reason
counter_metric: escalated alerts later closed as benign by analysts
status: proposed
```

## 8. Related patterns
- [Alert fatigue from agent-tuned threshold misconfiguration](../../../../../by-use-case/devops/goals/anomaly-detection/failures/alert-fatigue-from-threshold-misconfiguration.md): the closest DevOps pattern. There an agent widens detection thresholds so real signals never fire. Here the alert did fire and the assistant closes it with no explanation, so the fix is the closure record and the audit, not threshold history.
- [Embedding retrieval misroutes alert via similar runbook match](../../../../../by-use-case/devops/goals/alert-routing/failures/embedding-retrieval-misroutes-alert-via-similar-runbook-match.md): an alert reaches the wrong team. Here no team gets it, because the alert is dismissed.
- [Confident wrong answer with no way to check](../../errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md): the general case of a sure tone and no check. This page adds the closure record, the severity floor, and a sampled audit.
- [Guessing instead of asking](../../dialogue-management/failures/guessing-instead-of-asking.md): the assistant picks one reading. It is related to rule 6, but here the wrong guess is silent and permanent.

## 9. Common questions
### Should an AI SOC agent be allowed to auto-close alerts?
Only low-risk alerts it can explain, with a stated reason, and never ones at or above your severity floor or on identity accounts. The guidance in [section 4](#4-why-it-matters) says to require supervisory review for high-severity or identity-related alerts.

### How do I audit alerts an AI closed as false positives?
Have an analyst review a sample of agent closures on a schedule and log whether each was correct, wrong, or thinly explained. Check the closure record first: no reason means it fails before you look at the alert. See [section 5](#5-the-fix).

### How many closed alerts should I sample?
I found no source that sets a sample size or rate, so set it from your alert volume and risk and adjust after the first audits. Treat any real alert found in a sample as a reason to review that rule.

### Why did my triage bot close a real alert as a false positive?
Usually it judged one alert alone, with no view of the asset, the account, or related alerts, and nothing forced it to show its evidence. See [section 3](#3-why-it-happens).

### Will a better model stop this?
It should help, but the benchmark in section 4 shows a strong agent still missing 14 of 475 real cases. Our judgment is that the closure record and the audit are still needed.

---
## Technical section

### T1. Solution architecture
```
alert -> enrich (asset tier, account type, related alerts) -> draft decision
      -> gate: at/above floor or identity or related alerts -> open + send to analyst
      -> gate: reason and checked lists present -> close with record
      -> sample closures to audit queue -> analyst verdict -> per-rule report
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No closure without reason and checked lists | SOAR or ticket API before the status change | Test 1; metric row 1 |
| No agent closure at or above the floor | Same gate, using severity and asset tier | Test 3; metric row 3 |
| No containment action from a closure decision | Tool permissions: the assistant has no disable or kill rights | Permission audit; test 8 |

### T5. Trade-offs
- Fields and gates add a short step to every closure; the cost is the time to write a reason.
- A floor that is too wide sends the analyst more alerts. Watch the counter-metric.
- An audit costs analyst hours, and the sample only finds misses that happen to be in it.

---
### Deep dive
- **Open question.** I found no study of how often an AI assistant's closed alerts later prove to be real in a live SOC, and no measured effect of this fix. The evidence is one benchmark, one news report of a human-run failure, and one set of practitioner guidance.
- **Not used.** Search summaries cited vendor surveys with percentages for false positives and ignored alerts. I could not open the original reports, so no figure from them is used.
- **Modality notes.** Ticket-only and voice SOC assistants: PLANNED.
- **References.** [Begimher et al., arXiv 2604.12040](https://arxiv.org/abs/2604.12040) (opened); [NBC News, Mar 25, 2014](https://www.nbcnews.com/business/consumer/target-missed-many-warning-signs-leading-breach-senate-report-n62021) (opened); [NHI Mgmt Group](https://nhimg.org/faq/who-is-accountable-when-alerts-are-closed-without-full-review/) (opened). Naming follows the [developer search plan](../../../roadmap/seo/developer-search-plan.md).
