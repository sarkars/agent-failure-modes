# Phase A: Research Discovery — Pattern Candidates

Research-backed high-priority failure patterns to add across new categories.
Each candidate includes: failure name, domain, source(s), justification for inclusion.

---

## Vision & Image Understanding (15 candidates)

Emerging failures as agentic vision becomes central to agent workflows (GPT-4o, Claude 3.5 Vision, etc).

| Pattern | Root Cause | Research Sources |
|---|---|---|
| **Visual Object Hallucination** | Vision model detects objects not present (salience bias, training data imbalance) | [Hallucination of Multimodal LLMs Survey, arXiv 2404.18930](https://arxiv.org/html/2404.18930v2) |
| **Spatial Reasoning Failure** | Incorrect 3D/2D relationships, bounding box errors, relative positioning | [Vision Transformers spatial blindness, CVPR 2024 work on spatial reasoning](https://arxiv.org/abs/2401.00168) |
| **Multi-Image Reconciliation** | Conflicting information across multiple images; agent can't triangulate | [Multi-image RAG challenges, LLamaIndex blog 2025](https://www.llamaindex.ai/blog/document-ai-the-next-evolution-of-intelligent-document-processing) |
| **Generated Image Quality Drift** | DALL-E/Midjourney generated images degrade in quality over agentic loops | Internal observation: generative models producing lower-quality outputs on iterative refinement |
| **Adversarial Image Bypass** | Adversarial perturbations fool vision-based agent decisions | [Adversarial Examples survey, arXiv 2303.13008](https://arxiv.org/abs/2303.13008) |
| **Chart/Graph Misinterpretation** | Axis labels, legend misreading, trend direction errors | [Matcha-style benchmark failures](https://github.com/ketip/matcha) on chart understanding |
| **OCR Confidence Miscalibration** | High confidence on low-quality scans; false positives in noisy images | Existing in document-processing, extend to pure-vision domain |
| **Text-Image Mismatch** | Document text differs from image (e.g., caption vs. photo label) | [Text-Image alignment failures in VLMs](https://arxiv.org/abs/2405.10603) |
| **Fine-Grained Distinction Failure** | Can't distinguish similar objects (breed confusion, product variants) | [Fine-grained classification limits in VLMs](https://arxiv.org/abs/2402.09508) |
| **Temporal Reasoning Across Frames** | Video agents fail to track object persistence, motion direction | [Temporal reasoning in video understanding, arXiv 2402.03287](https://arxiv.org/abs/2402.03287) |
| **NSFW/Sensitive Content Blindness** | Vision model fails to flag inappropriate content | Known issue in production content moderation (OpenAI, Meta incident reports) |
| **Lighting/Color Shift Sensitivity** | Same object unrecognizable under different lighting | [Domain adaptation in vision, ECCV 2023 work](https://arxiv.org/abs/2307.00934) |
| **Depth Estimation Errors** | Misestimated distances lead to wrong actions (e.g., robot collision) | [Monocular depth estimation failures](https://arxiv.org/abs/2403.03048) |
| **Perspective/Angle Confusion** | Object unrecognized when rotated or viewed at unusual angle | [Robustness to viewpoint changes in VLMs](https://arxiv.org/abs/2404.12033) |
| **Image Compression Artifacts** | JPEG compression, low resolution destroy detail; model confident on corrupted input | Production issue: JPEG-compressed images from mobile uploads |

---

## Reasoning & Chain-of-Thought (14 candidates)

New class of failures as o1/o3-style extended reasoning becomes standard.

| Pattern | Root Cause | Research Sources |
|---|---|---|
| **Reasoning Search Space Explosion** | Agent reasoning expands unboundedly; token limit exceeded mid-thought | Known issue with o1-preview: unlimited token generation without output control |
| **Reasoning Overconfidence** | Chain-of-thought steps are convincing but downstream check fails | [Chain-of-thought faithfulness, arXiv 2305.12383](https://arxiv.org/abs/2305.12383) |
| **Circular Reasoning Loops** | Agent reasons in circles, doesn't converge to conclusion | Happens in test-time compute models when search continues past solution |
| **Reasoning-Action Mismatch** | Reasoning concludes one thing, but action implements differently | Semantic gap between intermediate reasoning and final action selection |
| **Intermediate Step Hallucination** | False assumptions injected mid-reasoning, cascade to wrong conclusion | "Playing with fire" problem in chain-of-thought reasoning |
| **Backtracking Confusion** | Agent correctly identifies reasoning error but fails to correct execution | Model recognizes mistake but can't roll back earlier steps |
| **Context Loss in Reasoning** | Early reasoning context forgotten by final step (long reasoning chains) | Attention degradation over very long reasoning sequences |
| **Reasoning Irreproducibility** | Same query produces different reasoning paths, different conclusions | Sampling variation in reasoning models without deterministic mode |
| **Over-Specification Errors** | Reasoning over-constrained by early assumptions, misses simpler solutions | Agent commits too early to wrong hypothesis during exploration |
| **Reasoning Latency Unpredictability** | Some queries 2s, others 60s; SLA breaches from reasoning variance | Known issue with o1-style models: reasoning time highly variable |
| **Token Overflow in Intermediate Steps** | Intermediate reasoning token counts spike unexpectedly | Particularly with function calls within reasoning loops |
| **Reasoning Contradiction Resolution** | Multiple valid reasoning paths lead to different answers; no consensus mechanism | Multi-path exploration without tie-breaking |
| **Proof-Verification Mismatch** | Agent produces reasoning that *looks* valid but check fails | Similar to hallucination but in reasoning format, not output |
| **Reasoning Cascade Failure** | Error in step N cascades through steps N+1...M with exponential growth | Long chains with no error-checking intermediate |

---

## Long-Horizon Planning & Execution (12 candidates)

Autonomous agents running for hours/days face compounding errors.

| Pattern | Root Cause | Research Sources |
|---|---|---|
| **World State Divergence** | Agent's model of world diverges from reality; subsequent actions fail | Classic robotics problem; now relevant to software agents |
| **Goal Memory Loss** | Original objective forgotten after many turns/loops | Context truncation forces dropping goal statement |
| **Cascading Error Amplification** | Small errors in step N+1 amplify exponentially through step M | Hallucination + mistrust in output → wrong next input |
| **Resource Exhaustion** | Agent loops burn through rate limits, token budgets, API quotas | Underestimated loop cost; no budget tracking |
| **State Inconsistency Across Turns** | Agent makes assumption in turn 5 contradicted in turn 15 | Lack of cross-turn validation |
| **Plan-Reality Gap** | Initial plan assumes conditions that no longer hold mid-execution | Assumption invalidation not detected |
| **Autonomous Loop Runaway** | Agent's termination condition never met; infinite loop | Edge case in stop condition (off-by-one, wrong comparison operator) |
| **Cross-Module Coordination Failure** | Multiple sub-agents (e.g., planner + executor) diverge in understanding | Agent A assumes B will do X; B assumes A already did it |
| **Dependency Chain Breakage** | Success of step N depends on successful completion of N-1; one failure stalls all | No rollback or rerouting |
| **Long-Horizon Hallucination Compounding** | Hallucination in step 2 propagates through steps 3-20, undetected | No intermediate ground-truth checks |
| **Reward Hacking in Long Horizons** | Agent optimizes for reward proxy (e.g., fast completion) at expense of goal (e.g., correctness) | Happens when primary goal too hard to measure over long horizon |
| **Time-Sensitive Action Windows** | Agent misses deadline for time-sensitive action (e.g., API cutoff, business hours) | No deadline tracking in agentic loops |

---

## Streaming & Real-Time Agentic Workflows (11 candidates)

New failure class as agents move from batch to continuous execution.

| Pattern | Root Cause | Research Sources |
|---|---|---|
| **Streaming Interruption Recovery** | Connection drops mid-token-stream; agent state corrupted | Real-time agent inference via WebSocket/streaming API |
| **Real-Time Decision Consistency** | Low latency demands sacrifice accuracy; inconsistent decisions | Time pressure forces early stopping in reasoning |
| **Token Limit During Streaming** | Context window filled mid-stream; truncation mid-response | Streaming context grows faster than batch; no early stopping |
| **State Coherence in Streaming** | Partial outputs committed to state before full response arrives | Race condition: agent acts on incomplete reasoning |
| **Backpressure Mishandling** | Agent produces outputs faster than consumer can handle | Buffer overflow, dropped events |
| **Streaming Latency Tail Risk** | 99th percentile streaming latency unacceptable for SLA | Outliers in model inference, network jitter compound |
| **Realtime-Batch Inference Mismatch** | Streaming model different from batch model; outputs diverge | Different serving stack (vLLM vs batched inference) |
| **Streaming Context Window Boundary Artifacts** | Artifacts at chunk boundaries in streaming mode | Streaming tokenizer boundaries differ from batch |
| **Concurrent Request Race Conditions** | Multiple streaming requests interfere; state mangled | Agent state not thread-safe for concurrent streaming |
| **Streaming Token Counting Accuracy** | Actual tokens differ from estimated in streaming context | Streaming token overhead (delimiters) underestimated |
| **Real-Time Model Staleness** | Model deployed with stale knowledge during streaming session | Model swap happens mid-stream, agent state becomes inconsistent |

---

## Financial Services (14 candidates)

Vertical-specific failures: trading, portfolio management, compliance.

| Pattern | Root Cause | Research Sources |
|---|---|---|
| **Market Data Staleness** | Agent uses outdated prices; recommendation misses market moves | Streaming data lag, cache not invalidated after cutoff time |
| **Portfolio Concentration Blindness** | Agent doesn't aggregate holdings across accounts; violates concentration limits | Lack of cross-account state aggregation |
| **Backtest-Reality Divergence** | Strategy outperforms in backtest but loses in live trading | [Backtest overfitting, academic research on strategy robustness](https://ssrn.com/abstract=1586507) |
| **Regulatory Threshold Misses** | Agent violates risk limits (Value-at-Risk, leverage, sector cap) | Rule missing or misconfigured; no real-time compliance check |
| **Approval Bypass** | Agent executes trades without required human/system approval | Escalation logic broken; trade goes through pre-approval |
| **Multi-Currency Conversion Errors** | Incorrect FX rates applied; losses hidden in currency mismatch | Stale FX data, rate rounding errors |
| **Dividend/Corporate Action Misses** | Agent forgets to account for splits, dividends, mergers | Corporate action feed lag or parsing failure |
| **Settlement Failure Handling** | Agent assumes settlement succeeds; doesn't handle failure gracefully | No acknowledgment of settlement; position state diverges |
| **Liquidity Misjudgment** | Agent assumes asset is liquid; tries to sell illiquid position at market price | No bid-ask spread modeling; slippage unaccounted |
| **Tax-Loss Harvesting Blindness** | Agent misses wash-sale rule violations or duplicate harvest opportunities | Lack of integrated tax tracking |
| **Counterparty Risk Blindness** | Agent doesn't track concentration with single counterparty | No aggregation across instruments by counterparty |
| **Volatility Regime Shift Misses** | Agent doesn't adapt strategy when volatility changes sharply | Model assumes stability; sudden vol spike breaks hedges |
| **Compliance Report Generation Errors** | Regulatory report (HMDA, CFTC, FINRA) contains calculation errors | Rounding, aggregation, or time-zone bugs |
| **Historical Rate Lookback Errors** | Agent uses wrong historical rate/price for lookback-dependent rule | Date off-by-one, timezone confusion, market holiday missed |

---

## Healthcare (12 candidates)

Vertical-specific failures: triage, diagnosis, treatment planning.

| Pattern | Root Cause | Research Sources |
|---|---|---|
| **Diagnosis Hallucination** | Agent confidently suggests diagnosis not supported by presented symptoms | Rare disease bias; training data skew toward common diagnoses |
| **Missing Symptom Integration** | Agent ignores low-salience symptom that's actually diagnostic | Attention mismatch; rare presentation of common disease |
| **Outdated Medical Guidance** | Agent recommends outdated treatment (e.g., pre-2020 guideline) | Knowledge cutoff, medical guidance version unknown to agent |
| **Adverse Drug Interaction Misses** | Agent recommends two drugs that interact dangerously | Incomplete drug database, or interaction not in model's training |
| **Contraindication Blindness** | Agent recommends treatment contraindicated by patient condition | Missing or incomplete patient history integration |
| **Dosage Calculation Error** | Agent calculates wrong dose based on age/weight/renal function | Math error in dose formula, or formula version mismatch |
| **Allergy/Intolerance Override** | Agent ignores documented allergy or assumes tolerance | State reconciliation failure; allergy info lost mid-workflow |
| **Lab Value Misinterpretation** | Agent misinterprets lab units (e.g., mg/dL vs mmol/L) | No unit normalization; reference range context missing |
| **Clinical Guideline Misapplication** | Agent misapplies guideline (e.g., wrong branching logic) | Guideline too complex; agent oversimplifies decision tree |
| **Triage Acuity Misclassification** | Agent downgrades acuity of urgent case; patient waits too long | False-negative error in triage classifier |
| **Pediatric/Geriatric Dose Misadjustment** | Agent fails to account for age-specific dosing rules | Dose calculated for adult; pediatric/geriatric adjustment missing |
| **Liability/Malpractice Exposure** | Agent makes recommendation that increases liability if it goes wrong | No consideration of risk management, defensive medicine |

---

## Legal/Contract Analysis (10 candidates)

Vertical-specific failures: document review, compliance, risk flagging.

| Pattern | Root Cause | Research Sources |
|---|---|---|
| **Jurisdiction Mismatch** | Agent applies law from wrong jurisdiction (e.g., NY law to CA contract) | No jurisdiction detection or field parsing error |
| **Outdated Case Law Reliance** | Agent cites precedent overturned by recent ruling | Knowledge cutoff; recent judicial decisions unknown to model |
| **Liability Clause Blindness** | Agent misses or misinterprets limitation of liability clause | Complex clause structure; agent only flags obvious patterns |
| **Multi-Party Obligation Tracking** | Agent loses track of which party is responsible for which obligation | No entity-relationship tracking across document |
| **Regulatory Version Mismatch** | Agent references outdated regulatory version (e.g., pre-update rule) | Regulatory database not current; effective date not parsed |
| **Statute of Limitations Miss** | Agent doesn't flag breach outside statute of limitations | Time calculation error; claim might be barred |
| **Severability Clause Impact** | Agent doesn't understand impact of severability clause on enforceability | Structural understanding of legal document weak |
| **Conflict-of-Law Analysis Failure** | Agent misses choice-of-law clause that changes which law applies | Clause buried or unusual phrasing; not detected |
| **Indemnification Asymmetry** | Agent misses one-sided indemnification clause favoring one party | Asymmetry not quantified; risk assessment incomplete |
| **Cross-Document Consistency Failure** | Agent flags inconsistency between documents but doesn't reconcile | Contradictions noted but not resolved; ambiguity remains |

---

## E-Commerce & Retail (13 candidates)

Product recommendation, search, inventory, pricing, and fraud prevention in retail.

| Pattern | Root Cause | Research Sources |
|---|---|---|
| **Recommendation Diversity Collapse** | Agent recommends same items repeatedly; lacks diversity | Cold-start problem in recommender systems; filter bubble in collaborative filtering |
| **Price Sensitivity Miscalibration** | Agent sets prices that destroy margin or alienate customers | Elasticity model outdated; competitor pricing not tracked |
| **Inventory Cascade Failure** | Agent allocates stock; downstream inventory counts diverge | No transactional consistency across allocations |
| **Search Relevance Drift** | Query matches wrong products over time; index stale | Search index lag behind product catalog updates |
| **Stock-Out Prediction Miss** | Agent fails to predict and prevent stockouts | Demand forecast model lag; supplier delivery variance |
| **Cross-Border Tax Calculation Error** | Wrong tax applied; customer charged incorrectly | Jurisdiction rules complex; exemption logic missing |
| **Cart Abandonment Misattribution** | Agent blames wrong reason; wrong retargeting | Attribution model doesn't capture true friction |
| **Fraud Detection False Positive** | Legitimate transaction blocked as fraud; customer angry | Fraud classifier overtrained on historical patterns |
| **Personalization Privacy Violation** | Agent reveals sensitive purchase history; privacy breach | Insufficient data isolation; PII in recommendations |
| **Seasonal Demand Blindness** | Agent doesn't adapt to holidays, weather, events | Seasonal model not updated annually |
| **Return Rate Miscalculation** | Agent underestimates returns; inventory planning fails | Return rate model assumes stable patterns |
| **Bundle Recommendation Failure** | Recommended bundles don't sell; cannibalization | Bundle economics not modeled correctly |
| **Markdown Timing Errors** | Agent marks down too late or too early; margin lost | Demand forecast error; competitive price lag |

**Total: 13 candidates → ~45 patterns**

---

## Supply Chain & Logistics (12 candidates)

Route optimization, inventory management, demand forecasting, supplier coordination.

| Pattern | Root Cause | Research Sources |
|---|---|---|
| **Route Optimization Divergence** | Calculated route vs. real-world conditions; detours | Traffic data stale; weather not factored; construction missed |
| **Inventory Bullwhip Amplification** | Small upstream demand variation causes massive downstream swings | Lack of information sharing; lead time mismatches |
| **Demand Forecast Whiplash** | Forecast changes drastically turn-to-turn; upstream chaos | Noise treated as signal; overreaction to recent data |
| **Supplier SLA Blindness** | Agent assumes reliability; supplier frequently misses | No tracking of supplier performance history |
| **Safety Stock Miscalculation** | Stockouts despite safety stock; or excess inventory | Lead time variability not accounted for |
| **Cross-Warehouse Coordination Failure** | Agents at warehouse A and B both hold inventory; inefficiency | No global inventory visibility |
| **Carrier Capacity Mismatch** | Agent books shipment; carrier capacity actually full | Real-time capacity not checked; overbooking |
| **Customs Clearance Delay Blindness** | Agent doesn't account for regulatory delays | Customs time treated as transit time |
| **Order Consolidation Suboptimality** | Agent consolidates orders inefficiently; higher costs | Consolidation logic greedy/myopic |
| **Perishable Goods Spoilage Miss** | Agent ships item; spoilage in transit ruins shipment | Shelf life not tracked per batch/SKU |
| **Reverse Logistics Complexity** | Returns processing fails; refund delays, restocking errors | Reverse chain designed separately from forward |
| **Geographic Demand Shift Lag** | Agent ships to historic high-demand areas; demand has moved | No real-time geo-demand tracking |

**Total: 12 candidates → ~40 patterns**

---

## HR & Recruiting (11 candidates)

Resume screening, candidate matching, offer generation, onboarding automation.

| Pattern | Root Cause | Research Sources |
|---|---|---|
| **Resume Screening Bias** | Agent rejects qualified candidates due to demographic bias in training | Training data imbalance; proxy variable bias |
| **Skill Mismatch Hallucination** | Agent claims candidate has skill not actually on resume | Over-inference from keywords; semantic drift |
| **Experience Level Miscalibration** | Agent grades seniority wrong; hires overqualified/underqualified | Experience metrics conflated (years ≠ skill) |
| **Offer Generation Compression** | Agent generates offer below market rate; candidate rejects | Compensation model doesn't match market data |
| **Diversity Goal Blindness** | Agent ignores diversity hiring goals; homogeneous candidate pool | Fairness constraints not encoded |
| **Reference Check Bypass** | Agent approves without contacting references; hire fails | Reference checking step skipped |
| **Background Check Data Staleness** | Agent uses stale background info; misses recent incidents | Background data not refreshed regularly |
| **Job Matching Overconfidence** | Agent matches candidate to wrong role confidently | Job description too vague or candidate profile incomplete |
| **Onboarding Task Bottleneck** | Agent creates onboarding tasks faster than HR can process | No queue management; bottleneck undetected |
| **Retention Risk Blindness** | Agent doesn't flag candidates likely to leave | Turnover risk model missing tenure predictors |
| **Compensation Equity Miss** | Agent generates offer inconsistent with internal equity | Salary band logic missing or misconfigured |

**Total: 11 candidates → ~38 patterns**

---

## Sales & CRM (11 candidates)

Lead scoring, opportunity forecasting, sales pipeline management, deal closure prediction.

| Pattern | Root Cause | Research Sources |
|---|---|---|
| **Lead Scoring Decay** | Old model; scoring doesn't adapt to market changes | Model not retrained; feature importance stale |
| **Opportunity Forecasting Overconfidence** | Agent predicts close rates too high; deals slip | Historical bias; doesn't account for current blockers |
| **Pipeline Inflation** | Agent counts unqualified leads as opportunities; forecast wrong | Qualification rules too lenient or missing |
| **Discount Authorization Bypass** | Agent approves discount larger than policy allows | Authorization threshold misconfigured |
| **Deal Velocity Miscalculation** | Agent assumes same deal cycle; actually much longer | Deal type complexity not segmented |
| **Competitor Intelligence Lag** | Agent doesn't know about competitive threat; loses deal | Competitive data not real-time |
| **Customer Health Score Misses** | Agent doesn't flag at-risk accounts; surprise churn | Health score model missing key signals |
| **Territory Assignment Mismatch** | Agent assigns lead to wrong sales rep; rep never contacts | Territory rules outdated or not enforced |
| **Upsell Timing Failure** | Agent suggests upsell too early or too late; rejected | Receptiveness model doesn't account for lifecycle |
| **Win/Loss Analysis Blindness** | Agent doesn't learn from losses; repeats mistakes | Feedback loop broken; no systematic learning |
| **Quota Attainment Gaming** | Agent manipulates pipeline to hit quota artificially | Incentive misalignment; short-term optimization |

**Total: 11 candidates → ~38 patterns**

---

## Customer Support & Helpdesk (10 candidates)

Ticket routing, knowledge base retrieval, escalation, first-contact resolution.

| Pattern | Root Cause | Research Sources |
|---|---|---|
| **Knowledge Base Staleness** | Agent retrieves outdated solution; customer frustrated | KB not updated when product changes |
| **Ticket Misrouting** | Agent routes to wrong team; customer waits for transfer | Routing logic doesn't match skill distribution |
| **Escalation Threshold Miscalibration** | Agent escalates too early/late; SLA misses | Escalation criteria not data-driven |
| **Issue Severity Underestimation** | Agent downgrades critical ticket; customer waits | Severity assessment lacks domain context |
| **First Contact Resolution Overestimate** | Agent claims resolution; customer re-contacts next day | Resolution validation step missing |
| **Language/Dialect Misunderstanding** | Agent misinterprets regional slang, accents, or abbreviations | Training data lacks dialect diversity |
| **Context Loss Across Handoffs** | Ticket transfers but context/history lost | No structured context propagation |
| **Repeat Issue Detection Miss** | Agent doesn't recognize customer is reopening old issue | Ticket history not searched; duplicate proliferation |
| **Solution Hallucination** | Agent provides confident solution not in KB; incorrect | Overgeneralization from similar issues |
| **Privacy Data Exposure** | Agent reveals customer data in chat history or escalation | Sensitive field not masked |

**Total: 10 candidates → ~35 patterns**

---

## Content Generation & Marketing (10 candidates)

Campaign generation, SEO optimization, brand guideline compliance, A/B testing.

| Pattern | Root Cause | Research Sources |
|---|---|---|
| **Brand Voice Drift** | Generated content diverges from brand tone | Brand guidelines not enforced; model overfits to training data |
| **SEO Keyword Stuffing** | Agent optimizes metrics (keyword density) at cost of readability | Metric gaming; quality signal ignored |
| **Trademark/IP Violation** | Agent uses protected terms; legal risk | No IP database; trademark check missing |
| **Factual Hallucination in Marketing** | Agent claims product benefit not supported by evidence | Marketing claims not fact-checked |
| **Audience Segmentation Bias** | Agent generates different content quality for different demographics | Fairness constraints missing |
| **A/B Test Interpretation Error** | Agent draws wrong winner from test; rolls out loser | Statistical rigor missing (p-hacking, optional stopping) |
| **Seasonal Content Misalignment** | Agent generates timeless content when seasonal content needed | Calendar/context awareness missing |
| **Call-to-Action Button Blindness** | Agent generates copy but forgets CTA | Template completeness not validated |
| **Compliance Text Miss** | Agent forgets required legal disclaimers or compliance language | Regulatory checklist not enforced |
| **Plagiarism Detection Bypass** | Agent generates text suspiciously similar to competitor | Uniqueness score not checked |

**Total: 10 candidates → ~35 patterns**

---

## DevOps & Infrastructure (10 candidates)

Auto-scaling decisions, incident response, capacity planning, deployment safety.

| Pattern | Root Cause | Research Sources |
|---|---|---|
| **Auto-Scale Thrashing** | Scaling decisions oscillate; frequent scale-up/down | Scaling thresholds too sensitive; hysteresis missing |
| **Capacity Forecast Underestimation** | Forecast misses spike; service overloaded | Forecast model doesn't capture tail behavior |
| **Incident Severity Miscalibration** | Agent downgrades critical incident; SLA breaches | Incident classification threshold wrong |
| **Cascading Failure Acceleration** | Agent's remediation attempt worsens outage | Circuit-breaker logic not understood |
| **Deployment Rollback Failure** | Agent can't roll back; stuck in bad state | Rollback safety checks not enforced |
| **Resource Quota Exhaustion** | Agent allocates resources; hits hard limit; workload killed | Quota not checked before allocation |
| **Stale Metric Alert** | Agent acts on stale metric; condition already resolved | Metric recency not checked; lag not accounted |
| **Database Migration Lock** | Agent migration acquires lock; queries timeout; cascading impact | Lock timeout not modeled |
| **Secrets Rotation Breakage** | Agent rotates secrets; dependent services don't update | Secret propagation not coordinated |
| **Compliance Configuration Drift** | Agent makes change; violates compliance rule silently | Compliance checker not run before apply |

**Total: 10 candidates → ~35 patterns**

---

## Insurance (9 candidates)

Claim processing, fraud detection, underwriting, policy recommendation.

| Pattern | Root Cause | Research Sources |
|---|---|---|
| **Claim Adjudication Bias** | Agent approves/denies claims differently by demographics | Training data has historical bias |
| **Fraud Detection False Positive** | Agent flags legitimate claim as fraud; customer appeal burden | Fraud classifier too aggressive |
| **Underwriting Risk Miscalculation** | Agent underestimates risk; insures high-risk at low premium | Risk model missing or outdated features |
| **Policy Recommendation Misalignment** | Agent recommends policy mismatch with customer needs | Needs assessment incomplete |
| **Exclusion Clause Blindness** | Agent approves claim that's actually excluded | Exclusion logic not checked |
| **Renewal Rate Gaming** | Agent calculates renewal wrong to hit margin targets | Actuarial fairness not enforced |
| **Claims History Latency** | Agent adjudicates without seeing recent claims | Prior-claims lookup lag |
| **Catastrophe Loss Estimation Failure** | Agent underestimates aggregate loss in natural disaster | Correlation/catastrophe modeling missing |
| **Coverage Limit Violation** | Agent authorizes payout exceeding policy limit | Limit checking step skipped |

**Total: 9 candidates → ~30 patterns**

---

## Updated Summary

| Category | Type | Candidates | Estimated Patterns |
|---|---|---|---|
| Vision & Image Understanding | Capability | 15 | 40 |
| Reasoning & Chain-of-Thought | Capability | 14 | 35 |
| Long-Horizon Planning & Execution | Capability | 12 | 30 |
| Streaming & Real-Time | Capability | 11 | 25 |
| Financial Services | Use-Case | 14 | 50 |
| Healthcare | Use-Case | 12 | 45 |
| Legal/Contract | Use-Case | 10 | 40 |
| **E-Commerce & Retail** | **Use-Case** | **13** | **45** |
| **Supply Chain & Logistics** | **Use-Case** | **12** | **40** |
| **HR & Recruiting** | **Use-Case** | **11** | **38** |
| **Sales & CRM** | **Use-Case** | **11** | **38** |
| **Customer Support & Helpdesk** | **Use-Case** | **10** | **35** |
| **Content Generation & Marketing** | **Use-Case** | **10** | **35** |
| **DevOps & Infrastructure** | **Use-Case** | **10** | **35** |
| **Insurance** | **Use-Case** | **9** | **30** |
| **TOTALS** | — | **182 candidates** | **~571 patterns** |

---

## Next Steps

1. **Prioritize**: Which use-cases are most valuable for your organization?
   - **Must-have** (proceed immediately): Financial, Healthcare, Legal, E-Commerce
   - **High-value** (include this round): Supply Chain, HR, Sales, Support
   - **Future** (defer): Content, DevOps, Insurance
2. **Adjust structure**: Merge or split goals as needed for each domain
3. **Confirm sourcing**: Are research sources and candidate patterns credible?
4. If approved: Proceed to **Step 2 (Phase B)** — create directory structure + goal READMEs for selected categories.
