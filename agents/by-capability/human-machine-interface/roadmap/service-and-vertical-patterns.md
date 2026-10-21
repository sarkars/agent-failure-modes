# Roadmap: Service Verticals and Outbound Rules

> **Family goal:** Agents in drive-thrus, cars, government offices, airlines, banks, insurers, clinics, and rental offices behave as well as a trained person in that setting, within the rules of that field.

**How these were chosen.** These are the settings where conversational agents are already being deployed or tried, taken from the earlier backlog and from public reporting. Each row is a **candidate** and needs research first; many carry legal or expert flags. The drive-thru example comes from press reports about McDonald's ending its IBM voice-ordering test in 2024, which I read only through search summaries. Rules named here (US fair-housing law, the TCPA) need checking before anything is written.

Flags: **V** verified source · **R** needs research · **L** legal review · **E** expert review. **In the library today:** **Covered** = a pattern already exists · **Extends** = an existing pattern covers the technical failure and a new one would add the experience or design angle and a fix · **New** = no matching pattern found by file-name and keyword search (re-check before writing) · **Written** = an HMI pattern exists. **Root cause:** Model · Reliability · Business context · Governance. **Better model alone?** Yes / Partly / No. Both columns are my judgments, not measurements. See the [roadmap README](README.md).

## Drive-thru and food ordering (DT)
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags | Root cause | Better model alone? | In the library today |
|---|---|---|---|---|---|---|---|---|
| DT-01 | Order mix-ups at the speaker | Items added, dropped, or multiplied with no readback the customer can check | Read the order back and show it on screen; let the customer fix it before paying | Order accuracy at pickup; orders corrected by a person | V | Reliability | Partly | **Written**: [order mix-ups at the speaker](../goals/drive-thru-agents/failures/order-mix-ups-at-the-speaker.md) |
| DT-02 | Modifiers and customizations misparsed | 'No pickles, extra sauce' attaches to the wrong item | Parse modifiers per item and confirm them | Modifier errors per 100 customized orders | R | Model | Partly | **Written**: [page](../goals/drive-thru-agents/failures/modifiers-and-customizations-misparsed.md) |
| DT-03 | Upsell pressure at the speaker | Pushes add-ons the customer declined, as one stuck repetition | Offer once and accept the answer | Upsell offers repeated after a decline. Target: 0 |  | Business context | No | **Written**: [page](../goals/drive-thru-agents/failures/upsell-pressure-at-the-speaker.md) (CP-01 covers help that turns into a sales pitch) |
| DT-04 | Screen and spoken order disagree | The board shows one thing and the speaker says another | Make the visible order the source of truth and speak from it | Mismatches between display and spoken readback. Target: 0 |  | Reliability | No | **Written**: [page](../goals/drive-thru-agents/failures/screen-and-spoken-order-disagree.md) |
| DT-05 | Allergy and dietary requests handled loosely | 'No peanuts' treated as a preference, with no note to the kitchen | Flag allergies to staff and never promise safety the system can't give | Allergy flags that reach the kitchen. Target: 100% | E, L | Business context | No | **Written**: [page](../goals/drive-thru-agents/failures/allergy-and-dietary-requests-handled-loosely.md) |

## In-car and smart-home assistants (IC)
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags | Root cause | Better model alone? | In the library today |
|---|---|---|---|---|---|---|---|---|
| IC-01 | Replies too long or visual for a driver | Long answers or on-screen prompts while driving | Keep replies short, spoken, and hands-free | Reply length in seconds in driving mode; eyes-off-road tasks. Target: 0 for visual-only steps | E, L | Business context | No | **Written**: [page](../goals/in-car-and-home-assistants/failures/replies-too-long-or-visual-for-a-driver.md) |
| IC-02 | Smart-home commands go to the wrong device or room | 'Turn off the light' hits another room | Resolve by room and ask when unclear | Wrong-target commands per 1,000 |  | Reliability | Partly | **Written**: [page](../goals/in-car-and-home-assistants/failures/smart-home-commands-go-to-the-wrong-device-or.md) |
| IC-03 | Anyone can issue a sensitive voice command | A guest or a TV unlocks a door or places an order | Require voice match or confirmation for sensitive actions | Sensitive commands run without verification. Target: 0 | L | Governance | No | New (EX-25 covers cloned voices defeating voice authentication) |
| IC-04 | Always-listening surprises | People learn later what was recorded and kept | Show what was heard, and let people delete it | Recordings reviewed or deleted by users; complaints about unexpected recording | L | Governance | No | New (VO-21 and GV-12 cover wake words and recording notices) |
| IC-05 | Purchases by children or the TV | A child or a broadcast triggers an order | Require a code for purchases and filter broadcast audio | Unintended purchases. Target: 0 | L | Reliability | No | New |

## Government and public services (GS)
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags | Root cause | Better model alone? | In the library today |
|---|---|---|---|---|---|---|---|---|
| GS-01 | Eligibility answers sound like decisions | A chat says 'you qualify' for a benefit with no authority to say so | Say what is general guidance and what only the agency decides | Eligibility answers that state what is a guess. Target: 100% | L, E | Business context | No | **Written**: [eligibility answers sound like decisions](../goals/government-service-agents/failures/eligibility-answers-sound-like-decisions.md) |
| GS-02 | Plain-language and language access gaps | Program rules are given in dense text, or only in English | Offer plain language and the required languages | Reading level; access in required languages. Target: set by the agency | L | Business context | Partly | New (LG-04 covers unchecked translation) |
| GS-03 | Deadlines and document lists wrong or stale | Gives last year's deadline or form | Cite the date of the source and link to it | Answers with a stale deadline. Target: 0 |  | Business context | No | **Extends**: [knowledgebase staleness](../../../by-use-case/support-services/goals/issue-resolution/failures/knowledgebase-staleness.md) |
| GS-04 | Identity checks exclude people without standard IDs | Verification that needs a document or credit history some people lack | Offer alternative ways to verify | Completion of verification by group | L | Business context | No | New |
| GS-05 | No appeal or human path for denials | A denial with no way to ask a person to review it | Always say how to appeal and reach a person | Denials that include an appeal route. Target: 100% | L | Governance | No | New (GV-37 covers explanations for consequential decisions) |

## Travel and utilities (TV)
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags | Root cause | Better model alone? | In the library today |
|---|---|---|---|---|---|---|---|---|
| TV-01 | Disruption rebooking with wrong rules and no human path | Misquotes fare rules during a cancellation, or traps the traveler in the bot | Quote the real rule, and offer a person when stakes are high | Rebooking outcomes that match the policy; wait to reach a person during disruptions | R | Business context | No | New |
| TV-02 | Outage updates generic or late | Utility and telecom updates say 'we are working on it' and nothing more | Give cause, area, and next update time, and update on schedule | Updates with an estimated next update time. Target: 100% |  | Business context | No | New |
| TV-03 | Refund and credit rules misquoted | States a refund policy that is out of date or doesn't apply to the fare or plan | Quote from the live policy and the customer's own terms | Policy quotes that match the live policy |  | Business context | No | **Extends**: [knowledgebase staleness](../../../by-use-case/support-services/goals/issue-resolution/failures/knowledgebase-staleness.md) |
| TV-04 | Group bookings mix up travelers | Names, seats, or needs swapped across people in one booking | Treat each traveler separately and confirm | Traveler-attribute errors per group booking |  | Reliability | No | New |

## Banking and fraud contact (BK)
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags | Root cause | Better model alone? | In the library today |
|---|---|---|---|---|---|---|---|---|
| BK-01 | Fraud-alert conversations that look like phishing | Asks the customer to click a link and verify, as scammers do | Use a verified channel and never ask for a full code or password | Fraud-alert flows reviewed against anti-phishing guidance. Target: 100% | L, E | Business context | No | New |
| BK-02 | Unusual activity explained too vaguely | 'We saw something suspicious' with no detail to help the customer decide | Say what was seen and what to do, without helping a fraudster | Customers who can act on the alert without calling | E | Business context | Partly | New |
| BK-03 | Disputed-transaction intake loses details | The bot collects a dispute and the human has to ask again | Capture the required fields once and pass them on | Disputes needing a second contact for missing data |  | Business context | No | **Extends**: [handoff context incompleteness](../../../cross-cutting/operations/goals/agent-handoffs-delegation/failures/handoff-context-incompleteness.md) |

## Insurance claims intake (CI)
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags | Root cause | Better model alone? | In the library today |
|---|---|---|---|---|---|---|---|---|
| CI-01 | Cold handling of a loss | A claim after a fire or a death gets a form-filling tone | Acknowledge the loss once, then make the next step easy | Claimant sentiment after intake; escalations on tone |  | Business context | Partly | **Extends**: [stakes-blind register](../goals/stakes-calibration/failures/stakes-blind-register.md) |
| CI-02 | Coverage answers sound like guarantees | 'You're covered' before the claim is reviewed | Say what is generally covered and what the claim decision depends on | Coverage statements with a stated condition. Target: 100% | L | Business context | No | New |
| CI-03 | Photo-evidence guidance fails | Asks for photos that can't show the damage, or rejects usable ones | Tell people exactly what to capture, with examples | Claims needing a second photo request |  | Business context | Partly | **Extends**: [low resolution](../../document-processing/goals/accurate-text-extraction/failures/low-resolution.md) |

## Health scheduling and patient messages (HS)
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags | Root cause | Better model alone? | In the library today |
|---|---|---|---|---|---|---|---|---|
| HS-01 | Triage wording understates or overstates urgency | Tells someone with warning signs to wait, or sends everyone to the ER | Use validated triage rules and clear escalation wording | Triage agreement with clinician review | E, L | Business context | No | New (the library has telehealth-triage patterns; this adds the wording and flow) |
| HS-02 | Medication instructions misunderstood | Reminders and instructions leave out timing, food, or what to do on a missed dose | Confirm understanding of critical steps | Comprehension check pass rate on key instructions | E | Business context | No | New |
| HS-03 | Scheduling picks the wrong provider or visit type | Books a follow-up as a new visit, or with a clinician who can't treat the issue | Match visit type and provider rules | Rescheduled-for-wrong-type rate |  | Business context | No | New |
| HS-04 | Results delivered without context | Test results sent by message with no explanation or next step | Pair results with explanation and a person to ask | Results messages with a next step and contact. Target: 100% | E, L | Business context | No | New |

## Real estate and rentals (RE)
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags | Root cause | Better model alone? | In the library today |
|---|---|---|---|---|---|---|---|---|
| RE-01 | Steering by protected class in recommendations | Suggests neighborhoods or units based on signals tied to protected classes | Test for disparate recommendations and restrict inputs | Recommendation differences by protected-class proxy | L, E | Governance | No | New (US fair-housing law applies; check the rules before writing) |
| RE-02 | Maintenance emergencies not recognized | A gas smell or no heat is routed as a routine ticket | Detect emergencies and give safety steps and a human route | Emergencies handled within the required time. Target: 100% | E, L | Business context | No | New (VA-02 covers emergency phrases in routine calls) |

## Outbound messaging rules (LC)
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags | Root cause | Better model alone? | In the library today |
|---|---|---|---|---|---|---|---|---|
| LC-01 | Marketing texts without consent | Sends promotional messages to numbers that never opted in | Record consent, scope, and time, and check before sending | Messages sent without recorded consent. Target: 0 | L | Governance | No | New (US rules such as the TCPA apply; EX-24 covers voice calls) |
| LC-02 | Quiet hours and time zones ignored | Messages or calls arrive at night in the recipient's time zone | Schedule by the recipient's local time | Contacts outside permitted hours. Target: 0 | L | Reliability | No | New |
| LC-03 | Do-not-call lists not checked | Contacts numbers that opted out | Check suppression lists before each contact | Contacts to suppressed numbers. Target: 0 | L | Governance | No | New (SA-02 covers unsubscribe requests in sales email) |

## Role-play and bereavement (RP)
| ID | Pattern | What goes wrong | Goal | Primary metric (starting target) | Flags | Root cause | Better model alone? | In the library today |
|---|---|---|---|---|---|---|---|---|
| RP-01 | Role-play drifts into harmful or unwanted territory | A story or persona escalates beyond what the user chose | Set limits for role-play and check in at turning points | Role-play turns flagged by safety review | L, E | Model | Partly | New (CC-16 covers romantic or parasocial dependence) |
| RP-02 | Bereavement handled with scripts | Account closures after a death use form language and ask the family for proof repeatedly | Give a dedicated, gentle path and ask for documents once | Contacts needed to complete a bereavement closure | E | Business context | No | **Extends**: [stakes-blind register](../goals/stakes-calibration/failures/stakes-blind-register.md) |
