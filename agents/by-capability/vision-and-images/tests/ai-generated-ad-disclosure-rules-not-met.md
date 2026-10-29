# Test File: AI-Generated Ad Disclosure Rules Not Met

**Pattern:** [AI-Generated Ad Disclosure Laws by Market: When One Market's AI Label Rule Is Missed](../goals/ai-image-generation-business-risks/failures/ai-generated-ad-disclosure-rules-not-met.md)
**Pattern ID:** ai-generated-ad-disclosure-rules-not-met
**Goal:** AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm.
**Primary metric:** Unchecked market launch rate: creative-market pairs that went live with no gate decision logged against a current register row, divided by all live creative-market pairs sampled (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a campaign workflow (asset tags, flight setup, disclosure register and pre-launch gate) shows the failure. They do not test whether any label meets any law; that is counsel's call, and the register rows used here are fixtures, not legal conclusions. Run them in a test ad account or on paused flights with no spend, and never let a test ad reach the public. All brands, assets, people, rows and IDs below are invented. Covers image and video. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Counsel-owned register | Every row has rule, trigger, label, effective date, status, reviewer and review date; the register says it is not complete | A row missing any field is used by the gate |
| R2 | 2. Expand flights into legal markets | "US national" and "EU" are expanded before the gate runs | Gate runs on "US national" as one market |
| R3 | 3. Tag AI facts at intake | Blank or "unknown" tags block the gate | Gate runs with blank tags |
| R4 | 4. Gate every creative-market pair | Each pair gets one of the five outcomes, and "no row" is held | A pair launches with no outcome, or "no row" passes |
| R5 | 5. Hold only that market | Other markets proceed | Whole campaign held, or the held market launches |
| R6 | 6. Labels per market | Each market version carries its row's label; platform label counts only if the row says so | One label for all markets, or platform label accepted against the row |
| R7 | 7. Stale rows block | Row past review date holds new launches in that market | Launches on a stale row |
| R8 | 8. Re-run on change | New market, cut, AI edit or re-tag re-runs the gate | Change goes live on the old decision |
| R9 | 9. Log every decision | Log has creative version, market, row and review date, outcome, label, decider, date | Missing log or fields |
| O | Don't over-correct | Reviewed rows with no trigger pass with no label added; ordinary retouching does not trigger AI rows | Held "to be safe," or a generic AI label forced on every market |

## Test cases
1. **US national hides New York (R2, R4, R6).**
   Setup: Creative "Harbor Coffee / morning-spot-v2" (fake), tagged "AI-generated person, not a real person." Fixture row US-NY: label required, label file "NY end card," status in force, reviewed last month. Flight: "US national," no state list.
   Action: Schedule the flight.
   Pass: Flight expanded; US-NY pair blocked because the NY label is not attached; other states with no row are held as "not reviewed."
   Fail: Flight schedules as one US market with no NY check.
2. **Blank AI tags (R3).**
   Setup: Upload a 15s video with the AI tag fields empty.
   Action: Run the gate for Germany.
   Pass: Gate blocked; the tool asks one question about whether the person shown is real, AI-made or AI-edited.
   Fail: Gate runs and returns "no rule matched."
3. **Counsel decision needed (R4, R5).**
   Setup: Fixture rows DE and FR say "counsel decides if this is a deep fake." Flight: DE, FR, CN. CN row satisfied.
   Action: Run the gate.
   Pass: DE and FR held and routed to the named counsel with creative, tags and row; CN proceeds.
   Fail: All three held, or DE and FR launch.
4. **Market with no row (R4).**
   Setup: Add Brazil to a flight; the register has no Brazil row.
   Action: Run the gate.
   Pass: Brazil held with the words "not reviewed" and the register owner named.
   Fail: Brazil passes as "no rule."
5. **Platform label only (R6).**
   Setup: Fixture row requires the advertiser's own label and says the platform label does not count. Only the platform's automatic AI label is on.
   Action: Run the gate for that market.
   Pass: Blocked for a missing label.
   Fail: Passes on the platform label.
6. **Stale row (R7).**
   Setup: Fixture row CN with a next-review date 10 days ago.
   Action: Schedule a new CN flight.
   Pass: Held until counsel re-reviews; the hold names the row and its review date.
   Fail: Launches.
7. **New market after approval (R8).**
   Setup: Approved flight US-NY and CN. Add France after approval.
   Action: Save the flight change.
   Pass: Gate re-runs for the France pair before it can launch.
   Fail: France launches on the old approval.
8. **Log completeness (R9).**
   Setup: Run tests 1 to 7 and 9.
   Action: Export the gate log.
   Pass: Every decision has all fields listed in R9.
   Fail: Any decision is missing or has blank fields.
9. **Incomplete register row (R1).**
   Setup: Fixture row FR with no reviewer and no review date.
   Action: Run the gate for France.
   Pass: The gate will not use the row; France is held and routed to the register owner.
   Fail: The gate uses the row and returns an outcome.
10. **DNS: reviewed row, no trigger (O).**
   Setup: Product-only creative tagged "no AI person, not AI-edited." Fixture US-NY row reviewed and current.
   Action: Run the gate.
   Pass: Passes with no label added.
   Fail: Held, or a label forced on.
11. **DNS: per-market labels differ (O).**
    Setup: Rows for US-NY and CN name different label files.
    Action: Run the gate.
    Pass: Each market carries its own label; the tool does not replace both with one generic "AI" label.
    Fail: One label forced on both.
12. **DNS: color correction (O).**
    Setup: Photo-shoot creative with only exposure and color correction, tagged as such.
    Action: Run the gate for all markets.
    Pass: No AI row triggered.
    Fail: Tagged or held as AI-edited.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |

## Notes
Test 1 follows New York's synthetic performer disclosure rule (NY Senate S8420A; in effect June 9, 2026 per Cooley and AP), cited on the page; the row contents are fixtures, and real wording comes from counsel. Test 3 follows EU AI Act Article 50(4), whose deep fake trigger needs a legal judgment. Test 11 follows Loeb & Loeb's summary that China's national standard sets label formats. The rest are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
